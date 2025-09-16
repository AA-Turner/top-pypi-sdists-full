from orionis.container.facades.facade import Facade

class Test(Facade):

    @classmethod
    def getFacadeAccessor(cls) -> str:
        """
        Retrieves the service container binding key for the testing component.

        This method returns the unique string identifier used by the service container
        to resolve the implementation of the testing component. The facade relies on
        this key to delegate static method calls to the appropriate service instance.

        Returns
        -------
        str
            The string "x-orionis.test.contracts.unit_test.IUnitTest", which is the
            service container binding key for the unit testing component.
        """

        # Return the binding key used to resolve the unit testing component from the container
        return "x-orionis.test.contracts.unit_test.IUnitTest"
