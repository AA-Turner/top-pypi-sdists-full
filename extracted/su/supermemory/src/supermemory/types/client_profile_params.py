# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union, Iterable
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = [
    "ClientProfileParams",
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


class ClientProfileParams(TypedDict, total=False):
    container_tag: Required[Annotated[str, PropertyInfo(alias="containerTag")]]
    """Tag to filter the profile by.

    This can be an ID for your user, a project ID, or any other identifier you wish
    to use to filter memories.
    """

    buckets: SequenceNotStr[str]
    """Specific bucket keys to return.

    Omit to return all configured buckets. Only relevant when "buckets" is included.
    """

    filters: Filters
    """Optional metadata filters to apply to profile results and search results.

    Supports complex AND/OR queries with multiple conditions.
    """

    include: List[Literal["static", "dynamic", "buckets"]]
    """Profile sections to return.

    Omit to return all sections. Pass a subset to reduce payload — e.g. ["buckets"]
    skips static and dynamic entirely.
    """

    q: str
    """Optional search query to include search results in the response"""

    threshold: float
    """Threshold for search results.

    Only results with a score above this threshold will be included.
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
