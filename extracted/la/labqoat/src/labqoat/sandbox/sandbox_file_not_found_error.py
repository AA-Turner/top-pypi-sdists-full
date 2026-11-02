"""A file a sandbox that exists could not hand over."""

from labqoat.sandbox.sandbox_not_found_error import SandboxNotFoundError


class SandboxFileNotFoundError(SandboxNotFoundError):
    """The sandbox has no readable file at the requested path; the sandbox itself is still there."""
