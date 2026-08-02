TRUE_STRINGS = {"1", "true", "yes", "on"}
FALSE_STRINGS = {"0", "false", "no", "off"}


def str_to_bool(value: str, *, default: bool = False) -> bool:
    normalized_value = value.strip().lower()
    if normalized_value in TRUE_STRINGS:
        return True
    if normalized_value in FALSE_STRINGS:
        return False
    return default
