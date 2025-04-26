from tecton_proto.databricks_api import jobs__client_pb2 as _jobs__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
FAILED: LibraryStatus
INSTALLED: LibraryStatus
INSTALLING: LibraryStatus
RESOLVING: LibraryStatus
RESTORED: LibraryStatus
SKIPPED: LibraryStatus
UNINSTALL_ON_RESTART: LibraryStatus

class ClusterStatusResponse(_message.Message):
    __slots__ = ["library_statuses"]
    LIBRARY_STATUSES_FIELD_NUMBER: _ClassVar[int]
    library_statuses: _containers.RepeatedCompositeFieldContainer[LibraryStatusEntry]
    def __init__(self, library_statuses: _Optional[_Iterable[_Union[LibraryStatusEntry, _Mapping]]] = ...) -> None: ...

class LibraryInstallRequest(_message.Message):
    __slots__ = ["cluster_id", "libraries"]
    CLUSTER_ID_FIELD_NUMBER: _ClassVar[int]
    LIBRARIES_FIELD_NUMBER: _ClassVar[int]
    cluster_id: str
    libraries: _containers.RepeatedCompositeFieldContainer[_jobs__client_pb2.RemoteLibrary]
    def __init__(self, cluster_id: _Optional[str] = ..., libraries: _Optional[_Iterable[_Union[_jobs__client_pb2.RemoteLibrary, _Mapping]]] = ...) -> None: ...

class LibraryStatusEntry(_message.Message):
    __slots__ = ["library", "status"]
    LIBRARY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    library: _jobs__client_pb2.RemoteLibrary
    status: LibraryStatus
    def __init__(self, library: _Optional[_Union[_jobs__client_pb2.RemoteLibrary, _Mapping]] = ..., status: _Optional[_Union[LibraryStatus, str]] = ...) -> None: ...

class LibraryStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
