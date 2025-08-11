from chalk._gen.chalk.auth.v1 import permissions_pb2 as _permissions_pb2
from chalk._gen.chalk.graph.v1 import graph_pb2 as _graph_pb2
from google.protobuf.internal import containers as _containers
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

class GetAllNamedQueriesRequest(_message.Message):
    __slots__ = ("deployment_id",)
    DEPLOYMENT_ID_FIELD_NUMBER: _ClassVar[int]
    deployment_id: str
    def __init__(self, deployment_id: _Optional[str] = ...) -> None: ...

class GetNamedQueryByNameRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class GetNamedQueryByNameResponse(_message.Message):
    __slots__ = ("named_queries",)
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    named_queries: _containers.RepeatedCompositeFieldContainer[_graph_pb2.NamedQuery]
    def __init__(self, named_queries: _Optional[_Iterable[_Union[_graph_pb2.NamedQuery, _Mapping]]] = ...) -> None: ...

class GetAllNamedQueriesResponse(_message.Message):
    __slots__ = ("named_queries",)
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    named_queries: _containers.RepeatedCompositeFieldContainer[_graph_pb2.NamedQuery]
    def __init__(self, named_queries: _Optional[_Iterable[_Union[_graph_pb2.NamedQuery, _Mapping]]] = ...) -> None: ...

class GetAllNamedQueriesActiveDeploymentRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetAllNamedQueriesActiveDeploymentResponse(_message.Message):
    __slots__ = ("named_queries",)
    NAMED_QUERIES_FIELD_NUMBER: _ClassVar[int]
    named_queries: _containers.RepeatedCompositeFieldContainer[_graph_pb2.NamedQuery]
    def __init__(self, named_queries: _Optional[_Iterable[_Union[_graph_pb2.NamedQuery, _Mapping]]] = ...) -> None: ...
