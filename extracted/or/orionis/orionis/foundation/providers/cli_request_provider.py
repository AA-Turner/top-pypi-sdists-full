from orionis.console.contracts.cli_request import ICLIRequest
from orionis.console.request.cli_request import CLIRequest
from orionis.container.providers.service_provider import ServiceProvider

class CLRequestProvider(ServiceProvider):
    """
    Service provider for registering CLI request services in the Orionis framework.

    This provider handles the registration and binding of CLI request interfaces
    to their concrete implementations within the application container.
    """

    def register(self) -> None:
        """
        Register CLI request services in the application container.

        Binds the ICLIRequest interface to the CLIRequest implementation as a
        transient service, making it available for dependency injection throughout
        the application with the specified alias.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Register CLIRequest as a transient service bound to ICLIRequest interface
        # Transient services create a new instance each time they are resolved
        self.app.transient(ICLIRequest, CLIRequest, alias=f"x-{ICLIRequest.__module__}.{ICLIRequest.__name__}")

    def boot(self) -> None:
        """
        Perform any necessary bootstrapping after service registration.

        This method is called after all services have been registered and can be
        used to perform additional setup or configuration tasks. Currently, no
        bootstrapping logic is required for CLI request services.

        Returns
        -------
        None
            This method does not return any value.
        """
        # No bootstrapping logic required for CLI request services
        pass