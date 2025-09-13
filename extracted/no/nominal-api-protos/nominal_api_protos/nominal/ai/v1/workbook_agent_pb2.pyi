from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StreamChatRequest(_message.Message):
    __slots__ = ("messages", "notebook_as_json", "selected_tab_index", "images")
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_AS_JSON_FIELD_NUMBER: _ClassVar[int]
    SELECTED_TAB_INDEX_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    messages: _containers.RepeatedCompositeFieldContainer[ModelMessage]
    notebook_as_json: str
    selected_tab_index: int
    images: _containers.RepeatedCompositeFieldContainer[ImagePart]
    def __init__(self, messages: _Optional[_Iterable[_Union[ModelMessage, _Mapping]]] = ..., notebook_as_json: _Optional[str] = ..., selected_tab_index: _Optional[int] = ..., images: _Optional[_Iterable[_Union[ImagePart, _Mapping]]] = ...) -> None: ...

class ModelMessage(_message.Message):
    __slots__ = ("user", "assistant")
    USER_FIELD_NUMBER: _ClassVar[int]
    ASSISTANT_FIELD_NUMBER: _ClassVar[int]
    user: UserModelMessage
    assistant: AssistantModelMessage
    def __init__(self, user: _Optional[_Union[UserModelMessage, _Mapping]] = ..., assistant: _Optional[_Union[AssistantModelMessage, _Mapping]] = ...) -> None: ...

class UserModelMessage(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: _containers.RepeatedCompositeFieldContainer[UserContentPart]
    def __init__(self, text: _Optional[_Iterable[_Union[UserContentPart, _Mapping]]] = ...) -> None: ...

class AssistantModelMessage(_message.Message):
    __slots__ = ("content_parts",)
    CONTENT_PARTS_FIELD_NUMBER: _ClassVar[int]
    content_parts: _containers.RepeatedCompositeFieldContainer[AssistantContentPart]
    def __init__(self, content_parts: _Optional[_Iterable[_Union[AssistantContentPart, _Mapping]]] = ...) -> None: ...

class UserContentPart(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: TextPart
    def __init__(self, text: _Optional[_Union[TextPart, _Mapping]] = ...) -> None: ...

class AssistantContentPart(_message.Message):
    __slots__ = ("text", "reasoning")
    TEXT_FIELD_NUMBER: _ClassVar[int]
    REASONING_FIELD_NUMBER: _ClassVar[int]
    text: TextPart
    reasoning: ReasoningPart
    def __init__(self, text: _Optional[_Union[TextPart, _Mapping]] = ..., reasoning: _Optional[_Union[ReasoningPart, _Mapping]] = ...) -> None: ...

class TextPart(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class ImagePart(_message.Message):
    __slots__ = ("data", "media_type", "filename")
    DATA_FIELD_NUMBER: _ClassVar[int]
    MEDIA_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    media_type: str
    filename: str
    def __init__(self, data: _Optional[bytes] = ..., media_type: _Optional[str] = ..., filename: _Optional[str] = ...) -> None: ...

class ReasoningPart(_message.Message):
    __slots__ = ("reasoning",)
    REASONING_FIELD_NUMBER: _ClassVar[int]
    reasoning: str
    def __init__(self, reasoning: _Optional[str] = ...) -> None: ...

class StreamChatResponse(_message.Message):
    __slots__ = ("finish", "error", "text_start", "text_delta", "text_end", "reasoning_start", "reasoning_delta", "reasoning_end", "workbook_mutation", "tool_action")
    FINISH_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TEXT_START_FIELD_NUMBER: _ClassVar[int]
    TEXT_DELTA_FIELD_NUMBER: _ClassVar[int]
    TEXT_END_FIELD_NUMBER: _ClassVar[int]
    REASONING_START_FIELD_NUMBER: _ClassVar[int]
    REASONING_DELTA_FIELD_NUMBER: _ClassVar[int]
    REASONING_END_FIELD_NUMBER: _ClassVar[int]
    WORKBOOK_MUTATION_FIELD_NUMBER: _ClassVar[int]
    TOOL_ACTION_FIELD_NUMBER: _ClassVar[int]
    finish: Finish
    error: Error
    text_start: TextStart
    text_delta: TextDelta
    text_end: TextEnd
    reasoning_start: ReasoningStart
    reasoning_delta: ReasoningDelta
    reasoning_end: ReasoningEnd
    workbook_mutation: WorkbookMutation
    tool_action: ToolAction
    def __init__(self, finish: _Optional[_Union[Finish, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ..., text_start: _Optional[_Union[TextStart, _Mapping]] = ..., text_delta: _Optional[_Union[TextDelta, _Mapping]] = ..., text_end: _Optional[_Union[TextEnd, _Mapping]] = ..., reasoning_start: _Optional[_Union[ReasoningStart, _Mapping]] = ..., reasoning_delta: _Optional[_Union[ReasoningDelta, _Mapping]] = ..., reasoning_end: _Optional[_Union[ReasoningEnd, _Mapping]] = ..., workbook_mutation: _Optional[_Union[WorkbookMutation, _Mapping]] = ..., tool_action: _Optional[_Union[ToolAction, _Mapping]] = ...) -> None: ...

class Finish(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Error(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class TextStart(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TextDelta(_message.Message):
    __slots__ = ("id", "delta")
    ID_FIELD_NUMBER: _ClassVar[int]
    DELTA_FIELD_NUMBER: _ClassVar[int]
    id: str
    delta: str
    def __init__(self, id: _Optional[str] = ..., delta: _Optional[str] = ...) -> None: ...

class TextEnd(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ReasoningStart(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class ReasoningDelta(_message.Message):
    __slots__ = ("id", "delta")
    ID_FIELD_NUMBER: _ClassVar[int]
    DELTA_FIELD_NUMBER: _ClassVar[int]
    id: str
    delta: str
    def __init__(self, id: _Optional[str] = ..., delta: _Optional[str] = ...) -> None: ...

class ReasoningEnd(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class AddTabMutation(_message.Message):
    __slots__ = ("tab_name",)
    TAB_NAME_FIELD_NUMBER: _ClassVar[int]
    tab_name: str
    def __init__(self, tab_name: _Optional[str] = ...) -> None: ...

class AddOrUpdatePanelMutation(_message.Message):
    __slots__ = ("panel_as_json", "panel_id", "tab_index")
    PANEL_AS_JSON_FIELD_NUMBER: _ClassVar[int]
    PANEL_ID_FIELD_NUMBER: _ClassVar[int]
    TAB_INDEX_FIELD_NUMBER: _ClassVar[int]
    panel_as_json: str
    panel_id: str
    tab_index: int
    def __init__(self, panel_as_json: _Optional[str] = ..., panel_id: _Optional[str] = ..., tab_index: _Optional[int] = ...) -> None: ...

class RemovePanelsMutation(_message.Message):
    __slots__ = ("panel_ids",)
    PANEL_IDS_FIELD_NUMBER: _ClassVar[int]
    panel_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, panel_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AddOrReplaceVariableMutation(_message.Message):
    __slots__ = ("compute_spec_as_json", "variable_name", "display_name")
    COMPUTE_SPEC_AS_JSON_FIELD_NUMBER: _ClassVar[int]
    VARIABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    DISPLAY_NAME_FIELD_NUMBER: _ClassVar[int]
    compute_spec_as_json: str
    variable_name: str
    display_name: str
    def __init__(self, compute_spec_as_json: _Optional[str] = ..., variable_name: _Optional[str] = ..., display_name: _Optional[str] = ...) -> None: ...

class DeleteVariablesMutation(_message.Message):
    __slots__ = ("variable_names",)
    VARIABLE_NAMES_FIELD_NUMBER: _ClassVar[int]
    variable_names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, variable_names: _Optional[_Iterable[str]] = ...) -> None: ...

class WorkbookMutation(_message.Message):
    __slots__ = ("id", "add_tab", "add_or_update_panel", "remove_panels", "add_or_replace_variable", "delete_variables")
    ID_FIELD_NUMBER: _ClassVar[int]
    ADD_TAB_FIELD_NUMBER: _ClassVar[int]
    ADD_OR_UPDATE_PANEL_FIELD_NUMBER: _ClassVar[int]
    REMOVE_PANELS_FIELD_NUMBER: _ClassVar[int]
    ADD_OR_REPLACE_VARIABLE_FIELD_NUMBER: _ClassVar[int]
    DELETE_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    id: str
    add_tab: AddTabMutation
    add_or_update_panel: AddOrUpdatePanelMutation
    remove_panels: RemovePanelsMutation
    add_or_replace_variable: AddOrReplaceVariableMutation
    delete_variables: DeleteVariablesMutation
    def __init__(self, id: _Optional[str] = ..., add_tab: _Optional[_Union[AddTabMutation, _Mapping]] = ..., add_or_update_panel: _Optional[_Union[AddOrUpdatePanelMutation, _Mapping]] = ..., remove_panels: _Optional[_Union[RemovePanelsMutation, _Mapping]] = ..., add_or_replace_variable: _Optional[_Union[AddOrReplaceVariableMutation, _Mapping]] = ..., delete_variables: _Optional[_Union[DeleteVariablesMutation, _Mapping]] = ...) -> None: ...

class ToolAction(_message.Message):
    __slots__ = ("id", "tool_action_verb", "tool_target")
    ID_FIELD_NUMBER: _ClassVar[int]
    TOOL_ACTION_VERB_FIELD_NUMBER: _ClassVar[int]
    TOOL_TARGET_FIELD_NUMBER: _ClassVar[int]
    id: str
    tool_action_verb: str
    tool_target: str
    def __init__(self, id: _Optional[str] = ..., tool_action_verb: _Optional[str] = ..., tool_target: _Optional[str] = ...) -> None: ...
