def fix_null_type(spec):
    def recurse(obj):
        if isinstance(obj, dict):
            # Fix cases where "type": "null"
            if obj.get("type") == "null":
                obj.pop("type")
                obj["nullable"] = True

            # Fix within anyOf/oneOf/allOf
            for key in ["anyOf", "oneOf", "allOf"]:
                if key in obj and isinstance(obj[key], list):
                    for item in obj[key]:
                        recurse(item)

            for v in obj.values():
                recurse(v)

        elif isinstance(obj, list):
            for item in obj:
                recurse(item)

    recurse(spec)
    return spec
