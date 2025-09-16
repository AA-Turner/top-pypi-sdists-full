from orionis.console.output.console import Console
from orionis.console.contracts.console import IConsole
from orionis.container.providers.service_provider import ServiceProvider

class ConsoleProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the console output service within the application's dependency injection container.

        This method binds the `IConsole` interface to its concrete `Console` implementation,
        enabling console output functionality to be injected wherever required in the application.
        The service is registered as a transient dependency, ensuring that a new instance of
        `Console` is created each time the service is resolved from the container. The registration
        uses a predefined alias to maintain consistent service identification and facilitate
        straightforward service resolution throughout the framework.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs side effects by
            modifying the application's service container to register the console service.
        """

        # Register the IConsole interface to the Console implementation as a transient service.
        # This ensures a new Console instance is provided on each resolution.
        self.app.transient(IConsole, Console, alias="x-orionis.console.contracts.console.IConsole")