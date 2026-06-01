def fix_booleans(obj):
    if isinstance(obj, dict):
        for key in list(obj.keys()):
            val = obj[key]
            if isinstance(val, str) and val.lower() in ["true", "false"]:
                obj[key] = val.lower() == "true"
            elif isinstance(val, (dict, list)):
                obj[key] = fix_booleans(val)
    elif isinstance(obj, list):
        return [fix_booleans(item) for item in obj]
    return obj
