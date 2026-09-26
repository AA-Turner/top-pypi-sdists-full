# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from ...._types import SequenceNotStr

__all__ = ["ApplicationCreateParams", "Variant0", "Variant1"]


class Variant0(TypedDict, total=False):
    account_id: Required[str]

    hostnames: Required[SequenceNotStr[str]]
    """Hostnames matched by the application."""

    category_id: int
    """Returns the category ID."""

    human_id: str
    """Returns the human readable ID."""

    ip_subnets: SequenceNotStr[str]
    """IP subnets for this application.

    Custom application create and update requests accept IPv4 prefix lengths /8
    through /32 and IPv6 prefix lengths /32 through /128.
    """

    name: str
    """Returns the application name."""

    port_protocols: SequenceNotStr[str]
    """Port and protocol pairs matched by the application."""

    support_domains: SequenceNotStr[str]
    """Support domains matched by the application."""


class Variant1(TypedDict, total=False):
    account_id: Required[str]

    ip_subnets: Required[SequenceNotStr[str]]
    """IP subnets for this application.

    Custom application create and update requests accept IPv4 prefix lengths /8
    through /32 and IPv6 prefix lengths /32 through /128.
    """

    category_id: int
    """Returns the category ID."""

    hostnames: SequenceNotStr[str]
    """Hostnames matched by the application."""

    human_id: str
    """Returns the human readable ID."""

    name: str
    """Returns the application name."""

    port_protocols: SequenceNotStr[str]
    """Port and protocol pairs matched by the application."""

    support_domains: SequenceNotStr[str]
    """Support domains matched by the application."""


ApplicationCreateParams: TypeAlias = Union[Variant0, Variant1]
