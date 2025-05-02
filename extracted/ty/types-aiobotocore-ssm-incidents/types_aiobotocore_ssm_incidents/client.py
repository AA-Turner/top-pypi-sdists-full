"""
Type annotations for ssm-incidents service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_incidents.client import SSMIncidentsClient

    session = get_session()
    async with session.create_client("ssm-incidents") as client:
        client: SSMIncidentsClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    GetResourcePoliciesPaginator,
    ListIncidentFindingsPaginator,
    ListIncidentRecordsPaginator,
    ListRelatedItemsPaginator,
    ListReplicationSetsPaginator,
    ListResponsePlansPaginator,
    ListTimelineEventsPaginator,
)
from .type_defs import (
    BatchGetIncidentFindingsInputTypeDef,
    BatchGetIncidentFindingsOutputTypeDef,
    CreateReplicationSetInputTypeDef,
    CreateReplicationSetOutputTypeDef,
    CreateResponsePlanInputTypeDef,
    CreateResponsePlanOutputTypeDef,
    CreateTimelineEventInputTypeDef,
    CreateTimelineEventOutputTypeDef,
    DeleteIncidentRecordInputTypeDef,
    DeleteReplicationSetInputTypeDef,
    DeleteResourcePolicyInputTypeDef,
    DeleteResponsePlanInputTypeDef,
    DeleteTimelineEventInputTypeDef,
    GetIncidentRecordInputTypeDef,
    GetIncidentRecordOutputTypeDef,
    GetReplicationSetInputTypeDef,
    GetReplicationSetOutputTypeDef,
    GetResourcePoliciesInputTypeDef,
    GetResourcePoliciesOutputTypeDef,
    GetResponsePlanInputTypeDef,
    GetResponsePlanOutputTypeDef,
    GetTimelineEventInputTypeDef,
    GetTimelineEventOutputTypeDef,
    ListIncidentFindingsInputTypeDef,
    ListIncidentFindingsOutputTypeDef,
    ListIncidentRecordsInputTypeDef,
    ListIncidentRecordsOutputTypeDef,
    ListRelatedItemsInputTypeDef,
    ListRelatedItemsOutputTypeDef,
    ListReplicationSetsInputTypeDef,
    ListReplicationSetsOutputTypeDef,
    ListResponsePlansInputTypeDef,
    ListResponsePlansOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTimelineEventsInputTypeDef,
    ListTimelineEventsOutputTypeDef,
    PutResourcePolicyInputTypeDef,
    PutResourcePolicyOutputTypeDef,
    StartIncidentInputTypeDef,
    StartIncidentOutputTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateDeletionProtectionInputTypeDef,
    UpdateIncidentRecordInputTypeDef,
    UpdateRelatedItemsInputTypeDef,
    UpdateReplicationSetInputTypeDef,
    UpdateResponsePlanInputTypeDef,
    UpdateTimelineEventInputTypeDef,
)
from .waiter import WaitForReplicationSetActiveWaiter, WaitForReplicationSetDeletedWaiter

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("SSMIncidentsClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class SSMIncidentsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SSMIncidentsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#generate_presigned_url)
        """

    async def batch_get_incident_findings(
        self, **kwargs: Unpack[BatchGetIncidentFindingsInputTypeDef]
    ) -> BatchGetIncidentFindingsOutputTypeDef:
        """
        Retrieves details about all specified findings for an incident, including
        descriptive details about each finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/batch_get_incident_findings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#batch_get_incident_findings)
        """

    async def create_replication_set(
        self, **kwargs: Unpack[CreateReplicationSetInputTypeDef]
    ) -> CreateReplicationSetOutputTypeDef:
        """
        A replication set replicates and encrypts your data to the provided Regions
        with the provided KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/create_replication_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#create_replication_set)
        """

    async def create_response_plan(
        self, **kwargs: Unpack[CreateResponsePlanInputTypeDef]
    ) -> CreateResponsePlanOutputTypeDef:
        """
        Creates a response plan that automates the initial response to incidents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/create_response_plan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#create_response_plan)
        """

    async def create_timeline_event(
        self, **kwargs: Unpack[CreateTimelineEventInputTypeDef]
    ) -> CreateTimelineEventOutputTypeDef:
        """
        Creates a custom timeline event on the incident details page of an incident
        record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/create_timeline_event.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#create_timeline_event)
        """

    async def delete_incident_record(
        self, **kwargs: Unpack[DeleteIncidentRecordInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an incident record from Incident Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_incident_record.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_incident_record)
        """

    async def delete_replication_set(
        self, **kwargs: Unpack[DeleteReplicationSetInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes all Regions in your replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_replication_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_replication_set)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the resource policy that Resource Access Manager uses to share your
        Incident Manager resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_resource_policy)
        """

    async def delete_response_plan(
        self, **kwargs: Unpack[DeleteResponsePlanInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_response_plan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_response_plan)
        """

    async def delete_timeline_event(
        self, **kwargs: Unpack[DeleteTimelineEventInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a timeline event from an incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/delete_timeline_event.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#delete_timeline_event)
        """

    async def get_incident_record(
        self, **kwargs: Unpack[GetIncidentRecordInputTypeDef]
    ) -> GetIncidentRecordOutputTypeDef:
        """
        Returns the details for the specified incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_incident_record.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_incident_record)
        """

    async def get_replication_set(
        self, **kwargs: Unpack[GetReplicationSetInputTypeDef]
    ) -> GetReplicationSetOutputTypeDef:
        """
        Retrieve your Incident Manager replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_replication_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_replication_set)
        """

    async def get_resource_policies(
        self, **kwargs: Unpack[GetResourcePoliciesInputTypeDef]
    ) -> GetResourcePoliciesOutputTypeDef:
        """
        Retrieves the resource policies attached to the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_resource_policies.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_resource_policies)
        """

    async def get_response_plan(
        self, **kwargs: Unpack[GetResponsePlanInputTypeDef]
    ) -> GetResponsePlanOutputTypeDef:
        """
        Retrieves the details of the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_response_plan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_response_plan)
        """

    async def get_timeline_event(
        self, **kwargs: Unpack[GetTimelineEventInputTypeDef]
    ) -> GetTimelineEventOutputTypeDef:
        """
        Retrieves a timeline event based on its ID and incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_timeline_event.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_timeline_event)
        """

    async def list_incident_findings(
        self, **kwargs: Unpack[ListIncidentFindingsInputTypeDef]
    ) -> ListIncidentFindingsOutputTypeDef:
        """
        Retrieves a list of the IDs of findings, plus their last modified times, that
        have been identified for a specified incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_incident_findings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_incident_findings)
        """

    async def list_incident_records(
        self, **kwargs: Unpack[ListIncidentRecordsInputTypeDef]
    ) -> ListIncidentRecordsOutputTypeDef:
        """
        Lists all incident records in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_incident_records.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_incident_records)
        """

    async def list_related_items(
        self, **kwargs: Unpack[ListRelatedItemsInputTypeDef]
    ) -> ListRelatedItemsOutputTypeDef:
        """
        List all related items for an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_related_items.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_related_items)
        """

    async def list_replication_sets(
        self, **kwargs: Unpack[ListReplicationSetsInputTypeDef]
    ) -> ListReplicationSetsOutputTypeDef:
        """
        Lists details about the replication set configured in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_replication_sets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_replication_sets)
        """

    async def list_response_plans(
        self, **kwargs: Unpack[ListResponsePlansInputTypeDef]
    ) -> ListResponsePlansOutputTypeDef:
        """
        Lists all response plans in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_response_plans.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_response_plans)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags that are attached to the specified response plan or incident.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_tags_for_resource)
        """

    async def list_timeline_events(
        self, **kwargs: Unpack[ListTimelineEventsInputTypeDef]
    ) -> ListTimelineEventsOutputTypeDef:
        """
        Lists timeline events for the specified incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/list_timeline_events.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#list_timeline_events)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyInputTypeDef]
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Adds a resource policy to the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/put_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#put_resource_policy)
        """

    async def start_incident(
        self, **kwargs: Unpack[StartIncidentInputTypeDef]
    ) -> StartIncidentOutputTypeDef:
        """
        Used to start an incident from CloudWatch alarms, EventBridge events, or
        manually.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/start_incident.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#start_incident)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds a tag to a response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#untag_resource)
        """

    async def update_deletion_protection(
        self, **kwargs: Unpack[UpdateDeletionProtectionInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Update deletion protection to either allow or deny deletion of the final Region
        in a replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_deletion_protection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_deletion_protection)
        """

    async def update_incident_record(
        self, **kwargs: Unpack[UpdateIncidentRecordInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Update the details of an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_incident_record.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_incident_record)
        """

    async def update_related_items(
        self, **kwargs: Unpack[UpdateRelatedItemsInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Add or remove related items from the related items tab of an incident record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_related_items.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_related_items)
        """

    async def update_replication_set(
        self, **kwargs: Unpack[UpdateReplicationSetInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Add or delete Regions from your replication set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_replication_set.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_replication_set)
        """

    async def update_response_plan(
        self, **kwargs: Unpack[UpdateResponsePlanInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified response plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_response_plan.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_response_plan)
        """

    async def update_timeline_event(
        self, **kwargs: Unpack[UpdateTimelineEventInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates a timeline event.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/update_timeline_event.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#update_timeline_event)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_resource_policies"]
    ) -> GetResourcePoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_incident_findings"]
    ) -> ListIncidentFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_incident_records"]
    ) -> ListIncidentRecordsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_related_items"]
    ) -> ListRelatedItemsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_replication_sets"]
    ) -> ListReplicationSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_response_plans"]
    ) -> ListResponsePlansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_timeline_events"]
    ) -> ListTimelineEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["wait_for_replication_set_active"]
    ) -> WaitForReplicationSetActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["wait_for_replication_set_deleted"]
    ) -> WaitForReplicationSetDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-incidents.html#SSMIncidents.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_incidents/client/)
        """
