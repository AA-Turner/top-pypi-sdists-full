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
from orionis.services.log.contracts.log_service import ILogger
from orionis.support.wrapper.dataclass import DataClass

class Application(Container, IApplication):
    """
    Application: Main container that manages the complete lifecycle of the Orionis application.

    This class extends `Container` and acts as the central core of the Orionis framework,
    orchestrating initialization, configuration, registration, and bootstrapping of all
    application components and services. It follows a fluent interface pattern, enabling
    method chaining for clear and concise configuration.

    Key Responsibilities:
    ---------------------
    - Registers and boots both native and user-defined service providers, ensuring all
        dependencies and services are available throughout the application lifecycle.
    - Loads and manages essential framework kernels (CLI, testing, etc.), guaranteeing
        that core components are properly initialized and accessible.
    - Centralizes configuration management for all critical subsystems: authentication,
        cache, database, logging, mail, queue, routing, storage, session, testing, and more.
    - Provides methods for customizing and extending the application architecture,
        supporting dynamic configurator loading and seamless integration of additional services.
    - Implements mechanisms for custom exception handling and schedulers, enhancing
        robustness and flexibility across the application lifecycle.
    - Exposes utilities for accessing configuration and path settings using dot notation.

    Typical Workflow:
    -----------------
    1. Instantiate the Application class.
    2. Register providers and configurators via `withProviders` and `withConfigurators`.
    3. Optionally customize exception handlers and schedulers.
    4. Call `create()` to initialize and boot the application, loading kernels and providers.
    5. Access services, configuration, and paths through the Application instance.

    Attributes
    ----------
    isBooted : bool
            Read-only property indicating whether the application providers have been booted.
    startAt : int
            Read-only property containing the timestamp (epoch) when the application was started.
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
            self.instance(abstract, concrete(self), alias=f"x-{abstract.__module__}.{abstract.__name__}")

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

        This private method iterates through all service provider classes previously added to the application,
        instantiates each provider with the current application instance, and invokes their `register()` method
        to bind services into the dependency injection container. Both synchronous and asynchronous `register()`
        methods are supported and handled appropriately.

        After registration, the internal providers list is updated to contain the instantiated provider objects
        instead of class references. This ensures that subsequent booting operations are performed on the actual
        provider instances.

        Notes
        -----
        - This method is called automatically during application bootstrapping.
        - Handles both coroutine and regular `register()` methods using `asyncio` when necessary.
        - The providers list is updated in-place to hold provider instances.

        Returns
        -------
        None
            This method does not return any value. It updates the internal state of the application by
            replacing the provider class references with their instantiated objects.
        """

        # Prepare a list to hold initialized provider instances
        initialized_providers = []

        # Iterate over each provider class in the providers list
        for provider_cls in self.__providers:

            # Instantiate the provider with the current application instance
            provider_instance = provider_cls(self)

            # Retrieve the 'register' method if it exists
            register_method = getattr(provider_instance, 'register', None)

            # If the register method exists, call it
            if callable(register_method):

                # If the register method is a coroutine, run it asynchronously
                if asyncio.iscoroutinefunction(register_method):
                    asyncio.run(register_method())

                # Otherwise, call it synchronously
                else:
                    register_method()

            # Add the initialized provider instance to the list
            initialized_providers.append(provider_instance)

        # Replace the providers list with the list of initialized provider instances
        self.__providers = initialized_providers

    def __bootProviders(
        self
    ) -> None:
        """
        Boot all registered service providers after registration.

        This private method iterates through all instantiated service providers and calls their
        `boot()` method to perform any post-registration initialization. This two-phase approach
        ensures that all dependencies are registered before any provider attempts to use them.
        Both synchronous and asynchronous `boot()` methods are supported.

        After all providers have been booted, the internal providers list is cleared to free memory,
        as provider instances are no longer needed after initialization.

        Notes
        -----
        - This method is called automatically during application bootstrapping, after all providers
          have been registered.
        - Supports both synchronous and asynchronous `boot()` methods on providers.
        - The providers list is cleared after booting to prevent memory leaks.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Iterate over each initialized provider and call its boot method if available
        for provider in self.__providers:

            # Get the boot method if it exists
            boot_method = getattr(provider, 'boot', None)

            if callable(boot_method):

                # If the boot method is a coroutine, run it asynchronously
                if asyncio.iscoroutinefunction(boot_method):
                    asyncio.run(boot_method())

                # Otherwise, call it synchronously
                else:
                    boot_method()

        # Clear the providers list to free memory after booting is complete
        self.__providers.clear()

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
        cache: Cache | dict = Cache(),
        cors: Cors | dict = Cors(),
        database: Database | dict = Database(),
        filesystems: Filesystems | dict = Filesystems(),
        logging: Logging | dict = Logging(),
        mail: Mail | dict = Mail(),
        path: Paths | dict = Paths(),
        queue: Queue | dict = Queue(),
        session: Session | dict = Session(),
        testing: Testing | dict = Testing()
    ) -> 'Application':
        """
        Configure all major application subsystems using configuration entities or dictionaries.

        This method provides a centralized interface for setting up the application's
        configuration by accepting configuration objects or dictionaries for each major
        subsystem. Each configurator parameter corresponds to a specific aspect of the
        application, such as authentication, caching, database, logging, mail, paths,
        queue, session, and testing. The method validates and loads each configurator
        into the application's configuration system.

        Parameters
        ----------
        app : App or dict, optional
            Application-level configuration (e.g., name, environment, debug settings).
            Defaults to a new App() instance.
        auth : Auth or dict, optional
            Authentication configuration (e.g., guards, providers, password settings).
            Defaults to a new Auth() instance.
        cache : Cache or dict, optional
            Caching configuration (e.g., default store, prefix, driver options).
            Defaults to a new Cache() instance.
        cors : Cors or dict, optional
            CORS configuration (e.g., allowed origins, methods, headers).
            Defaults to a new Cors() instance.
        database : Database or dict, optional
            Database configuration (e.g., connections, migration settings).
            Defaults to a new Database() instance.
        filesystems : Filesystems or dict, optional
            Filesystem configuration (e.g., disks, cloud storage).
            Defaults to a new Filesystems() instance.
        logging : Logging or dict, optional
            Logging configuration (e.g., channels, levels).
            Defaults to a new Logging() instance.
        mail : Mail or dict, optional
            Mail configuration (e.g., mailers, transport settings).
            Defaults to a new Mail() instance.
        path : Paths or dict, optional
            Application path configuration (e.g., directories for components).
            Defaults to a new Paths() instance.
        queue : Queue or dict, optional
            Queue configuration (e.g., connections, worker settings).
            Defaults to a new Queue() instance.
        session : Session or dict, optional
            Session configuration (e.g., driver, lifetime, encryption).
            Defaults to a new Session() instance.
        testing : Testing or dict, optional
            Testing configuration (e.g., database, environment variables).
            Defaults to a new Testing() instance.

        Returns
        -------
        Application
            The current Application instance, allowing for method chaining.

        Raises
        ------
        OrionisTypeError
            If any configurator parameter is not an instance of its expected type
            or a dictionary convertible to the expected type.

        Notes
        -----
        - Each configurator is validated and loaded using its corresponding load method.
        - This method does not perform deep validation of the contents of each configurator.
        - The method returns the Application instance itself for fluent chaining.
        """

        # Load each configurator into the application's configuration system.
        self.loadConfigApp(app)                 # Load application-level configuration
        self.loadConfigAuth(auth)               # Load authentication configuration
        self.loadConfigCache(cache)             # Load cache configuration
        self.loadConfigCors(cors)               # Load CORS configuration
        self.loadConfigDatabase(database)       # Load database configuration
        self.loadConfigFilesystems(filesystems) # Load filesystems configuration
        self.loadConfigLogging(logging)         # Load logging configuration
        self.loadConfigMail(mail)               # Load mail configuration
        self.loadConfigPaths(path)              # Load path configuration
        self.loadConfigQueue(queue)             # Load queue configuration
        self.loadConfigSession(session)         # Load session configuration
        self.loadConfigTesting(testing)         # Load testing configuration

        # Return self for method chaining
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

        # Load configuration using App instance
        self.loadConfigApp(**app_config)

        # Return the application instance for method chaining
        return self

    def loadConfigApp(
        self,
        app: App | dict
    ) -> 'Application':
        """
        Load and store the application configuration from an `App` instance or dictionary.

        This method validates and stores the application-level configuration in the internal
        configurators dictionary. If a dictionary is provided, it is converted to an `App`
        instance before storage. The configuration is always stored as a dictionary representation
        of the `App` dataclass.

        Parameters
        ----------
        app : App or dict
            The application configuration, either as an `App` instance or a dictionary
            containing configuration parameters compatible with the `App` dataclass.

        Returns
        -------
        Application
            The current `Application` instance, enabling method chaining.

        Raises
        ------
        OrionisTypeError
            If the `app` parameter is not an instance of `App`, a subclass of `App`, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the `DataClass` wrapper.
        - If a dictionary is provided, it is unpacked into an `App` instance.
        - The resulting configuration is stored in the internal configurators under the 'app' key.
        - The method always returns the current `Application` instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(app, type) and issubclass(app, App)):
            _app = DataClass(App).fromDataclass(app).toDict()

        # Convert dictionary to App instance, then to dict
        elif isinstance(app, dict):
            _app = App(**app).toDict()

        # Convert App instance to dict
        elif isinstance(app, App):
            _app = app.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected App instance or dict, got {type(app).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['app'] = _app

        # Return self for method chaining
        return self

    def setConfigAuth(
        self,
        **auth_config
    ) -> 'Application':
        """
        Configure the authentication subsystem using keyword arguments.

        This method allows you to set authentication configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct an `Auth` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **auth_config : dict
            Keyword arguments representing authentication configuration options.
            These must match the field names and types expected by the `Auth` dataclass
            from `orionis.foundation.config.auth.entities.auth.Auth`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates an `Auth` instance from the provided keyword
          arguments and then calls `loadConfigAuth()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load authentication configuration using provided keyword arguments
        self.loadConfigAuth(**auth_config)

        # Return the application instance for method chaining
        return self

    def loadConfigAuth(
        self,
        auth: Auth | dict
    ) -> 'Application':
        """
        Load and store authentication configuration from an Auth instance or dictionary.

        This method validates and stores the authentication configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to an
        Auth instance before being stored. The configuration is always stored as a dictionary
        representation of the Auth dataclass.

        Parameters
        ----------
        auth : Auth or dict
            The authentication configuration, either as an Auth instance or a dictionary
            containing parameters compatible with the Auth dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `auth` parameter is not an instance of Auth, a subclass of Auth, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into an Auth instance.
        - The resulting configuration is stored in the internal configurators under the 'auth' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(auth, type) and issubclass(auth, Auth)):
            _auth = DataClass(Auth).fromDataclass(auth).toDict()

        # Convert dictionary to Auth instance, then to dict
        elif isinstance(auth, dict):
            _auth = Auth(**auth).toDict()

        # Convert Auth instance to dict
        elif isinstance(auth, Auth):
            _auth = auth.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Auth instance or dict, got {type(auth).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['auth'] = _auth

        # Return self for method chaining
        return self

    def setConfigCache(
        self,
        **cache_config
    ) -> 'Application':
        """
        Configure the cache subsystem using keyword arguments.

        This method allows you to set cache configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Cache` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **cache_config : dict
            Keyword arguments representing cache configuration options.
            These must match the field names and types expected by the `Cache` dataclass
            from `orionis.foundation.config.cache.entities.cache.Cache`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Cache` instance from the provided keyword
          arguments and then calls `loadConfigCache()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load cache configuration using provided keyword arguments
        self.loadConfigCache(**cache_config)

        # Return the application instance for method chaining
        return self

    def loadConfigCache(
        self,
        cache: Cache | dict
    ) -> 'Application':
        """
        Load and store cache configuration from a Cache instance or dictionary.

        This method validates and stores the cache configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Cache instance before being stored. The configuration is always stored as a dictionary
        representation of the Cache dataclass.

        Parameters
        ----------
        cache : Cache or dict
            The cache configuration, either as a Cache instance or a dictionary
            containing parameters compatible with the Cache dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `cache` parameter is not an instance of Cache, a subclass of Cache, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Cache instance.
        - The resulting configuration is stored in the internal configurators under the 'cache' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(cache, type) and issubclass(cache, Cache)):
            _cache = DataClass(Cache).fromDataclass(cache).toDict()

        # Convert dictionary to Cache instance, then to dict
        elif isinstance(cache, dict):
            _cache = Cache(**cache).toDict()

        # Convert Cache instance to dict
        elif isinstance(cache, Cache):
            _cache = cache.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Cache instance or dict, got {type(cache).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['cache'] = _cache

        # Return self for method chaining
        return self

    def setConfigCors(
        self,
        **cors_config
    ) -> 'Application':
        """
        Configure the CORS subsystem using keyword arguments.

        This method allows you to set CORS configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Cors` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **cors_config : dict
            Keyword arguments representing CORS configuration options.
            These must match the field names and types expected by the `Cors` dataclass
            from `orionis.foundation.config.cors.entities.cors.Cors`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Cors` instance from the provided keyword
          arguments and then calls `loadConfigCors()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load CORS configuration using provided keyword arguments
        self.loadConfigCors(**cors_config)

        # Return the application instance for method chaining
        return self

    def loadConfigCors(
        self,
        cors: Cors | dict
    ) -> 'Application':
        """
        Load and store CORS configuration from a Cors instance or dictionary.

        This method validates and stores the CORS configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Cors instance before being stored. The configuration is always stored as a dictionary
        representation of the Cors dataclass.

        Parameters
        ----------
        cors : Cors or dict
            The CORS configuration, either as a Cors instance or a dictionary
            containing parameters compatible with the Cors dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `cors` parameter is not an instance of Cors, a subclass of Cors, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Cors instance.
        - The resulting configuration is stored in the internal configurators under the 'cors' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(cors, type) and issubclass(cors, Cors)):
            _cors = DataClass(Cors).fromDataclass(cors).toDict()

        # Convert dictionary to Cors instance, then to dict
        elif isinstance(cors, dict):
            _cors = Cors(**cors).toDict()

        # Convert Cors instance to dict
        elif isinstance(cors, Cors):
            _cors = cors.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Cors instance or dict, got {type(cors).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['cors'] = _cors

        # Return self for method chaining
        return self

    def setConfigDatabase(
        self,
        **database_config
    ) -> 'Application':
        """
        Configure the database subsystem using keyword arguments.

        This method allows you to set database configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Database` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **database_config : dict
            Keyword arguments representing database configuration options.
            These must match the field names and types expected by the `Database` dataclass
            from `orionis.foundation.config.database.entities.database.Database`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Database` instance from the provided keyword
          arguments and then calls `loadConfigDatabase()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load database configuration using provided keyword arguments
        self.loadConfigDatabase(**database_config)

        # Return the application instance for method chaining
        return self

    def loadConfigDatabase(
        self,
        database: Database | dict
    ) -> 'Application':
        """
        Load and store database configuration from a Database instance or dictionary.

        This method validates and stores the database configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Database instance before being stored. The configuration is always stored as a dictionary
        representation of the Database dataclass.

        Parameters
        ----------
        database : Database or dict
            The database configuration, either as a Database instance or a dictionary
            containing parameters compatible with the Database dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `database` parameter is not an instance of Database, a subclass of Database, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Database instance.
        - The resulting configuration is stored in the internal configurators under the 'database' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(database, type) and issubclass(database, Database)):
            _database = DataClass(Database).fromDataclass(database).toDict()

        # Convert dictionary to Database instance, then to dict
        elif isinstance(database, dict):
            _database = Database(**database).toDict()

        # Convert Database instance to dict
        elif isinstance(database, Database):
            _database = database.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Database instance or dict, got {type(database).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['database'] = _database

        # Return self for method chaining
        return self

    def setConfigFilesystems(
        self,
        **filesystems_config
    ) -> 'Application':
        """
        Configure the filesystems subsystem using keyword arguments.

        This method allows you to set filesystems configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Filesystems` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **filesystems_config : dict
            Keyword arguments representing filesystems configuration options.
            These must match the field names and types expected by the `Filesystems` dataclass
            from `orionis.foundation.config.filesystems.entitites.filesystems.Filesystems`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Filesystems` instance from the provided keyword
          arguments and then calls `loadConfigFilesystems()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load filesystems configuration using provided keyword arguments
        self.loadConfigFilesystems(**filesystems_config)

        # Return the application instance for method chaining
        return self

    def loadConfigFilesystems(
        self,
        filesystems: Filesystems | dict
    ) -> 'Application':
        """
        Load and store filesystems configuration from a Filesystems instance or dictionary.

        This method validates and stores the filesystems configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Filesystems instance before being stored. The configuration is always stored as a dictionary
        representation of the Filesystems dataclass.

        Parameters
        ----------
        filesystems : Filesystems or dict
            The filesystems configuration, either as a Filesystems instance or a dictionary
            containing parameters compatible with the Filesystems dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `filesystems` parameter is not an instance of Filesystems, a subclass of Filesystems, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Filesystems instance.
        - The resulting configuration is stored in the internal configurators under the 'filesystems' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(filesystems, type) and issubclass(filesystems, Filesystems)):
            _filesystems = DataClass(Filesystems).fromDataclass(filesystems).toDict()

        # Convert dictionary to Filesystems instance, then to dict
        elif isinstance(filesystems, dict):
            _filesystems = Filesystems(**filesystems).toDict()

        # Convert Filesystems instance to dict
        elif isinstance(filesystems, Filesystems):
            _filesystems = filesystems.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Filesystems instance or dict, got {type(filesystems).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['filesystems'] = _filesystems

        # Return self for method chaining
        return self

    def setConfigLogging(
        self,
        **logging_config
    ) -> 'Application':
        """
        Configure the logging subsystem using keyword arguments.

        This method allows you to set logging configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Logging` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **logging_config : dict
            Keyword arguments representing logging configuration options.
            These must match the field names and types expected by the `Logging` dataclass
            from `orionis.foundation.config.logging.entities.logging.Logging`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Logging` instance from the provided keyword
          arguments and then calls `loadConfigLogging()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load logging configuration using provided keyword arguments
        self.loadConfigLogging(**logging_config)

        # Return the application instance for method chaining
        return self

    def loadConfigLogging(
        self,
        logging: Logging | dict
    ) -> 'Application':
        """
        Load and store logging configuration from a Logging instance or dictionary.

        This method validates and stores the logging configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Logging instance before being stored. The configuration is always stored as a dictionary
        representation of the Logging dataclass.

        Parameters
        ----------
        logging : Logging or dict
            The logging configuration, either as a Logging instance or a dictionary
            containing parameters compatible with the Logging dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `logging` parameter is not an instance of Logging, a subclass of Logging, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Logging instance.
        - The resulting configuration is stored in the internal configurators under the 'logging' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(logging, type) and issubclass(logging, Logging)):
            _logging = DataClass(Logging).fromDataclass(logging).toDict()

        # Convert dictionary to Logging instance, then to dict
        elif isinstance(logging, dict):
            _logging = Logging(**logging).toDict()

        # Convert Logging instance to dict
        elif isinstance(logging, Logging):
            _logging = logging.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Logging instance or dict, got {type(logging).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['logging'] = _logging

        # Return self for method chaining
        return self

    def setConfigMail(
        self,
        **mail_config
    ) -> 'Application':
        """
        Configure the mail subsystem using keyword arguments.

        This method allows you to set mail configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Mail` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **mail_config : dict
            Keyword arguments representing mail configuration options.
            These must match the field names and types expected by the `Mail` dataclass
            from `orionis.foundation.config.mail.entities.mail.Mail`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Mail` instance from the provided keyword
          arguments and then calls `loadConfigMail()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load mail configuration using provided keyword arguments
        self.loadConfigMail(**mail_config)

        # Return the application instance for method chaining
        return self

    def loadConfigMail(
        self,
        mail: Mail | dict
    ) -> 'Application':
        """
        Load and store mail configuration from a Mail instance or dictionary.

        This method validates and stores the mail configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Mail instance before being stored. The configuration is always stored as a dictionary
        representation of the Mail dataclass.

        Parameters
        ----------
        mail : Mail or dict
            The mail configuration, either as a Mail instance or a dictionary
            containing parameters compatible with the Mail dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `mail` parameter is not an instance of Mail, a subclass of Mail, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Mail instance.
        - The resulting configuration is stored in the internal configurators under the 'mail' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(mail, type) and issubclass(mail, Mail)):
            _mail = DataClass(Mail).fromDataclass(mail).toDict()

        # Convert dictionary to Mail instance, then to dict
        elif isinstance(mail, dict):
            _mail = Mail(**mail).toDict()

        # Convert Mail instance to dict
        elif isinstance(mail, Mail):
            _mail = mail.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Mail instance or dict, got {type(mail).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['mail'] = _mail

        # Return self for method chaining
        return self

    def setConfigQueue(
        self,
        **queue_config
    ) -> 'Application':
        """
        Configure the queue subsystem using keyword arguments.

        This method allows you to set queue configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Queue` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **queue_config : dict
            Keyword arguments representing queue configuration options.
            These must match the field names and types expected by the `Queue` dataclass
            from `orionis.foundation.config.queue.entities.queue.Queue`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Queue` instance from the provided keyword
          arguments and then calls `loadConfigQueue()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load queue configuration using provided keyword arguments
        self.loadConfigQueue(**queue_config)

        # Return the application instance for method chaining
        return self

    def loadConfigQueue(
        self,
        queue: Queue | dict
    ) -> 'Application':
        """
        Load and store queue configuration from a Queue instance or dictionary.

        This method validates and stores the queue configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Queue instance before being stored. The configuration is always stored as a dictionary
        representation of the Queue dataclass.

        Parameters
        ----------
        queue : Queue or dict
            The queue configuration, either as a Queue instance or a dictionary
            containing parameters compatible with the Queue dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `queue` parameter is not an instance of Queue, a subclass of Queue, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Queue instance.
        - The resulting configuration is stored in the internal configurators under the 'queue' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(queue, type) and issubclass(queue, Queue)):
            _queue = DataClass(Queue).fromDataclass(queue).toDict()

        # Convert dictionary to Queue instance, then to dict
        elif isinstance(queue, dict):
            _queue = Queue(**queue).toDict()

        # Convert Queue instance to dict
        elif isinstance(queue, Queue):
            _queue = queue.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Queue instance or dict, got {type(queue).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['queue'] = _queue

        # Return self for method chaining
        return self

    def setConfigSession(
        self,
        **session_config
    ) -> 'Application':
        """
        Configure the session subsystem using keyword arguments.

        This method allows you to set session configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Session` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **session_config : dict
            Keyword arguments representing session configuration options.
            These must match the field names and types expected by the `Session` dataclass
            from `orionis.foundation.config.session.entities.session.Session`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Session` instance from the provided keyword
          arguments and then calls `loadConfigSession()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load session configuration using provided keyword arguments
        self.loadConfigSession(**session_config)

        # Return the application instance for method chaining
        return self

    def loadConfigSession(
        self,
        session: Session | dict
    ) -> 'Application':
        """
        Load and store session configuration from a Session instance or dictionary.

        This method validates and stores the session configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Session instance before being stored. The configuration is always stored as a dictionary
        representation of the Session dataclass.

        Parameters
        ----------
        session : Session or dict
            The session configuration, either as a Session instance or a dictionary
            containing parameters compatible with the Session dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `session` parameter is not an instance of Session, a subclass of Session, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Session instance.
        - The resulting configuration is stored in the internal configurators under the 'session' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(session, type) and issubclass(session, Session)):
            _session = DataClass(Session).fromDataclass(session).toDict()

        # Convert dictionary to Session instance, then to dict
        elif isinstance(session, dict):
            _session = Session(**session).toDict()

        # Convert Session instance to dict
        elif isinstance(session, Session):
            _session = session.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Session instance or dict, got {type(session).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['session'] = _session

        # Return self for method chaining
        return self

    def setConfigTesting(
        self,
        **testing_config
    ) -> 'Application':
        """
        Configure the testing subsystem using keyword arguments.

        This method allows you to set testing configuration for the application
        by passing individual configuration parameters as keyword arguments. The provided
        parameters are used to construct a `Testing` configuration instance, which is then
        loaded into the application's internal configurators.

        Parameters
        ----------
        **testing_config : dict
            Keyword arguments representing testing configuration options.
            These must match the field names and types expected by the `Testing` dataclass
            from `orionis.foundation.config.testing.entities.testing.Testing`.

        Returns
        -------
        Application
            Returns the current `Application` instance to enable method chaining.

        Notes
        -----
        - This method internally creates a `Testing` instance from the provided keyword
          arguments and then calls `loadConfigTesting()` to store the configuration.
        - The configuration is validated and stored for use during application bootstrapping.
        """

        # Load testing configuration using provided keyword arguments
        self.loadConfigTesting(**testing_config)

        # Return the application instance for method chaining
        return self

    def loadConfigTesting(
        self,
        testing: Testing | dict
    ) -> 'Application':
        """
        Load and store testing configuration from a Testing instance or dictionary.

        This method validates and stores the testing configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Testing instance before being stored. The configuration is always stored as a dictionary
        representation of the Testing dataclass.

        Parameters
        ----------
        testing : Testing or dict
            The testing configuration, either as a Testing instance or a dictionary
            containing parameters compatible with the Testing dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `testing` parameter is not an instance of Testing, a subclass of Testing, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Testing instance.
        - The resulting configuration is stored in the internal configurators under the 'testing' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(testing, type) and issubclass(testing, Testing)):
            _testing = DataClass(Testing).fromDataclass(testing).toDict()

        # Convert dictionary to Testing instance, then to dict
        elif isinstance(testing, dict):
            _testing = Testing(**testing).toDict()

        # Convert Testing instance to dict
        elif isinstance(testing, Testing):
            _testing = testing.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Testing instance or dict, got {type(testing).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['testing'] = _testing

        # Return self for method chaining
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

        This method validates and stores the path configuration in the application's
        internal configurators dictionary. If a dictionary is provided, it is converted to a
        Paths instance before being stored. The configuration is always stored as a dictionary
        representation of the Paths dataclass.

        Parameters
        ----------
        paths : Paths or dict
            The path configuration, either as a Paths instance or a dictionary
            containing parameters compatible with the Paths dataclass.

        Returns
        -------
        Application
            The current Application instance, enabling method chaining. This allows further
            configuration or initialization calls to be chained after this method.

        Raises
        ------
        OrionisTypeError
            If the `paths` parameter is not an instance of Paths, a subclass of Paths, or a dictionary.

        Notes
        -----
        - If a class type is provided, it is converted using the DataClass wrapper.
        - If a dictionary is provided, it is unpacked into a Paths instance.
        - The resulting configuration is stored in the internal configurators under the 'path' key.
        - The method always returns the current Application instance.
        """

        # Convert class type to dict using DataClass wrapper
        if (isinstance(paths, type) and issubclass(paths, Paths)):
            _paths = DataClass(Paths).fromDataclass(paths).toDict()

        # Convert dictionary to Paths instance, then to dict
        elif isinstance(paths, dict):
            _paths = Paths(**paths).toDict()

        # Convert Paths instance to dict
        elif isinstance(paths, Paths):
            _paths = paths.toDict()

        # Raise error if type is invalid
        else:
            raise OrionisTypeError(f"Expected Paths instance or dict, got {type(paths).__name__}")

        # Store the configuration dictionary in internal configurators
        self.__configurators['path'] = _paths

        # Return self for method chaining
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

                # Assign the configurators to config and clean up
                else:
                    self.__config = self.__configurators
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