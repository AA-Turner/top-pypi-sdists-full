import inspect
import json
import re
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    List,
    Optional,
    TypeVar,
    Union,
)

from .. import env
from ..build_config import get_build_config_for_task, get_override_build_config_for_task
from ..config import config
from ..util import make_cf_tags

if TYPE_CHECKING:
    from ..controller import AsyncLambdaController  # pragma: not covered

from ..middleware import RT, MiddlewareStackExecutor
from .events.dynamodb_event import DynamoDBEvent
from .events.managed_sqs_batch_event import ManagedSQSBatchEvent
from .events.managed_sqs_event import ManagedSQSEvent
from .events.scheduled_event import ScheduledEvent
from .events.unmanaged_sqs_event import UnmanagedSQSEvent


class TaskTriggerType(Enum):
    """
    Enumeration of possible trigger types for an async Lambda task.

    Members:
        MANAGED_SQS: Triggered by a managed SQS event.
        MANAGED_SQS_BATCH: Triggered by a batch of managed SQS events.
        UNMANAGED_SQS: Triggered by an unmanaged SQS event.
        SCHEDULED_EVENT: Triggered by a scheduled event (e.g., cron).
        API_EVENT: Triggered by an API event (e.g., HTTP request).
        DYNAMODB_EVENT: Triggered by a DynamoDB event.
        BASE_EVENT: Triggered by a generic base event.
    """

    MANAGED_SQS = 1
    MANAGED_SQS_BATCH = 2
    UNMANAGED_SQS = 3
    SCHEDULED_EVENT = 4
    API_EVENT = 5
    DYNAMODB_EVENT = 6
    BASE_EVENT = 7


MANAGED_SQS_TASK_TYPES = {
    TaskTriggerType.MANAGED_SQS,
    TaskTriggerType.MANAGED_SQS_BATCH,
}

EventType = TypeVar(
    "EventType",
    bound=Union[
        ManagedSQSEvent,
        ManagedSQSBatchEvent,
        ScheduledEvent,
        UnmanagedSQSEvent,
        DynamoDBEvent,
    ],
)


class AsyncLambdaTask(Generic[EventType, RT]):
    """
    Represents an asynchronous Lambda task with configurable triggers, concurrency, and initialization logic.

    This class encapsulates the configuration and behavior for an async Lambda task, supporting various trigger types
    (managed SQS, unmanaged SQS, scheduled events, API events, DynamoDB streams). It provides methods for
    generating AWS SAM templates, managing queue names and ARNs, handling initialization tasks, and executing the
    task with middleware support.

    Attributes:
        controller (AsyncLambdaController): Controller managing this task.
        task_id (str): Unique identifier for the task.
        trigger_type (TaskTriggerType): Type of trigger for the task.
        trigger_config (dict): Configuration specific to the trigger type.
        timeout (int): Lambda function timeout (seconds).
        memory (Optional[int]): Memory size for the Lambda function.
        ephemeral_storage (Optional[int]): Ephemeral storage size for the Lambda function.
        maximum_concurrency (Optional[Union[int, List[int]]]): Maximum concurrency for the task or per lane.
        init_tasks (List[Union[Callable[[str], Any], Callable[[], Any]]]): Initialization tasks to run before execution.
        _has_run_init_tasks (bool): Flag indicating if initialization tasks have been run.
        executable (Callable[[EventType], RT]): Main function to execute for the task.
    """

    controller: "AsyncLambdaController"
    task_id: str
    trigger_type: TaskTriggerType
    trigger_config: dict

    timeout: int
    memory: Optional[int]
    ephemeral_storage: Optional[int]
    maximum_concurrency: Optional[Union[int, List[int]]]
    init_tasks: List[Union[Callable[[str], Any], Callable[[], Any]]]
    _has_run_init_tasks: bool

    executable: Callable[[EventType], RT]

    def __init__(
        self,
        controller: "AsyncLambdaController",
        executable: Callable[[EventType], RT],
        task_id: str,
        trigger_type: TaskTriggerType,
        trigger_config: Optional[dict] = None,
        timeout: int = 60,
        memory: Optional[int] = None,
        ephemeral_storage: Optional[int] = None,
        maximum_concurrency: Optional[Union[int, List[int]]] = None,
        init_tasks: Optional[
            List[Union[Callable[[str], Any], Callable[[], Any]]]
        ] = None,
    ):
        """
        Initialize an AsyncLambdaTask instance.

        Args:
            controller (AsyncLambdaController): Controller managing this task.
            executable (Callable[[EventType], RT]): Function to execute for this task.
            task_id (str): Unique identifier for the task.
            trigger_type (TaskTriggerType): Type of trigger for the task.
            trigger_config (Optional[dict], optional): Configuration for the trigger. Defaults to None.
            timeout (int, optional): Maximum execution time (seconds). Defaults to 60.
            memory (Optional[int], optional): Memory allocation (MB). Defaults to None.
            ephemeral_storage (Optional[int], optional): Ephemeral storage (MB). Defaults to None.
            maximum_concurrency (Optional[Union[int, List[int]]], optional): Maximum concurrency for the task. Defaults to None.
            init_tasks (Optional[List[Union[Callable[[str], Any], Callable[[], Any]]]], optional): Initialization tasks to run before execution. Defaults to None.

        Raises:
            Exception: If the DLQ (Dead Letter Queue) task ID is specified but does not exist or is not an async-task.
        """
        AsyncLambdaTask.validate_task_id(task_id)
        self.controller = controller
        self.executable = executable
        self.task_id = task_id
        self.trigger_type = trigger_type
        self.trigger_config = trigger_config if trigger_config is not None else dict()
        self.timeout = timeout
        self.memory = memory
        self.ephemeral_storage = ephemeral_storage
        self.maximum_concurrency = maximum_concurrency
        if init_tasks is None:
            self.init_tasks = []
        else:
            self.init_tasks = init_tasks
        self._has_run_init_tasks = False

        if (
            self.trigger_type in MANAGED_SQS_TASK_TYPES
            and "dlq_task_id" in self.trigger_config
        ):
            dlq_task_id = self.trigger_config["dlq_task_id"]
            if dlq_task_id:
                dlq_task = self.controller.get_task(dlq_task_id)
                if dlq_task is None:
                    raise Exception(
                        f"Error setting DLQ Task ID: No task with the task_id {dlq_task_id} exists."
                    )
                if dlq_task.trigger_type not in MANAGED_SQS_TASK_TYPES:
                    raise Exception(
                        f"Error setting DLQ Task ID: Task {dlq_task_id} is not an async-task."
                    )
        if env.is_cloud() and env.get_current_task_id() == self.task_id:
            self._run_init_tasks()

    def _run_init_tasks(self):
        """
        Run all initialization tasks for this instance if not already run.

        Calls each task in `self.init_tasks`:
            - If the task takes no parameters, it is called without arguments.
            - If the task takes one parameter, it is called with `self.task_id`.
            - If the task takes more than one parameter, raises an Exception.

        Sets `self._has_run_init_tasks` to True after execution.
        """
        if self._has_run_init_tasks:
            return
        for _init_task in self.init_tasks:
            if len(inspect.signature(_init_task).parameters) == 0:
                _init_task()  # type: ignore
            elif len(inspect.signature(_init_task).parameters) == 1:
                _init_task(self.task_id)  # type: ignore
            else:
                raise Exception(f"The init task {_init_task} has an invalid signature.")

        self._has_run_init_tasks = True

    @staticmethod
    def validate_task_id(task_id: str):
        """
        Validate a task ID to ensure it is alphanumeric and <= 32 characters.

        Args:
            task_id (str): Task ID to validate.

        Raises:
            ValueError: If the task ID contains non-alphanumeric characters or is longer than 32 characters.
        """
        if not task_id.isalnum():
            raise ValueError("Task ID must contain only A-Za-z0-9")
        if len(task_id) > 32:
            raise ValueError("Task ID must be less than 32 characters long.")

    def get_lane_count(self) -> int:
        """
        Get the lane count for the task.

        Returns:
            int: Number of lanes for the task.

        Raises:
            Exception: If the task is not a managed queue task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if "lane_count" in self.trigger_config and isinstance(
            self.trigger_config["lane_count"], int
        ):
            return self.trigger_config["lane_count"]
        return self.controller.get_lane_count()

    def should_propagate_lane_assignment(self) -> bool:
        """
        Determine whether lane assignment should be propagated for this task.

        Returns:
            bool: True if propagation is enabled, otherwise False.

        Raises:
            Exception: If the task is not a managed queue task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if "propagate_lane_assignment" in self.trigger_config and isinstance(
            self.trigger_config["propagate_lane_assignment"], bool
        ):
            return self.trigger_config["propagate_lane_assignment"]
        return self.controller.should_propagate_lane_assignment()

    def get_managed_queue_name(self, lane: int = 0):
        """
        Get the managed queue's name for this task.

        Args:
            lane (int, optional): Lane number for the managed queue. Defaults to 0.

        Returns:
            str: Name of the managed queue for this task.

        Raises:
            Exception: If the task is not a managed queue task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if lane == 0:
            return f"{config.name}-{self.task_id}"
        return f"{config.name}-{self.task_id}-L{lane}"

    def get_function_name(self):
        """
        Get the Lambda function name for this task.

        Returns:
            str: Function name in the format '<config.name>-<task_id>'.
        """
        return f"{config.name}-{self.task_id}"

    def get_managed_queue_arn(self, lane: int = 0):
        """
        Get the AWS ARN for the managed SQS queue for this task.

        Args:
            lane (int, optional): Lane number for the queue. Defaults to 0.

        Returns:
            str: ARN of the managed SQS queue.

        Raises:
            Exception: If the task is not a managed queue task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        return f"arn:aws:sqs:{env.get_aws_region()}:{env.get_aws_account_id()}:{self.get_managed_queue_name(lane=lane)}"

    def get_managed_queue_url(self, lane: int = 0):
        """
        Get the URL of the managed SQS queue for this task.

        Args:
            lane (int, optional): Lane number for the queue. Defaults to 0.

        Returns:
            str: URL of the managed SQS queue.

        Raises:
            Exception: If the task is not a managed queue task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        return f"https://sqs.{env.get_aws_region()}.amazonaws.com/{env.get_aws_account_id()}/{self.get_managed_queue_name(lane=lane)}"

    def get_function_logical_id(self):
        """
        Get the CloudFormation logical ID for the function associated with this task.

        Returns:
            str: Logical ID string, composed of the task ID followed by 'ALFunc'.
        """
        return f"{self.task_id}ALFunc"

    def get_managed_queue_logical_id(self, lane: int = 0):
        """
        Get the logical ID for the managed queue associated with this task.

        Args:
            lane (int, optional): Lane number for the queue. Defaults to 0.

        Returns:
            str: Logical ID of the managed queue.

        Raises:
            Exception: If the task is not a managed queue task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if lane == 0:
            return f"{self.task_id}ALQueue"
        return f"{self.task_id}ALQueueL{lane}"

    def get_managed_queue_extra_logical_id(self, index: int, lane: int = 0):
        """
        Get the logical ID for an extra managed queue associated with this task.

        Args:
            index (int): Index of the extra managed queue.
            lane (int, optional): Lane number for the queue. Defaults to 0.

        Returns:
            str: Logical ID string for the managed queue.

        Raises:
            Exception: If the task is not a managed queue task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if lane == 0:
            return f"{self.get_function_logical_id()}Extra{index}"
        return f"{self.get_function_logical_id()}Extra{index}L{lane}"

    def get_managed_queue_event_logical_id(self, lane: int = 0):
        """
        Get the logical ID for the managed SQS queue event associated with this task.

        Args:
            lane (int, optional): Lane number for the managed queue. Defaults to 0.

        Returns:
            str: Logical ID for the managed SQS queue event. Returns "ManagedSQS" if lane is 0, otherwise "ManagedSQSL{lane}".

        Raises:
            Exception: If the task is not a managed queue task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if lane == 0:
            return "ManagedSQS"
        return f"ManagedSQSL{lane}"

    def get_template_events(self) -> dict:
        """
        Generate event configuration templates for the task based on its trigger type and concurrency settings.

        Returns:
            dict: Event configuration for the task.

        Raises:
            Exception: If the maximum concurrency configuration is invalid for the task type.
            NotImplementedError: If the trigger type is not supported.
        """
        sqs_properties = {}
        if (
            isinstance(self.maximum_concurrency, list)
            and self.trigger_type not in MANAGED_SQS_TASK_TYPES
        ):
            raise Exception(
                f"Invalid maximum concurrency configuration for task {self.task_id}. Must be an int, not a list of ints. Lanes are only supported for ManagedSQS tasks."
            )
        if (
            isinstance(self.maximum_concurrency, list)
            and self.trigger_type in MANAGED_SQS_TASK_TYPES
            and len(self.maximum_concurrency) != self.get_lane_count()
        ):
            raise Exception(
                f"Invalid maximum concurrency configuration for task {self.task_id}. The list of maximum concurrency must be equal to the # of lanes for the task."
            )
        if self.maximum_concurrency is not None:
            sqs_properties["ScalingConfig"] = {
                "MaximumConcurrency": self.maximum_concurrency
            }
        if self.trigger_type in MANAGED_SQS_TASK_TYPES:
            events = {}
            for lane_index in range(self.get_lane_count()):
                sqs_properties = {}
                if isinstance(self.maximum_concurrency, list):
                    sqs_properties["ScalingConfig"] = {
                        "MaximumConcurrency": self.maximum_concurrency[lane_index]
                    }
                elif self.maximum_concurrency is not None:
                    sqs_properties["ScalingConfig"] = {
                        "MaximumConcurrency": self.maximum_concurrency
                    }
                if (
                    self.trigger_config.get("max_batching_window")
                    or self.trigger_config["batch_size"] > 10
                ):
                    sqs_properties["MaximumBatchingWindowInSeconds"] = (
                        self.trigger_config.get("max_batching_window") or 30
                    )

                events[self.get_managed_queue_event_logical_id(lane=lane_index)] = {
                    "Type": "SQS",
                    "Properties": {
                        "BatchSize": self.trigger_config["batch_size"],
                        "Enabled": True,
                        "Queue": {
                            "Fn::GetAtt": [
                                self.get_managed_queue_logical_id(lane=lane_index),
                                "Arn",
                            ]
                        },
                        **sqs_properties,
                    },
                }
            return events
        elif self.trigger_type == TaskTriggerType.UNMANAGED_SQS:
            return {
                "UnmanagedSQS": {
                    "Type": "SQS",
                    "Properties": {
                        "BatchSize": 1,
                        "Enabled": True,
                        "Queue": self.trigger_config["queue_arn"],
                        **sqs_properties,
                    },
                }
            }
        elif self.trigger_type == TaskTriggerType.SCHEDULED_EVENT:
            return {
                "ScheduledEvent": {
                    "Type": "ScheduleV2",
                    "Properties": {
                        "ScheduleExpression": self.trigger_config[
                            "schedule_expression"
                        ],
                        "Name": self.get_function_name(),
                    },
                }
            }
        elif self.trigger_type == TaskTriggerType.API_EVENT:
            return {
                "APIEvent": {
                    "Type": "Api",
                    "Properties": {
                        "Path": self.trigger_config["path"],
                        "Method": self.trigger_config["method"].lower(),
                        "RestApiId": {"Ref": "AsyncLambdaAPIGateway"},
                    },
                }
            }
        elif self.trigger_type == TaskTriggerType.DYNAMODB_EVENT:
            return {
                "DynamoDBEvent": {
                    "Type": "DynamoDB",
                    "Properties": {
                        "Stream": self.trigger_config["stream_arn"],
                        "StartingPosition": "TRIM_HORIZON",
                        "BatchSize": self.trigger_config["batch_size"],
                        "MaximumBatchingWindowInSeconds": self.trigger_config[
                            "max_batching_window"
                        ],
                        "Enabled": True,
                    },
                }
            }
        elif self.trigger_type == TaskTriggerType.BASE_EVENT:
            return {}
        raise NotImplementedError()

    def get_policy_sqs_resources(self) -> List[dict]:
        """
        Get a list of SQS resource ARNs or references for IAM policy statements, based on the task's trigger type.

        Returns:
            List[dict]: SQS resource references or ARNs for IAM policy usage.
        """
        if self.trigger_type in MANAGED_SQS_TASK_TYPES:
            return [
                {
                    "Fn::GetAtt": [
                        self.get_managed_queue_logical_id(lane=lane_index),
                        "Arn",
                    ]
                }
                for lane_index in range(self.get_lane_count())
            ]
        elif self.trigger_type == TaskTriggerType.UNMANAGED_SQS:
            return [self.trigger_config["queue_arn"]]
        return []

    @classmethod
    def get_policy_external_task_resources(cls, external_task_id: str) -> list:
        """
        Get a list containing an AWS SQS ARN resource for a given external task ID.

        Args:
            external_task_id (str): External task ID to use in the ARN.

        Returns:
            list: List with a single dictionary containing the formatted SQS ARN using CloudFormation Fn::Sub.
        """
        return [
            {
                "Fn::Sub": "arn:aws:sqs:${AWS::Region}:${AWS::AccountId}:external_task_id".replace(
                    "external_task_id", external_task_id
                )
            }
        ]

    def get_sam_template(
        self,
        task_ref_policy_ids: List[str],
        config_dict: dict,
        stage: Optional[str] = None,
    ) -> dict:
        """
        Generate an AWS SAM (Serverless Application Model) template for the current async lambda task.

        This template inherits the global SAM values provided via the controller's generate_sam_template(...) method.

        Args:
            task_ref_policy_ids (List[str]): List of ManagedPolicy logical IDs to attach via CloudFormation Ref.
            config_dict (dict): Configuration dictionary for deployment settings.
            stage (Optional[str], optional): Deployment stage (e.g., 'dev', 'prod'). Defaults to None.

        Returns:
            dict: SAM template resources for this task.
        """
        build_config = get_build_config_for_task(
            config=config_dict, task_id=self.task_id, stage=stage
        )
        override_config = get_override_build_config_for_task(
            config=config_dict, task_id=self.task_id, stage=stage
        )
        events = self.get_template_events()
        policy_sqs_resources = self.get_policy_sqs_resources()

        policy_statements = [
            {
                "Effect": "Allow",
                "Action": [
                    "s3:DeleteObject",
                    "s3:PutObject",
                    "s3:GetObject",
                ],
                "Resource": {
                    "Fn::Join": [
                        "",
                        [
                            "arn:aws:s3:::",
                            {"Ref": "AsyncLambdaPayloadBucket"},
                            "/*",
                        ],
                    ]
                },
            },
        ]
        if len(policy_sqs_resources) > 0:
            policy_statements.append(
                {
                    "Effect": "Allow",
                    "Action": [
                        "sqs:ChangeMessageVisibility",
                        "sqs:DeleteMessage",
                        "sqs:GetQueueAttributes",
                        "sqs:GetQueueUrl",
                        "sqs:ReceiveMessage",
                    ],
                    "Resource": policy_sqs_resources,
                },
            )

        policies = [
            {"Statement": policy_statements},
            *build_config.policies,
            *[{"Ref": policy_id} for policy_id in task_ref_policy_ids],
        ]

        template = {
            self.get_function_logical_id(): {
                "Type": "AWS::Serverless::Function",
                "Properties": {
                    "Environment": {
                        "Variables": {
                            "ASYNC_LAMBDA_TASK_ID": self.task_id,
                            **override_config.environment_variables,
                        }
                    },
                    "FunctionName": self.get_function_name(),
                    "Timeout": self.timeout,
                    "Events": events,
                    "Policies": policies,
                    "CodeUri": ".async_lambda/build/deployment.zip",
                    **override_config.function_properties,
                },
            }
        }
        if self.memory is not None:
            template[self.get_function_logical_id()]["Properties"]["MemorySize"] = (
                self.memory
            )
        if self.ephemeral_storage is not None:
            template[self.get_function_logical_id()]["Properties"][
                "EphemeralStorage"
            ] = {"Size": self.ephemeral_storage}

        if self.trigger_type in MANAGED_SQS_TASK_TYPES:
            dlq_task = self.get_dlq_task()
            if dlq_task is None:
                dead_letter_target_arn = {
                    "Fn::GetAtt": [
                        "AsyncLambdaDLQ",
                        "Arn",
                    ]
                }
            else:
                dead_letter_target_arn = {
                    "Fn::GetAtt": [
                        dlq_task.get_managed_queue_logical_id(),
                        "Arn",
                    ]
                }
            for lane_index in range(self.get_lane_count()):
                _extra_tags = {
                    "async-lambda-lane": str(lane_index),
                    "async-lambda-queue-type": "managed",
                }
                if self.trigger_config["is_dlq_task"]:
                    _extra_tags["async-lambda-queue-type"] = "dlq-task"
                template[self.get_managed_queue_logical_id(lane=lane_index)] = {
                    "Type": "AWS::SQS::Queue",
                    "Properties": {
                        "Tags": make_cf_tags({**build_config.tags, **_extra_tags}),
                        "QueueName": self.get_managed_queue_name(lane=lane_index),
                        "RedrivePolicy": {
                            "deadLetterTargetArn": dead_letter_target_arn,
                            "maxReceiveCount": self.trigger_config["max_receive_count"],
                        },
                        "VisibilityTimeout": self.timeout,
                        "MessageRetentionPeriod": 1_209_600,  # 14 days
                    },
                }
                for extra_index, extra in enumerate(build_config.managed_queue_extras):
                    template[
                        self.get_managed_queue_extra_logical_id(
                            extra_index, lane=lane_index
                        )
                    ] = self._managed_queue_extras_replace_references(
                        extra, lane=lane_index
                    )

        return template

    def _managed_queue_extras_replace_references(self, extra: dict, lane: int) -> dict:
        """
        Replace placeholder references in the `extra` dictionary with actual logical IDs for managed queues.

        Args:
            extra (dict): Dictionary containing placeholders to be replaced.
            lane (int): Lane identifier used to resolve logical IDs.

        Returns:
            dict: Dictionary with all placeholders replaced by their corresponding logical IDs.
        """
        stringified_extra = json.dumps(extra)
        stringified_extra = re.sub(
            r"\$EXTRA(?P<index>[0-9]+)",
            lambda m: self.get_managed_queue_extra_logical_id(
                int(m.group("index")), lane=lane
            ),
            stringified_extra,
        )
        stringified_extra = stringified_extra.replace(
            "$QUEUEID", self.get_managed_queue_logical_id(lane=lane)
        )

        return json.loads(stringified_extra)

    def get_dlq_task(self) -> Optional["AsyncLambdaTask"]:
        """
        Get the Dead Letter Queue (DLQ) task associated with the current task.

        Returns:
            Optional[AsyncLambdaTask]: DLQ task if applicable, otherwise None.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            return None
        if self.trigger_config.get("is_dlq_task"):
            return None
        if self.trigger_config.get("dlq_task_id") is not None:
            return self.controller.get_task(self.trigger_config["dlq_task_id"])
        return self.controller.get_dlq_task()

    def execute(self, event: EventType) -> RT:
        """
        Execute the task's main function with the provided event, applying any relevant middleware.

        Args:
            event (EventType): Event object that triggers the task execution.

        Returns:
            RT: Result of executing the task's main function after all middleware has been applied.
        """
        self._run_init_tasks()
        middleware = self.controller.get_middleware_for_event(event)
        middleware_stack_executor = MiddlewareStackExecutor[EventType, RT](
            middleware=middleware, final=self.executable
        )
        return middleware_stack_executor.call_next(event)
