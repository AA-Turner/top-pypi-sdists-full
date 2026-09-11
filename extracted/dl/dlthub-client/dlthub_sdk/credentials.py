"""How the SDK obtains the control-plane credential, and renews it.

A caller with a static token passes it to :func:`~dlthub_sdk.connect` and needs
none of this. A caller whose credential rotates — the CLI, holding a refresh
token, or a long-lived server — implements :class:`Credentials` instead, so the
SDK keeps owning its HTTP clients.

Conformance is structural, as it is for ``Transport``: do **not** inherit these
protocols. A protocol member's ``...`` body is a concrete method returning
``None``, so a subclass that forgets :meth:`Credentials.refreshed` would inherit
one that silently means "give up" instead of failing. Unrelated to a class, a
missing method is an ``AttributeError`` on first use, and mypy catches it at the
``connect(credentials=...)`` call site either way.

A leaf module: it imports nothing else from the package, and nothing from
``httpx`` crosses it.
"""

from __future__ import annotations

# Python internals
from typing import TYPE_CHECKING, Protocol


class Credentials(Protocol):
    """A control-plane credential the SDK reads before each request.

    Implement this for a credential that changes over the client's life. The
    SDK never stores what :meth:`token` returns, so a rotation takes effect on
    the next request.
    """

    def token(self) -> str:
        """Return the credential to send now.

        Called before every control-plane request, so an implementation that
        renews proactively does it here.

        Returns:
            The bearer token.
        """
        ...

    def refreshed(self) -> str | None:
        """Renew the credential after the platform rejected it.

        Called at most once per request, only for a 401. Returning ``None``
        makes the rejection final and the caller sees ``NotAuthenticated``.

        Returns:
            A token to retry with, or ``None`` to give up.
        """
        ...


class AsyncCredentials(Protocol):
    """The awaited twin of :class:`Credentials`, for ``connect_async``."""

    async def token(self) -> str:
        """Return the credential to send now.

        Returns:
            The bearer token.
        """
        ...

    async def refreshed(self) -> str | None:
        """Renew the credential after the platform rejected it.

        Returns:
            A token to retry with, or ``None`` to give up.
        """
        ...


class _Static:
    """What ``connect(token=...)`` becomes, so there is one credential path.

    Args:
        token: The credential, which never changes.
    """

    def __init__(self, token: str) -> None:
        self._token = token

    def token(self) -> str:
        return self._token

    def refreshed(self) -> str | None:
        # Nothing to renew from: a static token that is rejected stays rejected.
        return None


class _AsyncStatic:
    """The awaited twin of :class:`_Static`.

    Args:
        token: The credential, which never changes.
    """

    def __init__(self, token: str) -> None:
        self._token = token

    async def token(self) -> str:
        return self._token

    async def refreshed(self) -> str | None:
        return None


if TYPE_CHECKING:

    def _statics_match_the_protocols(sync: _Static, asynchronous: _AsyncStatic) -> None:
        """Bind each static credential to its protocol, so drift fails mypy.

        Args:
            sync: The blocking one.
            asynchronous: The awaiting one.
        """
        _sync: Credentials = sync
        _async: AsyncCredentials = asynchronous
        del _sync, _async


__all__ = ["AsyncCredentials", "Credentials"]
