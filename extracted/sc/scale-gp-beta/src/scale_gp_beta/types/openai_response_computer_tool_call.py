# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "OpenAIResponseComputerToolCall",
    "Action",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionClick",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionDoubleClick",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionDrag",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionDragPath",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionKeypress",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionMove",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionScreenshot",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionScroll",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionType",
    "ActionOpenAITypesResponsesResponseComputerToolCallActionWait",
    "PendingSafetyCheck",
]


class ActionOpenAITypesResponsesResponseComputerToolCallActionClick(BaseModel):
    button: Literal["left", "right", "wheel", "back", "forward"]

    type: Literal["click"]

    x: int

    y: int

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionDoubleClick(BaseModel):
    type: Literal["double_click"]

    x: int

    y: int

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionDragPath(BaseModel):
    x: int

    y: int

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionDrag(BaseModel):
    path: List[ActionOpenAITypesResponsesResponseComputerToolCallActionDragPath]

    type: Literal["drag"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionKeypress(BaseModel):
    keys: List[str]

    type: Literal["keypress"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionMove(BaseModel):
    type: Literal["move"]

    x: int

    y: int

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionScreenshot(BaseModel):
    type: Literal["screenshot"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionScroll(BaseModel):
    scroll_x: int

    scroll_y: int

    type: Literal["scroll"]

    x: int

    y: int

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionType(BaseModel):
    text: str

    type: Literal["type"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ActionOpenAITypesResponsesResponseComputerToolCallActionWait(BaseModel):
    type: Literal["wait"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


Action: TypeAlias = Union[
    ActionOpenAITypesResponsesResponseComputerToolCallActionClick,
    ActionOpenAITypesResponsesResponseComputerToolCallActionDoubleClick,
    ActionOpenAITypesResponsesResponseComputerToolCallActionDrag,
    ActionOpenAITypesResponsesResponseComputerToolCallActionKeypress,
    ActionOpenAITypesResponsesResponseComputerToolCallActionMove,
    ActionOpenAITypesResponsesResponseComputerToolCallActionScreenshot,
    ActionOpenAITypesResponsesResponseComputerToolCallActionScroll,
    ActionOpenAITypesResponsesResponseComputerToolCallActionType,
    ActionOpenAITypesResponsesResponseComputerToolCallActionWait,
]


class PendingSafetyCheck(BaseModel):
    id: str

    code: str

    message: str

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class OpenAIResponseComputerToolCall(BaseModel):
    id: str

    action: Action

    call_id: str

    pending_safety_checks: List[PendingSafetyCheck]

    status: Literal["in_progress", "completed", "incomplete"]

    type: Literal["computer_call"]

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
