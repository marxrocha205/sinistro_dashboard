from .api_client import APIClient


class UserService:
    @staticmethod
    def list_users(token: str):
        response = APIClient.get("/usuarios", token=token)

        if response.status_code != 200:
            return []

        return response.json()

    @staticmethod
    def create_user(token: str, data: dict) -> bool:
        response = APIClient.post(
            "/usuarios",
            token=token,
            data=data,
        )
        return response.status_code == 200