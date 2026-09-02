from __future__ import annotations

from urllib.parse import parse_qs, urlparse


def _host_matches(host: str, domain: str) -> bool:
    return host == domain or host.endswith(f".{domain}")


def video_embed_provider(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return None
    host = (parsed.hostname or "").lower().rstrip(".")
    path = parsed.path.lower()
    query = parse_qs(parsed.query)

    if (_host_matches(host, "youtube.com") or _host_matches(host, "youtube-nocookie.com")) and (
        path.startswith("/embed/") or (path == "/watch" and bool(query.get("v")))
    ):
        return "youtube"
    if host == "youtu.be" and path.strip("/"):
        return "youtube"
    if _host_matches(host, "vimeo.com") and (
        path.startswith("/video/") or host != "player.vimeo.com"
    ):
        return "vimeo"
    if _host_matches(host, "facebook.com") and path.startswith("/plugins/video"):
        return "facebook"
    if _host_matches(host, "dailymotion.com") and path.startswith("/embed/video/"):
        return "dailymotion"
    if host == "dai.ly" and path.strip("/"):
        return "dailymotion"
    if host == "player.twitch.tv" and (query.get("channel") or query.get("video")):
        return "twitch"
    if _host_matches(host, "instagram.com") and path.startswith(("/p/", "/reel/", "/reels/")):
        return "instagram"
    if _host_matches(host, "tiktok.com") and path.startswith(("/embed/", "/player/")):
        return "tiktok"
    if _host_matches(host, "rumble.com") and path.startswith("/embed/"):
        return "rumble"
    if _host_matches(host, "ted.com") and path.startswith("/talks/embed/"):
        return "ted"
    if _host_matches(host, "wistia.net") or _host_matches(host, "wistia.com"):
        if "/embed/" in path or "/medias/" in path:
            return "wistia"
    if _host_matches(host, "loom.com") and path.startswith("/embed/"):
        return "loom"
    if host == "play.vidyard.com" and path.strip("/"):
        return "vidyard"
    if _host_matches(host, "brightcove.net") and query.get("videoId"):
        return "brightcove"
    if host == "videos.sproutvideo.com" and path.startswith("/embed/"):
        return "sproutvideo"
    if host == "iframe.mediadelivery.net" and path.startswith("/embed/"):
        return "bunny_stream"
    return None


__all__ = ["video_embed_provider"]
