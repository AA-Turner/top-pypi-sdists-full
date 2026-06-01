def convert_nullable(schema: dict) -> dict:
    if isinstance(schema, dict):
        for key, value in list(schema.items()):
            if key == "type" and isinstance(value, list) and "null" in value:
                value = [t for t in value if t != "null"]
                schema["type"] = value[0] if len(value) == 1 else value
                schema["nullable"] = True
            else:
                convert_nullable(value)
    elif isinstance(schema, list):
        for item in schema:
            convert_nullable(item)
    return schema
