from abc import abstractmethod
from pathlib import Path
from typing import Any, List, Type
from orionis.foundation.config.roots.paths import Paths
from orionis.container.contracts.service_provider import IServiceProvider
from orionis.container.contracts.container import IContainer
from orionis.foundation.config.app.entities.app import App
from orionis.foundation.config.auth.entities.auth import Auth
from orionis.foundation.config.cache.entities.cache import Cache
from orionis.foundation.config.cors.entities.cors import Cors
from orionis.foundation.config.database.entities.database import Database
from orionis.foundation.config.filesystems.entitites.filesystems import Filesystems
from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.mail.entities.mail import Mail
from orionis.foundation.config.queue.entities.queue import Queue
from orionis.foundation.config.session.entities.session import Session
from orionis.foundation.config.testing.entities.testing import Testing

class IApplication(IContainer):

    @property
    @abstractmethod
    def isBooted(self) -> bool:
        """
        Indicates whether the application has been booted.

        Returns
        -------
        bool
            True if the application is booted, False otherwise.
        """
        pass

    @property
    @abstractmethod
    def startAt(self) -> int:
        """
        Returns the timestamp when the application was started.

        Returns
        -------
        int
            The start time as a Unix timestamp.
        """
        pass

    @abstractmethod
    def withProviders(self, providers: List[Type[IServiceProvider]] = []) -> 'IApplication':
        """
        Add multiple service providers to the application.

        Parameters
        ----------
        providers : List[Type[IServiceProvider]], optional
            List of provider classes to add to the application.

        Returns
        -------
        IApplication
            The application instance for method chaining.
        """
        pass

    @abstractmethod
    def addProvider(self, provider: Type[IServiceProvider]) -> 'IApplication':
        """
        Add a single service provider to the application.

        Parameters
        ----------
        provider : Type[IServiceProvider]
            The provider class to add to the application.

        Returns
        -------
        IApplication
            The application instance for method chaining.
        """
        pass

    @abstractmethod
    def withConfigurators(
        self,
        *,
        app: App | dict = App(),
        auth: Auth | dict = Auth(),
        cache : Cache | dict = Cache(),
        cors : Cors | dict = Cors(),
        database : Database | dict = Database(),
        filesystems : Filesystems | dict = Filesystems(),
        logging : Logging | dict = Logging(),
        mail : Mail | dict = Mail(),
        path : Paths | dict = Paths(),
        queue : Queue | dict = Queue(),
        session : Session | dict = Session(),
        testing : Testing | dict = Testing()
    ) -> 'IApplication':
        """
        Configure the application with various service configurators.
        Allows setting up different aspects of the application by providing configurator instances for services like authentication, caching, database, etc.

        Returns
        -------
        IApplication
            Returns self to allow method chaining.
        """
        pass

    @abstractmethod
    def setConfigApp(self, **app_config) -> 'IApplication':
        """
        Set the application configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigApp(self, app: App | dict) -> 'IApplication':
        """
        Load the application configuration from an App instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigAuth(self, **auth_config) -> 'IApplication':
        """
        Set the authentication configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigAuth(self, auth: Auth | dict) -> 'IApplication':
        """
        Load the authentication configuration from an Auth instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigCache(self, **cache_config) -> 'IApplication':
        """
        Set the cache configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigCache(self, cache: Cache | dict) -> 'IApplication':
        """
        Load the cache configuration from a Cache instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigCors(self, **cors_config) -> 'IApplication':
        """
        Set the CORS configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigCors(self, cors: Cors | dict) -> 'IApplication':
        """
        Load the CORS configuration from a Cors instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigDatabase(self, **database_config) -> 'IApplication':
        """
        Set the database configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigDatabase(self, database: Database | dict) -> 'IApplication':
        """
        Load the database configuration from a Database instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigFilesystems(self, **filesystems_config) -> 'IApplication':
        """
        Set the filesystems configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigFilesystems(self, filesystems: Filesystems | dict) -> 'IApplication':
        """
        Load the filesystems configuration from a Filesystems instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigLogging(self, **logging_config) -> 'IApplication':
        """
        Set the logging configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigLogging(self, logging: Logging | dict) -> 'IApplication':
        """
        Load the logging configuration from a Logging instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigMail(self, **mail_config) -> 'IApplication':
        """
        Set the mail configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigMail(self, mail: Mail | dict) -> 'IApplication':
        """
        Load the mail configuration from a Mail instance or dictionary.
        """
        pass

    @abstractmethod
    def setPaths(
        self,
        *,
        console_scheduler: str | Path = (Path.cwd() / 'app' / 'console' / 'kernel.py').resolve(),
        console_commands: str | Path = (Path.cwd() / 'app' / 'console' / 'commands').resolve(),
        http_controllers: str | Path = (Path.cwd() / 'app' / 'http' / 'controllers').resolve(),
        http_middleware: str | Path = (Path.cwd() / 'app' / 'http' / 'middleware').resolve(),
        http_requests: str | Path = (Path.cwd() / 'app' / 'http' / 'requests').resolve(),
        models: str | Path = (Path.cwd() / 'app' / 'models').resolve(),
        providers: str | Path = (Path.cwd() / 'app' / 'providers').resolve(),
        events: str | Path = (Path.cwd() / 'app' / 'events').resolve(),
        listeners: str | Path = (Path.cwd() / 'app' / 'listeners').resolve(),
        notifications: str | Path = (Path.cwd() / 'app' / 'notifications').resolve(),
        jobs: str | Path = (Path.cwd() / 'app' / 'jobs').resolve(),
        policies: str | Path = (Path.cwd() / 'app' / 'policies').resolve(),
        exceptions: str | Path = (Path.cwd() / 'app' / 'exceptions').resolve(),
        services: str | Path = (Path.cwd() / 'app' / 'services').resolve(),
        views: str | Path = (Path.cwd() / 'resources' / 'views').resolve(),
        lang: str | Path = (Path.cwd() / 'resources' / 'lang').resolve(),
        assets: str | Path = (Path.cwd() / 'resources' / 'assets').resolve(),
        routes_web: str | Path = (Path.cwd() / 'routes' / 'web.py').resolve(),
        routes_api: str | Path = (Path.cwd() / 'routes' / 'api.py').resolve(),
        routes_console: str | Path = (Path.cwd() / 'routes' / 'console.py').resolve(),
        routes_channels: str | Path = (Path.cwd() / 'routes' / 'channels.py').resolve(),
        config: str | Path = (Path.cwd() / 'config').resolve(),
        migrations: str | Path = (Path.cwd() / 'database' / 'migrations').resolve(),
        seeders: str | Path = (Path.cwd() / 'database' / 'seeders').resolve(),
        factories: str | Path = (Path.cwd() / 'database' / 'factories').resolve(),
        storage_logs: str | Path = (Path.cwd() / 'storage' / 'logs').resolve(),
        storage_framework: str | Path = (Path.cwd() / 'storage' / 'framework').resolve(),
        storage_sessions: str | Path = (Path.cwd() / 'storage' / 'framework' / 'sessions').resolve(),
        storage_cache: str | Path = (Path.cwd() / 'storage' / 'framework' / 'cache').resolve(),
        storage_views: str | Path = (Path.cwd() / 'storage' / 'framework' / 'views').resolve(),
    ) -> 'IApplication':
        """
        Set the application paths configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadPaths(self, paths: Paths | dict) -> 'IApplication':
        """
        Load the application paths configuration from a Paths instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigQueue(self, **queue_config) -> 'IApplication':
        """
        Set the queue configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigQueue(self, queue: Queue | dict) -> 'IApplication':
        """
        Load the queue configuration from a Queue instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigSession(self, **session_config) -> 'IApplication':
        """
        Set the session configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigSession(self, session: Session | dict) -> 'IApplication':
        """
        Load the session configuration from a Session instance or dictionary.
        """
        pass

    @abstractmethod
    def setConfigTesting(self, **testing_config) -> 'IApplication':
        """
        Set the testing configuration using keyword arguments.
        """
        pass

    @abstractmethod
    def loadConfigTesting(self, testing: Testing | dict) -> 'IApplication':
        """
        Load the testing configuration from a Testing instance or dictionary.
        """
        pass

    @abstractmethod
    def config(self, key: str = None, default: Any = None) -> Any:
        """
        Retrieve a configuration value using dot notation, or the entire configuration if no key is provided.

        Parameters
        ----------
        key : str, optional
            The configuration key to retrieve.
        default : Any, optional
            The default value to return if the key is not found.

        Returns
        -------
        Any
            The configuration value or the default.
        """
        pass

    @abstractmethod
    def path(self, key: str = None, default: Any = None) -> Any:
        """
        Retrieve a path configuration value using dot notation, or the entire paths configuration if no key is provided.

        Parameters
        ----------
        key : str, optional
            The path key to retrieve.
        default : Any, optional
            The default value to return if the key is not found.

        Returns
        -------
        Any
            The path value or the default.
        """
        pass

    @abstractmethod
    def create(self) -> 'IApplication':
        """
        Bootstrap the application, loading all necessary providers and kernels.

        Returns
        -------
        IApplication
            The initialized application instance.
        """
        pass
