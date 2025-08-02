import sys
import types
from orionis.services.system.imports import Imports
from orionis.test.cases.asynchronous import AsyncTestCase

class TestServicesSystemImports(AsyncTestCase):

    async def testImportModule(self) -> None:
        """
        Tests that an Imports instance can be created and that the collect() method
        successfully populates its imports list.

        This test verifies the basic instantiation of the Imports class and ensures
        that the collect() method executes without errors.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Create an instance of Imports
        imports = Imports()

        # Populate the imports list
        imports.collect()

        # Assert that the instance is of type Imports
        self.assertIsInstance(imports, Imports)

    async def testCollectPopulatesImports(self):
        """
        Tests that the `collect()` method of the Imports class populates the imports list with modules.

        This test creates a dummy module, adds it to `sys.modules`, and verifies that after calling
        `collect()`, the dummy module appears in the `imports` list of the Imports instance.

        Parameters
        ----------
        self : TestServicesSystemImports
            The test case instance.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Create a dummy module and set its __file__ attribute
        dummy_mod = types.ModuleType("dummy_mod")
        dummy_mod.__file__ = __file__

        # Add a dummy function to the module and set its __module__ attribute
        def dummy_func(): pass
        dummy_mod.dummy_func = dummy_func
        dummy_func.__module__ = "dummy_mod"

        # Register the dummy module in sys.modules
        sys.modules["dummy_mod"] = dummy_mod

        # Create Imports instance and collect imports
        imports = Imports()
        imports.collect()

        # Check if the dummy module was collected
        found = any(imp["name"] == "dummy_mod" for imp in imports.imports)
        self.assertTrue(found)

        # Cleanup: remove the dummy module from sys.modules
        del sys.modules["dummy_mod"]

    async def testCollectExcludesStdlibAndSpecialModules(self):
        """
        Tests that the `collect()` method of the Imports class excludes standard library modules and special modules.

        This test verifies that after calling `collect()`, the resulting imports list does not contain entries for
        standard library modules such as `__main__` or modules whose names start with `_distutils`. This ensures
        that the Imports class correctly filters out modules that should not be included in the imports list.

        Parameters
        ----------
        self : TestServicesSystemImports
            The test case instance.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Create Imports instance and collect imports
        imports = Imports()
        imports.collect()

        # Extract the names of collected modules
        names = [imp["name"] for imp in imports.imports]

        # Assert that '__main__' is not in the collected imports
        self.assertNotIn("__main__", names)

        # Assert that modules starting with '_distutils' are not in the collected imports
        self.assertFalse(any(n.startswith("_distutils") for n in names))

    async def testClearEmptiesImports(self):
        """
        Tests that the `clear()` method of the Imports class empties the imports list.

        This test manually populates the `imports` attribute of an Imports instance,
        calls the `clear()` method, and verifies that the imports list is empty afterward.

        Parameters
        ----------
        self : TestServicesSystemImports
            The test case instance.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Create Imports instance and manually populate the imports list
        imports = Imports()
        imports.imports = [{"name": "test", "file": "test.py", "symbols": ["a"]}]

        # Call clear() to empty the imports list
        imports.clear()

        # Assert that the imports list is now empty
        self.assertEqual(imports.imports, [])

    async def testCollectHandlesModulesWithoutFile(self):
        """
        Tests that the `collect()` method of the Imports class correctly handles modules that do not have a `__file__` attribute.

        This test creates a dummy module without a `__file__` attribute, registers it in `sys.modules`, and verifies that after calling
        `collect()`, the module does not appear in the `imports` list of the Imports instance. This ensures that the Imports class
        properly skips modules lacking a `__file__` attribute, which are typically built-in or dynamically created modules.

        Parameters
        ----------
        self : TestServicesSystemImports
            The test case instance.

        Returns
        -------
        None
            This method does not return any value.
        """
        # Create a dummy module without a __file__ attribute
        mod = types.ModuleType("mod_without_file")
        sys.modules["mod_without_file"] = mod

        # Create Imports instance and collect imports
        imports = Imports()
        imports.collect()

        # Extract the names of collected modules
        names = [imp["name"] for imp in imports.imports]

        # Assert that the dummy module is not in the collected imports
        self.assertNotIn("mod_without_file", names)

        # Cleanup: remove the dummy module from sys.modules
        del sys.modules["mod_without_file"]

    async def testCollectSkipsBinaryExtensions(self):
        """
        Tests that the `collect()` method of the Imports class skips binary extension modules.

        This test creates a dummy module with a `.pyd` file extension (representing a binary extension),
        registers it in `sys.modules`, and verifies that after calling `collect()`, the module does not
        appear in the `imports` list of the Imports instance. This ensures that the Imports class
        properly excludes binary extension modules from its collected imports.

        Parameters
        ----------
        self : TestServicesSystemImports
            The test case instance.

        Returns
        -------
        None
            This method does not return any value.
        """

        # Create a dummy module with a .pyd file extension to simulate a binary extension
        mod = types.ModuleType("bin_mod")
        mod.__file__ = "bin_mod.pyd"

        # Register the dummy binary module in sys.modules
        sys.modules["bin_mod"] = mod

        # Create Imports instance and collect imports
        imports = Imports()
        imports.collect()

        # Extract the names of collected modules
        names = [imp["name"] for imp in imports.imports]

        # Assert that the binary module is not in the collected imports
        self.assertNotIn("bin_mod", names)

        # Cleanup: remove the dummy binary module from sys.modules
        del sys.modules["bin_mod"]