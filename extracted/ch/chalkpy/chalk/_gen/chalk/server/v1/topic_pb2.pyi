from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SQSTopic(_message.Message):
    __slots__ = ("queue_url",)
    QUEUE_URL_FIELD_NUMBER: _ClassVar[int]
    queue_url: str
    def __init__(self, queue_url: _Optional[str] = ...) -> None: ...

class PubSubTopic(_message.Message):
    __slots__ = ("project_id", "topic_id")
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    TOPIC_ID_FIELD_NUMBER: _ClassVar[int]
    project_id: str
    topic_id: str
    def __init__(self, project_id: _Optional[str] = ..., topic_id: _Optional[str] = ...) -> None: ...

class InMemoryTopic(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Topic(_message.Message):
    __slots__ = ("sqs_topic", "pubsub_topic", "in_memory_topic")
    SQS_TOPIC_FIELD_NUMBER: _ClassVar[int]
    PUBSUB_TOPIC_FIELD_NUMBER: _ClassVar[int]
    IN_MEMORY_TOPIC_FIELD_NUMBER: _ClassVar[int]
    sqs_topic: SQSTopic
    pubsub_topic: PubSubTopic
    in_memory_topic: InMemoryTopic
    def __init__(
        self,
        sqs_topic: _Optional[_Union[SQSTopic, _Mapping]] = ...,
        pubsub_topic: _Optional[_Union[PubSubTopic, _Mapping]] = ...,
        in_memory_topic: _Optional[_Union[InMemoryTopic, _Mapping]] = ...,
    ) -> None: ...
