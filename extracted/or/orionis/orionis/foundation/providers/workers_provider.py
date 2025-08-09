from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.system.contracts.workers import IWorkers
from orionis.services.system.workers import Workers

class WorkersProvider(ServiceProvider):
    """
    Provides and registers the worker management service within the application container.

    This provider determines and registers the optimal worker management implementation,
    making it available for dependency injection throughout the application.

    Attributes
    ----------
    app : Application
        The application container instance where services are registered.
    """

    def register(self) -> None:
        """
        Register the worker service in the application container.

        Registers the `Workers` implementation as a transient service for the `IWorkers`
        contract, with the alias "core.orionis.workers".

        Returns
        -------
        None
        """

        self.app.transient(IWorkers, Workers, alias="core.orionis.workers")

    def boot(self) -> None:
        """
        Perform post-registration initialization if required.

        This method is a placeholder for any initialization logic that should occur
        after the worker service has been registered.

        Returns
        -------
        None
        """

        pass