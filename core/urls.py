from django.urls import path, include
from .views import index, imc, login_view, contato, cadastro_view


urlpatterns = [
    path("", index, name="index"),
    path("contas/", include("django.contrib.auth.urls")),
    path("imc/", imc, name="imc"),
    path("contato/", contato, name="contato"),
    path("login/", login_view, name="login"),
    path("cadastro/", cadastro_view, name="cadastro"),
]
