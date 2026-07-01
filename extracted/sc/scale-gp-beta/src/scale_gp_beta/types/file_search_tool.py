# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = [
    "FileSearchTool",
    "Filters",
    "FiltersComparisonFilter",
    "FiltersCompoundFilter",
    "FiltersCompoundFilterFilter",
    "FiltersCompoundFilterFilterComparisonFilter",
    "RankingOptions",
    "RankingOptionsHybridSearch",
]


class FiltersComparisonFilter(BaseModel):
    """
    A filter used to compare a specified attribute key to a given value using a defined comparison operation.
    """

    key: str

    type: Literal["eq", "ne", "gt", "gte", "lt", "lte"]

    value: Union[str, float, bool, List[Union[str, float]]]

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


class FiltersCompoundFilterFilterComparisonFilter(BaseModel):
    """
    A filter used to compare a specified attribute key to a given value using a defined comparison operation.
    """

    key: str

    type: Literal["eq", "ne", "gt", "gte", "lt", "lte"]

    value: Union[str, float, bool, List[Union[str, float]]]

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


FiltersCompoundFilterFilter: TypeAlias = Union[FiltersCompoundFilterFilterComparisonFilter, object]


class FiltersCompoundFilter(BaseModel):
    """Combine multiple filters using `and` or `or`."""

    filters: List[FiltersCompoundFilterFilter]

    type: Literal["and", "or"]

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


Filters: TypeAlias = Union[FiltersComparisonFilter, FiltersCompoundFilter]


class RankingOptionsHybridSearch(BaseModel):
    """
    Weights that control how reciprocal rank fusion balances semantic embedding matches versus sparse keyword matches when hybrid search is enabled.
    """

    embedding_weight: float

    text_weight: float

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


class RankingOptions(BaseModel):
    """Ranking options for search."""

    hybrid_search: Optional[RankingOptionsHybridSearch] = None
    """
    Weights that control how reciprocal rank fusion balances semantic embedding
    matches versus sparse keyword matches when hybrid search is enabled.
    """

    ranker: Optional[Literal["auto", "default-2024-11-15"]] = None

    score_threshold: Optional[float] = None

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


class FileSearchTool(BaseModel):
    """A tool that searches for relevant content from uploaded files.

    Learn more about the [file search tool](https://platform.openai.com/docs/guides/tools-file-search).
    """

    type: Literal["file_search"]

    vector_store_ids: List[str]

    filters: Optional[Filters] = None
    """
    A filter used to compare a specified attribute key to a given value using a
    defined comparison operation.
    """

    max_num_results: Optional[int] = None

    ranking_options: Optional[RankingOptions] = None
    """Ranking options for search."""

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
