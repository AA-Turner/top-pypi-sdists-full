# Copyright 2024 Agnostiq Inc.

import time
from enum import Enum
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from covalent_cloud.function_serve.models import Deployment

__all__ = [
    "DEPLOY_ELECTRON_PREFIX",
    "ACTIVE_DEPLOYMENT_POLL_INTERVAL",
    "SupportedMethods",
    "ServiceStatus",
    "rename",
    "wait_for_deployment_to_be_active",
]


DEPLOY_ELECTRON_PREFIX = "#__deploy_electron__#"
ACTIVE_DEPLOYMENT_POLL_INTERVAL = 10  # seconds


class SupportedMethods(str, Enum):
    """Supported HTTP methods for a function service."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"


class ServiceStatus(str, Enum):
    """Possible statuses for a function service."""

    NEW_OBJECT = "NEW_OBJECT"
    CREATING = "CREATING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ERROR = "ERROR"


WAITING_STATUSES = {ServiceStatus.NEW_OBJECT, ServiceStatus.CREATING}


class ServeAssetType(str, Enum):
    """Possible types for the ServeAsset `type` field."""

    ASSET = "Asset"
    JSON = "JSON"


def rename(name):
    def decorator(fn):
        fn.__name__ = name
        return fn

    return decorator


def wait_for_deployment_to_be_active(
    deployment: "Deployment",
    verbose: bool = False,
    wait_time_max: Union[int, float] = 3600,
) -> "Deployment":
    """Repeatedly reloads the deployment and waits for it to become active."""

    start_time = time.monotonic()
    while deployment.status in WAITING_STATUSES:
        if time.monotonic() - start_time >= wait_time_max:
            raise TimeoutError(
                f"Timed out after {wait_time_max / 60:.1f} minutes while waiting for "
                "the deployment to become active"
            )

        if verbose:
            print(f"Deployment {deployment.function_id} status: {deployment.status}")

        # Sleep for poll interval before checking again
        time.sleep(ACTIVE_DEPLOYMENT_POLL_INTERVAL)
        deployment.reload()

    # Reload anyways in case while loop is skipped
    deployment.reload()

    return deployment
