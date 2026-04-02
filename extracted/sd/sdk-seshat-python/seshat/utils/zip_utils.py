import json
import zipfile
import logging
from io import BytesIO
from typing import Dict, Set, BinaryIO, Optional

from seshat.utils.file import is_binary_file
from seshat.utils.binary_utils import encode_binary_content, decode_binary_content

logger = logging.getLogger(__name__)


def create_zip_from_files(
    files: Dict[str, str], binary_files: Set[str], metadata: Optional[Dict] = None
) -> BinaryIO:
    """
    Create a zip file from a dictionary of files.

    Args:
        files: Dictionary mapping file paths to content
        binary_files: Set of file paths that are binary
        metadata: Optional metadata to include in the zip

    Returns:
        BytesIO object containing the zip file
    """
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Add binary marker files
        for binary_file in binary_files:
            marker_file = f"{binary_file}.is_binary"
            # Skip adding marker files that might already be in the files
            if marker_file not in files:
                zip_file.writestr(marker_file, "")

        # Add all files
        for filename, content in files.items():
            # Skip marker files that might be in the files
            if filename.endswith(".is_binary"):
                continue

            if filename in binary_files:
                # For binary files, decode from base64 if it's a string
                if isinstance(content, str):
                    try:
                        # Decode binary content
                        binary_content, _ = decode_binary_content(content)
                        zip_file.writestr(filename, binary_content)
                    except Exception as e:
                        logger.error(
                            f"Failed to decode binary content for {filename}: {e}"
                        )
                        # Fall back to treating as string
                        zip_file.writestr(filename, content)
                else:
                    # Already binary
                    zip_file.writestr(filename, content)
            else:
                # Text files
                zip_file.writestr(filename, content)

        # Add metadata if provided
        if metadata:
            zip_file.writestr("metadata.json", json.dumps(metadata))

    zip_buffer.seek(0)
    return zip_buffer


def extract_zip(zip_data: BinaryIO) -> Dict:
    """
    Extract files and metadata from a zip file.

    Args:
        zip_data: BytesIO object containing the zip file

    Returns:
        Dictionary with extracted files, binary_files, and metadata
    """
    files = {}
    binary_files = set()
    metadata = {}

    with zipfile.ZipFile(zip_data) as zip_file:
        # Extract metadata if present
        if "metadata.json" in zip_file.namelist():
            metadata = json.loads(zip_file.read("metadata.json"))

        # First pass: identify binary files from markers
        for filename in zip_file.namelist():
            if filename.endswith(".is_binary"):
                # The actual file is the name without the .is_binary suffix
                binary_file = filename[:-10]  # Remove .is_binary
                binary_files.add(binary_file)
            # Also check for binary files by extension
            elif is_binary_file(filename):
                binary_files.add(filename)

        # Extract files
        for filename in zip_file.namelist():
            # Skip metadata and marker files
            if filename == "metadata.json" or filename.endswith(".is_binary"):
                continue

            file_content = zip_file.read(filename)

            # Handle binary files
            if filename in binary_files:
                # Store binary content as base64 encoded string
                files[filename] = encode_binary_content(file_content)
            else:
                # Try to decode as UTF-8 text
                try:
                    files[filename] = file_content.decode("utf-8")
                except UnicodeDecodeError:
                    # If decoding fails, assume it's a binary file without a marker
                    logger.warning(
                        f"File {filename} has no binary marker but appears to be binary. Treating as binary."
                    )
                    binary_files.add(filename)
                    files[filename] = encode_binary_content(file_content)

    return {"files": files, "binary_files": binary_files, "metadata": metadata}
