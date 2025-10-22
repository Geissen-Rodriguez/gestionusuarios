from django.contrib.auth.models import AbstractUser
from django.db import models

CARGOS_VALIDOS = [
    ('medico', 'Médico'),
    ('matron', 'Matron/a'),
    ('enfermero', 'Enfermero/a'),
    ('administrativo', 'Administrativo'),
]

class Usuario(AbstractUser):
    cargo = models.CharField(max_length=20, choices=CARGOS_VALIDOS)
    intentos_fallidos = models.IntegerField(default=0)
    bloqueado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_cargo_display()})"

