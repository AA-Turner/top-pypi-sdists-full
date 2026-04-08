"""Workspace transport implementations."""

from plato.transports.base import Transport
from plato.transports.nfs import NFSTransport
from plato.transports.rsync import RsyncTransport, rsync_from, rsync_to
from plato.transports.sshfs import SSHFSTransport

# Lazy imports for GitTransport to avoid requiring gitpython in all environments.
# Access via `from plato.transports import GitTransport` or `from plato.transports.git import ...`.


def __getattr__(name: str) -> object:
    if name in ("GitTransport", "GitPushConflict", "GitPublishedRef"):
        from plato.transports import git

        return getattr(git, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Transport",
    "GitPushConflict",
    "GitPublishedRef",
    "GitTransport",
    "NFSTransport",
    "RsyncTransport",
    "SSHFSTransport",
    "rsync_to",
    "rsync_from",
]
