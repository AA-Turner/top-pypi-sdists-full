from datetime import datetime
import os
import re


def gen_valid_name(prefix: str = "autogenerated") -> str:
    """Generate a name for anyscale resources."""
    INVALID_NAME_REGEX_PATTERN = r"[^A-Za-z0-9_-]"

    generated_name = f"{prefix}-{datetime.now().isoformat()}"
    generated_name = re.sub(INVALID_NAME_REGEX_PATTERN, "-", generated_name)
    return generated_name


def get_full_name():
    """Gets the full name of the user as a lowercase `snake_case` string.
    Uses the Linux username if full name is not available.

    If still not available, returns `"default"`.

    eg. `get_full_name() -> "john_doe"`
    """
    full_name = (
        os.getenv("ANYSCALE_USERNAME")
        or os.getenv("USERNAME")
        or os.getenv("USER")
        or "default"
    )
    # Join the full name with underscores
    full_name = "_".join(full_name.split())
    # Lowercase the full name
    full_name = full_name.lower()
    return full_name
