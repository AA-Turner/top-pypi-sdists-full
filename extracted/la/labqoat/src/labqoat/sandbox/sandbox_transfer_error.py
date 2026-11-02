"""A directory transfer whose archive command failed inside the sandbox."""

from labqoat.sandbox.sandbox_error import SandboxError


class SandboxTransferError(SandboxError):
    """The sandbox could not pack or unpack a directory, so the tree did not arrive intact."""

    def __init__(self, message: str, exit_code: int, output: str) -> None:
        """Describe the failed archive command and keep its exit code and output for diagnosis."""
        super().__init__(f"{message} (exit code {exit_code}): {output.strip()}")
        self.exit_code = exit_code
        self.output = output
