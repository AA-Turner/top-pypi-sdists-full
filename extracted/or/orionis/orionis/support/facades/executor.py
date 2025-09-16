from orionis.container.facades.facade import Facade

class ConsoleExecutor(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Retrieves the binding key used by the service container to resolve the executor service.

        This method returns the unique string identifier associated with the executor service
        in the Orionis framework's dependency injection container. The executor service is
        responsible for managing command-line operations and console output within the framework.
        By providing this binding key, the facade enables the framework to locate and instantiate
        the correct executor implementation.

        Returns
        -------
        str
            The binding key 'x-orionis.console.contracts.executor.IExecutor' that identifies
            the executor service in the service container.
        """

        # Return the predefined binding key for the executor service in the container
        return "x-orionis.console.contracts.executor.IExecutor"
