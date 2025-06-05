from django.urls import path
from . import views

urlpatterns = [
    path('cuerpo/', views.pagina_cuerpo, name='pagina_cuerpo'),
    path('progreso/', views.registrar_entrenamiento, name='registrar_entrenamiento'),
    path('estadisticas/', views.estadisticas, name='estadisticas'),

    path('staff/musculos/', views.lista_musculos, name='staff_lista_musculos'),
    path('staff/musculos/nuevo/', views.crear_musculo, name='staff_crear_musculo'),
    path('staff/musculos/<int:pk>/editar/', views.editar_musculo, name='staff_editar_musculo'),
    path('staff/musculos/<int:pk>/eliminar/', views.eliminar_musculo, name='staff_eliminar_musculo'),

    path('staff/ejercicios/', views.lista_ejercicios, name='staff_lista_ejercicios'),
    path('staff/ejercicios/nuevo/', views.crear_ejercicio, name='staff_crear_ejercicio'),
    path('staff/ejercicios/<int:pk>/editar/', views.editar_ejercicio, name='staff_editar_ejercicio'),
    path('staff/ejercicios/<int:pk>/eliminar/', views.eliminar_ejercicio, name='staff_eliminar_ejercicio'),


]