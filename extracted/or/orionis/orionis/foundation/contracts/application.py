from abc import abstractmethod
from pathlib import Path
from typing import Any, List, Type
from orionis.console.base.scheduler import BaseScheduler
from orionis.failure.contracts.handler import IBaseExceptionHandler
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

    def setExceptionHandler(
        self,
        handler: IBaseExceptionHandler
    ) -> 'IApplication':
        """
        Register a custom exception handler class for the application.

        This method allows you to specify a custom exception handler class that
        inherits from BaseHandlerException. The handler class will be used to
        manage exceptions raised within the application, including reporting and
        rendering error messages. The provided handler must be a class (not an
        instance) and must inherit from BaseHandlerException.

        Parameters
        ----------
        handler : Type[BaseHandlerException]
            The exception handler class to be used by the application. Must be a
            subclass of BaseHandlerException.

        Returns
        -------
        Application
            The current Application instance, allowing for method chaining.

        Raises
        ------
        OrionisTypeError
            If the provided handler is not a class or is not a subclass of BaseHandlerException.

        Notes
        -----
        The handler is stored internally and will be instantiated when needed.
        This method does not instantiate the handler; it only registers the class.
        """
        pass

    def getExceptionHandler(
        self
    ) -> IBaseExceptionHandler:
        """
        Retrieve the currently registered exception handler instance.

        This method returns an instance of the exception handler that has been set using
        the `setExceptionHandler` method. If no custom handler has been set, it returns
        a default `BaseHandlerException` instance. The returned object is responsible
        for handling exceptions within the application, including reporting and rendering
        error messages.

        Returns
        -------
        BaseHandlerException
            An instance of the currently registered exception handler. If no handler
            has been set, returns a default `BaseHandlerException` instance.

        Notes
        -----
        This method always returns an instance (not a class) of the exception handler.
        If a custom handler was registered, it is instantiated and returned; otherwise,
        a default handler is used.
        """
        pass

    @abstractmethod
    def setScheduler(
        self,
        scheduler: BaseScheduler
    ) -> 'IApplication':
        """
        Register a custom scheduler class for the application.

        This method allows you to specify a custom scheduler class that inherits from
        `BaseScheduler`. The scheduler is responsible for managing scheduled tasks
        within the application. The provided class will be validated to ensure it is
        a subclass of `BaseScheduler` and then stored for later use.

        Parameters
        ----------
        scheduler : Type[BaseScheduler]
            The scheduler class to be used by the application. Must inherit from
            `BaseScheduler`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the provided scheduler is not a subclass of `BaseScheduler`.

        Notes
        -----
        The scheduler class is stored internally and can be used by the application
        to manage scheduled jobs or tasks. This method does not instantiate the
        scheduler; it only registers the class for later use.
        """
        pass

    @abstractmethod
    def getScheduler(
        self
    ) -> BaseScheduler:
        """
        Retrieve the currently registered scheduler instance.

        This method returns the scheduler instance that has been set using the
        `setScheduler` method. If no scheduler has been set, it raises an error.

        Returns
        -------
        BaseScheduler
            The currently registered scheduler instance.

        Raises
        ------
        OrionisRuntimeError
            If no scheduler has been set in the application.
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
        root: str | Path = Path.cwd().resolve(),
        commands: str | Path = (Path.cwd() / 'app' / 'console' / 'commands').resolve(),
        controllers: str | Path = (Path.cwd() / 'app' / 'http' / 'controllers').resolve(),
        middleware: str | Path = (Path.cwd() / 'app' / 'http' / 'middleware').resolve(),
        requests: str | Path = (Path.cwd() / 'app' / 'http' / 'requests').resolve(),
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
        routes: str | Path = (Path.cwd() / 'routes').resolve(),
        config: str | Path = (Path.cwd() / 'config').resolve(),
        migrations: str | Path = (Path.cwd() / 'database' / 'migrations').resolve(),
        seeders: str | Path = (Path.cwd() / 'database' / 'seeders').resolve(),
        factories: str | Path = (Path.cwd() / 'database' / 'factories').resolve(),
        logs: str | Path = (Path.cwd() / 'storage' / 'logs').resolve(),
        sessions: str | Path = (Path.cwd() / 'storage' / 'framework' / 'sessions').resolve(),
        cache: str | Path = (Path.cwd() / 'storage' / 'framework' / 'cache').resolve(),
        testing: str | Path = (Path.cwd() / 'storage' / 'framework' / 'testing').resolve(),
        storage: str | Path = (Path.cwd() / 'storage').resolve()
    ) -> 'IApplication':
        """
        Set and resolve application directory paths using keyword arguments.

        This method allows customization of all major application directory paths, such as
        console components, HTTP components, application layers, resources, routes,
        database files, and storage locations. All provided paths are resolved to absolute
        paths and stored as strings in the configuration dictionary.

        Parameters
        ----------
        root : str or Path, optional
            Root directory of the application. Defaults to the current working directory.
        commands : str or Path, optional
            Directory for console command classes. Defaults to 'app/console/commands'.
        controllers : str or Path, optional
            Directory for HTTP controller classes. Defaults to 'app/http/controllers'.
        middleware : str or Path, optional
            Directory for HTTP middleware classes. Defaults to 'app/http/middleware'.
        requests : str or Path, optional
            Directory for HTTP request classes. Defaults to 'app/http/requests'.
        models : str or Path, optional
            Directory for data model classes. Defaults to 'app/models'.
        providers : str or Path, optional
            Directory for service provider classes. Defaults to 'app/providers'.
        events : str or Path, optional
            Directory for event classes. Defaults to 'app/events'.
        listeners : str or Path, optional
            Directory for event listener classes. Defaults to 'app/listeners'.
        notifications : str or Path, optional
            Directory for notification classes. Defaults to 'app/notifications'.
        jobs : str or Path, optional
            Directory for queue job classes. Defaults to 'app/jobs'.
        policies : str or Path, optional
            Directory for authorization policy classes. Defaults to 'app/policies'.
        exceptions : str or Path, optional
            Directory for custom exception classes. Defaults to 'app/exceptions'.
        services : str or Path, optional
            Directory for application service classes. Defaults to 'app/services'.
        views : str or Path, optional
            Directory for view templates. Defaults to 'resources/views'.
        lang : str or Path, optional
            Directory for language files. Defaults to 'resources/lang'.
        assets : str or Path, optional
            Directory for asset files. Defaults to 'resources/assets'.
        routes : str or Path, optional
            Directory for route definitions. Defaults to 'routes'.
        config : str or Path, optional
            Directory for configuration files. Defaults to 'config'.
        migrations : str or Path, optional
            Directory for database migration files. Defaults to 'database/migrations'.
        seeders : str or Path, optional
            Directory for database seeder files. Defaults to 'database/seeders'.
        factories : str or Path, optional
            Directory for model factory files. Defaults to 'database/factories'.
        logs : str or Path, optional
            Directory for log file storage. Defaults to 'storage/logs'.
        sessions : str or Path, optional
            Directory for session file storage. Defaults to 'storage/framework/sessions'.
        cache : str or Path, optional
            Directory for cache file storage. Defaults to 'storage/framework/cache'.
        testing : str or Path, optional
            Directory for testing file storage. Defaults to 'storage/framework/testing'.

        Returns
        -------
        Application
            Returns the current Application instance to enable method chaining.

        Notes
        -----
        All path parameters accept either string or Path objects and are automatically
        resolved to absolute paths relative to the current working directory. The
        resolved paths are stored as strings in the internal configuration dictionary.
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
    def setBasePath(
        self,
        basePath: Path
    ) -> 'IApplication':
        """
        Set the base path for the application.

        This method allows setting the base path of the application, which is
        used as the root directory for all relative paths in the application.
        The provided basePath is resolved to an absolute path.

        Parameters
        ----------
        basePath : Path
            The base path to set for the application. It can be a string or a Path object.

        Returns
        -------
        Application
            The current application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def getBasePath(
        self
    ) -> Path:
        """
        Get the base path of the application.

        This method returns the base path that was previously set using setBasePath().
        If no base path has been set, it returns None.

        Returns
        -------
        Path
            The base path of the application as a string or Path object, or None if not set.
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
    def path(self, key: str = None, default: Any = None) -> str:
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
        str
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
