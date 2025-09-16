from orionis.console.contracts.cli_request import ICLIRequest
from orionis.console.request.cli_request import CLIRequest
from orionis.container.providers.service_provider import ServiceProvider

class CLRequestProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the CLI request services in the application container.

        This method binds the `ICLIRequest` interface to the `CLIRequest` implementation
        as a transient service within the application's dependency injection container.
        By registering this binding, any component that depends on `ICLIRequest` will
        receive a new instance of `CLIRequest` each time it is resolved. The binding is
        also associated with a specific alias for reference within the container.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs registration as a side effect.
        """

        # Bind the ICLIRequest interface to the CLIRequest implementation as a transient service.
        # Each resolution of ICLIRequest will provide a new CLIRequest instance.
        self.app.transient(ICLIRequest, CLIRequest, alias="x-orionis.console.contracts.cli_request.ICLIRequest")