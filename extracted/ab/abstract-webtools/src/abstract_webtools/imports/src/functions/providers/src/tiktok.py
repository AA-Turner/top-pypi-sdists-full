TIKTOK_HOSTS = {"tiktok.com", "www.tiktok.com", "vm.tiktok.com", "m.tiktok.com"}

def detect_tiktok(parsed):
    if parsed.netloc.lower() not in TIKTOK_HOSTS:
        return None

    parts = parsed.path.split("/")
    if "video" in parts:
        idx = parts.index("video")
        vid = parts[idx + 1] if idx + 1 < len(parts) else None
        return {"downloadable": True, "kind": "video", "provider": "tiktok",
                "id": vid, "direct": False}

    return {"downloadable": False, "provider": "tiktok"}
