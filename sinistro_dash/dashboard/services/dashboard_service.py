from .api_client import APIClient


class DashboardService:
    @staticmethod
    def overview(token: str):
        response = APIClient.get("/dashboard/overview", token=token)

        if response.status_code != 200:
            return None

        return response.json()
