import asyncio
import fnmatch
import json
import logging
import shutil
import tempfile
import time
import zipfile
from os import PathLike
from pathlib import Path
from typing import Any, NoReturn
from uuid import UUID

import aiofiles
import requests as requests_lib
from httpx import (
    AsyncClient,
    Client,
    ConnectError,
    HTTPStatusError,
    QueryParams,
    ReadError,
    RemoteProtocolError,
    TimeoutException,
    codes,
)
from lmi.utils import gather_with_concurrency
from pydantic import HttpUrl
from tenacity import (
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
)
from tqdm import tqdm

from edison_client.clients.exceptions import (
    DataStorageConflictError,
    DataStorageCreationError,
    DataStorageError,
    DataStorageNotFoundError,
    DataStoragePermissionError,
    DataStorageRetrievalError,
    DataStorageValidationError,
    RestClientError,  # noqa: F401 - re-exported for backward compatibility
)
from edison_client.clients.multipart_upload import (
    _aupload_file_multipart,
    _upload_file_multipart,
)
from edison_client.models.data_storage_methods import (
    CreateDatasetPayload,
    DataContentType,
    DataStorageEntryStatusResponse,
    DataStorageLocationPayload,
    DataStorageRequestPayload,
    DataStorageResponse,
    DataStorageRevisionListResponse,
    DataStorageRevisionUpdate,
    DataStorageType,
    DirectoryManifest,
    GetDatasetAndEntriesResponse,
    ManifestEntry,
    PermittedAccessors,
    RawFetchResponse,
    ShareStatus,
)
from edison_client.models.rest import (
    DataStorageSearchPayload,
    FilterLogic,
    SearchCriterion,
)
from edison_client.utils.general import retry_if_connection_error

# this is only required if they're using a yaml manifest
try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]


logger = logging.getLogger(__name__)

# TODO: [PLA-1160] pdf support, unsure what package we want to use
SUPPORTED_FILE_TYPES_TO_TEXT_CONTENT = ["txt", "md", "csv", "json", "yaml", "yml"]
SMALL_FILE_THRESHOLD_BYTES = 10 * 1024 * 1024  # 10MB
DOWNLOAD_CONCURRENCY = 3
MAX_REVISION_HISTORY_LIMIT = 100


def _entry_read_url(
    entry_id: UUID | str, version: int | None, revision_id: UUID | None
) -> str:
    if version is not None and revision_id is not None:
        raise DataStorageValidationError(
            "Select a revision by ID or version number, not both."
        )
    if version is not None and version < 0:
        raise DataStorageValidationError("Version must be zero or greater.")
    url = f"/v0.1/data-storage/data-entries/{entry_id}"
    if version is not None:
        return f"{url}?{QueryParams(version=version)}"
    if revision_id is not None:
        return f"{url}?{QueryParams(revision_id=str(revision_id))}"
    return url


def _revision_history_params(
    limit: int, offset: int, include_unpublished: bool
) -> dict:
    if not 1 <= limit <= MAX_REVISION_HISTORY_LIMIT or offset < 0:
        raise DataStorageValidationError(
            "History requires limit between 1 and 100 and a nonnegative offset."
        )
    return {
        "limit": limit,
        "offset": offset,
        "include_unpublished": include_unpublished,
    }


def _should_ignore_file(
    file_path: Path | PathLike,
    base_path: Path | PathLike,
    ignore_patterns: list[str] | None = None,
) -> bool:
    """Check if a file should be ignored based on ignore patterns.

    Args:
        file_path: Path to the file to check
        base_path: Base directory path
        ignore_patterns: List of ignore patterns (supports gitignore-style patterns)

    Returns:
        True if file should be ignored
    """
    if not ignore_patterns:
        return False

    try:
        file_path = Path(file_path)
        base_path = Path(base_path)
        rel_path = file_path.relative_to(base_path)
        rel_path_str = str(rel_path)

        for pattern in ignore_patterns:
            pattern = pattern.strip()
            if not pattern or pattern.startswith("#"):
                continue

            is_absolute_match = pattern.startswith("/") and rel_path_str.startswith(
                pattern[1:]
            )
            is_nested_match = "/" in pattern and pattern in rel_path_str
            is_name_match = fnmatch.fnmatch(file_path.name, pattern)
            is_part_match = pattern in rel_path.parts

            if is_absolute_match or is_nested_match or is_name_match or is_part_match:
                return True

    except ValueError:
        pass

    return False


def _read_ignore_file(dir_path: Path, ignore_filename: str = ".gitignore") -> list[str]:
    """Read ignore patterns from a file in the directory.

    Args:
        dir_path: Directory to look for ignore file
        ignore_filename: Name of ignore file to read

    Returns:
        List of ignore patterns
    """
    ignore_file = dir_path / ignore_filename
    if ignore_file.exists():
        try:
            with open(ignore_file, encoding="utf-8") as f:
                return [line.strip() for line in f]
        except Exception as e:
            logger.warning(f"Failed to read {ignore_filename}: {e}")
            return []
    else:
        return []


def _collect_ignore_patterns(
    dir_path: Path,
    ignore_patterns: list[str] | None = None,
    ignore_filename: str = ".gitignore",
) -> list[str]:
    """Collect all ignore patterns from multiple sources.

    Args:
        dir_path: Directory to check for ignore files
        ignore_patterns: Explicit ignore patterns
        ignore_filename: Name of ignore file to read from directory

    Returns:
        Combined list of ignore patterns
    """
    all_ignore_patterns = ignore_patterns or []
    file_patterns = _read_ignore_file(dir_path, ignore_filename)
    all_ignore_patterns.extend(file_patterns)

    default_ignores = [".git", "__pycache__", "*.pyc", ".DS_Store", "node_modules"]
    all_ignore_patterns.extend(default_ignores)

    return all_ignore_patterns


def _create_directory_zip(
    dir_path: Path,
    zip_path: Path,
    ignore_patterns: list[str] | None = None,
    ignore_filename: str = ".gitignore",
) -> int:
    """Create a zip file from a directory with ignore patterns.

    Args:
        dir_path: Directory to zip
        zip_path: Output zip file path
        ignore_patterns: Explicit ignore patterns
        ignore_filename: Name of ignore file to read from directory

    Returns:
        Size of created zip file in bytes
    """
    all_ignore_patterns = _collect_ignore_patterns(
        dir_path, ignore_patterns, ignore_filename
    )

    logger.debug(f"Creating zip with ignore patterns: {all_ignore_patterns}")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in dir_path.rglob("*"):
            if file_path.is_file() and not _should_ignore_file(
                file_path, dir_path, all_ignore_patterns
            ):
                arcname = file_path.relative_to(dir_path)
                zipf.write(file_path, arcname)
                logger.debug(f"Added to zip: {arcname}")

    zip_size = zip_path.stat().st_size
    logger.debug(f"Created zip file {zip_path} with size {zip_size:,} bytes")
    return zip_size


def _should_send_as_text_content(file_path: Path, file_size: int) -> bool:
    """Check if a file should be sent as text content instead of file upload.

    Args:
        file_path: Path to the file
        file_size: Size of file in bytes

    Returns:
        True if file should be sent as text content
    """
    # small files can be treated as raw text
    if file_size >= SMALL_FILE_THRESHOLD_BYTES:
        return False

    file_extension = file_path.suffix.lower().lstrip(".")
    return file_extension in SUPPORTED_FILE_TYPES_TO_TEXT_CONTENT


def _extract_text_from_file(file_path: Path) -> str | None:
    """Extract text content from a file.

    Args:
        file_path: Path to the file

    Returns:
        Extracted text content or None if extraction failed
    """
    file_extension = file_path.suffix.lower().lstrip(".")

    if file_extension in SUPPORTED_FILE_TYPES_TO_TEXT_CONTENT:
        try:
            return file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Failed to extract text from {file_path}: {e}")
            return None
    else:
        return None


class DataStorageMethods:  # noqa: PLR0904
    """Data storage methods for RestClient.

    This class contains methods for interacting with the data storage API endpoints.
    """

    # needed for mypy `NoReturn`
    def _handle_http_errors(self, e: HTTPStatusError, operation: str) -> NoReturn:  # noqa: PLR6301
        """Handle common HTTP errors for data storage operations."""
        if e.response.status_code == codes.FORBIDDEN:
            raise DataStoragePermissionError(
                f"Error {operation} data storage entry, not authorized"
            ) from e
        if e.response.status_code == codes.UNPROCESSABLE_ENTITY:
            raise DataStorageValidationError(
                f"Invalid request payload: {e.response.text}"
            ) from e
        if e.response.status_code == codes.NOT_FOUND:
            raise DataStorageNotFoundError(
                f"Error {operation} data storage entry: {e.response.status_code} - {e.response.text}"
            ) from e
        if e.response.status_code == codes.CONFLICT:
            raise DataStorageConflictError(
                f"Error {operation} data storage entry: {e.response.status_code} - {e.response.text}"
            ) from e
        raise DataStorageError(
            f"Error {operation} data storage entry: {e.response.status_code} - {e.response.text}"
        ) from e

    def _validate_file_path(self, file_path: str | Path) -> Path:  # noqa: PLR6301
        """Validate file path exists and return Path object."""
        file_path = Path(file_path)
        if not file_path.exists():
            raise DataStorageError(f"File or directory not found: {file_path}")
        return file_path

    def _build_zip_path(  # noqa: PLR6301
        self, name: str, path_override: str | Path | None
    ) -> str | Path:
        """Build GCS path for zip file."""
        zip_filename = name if name.endswith(".zip") else f"{name}.zip"
        if path_override:
            if isinstance(path_override, str):
                return f"{path_override.rstrip('/')}/{zip_filename}"
            return path_override / zip_filename
        return zip_filename

    # TODO: [PLA-1162] methods in here need to be moved to fh tools
    # =====================================
    def _is_zip_file(self, file_path: Path) -> bool:  # noqa: PLR6301
        """Check if a file is a zip file by checking its magic bytes and excluding known packaged document formats."""
        # File extensions that should not be treated as ZIP archives even if they have PK magic bytes
        PACKAGED_ZIP_EXTENSIONS = {
            ".xlsx",
            ".xlsm",
            ".xlsb",  # Excel formats
            ".docx",
            ".docm",  # Word formats
            ".pptx",
            ".pptm",  # PowerPoint formats
            ".odt",
            ".ods",
            ".odp",  # OpenDocument formats
            ".pages",
            ".numbers",
            ".key",  # Apple iWork formats
            ".prism",  # GraphPad Prism 10+ project
            ".phxproj",  # Certara Phoenix WinNonlin project
        }

        if file_path.suffix.lower() in PACKAGED_ZIP_EXTENSIONS:
            return False

        # Then check magic bytes for actual ZIP files
        try:
            with open(file_path, "rb") as f:
                magic = f.read(2)
                return magic == b"PK"
        except Exception:
            return False

    def _extract_zip_file(self, zip_path: Path, extract_to: Path) -> Path:  # noqa: PLR6301
        """Extract a zip file and return the path to the extracted content.

        Args:
            zip_path: Path to the zip file
            extract_to: Directory to extract to

        Returns:
            Path to the extracted content (directory or single file)
        """
        extract_dir = extract_to
        extract_dir.mkdir(exist_ok=True)

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)
        except FileExistsError:
            logger.warning(f"File {zip_path} already exists in {extract_dir}")
            extract_dir = extract_dir / "extracted"
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

        extracted_items = list(extract_dir.iterdir())

        # Delete the zip file
        zip_path.unlink()

        if len(extracted_items) == 1:
            return extracted_items[0]
        return extract_dir

    async def _adownload_attempt(  # noqa: PLR6301
        self,
        signed_url: str,
        temp_file: Path,
        offset: int,
        file_name: str,
    ) -> tuple[Path, int]:
        """Perform a single async HTTP GET attempt, appending to temp_file from offset.

        Returns the (possibly renamed) temp_file path and the new byte offset.
        """
        headers = {"Range": f"bytes={offset}-"} if offset > 0 else {}
        async with (
            AsyncClient(timeout=30) as download_client,
            download_client.stream("GET", signed_url, headers=headers) as response,
        ):
            response.raise_for_status()

            if offset == 0:
                content_disposition = response.headers.get("content-disposition", "")
                filename = Path(file_name).name
                if "filename=" in content_disposition:
                    filename = Path(
                        content_disposition.split("filename=")[-1].strip('"')
                    ).name
                if filename and filename != Path(file_name).name:
                    temp_file = temp_file.parent / filename

            if offset > 0 and response.status_code != codes.PARTIAL_CONTENT:
                logger.warning(
                    "Server ignored Range header (returned %s instead of 206), "
                    "restarting download from byte 0",
                    response.status_code,
                )
                offset = 0

            safe_path = temp_file.resolve()
            safe_path.relative_to(temp_file.parent.resolve())
            async with aiofiles.open(safe_path, "ab" if offset > 0 else "wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    await f.write(chunk)
                    offset += len(chunk)

        return temp_file, offset

    async def _adownload_from_gcs(
        self,
        signed_url: str,
        file_name: str | None = None,
        max_retries: int = 5,
        retry_wait_base: int = 2,
    ) -> Path:
        """Download file from GCS using signed URL and handle unzipping if needed.

        Resumes interrupted downloads using HTTP Range headers rather than restarting
        from byte 0. Retries up to max_retries times with exponential backoff.

        Args:
            signed_url: The signed URL to download from
            file_name: The name of the file to download
            max_retries: Maximum number of resume attempts on connection failure
            retry_wait_base: Base seconds for exponential backoff between retries

        Returns:
            Path to the downloaded file (or unzipped directory if it was a zip)
        """
        file_name = Path(file_name).name if file_name else "downloaded_file"
        temp_dir = Path(tempfile.mkdtemp())

        try:
            temp_file = temp_dir / file_name
            offset = 0

            for attempt in range(max_retries + 1):
                try:
                    temp_file, offset = await self._adownload_attempt(
                        signed_url, temp_file, offset, file_name
                    )
                    break  # download complete
                except HTTPStatusError as e:
                    # HTTP 416: Range already satisfied — file is complete
                    if e.response.status_code == codes.REQUESTED_RANGE_NOT_SATISFIABLE:
                        logger.debug(
                            "Received 416 Range Not Satisfiable — file already complete"
                        )
                        break
                    raise
                except (
                    ReadError,
                    ConnectError,
                    RemoteProtocolError,
                    TimeoutException,
                ) as e:
                    if attempt == max_retries:
                        raise
                    # Recover offset from whichever file exists in temp_dir
                    dir_contents = await asyncio.to_thread(
                        lambda: list(temp_dir.iterdir())
                    )
                    existing = next(iter(dir_contents), None)
                    offset = (
                        await asyncio.to_thread(lambda p: p.stat().st_size, existing)
                        if existing is not None
                        else 0
                    )
                    if existing is not None:
                        temp_file = existing
                    wait = retry_wait_base * (2**attempt)
                    logger.warning(
                        f"Download interrupted at {offset:,} bytes "
                        f"(attempt {attempt + 1}/{max_retries}), "
                        f"resuming in {wait}s: {e}"
                    )
                    await asyncio.sleep(wait)

            logger.debug(
                f"Downloaded file to {temp_file} (size: {temp_file.stat().st_size:,} bytes)"
            )

            if self._is_zip_file(temp_file):
                logger.debug(f"File {temp_file} is a zip file, extracting...")
                return self._extract_zip_file(temp_file, temp_dir)

        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise DataStorageError(f"Failed to download from GCS: {e}") from e
        else:
            return temp_file

    def _download_attempt(  # noqa: PLR6301
        self,
        signed_url: str,
        temp_file: Path,
        offset: int,
        file_name: str,
    ) -> tuple[Path, int]:
        """Perform a single HTTP GET attempt, appending to temp_file from offset.

        Returns the (possibly renamed) temp_file path and the new byte offset.
        Raises requests_lib.exceptions.HTTPError with status 416 when the server
        reports the range is already satisfied (file is complete).
        """
        headers = {"Range": f"bytes={offset}-"} if offset > 0 else {}
        with requests_lib.get(
            signed_url, stream=True, timeout=30, headers=headers
        ) as response:
            response.raise_for_status()

            if offset == 0:
                content_disposition = response.headers.get("content-disposition", "")
                filename = Path(file_name).name
                if "filename=" in content_disposition:
                    filename = Path(
                        content_disposition.split("filename=")[-1].strip('"')
                    ).name
                if filename and filename != Path(file_name).name:
                    temp_file = temp_file.parent / filename

            if offset > 0 and response.status_code != codes.PARTIAL_CONTENT:
                logger.warning(
                    "Server ignored Range header (returned %s instead of 206), "
                    "restarting download from byte 0",
                    response.status_code,
                )
                offset = 0

            mode = "ab" if offset > 0 else "wb"
            safe_path = temp_file.resolve()
            safe_path.relative_to(temp_file.parent.resolve())
            with open(safe_path, mode) as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        offset += len(chunk)

        return temp_file, offset

    def _download_from_gcs(
        self,
        signed_url: str,
        file_name: str | None = None,
        max_retries: int = 5,
        retry_wait_base: int = 2,
    ) -> Path:
        """Download file from GCS using signed URL and handle unzipping if needed (sync version).

        Resumes interrupted downloads using HTTP Range headers rather than restarting
        from byte 0. Retries up to max_retries times with exponential backoff.

        Args:
            signed_url: The signed URL to download from
            file_name: The name of the file to download
            max_retries: Maximum number of resume attempts on connection failure
            retry_wait_base: Base seconds for exponential backoff between retries
        Returns:
            Path to the downloaded file (or unzipped directory if it was a zip)
        """
        file_name = Path(file_name).name if file_name else "downloaded_file"
        temp_dir = Path(tempfile.mkdtemp())

        try:
            temp_file = temp_dir / file_name
            offset = 0

            for attempt in range(max_retries + 1):
                try:
                    temp_file, offset = self._download_attempt(
                        signed_url, temp_file, offset, file_name
                    )
                    break  # download complete
                except requests_lib.exceptions.HTTPError as e:
                    # HTTP 416 means the Range is already satisfied — the file
                    # is complete even though the connection dropped before the
                    # HTTP response finished. Treat this as success.
                    if (
                        e.response is not None
                        and e.response.status_code
                        == codes.REQUESTED_RANGE_NOT_SATISFIABLE
                    ):
                        logger.debug(
                            "Received 416 Range Not Satisfiable — file already complete"
                        )
                        break
                    raise
                except (
                    requests_lib.exceptions.ChunkedEncodingError,
                    requests_lib.exceptions.ConnectionError,
                    requests_lib.exceptions.Timeout,
                ) as e:
                    if attempt == max_retries:
                        raise
                    # Recover offset from whichever file exists in temp_dir
                    # (content-disposition may have renamed temp_file on attempt 0)
                    existing = next(iter(temp_dir.iterdir()), None)
                    offset = existing.stat().st_size if existing is not None else 0
                    if existing is not None:
                        temp_file = existing
                    wait = retry_wait_base * (2**attempt)
                    logger.warning(
                        f"Download interrupted at {offset:,} bytes "
                        f"(attempt {attempt + 1}/{max_retries}), "
                        f"resuming in {wait}s: {e}"
                    )
                    time.sleep(wait)

            logger.debug(
                f"Downloaded file to {temp_file} (size: {temp_file.stat().st_size:,} bytes)"
            )

            if self._is_zip_file(temp_file):
                logger.debug(f"File {temp_file} is a zip file, extracting...")
                return self._extract_zip_file(temp_file, temp_dir)

        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise DataStorageError(f"Failed to download from GCS: {e}") from e
        else:
            return temp_file

    def _prepare_single_file_upload(  # noqa: PLR0917, PLR6301
        self,
        name: str,
        file_path: Path,
        description: str | None,
        file_path_override: str | Path | None,
        dataset_id: UUID | None,
        project_id: UUID | None,
        metadata: dict[str, Any] | None,
        tags: list[str] | None,
        parent_id: UUID | None,
    ) -> tuple[int, DataStorageRequestPayload | None]:
        """Prepare single file for upload, return file size and payload if text content."""
        file_size = file_path.stat().st_size
        logger.debug(
            f"Starting upload of single file: {file_path} (size: {file_size:,} bytes)"
        )

        if _should_send_as_text_content(file_path, file_size):
            logger.debug(
                f"Small text file ({file_size:,} bytes) - sending as text content"
            )
            text_content = _extract_text_from_file(file_path)
            if text_content is not None:
                return file_size, DataStorageRequestPayload(
                    name=name,
                    description=description,
                    content=text_content,
                    file_path=file_path_override or file_path,
                    is_collection=False,
                    project_id=project_id,
                    metadata=metadata,
                    tags=tags,
                    dataset_id=dataset_id,
                    parent_id=parent_id,
                )
            logger.warning(
                "Could not extract text content, falling back to file upload"
            )

        return file_size, None

    def _create_data_storage_entry(
        self, payload: DataStorageRequestPayload
    ) -> DataStorageResponse:
        """Create data storage entry via API (sync version)."""
        response = self.client.post(
            "/v0.1/data-storage/data-entries",
            json=payload.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return DataStorageResponse.model_validate(response.json())

    async def _acreate_data_storage_entry(
        self, payload: DataStorageRequestPayload
    ) -> DataStorageResponse:
        """Create data storage entry via API (async version)."""
        response = await self.async_client.post(
            "/v0.1/data-storage/data-entries",
            json=payload.model_dump(mode="json", exclude_none=True),
        )
        response.raise_for_status()
        return DataStorageResponse.model_validate(response.json())

    def _generate_folder_description_from_files(  # noqa: PLR6301
        self, dir_path: Path, manifest: DirectoryManifest
    ) -> str:
        """Generate folder description by concatenating descriptions of top-level files."""
        descriptions = []

        # Get top-level files only (not recursive)
        for item in dir_path.iterdir():
            if item.is_file():
                # Try to get description from manifest first
                file_desc = manifest.get_entry_description(item.name)

                if file_desc:
                    descriptions.append(f"{item.name}: {file_desc}")
                else:
                    descriptions.append(item.name)

        if descriptions:
            return f"Directory containing: {', '.join(descriptions)}"
        return f"Directory: {dir_path.name}"

    def _load_manifest(  # noqa: PLR6301
        self, dir_path: Path, manifest_filename: str | None
    ) -> DirectoryManifest:
        """Load and parse a manifest file (JSON or YAML) into a structured model."""
        if not manifest_filename:
            return DirectoryManifest()

        manifest_path = dir_path / manifest_filename
        if not manifest_path.exists():
            logger.error(f"Manifest file not found at {manifest_path}")
            raise DataStorageCreationError(
                f"Manifest file {manifest_filename} not found in directory {dir_path}. Ensure the manifest exists and is correctly named, or do not pass it as an argument."
            )

        try:
            with open(manifest_path, encoding="utf-8") as f:
                data = {}
                if manifest_filename.lower().endswith(".json"):
                    data = json.load(f)
                elif manifest_filename.lower().endswith((".yaml", ".yml")):
                    if yaml is None:
                        raise ImportError(
                            "pyyaml is required to parse .yaml manifest files. "
                            "Please install it with `pip install pyyaml`."
                        )
                    data = yaml.safe_load(f)
                else:
                    logger.warning(
                        f"Unsupported manifest file extension: {manifest_filename}"
                    )
                    return DirectoryManifest()

                return DirectoryManifest.from_dict(data or {})

        except Exception as e:
            logger.warning(f"Failed to load manifest {manifest_filename}: {e}")

        return DirectoryManifest()

    def _upload_data_directory(  # noqa: PLR0917
        self,
        name: str,
        dir_path: Path,
        description: str | None,
        dir_path_override: str | Path | None = None,
        ignore_patterns: list[str] | None = None,
        ignore_filename: str = ".gitignore",
        project_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        dataset_id: UUID | None = None,
        parent_id: UUID | None = None,
    ) -> DataStorageResponse:
        """Upload a directory as a single zip file collection.

        Args:
            name: Name for the directory collection
            dir_path: Path to directory to zip and upload
            description: Description for the collection
            dir_path_override: Optional GCS path for the zip file
            ignore_patterns: List of patterns to ignore when zipping
            ignore_filename: Name of ignore file to read from directory
            project_id: ID of the project this data storage entry belongs to
            tags: List of tags to associate with the data storage entry
            metadata: Optional metadata for the data storage entry
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset
            parent_id: Optional parent ID for the data storage entry

        Returns:
            DataStorageResponse for the uploaded zip file
        """
        logger.debug(f"Uploading directory as zip: {dir_path}")

        with tempfile.NamedTemporaryFile(suffix=".zip") as temp_file:
            temp_zip_path = Path(temp_file.name)

            zip_size = _create_directory_zip(
                dir_path, temp_zip_path, ignore_patterns, ignore_filename
            )

            metadata = metadata or {}
            metadata["size"] = zip_size

            zip_gcs_path = self._build_zip_path(name, dir_path_override)
            payload = DataStorageRequestPayload(
                name=name,
                description=description,
                file_path=zip_gcs_path,
                is_collection=True,
                project_id=project_id,
                tags=tags,
                metadata=metadata,
                dataset_id=dataset_id,
                parent_id=parent_id,
            )

            logger.debug(
                f"Creating data storage entry for zip: {payload.model_dump(exclude_none=True)}"
            )
            data_storage_response = self._create_data_storage_entry(payload)

            with tqdm(
                total=zip_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Uploading {dir_path.name} (zipped)",
                miniters=1,
                mininterval=0.1,
            ) as pbar:
                _upload_file_multipart(
                    client=self.client,
                    entry_id=data_storage_response.data_storage.id,
                    file_path=temp_zip_path,
                    file_size=zip_size,
                    progress_bar=pbar,
                )

            status_response = self.client.patch(
                f"/v0.1/data-storage/data-entries/{data_storage_response.data_storage.id}",
                json={"status": "active"},
            )
            status_response.raise_for_status()

            logger.debug(
                f"Successfully uploaded directory {dir_path.name} as zip ({zip_size:,} bytes)"
            )
            return DataStorageResponse.model_validate(status_response.json())

    async def _aupload_data_directory(  # noqa: PLR0917
        self,
        name: str,
        dir_path: Path,
        description: str | None,
        dir_path_override: str | Path | None = None,
        ignore_patterns: list[str] | None = None,
        ignore_filename: str = ".gitignore",
        project_id: UUID | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        dataset_id: UUID | None = None,
        parent_id: UUID | None = None,
    ) -> DataStorageResponse:
        """Asynchronously upload a directory as a single zip file.

        Args:
            name: Name for the directory collection
            dir_path: Path to directory to zip and upload
            description: Description for the collection
            dir_path_override: Optional GCS path for the zip file
            ignore_patterns: List of patterns to ignore when zipping
            ignore_filename: Name of ignore file to read from directory
            project_id: ID of the project this data storage entry belongs to
            tags: List of tags to associate with the data storage entry
            metadata: Optional metadata for the data storage entry
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset
            parent_id: Optional parent ID for the data storage entry

        Returns:
            DataStorageResponse for the uploaded zip file
        """
        logger.debug(f"Async uploading directory as zip: {dir_path}")

        with tempfile.NamedTemporaryFile(suffix=".zip") as temp_file:
            temp_zip_path = Path(temp_file.name)

            zip_size = _create_directory_zip(
                dir_path, temp_zip_path, ignore_patterns, ignore_filename
            )

            metadata = metadata or {}
            metadata["size"] = zip_size

            zip_gcs_path = self._build_zip_path(name, dir_path_override)
            payload = DataStorageRequestPayload(
                name=name,
                description=description,
                file_path=zip_gcs_path,
                is_collection=True,
                project_id=project_id,
                tags=tags,
                metadata=metadata,
                dataset_id=dataset_id,
                parent_id=parent_id,
            )

            data_storage_response = await self._acreate_data_storage_entry(payload)

            with tqdm(
                total=zip_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Uploading {dir_path.name} (zipped)",
                miniters=1,
                mininterval=0.1,
            ) as pbar:
                await _aupload_file_multipart(
                    client=self.async_client,
                    entry_id=data_storage_response.data_storage.id,
                    file_path=temp_zip_path,
                    file_size=zip_size,
                    progress_bar=pbar,
                )

            status_response = await self.async_client.patch(
                f"/v0.1/data-storage/data-entries/{data_storage_response.data_storage.id}",
                json={"status": "active"},
            )
            status_response.raise_for_status()

            logger.debug(
                f"Successfully uploaded directory {dir_path.name} as zip ({zip_size:,} bytes)"
            )
            return DataStorageResponse.model_validate(status_response.json())

    def _upload_data_single_file(  # noqa: PLR0917
        self,
        name: str,
        file_path: Path,
        description: str | None,
        file_path_override: str | Path | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        dataset_id: UUID | None = None,
        parent_id: UUID | None = None,
        embedding: list[float] | None = None,
    ) -> DataStorageResponse:
        """Upload a single file."""
        file_size = file_path.stat().st_size
        logger.debug(
            f"Starting upload of single file: {file_path} (size: {file_size:,} bytes)"
        )

        metadata = metadata or {}
        metadata["size"] = file_size

        if _should_send_as_text_content(file_path, file_size):
            logger.debug(
                f"Small text file ({file_size:,} bytes) - sending as text content"
            )

            text_content = _extract_text_from_file(file_path)
            if text_content is not None:
                payload = DataStorageRequestPayload(
                    name=name,
                    description=description,
                    content=text_content,
                    embedding=embedding,
                    file_path=file_path_override or file_path,
                    is_collection=False,
                    project_id=project_id,
                    metadata=metadata,
                    tags=tags,
                    dataset_id=dataset_id,
                    parent_id=parent_id,
                )

                logger.debug("Sending file as text content")
                return self._create_data_storage_entry(payload)
            logger.warning(
                "Could not extract text content, falling back to file upload"
            )

        logger.debug(
            f"Large/binary file ({file_size:,} bytes) - requesting signed URL for upload"
        )
        payload = DataStorageRequestPayload(
            name=name,
            description=description,
            embedding=embedding,
            file_path=file_path_override or file_path,
            is_collection=False,
            project_id=project_id,
            metadata=metadata,
            tags=tags,
            dataset_id=dataset_id,
            parent_id=parent_id,
        )

        logger.debug(
            f"Requesting signed URL with payload: {payload.model_dump(exclude_none=True)}"
        )

        data_storage_response = self._create_data_storage_entry(payload)

        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"Uploading {file_path.name}",
            miniters=1,
            mininterval=0.1,
        ) as pbar:
            try:
                _upload_file_multipart(
                    client=self.client,
                    entry_id=data_storage_response.data_storage.id,
                    file_path=file_path,
                    file_size=file_size,
                    progress_bar=pbar,
                )
                logger.debug("File upload via multipart completed successfully")
            except Exception as e:
                logger.error(f"Failed to upload file via multipart: {e}")
                raise

        logger.debug("Updating data storage status to active")
        status_response = self.client.patch(
            f"/v0.1/data-storage/data-entries/{data_storage_response.data_storage.id}",
            json={"status": "active"},
        )
        status_response.raise_for_status()
        logger.debug("Data storage status updated successfully")

        return DataStorageResponse.model_validate(status_response.json())

    async def _aupload_data_single_file(  # noqa: PLR0917
        self,
        name: str,
        file_path: Path,
        description: str | None,
        file_path_override: str | Path | None = None,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        parent_id: UUID | None = None,
        embedding: list[float] | None = None,
    ) -> DataStorageResponse:
        """Asynchronously upload a single file."""
        file_size, text_payload = self._prepare_single_file_upload(
            name=name,
            file_path=file_path,
            description=description,
            file_path_override=file_path_override,
            dataset_id=dataset_id,
            project_id=project_id,
            metadata=metadata,
            tags=tags,
            parent_id=parent_id,
        )

        metadata = metadata or {}
        metadata["size"] = file_size

        if text_payload:
            logger.debug("Sending file as text content")
            text_payload.dataset_id = dataset_id
            text_payload.embedding = embedding
            return await self._acreate_data_storage_entry(text_payload)

        logger.debug(
            f"Large/binary file ({file_size:,} bytes) - requesting signed URL for upload"
        )
        payload = DataStorageRequestPayload(
            name=name,
            description=description,
            embedding=embedding,
            file_path=file_path_override or file_path,
            is_collection=False,
            dataset_id=dataset_id,
            project_id=project_id,
            metadata=metadata,
            tags=tags,
            parent_id=parent_id,
        )

        data_storage_response = await self._acreate_data_storage_entry(payload)

        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"Uploading {file_path.name}",
            miniters=1,
            mininterval=0.1,
            leave=False,
        ) as pbar:
            await _aupload_file_multipart(
                client=self.async_client,
                entry_id=data_storage_response.data_storage.id,
                file_path=file_path,
                file_size=file_size,
                progress_bar=pbar,
            )

        status_response = await self.async_client.patch(
            f"/v0.1/data-storage/data-entries/{data_storage_response.data_storage.id}",
            json={"status": "active"},
        )
        status_response.raise_for_status()

        return DataStorageResponse.model_validate(status_response.json())

    def _upload_data_single_file_with_parent(  # noqa: PLR0917
        self,
        name: str,
        file_path: Path,
        description: str | None,
        file_path_override: str | None,
        parent_id: UUID | None,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> DataStorageResponse:
        """Upload a single file with a parent ID (sync version)."""
        file_size, text_payload = self._prepare_single_file_upload(
            name=name,
            file_path=file_path,
            description=description,
            file_path_override=file_path_override,
            dataset_id=dataset_id,
            project_id=project_id,
            metadata=metadata,
            tags=tags,
            parent_id=parent_id,
        )

        if text_payload:
            logger.debug("Sending file as text content with parent_id")
            text_payload.parent_id = parent_id
            text_payload.dataset_id = dataset_id
            text_payload.project_id = project_id
            return self._create_data_storage_entry(text_payload)

        logger.debug(
            f"Large/binary file ({file_size:,} bytes) - requesting signed URL for upload"
        )
        payload = DataStorageRequestPayload(
            name=name,
            description=description,
            file_path=file_path_override or file_path,
            is_collection=False,
            parent_id=parent_id,
            dataset_id=dataset_id,
            project_id=project_id,
            metadata=metadata,
            tags=tags,
        )
        data_storage_response = self._create_data_storage_entry(payload)

        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"Uploading {file_path.name}",
            miniters=1,
            mininterval=0.1,
            leave=False,
        ) as pbar:
            _upload_file_multipart(
                client=self.client,
                entry_id=data_storage_response.data_storage.id,
                file_path=file_path,
                file_size=file_size,
                progress_bar=pbar,
            )

        status_response = self.client.patch(
            f"/v0.1/data-storage/data-entries/{data_storage_response.data_storage.id}",
            json={"status": "active"},
        )
        status_response.raise_for_status()

        return DataStorageResponse.model_validate(status_response.json())

    def _process_file_item(  # noqa: PLR0917
        self,
        item: Path,
        dir_manifest: DirectoryManifest,
        current_parent_id: UUID,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> DataStorageResponse | None:
        """Process a single file item for upload."""
        try:
            manifest_desc = dir_manifest.get_entry_description(item.name)
            file_description = manifest_desc or f"File: {item.name}"

            logger.debug(
                f"Processing file {item.name} with description: '{file_description}'"
            )

            return self._upload_data_single_file_with_parent(
                name=item.name,
                file_path=item,
                description=file_description,
                file_path_override=None,
                parent_id=current_parent_id,
                dataset_id=dataset_id,
                project_id=project_id,
                metadata=metadata,
                tags=tags,
            )
        except Exception as e:
            logger.error(f"Failed to upload file {item}: {e}")
            return None

    def _upload_directory_hierarchically(  # noqa: PLR0917
        self,
        name: str,
        dir_path: Path,
        description: str | None = None,
        manifest_filename: str | None = None,
        parent_id: UUID | None = None,
        ignore_patterns: list[str] | None = None,
        ignore_filename: str = ".gitignore",
        base_dir: Path | None = None,
        dir_manifest: DirectoryManifest | None = None,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> list[DataStorageResponse]:
        """Upload a directory with single dataset and individual file storage entries."""
        responses = []
        if parent_id is None:
            base_dir = dir_path
            all_ignore_patterns = _collect_ignore_patterns(
                base_dir, ignore_patterns, ignore_filename
            )

            payload = DataStorageRequestPayload(
                name=name,
                description=description,
                parent_id=None,
                dataset_id=None,
                is_collection=False,
                project_id=project_id,
                metadata=metadata,
                tags=tags,
            )

            dir_response = self._create_data_storage_entry(payload)
            responses.append(dir_response)
            current_parent_id = dir_response.data_storage.id
            current_dataset_id = dir_response.data_storage.dataset_id

            dir_manifest = self._load_directory_manifest(
                manifest_filename, parent_id, dir_path
            )
        else:
            all_ignore_patterns = ignore_patterns or []
            current_parent_id = parent_id
            current_dataset_id = dataset_id

        for item in dir_path.iterdir():
            if base_dir and _should_ignore_file(item, base_dir, all_ignore_patterns):
                continue

            if item.is_dir():
                subdir_manifest = DirectoryManifest()
                if dir_manifest:
                    entry = dir_manifest.entries.get(item.name)
                    if isinstance(entry, DirectoryManifest):
                        subdir_manifest = entry
                    elif isinstance(entry, ManifestEntry):
                        # Convert single entry to manifest
                        subdir_manifest = DirectoryManifest(entries={item.name: entry})

                subdir_description = subdir_manifest.get_entry_description(item.name)
                if not subdir_description:
                    subdir_description = self._generate_folder_description_from_files(
                        item, subdir_manifest
                    )

                subdir_payload = DataStorageRequestPayload(
                    name=item.name,
                    description=subdir_description,
                    parent_id=current_parent_id,
                    dataset_id=current_dataset_id,
                    is_collection=False,
                    project_id=project_id,
                    metadata=metadata,
                    tags=tags,
                )
                subdir_response = self._create_data_storage_entry(subdir_payload)
                responses.append(subdir_response)

                subdir_responses = self._upload_directory_hierarchically(
                    name=item.name,
                    dir_path=item,
                    description=None,
                    manifest_filename=None,
                    parent_id=subdir_response.data_storage.id,
                    ignore_patterns=all_ignore_patterns,
                    ignore_filename=ignore_filename,
                    base_dir=base_dir,
                    dir_manifest=subdir_manifest,
                    dataset_id=current_dataset_id,
                    project_id=project_id,
                    metadata=metadata,
                    tags=tags,
                )
                responses.extend(subdir_responses)
            elif item.is_file():
                file_response = self._process_file_item(
                    item=item,
                    dir_manifest=dir_manifest or DirectoryManifest(),
                    current_parent_id=current_parent_id,
                    dataset_id=current_dataset_id,
                    project_id=project_id,
                    metadata=metadata,
                    tags=tags,
                )
                if file_response:
                    responses.append(file_response)

        return responses

    def _load_directory_manifest(
        self,
        manifest_filename: str | None,
        parent_id: UUID | None,
        dir_path: Path,
    ) -> DirectoryManifest:
        """Load directory manifest if available."""
        if manifest_filename and not parent_id:
            manifest_data = self._load_manifest(Path.cwd(), manifest_filename)
            dir_name = dir_path.name
            logger.debug(
                f"Loaded manifest entries: {list(manifest_data.entries.keys())}"
            )
            logger.debug(
                f"Looking for manifest entry with directory name: '{dir_name}'"
            )

            entry = manifest_data.entries.get(dir_name)
            if isinstance(entry, DirectoryManifest):
                return entry
            if isinstance(entry, ManifestEntry):
                return DirectoryManifest(entries={dir_name: entry})
            logger.debug(
                f"No manifest entry found for '{dir_name}', available keys: {list(manifest_data.entries.keys())}"
            )
            return DirectoryManifest()
        return DirectoryManifest()

    async def _aupload_data_single_file_with_parent(  # noqa: PLR0917
        self,
        name: str,
        file_path: Path,
        description: str | None,
        file_path_override: str | None,
        parent_id: UUID | None,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> DataStorageResponse:
        """Asynchronously upload a single file with a parent ID."""
        file_size, text_payload = self._prepare_single_file_upload(
            name=name,
            file_path=file_path,
            description=description,
            file_path_override=file_path_override,
            dataset_id=dataset_id,
            project_id=project_id,
            metadata=metadata,
            tags=tags,
            parent_id=parent_id,
        )

        if text_payload:
            logger.debug("Sending file as text content with parent_id")
            text_payload.parent_id = parent_id
            text_payload.dataset_id = dataset_id
            text_payload.project_id = project_id
            return await self._acreate_data_storage_entry(text_payload)

        logger.debug(
            f"Large/binary file ({file_size:,} bytes) - requesting signed URL for upload"
        )
        payload = DataStorageRequestPayload(
            name=name,
            description=description,
            file_path=file_path_override or file_path,
            is_collection=False,
            parent_id=parent_id,
            dataset_id=dataset_id,
            project_id=project_id,
            metadata=metadata,
            tags=tags,
        )
        data_storage_response = await self._acreate_data_storage_entry(payload)

        with tqdm(
            total=file_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=f"Uploading {file_path.name}",
            miniters=1,
            mininterval=0.1,
        ) as pbar:
            await _aupload_file_multipart(
                client=self.async_client,
                entry_id=data_storage_response.data_storage.id,
                file_path=file_path,
                file_size=file_size,
                progress_bar=pbar,
            )

        status_response = await self.async_client.patch(
            f"/v0.1/data-storage/data-entries/{data_storage_response.data_storage.id}",
            json={"status": "active"},
        )
        status_response.raise_for_status()

        return DataStorageResponse.model_validate(status_response.json())

    async def _aprocess_file_item(
        self,
        item: Path,
        dir_manifest: DirectoryManifest,
        current_parent_id: UUID,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
    ) -> DataStorageResponse | None:
        """Asynchronously process a single file item for upload."""
        try:
            manifest_desc = dir_manifest.get_entry_description(item.name)
            file_description = manifest_desc or f"File: {item.name}"

            logger.debug(
                f"Processing file {item.name} with description: '{file_description}'"
            )

            return await self._aupload_data_single_file_with_parent(
                name=item.name,
                file_path=item,
                description=file_description,
                file_path_override=None,
                parent_id=current_parent_id,
                dataset_id=dataset_id,
                project_id=project_id,
            )
        except Exception as e:
            logger.error(f"Failed to upload file {item}: {e}")
            return None

    async def _aupload_directory_hierarchically(  # noqa: PLR0917
        self,
        name: str,
        dir_path: Path,
        description: str | None = None,
        manifest_filename: str | None = None,
        parent_id: UUID | None = None,
        ignore_patterns: list[str] | None = None,
        ignore_filename: str = ".gitignore",
        base_dir: Path | None = None,
        dir_manifest: DirectoryManifest | None = None,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
    ) -> list[DataStorageResponse]:
        """Upload a directory with single dataset and individual file storage entries (async)."""
        responses = []

        if parent_id is None:
            base_dir = dir_path
            all_ignore_patterns = _collect_ignore_patterns(
                base_dir, ignore_patterns, ignore_filename
            )

            payload = DataStorageRequestPayload(
                name=name,
                description=description,
                parent_id=None,
                dataset_id=None,
                is_collection=False,
                project_id=project_id,
                metadata=metadata,
                tags=tags,
            )

            dir_response = await self._acreate_data_storage_entry(payload)
            responses.append(dir_response)
            current_parent_id = dir_response.data_storage.id
            current_dataset_id = dir_response.data_storage.dataset_id

            dir_manifest = self._load_directory_manifest(
                manifest_filename, parent_id, dir_path
            )
        else:
            all_ignore_patterns = ignore_patterns or []
            current_parent_id = parent_id
            current_dataset_id = dataset_id

        for item in dir_path.iterdir():  # noqa: ASYNC240
            if base_dir and _should_ignore_file(item, base_dir, all_ignore_patterns):
                continue

            if item.is_dir():
                subdir_manifest = DirectoryManifest()
                if dir_manifest:
                    entry = dir_manifest.entries.get(item.name)
                    if isinstance(entry, DirectoryManifest):
                        subdir_manifest = entry
                    elif isinstance(entry, ManifestEntry):
                        subdir_manifest = DirectoryManifest(entries={item.name: entry})

                subdir_description = subdir_manifest.get_entry_description(item.name)
                if not subdir_description:
                    subdir_description = self._generate_folder_description_from_files(
                        item, subdir_manifest
                    )

                subdir_payload = DataStorageRequestPayload(
                    name=item.name,
                    description=subdir_description,
                    parent_id=current_parent_id,
                    dataset_id=current_dataset_id,
                    is_collection=False,
                    project_id=project_id,
                    metadata=metadata,
                    tags=tags,
                )
                subdir_response = await self._acreate_data_storage_entry(subdir_payload)
                responses.append(subdir_response)

                subdir_responses = await self._aupload_directory_hierarchically(
                    name=item.name,
                    dir_path=item,
                    description=None,
                    manifest_filename=None,
                    parent_id=subdir_response.data_storage.id,
                    ignore_patterns=all_ignore_patterns,
                    ignore_filename=ignore_filename,
                    base_dir=base_dir,
                    dir_manifest=subdir_manifest,
                    dataset_id=current_dataset_id,
                    project_id=project_id,
                    metadata=metadata,
                    tags=tags,
                )
                responses.extend(subdir_responses)
            elif item.is_file():
                file_response = await self._aprocess_file_item(
                    item,
                    dir_manifest or DirectoryManifest(),
                    current_parent_id,
                    current_dataset_id,
                )
                if file_response:
                    responses.append(file_response)

        return responses

    @property
    def client(self) -> Client:
        raise NotImplementedError("client property must be implemented by subclass")

    @property
    def async_client(self) -> AsyncClient:
        raise NotImplementedError(
            "async_client property must be implemented by subclass"
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def store_text_content(  # noqa: PLR0917
        self,
        name: str,
        content: str,
        description: str | None = None,
        file_path: str | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        dataset_id: UUID | None = None,
        parent_id: UUID | None = None,
        embedding: list[float] | None = None,
    ) -> DataStorageResponse:
        """Store content as a string in the data storage system.

        Args:
            name: Name of the data storage entry
            content: Content to store as a string
            description: Optional description of the data storage entry
            file_path: Optional path for the data storage entry
            project_id: ID of the project this data storage entry belongs to
            metadata: Optional metadata for the data storage entry
            tags: Optional tags for the data storage entry
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset
            parent_id: Optional parent ID for the data storage entry
            embedding: Optional embedding vector for the content

        Returns:
            DataStorageResponse: A Pydantic model containing:
                - data_storage: DataStorageEntry with fields:
                    - id - Unique identifier for the data storage entry
                    - name - Name of the data storage entry
                    - description - Description of the data storage entry
                    - content - Content of the data storage entry
                    - embedding - Embedding vector for the content
                    - is_collection - Whether this entry is a collection
                    - tags - List of tags associated with the entry
                    - parent_id - ID of the parent entry for hierarchical storage
                    - project_id - ID of the project this entry belongs to
                    - dataset_id - ID of the dataset this entry belongs to
                    - file_path - Filepath in the storage system where this entry is located
                    - bigquery_schema - Target BigQuery schema for the entry
                    - user_id - ID of the user who created this entry
                    - created_at - Timestamp when the entry was created
                    - modified_at - Timestamp when the entry was last updated
                - storage_locations with each location containing:
                    - id - Unique identifier for the storage location
                    - data_storage_id - ID of the associated data storage entry
                    - storage_config pydantic model with fields:
                        - storage_type - Type of storage (e.g., 'gcs', 'pg_table')
                        - content_type - Type of content stored
                        - content_schema - Content schema
                        - metadata - Location metadata
                        - location - Location path or identifier
                        - signed_url - Signed URL for uploading/downloading

        Raises:
            DataStorageCreationError: If there's an error creating the data storage entry
        """
        try:
            payload = DataStorageRequestPayload(
                name=name,
                content=content,
                description=description,
                file_path=file_path,
                project_id=project_id,
                metadata=metadata,
                tags=tags,
                dataset_id=dataset_id,
                parent_id=parent_id,
                embedding=embedding,
            )
            return self._create_data_storage_entry(payload)
        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def astore_text_content(  # noqa: PLR0917
        self,
        name: str,
        content: str,
        description: str | None = None,
        file_path: str | None = None,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        parent_id: UUID | None = None,
        embedding: list[float] | None = None,
    ) -> DataStorageResponse:
        """Asynchronously store content as a string in the data storage system.

        Args:
            name: Name of the data storage entry
            content: Content to store as a string
            description: Optional description of the data storage entry
            file_path: Optional path for the data storage entry
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset
            project_id: ID of the project this data storage entry belongs to
            metadata: Optional metadata for the data storage entry
            tags: Optional tags for the data storage entry
            parent_id: Optional parent ID for the data storage entry
            embedding: Optional embedding vector for the content

        Returns:
            DataStorageResponse: A Pydantic model containing:
                - data_storage: DataStorageEntry with fields:
                    - id - Unique identifier for the data storage entry
                    - name - Name of the data storage entry
                    - description - Description of the data storage entry
                    - content - Content of the data storage entry
                    - embedding - Embedding vector for the content
                    - is_collection - Whether this entry is a collection
                    - tags - List of tags associated with the entry
                    - parent_id - ID of the parent entry for hierarchical storage
                    - project_id - ID of the project this entry belongs to
                    - dataset_id - ID of the dataset this entry belongs to
                    - file_path - Filepath in the storage system where this entry is located
                    - bigquery_schema - Target BigQuery schema for the entry
                    - user_id - ID of the user who created this entry
                    - created_at - Timestamp when the entry was created
                    - modified_at - Timestamp when the entry was last updated
                - storage_locations with each location containing:
                    - id - Unique identifier for the storage location
                    - data_storage_id - ID of the associated data storage entry
                    - storage_config pydantic model with fields:
                        - storage_type - Type of storage (e.g., 'gcs', 'pg_table')
                        - content_type - Type of content stored
                        - content_schema - Content schema
                        - metadata - Location metadata
                        - location - Location path or identifier
                        - signed_url - Signed URL for uploading/downloading

        Raises:
            DataStorageCreationError: If there's an error creating the data storage entry
        """
        try:
            payload = DataStorageRequestPayload(
                name=name,
                content=content,
                description=description,
                file_path=file_path,
                dataset_id=dataset_id,
                project_id=project_id,
                metadata=metadata,
                tags=tags,
                parent_id=parent_id,
                embedding=embedding,
            )
            return await self._acreate_data_storage_entry(payload)
        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def astore_link(  # noqa: PLR0917
        self,
        name: str,
        url: HttpUrl,
        description: str,
        instructions: str,
        api_key: str | None = None,
        metadata: dict[str, Any] | None = None,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        tags: list[str] | None = None,
        parent_id: UUID | None = None,
    ) -> DataStorageResponse:
        """Asynchronously store a link/URL in the data storage system.

        Args:
            name: Name of the link entry
            url: The URL/link to store
            description: Searchable details of the link
            instructions: Instructions for how to consume the link or api
            api_key: Any authentication key to access the api. If this is included, you should also include
                details of how the key should be consumed in the instructions.
            metadata: Any additional metadata about the link
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset
            project_id: ID of the project this data storage entry belongs to
            tags: Optional tags for the data storage entry
            parent_id: Optional parent ID for the data storage entry

        Returns:
            DataStorageResponse containing the created link storage entry

        Raises:
            DataStorageCreationError: If there's an error creating the link storage entry
        """
        try:
            link_metadata = metadata.copy() if metadata else {}
            link_metadata["instructions"] = instructions
            if api_key:
                link_metadata["api_key"] = api_key

            existing_location = DataStorageLocationPayload(
                storage_type=DataStorageType.LINK,
                content_type=DataContentType.TEXT,
                location=str(url),
                metadata=link_metadata or None,
            )

            payload = DataStorageRequestPayload(
                name=name,
                content=str(url),
                description=description,
                dataset_id=dataset_id,
                project_id=project_id,
                existing_location=existing_location,
                tags=tags,
                metadata=metadata,
                parent_id=parent_id,
            )
            return await self._acreate_data_storage_entry(payload)
        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    def store_link(  # noqa: PLR0917
        self,
        name: str,
        url: HttpUrl,
        description: str,
        instructions: str,
        api_key: str | None = None,
        metadata: dict[str, Any] | None = None,
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        tags: list[str] | None = None,
        parent_id: UUID | None = None,
    ) -> DataStorageResponse:
        """Store a link/URL in the data storage system.

        Args:
            name: Name of the link entry
            url: The URL/link to store
            description: Searchable details of the link
            instructions: Instructions for how to consume the link or api
            api_key: Any authentication key to access the api. If this is included, you should also include
                details of how the key should be consumed in the instructions.
            metadata: Any additional metadata about the link
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset
            project_id: ID of the project this data storage entry belongs to
            tags: Optional tags for the data storage entry
            parent_id: Optional parent ID for the data storage entry

        Returns:
            DataStorageResponse containing the created link storage entry

        Raises:
            DataStorageCreationError: If there's an error creating the link storage entry
        """
        try:
            link_metadata = metadata.copy() if metadata else {}
            link_metadata["instructions"] = instructions
            if api_key:
                link_metadata["api_key"] = api_key

            existing_location = DataStorageLocationPayload(
                storage_type=DataStorageType.LINK,
                content_type=DataContentType.TEXT,
                location=str(url),
                metadata=link_metadata or None,
            )

            payload = DataStorageRequestPayload(
                name=name,
                content=str(url),
                description=description,
                dataset_id=dataset_id,
                project_id=project_id,
                existing_location=existing_location,
                tags=tags,
                metadata=metadata,
                parent_id=parent_id,
            )
            return self._create_data_storage_entry(payload)
        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def store_file_content(  # noqa: PLR0917
        self,
        name: str,
        file_path: str | Path,
        description: str | None = None,
        file_path_override: str | Path | None = None,
        as_collection: bool = False,
        manifest_filename: str | None = None,
        ignore_patterns: list[str] | None = None,
        ignore_filename: str = ".gitignore",
        project_id: UUID | None = None,
        dataset_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        parent_id: UUID | None = None,
        embedding: list[float] | None = None,
    ) -> DataStorageResponse:
        """Store file or directory content in the data storage system.

        For files: Small text files (< 10MB, supported formats) are sent as text content,
        larger/binary files are uploaded via signed URL.

        For directories: Zipped as a single file with ignore pattern support and uploaded
        as a collection.

        Args:
            name: Name of the data storage entry
            file_path: Path to file or directory to upload
            description: Optional description of the data storage entry
            file_path_override: Optional path for the data storage entry
            as_collection: If true, upload directories as a single zip file collection.
            manifest_filename: Name of manifest file (JSON or YAML) containing:
                - entries - Map of file/directory names to their manifest entries
                - Each ManifestEntry contains:
                    - description - Description of the file or directory
                    - metadata - Additional metadata for the entry
                - Each DirectoryManifest contains nested entries following the same structure
            ignore_patterns: List of patterns to ignore when zipping directories
            ignore_filename: Name of ignore file to read from directory (default: .gitignore)
            project_id: ID of the project this data storage entry belongs to
            dataset_id: ID of the dataset this data storage entry belongs to
            metadata: Optional metadata for the data storage entry
            tags: Optional tags for the data storage entry
            parent_id: Optional parent ID for the data storage entry
            embedding: Optional embedding vector for the content

        Returns:
            DataStorageResponse: A Pydantic model containing:
                - data_storage: DataStorageEntry with fields:
                    - id - Unique identifier for the data storage entry
                    - name - Name of the data storage entry
                    - description - Description of the data storage entry
                    - content - Content of the data storage entry
                    - embedding - Embedding vector for the content
                    - is_collection - Whether this entry is a collection
                    - tags - List of tags associated with the entry
                    - parent_id - ID of the parent entry for hierarchical storage
                    - project_id - ID of the project this entry belongs to
                    - dataset_id - ID of the dataset this entry belongs to
                    - file_path - Filepath in the storage system where this entry is located
                    - bigquery_schema - Target BigQuery schema for the entry
                    - user_id - ID of the user who created this entry
                    - created_at - Timestamp when the entry was created
                    - modified_at - Timestamp when the entry was last updated
                - storage_locations with each location containing:
                    - id - Unique identifier for the storage location
                    - data_storage_id - ID of the associated data storage entry
                    - storage_config pydantic model with fields:
                        - storage_type - Type of storage (e.g., 'gcs', 'pg_table')
                        - content_type - Type of content stored
                        - content_schema - Content schema
                        - metadata - Location metadata
                        - location - Location path or identifier
                        - signed_url - Signed URL for uploading/downloading

        Raises:
            DataStorageCreationError: If there's an error in the process
        """
        file_path = self._validate_file_path(file_path)

        try:
            if file_path.is_dir() and as_collection:
                return self._upload_data_directory(
                    name=name,
                    dir_path=file_path,
                    description=description,
                    dir_path_override=file_path_override,
                    ignore_patterns=ignore_patterns,
                    ignore_filename=ignore_filename,
                    project_id=project_id,
                    dataset_id=dataset_id,
                    parent_id=parent_id,
                    metadata=metadata,
                    tags=tags,
                )
            if file_path.is_dir() and not as_collection:
                responses = self._upload_directory_hierarchically(
                    name=name,
                    dir_path=file_path,
                    description=description,
                    manifest_filename=manifest_filename,
                    ignore_patterns=ignore_patterns,
                    ignore_filename=ignore_filename,
                    project_id=project_id,
                    dataset_id=dataset_id,
                    parent_id=parent_id,
                    metadata=metadata,
                    tags=tags,
                )
                if not responses:
                    raise DataStorageCreationError(
                        "No data storage entries were created"
                    )
                return responses[0]
            return self._upload_data_single_file(
                name,
                file_path,
                description,
                file_path_override,
                project_id,
                metadata=metadata,
                tags=tags,
                dataset_id=dataset_id,
                parent_id=parent_id,
                embedding=embedding,
            )

        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred during file upload: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def astore_file_content(  # noqa: PLR0917
        self,
        name: str,
        file_path: str | Path,
        description: str | None = None,
        file_path_override: str | Path | None = None,
        as_collection: bool = False,
        manifest_filename: str | None = None,
        ignore_patterns: list[str] | None = None,
        ignore_filename: str = ".gitignore",
        dataset_id: UUID | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        parent_id: UUID | None = None,
        embedding: list[float] | None = None,
    ) -> DataStorageResponse:
        """Asynchronously store file or directory content in the data storage system.

        Args:
            name: Name of the data storage entry.
            file_path: Path to the file or directory to upload.
            description: Optional description for the entry.
            file_path_override: Optional GCS path for the entry.
            as_collection: If uploading a directory, `True` zips it into a single collection,
                           `False` uploads it as a hierarchical structure of individual objects.
            manifest_filename: Optional manifest file (JSON or YAML) for hierarchical uploads containing:
                - entries - Map of file/directory names to their manifest entries
                - Each ManifestEntry contains:
                    - description - Description of the file or directory
                    - metadata - Additional metadata for the entry
                - Each DirectoryManifest contains nested entries following the same structure
            ignore_patterns: List of patterns to ignore when zipping.
            ignore_filename: Name of ignore file to read (default: .gitignore).
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset.
            project_id: ID of the project this data storage entry belongs to
            metadata: Optional metadata for the data storage entry
            tags: Optional tags for the data storage entry
            parent_id: Optional parent ID for the data storage entry
            embedding: Optional embedding vector for the content

        Returns:
            DataStorageResponse: A Pydantic model containing:
                - data_storage: DataStorageEntry with fields:
                    - id - Unique identifier for the data storage entry
                    - name - Name of the data storage entry
                    - description - Description of the data storage entry
                    - content - Content of the data storage entry
                    - embedding - Embedding vector for the content
                    - is_collection - Whether this entry is a collection
                    - tags - List of tags associated with the entry
                    - parent_id - ID of the parent entry for hierarchical storage
                    - project_id - ID of the project this entry belongs to
                    - dataset_id - ID of the dataset this entry belongs to
                    - file_path - Filepath in the storage system where this entry is located
                    - bigquery_schema - Target BigQuery schema for the entry
                    - user_id - ID of the user who created this entry
                    - created_at - Timestamp when the entry was created
                    - modified_at - Timestamp when the entry was last updated
                - storage_locations with each location containing:
                    - id - Unique identifier for the storage location
                    - data_storage_id - ID of the associated data storage entry
                    - storage_config pydantic model with fields:
                        - storage_type - Type of storage (e.g., 'gcs', 'pg_table')
                        - content_type - Type of content stored
                        - content_schema - Content schema
                        - metadata - Location metadata
                        - location - Location path or identifier
                        - signed_url - Signed URL for uploading/downloading

            For hierarchical uploads, this is the response for the root directory entry.
        """
        file_path = self._validate_file_path(file_path)

        try:
            if file_path.is_dir():
                if as_collection:
                    return await self._aupload_data_directory(
                        name=name,
                        dir_path=file_path,
                        description=description,
                        dir_path_override=file_path_override,
                        ignore_patterns=ignore_patterns,
                        ignore_filename=ignore_filename,
                        project_id=project_id,
                        metadata=metadata,
                        tags=tags,
                        dataset_id=dataset_id,
                        parent_id=parent_id,
                    )
                responses = await self._aupload_directory_hierarchically(
                    name=name,
                    dir_path=file_path,
                    description=description,
                    manifest_filename=manifest_filename,
                    ignore_patterns=ignore_patterns,
                    ignore_filename=ignore_filename,
                    dataset_id=dataset_id,
                    project_id=project_id,
                    metadata=metadata,
                    tags=tags,
                    parent_id=parent_id,
                )
                if not responses:
                    raise DataStorageCreationError(
                        "No data storage entries were created"
                    )
                return responses[0]
            return await self._aupload_data_single_file(
                name=name,
                file_path=file_path,
                description=description,
                file_path_override=file_path_override,
                dataset_id=dataset_id,
                project_id=project_id,
                metadata=metadata,
                tags=tags,
                parent_id=parent_id,
                embedding=embedding,
            )

        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred during async file upload: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def register_existing_data_source(  # noqa: PLR0917
        self,
        name: str,
        existing_location: DataStorageLocationPayload,
        description: str | None = None,
        as_collection: bool = False,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        parent_id: UUID | None = None,
        dataset_id: UUID | None = None,
    ) -> DataStorageResponse:
        """Register an existing non-GCS data source.

        Args:
            name: Name of the data storage entry
            existing_location: a pydantic model describing the existing data source location to register, containing:
                - storage_type - Type of storage (BIGQUERY, PG_TABLE, RAW_CONTENT, ELASTIC_SEARCH)
                - content_type - Type of content (BQ_DATASET, BQ_TABLE, TEXT, TEXT_W_EMBEDDINGS, DIRECTORY, FILE, INDEX, INDEX_W_EMBEDDINGS)
                - content_schema - Content schema for the data
                - metadata - Additional metadata for the location
                - location - Location path or identifier
            description: Optional description of the data storage entry
            as_collection: If uploading a directory, `True` creates a single storage entry for
                the whole directory and multiple storage locations for each file, `False` assumes
                you are uploading a single file.
            project_id: ID of the project this data storage entry belongs to
            metadata: Optional metadata for the data storage entry
            tags: Optional tags for the data storage entry
            parent_id: Optional parent ID for the data storage entry
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset

        Returns:
            DataStorageResponse: A Pydantic model containing:
                - data_storage: DataStorageEntry with fields:
                    - id - Unique identifier for the data storage entry
                    - name - Name of the data storage entry
                    - description - Description of the data storage entry
                    - content - Content of the data storage entry
                    - embedding - Embedding vector for the content
                    - is_collection - Whether this entry is a collection
                    - tags - List of tags associated with the entry
                    - parent_id - ID of the parent entry for hierarchical storage
                    - project_id - ID of the project this entry belongs to
                    - dataset_id - ID of the dataset this entry belongs to
                    - file_path - Filepath in the storage system where this entry is located
                    - bigquery_schema - Target BigQuery schema for the entry
                    - user_id - ID of the user who created this entry
                    - created_at - Timestamp when the entry was created
                    - modified_at - Timestamp when the entry was last updated
                - storage_locations with each location containing:
                    - id - Unique identifier for the storage location
                    - data_storage_id - ID of the associated data storage entry
                    - storage_config pydantic model with fields:
                        - storage_type - Type of storage (e.g., 'gcs', 'pg_table')
                        - content_type - Type of content stored
                        - content_schema - Content schema
                        - metadata - Location metadata
                        - location - Location path or identifier
                        - signed_url - Signed URL for uploading/downloading

        Raises:
            DataStorageCreationError: If there's an error creating the data storage entry
        """
        try:
            payload = DataStorageRequestPayload(
                name=name,
                description=description,
                existing_location=existing_location,
                file_path=existing_location.location,
                project_id=project_id,
                is_collection=as_collection,
                metadata=metadata,
                tags=tags,
                parent_id=parent_id,
                dataset_id=dataset_id,
            )
            response = self.client.post(
                "/v0.1/data-storage/data-entries",
                json=payload.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aregister_existing_data_source(  # noqa: PLR0917
        self,
        name: str,
        existing_location: DataStorageLocationPayload,
        as_collection: bool = False,
        description: str | None = None,
        project_id: UUID | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        parent_id: UUID | None = None,
        dataset_id: UUID | None = None,
    ) -> DataStorageResponse:
        """Register an existing non-GCS data source.

        Args:
            name: Name of the data storage entry
            existing_location: a pydantic model describing the existing data source location to register, containing:
                - storage_type - Type of storage (BIGQUERY, PG_TABLE, RAW_CONTENT, ELASTIC_SEARCH)
                - content_type - Type of content (BQ_DATASET, BQ_TABLE, TEXT, TEXT_W_EMBEDDINGS, DIRECTORY, FILE, INDEX, INDEX_W_EMBEDDINGS)
                - content_schema - Content schema for the data
                - metadata - Additional metadata for the location
                - location - Location path or identifier
            description: Optional description of the data storage entry
            as_collection: If uploading a directory, `True` creates a single storage entry for
                the whole directory and multiple storage locations for each file, `False` assumes
                you are uploading a single file.
            project_id: ID of the project this data storage entry belongs to
            metadata: Optional metadata for the data storage entry
            tags: Optional tags for the data storage entry
            parent_id: Optional parent ID for the data storage entry
            dataset_id: Optional dataset ID to add entry to, or None to create new dataset

        Returns:
            DataStorageResponse: A Pydantic model containing:
                - data_storage: DataStorageEntry with fields:
                    - id - Unique identifier for the data storage entry
                    - name - Name of the data storage entry
                    - description - Description of the data storage entry
                    - content - Content of the data storage entry
                    - embedding - Embedding vector for the content
                    - is_collection - Whether this entry is a collection
                    - tags - List of tags associated with the entry
                    - parent_id - ID of the parent entry for hierarchical storage
                    - project_id - ID of the project this entry belongs to
                    - dataset_id - ID of the dataset this entry belongs to
                    - file_path - Filepath in the storage system where this entry is located
                    - bigquery_schema - Target BigQuery schema for the entry
                    - user_id - ID of the user who created this entry
                    - created_at - Timestamp when the entry was created
                    - modified_at - Timestamp when the entry was last updated
                - storage_locations with each location containing:
                    - id - Unique identifier for the storage location
                    - data_storage_id - ID of the associated data storage entry
                    - storage_config pydantic model with fields:
                        - storage_type - Type of storage (e.g., 'gcs', 'pg_table')
                        - content_type - Type of content stored
                        - content_schema - Content schema
                        - metadata - Location metadata
                        - location - Location path or identifier
                        - signed_url - Signed URL for uploading/downloading

        Raises:
            DataStorageCreationError: If there's an error creating the data storage entry
        """
        try:
            payload = DataStorageRequestPayload(
                name=name,
                description=description,
                existing_location=existing_location,
                project_id=project_id,
                is_collection=as_collection,
                file_path=existing_location.location,
                metadata=metadata,
                tags=tags,
                parent_id=parent_id,
                dataset_id=dataset_id,
            )
            response = await self.async_client.post(
                "/v0.1/data-storage/data-entries",
                json=payload.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def search_data_storage(  # noqa: PLR0917
        self,
        criteria: list[SearchCriterion] | None = None,
        limit: int = 10,
        offset: int = 0,
        filter_logic: FilterLogic = FilterLogic.OR,
        text_query: str | None = None,
        highlight: bool = False,
        highlight_fields: list[str] | None = None,
        highlight_fragment_size: int = 1000,
        highlight_num_fragments: int = 3,
    ) -> list[dict]:
        """Search data storage objects using structured criteria.

        Args:
            criteria: List of SearchCriterion pydantic models with fields:
                - field - Field name to search on
                - operator - Search operator (EQUALS, CONTAINS, STARTS_WITH, ENDS_WITH, GREATER_THAN, LESS_THAN, BETWEEN, IN)
                - value - Value to search for
            limit: Number of results to return (1-1000)
            offset: Number of results to skip
            filter_logic: Either "AND" (all criteria must match) or "OR" (at least one must match)
            text_query: Optional raw text query for full-text search
            highlight: Enable highlighting of matched terms in results
            highlight_fields: Fields to highlight (default: content, description)
            highlight_fragment_size: Max characters per highlight fragment
            highlight_num_fragments: Max fragments per field

        Returns:
            List of search results with scores and data storage information.
            When highlight=True, each result includes a 'highlights' field with snippets.

        Raises:
            DataStorageCreationError: If there's an error searching data storage entries

        Example:
            from edison_client.models.rest import SearchCriterion, SearchOperator
            criteria = [
                SearchCriterion(field="name", operator=SearchOperator.CONTAINS, value="document"),
                SearchCriterion(field="project_id", operator=SearchOperator.EQUALS, value="my-project-id"),
                SearchCriterion(field="status", operator=SearchOperator.EQUALS, value="active"),
            ]
            results = client.search_data_storage(criteria=criteria, limit=20, highlight=True)
        """
        try:
            payload = DataStorageSearchPayload(
                criteria=criteria or [],
                limit=max(1, min(1000, limit)),  # Clamp between 1-1000
                offset=offset,
                filter_logic=filter_logic,
                text_query=text_query,
                highlight=highlight,
                highlight_fields=highlight_fields,
                highlight_fragment_size=highlight_fragment_size,
                highlight_num_fragments=highlight_num_fragments,
            )

            response = self.client.post(
                "/v0.1/data-storage/search",
                json=payload.model_dump(mode="json"),
            )
            response.raise_for_status()
            return response.json()

        except HTTPStatusError as e:
            if e.response.status_code == codes.SERVICE_UNAVAILABLE:
                raise DataStorageCreationError(
                    "Search functionality is currently unavailable"
                ) from e
            self._handle_http_errors(e, "searching")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred during search: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def asearch_data_storage(  # noqa: PLR0917
        self,
        criteria: list[SearchCriterion] | None = None,
        limit: int = 10,
        offset: int = 0,
        filter_logic: FilterLogic = FilterLogic.OR,
        text_query: str | None = None,
        highlight: bool = False,
        highlight_fields: list[str] | None = None,
        highlight_fragment_size: int = 1000,
        highlight_num_fragments: int = 3,
    ) -> list[dict]:
        """Asynchronously search data storage objects using structured criteria.

        Args:
            criteria: List of SearchCriterion pydantic models with fields:
                - field - Field name to search on
                - operator - Search operator (EQUALS, CONTAINS, STARTS_WITH, ENDS_WITH, GREATER_THAN, LESS_THAN, BETWEEN, IN)
                - value - Value to search for
            limit: Number of results to return (1-1000)
            offset: Number of results to skip
            filter_logic: Either "AND" (all criteria must match) or "OR" (at least one must match)
            text_query: Optional raw text query for full-text search
            highlight: Enable highlighting of matched terms in results
            highlight_fields: Fields to highlight (default: content, description)
            highlight_fragment_size: Max characters per highlight fragment
            highlight_num_fragments: Max fragments per field

        Returns:
            List of search results with scores and data storage information.
            When highlight=True, each result includes a 'highlights' field with snippets.

        Raises:
            DataStorageCreationError: If there's an error searching data storage entries

        Example:
            from edison_client.models.rest import SearchCriterion, SearchOperator
            criteria = [
                SearchCriterion(field="name", operator=SearchOperator.CONTAINS, value="document"),
                SearchCriterion(field="project_id", operator=SearchOperator.EQUALS, value="my-project-id"),
                SearchCriterion(field="status", operator=SearchOperator.EQUALS, value="active"),
            ]
            results = await client.asearch_data_storage(criteria=criteria, limit=20, highlight=True)
        """
        try:
            payload = DataStorageSearchPayload(
                criteria=criteria or [],
                limit=max(1, min(1000, limit)),  # Clamp between 1-1000
                offset=offset,
                filter_logic=filter_logic,
                text_query=text_query,
                highlight=highlight,
                highlight_fields=highlight_fields,
                highlight_fragment_size=highlight_fragment_size,
                highlight_num_fragments=highlight_num_fragments,
            )

            response = await self.async_client.post(
                "/v0.1/data-storage/search",
                json=payload.model_dump(mode="json"),
            )
            response.raise_for_status()
            return response.json()

        except HTTPStatusError as e:
            if e.response.status_code == codes.SERVICE_UNAVAILABLE:
                raise DataStorageCreationError(
                    "Search functionality is currently unavailable"
                ) from e
            self._handle_http_errors(e, "searching")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred during async search: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def similarity_search_data_storage(  # noqa: PLR0917
        self,
        embedding: list[float],
        size: int = 10,
        min_score: float = 0.7,
        dataset_id: UUID | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        project_id: str | None = None,
    ) -> list[dict]:
        """Search data storage objects using vector similarity.

        Args:
            embedding: List of float values representing the embedding vector for similarity search
            size: Number of results to return (1-100)
            min_score: Minimum similarity score (0.0-1.0)
            dataset_id: Optional dataset ID filter
            tags: Optional list of string tags to filter by
            user_id: Optional user ID filter (admin only)
            project_id: Optional project ID filter

        Returns:
            List of search results with similarity scores and data storage information

        Raises:
            DataStorageCreationError: If there's an error performing similarity search
        """
        try:
            # Validate inputs
            if not embedding:
                raise DataStorageCreationError("Embedding vector is required")

            if not all(isinstance(x, int | float) for x in embedding):
                raise DataStorageCreationError("Embedding must be a list of numbers")

            # Build request payload
            payload = {
                "embedding": embedding,
                "size": size,
                "min_score": min_score,
            }

            # Add optional filters
            if dataset_id is not None:
                payload["dataset_id"] = str(dataset_id)
            if tags is not None:
                payload["tags"] = tags
            if user_id is not None:
                payload["user_id"] = user_id
            if project_id is not None:
                payload["project_id"] = project_id

            response = self.client.post(
                "/v0.1/data-storage/similarity-search", json=payload
            )
            response.raise_for_status()
            return response.json()

        except HTTPStatusError as e:
            if e.response.status_code == codes.SERVICE_UNAVAILABLE:
                raise DataStorageCreationError(
                    "Similarity search functionality is currently unavailable"
                ) from e
            self._handle_http_errors(e, "performing similarity search")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred during similarity search: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def asimilarity_search_data_storage(  # noqa: PLR0917
        self,
        embedding: list[float],
        size: int = 10,
        min_score: float = 0.7,
        dataset_id: UUID | None = None,
        tags: list[str] | None = None,
        user_id: str | None = None,
        project_id: str | None = None,
    ) -> list[dict]:
        """Asynchronously search data storage objects using vector similarity.

        Args:
            embedding: List of float values representing the embedding vector for similarity search
            size: Number of results to return (1-100)
            min_score: Minimum similarity score (0.0-1.0)
            dataset_id: Optional dataset ID filter
            tags: Optional list of string tags to filter by
            user_id: Optional user ID filter (admin only)
            project_id: Optional project ID filter

        Returns:
            List of search results with similarity scores and data storage information

        Raises:
            DataStorageCreationError: If there's an error performing similarity search
        """
        try:
            # Validate inputs
            if not embedding:
                raise DataStorageCreationError("Embedding vector is required")

            if not all(isinstance(x, int | float) for x in embedding):
                raise DataStorageCreationError("Embedding must be a list of numbers")

            # Build request payload
            payload = {
                "embedding": embedding,
                "size": size,
                "min_score": min_score,
            }

            # Add optional filters
            if dataset_id is not None:
                payload["dataset_id"] = str(dataset_id)
            if tags is not None:
                payload["tags"] = tags
            if user_id is not None:
                payload["user_id"] = user_id
            if project_id is not None:
                payload["project_id"] = project_id

            response = await self.async_client.post(
                "/v0.1/data-storage/similarity-search", json=payload
            )
            response.raise_for_status()
            return response.json()

        except HTTPStatusError as e:
            if e.response.status_code == codes.SERVICE_UNAVAILABLE:
                raise DataStorageCreationError(
                    "Similarity search functionality is currently unavailable"
                ) from e
            self._handle_http_errors(e, "performing similarity search")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred during async similarity search: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def fetch_data_from_storage(
        self,
        data_storage_id: UUID | str | None = None,
        *,
        version: int | None = None,
        revision_id: UUID | None = None,
    ) -> RawFetchResponse | Path | list[Path] | None:
        """Fetch data from the storage system.

        This is the recommended method for downloading files and retrieving data from
        the data storage service. It supports multiple storage backends (GCS, raw content,
        PostgreSQL tables) and automatically handles different data formats.

        Args:
            data_storage_id: Identifier of the data storage entry to fetch.
                May be either the entry UUID or a bare short alias string.
                If you have a ``data_entry:...`` URI, strip the prefix before
                passing it here. This is typically obtained from task results,
                file listings, or upload operations.
            version: Exact version number; omitted selects latest published content.
            revision_id: Exact revision UUID, mutually exclusive with version.

        Returns:
            The return type depends on the storage backend:

            - **GCS storage**: Returns ``Path`` to the downloaded file. If the file was
              a zip archive, it will be automatically extracted and the path to the
              extracted directory is returned.

            - **Raw content or PostgreSQL table**: Returns ``RawFetchResponse`` object
              containing the content as a string along with metadata (filename, entry_id,
              entry_name).

            - **Multi-location entries**: Returns ``list[Path]`` with one Path object
              for each storage location.

            - **Not found**: Returns ``None`` if the entry is not found or has no content.

        Raises:
            DataStorageRetrievalError: If the data_storage_id is not provided, if there's
                an error accessing the storage backend, or if the storage type is not supported.

        Note:
            Files are downloaded to a temporary directory managed by the system.
            For more control over the destination path, you may need to copy the
            file after download.
        """
        if not data_storage_id:
            raise DataStorageRetrievalError(
                "data_storage_id must be provided at this time"
            )

        url = _entry_read_url(data_storage_id, version, revision_id)
        try:
            response = self.client.get(url, timeout=100)
            response.raise_for_status()
            result = DataStorageResponse.model_validate(response.json())

            if len(result.storage_locations) > 1:
                return [
                    self._download_from_gcs(
                        signed_url=location.storage_config.signed_url or "",
                        file_name=(
                            Path(result.data_storage.file_path).name
                            if result.data_storage.file_path
                            else None
                        ),
                    )
                    for location in result.storage_locations
                ]

            # Most scenarios will only have one location
            storage_location = result.storage_locations[0]
            storage_type = storage_location.storage_config.storage_type

            if storage_type == "gcs":
                if not storage_location.storage_config.signed_url:
                    raise DataStorageRetrievalError(
                        "No signed URL available for GCS download"
                    )

                return self._download_from_gcs(
                    signed_url=storage_location.storage_config.signed_url,
                    file_name=(
                        Path(result.data_storage.file_path).name
                        if result.data_storage.file_path
                        else None
                    ),
                )

            if storage_type in {"raw_content", "pg_table"}:
                content = result.data_storage.content
                if content is None:
                    logger.warning(
                        f"No content found for data storage entry {data_storage_id}"
                    )
                    return None

                if result.data_storage.file_path:
                    return RawFetchResponse(
                        filename=Path(result.data_storage.file_path),
                        content=content,
                        entry_id=result.data_storage.id,
                        entry_name=result.data_storage.name,
                    )

                return RawFetchResponse(
                    content=content,
                    entry_id=result.data_storage.id,
                    entry_name=result.data_storage.name,
                )

            raise DataStorageRetrievalError(f"Unsupported storage type: {storage_type}")

        except HTTPStatusError as e:
            self._handle_http_errors(e, "retrieving")
        except Exception as e:
            raise DataStorageRetrievalError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def afetch_data_from_storage(
        self,
        data_storage_id: UUID | str | None = None,
        *,
        version: int | None = None,
        revision_id: UUID | None = None,
    ) -> RawFetchResponse | Path | list[Path] | None:
        """Fetch data from the storage system.

        Args:
            data_storage_id: Identifier of the data storage entry to fetch.
                May be either the entry UUID or a bare short alias string.
                If you have a ``data_entry:...`` URI, strip the prefix before
                passing it here.
            version: Exact version number; omitted selects latest published content.
            revision_id: Exact revision UUID, mutually exclusive with version.

        Returns:
            For PG_TABLE storage: string content
            For GCS storage: Path to downloaded file (may be unzipped if it was a zip)
            For multi-location entries: list of downloaded files
            None if not found or error occurred
        """
        if not data_storage_id:
            raise DataStorageRetrievalError(
                "data_storage_id must be provided at this time"
            )

        url = _entry_read_url(data_storage_id, version, revision_id)
        try:
            response = await self.async_client.get(url, timeout=100)
            response.raise_for_status()
            result = DataStorageResponse.model_validate(response.json())

            if len(result.storage_locations) > 1:
                return await gather_with_concurrency(
                    DOWNLOAD_CONCURRENCY,
                    [
                        self._adownload_from_gcs(
                            signed_url=location.storage_config.signed_url or "",
                            file_name=(
                                Path(result.data_storage.file_path).name
                                if result.data_storage.file_path
                                else None
                            ),
                        )
                        for location in result.storage_locations
                    ],
                )

            # Most scenarios will only have one location
            storage_location = result.storage_locations[0]
            storage_type = storage_location.storage_config.storage_type

            if storage_type == "gcs":
                if not storage_location.storage_config.signed_url:
                    raise DataStorageRetrievalError(
                        "No signed URL available for GCS download"
                    )

                return await self._adownload_from_gcs(
                    signed_url=storage_location.storage_config.signed_url,
                    file_name=(
                        Path(result.data_storage.file_path).name
                        if result.data_storage.file_path
                        else None
                    ),
                )

            if storage_type in {"raw_content", "pg_table"}:
                content = result.data_storage.content
                if content is None:
                    logger.warning(
                        f"No content found for data storage entry {data_storage_id}"
                    )
                    return None

                if result.data_storage.file_path:
                    return RawFetchResponse(
                        filename=Path(result.data_storage.file_path),
                        content=content,
                        entry_id=result.data_storage.id,
                        entry_name=result.data_storage.name,
                    )

                return RawFetchResponse(
                    content=content,
                    entry_id=result.data_storage.id,
                    entry_name=result.data_storage.name,
                )

            raise DataStorageRetrievalError(f"Unsupported storage type: {storage_type}")

        except HTTPStatusError as e:
            self._handle_http_errors(e, "retrieving")
        except Exception as e:
            raise DataStorageRetrievalError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_data_storage_status(
        self,
        data_storage_id: UUID | str,
    ) -> DataStorageEntryStatusResponse:
        try:
            response = await self.async_client.get(
                f"/v0.1/data-storage/data-entries/{data_storage_id}/status"
            )
            response.raise_for_status()
            return DataStorageEntryStatusResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "checking status of")
        except Exception as e:
            raise DataStorageRetrievalError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def acreate_dataset(
        self,
        name: str,
        description: str | None = None,
        dataset_id: UUID | None = None,
    ) -> CreateDatasetPayload:
        """Asynchronously create a new dataset.

        Args:
            name: Name of the dataset to create
            description: Optional description of the dataset
            dataset_id: Optional UUID to assign to the dataset, or None to auto-generate

        Returns:
            CreateDatasetPayload: A Pydantic model containing:
                - id - ID of the created dataset (None if auto-generated)
                - name - Name of the dataset
                - description - Description of the dataset

        Raises:
            DataStorageCreationError: If there's an error creating the dataset
        """
        try:
            payload = CreateDatasetPayload(
                name=name,
                description=description,
                id=dataset_id,
            )
            response = await self.async_client.post(
                "/v0.1/data-storage/datasets",
                json=payload.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            return CreateDatasetPayload.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def create_dataset(
        self,
        name: str,
        description: str | None = None,
        dataset_id: UUID | None = None,
    ) -> CreateDatasetPayload:
        """Create a new dataset.

        Args:
            name: Name of the dataset to create
            description: Optional description of the dataset
            dataset_id: Optional UUID to assign to the dataset, or None to auto-generate

        Returns:
            CreateDatasetPayload: A Pydantic model containing:
                - id - ID of the created dataset (None if auto-generated)
                - name - Name of the dataset
                - description - Description of the dataset

        Raises:
            DataStorageCreationError: If there's an error creating the dataset
        """
        try:
            payload = CreateDatasetPayload(
                name=name,
                description=description,
                id=dataset_id,
            )
            response = self.client.post(
                "/v0.1/data-storage/datasets",
                json=payload.model_dump(exclude_none=True),
            )
            response.raise_for_status()
            return CreateDatasetPayload.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "creating")
        except Exception as e:
            raise DataStorageCreationError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def adelete_dataset(self, dataset_id: UUID):
        """Delete a dataset.

        Note: This will delete all data storage entries associated with the dataset.

        Args:
            dataset_id: ID of the dataset to delete

        Raises:
            DataStorageError: If there's an error deleting the dataset
        """
        try:
            await self.async_client.delete(f"/v0.1/data-storage/datasets/{dataset_id}")
        except HTTPStatusError as e:
            self._handle_http_errors(e, "deleting")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def delete_dataset(self, dataset_id: UUID):
        """Delete a dataset.

        Note: This will delete all data storage entries associated with the dataset.

        Args:
            dataset_id: ID of the dataset to delete

        Raises:
            DataStorageError: If there's an error deleting the dataset
        """
        try:
            self.client.delete(f"/v0.1/data-storage/datasets/{dataset_id}")
        except HTTPStatusError as e:
            self._handle_http_errors(e, "deleting")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_dataset(self, dataset_id: UUID) -> GetDatasetAndEntriesResponse:
        """Asynchronously retrieve a dataset by ID.

        Args:
            dataset_id: UUID of the dataset to retrieve

        Returns:
            GetDatasetAndEntriesResponse: A dict containing:
                - dataset: DatasetStorage with fields:
                    - id - Unique identifier for the dataset
                    - name - Name of the dataset
                    - user_id - ID of the user who created the dataset
                    - description - Description of the dataset
                    - created_at - Timestamp when the dataset was created
                    - modified_at - Timestamp when the dataset was last modified
                - data_storage_entries - List of data storage entries in the dataset, each containing:
                    - id - Unique identifier for the data storage entry
                    - name - Name of the data storage entry
                    - description - Description of the data storage entry
                    - content - Content of the data storage entry
                    - embedding - Embedding vector for the content
                    - is_collection - Whether this entry is a collection
                    - tags - List of tags associated with the entry
                    - parent_id - ID of the parent entry for hierarchical storage
                    - project_id - ID of the project this entry belongs to
                    - dataset_id - ID of the dataset this entry belongs to
                    - file_path - Filepath in the storage system where this entry is located
                    - bigquery_schema - Target BigQuery schema for the entry
                    - user_id - ID of the user who created this entry
                    - created_at - Timestamp when the entry was created
                    - modified_at - Timestamp when the entry was last updated

        Raises:
            DataStorageError: If there's an error retrieving the dataset
        """
        try:
            response = await self.async_client.get(
                f"/v0.1/data-storage/datasets/{dataset_id}"
            )
            response.raise_for_status()

            return GetDatasetAndEntriesResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "retrieving")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_dataset(self, dataset_id: UUID) -> GetDatasetAndEntriesResponse:
        """Retrieve a dataset by ID.

        Args:
            dataset_id: UUID of the dataset to retrieve

        Returns:
            GetDatasetAndEntriesResponse: A dict containing:
                - dataset: DatasetStorage with fields:
                    - id - Unique identifier for the dataset
                    - name - Name of the dataset
                    - user_id - ID of the user who created the dataset
                    - description - Description of the dataset
                    - created_at - Timestamp when the dataset was created
                    - modified_at - Timestamp when the dataset was last modified
                - data_storage_entries - List of data storage entries in the dataset, each containing:
                    - id - Unique identifier for the data storage entry
                    - name - Name of the data storage entry
                    - description - Description of the data storage entry
                    - content - Content of the data storage entry
                    - embedding - Embedding vector for the content
                    - is_collection - Whether this entry is a collection
                    - tags - List of tags associated with the entry
                    - parent_id - ID of the parent entry for hierarchical storage
                    - project_id - ID of the project this entry belongs to
                    - dataset_id - ID of the dataset this entry belongs to
                    - path - Path in the storage system where this entry is located
                    - bigquery_schema - Target BigQuery schema for the entry
                    - user_id - ID of the user who created this entry
                    - created_at - Timestamp when the entry was created
                    - modified_at - Timestamp when the entry was last updated

        Raises:
            DataStorageError: If there's an error retrieving the dataset
        """
        try:
            response = self.client.get(f"/v0.1/data-storage/datasets/{dataset_id}")
            response.raise_for_status()

            return GetDatasetAndEntriesResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "retrieving")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def get_data_storage_entry(
        self,
        data_storage_id: UUID | str,
        *,
        version: int | None = None,
        revision_id: UUID | None = None,
    ) -> DataStorageResponse:
        """Get a data storage entry with all details including storage locations and metadata.

        Args:
            data_storage_id: ID of the data storage entry to retrieve
            version: Exact version number; omitted selects latest published content.
            revision_id: Exact revision UUID, mutually exclusive with version.

        Returns:
            DataStorageResponse with entry details and storage locations

        Raises:
            DataStorageRetrievalError: If there's an error retrieving the entry
        """
        url = _entry_read_url(data_storage_id, version, revision_id)
        try:
            response = self.client.get(url, timeout=100)
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "retrieving")
        except Exception as e:
            raise DataStorageRetrievalError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aget_data_storage_entry(
        self,
        data_storage_id: UUID | str,
        *,
        version: int | None = None,
        revision_id: UUID | None = None,
    ) -> DataStorageResponse:
        """Get a data storage entry with all details including storage locations and metadata.

        Args:
            data_storage_id: ID of the data storage entry to retrieve
            version: Exact version number; omitted selects latest published content.
            revision_id: Exact revision UUID, mutually exclusive with version.

        Returns:
            DataStorageResponse with entry details and storage locations

        Raises:
            DataStorageRetrievalError: If there's an error retrieving the entry
        """
        url = _entry_read_url(data_storage_id, version, revision_id)
        try:
            response = await self.async_client.get(url, timeout=100)
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "retrieving")
        except Exception as e:
            raise DataStorageRetrievalError(
                f"An unexpected error occurred: {e!r}"
            ) from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aupdate_data_storage_entry(
        self, data_storage_id: UUID | str, payload: DataStorageRevisionUpdate
    ) -> DataStorageResponse:
        """Create/publish revision content through PATCH; reuse payload on retries.

        The base_revision_id must be the revision read before editing. To publish
        an existing draft, pass its revision_id and original base_revision_id
        without content. Set publish=False with new content to save a draft.
        """
        response = await self.async_client.patch(
            f"/v0.1/data-storage/data-entries/{data_storage_id}",
            json=payload.model_dump(mode="json", exclude_none=True),
            timeout=100,
        )
        try:
            response.raise_for_status()
        except HTTPStatusError as exc:
            self._handle_http_errors(exc, "updating")
        return DataStorageResponse.model_validate(response.json())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def alist_data_storage_revisions(
        self,
        data_storage_id: UUID | str,
        *,
        limit: int = 50,
        offset: int = 0,
        include_unpublished: bool = False,
    ) -> DataStorageRevisionListResponse:
        """List published history; including drafts requires edit permission."""
        params = _revision_history_params(limit, offset, include_unpublished)
        response = await self.async_client.get(
            f"/v0.1/data-storage/data-entries/{data_storage_id}/revisions",
            params=params,
            timeout=100,
        )
        try:
            response.raise_for_status()
        except HTTPStatusError as exc:
            self._handle_http_errors(exc, "listing revisions for")
        return DataStorageRevisionListResponse.model_validate(response.json())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def adelete_data_storage_entry(self, data_storage_entry_id: UUID) -> None:
        """Asynchronously delete a data storage entry.

        Args:
            data_storage_entry_id: UUID of the data storage entry to delete

        Raises:
            DataStorageError: If there's an error deleting the data storage entry
        """
        try:
            await self.async_client.delete(
                f"/v0.1/data-storage/data-entries/{data_storage_entry_id}"
            )
        except HTTPStatusError as e:
            self._handle_http_errors(e, "deleting")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def update_data_storage_entry(
        self, data_storage_id: UUID | str, payload: DataStorageRevisionUpdate
    ) -> DataStorageResponse:
        """Create/publish revision content through PATCH; reuse payload on retries.

        The base_revision_id must be the revision read before editing. To publish
        an existing draft, pass its revision_id and original base_revision_id
        without content. Set publish=False with new content to save a draft.
        """
        response = self.client.patch(
            f"/v0.1/data-storage/data-entries/{data_storage_id}",
            json=payload.model_dump(mode="json", exclude_none=True),
            timeout=100,
        )
        try:
            response.raise_for_status()
        except HTTPStatusError as exc:
            self._handle_http_errors(exc, "updating")
        return DataStorageResponse.model_validate(response.json())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def list_data_storage_revisions(
        self,
        data_storage_id: UUID | str,
        *,
        limit: int = 50,
        offset: int = 0,
        include_unpublished: bool = False,
    ) -> DataStorageRevisionListResponse:
        """List published history; including drafts requires edit permission."""
        params = _revision_history_params(limit, offset, include_unpublished)
        response = self.client.get(
            f"/v0.1/data-storage/data-entries/{data_storage_id}/revisions",
            params=params,
            timeout=100,
        )
        try:
            response.raise_for_status()
        except HTTPStatusError as exc:
            self._handle_http_errors(exc, "listing revisions for")
        return DataStorageRevisionListResponse.model_validate(response.json())

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def delete_data_storage_entry(self, data_storage_entry_id: UUID) -> None:
        """Delete a data storage entry.

        Args:
            data_storage_entry_id: UUID of the data storage entry to delete

        Raises:
            DataStorageError: If there's an error deleting the data storage entry
        """
        try:
            self.client.delete(
                f"/v0.1/data-storage/data-entries/{data_storage_entry_id}"
            )
        except HTTPStatusError as e:
            self._handle_http_errors(e, "deleting")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aupdate_entry_permissions(
        self,
        data_storage_id: UUID,
        share_status: ShareStatus,
        permitted_accessors: PermittedAccessors,
    ) -> DataStorageResponse:
        """Update the permissions of a data storage entry.

        Args:
            data_storage_id: UUID of the data storage entry to update
            share_status: Share status to set
            permitted_accessors: Permitted accessors to set

        Returns:
            DataStorageResponse with updated entry details and storage locations

        Raises:
            DataStorageError: If there's an error updating the entry permissions
        """
        try:
            response = await self.async_client.patch(
                f"/v0.1/data-storage/data-entries/{data_storage_id}",
                json={
                    "share_status": share_status,
                    "permitted_accessors": permitted_accessors.model_dump(),
                },
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "updating")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def update_entry_permissions(
        self,
        data_storage_id: UUID,
        share_status: ShareStatus,
        permitted_accessors: PermittedAccessors,
    ) -> DataStorageResponse:
        """Update the permissions of a data storage entry."""
        try:
            response = self.client.patch(
                f"/v0.1/data-storage/data-entries/{data_storage_id}",
                json={
                    "share_status": share_status,
                    "permitted_accessors": permitted_accessors.model_dump(),
                },
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "updating")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def update_entry_tags(
        self,
        data_storage_id: UUID | str,
        tags: list[str],
    ) -> DataStorageResponse:
        """Update the tags of a data storage entry."""
        try:
            response = self.client.patch(
                f"/v0.1/data-storage/data-entries/{data_storage_id}",
                json={"tags": tags},
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "updating")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, max=10),
        retry=retry_if_connection_error,
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    async def aupdate_entry_tags(
        self,
        data_storage_id: UUID | str,
        tags: list[str],
    ) -> DataStorageResponse:
        """Update the tags of a data storage entry (async)."""
        try:
            response = await self.async_client.patch(
                f"/v0.1/data-storage/data-entries/{data_storage_id}",
                json={"tags": tags},
            )
            response.raise_for_status()
            return DataStorageResponse.model_validate(response.json())
        except HTTPStatusError as e:
            self._handle_http_errors(e, "updating")
        except Exception as e:
            raise DataStorageError(f"An unexpected error occurred: {e!r}") from e
