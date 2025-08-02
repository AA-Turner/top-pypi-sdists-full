from abc import ABC, abstractmethod

class EmbedderBase(ABC):
    """
    Abstract base class for embedding files.

    This class serves as a blueprint for creating various file embedders. 
    Any subclass of EmbedderBase must implement the `embed_file` method.
    """

    @abstractmethod
    def embed_file(self, source_url: str, file_name: str = None):
        """
        Abstract method to embed a file.

        Args:
            source_url (str): The URL of the source file to be embedded.
            file_name (str, optional): The name of the file. Defaults to None.

        Raises:
            NotImplementedError: This method must be overridden in a subclass.
        """
        pass