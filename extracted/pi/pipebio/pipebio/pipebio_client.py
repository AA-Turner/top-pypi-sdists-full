"""Top-level entry point for the PipeBio Python SDK.

This module exposes :class:`PipebioClient`, the object most callers create first.
It wires together the per-resource service objects (``entities``, ``jobs``,
``sequences``, ``shareables``, ``organization_lists`` and ``workflows``), handles
authentication from environment variables, and provides high-level convenience
helpers for uploading and exporting documents.

Example:
    Create a client and upload a file::

        from pipebio.pipebio_client import PipebioClient

        # Reads PIPE_API_KEY from the environment (or a local .env file).
        client = PipebioClient(url="https://app.pipebio.com")
        job = client.upload_file(
            file_name="sequences.fasta",
            absolute_file_location="/tmp/sequences.fasta",
            parent_id="123",
            project_id="456",
            poll_job=True,
        )
"""

import importlib.metadata
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from urllib.request import urlopen
from zipfile import ZipFile

from dotenv import load_dotenv
from requests_toolbelt import sessions
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.entities import Entities
from pipebio.jobs import Jobs
from pipebio.models.export_format import ExportFormat
from pipebio.models.job_type import JobType
from pipebio.models.upload_detail import UploadDetail
from pipebio.multipart_upload import (
    MULTIPART_THRESHOLD,
    upload_multipart_aws,
)
from pipebio.organization_lists import OrganizationLists
from pipebio.sequences import Sequences
from pipebio.shareables import Shareables
from pipebio.util import Util
from pipebio.workflows import Workflows


class PipebioClient:
    """Authenticated client for the PipeBio API.

    The client authenticates on construction (using ``PIPE_API_KEY`` by default)
    and exposes per-resource service objects as attributes:

    Attributes:
        session: The underlying authenticated :class:`requests` session. Use it
            directly to call endpoints not yet wrapped by the SDK.
        shareables: Operations on shareables (projects/folders ownership).
        entities: Operations on entities (documents, folders).
        jobs: Operations on jobs (create, list, poll, update).
        sequences: Operations on sequence documents (download, upload, import).
        organization_lists: Operations on organization-level lists.
        workflows: Operations on workflows.
        user: The authenticated user object, or ``None`` when manual auth is used.
    """

    session: BaseUrlSession
    shareables: Shareables
    entities: Entities
    jobs: Jobs
    sequences: Sequences
    organization_lists: OrganizationLists
    workflows: Workflows
    user: Any

    _url: str
    _is_aws: bool

    def __init__(self, url: Optional[str] = None) -> None:
        """Create and authenticate a client.

        Args:
            url: Base URL of the PipeBio instance, e.g.
                ``"https://app.pipebio.com"``. Required.

        Raises:
            Exception: If ``url`` is missing, or if no authentication token is
                available and ``PIPEBIO_MANUAL_AUTH`` is not set to ``"true"``.
        """
        __version__ = importlib.metadata.version("pipebio")
        print(f"PipeBio SDK version {__version__}")
        self._is_aws = None
        self._url = url
        # Load .env: try script directory first, then project root (e.g. when run via pytest)
        path = os.path.dirname(sys.argv[0])
        full_path = os.path.join(os.path.abspath(path), ".env")
        if not load_dotenv(full_path):
            # Fallback: project root (parent of pipebio package)
            _project_root = Path(__file__).resolve().parent.parent
            load_dotenv(_project_root / ".env")

        def first_not_none(*values):
            return next((v for v in values if v is not None), None)

        manual_auth = os.environ.get("PIPEBIO_MANUAL_AUTH", "false").lower() == "true"
        benchling_s2s_token = os.environ.get("BENCHLING_S2S_TOKEN") or None
        api_key = os.environ.get("PIPE_API_KEY") or None
        # User tokens are used by plugins running inside PipeBio and only ever set by Pipebio.
        # They are never used by users directly, they should always use PIPE_API_KEY.
        user_token = os.environ.get("USER_TOKEN") or None

        # Strip whitespace (e.g. from .env inline comments) - can cause 401 if present
        def _strip(s):
            return s.strip() if s else None

        benchling_s2s_token = _strip(benchling_s2s_token)
        api_key = _strip(api_key)
        user_token = _strip(user_token)

        token = first_not_none(user_token, benchling_s2s_token, api_key)

        if token is None and not manual_auth:
            print(f"PIPE_API_KEY={api_key}")
            raise Exception("PIPE_API_KEY required.")

        if url is None:
            raise Exception("url required.")

        base_url = f"{url}/api/v2/"

        self.session = sessions.BaseUrlSession(base_url=base_url)

        # Set Bearer token header with API KEY, Benchling S2S token or USER TOKEN.
        if token is not None:
            self.session.headers.update({"Authorization": f"Bearer {token}"})
            # Will also check api_key and fail fast, with friendly error if auth fails.
            self.user = self.get_user()
            first_name = self.user.get("firstName", "")
            last_name = self.user.get("lastName", "")
            print(f"\nUsing api key for {first_name} {last_name}.\n")
        else:
            self.user = None

        self.shareables = Shareables(self.session)
        self._init_user_dependent_services()
        self.internal_tools = _InternalTools(self)

    def _init_user_dependent_services(self):
        job_id = os.environ["JOB_ID"] if "JOB_ID" in os.environ else None
        self.entities = Entities(self.session, self.user)
        self.sequences = Sequences(self.session, self.is_aws, self.user)
        self.jobs = Jobs(self.session, self.user, job_id)
        self.organization_lists = OrganizationLists(self.session, self.user)
        self.workflows = Workflows(
            self.session, self.organization_lists, self.user, self.jobs
        )

    @staticmethod
    def sanitize_baseurl(url: str) -> str:
        """Validate and normalise a PipeBio base URL.

        Args:
            url: The base URL to sanitise.

        Returns:
            The URL with surrounding whitespace and any trailing slash removed.

        Raises:
            ValueError: If the URL does not start with ``https://``.
        """
        url = url.strip()

        if not url.startswith("https://"):
            raise ValueError(
                "Base URL must start with 'https://'. Please provide a full URL like 'https://app.pipebio.com' or 'https://your-company.pipebio.benchling.com'"
            )

        if url != "https://" and url.endswith("/"):
            url = url[:-1]

        return url

    def get_user(self) -> Dict[str, Any]:
        """Fetch the authenticated user from the ``me`` endpoint.

        Returns:
            The user object as returned by the API.

        Raises:
            ValueError: If authentication fails (HTTP 401).

        .. API reference (generated - do not edit) ::

        **GET** ``/me``

        Get me

        Returns information about the currently authenticated user

        .. end API reference ::
        """
        response = self.session.get("me")
        if response.status_code == 401:
            raise ValueError("Failed to authenticate, please check PIPE_API_KEY")
        user = response.json()
        return user

    def upload_file(
        self,
        file_name: str,
        absolute_file_location: str,
        parent_id: str,
        project_id: str,
        organization_id: Optional[str] = None,
        details: Optional[List[UploadDetail]] = None,
        file_name_id: Optional[str] = None,
        poll_job: bool = False,
        on_progress: Optional[Callable[[int, int], None]] = None,
    ) -> Dict[str, Any]:
        """Upload a single local file as a new document.

        Large files (at or above the multipart threshold) are uploaded with a
        multipart upload on AWS instances; otherwise a single signed upload is
        used.

        Args:
            file_name: Friendly name shown in the PipeBio UI.
            absolute_file_location: Absolute path to the file on local disk.
            parent_id: Id of the parent folder/document the upload belongs to.
            project_id: Id of the project (shareable) to upload into.
            organization_id: Organization id. Defaults to the user's default org.
            details: Optional per-file upload details/metadata.
            file_name_id: Optional client-supplied id used to correlate the file.
            poll_job: If ``True``, block until the parsing job finishes and
                return the completed job.
            on_progress: Optional callback receiving ``(bytes_sent, total_bytes)``
                during multipart uploads.

        Returns:
            The upload/parse job object. When ``poll_job`` is ``True`` this is the
            completed job; otherwise it is the in-progress job.
        """
        _organization_id = (
            organization_id
            if organization_id is not None
            else Util.get_organization_id(self.user)
        )

        # Normalize file_name to use forward slashes for cross-platform compatibility.
        normalized_file_name = file_name.replace("\\", "/")
        file_size = os.path.getsize(absolute_file_location)
        use_multipart = file_size >= MULTIPART_THRESHOLD

        if use_multipart and Util.is_aws():
            job = upload_multipart_aws(
                session=self.session,
                absolute_file_location=absolute_file_location,
                file_name=normalized_file_name,
                parent_id=parent_id,
                project_id=project_id,
                organization_id=_organization_id,
                details=details,
                file_name_id=file_name_id,
                on_progress=on_progress,
            )
            job_id = job["id"]
        else:
            print(f"Uploading {normalized_file_name}.")
            response = self.jobs.create_signed_upload(
                file_name=normalized_file_name,
                parent_id=parent_id,
                project_id=project_id,
                details=details,
                file_name_id=file_name_id,
                organization_id=_organization_id,
            )
            url = response["data"]["url"]
            job = response["data"]["job"]
            job_id = job["id"]
            headers = response["data"]["headers"]

            self.jobs.upload_data_to_signed_url(absolute_file_location, url, headers)

        print(f"Upload complete for {normalized_file_name}. Parsing contents.\n")

        if poll_job:
            return self.jobs.poll_job(job_id)
        else:
            return job

    def export(
        self,
        entity_id: str,
        format: ExportFormat,
        destination_folder: Optional[str] = None,
        destination_filename: Optional[str] = None,
        params: Optional[dict] = None,
    ) -> List[str]:
        """Export an entity to a file and download the result.

        Runs an ``ExportJob`` server-side, waits for completion, then downloads
        every output link to ``destination_folder``.

        Args:
            entity_id: Id of the entity to export.
            format: The :class:`~pipebio.models.export_format.ExportFormat` to
                produce (e.g. GenBank, FASTA).
            destination_folder: Local folder to write the downloaded file(s) to.
            destination_filename: Optional output filename; defaults to the
                entity name.
            params: Optional extra export parameters merged into the job params.

        Returns:
            The list of local file paths that were downloaded.
        """
        entity = self.entities.get(entity_id)
        entity_name = entity["name"]
        user = self.user

        params = {} if params is None else params
        params["format"] = format.value if "format" not in params else params["format"]
        params["fileName"] = (
            entity_name if "fileName" not in params else params["fileName"]
        )

        destination_filename = (
            destination_filename if destination_filename else entity_name
        )
        print(f"Exporting {entity_id} to {destination_folder}/{destination_filename}")
        job_id = self.jobs.create(
            owner_id=user["org"]["id"],
            shareable_id=entity["ownerId"],
            job_type=JobType.ExportJob,
            name="Export from python client",
            input_entity_ids=[entity_id],
            params=params,
        )

        # Wait for the file to be converted to Genbank.
        job = self.jobs.poll_job(job_id)

        links = job["outputLinks"]

        outputs = []

        for link in links:
            destination = os.path.join(destination_folder, destination_filename)
            response = urlopen(link["url"])
            with open(destination, "wb") as file:
                file.write(response.read())
            outputs.append(destination)

        return outputs

    @staticmethod
    def _get_file_list(filename_pattern: str, local_folder_path: str):
        """
        Helper function for getting file list from local folder.
        :param filename_pattern:
        :param local_folder_path:
        :return:
        """
        if filename_pattern is not None:
            try:
                re.compile(filename_pattern)
            except re.error:
                raise ValueError("Invalid filename_pattern")

        local_files_to_upload: List[Dict[str, str]] = []
        for dir_path, dir_names, filenames in os.walk(local_folder_path):
            for filename in filenames:
                if filename_pattern is None or re.search(filename_pattern, filename):
                    local_files_to_upload.append(
                        {
                            "filename": filename,
                            "full_path": os.path.join(local_folder_path, filename),
                        }
                    )

        local_file_count = len(local_files_to_upload)
        if local_file_count == 0:
            raise ValueError(
                f"No files to upload, is the folder empty or your filename_pattern "
                f'"{filename_pattern}" incorrect?'
            )

        return local_files_to_upload

    def upload_files(
        self,
        absolute_folder_path: str,
        parent_id: str,
        project_id: str,
        organization_id: Optional[str] = None,
        filename_pattern: Optional[str] = None,
        poll_jobs: bool = False,
    ) -> List[Dict[str, Any]]:
        """Upload multiple files from a folder, one document per file.

        Useful for uploading a number of files to a single folder, e.g. ab1
        files. Uploads are started in parallel and parsing is not awaited unless
        ``poll_jobs`` is set.

        Args:
            absolute_folder_path: Full path to the folder containing the files.
            parent_id: Id of the parent folder/document.
            project_id: Id of the project (shareable) to upload into.
            organization_id: Organization id. Defaults to the user's default org.
            filename_pattern: Optional regex matched against filenames, e.g.
                ``r".*\\.ab1"``.
            poll_jobs: If ``True``, block until all parsing jobs finish.

        Returns:
            The list of upload job objects (completed when ``poll_jobs`` is set).
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = (
            organization_id
            if organization_id is not None
            else Util.get_organization_id(self.user)
        )

        local_files_to_upload = self._get_file_list(
            filename_pattern, absolute_folder_path
        )
        local_file_count = len(local_files_to_upload)
        print(f"Uploading {local_file_count} files")

        # Upload the data, but don't wait for parsing to complete. Just to be efficient.
        index = 1
        upload_ids = []
        upload_jobs = []
        for local_file in local_files_to_upload:
            filename = local_file["filename"]
            print(f"Uploading file {index}/{local_file_count} ({filename})")

            upload_job = self.upload_file(
                # Friendly name that will be shown in PipeBio ui.
                file_name=filename,
                # Path on local disk.
                absolute_file_location=local_file["full_path"],
                # Optional.
                parent_id=parent_id,
                project_id=project_id,
                organization_id=_organization_id,
            )

            upload_ids.append(upload_job["id"])
            upload_jobs.append(upload_job)
            index += 1

        if poll_jobs:
            jobs = self.jobs.poll_jobs(upload_ids, None)
            print("Finished uploading files.")
            return jobs
        else:
            print("Uploading files.")
            return upload_jobs

    def upload_files_as_zip(
        self,
        absolute_folder_path: str,
        parent_id: str,
        project_id: str,
        organization_id: Optional[str] = None,
        filename_pattern: Optional[str] = None,
        poll_jobs: bool = False,
    ) -> Dict[str, Any]:
        """Zip the matching files in a folder and upload them as one document.

        Useful for uploading a number of files as a single document, e.g. ab1
        files.

        Args:
            absolute_folder_path: Full path to the folder containing the files.
            parent_id: Id of the parent folder/document.
            project_id: Id of the project (shareable) to upload into.
            organization_id: Organization id. Defaults to the user's default org.
            filename_pattern: Optional regex matched against filenames, e.g.
                ``r".*\\.ab1"``.
            poll_jobs: If ``True``, block until the parsing job finishes.

        Returns:
            The single upload job object (completed when ``poll_jobs`` is set).
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = (
            organization_id
            if organization_id is not None
            else Util.get_organization_id(self.user)
        )

        local_files_to_upload = self._get_file_list(
            filename_pattern, absolute_folder_path
        )
        local_file_count = len(local_files_to_upload)
        print(f"Uploading {local_file_count} files")

        file = tempfile.NamedTemporaryFile()
        with ZipFile(file.name, "w") as zip_file:
            for local_file in local_files_to_upload:
                zip_file.write(
                    filename=local_file["full_path"], arcname=local_file["filename"]
                )

        upload_job = self.upload_file(
            # Friendly name that will be shown in PipeBio ui.
            file_name=os.path.basename(absolute_folder_path),
            # Path on local disk.
            absolute_file_location=file.name,
            # Optional.
            parent_id=parent_id,
            project_id=project_id,
            organization_id=_organization_id,
        )

        if poll_jobs:
            job = self.jobs.poll_job(upload_job["id"], None)
            print("Finished uploading files.")
            return job
        else:
            print("Uploading files.")
            return upload_job

    def set_correlation_id(self, correlation_id: str) -> None:
        """Set a correlation ID sent as an X-Correlation-Id header on every subsequent API request.

        Use this to link all API calls belonging to a single logical operation
        so they can be correlated in PipeBio server logs.

        Args:
            correlation_id: An opaque identifier for the operation being performed.
        """
        self.session.headers.update({"X-Correlation-Id": correlation_id})

    @property
    def is_aws(self) -> bool:
        """Whether the connected PipeBio instance runs on AWS.

        The result is determined once from the ``/debug/about`` endpoint and
        cached for the lifetime of the client.

        Returns:
            ``True`` if the instance is an AWS deployment, otherwise ``False``.
        """
        if self._is_aws is None:
            url = f"{self._url}/debug/about"
            response = self.session.get(url)
            Util.raise_detailed_error(response)
            # Stack is not set in GCP, so we use that as a flag that we are running in AWS here.
            self._is_aws = "stack" in response.json()
            os.environ["IS_AWS"] = str(self._is_aws)

        return self._is_aws


class _InternalTools:
    """Internal tools for Benchling integration use only. Not for external SDK users."""

    def __init__(self, client: PipebioClient):
        self._client = client

    def set_s2s_token(self, token: str) -> None:
        """
        Set the S2S (Service-to-Service) authentication token programmatically.

        This is for internal Benchling integration use only. Regular SDK users should
        use the PIPE_API_KEY environment variable.

        Requires PIPEBIO_MANUAL_AUTH=true to be set when instantiating the client.

        Args:
            token: The S2S token to use for authentication
        """
        self._client.session.headers.update({"Authorization": f"Bearer {token}"})
        self._client.user = self._client.get_user()
        self._client._init_user_dependent_services()
        first_name = self._client.user.get("firstName", "")
        last_name = self._client.user.get("lastName", "")
        print(f"Authenticated as {first_name} {last_name}.\n")
