import os
from urllib.parse import urlencode


class MPDSOAuthRepository:
    def __init__(self, api_url: str = None):
        self.api_url = (
            api_url or f"{os.getenv('API_URL', 'http://localhost:8000').rstrip('/')}/api/v1"
        )

    def generate_auth_url(self, redirect_url: str = None) -> str:
        params = {}
        if redirect_url:
            params["redirect"] = redirect_url
        query_string = f"?{urlencode(params)}" if params else ""
        return f"{self.api_url}/auth/mpds{query_string}"
