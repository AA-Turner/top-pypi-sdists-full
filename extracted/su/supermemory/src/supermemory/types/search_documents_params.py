# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = [
    "SearchDocumentsParams",
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
]


class SearchDocumentsParams(TypedDict, total=False):
    q: Required[str]
    """Search query string"""

    categories_filter: Annotated[SequenceNotStr[str], PropertyInfo(alias="categoriesFilter")]
    """DEPRECATED: Optional category filters"""

    chunk_threshold: Annotated[float, PropertyInfo(alias="chunkThreshold")]
    """Threshold / sensitivity for chunk selection.

    0 is least sensitive (returns most chunks, more results), 1 is most sensitive
    (returns lesser chunks, accurate results)
    """

    container_tag: Annotated[str, PropertyInfo(alias="containerTag")]
    """Optional single container tag. Use this or containerTags."""

    container_tags: Annotated[SequenceNotStr[str], PropertyInfo(alias="containerTags")]
    """Optional tags this search should be containerized by.

    This can be an ID for your user, a project ID, or any other identifier you wish
    to use to filter documents.
    """

    doc_id: Annotated[str, PropertyInfo(alias="docId")]
    """Optional document ID to search within.

    You can use this to find chunks in a very large document.
    """

    document_threshold: Annotated[float, PropertyInfo(alias="documentThreshold")]
    """DEPRECATED: This field is no longer used in v3 search.

    The search now uses chunkThreshold only. This parameter will be ignored.
    """

    filepath: str
    """Filter search results by filepath.

    Exact match for full paths, prefix match if ending with /
    """

    filters: Filters
    """Optional filters to apply to the search. Can be a JSON string or Query object."""

    include_full_docs: Annotated[bool, PropertyInfo(alias="includeFullDocs")]
    """If true, include full document in the response.

    This is helpful if you want a chatbot to know the full context of the document.
    """

    include_summary: Annotated[bool, PropertyInfo(alias="includeSummary")]
    """If true, include document summary in the response.

    This is helpful if you want a chatbot to know the full context of the document.
    """

    limit: int
    """Maximum number of results to return"""

    only_matching_chunks: Annotated[bool, PropertyInfo(alias="onlyMatchingChunks")]
    """If true, only return matching chunks without context.

    Normally, we send the previous and next chunk to provide more context for LLMs.
    If you only want the matching chunk, set this to true.
    """

    rerank: bool
    """If true, rerank the results based on the query.

    This is helpful if you want to ensure the most relevant results are returned.
    """

    rewrite_query: Annotated[bool, PropertyInfo(alias="rewriteQuery")]
    """If true, rewrites the query to make it easier to find documents.

    This increases the latency by about 400ms
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
