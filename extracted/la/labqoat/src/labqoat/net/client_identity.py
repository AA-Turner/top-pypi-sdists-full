"""Which release of the SDK sent a request."""

from typing import ClassVar

from labqoat import __version__


class ClientIdentity:
    """Name the SDK release on every request, so a platform can tell a client too old for it what to install."""

    HEADERS: ClassVar[dict[str, str]] = {"User-Agent": f"labqoat-python/{__version__}"}
