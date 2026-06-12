REDDIT_HOSTS = {"reddit.com", "www.reddit.com", "v.redd.it"}

def detect_reddit(parsed):
    net = parsed.netloc.lower()

    if net == "v.redd.it":
        vid = parsed.path.strip("/")
        return {"downloadable": True, "kind": "video", "provider": "reddit",
                "id": vid, "direct": False}

    return {"downloadable": False, "provider": "reddit"}
