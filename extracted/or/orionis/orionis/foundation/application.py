import asyncio
import time
from pathlib import Path
from typing import Any, List, Type, Dict
from orionis.console.contracts.base_scheduler import IBaseScheduler
from orionis.console.base.scheduler import BaseScheduler
from orionis.container.container import Container
from orionis.container.contracts.service_provider import IServiceProvider
from orionis.failure.base.handler import BaseExceptionHandler
from orionis.failure.contracts.handler import IBaseExceptionHandler
from orionis.foundation.config.app.entities.app import App
from orionis.foundation.config.auth.entities.auth import Auth
from orionis.foundation.config.cache.entities.cache import Cache
from orionis.foundation.config.cors.entities.cors import Cors
from orionis.foundation.config.database.entities.database import Database
from orionis.foundation.config.filesystems.entitites.filesystems import Filesystems
from orionis.foundation.config.logging.entities.logging import Logging
from orionis.foundation.config.mail.entities.mail import Mail
from orionis.foundation.config.queue.entities.queue import Queue
from orionis.foundation.config.roots.paths import Paths
from orionis.foundation.config.session.entities.session import Session
from orionis.foundation.config.startup import Configuration
from orionis.foundation.config.testing.entities.testing import Testing
from orionis.foundation.contracts.application import IApplication
from orionis.foundation.exceptions import OrionisTypeError, OrionisRuntimeError, OrionisValueError
from orionis.services.asynchrony.coroutines import Coroutine
from orionis.services.log.contracts.log_service import ILogger

class Application(Container, IApplication):
    """
    Main application container that manages the complete application lifecycle.

    This class extends the Container to provide comprehensive application-level
    functionality including service provider registration and bootstrapping, kernel
    management, configuration handling, and application initialization. It implements
    a fluent interface pattern to enable method chaining for configuration setup.

    The Application class serves as the central orchestrator for the Orionis framework,
    managing the loading and booting of service providers, framework kernels, and
    various configuration subsystems such as authentication, caching, database,
    logging, and more.

    Attributes
    ----------
    isBooted : bool
        Read-only property indicating whether the application providers have been booted.
    startAt : int
        Read-only property containing the timestamp when the application was started.
    """

    @property
    def isBooted(
        self
    ) -> bool:
        """
        Determine whether the application service providers have been booted.

        Returns
        -------
        bool
            True if all service providers have been successfully booted and the
            application is ready for use, False otherwise.
        """
        return self.__booted

    @property
    def startAt(
        self
    ) -> int:
        """
        Retrieve the application startup timestamp.

        Returns
        -------
        int
            The timestamp in nanoseconds since Unix epoch when the application
            instance was initialized.
        """
        return self.__startAt

    def __init__(
        self
    ) -> None:
        """
        Initialize the Application container with default configuration.

        Sets up the initial application state including empty service providers list,
        configuration storage, and boot status. Implements singleton pattern to
        prevent multiple initializations of the same application instance.

        Notes
        -----
        The initialization process records the startup timestamp, initializes internal
        data structures for providers and configurators, and sets the application
        boot status to False until explicitly booted via the create() method.
        """

        # Initialize base container with application paths
        super().__init__()

        # Singleton pattern - prevent multiple initializations
        if not hasattr(self, '_Application__initialized'):

            # Start time in nanoseconds
            self.__startAt = time.time_ns()

            # Propierty to store service providers.
            self.__providers: List[IServiceProvider, Any] = []

            # Property to store configurators and paths
            self.__configurators : dict = {}

            # Property to indicate if the application has been booted
            self.__booted: bool = False

            # Property to store application configuration
            # This will be initialized with default values or from configurators
            self.__config: dict = {}

            # Property to store the scheduler instance
            self.__scheduler: BaseScheduler = None

            # Property to store the exception handler class
            self.__exception_handler: Type[BaseExceptionHandler] = None

            # Flag to prevent re-initialization
            self.__initialized = True

    # === Native Kernels and Providers for Orionis Framework ===
    # Responsible for loading the native kernels and service providers of the Orionis framework.
    # These kernels and providers are essential for the core functionality of the framework.
    # Private methods are used to load these native components, ensuring they cannot be modified externally.

    def __loadFrameworksKernel(
        self
    ) -> None:
        """
        Load and register essential framework kernels into the container.

        This method imports and instantiates core framework kernels including the
        TestKernel for testing functionality and KernelCLI for command-line interface
        operations. Each kernel is registered as a singleton instance in the
        application container for later retrieval and use.

        Notes
        -----
        This is a private method called during application bootstrapping to ensure
        core framework functionality is available before user-defined providers
        are loaded.
        """

        # Import core framework kernels
        from orionis.test.kernel import TestKernel, ITestKernel
        from orionis.console.kernel import KernelCLI, IKernelCLI

        # Core framework kernels
        core_kernels = {
            ITestKernel: TestKernel,
            IKernelCLI: KernelCLI
        }

        # Register each kernel instance
        for abstract, concrete in core_kernels.items():
            self.instance(
                abstract,
                concrete(self),
                alias=f"x-{abstract.__module__}.{abstract.__name__}"
            )

    def __loadFrameworkProviders(
        self
    ) -> None:
        """
        Load and register core framework service providers.

        This method imports and adds essential service providers required for
        framework operation including console functionality, dumping utilities,
        path resolution, progress bars, workers, logging, and testing capabilities.
        These providers form the foundation layer of the framework's service
        architecture.

        Notes
        -----
        This is a private method executed during application bootstrapping to
        ensure core framework services are available before any user-defined
        providers are registered.
        """
        # Import core framework providers
        from orionis.foundation.providers.catch_provider import CathcProvider
        from orionis.foundation.providers.cli_request_provider import CLRequestProvider
        from orionis.foundation.providers.console_provider import ConsoleProvider
        from orionis.foundation.providers.directory_provider import DirectoryProvider
        from orionis.foundation.providers.dumper_provider import DumperProvider
        from orionis.foundation.providers.executor_provider import ConsoleExecuteProvider
        from orionis.foundation.providers.inspirational_provider import InspirationalProvider
        from orionis.foundation.providers.logger_provider import LoggerProvider
        from orionis.foundation.providers.performance_counter_provider import PerformanceCounterProvider
        from orionis.foundation.providers.progress_bar_provider import ProgressBarProvider
        from orionis.foundation.providers.reactor_provider import ReactorProvider
        from orionis.foundation.providers.scheduler_provider import ScheduleProvider
        from orionis.foundation.providers.testing_provider import TestingProvider
        from orionis.foundation.providers.workers_provider import WorkersProvider

        # Core framework providers
        core_providers = [
            CathcProvider,
            CLRequestProvider,
            ConsoleProvider,
            DirectoryProvider,
            DumperProvider,
            ConsoleExecuteProvider,
            InspirationalProvider,
            LoggerProvider,
            PerformanceCounterProvider,
            ProgressBarProvider,
            ReactorProvider,
            ScheduleProvider,
            TestingProvider,
            WorkersProvider
        ]

        # Register each core provider
        for provider_cls in core_providers:
            self.addProvider(provider_cls)

    # === Service Provider Registration and Bootstrapping ===
    # These private methods enable developers to register and boot custom service providers.
    # Registration and booting are handled separately, ensuring a clear lifecycle for each provider.
    # Both methods are invoked automatically during application initialization.

    def withProviders(
        self,
        providers: List[Type[IServiceProvider]] = []
    ) -> 'Application':
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

        # Add each provider class
        for provider_cls in providers:

            # Register the provider
            self.addProvider(provider_cls)

        # Return self instance for method chaining
        return self

    def addProvider(
        self,
        provider: Type[IServiceProvider]
    ) -> 'Application':
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

        # Validate provider type
        if not isinstance(provider, type) or not issubclass(provider, IServiceProvider):
            raise OrionisTypeError(f"Expected IServiceProvider class, got {type(provider).__name__}")

        # Add the provider to the list
        if provider not in self.__providers:
            self.__providers.append(provider)

        # If already added, raise an error
        else:
            raise OrionisTypeError(f"Provider {provider.__name__} is already registered.")

        # Return self instance.
        return self

    def __registerProviders(
        self
    ) -> None:
        """
        Instantiate and register all service providers in the container.

        This method iterates through all added provider classes, instantiates them
        with the current application instance, and calls their register() method
        to bind services into the dependency injection container. Supports both
        synchronous and asynchronous registration methods.

        Notes
        -----
        This is a private method called during application bootstrapping. After
        registration, the providers list is updated to contain instantiated provider
        objects rather than class references. The method handles both coroutine
        and regular register methods using asyncio when necessary.
        """

        # Ensure providers list is empty before registration
        initialized_providers = []

        # Iterate over each provider and register it
        for provider in self.__providers:

            # Initialize the provider
            class_provider: IServiceProvider = provider(self)

            # Register the provider in the container
            # Check if register is a coroutine function
            if asyncio.iscoroutinefunction(class_provider.register):
                Coroutine(class_provider.register).run()
            else:
                class_provider.register()

            # Add the initialized provider to the list
            initialized_providers.append(class_provider)

        # Update the providers list with initialized providers
        self.__providers = initialized_providers

    def __bootProviders(
        self
    ) -> None:
        """
        Execute the boot process for all registered service providers.

        This method calls the boot() method on each instantiated service provider
        to initialize services after all providers have been registered. This
        two-phase process ensures all dependencies are available before any
        provider attempts to use them. Supports both synchronous and asynchronous
        boot methods.

        Notes
        -----
        This is a private method called during application bootstrapping after
        provider registration is complete. After booting, the providers list is
        deleted to prevent memory leaks since providers are no longer needed
        after initialization.
        """

        # Iterate over each provider and boot it
        for provider in self.__providers:

            # Ensure provider is initialized before calling boot
            if hasattr(provider, 'boot') and callable(getattr(provider, 'boot')):
                # Check if boot is a coroutine function
                if asyncio.iscoroutinefunction(provider.boot):
                    Coroutine(provider.boot).run()
                else:
                    provider.boot()

        # Remove the __providers attribute to prevent memory leaks
        if hasattr(self, '_Application__providers'):
            del self.__providers

    # === Application Skeleton Configuration Methods ===
    # The Orionis framework provides methods to configure each component of the application,
    # enabling the creation of fully customized application skeletons.
    # These configurator loading methods allow developers to tailor the architecture
    # for complex and unique application requirements, supporting advanced customization
    # of every subsystem as needed.

    def setExceptionHandler(
        self,
        handler: IBaseExceptionHandler
    ) -> 'Application':
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

        # Ensure the provided handler is a subclass of BaseExceptionHandler
        if not issubclass(handler, BaseExceptionHandler):
            raise OrionisTypeError(f"Expected BaseExceptionHandler subclass, got {type(handler).__name__}")

        # Store the handler class in the application for later use
        self.__exception_handler = handler

        # Return the application instance for method chaining
        return self

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

        # Check if an exception handler has been set
        if self.__exception_handler is None:

            # Return the default exception handler instance
            return self.make(BaseExceptionHandler)

        # Instantiate and return the registered exception handler
        return self.make(self.__exception_handler)

    def setScheduler(
        self,
        scheduler: IBaseScheduler
    ) -> 'Application':
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

        # Ensure the provided scheduler is a subclass of BaseScheduler
        if not issubclass(scheduler, BaseScheduler):
            raise OrionisTypeError(f"Expected BaseScheduler subclass, got {type(scheduler).__name__}")

        # Store the scheduler class in the application for later use
        self.__scheduler = scheduler

        # Return the application instance for method chaining
        return self

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

        # Check if a scheduler has been set
        if self.__scheduler is None:
            return BaseScheduler()

        # Return the registered scheduler instance
        return self.__scheduler()

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
    ) -> 'Application':
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

        # Convert dataclass instances to dictionaries
        from orionis.services.introspection.dataclass.extractor import extractor

        # Load app configurator
        if (isinstance(app, type) and issubclass(app, App)):
            app = extractor(app)
        if not isinstance(app, (App, dict)):
            raise OrionisTypeError(f"Expected App instance or dict, got {type(app).__name__}")
        self.loadConfigApp(app)

        # Load auth configurator
        if (isinstance(auth, type) and issubclass(auth, Auth)):
            auth = extractor(auth)
        if not isinstance(auth, (Auth, dict)):
            raise OrionisTypeError(f"Expected Auth instance or dict, got {type(auth).__name__}")
        self.loadConfigAuth(auth)

        # Load cache configurator
        if (isinstance(cache, type) and issubclass(cache, Cache)):
            cache = extractor(cache)
        if not isinstance(cache, (Cache, dict)):
            raise OrionisTypeError(f"Expected Cache instance or dict, got {type(cache).__name__}")
        self.loadConfigCache(cache)

        # Load cors configurator
        if (isinstance(cors, type) and issubclass(cors, Cors)):
            cors = extractor(cors)
        if not isinstance(cors, (Cors, dict)):
            raise OrionisTypeError(f"Expected Cors instance or dict, got {type(cors).__name__}")
        self.loadConfigCors(cors)

        # Load database configurator
        if (isinstance(database, type) and issubclass(database, Database)):
            database = extractor(database)
        if not isinstance(database, (Database, dict)):
            raise OrionisTypeError(f"Expected Database instance or dict, got {type(database).__name__}")
        self.loadConfigDatabase(database)

        # Load filesystems configurator
        if (isinstance(filesystems, type) and issubclass(filesystems, Filesystems)):
            filesystems = extractor(filesystems)
        if not isinstance(filesystems, (Filesystems, dict)):
            raise OrionisTypeError(f"Expected Filesystems instance or dict, got {type(filesystems).__name__}")
        self.loadConfigFilesystems(filesystems)

        # Load logging configurator
        if (isinstance(logging, type) and issubclass(logging, Logging)):
            logging = extractor(logging)
        if not isinstance(logging, (Logging, dict)):
            raise OrionisTypeError(f"Expected Logging instance or dict, got {type(logging).__name__}")
        self.loadConfigLogging(logging)

        # Load mail configurator
        if (isinstance(mail, type) and issubclass(mail, Mail)):
            mail = extractor(mail)
        if not isinstance(mail, (Mail, dict)):
            raise OrionisTypeError(f"Expected Mail instance or dict, got {type(mail).__name__}")
        self.loadConfigMail(mail)

        # Load paths configurator
        if (isinstance(path, type) and issubclass(path, Paths)):
            path = extractor(path)
        if not isinstance(path, (Paths, dict)):
            raise OrionisTypeError(f"Expected Paths instance or dict, got {type(path).__name__}")
        self.loadConfigPaths(path)

        # Load queue configurator
        if (isinstance(queue, type) and issubclass(queue, Queue)):
            queue = extractor(queue)
        if not isinstance(queue, (Queue, dict)):
            raise OrionisTypeError(f"Expected Queue instance or dict, got {type(queue).__name__}")
        self.loadConfigQueue(queue)

        # Load session configurator
        if (isinstance(session, type) and issubclass(session, Session)):
            session = extractor(session)
        if not isinstance(session, (Session, dict)):
            raise OrionisTypeError(f"Expected Session instance or dict, got {type(session).__name__}")
        self.loadConfigSession(session)

        # Load testing configurator
        if (isinstance(testing, type) and issubclass(testing, Testing)):
            testing = extractor(testing)
        if not isinstance(testing, (Testing, dict)):
            raise OrionisTypeError(f"Expected Testing instance or dict, got {type(testing).__name__}")
        self.loadConfigTesting(testing)

        # Return self instance for method chaining
        return self

    def setConfigApp(
        self,
        **app_config
    ) -> 'Application':
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

        # Create App instance with provided parameters
        app = App(**app_config)

        # Load configuration using App instance
        self.loadConfigApp(app)

        # Return the application instance for method chaining
        return self

    def loadConfigApp(
        self,
        app: App | dict
    ) -> 'Application':
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

        # Validate app type
        if not isinstance(app, (App, dict)):
            raise OrionisTypeError(f"Expected App instance or dict, got {type(app).__name__}")

        # If app is a dict, convert it to App instance
        if isinstance(app, dict):
            app = App(**app).toDict()
        elif isinstance(app, App):
            app = app.toDict()

        # Store the configuration
        self.__configurators['app'] = app

        # Return the application instance for method chaining
        return self

    def setConfigAuth(
        self,
        **auth_config
    ) -> 'Application':
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

        # Create Auth instance with provided parameters
        auth = Auth(**auth_config)

        # Load configuration using Auth instance
        self.loadConfigAuth(auth)

        # Return the application instance for method chaining
        return self

    def loadConfigAuth(
        self,
        auth: Auth | dict
    ) -> 'Application':
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

        # Validate auth type
        if not isinstance(auth, (Auth, dict)):
            raise OrionisTypeError(f"Expected Auth instance or dict, got {type(auth).__name__}")

        # If auth is a dict, convert it to Auth instance
        if isinstance(auth, dict):
            auth = Auth(**auth).toDict()
        elif isinstance(auth, Auth):
            auth = auth.toDict()

        # Store the configuration
        self.__configurators['auth'] = auth

        # Return the application instance for method chaining
        return self

    def setConfigCache(
        self,
        **cache_config
    ) -> 'Application':
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

        # Create Cache instance with provided parameters
        cache = Cache(**cache_config)

        # Load configuration using Cache instance
        self.loadConfigCache(cache)

        # Return the application instance for method chaining
        return self

    def loadConfigCache(
        self,
        cache: Cache | dict
    ) -> 'Application':
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

        # Validate cache type
        if not isinstance(cache, (Cache, dict)):
            raise OrionisTypeError(f"Expected Cache instance or dict, got {type(cache).__name__}")

        # If cache is a dict, convert it to Cache instance
        if isinstance(cache, dict):
            cache = Cache(**cache).toDict()
        elif isinstance(cache, Cache):
            cache = cache.toDict()

        # Store the configuration
        self.__configurators['cache'] = cache

        # Return the application instance for method chaining
        return self

    def setConfigCors(
        self,
        **cors_config
    ) -> 'Application':
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

        # Create Cors instance with provided parameters
        cors = Cors(**cors_config)

        # Load configuration using Cors instance
        self.loadConfigCors(cors)

        # Return the application instance for method chaining
        return self

    def loadConfigCors(
        self,
        cors: Cors | dict
    ) -> 'Application':
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

        # Validate cors type
        if not isinstance(cors, (Cors, dict)):
            raise OrionisTypeError(f"Expected Cors instance or dict, got {type(cors).__name__}")

        # If cors is a dict, convert it to Cors instance
        if isinstance(cors, dict):
            cors = Cors(**cors).toDict()
        elif isinstance(cors, Cors):
            cors = cors.toDict()

        # Store the configuration
        self.__configurators['cors'] = cors

        # Return the application instance for method chaining
        return self

    def setConfigDatabase(
        self,
        **database_config
    ) -> 'Application':
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

        # Create Database instance with provided parameters
        database = Database(**database_config)

        # Load configuration using Database instance
        self.loadConfigDatabase(database)

        # Return the application instance for method chaining
        return self

    def loadConfigDatabase(
        self,
        database: Database | dict
    ) -> 'Application':
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

        # Validate database type
        if not isinstance(database, (Database, dict)):
            raise OrionisTypeError(f"Expected Database instance or dict, got {type(database).__name__}")

        # If database is a dict, convert it to Database instance
        if isinstance(database, dict):
            database = Database(**database).toDict()
        elif isinstance(database, Database):
            database = database.toDict()

        # Store the configuration
        self.__configurators['database'] = database

        # Return the application instance for method chaining
        return self

    def setConfigFilesystems(
        self,
        **filesystems_config
    ) -> 'Application':
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

        # Create Filesystems instance with provided parameters
        filesystems = Filesystems(**filesystems_config)

        # Load configuration using Filesystems instance
        self.loadConfigFilesystems(filesystems)

        # Return the application instance for method chaining
        return self

    def loadConfigFilesystems(
        self,
        filesystems: Filesystems | dict
    ) -> 'Application':
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

        # Validate filesystems type
        if not isinstance(filesystems, (Filesystems, dict)):
            raise OrionisTypeError(f"Expected Filesystems instance or dict, got {type(filesystems).__name__}")

        # If filesystems is a dict, convert it to Filesystems instance
        if isinstance(filesystems, dict):
            filesystems = Filesystems(**filesystems).toDict()
        elif isinstance(filesystems, Filesystems):
            filesystems = filesystems.toDict()

        # Store the configuration
        self.__configurators['filesystems'] = filesystems

        # Return the application instance for method chaining
        return self

    def setConfigLogging(
        self,
        **logging_config
    ) -> 'Application':
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

        # Create Logging instance with provided parameters
        logging = Logging(**logging_config)

        # Load configuration using Logging instance
        self.loadConfigLogging(logging)

        # Return the application instance for method chaining
        return self

    def loadConfigLogging(
        self,
        logging: Logging | dict
    ) -> 'Application':
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

        # Validate logging type
        if not isinstance(logging, (Logging, dict)):
            raise OrionisTypeError(f"Expected Logging instance or dict, got {type(logging).__name__}")

        # If logging is a dict, convert it to Logging instance
        if isinstance(logging, dict):
            logging = Logging(**logging).toDict()
        elif isinstance(logging, Logging):
            logging = logging.toDict()

        # Store the configuration
        self.__configurators['logging'] = logging

        # Return the application instance for method chaining
        return self

    def setConfigMail(
        self,
        **mail_config
    ) -> 'Application':
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

        # Create Mail instance with provided parameters
        mail = Mail(**mail_config)

        # Load configuration using Mail instance
        self.loadConfigMail(mail)

        # Return the application instance for method chaining
        return self

    def loadConfigMail(
        self,
        mail: Mail | dict
    ) -> 'Application':
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

        # Validate mail type
        if not isinstance(mail, (Mail, dict)):
            raise OrionisTypeError(f"Expected Mail instance or dict, got {type(mail).__name__}")

        # If mail is a dict, convert it to Mail instance
        if isinstance(mail, dict):
            mail = Mail(**mail).toDict()
        elif isinstance(mail, Mail):
            mail = mail.toDict()

        # Store the configuration
        self.__configurators['mail'] = mail

        # Return the application instance for method chaining
        return self

    def setConfigQueue(
        self,
        **queue_config
    ) -> 'Application':
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

        # Create Queue instance with provided parameters
        queue = Queue(**queue_config)

        # Load configuration using Queue instance
        self.loadConfigQueue(queue)

        # Return the application instance for method chaining
        return self

    def loadConfigQueue(
        self,
        queue: Queue | dict
    ) -> 'Application':
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

        # Validate queue type
        if not isinstance(queue, (Queue, dict)):
            raise OrionisTypeError(f"Expected Queue instance or dict, got {type(queue).__name__}")

        # If queue is a dict, convert it to Queue instance
        if isinstance(queue, dict):
            queue = Queue(**queue).toDict()
        elif isinstance(queue, Queue):
            queue = queue.toDict()

        # Store the configuration
        self.__configurators['queue'] = queue

        # Return the application instance for method chaining
        return self

    def setConfigSession(
        self,
        **session_config
    ) -> 'Application':
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

        # Create Session instance with provided parameters
        session = Session(**session_config)

        # Load configuration using Session instance
        self.loadConfigSession(session)

        # Return the application instance for method chaining
        return self

    def loadConfigSession(
        self,
        session: Session | dict
    ) -> 'Application':
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

        # Validate session type
        if not isinstance(session, (Session, dict)):
            raise OrionisTypeError(f"Expected Session instance or dict, got {type(session).__name__}")

        # If session is a dict, convert it to Session instance
        if isinstance(session, dict):
            session = Session(**session).toDict()
        elif isinstance(session, Session):
            session = session.toDict()

        # Store the configuration
        self.__configurators['session'] = session

        # Return the application instance for method chaining
        return self

    def setConfigTesting(
        self,
        **testing_config
    ) -> 'Application':
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

        # Create Testing instance with provided parameters
        testing = Testing(**testing_config)

        # Load configuration using Testing instance
        self.loadConfigTesting(testing)

        # Return the application instance for method chaining
        return self

    def loadConfigTesting(
        self,
        testing: Testing | dict
    ) -> 'Application':
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

        # Validate testing type
        if not isinstance(testing, (Testing, dict)):
            raise OrionisTypeError(f"Expected Testing instance or dict, got {type(testing).__name__}")

        # If testing is a dict, convert it to Testing instance
        if isinstance(testing, dict):
            testing = Testing(**testing).toDict()
        elif isinstance(testing, Testing):
            testing = testing.toDict()

        # Store the configuration
        self.__configurators['testing'] = testing

        # Return the application instance for method chaining
        return self

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
    ) -> 'Application':
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

        self.__configurators['path'] = {
            'root': str(root),
            'app': str(app),
            'console': str(console),
            'exceptions': str(exceptions),
            'http': str(http),
            'models': str(models),
            'providers': str(providers),
            'notifications': str(notifications),
            'services': str(services),
            'jobs': str(jobs),
            'bootstrap': str(bootstrap),
            'config': str(config),
            'database': str(database),
            'resources': str(resources),
            'routes': str(routes),
            'storage': str(storage),
            'tests': str(tests)
        }

        return self

    def loadConfigPaths(
        self,
        paths: Paths | dict
    ) -> 'Application':
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

        # Validate paths type
        if not isinstance(paths, (Paths, dict)):
            raise OrionisTypeError(f"Expected Paths instance or dict, got {type(paths).__name__}")

        # If paths is a dict, convert it to Paths instance
        if isinstance(paths, dict):
            paths = Paths(**paths).toDict()
        elif isinstance(paths, Paths):
            paths = paths.toDict()

        # Store the configuration
        self.__configurators['path'] = paths

        # Return the application instance for method chaining
        return self

    def __loadConfig(
        self,
    ) -> None:
        """
        Initialize and load the application configuration from configurators.

        This private method processes all stored configurators and converts them
        into a unified configuration dictionary. If no custom configurators have
        been set, it initializes with default configuration values. The method
        handles the conversion from individual configurator instances to a flat
        configuration structure.

        Raises
        ------
        OrionisRuntimeError
            If an error occurs during configuration loading or processing.

        Notes
        -----
        This method is called automatically during application bootstrapping.
        After successful loading, the configurators storage is cleaned up to
        prevent memory leaks. The resulting configuration is stored in the
        __config attribute for later retrieval via config() method.
        """

        # Try to load the configuration
        try:

            # Check if configuration is a dictionary
            if not self.__config:

                # Initialize with default configuration
                if not self.__configurators:
                    self.__config = Configuration().toDict()

                # Convert configurators to a dictionary
                else:
                    self.__config = Configuration(**self.__configurators).toDict()

                # Remove __configurators ofter loading configuration
                if hasattr(self, '_Application__configurators'):
                    del self.__configurators

        except Exception as e:

            # Handle any exceptions during configuration loading
            raise OrionisRuntimeError(f"Failed to load application configuration: {str(e)}")

    # === Configuration Access Method ===
    # The config() method provides access to application configuration settings.
    # It supports dot notation for retrieving nested configuration values.
    # You can obtain a specific configuration value by providing a key,
    # or retrieve the entire configuration dictionary by omitting the key.

    def config(
        self,
        key: str = None
    ) -> Any:
        """
        Retrieve application configuration values using dot notation.

        This method provides access to the application's configuration settings,
        supporting retrieval of nested values using dot notation (e.g., "database.default").
        If a key is provided, the method returns the corresponding configuration value.
        If no key is provided, it returns the entire configuration dictionary, excluding
        path-related configuration (which should be accessed via the `path()` method).

        Parameters
        ----------
        key : str, optional
            The configuration key to retrieve, supporting dot notation for nested
            values (e.g., "database.default", "app.name"). If None, the method returns
            the entire configuration dictionary except for the 'path' configuration.
            Default is None.

        Returns
        -------
        Any
            If `key` is provided and found, returns the corresponding configuration value.
            If `key` is None, returns the entire configuration dictionary (excluding 'path').
            If the key is not found, returns None.

        Raises
        ------
        OrionisRuntimeError
            If the application configuration has not been initialized (i.e., if `create()`
            has not been called before accessing configuration).
        OrionisValueError
            If the provided `key` parameter is not a string type.

        Notes
        -----
        The method traverses nested configuration structures by splitting the key
        on dots and navigating through dictionary levels. Path configurations are
        excluded from full configuration returns and should be accessed via the
        `path()` method instead.
        """

        # Create a local copy of the configuration to avoid mutating the original
        if not hasattr(self, '_Application__runtime_config') or self.__runtime_config is None:
            self.__runtime_config = self.__config.copy()

        # Remove 'path' from the local copy to ensure path config is not returned here
        if 'path' in self.__runtime_config:
            del self.__runtime_config['path']

        # Ensure the application is booted before accessing configuration
        if not self.__runtime_config:
            raise OrionisRuntimeError(
                "Application configuration is not initialized. Please call create() before accessing configuration."
            )

        # If no key is provided, return the entire configuration (excluding 'path')
        if key is None:
            return self.__runtime_config

        # Ensure the key is a string
        if not isinstance(key, str):
            raise OrionisValueError(
                "Key must be a string. Use config() without arguments to retrieve the entire configuration."
            )

        # Split the key by dot notation to support nested access
        parts = key.split('.')

        # Start with the full config and traverse according to the key parts
        config_value = self.__runtime_config
        for part in parts:
            # If the part exists in the current config_value, go deeper
            if isinstance(config_value, dict) and part in config_value:
                config_value = config_value[part]
            else:
                # If any part is missing, return None
                return None

        # Return the final configuration value found
        return config_value

    # === Path Configuration Access Method ===
    # The path() method provides access to application path configurations.
    # It allows you to retrieve specific path configurations using dot notation.
    # If no key is provided, it returns the entire 'paths' configuration dictionary.

    def path(
        self,
        key: str = None
    ) -> Path | dict:
        """
        Retrieve application path configuration values using dot notation.

        Provides access to the application's path configuration, allowing retrieval of either a specific path value or the entire paths configuration dictionary. If a key is provided, the corresponding path is returned as a `Path` object. If no key is provided, a dictionary mapping all path configuration keys to their resolved `Path` objects is returned.

        Parameters
        ----------
        key : str, optional
            Dot-notated key specifying the path configuration to retrieve (e.g., "console", "storage.logs").
            If None, returns the entire paths configuration dictionary. Default is None.

        Returns
        -------
        Path or dict
            If `key` is provided and found, returns the resolved `Path` object for that key.
            If `key` is None, returns a dictionary mapping all path keys to their `Path` objects.
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

        # Create a local copy of the path configuration to avoid mutation
        if not hasattr(self, '_Application__runtime_path_config') or self.__runtime_path_config is None:
            self.__runtime_path_config = self.__config.get('path', {}).copy() if self.__config else {}

        # Ensure the application is booted before accessing configuration
        if not self.__runtime_path_config:
            raise OrionisRuntimeError(
                "Application configuration is not initialized. Please call create() before accessing path configuration."
            )

        # If no key is provided, return all paths as a dictionary of Path objects
        if key is None:
            path_resolved: Dict[str, Path] = {}
            for k, v in self.__runtime_path_config.items():
                # Convert each path string to a Path object
                path_resolved[k] = Path(v)
            return path_resolved

        # Ensure the key is a string
        if not isinstance(key, str):
            raise OrionisValueError(
                "Key must be a string. Use path() without arguments to get the entire paths configuration."
            )

        # Direct key match: return the resolved Path object if the key exists
        if key in self.__runtime_path_config:
            return Path(self.__runtime_path_config[key])

        # If the key is not found, return None
        return None

    # === Application Creation Method ===
    # The create() method is responsible for bootstrapping the application.
    # It loads the necessary providers and kernels, ensuring that the application
    # is ready for use. This method should be called once to initialize the application.

    def create(
        self
    ) -> 'Application':
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
        4. Initialize framework kernels (Testing, CLI)
        5. Log successful startup with timing information
        6. Mark application as booted to prevent re-initialization

        This method is idempotent - calling it multiple times will not cause
        duplicate initialization. The startup time is calculated and logged
        for performance monitoring purposes.
        """
        # Check if already booted
        if not self.__booted:

            # Register the application instance in the container
            self.instance(
                IApplication,
                self,
                alias=f"x-{IApplication.__module__}.{IApplication.__name__}",
                enforce_decoupling=None
            )

            # Load configuration if not already set
            self.__loadConfig()

            # Load framework providers and register them
            self.__loadFrameworkProviders()
            self.__registerProviders()
            self.__bootProviders()

            # Mark as booted
            self.__booted = True

            # Load core framework kernels with app booted
            self.__loadFrameworksKernel()

            # Retrieve logger and console instances from the container
            logger: ILogger = self.make(ILogger)

            # Calculate elapsed time in milliseconds since application start
            elapsed_ms = (time.time_ns() - self.startAt) // 1_000_000

            # Compose the boot message
            boot_message = f"Orionis Framework has been successfully booted. Startup time: {elapsed_ms} ms. Started at: {self.startAt} ns"

            # Log message to the logger
            logger.info(boot_message)

        # Return the application instance for method chaining
        return self

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

        # Retrieve the current application environment from configuration
        app_env = self.config('app.env')

        # Ensure the application is booted before accessing configuration
        if app_env is None:
            raise OrionisRuntimeError(
                "Application configuration is not initialized. Please call create() before checking the environment."
            )

        # Return True if the environment is 'production', otherwise False
        return str(app_env).lower() == 'production'