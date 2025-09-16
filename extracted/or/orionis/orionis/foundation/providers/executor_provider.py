from orionis.console.contracts.executor import IExecutor
from orionis.console.output.executor import Executor
from orionis.container.providers.service_provider import ServiceProvider

class ConsoleExecuteProvider(ServiceProvider):

    def register(self) -> None:
        """
        Registers the console executor service within the application container.

        This method binds the `IExecutor` interface to its concrete `Executor` implementation
        as a transient service. Each time the service is requested from the container, a new
        instance of `Executor` is created, ensuring isolated execution contexts for console
        operations. The service is registered with the alias
        `"x-orionis.console.contracts.executor.IExecutor"` for convenient retrieval and
        identification within the dependency injection container.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. It performs the side effect of
            registering the executor service binding in the application container.
        """

        # Bind the IExecutor interface to the Executor implementation as a transient service.
        # This ensures a new Executor instance is created on each request.
        self.app.transient(IExecutor, Executor, alias="x-orionis.console.contracts.executor.IExecutor")