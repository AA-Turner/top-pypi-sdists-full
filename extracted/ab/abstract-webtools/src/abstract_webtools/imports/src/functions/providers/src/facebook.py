FACEBOOK_HOSTS = {"facebook.com", "www.facebook.com", "m.facebook.com", "fb.watch"}

def detect_facebook(parsed):
    net = parsed.netloc.lower()
    if net not in FACEBOOK_HOSTS:
        return None

    parts = [p for p in parsed.path.split("/") if p]

    if len(parts) >= 3 and parts[0] == "share" and parts[1] == "v":
        return {"downloadable": True, "kind": "video", "provider": "facebook",
                "id": parts[2], "direct": False}

    if net == "fb.watch":
        vid = parsed.path.strip("/")
        return {"downloadable": True, "kind": "video", "provider": "facebook",
                "id": vid, "direct": False}

    return {"downloadable": False, "provider": "facebook"}
