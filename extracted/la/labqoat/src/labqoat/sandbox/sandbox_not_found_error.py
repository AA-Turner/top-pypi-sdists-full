"""A sandbox or sandbox file that does not exist."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxNotFoundError(SandboxError):
    """The host knows no such sandbox; a file missing from a sandbox it knows raises the file's own subclass."""
