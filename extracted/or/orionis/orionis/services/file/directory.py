from pathlib import Path
from orionis.foundation.contracts.application import IApplication
from orionis.services.file.contracts.directory import IDirectory

class Directory(IDirectory):
    """
    Provides convenient access to various application directories.

    This class uses the application instance to resolve and return
    paths to different directories within the application's structure.

    Parameters
    ----------
    app : IApplication
        The application instance used to resolve directory paths.
    """

    def __init__(self, app: IApplication) -> None:
        """
        Initialize the Directory service.

        Parameters
        ----------
        app : IApplication
            The application instance used to resolve directory paths.

        Returns
        -------
        None
        """
        self.__app = app

    def root(self) -> Path:
        """
        Get the root directory of the application.

        Returns
        -------
        Path
            Path object representing the root directory.
        """
        return Path(self.__app.path('root'))

    def app(self) -> Path:
        """
        Get the main application directory.

        Returns
        -------
        Path
            Path object representing the application directory.
        """
        return Path(self.__app.path('app'))

    def console(self) -> Path:
        """
        Get the console directory.

        Returns
        -------
        Path
            Path object representing the console directory.
        """
        return Path(self.__app.path('console'))

    def exceptions(self) -> Path:
        """
        Get the exceptions directory.

        Returns
        -------
        Path
            Path object representing the exceptions directory.
        """
        return Path(self.__app.path('exceptions'))

    def http(self) -> Path:
        """
        Get the HTTP directory.

        Returns
        -------
        Path
            Path object representing the HTTP directory.
        """
        return Path(self.__app.path('http'))

    def models(self) -> Path:
        """
        Get the models directory.

        Returns
        -------
        Path
            Path object representing the models directory.
        """
        return Path(self.__app.path('models'))

    def providers(self) -> Path:
        """
        Get the providers directory.

        Returns
        -------
        Path
            Path object representing the providers directory.
        """
        return Path(self.__app.path('providers'))

    def notifications(self) -> Path:
        """
        Get the notifications directory.

        Returns
        -------
        Path
            Path object representing the notifications directory.
        """
        return Path(self.__app.path('notifications'))

    def services(self) -> Path:
        """
        Get the services directory.

        Returns
        -------
        Path
            Path object representing the services directory.
        """
        return Path(self.__app.path('services'))

    def jobs(self) -> Path:
        """
        Get the jobs directory.

        Returns
        -------
        Path
            Path object representing the jobs directory.
        """
        return Path(self.__app.path('jobs'))

    def bootstrap(self) -> Path:
        """
        Get the bootstrap directory.

        Returns
        -------
        Path
            Path object representing the bootstrap directory.
        """
        return Path(self.__app.path('bootstrap'))

    def config(self) -> Path:
        """
        Get the configuration directory.

        Returns
        -------
        Path
            Path object representing the configuration directory.
        """
        return Path(self.__app.path('config'))

    def database(self) -> Path:
        """
        Get the database directory.

        Returns
        -------
        Path
            Path object representing the database directory.
        """
        return Path(self.__app.path('database'))

    def resources(self) -> Path:
        """
        Get the resources directory.

        Returns
        -------
        Path
            Path object representing the resources directory.
        """
        return Path(self.__app.path('resources'))

    def routes(self) -> Path:
        """
        Get the routes directory.

        Returns
        -------
        Path
            Path object representing the routes directory.
        """
        return Path(self.__app.path('routes'))

    def storage(self) -> Path:
        """
        Get the storage directory.

        Returns
        -------
        Path
            Path object representing the storage directory.
        """
        return Path(self.__app.path('storage'))

    def tests(self) -> Path:
        """
        Get the tests directory.

        Returns
        -------
        Path
            Path object representing the tests directory.
        """
        return Path(self.__app.path('tests'))
