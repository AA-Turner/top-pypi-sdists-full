def resolve_object(data: dict, resolve: str):
    try:
        resolved = data.get(resolve)
        if resolved:
            return resolved
        else:
            return data
    except AttributeError:
        return data
