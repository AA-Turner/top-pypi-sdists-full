from orionis.foundation.config.auth.entities.auth import Auth
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigAuth(AsyncTestCase):
    """
    Test suite for verifying the behavior of the Auth configuration within the application.

    This class contains asynchronous test cases to ensure that the Auth object
    correctly handles the assignment and retrieval of new attribute values.
    """

    async def testNewValue(self):
        """
        Test assignment and retrieval of new attribute values in Auth.

        This test creates a new Auth object and assigns values to new attributes.
        It then asserts that these attributes hold the expected values.

        Returns
        -------
        None
            This method does not return a value.
        """
        auth = Auth()
        auth.new_value = 'new_value'
        auth.new_value2 = 'new_value2'

        self.assertEqual(auth.new_value, 'new_value')
        self.assertEqual(auth.new_value2, 'new_value2')