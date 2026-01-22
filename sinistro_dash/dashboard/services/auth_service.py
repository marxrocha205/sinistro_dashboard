from .api_client import APIClient


class AuthService:
    @staticmethod
    def login(username: str, password: str) -> str | None:
        response = APIClient.post_form(
            "/auth/login",
            data={
                "username": username,
                "password": password,
            },
        )

        if response.status_code != 200:
            return None

        return response.json().get("access_token")
