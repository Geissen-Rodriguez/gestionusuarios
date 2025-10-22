from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.contrib.auth import get_user_model, logout
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib.auth.views import LogoutView

import random

# Create your views here.

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('bienvenida', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        # After successful authentication, check if user is blocked
        response = super().form_valid(form)
        user = self.request.user
        if getattr(user, 'bloqueado', False):
            logout(self.request)
            # Render login again with an error message
            return render(self.request, self.template_name, {'form': form, 'error': 'Cuenta bloqueada.'})
        return response


class BienvenidaView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/bienvenida.html'

    def dispatch(self, request, *args, **kwargs):
        # Ensure the pk in URL matches logged-in user
        try:
            pk = int(kwargs.get('pk', 0))
        except (TypeError, ValueError):
            pk = 0
        if pk != request.user.pk:
            return HttpResponseForbidden("No tienes permiso para ver esta página.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['user'] = self.request.user
        return ctx


class RecuperacionForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')


class RecuperacionView(FormView):
    template_name = 'accounts/recuperacion.html'
    form_class = RecuperacionForm

    def form_valid(self, form):
        # Simulate sending a 6-digit code to the user's email
        codigo = ''.join(str(random.randint(0, 9)) for _ in range(6))
        return render(self.request, 'accounts/codigo_enviado.html', {'codigo': codigo})

class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirige al login después de cerrar sesión
    http_method_names = ['get', 'post']  # Permite tanto GET como POST

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)