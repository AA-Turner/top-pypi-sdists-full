GIPHY_HOSTS = {"giphy.com", "media.giphy.com"}

def detect_giphy(parsed):
    if parsed.netloc.lower() not in GIPHY_HOSTS:
        return None

    # gifs have direct .gif or mp4 endpoints
    if parsed.path.endswith(".gif") or parsed.path.endswith(".mp4"):
        return {"downloadable": True, "kind": "image", "provider": "giphy",
                "id": parsed.path.strip("/"), "direct": True}

    return {"downloadable": False, "provider": "giphy"}
