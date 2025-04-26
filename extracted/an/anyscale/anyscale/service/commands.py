from typing import Optional, Union

from anyscale._private.sdk import sdk_command
from anyscale.service._private.service_sdk import PrivateServiceSDK
from anyscale.service.models import (
    ServiceConfig,
    ServiceLogMode,
    ServiceState,
    ServiceStatus,
)


_SERVICE_SDK_SINGLETON_KEY = "service_sdk"

_DEPLOY_EXAMPLE = """
import anyscale
from anyscale.service.models import ServiceConfig

anyscale.service.deploy(
    ServiceConfig(
        name="my-service",
        applications=[
            {"import_path": "main:app"},
        ],
        working_dir=".",
    ),
    canary_percent=50,
)
"""

_DEPLOY_ARG_DOCSTRINGS = {
    "config": "The config options defining the service.",
    "in_place": "Perform an in-place upgrade without starting a new cluster. This can be used for faster iteration during development but is *not* currently recommended for production deploys. This *cannot* be used to change cluster-level options such as image and compute config (they will be ignored).",
    "canary_percent": "The percentage of traffic to send to the canary version of the service (0-100). This can be used to manually shift traffic toward (or away from) the canary version. If not provided, traffic will be shifted incrementally toward the canary version until it reaches 100. Not supported when using --in-place.",
    "max_surge_percent": "Amount of excess capacity allowed to be used while updating the service (0-100). Defaults to 100. Not supported when using --in-place.",
}


@sdk_command(
    _SERVICE_SDK_SINGLETON_KEY,
    PrivateServiceSDK,
    doc_py_example=_DEPLOY_EXAMPLE,
    arg_docstrings=_DEPLOY_ARG_DOCSTRINGS,
)
def deploy(
    config: ServiceConfig,
    *,
    in_place: bool = False,
    canary_percent: Optional[int] = None,
    max_surge_percent: Optional[int] = None,
    _private_sdk: Optional[PrivateServiceSDK] = None,
) -> str:
    """Deploy a service.

    If no service with the provided name is running, one will be created, else the existing service will be updated.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the deployed service.
    """
    return _private_sdk.deploy(  # type: ignore
        config,
        in_place=in_place,
        canary_percent=canary_percent,
        max_surge_percent=max_surge_percent,
    )


_ROLLBACK_EXAMPLE = """
import anyscale

anyscale.service.rollback(name="my-service")
"""

_ROLLBACK_ARG_DOCSTRINGS = {
    "name": "Name of the service. When running in a workspace, this defaults to the workspace name.",
    "cloud": "The Anyscale Cloud of this workload. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the service. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "max_surge_percent": "Amount of excess capacity allowed to be used while rolling back to the primary version of the service (0-100). Defaults to 100.",
}


@sdk_command(
    _SERVICE_SDK_SINGLETON_KEY,
    PrivateServiceSDK,
    doc_py_example=_ROLLBACK_EXAMPLE,
    arg_docstrings=_ROLLBACK_ARG_DOCSTRINGS,
)
def rollback(
    name: Optional[str],
    *,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    max_surge_percent: Optional[int] = None,
    _private_sdk: Optional[PrivateServiceSDK] = None,
) -> str:
    """Rollback to the primary version of the service.

    This command can only be used when there is an active rollout in progress. The
    rollout will be cancelled and the service will revert to the primary version.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the rolled back service.
    """
    return _private_sdk.rollback(  # type: ignore
        name=name, cloud=cloud, project=project, max_surge_percent=max_surge_percent
    )


_TERMINATE_EXAMPLE = """
import anyscale

anyscale.service.terminate(name="my-service")
"""

_TERMINATE_ARG_DOCSTRINGS = {
    "name": "Name of the service. When running in a workspace, this defaults to the workspace name.",
    "cloud": "The Anyscale Cloud of this workload. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the service. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _SERVICE_SDK_SINGLETON_KEY,
    PrivateServiceSDK,
    doc_py_example=_TERMINATE_EXAMPLE,
    arg_docstrings=_TERMINATE_ARG_DOCSTRINGS,
)
def terminate(
    name: Optional[str] = None,
    *,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateServiceSDK] = None,
) -> str:
    """Terminate a service.

    This command is asynchronous, so it always returns immediately.

    Returns the id of the terminated service.
    """
    return _private_sdk.terminate(name=name, cloud=cloud, project=project)  # type: ignore


_ARCHIVE_EXAMPLE = """
import anyscale

anyscale.service.archive(name="my-service")
"""

_ARCHIVE_ARG_DOCSTRINGS = {
    "id": "ID of the service.",
    "name": "Name of the service. When running in a workspace, this defaults to the workspace name.",
    "cloud": "The Anyscale Cloud of this workload. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the service. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _SERVICE_SDK_SINGLETON_KEY,
    PrivateServiceSDK,
    doc_py_example=_ARCHIVE_EXAMPLE,
    arg_docstrings=_ARCHIVE_ARG_DOCSTRINGS,
)
def archive(
    id: Optional[str] = None,  # noqa: A002
    name: Optional[str] = None,
    *,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateServiceSDK] = None,
) -> str:
    """Archive a service.

    This command is asynchronous, so it always returns immediately.

    Returns the ID of the archived service.
    """
    return _private_sdk.archive(id=id, name=name, cloud=cloud, project=project)  # type: ignore


_DELETE_EXAMPLE = """
import anyscale

anyscale.service.delete(name="my-service")
"""

_DELETE_ARG_DOCSTRINGS = {
    "id": "ID of the service.",
    "name": "Name of the service. When running in a workspace, this defaults to the workspace name.",
    "cloud": "The Anyscale Cloud of this workload. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the service. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _SERVICE_SDK_SINGLETON_KEY,
    PrivateServiceSDK,
    doc_py_example=_DELETE_EXAMPLE,
    arg_docstrings=_DELETE_ARG_DOCSTRINGS,
)
def delete(
    id: Optional[str] = None,  # noqa: A002
    name: Optional[str] = None,
    *,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateServiceSDK] = None,
) -> str:
    """Delete a service.

    This command is asynchronous, so it always returns immediately.

    Returns the ID of the deleted service.
    """
    return _private_sdk.delete(id=id, name=name, cloud=cloud, project=project)  # type: ignore


_STATUS_EXAMPLE = """
import anyscale
from anyscale.service.models import ServiceStatus

status: ServiceStatus = anyscale.service.status(name="my-service")
"""

_STATUS_ARG_DOCSTRINGS = {
    "name": "Name of the service.",
    "cloud": "The Anyscale Cloud of this workload. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the service. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
}


@sdk_command(
    _SERVICE_SDK_SINGLETON_KEY,
    PrivateServiceSDK,
    doc_py_example=_STATUS_EXAMPLE,
    arg_docstrings=_STATUS_ARG_DOCSTRINGS,
)
def status(
    name: str,
    *,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    _private_sdk: Optional[PrivateServiceSDK] = None,
) -> ServiceStatus:
    """Get the status of a service."""
    return _private_sdk.status(name=name, cloud=cloud, project=project)  # type: ignore


_WAIT_EXAMPLE = """
import anyscale
from anyscale.service.models import ServiceState

anyscale.service.wait(name="my-service", state=ServiceState.RUNNING)
"""

_WAIT_ARG_DOCSTRINGS = {
    "name": "Name of the service.",
    "cloud": "The Anyscale Cloud of this workload. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the service. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "state": "The state to wait for the service to reach.",
    "timeout_s": "Timeout to wait for the service to reach the target state.",
}


@sdk_command(
    _SERVICE_SDK_SINGLETON_KEY,
    PrivateServiceSDK,
    doc_py_example=_WAIT_EXAMPLE,
    arg_docstrings=_WAIT_ARG_DOCSTRINGS,
)
def wait(
    name: str,
    *,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    state: Union[str, ServiceState] = ServiceState.RUNNING,
    timeout_s: float = 600,
    _private_sdk: Optional[PrivateServiceSDK] = None,
    _interval_s: float = 5,
):
    """Wait for a service to reach a target state."""
    _private_sdk.wait(  # type: ignore
        name=name,
        cloud=cloud,
        project=project,
        state=ServiceState(state),
        timeout_s=timeout_s,
        interval_s=_interval_s,
    )  # type: ignore


_CONTROLLER_LOGS_EXAMPLE = """
import anyscale

anyscale.service.controller_logs("my-service", canary=True)
"""

_CONTROLLER_LOGS_ARG_DOCSTRINGS = {
    "name": "Name of the service.",
    "cloud": "The Anyscale Cloud of this workload. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace).",
    "project": "Named project to use for the service. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace).",
    "canary": "Whether to show the logs of the canary version of the service. If not provided, the primary version logs will be shown.",
    "mode": "The mode of log fetching to be used. Supported modes can be found in ServiceLogMode. If not provided, ServiceLogMode.TAIL will be used.",
    "max_lines": "The number of log lines to be fetched. If not provided, 1000 lines will be fetched.",
}


# This is a private command that is not exposed to the user.
@sdk_command(
    _SERVICE_SDK_SINGLETON_KEY,
    PrivateServiceSDK,
    doc_py_example=_CONTROLLER_LOGS_EXAMPLE,
    arg_docstrings=_CONTROLLER_LOGS_ARG_DOCSTRINGS,
)
def _controller_logs(
    name: str,
    *,
    cloud: Optional[str] = None,
    project: Optional[str] = None,
    canary: bool = False,
    mode: Union[str, ServiceLogMode] = ServiceLogMode.TAIL,
    max_lines: int = 1000,
    _private_sdk: Optional[PrivateServiceSDK] = None,
):
    """Wait for a service to reach a target state."""
    return _private_sdk.controller_logs(  # type: ignore
        name,
        cloud=cloud,
        project=project,
        canary=canary,
        mode=mode,
        max_lines=max_lines,
    )
