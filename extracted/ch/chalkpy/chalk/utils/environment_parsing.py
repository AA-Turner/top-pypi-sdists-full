import os

_TRUTHY_VALUES = {"1", "true", "yes", "t", "y"}
_FALSY_VALUES = {"0", "false", "no", "f", "n"}


def env_var_bool(env_name: str, default: bool = False) -> bool:
    var = os.environ.get(env_name)
    # Treat unset or empty environment variables as missing, and fall back to the default.
    if var is None or var == "":
        return default
    if var.lower() in _TRUTHY_VALUES:
        return True
    if var.lower() in _FALSY_VALUES:
        return False
    raise ValueError(
        f"Environ '{env_name}' is set to '{var}', which cannot be converted to a boolean value. Please set to '0' or '1'."
    )
