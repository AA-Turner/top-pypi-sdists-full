import ast
import datetime
import io
import os
import platform
import re
import subprocess
import sys
import tarfile
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import PyInstaller.__main__
import tomli

DEFAULT_EXCLUDE_MODULES = (
    "IPython",
    "jedi",
    "fastapi",
    "watchfiles",
    "uvicorn",
    "fastapi",
)

__all__ = (
    "compile_executable_for_onprem",
    "collect_package_data_files",
    "DEFAULT_EXCLUDE_MODULES",
    "get_about_path_from_package",
    "get_version_from_package",
)


def collect_package_data_files(connector_root_dir: Path) -> list[tuple[Path, str]]:
    """
    Read ``[tool.setuptools.package-data]`` from ``connector_root_dir/pyproject.toml``
    and return ``(absolute_source, bundle_destination)`` pairs.

    The destination is package-relative (e.g. ``sap_s_4hana/instructions``) so
    PyInstaller places each file where ``Path(__file__).parent`` expects it at
    runtime. PyInstaller does not honor setuptools' ``package-data`` declaration on
    its own, so we resolve it here and feed the files in via ``--add-data``.

    Returns an empty list when there is no ``pyproject.toml`` or no
    ``package-data`` table (a no-op for connectors without data files).
    """
    pyproject_path = connector_root_dir / "pyproject.toml"
    if not pyproject_path.is_file():
        return []

    with pyproject_path.open("rb") as f:
        pyproject = tomli.load(f)

    package_data = pyproject.get("tool", {}).get("setuptools", {}).get("package-data", {})
    if not package_data:
        return []

    collected: list[tuple[Path, str]] = []
    for package, patterns in package_data.items():
        # Skip wildcards keys since they are overly broad
        if package in ("", "*"):
            print(
                f"Skipping unsupported wildcard package-data key {package!r} in "
                f"{pyproject_path}",
                file=sys.stderr,
            )
            continue

        package_path = package.replace(".", "/")
        package_dir = connector_root_dir / package_path
        for pattern in patterns:
            for source in sorted(package_dir.glob(pattern)):
                if not source.is_file():
                    continue
                relative_parent = source.relative_to(package_dir).parent
                destination = (
                    package_path
                    if relative_parent == Path(".")
                    else f"{package_path}/{relative_parent}"
                )
                collected.append((source.resolve(), destination))

    return collected


def compile_executable_for_onprem(
    *,
    connector_root_module_dir: Path,
    app_id: str,
    exclude_modules: Iterable[str],
    sdk_root: Path,
    compile_directory: Path | None = None,
) -> None:
    connector_main_path = connector_root_module_dir / "main.py"
    module_name = os.path.basename(connector_root_module_dir)
    connector_root_dir = connector_root_module_dir.parent

    # Collect package-data files declared in the connector's pyproject.toml, since
    # PyInstaller doesn't honor setuptools' package-data declaration on its own.
    resolved_data_files = collect_package_data_files(connector_root_dir)
    if resolved_data_files:
        print(
            f"Auto-collected {len(resolved_data_files)} package-data file(s): "
            f"{', '.join(str(src) for src, _ in resolved_data_files)}",
            file=sys.stderr,
        )

    fs_timestamp = re.sub(r"\W", "-", datetime.datetime.now(datetime.timezone.utc).isoformat())
    timestamped_build_dir = Path(os.getcwd()) / "compiled" / f"{app_id}-{fs_timestamp}"

    if not compile_directory:
        compile_directory = timestamped_build_dir
    compile_directory.mkdir(parents=True, exist_ok=True)

    spec_directory = compile_directory / "spec"
    spec_directory.mkdir(parents=True, exist_ok=True)

    if not os.path.isfile(connector_main_path):
        raise RuntimeError(f"No entrypoint found for {module_name} at {connector_main_path}")

    # Find path to nearest __about__.py from path
    version = get_version_from_package(connector_root_dir)

    # Find the connector-sdk-types package directory
    current_dir = Path(__file__).parent  # connector/
    sdk_types_path = current_dir.parent.parent / "connector-sdk-types"

    print(f"Compiling executable for {app_id} in {compile_directory}", file=sys.stderr)

    # Generate third-party licenses file
    try:
        subprocess.run(["pip-licenses", "--version"], check=True, capture_output=True, text=True)
    except FileNotFoundError:
        print("pip-licenses not found in PATH. Please pip install pip-licenses", file=sys.stderr)
        return
    except subprocess.CalledProcessError as e:
        print(
            f"pip-licenses --version command failed with exit code {e.returncode}", file=sys.stderr
        )
        print(f"STDOUT: {e.stdout}", file=sys.stderr)
        print(f"STDERR: {e.stderr}", file=sys.stderr)
        return

    licenses_command = [
        "pip-licenses",
        "--with-license-file",
        "--with-authors",
        "--with-urls",
        "--format=plain-vertical",
        "--output-file",
        # Unclear why this needs to go in the spec directory,
        # but otherwise pyinstaller won't find it
        f"{compile_directory}/spec/THIRD_PARTY_LICENSES.txt",
    ]
    try:
        subprocess.run(licenses_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"pip-licenses command failed with exit code {e.returncode}", file=sys.stderr)
        print(f"Command: {' '.join(licenses_command)}", file=sys.stderr)
        print(f"STDOUT: {e.stdout}", file=sys.stderr)
        print(f"STDERR: {e.stderr}", file=sys.stderr)
        raise

    # Build PyInstaller arguments
    pyinstaller_args = [
        str(connector_main_path.absolute()),
        "--clean",
        f"--paths={sdk_root.absolute()}",
        f"--paths={sdk_types_path.absolute()}",
        "-y",
        f"--distpath={compile_directory / 'dist'}",
        f"--workpath={compile_directory / 'work'}",
        f"--specpath={compile_directory / 'spec'}",
        "--log-level=ERROR",
        "--add-data",
        f"THIRD_PARTY_LICENSES.txt{os.pathsep}.",
        *[f"--exclude-module={module}" for module in exclude_modules],
        "--exclude-module=pkg_resources",
    ]

    # Add resolved data files with their directory structure preserved
    for resolved_file, destination in resolved_data_files:
        # PyInstaller --add-data format: source:destination
        # Destination preserves the directory structure from connector root
        pyinstaller_args.extend(
            ["--add-data", f"{resolved_file.absolute()}{os.pathsep}{destination}"]
        )

    PyInstaller.__main__.run(pyinstaller_args)

    try:
        os.remove("THIRD_PARTY_LICENSES.txt")
    except FileNotFoundError:
        pass
    main_location = compile_directory / "dist" / "main" / "main"
    print("Compiled to:", main_location, file=sys.stderr)
    print("Bundling compiled code to", compile_directory / "bundled", file=sys.stderr)
    archive_location = bundle_onprem(
        BundleDetails(
            source_root_directory=connector_root_dir,
            compiled_root_directory=compile_directory / "dist" / "main",
            bundle_directory=compile_directory / "bundled",
            version=version,
            app_id=app_id,
        )
    )
    print("Bundled into:", file=sys.stderr)
    print(archive_location)


def get_about_path_from_package(package_path: Path) -> Path:
    """
    Find the closest `__about__.py` file to a package's root directory.

    Raise if no file is found.
    """
    nearest_about_file = None
    shortest_distance = float("inf")

    for filepath in package_path.rglob("__about__.py"):
        relative_path = filepath.relative_to(package_path)
        distance = len(relative_path.parts)
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_about_file = filepath

    if not nearest_about_file:
        raise FileNotFoundError(f"__about__.py not found in {package_path}")
    return nearest_about_file


def get_version_from_package(package_path: Path) -> str:
    """
    Get the __version__ member set from the package's __about__.py file.

    Raises if there's no version found.
    """
    about_file_path = get_about_path_from_package(package_path)
    with about_file_path.open("r") as f:
        node = ast.parse(f.read(), filename=str(about_file_path))
        for element in node.body:
            if isinstance(element, ast.Assign):
                for target in element.targets:
                    if isinstance(target, ast.Name) and target.id == "__version__":
                        if isinstance(element.value, ast.Constant):  # For Python 3.8+
                            if isinstance(element.value.value, str):
                                return element.value.value
    raise RuntimeError(f"Unable to find __version__ in {about_file_path}")


@dataclass(frozen=True)
class BundleDetails:
    """A package we build and test in this repo"""

    source_root_directory: Path
    """Location of the pyproject.toml"""

    compiled_root_directory: Path
    """Where we've compiled this connector with pyinstaller"""

    bundle_directory: Path
    """Where we should write the bundled archive"""

    version: str
    """The version of this connector"""

    app_id: str
    """An importable Python module name. Underscores, no hyphens"""


def bundle_onprem(bundle: BundleDetails) -> Path:
    system = platform.system().lower()  # linux or windows
    bundle.bundle_directory.mkdir(parents=True, exist_ok=True)

    metadata_file_content = connector_metadata_file(
        app_id=f"{bundle.app_id.removesuffix('_on_prem')}_on_prem", version=bundle.version
    )

    archive_filename = get_archive_filename(bundle)

    if system == "windows":
        local_file_path = bundle.bundle_directory / archive_filename
        with zipfile.ZipFile(local_file_path, "w") as zipf:
            for file in (bundle.compiled_root_directory).rglob("*"):
                location_in_archive = file.relative_to(bundle.compiled_root_directory)
                zipf.write(file, location_in_archive)

            zipf.writestr("metadata.toml", metadata_file_content)
        return local_file_path
    else:
        local_file_path = bundle.bundle_directory / archive_filename
        # change file permissions across the whole tree before archiving, as these
        # are preserved in the tar. tar.add() recurses into directories, so every
        # descendant must already have the desired mode before its parent is added.
        for path in bundle.compiled_root_directory.rglob("*"):
            os.chmod(path, 0o770)
        with tarfile.open(local_file_path, "w:gz") as tar:
            for file in (bundle.compiled_root_directory).rglob("*"):
                location_in_archive = file.relative_to(bundle.compiled_root_directory)
                tar.add(file, location_in_archive)

            tarinfo = tarfile.TarInfo(name="metadata.toml")
            tarinfo.size = len(metadata_file_content)
            tar.addfile(tarinfo, io.BytesIO(metadata_file_content.encode("utf-8")))
        return local_file_path


def get_archive_filename(bundle: BundleDetails) -> str:
    file_without_extension = f"{bundle.app_id}-{bundle.version}"
    extension = "tar.gz"
    if platform.system() == "Windows":
        extension = "zip"
    return f"{file_without_extension}.{extension}"


def connector_metadata_file(app_id: str, version: str) -> str:
    """
    This metadata file is used by the on prem agent. The agent reads this file's contents
    to grab the connector version and determine whether to auto update.
    """
    return f"""[connector]
app_id = "{app_id}"
version = "{version}"
"""
