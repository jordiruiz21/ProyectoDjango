from django.db import models

class Centro(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=15)
    horario = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to="img/", blank=True, null=True)

    def __str__(self):
        return self.nombre
