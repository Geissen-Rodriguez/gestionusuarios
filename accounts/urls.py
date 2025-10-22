from django.urls import path
from .views import CustomLoginView, BienvenidaView, RecuperacionView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('bienvenida/<int:pk>/', BienvenidaView.as_view(), name='bienvenida'),
    path('recuperacion/', RecuperacionView.as_view(), name='recuperacion'),
]
