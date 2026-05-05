# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "OpenAIResponseFunctionWebSearch",
    "Action",
    "ActionOpenAITypesResponsesResponseFunctionWebSearchActionSearch",
    "ActionOpenAITypesResponsesResponseFunctionWebSearchActionSearchSource",
    "ActionOpenAITypesResponsesResponseFunctionWebSearchActionOpenPage",
    "ActionActionFind",
]


class ActionOpenAITypesResponsesResponseFunctionWebSearchActionSearchSource(BaseModel):
    """A source used in the search."""

    type: Literal["url"]

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


class ActionOpenAITypesResponsesResponseFunctionWebSearchActionSearch(BaseModel):
    """Action type "search" - Performs a web search query."""

    query: str

    type: Literal["search"]

    queries: Optional[List[str]] = None

    sources: Optional[List[ActionOpenAITypesResponsesResponseFunctionWebSearchActionSearchSource]] = None

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
    """Action type "open_page" - Opens a specific URL from search results."""

    type: Literal["open_page"]

    url: Optional[str] = None

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


class ActionActionFind(BaseModel):
    """Action type "find_in_page": Searches for a pattern within a loaded page."""

    pattern: str

    type: Literal["find_in_page"]

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
    ActionActionFind,
]


class OpenAIResponseFunctionWebSearch(BaseModel):
    """The results of a web search tool call.

    See the
    [web search guide](https://platform.openai.com/docs/guides/tools-web-search) for more information.
    """

    id: str

    action: Action
    """Action type "search" - Performs a web search query."""

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
