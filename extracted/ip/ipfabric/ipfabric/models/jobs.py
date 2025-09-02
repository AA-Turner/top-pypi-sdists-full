import base64
import logging
from time import sleep
from typing import Any, Literal, Optional, Union

import httpx
from pydantic import BaseModel, Field, field_validator, ConfigDict

from ipfabric.tools.shared import raise_for_status, VALID_REFS, valid_snapshot
from .table import BaseTable

logger = logging.getLogger("ipfabric")

SNAP_JOBS = {
    "load": "snapshotLoad",
    "unload": "snapshotUnload",
    "download": "snapshotDownload",
    "add": "discoveryAdd",
    "refresh": "discoveryRefresh",
    "delete": "deleteDevice",
    "recalculate": "recalculateSites",
    "new": "discoveryNew",
}
ALL_JOBS = {
    "export": "configurationExport",
    "import": "configurationImport",
    "load_graph": "loadGraphCache",
    "history": "saveHistoricalData",
    "report": "report",
    **SNAP_JOBS,
}

SNAP_ACTIONS = Literal["load", "unload", "download", "add", "refresh", "delete", "discoveryNew"]
ALL_ACTIONS = Union[Literal["export", "import"], SNAP_ACTIONS]
SORT = {"order": "desc", "column": "startedAt"}


class TechsupportSnapshotSettings(BaseModel):
    id: Union[str, Literal["$last", "$prev", "$lastLocked"]] = "$last"
    backupDb: bool = True
    removeCli: bool = False

    @field_validator("id")
    @classmethod
    def _valid_snapshot(cls, v: str) -> str:
        return valid_snapshot(v)


class TechsupportPayload(BaseModel):
    databases: bool = False
    systemLogs: bool = True
    discoveryServicesLogs: bool = True
    snapshot: TechsupportSnapshotSettings = Field(default_factory=TechsupportSnapshotSettings)
    usageData: bool = True
    ipfChecker: bool = True


class Job(BaseModel):
    model_config = ConfigDict(extra="allow")
    finishedAt: Optional[int] = None
    snapshot: Optional[str] = None
    name: Optional[str] = None
    id: Optional[str] = None
    username: Optional[str] = None
    isDone: bool = False
    scheduledAt: Optional[int] = None
    downloadFile: Optional[str] = None
    startedAt: Optional[int] = None
    status: Optional[str] = None

    @field_validator("snapshot")
    @classmethod
    def _empty_str_to_none(cls, v: Union[None, str]) -> Union[None, str]:
        return v if v else None


class Jobs(BaseModel):
    client: Any = Field(exclude=True)

    @property
    def all_jobs(self):
        return BaseTable(client=self.client, endpoint="tables/jobs")

    @property
    def columns(self):
        return [
            "id",
            "downloadFile",
            "finishedAt",
            "isDone",
            "name",
            "scheduledAt",
            "snapshot",
            "startedAt",
            "status",
            "username",
        ]

    def get_job_by_id(self, job_id: Union[str, int]) -> Optional[Job]:
        """Get a job by its ID and returns it as a Job object.

        Args:
            job_id: ID of the job to retrieve

        Returns: Job object if found, None if not found

        """
        jobs = self.all_jobs.all(filters={"id": ["eq", str(job_id)]}, columns=self.columns)
        if not jobs:
            return None
        return Job(**jobs[0])

    def find_job(self, started: int, action: ALL_ACTIONS, snapshot_id: str = None) -> Union[Job, None]:
        """Finds a job and returns it.

        Args:
            started: int: Integer time since epoch in milliseconds
            action: str: Type of job to filter on.
            snapshot_id: str: Optional: UUID of a snapshot to filter on

        Returns:
            Job: Job object or None if not found.
        """
        j_filter = dict(name=["eq", ALL_JOBS[action]], startedAt=["gte", started - 1000])
        j_filter.update(dict(snapshot=["eq", snapshot_id]) if snapshot_id else dict())
        sleep(5)  # give the IPF server a chance to start the job
        # find the running snapshotDownload job (i.e. not done)
        jobs = self.all_jobs.fetch(
            filters=j_filter,
            sort={"order": "desc", "column": "startedAt"},
            columns=self.columns,
        )
        logger.debug(f"Job filter: {j_filter}\nList of jobs:{jobs}")
        if not jobs:
            logger.warning(f"Job not found: {j_filter}")
            return None
        return Job(**jobs[0])

    def return_job_when_done(self, job: Union[Job, str], retry: int = 5, timeout: int = 5) -> Union[Job, None]:
        """
        Returns the finished job.

        Args:
            job: str: Job ID string; Job: Job object
            retry: int: How many times to query the table
            timeout: int: How long to wait in-between retries

        Returns:
            job: Job: Object about the job
        """
        job = self.get_job_by_id(job if isinstance(job, str) else job.id)
        if not job:
            logger.critical(f"Job not found: {job}")
            return None

        if job.isDone:
            return job

        for _ in range(retry):
            job = self.get_job_by_id(job.id)
            if job.isDone:
                return job
            sleep(timeout)

        return None

    def check_snapshot_job(
        self, snapshot_id: str, started: int, action: SNAP_ACTIONS, retry: int = 5, timeout: int = 5
    ) -> Union[Job, None]:
        """Checks to see if a snapshot load job is completed.

        Args:
            snapshot_id: str: UUID of a snapshot
            started: int: Integer time since epoch in milliseconds
            action: str: Type of job to filter on
            timeout: int: How long in seconds to wait before retry
            retry: int: How many retries to use when looking for a job, increase for large downloads

        Returns:
            Job: Job object or None if did not complete.
        """
        job = self.find_job(started=started, action=action, snapshot_id=snapshot_id)
        return self.return_job_when_done(job, retry=retry, timeout=timeout)

    def check_snapshot_assurance_jobs(
        self, snapshot_id: str, assurance_settings: dict, started: int, retry: int = 5, timeout: int = 5
    ):
        """Checks to see if a snapshot Assurance Engine calculation jobs are completed.

        Args:
            snapshot_id: UUID of a snapshot
            assurance_settings: Dictionary from Snapshot.get_assurance_engine_settings
            started: Integer time since epoch in milliseconds
            timeout: How long in seconds to wait before retry
            retry: how many retries to use when looking for a job, increase for large downloads

        Returns:
            True if load is completed, False if still loading
        """
        if assurance_settings["disabled_graph_cache"] is False:
            job = self.find_job(started=started, action="load_graph", snapshot_id=snapshot_id)
            if not job or self.return_job_when_done(job, retry=retry, timeout=timeout) is None:
                logger.error("Graph Cache did not finish loading; Snapshot is not fully loaded yet.")
                return False
        if assurance_settings["disabled_historical_data"] is False:
            job = self.find_job(started=started, action="history", snapshot_id=snapshot_id)
            if not job or self.return_job_when_done(job, retry=retry, timeout=timeout) is None:
                logger.error("Historical Data did not finish loading; Snapshot is not fully loaded yet.")
                return False
        if assurance_settings["disabled_intent_verification"] is False:
            job = self.find_job(started=started, action="report", snapshot_id=snapshot_id)
            if not job or self.return_job_when_done(job, retry=retry, timeout=timeout) is None:
                logger.error("Intent Calculations did not finish loading; Snapshot is not fully loaded yet.")
                return False
        return True

    def generate_techsupport(
        self,
        payload: TechsupportPayload = TechsupportPayload(),
        wait_for_ts: bool = True,
        timeout: int = 60,
        retry: int = 5,
    ) -> Job:
        if payload.snapshot.id in VALID_REFS:
            payload.snapshot.id = self.client.snapshots[payload.snapshot.id].snapshot_id
        _ = raise_for_status(self.client.post(url="/os/techsupport", json=payload.model_dump()))

        # Wait for the job to start
        sleep(2)
        tech_support_jobs = self.all_jobs.all(filters={"name": ["eq", "techsupport"]}, sort=SORT)

        if not tech_support_jobs:
            raise LookupError("No techsupport jobs found.")

        job = tech_support_jobs[0]
        if wait_for_ts:
            job = self.return_job_when_done(
                job=job,
                retry=retry,
                timeout=timeout,
            )
        return job

    def download_job_file(self, job_id: str) -> httpx.Response:
        return self.client.get(f"jobs/{str(job_id)}/download")

    def download_techsupport_file(self, job_id: str) -> httpx.Response:
        return self.download_job_file(job_id)

    def upload_techsupport_file(
        self,
        upload_username: str = "techsupport",
        upload_password: Optional[str] = None,
        upload_file_timeout: int = 600,
        upload_server: Literal["eu", "us"] = "eu",
        techsupport_bytes: bytes = None,
        techsupport_job_id: str = None,
        upload_verify: bool = True,
    ):
        if not upload_password:
            raise ValueError("Upload password is required.")
        if not techsupport_job_id and not techsupport_bytes:
            raise ValueError("Techsupport bytes or Job ID is required.")

        if not techsupport_bytes:
            resp = self.download_techsupport_file(techsupport_job_id)
            if resp.status_code != 200:
                raise httpx.HTTPStatusError(
                    f"Failed to download techsupport file: {resp.status_code}", request=resp.request, response=resp
                )
            techsupport_bytes = resp.content
        base64_credentials = base64.b64encode(f"{upload_username}:{upload_password}".encode("utf-8")).decode("utf-8")

        headers = {
            "Content-Type": "application/x-tar",
            "Accept": "application/json",
            "Authorization": f"Basic {base64_credentials}",
            "Content-Length": str(len(techsupport_bytes)),
        }

        upload_response = httpx.post(
            url=f"https://upload.{upload_server}.ipfabric.io/upload",
            headers=headers,
            content=techsupport_bytes,
            timeout=upload_file_timeout,
            verify=upload_verify,
        )

        if upload_response.status_code == 200:
            logger.info("Successfully uploaded techsupport file")
        else:
            logger.error(f"Failed to upload techsupport file. Status code: {upload_response.status_code}")
            logger.error(f"Response content: {upload_response.text}")
            upload_response.raise_for_status()
