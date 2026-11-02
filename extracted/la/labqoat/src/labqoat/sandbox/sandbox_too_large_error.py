"""A request body beyond what the sandbox host accepts."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxTooLargeError(SandboxError):
    """A JSON request reached one mebibyte, or a file exceeded the host's transfer limit."""
