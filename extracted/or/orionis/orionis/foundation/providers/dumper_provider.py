from orionis.console.dumper.debug import Debug
from orionis.console.contracts.debug import IDebug
from orionis.container.providers.service_provider import ServiceProvider

class DumperProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the debug service in the application container.

        This method binds the `IDebug` interface to its concrete implementation, the `Debug` class,
        within the application's dependency injection container. The service is registered as
        transient, ensuring that a new instance is created each time it is requested. Additionally,
        an alias is assigned to the service for convenient retrieval throughout the application.

        This registration enables the application to resolve dependencies related to debugging,
        error reporting, and console diagnostics by referencing the interface or its alias.

        Returns
        -------
        None
            This method does not return any value. It performs side effects by modifying
            the application's service registry.
        """

        # Register the Debug service as a transient binding for the IDebug interface.
        # A new instance of Debug will be created each time it is requested.
        # The alias allows for easy retrieval of the service elsewhere in the application.
        self.app.transient(IDebug, Debug, alias=f"x-orionis.console.contracts.debug.IDebug")