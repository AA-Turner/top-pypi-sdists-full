import functools
import json
import logging
import random
import re
import time
from datetime import datetime, timezone
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Type,
    TypeVar,
    Union,
)
from uuid import uuid4

from . import env
from .build_config import get_build_config_for_stage
from .client import get_s3_client, get_sqs_client
from .config import config
from .middleware import MET, RT, MiddlewareFunction, MiddlewareRegistration
from .models.events.api_event import APIEvent
from .models.events.base_event import BaseEvent
from .models.events.dynamodb_event import DynamoDBEvent
from .models.events.managed_sqs_batch_event import ManagedSQSBatchEvent
from .models.events.managed_sqs_event import ManagedSQSEvent
from .models.events.scheduled_event import ScheduledEvent
from .models.events.unmanaged_sqs_event import UnmanagedSQSEvent
from .models.mock.mock_context import MockLambdaContext
from .models.mock.mock_event import MockSQSLambdaEvent
from .models.task import MANAGED_SQS_TASK_TYPES, AsyncLambdaTask, TaskTriggerType
from .payload_encoder import PayloadEncoder
from .util import make_cf_tags

logger = logging.getLogger(__name__)

BaseEventT = TypeVar("BaseEventT", bound=BaseEvent)
APIEventT = TypeVar("APIEventT", bound=APIEvent)
ManagedSQSEventT = TypeVar("ManagedSQSEventT", bound=ManagedSQSEvent)
ManagedSQSBatchEventT = TypeVar("ManagedSQSBatchEventT", bound=ManagedSQSBatchEvent)
UnmanagedSQSEventT = TypeVar("UnmanagedSQSEventT", bound=UnmanagedSQSEvent)
ScheduledEventT = TypeVar("ScheduledEventT", bound=ScheduledEvent)
DynamoDBEventT = TypeVar("DynamoDBEventT", bound=DynamoDBEvent)


class BatchInvokeException(Exception):
    """
    Exception raised when a batch invocation fails for one or more payloads.

    Attributes:
        failed_payloads (List[int]): List of indices or identifiers of payloads that failed during batch invocation.

    Args:
        msg (str): Description of the error.
        failed_payloads (List[int]): List of failed payload indices or identifiers.
    """

    failed_payloads: List[int]

    def __init__(self, msg: str, failed_payloads: List[int]):
        self.failed_payloads = failed_payloads
        super().__init__(msg)


class AsyncLambdaController:
    """
    AsyncLambdaController manages async tasks, middleware, and invocation logic for the async-lambda framework.

    This controller enables registration, invocation, and orchestration of various Lambda tasks triggered by SQS, API Gateway, DynamoDB Streams, scheduled events, and more. It supports lane-based parallelism, payload management (including S3 for large payloads), middleware chaining, and parent-child controller composition.

    Key Features:
    - Register async tasks via decorators for SQS, API, scheduled, DynamoDB, and pure Lambda events.
    - Invoke tasks asynchronously or synchronously, with support for batching and lane assignment.
    - Manage middleware for event processing, including inheritance from parent controllers.
    - Handle payload serialization, S3 offloading for large payloads, and deletion after processing.
    - Generate AWS SAM templates for deployment, including SQS queues, S3 buckets, and API Gateway resources.
    - Support for Dead Letter Queue (DLQ) tasks and external async tasks.
    - Track invocation context, lane, and task IDs for advanced orchestration.

    Attributes:
        is_sub (bool): Indicates if this controller is a sub-controller.
        lane_count (Optional[int]): Number of parallel lanes for task execution.
        propagate_lane_assignment (Optional[bool]): Whether lane assignment should propagate to child controllers.
        tasks (Dict[str, AsyncLambdaTask]): Registered async tasks.
        external_async_tasks (Set[str]): External async task identifiers.
        current_task_id (Optional[str]): Currently executing task ID.
        current_lane (Optional[int]): Currently executing lane index.
        current_invocation_id (Optional[str]): Current invocation ID.
        parent_controller (Optional[AsyncLambdaController]): Parent controller for composition.
        middleware (List[MiddlewareRegistration]): Registered middleware functions.
        delete_s3_payloads (bool): Whether to delete S3 payloads after processing.
        controller_name (Optional[str]): Name of the controller.
        dlq_task_id (Optional[str]): Task ID for the Dead Letter Queue.

    Methods:
        add_middleware(event_types, func): Register middleware for specific event types.
        get_middleware_for_event(event): Retrieve applicable middleware for an event.
        add_task(task): Register a new async task.
        add_external_task(external_task_id): Register an external async task.
        get_lane_count(): Get the number of lanes for execution.
        should_propagate_lane_assignment(): Determine lane propagation behavior.
        get_task(task_id): Retrieve a registered task by ID.
        set_dlq_task_id(task_id): Set the DLQ task ID.
        get_dlq_task(): Retrieve the DLQ task.
        generate_sam_template(module, config_dict, stage): Generate AWS SAM template for deployment.
        set_current_task_id(task_id): Set the current task ID.
        set_current_lane(lane): Set the current lane index.
        get_current_lane(): Get the current lane index.
        set_current_invocation_id(invocation_id): Set the current invocation ID.
        handle_invocation(event, context, task_id): Direct invocation to the appropriate task executor.
        send_async_invoke_payload(...): Asynchronously invoke a task via SQS.
        send_async_invoke_payload_batch(...): Asynchronously invoke a batch of tasks via SQS.
        new_payload(payload, destination_task_id, force_sync): Prepare a payload for async invocation.
        add_controller(controller): Compose another controller as a child.
        async_invoke(task_id, payload, ...): Invoke an async task.
        async_invoke_batch(task_id, payloads, ...): Invoke a batch of async tasks.
        async_lambda_handler(event, context): Lambda handler entrypoint.
        async_task(...): Decorator to register a managed SQS async task.
        async_batch_task(...): Decorator to register a managed SQS batch async task.
        sqs_task(...): Decorator to register an unmanaged SQS task.
        scheduled_task(...): Decorator to register a scheduled task.
        api_task(...): Decorator to register an API Gateway task.
        dynamodb_task(...): Decorator to register a DynamoDB stream task.
        pure_task(...): Decorator to register a pure Lambda task.
    """

    is_sub: bool
    lane_count: Optional[int] = None
    propagate_lane_assignment: Optional[bool] = None
    propagate_message_group_id: Optional[bool] = None
    tasks: Dict[str, AsyncLambdaTask]
    external_async_tasks: Set[str]
    current_task_id: Optional[str] = None
    current_lane: Optional[int] = None
    current_invocation_id: Optional[str] = None
    _current_event_context: Optional[Any] = None
    _current_message_group_id: Optional[str] = None
    parent_controller: Optional["AsyncLambdaController"] = None
    middleware: List[MiddlewareRegistration]
    delete_s3_payloads: bool = False
    controller_name: Optional[str] = None

    dlq_task_id: Optional[str] = None

    def __init__(
        self,
        is_sub: bool = False,
        lane_count: Optional[int] = None,
        propagate_lane_assignment: Optional[bool] = None,
        propagate_message_group_id: Optional[bool] = None,
        middleware: Optional[List[MiddlewareRegistration]] = None,
        delete_s3_payloads: bool = False,
        controller_name: Optional[str] = None,
    ):
        """
        Initializes the controller with optional configuration parameters.

        Args:
            is_sub (bool, optional): Indicates if the controller is a sub-controller. Defaults to False.
            lane_count (Optional[int], optional): Number of lanes for task processing. Defaults to None.
            propagate_lane_assignment (Optional[bool], optional): Whether to propagate lane assignment to tasks. Defaults to None.
            middleware (Optional[List[MiddlewareRegistration]], optional): List of middleware registrations to apply. Defaults to None.
            delete_s3_payloads (bool, optional): Whether to delete S3 payloads after processing. Defaults to False.
            controller_name (Optional[str], optional): Name of the controller instance. Defaults to None.
        """
        self.tasks = dict()
        self.external_async_tasks = set()
        self.is_sub = is_sub
        self.lane_count = lane_count
        self.propagate_lane_assignment = propagate_lane_assignment
        self.propagate_message_group_id = propagate_message_group_id
        self.middleware = middleware or list()
        self.delete_s3_payloads = delete_s3_payloads
        self.controller_name = controller_name

    # itertools.batched is much cleaner but only available in python 3.12+
    @staticmethod
    def _batched(items: Sequence[dict], batch_size: int) -> List[List[dict]]:
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0")
        return [
            list(items[i : i + batch_size]) for i in range(0, len(items), batch_size)
        ]

    @classmethod
    def _build_send_to_all_async_lambda_queues_policies(
        cls,
        managed_tasks_resources: List[dict],
        policy_batch_size: int = 30,
    ) -> Dict[str, dict]:
        task_ref_policies: Dict[str, dict] = {}
        for chunk_index, resource_chunk in enumerate(
            cls._batched(items=managed_tasks_resources, batch_size=policy_batch_size),
            start=0,
        ):
            policy_id = f"SendToAllAsyncLambdaQueuesPolicy{chunk_index}"
            task_ref_policies[policy_id] = {
                "Type": "AWS::IAM::ManagedPolicy",
                "Properties": {
                    "ManagedPolicyName": {
                        "Fn::Sub": f"${{AWS::StackName}}-send-to-all-queues-{chunk_index}"
                    },
                    "PolicyDocument": {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Sid": "SendToAllQueues",
                                "Effect": "Allow",
                                "Action": ["sqs:SendMessage"],
                                "Resource": resource_chunk,
                            },
                        ],
                    },
                },
            }
        return task_ref_policies

    def add_middleware(
        self, event_types: List[Type[BaseEvent]], func: MiddlewareFunction[MET, RT]
    ):
        """
        Adds a middleware function to be executed for specified event types.

        Args:
            event_types (List[Type[BaseEvent]]): Event types the middleware should handle.
            func (MiddlewareFunction[MET, RT]): Middleware function to add.
        """
        self.middleware.append((event_types, func))

    def get_middleware_for_event(self, event: MET) -> List[MiddlewareFunction[MET, RT]]:
        """
        Retrieves a list of middleware functions applicable to the given event.

        This method checks if the current controller has a parent controller and, if so,
        includes middleware functions from the parent. It then iterates through the
        middleware registered in the current controller, appending functions whose
        associated event types match the type of the provided event.

        Args:
            event (MET): The event instance for which middleware functions are to be retrieved.

        Returns:
            List[MiddlewareFunction[MET, RT]]: A list of middleware functions that should be applied to the event.
        """
        if self.parent_controller is not None:
            _middleware_functions = self.parent_controller.get_middleware_for_event(
                event
            )
        else:
            _middleware_functions = list()

        for event_types, func in self.middleware:
            if any(isinstance(event, event_type) for event_type in event_types):
                _middleware_functions.append(func)

        return _middleware_functions

    def add_task(self, task: AsyncLambdaTask):
        """
        Adds an async task to the controller.

        Args:
            task (AsyncLambdaTask): The async task to add.

        Raises:
            Exception: If a task with the same task_id already exists.
        """
        if task.task_id in self.tasks:
            raise Exception(
                f"A task with the task_id {task.task_id} already exists. DUPLICATE TASK IDS"
            )
        self.tasks[task.task_id] = task

    def add_external_task(self, external_task_id: str):
        """
        Adds an external async task to the controller, enabling async invocation.

        Args:
            external_task_id (str): External task identifier (usually `{config.name}-{task_id}`).

        Note:
            Sending payloads via S3 is not supported for external tasks.
        """
        self.external_async_tasks.add(external_task_id)

    def get_lane_count(self) -> int:
        """
        Returns the number of lanes for the current controller.

        If the lane count is explicitly set for this controller, returns that value.
        Otherwise, if a parent controller exists, delegates the call to the parent controller.
        If neither is set, defaults to 1.

        Returns:
            int: The number of lanes.
        """
        if self.lane_count is not None:
            return self.lane_count

        if self.parent_controller is not None:
            return self.parent_controller.get_lane_count()
        return 1

    def should_propagate_lane_assignment(self) -> bool:
        """
        Determines whether lane assignment should be propagated.

        Returns:
            bool: True if lane assignment should be propagated, otherwise False.
                - If `self.propagate_lane_assignment` is set, its value is returned.
                - If not set and a parent controller exists, delegates the decision to the parent controller.
                - Defaults to True if neither condition is met.
        """
        if self.propagate_lane_assignment is not None:
            return self.propagate_lane_assignment
        if self.parent_controller is not None:
            return self.parent_controller.should_propagate_lane_assignment()
        return True

    def should_propagate_message_group_id(self) -> bool:
        """
        Determines whether the message group ID should be propagated.

        Returns:
            bool: True if the message group ID should be propagated, otherwise False.
                - If `self.propagate_message_group_id` is set, its value is returned.
                - If not set and a parent controller exists, the parent's value is used.
                - Defaults to True if neither is set.
        """
        if self.propagate_message_group_id is not None:
            return self.propagate_message_group_id
        if self.parent_controller is not None:
            return self.parent_controller.should_propagate_message_group_id()
        return True

    def get_task(self, task_id: str) -> Optional[AsyncLambdaTask]:
        """
        Retrieve a task by task_id from this or any parent controllers.
        """
        if task_id in self.tasks:
            return self.tasks[task_id]
        if self.parent_controller is not None:
            return self.parent_controller.get_task(task_id)
        return None

    def set_dlq_task_id(self, task_id: str) -> None:
        """
        Sets the Dead Letter Queue (DLQ) task ID for the controller.

        Args:
            task_id (str): The ID of the task to be set as the DLQ task.

        Raises:
            Exception: If no task with the given task_id exists.
            Exception: If the task's trigger type is not MANAGED_SQS (i.e., not an async-task).
        """
        self.dlq_task_id = task_id
        dlq_task = self.get_task(task_id)
        if dlq_task is None:
            raise Exception(
                f"Error setting DLQ Task ID: No task with the task_id {task_id} exists."
            )
        if dlq_task.trigger_type != TaskTriggerType.MANAGED_SQS:
            raise Exception(
                f"Error setting DLQ Task ID: Task {task_id} is not an async-task."
            )

    def get_dlq_task(self) -> Optional[AsyncLambdaTask]:
        """
        Retrieves the Dead Letter Queue (DLQ) task associated with this controller.

        If the current controller has a DLQ task ID, returns the corresponding AsyncLambdaTask.
        Otherwise, if a parent controller exists, recursively attempts to retrieve the DLQ task from the parent.
        Returns None if no DLQ task is found.

        Returns:
            Optional[AsyncLambdaTask]: The DLQ task if available, otherwise None.
        """
        if self.dlq_task_id is not None:
            return self.get_task(self.dlq_task_id)
        if self.parent_controller is not None:
            return self.parent_controller.get_dlq_task()
        return None

    def generate_sam_template(
        self,
        module: str,
        config_dict: dict,
        stage: Optional[str] = None,
    ) -> dict:
        """
        Generates the SAM Template for this project.
        """
        build_config = get_build_config_for_stage(config_dict, stage)
        s3_bucket_properties = {}
        if config.s3_payload_retention:
            s3_bucket_properties["LifecycleConfiguration"] = {
                "Rules": [
                    {
                        "Id": f"Auto delete objects after {config.s3_payload_retention} days.",
                        "ExpirationInDays": config.s3_payload_retention,
                        "Status": "Enabled",
                    }
                ]
            }

        template = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Transform": "AWS::Serverless-2016-10-31",
            "Globals": {
                "Function": {
                    "Tags": build_config.tags,
                    "Handler": f"{module}.lambda_handler",
                    "Runtime": config.runtime,
                    "Environment": {
                        "Variables": {
                            "ASYNC_LAMBDA_PAYLOAD_S3_BUCKET": {
                                "Ref": "AsyncLambdaPayloadBucket"
                            },
                            "ASYNC_LAMBDA_ACCOUNT_ID": {"Ref": "AWS::AccountId"},
                            **build_config.environment_variables,
                        },
                    },
                    "MemorySize": config.default_task_memory,
                    "EphemeralStorage": {"Size": config.default_task_ephemeral_storage},
                    **build_config.function_properties,
                }
            },
            "Resources": {
                "AsyncLambdaPayloadBucket": {
                    "Type": "AWS::S3::Bucket",
                    "Properties": {
                        "Tags": make_cf_tags(build_config.tags),
                        **s3_bucket_properties,
                    },
                },
                "AsyncLambdaDLQ": {
                    "Type": "AWS::SQS::Queue",
                    "Properties": {
                        "MessageRetentionPeriod": 1_209_600,  # 14 days
                        "Tags": make_cf_tags(
                            {
                                **build_config.tags,
                                "async-lambda-queue-type": "dlq",
                            }
                        ),
                    },
                },
            },
        }
        _task_list = list(self.tasks.values())
        managed_tasks_resources = [
            resource
            for task in _task_list
            if task.trigger_type in MANAGED_SQS_TASK_TYPES
            for resource in task.get_policy_sqs_resources()
        ] + [
            resource
            for external_async_task_id in self.external_async_tasks
            for resource in AsyncLambdaTask.get_policy_external_task_resources(
                external_async_task_id
            )
        ]
        task_ref_policies = {}
        if len(managed_tasks_resources) > 0:
            task_ref_policies = self._build_send_to_all_async_lambda_queues_policies(
                managed_tasks_resources
            )
            for key in task_ref_policies.keys():
                template["Resources"][key] = task_ref_policies[key]

        has_api_tasks = False
        for task in _task_list:
            if task.trigger_type == TaskTriggerType.API_EVENT:
                has_api_tasks = True
            for logical_id, resource in task.get_sam_template(
                task_ref_policy_ids=list(task_ref_policies.keys()),
                config_dict=config_dict,
                stage=stage,
            ).items():
                template["Resources"][logical_id] = resource

        for extra_index, extra in enumerate(build_config.managed_queue_extras):
            template["Resources"][self._dlq_extra_logical_id(extra_index)] = (
                self._dlq_extras_replace_references(extra)
            )

        if has_api_tasks:
            properties: dict = {
                "StageName": "prod",
                "PropagateTags": True,
                "Tags": build_config.tags,
            }
            if len(build_config.method_settings) > 0:
                properties["MethodSettings"] = build_config.method_settings
            if build_config.domain_name is not None:
                domain_dict: dict = {
                    "DomainName": build_config.domain_name,
                }
                properties["Domain"] = domain_dict
                if build_config.certificate_arn is not None:
                    properties["Domain"]["CertificateArn"] = (
                        build_config.certificate_arn
                    )
                    if build_config.tls_version is not None:
                        properties["Domain"]["SecurityPolicy"] = (
                            build_config.tls_version
                        )
                elif (
                    build_config.auto_create_acm_certificate is True
                    and build_config.hosted_zone_id is not None
                ):
                    template["Resources"]["AsyncLambdaAPICertificate"] = {
                        "Type": "AWS::CertificateManager::Certificate",
                        "Properties": {
                            "DomainName": build_config.domain_name,
                            "ValidationMethod": "DNS",
                            "DomainValidationOptions": [
                                {
                                    "DomainName": build_config.domain_name,
                                    "HostedZoneId": build_config.hosted_zone_id,
                                }
                            ],
                        },
                    }
                    properties["Domain"]["CertificateArn"] = {
                        "Ref": "AsyncLambdaAPICertificate"
                    }
                    if build_config.tls_version is not None:
                        properties["Domain"]["SecurityPolicy"] = (
                            build_config.tls_version
                        )
                if build_config.hosted_zone_id is not None:
                    properties["Domain"]["Route53"] = {
                        "HostedZoneId": build_config.hosted_zone_id
                    }

            template["Resources"]["AsyncLambdaAPIGateway"] = {
                "Type": "AWS::Serverless::Api",
                "Properties": properties,
            }
        return template

    def _dlq_extra_logical_id(self, index: int):
        """
        Generates a logical ID string for an extra Dead Letter Queue (DLQ) resource.

        Args:
            index (int): The index to differentiate multiple DLQ resources.

        Returns:
            str: A formatted logical ID string for the DLQ resource.
        """
        return f"AsyncLambdaDLQExtra{index}"

    def _dlq_extras_replace_references(self, extra: dict) -> dict:
        """
        Replaces placeholder references in the given 'extra' dictionary with actual values.

        This method serializes the input dictionary to a JSON string, then:
          - Replaces occurrences of "$EXTRA{index}" with the logical ID generated by _dlq_extra_logical_id for the given index.
          - Replaces all occurrences of "$QUEUEID" with "AsyncLambdaDLQ".
        The modified string is then deserialized back into a dictionary.

        Args:
            extra (dict): The dictionary containing placeholder references to be replaced.

        Returns:
            dict: The dictionary with all placeholder references replaced by their actual values.
        """
        stringified_extra = json.dumps(extra)
        stringified_extra = re.sub(
            r"\$EXTRA(?P<index>[0-9]+)",
            lambda m: self._dlq_extra_logical_id(int(m.group("index"))),
            stringified_extra,
        )
        stringified_extra = stringified_extra.replace("$QUEUEID", "AsyncLambdaDLQ")

        return json.loads(stringified_extra)

    def set_current_task_id(self, task_id: Optional[str] = None):
        """
        Set the current_task_id
        """
        if self.parent_controller is not None:
            self.parent_controller.set_current_task_id(task_id)
        self.current_task_id = task_id

    def set_current_lane(self, lane: int):
        """
        Set the current lane
        """
        if self.parent_controller is not None:
            self.parent_controller.set_current_lane(lane)
        self.current_lane = lane

    def get_current_lane(self) -> int:
        """
        Returns the current lane number.

        If a parent controller exists, delegates the call to its `get_current_lane` method.
        If `current_lane` is not set, returns 0 as the default lane.
        Otherwise, returns the value of `current_lane`.

        Returns:
            int: The current lane number.
        """
        if self.parent_controller is not None:
            return self.parent_controller.get_current_lane()
        if self.current_lane is None:
            return 0
        return self.current_lane

    def set_current_invocation_id(self, invocation_id: str):
        """
        Set the current_invocation_id
        """
        if self.parent_controller is not None:
            self.parent_controller.set_current_invocation_id(invocation_id)
        self.current_invocation_id = invocation_id

    def set_current_event_context(self, context: Any):
        """
        Set the current event context on the parent controller.
        """
        if self.parent_controller is not None:
            self.parent_controller.set_current_event_context(context)
            return
        self._current_event_context = context

    def get_current_event_context(self) -> Any:
        """
        Get the current event context
        """
        if self.parent_controller is not None:
            return self.parent_controller.get_current_event_context()
        return self._current_event_context

    def set_current_message_group_id(self, message_group_id: Optional[str]):
        """
        Sets the current message group ID for the controller.

        If a parent controller exists, delegates the operation to the parent controller.
        Otherwise, sets the message group ID for the current controller instance.

        Args:
            message_group_id (str): The ID of the message group to set as current.
        """
        if self.parent_controller is not None:
            self.parent_controller.set_current_message_group_id(message_group_id)
            return
        self._current_message_group_id = message_group_id

    def get_current_message_group_id(self) -> Optional[str]:
        """
        Retrieves the current message group ID.

        If a parent controller exists, delegates the retrieval to the parent controller.
        Otherwise, returns the current message group ID stored in this controller.

        Returns:
            Optional[str]: The current message group ID, or None if not set.
        """
        if self.parent_controller is not None:
            return self.parent_controller.get_current_message_group_id()
        return self._current_message_group_id

    def handle_invocation(self, event, context, task_id: Optional[str] = None):
        """
        Handles the invocation of a task based on its trigger type.

        This method determines the appropriate event wrapper and execution lane for the given task,
        then executes the task with the constructed event. It supports various trigger types, including
        managed and unmanaged SQS, scheduled events, API events, DynamoDB events, and base events.

        Args:
            event: The event payload received by the Lambda function.
            context: The Lambda context object.
            task_id (Optional[str]): The identifier of the task to invoke. If not provided, it is
                retrieved from the environment.

        Returns:
            The result of the task execution, which may be a custom response for API events.

        Raises:
            NotImplementedError: If the task's trigger type is not supported.
        """

        self.current_lane = None
        if task_id is None:
            task_id = env.get_current_task_id()
        task = self.tasks[task_id]

        args = (event, context, task)

        self.set_current_event_context(context)

        if task.trigger_type == TaskTriggerType.MANAGED_SQS:
            _event = ManagedSQSEvent(*args)
            lane_count = task.get_lane_count()
            if lane_count == 1:
                self.set_current_lane(lane=0)
            else:
                for lane_index in range(lane_count):
                    if _event.event_source_arn == task.get_managed_queue_arn(
                        lane=lane_index
                    ):
                        self.set_current_lane(lane=lane_index)
                        break
            self.set_current_invocation_id(_event.invocation_id)
            self.set_current_message_group_id(_event.message_group_id)
        elif task.trigger_type == TaskTriggerType.MANAGED_SQS_BATCH:
            _event = ManagedSQSBatchEvent(*args)
            lane_count = task.get_lane_count()
            if lane_count == 1:
                self.set_current_lane(lane=0)
            else:
                assert all(
                    event.event_source_arn == _event.events[0].event_source_arn
                    for event in _event.events
                )
                for lane_index in range(lane_count):
                    if _event.events[0].event_source_arn == task.get_managed_queue_arn(
                        lane=lane_index
                    ):
                        self.set_current_lane(lane=lane_index)
                        break
        elif task.trigger_type == TaskTriggerType.UNMANAGED_SQS:
            _event = UnmanagedSQSEvent(*args)
        elif task.trigger_type == TaskTriggerType.SCHEDULED_EVENT:
            _event = ScheduledEvent(*args)
        elif task.trigger_type == TaskTriggerType.API_EVENT:
            _event = APIEvent(*args)
        elif task.trigger_type == TaskTriggerType.DYNAMODB_EVENT:
            _event = DynamoDBEvent(*args)
        elif task.trigger_type == TaskTriggerType.BASE_EVENT:
            _event = BaseEvent(*args)
        else:
            raise NotImplementedError(
                f"Trigger type of {task.trigger_type} is not supported."
            )
        response = task.execute(_event)

        if task.trigger_type == TaskTriggerType.API_EVENT and hasattr(
            response, "__async_lambda_response__"
        ):
            response = response.__async_lambda_response__()
        if (
            isinstance(_event, ManagedSQSEvent)
            and _event.s3_payload_key is not None
            and self.delete_s3_payloads
        ):
            get_s3_client().delete_object(
                Bucket=env.get_payload_bucket(), Key=_event.s3_payload_key
            )
        return response

    def send_async_invoke_payload(
        self,
        destination_task_id: str,
        sqs_payload: dict,
        delay: int = 0,
        force_sync: bool = False,
        lane: Optional[int] = None,
        message_group_id: Optional[str] = None,
    ):
        """
        Sends an asynchronous invocation payload to a managed or external task via SQS.

        If a parent controller exists, delegates the invocation to the parent. Validates the
        destination task and lane, and determines whether to invoke synchronously (locally)
        or asynchronously (via SQS). Handles both managed and external tasks, enforcing lane
        constraints and supporting optional invocation delay.

        Args:
            destination_task_id (str): The ID of the task to invoke.
            sqs_payload (dict): The payload to send to the task.
            delay (int, optional): Delay in seconds before sending the message. Defaults to 0.
            force_sync (bool, optional): If True, invokes the task synchronously. Defaults to False.
            lane (Optional[int], optional): The lane to use for invocation. If None, lane assignment is determined automatically.

        Returns:
            Any: The result of the synchronous invocation if `force_sync` is True; otherwise, None.

        Raises:
            Exception: If the destination task does not exist, is not a managed SQS task, or the lane is invalid.
            NotImplementedError: If attempting to run an external task synchronously.
        """
        if self.parent_controller is not None:
            return self.parent_controller.send_async_invoke_payload(
                destination_task_id=destination_task_id,
                sqs_payload=sqs_payload,
                delay=delay,
                force_sync=force_sync,
                lane=lane,
                message_group_id=message_group_id,
            )
        is_external_task = False
        if destination_task_id not in self.tasks:
            if destination_task_id in self.external_async_tasks:
                is_external_task = True
            else:
                raise Exception(
                    f"No such task exists with the task_id {destination_task_id}"
                )
        destination_task = None
        if not is_external_task:
            destination_task = self.tasks[destination_task_id]
            if destination_task.trigger_type not in MANAGED_SQS_TASK_TYPES:
                raise Exception(
                    f"Unable to invoke task '{destination_task_id}' because it is a {destination_task.trigger_type} task"
                )

            if lane is None and destination_task.should_propagate_lane_assignment():
                lane = self.get_current_lane()
            if lane is None:
                lane = 0

            if lane < 0 or lane >= destination_task.get_lane_count():
                raise Exception(
                    f"Unable to invoke task {destination_task_id} in lane {lane} because it is not a valid lane for the task."
                )
        else:
            if lane is None:
                lane = self.get_current_lane()
            if lane != 0:
                logger.warning(
                    f"Selected lane is {lane}. External tasks only support lane 0."
                )
            lane = 0

        _message_group_id = message_group_id
        if (
            message_group_id is None
            and (current_message_group_id := self.get_current_message_group_id())
            is not None
            and self.should_propagate_message_group_id()
        ):
            _message_group_id = current_message_group_id

        if force_sync or env.get_force_sync_mode():
            assert destination_task is not None
            if is_external_task:
                raise NotImplementedError(
                    f"Unable to run external task {destination_task_id} locally."
                )
            if delay:
                time.sleep(delay)
            # Sync invocation with mock event/context
            current_task_id = self.current_task_id
            current_lane = self.get_current_lane()
            current_context = self.get_current_event_context()
            current_message_group_id = self.get_current_message_group_id()
            queue_arn = destination_task.get_managed_queue_arn(lane=lane)
            mock_event = MockSQSLambdaEvent(
                json.dumps(sqs_payload),
                source_queue_arn=queue_arn,
                message_group_id=_message_group_id,
            )
            mock_context = MockLambdaContext(destination_task.task_id)
            result = self.handle_invocation(
                mock_event, mock_context, task_id=destination_task_id
            )
            self.set_current_task_id(current_task_id)
            self.set_current_lane(current_lane)
            self.set_current_event_context(current_context)
            self.set_current_message_group_id(current_message_group_id)
            return result
        else:
            if is_external_task:
                url = f"https://sqs.{env.get_aws_region()}.amazonaws.com/{env.get_aws_account_id()}/{destination_task_id}"
            else:
                assert destination_task is not None
                url = destination_task.get_managed_queue_url(lane=lane)

            _kwargs = {}
            if _message_group_id:
                _kwargs["MessageGroupId"] = _message_group_id

            get_sqs_client().send_message(
                QueueUrl=url,
                MessageBody=json.dumps(sqs_payload),
                DelaySeconds=delay,
                **_kwargs,
            )

    def send_async_invoke_payload_batch(
        self,
        destination_task_id: str,
        sqs_payloads: Sequence[dict],
        delay: Union[int, Sequence[int]] = 0,
        message_group_id: Union[Optional[str], Sequence[Optional[str]]] = None,
        force_sync: bool = False,
        lane: Optional[int] = None,
        index: int = 0,
    ):
        """
        Sends a batch of payloads for asynchronous invocation to a specified task via SQS.

        If a parent controller exists, delegates the invocation to the parent. Handles both internal and external tasks,
        validating the destination and lane assignment. Supports synchronous invocation for testing or local execution.

        Args:
            destination_task_id (str): The ID of the task to invoke.
            sqs_payloads (Sequence[dict]): A sequence of payloads to send.
            delay (Union[int, Sequence[int]], optional): Delay in seconds before sending each message. Can be a single int or a sequence of ints. Defaults to 0.
            force_sync (bool, optional): If True, invokes the task synchronously (for local testing). Defaults to False.
            lane (Optional[int], optional): The lane to use for invocation. If None, lane assignment is determined automatically. Defaults to None.
            index (int, optional): Starting index for message IDs in the batch. Defaults to 0.

        Raises:
            Exception: If the destination task does not exist or is not a managed SQS task.
            NotImplementedError: If attempting to run an external task synchronously.
            BatchInvokeException: If one or more messages fail to send after retries.

        Returns:
            None
        """
        if self.parent_controller is not None:
            return self.parent_controller.send_async_invoke_payload_batch(
                destination_task_id=destination_task_id,
                sqs_payloads=sqs_payloads,
                delay=delay,
                force_sync=force_sync,
                lane=lane,
            )

        is_external_task = False
        if destination_task_id not in self.tasks:
            if destination_task_id in self.external_async_tasks:
                is_external_task = True
            else:
                raise Exception(
                    f"No such task exists with the task_id {destination_task_id}"
                )
        destination_task = None
        if not is_external_task:
            destination_task = self.tasks[destination_task_id]
            if destination_task.trigger_type not in MANAGED_SQS_TASK_TYPES:
                raise Exception(
                    f"Unable to invoke task '{destination_task_id}' because it is a {destination_task.trigger_type} task"
                )

            if lane is None and destination_task.should_propagate_lane_assignment():
                lane = self.get_current_lane()
            if lane is None:
                lane = 0

            if lane < 0 or lane >= destination_task.get_lane_count():
                raise Exception(
                    f"Unable to invoke task {destination_task_id} in lane {lane} because it is not a valid lane for the task."
                )
        else:
            if lane is None:
                lane = self.get_current_lane()
            if lane != 0:
                logger.warning(
                    f"Selected lane is {lane}. External tasks only support lane 0."
                )
            lane = 0

        if force_sync or env.get_force_sync_mode():
            if is_external_task:
                raise NotImplementedError(
                    f"Unable to run external task {destination_task_id} locally."
                )
            # Sync invocation with mock event/context
            current_task_id = self.current_task_id
            current_lane = self.get_current_lane()
            assert destination_task is not None
            queue_arn = destination_task.get_managed_queue_arn(lane=lane)
            for i, sqs_payload in enumerate(sqs_payloads):
                if delay:
                    if isinstance(delay, Sequence):
                        time.sleep(delay[i])
                    else:
                        time.sleep(delay)

                _message_group_id = (
                    message_group_id[i]
                    if isinstance(message_group_id, Sequence)
                    and not isinstance(message_group_id, str)
                    else message_group_id
                )
                if (
                    _message_group_id is None
                    and (
                        current_message_group_id := self.get_current_message_group_id()
                    )
                    is not None
                    and self.should_propagate_message_group_id()
                ):
                    _message_group_id = current_message_group_id

                current_message_group_id = self.get_current_message_group_id()
                mock_event = MockSQSLambdaEvent(
                    json.dumps(sqs_payload),
                    source_queue_arn=queue_arn,
                    message_group_id=_message_group_id,
                )
                mock_context = MockLambdaContext(destination_task.task_id)
                self.handle_invocation(
                    mock_event, mock_context, task_id=destination_task_id
                )
                self.set_current_lane(current_lane)
                self.set_current_task_id(current_task_id)
                self.set_current_message_group_id(current_message_group_id)
        else:
            entries: List[dict] = []
            for i, sqs_payload in enumerate(sqs_payloads):
                if isinstance(delay, Sequence):
                    _delay = delay[i]
                else:
                    _delay = delay

                _message_group_id = (
                    message_group_id[i]
                    if isinstance(message_group_id, Sequence)
                    and not isinstance(message_group_id, str)
                    else message_group_id
                )
                if (
                    _message_group_id is None
                    and (
                        current_message_group_id := self.get_current_message_group_id()
                    )
                    is not None
                    and self.should_propagate_message_group_id()
                ):
                    _message_group_id = current_message_group_id

                entry = {
                    "MessageBody": json.dumps(sqs_payload),
                    "DelaySeconds": _delay,
                    "Id": f"index_{index + i}",
                }
                if _message_group_id:
                    entry["MessageGroupId"] = _message_group_id
                entries.append(entry)
            if is_external_task:
                url = f"https://sqs.{env.get_aws_region()}.amazonaws.com/{env.get_aws_account_id()}/{destination_task_id}"
            else:
                assert destination_task is not None
                url = destination_task.get_managed_queue_url(lane=lane)
            failed_messages = []
            batch_retry_count = env.get_batch_failure_retry_count() + 1
            for i in range(batch_retry_count):
                response = get_sqs_client().send_message_batch(
                    QueueUrl=url,
                    Entries=entries,
                )
                failed_messages: List[dict] = response.get("Failed", [])
                if len(failed_messages) == 0:
                    return
                logger.warning(failed_messages)
                logger.warning(f"{len(failed_messages)} messages failed to send. ")
                failed_message_ids = {message["Id"] for message in failed_messages}
                entries = [
                    entry for entry in entries if entry["Id"] in failed_message_ids
                ]
                if i < batch_retry_count:
                    send_delay = 0.5 + random.random()
                    logger.info(
                        f"Waiting {send_delay:.3f} before attempting batch failures again."
                    )
                    time.sleep(send_delay)
            logger.error(failed_messages)
            raise BatchInvokeException(
                f"Failed to send {len(failed_messages)} messages.",
                failed_payloads=[int(entry["Id"].split("_")[-1]) for entry in entries],
            )

    def new_payload(
        self,
        payload: Any,
        destination_task_id: str,
        force_sync: bool,
    ) -> dict:
        """
        Constructs a new payload dictionary for task invocation, handling serialization and storage based on payload size and task type.

        If a parent controller exists, delegates payload creation to it. Otherwise, generates a new invocation ID if necessary and builds the payload metadata.

        For payloads smaller than the SQS size limit, serializes and embeds the payload directly. For larger payloads, stores the payload in S3 and includes a reference key, unless the destination is an external task (which is not supported for S3 payloads).

        Args:
            payload (Any): The data to be sent to the destination task.
            destination_task_id (str): The identifier of the destination task.
            force_sync (bool): If True, forces synchronous payload delivery regardless of size.

        Returns:
            dict: The constructed payload dictionary containing metadata and either the serialized payload or an S3 reference key.

        Raises:
            NotImplementedError: If the payload is too large for SQS and the destination is an external task.
        """
        if self.parent_controller is not None:
            return self.parent_controller.new_payload(
                payload=payload,
                destination_task_id=destination_task_id,
                force_sync=force_sync,
            )
        if self.current_invocation_id is None:
            invocation_id = str(uuid4())
        else:
            invocation_id = self.current_invocation_id
        raw_sqs_body = {
            "source_task_id": self.current_task_id,
            "destination_task_id": destination_task_id,
            "invocation_id": invocation_id,
        }
        is_external_task = False
        if (
            self.get_task(destination_task_id) is None
            and destination_task_id in self.external_async_tasks
        ):
            is_external_task = True
            raw_sqs_body["source_app"] = config.name

        serialized_payload = json.dumps(payload, cls=PayloadEncoder)
        payload_size = len(serialized_payload.encode())
        if payload_size < 250_000:  # we need to double encode to be sure
            payload_size = len(json.dumps(serialized_payload).encode())

        if force_sync or env.get_force_sync_mode():
            raw_sqs_body["payload"] = serialized_payload
        elif payload_size >= 250_000:  # payload is bigger than max SQS size
            if is_external_task:
                raise NotImplementedError(
                    "Payload is too large for SQS and S3 payloads are not supported with external invocations"
                )
            date_part = datetime.now(tz=timezone.utc).strftime("%Y/%m/%d")
            key = f"{date_part}/{uuid4().hex}.json"
            logger.info(f"Utilizing S3 Payload because of payload size. Key: {key}")
            raw_sqs_body["s3_payload_key"] = key
            get_s3_client().put_object(
                Bucket=env.get_payload_bucket(), Key=key, Body=serialized_payload
            )
        else:
            raw_sqs_body["payload"] = serialized_payload

        return raw_sqs_body

    def add_controller(self, controller: "AsyncLambdaController"):
        """
        Adds an AsyncLambdaController as a child to the current controller.

        This method sets the parent_controller of the provided controller to self,
        adds all tasks from the child controller to the current controller, and
        merges the external asynchronous tasks.

        Args:
            controller (AsyncLambdaController): The controller to be added as a child.
        """
        controller.parent_controller = self
        for task in controller.tasks.values():
            self.add_task(task)

        for task_id in controller.external_async_tasks:
            self.external_async_tasks.add(task_id)

    def async_invoke(
        self,
        task_id: str,
        payload: Any,
        delay: int = 0,
        force_sync: bool = False,
        lane: Optional[int] = None,
        message_group_id: Optional[str] = None,
    ):
        """
        Asynchronously invokes a task by sending a payload to the specified destination.

        If the invocation happens synchronously then the return value for the task function will be returned.
        This behavior will not happen during asynchronous cloud based invocations and even the
        synchronous implementation should not be considered stable.

        Args:
            task_id (str): The identifier of the task to invoke.
            payload (Any): The data to send to the task.
            delay (int, optional): Delay in seconds before invoking the task. Defaults to 0.
            force_sync (bool, optional): If True, forces synchronous invocation. Defaults to False.
            lane (Optional[int], optional): Optional lane identifier for routing. Defaults to None.

        Returns:
            Any: The result of sending the asynchronous invocation payload.
        """

        sqs_payload = self.new_payload(
            payload=payload, destination_task_id=task_id, force_sync=force_sync
        )
        return self.send_async_invoke_payload(
            destination_task_id=task_id,
            sqs_payload=sqs_payload,
            delay=delay,
            force_sync=force_sync,
            lane=lane,
            message_group_id=message_group_id,
        )

    def async_invoke_batch(
        self,
        task_id: str,
        payloads: Sequence[Any],
        delay: Union[int, Sequence[int]] = 0,
        message_group_id: Union[Optional[str], Sequence[Optional[str]]] = None,
        force_sync: bool = False,
        lane: Optional[int] = None,
    ):
        """
        Invokes a batch of asynchronous tasks by sending payloads in groups of 10 to the specified task.

        Args:
            task_id (str): Identifier of the destination task to invoke.
            payloads (Sequence[Any]): A sequence of payloads to be sent for invocation.
            delay (Union[int, Sequence[int]], optional): Delay in seconds before invoking the tasks. Can be a single integer or a sequence of integers. Defaults to 0.
            force_sync (bool, optional): If True, forces synchronous invocation. Defaults to False.
            lane (Optional[int], optional): Optional lane identifier for invocation. Defaults to None.

        Returns:
            None
        """
        if len(payloads) == 0:
            return

        for i in range(0, len(payloads), 10):
            payloads_slice = payloads[i : i + 10]
            logger.info(f"Sending batch of {len(payloads_slice)} to task {task_id}.")
            sqs_payloads = [
                self.new_payload(
                    payload=payload, destination_task_id=task_id, force_sync=force_sync
                )
                for payload in payloads_slice
            ]
            self.send_async_invoke_payload_batch(
                destination_task_id=task_id,
                sqs_payloads=sqs_payloads,
                delay=delay,
                message_group_id=message_group_id,
                force_sync=force_sync,
                lane=lane,
                index=i,
            )

    def async_lambda_handler(self, event, context):
        """
        Handles the invocation of an asynchronous AWS Lambda function.
        This should be "exported" by the `app.py` file in your project.
        ```
        app = AsyncLambdaController()
        lambda_handler = app.async_lambda_handler
        ```

        Args:
            event (dict): The event data passed to the Lambda function.
            context (LambdaContext): The runtime information of the Lambda function.

        Returns:
            Any: The result of the invocation handled by `handle_invocation`.
        """

        return self.handle_invocation(event, context, task_id=None)

    def async_task(
        self,
        task_id: str,
        max_receive_count: int = 1,
        dlq_task_id: Optional[str] = None,
        is_dlq_task: bool = False,
        lane_count: Optional[int] = None,
        propagate_lane_assignment: Optional[bool] = None,
        timeout: int = 60,
        memory: Optional[int] = None,
        ephemeral_storage: Optional[int] = None,
        **kwargs,
    ):
        """
        Decorate a function to register it as an async task.
        Registered functions can be asynchronously invoked with `async_invoke` using their `task_id`.

        Args:
            task_id (str): Unique identifier for the async task.
            max_receive_count (int, optional): Maximum receives before moving to DLQ. Defaults to 1.
            dlq_task_id (Optional[str], optional): DLQ task ID. Defaults to None.
            is_dlq_task (bool, optional): Whether this is a DLQ task. Defaults to False.
            lane_count (Optional[int], optional): Number of parallel lanes. Defaults to None.
            propagate_lane_assignment (Optional[bool], optional): Propagate lane assignment. Defaults to None.
            timeout (int, optional): Lambda timeout (seconds). Defaults to 60.
            memory (Optional[int], optional): Lambda memory (MB). Defaults to None.
            ephemeral_storage (int, optional): Ephemeral storage (MB). Defaults to 512.
            **kwargs: Additional keyword arguments.

        Example:
            app = AsyncLambdaController()

            @app.async_task("my_async_task")
            def my_async_task_handler(event):
                print("Received event:", event)
                app.async_invoke("other_async_task", {"foo": "bar"})
                return

            @app.async_task("other_async_task")
            def other_async_task_handler(event):
                print("Other async task received:", event)
                return
        """
        logger.debug(f"Registering async task '{task_id}' with the controller.")

        def _task(func: Callable[[ManagedSQSEventT], Any]):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                self.set_current_task_id(task_id)
                return func(*args, **kwargs)

            self.add_task(
                AsyncLambdaTask(
                    controller=self,
                    executable=inner,
                    task_id=task_id,
                    trigger_type=TaskTriggerType.MANAGED_SQS,
                    trigger_config={
                        "max_receive_count": max_receive_count,
                        "dlq_task_id": dlq_task_id,
                        "is_dlq_task": is_dlq_task,
                        "lane_count": lane_count,
                        "propagate_lane_assignment": propagate_lane_assignment,
                        "batch_size": 1,
                    },
                    timeout=timeout,
                    memory=memory,
                    ephemeral_storage=ephemeral_storage,
                    **kwargs,
                )
            )
            return inner

        return _task

    def async_batch_task(
        self,
        task_id: str,
        max_receive_count: int = 1,
        dlq_task_id: Optional[str] = None,
        is_dlq_task: bool = False,
        lane_count: Optional[int] = None,
        propagate_lane_assignment: Optional[bool] = None,
        batch_size: int = 20,
        max_batching_window: Optional[int] = None,
        timeout: int = 60,
        memory: Optional[int] = None,
        ephemeral_storage: Optional[int] = None,
        **kwargs,
    ):
        """
        Decorate a function to register it as an async batch task.
        Registered functions can be asynchronously invoked with `async_invoke_batch` using their `task_id`.

        Args:
            task_id (str): Unique identifier for the async batch task.
            max_receive_count (int, optional): Maximum receives before moving to DLQ. Defaults to 1.
            dlq_task_id (Optional[str], optional): DLQ task ID. Defaults to None.
            is_dlq_task (bool, optional): Whether this is a DLQ task. Defaults to False.
            lane_count (Optional[int], optional): Number of parallel lanes. Defaults to None.
            propagate_lane_assignment (Optional[bool], optional): Propagate lane assignment. Defaults to None.
            batch_size (int, optional): Maximum records per batch. Defaults to 20.
            max_batching_window (Optional[int], optional): Maximum batching window (seconds). Defaults to None.
            timeout (int, optional): Lambda timeout (seconds). Defaults to 60.
            memory (Optional[int], optional): Lambda memory (MB). Defaults to None.
            ephemeral_storage (int, optional): Ephemeral storage (MB). Defaults to 512.
            **kwargs: Additional keyword arguments.

        Example:
            app = AsyncLambdaController()

            @app.async_batch_task("my_batch_task", batch_size=10)
            def my_batch_task_handler(event):
                for record in event.events:
                    print("Processing record:", record)
                return

            # To invoke batch:
            app.async_invoke_batch("my_batch_task", [{"foo": 1}, {"foo": 2}, {"foo": 3}])
        """
        logger.debug(f"Registering async batch task '{task_id}' with the controller.")

        def _task(func: Callable[[ManagedSQSBatchEventT], Any]):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                self.set_current_task_id(task_id)
                return func(*args, **kwargs)

            self.add_task(
                AsyncLambdaTask(
                    controller=self,
                    executable=inner,
                    task_id=task_id,
                    trigger_type=TaskTriggerType.MANAGED_SQS_BATCH,
                    trigger_config={
                        "max_receive_count": max_receive_count,
                        "dlq_task_id": dlq_task_id,
                        "is_dlq_task": is_dlq_task,
                        "lane_count": lane_count,
                        "propagate_lane_assignment": propagate_lane_assignment,
                        "batch_size": batch_size,
                        "max_batching_window": max_batching_window,
                    },
                    timeout=timeout,
                    memory=memory,
                    ephemeral_storage=ephemeral_storage,
                    **kwargs,
                )
            )
            return inner

        return _task

    def sqs_task(
        self,
        task_id: str,
        queue_arn: str,
        timeout: int = 60,
        memory: Optional[int] = None,
        ephemeral_storage: Optional[int] = None,
        **kwargs,
    ):
        """
        Decorate a function to register it as an unmanaged SQS task.
        Registered functions will be triggered by messages in the specified SQS queue.

        Args:
            task_id (str): Unique identifier for the SQS task.
            queue_arn (str): ARN of the SQS queue to listen to.
            timeout (int, optional): Lambda timeout (seconds). Defaults to 60.
            memory (Optional[int], optional): Lambda memory (MB). Defaults to None.
            ephemeral_storage (int, optional): Ephemeral storage (MB). Defaults to 512.
            **kwargs: Additional keyword arguments.

        Example:
            app = AsyncLambdaController()

            @app.sqs_task(
                task_id="my_unmanaged_sqs_task",
                queue_arn="arn:aws:sqs:us-east-1:123456789012:my-queue"
            )
            def my_unmanaged_sqs_handler(event):
                print("Received SQS event:", event)
                return
        """
        logger.debug(
            f"Registering sqs task '{task_id}' arn '{queue_arn}' with the controller."
        )

        def _task(func: Callable[[UnmanagedSQSEventT], Any]):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                self.set_current_task_id(task_id)
                return func(*args, **kwargs)

            self.add_task(
                AsyncLambdaTask(
                    controller=self,
                    executable=inner,
                    task_id=task_id,
                    trigger_type=TaskTriggerType.UNMANAGED_SQS,
                    trigger_config={"queue_arn": queue_arn},
                    timeout=timeout,
                    memory=memory,
                    ephemeral_storage=ephemeral_storage,
                    **kwargs,
                )
            )

            return inner

        return _task

    def scheduled_task(
        self,
        task_id: str,
        schedule_expression: str,
        timeout: int = 60,
        memory: Optional[int] = None,
        ephemeral_storage: Optional[int] = None,
        **kwargs,
    ):
        """
        Decorate a function to register it as a scheduled task.
        Registered functions will be triggered by the specified schedule expression.

        Args:
            task_id (str): Unique identifier for the scheduled task.
            schedule_expression (str): Schedule expression for triggering. See AWS docs for valid expressions.
            timeout (int, optional): Lambda timeout (seconds). Defaults to 60.
            memory (Optional[int], optional): Lambda memory (MB). Defaults to None.
            ephemeral_storage (int, optional): Ephemeral storage (MB). Defaults to 512.
            **kwargs: Additional keyword arguments.

        Example:
            app = AsyncLambdaController()

            @app.scheduled_task(
                task_id="my_scheduled_task",
                schedule_expression="rate(5 minutes)"
            )
            def my_scheduled_task_handler(event):
                print("Scheduled event triggered:", event)
                return
        """
        logger.debug(
            f"Registering scheduled task '{task_id}' with schedule '{schedule_expression}' with the controller."
        )

        def _task(func: Callable[[ScheduledEventT], Any]):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                self.set_current_task_id(task_id)
                return func(*args, **kwargs)

            self.add_task(
                AsyncLambdaTask(
                    controller=self,
                    executable=inner,
                    task_id=task_id,
                    trigger_type=TaskTriggerType.SCHEDULED_EVENT,
                    trigger_config={"schedule_expression": schedule_expression},
                    timeout=timeout,
                    memory=memory,
                    ephemeral_storage=ephemeral_storage,
                    **kwargs,
                )
            )

            return inner

        return _task

    def api_task(
        self,
        task_id: str,
        path: str,
        method: str,
        timeout: int = 60,
        memory: Optional[int] = None,
        ephemeral_storage: Optional[int] = None,
        **kwargs,
    ):
        """
        Decorate a function to register it as an API task.
        Registered functions will be triggered by API Gateway calls to the specified path and method.

        Args:
            task_id (str): Unique identifier for the API task.
            path (str): API Gateway path (e.g., "/users").
            method (str): HTTP method (e.g., "GET", "POST").
            timeout (int, optional): Lambda timeout (seconds). Defaults to 60.
            memory (Optional[int], optional): Lambda memory (MB). Defaults to None.
            ephemeral_storage (int, optional): Ephemeral storage (MB). Defaults to 512.
            **kwargs: Additional keyword arguments.

        Example:
            app = AsyncLambdaController()

            @app.api_task(
                task_id="get_user",
                path="/user",
                method="GET"
            )
            def get_user_handler(event):
                user_id = event.querystring_params["user_id"]
                return {"user_id": user_id, "name": "John Doe"}
        """
        logger.debug(
            f"Registering api task '{task_id}' with the path '{path}' and method '{method}' with the controller."
        )

        def _task(func: Callable[[APIEventT], Any]):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                self.set_current_task_id(task_id)
                return func(*args, **kwargs)

            self.add_task(
                AsyncLambdaTask(
                    controller=self,
                    executable=inner,
                    task_id=task_id,
                    trigger_type=TaskTriggerType.API_EVENT,
                    trigger_config={"path": path, "method": method},
                    timeout=timeout,
                    memory=memory,
                    ephemeral_storage=ephemeral_storage,
                    **kwargs,
                )
            )

            return inner

        return _task

    def dynamodb_task(
        self,
        task_id: str,
        *,
        stream_arn: str,
        batch_size: int,
        max_batching_window: int = 0,
        timeout: int = 60,
        memory: Optional[int] = None,
        ephemeral_storage: Optional[int] = None,
        **kwargs,
    ):
        """
        Decorate a function to register it as a DynamoDB task.
        Registered functions will be triggered by the specified DynamoDB stream.

        Args:
            task_id (str): Unique identifier for the DynamoDB task.
            stream_arn (str): ARN of the DynamoDB stream to listen to.
            batch_size (int): Maximum records per batch.
            max_batching_window (int, optional): Maximum batching window (seconds). Defaults to 0.
            timeout (int, optional): Lambda timeout (seconds). Defaults to 60.
            memory (Optional[int], optional): Lambda memory (MB). Defaults to None.
            ephemeral_storage (int, optional): Ephemeral storage (MB). Defaults to 512.
            **kwargs: Additional keyword arguments.

        Example:
            app = AsyncLambdaController()

            @app.dynamodb_task(
                task_id="my_dynamodb_task",
                stream_arn="arn:aws:dynamodb:us-east-1:123456789012:table/my-table/stream/2024-06-01T00:00:00.000",
                batch_size=100,
                max_batching_window=5
            )
            def my_dynamodb_task_handler(event):
                for record in event:
                    print("Processing DynamoDB record:", record)
                return
        """
        logger.debug(
            f"Registered dynamodb task '{task_id}' with stream_arn '{stream_arn}' and batch_size '{batch_size}' with the controller."
        )

        def _task(func: Callable[[DynamoDBEventT], Any]):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                self.set_current_task_id(task_id)
                return func(*args, **kwargs)

            self.add_task(
                AsyncLambdaTask(
                    controller=self,
                    executable=inner,
                    task_id=task_id,
                    trigger_type=TaskTriggerType.DYNAMODB_EVENT,
                    trigger_config={
                        "stream_arn": stream_arn,
                        "batch_size": batch_size,
                        "max_batching_window": max_batching_window,
                    },
                    timeout=timeout,
                    memory=memory,
                    ephemeral_storage=ephemeral_storage,
                    **kwargs,
                )
            )

            return inner

        return _task

    def pure_task(
        self,
        task_id: str,
        timeout: int = 60,
        memory: Optional[int] = None,
        ephemeral_storage: Optional[int] = None,
        **kwargs,
    ):
        """
        Decorate a function to register it as a pure Lambda task.
        Registered functions have no triggers and are only invoked directly via code.

        Args:
            task_id (str): Unique identifier for the pure task.
            timeout (int, optional): Lambda timeout (seconds). Defaults to 60.
            memory (Optional[int], optional): Lambda memory (MB). Defaults to None.
            ephemeral_storage (int, optional): Ephemeral storage (MB). Defaults to 512.
            **kwargs: Additional keyword arguments.

        Example:
            app = AsyncLambdaController()

            @app.pure_task("my_pure_task")
            def my_pure_task_handler(event):
                print("Pure task invoked:", event)
                return {"result": "success"}

            # Invoke directly
            app.async_invoke("my_pure_task", {"foo": "bar"}, force_sync=True)
        """
        logger.debug(f"Registered pure task '{task_id}' with the controller.")

        def _task(func: Callable[[BaseEventT], Any]):
            @functools.wraps(func)
            def inner(*args, **kwargs):
                self.set_current_task_id(task_id)
                return func(*args, **kwargs)

            self.add_task(
                AsyncLambdaTask(
                    controller=self,
                    executable=inner,
                    task_id=task_id,
                    trigger_type=TaskTriggerType.BASE_EVENT,
                    trigger_config={},
                    timeout=timeout,
                    memory=memory,
                    ephemeral_storage=ephemeral_storage,
                    **kwargs,
                )
            )

            return inner

        return _task
