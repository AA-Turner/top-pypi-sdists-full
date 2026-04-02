import base64
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def encode_binary_content(binary_content: bytes) -> str:
    """
    Encode binary content as base64 string.

    Args:
        binary_content: The binary content to encode

    Returns:
        Base64 encoded string
    """
    return base64.b64encode(binary_content).decode("ascii")


def decode_binary_content(content: str) -> Tuple[bytes, str]:
    """
    Attempt to decode binary content from base64 or hex encoding.

    Args:
        content: The encoded content as string

    Returns:
        Tuple of (decoded_content, encoding_type) where encoding_type is 'base64', 'hex', or 'unknown'
    """
    # Try base64 decoding first (new format)
    try:
        binary_content = base64.b64decode(content)
        return binary_content, "base64"
    except Exception:
        # Try hex decoding as fallback (old format)
        try:
            binary_content = bytes.fromhex(content)
            return binary_content, "hex"
        except Exception as e:
            logger.warning(f"Failed to decode content: {e}")
            return content.encode("utf-8"), "unknown"


def read_binary_file(file_path: str) -> bytes:
    """
    Read a binary file and return its content.

    Args:
        file_path: Path to the binary file

    Returns:
        Binary content of the file
    """
    with open(file_path, "rb") as f:
        return f.read()


def read_and_encode_file(file_path: str, is_binary: bool = None) -> Tuple[str, bool]:
    """
    Read a file and encode it appropriately based on whether it's binary.

    Args:
        file_path: Path to the file
        is_binary: Whether the file is binary. If None, will attempt to detect.

    Returns:
        Tuple of (encoded_content, is_binary)
    """
    from seshat.utils.file import is_binary_file

    # Determine if binary if not specified
    if is_binary is None:
        is_binary = is_binary_file(file_path)

    try:
        if is_binary:
            # Read as binary and encode as base64
            binary_content = read_binary_file(file_path)
            return encode_binary_content(binary_content), True
        else:
            # Try to read as text
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read(), False
    except UnicodeDecodeError:
        # If we get here, the file was not detected as binary but is binary
        logger.warning(
            f"File {file_path} appears to be binary but wasn't detected by extension"
        )
        binary_content = read_binary_file(file_path)
        return encode_binary_content(binary_content), True
