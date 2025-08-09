from abc import ABC, abstractmethod

class IResolver(ABC):

    @abstractmethod
    def relativePath(self, relative_path: str) -> 'IResolver':
        """
        Resolves a relative path into an absolute one and validates its existence.

        Parameters
        ----------
        relative_path : str
            The relative path to resolve.

        Returns
        -------
        ResolverInterface
            The instance itself for method chaining.

        Raises
        ------
        FileNotFoundError
            If the resolved path does not exist.
        ValueError
            If the resolved path is neither a file nor a directory.
        """
        pass

    @abstractmethod
    def toString(self) -> str:
        """
        Returns the resolved path as a string.

        Returns
        -------
        str
            The resolved path.
        """
        pass

    @abstractmethod
    def get(self):
        """
        Returns the resolved path as a Path object.

        Returns
        -------
        Path
            The resolved path.
        """
        pass