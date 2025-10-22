from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re

def validate_username_format(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError('El username solo puede contener letras, numeros y guiones bajos.')

def validate_email_domain(value):
    allowed_domains = ['hospital.cl', 'salud.gob.cl']
    domain = value.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError('El email debe ser institucional.')

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

    def clean(self):
        super().clean()
        validate_username_format(self.username)
        if self.email:
            validate_email_domain(self.email)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.get_cargo_display()})"


class RecoveryToken(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='recovery_tokens')
    token = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Token de recuperación'
        verbose_name_plural = 'Tokens de recuperación'

    def __str__(self):
        return f"Token {self.token} para {self.user.username}"

