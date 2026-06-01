VIMEO_HOSTS = {"vimeo.com", "www.vimeo.com"}

def detect_vimeo(parsed):
    if parsed.netloc.lower() not in VIMEO_HOSTS:
        return None

    vid = parsed.path.strip("/")
    if vid.isdigit():
        return {"downloadable": True, "kind": "video", "provider": "vimeo",
                "id": vid, "direct": False}

    return {"downloadable": False, "provider": "vimeo"}
