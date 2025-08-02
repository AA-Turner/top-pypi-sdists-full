from pathlib import Path
import re
from typing import List
from os import walk
from orionis.console.output.contracts.console import IConsole
from orionis.foundation.config.testing.entities.testing import Testing
from orionis.foundation.contracts.application import IApplication
from orionis.test.contracts.kernel import ITestKernel
from orionis.test.contracts.unit_test import IUnitTest
from orionis.test.exceptions import OrionisTestConfigException, OrionisTestFailureException

class TestKernel(ITestKernel):

    def __init__(
        self,
        app: IApplication
    ) -> None:
        """
        Initialize the TestKernel with the provided application instance.

        Parameters
        ----------
        app : IApplication
            The application instance implementing the IApplication contract.

        Raises
        ------
        OrionisTestConfigException
            If the provided app is not an instance of IApplication.
        """

        # Validate that the app is an instance of IApplication
        if not isinstance(app, IApplication):
            raise OrionisTestConfigException(
                f"Failed to initialize TestKernel: expected IApplication, got {type(app).__module__}.{type(app).__name__}."
            )

        # Load testing configuration from the application
        self.__config = Testing(**app.config('testing'))

        # Create and configure the unit test instance
        self.__unit_test: IUnitTest = app.make('core.orionis.testing')
        self.__unit_test._UnitTest__app = app
        self.__unit_test._UnitTest__storage = app.path('storage_testing')

        # Initialize the console for output
        self.__console: IConsole = app.make('core.orionis.console')

    def __listMatchingFolders(
        self,
        base_path: Path,
        custom_path: Path,
        pattern: str
    ) -> List[str]:
        """
        List folders within a custom path whose files match a given pattern.

        Parameters
        ----------
        base_path : Path
            The base directory path for relative calculation.
        custom_path : Path
            The custom directory path to search for matching files.
        pattern : str
            The filename pattern to match (supports '*' and '?').

        Returns
        -------
        List[str]
            List of relative folder paths containing files matching the pattern.
        """

        # Compile the pattern into a regex for matching file names
        regex = re.compile('^' + pattern.replace('*', '.*').replace('?', '.') + '$')
        matched_folders = set()

        # Walk through the directory tree starting at custom_path
        for root, _, files in walk(str(custom_path)):

            # Check if any file in the current folder matches the pattern
            if any(regex.fullmatch(file) for file in files):

                # Calculate the relative path from base_path and add to results
                rel_path = Path(root).relative_to(base_path).as_posix()
                matched_folders.add(rel_path)

        # Return the list of matching folder paths
        return list(matched_folders)

    def handle(self) -> IUnitTest:
        """
        Configure and execute the unit tests based on the current configuration.

        Returns
        -------
        IUnitTest
            The configured and executed unit test instance.
        """
        try:

            # Configure the unit test with parameters from the configuration
            self.__unit_test.configure(
                verbosity=self.__config.verbosity,
                execution_mode=self.__config.execution_mode,
                max_workers=self.__config.max_workers,
                fail_fast=self.__config.fail_fast,
                print_result=self.__config.print_result,
                throw_exception=self.__config.throw_exception,
                persistent=self.__config.persistent,
                persistent_driver=self.__config.persistent_driver,
                web_report=self.__config.web_report
            )

            # Prepare paths and pattern for test discovery
            base_path = (Path.cwd() / self.__config.base_path).resolve()
            folder_path = self.__config.folder_path
            pattern = self.__config.pattern

            # Set to hold discovered folders
            discovered_folders = set()

            # Discover folders containing test files according to the configuration

            # Search all folders under base_path
            if folder_path == '*':
                discovered_folders.update(self.__listMatchingFolders(base_path, base_path, pattern))

            # Search each custom folder in the list
            elif isinstance(folder_path, list):
                for custom in folder_path:
                    custom_path = (base_path / custom).resolve()
                    discovered_folders.update(self.__listMatchingFolders(base_path, custom_path, pattern))

            # Search a single custom folder
            else:
                custom_path = (base_path / folder_path).resolve()
                discovered_folders.update(self.__listMatchingFolders(base_path, custom_path, pattern))

            # Register discovered folders with the unit test for test discovery
            for folder in discovered_folders:
                self.__unit_test.discoverTestsInFolder(
                    folder_path=folder,
                    base_path=self.__config.base_path,
                    pattern=pattern,
                    test_name_pattern=self.__config.test_name_pattern or None,
                    tags=self.__config.tags or None
                )

            # Run the unit tests and return the result
            return self.__unit_test.run()

        except OrionisTestFailureException as e:

            # Handle test failures and exit with an error message
            self.__console.exitError(f"Test execution failed: {e}")

        except Exception as e:

            # Handle unexpected errors and exit with a generic error message
            self.__console.exitError(f"An unexpected error occurred: {e}")