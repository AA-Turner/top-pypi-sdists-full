from abc import ABC, abstractmethod
from pathlib import Path

class IDirectory(ABC):

    @abstractmethod
    def root(self) -> Path:
        """
        Get the root directory of the application.

        Returns
        -------
        Path
            Path object representing the root directory.
        """
        pass

    @abstractmethod
    def app(self) -> Path:
        """
        Get the main application directory.

        Returns
        -------
        Path
            Path object representing the application directory.
        """
        pass

    @abstractmethod
    def console(self) -> Path:
        """
        Get the console directory.

        Returns
        -------
        Path
            Path object representing the console directory.
        """
        pass

    @abstractmethod
    def exceptions(self) -> Path:
        """
        Get the exceptions directory.

        Returns
        -------
        Path
            Path object representing the exceptions directory.
        """
        pass

    @abstractmethod
    def http(self) -> Path:
        """
        Get the HTTP directory.

        Returns
        -------
        Path
            Path object representing the HTTP directory.
        """
        pass

    @abstractmethod
    def models(self) -> Path:
        """
        Get the models directory.

        Returns
        -------
        Path
            Path object representing the models directory.
        """
        pass

    @abstractmethod
    def providers(self) -> Path:
        """
        Get the providers directory.

        Returns
        -------
        Path
            Path object representing the providers directory.
        """
        pass

    @abstractmethod
    def notifications(self) -> Path:
        """
        Get the notifications directory.

        Returns
        -------
        Path
            Path object representing the notifications directory.
        """
        pass

    @abstractmethod
    def services(self) -> Path:
        """
        Get the services directory.

        Returns
        -------
        Path
            Path object representing the services directory.
        """
        pass

    @abstractmethod
    def jobs(self) -> Path:
        """
        Get the jobs directory.

        Returns
        -------
        Path
            Path object representing the jobs directory.
        """
        pass

    @abstractmethod
    def bootstrap(self) -> Path:
        """
        Get the bootstrap directory.

        Returns
        -------
        Path
            Path object representing the bootstrap directory.
        """
        pass

    @abstractmethod
    def config(self) -> Path:
        """
        Get the configuration directory.

        Returns
        -------
        Path
            Path object representing the configuration directory.
        """
        pass

    @abstractmethod
    def database(self) -> Path:
        """
        Get the database directory.

        Returns
        -------
        Path
            Path object representing the database directory.
        """
        pass

    @abstractmethod
    def resources(self) -> Path:
        """
        Get the resources directory.

        Returns
        -------
        Path
            Path object representing the resources directory.
        """
        pass

    @abstractmethod
    def routes(self) -> Path:
        """
        Get the routes directory.

        Returns
        -------
        Path
            Path object representing the routes directory.
        """
        pass

    @abstractmethod
    def storage(self) -> Path:
        """
        Get the storage directory.

        Returns
        -------
        Path
            Path object representing the storage directory.
        """
        pass

    @abstractmethod
    def tests(self) -> Path:
        """
        Get the tests directory.

        Returns
        -------
        Path
            Path object representing the tests directory.
        """
        pass