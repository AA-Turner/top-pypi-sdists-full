import hashlib
from shipyard_templates import ShipyardLogger
import re
from pathlib import Path

logger = ShipyardLogger.get_logger()


def hash_text(text_var: str, hash_algorithm="sha256"):
    """
    Hash the provided text with a specified hash_algorithm.
    """
    logger.debug(f"Hashing {text_var} with {hash_algorithm}...")

    hash_algorithms = {
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
        "md5": hashlib.md5,
    }

    if hash_algorithm not in hash_algorithms:
        logger.error(f"Hash algorithm {hash_algorithm} is not supported.")
        raise ValueError(f"Hash algorithm {hash_algorithm} is not supported.")

    hashed_text = hash_algorithms[hash_algorithm](text_var.encode("ascii")).hexdigest()
    logger.debug(f"Successfully hashed: {hashed_text}")

    return hashed_text


def content_file_injection(text_input: str) -> str:
    """
    Replace every {{text:filename}} marker in *text_input* with the file’s UTF‑8 text.

    Args:
        text_input: String that may contain zero or more {{text:...}} placeholders.

    Returns:
        The text with each placeholder replaced by the corresponding file’s contents.

    Raises:
        FileNotFoundError   – if a referenced file does not exist
        OSError             – for other I/O problems (permissions, etc.)
    """
    file_pattern = re.compile(r"\{\{\s*text:(?P<filename>[^{}\s]+)\s*}}")

    def _inject(match: re.Match) -> str:
        file_name = match["filename"]
        path = Path(file_name)

        try:
            return path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_name}' not found") from None
        except OSError as exc:
            raise OSError(f"Error opening '{file_name}': {exc}") from None

    return file_pattern.sub(_inject, text_input)
