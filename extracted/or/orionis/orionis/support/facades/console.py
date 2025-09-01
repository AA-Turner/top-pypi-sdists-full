from orionis.console.contracts.console import IConsole
from orionis.container.facades.facade import Facade

class Console(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Get the registered service container binding key for the console component.

        This method returns the specific binding key that is used to resolve the
        console output service from the dependency injection container. The facade
        pattern uses this key to locate and instantiate the underlying console
        service implementation.

        Returns
        -------
        str
            The string identifier 'x-orionis.console.contracts.console.IConsole' used as the
            binding key to resolve the console service from the service container.
        """

        # Return the predefined binding key for the console output service
        return f"x-{IConsole.__module__}.{IConsole.__name__}"