import os
from pathlib import Path
from orionis.services.paths.contracts.resolver import IResolver
from orionis.services.paths.exceptions import (
    OrionisFileNotFoundException,
    OrionisPathValueException
)

class Resolver(IResolver):
    """
    A utility class for resolving file and directory paths relative to the project's root directory.
    """

    def __init__(self, root_path: str = None):
        """
        Initializes the Resolver instance with the project's root directory.

        Parameters
        ----------
        root_path : str, optional
            The root directory of the project. If not provided, it defaults to the current working directory.
        """
        self.base_path = Path(root_path).resolve() if root_path else Path(os.getcwd()).resolve()
        self.resolved_path = None

    def relativePath(self, relative_path: str) -> 'Resolver':
        """
        Resolves a given relative path to an absolute path and validates its existence.

        This method combines the project's root directory with the provided relative path,
        resolves it to an absolute path, and ensures it exists as either a directory or a file.

        Parameters
        ----------
        relative_path : str
            The relative path to a directory or file to be resolved.

        Returns
        -------
        Resolver
            The current instance of the Resolver class with the resolved path.

        Raises
        ------
        OrionisFileNotFoundException
            If the resolved path does not exist.
        OrionisPathValueException
            If the resolved path is neither a valid directory nor a file.
        """
        # Combine the base path with the relative path and resolve it
        resolved_path = (self.base_path / relative_path).resolve()

        # Validate that the path exists
        if not resolved_path.exists():
            raise OrionisFileNotFoundException(f"The requested path does not exist: {resolved_path}")

        # Validate that the path is either a directory or a file
        if not (resolved_path.is_dir() or resolved_path.is_file()):
            raise OrionisPathValueException(f"The requested path is neither a valid directory nor a file: {resolved_path}")

        # Store the resolved path in the instance variable
        self.resolved_path = resolved_path

        # Return the current instance
        return self

    def toString(self) -> str:
        """
        Returns the string representation of the resolved path.

        Returns
        -------
        str
            The resolved path as a string.
        """
        return str(self.resolved_path)

    def get(self) -> Path:
        """
        Returns the resolved path as a Path object.

        Returns
        -------
        Path
            The resolved path.
        """
        return self.resolved_path

    def __str__(self) -> str:
        """
        Returns the string representation of the resolved path.

        Returns
        -------
        str
            The resolved path as a string.
        """
        return str(self.resolved_path)