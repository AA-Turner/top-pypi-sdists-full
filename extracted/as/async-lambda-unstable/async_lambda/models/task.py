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
    Set,
    TypeVar,
    Union,
)

from async_lambda.util import make_cf_tags

from .. import env
from ..build_config import get_build_config_for_task
from ..config import config

if TYPE_CHECKING:
    from ..controller import AsyncLambdaController  # pragma: not covered

from ..middleware import RT, MiddlewareStackExecutor
from .events.dynamodb_event import DynamoDBEvent
from .events.managed_sqs_batch_event import ManagedSQSBatchEvent
from .events.managed_sqs_event import ManagedSQSEvent
from .events.scheduled_event import ScheduledEvent
from .events.unmanaged_sqs_event import UnmanagedSQSEvent


class TaskTriggerType(Enum):
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
    controller: "AsyncLambdaController"
    task_id: str
    trigger_type: TaskTriggerType
    trigger_config: dict

    timeout: int
    memory: int
    ephemeral_storage: int
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
        memory: int = 128,
        ephemeral_storage: int = 512,
        maximum_concurrency: Optional[Union[int, List[int]]] = None,
        init_tasks: Optional[
            List[Union[Callable[[str], Any], Callable[[], Any]]]
        ] = None,
    ):
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
        if not task_id.isalnum():
            raise ValueError("Task ID must contain only A-Za-z0-9")
        if len(task_id) > 32:
            raise ValueError("Task ID must be less than 32 characters long.")

    def get_lane_count(self) -> int:
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if "lane_count" in self.trigger_config and isinstance(
            self.trigger_config["lane_count"], int
        ):
            return self.trigger_config["lane_count"]
        return self.controller.get_lane_count()

    def should_propagate_lane_assignment(self) -> bool:
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if "propagate_lane_assignment" in self.trigger_config and isinstance(
            self.trigger_config["propagate_lane_assignment"], bool
        ):
            return self.trigger_config["propagate_lane_assignment"]
        return self.controller.should_propagate_lane_assignment()

    def get_managed_queue_name(self, lane: int = 0):
        """
        Returns the managed queue's name for this task.
        """
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if lane == 0:
            return f"{config.name}-{self.task_id}"
        return f"{config.name}-{self.task_id}-L{lane}"

    def get_function_name(self):
        return f"{config.name}-{self.task_id}"

    def get_managed_queue_arn(self, lane: int = 0):
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        return f"arn:aws:sqs:{env.get_aws_region()}:{env.get_aws_account_id()}:{self.get_managed_queue_name(lane=lane)}"

    def get_managed_queue_url(self, lane: int = 0):
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        return f"https://sqs.{env.get_aws_region()}.amazonaws.com/{env.get_aws_account_id()}/{self.get_managed_queue_name(lane=lane)}"

    def get_function_logical_id(self):
        return f"{self.task_id}ALFunc"

    def get_managed_queue_logical_id(self, lane: int = 0):
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if lane == 0:
            return f"{self.task_id}ALQueue"
        return f"{self.task_id}ALQueueL{lane}"

    def get_managed_queue_extra_logical_id(self, index: int, lane: int = 0):
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if lane == 0:
            return f"{self.get_function_logical_id()}Extra{index}"
        return f"{self.get_function_logical_id()}Extra{index}L{lane}"

    def get_managed_queue_event_logical_id(self, lane: int = 0):
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            raise Exception(f"The task {self.task_id} is not a managed queue task.")
        if lane == 0:
            return "ManagedSQS"
        return f"ManagedSQSL{lane}"

    def get_template_events(self) -> dict:
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
        return [
            {
                "Fn::Sub": "arn:aws:sqs:${AWS::Region}:${AWS::AccountId}:external_task_id".replace(
                    "external_task_id", external_task_id
                )
            }
        ]

    def get_sam_template(
        self,
        module: str,
        tasks: List["AsyncLambdaTask"],
        external_async_tasks: Set[str],
        config_dict: dict,
        stage: Optional[str] = None,
    ) -> dict:
        build_config = get_build_config_for_task(config_dict, self.task_id, stage=stage)
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
        managed_tasks_resources = [
            resource
            for task in tasks
            if task.trigger_type in MANAGED_SQS_TASK_TYPES
            for resource in task.get_policy_sqs_resources()
        ] + [
            resource
            for external_async_task_id in external_async_tasks
            for resource in self.get_policy_external_task_resources(
                external_async_task_id
            )
        ]
        if len(managed_tasks_resources) > 0:
            policy_statements.append(
                {
                    "Effect": "Allow",
                    "Action": ["sqs:SendMessage"],
                    "Resource": [
                        managed_tasks_resource
                        for managed_tasks_resource in managed_tasks_resources
                    ],
                },
            )
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
        function_properties = {}
        if len(build_config.layers) > 0:
            function_properties["Layers"] = sorted(build_config.layers)
        if len(build_config.security_group_ids) > 0 or len(build_config.subnet_ids) > 0:
            function_properties["VpcConfig"] = {}
            if len(build_config.security_group_ids) > 0:
                function_properties["VpcConfig"]["SecurityGroupIds"] = sorted(
                    build_config.security_group_ids
                )
            if len(build_config.subnet_ids) > 0:
                function_properties["VpcConfig"]["SubnetIds"] = sorted(
                    build_config.subnet_ids
                )
        if len(build_config.logging_config) > 0:
            function_properties["LoggingConfig"] = build_config.logging_config

        template = {
            self.get_function_logical_id(): {
                "Type": "AWS::Serverless::Function",
                "Properties": {
                    "Tags": build_config.tags,
                    "Handler": f"{module}.lambda_handler",
                    "Runtime": config.runtime,
                    "Environment": {
                        "Variables": {
                            "ASYNC_LAMBDA_PAYLOAD_S3_BUCKET": {
                                "Ref": "AsyncLambdaPayloadBucket"
                            },
                            "ASYNC_LAMBDA_TASK_ID": self.task_id,
                            "ASYNC_LAMBDA_ACCOUNT_ID": {"Ref": "AWS::AccountId"},
                            **build_config.environment_variables,
                        }
                    },
                    "FunctionName": self.get_function_name(),
                    "CodeUri": ".async_lambda/build/deployment.zip",
                    "EphemeralStorage": {"Size": self.ephemeral_storage},
                    "MemorySize": self.memory,
                    "Timeout": self.timeout,
                    "Events": events,
                    "Policies": [
                        {"Statement": policy_statements},
                        *build_config.policies,
                    ],
                    **function_properties,
                },
            }
        }

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
        if self.trigger_type not in MANAGED_SQS_TASK_TYPES:
            return None
        if self.trigger_config.get("is_dlq_task"):
            return None
        if self.trigger_config.get("dlq_task_id") is not None:
            return self.controller.get_task(self.trigger_config["dlq_task_id"])
        return self.controller.get_dlq_task()

    def execute(self, event: EventType) -> RT:
        """
        Executes the tasks function
        """
        self._run_init_tasks()
        middleware = self.controller.get_middleware_for_event(event)
        middleware_stack_executor = MiddlewareStackExecutor[EventType, RT](
            middleware=middleware, final=self.executable
        )
        return middleware_stack_executor.call_next(event)
