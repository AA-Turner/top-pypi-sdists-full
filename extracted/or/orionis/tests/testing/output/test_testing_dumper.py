from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.output.dumper import TestDumper

class TestTestingDumper(AsyncTestCase):

    async def testMethodsExist(self):
        """
        Checks if the required methods are present in the TestDumper class.

        This test verifies that the `TestDumper` class contains all methods
        specified in the `required_methods` list. It asserts the existence of
        each method using `hasattr`.

        Returns
        -------
        None
            This method does not return any value. It raises an assertion error if any required method is missing.
        """

        required_methods = [
            "dd",
            "dump"
        ]

        # Iterate over the list of required method names
        for method_name in required_methods:

            # Assert that each required method exists in TestDumper
            self.assertTrue(
                hasattr(TestDumper, method_name),
                f"{method_name} does not exist"
            )
