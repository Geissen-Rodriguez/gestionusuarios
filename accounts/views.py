from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model, authenticate
from django.urls import reverse_lazy
from .models import RecoveryToken
from .forms import LoginForm, RecuperacionForm

import random

User = get_user_model()

# Vista de login con bloqueo por intentos fallidos
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('bienvenida', kwargs={'pk': self.request.user.pk})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()

        if user:
            if user.bloqueado:
                return render(request, self.template_name, {
                    'form': self.get_form(),
                    'error': 'Tu cuenta está bloqueada.'
                })

            auth_user = authenticate(request, username=username, password=password)
            if auth_user:
                user.intentos_fallidos = 0
                user.save()
                return super().post(request, *args, **kwargs)
            else:
                user.intentos_fallidos += 1
                if user.intentos_fallidos >= 3:
                    user.bloqueado = True
                    user.save()
                    return render(request, self.template_name, {
                        'form': self.get_form(),
                        'error': 'Su cuenta ha sido bloqueada despues de 3 intentos fallidos.'
                    })
                user.save()
                return render(request, self.template_name, {
                    'form': self.get_form(),
                    'error': f'Credenciales incorrectas. Le quedan {3 - user.intentos_fallidos} intentos.'
                })

        return render(request, self.template_name, {
            'form': self.get_form(),
            'error': 'Usuario no encontrado.'
        })

# Vista de bienvenida protegida
class BienvenidaView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/bienvenida.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user

# Vista de recuperación de contraseña
class RecuperacionView(FormView):
    template_name = 'accounts/recuperacion.html'
    form_class = RecuperacionForm
    success_url = reverse_lazy('codigo_enviado')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        codigo = ''.join(str(random.randint(0, 9)) for _ in range(6))
        
        # Crear token único
        RecoveryToken.objects.create(
            user=user,
            token=codigo
        )
        
        return render(self.request, 'accounts/codigo_enviado.html', {'codigo': codigo})

# Vista de logout con soporte para GET
class CustomLogoutView(LogoutView):
    next_page = 'login'
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
