# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from collections.abc import Mapping
from datetime import date, datetime
from decimal import Decimal
from types import UnionType
from typing import Any, Literal, TypeVar, Union, get_args, get_origin
from uuid import UUID

import httpx
from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict, PrivateAttr, TypeAdapter, ValidationError

from trajectory._types import Headers, NotGiven, Query, not_given

ModelT = TypeVar("ModelT", bound="BaseModel")
PydanticModelT = TypeVar("PydanticModelT", bound=PydanticBaseModel)


class BaseModel(PydanticBaseModel):
  """Base class for every generated API response model."""

  model_config = ConfigDict(extra="allow", populate_by_name=True, defer_build=True)
  _request_id: str | None = PrivateAttr(default=None)

  def __str__(self) -> str:
    return f"{self.__repr_name__()}({self.__repr_str__(', ')})"  # type: ignore[misc]

  def to_dict(
    self,
    *,
    mode: Literal["json", "python"] = "python",
    use_api_names: bool = True,
    exclude_unset: bool = True,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    warnings: bool = True,
  ) -> dict[str, object]:
    return self.model_dump(
      mode=mode,
      by_alias=use_api_names,
      exclude_unset=exclude_unset,
      exclude_defaults=exclude_defaults,
      exclude_none=exclude_none,
      warnings=warnings,
    )

  def to_json(
    self,
    *,
    indent: int | None = 2,
    use_api_names: bool = True,
    exclude_unset: bool = True,
    exclude_defaults: bool = False,
    exclude_none: bool = False,
    warnings: bool = True,
  ) -> str:
    return self.model_dump_json(
      indent=indent,
      by_alias=use_api_names,
      exclude_unset=exclude_unset,
      exclude_defaults=exclude_defaults,
      exclude_none=exclude_none,
      warnings=warnings,
    )

  @classmethod
  def construct(
    cls: type[ModelT],
    _fields_set: set[str] | None = None,
    **values: object,
  ) -> ModelT:
    """Construct a response model recursively without rejecting schema drift."""
    return _construct_model(cls, values, _fields_set)


def _construct_model(
  model_type: type[PydanticModelT],
  values: Mapping[str, object],
  fields_set: set[str] | None = None,
) -> PydanticModelT:
  remaining = dict(values)
  fields = {}
  resolved_fields_set = set() if fields_set is None else set(fields_set)
  for name, field in model_type.model_fields.items():
    key = field.alias or name
    if key not in remaining and name in remaining:
      key = name
    if key in remaining:
      fields[name] = construct_type(remaining.pop(key), field.annotation)
      resolved_fields_set.add(name)
  return model_type.model_construct(
    _fields_set=resolved_fields_set,
    **fields,
    **remaining,
  )


def construct_type(value: object, type_: object) -> object:
  """Recursively build known response shapes without rejecting schema drift."""
  origin = get_origin(type_)
  arguments = get_args(type_)
  if origin in {Union, UnionType}:
    try:
      return TypeAdapter(type_).validate_python(value)
    except (TypeError, ValidationError):
      pass
    if value is None and type(None) in arguments:
      return None
    for candidate in arguments:
      if candidate is type(None):
        continue
      try:
        return construct_type(value, candidate)
      except (TypeError, ValueError):
        continue
    raise RuntimeError(f"Could not construct a response value as {type_}")
  if origin is list and isinstance(value, list):
    return [construct_type(item, arguments[0]) for item in value]
  if origin in {dict, Mapping} and isinstance(value, Mapping):
    return {key: construct_type(item, arguments[1]) for key, item in value.items()}

  model_type = origin or type_
  if isinstance(model_type, type) and issubclass(model_type, PydanticBaseModel):
    if not isinstance(value, Mapping):
      return value
    return _construct_model(model_type, value)

  if model_type is float and isinstance(value, int):
    converted = float(value)
    return converted if converted == value else value
  if model_type in {date, datetime, Decimal, UUID}:
    try:
      return TypeAdapter(model_type).validate_python(value)
    except (TypeError, ValidationError):
      return value
  return value


class FinalRequestOptions(PydanticBaseModel):
  """The fully resolved shape of one HTTP request, built right before it is sent."""

  model_config = ConfigDict(arbitrary_types_allowed=True)

  method: str
  url: str
  headers: Headers | None = None
  params: Query = {}
  timeout: float | httpx.Timeout | None | NotGiven = not_given
  content: Any = None
  files: Any = None
  json_data: Any = None  # not `json` - would incompatibly override BaseModel.json()
  extra_json: Mapping[str, Any] | None = None
  synthesize_event_and_data: bool = False

  @classmethod
  def construct(  # type: ignore[override]
    cls, *, method: str, url: str, **kwargs: Any
  ) -> "FinalRequestOptions":
    """Build one without validation, the way each client verb assembles a request."""
    return cls.model_construct(method=method, url=url, **kwargs)
