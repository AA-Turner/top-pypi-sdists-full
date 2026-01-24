from pyspark.sql.connect.proto import relations_pb2 as _relations_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Rdd(_message.Message):
    __slots__ = ["map", "reduce"]
    MAP_FIELD_NUMBER: _ClassVar[int]
    REDUCE_FIELD_NUMBER: _ClassVar[int]
    map: RddMap
    reduce: RddReduce
    def __init__(self, map: _Optional[_Union[RddMap, _Mapping]] = ..., reduce: _Optional[_Union[RddReduce, _Mapping]] = ...) -> None: ...

class RddMap(_message.Message):
    __slots__ = ["func", "input"]
    FUNC_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    func: bytes
    input: _relations_pb2.Relation
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., func: _Optional[bytes] = ...) -> None: ...

class RddReduce(_message.Message):
    __slots__ = ["func", "input"]
    FUNC_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    func: bytes
    input: _relations_pb2.Relation
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., func: _Optional[bytes] = ...) -> None: ...

class SubqueryColumnAliases(_message.Message):
    __slots__ = ["aliases", "input"]
    ALIASES_FIELD_NUMBER: _ClassVar[int]
    INPUT_FIELD_NUMBER: _ClassVar[int]
    aliases: _containers.RepeatedScalarFieldContainer[str]
    input: _relations_pb2.Relation
    def __init__(self, input: _Optional[_Union[_relations_pb2.Relation, _Mapping]] = ..., aliases: _Optional[_Iterable[str]] = ...) -> None: ...
