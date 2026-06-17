from chalk._gen.chalk.artifacts.v1 import export_pb2 as _export_pb2
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

class HealthCheckRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HealthCheckResponse(_message.Message):
    __slots__ = ("status", "service")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    status: str
    service: str
    def __init__(self, status: _Optional[str] = ..., service: _Optional[str] = ...) -> None: ...

class GetStaticConversionDiagnosticsRequest(_message.Message):
    __slots__ = ("export", "render_failed_proofs")
    EXPORT_FIELD_NUMBER: _ClassVar[int]
    RENDER_FAILED_PROOFS_FIELD_NUMBER: _ClassVar[int]
    export: _export_pb2.Export
    render_failed_proofs: bool
    def __init__(
        self, export: _Optional[_Union[_export_pb2.Export, _Mapping]] = ..., render_failed_proofs: bool = ...
    ) -> None: ...

class GetSupportedPythonSurfaceRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSupportedPythonSurfaceResponse(_message.Message):
    __slots__ = ("namespaces", "types")
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    namespaces: _containers.RepeatedCompositeFieldContainer[PythonNamespaceSurface]
    types: _containers.RepeatedCompositeFieldContainer[PythonTypeSurface]
    def __init__(
        self,
        namespaces: _Optional[_Iterable[_Union[PythonNamespaceSurface, _Mapping]]] = ...,
        types: _Optional[_Iterable[_Union[PythonTypeSurface, _Mapping]]] = ...,
    ) -> None: ...

class PythonNamespaceSurface(_message.Message):
    __slots__ = ("name", "members")
    NAME_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    name: PythonQualifiedName
    members: _containers.RepeatedCompositeFieldContainer[PythonMember]
    def __init__(
        self,
        name: _Optional[_Union[PythonQualifiedName, _Mapping]] = ...,
        members: _Optional[_Iterable[_Union[PythonMember, _Mapping]]] = ...,
    ) -> None: ...

class PythonTypeSurface(_message.Message):
    __slots__ = ("receiver", "members")
    RECEIVER_FIELD_NUMBER: _ClassVar[int]
    MEMBERS_FIELD_NUMBER: _ClassVar[int]
    receiver: TypePattern
    members: _containers.RepeatedCompositeFieldContainer[PythonMember]
    def __init__(
        self,
        receiver: _Optional[_Union[TypePattern, _Mapping]] = ...,
        members: _Optional[_Iterable[_Union[PythonMember, _Mapping]]] = ...,
    ) -> None: ...

class PythonQualifiedName(_message.Message):
    __slots__ = ("parts",)
    PARTS_FIELD_NUMBER: _ClassVar[int]
    parts: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, parts: _Optional[_Iterable[str]] = ...) -> None: ...

class PythonMember(_message.Message):
    __slots__ = ("name", "documentation", "callable", "attribute")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOCUMENTATION_FIELD_NUMBER: _ClassVar[int]
    CALLABLE_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTE_FIELD_NUMBER: _ClassVar[int]
    name: str
    documentation: str
    callable: CallableSupport
    attribute: AttributeSupport
    def __init__(
        self,
        name: _Optional[str] = ...,
        documentation: _Optional[str] = ...,
        callable: _Optional[_Union[CallableSupport, _Mapping]] = ...,
        attribute: _Optional[_Union[AttributeSupport, _Mapping]] = ...,
    ) -> None: ...

class CallableSupport(_message.Message):
    __slots__ = ("overloads",)
    OVERLOADS_FIELD_NUMBER: _ClassVar[int]
    overloads: _containers.RepeatedCompositeFieldContainer[CallableOverload]
    def __init__(self, overloads: _Optional[_Iterable[_Union[CallableOverload, _Mapping]]] = ...) -> None: ...

class CallableOverload(_message.Message):
    __slots__ = ("signature", "parameters", "return_type", "behavior", "source_module")
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    RETURN_TYPE_FIELD_NUMBER: _ClassVar[int]
    BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    SOURCE_MODULE_FIELD_NUMBER: _ClassVar[int]
    signature: str
    parameters: _containers.RepeatedCompositeFieldContainer[ParameterSupport]
    return_type: TypePattern
    behavior: BehaviorSupport
    source_module: str
    def __init__(
        self,
        signature: _Optional[str] = ...,
        parameters: _Optional[_Iterable[_Union[ParameterSupport, _Mapping]]] = ...,
        return_type: _Optional[_Union[TypePattern, _Mapping]] = ...,
        behavior: _Optional[_Union[BehaviorSupport, _Mapping]] = ...,
        source_module: _Optional[str] = ...,
    ) -> None: ...

class ParameterSupport(_message.Message):
    __slots__ = ("name", "type", "optional", "default_display", "requires_static_value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    OPTIONAL_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_DISPLAY_FIELD_NUMBER: _ClassVar[int]
    REQUIRES_STATIC_VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    type: TypePattern
    optional: bool
    default_display: str
    requires_static_value: bool
    def __init__(
        self,
        name: _Optional[str] = ...,
        type: _Optional[_Union[TypePattern, _Mapping]] = ...,
        optional: bool = ...,
        default_display: _Optional[str] = ...,
        requires_static_value: bool = ...,
    ) -> None: ...

class BehaviorSupport(_message.Message):
    __slots__ = ("has_proof", "may_raise", "raises", "row_fallible")
    HAS_PROOF_FIELD_NUMBER: _ClassVar[int]
    MAY_RAISE_FIELD_NUMBER: _ClassVar[int]
    RAISES_FIELD_NUMBER: _ClassVar[int]
    ROW_FALLIBLE_FIELD_NUMBER: _ClassVar[int]
    has_proof: bool
    may_raise: bool
    raises: _containers.RepeatedScalarFieldContainer[str]
    row_fallible: bool
    def __init__(
        self,
        has_proof: bool = ...,
        may_raise: bool = ...,
        raises: _Optional[_Iterable[str]] = ...,
        row_fallible: bool = ...,
    ) -> None: ...

class AttributeSupport(_message.Message):
    __slots__ = ("value_type", "source_module")
    VALUE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_MODULE_FIELD_NUMBER: _ClassVar[int]
    value_type: TypePattern
    source_module: str
    def __init__(
        self, value_type: _Optional[_Union[TypePattern, _Mapping]] = ..., source_module: _Optional[str] = ...
    ) -> None: ...

class TypePattern(_message.Message):
    __slots__ = ("key", "display", "nullable", "exact", "subclass", "generic", "any")
    KEY_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_FIELD_NUMBER: _ClassVar[int]
    NULLABLE_FIELD_NUMBER: _ClassVar[int]
    EXACT_FIELD_NUMBER: _ClassVar[int]
    SUBCLASS_FIELD_NUMBER: _ClassVar[int]
    GENERIC_FIELD_NUMBER: _ClassVar[int]
    ANY_FIELD_NUMBER: _ClassVar[int]
    key: str
    display: str
    nullable: bool
    exact: ExactType
    subclass: SubclassType
    generic: GenericType
    any: AnyType
    def __init__(
        self,
        key: _Optional[str] = ...,
        display: _Optional[str] = ...,
        nullable: bool = ...,
        exact: _Optional[_Union[ExactType, _Mapping]] = ...,
        subclass: _Optional[_Union[SubclassType, _Mapping]] = ...,
        generic: _Optional[_Union[GenericType, _Mapping]] = ...,
        any: _Optional[_Union[AnyType, _Mapping]] = ...,
    ) -> None: ...

class ExactType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class SubclassType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GenericType(_message.Message):
    __slots__ = ("parameters",)
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    parameters: _containers.RepeatedCompositeFieldContainer[TypePattern]
    def __init__(self, parameters: _Optional[_Iterable[_Union[TypePattern, _Mapping]]] = ...) -> None: ...

class AnyType(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
