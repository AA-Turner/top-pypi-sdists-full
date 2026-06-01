def conditionals_to_oneof(schema: dict) -> dict:
    def transform(current_schema):
        if not isinstance(current_schema, dict):
            return current_schema

        # First, recurse into children
        # Iterate over a copy of items to avoid issues if current_schema is modified
        for key, value in list(current_schema.items()):
            if isinstance(value, dict):
                current_schema[key] = transform(value)
            elif isinstance(value, list):
                current_schema[key] = [transform(v) if isinstance(v, dict) else v for v in value]

        # Now, process the current schema for 'if/then/else'
        if "if" in current_schema and ("then" in current_schema or "else" in current_schema):
            if_cond = current_schema.get("if", {})
            then_cond = current_schema.get("then", {})
            else_cond = current_schema.get("else", {})

            # Basic check: if condition is based on a constant property
            props = if_cond.get("properties", {})
            if len(props) == 1:
                prop, condition = next(iter(props.items()))
                if "const" in condition:
                    const_value = condition["const"]

                    then_schema = {
                        "required": then_cond.get("required", []) + [prop],
                        "properties": {
                            **then_cond.get("properties", {}),
                            prop: {"enum": [const_value]},
                        }
                    }

                    else_schema = {
                        "required": else_cond.get("required", []) + [prop],
                        "properties": {
                            **else_cond.get("properties", {}),
                            prop: {"not": {"const": const_value}},
                        }
                    }

                    current_schema.pop("if", None)
                    current_schema.pop("then", None)
                    current_schema.pop("else", None)
                    current_schema["oneOf"] = [then_schema, else_schema]
                else:
                    current_schema["x-original-conditionals"] = {
                        "if": current_schema.pop("if"),
                        "then": current_schema.pop("then", None),
                        "else": current_schema.pop("else", None)
                    }
            else:
                current_schema["x-original-conditionals"] = {
                    "if": current_schema.pop("if"),
                    "then": current_schema.pop("then", None),
                    "else": current_schema.pop("else", None)
                }

        return current_schema

    return transform(schema)
