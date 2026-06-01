from typing import Any, Dict, Union

import attrs
import jsonschema


def filter_fields(obj: Dict[str, Any], t: Any):
    return {k: v for k, v in obj.items() if k in attrs.fields_dict(t)}


def typ(t: Any, **kwargs) -> Any:
    return attrs.field(converter=lambda obj: t(**filter_fields(obj, t)), **kwargs)


def typ_or_none(t: Any, **kwargs) -> Union[Any, None]:
    return attrs.field(
        converter=lambda obj: t(**filter_fields(obj, t)) if obj is not None else None,
        default=None,
        **kwargs,
    )


def _check_parameters_schema(obj, attribute, value):
    try:
        jsonschema.Draft202012Validator.check_schema(value)
    except jsonschema.SchemaError as e:
        raise ValueError(f"Invalid parameters schema for tool {obj.name}") from e
