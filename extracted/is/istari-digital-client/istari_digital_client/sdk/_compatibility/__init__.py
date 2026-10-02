"""Platform compatibility internals."""

from istari_digital_client.sdk._compatibility.checker import CompatibilityChecker, CompatibilityResult

try:
    from istari_digital_client.sdk._compatibility._api_hashes import API_HASHES
except ImportError:
    API_HASHES: dict[str, str] = {}  # type: ignore[no-redef]

__all__ = ["API_HASHES", "CompatibilityChecker", "CompatibilityResult"]
