from orionis.container.context.scope import ScopedContext
from orionis.test.cases.asynchronous import AsyncTestCase

class TestScopedContextMethods(AsyncTestCase):

    def testMethodsExist(self):
        """
        Checks that all required methods are present in the ScopedContext class.

        This test verifies the existence of specific methods that are essential for the correct
        operation of ScopedContext. It ensures that the class interface is complete and that
        method names have not been changed or removed.

        Returns
        -------
        None
            This method does not return anything. It asserts the existence of methods and fails the test if any are missing.
        """
        # List of method names expected to be present in ScopedContext
        expected_methods = [
            "getCurrentScope",
            "setCurrentScope",
            "clear"
        ]

        # Iterate through each expected method and assert its existence
        for method in expected_methods:
            self.assertTrue(
                hasattr(ScopedContext, method),
                f"Method '{method}' does not exist in ScopedContext class."
            )
