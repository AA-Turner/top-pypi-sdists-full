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
        Initialize the ServiceProvider with the application container.

        Parameters
        ----------
        app : IApplication
            The application container instance.
        """
        self.app = app

    async def register(self) -> None:
        """
        Register services and components into the application container.

        This method must be implemented by subclasses to bind services,
        configurations, or other components to the application container.

        Raises
        ------
        NotImplementedError
            If the method is not overridden in a subclass.
        """
        raise NotImplementedError("This method should be overridden in the subclass")

    async def boot(self) -> None:
        """
        Perform post-registration initialization or bootstrapping.

        This method is called after all services have been registered.
        Override this method to initialize services, set up event listeners,
        or perform other boot-time operations.
        """
        pass
