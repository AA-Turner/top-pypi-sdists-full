"""Something that ran out of time inside a healthy sandbox host."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxTimeoutError(SandboxError):
    """A process ran past its timeout and was killed with everything it started, or a sandbox was not ready in time.

    This is the work's own outcome. A host that stops answering raises ``SandboxUnavailableError`` instead.
    """
