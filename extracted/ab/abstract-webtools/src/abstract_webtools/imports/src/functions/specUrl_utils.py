from .DomainManager import *
from .url_utils import *
from ..imports import *


def get_parsed_dict(url=None, parsed=None, parsed_dict=None):
    if url and not parsed:
        parsed = parse_url(url)
    if parsed and not parsed_dict:
        parsed_dict = parse_url(parsed=parsed)
    return parsed_dict 
def reconstructUrlFromUrlParse(url=None, parsed=None, parsed_dict=None):
    parsed_dict = parsed_dict or get_parsed_dict(url)
    keys = ['scheme','domain','netloc','path','params','query','fragment']
    if parsed_dict:
        scheme = parsed_dict.get('scheme')
        
        nuUrl = ''
        for key in keys:
            value = parsed_dict.get(key, '')
            if key == 'scheme':
                nuUrl += f'{value}://' if value else ''
            elif key == 'query':
                nuUrl += f'?{reconstructQuery(value)}' if value else ''
            elif key == 'netloc':
                nuUrl += reconstructNetLoc(value) if value else ''
            else:
                # removed noisy print(value)
                nuUrl += f"/{value}"
        return nuUrl
    return url
def get_youtube_parsed_dict(url=None, parsed=None, parsed_dict=None):
    parsed_dict =  get_parsed_dict(url=url, parsed=parsed, parsed_dict=parsed_dict)
    if parsed_dict:
        netloc = parsed_dict.get("netloc")
        domain = (netloc or {})
        if isinstance(domain,dict):
            domain = domain.get('domain') or ''
        query  = parsed_dict.get('query') or {}
        path   = parsed_dict.get('path') or ''
        if domain.startswith('youtu'):
            # force youtube.com and /watch?v=ID
            netloc['www'] = True
            netloc['domain'] = 'youtube'
            netloc['extention'] = '.com'
            parsed_dict['netloc'] = netloc

            # keep v if present; otherwise derive
            v_query = query.get('v')
            if not v_query:
                if path.startswith('/watch/') or path.startswith('/shorts/'):
                    v_query = eatAll(path, ['/','watch','shorts'])
                else:
                    v_query = eatAll(path, ['/'])
            parsed_dict['path'] = '/watch'
            parsed_dict['query'] = {'v': v_query} if v_query else {}
            return parsed_dict
def get_youtube_v_query(url=None, parsed=None, parsed_dict=None):
    parsed_dict =  get_youtube_parsed_dict(url=url, parsed=parsed, parsed_dict=parsed_dict)
    v_query = parsed_dict.get('query',{})
    if isinstance(v_query,dict):
        v_query = v_query.get('v')
    return v_query
def get_youtube_url(url=None, parsed=None, parsed_dict=None):
    parsed_dict =  get_youtube_parsed_dict(url=url, parsed=parsed, parsed_dict=parsed_dict)
    return reconstructUrlFromUrlParse(parsed_dict=parsed_dict)
def get_threads_url(url=None,parsed=None, parsed_dict =None ):
    parsed_dict =  get_parsed_dict(url=url, parsed=parsed, parsed_dict=parsed_dict)
    if parsed_dict:
        netloc = parsed_dict.get("netloc")
        domain = (netloc or {})
        if isinstance(domain,dict):
            domain = domain.get('domain') or ''
        if domain.startswith('threads'):
            netloc['www']=True
            netloc['domain'] ='threads'
            netloc['extention'] = '.net'
            parsed['netloc']=netloc
            return reconstructUrlFromUrlParse(url=url,parsed=parsed,parsed_dict=None)  


def _clean_url(url: str) -> str:
    """ normalize scheme + strip weird fragments """
    if not url:
        return ""
    url = url.strip()
    if url.startswith("//"):
        url = "https:" + url
    return url

# -----------------------------------------------------
# PLATFORM EXTRACTORS
# -----------------------------------------------------

def detect_youtube(parsed, query):
    netloc = parsed.netloc.lower()
    if netloc not in YOUTUBE_HOSTS:
        return None

    # video id
    if "v" in query:
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "youtube",
            "id": query.get("v", [None])[0],
            "direct": False,
        }

    # youtu.be short links
    if parsed.netloc == "youtu.be":
        vid = parsed.path.strip("/")
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "youtube",
            "id": vid,
            "direct": False,
        }

    # playlists
    if "list" in query:
        return {
            "downloadable": True,
            "kind": "playlist",
            "provider": "youtube",
            "id": query.get("list", [None])[0],
            "direct": False,
        }

    return {
        "downloadable": False,
        "kind": None,
        "provider": "youtube",
        "id": None,
        "direct": False,
    }


def detect_vimeo(parsed):
    if parsed.netloc.lower() not in VIMEO_HOSTS:
        return None
    vid = parsed.path.strip("/")
    if vid.isdigit():
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "vimeo",
            "id": vid,
            "direct": False
        }
    return {"downloadable": False, "provider": "vimeo"}


def detect_tiktok(parsed):
    if parsed.netloc.lower() not in TIKTOK_HOSTS:
        return None

    parts = parsed.path.split("/")
    # /@user/video/123456
    if "video" in parts:
        idx = parts.index("video")
        vid = parts[idx + 1] if idx + 1 < len(parts) else None
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "tiktok",
            "id": vid,
            "direct": False,
        }
    return {"downloadable": False, "provider": "tiktok"}


def detect_twitter(parsed, query):
    if parsed.netloc.lower() not in TWITTER_HOSTS:
        return None

    parts = parsed.path.split("/")
    # /username/status/ID
    if "status" in parts:
        idx = parts.index("status")
        tid = parts[idx + 1] if idx + 1 < len(parts) else None
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "twitter",
            "id": tid,
            "direct": False,
        }
    return {"downloadable": False, "provider": "twitter"}


def detect_facebook(parsed):
    net = parsed.netloc.lower()

    if net not in FACEBOOK_HOSTS:
        return None

    # Pattern 1: /share/v/{video_id}/
    # Example: https://www.facebook.com/share/v/1EqXAsf57B/
    parts = [p for p in parsed.path.split("/") if p]

    if len(parts) >= 3 and parts[0] == "share" and parts[1] == "v":
        vid = parts[2]
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "facebook",
            "id": vid,
            "direct": False,
        }

    # Pattern 2: Watch URLs (fb.watch/xxxx)
    if net == "fb.watch":
        vid = parsed.path.strip("/")
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "facebook",
            "id": vid,
            "direct": False,
        }

    # Pattern 3: Regular watch URLs
    # https://www.facebook.com/watch/?v=123456789
    query = parse_qs(parsed.query)
    if "v" in query:
        return {
            "downloadable": True,
            "kind": "video",
            "provider": "facebook",
            "id": query["v"][0],
            "direct": False,
        }

    return {"downloadable": False, "provider": "facebook"}
def detect_direct_file(parsed):
    ext = os.path.splitext(parsed.path)[1].lower()
    if ext in DIRECT_EXTS:
        return {
            "downloadable": True,
            "kind": mimetypes.guess_type(parsed.path)[0] or "file",
            "provider": None,
            "id": None,
            "direct": True,
        }
    return None


# -----------------------------------------------------
# MAIN ENTRY POINT
# -----------------------------------------------------

def get_downloadable_info(url: str):
    url = _clean_url(url)
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    # 1. Direct file
    direct = detect_direct_file(parsed)
    if direct:
        direct["url"] = url
        return direct

    # 2. YouTube
    yt = detect_youtube(parsed, query)
    if yt:
        yt["url"] = url
        return yt

    # 3. Vimeo
    vimeo = detect_vimeo(parsed)
    if vimeo:
        vimeo["url"] = url
        return vimeo

    # 4. TikTok
    tiktok = detect_tiktok(parsed)
    if tiktok:
        tiktok["url"] = url
        return tiktok

    # 5. Twitter/X
    tw = detect_twitter(parsed, query)
    if tw:
        tw["url"] = url
        return tw

    # fallback
    return {
        "downloadable": False,
        "kind": None,
        "provider": None,
        "id": None,
        "direct": False,
        "url": url,
    }

def get_corrected_url(url=None,parsed=None, parsed_dict =None ):
    return get_downloadable_info(url).get('url')
##    parsed_dict =  get_parsed_dict(url=url, parsed=parsed, parsed_dict=parsed_dict)
##    if parsed_dict:
##        funcs = [get_threads_url,get_youtube_url,reconstructUrlFromUrlParse]
##        for func in funcs:
##            corrected_url = func(url=url,parsed=parsed,parsed_dict=parsed_dict)
##            if corrected_url:
##                return corrected_url

