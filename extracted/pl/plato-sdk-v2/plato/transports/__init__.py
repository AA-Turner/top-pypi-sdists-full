"""Workspace transport implementations."""

from plato.transports.base import Transport
from plato.transports.nfs import NFSTransport
from plato.transports.rsync import RsyncTransport, rsync_from, rsync_to
from plato.transports.sshfs import SSHFSTransport

# Lazy imports for GitTransport to avoid requiring gitpython in all environments,
# and for FuseDirectTransport to keep this package init free of import-order
# coupling. Access via `from plato.transports import GitTransport` or the
# submodules directly.


def __getattr__(name: str) -> object:
    if name in ("GitTransport", "GitPushConflict", "GitPublishedRef"):
        from plato.transports import git

        return getattr(git, name)
    if name == "FuseDirectTransport":
        from plato.transports.fuse import FuseDirectTransport

        return FuseDirectTransport
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "Transport",
    "FuseDirectTransport",
    "GitPushConflict",
    "GitPublishedRef",
    "GitTransport",
    "NFSTransport",
    "RsyncTransport",
    "SSHFSTransport",
    "rsync_to",
    "rsync_from",
]
