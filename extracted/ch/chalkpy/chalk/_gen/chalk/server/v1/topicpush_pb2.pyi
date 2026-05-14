from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.server.v1 import topic_pb2 as _topic_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)

DESCRIPTOR: _descriptor.FileDescriptor

class TopicPushQueue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TOPIC_PUSH_QUEUE_UNSPECIFIED: _ClassVar[TopicPushQueue]
    TOPIC_PUSH_QUEUE_DEFAULT: _ClassVar[TopicPushQueue]
    TOPIC_PUSH_QUEUE_METRICS: _ClassVar[TopicPushQueue]

TOPIC_PUSH_QUEUE_UNSPECIFIED: TopicPushQueue
TOPIC_PUSH_QUEUE_DEFAULT: TopicPushQueue
TOPIC_PUSH_QUEUE_METRICS: TopicPushQueue

class ScheduledJob(_message.Message):
    __slots__ = ("id", "name", "payload", "schedule", "topic", "attributes", "environment", "tags")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    payload: str
    schedule: str
    topic: _topic_pb2.Topic
    attributes: _containers.ScalarMap[str, str]
    environment: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        payload: _Optional[str] = ...,
        schedule: _Optional[str] = ...,
        topic: _Optional[_Union[_topic_pb2.Topic, _Mapping]] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
        environment: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
    ) -> None: ...

class UpdateJobRequest(_message.Message):
    __slots__ = ("id", "name", "payload", "schedule", "topic", "attributes", "environment", "tags", "queue")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    payload: str
    schedule: str
    topic: _topic_pb2.Topic
    attributes: _containers.ScalarMap[str, str]
    environment: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    queue: TopicPushQueue
    def __init__(
        self,
        id: _Optional[str] = ...,
        name: _Optional[str] = ...,
        payload: _Optional[str] = ...,
        schedule: _Optional[str] = ...,
        topic: _Optional[_Union[_topic_pb2.Topic, _Mapping]] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
        environment: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        queue: _Optional[_Union[TopicPushQueue, str]] = ...,
    ) -> None: ...

class UpdateJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: ScheduledJob
    def __init__(self, job: _Optional[_Union[ScheduledJob, _Mapping]] = ...) -> None: ...

class ListJobsRequest(_message.Message):
    __slots__ = ("queue",)
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    queue: TopicPushQueue
    def __init__(self, queue: _Optional[_Union[TopicPushQueue, str]] = ...) -> None: ...

class ListJobsResponse(_message.Message):
    __slots__ = ("jobs",)
    JOBS_FIELD_NUMBER: _ClassVar[int]
    jobs: _containers.RepeatedCompositeFieldContainer[ScheduledJob]
    def __init__(self, jobs: _Optional[_Iterable[_Union[ScheduledJob, _Mapping]]] = ...) -> None: ...

class CreateJobRequest(_message.Message):
    __slots__ = ("name", "payload", "schedule", "topic", "attributes", "environment", "tags", "queue")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

    NAME_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    payload: str
    schedule: str
    topic: _topic_pb2.Topic
    attributes: _containers.ScalarMap[str, str]
    environment: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    queue: TopicPushQueue
    def __init__(
        self,
        name: _Optional[str] = ...,
        payload: _Optional[str] = ...,
        schedule: _Optional[str] = ...,
        topic: _Optional[_Union[_topic_pb2.Topic, _Mapping]] = ...,
        attributes: _Optional[_Mapping[str, str]] = ...,
        environment: _Optional[str] = ...,
        tags: _Optional[_Iterable[str]] = ...,
        queue: _Optional[_Union[TopicPushQueue, str]] = ...,
    ) -> None: ...

class CreateJobResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: ScheduledJob
    def __init__(self, job: _Optional[_Union[ScheduledJob, _Mapping]] = ...) -> None: ...

class DeleteJobRequest(_message.Message):
    __slots__ = ("id", "queue")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    id: str
    queue: TopicPushQueue
    def __init__(self, id: _Optional[str] = ..., queue: _Optional[_Union[TopicPushQueue, str]] = ...) -> None: ...

class DeleteJobResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetJobByNameRequest(_message.Message):
    __slots__ = ("name", "queue")
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    queue: TopicPushQueue
    def __init__(self, name: _Optional[str] = ..., queue: _Optional[_Union[TopicPushQueue, str]] = ...) -> None: ...

class GetJobByNameResponse(_message.Message):
    __slots__ = ("job",)
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: ScheduledJob
    def __init__(self, job: _Optional[_Union[ScheduledJob, _Mapping]] = ...) -> None: ...
