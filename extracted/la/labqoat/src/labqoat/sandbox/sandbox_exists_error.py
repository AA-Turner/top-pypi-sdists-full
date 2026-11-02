"""A sandbox identifier that is already taken."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxExistsError(SandboxError):
    """The host already runs a sandbox with the requested identifier."""
