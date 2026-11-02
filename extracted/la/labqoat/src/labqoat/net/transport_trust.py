"""One verified TLS trust context per trust store for every connection a process opens."""

import http.client
import os
import ssl
from typing import ClassVar


class TransportTrust:
    """Read each trust store once per process instead of once per connection.

    Building a context loads every trusted certificate, about twenty milliseconds on a worker. A process forked
    from the worker template inherits the context the template prepared, so a run pays nothing.
    """

    _context: ClassVar[ssl.SSLContext | None] = None
    _bundled: ClassVar[ssl.SSLContext | None] = None

    @classmethod
    def context(cls) -> ssl.SSLContext:
        """Return the process's verifying context, building it from the system trust store on first use."""
        if cls._context is None:
            cls._context = ssl.create_default_context()
        return cls._context

    @classmethod
    def bundled(cls) -> ssl.SSLContext:
        """Return a verifying context over ``SSL_CERT_FILE`` or ``SSL_CERT_DIR``, else the ``certifi`` bundle.

        A person's machine may run a Python whose system trust store is empty, so clients trust certifi's
        certificates unless the environment names its own: a worker is handed the platform's authority that
        way, and so is a machine behind an inspecting proxy.
        """
        if cls._bundled is None:
            named = os.environ.get("SSL_CERT_FILE") or None, os.environ.get("SSL_CERT_DIR") or None
            if any(named):
                cls._bundled = ssl.create_default_context(cafile=named[0], capath=named[1])
            else:
                import certifi

                cls._bundled = ssl.create_default_context(cafile=certifi.where())
        return cls._bundled

    @classmethod
    def connection(
        cls, scheme: str, host: str, port: int | None, *, timeout: float, blocksize: int = 8192
    ) -> http.client.HTTPConnection:
        """Open a lazy connection of the endpoint's scheme; HTTPS always verifies against the shared context."""
        if scheme == "https":
            return http.client.HTTPSConnection(host, port, timeout=timeout, blocksize=blocksize, context=cls.context())
        return http.client.HTTPConnection(host, port, timeout=timeout, blocksize=blocksize)
