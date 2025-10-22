from django.urls import path
from django.views.generic import RedirectView
from .views import CustomLoginView, BienvenidaView, RecuperacionView, CustomLogoutView

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False)),  # Redirige / a /login/
    path('login/', CustomLoginView.as_view(), name='login'),
    path('bienvenida/<int:pk>/', BienvenidaView.as_view(), name='bienvenida'),
    path('recuperacion/', RecuperacionView.as_view(), name='recuperacion'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Nueva ruta
]

