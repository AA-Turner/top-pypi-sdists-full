def require_activity_context_value(value: str | None, *, field_name: str) -> str:
    if value is None:
        raise RuntimeError(f"Temporal activity info is missing {field_name}")
    return value
