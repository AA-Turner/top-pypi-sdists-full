def model_enum_to_list(cls):
    allowed = getattr(cls, "allowed_values", None)
    if not allowed or not isinstance(allowed, dict):
        return []

    values = allowed.get(("value",))
    if not values or not isinstance(values, dict):
        return []

    return list(values.values())
