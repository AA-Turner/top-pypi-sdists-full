TENOR_HOSTS = {"tenor.com", "www.tenor.com"}

def detect_tenor(parsed):
    if parsed.netloc.lower() not in TENOR_HOSTS:
        return None

    parts = parsed.path.split("/")
    if len(parts) > 2 and parts[-1].isdigit():
        return {"downloadable": True, "kind": "image", "provider": "tenor",
                "id": parts[-1], "direct": False}

    return {"downloadable": False, "provider": "tenor"}
