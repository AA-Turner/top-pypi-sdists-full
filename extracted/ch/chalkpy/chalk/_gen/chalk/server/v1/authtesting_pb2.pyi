from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.flags.v1 import flags_pb2 as _flags_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetUnauthedTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAuthedTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetViewerTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDataScientistTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDeveloperTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAdminTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetOwnerTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAuthServiceManagerTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetFeatureFlagTestEndpointRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetUnauthedTestEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAuthedTestEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetViewerTestEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDataScientistTestEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetDeveloperTestEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAdminTestEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetOwnerTestEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAuthServiceManagerTestEndpointResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetFeatureFlagTestEndpointResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
