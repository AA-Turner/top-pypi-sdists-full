from orionis.container.facades.facade import Facade

class Console(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the binding key used to resolve the console service from the service container.

        This method provides the unique string identifier associated with the console output
        service in the dependency injection container. The facade uses this key to retrieve
        the underlying implementation of the console service, enabling decoupled access to
        console output functionality throughout the application.

        Returns
        -------
        str
            The binding key 'x-orionis.console.contracts.console.IConsole' that identifies
            the console service in the service container.
        """

        # Return the predefined binding key for the console output service
        return "x-orionis.console.contracts.console.IConsole"
