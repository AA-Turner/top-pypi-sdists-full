"""Discover the API contracts of standalone arms installed on this host."""

from ..imports import http_json, os, read_json, urlsplit


def installed_arms(directory="/usr/share/hugpy/arms.d"):
    """Read local installer descriptors without importing arm runtimes."""
    if not os.path.isdir(directory):
        return {}
    arms = {}
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        try:
            entry = read_json(os.path.join(directory, name))
            upstream = urlsplit(entry["upstream"])
            arm = entry["arm"]
            categories = entry["categories"]
        except (OSError, ValueError, TypeError, KeyError):
            continue
        if (not isinstance(arm, str) or arm != name[:-5]
                or not isinstance(categories, list) or not all(isinstance(item, str) for item in categories)
                or upstream.scheme != "http" or upstream.hostname not in {"127.0.0.1", "::1"}
                or upstream.username is not None or upstream.password is not None
                or upstream.path not in {"", "/"} or upstream.query or upstream.fragment
                or entry.get("api_prefix") != "/api"):
            continue
        arms[arm] = entry
    return arms


def arm_routes(entry):
    """Read the Flask inspector, limited to categories owned by this arm."""
    categories = set(entry["categories"])
    try:
        status, rows = http_json(entry["upstream"].rstrip("/") + "/api/endpoints", timeout=1.0)
    except (OSError, ValueError):
        return None
    if status != 200 or not isinstance(rows, list):
        return None
    methods = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        path, verbs = row.get("url"), row.get("methods")
        if (not isinstance(path, str) or not path.startswith("/api/")
                or path.split("/", 3)[2] not in categories or not isinstance(verbs, list)):
            continue
        for verb in verbs:
            if verb in ("GET", "POST", "PATCH", "PUT", "DELETE"):
                methods.setdefault(path, set()).add(verb)
    return [{"path": path, "methods": sorted(verbs)} for path, verbs in sorted(methods.items())]
