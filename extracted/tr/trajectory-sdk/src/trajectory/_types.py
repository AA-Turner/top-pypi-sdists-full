# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from collections.abc import Mapping
from typing import Literal, TypeVar


class NotGiven:
  def __bool__(self) -> Literal[False]:
    return False

  def __repr__(self) -> str:
    return "NOT_GIVEN"


not_given = NotGiven()


class Omit:
  def __bool__(self) -> Literal[False]:
    return False

  def __repr__(self) -> str:
    return "OMIT"


omit = Omit()


class PropertyInfo:
  def __init__(self, alias: str) -> None:
    self.alias = alias


Body = object
Query = Mapping[str, object]
Headers = Mapping[str, str | Omit]

_T = TypeVar("_T")
SequenceNotStr = list[_T] | tuple[_T, ...] | set[_T] | frozenset[_T]
