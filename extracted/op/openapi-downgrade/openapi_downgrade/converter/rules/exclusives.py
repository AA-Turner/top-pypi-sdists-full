def fix_exclusive_min_max(spec):
    def recursive_fix(obj):
        if isinstance(obj, dict):
            if "exclusiveMinimum" in obj and isinstance(obj["exclusiveMinimum"], (int, float)):
                obj["minimum"] = obj["exclusiveMinimum"]
                obj["exclusiveMinimum"] = True

            if "exclusiveMaximum" in obj and isinstance(obj["exclusiveMaximum"], (int, float)):
                obj["maximum"] = obj["exclusiveMaximum"]
                obj["exclusiveMaximum"] = True

            for value in obj.values():
                recursive_fix(value)

        elif isinstance(obj, list):
            for item in obj:
                recursive_fix(item)

    recursive_fix(spec)
    return spec
