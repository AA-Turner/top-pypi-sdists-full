from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.output.printer import TestPrinter

class TestTestingPrinter(AsyncTestCase):

    async def testMethodsExist(self):
        """
        Verify that all required methods are present in the TestPrinter class.

        This asynchronous test checks whether each method listed in `required_methods`
        exists as an attribute of the TestPrinter class. An assertion error is raised
        if any required method is missing.

        Parameters
        ----------
        self : TestTestingPrinter
            Instance of the test case.

        Returns
        -------
        None
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
