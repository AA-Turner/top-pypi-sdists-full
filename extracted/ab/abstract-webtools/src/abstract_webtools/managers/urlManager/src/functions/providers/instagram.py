INSTAGRAM_HOSTS = {"instagram.com", "www.instagram.com"}

def detect_instagram(parsed):
    if parsed.netloc.lower() not in INSTAGRAM_HOSTS:
        return None

    parts = [p for p in parsed.path.split("/") if p]

    # /reel/{id}/
    if len(parts) >= 2 and parts[0] in {"reel", "p", "tv"}:
        return {"downloadable": True, "kind": "video", "provider": "instagram",
                "id": parts[1], "direct": False}

    return {"downloadable": False, "provider": "instagram"}
