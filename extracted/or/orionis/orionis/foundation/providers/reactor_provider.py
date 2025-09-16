from orionis.console.contracts.reactor import IReactor
from orionis.console.core.reactor import Reactor
from orionis.container.providers.service_provider import ServiceProvider

class ReactorProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the reactor management service in the application container.

        This method binds the `IReactor` interface to the `Reactor` implementation
        within the application's dependency injection container. The service is registered
        as a singleton, ensuring that the same `Reactor` instance is returned for every
        resolution. An alias is provided for convenient retrieval.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs service registration
            as a side effect on the application container.

        Notes
        -----
        - The `IReactor` interface is bound to the `Reactor` implementation.
        - The service is registered as a singleton, so only one instance of `Reactor`
          will exist throughout the application lifecycle.
        - The alias "x-orionis.console.contracts.reactor.IReactor" can be used to
          retrieve the service explicitly from the container.
        """

        # Register the Reactor service as a singleton in the application container.
        # This ensures only one instance of Reactor is created and shared.
        self.app.singleton(IReactor, Reactor, alias="x-orionis.console.contracts.reactor.IReactor")