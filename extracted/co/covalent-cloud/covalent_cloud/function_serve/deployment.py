# Copyright 2024 Agnostiq Inc.

import inspect
import typing
import warnings
from typing import Any, Callable, List, Optional, Union

from covalent._workflow.lattice import Lattice

from covalent_cloud.function_serve.assets import AssetsMediator
from covalent_cloud.function_serve.common import wait_for_deployment_to_be_active
from covalent_cloud.function_serve.models import (
    Deployment,
    FunctionDeploymentList,
    InferenceAPIKey,
    InferenceKeyMetadata,
)
from covalent_cloud.service_account_interface.client import get_deployment_client
from covalent_cloud.shared.classes.settings import Settings, settings
from covalent_cloud.shared.schemas.volume import Volume

if typing.TYPE_CHECKING:
    from covalent_cloud.function_serve.service_class import FunctionService

__all__ = [
    "deploy",
    "get_deployment",
    "list_function_deployments",
    "create_inference_api_key",
    "list_inference_api_keys",
    "delete_inference_api_key",
]


def deploy(
    function_service: "FunctionService", volume: Volume = None, settings: Settings = settings
) -> Callable[[Any], Deployment]:
    """Deploy a function service to Covalent Cloud.

    Args:
        function_service: A function decorated with `@cc.service`.
        volume: Grant access to a cloud storage volume in Covalent Cloud. Defaults to None.
        settings: User settings for Covalent Cloud. Defaults to settings on the client machine.

    Returns:
        A callable which launches the deployment and has the same signature as the initializer
        for `function_service`.
    """
    warnings.warn(
        "The function serve functionality is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2,
    )

    if isinstance(function_service, Lattice):
        raise TypeError("Lattices cannot be deployed. Please use `cc.dispatch()` instead.")

    def deploy_wrapper(*args, **kwargs) -> Deployment:

        # Force a TypeError if the arguments are invalid.
        # If not done here, error will be raised in remote host.
        sig = inspect.signature(function_service.init_func)
        sig.bind(*args, **kwargs)

        if volume is not None:
            # Override the volume for the function service
            function_service.volume = volume

        fn_service_model = function_service.get_model(*args, **kwargs)

        assets_mediator = AssetsMediator()
        fn_service_model = assets_mediator.hydrate_assets_from_model(
            fn_service_model, settings=settings
        )

        assets_mediator.upload_all()

        dumped_model = fn_service_model.model_dump()

        deployment_client = get_deployment_client(settings)
        response = deployment_client.post(
            "/functions",
            request_options={
                "json": dumped_model,
            },
        )

        deployment = Deployment.from_function_record(response.json())

        # Attach route methods for ease of use
        deployment.attach_route_methods()

        return deployment

    return deploy_wrapper


def get_deployment(
    function_id: Union[str, Deployment],
    wait: Union[bool, int, float] = False,
    settings: Settings = settings,
) -> Deployment:
    """Retrieve or refresh a client object for a deployed function service.

    Args:
        function_id: ID string or client object for the target deployment.
        wait: Option to wait for the deployment to be active. Defaults to False.
            Numerical values represent the approximate time to wait (in seconds)
            for the deployment to finish initializing, before raising a client-side `TimeoutError`.
            The boolean value True corresponds to 3600, i.e. 1 hour.
        settings: User settings for Covalent Cloud. Defaults to settings on the client machine.

    Returns:
        Deployment: Deployment object for the function service.
    """
    warnings.warn(
        "The function serve functionality is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2,
    )

    if isinstance(function_id, Deployment):
        function_id = function_id.function_id

    deployment_client = get_deployment_client(settings)
    response = deployment_client.get(f"/functions/{function_id}")
    deployment = Deployment.from_function_record(response.json())

    # Attach route methods for ease of use
    deployment.attach_route_methods()

    if not wait:
        return deployment

    if isinstance(wait, bool):
        wait_time_max = 3600
    elif isinstance(wait, (int, float)) and wait > 0:
        wait_time_max = wait
    else:
        raise ValueError("Invalid value for `wait`. Must be a boolean or a positive int or float.")

    return wait_for_deployment_to_be_active(deployment, wait_time_max=wait_time_max)


def list_function_deployments(
    generate_presigned_urls: bool = False,
    count: int = 10,
    page: int = 0,
    search: Optional[str] = None,
    sort: Optional[str] = "created_at",
    direction: str = "desc",
    status: Optional[str] = None,
    settings: Settings = settings,
) -> FunctionDeploymentList:
    """List all function serve deployments for the authenticated user.

    Args:
        generate_presigned_urls: Whether to generate presigned URLs for function assets. Defaults to False.
        count: Number of items per page. Defaults to 10.
        page: Page number (0-indexed). Defaults to 0.
        search: Search query to filter deployments. Defaults to None.
        sort: Field to sort by. Defaults to "created_at".
        direction: Sort direction, either "asc" or "desc". Defaults to "desc".
        status: Filter by deployment status. Defaults to None.
        settings: User settings for Covalent Cloud. Defaults to settings on the client machine.

    Returns:
        FunctionDeploymentList containing records and metadata.

    Examples:
        >>> # List all active deployments
        >>> deployments = cc.list_function_deployments(status="ACTIVE")

        >>> # Search for specific deployment
        >>> ml_services = cc.list_function_deployments(search="ML model")

        >>> # Get first page with 5 items, sorted by title
        >>> deployments = cc.list_function_deployments(count=5, page=0, sort="title", direction="asc")
    """
    warnings.warn(
        "The function serve functionality is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2,
    )

    deployment_client = get_deployment_client(settings)

    params = {
        "generate_presigned_urls": generate_presigned_urls,
        "count": count,
        "page": page,
        "direction": direction.upper(),
    }

    if search:
        params["search"] = search
    if sort:
        params["sort"] = sort
    if status:
        params["status"] = status

    response = deployment_client.get(
        "/functions",
        request_options={
            "params": params,
        },
    )

    return FunctionDeploymentList.model_validate(response.json())


def create_inference_api_key(function_id: str, settings: Settings = settings) -> InferenceAPIKey:
    """Create a new API key for function serve inference.

    Args:
        function_id: The ID of the function deployment to create an API key for.
        settings: User settings for Covalent Cloud. Defaults to settings on the client machine.

    Returns:
        InferenceAPIKey object with key details.

    Note:
        The API key value is only shown once after creation. Make sure to save it securely.

    Examples:
        >>> new_key = cc.create_inference_api_key("function-abc-123")
        >>> print(f"New API key: {new_key.key}")  # Save this - won't be shown again
        >>> print(f"Key ID: {new_key.key_id}")
    """
    warnings.warn(
        "The function serve functionality is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2,
    )

    if not function_id or not function_id.strip():
        raise ValueError("function_id cannot be empty")

    deployment_client = get_deployment_client(settings)
    response = deployment_client.post(f"/functions/{function_id}/inference-keys")

    # Convert the response to match our model format
    response_data = response.json()
    return InferenceAPIKey(
        key_id=str(response_data["id"]),
        key=response_data["key"],
        created_at=response_data.get("created_at", response_data.get("updated_at")),
    )


def list_inference_api_keys(
    function_id: str, settings: Settings = settings
) -> List[InferenceKeyMetadata]:
    """List all API keys for a function deployment.

    Args:
        function_id: The ID of the function deployment to list API keys for.
        settings: User settings for Covalent Cloud. Defaults to settings on the client machine.

    Returns:
        List of InferenceKeyMetadata objects (keys not included for security).

    Examples:
        >>> keys = cc.list_inference_api_keys("function-abc-123")
        >>> for key in keys:
        ...     print(f"Key ID: {key.key_id}, Created: {key.created_at}")
    """
    warnings.warn(
        "The function serve functionality is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2,
    )

    deployment_client = get_deployment_client(settings)
    response = deployment_client.get(f"/functions/{function_id}/inference-keys")

    # Convert the response to match our model format
    response_data = response.json()
    return [
        InferenceKeyMetadata(
            key_id=str(key_data["id"]),
            created_at=key_data.get("created_at", key_data.get("updated_at")),
            last_used=key_data.get("last_used"),
        )
        for key_data in response_data
    ]


def delete_inference_api_key(function_id: str, key_id: str, settings: Settings = settings) -> bool:
    """Delete an API key for function serve.

    Args:
        function_id: The ID of the function deployment the API key belongs to.
        key_id: The ID of the API key to delete.
        settings: User settings for Covalent Cloud. Defaults to settings on the client machine.

    Returns:
        True if successful, False otherwise.

    Examples:
        >>> success = cc.delete_inference_api_key("function-abc-123", "key-456")
        >>> if success:
        ...     print("API key deleted successfully")
    """
    warnings.warn(
        "The function serve functionality is deprecated and will be removed in a future version.",
        DeprecationWarning,
        stacklevel=2,
    )

    if not function_id or not function_id.strip():
        raise ValueError("function_id cannot be empty")
    if not key_id or not key_id.strip():
        raise ValueError("key_id cannot be empty")

    try:
        deployment_client = get_deployment_client(settings)
        response = deployment_client.delete(f"/functions/{function_id}/inference-keys/{key_id}")
        return response.status_code == 204
    except Exception:
        return False
