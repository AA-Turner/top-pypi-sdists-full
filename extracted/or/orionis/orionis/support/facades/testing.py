from orionis.container.facades.facade import Facade

class Test(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the binding key for the testing component in the service container.

        Returns
        -------
        str
            The unique string identifier for the testing component, used by the service
            container to resolve the appropriate implementation.
        """
        return "core.orionis.testing"
