from orionis.container.contracts.service_provider import IServiceProvider
from orionis.foundation.contracts.application import IApplication

class ServiceProvider(IServiceProvider):
    """
    Base class for service providers in the Orionis framework.

    Service providers are responsible for registering and bootstrapping
    services and components into the application container.

    Parameters
    ----------
    app : IApplication
        The application container instance to which services will be registered.
    """

    def __init__(self, app: IApplication) -> None:
        """
        Initialize a new ServiceProvider instance with the given application container.

        Parameters
        ----------
        app : IApplication
            The application container instance to which this service provider will be attached.

        Returns
        -------
        None
            This constructor does not return a value.
        """

        # Store the application container instance for use in service registration and bootstrapping
        self.app = app

    async def register(self) -> None:
        """
        Register services and components into the application container.

        This asynchronous method should be implemented by subclasses to bind services,
        configurations, or other components to the application container. It is called
        during the application's service registration phase.

        Returns
        -------
        None
            This method does not return a value.

        Raises
        ------
        NotImplementedError
            If the method is not overridden in a subclass.
        """

        # Optionally overridden by subclasses to register services
        pass

    async def boot(self) -> None:
        """
        Perform post-registration initialization or bootstrapping tasks.

        This asynchronous method is called after all services have been registered.
        Subclasses may override this method to initialize services, set up event listeners,
        or perform other operations required at application boot time.

        Returns
        -------
        None
            This method does not return a value.
        """

        # Optionally overridden by subclasses to perform boot-time operations
        pass
