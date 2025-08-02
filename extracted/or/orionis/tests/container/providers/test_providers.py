import inspect
from orionis.container.contracts.service_provider import IServiceProvider
from orionis.container.providers.service_provider import ServiceProvider
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServiceProviderMethods(AsyncTestCase):

    async def testMethodsExist(self):
        """
        Validates the implementation of required methods and inheritance in the ServiceProvider class.

        This test performs the following checks:
        - Verifies that the ServiceProvider class defines the '__init__', 'register', and 'boot' methods.
        - Ensures that the 'register' and 'boot' methods are asynchronous coroutine functions.
        - Confirms that ServiceProvider is a subclass of IServiceProvider.

        Parameters
        ----------
        None

        Returns
        -------
        None
            The method does not return any value. Assertions are used to validate class structure and method types.
        """

        # List of required methods and their associated class
        expected_methods = [
            ("__init__", ServiceProvider),
            ("register", ServiceProvider),
            ("boot", ServiceProvider),
        ]

        # Check that each required method exists in ServiceProvider
        for method_name, cls in expected_methods:
            self.assertTrue(
                hasattr(cls, method_name),
                f"Method '{method_name}' does not exist in {cls.__name__}."
            )

        # Ensure 'register' and 'boot' are asynchronous methods
        self.assertTrue(
            inspect.iscoroutinefunction(ServiceProvider.register),
            "'register' must be an async coroutine function."
        )
        self.assertTrue(
            inspect.iscoroutinefunction(ServiceProvider.boot),
            "'boot' must be an async coroutine function."
        )

        # Ensure ServiceProvider inherits from IServiceProvider
        self.assertTrue(
            issubclass(ServiceProvider, IServiceProvider),
            "ServiceProvider must inherit from IServiceProvider."
        )
