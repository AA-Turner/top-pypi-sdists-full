from orionis.container.facades.facade import Facade
from orionis.test.contracts.unit_test import IUnitTest

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
            The service container binding key "x-orionis.test.contracts.unit_test.IUnitTest"
            used to resolve the testing component implementation.
        """

        return f"x-{IUnitTest.__module__}.{IUnitTest.__name__}"
