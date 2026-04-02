"""Backwards-compatible re-exports. Prefer ``plato.transports``."""

from plato.transports import (
    NFSTransport,
    RsyncTransport,
    Transport,
    rsync_from,
    rsync_to,
)
from plato.transports import (
    NFSTransport as NFSWorkspace,
)
from plato.transports import (
    RsyncTransport as RsyncWorkspace,
)
from plato.transports import (
    Transport as Workspace,
)

__all__ = [
    "Transport",
    "NFSTransport",
    "RsyncTransport",
    # Backwards-compat aliases
    "Workspace",
    "NFSWorkspace",
    "RsyncWorkspace",
    "rsync_to",
    "rsync_from",
]
