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

        # 🔥 DEBUG
        print("LOGIN STATUS:", response.status_code)
        print("LOGIN BODY:", response.text)

        if response.status_code != 200:
            return None

        data = response.json()

        print("LOGIN JSON:", data)

        return data.get("access_token")
