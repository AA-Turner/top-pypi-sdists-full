import os
import tempfile
from pathlib import Path
from orionis.services.paths.exceptions import OrionisFileNotFoundException
from orionis.services.paths.resolver import Resolver
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServicesResolver(AsyncTestCase):

    async def testFileNotFound(self):
        """
        Test that resolving a non-existent file path raises OrionisFileNotFoundException.

        Returns
        -------
        None

        Raises
        ------
        OrionisFileNotFoundException
            If the file does not exist.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            resolver = Resolver(tmpdir)
            non_existent = "does_not_exist.txt"
            with self.assertRaises(OrionisFileNotFoundException):
                resolver.relativePath(non_existent)

    async def testValidFilePath(self):
        """
        Test that resolving a valid file path returns the correct absolute path.

        Returns
        -------
        None

        Asserts
        -------
        The resolved path ends with the file name and is absolute.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a temporary file inside the temp directory
            file_path = Path(tmpdir) / "testfile.txt"
            file_path.write_text("sample content")
            resolver = Resolver(tmpdir)
            resolved = resolver.relativePath("testfile.txt").toString()
            # The resolved path should end with the file name
            self.assertTrue(resolved.endswith("testfile.txt"))
            # The resolved path should be absolute
            self.assertTrue(os.path.isabs(resolved))

    async def testValidDirectoryPath(self):
        """
        Test that resolving a valid directory path returns the correct absolute path.

        Returns
        -------
        None

        Asserts
        -------
        The resolved path ends with the directory name and is absolute.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a subdirectory inside the temp directory
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            resolver = Resolver(tmpdir)
            resolved = resolver.relativePath("subdir").toString()
            self.assertTrue(resolved.endswith("subdir"))
            self.assertTrue(os.path.isabs(resolved))

    async def testOtherBasePath(self):
        """
        Test that providing a different base path to Resolver works as expected.

        Returns
        -------
        None

        Asserts
        -------
        The resolved path ends with the file name and is absolute.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file in a subdirectory
            subdir = Path(tmpdir) / "base"
            subdir.mkdir()
            file_path = subdir / "file.txt"
            file_path.write_text("data")
            resolver = Resolver(str(subdir))
            resolved = resolver.relativePath("file.txt").toString()
            self.assertTrue(resolved.endswith("file.txt"))
            self.assertTrue(os.path.isabs(resolved))

    async def testEqualOutputString(self):
        """
        Test that the string representation of the resolved path matches the output of toString().

        Returns
        -------
        None

        Asserts
        -------
        The string representation of the resolved path matches the output of toString().
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "file.txt"
            file_path.write_text("abc")
            resolver = Resolver(tmpdir).relativePath("file.txt")
            self.assertEqual(resolver.toString(), str(resolver))