TWITCH_HOSTS = {"twitch.tv", "www.twitch.tv", "clips.twitch.tv"}

def detect_twitch(parsed):
    net = parsed.netloc.lower()

    if net == "clips.twitch.tv":
        clip_id = parsed.path.strip("/")
        return {"downloadable": True, "kind": "video", "provider": "twitch",
                "id": clip_id, "direct": False}

    return None
