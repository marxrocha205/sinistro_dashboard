from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("health/", views.health_check),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("usuarios/", views.usuarios_view, name="usuarios"),
    path("usuarios/novo/", views.usuario_create_view, name="usuario_create"),
    path("sinistros/", views.sinistros_view, name="sinistros"),
    path(
        "sinistros/<int:sinistro_id>/",
        views.sinistro_detail_view,
        name="sinistro_detail",
    ),
    path("", views.overview_view, name="overview"),
]
