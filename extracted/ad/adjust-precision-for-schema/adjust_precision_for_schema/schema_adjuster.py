"""The purpose of this module is to adjust the decimal library's precision to match a schema's maximum precision

This is particularly useful in singer-io and meltano runs, because most targets validate the schema from a tap

The example use case is tap-mongodb produces a schema where multipleOf = 1e-34, but the default precision of the
decimal library is 28. """
from decimal import Decimal
import decimal
import math
import logging as logger


def calc_digits(num):
    """Calculates the total number of digits required to store a number"""
    v = abs(Decimal(num or 1)).log10()
    if v < 0:
        precision = round(math.floor(v))
    else:
        precision = round(math.ceil(v))
    return abs(precision)


def get_schema_precision(minimum=1, maximum=1, multiple_of=1):
    """Returns a tuple where scale = the number of significant digits and digits = the number of decimal places"""
    scale = calc_digits(multiple_of)
    digits = max(calc_digits(minimum), calc_digits(maximum))
    return scale, digits


def numeric_schema_with_precision(schema):
    """Returns true if the property type is a numeric type that involves precision"""
    if "type" not in schema:
        return False
    if isinstance(schema["type"], list):
        if "number" not in schema["type"]:
            return False
    elif schema["type"] != "number":
        return False
    if "multipleOf" in schema:
        return True
    return "minimum" in schema or "maximum" in schema


def adjust_decimal_precision_for_schema(schema, context=None):
    """Adjust the decimal context's precision based on the precision specified in the JSON schema
    For example, the default precision is 28 characters (significant digits + decimal places),
    but MongoDB handles 34 decimal places. This will increase the context's precision to 34 to handle the schema"""
    if not context:
        context = decimal.getcontext()
    if isinstance(schema, list):
        for v in schema:
            adjust_decimal_precision_for_schema(v)
    elif isinstance(schema, dict):
        if numeric_schema_with_precision(schema):
            scale, digits = get_schema_precision(
                minimum=schema.get("minimum"),
                maximum=schema.get("maxium"),
                multiple_of=schema.get("multipleOf"),
            )
            precision = 2 + digits + scale
            if context.prec < precision:
                logger.debug("Setting decimal precision to {}".format(precision))
                context.prec = precision
        else:
            for v in schema.values():
                adjust_decimal_precision_for_schema(v)
