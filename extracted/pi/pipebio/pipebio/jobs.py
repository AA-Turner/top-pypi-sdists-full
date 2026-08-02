"""Operations on PipeBio jobs.

A *job* is a unit of server-side (or client-side) work, such as importing,
exporting, aligning or annotating. This module wraps the ``jobs`` API endpoints
- creating, listing, polling, updating and cancelling jobs - and is exposed as
:attr:`PipebioClient.jobs`.
"""

import concurrent.futures
import time
from typing import Any, Dict, List, Optional

import requests
from requests_toolbelt.sessions import BaseUrlSession

from pipebio.models.entity_types import EntityTypes
from pipebio.models.job_filter import JobFilter
from pipebio.models.job_status import JobStatus
from pipebio.models.job_type import JobType
from pipebio.models.output_link import OutputLink
from pipebio.models.upload_detail import UploadDetail
from pipebio.util import Util


class Jobs:
    """Wraps the ``jobs`` API endpoints.

    Obtain an instance via :attr:`PipebioClient.jobs` rather than constructing
    it directly. The service can hold a current ``job_id`` (e.g. when running
    inside a job) which several methods fall back to when no id is supplied.
    """

    _session: BaseUrlSession
    _url: str
    _job_id: str
    _user: Any

    def __init__(self, session: BaseUrlSession, user: Any, job_id: str = None) -> None:
        """Initialise the service.

        Args:
            session: An authenticated base-url session from the client.
            user: The authenticated user object (used to resolve the default
                organization).
            job_id: Optional current job id used as a default by some methods.
        """
        self._url = "jobs"
        self._session = Util.mount_standard_session(session)
        self._job_id = job_id
        self._user = user

    def create(
        self,
        shareable_id: str,
        job_type: JobType,
        name: str,
        input_entity_ids: List[str],
        owner_id: str = None,
        params=None,
        poll_jobs: bool = False,
        client_side: bool = False,
        messages: Optional[List[str]] = None,
        status: Optional[JobStatus] = None,
        allow_deleted_entities: bool = False,
    ) -> str:
        """Create a new job.

        Args:
            shareable_id: Project the input documents belong to.
            job_type: The :class:`~pipebio.models.job_type.JobType` to run.
            name: User-facing job name.
            input_entity_ids: Ids of the input documents/entities.
            owner_id: Organization id owning this job. Defaults to the user's
                default org.
            params: Job-specific parameters.
            poll_jobs: If ``True``, block until the job completes.
            client_side: If ``True``, run locally rather than on PipeBio servers.
            messages: Optional initial status messages (max 10).
            status: Optional initial status (defaults to ``QUEUED``).
            allow_deleted_entities: Allow referencing deleted entities.

        Returns:
            The id of the created job.

        .. API reference (generated - do not edit) ::

        **POST** ``/jobs``

        Create

        Create a new job

        API parameters:
            * ``allowDeletedEntities`` (query) -- If true, allow referencing entities that have been soft-deleted.

        API request body:
            * ``name`` -- Give the job a friendly name that is meaningful to the end user
            * ``clientSide`` (optional) -- Set true if you want to run the job locally yourself and not on PipeBio servers
            * ``shareableId`` -- Copy your project id from the project settings page
            * ``params`` -- Parameters the job can use
            * ``type`` -- What type of job is this
            * ``messages`` -- Update the user with details about what the job is currently doing
            * ``inputEntities`` -- Entity ids of entities that should be fed into this job
            * ``status`` -- Initial status of the job.

        .. end API reference ::
        """
        if params is None:
            params = {}
        else:
            params = dict(params)

        # Inject correlationId into params if set on the session header and not already provided.
        correlation_id = self._session.headers.get("X-Correlation-Id")
        if correlation_id and "correlationId" not in params:
            params["correlationId"] = correlation_id

        # Use owner_id if supplied, otherwise use default org id.
        _organization_id = (
            owner_id if owner_id is not None else Util.get_organization_id(self._user)
        )

        body = {
            "name": name,
            "params": params,
            "shareableId": shareable_id,
            "ownerId": _organization_id,
            "inputEntities": input_entity_ids,
            "type": job_type.value,
            "clientSide": client_side,
        }

        if messages is not None:
            body["messages"] = messages
        if status is not None:
            body["status"] = status.value

        query_params = {}
        if allow_deleted_entities:
            query_params["allowDeletedEntities"] = "true"

        response = self._session.post(
            self._url, json=body, params=query_params if query_params else None
        )

        Util.raise_detailed_error(response)

        data = response.json()
        job_id = data["id"]
        self._job_id = job_id

        if poll_jobs:
            self.poll_jobs([job_id], None)

        return job_id

    def list(
        self,
        organization_id: str = None,
        page_offset: Optional[int] = None,
        page_limit: Optional[int] = None,
        sort: Optional[str] = None,
        include_cols: Optional[List[str]] = None,
        include_total_count: Optional[bool] = None,
        filters: Optional[List[JobFilter]] = None,
    ) -> Dict[str, Any]:
        """List jobs with optional pagination, sorting and filtering.

        When ``filters`` is provided this uses ``POST /jobs/_search``; otherwise
        it uses ``GET /jobs``.

        Args:
            organization_id: Organization to list jobs for. Defaults to the
                user's default org.
            page_offset: Pagination offset (0-based).
            page_limit: Maximum results per page (default 100).
            sort: Comma-separated sort fields; prefix with ``-`` for descending
                (e.g. ``"-created_at,name"``).
            include_cols: Columns to include in the response.
            include_total_count: Whether to include the total count.
            filters: Filter conditions; when provided, the ``_search`` endpoint
                is used.

        Returns:
            The response object with a ``data`` array and optional total count.

        .. API reference (generated - do not edit) ::

        **GET** ``/jobs``

        List

        List jobs for the current user

        API parameters:
            * ``sort`` (query) -- Sort expression in the form "columnName:asc" or "columnName:desc".
            * ``pageOffset`` (query) -- Zero-based index of the first row to return.
            * ``pageLimit`` (query) -- Maximum number of rows to return.
            * ``includeCols`` (query) -- Comma-separated list of column names to include in the response.
            * ``excludeCols`` (query) -- Comma-separated list of column names to exclude from the response.
            * ``includeTotalCount`` (query) -- If true, include the total matching row count in the response.

        .. end API reference ::
        """
        _organization_id = (
            organization_id
            if organization_id is not None
            else Util.get_organization_id(self._user)
        )

        params = {"organizationId": _organization_id}
        if page_offset is not None:
            params["pageOffset"] = page_offset
        if page_limit is not None:
            params["pageLimit"] = page_limit
        if sort is not None:
            params["sort"] = sort
        if include_cols is not None:
            params["includeCols"] = ",".join(include_cols)
        if include_total_count is not None:
            params["includeTotalCount"] = str(include_total_count).lower()

        if filters is not None and len(filters) > 0:
            body = {"filter": [f.to_json() for f in filters]}
            response = self._session.post(
                f"{self._url}/_search", params=params, json=body
            )
        else:
            response = self._session.get(self._url, params=params)

        Util.raise_detailed_error(response)
        return response.json()

    def get(self, job_id: str = None) -> Dict[str, Any]:
        """Fetch a single job by id.

        Args:
            job_id: Job id to fetch. Falls back to the instance job id if omitted.

        Returns:
            The job object.

        .. API reference (generated - do not edit) ::

        **GET** ``/jobs/{jobId}``

        Get

        Get a single job.

        API parameters:
            * ``jobId`` (path) -- Id of the job to fetch.

        .. end API reference ::
        """
        if job_id is None:
            job_id = self._job_id
        url = f"{self._url}/{job_id}"
        response = self._session.get(url)
        Util.raise_detailed_error(response)
        return response.json()

    def cancel(self, job_id: str = None) -> None:
        """Cancel a running or queued job.

        Args:
            job_id: Job id to cancel. Falls back to the instance job id if
                omitted.

        .. API reference (generated - do not edit) ::

        **DELETE** ``/jobs/{jobId}``

        Cancel

        Cancel a job

        API parameters:
            * ``jobId`` (path) -- Id of the job to cancel.

        .. end API reference ::
        """
        if job_id is None:
            job_id = self._job_id
        url = f"{self._url}/{job_id}"
        response = self._session.delete(url)
        Util.raise_detailed_error(response)

    def reschedule(self, job_id: str = None, automated: Optional[bool] = None) -> Dict[str, Any]:
        """Re-run a failed job.

        Args:
            job_id: Job id to reschedule. Falls back to the instance job id if
                omitted.
            automated: Whether this is an automated (vs user-initiated)
                reschedule.

        Returns:
            The updated job object.

        .. API reference (generated - do not edit) ::

        **POST** ``/jobs/{jobId}/reschedule``

        Reschedule

        Re-run a failed job

        API parameters:
            * ``jobId`` (path) -- Id of the job to reschedule.

        API request body:
            * ``automated`` (optional) -- Set true when the reschedule is triggered automatically rather than by a user.

        .. end API reference ::
        """
        if job_id is None:
            job_id = self._job_id
        url = f"{self._url}/{job_id}/reschedule"
        body = {}
        if automated is not None:
            body["automated"] = automated
        response = self._session.post(url, json=body if body else None)
        Util.raise_detailed_error(response)
        return response.json()

    def bulk_update(self, updates: List[dict]) -> None:
        """Update multiple jobs in a single request.

        Args:
            updates: List of update dicts. Each requires ``id`` and ``status``
                and may include ``progress``, ``messages``, ``outputEntities``
                and ``outputLinks``. Between 1 and 100 updates are allowed.

        Raises:
            ValueError: If no updates are given or more than 100 are supplied.

        .. API reference (generated - do not edit) ::

        **PATCH** ``/jobs``

        Update bulk

        Update jobs in bulk

        API request body:
            * ``updates`` -- List of per-job updates to apply (1-100 items).

        .. end API reference ::
        """
        if not updates:
            raise ValueError("At least one update is required")
        if len(updates) > 100:
            raise ValueError("Maximum 100 updates allowed")
        response = self._session.patch(self._url, json={"updates": updates})
        Util.raise_detailed_error(response)

    def start_import_job(self, file_size: Optional[int] = None) -> requests.Response:
        """Trigger an import job run via the job-processing engine.

        Args:
            file_size: Optional size of the uploaded file in bytes.

        Returns:
            The raw API response.

        .. API reference (generated - do not edit) ::

        **PATCH** ``/jobs/{jobId}/import``

        Import

        Parse newly imported sequences once their bytes have been uploaded

        API parameters:
            * ``jobId`` (path) -- Id of the import job to finalise.

        API request body:
            * ``fileSize`` (optional) -- Size of the uploaded file in bytes; can improve upload throughput.

        .. end API reference ::
        """
        body = {}
        if file_size is not None:
            body["fileSize"] = file_size
        response = self._session.patch(
            f"{self._url}/{self._job_id}/import", json=body if body else None
        )
        Util.raise_detailed_error(response)
        return response

    def poll_job(self, job_id: str = None, timeout_seconds: Optional[int] = None) -> Dict[str, Any]:
        """Poll a job until it completes or fails.

        Args:
            job_id: Job id to poll. Falls back to the instance job id if omitted.
            timeout_seconds: Maximum time to wait. Defaults to 600 seconds.

        Returns:
            The final job object.

        Raises:
            Exception: If the timeout elapses before the job finishes.
        """
        if job_id is None:
            job_id = self._job_id

        done = False
        job_status = None
        job = None

        print(f"Polling job: {job_id}")

        # 10 mins default timeout
        timeout = time.time() + (
            timeout_seconds if timeout_seconds is not None else 60 * 10
        )

        while not done:
            time.sleep(5)
            job = self.get(job_id)
            job_status = job["status"]
            print(f"     Job {job_id} status: {job_status}")
            done = job_status in [JobStatus.COMPLETE.value, JobStatus.FAILED.value]

            if time.time() > timeout:
                raise Exception(f"Timeout waiting for job {job_id} to finish.")

        print(f"Job {job_id} is: {job_status}")
        return job

    def poll_jobs(self, job_ids: List[str], timeout_seconds: Optional[int] = None) -> List[Dict[str, Any]]:
        """Poll multiple jobs in parallel until they complete or fail.

        Args:
            job_ids: Ids of the jobs to poll.
            timeout_seconds: Maximum time to wait per job. Defaults to 600
                seconds.

        Returns:
            The list of final job objects.
        """
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        results = [
            executor.submit(self.poll_job, job_id, timeout_seconds)
            for job_id in iter(job_ids)
        ]
        executor.shutdown(wait=True)
        return list(map(lambda result: result.result(), results))

    def create_signed_upload(
        self,
        file_name: str,
        parent_id: str,
        project_id: str,
        details: List[UploadDetail],
        file_name_id: str,
        organization_id: str = None,
    ) -> dict:
        """Create a signed upload slot for a new sequence document.

        Args:
            file_name: Friendly name shown in the PipeBio UI.
            parent_id: Id of the target parent folder.
            project_id: Id of the project (shareable) to upload into.
            details: Per-file upload details/metadata.
            file_name_id: Optional client-supplied id to correlate the file.
            organization_id: Organization id. Defaults to the user's default org.

        Returns:
            The signed-upload response, including the URL, headers and job.

        .. API reference (generated - do not edit) ::

        **POST** ``/signed-url``

        Create (start upload)

        Start an upload with a signed url.

        API request body:
            * ``name`` -- Name to give the entity created from the upload.
            * ``type`` -- Type of entity to create from the upload.
            * ``contentType`` -- MIME type of the uploaded content.
            * ``details`` -- Per-row attributes to attach to the created entity.
            * ``source`` -- Identifier of the external system the data came from.
            * ``sourceId`` -- Id of the source record in the originating system.
            * ``shareableId`` -- Id of the project the new entity belongs to.
            * ``targetFolderId`` -- Id of the folder to place the new entity in.
            * ``options`` -- Additional options controlling the create-from-upload job.
            * ``columns`` -- Column definitions (name and kind) for the uploaded data.
            * ``location`` -- Can help with upload speeds

        .. end API reference ::
        """
        # Use organization_id if supplied, otherwise use default org id.
        _organization_id = (
            organization_id
            if organization_id is not None
            else Util.get_organization_id(self._user)
        )

        data = dict(
            name=file_name,
            type=EntityTypes.SEQUENCE_DOCUMENT.value,
            targetFolderId=parent_id,
            shareableId=project_id,
            ownerId=_organization_id,
            details=[],
        )

        if details is not None:
            # Details should be an
            for detail in details:
                data["details"].append(detail.to_json())

        if file_name_id is not None:
            data["details"].append(
                {"name": "fileNameId", "type": "fileNameId", "value": file_name_id}
            )

        response = self._session.post("signed-url", json=data)

        Util.raise_detailed_error(response)

        return response.json()

    def upload_data_to_signed_url(
        self, absolute_file_location: str, signed_url: str, signed_headers: Any
    ) -> None:
        """Upload a file to a signed URL (small-file path).

        For large files, prefer
        :func:`pipebio.multipart_upload.upload_multipart_aws`.

        Args:
            absolute_file_location: Path to the local file to upload.
            signed_url: The signed URL to upload to.
            signed_headers: Headers that must be sent unmodified with the upload.

        .. API reference (generated - do not edit) ::

        **POST** ``/sequences/signed-upload/{entityId}``

        Create a signed upload

        Start a signed upload; Upload sequences in bulk.

        API parameters:
            * ``entityId`` (path) -- Id of the entity the signed upload writes sequences into.
            * ``allowDeleted`` (query) -- If true, also operate on the entity when it has been soft-deleted.

        API request body:
            * ``location`` -- Can help with upload speeds

        .. end API reference ::
        """
        if Util.is_aws():
            with open(absolute_file_location, "rb") as file:
                upload_response = requests.put(
                    signed_url,
                    data=file,
                    headers=signed_headers,
                    timeout=60 * 60,
                )
            Util.raise_detailed_error(upload_response)
        else:
            # 1. Start the signed-upload.
            # NOTE: Url and headers cannot be modified or the upload will fail.
            create_upload_response = self._session.post(
                signed_url, headers=signed_headers
            )
            Util.raise_detailed_error(create_upload_response)
            response_headers = create_upload_response.headers
            location = response_headers["Location"]

            # 2. Upload bytes.
            with open(absolute_file_location, "rb") as file:
                upload_response = self._session.put(location, data=file)
                Util.raise_detailed_error(upload_response)

    def update(
        self,
        status: JobStatus,
        progress=None,
        messages: List[str] = None,
        output_entity_ids: List[str] = None,
        output_links: List[OutputLink] = None,
        allow_deleted_entities: bool = False,
    ) -> requests.Response:
        """Update the current job's status.

        Args:
            status: The new :class:`~pipebio.models.job_status.JobStatus`.
            progress: Progress value, clamped to the range 0-100.
            messages: Status messages to attach.
            output_entity_ids: Ids of output entities produced by the job.
            output_links: Download links produced by the job.
            allow_deleted_entities: Allow referencing deleted entities.

        Returns:
            The raw API response.

        .. API reference (generated - do not edit) ::

        **PATCH** ``/jobs/{jobId}``

        Update

        Update a single job

        API parameters:
            * ``jobId`` (path) -- Id of the job to update.
            * ``allowDeletedEntities`` (query) -- If true, allow referencing entities that have been soft-deleted.

        API request body:
            * ``status`` -- New status to set on the job.
            * ``progress`` (optional) -- Job completion percentage between 0 and 100.
            * ``messages`` (optional) -- Status messages describing what the job is currently doing.
            * ``outputEntities`` (optional) -- Entity ids produced by the job.
            * ``outputLinks`` (optional) -- Downloadable output files produced by the job.

        .. end API reference ::
        """
        job_id = self._job_id
        body = {
            "status": status.value,
        }

        if progress is not None:
            # Clamp the progress between 0 and 100.
            body["progress"] = max(0, min(100, progress))

        if messages is not None:
            body["messages"] = messages

        if output_entity_ids is not None:
            body["outputEntities"] = output_entity_ids

        if output_links is not None:
            body["outputLinks"] = list(map(lambda link: link.to_json(), output_links))

        query_params = {}
        if allow_deleted_entities:
            query_params["allowDeletedEntities"] = "true"

        response = self._session.patch(
            f"{self._url}/{job_id}",
            json=body,
            params=query_params if query_params else None,
        )
        Util.raise_detailed_error(response)
        return response

    def set_complete(
        self,
        messages: List[str] = None,
        output_entity_ids: List[str] = None,
        output_links: List[OutputLink] = None,
    ) -> requests.Response:
        """Mark the current job complete (status COMPLETE, progress 100).

        Args:
            messages: Optional final status messages.
            output_entity_ids: Ids of output entities produced by the job.
            output_links: Download links produced by the job.

        Returns:
            The raw API response.
        """
        return self.update(
            JobStatus.COMPLETE,
            100,
            messages=messages,
            output_entity_ids=output_entity_ids,
            output_links=output_links,
        )
