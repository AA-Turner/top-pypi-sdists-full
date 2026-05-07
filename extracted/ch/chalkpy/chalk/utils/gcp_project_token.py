from __future__ import annotations

import base64
import dataclasses
import os
import tempfile
from typing import TYPE_CHECKING

from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception

if TYPE_CHECKING:
    from google.auth.credentials import Credentials


_logger = get_logger(__name__)


@dataclasses.dataclass
class GCPProjectToken:
    credentials: Credentials
    project: str | None


def _base64_decode_str(s: str) -> str:
    return base64.b64decode(s).decode("utf-8")


def _read_b64_credentials(filename: str) -> str:
    with open(filename, "r") as creds:
        return _base64_decode_str(creds.read())


def _read_raw_json_credentials(filename: str) -> str:
    with open(filename, "r") as creds:
        return creds.read()


def get_credentials_from_file_base64(creds_filepath: str):
    try:
        import google.auth
    except ImportError:
        raise missing_dependency_exception("chalkpy[runtime]")
    with tempfile.TemporaryDirectory() as tmp_dir:
        temp_filename = os.path.join(tmp_dir, "credentials.json")
        with open(temp_filename, "w") as temp_creds_file:
            try:
                # first try to base64 decode the creds. But maybe in staging they are raw JSON...
                creds = _read_b64_credentials(creds_filepath)
            except Exception:
                # so if we get an exception here just try to read the raw file without decoding
                creds = _read_raw_json_credentials(creds_filepath)
            temp_creds_file.write(creds)

        creds, project = google.auth.load_credentials_from_file(temp_filename)
        return GCPProjectToken(project=project, credentials=creds)
