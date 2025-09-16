from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.system.contracts.workers import IWorkers
from orionis.services.system.workers import Workers

class WorkersProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the worker management service in the application container.

        This method binds the `IWorkers` interface to its concrete implementation
        `Workers` within the application's dependency injection container. The
        registration uses a transient lifetime, ensuring that a new instance of
        `Workers` is created each time the service is resolved. An alias is also
        provided for convenient identification and retrieval.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs a side effect by
            registering the service in the application container.

        Notes
        -----
        - The service is registered with a transient lifetime:
            - A new instance is created for each resolution request.
            - No instance is cached or reused.
            - This is suitable for stateless or short-lived worker operations.
        - The alias used for registration is
          "x-orionis.services.system.contracts.workers.IWorkers".
        """

        # Register the Workers implementation as a transient service for IWorkers.
        # Each resolution will create a new instance.
        self.app.transient(IWorkers, Workers, alias="x-orionis.services.system.contracts.workers.IWorkers")