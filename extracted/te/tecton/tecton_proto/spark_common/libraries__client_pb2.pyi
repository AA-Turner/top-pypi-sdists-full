from tecton_proto.spark_common import clusters__client_pb2 as _clusters__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Library(_message.Message):
    __slots__ = ["egg", "egg_resource", "jar", "jar_resource", "maven", "pypi", "whl", "whl_resource"]
    EGG_FIELD_NUMBER: _ClassVar[int]
    EGG_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    JAR_FIELD_NUMBER: _ClassVar[int]
    JAR_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    MAVEN_FIELD_NUMBER: _ClassVar[int]
    PYPI_FIELD_NUMBER: _ClassVar[int]
    WHL_FIELD_NUMBER: _ClassVar[int]
    WHL_RESOURCE_FIELD_NUMBER: _ClassVar[int]
    egg: str
    egg_resource: _clusters__client_pb2.ResourceLocation
    jar: str
    jar_resource: _clusters__client_pb2.ResourceLocation
    maven: MavenLibrary
    pypi: PyPiLibrary
    whl: str
    whl_resource: _clusters__client_pb2.ResourceLocation
    def __init__(self, jar: _Optional[str] = ..., egg: _Optional[str] = ..., whl: _Optional[str] = ..., jar_resource: _Optional[_Union[_clusters__client_pb2.ResourceLocation, _Mapping]] = ..., egg_resource: _Optional[_Union[_clusters__client_pb2.ResourceLocation, _Mapping]] = ..., whl_resource: _Optional[_Union[_clusters__client_pb2.ResourceLocation, _Mapping]] = ..., maven: _Optional[_Union[MavenLibrary, _Mapping]] = ..., pypi: _Optional[_Union[PyPiLibrary, _Mapping]] = ...) -> None: ...

class MavenLibrary(_message.Message):
    __slots__ = ["coordinates", "exclusions", "repo"]
    COORDINATES_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIONS_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    coordinates: str
    exclusions: _containers.RepeatedScalarFieldContainer[str]
    repo: str
    def __init__(self, coordinates: _Optional[str] = ..., repo: _Optional[str] = ..., exclusions: _Optional[_Iterable[str]] = ...) -> None: ...

class PyPiLibrary(_message.Message):
    __slots__ = ["package", "repo"]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    package: str
    repo: str
    def __init__(self, package: _Optional[str] = ..., repo: _Optional[str] = ...) -> None: ...
