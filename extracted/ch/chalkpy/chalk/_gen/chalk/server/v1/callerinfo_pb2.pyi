from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetCallerInfoRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCallerInfoResponse(_message.Message):
    __slots__ = ("ipv4_address", "ipv6_address", "user_agent")
    IPV4_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    IPV6_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USER_AGENT_FIELD_NUMBER: _ClassVar[int]
    ipv4_address: str
    ipv6_address: str
    user_agent: str
    def __init__(
        self, ipv4_address: _Optional[str] = ..., ipv6_address: _Optional[str] = ..., user_agent: _Optional[str] = ...
    ) -> None: ...
