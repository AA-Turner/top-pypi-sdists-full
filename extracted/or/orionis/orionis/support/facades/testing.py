from orionis.container.facades.facade import Facade

class Test(Facade):

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
            The service container binding key "x-orionis.test.core.unit_test"
            used to resolve the testing component implementation.
        """

        return "x-orionis.test.core.unit_test"
