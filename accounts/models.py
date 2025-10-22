from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)
    usuario = models.CharField(max_length=30, unique=True)
    contraseña = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre
