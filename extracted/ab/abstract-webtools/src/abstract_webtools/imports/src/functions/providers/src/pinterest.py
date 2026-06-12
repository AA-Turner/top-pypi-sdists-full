PINTEREST_HOSTS = {"pinterest.com", "www.pinterest.com"}

def detect_pinterest(parsed):
    if parsed.netloc.lower() not in PINTEREST_HOSTS:
        return None

    parts = parsed.path.split("/")
    if len(parts) > 2 and parts[1] == "pin":
        return {"downloadable": True, "kind": "image", "provider": "pinterest",
                "id": parts[2], "direct": False}

    return {"downloadable": False, "provider": "pinterest"}
