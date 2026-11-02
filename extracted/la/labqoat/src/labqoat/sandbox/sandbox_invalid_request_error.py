"""A request the sandbox host refused to act on as written."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxInvalidRequestError(SandboxError):
    """The host rejected an identifier, path, environment name, user, timeout or other request field."""
