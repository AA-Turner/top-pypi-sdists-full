from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.foundation.config.roots.paths import Paths
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigRootPaths(AsyncTestCase):
    """
    Test suite for the `Paths` dataclass, which defines the project directory structure.

    This class contains asynchronous unit tests to verify the integrity, default values,
    type constraints, immutability, and metadata accessibility of the `Paths` dataclass.
    """

    def testDefaultPathsInstantiation(self):
        """
        Test instantiation of `Paths` with default values.

        Ensures that a `Paths` instance can be created using default arguments and
        that the resulting object is an instance of `Paths`.

        Returns
        -------
        None
        """
        paths = Paths()
        self.assertIsInstance(paths, Paths)

    def testAllPathsAreStrings(self):
        """
        Verify that all attributes of `Paths` are strings.

        Iterates through all fields of the `Paths` dataclass and asserts that each
        attribute is a non-empty string.

        Returns
        -------
        None
        """
        paths = Paths()
        for field_name in paths.__dataclass_fields__:
            value = getattr(paths, field_name)
            self.assertIsInstance(value, str)
            self.assertTrue(len(value) > 0)

    def testPathValidationRejectsNonStringValues(self):
        """
        Ensure non-string path values raise `OrionisIntegrityException`.

        Attempts to instantiate `Paths` with a non-string value for a path field
        and asserts that an `OrionisIntegrityException` is raised.

        Returns
        -------
        None
        """
        with self.assertRaises(OrionisIntegrityException):
            Paths(console_scheduler=123)

    def testToDictReturnsCompleteDictionary(self):
        """
        Test that `toDict()` returns a complete dictionary of all path fields.

        Asserts that the dictionary returned by `toDict()` contains all fields
        defined in the `Paths` dataclass and that the dictionary has the correct length.

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
        Verify that the `Paths` dataclass is immutable (frozen).

        Attempts to modify an attribute of a `Paths` instance after creation and
        asserts that an exception is raised due to immutability.

        Returns
        -------
        None
        """
        paths = Paths()
        with self.assertRaises(Exception):
            paths.console_scheduler = 'new/path'  # type: ignore

    def testPathMetadataIsAccessible(self):
        """
        Check accessibility and structure of path field metadata.

        Iterates through all fields of the `Paths` dataclass and asserts that each
        field's metadata contains both 'description' and 'default' keys, and that
        their values are of the expected types.

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
