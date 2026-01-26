from .api_client import APIClient


class SinistroService:

    # ===============================
    # LISTAGEM
    # ===============================

    @staticmethod
    def list(token: str, params: dict):
        response = APIClient.get(
            "/sinistros",
            token=token,
            params=params,
        )

        print("🚨 LIST STATUS:", response.status_code)
        print("🚨 LIST BODY:", response.text)

        if response.status_code != 200:
            return {"total": 0, "items": []}

        return response.json()

    # ===============================
    # DETALHE
    # ===============================

    @staticmethod
    def get_by_id(token: str, sinistro_id: int):

        response = APIClient.get(
            f"/sinistros/{sinistro_id}",
            token=token,
        )

        print("🔎 DETAIL STATUS:", response.status_code)
        print("🔎 DETAIL BODY:", response.text)

        if response.status_code != 200:
            return None

        return response.json()

    # ===============================
    # MAPA
    # ===============================

    @staticmethod
    def list_mapa(token: str):

        response = APIClient.get(
            "/sinistros/mapa",
            token=token
        )

        print("🗺 MAPA STATUS:", response.status_code)

        if response.status_code != 200:
            return []

        return response.json()

    # ===============================
    # COUNT
    # ===============================

    @staticmethod
    def count(token: str):

        response = APIClient.get(
            "/sinistros",
            token=token
        )

        print("📊 COUNT STATUS:", response.status_code)

        if response.status_code != 200:
            return 0

        return response.json().get("total", 0)
