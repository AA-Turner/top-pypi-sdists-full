from orionis.container.facades.facade import Facade

class Test(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Returns the service container binding key for the testing component.

        This method provides the unique string identifier used by the service container
        to resolve the testing component. It is typically used internally by the Facade
        system to retrieve the correct implementation from the container.

        Returns
        -------
        str
            The string key "core.orionis.testing" that identifies the testing component
            in the service container.
        """

        # Return the binding key for the testing component in the service container
        return "core.orionis.testing"