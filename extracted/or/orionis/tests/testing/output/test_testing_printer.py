from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.output.printer import TestPrinter

class TestTestingPrinter(AsyncTestCase):

    async def testMethodsExist(self):
        """
        Checks for the existence of required methods in the TestPrinter class.

        This test ensures that all methods listed in `required_methods` are present
        in the `TestPrinter` class by asserting their existence using `hasattr`.

        Parameters
        ----------
        self : TestTestingPrinter
            The test case instance.

        Returns
        -------
        None
            Raises an AssertionError if any required method is missing.
        """
        # List of method names that must exist in TestPrinter
        required_methods = [
            "print",
            "startMessage",
            "finishMessage",
            "executePanel",
            "linkWebReport",
            "summaryTable",
            "displayResults",
            "unittestResult"
        ]

        # Check each required method for existence in TestPrinter
        for method_name in required_methods:

            # Assert that the method exists in TestPrinter
            self.assertTrue(
                hasattr(TestPrinter, method_name),
                f"{method_name} does not exist"
            )
