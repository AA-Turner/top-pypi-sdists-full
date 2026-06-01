TWITTER_HOSTS = {"twitter.com", "x.com", "www.twitter.com", "www.x.com"}

def detect_twitter(parsed, query):
    if parsed.netloc.lower() not in TWITTER_HOSTS:
        return None

    parts = parsed.path.split("/")
    if "status" in parts:
        idx = parts.index("status")
        tid = parts[idx + 1] if idx + 1 < len(parts) else None
        return {"downloadable": True, "kind": "video", "provider": "twitter",
                "id": tid, "direct": False}

    return {"downloadable": False, "provider": "twitter"}
