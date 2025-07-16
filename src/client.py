import requests


class APIClient:
    """Client for fetching schedule data from external API."""

    API_URL = "https://ofc-test-01.tspb.su/test-task/"

    @classmethod
    def fetch_schedule(cls):
        """Fetch schedule data from the API."""
        try:
            response = requests.get(cls.API_URL, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ConnectionError(f"ошибка API: {e}")
