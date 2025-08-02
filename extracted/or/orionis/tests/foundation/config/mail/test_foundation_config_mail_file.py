from orionis.foundation.config.mail.entities.file import File
from orionis.foundation.exceptions.integrity import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigMailFile(AsyncTestCase):
    """
    Unit tests for the File entity in the mail configuration module.
    """

    async def testDefaultPathValue(self):
        """
        Test that the File instance is initialized with the correct default path.

        Notes
        -----
        Verifies that a new File object has 'storage/mail' as the default path.
        """
        file = File()
        self.assertEqual(file.path, "storage/mail")

    async def testPathValidation(self):
        """
        Test the path validation in the __post_init__ method.

        Raises
        ------
        OrionisIntegrityException
            If the path is not a string or is an empty string.

        Notes
        -----
        Verifies that non-string paths or empty strings raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            File(path=123)
        with self.assertRaises(OrionisIntegrityException):
            File(path="")

    async def testValidPathAssignment(self):
        """
        Test that valid path assignments work correctly.

        Notes
        -----
        Verifies that string paths are accepted and stored properly.
        """
        test_path = "custom/path/to/mail"
        file = File(path=test_path)
        self.assertEqual(file.path, test_path)

    async def testToDictMethod(self):
        """
        Test the toDict method returns a proper dictionary representation.

        Returns
        -------
        dict
            Dictionary representation of the File instance.

        Notes
        -----
        Checks that the toDict method converts the File instance into a dictionary
        with the expected path field.
        """
        file = File()
        result = file.toDict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result["path"], "storage/mail")

    async def testHashability(self):
        """
        Test that File instances are hashable due to unsafe_hash=True.

        Notes
        -----
        Verifies that instances can be used in sets or as dictionary keys.
        """
        file1 = File()
        file2 = File(path="other/path")
        test_set = {file1, file2}
        self.assertEqual(len(test_set), 2)

    async def testKwOnlyInitialization(self):
        """
        Test that File requires keyword arguments for initialization.

        Raises
        ------
        TypeError
            If positional arguments are used for initialization.

        Notes
        -----
        Verifies that the class enforces kw_only=True in its dataclass decorator.
        """
        with self.assertRaises(TypeError):
            File("storage/mail")