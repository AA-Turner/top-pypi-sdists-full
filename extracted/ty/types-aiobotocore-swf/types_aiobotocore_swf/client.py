"""
Type annotations for swf service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_swf.client import SWFClient

    session = get_session()
    async with session.create_client("swf") as client:
        client: SWFClient
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
    GetWorkflowExecutionHistoryPaginator,
    ListActivityTypesPaginator,
    ListClosedWorkflowExecutionsPaginator,
    ListDomainsPaginator,
    ListOpenWorkflowExecutionsPaginator,
    ListWorkflowTypesPaginator,
    PollForDecisionTaskPaginator,
)
from .type_defs import (
    ActivityTaskStatusTypeDef,
    ActivityTaskTypeDef,
    ActivityTypeDetailTypeDef,
    ActivityTypeInfosTypeDef,
    CountClosedWorkflowExecutionsInputTypeDef,
    CountOpenWorkflowExecutionsInputTypeDef,
    CountPendingActivityTasksInputTypeDef,
    CountPendingDecisionTasksInputTypeDef,
    DecisionTaskTypeDef,
    DeleteActivityTypeInputTypeDef,
    DeleteWorkflowTypeInputTypeDef,
    DeprecateActivityTypeInputTypeDef,
    DeprecateDomainInputTypeDef,
    DeprecateWorkflowTypeInputTypeDef,
    DescribeActivityTypeInputTypeDef,
    DescribeDomainInputTypeDef,
    DescribeWorkflowExecutionInputTypeDef,
    DescribeWorkflowTypeInputTypeDef,
    DomainDetailTypeDef,
    DomainInfosTypeDef,
    EmptyResponseMetadataTypeDef,
    GetWorkflowExecutionHistoryInputTypeDef,
    HistoryTypeDef,
    ListActivityTypesInputTypeDef,
    ListClosedWorkflowExecutionsInputTypeDef,
    ListDomainsInputTypeDef,
    ListOpenWorkflowExecutionsInputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWorkflowTypesInputTypeDef,
    PendingTaskCountTypeDef,
    PollForActivityTaskInputTypeDef,
    PollForDecisionTaskInputTypeDef,
    RecordActivityTaskHeartbeatInputTypeDef,
    RegisterActivityTypeInputTypeDef,
    RegisterDomainInputTypeDef,
    RegisterWorkflowTypeInputTypeDef,
    RequestCancelWorkflowExecutionInputTypeDef,
    RespondActivityTaskCanceledInputTypeDef,
    RespondActivityTaskCompletedInputTypeDef,
    RespondActivityTaskFailedInputTypeDef,
    RespondDecisionTaskCompletedInputTypeDef,
    RunTypeDef,
    SignalWorkflowExecutionInputTypeDef,
    StartWorkflowExecutionInputTypeDef,
    TagResourceInputTypeDef,
    TerminateWorkflowExecutionInputTypeDef,
    UndeprecateActivityTypeInputTypeDef,
    UndeprecateDomainInputTypeDef,
    UndeprecateWorkflowTypeInputTypeDef,
    UntagResourceInputTypeDef,
    WorkflowExecutionCountTypeDef,
    WorkflowExecutionDetailTypeDef,
    WorkflowExecutionInfosTypeDef,
    WorkflowTypeDetailTypeDef,
    WorkflowTypeInfosTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("SWFClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    DefaultUndefinedFault: Type[BotocoreClientError]
    DomainAlreadyExistsFault: Type[BotocoreClientError]
    DomainDeprecatedFault: Type[BotocoreClientError]
    LimitExceededFault: Type[BotocoreClientError]
    OperationNotPermittedFault: Type[BotocoreClientError]
    TooManyTagsFault: Type[BotocoreClientError]
    TypeAlreadyExistsFault: Type[BotocoreClientError]
    TypeDeprecatedFault: Type[BotocoreClientError]
    TypeNotDeprecatedFault: Type[BotocoreClientError]
    UnknownResourceFault: Type[BotocoreClientError]
    WorkflowExecutionAlreadyStartedFault: Type[BotocoreClientError]


class SWFClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SWFClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#generate_presigned_url)
        """

    async def count_closed_workflow_executions(
        self, **kwargs: Unpack[CountClosedWorkflowExecutionsInputTypeDef]
    ) -> WorkflowExecutionCountTypeDef:
        """
        Returns the number of closed workflow executions within the given domain that
        meet the specified filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/count_closed_workflow_executions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#count_closed_workflow_executions)
        """

    async def count_open_workflow_executions(
        self, **kwargs: Unpack[CountOpenWorkflowExecutionsInputTypeDef]
    ) -> WorkflowExecutionCountTypeDef:
        """
        Returns the number of open workflow executions within the given domain that
        meet the specified filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/count_open_workflow_executions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#count_open_workflow_executions)
        """

    async def count_pending_activity_tasks(
        self, **kwargs: Unpack[CountPendingActivityTasksInputTypeDef]
    ) -> PendingTaskCountTypeDef:
        """
        Returns the estimated number of activity tasks in the specified task list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/count_pending_activity_tasks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#count_pending_activity_tasks)
        """

    async def count_pending_decision_tasks(
        self, **kwargs: Unpack[CountPendingDecisionTasksInputTypeDef]
    ) -> PendingTaskCountTypeDef:
        """
        Returns the estimated number of decision tasks in the specified task list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/count_pending_decision_tasks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#count_pending_decision_tasks)
        """

    async def delete_activity_type(
        self, **kwargs: Unpack[DeleteActivityTypeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified <i>activity type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/delete_activity_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#delete_activity_type)
        """

    async def delete_workflow_type(
        self, **kwargs: Unpack[DeleteWorkflowTypeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified <i>workflow type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/delete_workflow_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#delete_workflow_type)
        """

    async def deprecate_activity_type(
        self, **kwargs: Unpack[DeprecateActivityTypeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified <i>activity type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/deprecate_activity_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#deprecate_activity_type)
        """

    async def deprecate_domain(
        self, **kwargs: Unpack[DeprecateDomainInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/deprecate_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#deprecate_domain)
        """

    async def deprecate_workflow_type(
        self, **kwargs: Unpack[DeprecateWorkflowTypeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deprecates the specified <i>workflow type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/deprecate_workflow_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#deprecate_workflow_type)
        """

    async def describe_activity_type(
        self, **kwargs: Unpack[DescribeActivityTypeInputTypeDef]
    ) -> ActivityTypeDetailTypeDef:
        """
        Returns information about the specified activity type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/describe_activity_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#describe_activity_type)
        """

    async def describe_domain(
        self, **kwargs: Unpack[DescribeDomainInputTypeDef]
    ) -> DomainDetailTypeDef:
        """
        Returns information about the specified domain, including description and
        status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/describe_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#describe_domain)
        """

    async def describe_workflow_execution(
        self, **kwargs: Unpack[DescribeWorkflowExecutionInputTypeDef]
    ) -> WorkflowExecutionDetailTypeDef:
        """
        Returns information about the specified workflow execution including its type
        and some statistics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/describe_workflow_execution.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#describe_workflow_execution)
        """

    async def describe_workflow_type(
        self, **kwargs: Unpack[DescribeWorkflowTypeInputTypeDef]
    ) -> WorkflowTypeDetailTypeDef:
        """
        Returns information about the specified <i>workflow type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/describe_workflow_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#describe_workflow_type)
        """

    async def get_workflow_execution_history(
        self, **kwargs: Unpack[GetWorkflowExecutionHistoryInputTypeDef]
    ) -> HistoryTypeDef:
        """
        Returns the history of the specified workflow execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_workflow_execution_history.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_workflow_execution_history)
        """

    async def list_activity_types(
        self, **kwargs: Unpack[ListActivityTypesInputTypeDef]
    ) -> ActivityTypeInfosTypeDef:
        """
        Returns information about all activities registered in the specified domain
        that match the specified name and registration status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_activity_types.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_activity_types)
        """

    async def list_closed_workflow_executions(
        self, **kwargs: Unpack[ListClosedWorkflowExecutionsInputTypeDef]
    ) -> WorkflowExecutionInfosTypeDef:
        """
        Returns a list of closed workflow executions in the specified domain that meet
        the filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_closed_workflow_executions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_closed_workflow_executions)
        """

    async def list_domains(self, **kwargs: Unpack[ListDomainsInputTypeDef]) -> DomainInfosTypeDef:
        """
        Returns the list of domains registered in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_domains.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_domains)
        """

    async def list_open_workflow_executions(
        self, **kwargs: Unpack[ListOpenWorkflowExecutionsInputTypeDef]
    ) -> WorkflowExecutionInfosTypeDef:
        """
        Returns a list of open workflow executions in the specified domain that meet
        the filtering criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_open_workflow_executions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_open_workflow_executions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List tags for a given domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_tags_for_resource)
        """

    async def list_workflow_types(
        self, **kwargs: Unpack[ListWorkflowTypesInputTypeDef]
    ) -> WorkflowTypeInfosTypeDef:
        """
        Returns information about workflow types in the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/list_workflow_types.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#list_workflow_types)
        """

    async def poll_for_activity_task(
        self, **kwargs: Unpack[PollForActivityTaskInputTypeDef]
    ) -> ActivityTaskTypeDef:
        """
        Used by workers to get an <a>ActivityTask</a> from the specified activity
        <code>taskList</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/poll_for_activity_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#poll_for_activity_task)
        """

    async def poll_for_decision_task(
        self, **kwargs: Unpack[PollForDecisionTaskInputTypeDef]
    ) -> DecisionTaskTypeDef:
        """
        Used by deciders to get a <a>DecisionTask</a> from the specified decision
        <code>taskList</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/poll_for_decision_task.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#poll_for_decision_task)
        """

    async def record_activity_task_heartbeat(
        self, **kwargs: Unpack[RecordActivityTaskHeartbeatInputTypeDef]
    ) -> ActivityTaskStatusTypeDef:
        """
        Used by activity workers to report to the service that the <a>ActivityTask</a>
        represented by the specified <code>taskToken</code> is still making progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/record_activity_task_heartbeat.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#record_activity_task_heartbeat)
        """

    async def register_activity_type(
        self, **kwargs: Unpack[RegisterActivityTypeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new <i>activity type</i> along with its configuration settings in
        the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/register_activity_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#register_activity_type)
        """

    async def register_domain(
        self, **kwargs: Unpack[RegisterDomainInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/register_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#register_domain)
        """

    async def register_workflow_type(
        self, **kwargs: Unpack[RegisterWorkflowTypeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Registers a new <i>workflow type</i> and its configuration settings in the
        specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/register_workflow_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#register_workflow_type)
        """

    async def request_cancel_workflow_execution(
        self, **kwargs: Unpack[RequestCancelWorkflowExecutionInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a <code>WorkflowExecutionCancelRequested</code> event in the currently
        running workflow execution identified by the given domain, workflowId, and
        runId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/request_cancel_workflow_execution.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#request_cancel_workflow_execution)
        """

    async def respond_activity_task_canceled(
        self, **kwargs: Unpack[RespondActivityTaskCanceledInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the <a>ActivityTask</a> identified by
        the <code>taskToken</code> was successfully canceled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/respond_activity_task_canceled.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#respond_activity_task_canceled)
        """

    async def respond_activity_task_completed(
        self, **kwargs: Unpack[RespondActivityTaskCompletedInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the <a>ActivityTask</a> identified by
        the <code>taskToken</code> completed successfully with a <code>result</code>
        (if provided).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/respond_activity_task_completed.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#respond_activity_task_completed)
        """

    async def respond_activity_task_failed(
        self, **kwargs: Unpack[RespondActivityTaskFailedInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by workers to tell the service that the <a>ActivityTask</a> identified by
        the <code>taskToken</code> has failed with <code>reason</code> (if specified).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/respond_activity_task_failed.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#respond_activity_task_failed)
        """

    async def respond_decision_task_completed(
        self, **kwargs: Unpack[RespondDecisionTaskCompletedInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Used by deciders to tell the service that the <a>DecisionTask</a> identified by
        the <code>taskToken</code> has successfully completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/respond_decision_task_completed.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#respond_decision_task_completed)
        """

    async def signal_workflow_execution(
        self, **kwargs: Unpack[SignalWorkflowExecutionInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a <code>WorkflowExecutionSignaled</code> event in the workflow
        execution history and creates a decision task for the workflow execution
        identified by the given domain, workflowId and runId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/signal_workflow_execution.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#signal_workflow_execution)
        """

    async def start_workflow_execution(
        self, **kwargs: Unpack[StartWorkflowExecutionInputTypeDef]
    ) -> RunTypeDef:
        """
        Starts an execution of the workflow type in the specified domain using the
        provided <code>workflowId</code> and input data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/start_workflow_execution.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#start_workflow_execution)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Add a tag to a Amazon SWF domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#tag_resource)
        """

    async def terminate_workflow_execution(
        self, **kwargs: Unpack[TerminateWorkflowExecutionInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Records a <code>WorkflowExecutionTerminated</code> event and forces closure of
        the workflow execution identified by the given domain, runId, and workflowId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/terminate_workflow_execution.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#terminate_workflow_execution)
        """

    async def undeprecate_activity_type(
        self, **kwargs: Unpack[UndeprecateActivityTypeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated <i>activity type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/undeprecate_activity_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#undeprecate_activity_type)
        """

    async def undeprecate_domain(
        self, **kwargs: Unpack[UndeprecateDomainInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/undeprecate_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#undeprecate_domain)
        """

    async def undeprecate_workflow_type(
        self, **kwargs: Unpack[UndeprecateWorkflowTypeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Undeprecates a previously deprecated <i>workflow type</i>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/undeprecate_workflow_type.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#undeprecate_workflow_type)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove a tag from a Amazon SWF domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_workflow_execution_history"]
    ) -> GetWorkflowExecutionHistoryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_activity_types"]
    ) -> ListActivityTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_closed_workflow_executions"]
    ) -> ListClosedWorkflowExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_domains"]
    ) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_open_workflow_executions"]
    ) -> ListOpenWorkflowExecutionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workflow_types"]
    ) -> ListWorkflowTypesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["poll_for_decision_task"]
    ) -> PollForDecisionTaskPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf.html#SWF.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/client/)
        """
