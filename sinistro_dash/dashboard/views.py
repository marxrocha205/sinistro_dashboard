from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from datetime import date
from django.urls import reverse

from sinistro_dash.dashboard.services.dashboard_service import DashboardService

from .services.sinistro_service import SinistroService
from .services.auth_service import AuthService
from .services.user_service import UserService
from .decorators import api_login_required


print("📂 views.py CARREGADO")
def health_check(request):
    return HttpResponse("Dashboard OK")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        token = AuthService.login(username, password)

        if token:
            print("✅ DASH LOGIN OK — token salvo:", token[:25])
            request.session["api_token"] = token
            print("🚀 REDIRECT PARA OVERVIEW")
            print("SESSION:", request.session.items())
            return redirect("dashboard:overview")

        print("❌ DASH LOGIN FALHOU")
        messages.error(request, "Usuário ou senha inválidos")

    return render(request, "dashboard/login.html")


def logout_view(request):
    print("🚪 LOGOUT — limpando sessão")
    request.session.flush()
    return redirect("dashboard:login")


# ================================
# DASHBOARD / OVERVIEW
# ================================
@api_login_required
def overview_view(request):
    print("🔥 OVERVIEW VIEW CHAMADA")

    token = request.session.get("api_token")
    print("📊 TOKEN:", token)

    # 📊 Dados principais do dashboard
    overview = DashboardService.overview(token)
    if not overview:
        messages.error(request, "Erro ao carregar dados do dashboard")
        return redirect("dashboard:login")

    # 🗺️ Dados do mapa (endpoint próprio)
    mapa = SinistroService.list_mapa(token)

    return render(
        request,
        "dashboard/overview.html",
        {
            "data": {
                **overview,
                "mapa": mapa,
            }
        }
    )


# ================================
# USUÁRIOS
# ================================
@api_login_required
def usuarios_view(request):

    token = request.session.get("api_token")
    print("👤 LIST USERS — token:", token)

    usuarios = UserService.list_users(token)
    print("👥 USERS:", usuarios)

    return render(
        request,
        "dashboard/usuarios.html",
        {"usuarios": usuarios},
    )


@api_login_required
def usuario_create_view(request):

    if request.method == "POST":
        token = request.session.get("api_token")

        print("➕ CREATE USER — token:", token)

        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "perfil": request.POST.get("perfil"),
        }

        print("📨 PAYLOAD:", data)

        success = UserService.create_user(token, data)

        print("RESULT CREATE:", success)

        if success:
            messages.success(request, "Usuário criado com sucesso")
            return redirect("dashboard:usuarios")

        messages.error(request, "Erro ao criar usuário")

    return render(request, "dashboard/usuario_form.html")


# ================================
# SINISTROS
# ================================
@api_login_required
def sinistros_view(request):

    token = request.session.get("api_token")
    print("🚨 LIST SINISTROS — token:", token)

    page = int(request.GET.get("page", 1))
    limit = 10
    skip = (page - 1) * limit

    params = {
        "skip": skip,
        "limit": limit,
        "tipo": request.GET.get("tipo") or None,
    }

    print("PARAMS:", params)

    data = SinistroService.list(token, params)
    print("RESULT:", data)

    total = data["total"]
    sinistros = data["items"]

    total_pages = (total // limit) + (1 if total % limit else 0)

    return render(
        request,
        "dashboard/sinistros.html",
        {
            "sinistros": sinistros,
            "page": page,
            "pages": range(1, total_pages + 1),
            "total_pages": total_pages,
        },
    )


@api_login_required
def sinistro_detail_view(request, sinistro_id: int):

    token = request.session.get("api_token")
    print("🔎 SINISTRO DETAIL — token:", token, "ID:", sinistro_id)

    sinistro = SinistroService.get_by_id(token, sinistro_id)
    print("SINISTRO:", sinistro)

    if not sinistro:
        messages.error(request, "Sinistro não encontrado")
        return redirect("dashboard:sinistros")

    return render(
        request,
        "dashboard/sinistro_detail.html",
        {
            "sinistro": sinistro,
            "API_BASE": settings.API_BASE_URL,
        },
    )
