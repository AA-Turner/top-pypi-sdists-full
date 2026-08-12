# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = [
    "SearchMemoriesParams",
    "Filters",
    "FiltersOr",
    "FiltersOrOr",
    "FiltersOrOrFilterCondition",
    "FiltersOrOrOr",
    "FiltersOrOrAnd",
    "FiltersAnd",
    "FiltersAndAnd",
    "FiltersAndAndFilterCondition",
    "FiltersAndAndOr",
    "FiltersAndAndAnd",
    "Include",
]


class SearchMemoriesParams(TypedDict, total=False):
    q: Required[str]
    """Search query string"""

    aggregate: bool
    """
    If true, aggregates information from multiple memories to create new synthesized
    memories. The result will be a mix of aggregated and non-aggregated memories,
    reranked by relevance to the query. Works in conjunction with reranking.
    """

    container_tag: Annotated[str, PropertyInfo(alias="containerTag")]
    """Optional tag this search should be containerized by.

    This can be an ID for your user, a project ID, or any other identifier you wish
    to use to filter memories.
    """

    container_tags: Annotated[SequenceNotStr[str], PropertyInfo(alias="containerTags")]
    """Optional tags this search should be containerized by.

    Search is scoped to memories under these tags.
    """

    filepath: str
    """Filter search results by filepath.

    Exact match for full paths, prefix match if ending with /
    """

    filters: Filters
    """Optional filters to apply to the search. Can be a JSON string or Query object."""

    include: Include

    limit: int
    """Maximum number of results to return"""

    rerank: bool
    """If true, rerank the results based on the query.

    This is helpful if you want to ensure the most relevant results are returned.
    """

    rewrite_query: Annotated[bool, PropertyInfo(alias="rewriteQuery")]
    """If true, rewrites the query to make it easier to find documents.

    This increases the latency by about 400ms
    """

    search_mode: Annotated[Literal["memories", "hybrid", "documents"], PropertyInfo(alias="searchMode")]
    """Search mode.

    'memories' searches only memory entries (default). 'hybrid' searches both
    memories and document chunks. 'documents' searches only document chunks.
    """

    threshold: float
    """Threshold / sensitivity for memories selection.

    0 is least sensitive (returns most memories, more results), 1 is most sensitive
    (returns lesser memories, accurate results)
    """


class FiltersOrOrFilterCondition(TypedDict, total=False):
    """
    A single filter condition based on metadata, numeric values, array contents, or string matching
    """

    key: Required[str]

    value: Required[str]

    filter_type: Annotated[
        Literal["metadata", "numeric", "array_contains", "string_contains"], PropertyInfo(alias="filterType")
    ]

    ignore_case: Annotated[Union[bool, Literal["true", "false"]], PropertyInfo(alias="ignoreCase")]

    negate: Union[bool, Literal["true", "false"]]

    numeric_operator: Annotated[Literal[">", "<", ">=", "<=", "="], PropertyInfo(alias="numericOperator")]


class FiltersOrOrOr(TypedDict, total=False):
    or_: Required[Annotated[Iterable[object], PropertyInfo(alias="OR")]]
    """OR: Array of conditions or nested expressions"""


class FiltersOrOrAnd(TypedDict, total=False):
    and_: Required[Annotated[Iterable[object], PropertyInfo(alias="AND")]]
    """AND: Array of conditions or nested expressions"""


FiltersOrOr: TypeAlias = Union[FiltersOrOrFilterCondition, FiltersOrOrOr, FiltersOrOrAnd]


class FiltersOr(TypedDict, total=False):
    or_: Required[Annotated[Iterable[FiltersOrOr], PropertyInfo(alias="OR")]]
    """Array of OR filter expressions"""


class FiltersAndAndFilterCondition(TypedDict, total=False):
    """
    A single filter condition based on metadata, numeric values, array contents, or string matching
    """

    key: Required[str]

    value: Required[str]

    filter_type: Annotated[
        Literal["metadata", "numeric", "array_contains", "string_contains"], PropertyInfo(alias="filterType")
    ]

    ignore_case: Annotated[Union[bool, Literal["true", "false"]], PropertyInfo(alias="ignoreCase")]

    negate: Union[bool, Literal["true", "false"]]

    numeric_operator: Annotated[Literal[">", "<", ">=", "<=", "="], PropertyInfo(alias="numericOperator")]


class FiltersAndAndOr(TypedDict, total=False):
    or_: Required[Annotated[Iterable[object], PropertyInfo(alias="OR")]]
    """OR: Array of conditions or nested expressions"""


class FiltersAndAndAnd(TypedDict, total=False):
    and_: Required[Annotated[Iterable[object], PropertyInfo(alias="AND")]]
    """AND: Array of conditions or nested expressions"""


FiltersAndAnd: TypeAlias = Union[FiltersAndAndFilterCondition, FiltersAndAndOr, FiltersAndAndAnd]


class FiltersAnd(TypedDict, total=False):
    and_: Required[Annotated[Iterable[FiltersAndAnd], PropertyInfo(alias="AND")]]
    """Array of AND filter expressions"""


Filters: TypeAlias = Union[FiltersOr, FiltersAnd]


class Include(TypedDict, total=False):
    chunks: bool
    """DEPRECATED: Use searchMode='hybrid' instead.

    If true, automatically switches to hybrid mode. This field is kept for backward
    compatibility only.
    """

    documents: bool

    forgotten_memories: Annotated[bool, PropertyInfo(alias="forgottenMemories")]
    """If true, include forgotten memories in search results.

    Forgotten memories are memories that have been explicitly forgotten or have
    passed their expiration date.
    """

    related_memories: Annotated[bool, PropertyInfo(alias="relatedMemories")]

    summaries: bool
