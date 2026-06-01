def convert_examples(schema: dict) -> dict:
    if isinstance(schema, dict):
        if "examples" in schema and isinstance(schema["examples"], list):
            if schema["examples"]:
                schema["example"] = schema["examples"][0]
            del schema["examples"]
        for value in schema.values():
            convert_examples(value)
    elif isinstance(schema, list):
        for item in schema:
            convert_examples(item)
    return schema
