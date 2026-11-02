"""HTTP/1.1 over a local unix socket."""

import http.client
import socket


class UnixConnection(http.client.HTTPConnection):
    """Connect to a socket path instead of a host; the request still names ``host`` in its Host field."""

    def __init__(self, path: str, host: str, timeout: float | None) -> None:
        """Bind the socket path without connecting."""
        super().__init__(host, timeout=timeout)
        self._path = path

    def connect(self) -> None:
        """Open the socket, closing it again if the connection fails."""
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            sock.settimeout(self.timeout)
            sock.connect(self._path)
        except BaseException:
            sock.close()
            raise
        self.sock = sock
