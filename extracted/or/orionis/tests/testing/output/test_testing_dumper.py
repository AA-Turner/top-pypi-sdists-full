from orionis.test.cases.asynchronous import AsyncTestCase
from orionis.test.output.dumper import TestDumper

class TestTestingDumper(AsyncTestCase):

    async def testMethodsExist(self):
        """
        Verify the presence of required methods in the TestDumper class.

        This asynchronous test checks whether the TestDumper class implements all methods listed in `required_methods`. 
        An assertion error is raised if any required method is missing.

        Returns
        -------
        None
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
