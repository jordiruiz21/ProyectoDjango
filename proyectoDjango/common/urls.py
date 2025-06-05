from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('contacto/', views.contacto, name='contacto'),
    path('centro/<int:pk>/', views.CentroDetailView.as_view(), name='detalle_centro'),
    path('staff/centros/', views.lista_centros, name='staff_lista_centros'),
    path('staff/centros/<int:pk>/editar/', views.editar_centro, name='staff_editar_centro'),
    path('staff/centros/<int:pk>/eliminar/', views.eliminar_centro, name='staff_eliminar_centro'),
    path('staff/centros/nuevo/', views.crear_centro, name='staff_crear_centro'),
    path('panel/', views.panel_usuario, name='panel_administracion'),



]