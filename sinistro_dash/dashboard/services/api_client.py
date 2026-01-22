import requests
from django.conf import settings


class APIClient:
    """
    Cliente HTTP centralizado para comunicação com a API FastAPI
    """

    @staticmethod
    def _headers(token: str | None = None, content_type: str | None = "application/json"):
        headers = {}
        if content_type:
            headers["Content-Type"] = content_type
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return headers

    @staticmethod
    def get(endpoint: str, token: str | None = None, params: dict | None = None):
        try:
            return requests.get(
                f"{settings.API_BASE_URL}{endpoint}",
                headers=APIClient._headers(token),
                params=params,
                timeout=10,
            )
        except requests.RequestException as exc:
            raise RuntimeError(f"Erro ao comunicar com a API: {exc}")

    @staticmethod
    def post(
        endpoint: str,
        token: str | None = None,
        data: dict | None = None,
        files: dict | None = None,
    ):
        try:
            return requests.post(
                f"{settings.API_BASE_URL}{endpoint}",
                headers=APIClient._headers(token),
                json=data,
                files=files,
                timeout=10,
            )
        except requests.RequestException as exc:
            raise RuntimeError(f"Erro ao comunicar com a API: {exc}")

    @staticmethod
    def post_form(endpoint: str, data: dict):
        """
        Usado para OAuth2 Password Flow (/auth/login)
        Envia application/x-www-form-urlencoded
        """
        try:
            return requests.post(
                f"{settings.API_BASE_URL}{endpoint}",
                data=data,  # FORM!
                headers=APIClient._headers(content_type=None),
                timeout=10,
            )
        except requests.RequestException as exc:
            raise RuntimeError(f"Erro ao comunicar com a API: {exc}")
