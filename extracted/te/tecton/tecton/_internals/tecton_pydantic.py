"""A utility module for Pydantic usages in Tecton.

For compatibility reasons (see TEC-18028), Tecton cannot yet use Pydantic V2. Tecton will use Pydantic V1 whether the
user has V2 or V1 installed locally (in the case of V2 via using the `pydantic.v1` compat library). Tecton code should
reference pydantic solely through this module, e.g.

from tecton._internals.tecton_pydantic import pydantic_v1

This is enforced via pre-submits.

Additionally, this module contains some Pydantic utilities to bridge the gap between Pydantic V1 and V2, e.g. the
StrictModel.
"""

import datetime


try:
    from pydantic import v1 as pydantic_v1

    # Try importing pydantic.v1.fields to detect if this is pydantic 1.* or 2.*. Pydantic released a breaking change
    # in 1.10.17 to this module (https://github.com/pydantic/pydantic/pull/9660).
    # See https://tecton.atlassian.net/browse/CS-5142.
    from pydantic.v1 import fields
except ImportError:
    import pydantic as pydantic_v1
    from pydantic import fields

import sys
import typing
from typing import Any
from typing import Dict
from typing import Type

import typeguard
from typing_extensions import Final


if sys.version_info >= (3, 8):
    from typing import get_args
    from typing import get_origin
else:
    from typing_extensions import get_args
    from typing_extensions import get_origin


class _BannedAnnotationsMeta(type(pydantic_v1.BaseModel)):
    """Block Union annotations that may lead to unwanted type coercion, e.g. Union[str, int], at class definition time.

    Providing an integer to a field with the annotation 'Union[str, int]' would pass the strict type check, but
    pydantic would coerce the integer to string during model construction.
    """

    def __new__(cls, name: str, bases: tuple, namespace: Dict[str, Any], **kwargs: Any) -> Type[pydantic_v1.BaseModel]:
        annotations = namespace.get("__annotations__", {})
        for field_name, field_type in annotations.items():
            if _annotation_has_banned_union(field_type):
                msg = f"Invalid StrictModel annotation: {field_name}. Unions with Pydantic coercible types are not allowed."
                raise TypeError(msg)
        return super().__new__(cls, name, bases, namespace, **kwargs)


class StrictModel(pydantic_v1.BaseModel, metaclass=_BannedAnnotationsMeta):
    """A "strict" pydantic v1 model that blocks extra fields and most Pydantic v1 type coercion.

    Pydantic V1 will coerce values, e.g. coercing integers to datetimes or strings to integers. This generally an
    undesirable behavior for how we use Pydantic. (Pydantic V2 has built-in strict models.)
    """

    @pydantic_v1.validator("*", pre=True)
    def _validate_strict_type(cls, v, field):
        """Check value types before pydantic type coercion. Fails if types do not match according to Typeguard."""
        assert (
            field.annotation is not None
        ), f"Missing annotation for {field.name} for {cls}. StrictModel requires that all fields have annotations."

        if _field_has_model_type(field):
            # Skip strict type checking on nested models. These nested models will run their own type checking.
            # Using strict type checking on these nested models breaks Pydantic deserialization. (This workaround is
            # not needed with Pydantic V2 strict models.)
            return v

        # Some handling for forward references, this will only work for top-level ForwardRefs, e.g. won't work for
        # Optional["Foo"]. Typeguard V4 and/or Pydantic V2 have better options for forward references, but we can't use
        # those due to Python 3.7 and various compatibility issues.
        field_type = field.type_ if isinstance(field.annotation, typing.ForwardRef) else field.annotation

        try:
            typeguard.check_type(field.name, v, field_type)
        except TypeError:
            msg = f"Invalid type for {field.name}. Expected {field.annotation}. Got {v} ({type(v)})."
            raise TypeError(msg)

        return v

    class Config:
        # Do not allow extra attributes during model initialization, i.e. providing kwargs that were not declared
        # fields.
        extra: Final[str] = "forbid"


class StrictFrozenModel(StrictModel):
    """A strict, frozen (i.e. immutable) Pydantic V1 model. See StrictModel."""

    class Config:
        allow_mutation: Final[bool] = False


def _field_has_model_type(field: fields.ModelField) -> bool:
    """Returns true if the field is a pydantic model or contains a model within a Union."""

    def is_model_class(annotation: typing.Any) -> bool:
        # Must check that the annotation is a "type" (e.g. a class) because typing annotation (e.g. Union) are not
        # "types".
        return isinstance(annotation, type) and issubclass(annotation, pydantic_v1.BaseModel)

    if get_origin(field.annotation) is typing.Union:
        return any(is_model_class(arg) for arg in get_args(field.annotation))
    else:
        return is_model_class(field.annotation)


_BANNED_UNION_TYPES = (int, float, str, bool, datetime.datetime, datetime.timedelta)


def _annotation_has_banned_union(annotation: typing.Any) -> bool:
    """Returns true if the field has an unsafe Union - i.e. a Union where Pydantic V1 may attempt a coercion."""
    args = get_args(annotation)

    # For Unions, check if any of the arguments (i.e. 'Union[arg1, arg2, ...]' are banned types. Optional is allowed.
    if get_origin(annotation) is typing.Union:
        is_optional = len(args) == 2 and type(None) in args
        contained_banned_type = any(isinstance(arg, type) and arg in _BANNED_UNION_TYPES for arg in args)

        if contained_banned_type and not is_optional:
            return True

    # Recursively check nested types, e.g. Dict[str, Union[int, float]].
    return any(_annotation_has_banned_union(arg) for arg in args)
