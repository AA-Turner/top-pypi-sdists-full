from orionis.container.context.manager import ScopeManager
from orionis.test.cases.asynchronous import AsyncTestCase

class TestScopeManagerMethods(AsyncTestCase):

    def testMethodsExist(self):
        """
        Checks that all required methods are present in the ScopeManager class.

        This test verifies the existence of a predefined list of methods that are
        essential for the correct functioning of ScopeManager. The methods checked
        include initialization, item access, containment, clearing, and context
        management methods.

        Returns
        -------
        None
            This method does not return any value. It asserts the existence of methods
            and fails the test if any are missing.
        """
        # List of expected method names in ScopeManager
        expected_methods = [
            "__init__",
            "__getitem__",
            "__setitem__",
            "__contains__",
            "clear",
            "__enter__",
            "__exit__"
        ]

        # Check each method for existence in ScopeManager
        for method in expected_methods:
            self.assertTrue(
                hasattr(ScopeManager, method),  # Assert method exists
                f"Method '{method}' does not exist in ScopeManager class."
            )
