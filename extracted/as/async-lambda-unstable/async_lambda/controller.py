import functools
import json
import logging
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


class AsyncLambdaController:
    is_sub: bool
    lane_count: Optional[int] = None
    propagate_lane_assignment: Optional[bool] = None
    tasks: Dict[str, AsyncLambdaTask]
    external_async_tasks: Set[str]
    current_task_id: Optional[str] = None
    current_lane: Optional[int] = None
    current_invocation_id: Optional[str] = None
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
        middleware: Optional[List[MiddlewareRegistration]] = None,
        delete_s3_payloads: bool = True,
        controller_name: Optional[str] = None,
    ):
        self.tasks = dict()
        self.external_async_tasks = set()
        self.is_sub = is_sub
        self.lane_count = lane_count
        self.propagate_lane_assignment = propagate_lane_assignment
        self.middleware = middleware or list()
        self.delete_s3_payloads = delete_s3_payloads
        self.controller_name = controller_name

    def add_middleware(
        self, event_types: List[Type[BaseEvent]], func: MiddlewareFunction[MET, RT]
    ):
        self.middleware.append((event_types, func))

    def get_middleware_for_event(self, event: MET) -> List[MiddlewareFunction[MET, RT]]:
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
        Adds a task to the async lambda controller.
        """
        if task.task_id in self.tasks:
            raise Exception(
                f"A task with the task_id {task.task_id} already exists. DUPLICATE TASK IDS"
            )
        self.tasks[task.task_id] = task

    def add_external_task(self, external_task_id: str):
        """
        Adds an external task to the controller, which will then be enabled to async_invoke.

        `external_task_id` is `{config.name}-{task_id}` of the external task (the queue name)

        Sending payloads via S3 is not currently supported with external tasks.
        """
        self.external_async_tasks.add(external_task_id)

    def get_lane_count(self) -> int:
        if self.lane_count is not None:
            return self.lane_count

        if self.parent_controller is not None:
            return self.parent_controller.get_lane_count()
        return 1

    def should_propagate_lane_assignment(self) -> bool:
        if self.propagate_lane_assignment is not None:
            return self.propagate_lane_assignment
        if self.parent_controller is not None:
            return self.parent_controller.should_propagate_lane_assignment()
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
        has_api_tasks = False
        for task in _task_list:
            if task.trigger_type == TaskTriggerType.API_EVENT:
                has_api_tasks = True
            for logical_id, resource in task.get_sam_template(
                module=module,
                tasks=_task_list,
                external_async_tasks=self.external_async_tasks,
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
                properties["Domain"] = {
                    "DomainName": build_config.domain_name,
                }
                if build_config.certificate_arn is not None:
                    properties["Domain"][
                        "CertificateArn"
                    ] = build_config.certificate_arn
                    if build_config.tls_version is not None:
                        properties["Domain"][
                            "SecurityPolicy"
                        ] = build_config.tls_version
            template["Resources"]["AsyncLambdaAPIGateway"] = {
                "Type": "AWS::Serverless::Api",
                "Properties": properties,
            }
        return template

    def _dlq_extra_logical_id(self, index: int):
        return f"AsyncLambdaDLQExtra{index}"

    def _dlq_extras_replace_references(self, extra: dict) -> dict:
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

    def handle_invocation(self, event, context, task_id: Optional[str] = None):
        """
        Direct the invocation to the task executor.
        """
        self.current_lane = None
        if task_id is None:
            task_id = env.get_current_task_id()
        task = self.tasks[task_id]

        args = (event, context, task)

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
    ):
        """
        Invoke an 'async-lambda' task asynchronously utilizing it's SQS queue.
        """
        if self.parent_controller is not None:
            return self.parent_controller.send_async_invoke_payload(
                destination_task_id=destination_task_id,
                sqs_payload=sqs_payload,
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
            if delay:
                time.sleep(delay)
            # Sync invocation with mock event/context
            current_task_id = self.current_task_id
            current_lane = self.get_current_lane()
            queue_arn = destination_task.get_managed_queue_arn(lane=lane)
            mock_event = MockSQSLambdaEvent(
                json.dumps(sqs_payload), source_queue_arn=queue_arn
            )
            mock_context = MockLambdaContext(destination_task.task_id)
            result = self.handle_invocation(
                mock_event, mock_context, task_id=destination_task_id
            )
            self.set_current_task_id(current_task_id)
            self.set_current_lane(current_lane)
            return result
        else:
            if is_external_task:
                url = f"https://sqs.{env.get_aws_region()}.amazonaws.com/{env.get_aws_account_id()}/{destination_task_id}"
            else:
                url = destination_task.get_managed_queue_url(lane=lane)
            get_sqs_client().send_message(
                QueueUrl=url,
                MessageBody=json.dumps(sqs_payload),
                DelaySeconds=delay,
            )

    def send_async_invoke_payload_batch(
        self,
        destination_task_id: str,
        sqs_payloads: Sequence[dict],
        delay: Union[int, Sequence[int]] = 0,
        force_sync: bool = False,
        lane: Optional[int] = None,
        index: int = 0,
    ):
        """
        Invoke an 'async-lambda' task asynchronously utilizing it's SQS queue.
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
            queue_arn = destination_task.get_managed_queue_arn(lane=lane)
            for i, sqs_payload in enumerate(sqs_payloads):
                if delay:
                    if isinstance(delay, Sequence):
                        time.sleep(delay[i])
                    else:
                        time.sleep(delay)
                mock_event = MockSQSLambdaEvent(
                    json.dumps(sqs_payload), source_queue_arn=queue_arn
                )
                mock_context = MockLambdaContext(destination_task.task_id)
                self.handle_invocation(
                    mock_event, mock_context, task_id=destination_task_id
                )
                self.set_current_lane(current_lane)
                self.set_current_task_id(current_task_id)
        else:
            entries: List[dict] = []
            for i, sqs_payload in enumerate(sqs_payloads):
                if isinstance(delay, Sequence):
                    _delay = delay[i]
                else:
                    _delay = delay
                entries.append(
                    {
                        "MessageBody": json.dumps(sqs_payload),
                        "DelaySeconds": _delay,
                        "Id": f"index_{index + i}",
                    }
                )
            if is_external_task:
                url = f"https://sqs.{env.get_aws_region()}.amazonaws.com/{env.get_aws_account_id()}/{destination_task_id}"
            else:
                url = destination_task.get_managed_queue_url(lane=lane)
            failed_messages = []
            for _ in range(5):
                response = get_sqs_client().send_message_batch(
                    QueueUrl=url,
                    Entries=entries,
                )
                failed_messages: List[dict] = response.get("Failed", [])
                if len(failed_messages) == 0:
                    return
                logger.warning(failed_messages)
                logger.warning(f"{len(failed_messages)} messages failed to send.")
                failed_message_ids = {message["Id"] for message in failed_messages}
                entries = [
                    entry for entry in entries if entry["Id"] in failed_message_ids
                ]
            logger.error(failed_messages)
            raise Exception(f"Failed to send {len(failed_messages)} messages.")

    def new_payload(
        self,
        payload: Any,
        destination_task_id: str,
        force_sync: bool,
    ) -> dict:
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
    ):
        """
        Invoke an Async-Lambda task.
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
        )

    def async_invoke_batch(
        self,
        task_id: str,
        payloads: Sequence[Any],
        delay: Union[int, Sequence[int]] = 0,
        force_sync: bool = False,
        lane: Optional[int] = None,
    ):
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
                force_sync=force_sync,
                lane=lane,
                index=i,
            )

    def async_lambda_handler(self, event, context):
        """
        The handler invoked by Lambda.
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
        **kwargs,
    ):
        """
        Decorate a function to register it as an async task.
        These functions can be asynchronously invoked with the `async_invoke` function
        via their `task_id`.
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
        **kwargs,
    ):
        """
        Decorate a function to register it as an async batch task.
        These functions can be asynchronously invoked with the `async_invoke` function
        via their `task_id`.
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
                    **kwargs,
                )
            )
            return inner

        return _task

    def sqs_task(self, task_id: str, queue_arn: str, **kwargs):
        """
        Decorate a function to register it as an SQS task.
        These tasks will be triggered by messages in the given queue.
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
                    **kwargs,
                )
            )

            return inner

        return _task

    def scheduled_task(self, task_id: str, schedule_expression: str, **kwargs):
        """
        Decorate a function to register it as a scheduled task.
        These tasks will be triggered by the given schedule expression.
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
                    **kwargs,
                )
            )

            return inner

        return _task

    def api_task(self, task_id: str, path: str, method: str, **kwargs):
        """
        Decorate a function to register it as an API task.
        These tasks will be triggered by an API call.
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
        **kwargs,
    ):
        """
        Decorate a function to register it as a DynamoDB task.
        These tasks will be triggered by the given DynamoDB stream.
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
                    **kwargs,
                )
            )

            return inner

        return _task

    def pure_task(self, task_id: str, **kwargs):
        """
        Decorate a function to register it as a pure lambda function.
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
                    **kwargs,
                )
            )

            return inner

        return _task
