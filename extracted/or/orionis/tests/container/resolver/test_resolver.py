import inspect
from orionis.container.contracts.resolver import IResolver
from orionis.container.resolver.resolver import Resolver
from orionis.test.cases.asynchronous import AsyncTestCase

class TestResolverMethods(AsyncTestCase):

    async def testMethodsExist(self):
        """
        Validates the implementation and structure of the `Resolver` class.

        This test checks that the `Resolver` class:
            - Implements all required methods.
            - Inherits from the `IResolver` interface.
            - Has main public methods (`resolve`, `resolveType`, `resolveSignature`) that are synchronous.

        Parameters
        ----------
        self : TestResolverMethods
            The test case instance.

        Returns
        -------
        None
            The method does not return any value. Assertions are used to validate the class structure.
        """

        # List of required method names that must be implemented by Resolver
        required_methods = [
            "__init__",
            "resolve",
            "resolveType",
            "resolveSignature",
            "_Resolver__resolveTransient",
            "_Resolver__resolveSingleton",
            "_Resolver__resolveScoped",
            "_Resolver__instantiateConcreteWithArgs",
            "_Resolver__instantiateCallableWithArgs",
            "_Resolver__instantiateConcreteReflective",
            "_Resolver__instantiateCallableReflective",
            "_Resolver__resolveDependencies",
        ]

        # Check that each required method exists in Resolver
        for method in required_methods:
            self.assertTrue(
                hasattr(Resolver, method),
                f"Resolver must implement the method '{method}'"
            )

        # Ensure Resolver inherits from IResolver
        self.assertTrue(
            issubclass(Resolver, IResolver),
            "Resolver must inherit from IResolver"
        )

        # Verify that main public methods are not asynchronous
        for method in ["resolve", "resolveType", "resolveSignature"]:
            self.assertFalse(
                inspect.iscoroutinefunction(getattr(Resolver, method)),
                f"The method '{method}' must not be async"
            )
