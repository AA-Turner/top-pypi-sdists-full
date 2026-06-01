def emulate_tuple_items(schema: dict, warnings: list = None) -> dict:
    if warnings is None:
        warnings = []

    if isinstance(schema, dict):
        if schema.get("type") == "array":
            items_list = None
            if isinstance(schema.get("prefixItems" ), list):
                items_list = schema.pop("prefixItems")
                warnings.add("Tuple-style 'prefixItems' detected; emulating using 'x-tuple-items'.")
                if "items" not in schema:
                    schema["items"] = {} # Allow additional items
            elif isinstance(schema.get("items"), list):
                items_list = schema.pop("items")
                warnings.add("Tuple-style 'items' array detected; emulating using 'x-tuple-items'.")
                schema["items"] = {} # Allow additional items

            if items_list:
                schema.setdefault("minItems", len(items_list))
                schema.setdefault("maxItems", len(items_list))

                # Add custom vendor extension to preserve logic
                schema["x-tuple-items"] = []
                for idx, item_schema in enumerate(items_list):
                    schema["x-tuple-items"].append({"index": idx, **item_schema})

        for value in schema.values():
            emulate_tuple_items(value, warnings)
    elif isinstance(schema, list):
        for item in schema:
            emulate_tuple_items(item, warnings)

    return schema
