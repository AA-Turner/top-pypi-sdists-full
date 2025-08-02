"""WARC file utilities for web automation."""

from pathlib import Path
from typing import Dict, Any
import logging

try:
    from warcio.archiveiterator import ArchiveIterator
except ImportError:
    raise ImportError(
        "warcio is required for WARC functionality. Install with: pip install warcio"
    )

logger = logging.getLogger(__name__)


def parse_warc_file(warc_file_path: Path) -> Dict[str, Dict[str, Any]]:
    """
    Parse a WARC file and extract response records.

    Args:
        warc_file_path: Path to the WARC file

    Returns:
        Dictionary mapping URLs to response data (status, headers, body)

    Raises:
        FileNotFoundError: If WARC file doesn't exist
        ValueError: If warc_file_path is not a Path object
    """
    responses = {}

    # Check if file exists
    if not warc_file_path.exists():
        raise FileNotFoundError(f"WARC file not found: {warc_file_path}")

    # Open file using context manager
    with open(warc_file_path, "rb") as f:
        for record in ArchiveIterator(f):
            if record.rec_type == "response":
                target_uri = record.rec_headers.get_header("WARC-Target-URI")
                if target_uri:
                    # Parse HTTP response
                    status_code = 200
                    headers = {}
                    body = b""

                    if record.http_headers:
                        # Extract status code
                        status_line = record.http_headers.get_statuscode()
                        if status_line:
                            try:
                                status_code = int(status_line)
                            except (ValueError, TypeError):
                                status_code = 200

                        # Extract headers
                        for header_name, header_value in record.http_headers.headers:
                            # Handle both bytes and str cases
                            name = (
                                header_name.decode("utf-8")
                                if isinstance(header_name, bytes)
                                else header_name
                            )
                            value = (
                                header_value.decode("utf-8")
                                if isinstance(header_value, bytes)
                                else header_value
                            )
                            headers[name] = value

                    # Read the response body
                    if record.content_stream():
                        body = record.content_stream().read()

                    responses[target_uri] = {
                        "status": status_code,
                        "headers": headers,
                        "body": body,
                    }

    return responses
