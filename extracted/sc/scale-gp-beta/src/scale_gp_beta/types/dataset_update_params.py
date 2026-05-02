# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from .._types import SequenceNotStr
from .restore_request_param import RestoreRequestParam

__all__ = ["DatasetUpdateParams", "Dataset", "DatasetPartialDatasetRequestBase"]


class DatasetUpdateParams(TypedDict, total=False):
    dataset: Required[Dataset]


class DatasetPartialDatasetRequestBase(TypedDict, total=False):
    description: str

    name: str

    tags: SequenceNotStr[str]
    """The tags associated with the entity"""


Dataset: TypeAlias = Union[DatasetPartialDatasetRequestBase, RestoreRequestParam]
