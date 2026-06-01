"""Module for domain system."""
from shutil import which


class CommandNotFound(Exception):
    """Command not found."""

    def __init__(self, command: str):
        """Initialize."""
        self.command = command
        super().__init__(f"Command '{command}' not found on path.")


class CLIProgram:
    """Program."""

    def __init__(self, name: str, verify_exists_func: callable = which):
        """Initialize."""
        self.name = name
        self.verify_exists_func = verify_exists_func

    def exists(self) -> bool:
        """Verify command line program exists on path."""
        return self.verify_exists_func(self.name) is not None
