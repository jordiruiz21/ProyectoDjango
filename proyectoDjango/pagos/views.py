
# Create your views here.

from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def iniciar_pago(request, tipo):
    suscripciones = {
        "basico": 45,  
        "estandar": 50,   
        "premium": 60,   
    }
    if tipo not in suscripciones:
        return redirect('pagina_error')

    context = {
        "tipo": tipo,
        "importe": suscripciones[tipo],
        "pedido_id": f"ORD{timezone.now().strftime('%Y%m%d%H%M%S')}",
        "url_respuesta": "/pasarela/respuesta/"  # redirige a tu propia lógica
    }
    return render(request, "pagos/pasarela_simulada.html", context)

@csrf_exempt
def respuesta_pasarela(request):
    if request.method == "POST":
        resultado = request.POST.get("resultado")
        tipo = request.POST.get("tipo")
        pedido_id = request.POST.get("pedido_id")
        importe = request.POST.get("importe")

        if resultado == "ok":
            # Aquí podrías activar la suscripción en tu modelo
            return render(request, "pagos/pago_exitoso.html", {
                "pedido_id": pedido_id,
                "tipo": tipo,
                "importe": importe
            })
        else:
            return render(request, "pagos/pago_fallido.html", {
                "pedido_id": pedido_id
            })
    return HttpResponse("Método no permitido", status=405)