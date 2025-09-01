from orionis.container.facades.facade import Facade
from orionis.console.contracts.reactor import IReactor

class Reactor(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Get the registered name of the component.

        This method returns the service container binding key that identifies
        the testing component implementation. The facade uses this key to
        resolve the appropriate testing service from the container when
        static methods are called on the facade.

        Returns
        -------
        str
            The service container binding key "x-orionis.console.contracts.reactor.IReactor"
            used to resolve the testing component implementation.
        """

        return f"x-{IReactor.__module__}.{IReactor.__name__}"
