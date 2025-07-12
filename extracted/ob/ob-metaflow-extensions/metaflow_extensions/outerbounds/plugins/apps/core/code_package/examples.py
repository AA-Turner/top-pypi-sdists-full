"""
Examples demonstrating how to use the code packager abstraction.

This file provides usage examples for the code packager classes.
These examples are for documentation purposes and are not meant to be run directly.
"""

import os
import sys
from io import BytesIO
from typing import List, Dict, Any, Callable, Optional

from .code_packager import CodePackager


def basic_usage_example(datastore_type: str = "s3") -> None:
    """
    Basic usage example with ContentAddressedStore.

    This example shows how to:
    1. Define paths to include in a package
    2. Create a package using CodePackager's default packaging
    3. Store the package using ContentAddressedStore directly
    4. Generate a download command

    Parameters
    ----------
    datastore_type : str, default "s3"
        The type of datastore to use: "s3", "azure", "gs", or "local"
    """
    # Define the paths to include in the package
    paths_to_include = ["./"]

    # Define which file suffixes to include
    file_suffixes = [".py", ".md"]

    # Create metadata for the package
    metadata = {"example": True, "timestamp": "2023-01-01T00:00:00Z"}

    # Initialize the packager with datastore configuration
    packager = CodePackager(
        datastore_type=datastore_type,
        code_package_prefix="my-custom-prefix",  # Optional
    )

    # Store the package with packaging parameters
    package_url, package_key = packager.store(
        paths_to_include=paths_to_include,
        file_suffixes=file_suffixes,
        metadata=metadata,
    )

    # Generate a download command
    download_cmd = CodePackager.get_download_cmd(
        package_url=package_url,
        datastore_type=datastore_type,
        target_file="my_package.tar",
    )

    # Generate complete package commands for downloading and setup
    package_commands = packager.get_package_commands(
        code_package_url=package_url,
        target_file="my_package.tar",
        working_dir="my_app",
    )

    # Print some information
    print(f"Package URL: {package_url}")
    print(f"Package Key: {package_key}")
    print(f"Download Command: {download_cmd}")
    print(f"Complete package commands: {package_commands}")


def usage_with_custom_package_function(datastore_type: str = "s3") -> None:
    """
    Example of using the CodePackager with a custom package creation function.

    Parameters
    ----------
    datastore_type : str, default "s3"
        The type of datastore to use: "s3", "azure", "gs", or "local"
    """

    # Define a custom package function
    def create_custom_package():
        # This is a simple example - in real use, you might create a more complex package
        from io import BytesIO
        import tarfile
        import time

        buf = BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tar:
            # Add a simple file to the tarball
            content = b"print('Hello, custom package!')"
            info = tarfile.TarInfo(name="hello.py")
            info.size = len(content)
            info.mtime = int(time.time())
            file_object = BytesIO(content)
            tar.addfile(info, file_object)

        return bytearray(buf.getvalue())

    # Initialize the packager with datastore configuration
    packager = CodePackager(datastore_type=datastore_type)

    # Store the package with the custom package function
    package_url, package_key = packager.store(package_create_fn=create_custom_package)

    # Generate a download command
    download_cmd = CodePackager.get_download_cmd(
        package_url=package_url,
        datastore_type=datastore_type,
        target_file="custom_package.tar",
    )

    # Generate complete package commands
    package_commands = packager.get_package_commands(
        code_package_url=package_url,
    )

    # Print some information
    print(f"Package URL: {package_url}")
    print(f"Package Key: {package_key}")
    print(f"Download Command: {download_cmd}")
    print(f"Complete commands: {package_commands}")
