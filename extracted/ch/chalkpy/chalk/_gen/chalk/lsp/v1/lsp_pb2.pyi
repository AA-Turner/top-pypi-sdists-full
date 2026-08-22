from chalk._gen.chalk.lsp.v1 import range_pb2 as _range_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import (
    ClassVar as _ClassVar,
    Iterable as _Iterable,
    Mapping as _Mapping,
    Optional as _Optional,
    Union as _Union,
)
from chalk._gen.chalk.lsp.v1.range_pb2 import Range as Range
from chalk._gen.chalk.lsp.v1.range_pb2 import Position as Position

DESCRIPTOR: _descriptor.FileDescriptor

class LogMessageSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOG_MESSAGE_SEVERITY_UNSPECIFIED: _ClassVar[LogMessageSeverity]
    LOG_MESSAGE_SEVERITY_ERROR: _ClassVar[LogMessageSeverity]
    LOG_MESSAGE_SEVERITY_WARNING: _ClassVar[LogMessageSeverity]
    LOG_MESSAGE_SEVERITY_INFO: _ClassVar[LogMessageSeverity]
    LOG_MESSAGE_SEVERITY_DEBUG: _ClassVar[LogMessageSeverity]

class DiagnosticSeverity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DIAGNOSTIC_SEVERITY_UNSPECIFIED: _ClassVar[DiagnosticSeverity]
    DIAGNOSTIC_SEVERITY_ERROR: _ClassVar[DiagnosticSeverity]
    DIAGNOSTIC_SEVERITY_WARNING: _ClassVar[DiagnosticSeverity]
    DIAGNOSTIC_SEVERITY_INFORMATION: _ClassVar[DiagnosticSeverity]
    DIAGNOSTIC_SEVERITY_HINT: _ClassVar[DiagnosticSeverity]

LOG_MESSAGE_SEVERITY_UNSPECIFIED: LogMessageSeverity
LOG_MESSAGE_SEVERITY_ERROR: LogMessageSeverity
LOG_MESSAGE_SEVERITY_WARNING: LogMessageSeverity
LOG_MESSAGE_SEVERITY_INFO: LogMessageSeverity
LOG_MESSAGE_SEVERITY_DEBUG: LogMessageSeverity
DIAGNOSTIC_SEVERITY_UNSPECIFIED: DiagnosticSeverity
DIAGNOSTIC_SEVERITY_ERROR: DiagnosticSeverity
DIAGNOSTIC_SEVERITY_WARNING: DiagnosticSeverity
DIAGNOSTIC_SEVERITY_INFORMATION: DiagnosticSeverity
DIAGNOSTIC_SEVERITY_HINT: DiagnosticSeverity

class LSP(_message.Message):
    __slots__ = ("diagnostics", "actions", "logs")
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    ACTIONS_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    diagnostics: _containers.RepeatedCompositeFieldContainer[PublishDiagnosticsParams]
    actions: _containers.RepeatedCompositeFieldContainer[CodeAction]
    logs: _containers.RepeatedCompositeFieldContainer[LogMessage]
    def __init__(
        self,
        diagnostics: _Optional[_Iterable[_Union[PublishDiagnosticsParams, _Mapping]]] = ...,
        actions: _Optional[_Iterable[_Union[CodeAction, _Mapping]]] = ...,
        logs: _Optional[_Iterable[_Union[LogMessage, _Mapping]]] = ...,
    ) -> None: ...

class LogMessage(_message.Message):
    __slots__ = ("severity", "message", "traceback")
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TRACEBACK_FIELD_NUMBER: _ClassVar[int]
    severity: LogMessageSeverity
    message: str
    traceback: str
    def __init__(
        self,
        severity: _Optional[_Union[LogMessageSeverity, str]] = ...,
        message: _Optional[str] = ...,
        traceback: _Optional[str] = ...,
    ) -> None: ...

class PublishDiagnosticsParams(_message.Message):
    __slots__ = ("uri", "diagnostics")
    URI_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    uri: str
    diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
    def __init__(
        self, uri: _Optional[str] = ..., diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping]]] = ...
    ) -> None: ...

class Diagnostic(_message.Message):
    __slots__ = ("range", "message", "severity", "code", "code_description", "related_information")
    RANGE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SEVERITY_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    CODE_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RELATED_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    range: _range_pb2.Range
    message: str
    severity: DiagnosticSeverity
    code: str
    code_description: CodeDescription
    related_information: _containers.RepeatedCompositeFieldContainer[DiagnosticRelatedInformation]
    def __init__(
        self,
        range: _Optional[_Union[_range_pb2.Range, _Mapping]] = ...,
        message: _Optional[str] = ...,
        severity: _Optional[_Union[DiagnosticSeverity, str]] = ...,
        code: _Optional[str] = ...,
        code_description: _Optional[_Union[CodeDescription, _Mapping]] = ...,
        related_information: _Optional[_Iterable[_Union[DiagnosticRelatedInformation, _Mapping]]] = ...,
    ) -> None: ...

class CodeAction(_message.Message):
    __slots__ = ("title", "diagnostics", "edit")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSTICS_FIELD_NUMBER: _ClassVar[int]
    EDIT_FIELD_NUMBER: _ClassVar[int]
    title: str
    diagnostics: _containers.RepeatedCompositeFieldContainer[Diagnostic]
    edit: WorkspaceEdit
    def __init__(
        self,
        title: _Optional[str] = ...,
        diagnostics: _Optional[_Iterable[_Union[Diagnostic, _Mapping]]] = ...,
        edit: _Optional[_Union[WorkspaceEdit, _Mapping]] = ...,
    ) -> None: ...

class WorkspaceEdit(_message.Message):
    __slots__ = ("document_changes",)
    DOCUMENT_CHANGES_FIELD_NUMBER: _ClassVar[int]
    document_changes: _containers.RepeatedCompositeFieldContainer[TextDocumentEdit]
    def __init__(self, document_changes: _Optional[_Iterable[_Union[TextDocumentEdit, _Mapping]]] = ...) -> None: ...

class TextDocumentEdit(_message.Message):
    __slots__ = ("text_document", "edits")
    TEXT_DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    EDITS_FIELD_NUMBER: _ClassVar[int]
    text_document: TextDocumentIdentifier
    edits: _containers.RepeatedCompositeFieldContainer[TextEdit]
    def __init__(
        self,
        text_document: _Optional[_Union[TextDocumentIdentifier, _Mapping]] = ...,
        edits: _Optional[_Iterable[_Union[TextEdit, _Mapping]]] = ...,
    ) -> None: ...

class TextDocumentIdentifier(_message.Message):
    __slots__ = ("uri",)
    URI_FIELD_NUMBER: _ClassVar[int]
    uri: str
    def __init__(self, uri: _Optional[str] = ...) -> None: ...

class TextEdit(_message.Message):
    __slots__ = ("range", "new_text")
    RANGE_FIELD_NUMBER: _ClassVar[int]
    NEW_TEXT_FIELD_NUMBER: _ClassVar[int]
    range: _range_pb2.Range
    new_text: str
    def __init__(
        self, range: _Optional[_Union[_range_pb2.Range, _Mapping]] = ..., new_text: _Optional[str] = ...
    ) -> None: ...

class CodeDescription(_message.Message):
    __slots__ = ("href",)
    HREF_FIELD_NUMBER: _ClassVar[int]
    href: str
    def __init__(self, href: _Optional[str] = ...) -> None: ...

class DiagnosticRelatedInformation(_message.Message):
    __slots__ = ("location", "message")
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    location: Location
    message: str
    def __init__(
        self, location: _Optional[_Union[Location, _Mapping]] = ..., message: _Optional[str] = ...
    ) -> None: ...

class Location(_message.Message):
    __slots__ = ("uri", "range")
    URI_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    uri: str
    range: _range_pb2.Range
    def __init__(
        self, uri: _Optional[str] = ..., range: _Optional[_Union[_range_pb2.Range, _Mapping]] = ...
    ) -> None: ...
