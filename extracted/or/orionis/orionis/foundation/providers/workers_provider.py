from orionis.container.providers.service_provider import ServiceProvider
from orionis.services.system.contracts.workers import IWorkers
from orionis.services.system.workers import Workers

class WorkersProvider(ServiceProvider):
    """
    WorkersProvider
    ===============

    Registers the worker management service in the application container.
    Determines the optimal number of workers to start based on system analysis.

    Methods
    -------
    register()
        Registers the worker service in the application container.
    boot()
        Performs post-registration initialization if needed.
    """

    def register(self) -> None:
        """
        Registers the worker service in the application container.

        Returns
        -------
        None
        """
        self.app.transient(IWorkers, Workers, alias="core.orionis.workers")

    def boot(self) -> None:
        """
        Performs post-registration initialization if needed.

        Returns
        -------
        None
        """
        pass