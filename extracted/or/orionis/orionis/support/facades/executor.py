from orionis.container.facades.facade import Facade

class ConsoleExecutor(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Get the registered service container binding key for the executor facade.

        This method provides the specific binding key that the service container
        uses to resolve and instantiate the executor service. The executor is
        responsible for handling command-line operations and console output
        management within the Orionis framework.

        Returns
        -------
        str
            The string identifier 'x-orionis.console.output.executor' used as
            the binding key to locate and resolve the executor service instance
            from the dependency injection container.
        """

        # Return the predefined binding key for the executor service
        return "x-orionis.console.output.executor"