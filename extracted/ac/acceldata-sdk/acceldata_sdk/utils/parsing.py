# acceldata_sdk/utils/parsing.py

def str_to_bool(value: str) -> bool:
    """
    Convert a string representation of truth to boolean.

    Accepted true values:
        '1', 'true', 'yes', 'y', 'on'

    Accepted false values:
        '0', 'false', 'no', 'n', 'off'

    Raises:
        ValueError if value is not a valid boolean string.
    """
    val = value.strip().lower()

    if val in {"1", "true", "yes", "y", "on"}:
        return True
    if val in {"0", "false", "no", "n", "off"}:
        return False

    raise ValueError(f"Invalid boolean value: {value}")
