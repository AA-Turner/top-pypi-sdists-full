try:
    from . import _pylhasa
except Exception:  # pragma: no cover - native module missing
    _pylhasa = None


if _pylhasa is not None:
    PylhasaError = _pylhasa.PylhasaError
    BadArchiveError = _pylhasa.BadArchiveError
else:
    class PylhasaError(Exception):
        """Base exception for pylhasa."""

    class BadArchiveError(PylhasaError):
        """Raised when an archive is malformed or unsupported."""


class UnsafePathError(PylhasaError):
    """Raised when an entry path is unsafe to extract."""
