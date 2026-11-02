"""Sandbox infrastructure that failed or could not be reached."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxUnavailableError(SandboxError):
    """The host, its runtime or an image failed, did not answer, or answered outside the protocol.

    Nothing is known about the command or sandbox the request concerned, so the caller must not treat the
    attempt as a task outcome.
    """
