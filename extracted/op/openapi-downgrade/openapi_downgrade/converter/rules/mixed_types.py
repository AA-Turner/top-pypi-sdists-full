def convert_mixed_types(schema: dict) -> dict:
    """
    Converts schemas with mixed types (e.g., type: ["string", "number"])
    into a 'oneOf' structure for OpenAPI 3.0 compatibility.

    This rule should run *after* 'convert_nullable' has extracted "null"
    and applied the "nullable: true" field.
    """
    if isinstance(schema, dict):
        # Recurse into sub-schemas first
        for value in schema.values():
            convert_mixed_types(value)

        # Now process the current schema object
        if "type" in schema and isinstance(schema["type"], list):
            types = schema["type"]
            if len(types) > 1:
                schema["oneOf"] = [{"type": t} for t in types]
                del schema["type"]

    elif isinstance(schema, list):
        # Recurse into list items
        for item in schema:
            convert_mixed_types(item)

    return schema
