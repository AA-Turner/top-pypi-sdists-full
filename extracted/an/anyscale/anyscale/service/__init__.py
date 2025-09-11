from typing import List, Optional, Union

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.models.model_base import ResultIterator
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.service._private.service_sdk import PrivateServiceSDK
from anyscale.service.commands import (
    _ARCHIVE_ARG_DOCSTRINGS,
    _ARCHIVE_EXAMPLE,
    _controller_logs,
    _CONTROLLER_LOGS_ARG_DOCSTRINGS,
    _CONTROLLER_LOGS_EXAMPLE,
    _DELETE_ARG_DOCSTRINGS,
    _DELETE_EXAMPLE,
    _DEPLOY_ARG_DOCSTRINGS,
    _DEPLOY_EXAMPLE,
    _LIST_ARG_DOCSTRINGS,
    _LIST_EXAMPLE,
    _ROLLBACK_ARG_DOCSTRINGS,
    _ROLLBACK_EXAMPLE,
    _STATUS_ARG_DOCSTRINGS,
    _STATUS_EXAMPLE,
    _TERMINATE_ARG_DOCSTRINGS,
    _TERMINATE_EXAMPLE,
    _WAIT_ARG_DOCSTRINGS,
    _WAIT_EXAMPLE,
    archive,
    delete,
    deploy,
    list,
    rollback,
    status,
    terminate,
    wait,
)
from anyscale.service.models import (
    ServiceConfig,
    ServiceLogMode,
    ServiceSortField,
    ServiceSortOrder,
    ServiceState,
    ServiceStatus,
)


class ServiceSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateServiceSDK(client=client, logger=logger, timer=timer)

    @sdk_docs(
        doc_py_example=_DEPLOY_EXAMPLE, arg_docstrings=_DEPLOY_ARG_DOCSTRINGS,
    )
    def deploy(  # noqa: F811
        self,
        config: ServiceConfig,
        *,
        in_place: bool = False,
        canary_percent: Optional[int] = None,
        max_surge_percent: Optional[int] = None,
    ) -> str:
        """Deploy a service.

        If no service with the provided name is running, one will be created, else the existing service will be updated.

        This command is asynchronous, so it always returns immediately.

        Returns the id of the deployed service.
        """
        return self._private_sdk.deploy(
            config,
            in_place=in_place,
            canary_percent=canary_percent,
            max_surge_percent=max_surge_percent,
        )

    @sdk_docs(
        doc_py_example=_ROLLBACK_EXAMPLE, arg_docstrings=_ROLLBACK_ARG_DOCSTRINGS,
    )
    def rollback(  # noqa: F811
        self,
        name: Optional[str] = None,
        *,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        max_surge_percent: Optional[int] = None,
    ) -> str:
        """Rollback to the primary version of the service.

        This command can only be used when there is an active rollout in progress. The
        rollout will be cancelled and the service will revert to the primary version.

        This command is asynchronous, so it always returns immediately.

        Returns the id of the rolled back service.
        """
        return self._private_sdk.rollback(
            name=name, max_surge_percent=max_surge_percent, cloud=cloud, project=project
        )

    @sdk_docs(
        doc_py_example=_TERMINATE_EXAMPLE, arg_docstrings=_TERMINATE_ARG_DOCSTRINGS,
    )
    def terminate(  # noqa: F811
        self,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        *,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        """Terminate a service.

        This command is asynchronous, so it always returns immediately.

        Returns the id of the terminated service.
        """
        return self._private_sdk.terminate(
            id=id, name=name, cloud=cloud, project=project
        )

    @sdk_docs(
        doc_py_example=_ARCHIVE_EXAMPLE, arg_docstrings=_ARCHIVE_ARG_DOCSTRINGS,
    )
    def archive(  # noqa: F811
        self,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        *,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        """Archive a service.

        This command is asynchronous, so it always returns immediately.

        Returns the ID of the archived service.
        """
        return self._private_sdk.archive(id=id, name=name, cloud=cloud, project=project)

    @sdk_docs(
        doc_py_example=_DELETE_EXAMPLE, arg_docstrings=_DELETE_ARG_DOCSTRINGS,
    )
    def delete(  # noqa: F811
        self,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        *,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ):
        """Delete a service.

        This command is asynchronous, so it always returns immediately.
        """
        return self._private_sdk.delete(id=id, name=name, cloud=cloud, project=project)

    @sdk_docs(
        doc_py_example=_LIST_EXAMPLE, arg_docstrings=_LIST_ARG_DOCSTRINGS,
    )
    def list(  # noqa: F811, A001
        self,
        *,
        # Single-item lookup
        service_id: Optional[str] = None,
        # Filters
        name: Optional[str] = None,
        state_filter: Optional[Union[List[ServiceState], List[str]]] = None,
        creator_id: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        include_archived: bool = False,
        # Paging
        max_items: Optional[int] = None,
        page_size: Optional[int] = None,
        # Sorting
        sort_field: Optional[Union[str, ServiceSortField]] = None,
        sort_order: Optional[Union[str, ServiceSortOrder]] = None,
    ) -> ResultIterator[ServiceStatus]:
        """List services.

        Returns
        -------
        ResultIterator[ServiceStatus]
            An iterator yielding ServiceStatus objects. Fetches pages
            lazily as needed. Use a `for` loop to iterate or `list()`
            to consume all at once.
        """
        return self._private_sdk.list(
            service_id=service_id,
            name=name,
            state_filter=state_filter,
            creator_id=creator_id,
            cloud=cloud,
            project=project,
            include_archived=include_archived,
            max_items=max_items,
            page_size=page_size,
            sort_field=sort_field,
            sort_order=sort_order,
        )

    @sdk_docs(
        doc_py_example=_STATUS_EXAMPLE, arg_docstrings=_STATUS_ARG_DOCSTRINGS,
    )
    def status(  # noqa: F811
        self, name: str, *, cloud: Optional[str] = None, project: Optional[str] = None
    ) -> ServiceStatus:
        """Get the status of a service."""
        return self._private_sdk.status(name=name, cloud=cloud, project=project)

    @sdk_docs(
        doc_py_example=_WAIT_EXAMPLE, arg_docstrings=_WAIT_ARG_DOCSTRINGS,
    )
    def wait(  # noqa: F811
        self,
        name: str,
        *,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        state: Union[str, ServiceState] = ServiceState.RUNNING,
        timeout_s: float = 600,
        _interval_s: float = 5,
    ):
        """Wait for a service to reach a target state."""
        return self._private_sdk.wait(
            name=name,
            cloud=cloud,
            project=project,
            state=ServiceState(state),
            timeout_s=timeout_s,
            interval_s=_interval_s,
        )

    @sdk_docs(
        doc_py_example=_CONTROLLER_LOGS_EXAMPLE,
        arg_docstrings=_CONTROLLER_LOGS_ARG_DOCSTRINGS,
    )
    def controller_logs(  # noqa: F811
        self,
        name: str,
        *,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        canary: bool = False,
        mode: Union[str, ServiceLogMode] = ServiceLogMode.TAIL,
        max_lines: int = 1000,
    ) -> str:
        """Get the controller logs of a service."""
        return self._private_sdk.controller_logs(
            name=name,
            cloud=cloud,
            project=project,
            canary=canary,
            mode=mode,
            max_lines=max_lines,
        )
