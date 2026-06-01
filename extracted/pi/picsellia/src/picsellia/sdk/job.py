import logging
import os
from pathlib import Path
from time import sleep

from beartype import beartype
from orjson import orjson

from picsellia import exceptions, utils
from picsellia.decorators import exception_handler
from picsellia.exceptions import (
    IllegalJobTransitionError,
    NotSupportedJobVersionError,
    WaitingAttemptsTimeout,
    WrongJobVersionError,
)
from picsellia.sdk.connection import Connection
from picsellia.sdk.dao import Dao
from picsellia.types.enums import JobRunStatus, JobStatus, ObjectDataType
from picsellia.types.schemas import JobRunSchema, JobSchema

logger = logging.getLogger("picsellia")


class Job(Dao):
    def __init__(self, connexion: Connection, data: dict, version: int) -> None:
        self._version = version
        Dao.__init__(self, connexion, data)

    @property
    def status(self) -> JobStatus | JobRunStatus:
        """Status of this (Job)"""
        return self._status

    def __str__(self):
        return f"JobV{self._version} {self.id}: {self.status}"

    @exception_handler
    @beartype
    def sync(self) -> dict:
        if self._version == 1:
            r = self.connection.get(f"/api/job/{self.id}").json()
        elif self._version == 2:
            r = self.connection.get(f"/api/v2/job/{self.id}").json()
        else:  # pragma: no cover
            raise NotSupportedJobVersionError(
                f"Unsupported Job version {self._version}"
            )
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def refresh(self, data: dict) -> JobSchema | JobRunSchema:
        if self._version == 1:
            schema = JobSchema(**data)
        elif self._version == 2:
            schema = JobRunSchema(**data)
        else:  # pragma: no cover
            raise NotSupportedJobVersionError(
                f"Unsupported Job version {self._version}"
            )
        self._status = schema.status
        return schema

    @exception_handler
    @beartype
    def wait_for_done(self, blocking_time_increment: float = 1.0, attempts: int = 20):
        """
        Wait for the job to be done.

        Examples:
            ```python
            job.wait_for_done()
            ```

        Arguments:
            blocking_time_increment: Time between each attempts
            attempts: Number of attempts
        """
        if self._version == 1:
            statuses = [
                JobStatus.SUCCESS,
                JobStatus.FAILED,
                JobStatus.TERMINATED,
            ]
        elif self._version == 2:
            statuses = [
                JobRunStatus.SUCCEEDED,
                JobRunStatus.FAILED,
                JobRunStatus.KILLED,
            ]
        else:  # pragma: no cover
            raise NotSupportedJobVersionError(
                f"Unsupported Job version {self._version}"
            )
        return self.wait_for_status(
            statuses,
            blocking_time_increment,
            attempts,
        )

    @exception_handler
    @beartype
    def wait_for_status(
        self,
        statuses: str | JobStatus | JobRunStatus | list[str | JobStatus | JobRunStatus],
        blocking_time_increment: float = 1.0,
        attempts: int = 20,
    ) -> JobStatus | JobRunStatus:
        """
        Wait for the job to be in a specific status.

        Examples:
            ```python
            job = client.get_job_by_id("job_id")
            job.wait_for_status(JobStatus.SUCCESS)
            ```

        Arguments:
            statuses: Status to wait for (JobStatus or JobRunStatus)
            blocking_time_increment: Time between each attempts
            attempts: Number of attempts

        Returns:
            (JobStatus) or (JobRunStatus) of the job

        """
        if (
            isinstance(statuses, JobRunStatus)
            or isinstance(statuses, JobStatus)
            or isinstance(statuses, str)
        ):
            statuses = [statuses]

        if self._version == 1:
            waited_statuses = [JobStatus.validate(status) for status in statuses]
        elif self._version == 2:
            waited_statuses = [JobRunStatus.validate(status) for status in statuses]
        else:  # pragma: no cover
            raise NotSupportedJobVersionError(
                f"Unsupported Job version {self._version}"
            )

        attempt = 0
        while attempt < attempts:
            self.sync()
            if self.status in waited_statuses:
                break

            sleep(blocking_time_increment)
            attempt += 1

        if attempt >= attempts:
            raise WaitingAttemptsTimeout(
                f"Job is still not in the status you've been waiting for, after {attempt} attempts."
                "Please wait a few more moment, or check"
            )

        return self.status

    @exception_handler
    @beartype
    def update_job_run_with_status(self, status: JobRunStatus):
        """
        Update the job run with a new status.

        Examples:
            ```python
            job.update_job_run_with_status(JobRunStatus.SUCCEEDED)
            ```

        Arguments:
            status: New status of the job run
        """
        if self._version != 2:  # pragma: no cover
            raise WrongJobVersionError("You can't use this method with this job")

        if status == JobRunStatus.SUCCEEDED:
            r = self.connection.post(f"/api/v2/job/{self.id}/succeed").json()
        elif status == JobRunStatus.FAILED:
            r = self.connection.post(f"/api/v2/job/{self.id}/fail").json()
        elif status == JobRunStatus.RUNNING:
            r = self.connection.post(f"/api/v2/job/{self.id}/running").json()
        else:
            raise IllegalJobTransitionError(
                f"You can change this job's status to {status}"
            )

        self.refresh(r)

    @exception_handler
    @beartype
    def send_logging(
        self,
        log: str | list,
        part: str,
        final: bool = False,
        special: str | bool | list = False,
    ) -> None:
        """Send a log entry to the job.

        Examples:
            ```python
            job.send_logging("log1", "part1")
            job.send_logging("log2", "part1")
            job.send_logging("log3", "part2")
            job.send_logging("log4", "part2", final=True)
            ```

        Arguments:
            log (str): Log content
            part (str): Logging Part
            final (bool, optional): True if Final line. Defaults to False.
            special (bool, optional): True if special log. Defaults to False.

        """
        if self._version != 2:  # pragma: no cover
            raise WrongJobVersionError("You can't use this method with this job")

        if not hasattr(self, "line_nb"):
            self.line_nb = 0

        to_send = {
            "line_nb": self.line_nb,
            "log": log,
            "final": final,
            "part": part,
            "special": special,
        }
        self.line_nb += 1
        self.connection.post(
            f"/api/v2/job/{self.id}/logging",
            data=orjson.dumps(to_send),
        )

    @exception_handler
    @beartype
    def start_logging_chapter(self, name: str) -> None:
        """Start a logging chapter.

        Examples:
            ```python
            job.start_logging_chapter("chapter1")
            job.send_logging("log1")
            job.send_logging("log2")
            job.end_logging_chapter()
            ```

        Arguments:
            name (str): Chapter name
        """
        utils.print_start_chapter_name(name)
        utils.print_line_return()

    @exception_handler
    @beartype
    def start_logging_buffer(self, length: int = 1) -> None:
        """Start a logging buffer.

        Examples:
            ```python
            job.start_logging_buffer()
            job.send_logging("log1")
            job.send_logging("log2")
            job.end_logging_buffer()
            ```

        Arguments:
            length (int, optional): Buffer length. Defaults to 1.
        """
        utils.print_logging_buffer(length)
        self.buffer_length = length

    @exception_handler
    @beartype
    def end_logging_buffer(self) -> None:
        """End the logging buffer."""
        utils.print_logging_buffer(self.buffer_length)

    @exception_handler
    @beartype
    def store_logging_file(self, path: str | Path) -> str:
        """Store a logging file in the platform.

        Examples:
            ```python
            job.store_logging_file("path/to/file")
            ```
        Arguments:
            path (str or Path): path to the file or folder.

        Raises:
            FileNotFoundException: No file found at the given path

        Returns:
            Object name of logging file as string
        """
        if self._version != 2:  # pragma: no cover
            raise WrongJobVersionError("You can't use this method with this job")

        if not os.path.exists(path):
            raise exceptions.FileNotFoundException(f"{path} not found")

        filename = os.path.basename(path)
        object_name = self.connection.generate_job_object_name(
            filename, ObjectDataType.LOGGING, self.id
        )
        _, is_large, _ = self.connection.upload_file(object_name, path)

        payload = {"logging_object_name": object_name}

        r = self.connection.post(
            f"/api/v2/job/{self.id}/logging/save",
            data=orjson.dumps(payload),
        ).json()
        return r["logging_object_name"]
