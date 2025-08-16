import inspect
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from orionis.console.base.command import BaseCommand
from orionis.console.contracts.reactor import IReactor
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.metadata.framework import VERSION

class PublisherCommand(BaseCommand):
    """
    PublisherCommand is a console command for automating the process of publishing a Python package to the Orionis repository (PyPI).

    This command performs the following steps:
        1. Runs the project's test suite and aborts if there are any test failures or errors.
        2. Bumps the minor version number in the file where the VERSION constant is defined.
        3. Commits and pushes changes to the Git repository if there are modifications.
        4. Builds the package distributions (source and wheel) using `setup.py`.
        5. Publishes the built distributions to PyPI using Twine and a token from environment variables.
        6. Cleans up temporary build artifacts and metadata directories after publishing.

    Attributes
    ----------
    timestamps : bool
        Indicates whether timestamps will be shown in the command output.
    signature : str
        Command signature ("publisher").
    description : str
        Command description.

    Methods
    -------
    __init__(console: Console)
        Initializes the PublisherCommand instance, setting up the console, project root, console width, and PyPI token.
    __bumpMinorVersion()
        Increments the minor version number in the file where the VERSION constant is defined.
    __gitPush()
        Commits and pushes changes to the Git repository if there are modifications.
    __build()
        Builds the package distributions using `setup.py`.
    __publish()
        Publishes the built distributions to PyPI using Twine and a token from environment variables.
    __clearRepository()
        Cleans up temporary build artifacts and metadata directories after publishing.
    handle(reactor: IReactor) -> None
        Orchestrates the publishing process, running tests, bumping version, pushing to Git, building, and publishing the package.

    Returns
    -------
    None
        This class does not return a value directly. The main workflow is executed via the `handle` method, which returns None.
    """

    # Indicates whether timestamps will be shown in the command output
    timestamps: bool = False

    # Command signature and description
    signature: str = "__publisher__"

    # Command description
    description: str = "Publishes Package to the Orionis repository."

    def __init__(self, console: Console):
        """
        Initializes the PublisherCommand instance with the provided console and sets up
        essential attributes for publishing operations.

        This constructor sets up the console for output, determines the project root
        directory, calculates the console width for display panels, and retrieves the
        PyPI authentication token from environment variables.

        Parameters
        ----------
        console : Console
            The Rich Console instance used for formatted output throughout the command execution.

        Returns
        -------
        None
            This method does not return any value. It initializes instance attributes for use in other methods.
        """

        # Store the console instance for output
        self.__console = console

        # Set the project root to the current working directory
        self.__project_root = Path.cwd()

        # Calculate the width for console panels (3/4 of the console width)
        self.__with_console = (self.__console.width // 4) * 3

        # Retrieve the PyPI token from environment variables and remove leading/trailing whitespace
        self.__token = os.getenv("PYPI_TOKEN").strip()

    def __bumpMinorVersion(self):
        """
        Increment the minor version number in the file where the VERSION constant is defined.

        This method locates the file containing the VERSION constant, reads its contents,
        searches for the version assignment line, increments the minor version component,
        and writes the updated version string back to the file. The patch and major
        components remain unchanged.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. The version is updated in-place in the file.

        Raises
        ------
        FileNotFoundError
            If the file containing the VERSION constant cannot be found.
        IOError
            If there is an error reading from or writing to the file.
        """

        # Get the file path where the VERSION constant is defined
        # VERSION is imported from orionis.metadata.framework
        import orionis.metadata.framework
        filepath = Path(inspect.getfile(orionis.metadata.framework))
        if not filepath.exists():
            raise FileNotFoundError(f"VERSION file not found at {filepath}")

        # Read all lines from the file
        with open(filepath, 'r') as f:
            lines = f.readlines()

        # Prepare a list to hold the new lines
        new_lines = []

        # Regular expression to match the VERSION assignment line
        pattern = re.compile(r'^(VERSION\s*=\s*["\'])(\d+)\.(\d+)\.(\d+)(["\'])')

        # Iterate through each line in the file
        for line in lines:
            match = pattern.match(line)
            if match:

                # Extract major, minor, and patch numbers
                major, minor, patch = int(match.group(2)), int(match.group(3)), int(match.group(4))

                # Increment the minor version
                minor += 1

                # Construct the new version string
                new_version = f'{match.group(1)}{major}.{minor}.{patch}{match.group(5)}'
                new_lines.append(new_version + '\n')

            else:

                # Keep all other lines unchanged
                new_lines.append(line)

        # Write the updated lines back to the file
        with open(filepath, 'w') as f:
            f.writelines(new_lines)

        # Print a message indicating the version has been bumped
        self.__console.print(
            Panel(
                f"[green]📦 Bumped minor version to {VERSION}[/]",
                border_style="green",
                width=self.__with_console
            )
        )

    def __gitPush(self):
        """
        Commits and pushes changes to the Git repository if there are modifications.

        This method checks for uncommitted changes in the current project directory.
        If changes are detected, it stages all modifications, commits them with a
        message containing the current version, and pushes the commit to the remote
        repository. If there are no changes, it logs a message indicating that no
        commit or push is necessary.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. All output is printed to the console.

        Raises
        ------
        subprocess.CalledProcessError
            If any of the subprocess calls to Git fail.
        """

        # Check the current Git status to see if there are modified files
        git_status = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True, cwd=self.__project_root
        )

        # Check if the command was successful and if there are modified files
        modified_files = git_status.stdout.strip()

        # If there are modified files, proceed with staging and committing
        if modified_files:

            # Print the status of modified files
            self.__console.print(
                Panel(
                    "[cyan]📌 Staging files for commit...[/]",
                    border_style="cyan",
                    width=self.__with_console
                )
            )

            # Stage all modified files
            subprocess.run(
                ["git", "add", "."], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.__project_root
            )

            # Commit the changes with a message
            self.__console.print(
                Panel(
                    f"[cyan]✅ Committing changes: [📦 Release version {VERSION}][/]",
                    border_style="cyan",
                    width=self.__with_console
                )
            )

            # Wait for a short period to ensure the commit is registered
            time.sleep(5)

            subprocess.run(
                ["git", "commit", "-m", f"📦 Release version {VERSION}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.__project_root
            )
            self.__console.print(
                Panel(
                    "[cyan]🚀 Pushing changes to the remote repository...[/]",
                    border_style="cyan",
                    width=self.__with_console
                )
            )

            # Push the changes to the remote repository
            subprocess.run(
                ["git", "push", "-f"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.__project_root
            )
            self.__console.print(
                Panel(
                    "[green]🌟 Git push completed![/]",
                    border_style="green",
                    width=self.__with_console
                )
            )

        else:

            self.__console.print(
                Panel(
                    "[green]✅ No changes to commit.[/]",
                    border_style="green",
                    width=self.__with_console
                )
            )

    def __build(self):
        """
        Builds the package distributions using `setup.py`.

        This method compiles the package by invoking the `setup.py` script located
        at the project root. It generates both source (`sdist`) and wheel (`bdist_wheel`)
        distribution files, which are required for publishing the package to a repository.
        If the `setup.py` file is not found, an error message is displayed and the build
        process is aborted.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. All output is printed to the console.

        Raises
        ------
        subprocess.CalledProcessError
            If the `setup.py` build command fails.
        """

        try:

            # Notify the user that the build process is starting
            self.__console.print(
                Panel(
                    "[cyan]🛠️  Building the package...[/]",
                    border_style="cyan",
                    width=self.__with_console
                )
            )

            # Define the path to the setup.py file in the project root
            setup_path = self.__project_root / "setup.py"

            # Check if setup.py exists in the project root
            if not os.path.exists(setup_path):
                self.__console.print(
                    Panel(
                        "[bold red]❌ Error: setup.py not found in the current execution directory.[/]",
                        border_style="red",
                        width=self.__with_console
                    )
                )
                return

            # Run the setup.py script to build both sdist and wheel distributions
            subprocess.run(
                [sys.executable, "setup.py", "sdist", "bdist_wheel"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd=self.__project_root
            )

            # Notify the user that the build was successful
            self.__console.print(
                Panel(
                    "[green]✅ Build process completed successfully![/]",
                    border_style="green",
                    width=self.__with_console
                )
            )

        except subprocess.CalledProcessError as e:

            # Notify the user if the build process fails
            self.__console.print(
                Panel(
                    f"[bold red]❌ Build failed: {e}[/]",
                    border_style="red",
                    width=self.__with_console
                )
            )

    def __publish(self):
        """
        Uploads the built package distributions to the PyPI repository using Twine.

        This method locates the Twine executable (preferring the local virtual environment if available),
        and uploads all distribution files from the `dist/` directory to PyPI using the authentication
        token provided via the `PYPI_TOKEN` environment variable. If the token is missing, the process
        is aborted and an error message is displayed. After a successful upload, the method cleans up
        temporary Python bytecode files and `__pycache__` directories.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. All output is printed to the console.

        Raises
        ------
        subprocess.CalledProcessError
            If the Twine upload or cleanup commands fail.
        ValueError
            If the PyPI token is not found in the environment variables.
        """

        # Get the PyPI token from environment variables
        token = self.__token

        # Check if the PyPI token is available
        if not token:
            self.__console.print(
                Panel(
                    "[bold red]❌ Error: PyPI token not found in environment variables.[/]",
                    border_style="red",
                    width=self.__with_console
                )
            )
            return

        # Try to find 'twine' in the local virtual environment, otherwise use system PATH
        venv_twine = self.__project_root / 'venv' / 'Scripts' / 'twine'
        if venv_twine.exists():
            twine_path = str(venv_twine.resolve())
        else:
            twine_path = 'twine'

        # Notify user that the upload process is starting
        self.__console.print(
            Panel(
                "[cyan]📤 Uploading package to PyPI...[/]",
                border_style="cyan",
                width=self.__with_console
            )
        )

        # Upload the package distributions to PyPI using Twine
        try:
            subprocess.run(
                [twine_path, "upload", "dist/*", "-u", "__token__", "-p", token],
                check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.__project_root
            )
            self.__console.print(
                Panel(
                    "[green]✅ Package published successfully![/]",
                    border_style="green",
                    width=self.__with_console
                )
            )

        # Print error message and exit if upload fails
        except Exception as e:
            self.__console.print(
                Panel(
                    f"[bold red]🔴 Error uploading the package. Try changing the version and retry. Error: {e}[/]",
                    border_style="red",
                    width=self.__with_console
                )
            )
            exit(1)

        # Notify user that cleanup is starting
        self.__console.print(
            Panel(
                "[cyan]🧹 Cleaning up temporary files...[/]",
                border_style="cyan",
                width=self.__with_console
            )
        )

        # Remove all .pyc files and __pycache__ directories recursively
        subprocess.run(
            ["powershell", "-Command", "Get-ChildItem -Recurse -Filter *.pyc | Remove-Item; Get-ChildItem -Recurse -Filter __pycache__ | Remove-Item -Recurse"],
            check=True, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=self.__project_root
        )

        # Optionally, clear build artifacts (currently commented out)
        self.__clearRepository()

        # Notify user that the publishing process is complete
        self.__console.print(
            Panel(
                f"[bold green]✅ Publishing process completed successfully![/]",
                border_style="green",
                width=self.__with_console
            )
        )
        self.__console.print()

    def __clearRepository(self):
        """
        Removes temporary build artifacts and metadata directories from the project root.

        This method deletes the following directories if they exist:
            - `build/`: Contains temporary build files generated during packaging.
            - `dist/`: Contains distribution archives (e.g., .tar.gz, .whl) created by the build process.
            - `orionis.egg-info/`: Contains package metadata generated by setuptools.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method does not return any value. All output is printed to the console.

        Raises
        ------
        PermissionError
            If the method fails to delete any of the directories due to insufficient permissions.
        Exception
            If any other error occurs during the deletion process.
        """

        # List of directories to remove after publishing
        folders = ["build", "dist", "orionis.egg-info"]

        for folder in folders:
            folder_path = self.__project_root / folder

            # Check if the directory exists before attempting to remove it
            if os.path.exists(folder_path):

                # Recursively remove the directory and its contents
                try:
                    shutil.rmtree(folder_path)

                # Handle insufficient permissions error
                except PermissionError:
                    self.__console.print(
                        Panel(
                            f"[bold red]❌ Error: Could not remove {folder_path} due to insufficient permissions.[/]",
                            border_style="red",
                            width=self.__with_console
                        )
                    )

                # Handle any other exceptions that may occur
                except Exception as e:
                    self.__console.print(
                        Panel(
                            f"[bold red]❌ Error removing {folder_path}: {str(e)}[/]",
                            border_style="red",
                            width=self.__with_console
                        )
                    )

    def handle(self, reactor: IReactor) -> None:
        """
        Displays usage information and a list of available commands for the Orionis CLI.

        Parameters
        ----------
        reactor : IReactor
            The reactor instance providing command metadata via the `info()` method.

        Returns
        -------
        None
            This method does not return any value. It prints help information to the console.

        Raises
        ------
        CLIOrionisRuntimeError
            If an unexpected error occurs during help information generation or display.
        """
        try:

            # Execute  test suite
            response: dict = reactor.call("test")

            # Determinar si existieron errores en el test suite
            failed = response.get("failed", 0)
            errors = response.get("errors", 0)

            # If there are any failed tests, print a warning message
            if failed > 0 or errors > 0:
                console = Console()
                console.print(
                    Panel(
                        f"Tests failed: {failed}, Errors: {errors}",
                        title="Test Suite Results",
                        style="bold red"
                    )
                )

                # If there are failed tests, we do not proceed with the publishing
                return

            # Bump the minor version number
            self.__bumpMinorVersion()

            # Push changes to Git
            self.__gitPush()

            # Build the package
            self.__build()

            # Publish the package to PyPI
            self.__publish()

        except Exception as e:

            # Raise a custom runtime error if any exception occurs
            raise CLIOrionisRuntimeError(f"An unexpected error occurred: {e}") from e
