"""
Type annotations for agent-registry-control service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_agent_registry_control.client import AgentRegistryControlClient

    session = get_session()
    async with session.create_client("agent-registry-control") as client:
        client: AgentRegistryControlClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListRegistriesPaginator, ListRegistryRecordsPaginator
from .type_defs import (
    CreateRegistryRecordRequestTypeDef,
    CreateRegistryRecordResponseTypeDef,
    CreateRegistryRequestTypeDef,
    CreateRegistryResponseTypeDef,
    DeleteRegistryRecordRequestTypeDef,
    DeleteRegistryRequestTypeDef,
    DeleteRegistryResponseTypeDef,
    GetRegistryRecordRequestTypeDef,
    GetRegistryRecordResponseTypeDef,
    GetRegistryRequestTypeDef,
    GetRegistryResponseTypeDef,
    ListRegistriesRequestTypeDef,
    ListRegistriesResponseTypeDef,
    ListRegistryRecordsRequestTypeDef,
    ListRegistryRecordsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SubmitRegistryRecordForApprovalRequestTypeDef,
    SubmitRegistryRecordForApprovalResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateRegistryRecordRequestTypeDef,
    UpdateRegistryRecordResponseTypeDef,
    UpdateRegistryRecordStatusRequestTypeDef,
    UpdateRegistryRecordStatusResponseTypeDef,
    UpdateRegistryRequestTypeDef,
    UpdateRegistryResponseTypeDef,
)
from .waiter import RegistryReadyWaiter, RegistryRecordApprovedWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("AgentRegistryControlClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class AgentRegistryControlClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control.html#AgentRegistryControl.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AgentRegistryControlClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control.html#AgentRegistryControl.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#generate_presigned_url)
        """

    async def create_registry(
        self, **kwargs: Unpack[CreateRegistryRequestTypeDef]
    ) -> CreateRegistryResponseTypeDef:
        """
        Creates a new registry, a catalog that organizes registry records and defines
        their discovery authorization and record approval behavior.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/create_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#create_registry)
        """

    async def create_registry_record(
        self, **kwargs: Unpack[CreateRegistryRecordRequestTypeDef]
    ) -> CreateRegistryRecordResponseTypeDef:
        """
        Creates a registry record within a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/create_registry_record.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#create_registry_record)
        """

    async def delete_registry(
        self, **kwargs: Unpack[DeleteRegistryRequestTypeDef]
    ) -> DeleteRegistryResponseTypeDef:
        """
        Deletes a registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/delete_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#delete_registry)
        """

    async def delete_registry_record(
        self, **kwargs: Unpack[DeleteRegistryRecordRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a registry record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/delete_registry_record.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#delete_registry_record)
        """

    async def get_registry(
        self, **kwargs: Unpack[GetRegistryRequestTypeDef]
    ) -> GetRegistryResponseTypeDef:
        """
        Gets a registry by identifier (ARN or ID).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/get_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#get_registry)
        """

    async def get_registry_record(
        self, **kwargs: Unpack[GetRegistryRecordRequestTypeDef]
    ) -> GetRegistryRecordResponseTypeDef:
        """
        Retrieves the details of a registry record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/get_registry_record.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#get_registry_record)
        """

    async def list_registries(
        self, **kwargs: Unpack[ListRegistriesRequestTypeDef]
    ) -> ListRegistriesResponseTypeDef:
        """
        Lists the registries in the caller's account and Region, with optional
        filtering by status and discovery authorizer type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/list_registries.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#list_registries)
        """

    async def list_registry_records(
        self, **kwargs: Unpack[ListRegistryRecordsRequestTypeDef]
    ) -> ListRegistryRecordsResponseTypeDef:
        """
        Lists the registry records within a registry, with optional filtering by name,
        status, and record type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/list_registry_records.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#list_registry_records)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List the tags on a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#list_tags_for_resource)
        """

    async def submit_registry_record_for_approval(
        self, **kwargs: Unpack[SubmitRegistryRecordForApprovalRequestTypeDef]
    ) -> SubmitRegistryRecordForApprovalResponseTypeDef:
        """
        Submits a DRAFT registry record for approval, moving it into the registry's
        approval workflow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/submit_registry_record_for_approval.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#submit_registry_record_for_approval)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Tag a resource with key-value pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Remove tags from a resource by key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#untag_resource)
        """

    async def update_registry(
        self, **kwargs: Unpack[UpdateRegistryRequestTypeDef]
    ) -> UpdateRegistryResponseTypeDef:
        """
        Updates an existing registry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/update_registry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#update_registry)
        """

    async def update_registry_record(
        self, **kwargs: Unpack[UpdateRegistryRecordRequestTypeDef]
    ) -> UpdateRegistryRecordResponseTypeDef:
        """
        Updates a registry record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/update_registry_record.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#update_registry_record)
        """

    async def update_registry_record_status(
        self, **kwargs: Unpack[UpdateRegistryRecordStatusRequestTypeDef]
    ) -> UpdateRegistryRecordStatusResponseTypeDef:
        """
        Updates the status of a registry record as part of the registry's curation
        workflow, for example to approve or reject a record that is pending approval,
        or to deprecate an approved record so that it is no longer discoverable.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/update_registry_record_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#update_registry_record_status)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_registries"]
    ) -> ListRegistriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_registry_records"]
    ) -> ListRegistryRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["registry_ready"]
    ) -> RegistryReadyWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["registry_record_approved"]
    ) -> RegistryRecordApprovedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control.html#AgentRegistryControl.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/agent-registry-control.html#AgentRegistryControl.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_agent_registry_control/client/)
        """
