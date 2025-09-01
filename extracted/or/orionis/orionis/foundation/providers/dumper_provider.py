from orionis.console.dumper.debug import Debug
from orionis.console.contracts.debug import IDebug
from orionis.container.providers.service_provider import ServiceProvider

class DumperProvider(ServiceProvider):
    """
    Service provider for registering debug and dumper services in the application container.

    This provider is responsible for binding debug-related interfaces to their concrete
    implementations within the application's dependency injection container. It enables
    comprehensive debug message printing, error reporting, console diagnostics, and
    data dumping functionality throughout the application.

    The provider follows the service provider pattern, ensuring that debug services
    are properly registered and available for dependency injection across all
    application components that require debugging capabilities.

    Attributes
    ----------
    app : Application
        The application container instance used for service registration and
        dependency injection management.

    Methods
    -------
    register() -> None
        Register the debug service interface binding in the application container.
    boot() -> None
        Perform any post-registration initialization tasks for the dumper services.

    Notes
    -----
    This provider registers services as transient, meaning new instances are created
    for each resolution request, ensuring isolated debugging contexts.
    """

    def register(self) -> None:
        """
        Register the debug service in the application container.

        This method binds the IDebug interface to its concrete implementation (Debug class)
        in the application's dependency injection container. The service is registered as
        transient, meaning a new instance will be created each time it is requested.
        The service is also assigned an alias for easy retrieval throughout the application.

        The registration enables the application to resolve debug-related dependencies
        and provides access to debugging, error reporting, and console diagnostic
        functionality via the registered alias.

        Returns
        -------
        None
            This method does not return any value. It performs side effects by
            modifying the application container's service registry.
        """

        self.app.transient(IDebug, Debug, alias=f"x-{IDebug.__module__}.{IDebug.__name__}")

    def boot(self) -> None:
        """
        Perform post-registration initialization for the dumper service provider.

        This method is called after all service providers have been registered
        in the application container. It provides an opportunity to perform
        additional setup, configuration, or initialization logic that depends
        on other services being available in the container.

        Currently, this method contains no implementation as the dumper service
        does not require any post-registration initialization. The debug service
        registration is sufficient and complete during the register() phase.

        Returns
        -------
        None
            This method does not return any value and performs no operations
            in the current implementation.
        """

        pass