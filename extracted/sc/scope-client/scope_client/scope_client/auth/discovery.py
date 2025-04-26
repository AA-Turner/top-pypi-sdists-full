from urllib.parse import urlparse

import requests


class ArthurOIDCMetadata:
    def __init__(self, arthur_host: str):
        self.arthur_host = ArthurOIDCMetadata.extract_host(arthur_host)
        self.metadata = None

    @staticmethod
    def extract_host(arthur_host: str) -> str:
        parsed = urlparse(arthur_host, scheme="https")
        if not parsed.netloc:
            raise ValueError("Bad Arthur host configuration, hostname not found")
        return parsed.scheme + "://" + parsed.netloc

    def _well_known_endpoint(self) -> str:
        return (
            self.arthur_host.rstrip("/")
            + "/api/v1/auth/oidc/.well-known/openid-configuration"
        )

    def _fetch_metadata(self) -> None:
        resp = requests.get(self._well_known_endpoint())
        self.metadata = resp.json()

    @property
    def token_endpoint(self) -> str:
        if self.metadata is None:
            self._fetch_metadata()

        return self.metadata["token_endpoint"]

    @property
    def device_authorization_endpoint(self) -> str:
        if self.metadata is None:
            self._fetch_metadata()

        return self.metadata["device_authorization_endpoint"]
