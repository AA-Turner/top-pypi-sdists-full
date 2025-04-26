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

class Topic(_message.Message):
    __slots__ = ("sqs_topic", "pubsub_topic")
    SQS_TOPIC_FIELD_NUMBER: _ClassVar[int]
    PUBSUB_TOPIC_FIELD_NUMBER: _ClassVar[int]
    sqs_topic: SQSTopic
    pubsub_topic: PubSubTopic
    def __init__(
        self,
        sqs_topic: _Optional[_Union[SQSTopic, _Mapping]] = ...,
        pubsub_topic: _Optional[_Union[PubSubTopic, _Mapping]] = ...,
    ) -> None: ...
