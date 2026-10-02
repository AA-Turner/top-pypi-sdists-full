# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from __future__ import annotations

from collections.abc import Iterable, Mapping
from datetime import date, datetime
from decimal import Decimal
from types import UnionType
from typing import (
  Annotated,
  Any,
  Required,
  Union,
  cast,
  get_args,
  get_origin,
  get_type_hints,
  is_typeddict,
)
from uuid import UUID

from pydantic import BaseModel

from trajectory._types import NotGiven, Omit


class PropertyInfo:
  """Wire metadata attached to generated request fields."""

  def __init__(self, alias: str | None = None, format: str | None = None) -> None:
    self.alias = alias
    self.format = format


def maybe_transform(data: object, expected_type: object | None = None) -> Any:
  if expected_type is None:
    return _transform_value(data, None)
  return _transform_value(data, expected_type)


def _transform_value(
  data: object,
  annotation: object | None,
  inherited_property_info: PropertyInfo | None = None,
) -> object:
  if isinstance(data, (NotGiven, Omit)):
    return data
  annotation, property_info = _unwrap_annotation(annotation)
  property_info = property_info or inherited_property_info
  origin = get_origin(annotation)
  if origin in {Union, UnionType}:
    for member in get_args(annotation):
      data = _transform_value(data, member, property_info)
    return data
  if annotation is not None and is_typeddict(annotation) and isinstance(data, Mapping):
    return _transform_typed_dict(data, cast(type, annotation))
  if isinstance(data, BaseModel):
    return data.model_dump(mode="json", by_alias=True, exclude_unset=True)
  if isinstance(data, (Decimal, UUID)):
    return str(data)
  if isinstance(data, Mapping):
    value_type = (
      get_args(annotation)[1]
      if origin in {dict, Mapping} and len(get_args(annotation)) > 1
      else None
    )
    return {
      key: _transform_value(value, value_type)
      for key, value in data.items()
      if not isinstance(value, (NotGiven, Omit))
    }
  if isinstance(data, Iterable) and not isinstance(data, (str, bytes)):
    item_type = get_args(annotation)[0] if get_args(annotation) else None
    return [
      _transform_value(value, item_type)
      for value in data
      if not isinstance(value, (NotGiven, Omit))
    ]
  if property_info is not None and property_info.format == "iso8601":
    if isinstance(data, (date, datetime)):
      return data.isoformat()
  return data


def _transform_typed_dict(data: Mapping[str, object], expected_type: type) -> dict[str, object]:
  annotations = get_type_hints(expected_type, include_extras=True)
  transformed = {}
  for key, value in data.items():
    if isinstance(value, (NotGiven, Omit)):
      continue
    annotation = annotations.get(key)
    _, property_info = _unwrap_annotation(annotation)
    wire_name = property_info.alias if property_info is not None and property_info.alias else key
    transformed[wire_name] = _transform_value(value, annotation)
  return transformed


def _unwrap_annotation(annotation: object | None) -> tuple[object | None, PropertyInfo | None]:
  if annotation is None:
    return None, None
  origin = get_origin(annotation)
  if origin is Required:
    return _unwrap_annotation(get_args(annotation)[0])
  if origin is Annotated:
    underlying, *metadata = get_args(annotation)
    property_info = next((item for item in metadata if isinstance(item, PropertyInfo)), None)
    return underlying, property_info
  return annotation, None
