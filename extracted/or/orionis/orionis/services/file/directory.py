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
        Initialize the Directory with an application instance.

        Parameters
        ----------
        app : IApplication
            The application instance used to resolve directory paths.
        """
        self.__app = app

    def root(self) -> Path:
        """
        Get the root directory path of the application.

        Returns
        -------
        Path
            The path to the application's root directory.
        """
        return Path(self.__app.path('root'))

    def console(self) -> Path:
        """
        Get the console directory path.

        Returns
        -------
        Path
            The path to the console directory.
        """
        return Path(self.__app.path('console'))

    def consoleCommands(self) -> Path:
        """
        Get the console commands directory path.

        Returns
        -------
        Path
            The path to the console commands directory.
        """
        return Path(self.__app.path('console')) / 'commands'

    def consoleListeners(self) -> Path:
        """
        Get the console listeners directory path.

        Returns
        -------
        Path
            The path to the console listeners directory.
        """
        return Path(self.__app.path('console')) / 'listeners'

    def controllers(self) -> Path:
        """
        Get the controllers directory path.

        Returns
        -------
        Path
            The path to the controllers directory.
        """
        return Path(self.__app.path('controllers'))

    def middleware(self) -> Path:
        """
        Get the middleware directory path.

        Returns
        -------
        Path
            The path to the middleware directory.
        """
        return Path(self.__app.path('middleware'))

    def requests(self) -> Path:
        """
        Get the requests directory path.

        Returns
        -------
        Path
            The path to the requests directory.
        """
        return Path(self.__app.path('requests'))

    def models(self) -> Path:
        """
        Get the models directory path.

        Returns
        -------
        Path
            The path to the models directory.
        """
        return Path(self.__app.path('models'))

    def providers(self) -> Path:
        """
        Get the providers directory path.

        Returns
        -------
        Path
            The path to the providers directory.
        """
        return Path(self.__app.path('providers'))

    def events(self) -> Path:
        """
        Get the events directory path.

        Returns
        -------
        Path
            The path to the events directory.
        """
        return Path(self.__app.path('events'))

    def listeners(self) -> Path:
        """
        Get the listeners directory path.

        Returns
        -------
        Path
            The path to the listeners directory.
        """
        return Path(self.__app.path('listeners'))

    def notifications(self) -> Path:
        """
        Get the notifications directory path.

        Returns
        -------
        Path
            The path to the notifications directory.
        """
        return Path(self.__app.path('notifications'))

    def jobs(self) -> Path:
        """
        Get the jobs directory path.

        Returns
        -------
        Path
            The path to the jobs directory.
        """
        return Path(self.__app.path('jobs'))

    def policies(self) -> Path:
        """
        Get the policies directory path.

        Returns
        -------
        Path
            The path to the policies directory.
        """
        return Path(self.__app.path('policies'))

    def exceptions(self) -> Path:
        """
        Get the exceptions directory path.

        Returns
        -------
        Path
            The path to the exceptions directory.
        """
        return Path(self.__app.path('exceptions'))

    def services(self) -> Path:
        """
        Get the services directory path.

        Returns
        -------
        Path
            The path to the services directory.
        """
        return Path(self.__app.path('services'))

    def views(self) -> Path:
        """
        Get the views directory path.

        Returns
        -------
        Path
            The path to the views directory.
        """
        return Path(self.__app.path('views'))

    def lang(self) -> Path:
        """
        Get the language files directory path.

        Returns
        -------
        Path
            The path to the language files directory.
        """
        return Path(self.__app.path('lang'))

    def assets(self) -> Path:
        """
        Get the assets directory path.

        Returns
        -------
        Path
            The path to the assets directory.
        """
        return Path(self.__app.path('assets'))

    def routes(self) -> Path:
        """
        Get the routes directory path.

        Returns
        -------
        Path
            The path to the routes directory.
        """
        return Path(self.__app.path('routes'))

    def config(self) -> Path:
        """
        Get the configuration directory path.

        Returns
        -------
        Path
            The path to the configuration directory.
        """
        return Path(self.__app.path('config'))

    def migrations(self) -> Path:
        """
        Get the migrations directory path.

        Returns
        -------
        Path
            The path to the migrations directory.
        """
        return Path(self.__app.path('migrations'))

    def seeders(self) -> Path:
        """
        Get the seeders directory path.

        Returns
        -------
        Path
            The path to the seeders directory.
        """
        return Path(self.__app.path('seeders'))

    def factories(self) -> Path:
        """
        Get the factories directory path.

        Returns
        -------
        Path
            The path to the factories directory.
        """
        return Path(self.__app.path('factories'))

    def logs(self) -> Path:
        """
        Get the logs directory path.

        Returns
        -------
        Path
            The path to the logs directory.
        """
        return Path(self.__app.path('logs'))

    def sessions(self) -> Path:
        """
        Get the sessions directory path.

        Returns
        -------
        Path
            The path to the sessions directory.
        """
        return Path(self.__app.path('sessions'))

    def cache(self) -> Path:
        """
        Get the cache directory path.

        Returns
        -------
        Path
            The path to the cache directory.
        """
        return Path(self.__app.path('cache'))

    def testing(self) -> Path:
        """
        Get the testing directory path.

        Returns
        -------
        Path
            The path to the testing directory.
        """
        return Path(self.__app.path('testing'))

    def storage(self) -> Path:
        """
        Get the storage directory path.

        Returns
        -------
        Path
            The path to the storage directory.
        """
        return Path(self.__app.path('storage'))