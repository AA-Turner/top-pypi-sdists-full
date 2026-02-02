"""httpx compatibility layer"""

try:
    import httpx  # noqa: F401
except ImportError as e:
    err = "httpx is not installed. Please install httpx to use the httpx compatibility layer."
    raise ImportError(err) from e

from .transport import HttpxTransport, SyncHttpxTransport

__all__ = ["HttpxTransport", "SyncHttpxTransport"]
