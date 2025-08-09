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
    """
    Abstract interface for the core application container.

    This interface defines the contract for application instances that manage
    service providers, configuration, and application lifecycle. It extends
    the base container interface to provide application-specific functionality
    including configuration management, service provider registration, and
    bootstrap operations.
    """

    @property
    @abstractmethod
    def isBooted(self) -> bool:
        """
        Check if the application has completed its bootstrap process.

        Returns
        -------
        bool
            True if the application has been successfully booted and is ready
            for operation, False otherwise.
        """
        pass

    @property
    @abstractmethod
    def startAt(self) -> int:
        """
        Get the application startup timestamp.

        Returns
        -------
        int
            The Unix timestamp representing when the application was started.
        """
        pass

    @abstractmethod
    def withProviders(self, providers: List[Type[IServiceProvider]] = []) -> 'IApplication':
        """
        Register multiple service providers with the application.

        Parameters
        ----------
        providers : List[Type[IServiceProvider]], optional
            A list of service provider classes to register. Each provider will
            be instantiated and registered with the application container.
            Defaults to an empty list.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def addProvider(self, provider: Type[IServiceProvider]) -> 'IApplication':
        """
        Register a single service provider with the application.

        Parameters
        ----------
        provider : Type[IServiceProvider]
            The service provider class to register with the application.
            The provider will be instantiated and its services bound to
            the container.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
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
        Configure the application with multiple service configuration objects.

        This method allows comprehensive configuration of various application
        services by providing configuration objects or dictionaries for each
        service type. All parameters are keyword-only to prevent positional
        argument confusion.

        Parameters
        ----------
        app : App | dict, optional
            Application-level configuration settings.
        auth : Auth | dict, optional
            Authentication service configuration.
        cache : Cache | dict, optional
            Caching service configuration.
        cors : Cors | dict, optional
            Cross-Origin Resource Sharing configuration.
        database : Database | dict, optional
            Database connection and settings configuration.
        filesystems : Filesystems | dict, optional
            File storage and filesystem configuration.
        logging : Logging | dict, optional
            Logging service configuration.
        mail : Mail | dict, optional
            Email service configuration.
        path : Paths | dict, optional
            Application directory paths configuration.
        queue : Queue | dict, optional
            Job queue service configuration.
        session : Session | dict, optional
            Session management configuration.
        testing : Testing | dict, optional
            Testing environment configuration.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigApp(self, **app_config) -> 'IApplication':
        """
        Configure application settings using keyword arguments.

        Parameters
        ----------
        **app_config
            Arbitrary keyword arguments representing application configuration
            settings. Keys should match the expected application configuration
            parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigApp(self, app: App | dict) -> 'IApplication':
        """
        Load application configuration from a configuration object or dictionary.

        Parameters
        ----------
        app : App | dict
            An App configuration object or dictionary containing application
            settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigAuth(self, **auth_config) -> 'IApplication':
        """
        Configure authentication settings using keyword arguments.

        Parameters
        ----------
        **auth_config
            Arbitrary keyword arguments representing authentication configuration
            settings. Keys should match the expected authentication parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigAuth(self, auth: Auth | dict) -> 'IApplication':
        """
        Load authentication configuration from a configuration object or dictionary.

        Parameters
        ----------
        auth : Auth | dict
            An Auth configuration object or dictionary containing authentication
            settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigCache(self, **cache_config) -> 'IApplication':
        """
        Configure cache settings using keyword arguments.

        Parameters
        ----------
        **cache_config
            Arbitrary keyword arguments representing cache configuration
            settings. Keys should match the expected cache parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigCache(self, cache: Cache | dict) -> 'IApplication':
        """
        Load cache configuration from a configuration object or dictionary.

        Parameters
        ----------
        cache : Cache | dict
            A Cache configuration object or dictionary containing cache
            settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigCors(self, **cors_config) -> 'IApplication':
        """
        Configure CORS settings using keyword arguments.

        Parameters
        ----------
        **cors_config
            Arbitrary keyword arguments representing Cross-Origin Resource Sharing
            configuration settings. Keys should match the expected CORS parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigCors(self, cors: Cors | dict) -> 'IApplication':
        """
        Load CORS configuration from a configuration object or dictionary.

        Parameters
        ----------
        cors : Cors | dict
            A Cors configuration object or dictionary containing CORS
            settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigDatabase(self, **database_config) -> 'IApplication':
        """
        Configure database settings using keyword arguments.

        Parameters
        ----------
        **database_config
            Arbitrary keyword arguments representing database configuration
            settings. Keys should match the expected database parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigDatabase(self, database: Database | dict) -> 'IApplication':
        """
        Load database configuration from a configuration object or dictionary.

        Parameters
        ----------
        database : Database | dict
            A Database configuration object or dictionary containing database
            connection and settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigFilesystems(self, **filesystems_config) -> 'IApplication':
        """
        Configure filesystem settings using keyword arguments.

        Parameters
        ----------
        **filesystems_config
            Arbitrary keyword arguments representing filesystem configuration
            settings. Keys should match the expected filesystem parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigFilesystems(self, filesystems: Filesystems | dict) -> 'IApplication':
        """
        Load filesystem configuration from a configuration object or dictionary.

        Parameters
        ----------
        filesystems : Filesystems | dict
            A Filesystems configuration object or dictionary containing filesystem
            settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigLogging(self, **logging_config) -> 'IApplication':
        """
        Configure logging settings using keyword arguments.

        Parameters
        ----------
        **logging_config
            Arbitrary keyword arguments representing logging configuration
            settings. Keys should match the expected logging parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigLogging(self, logging: Logging | dict) -> 'IApplication':
        """
        Load logging configuration from a configuration object or dictionary.

        Parameters
        ----------
        logging : Logging | dict
            A Logging configuration object or dictionary containing logging
            settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigMail(self, **mail_config) -> 'IApplication':
        """
        Configure mail service settings using keyword arguments.

        Parameters
        ----------
        **mail_config
            Arbitrary keyword arguments representing mail service configuration
            settings. Keys should match the expected mail parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigMail(self, mail: Mail | dict) -> 'IApplication':
        """
        Load mail configuration from a configuration object or dictionary.

        Parameters
        ----------
        mail : Mail | dict
            A Mail configuration object or dictionary containing mail service
            settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
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
        Configure application directory paths using keyword arguments.

        This method allows setting custom paths for various application directories
        including controllers, models, views, storage locations, and other framework
        components. All parameters are keyword-only and have sensible defaults based
        on common MVC framework conventions.

        Parameters
        ----------
        console_scheduler : str | Path, optional
            Path to the console kernel scheduler file.
        console_commands : str | Path, optional
            Directory path for console command classes.
        http_controllers : str | Path, optional
            Directory path for HTTP controller classes.
        http_middleware : str | Path, optional
            Directory path for HTTP middleware classes.
        http_requests : str | Path, optional
            Directory path for HTTP request classes.
        models : str | Path, optional
            Directory path for model classes.
        providers : str | Path, optional
            Directory path for service provider classes.
        events : str | Path, optional
            Directory path for event classes.
        listeners : str | Path, optional
            Directory path for event listener classes.
        notifications : str | Path, optional
            Directory path for notification classes.
        jobs : str | Path, optional
            Directory path for job classes.
        policies : str | Path, optional
            Directory path for authorization policy classes.
        exceptions : str | Path, optional
            Directory path for custom exception classes.
        services : str | Path, optional
            Directory path for service classes.
        views : str | Path, optional
            Directory path for view templates.
        lang : str | Path, optional
            Directory path for language localization files.
        assets : str | Path, optional
            Directory path for static assets.
        routes_web : str | Path, optional
            File path for web routes definition.
        routes_api : str | Path, optional
            File path for API routes definition.
        routes_console : str | Path, optional
            File path for console routes definition.
        routes_channels : str | Path, optional
            File path for channel routes definition.
        config : str | Path, optional
            Directory path for configuration files.
        migrations : str | Path, optional
            Directory path for database migration files.
        seeders : str | Path, optional
            Directory path for database seeder files.
        factories : str | Path, optional
            Directory path for model factory files.
        storage_logs : str | Path, optional
            Directory path for log files.
        storage_framework : str | Path, optional
            Directory path for framework storage files.
        storage_sessions : str | Path, optional
            Directory path for session storage files.
        storage_cache : str | Path, optional
            Directory path for cache storage files.
        storage_views : str | Path, optional
            Directory path for compiled view cache files.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadPaths(self, paths: Paths | dict) -> 'IApplication':
        """
        Load application paths configuration from a configuration object or dictionary.

        Parameters
        ----------
        paths : Paths | dict
            A Paths configuration object or dictionary containing application
            directory paths to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigQueue(self, **queue_config) -> 'IApplication':
        """
        Configure queue service settings using keyword arguments.

        Parameters
        ----------
        **queue_config
            Arbitrary keyword arguments representing queue service configuration
            settings. Keys should match the expected queue parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigQueue(self, queue: Queue | dict) -> 'IApplication':
        """
        Load queue configuration from a configuration object or dictionary.

        Parameters
        ----------
        queue : Queue | dict
            A Queue configuration object or dictionary containing queue service
            settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigSession(self, **session_config) -> 'IApplication':
        """
        Configure session management settings using keyword arguments.

        Parameters
        ----------
        **session_config
            Arbitrary keyword arguments representing session management configuration
            settings. Keys should match the expected session parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigSession(self, session: Session | dict) -> 'IApplication':
        """
        Load session configuration from a configuration object or dictionary.

        Parameters
        ----------
        session : Session | dict
            A Session configuration object or dictionary containing session
            management settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def setConfigTesting(self, **testing_config) -> 'IApplication':
        """
        Configure testing environment settings using keyword arguments.

        Parameters
        ----------
        **testing_config
            Arbitrary keyword arguments representing testing configuration
            settings. Keys should match the expected testing parameter names.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigTesting(self, testing: Testing | dict) -> 'IApplication':
        """
        Load testing configuration from a configuration object or dictionary.

        Parameters
        ----------
        testing : Testing | dict
            A Testing configuration object or dictionary containing testing
            environment settings to be loaded into the application.

        Returns
        -------
        IApplication
            The application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def config(self, key: str = None, default: Any = None) -> Any:
        """
        Retrieve configuration values using dot notation access.

        This method provides access to the application's configuration system,
        allowing retrieval of specific configuration values by key or the entire
        configuration object when no key is specified.

        Parameters
        ----------
        key : str, optional
            The configuration key to retrieve using dot notation (e.g., 'database.host').
            If None, returns the entire configuration object.
        default : Any, optional
            The default value to return if the specified key is not found.

        Returns
        -------
        Any
            The configuration value associated with the key, the entire configuration
            object if no key is provided, or the default value if the key is not found.
        """
        pass

    @abstractmethod
    def path(self, key: str = None, default: Any = None) -> Any:
        """
        Retrieve path configuration values using dot notation access.

        This method provides access to the application's path configuration system,
        allowing retrieval of specific path values by key or the entire paths
        configuration when no key is specified.

        Parameters
        ----------
        key : str, optional
            The path configuration key to retrieve using dot notation (e.g., 'storage.logs').
            If None, returns the entire paths configuration object.
        default : Any, optional
            The default value to return if the specified key is not found.

        Returns
        -------
        Any
            The path value associated with the key, the entire paths configuration
            object if no key is provided, or the default value if the key is not found.
        """
        pass

    @abstractmethod
    def create(self) -> 'IApplication':
        """
        Bootstrap and initialize the application.

        This method performs the complete application initialization process,
        including loading and registering all configured service providers,
        initializing kernels, and preparing the application for operation.
        After calling this method, the application should be fully operational
        and ready to handle requests or commands.

        Returns
        -------
        IApplication
            The fully initialized application instance ready for operation.
        """
        pass
