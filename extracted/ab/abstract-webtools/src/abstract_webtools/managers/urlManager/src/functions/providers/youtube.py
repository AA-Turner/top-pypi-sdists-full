YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "youtu.be"}

def detect_youtube(parsed, query):
    net = parsed.netloc.lower()
    if net not in YOUTUBE_HOSTS:
        return None

    if "v" in query:
        return {"downloadable": True, "kind": "video", "provider": "youtube",
                "id": query["v"][0], "direct": False}

    if net == "youtu.be":
        vid = parsed.path.strip("/")
        return {"downloadable": True, "kind": "video", "provider": "youtube",
                "id": vid, "direct": False}

    if "list" in query:
        return {"downloadable": True, "kind": "playlist", "provider": "youtube",
                "id": query["list"][0], "direct": False}

    return {"downloadable": False, "provider": "youtube"}
