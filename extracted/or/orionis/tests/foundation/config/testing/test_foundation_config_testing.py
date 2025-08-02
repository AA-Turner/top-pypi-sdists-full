from orionis.foundation.config.testing.entities.testing import Testing
from orionis.foundation.config.testing.enums.mode import ExecutionMode
from orionis.foundation.exceptions import OrionisIntegrityException
from orionis.test.cases.asynchronous import AsyncTestCase

class TestFoundationConfigTesting(AsyncTestCase):
    """
    Test suite for the Testing configuration entity.

    This class contains asynchronous test cases to validate the default values,
    custom values, and integrity constraints of the Testing configuration.
    """

    async def testDefaultValues(self):
        """
        Test the default values of the Testing configuration.

        Notes
        -----
        Ensures that all default attributes of the Testing configuration are set
        as expected.
        """
        t = Testing()
        self.assertEqual(t.verbosity, 2)
        self.assertEqual(t.execution_mode, ExecutionMode.SEQUENTIAL.value)
        self.assertTrue(isinstance(t.max_workers, int) and t.max_workers >= 1)
        self.assertFalse(t.fail_fast)
        self.assertTrue(t.print_result)
        self.assertFalse(t.throw_exception)
        self.assertEqual(t.base_path, "tests")
        self.assertEqual(t.folder_path, "*")
        self.assertEqual(t.pattern, "test_*.py")
        self.assertIsNone(t.test_name_pattern)
        self.assertEqual(t.tags, [])

    async def testValidCustomValues(self):
        """
        Test custom valid values for all fields.

        Notes
        -----
        Verifies that the Testing configuration accepts and correctly sets
        custom valid values for all its fields.
        """
        t = Testing(
            verbosity=1,
            execution_mode=ExecutionMode.PARALLEL,
            max_workers=4,
            fail_fast=True,
            print_result=False,
            throw_exception=True,
            base_path="my_tests",
            folder_path=["unit", "integration"],
            pattern="*_spec.py",
            test_name_pattern="test_login*",
            tags=["fast", "critical"]
        )
        self.assertEqual(t.verbosity, 1)
        self.assertEqual(t.execution_mode, ExecutionMode.PARALLEL.value)
        self.assertEqual(t.max_workers, 4)
        self.assertTrue(t.fail_fast)
        self.assertFalse(t.print_result)
        self.assertTrue(t.throw_exception)
        self.assertEqual(t.base_path, "my_tests")
        self.assertEqual(t.folder_path, ["unit", "integration"])
        self.assertEqual(t.pattern, "*_spec.py")
        self.assertEqual(t.test_name_pattern, "test_login*")
        self.assertEqual(t.tags, ["fast", "critical"])

    async def testFolderPathStringAndList(self):
        """
        Test folder_path accepts both string and list of strings.

        Notes
        -----
        Checks that the folder_path attribute can be set as a string or a list of strings.
        """
        t1 = Testing(folder_path="integration")
        self.assertEqual(t1.folder_path, "integration")
        t2 = Testing(folder_path=["integration", "unit"])
        self.assertEqual(t2.folder_path, ["integration", "unit"])

    async def testTagsNoneOrList(self):
        """
        Test tags accepts None or list of strings.

        Notes
        -----
        Ensures that the tags attribute can be set to None or a list of strings.
        """
        t1 = Testing(tags=None)
        self.assertIsNone(t1.tags)
        t2 = Testing(tags=["a", "b"])
        self.assertEqual(t2.tags, ["a", "b"])

    async def testInvalidVerbosity(self):
        """
        Test invalid verbosity values.

        Notes
        -----
        Verifies that invalid verbosity values raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(verbosity=-1)
        with self.assertRaises(OrionisIntegrityException):
            Testing(verbosity=3)
        with self.assertRaises(OrionisIntegrityException):
            Testing(verbosity="high")

    async def testInvalidExecutionMode(self):
        """
        Test execution_mode cannot be None.

        Notes
        -----
        Ensures that setting execution_mode to None raises OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(execution_mode=None)

    async def testInvalidMaxWorkers(self):
        """
        Test invalid max_workers values.

        Notes
        -----
        Checks that invalid values for max_workers raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(max_workers=0)
        with self.assertRaises(OrionisIntegrityException):
            Testing(max_workers=-5)
        with self.assertRaises(OrionisIntegrityException):
            Testing(max_workers="many")

    async def testInvalidFailFast(self):
        """
        Test fail_fast must be boolean.

        Notes
        -----
        Ensures that non-boolean values for fail_fast raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(fail_fast="yes")

    async def testInvalidPrintResult(self):
        """
        Test print_result must be boolean.

        Notes
        -----
        Ensures that non-boolean values for print_result raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(print_result=1)

    async def testInvalidThrowException(self):
        """
        Test throw_exception must be boolean.

        Notes
        -----
        Ensures that non-boolean values for throw_exception raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(throw_exception="no")

    async def testInvalidBasePath(self):
        """
        Test base_path must be string.

        Notes
        -----
        Ensures that non-string values for base_path raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(base_path=123)

    async def testInvalidFolderPath(self):
        """
        Test folder_path must be string or list of strings.

        Notes
        -----
        Ensures that invalid types for folder_path raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(folder_path=123)
        with self.assertRaises(OrionisIntegrityException):
            Testing(folder_path=[1, 2])
        with self.assertRaises(OrionisIntegrityException):
            Testing(folder_path=["ok", 2])

    async def testInvalidPattern(self):
        """
        Test pattern must be string.

        Notes
        -----
        Ensures that non-string values for pattern raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(pattern=[])
        with self.assertRaises(OrionisIntegrityException):
            Testing(pattern=123)

    async def testInvalidTestNamePattern(self):
        """
        Test test_name_pattern must be string or None.

        Notes
        -----
        Ensures that invalid types for test_name_pattern raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(test_name_pattern=[])
        with self.assertRaises(OrionisIntegrityException):
            Testing(test_name_pattern=123)

    async def testInvalidTags(self):
        """
        Test tags must be None or list of strings.

        Notes
        -----
        Ensures that invalid types for tags raise OrionisIntegrityException.
        """
        with self.assertRaises(OrionisIntegrityException):
            Testing(tags="fast")
        with self.assertRaises(OrionisIntegrityException):
            Testing(tags=[1, 2])
        with self.assertRaises(OrionisIntegrityException):
            Testing(tags=["ok", 2])