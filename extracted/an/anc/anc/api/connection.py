import requests
from typing import Optional, Dict

class Connection:
    def __init__(self, url: str, token: Optional[str] = None):
        self._url = url
        self._token = token
        self._header = {"Authorization": "Bearer " + token} if token else {}
        self._timeout = 120
        self._session = requests.Session()

    def get(self, path: str, *args, **kwargs):
        return self._session.get(self._url + path, *args, **kwargs)

    def post(self, path: str, *args, stream: bool = False, **kwargs):
        response = self._session.post(self._url + path, *args, **kwargs, stream=stream)
        return response

    def patch(self, path: str, *args, **kwargs):
        return self._session.patch(self._url + path, *args, **self._safe_add(kwargs))

    def put(self, path: str, *args, **kwargs):
        return self._session.put(self._url + path, *args, **self._safe_add(kwargs))

    def delete(self, path: str, *args, **kwargs):
        return self._session.delete(self._url + path, *args, **self._safe_add(kwargs))

    def head(self, path: str, *args, **kwargs):
        return self._session.head(self._url + path, *args, **self._safe_add(kwargs))
