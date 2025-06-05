from .models import Centro
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from django.views.generic.detail import DetailView
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CentroForm  # lo creamos abajo
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy




def landing_page(request):
    centros = Centro.objects.all()
    return render(request, 'common/landing.html', {'centros': centros})


def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            mensaje_completo = f"""
            Has recibido un nuevo mensaje desde el formulario de contacto:

            Nombre: {nombre}
            Email: {email}
            Mensaje:
            {mensaje}
            """

            send_mail(
                subject='Nuevo mensaje de contacto',
                message=mensaje_completo,
                from_email=settings.EMAIL_HOST_USER,  # Siempre tú
                recipient_list=['jordiruizroman21@gmail.com'],  # Aquí tu correo
                fail_silently=False,
            )

            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('contacto')
    else:
        form = ContactForm()
    return render(request, 'common/contacto.html', {'form': form})


class CentroDetailView(DetailView):
    model = Centro
    template_name = 'common/detalle_centro.html'  # crea este archivo a continuación
    context_object_name = 'centro'

# Vistas de Staff
@staff_member_required
def lista_centros(request):
    centros = Centro.objects.all()
    return render(request, 'common/staff/centros_list.html', {'centros': centros})

@staff_member_required
def editar_centro(request, pk):
    centro = get_object_or_404(Centro, pk=pk)
    if request.method == 'POST':
        form = CentroForm(request.POST, request.FILES, instance=centro)
        if form.is_valid():
            form.save()
            return redirect('staff_lista_centros')
    else:
        form = CentroForm(instance=centro)
    return render(request, 'common/staff/centro_update.html', {'form': form, 'centro': centro})

@staff_member_required
def eliminar_centro(request, pk):
    centro = get_object_or_404(Centro, pk=pk)
    if request.method == 'POST':
        centro.delete()
        return redirect('staff_lista_centros')
    return render(request, 'common/staff/centros_confirm_delete.html', {'centro': centro})

@staff_member_required
def crear_centro(request):
    if request.method == 'POST':
        form = CentroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staff_lista_centros')
    else:
        form = CentroForm()
    return render(request, 'common/staff/centro_create.html', {'form': form})


@staff_member_required
def panel_usuario(request):
    return render(request, 'common/staff/panel_staff.html')