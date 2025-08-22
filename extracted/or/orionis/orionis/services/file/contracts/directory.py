from abc import ABC, abstractmethod
from pathlib import Path
from orionis.foundation.contracts.application import IApplication

class IDirectory(ABC):

    @abstractmethod
    def root(self) -> Path:
        """
        Get the root directory path of the application.

        Returns
        -------
        Path
            The path to the application's root directory.
        """
        pass

    @abstractmethod
    def commands(self) -> Path:
        """
        Get the commands directory path.

        Returns
        -------
        Path
            The path to the commands directory.
        """
        pass

    @abstractmethod
    def controllers(self) -> Path:
        """
        Get the controllers directory path.

        Returns
        -------
        Path
            The path to the controllers directory.
        """
        pass

    @abstractmethod
    def middleware(self) -> Path:
        """
        Get the middleware directory path.

        Returns
        -------
        Path
            The path to the middleware directory.
        """
        pass

    @abstractmethod
    def requests(self) -> Path:
        """
        Get the requests directory path.

        Returns
        -------
        Path
            The path to the requests directory.
        """
        pass

    @abstractmethod
    def models(self) -> Path:
        """
        Get the models directory path.

        Returns
        -------
        Path
            The path to the models directory.
        """
        pass

    @abstractmethod
    def providers(self) -> Path:
        """
        Get the providers directory path.

        Returns
        -------
        Path
            The path to the providers directory.
        """
        pass

    @abstractmethod
    def events(self) -> Path:
        """
        Get the events directory path.

        Returns
        -------
        Path
            The path to the events directory.
        """
        pass

    @abstractmethod
    def listeners(self) -> Path:
        """
        Get the listeners directory path.

        Returns
        -------
        Path
            The path to the listeners directory.
        """
        pass

    @abstractmethod
    def notifications(self) -> Path:
        """
        Get the notifications directory path.

        Returns
        -------
        Path
            The path to the notifications directory.
        """
        pass

    @abstractmethod
    def jobs(self) -> Path:
        """
        Get the jobs directory path.

        Returns
        -------
        Path
            The path to the jobs directory.
        """
        pass

    @abstractmethod
    def policies(self) -> Path:
        """
        Get the policies directory path.

        Returns
        -------
        Path
            The path to the policies directory.
        """
        pass

    @abstractmethod
    def exceptions(self) -> Path:
        """
        Get the exceptions directory path.

        Returns
        -------
        Path
            The path to the exceptions directory.
        """
        pass

    @abstractmethod
    def services(self) -> Path:
        """
        Get the services directory path.

        Returns
        -------
        Path
            The path to the services directory.
        """
        pass

    @abstractmethod
    def views(self) -> Path:
        """
        Get the views directory path.

        Returns
        -------
        Path
            The path to the views directory.
        """
        pass

    @abstractmethod
    def lang(self) -> Path:
        """
        Get the language files directory path.

        Returns
        -------
        Path
            The path to the language files directory.
        """
        pass

    @abstractmethod
    def assets(self) -> Path:
        """
        Get the assets directory path.

        Returns
        -------
        Path
            The path to the assets directory.
        """
        pass

    @abstractmethod
    def routes(self) -> Path:
        """
        Get the routes directory path.

        Returns
        -------
        Path
            The path to the routes directory.
        """
        pass

    @abstractmethod
    def config(self) -> Path:
        """
        Get the configuration directory path.

        Returns
        -------
        Path
            The path to the configuration directory.
        """
        pass

    @abstractmethod
    def migrations(self) -> Path:
        """
        Get the migrations directory path.

        Returns
        -------
        Path
            The path to the migrations directory.
        """
        pass

    @abstractmethod
    def seeders(self) -> Path:
        """
        Get the seeders directory path.

        Returns
        -------
        Path
            The path to the seeders directory.
        """
        pass

    @abstractmethod
    def factories(self) -> Path:
        """
        Get the factories directory path.

        Returns
        -------
        Path
            The path to the factories directory.
        """
        pass

    @abstractmethod
    def logs(self) -> Path:
        """
        Get the logs directory path.

        Returns
        -------
        Path
            The path to the logs directory.
        """
        pass

    @abstractmethod
    def sessions(self) -> Path:
        """
        Get the sessions directory path.

        Returns
        -------
        Path
            The path to the sessions directory.
        """
        pass

    @abstractmethod
    def cache(self) -> Path:
        """
        Get the cache directory path.

        Returns
        -------
        Path
            The path to the cache directory.
        """
        pass

    @abstractmethod
    def testing(self) -> Path:
        """
        Get the testing directory path.

        Returns
        -------
        Path
            The path to the testing directory.
        """
        pass

    @abstractmethod
    def storage(self) -> Path:
        """
        Get the storage directory path.

        Returns
        -------
        Path
            The path to the storage directory.
        """
        pass