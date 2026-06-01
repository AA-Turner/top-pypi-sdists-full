def convert_const(schema: dict) -> dict:
    if isinstance(schema, dict):
        if "const" in schema:
            schema["enum"] = [schema.pop("const")]
        for value in schema.values():
            convert_const(value)
    elif isinstance(schema, list):
        for item in schema:
            convert_const(item)
    return schema