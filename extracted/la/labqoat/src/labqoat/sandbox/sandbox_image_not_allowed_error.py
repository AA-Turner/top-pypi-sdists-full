"""An image the sandbox host was not launched with."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxImageNotAllowedError(SandboxError):
    """Sandboxes start only from the prebuilt images their host was launched with."""
