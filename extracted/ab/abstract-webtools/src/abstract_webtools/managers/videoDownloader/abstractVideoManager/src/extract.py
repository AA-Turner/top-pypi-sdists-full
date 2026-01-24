# abstract_youtube/extract.py
from .imports import *
def extract_googlevideo_urls_from_html(html: str) -> list[str]:
    """
    DEBUG / INSPECTION ONLY.
    Finds googlevideo URLs embedded in JS blobs.
    """
    urls = set()
    for m in re.findall(r'"(https://[^"]+googlevideo\.com[^"]+)"', html):
        try:
            urls.add(json.loads(f'"{m}"'))
        except Exception:
            continue
    return list(urls)


def extract_player_response(url: str) -> dict:
    req = requestManager(url)
    html = req.source_code

    m = re.search(
        r"ytInitialPlayerResponse\s*=\s*(\{.+?\});",
        html,
        re.S,
    )
    if not m:
        raise RuntimeError("ytInitialPlayerResponse not found")

    return json.loads(m.group(1))


def iter_streaming_urls(player_response: dict):
    streaming = player_response.get("streamingData", {})
    formats = (
        streaming.get("formats", []) +
        streaming.get("adaptiveFormats", [])
    )

    for fmt in formats:
        if "url" in fmt:
            yield fmt["url"], fmt
        elif "signatureCipher" in fmt:
            yield fmt["signatureCipher"], fmt
