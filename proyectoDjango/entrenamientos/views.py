from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EntrenamientoForm, SerieForm, MusculoForm, EjercicioForm
from .models import Entrenamiento, Serie, Musculo, Ejercicio
from django.forms import modelformset_factory
import json
from collections import defaultdict
from statistics import mean
from django.contrib.admin.views.decorators import staff_member_required




@login_required
def registrar_entrenamiento(request):
    num_series = int(request.GET.get('num_series', 3))  
    SerieFormSetCustom = modelformset_factory(Serie, form=SerieForm, extra=num_series)

    if request.method == 'POST':
        entrenamiento_form = EntrenamientoForm(request.POST)
        formset = SerieFormSetCustom(request.POST, queryset=Serie.objects.none())

        if entrenamiento_form.is_valid() and formset.is_valid():
            entrenamiento = entrenamiento_form.save(commit=False)
            entrenamiento.usuario = request.user
            entrenamiento.save()

            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    serie = form.save(commit=False)
                    serie.entrenamiento = entrenamiento
                    serie.save()

            return redirect('registrar_entrenamiento')
    else:
        entrenamiento_form = EntrenamientoForm()
        formset = SerieFormSetCustom(queryset=Serie.objects.none())

    historial = Entrenamiento.objects.filter(usuario=request.user).order_by('-fecha')

    return render(request, 'entrenamientos/registrar_entrenamiento.html', {
        'entrenamiento_form': entrenamiento_form,
        'formset': formset,
        'historial': historial,
        'num_series': num_series
    })

from collections import defaultdict
from statistics import mean

from collections import defaultdict
from statistics import mean
from django.shortcuts import render
from .models import Entrenamiento

def estadisticas(request):
    entrenamientos = Entrenamiento.objects.filter(
        usuario=request.user
    ).select_related('ejercicio').prefetch_related('serie_set').order_by('fecha')

    agrupado = defaultdict(lambda: defaultdict(list))  # { ejercicio: { fecha: [series] } }

    for entrenamiento in entrenamientos:
        fecha_str = entrenamiento.fecha.strftime('%Y-%m-%d')
        for serie in entrenamiento.series:
            agrupado[entrenamiento.ejercicio.nombre][fecha_str].append(serie)

    datos = {}
    mejoras = {}  # { ejercicio: mejora_en_kg }
    frecuencia = defaultdict(int)  # { ejercicio: total_sesiones }
    ejercicio_a_musculo = {}  # { ejercicio: musculo }

    for ejercicio, dias in agrupado.items():
        datos[ejercicio] = []
        pesos_por_fecha = []

        for fecha, series in dias.items():
            pesos = [s.peso_levantado for s in series]
            repes = [s.repeticiones for s in series]
            media_peso = round(mean(pesos), 2)
            media_repes = round(mean(repes), 2)
            total = round(media_peso * media_repes, 2)

            datos[ejercicio].append({
                'fecha': fecha,
                'peso': media_peso,
                'repeticiones': media_repes,
                'total': total,
            })

            pesos_por_fecha.append(media_peso)
            frecuencia[ejercicio] += 1

        if len(pesos_por_fecha) >= 2:
            mejora = round(pesos_por_fecha[-1] - pesos_por_fecha[0], 2)
            mejoras[ejercicio] = mejora

        # Guardar el músculo relacionado
        musculo = next(
            (ent.ejercicio.musculo for ent in entrenamientos if ent.ejercicio.nombre == ejercicio),
            None
        )
        ejercicio_a_musculo[ejercicio] = musculo

    # Mejor ejercicio
    mejor_ejercicio = max(mejoras.items(), key=lambda x: x[1])[0] if mejoras else None
    mejora_ejercicio = mejoras.get(mejor_ejercicio, 0) if mejor_ejercicio else 0

    # Músculo más mejorado
    musculo_mejoras = defaultdict(float)
    for ejercicio, mejora in mejoras.items():
        musculo = ejercicio_a_musculo[ejercicio]
        if musculo:
            musculo_mejoras[musculo] += mejora

    musculo_mas_mejorado = max(musculo_mejoras.items(), key=lambda x: x[1])[0] if musculo_mejoras else None
    mejora_musculo = musculo_mejoras.get(musculo_mas_mejorado, 0) if musculo_mas_mejorado else 0

    # Ejercicio más frecuente
    ejercicio_mas_frecuente = max(frecuencia.items(), key=lambda x: x[1])[0] if frecuencia else None
    frecuencia_ejercicio = frecuencia.get(ejercicio_mas_frecuente, 0)

    context = {
        'datos': datos,
        'mejor_ejercicio': mejor_ejercicio,
        'mejora_ejercicio': mejora_ejercicio,
        'musculo_mas_mejorado': musculo_mas_mejorado,
        'mejora_musculo': mejora_musculo,
        'ejercicio_mas_frecuente': ejercicio_mas_frecuente,
        'frecuencia_ejercicio': frecuencia_ejercicio,
    }

    return render(request, 'entrenamientos/estadisticas.html', context)




def pagina_cuerpo(request):
    return render(request, 'entrenamientos/cuerpo.html')


# Parte privada musculos
@staff_member_required
def lista_musculos(request):
    musculos = Musculo.objects.all()
    return render(request, 'entrenamientos/staff/musculos_list.html', {'musculos': musculos})

@staff_member_required
def crear_musculo(request):
    if request.method == 'POST':
        form = MusculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_lista_musculos')
    else:
        form = MusculoForm()
    return render(request, 'entrenamientos/staff/musculo_create.html', {'form': form})

@staff_member_required
def editar_musculo(request, pk):
    musculo = get_object_or_404(Musculo, pk=pk)
    if request.method == 'POST':
        form = MusculoForm(request.POST, instance=musculo)
        if form.is_valid():
            form.save()
            return redirect('staff_lista_musculos')
    else:
        form = MusculoForm(instance=musculo)
    return render(request, 'entrenamientos/staff/musculo_update.html', {'form': form, 'musculo': musculo})

@staff_member_required
def eliminar_musculo(request, pk):
    musculo = get_object_or_404(Musculo, pk=pk)
    if request.method == 'POST':
        musculo.delete()
        return redirect('staff_lista_musculos')
    return render(request, 'entrenamientos/staff/musculos_confirm_delete.html', {'musculo': musculo})

# Parte privada ejercicios
@staff_member_required
def lista_ejercicios(request):
    ejercicios = Ejercicio.objects.select_related('musculo').all()
    return render(request, 'entrenamientos/staff/ejercicios_list.html', {'ejercicios': ejercicios})

@staff_member_required
def crear_ejercicio(request):
    if request.method == 'POST':
        form = EjercicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_lista_ejercicios')
    else:
        form = EjercicioForm()
    return render(request, 'entrenamientos/staff/ejercicio_create.html', {'form': form})

@staff_member_required
def editar_ejercicio(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    if request.method == 'POST':
        form = EjercicioForm(request.POST, instance=ejercicio)
        if form.is_valid():
            form.save()
            return redirect('staff_lista_ejercicios')
    else:
        form = EjercicioForm(instance=ejercicio)
    return render(request, 'entrenamientos/staff/ejercicio_update.html', {'form': form, 'ejercicio': ejercicio})

@staff_member_required
def eliminar_ejercicio(request, pk):
    ejercicio = get_object_or_404(Ejercicio, pk=pk)
    if request.method == 'POST':
        ejercicio.delete()
        return redirect('staff_lista_ejercicios')
    return render(request, 'entrenamientos/staff/ejercicios_confirm_delete.html', {'ejercicio': ejercicio})