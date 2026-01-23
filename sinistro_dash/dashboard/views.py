from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from datetime import date

from .services.sinistro_service import SinistroService
from .services.auth_service import AuthService
from .services.user_service import UserService
from .decorators import api_login_required


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

    token = request.session.get("api_token")
    print("📊 OVERVIEW — token recebido:", token)

    mapa = SinistroService.list_mapa(token)
    print("🗺 MAPA:", mapa)

    data_api = SinistroService.list(token, params={})
    print("📦 DATA_API:", data_api)

    total = data_api.get("total", 0)
    items = data_api.get("items", [])

    hoje = date.today().isoformat()

    today_count = sum(
        1 for s in items
        if s["data_hora"].startswith(hoje)
    )

    mes_atual = hoje[:7]
    month_count = sum(
        1 for s in items
        if s["data_hora"].startswith(mes_atual)
    )

    categorias_map = {}
    for s in items:
        cat = s["tipo_principal"]
        categorias_map[cat] = categorias_map.get(cat, 0) + 1

    categorias = [
        {"label": k, "value": v}
        for k, v in categorias_map.items()
    ]

    timeline_map = {}
    for s in items:
        dia = s["data_hora"][:10]
        timeline_map[dia] = timeline_map.get(dia, 0) + 1

    timeline = [
        {"date": k, "value": v}
        for k, v in sorted(timeline_map.items())
    ]

    return render(
        request,
        "dashboard/overview.html",
        {
            "data": {
                "cards": {
                    "total": total,
                    "today": today_count,
                    "month": month_count,
                },
                "categorias": categorias,
                "timeline": timeline,
                "mapa": mapa
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
