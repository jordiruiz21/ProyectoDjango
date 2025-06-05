from django.db import models
from django.conf import settings


class Musculo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    musculo = models.ForeignKey(Musculo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Entrenamiento(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.ejercicio} - {self.fecha}"

    @property
    def series(self):
        return self.serie_set.all()
    

class Serie(models.Model):
    entrenamiento = models.ForeignKey(Entrenamiento, on_delete=models.CASCADE)
    repeticiones = models.PositiveIntegerField()
    peso_levantado = models.FloatField()

    def __str__(self):
        return f"{self.peso_levantado} kg x {self.repeticiones}"

