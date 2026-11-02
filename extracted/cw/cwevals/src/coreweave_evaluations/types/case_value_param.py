# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import TypeAlias

from .case_field_value_param import CaseFieldValueParam

__all__ = ["CaseValueParam"]

CaseValueParam: TypeAlias = Union[Dict[str, CaseFieldValueParam], bool, float, str, Iterable[object]]
