from django.contrib import admin
from .models import Musculo, Ejercicio, Entrenamiento, Serie


class SerieInline(admin.TabularInline):
    model = Serie
    extra = 0  # No series adicionales vacías
    readonly_fields = ('peso_levantado', 'repeticiones')  # Opcional

class EntrenamientoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ejercicio', 'fecha')
    list_filter = ('usuario', 'ejercicio', 'fecha')
    inlines = [SerieInline]
    
admin.site.register(Musculo)
admin.site.register(Ejercicio)
admin.site.register(Entrenamiento, EntrenamientoAdmin)
