from functools import wraps
from django.shortcuts import redirect


def api_login_required(view_func):

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        token = request.session.get("api_token")

        print("🛡 DECORATOR api_login_required")
        print("➡️ PATH:", request.path)
        print("➡️ METHOD:", request.method)
        print("➡️ SESSION TOKEN:", token)

        if not token:
            print("🚫 SEM TOKEN NA SESSÃO — REDIRECIONANDO LOGIN")
            return redirect("dashboard:login")

        print("✅ TOKEN OK — ACESSO PERMITIDO")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
