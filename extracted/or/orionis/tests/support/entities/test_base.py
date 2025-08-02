from orionis.test.cases.asynchronous import AsyncTestCase
from tests.support.entities.mock_dataclass import Color, ExampleEntity

class TestBaseEntity(AsyncTestCase):

    async def asyncSetUp(self):
        """
        Set up the test case asynchronously by initializing an ExampleEntity instance.

        This method is called before each test coroutine to prepare the test environment.
        It creates an ExampleEntity with predefined attributes.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Create an ExampleEntity instance for use in tests
        self.entity = ExampleEntity(id=42, name="test", color=Color.GREEN, tags=["a", "b"])

    async def testToDict(self):
        """
        Test the toDict method of ExampleEntity.

        Verifies that the toDict method returns a dictionary representation of the entity
        with correct field values.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Convert entity to dictionary
        result = self.entity.toDict()
        self.assertIsInstance(result, dict)

        # Check individual field values
        self.assertEqual(result["id"], 42)
        self.assertEqual(result["name"], "test")
        self.assertEqual(result["color"], Color.GREEN)
        self.assertEqual(result["tags"], ["a", "b"])

    async def testGetFields(self):
        """
        Test the getFields method of ExampleEntity.

        Ensures that getFields returns a list of field information dictionaries,
        each containing field name, types, default value, and metadata.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Retrieve field information from entity
        fields_info = self.entity.getFields()
        self.assertIsInstance(fields_info, list)

        # Extract field names for verification
        names = [f["name"] for f in fields_info]
        self.assertIn("id", names)
        self.assertIn("name", names)
        self.assertIn("color", names)
        self.assertIn("tags", names)

        # Check that each field info contains required keys
        for f in fields_info:
            self.assertIn("types", f)
            self.assertIn("default", f)
            self.assertIn("metadata", f)
