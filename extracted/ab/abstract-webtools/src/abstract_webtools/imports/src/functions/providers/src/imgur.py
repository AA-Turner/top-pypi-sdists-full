IMGUR_HOSTS = {"imgur.com", "i.imgur.com"}

def detect_imgur(parsed):
    net = parsed.netloc.lower()
    if net not in IMGUR_HOSTS:
        return None

    ext = os.path.splitext(parsed.path)[1].lower()
    if ext:
        return {"downloadable": True, "kind": "image", "provider": "imgur",
                "id": parsed.path.strip("/"), "direct": True}

    return {"downloadable": False, "provider": "imgur"}
