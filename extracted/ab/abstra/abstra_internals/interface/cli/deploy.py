import pathlib
import tempfile
import time
import uuid
import zipfile
from typing import Optional

import requests

from abstra_internals.cloud_api import create_build, get_api_key_info, update_build
from abstra_internals.credentials import resolve_headers
from abstra_internals.environment import REQUEST_TIMEOUT
from abstra_internals.interface.cli.deploy_messages import DeployMessages
from abstra_internals.logger import AbstraLogger
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings

_UPLOAD_MAX_ATTEMPTS = 3
_UPLOAD_RETRY_BASE_DELAY_SECONDS = 1.0


class ZipValidationError(Exception):
    """Raised when the generated zip file fails validation."""

    pass


class MissingCredentialsError(Exception):
    """Raised when there are no credentials to authenticate the deploy."""

    pass


def _validate_zip_file(zip_path: pathlib.Path) -> None:
    """
    Validates the generated zip file before upload.
    Raises ZipValidationError if validation fails.
    """
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        file_list = zip_file.namelist()

        # Check if zip is empty
        if not file_list:
            raise ZipValidationError(
                "The generated zip file is empty. No files were packaged for deploy. "
                "Please check your .gitignore file and ensure your project files exist. "
                "If the problem persists, contact us."
            )

        # Check if abstra.json exists
        if "abstra.json" not in file_list:
            raise ZipValidationError(
                "The abstra.json file is missing from the deploy package. "
                "This file is required for deployment. Please ensure it exists in your project root. "
                "If the problem persists, contact us."
            )


def _generate_zip_file() -> pathlib.Path:
    root_path = Settings.root_path
    zip_path = pathlib.Path(tempfile.gettempdir(), f"{uuid.uuid4()}.zip")

    with zipfile.ZipFile(zip_path, "w") as zip_file:
        for file in FileSystemService.list_files(root_path, use_ignore=True):
            # Always exclude .env from the bundle: `git check-ignore` returns
            # "not ignored" for files already tracked, so relying on .gitignore
            # alone leaks secrets when the user committed .env before ignoring it.
            if file.name == ".env" and file.parent == root_path:
                continue
            zip_file.write(file, file.relative_to(root_path))

    return zip_path


def _upload_file(url: str, file_path: pathlib.Path):
    """Upload the deploy bundle to the presigned S3 URL.

    The presigned PUT can come back with a non-2xx status (e.g. 403 once the
    URL has expired, or a transient 5xx). ``requests.put`` does NOT raise on
    those, so without an explicit status check the failure is silent: the build
    gets finalized while the object never reached S3, and the builder later
    fails to download a zip that isn't there. Check the status and retry
    transient failures; fail fast on 4xx that won't fix themselves on retry.
    """
    body = file_path.read_bytes()

    last_error: Optional[Exception] = None
    for attempt in range(1, _UPLOAD_MAX_ATTEMPTS + 1):
        try:
            response = requests.put(url=url, data=body, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            # 4xx won't recover on retry (e.g. an expired/invalid presigned URL
            # returns 403), except for the throttling/retriable ones.
            if status is not None and 400 <= status < 500 and status not in (408, 429):
                raise
            last_error = e
        except (requests.ConnectionError, requests.Timeout) as e:
            last_error = e

        if attempt < _UPLOAD_MAX_ATTEMPTS:
            time.sleep(_UPLOAD_RETRY_BASE_DELAY_SECONDS * 2 ** (attempt - 1))

    raise last_error or RuntimeError("Failed to upload deploy bundle to S3")


def _get_project_id(headers: dict) -> Optional[str]:
    try:
        api_key_info = get_api_key_info(headers)
        if api_key_info.get("logged"):
            return api_key_info.get("info", {}).get("projectId")
    except Exception:
        pass
    return None


def deploy_without_git(show_start_message: bool = True):
    if show_start_message:
        DeployMessages.start(method="upload")

    DeployMessages.authenticating()
    headers = resolve_headers()
    if not headers:
        DeployMessages.no_credentials()
        raise MissingCredentialsError(
            "No credentials found. Please log in and try again."
        )

    data = create_build(headers)

    try:
        DeployMessages.packaging()
        zip_path = _generate_zip_file()
        _validate_zip_file(zip_path)

        DeployMessages.uploading()
        _upload_file(url=data.url, file_path=zip_path)

        DeployMessages.finalizing()
        update_build(headers=headers, build_id=data.build_id)

        project_id = _get_project_id(headers)
        DeployMessages.success(project_id)
    except ZipValidationError as e:
        update_build(headers=headers, build_id=data.build_id, error=str(e))
        DeployMessages.validation_error(str(e))
        raise e
    except Exception as e:
        update_build(
            headers=headers, build_id=data.build_id, error="Failed to upload files"
        )
        DeployMessages.error(str(e))
        AbstraLogger.capture_exception(e)
        raise e
