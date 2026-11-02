"""A sandbox the host has no room for."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxCapacityError(SandboxError):
    """The host's sandbox budget is full; the same request can succeed once another sandbox has ended."""
