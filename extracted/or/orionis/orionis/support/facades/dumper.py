from orionis.container.facades.facade import Facade

class Dumper(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Retrieves the binding key for the dumper service in the application's service container.

        This method specifies the unique identifier used by the service container to resolve
        the dumper service instance. The returned binding key allows the facade to provide
        a static interface to the underlying dumper service implementation.

        Returns
        -------
        str
            The string "x-orionis.console.contracts.debug.IDebug", which is the binding key
            used to identify and resolve the dumper service from the service container.
        """

        # Return the unique binding key for the dumper service in the container
        return "x-orionis.console.contracts.debug.IDebug"
