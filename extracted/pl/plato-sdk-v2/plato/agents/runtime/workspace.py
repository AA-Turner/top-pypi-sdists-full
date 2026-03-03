"""Backwards-compatible re-exports. Use plato.agents.runtime.transport instead."""

from plato.agents.runtime.transport import (
    NFSTransport,
    RsyncTransport,
    Transport,
    rsync_from,
    rsync_to,
)
from plato.agents.runtime.transport import (
    NFSTransport as NFSWorkspace,
)
from plato.agents.runtime.transport import (
    RsyncTransport as RsyncWorkspace,
)
from plato.agents.runtime.transport import (
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
