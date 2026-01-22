from .api_client import APIClient


class SinistroService:
    @staticmethod
    def list(token: str, params: dict):
        response = APIClient.get(
            "/sinistros",
            token=token,
            params=params,
        )

        if response.status_code != 200:
            return {"items": [], "total": 0}

        return response.json()
    @staticmethod
    def get_by_id(token: str, sinistro_id: int) -> dict | None:
        response = APIClient.get(
            f"/sinistros/{sinistro_id}",
            token=token,
        )

        if response.status_code != 200:
            return None

        return response.json()
    @staticmethod
    def list(token: str, params: dict):
        response = APIClient.get("/sinistros", token=token, params=params)

        if response.status_code != 200:
            return {"total": 0, "items": []}

        return response.json()

    @staticmethod
    def count(token: str) -> int:
        response = APIClient.get("/sinistros", token=token)

        if response.status_code != 200:
            return 0

        return response.json().get("total", 0)
    
    @staticmethod
    def list_mapa(token: str) -> list:
        response = APIClient.get(
            "/sinistros/mapa",
            token=token
        )
        if response.status_code != 200:
            return []
    
        return response.json()