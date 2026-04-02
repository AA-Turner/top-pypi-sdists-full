import os
import logging
from typing import Dict, Set, Optional, Tuple

from seshat.utils.binary_utils import read_and_encode_file

logger = logging.getLogger(__name__)

# Maximum package size (50MB)
MAX_PACKAGE_SIZE = 50 * 1024 * 1024


def check_package_size(total_size: int) -> None:
    """
    Check if the package size exceeds the maximum allowed size.

    Args:
        total_size: Current size of the package in bytes

    Raises:
        ValueError: If the package size exceeds the maximum allowed size
    """
    if total_size > MAX_PACKAGE_SIZE:
        error_msg = (
            f"Package size ({total_size / (1024 * 1024):.2f}MB) exceeds maximum allowed size "
            f"({MAX_PACKAGE_SIZE / (1024 * 1024):.1f}MB)"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)


def add_file_to_package(
    filepath: str,
    relative_path: str,
    all_files: Dict[str, str],
    public_files: Optional[Dict[str, str]] = None,
    total_size: int = 0,
    echo_func=None,
) -> Tuple[int, bool]:
    """
    Add a file to the package, handling binary files appropriately.

    Args:
        filepath: Full path to the file
        relative_path: Relative path to store in the package
        all_files: Dictionary to store all files
        public_files: Optional dictionary to store public files
        total_size: Current total size of the package
        echo_func: Optional function to echo messages

    Returns:
        Tuple of (new_total_size, is_binary)
    """
    # Check package size
    check_package_size(total_size)

    # Read and encode the file
    try:
        content, is_binary = read_and_encode_file(filepath)

        # Add to all_files
        all_files[relative_path] = content

        # Add to public_files if provided
        if public_files is not None:
            public_files[relative_path] = content

        # Echo message if echo_func provided
        if echo_func:
            if is_binary:
                echo_func(f"📄 Added binary file {relative_path}")
            else:
                echo_func(f"📄 Added {relative_path}")

        # Update total size
        file_size = os.path.getsize(filepath)
        return total_size + file_size, is_binary

    except Exception as e:
        if echo_func:
            echo_func(f"⚠️ Error processing file {relative_path}: {str(e)}")
        logger.error(f"Error processing file {relative_path}: {str(e)}")
        return total_size, False


def extract_files_to_directory(
    files: Dict[str, str], binary_files: Set[str], directory: str, echo_func=None
) -> None:
    """
    Extract files from a package to a directory.

    Args:
        files: Dictionary of files (path -> content)
        binary_files: Set of binary file paths
        directory: Directory to extract to
        echo_func: Optional function to echo messages
    """
    from seshat.utils.binary_utils import decode_binary_content

    for file_path, content in files.items():
        file_full_path = os.path.join(directory, file_path)
        os.makedirs(os.path.dirname(file_full_path), exist_ok=True)

        # Check if this is a binary file
        is_binary = file_path in binary_files if binary_files else False

        if is_binary:
            # Decode binary content
            try:
                binary_content, encoding_type = decode_binary_content(content)
                with open(file_full_path, "wb") as f:
                    f.write(binary_content)
                if echo_func:
                    echo_func(
                        f"📄 Extracted binary file {file_path} ({encoding_type} encoded)"
                    )
            except Exception as e:
                if echo_func:
                    echo_func(
                        f"⚠️ Failed to decode binary content for {file_path}: {e}"
                    )
                # Write as-is as last resort
                with open(file_full_path, "w", encoding="utf-8") as f:
                    f.write(content)
        else:
            # Write text files normally
            with open(file_full_path, "w", encoding="utf-8") as f:
                f.write(content)
            if echo_func:
                echo_func(f"📄 Extracted {file_path}")
