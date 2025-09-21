from abc import abstractmethod
from pathlib import Path
from typing import Any, List, Type
from orionis.console.contracts.base_scheduler import IBaseScheduler
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

    @abstractmethod
    def withProviders(
        self,
        providers: List[Type[IServiceProvider]] = []
    ) -> 'IApplication':
        """
        Register multiple service providers with the application.

        This method provides a convenient way to add multiple service provider
        classes to the application in a single call. Each provider in the list
        will be validated and added to the internal providers collection.

        Parameters
        ----------
        providers : List[Type[IServiceProvider]], optional
            A list of service provider classes that implement IServiceProvider
            interface. Each provider will be added to the application's provider
            registry. Default is an empty list.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method iterates through the provided list and calls addProvider()
        for each provider class, which performs individual validation and
        registration.
        """
        pass

    @abstractmethod
    def addProvider(
        self,
        provider: Type[IServiceProvider]
    ) -> 'IApplication':
        """
        Register a single service provider with the application.

        This method validates and adds a service provider class to the application's
        provider registry. The provider must implement the IServiceProvider interface
        and will be checked for duplicates before registration.

        Parameters
        ----------
        provider : Type[IServiceProvider]
            A service provider class that implements the IServiceProvider interface.
            The class will be instantiated and registered during the application
            bootstrap process.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the provider parameter is not a class type or does not implement
            the IServiceProvider interface, or if the provider is already registered.

        Notes
        -----
        Providers are stored as class references and will be instantiated during
        the registration phase of the application bootstrap process.
        """
        pass

    @abstractmethod
    def setExceptionHandler(
        self,
        handler: IBaseExceptionHandler
    ) -> 'IApplication':
        """
        Register a custom exception handler class for the application.

        This method allows you to specify a custom exception handler class that
        inherits from BaseExceptionHandler. The handler class will be used to
        manage exceptions raised within the application, including reporting and
        rendering error messages. The provided handler must be a class (not an
        instance) and must inherit from BaseExceptionHandler.

        Parameters
        ----------
        handler : Type[BaseExceptionHandler]
            The exception handler class to be used by the application. Must be a
            subclass of BaseExceptionHandler.

        Returns
        -------
        Application
            The current Application instance, allowing for method chaining.

        Raises
        ------
        OrionisTypeError
            If the provided handler is not a class or is not a subclass of BaseExceptionHandler.

        Notes
        -----
        The handler is stored internally and will be instantiated when needed.
        This method does not instantiate the handler; it only registers the class.
        """
        pass

    @abstractmethod
    def getExceptionHandler(
        self
    ) -> IBaseExceptionHandler:
        """
        Retrieve the currently registered exception handler instance.

        This method returns an instance of the exception handler that has been set using
        the `setExceptionHandler` method. If no custom handler has been set, it returns
        a default `BaseExceptionHandler` instance. The returned object is responsible
        for handling exceptions within the application, including reporting and rendering
        error messages.

        Returns
        -------
        BaseExceptionHandler
            An instance of the currently registered exception handler. If no handler
            has been set, returns a default `BaseExceptionHandler` instance.

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
        scheduler: IBaseScheduler
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
    ) -> IBaseScheduler:
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
        Configure the application with comprehensive service configuration objects.

        This method provides a centralized way to configure all major application
        subsystems using either configuration entity instances or dictionary objects.
        Each configurator manages settings for a specific aspect of the application
        such as authentication, caching, database connectivity, logging, and more.

        Parameters
        ----------
        app : App or dict, optional
            Application-level configuration including name, environment, debug settings,
            and URL configuration. Default creates a new App() instance.
        auth : Auth or dict, optional
            Authentication system configuration including guards, providers, and
            password settings. Default creates a new Auth() instance.
        cache : Cache or dict, optional
            Caching system configuration including default store, prefix settings,
            and driver-specific options. Default creates a new Cache() instance.
        cors : Cors or dict, optional
            Cross-Origin Resource Sharing configuration including allowed origins,
            methods, and headers. Default creates a new Cors() instance.
        database : Database or dict, optional
            Database connectivity configuration including default connection, migration
            settings, and connection definitions. Default creates a new Database() instance.
        filesystems : Filesystems or dict, optional
            File storage system configuration including default disk, cloud storage
            settings, and disk definitions. Default creates a new Filesystems() instance.
        logging : Logging or dict, optional
            Logging system configuration including default channel, log levels,
            and channel definitions. Default creates a new Logging() instance.
        mail : Mail or dict, optional
            Email system configuration including default mailer, transport settings,
            and mailer definitions. Default creates a new Mail() instance.
        path : Paths or dict, optional
            Application path configuration including directories for controllers,
            models, views, and other application components. Default creates a new Paths() instance.
        queue : Queue or dict, optional
            Queue system configuration including default connection, worker settings,
            and connection definitions. Default creates a new Queue() instance.
        session : Session or dict, optional
            Session management configuration including driver, lifetime, encryption,
            and storage settings. Default creates a new Session() instance.
        testing : Testing or dict, optional
            Testing framework configuration including database settings, environment
            variables, and test-specific options. Default creates a new Testing() instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If any configurator parameter is not an instance of its expected type
            or a dictionary that can be converted to the expected type.

        Notes
        -----
        Each configurator is validated for type correctness and then passed to its
        corresponding load method for processing and storage in the application's
        configuration system.
        """
        pass

    @abstractmethod
    def setConfigApp(
        self,
        **app_config
    ) -> 'IApplication':
        """
        Configure the application using keyword arguments.

        This method provides a convenient way to set application configuration
        by passing individual configuration parameters as keyword arguments.
        The parameters are used to create an App configuration instance.

        Parameters
        ----------
        **app_config : dict
            Configuration parameters for the application. These must match the
            field names and types expected by the App dataclass from
            orionis.foundation.config.app.entities.app.App.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates an App instance from the provided keyword
        arguments and then calls loadConfigApp() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigApp(
        self,
        app: App | dict
    ) -> 'IApplication':
        """
        Load and store application configuration from an App instance or dictionary.

        This method validates and stores the application configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to an App instance before storage.

        Parameters
        ----------
        app : App or dict
            The application configuration as either an App instance or a dictionary
            containing configuration parameters that can be used to construct an
            App instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the app parameter is not an instance of App or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to App instances using
        the dictionary unpacking operator (**app).
        """
        pass

    @abstractmethod
    def setConfigAuth(
        self,
        **auth_config
    ) -> 'IApplication':
        """
        Configure the authentication system using keyword arguments.

        This method provides a convenient way to set authentication configuration
        by passing individual configuration parameters as keyword arguments.
        The parameters are used to create an Auth configuration instance.

        Parameters
        ----------
        **auth_config : dict
            Configuration parameters for authentication. These must match the
            field names and types expected by the Auth dataclass from
            orionis.foundation.config.auth.entities.auth.Auth.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates an Auth instance from the provided keyword
        arguments and then calls loadConfigAuth() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigAuth(
        self,
        auth: Auth | dict
    ) -> 'IApplication':
        """
        Load and store authentication configuration from an Auth instance or dictionary.

        This method validates and stores the authentication configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to an Auth instance before storage.

        Parameters
        ----------
        auth : Auth or dict
            The authentication configuration as either an Auth instance or a dictionary
            containing configuration parameters that can be used to construct an
            Auth instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the auth parameter is not an instance of Auth or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Auth instances using
        the dictionary unpacking operator (**auth).
        """
        pass

    @abstractmethod
    def setConfigCache(
        self,
        **cache_config
    ) -> 'IApplication':
        """
        Configure the cache system using keyword arguments.

        This method provides a convenient way to set cache configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Cache configuration instance.

        Parameters
        ----------
        **cache_config : dict
            Configuration parameters for the cache system. These must match the
            field names and types expected by the Cache dataclass from
            orionis.foundation.config.cache.entities.cache.Cache.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Cache instance from the provided keyword
        arguments and then calls loadConfigCache() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigCache(
        self,
        cache: Cache | dict
    ) -> 'IApplication':
        """
        Load and store cache configuration from a Cache instance or dictionary.

        This method validates and stores the cache configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to a Cache instance before storage.

        Parameters
        ----------
        cache : Cache or dict
            The cache configuration as either a Cache instance or a dictionary
            containing configuration parameters that can be used to construct a
            Cache instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the cache parameter is not an instance of Cache or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Cache instances using
        the dictionary unpacking operator (**cache).
        """
        pass

    @abstractmethod
    def setConfigCors(
        self,
        **cors_config
    ) -> 'IApplication':
        """
        Configure the CORS (Cross-Origin Resource Sharing) system using keyword arguments.

        This method provides a convenient way to set CORS configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Cors configuration instance.

        Parameters
        ----------
        **cors_config : dict
            Configuration parameters for CORS settings. These must match the
            field names and types expected by the Cors dataclass from
            orionis.foundation.config.cors.entities.cors.Cors.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Cors instance from the provided keyword
        arguments and then calls loadConfigCors() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigCors(
        self,
        cors: Cors | dict
    ) -> 'IApplication':
        """
        Load and store CORS configuration from a Cors instance or dictionary.

        This method validates and stores the CORS (Cross-Origin Resource Sharing)
        configuration in the internal configurators storage. If a dictionary is
        provided, it will be converted to a Cors instance before storage.

        Parameters
        ----------
        cors : Cors or dict
            The CORS configuration as either a Cors instance or a dictionary
            containing configuration parameters that can be used to construct a
            Cors instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the cors parameter is not an instance of Cors or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Cors instances using
        the dictionary unpacking operator (**cors).
        """
        pass

    @abstractmethod
    def setConfigDatabase(
        self,
        **database_config
    ) -> 'IApplication':
        """
        Configure the database system using keyword arguments.

        This method provides a convenient way to set database configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Database configuration instance.

        Parameters
        ----------
        **database_config : dict
            Configuration parameters for the database system. These must match the
            field names and types expected by the Database dataclass from
            orionis.foundation.config.database.entities.database.Database.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Database instance from the provided keyword
        arguments and then calls loadConfigDatabase() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigDatabase(
        self,
        database: Database | dict
    ) -> 'IApplication':
        """
        Load and store database configuration from a Database instance or dictionary.

        This method validates and stores the database configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to a Database instance before storage.

        Parameters
        ----------
        database : Database or dict
            The database configuration as either a Database instance or a dictionary
            containing configuration parameters that can be used to construct a
            Database instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the database parameter is not an instance of Database or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Database instances using
        the dictionary unpacking operator (**database).
        """
        pass

    @abstractmethod
    def setConfigFilesystems(
        self,
        **filesystems_config
    ) -> 'IApplication':
        """
        Configure the filesystems using keyword arguments.

        This method provides a convenient way to set filesystem configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Filesystems configuration instance.

        Parameters
        ----------
        **filesystems_config : dict
            Configuration parameters for the filesystems. These must match the
            field names and types expected by the Filesystems dataclass from
            orionis.foundation.config.filesystems.entitites.filesystems.Filesystems.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Filesystems instance from the provided keyword
        arguments and then calls loadConfigFilesystems() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigFilesystems(
        self,
        filesystems: Filesystems | dict
    ) -> 'IApplication':
        """
        Load and store filesystems configuration from a Filesystems instance or dictionary.

        This method validates and stores the filesystems configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to a Filesystems instance before storage.

        Parameters
        ----------
        filesystems : Filesystems or dict
            The filesystems configuration as either a Filesystems instance or a dictionary
            containing configuration parameters that can be used to construct a
            Filesystems instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the filesystems parameter is not an instance of Filesystems or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Filesystems instances using
        the dictionary unpacking operator (**filesystems).
        """
        pass

    @abstractmethod
    def setConfigLogging(
        self,
        **logging_config
    ) -> 'IApplication':
        """
        Configure the logging system using keyword arguments.

        This method provides a convenient way to set logging configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Logging configuration instance.

        Parameters
        ----------
        **logging_config : dict
            Configuration parameters for the logging system. These must match the
            field names and types expected by the Logging dataclass from
            orionis.foundation.config.logging.entities.logging.Logging.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Logging instance from the provided keyword
        arguments and then calls loadConfigLogging() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigLogging(
        self,
        logging: Logging | dict
    ) -> 'IApplication':
        """
        Load and store logging configuration from a Logging instance or dictionary.

        This method validates and stores the logging configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to a Logging instance before storage.

        Parameters
        ----------
        logging : Logging or dict
            The logging configuration as either a Logging instance or a dictionary
            containing configuration parameters that can be used to construct a
            Logging instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the logging parameter is not an instance of Logging or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Logging instances using
        the dictionary unpacking operator (**logging).
        """
        pass

    @abstractmethod
    def setConfigMail(
        self,
        **mail_config
    ) -> 'IApplication':
        """
        Configure the mail system using keyword arguments.

        This method provides a convenient way to set mail configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Mail configuration instance.

        Parameters
        ----------
        **mail_config : dict
            Configuration parameters for the mail system. These must match the
            field names and types expected by the Mail dataclass from
            orionis.foundation.config.mail.entities.mail.Mail.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Mail instance from the provided keyword
        arguments and then calls loadConfigMail() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigMail(
        self,
        mail: Mail | dict
    ) -> 'IApplication':
        """
        Load and store mail configuration from a Mail instance or dictionary.

        This method validates and stores the mail configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to a Mail instance before storage.

        Parameters
        ----------
        mail : Mail or dict
            The mail configuration as either a Mail instance or a dictionary
            containing configuration parameters that can be used to construct a
            Mail instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the mail parameter is not an instance of Mail or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Mail instances using
        the dictionary unpacking operator (**mail).
        """
        pass

    @abstractmethod
    def setConfigQueue(
        self,
        **queue_config
    ) -> 'IApplication':
        """
        Configure the queue system using keyword arguments.

        This method provides a convenient way to set queue configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Queue configuration instance.

        Parameters
        ----------
        **queue_config : dict
            Configuration parameters for the queue system. These must match the
            field names and types expected by the Queue dataclass from
            orionis.foundation.config.queue.entities.queue.Queue.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Queue instance from the provided keyword
        arguments and then calls loadConfigQueue() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigQueue(
        self,
        queue: Queue | dict
    ) -> 'IApplication':
        """
        Load and store queue configuration from a Queue instance or dictionary.

        This method validates and stores the queue configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to a Queue instance before storage.

        Parameters
        ----------
        queue : Queue or dict
            The queue configuration as either a Queue instance or a dictionary
            containing configuration parameters that can be used to construct a
            Queue instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the queue parameter is not an instance of Queue or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Queue instances using
        the dictionary unpacking operator (**queue).
        """
        pass

    @abstractmethod
    def setConfigSession(
        self,
        **session_config
    ) -> 'IApplication':
        """
        Configure the session system using keyword arguments.

        This method provides a convenient way to set session configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Session configuration instance.

        Parameters
        ----------
        **session_config : dict
            Configuration parameters for the session system. These must match the
            field names and types expected by the Session dataclass from
            orionis.foundation.config.session.entities.session.Session.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Session instance from the provided keyword
        arguments and then calls loadConfigSession() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigSession(
        self,
        session: Session | dict
    ) -> 'IApplication':
        """
        Load and store session configuration from a Session instance or dictionary.

        This method validates and stores the session configuration in the
        internal configurators storage. If a dictionary is provided, it will
        be converted to a Session instance before storage.

        Parameters
        ----------
        session : Session or dict
            The session configuration as either a Session instance or a dictionary
            containing configuration parameters that can be used to construct a
            Session instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the session parameter is not an instance of Session or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Session instances using
        the dictionary unpacking operator (**session).
        """
        pass

    @abstractmethod
    def setConfigTesting(
        self,
        **testing_config
    ) -> 'IApplication':
        """
        Configure the testing framework using keyword arguments.

        This method provides a convenient way to set testing configuration by
        passing individual configuration parameters as keyword arguments.
        The parameters are used to create a Testing configuration instance.

        Parameters
        ----------
        **testing_config : dict
            Configuration parameters for the testing framework. These must match the
            field names and types expected by the Testing dataclass from
            orionis.foundation.config.testing.entities.testing.Testing.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        This method internally creates a Testing instance from the provided keyword
        arguments and then calls loadConfigTesting() to store the configuration.
        """
        pass

    @abstractmethod
    def loadConfigTesting(
        self,
        testing: Testing | dict
    ) -> 'IApplication':
        """
        Load and store testing configuration from a Testing instance or dictionary.

        This method validates and stores the testing framework configuration in the
        internal configurators storage. If a dictionary is provided, it will be
        converted to a Testing instance before storage.

        Parameters
        ----------
        testing : Testing or dict
            The testing configuration as either a Testing instance or a dictionary
            containing configuration parameters that can be used to construct a
            Testing instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the testing parameter is not an instance of Testing or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Testing instances using
        the dictionary unpacking operator (**testing).
        """
        pass

    @abstractmethod
    def setConfigPaths(
        self,
        *,
        root: str | Path = str(Path.cwd().resolve()),
        app: str | Path = str((Path.cwd() / 'app').resolve()),
        console: str | Path = str((Path.cwd() / 'app' / 'console').resolve()),
        exceptions: str | Path = str((Path.cwd() / 'app' / 'exceptions').resolve()),
        http: str | Path = str((Path.cwd() / 'app' / 'http').resolve()),
        models: str | Path = str((Path.cwd() / 'app' / 'models').resolve()),
        providers: str | Path = str((Path.cwd() / 'app' / 'providers').resolve()),
        notifications: str | Path = str((Path.cwd() / 'app' / 'notifications').resolve()),
        services: str | Path = str((Path.cwd() / 'app' / 'services').resolve()),
        jobs: str | Path = str((Path.cwd() / 'app' / 'jobs').resolve()),
        bootstrap: str | Path = str((Path.cwd() / 'app' / 'bootstrap').resolve()),
        config: str | Path = str((Path.cwd() / 'config').resolve()),
        database: str | Path = str((Path.cwd() / 'database' / 'database').resolve()),
        resources: str | Path = str((Path.cwd() / 'resources').resolve()),
        routes: str | Path = str((Path.cwd() / 'routes').resolve()),
        storage: str | Path = str((Path.cwd() / 'storage').resolve()),
        tests: str | Path = str((Path.cwd() / 'tests').resolve())
    ) -> 'IApplication':
        """
        Set and resolve application directory paths using keyword arguments.

        Only the following options are available:
        - root
        - app
        - console
        - exceptions
        - http
        - models
        - providers
        - notifications
        - services
        - jobs
        - bootstrap
        - config
        - database
        - resources
        - routes
        - storage
        - tests

        All provided paths are resolved to absolute paths and stored as strings in the configuration dictionary.

        Returns
        -------
        Application
            Returns the current Application instance to enable method chaining.
        """
        pass

    @abstractmethod
    def loadConfigPaths(
        self,
        paths: Paths | dict
    ) -> 'IApplication':
        """
        Load and store path configuration from a Paths instance or dictionary.

        This method validates and stores the application path configuration in the
        internal configurators storage. If a dictionary is provided, it will be
        converted to a Paths instance before storage.

        Parameters
        ----------
        paths : Paths or dict
            The path configuration as either a Paths instance or a dictionary
            containing path parameters that can be used to construct a Paths instance.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Raises
        ------
        OrionisTypeError
            If the paths parameter is not an instance of Paths or a dictionary.

        Notes
        -----
        Dictionary inputs are automatically converted to Paths instances using
        the dictionary unpacking operator (**paths). This method is used internally
        by withConfigurators() and can be called directly for path configuration.
        """
        pass

    @abstractmethod
    def config(
        self,
        key: str = None,
        value: Any = None
    ) -> Any:
        """
        Retrieve or set application configuration values using dot notation.

        If only `key` is provided, returns the configuration value for that key.
        If both `key` and `value` are provided, sets the configuration value.
        If neither is provided, returns the entire configuration dictionary (excluding 'path').

        Parameters
        ----------
        key : str, optional
            Dot-notated configuration key (e.g., "database.default"). If None, returns all config.
        value : Any, optional
            Value to set for the given key. If None, performs a get operation.

        Returns
        -------
        Any
            The configuration value, or None if not found.

        Raises
        ------
        OrionisRuntimeError
            If configuration is not initialized.
        OrionisValueError
            If key is not a string.
        """
        pass

    @abstractmethod
    def resetConfig(
        self
    ) -> 'IApplication':
        """
        Reset the application configuration to an uninitialized state.

        This method clears the current runtime configuration and marks the application
        as unconfigured, allowing for re-initialization of the configuration by calling
        `create()` again. This is useful in scenarios such as testing or when dynamic
        reloading of configuration is required.

        Notes
        -----
        - After calling this method, you must call `create()` to reinitialize
          the configuration before accessing it again.
        - This method does not affect other aspects of the application state,
          such as registered providers or boot status.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.
        """
        pass

    @abstractmethod
    def path(
        self,
        key: str = None
    ) -> Path | dict:
        """
        Retrieve application path configuration values using dot notation.

        This method provides access to the application's path configuration, allowing retrieval of either a specific path value or the entire paths configuration dictionary. If a key is provided, the corresponding path is returned as a `Path` object. If no key is provided, a dictionary mapping all path configuration keys to their resolved `Path` objects is returned.

        Parameters
        ----------
        key : str, optional
            Dot-notated key specifying the path configuration to retrieve (e.g., "console", "storage.logs").
            If None, returns the entire paths configuration dictionary. Default is None.

        Returns
        -------
        Path or dict
            If `key` is provided and found, returns the resolved `Path` object for that key.
            If `key` is None, returns a dictionary mapping all path keys to their resolved `Path` objects.
            If `key` is not found, returns None.

        Raises
        ------
        OrionisRuntimeError
            If the application configuration has not been initialized (i.e., if `create()` has not been called).
        OrionisValueError
            If the provided `key` parameter is not a string.

        Notes
        -----
        - The method traverses the paths configuration structure by splitting the key on dots and navigating through dictionary levels.
        - This method is specifically designed for path-related configuration access, separate from general application configuration.
        - All returned paths are resolved as `Path` objects for consistency and ease of use.
        """
        pass

    @abstractmethod
    def create(
        self
    ) -> 'IApplication':
        """
        Bootstrap and initialize the complete application framework.

        This method orchestrates the entire application startup process including
        configuration loading, service provider registration and booting, framework
        kernel initialization, and logging setup. It ensures the application is
        fully prepared for operation and prevents duplicate initialization.

        Returns
        -------
        Application
            The current application instance to enable method chaining.

        Notes
        -----
        The bootstrap process follows this sequence:
        1. Load and process all configuration from configurators
        2. Register core framework service providers
        3. Register and boot all service providers
        4. Initialize framework kernels
        5. Mark application as booted to prevent re-initialization

        This method is idempotent - calling it multiple times will not cause
        duplicate initialization. The startup time is calculated and logged
        for performance monitoring purposes.
        """
        pass

    @abstractmethod
    def isProduction(
        self
    ) -> bool:
        """
        Check if the application is running in a production environment.

        This method determines whether the current application environment is set to 'production'.
        It checks the 'app.env' configuration value to make this determination.

        Returns
        -------
        bool
            True if the application environment is 'production', False otherwise.

        Raises
        ------
        OrionisRuntimeError
            If the application configuration has not been initialized (i.e., if `create()` has not been called).

        Notes
        -----
        The environment is typically defined in the application configuration and can be set to values such as 'development', 'testing', or 'production'.
        This method is useful for conditionally executing code based on the environment, such as enabling/disabling debug features or logging verbosity.
        """
        pass

    @abstractmethod
    def isDebug(
        self
    ) -> bool:
        """
        Check if the application is running in debug mode.

        This method determines whether the current application is set to run in debug mode.
        It checks the 'app.debug' configuration value to make this determination.

        Returns
        -------
        bool
            True if the application is in debug mode, False otherwise.

        Raises
        ------
        OrionisRuntimeError
            If the application configuration has not been initialized (i.e., if `create()` has not been called).

        Notes
        -----
        The debug mode is typically defined in the application configuration and can be enabled or disabled based on the environment or specific settings.
        This method is useful for conditionally executing code based on whether debugging features should be active, such as detailed error reporting or verbose logging.
        """
        pass