from agilicus.agilicus_api import Oauth2Auth


def get_oauth2_auth(properties, pop=False):
    existing = properties.get("oauth2", {})
    # Find all oauth2_-prefixed items
    matched = []
    for key, value in properties.items():
        parts = key.split("oauth2_", 2)
        if len(parts) != 2:
            continue
        matched.append(key)
        if value is None:
            continue
        if isinstance(value, tuple):
            value = list(value)
        existing[parts[1]] = value

    if matched and pop:
        for key in matched:
            properties.pop(key)

    if not existing:
        return None

    return Oauth2Auth(**existing)
