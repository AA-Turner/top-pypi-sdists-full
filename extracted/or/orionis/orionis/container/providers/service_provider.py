from orionis.container.contracts.service_provider import IServiceProvider
from orionis.foundation.contracts.application import IApplication

class ServiceProvider(IServiceProvider):
    """
    Base service provider class for the Orionis framework.

    This class serves as a base for all service providers in the application.
    Service providers are responsible for registering components and services
    into the application container, and initializing them when needed.

    Parameters
    ----------
    app : IApplication
        The application container instance to which services will be registered.

    Notes
    -----
    All concrete service providers should inherit from this class and implement
    the `register` method at minimum.
    """

    def __init__(self, app: IApplication) -> None:
        """
        Initialize the service provider with the application container.

        Parameters
        ----------
        app : IApplication
            The application container instance.
        """
        self.app = app

    async def register(self) -> None:
        """
        Register services into the application container.

        This method must be implemented by all concrete service providers.
        It should bind services, configurations, or other components
        to the application container.

        Raises
        ------
        NotImplementedError
            If the method is not overridden in a subclass.
        """
        raise NotImplementedError("This method should be overridden in the subclass")

    async def boot(self) -> None:
        """
        Perform any post-registration bootstrapping or initialization.

        This method is called after all services have been registered.
        Override this method to initialize services, set up event listeners,
        or perform other boot-time operations.
        """
        pass