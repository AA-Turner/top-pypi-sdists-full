# abstract_youtube/validators.py

from urllib.parse import urlparse, parse_qs

def looks_like_real_stream(url: str) -> bool:
    q = parse_qs(urlparse(url).query)
    return (
        "itag" in q and
        "mime" in q and
        ("sig" in q or "signature" in q)
    )
