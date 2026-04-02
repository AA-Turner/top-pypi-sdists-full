import os
import subprocess
import tempfile
from typing import Callable, NamedTuple

from seshat.general.models import CodePackage
from seshat.utils.binary_utils import read_and_encode_file
from seshat.utils.package_utils import extract_files_to_directory

MAIN_FILE_PATH_KEY = "main_file_path"
PYARMOR_RUNTIME = "pyarmor_runtime"


class ObfuscatedFiles(NamedTuple):
    """Named tuple for storing obfuscated files and binary files."""

    files: dict[str, str]
    binary_files: set[str]


def run_pyarmor(
    main_file_full_path: str, temp_dir: str, options: list[str] = None
) -> None:
    """Run pyarmor to obfuscate the code.

    Args:
        main_file_full_path: The path to the main file to be obfuscated
        temp_dir: The temporary directory where the obfuscated code will be output
        options: Optional list of additional pyarmor options
    """
    cmd = [
        "pyarmor",
        "gen",
    ]

    # Add custom options if provided, otherwise use default options
    if options:
        cmd.extend(options)
    else:
        cmd.extend(["--recursive"])

    # Always add output and main file path
    cmd.extend(
        [
            "--output",
            temp_dir,
            main_file_full_path,
        ]
    )

    subprocess.run(
        cmd,
        check=True,
        cwd=temp_dir,
    )


class Obfuscator:
    """Class for obfuscating code packages using pyarmor."""

    def __init__(
        self, echo_func: Callable | None = None, pyarmor_options: list[str] = None
    ):
        """Initialize the Obfuscator.

        Args:
            echo_func: Optional function for logging messages
            pyarmor_options: Optional list of pyarmor command options
        """
        self.echo = echo_func or (lambda x: None)
        self.pyarmor_options = pyarmor_options

    def _prepare_temp_directory(self, package: CodePackage, temp_dir: str) -> str:
        """Extract files to temporary directory and return the main file path.

        Args:
            package: The code package to extract
            temp_dir: The temporary directory to extract to

        Returns:
            The full path to the main file
        """
        main_file_path = package.metadata.get(MAIN_FILE_PATH_KEY)
        if not main_file_path:
            raise ValueError(f"{MAIN_FILE_PATH_KEY} not found in package metadata")

        extract_files_to_directory(
            files=package.files,
            binary_files=package.binary_files,
            directory=temp_dir,
            echo_func=self.echo,
        )

        return os.path.join(temp_dir, main_file_path)

    def _collect_obfuscated_files(self, temp_dir: str) -> ObfuscatedFiles:
        """Process obfuscated files and return files dict and binary files set.

        Args:
            temp_dir: The temporary directory containing obfuscated files

        Returns:
            ObfuscatedFiles named tuple with files and binary_files
        """
        obfuscated_files = {}
        binary_files = set()

        def scan_directory(directory):
            with os.scandir(directory) as entries:
                for entry in entries:
                    if entry.is_dir():
                        scan_directory(entry.path)
                    elif entry.is_file():
                        file_path = entry.path
                        relative_path = os.path.relpath(file_path, temp_dir)

                        force_binary = PYARMOR_RUNTIME in relative_path

                        content, is_binary = read_and_encode_file(
                            file_path=file_path,
                            is_binary=force_binary or None,
                        )

                        obfuscated_files[relative_path] = content
                        if is_binary:
                            binary_files.add(relative_path)
                            self.echo(f"📄 Added binary file {relative_path}")
                        else:
                            self.echo(f"📄 Added {relative_path}")

        scan_directory(temp_dir)
        return ObfuscatedFiles(files=obfuscated_files, binary_files=binary_files)

    def _add_non_python_files(
        self,
        package: CodePackage,
        obfuscated_files: dict[str, str],
        binary_files: set[str],
    ) -> None:
        """Add non-Python files from the original package to the obfuscated files.

        Args:
            package: The original code package
            obfuscated_files: The dictionary of obfuscated files to update
            binary_files: The set of binary files to update
        """
        for file_path, content in package.files.items():
            if file_path.endswith(".py"):
                continue

            if file_path in obfuscated_files:
                continue

            if file_path in package.binary_files:
                binary_files.add(file_path)

            obfuscated_files[file_path] = content

    def _create_obfuscated_package(
        self,
        package: CodePackage,
        obfuscated_files: dict[str, str],
        binary_files: set[str],
        obfuscated_main_path: str,
    ) -> CodePackage:
        """Create a new CodePackage with obfuscated files.

        Args:
            package: The original code package
            obfuscated_files: The dictionary of obfuscated files
            binary_files: The set of binary files
            obfuscated_main_path: The path to the obfuscated main file

        Returns:
            A new CodePackage with obfuscated files
        """
        updated_metadata = package.metadata.copy()
        updated_metadata[MAIN_FILE_PATH_KEY] = obfuscated_main_path

        self.echo(f"✅ Code obfuscated successfully. Main file: {obfuscated_main_path}")

        return CodePackage(
            name=package.name,
            version=package.version,
            executor_image_tag=package.executor_image_tag,
            files=obfuscated_files,
            metadata=updated_metadata,
            hash=package.hash,
            binary_files=binary_files,
        )

    def obfuscate_code(self, package: CodePackage) -> CodePackage:
        """Obfuscate code using pyarmor.

        Args:
            package: The code package to obfuscate

        Returns:
            A new CodePackage with obfuscated code

        Raises:
            ValueError: If obfuscation fails
            Exception: If any other error occurs during obfuscation
        """
        self.echo("🔒 Obfuscating code with pyarmor...")

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                main_file_full_path = self._prepare_temp_directory(package, temp_dir)

                run_pyarmor(main_file_full_path, temp_dir, self.pyarmor_options)

                obfuscated_files, binary_files = self._collect_obfuscated_files(
                    temp_dir
                )

                self._add_non_python_files(package, obfuscated_files, binary_files)

                obfuscated_main_path = package.metadata.get(MAIN_FILE_PATH_KEY)
                return self._create_obfuscated_package(
                    package, obfuscated_files, binary_files, obfuscated_main_path
                )

            except subprocess.CalledProcessError as e:
                self.echo(f"❌ Failed to obfuscate code: {str(e)}")
                raise ValueError(f"Failed to obfuscate code: {str(e)}")
            except Exception as e:
                self.echo(f"❌ An error occurred during obfuscation: {str(e)}")
                raise
