# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<str:tipo>/', views.iniciar_pago, name='iniciar_pago'),
    path('pasarela/respuesta/', views.respuesta_pasarela, name='respuesta_pasarela'),
]
