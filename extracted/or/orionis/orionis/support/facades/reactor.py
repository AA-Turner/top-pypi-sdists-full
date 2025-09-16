from orionis.container.facades.facade import Facade

class Reactor(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the service container binding key for the reactor component.

        This method provides the unique identifier used by the service container
        to resolve the implementation of the reactor component. The facade uses
        this key to retrieve the appropriate service instance whenever static
        methods are invoked on the facade.

        Returns
        -------
        str
            The string "x-orionis.console.contracts.reactor.IReactor", which is
            the binding key for the reactor component in the service container.
        """

        # Return the binding key for the reactor component in the service container
        return "x-orionis.console.contracts.reactor.IReactor"
