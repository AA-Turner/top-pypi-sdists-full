"""A file the sandbox could not store."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxWriteError(SandboxError):
    """The sandbox accepted the request but could not write the file at the requested path."""
