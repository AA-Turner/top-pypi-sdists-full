# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["FieldExtractorUpdateParams", "Rule", "RuleField"]


class FieldExtractorUpdateParams(TypedDict, total=False):
    account_id: Required[str]
    """Cloudflare account ID."""

    rules: Required[Iterable[Rule]]


class RuleField(TypedDict, total=False):
    expression: Required[str]

    name: Required[str]


class Rule(TypedDict, total=False):
    fields: Required[Iterable[RuleField]]

    ref: Required[str]

    description: str
