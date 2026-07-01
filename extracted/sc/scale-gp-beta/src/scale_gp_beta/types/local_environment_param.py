# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

__all__ = ["LocalEnvironmentParam", "Skill"]


class Skill(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    description: Required[str]

    name: Required[str]

    path: Required[str]


class LocalEnvironmentParam(TypedDict, total=False, extra_items=object):  # type: ignore[call-arg]
    type: Required[Literal["local"]]

    skills: Iterable[Skill]
