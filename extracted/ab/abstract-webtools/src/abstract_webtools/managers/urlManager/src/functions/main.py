from urllib.parse import urlparse, parse_qs
import os
import mimetypes

# Provider imports
from .providers.youtube import detect_youtube
from .providers.vimeo import detect_vimeo
from .providers.tiktok import detect_tiktok
from .providers.facebook import detect_facebook
from .providers.twitter import detect_twitter
from .providers.instagram import detect_instagram
from .providers.reddit import detect_reddit
from .providers.twitch import detect_twitch
from .providers.imgur import detect_imgur
from .providers.pinterest import detect_pinterest
from .providers.giphy import detect_giphy
from .providers.tenor import detect_tenor
from .providers.direct_file import detect_direct_file

PROVIDERS = [
    detect_direct_file,   # always check this first
    detect_youtube,
    detect_vimeo,
    detect_tiktok,
    detect_facebook,
    detect_twitter,
    detect_instagram,
    detect_reddit,
    detect_twitch,
    detect_imgur,
    detect_pinterest,
    detect_giphy,
    detect_tenor
]

def _clean_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    return url

def get_downloadable_info(url: str):
    url = _clean_url(url)
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    for provider in PROVIDERS:
        result = provider(parsed, query) if provider.__code__.co_argcount == 2 else provider(parsed)
        if result:
            result["url"] = url
            return result

    return {
        "downloadable": False,
        "kind": None,
        "provider": None,
        "id": None,
        "direct": False,
        "url": url,
    }
