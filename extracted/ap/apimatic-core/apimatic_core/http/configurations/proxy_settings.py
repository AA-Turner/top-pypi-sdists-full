from typing import Dict, Optional
from urllib.parse import quote


class ProxySettings:
    """
    A simple data model for configuring HTTP(S) proxy settings.
    """

    HTTP_SCHEME: str = "http://"
    HTTPS_SCHEME: str = "https://"

    address: str
    port: Optional[int]
    username: Optional[str]
    password: Optional[str]

    def __init__(self, address: str, port: Optional[int] = None,
                 username: Optional[str] = None, password: Optional[str] = None) -> None:
        """
        Parameters
        ----------
        address : str
            Hostname or IP of the proxy.
        port : int, optional
            Port of the proxy server.
        username : str, optional
            Username for authentication.
        password : str, optional
            Password for authentication.
        """
        self.address = address
        self.port = port
        self.username = username
        self.password = password

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """
        return (
            f"ProxySettings(address={self.address!r}, "
            f"port={self.port!r}, "
            f"username={self.username!r}, "
            f"password={'***' if self.password else None})"
        )

    def __str__(self) -> str:
        """
        Human-friendly string for display/logging.
        """
        user_info = f"{self.username}:***@" if self.username else ""
        port = f":{self.port}" if self.port else ""
        return f"{user_info}{self.address}{port}"

    def _sanitize_address(self) -> str:
        addr = (self.address or "").strip()
        # Trim scheme if present
        if addr.startswith(self.HTTP_SCHEME):
            addr = addr[len(self.HTTP_SCHEME):]
        elif addr.startswith(self.HTTPS_SCHEME):
            addr = addr[len(self.HTTPS_SCHEME):]
        # Drop trailing slash if user typed a URL-like form
        return addr.rstrip("/")

    def to_proxies(self) -> Dict[str, str]:
        """
        Build a `requests`-compatible proxies dictionary.
        """
        host = self._sanitize_address()
        auth = ""
        if self.username is not None:
            # URL-encode in case of special chars
            u = quote(self.username, safe="")
            p = quote(self.password or "", safe="")
            auth = f"{u}:{p}@"
        port = f":{self.port}" if self.port is not None else ""
        return {
            "http": f"{self.HTTP_SCHEME}{auth}{host}{port}",
            "https": f"{self.HTTPS_SCHEME}{auth}{host}{port}",
        }
