NULL_RESOURCE_ARG = "null"
"""Value a grant uses for a nullable arg when there is no id to name."""


def normalize_resource_arg(value: str) -> str:
    """Queried args come from f-strings, so a `None` id arrives as Python's `str(None)`.
    It means the same "no id to name" that NULL_RESOURCE_ARG does. Grants are unaffected —
    they never pass through here, so `null` stays their only spelling."""
    return NULL_RESOURCE_ARG if value == "None" else value
