from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SelfServeConsumptionDeliveryWorkflow(_message.Message):
    __slots__ = ["delivery_watermark", "delivery_watermark_v2"]
    DELIVERY_WATERMARK_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_WATERMARK_V2_FIELD_NUMBER: _ClassVar[int]
    delivery_watermark: _timestamp_pb2.Timestamp
    delivery_watermark_v2: _timestamp_pb2.Timestamp
    def __init__(self, delivery_watermark: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., delivery_watermark_v2: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...
