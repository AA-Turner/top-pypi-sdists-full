from orionis.console.contracts.debug import IDebug
from orionis.container.facades.facade import Facade

class Dumper(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Get the registered name of the component in the service container.

        This method defines the binding key used to resolve the dumper service
        from the application's service container. The dumper facade provides
        a static interface to the underlying dumper service implementation.

        Returns
        -------
        str
            The service container binding key "x-orionis.console.contracts.debug.IDebug"
            that identifies the dumper service instance.
        """

        # Return the specific binding key for the dumper service in the container
        return f"x-{IDebug.__module__}.{IDebug.__name__}"