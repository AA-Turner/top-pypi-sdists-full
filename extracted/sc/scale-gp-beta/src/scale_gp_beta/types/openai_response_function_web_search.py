# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, Union
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "OpenAIResponseFunctionWebSearch",
    "Action",
    "ActionOpenAITypesResponsesResponseFunctionWebSearchActionSearch",
    "ActionOpenAITypesResponsesResponseFunctionWebSearchActionOpenPage",
    "ActionOpenAITypesResponsesResponseFunctionWebSearchActionFind",
]


class ActionOpenAITypesResponsesResponseFunctionWebSearchActionSearch(BaseModel):
    query: str

    type: Literal["search"]

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


class ActionOpenAITypesResponsesResponseFunctionWebSearchActionOpenPage(BaseModel):
    type: Literal["open_page"]

    url: str

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


class ActionOpenAITypesResponsesResponseFunctionWebSearchActionFind(BaseModel):
    pattern: str

    type: Literal["find"]

    url: str

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
    ActionOpenAITypesResponsesResponseFunctionWebSearchActionSearch,
    ActionOpenAITypesResponsesResponseFunctionWebSearchActionOpenPage,
    ActionOpenAITypesResponsesResponseFunctionWebSearchActionFind,
]


class OpenAIResponseFunctionWebSearch(BaseModel):
    id: str

    action: Action

    status: Literal["in_progress", "searching", "completed", "failed"]

    type: Literal["web_search_call"]

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
