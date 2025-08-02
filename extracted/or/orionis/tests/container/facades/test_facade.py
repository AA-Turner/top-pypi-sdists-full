import inspect
from orionis.container.facades.facade import FacadeMeta, Facade
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFacadeMethods(AsyncTestCase):

    async def testFacadeMethodsExist(self):
        """
        Verify the existence of essential methods in the Facade and FacadeMeta classes.

        This test checks for the implementation of the following methods:
            - 'getFacadeAccessor' in the Facade class
            - 'resolve' in the Facade class
            - '__getattr__' in the FacadeMeta class

        The method asserts the presence of these required methods and raises an AssertionError if any are missing.

        Parameters
        ----------
        None

        Returns
        -------
        None
            Returns None. The method performs assertions to validate method existence.
        """

        # List of expected methods and their corresponding classes
        expected_methods = [
            ("getFacadeAccessor", Facade),
            ("resolve", Facade),
            ("__getattr__", FacadeMeta),
        ]

        # Iterate through each expected method and assert its existence
        for method_name, cls in expected_methods:
            self.assertTrue(
                hasattr(cls, method_name),
                f"Method '{method_name}' does not exist in {cls.__name__}."
            )

    async def testFacadeMethodSignatures(self):
        """
        Validate the method signatures of key Facade and FacadeMeta class methods.

        This test checks that:
            - 'getFacadeAccessor' in Facade accepts no parameters.
            - 'resolve' in Facade accepts variable positional and keyword arguments.
            - '__getattr__' in FacadeMeta accepts 'cls' and 'name' as parameters.

        The method asserts correct method signatures and raises AssertionError if any signature does not match expectations.

        Parameters
        ----------
        None

        Returns
        -------
        None
            Returns None. The method performs assertions to validate method signatures.
        """

        # Check that getFacadeAccessor has no parameters
        sig = inspect.signature(Facade.getFacadeAccessor)
        params = list(sig.parameters.values())
        self.assertEqual(len(params), 0)

        # Check that resolve has *args and **kwargs as parameters
        sig = inspect.signature(Facade.resolve)
        params = list(sig.parameters.values())
        self.assertEqual(params[0].name, "args")
        self.assertEqual(params[1].kind, inspect.Parameter.VAR_KEYWORD)

        # Check that __getattr__ has 'cls' and 'name' as parameters
        sig = inspect.signature(FacadeMeta.__getattr__)
        params = list(sig.parameters.values())
        self.assertEqual(params[0].name, "cls")
        self.assertEqual(params[1].name, "name")
