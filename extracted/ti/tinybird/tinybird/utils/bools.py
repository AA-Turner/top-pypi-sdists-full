TRUE_VALUES = {"y", "yes", "t", "true", "on", "1"}
FALSE_VALUES = {"n", "no", "f", "false", "off", "0"}


def parse_bool(value: object) -> bool:
    normalized_value = str(value).strip().lower()
    if normalized_value in TRUE_VALUES:
        return True
    if normalized_value in FALSE_VALUES:
        return False
    raise ValueError(f"invalid truth value {value!r}")


def parse_optional_bool(value: object, default: bool = False) -> bool:
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return value
    return parse_bool(value)
