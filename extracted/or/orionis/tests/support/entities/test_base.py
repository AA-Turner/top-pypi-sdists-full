from orionis.test.cases.asynchronous import AsyncTestCase
from tests.support.entities.mock_dataclass import Color, ExampleEntity

class TestBaseEntity(AsyncTestCase):

    async def asyncSetUp(self):
        """
        Asynchronously initializes the test environment before each test.

        Initializes an ExampleEntity instance with predefined attributes and assigns it to self.entity.

        Returns
        -------
        None
        """
        # Create an ExampleEntity instance for use in tests
        self.entity = ExampleEntity(id=42, name="test", color=Color.GREEN, tags=["a", "b"])

    async def testToDict(self):
        """
        Tests the toDict method of ExampleEntity.

        Verifies that toDict returns a dictionary with correct field values for the entity.

        Returns
        -------
        None
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
        Tests the getFields method of ExampleEntity.

        Ensures getFields returns a list of dictionaries, each containing field name, types, default value, and metadata.

        Returns
        -------
        None
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
