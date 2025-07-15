import requests


class APIClient:
    API_URL = "https://ofc-test-01.tspb.su/test-task/"

    @classmethod
    def fetch_schedule(cls):
        response = requests.get(cls.API_URL)
        response.raise_for_status()
        return response.json()
