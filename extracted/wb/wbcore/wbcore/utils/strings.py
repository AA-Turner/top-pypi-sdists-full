import json
from functools import reduce


def enumerated_string_join(array):
    """Generates a human readable string out of a list"""

    if len(array) > 0:
        casted_array = [str(i) for i in array]
        return (
            " and ".join([", ".join(casted_array[:-1]), casted_array[-1]])
            if len(casted_array) > 1
            else casted_array[0]
        )
    return ""


def format_number(number, decimal: int = 2, **kwargs) -> float | str:
    """
    utility function used to serialize an aggregate to a json compatible value
    Args:
        number: Number to serialize
        **kwargs: backward compatibility keyword argument

    Returns:

    """
    try:
        return float(round(number, decimal))
    except TypeError:
        return ""


class ReferenceIDMixin:
    @property
    def reference_id(self):
        return f"{self.id:06}"


def convert_str_to_boolean(fake_bool: str | bool) -> bool:
    """
    Converts any bool or str to a boolean - can throw JSONDecodeError
    """
    return json.loads(str(fake_bool).lower())


def snake_case_to_human(s: str) -> str:
    words = s.split("_")
    human_readable = " ".join(word.capitalize() for word in words)
    return human_readable


def camel_to_snake_case(s: str) -> str:
    """
    Convert a string as CamelCase to snake_case
    """
    return reduce(lambda x, y: x + ("_" if y.isupper() else "") + y, s).lower()


def get_aggregate_symbol(aggregate: str) -> str:
    match aggregate.lower():
        case "avg":
            return "μ"
        case "count":
            return "#"
        case "max":
            return "⋁"
        case "min":
            return "⋀"
        case "stddev":
            return "σ"
        case "sum":
            return "Σ"
        case "variance":
            return "σ2"
        case _:
            return aggregate
