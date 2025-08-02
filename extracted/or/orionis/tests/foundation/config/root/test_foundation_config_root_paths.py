from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.roots.paths import Paths
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigRootPaths(AsyncTestCase):
    """
    Test suite for the Paths dataclass which defines the project directory structure.

    This class verifies the integrity of path definitions, default values,
    and the behavior of accessor methods.

    Methods
    -------
    testDefaultPathsInstantiation()
        Test that a Paths instance can be created with default values.
    testAllPathsAreStrings()
        Test that all path attributes are strings.
    testPathValidationRejectsNonStringValues()
        Test that non-string path values raise OrionisIntegrityException.
    testToDictReturnsCompleteDictionary()
        Test that toDict() returns a complete dictionary of all paths.
    testFrozenDataclassBehavior()
        Test that the dataclass is truly frozen (immutable).
    testPathMetadataIsAccessible()
        Test that path metadata is properly defined and accessible.
    """

    def testDefaultPathsInstantiation(self):
        """
        Test that a Paths instance can be created with default values.

        Ensures that all default paths are correctly initialized and
        the instance is properly constructed.
        """
        paths = Paths()
        self.assertIsInstance(paths, Paths)

    def testAllPathsAreStrings(self):
        """
        Test that all path attributes are strings.

        Ensures that every field in Paths is a string by default.
        """
        paths = Paths()
        for field_name in paths.__dataclass_fields__:
            value = getattr(paths, field_name)
            self.assertIsInstance(value, str)
            self.assertTrue(len(value) > 0)

    def testPathValidationRejectsNonStringValues(self):
        """
        Test that non-string path values raise OrionisIntegrityException.

        Verifies that the __post_init__ validation rejects non-string values
        for all path fields.

        Raises
        ------
        OrionisIntegrityException
            If a non-string value is provided.
        """
        with self.assertRaises(OrionisIntegrityException):
            Paths(console_scheduler=123)

    def testToDictReturnsCompleteDictionary(self):
        """
        Test that toDict() returns a complete dictionary of all paths.

        Verifies that the returned dictionary contains all path fields
        with their current values.

        Returns
        -------
        None
        """
        paths = Paths()
        path_dict = paths.toDict()
        self.assertIsInstance(path_dict, dict)
        self.assertEqual(len(path_dict), len(paths.__dataclass_fields__))
        for field in paths.__dataclass_fields__:
            self.assertIn(field, path_dict)

    def testFrozenDataclassBehavior(self):
        """
        Test that the dataclass is truly frozen (immutable).

        Verifies that attempts to modify attributes after creation
        raise exceptions.

        Raises
        ------
        Exception
            If an attempt is made to modify a frozen dataclass.
        """
        paths = Paths()
        with self.assertRaises(Exception):
            paths.console_scheduler = 'new/path'  # type: ignore

    def testPathMetadataIsAccessible(self):
        """
        Test that path metadata is properly defined and accessible.

        Verifies that each path field has the expected metadata structure
        with description and default fields.

        Returns
        -------
        None
        """
        paths = Paths()
        for field in paths.__dataclass_fields__.values():
            metadata = field.metadata
            self.assertIn('description', metadata)
            self.assertIn('default', metadata)
            self.assertIsInstance(metadata['description'], str)
            default_value = metadata['default']
            if callable(default_value):
                default_value = default_value()
            self.assertIsInstance(default_value, str)
