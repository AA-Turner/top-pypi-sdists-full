"""One short TCP reachability check per public download invocation."""
import socket
import threading
from urllib.parse import urlsplit

from .api import internal_download_url


def _probe_endpoint(url: str, timeout: float) -> bool:
    # Parse the normalized download URL; never send its path or signature.
    address = urlsplit(internal_download_url(url))
    port = address.port or (443 if address.scheme == 'https' else 80)
    try:
        connection = socket.create_connection((address.hostname, port), timeout=timeout)
        connection.close()
        return True
    except OSError:
        return False


class DownloadProbe:
    """Share one result across workers/batches, assuming one OSS endpoint.

    The timeout bounds socket connections, not DNS or all address attempts.
    No result survives the owning download/download_many/download_group call.
    """

    def __init__(self, timeout: float):
        self._timeout = min(0.5, timeout)
        self._result = None
        self._lock = threading.Lock()

    @property
    def result(self) -> bool | None:
        return self._result

    def reachable(self, url: str) -> bool:
        # Hold the lock through the probe so concurrent Jobs do not duplicate it.
        with self._lock:
            if self._result is None:
                self._result = _probe_endpoint(url, self._timeout)
            return self._result
