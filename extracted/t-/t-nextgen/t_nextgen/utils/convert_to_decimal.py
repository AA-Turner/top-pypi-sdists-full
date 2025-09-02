from decimal import Decimal
from typing import Any
import re


def convert_to_decimal(str_value: Any, empty: bool = False) -> Decimal:
    """The function `convert_to_decimal` takes a string input, removes non-numeric characters.

    Returns a Decimal value, handling exceptions by returning 0.0 if conversion fails.

    Returns:
        Decimal: Returns a Decimal value after converting the input `str_value` to a Decimal
    """
    if empty and not str_value:  # there are places where we need an empty value instead of turn it to 0.0
        return str_value
    if isinstance(str_value, str):
        str_value = str_value.replace(",", "")
        # This regex will match numbers inside () -> we are getting it in the qty/charge
        parenthesis_pattern = r"\(([-+]?\d+)\)"
        dollar_pattern = r"\$"
        combined_pattern = f"{parenthesis_pattern}|{dollar_pattern}"
        str_value = re.sub(combined_pattern, "", str_value)
        str_value = str_value.translate(str.maketrans("", "", "()"))
        str_value = str_value.replace(" ", "")
        if str_value == "":
            return Decimal("0.0")
    return Decimal(str(str_value))
