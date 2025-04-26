from typing import Any, Dict, Optional, Union

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.job._private.job_sdk import PrivateJobSDK
from anyscale.job.commands import (
    _ARCHIVE_ARG_DOCSTRINGS,
    _ARCHIVE_EXAMPLE,
    _GET_LOGS_ARG_DOCSTRINGS,
    _GET_LOGS_EXAMPLE,
    _resolve_id_from_args,
    _STATUS_ARG_DOCSTRINGS,
    _STATUS_EXAMPLE,
    _SUBMIT_ARG_DOCSTRINGS,
    _SUBMIT_EXAMPLE,
    _TERMINATE_ARG_DOCSTRINGS,
    _TERMINATE_EXAMPLE,
    _WAIT_ARG_DOCSTRINGS,
    _WAIT_EXAMPLE,
    archive,
    get_logs,
    status,
    submit,
    terminate,
    wait,
)
from anyscale.job.models import JobConfig, JobLogMode, JobState, JobStatus


class JobSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateJobSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_SUBMIT_EXAMPLE, arg_docstrings=_SUBMIT_ARG_DOCSTRINGS,
    )
    def submit(self, config: JobConfig,) -> str:  # noqa: F811
        """Submit a job.

        Returns the id of the submitted job.
        """
        return self._private_sdk.submit(config=config)

    @sdk_docs(
        doc_py_example=_STATUS_EXAMPLE, arg_docstrings=_STATUS_ARG_DOCSTRINGS,
    )
    def status(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        **_kwargs: Dict[str, Any],
    ) -> JobStatus:
        """Get the status of a job."""
        id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
        return self._private_sdk.status(
            name=name, job_id=id, cloud=cloud, project=project
        )

    @sdk_docs(
        doc_py_example=_TERMINATE_EXAMPLE, arg_docstrings=_TERMINATE_ARG_DOCSTRINGS,
    )
    def terminate(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        **_kwargs: Dict[str, Any],
    ) -> str:
        """Terminate a job.

        This command is asynchronous, so it always returns immediately.

        Returns the ID of the terminated job.
        """
        id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
        return self._private_sdk.terminate(
            name=name, job_id=id, cloud=cloud, project=project
        )

    @sdk_docs(
        doc_py_example=_ARCHIVE_EXAMPLE, arg_docstrings=_ARCHIVE_ARG_DOCSTRINGS,
    )
    def archive(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        **_kwargs: Dict[str, Any],
    ) -> str:
        """Archive a job.

        This command is asynchronous, so it always returns immediately.

        Returns the ID of the archived job.
        """
        id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
        return self._private_sdk.archive(
            name=name, job_id=id, cloud=cloud, project=project
        )

    @sdk_docs(
        doc_py_example=_WAIT_EXAMPLE, arg_docstrings=_WAIT_ARG_DOCSTRINGS,
    )
    def wait(  # noqa: F811
        self,
        *,
        name: Optional[str] = None,
        id: Optional[str] = None,  # noqa: A002
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        state: Union[JobState, str] = JobState.SUCCEEDED,
        timeout_s: float = 1800,
        **_kwargs: Dict[str, Any],
    ) -> str:
        """"Wait for a job to enter a specific state."""
        id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
        return self._private_sdk.wait(
            name=name,
            job_id=id,
            cloud=cloud,
            project=project,
            state=state,
            timeout_s=timeout_s,
        )

    @sdk_docs(
        doc_py_example=_GET_LOGS_EXAMPLE, arg_docstrings=_GET_LOGS_ARG_DOCSTRINGS,
    )
    def get_logs(  # noqa: F811
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        run: Optional[str] = None,
        mode: Union[str, JobLogMode] = JobLogMode.TAIL,
        max_lines: Optional[int] = None,
        **_kwargs: Dict[str, Any],
    ) -> str:
        """"Wait for a job to enter a specific state."""
        id = _resolve_id_from_args(id, _kwargs)  # noqa: A001
        return self._private_sdk.get_logs(
            job_id=id,
            name=name,
            cloud=cloud,
            project=project,
            run=run,
            mode=mode,
            max_lines=max_lines,
        )
