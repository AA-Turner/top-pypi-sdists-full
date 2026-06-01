##import threading,os,re,yt_dlp
from ..imports import *
from .domain_utils import *
from .DomainManager import *
def reconstructNetLoc(netloc):
    keys = ['www','domain','extention']
    if isinstance(netloc, dict):
        vals = []
        for key in keys:
            value = netloc.get(key)
            if key == 'www':
                value = 'www' if value else ''
            vals.append(eatAll(value or '', ['.']))
        netloc = eatAll('.'.join(vals), ['.'])
    return netloc or ''

def reconstructQuery(query):
    if isinstance(query, dict):
        # Keep stable ordering if you want: sort by key
        return "&".join(f"{k}={v}" for k, v in query.items())
    return query or ''

def reconstructUrlParse(url=None, parsed=None, parsed_dict=None):
    d = parse_url(url=url, parsed=parsed, parsed_dict=parsed_dict)
    return urlunparse((
        d.get("scheme") or "",
        reconstructNetLoc(d.get("netloc")),
        d.get("path") or "",
        d.get("params") or "",
        reconstructQuery(d.get("query")),
        d.get("fragment") or "",
    ))
def dictquery(parsed):
    query = parsed.query if hasattr(parsed, "query") else parsed
    if not query:
        return {}
    nuqueries = {}
    for pair in str(query).split("&"):
        if not pair:
            continue
        if "=" in pair:
            k, v = pair.split("=", 1)
            nuqueries[k] = v
        else:
            nuqueries[pair] = ""
    return nuqueries

def parse_netloc(url=None,parsed=None,netloc=None):
    netloc = get_extention(url=url,parsed=parsed,netloc=netloc)
    www=False
    nunetloc={'www':www}
    nunetloc.update(netloc)
    domain = nunetloc.get("domain")
    if domain.startswith('www.'):
        nunetloc['domain']=domain[len('www.'):]
        www = True
    nunetloc['www'] = www
    return nunetloc
from urllib.parse import urlparse, ParseResult, urlunparse

def _parse_url(url=None, parsed=None, parsed_dict=None):
    """
    Accepts:
      - url: str
      - parsed: urllib.parse.ParseResult OR str (url) OR dict (already parsed)
      - parsed_dict: dict (already parsed)
    Returns a normalized dict with keys: scheme, netloc, path, params, query, fragment
    """
    # If caller already has a parsed dict, prefer that
    if isinstance(parsed_dict, dict):
        return parsed_dict

    # If caller accidentally passed dict into `parsed`, treat it as parsed_dict
    if isinstance(parsed, dict):
        return parsed

    # If `parsed` is actually a URL string, normalize to url
    if isinstance(parsed, str) and not url:
        url = parsed
        parsed = None

    # Build ParseResult if we have a URL and no parsed object
    if url and not isinstance(parsed, ParseResult):
        parsed = urlparse(url)

    # If we now have a real ParseResult, normalize it
    if isinstance(parsed, ParseResult):
        scheme = parsed.scheme or ALL_URL_KEYS["scheme"][0]

        # Handle bare "example" case (no scheme/netloc but a path with a hostname)
        netloc = parsed.netloc
        path   = parsed.path
        if not scheme and not netloc and path:
            parts = [p for p in path.split("/") if p]
            if parts:
                netloc = parts[0]
                path   = f"/{'/'.join(parts[1:])}" if len(parts) > 1 else ""
                # do not need to rebuild ParseResult; we only return dict

        netloc_data = get_extension(parsed=parsed, options=ALL_URL_KEYS["netloc"])

        return {
            "scheme": scheme,
            "netloc": netloc_data,
            "path": path or "",
            "params": parsed.params or "",
            "query": dictquery(parsed),
            "fragment": parsed.fragment or "",
        }

    # Fallback: if we only have a URL string
    if isinstance(url, str):
        p = urlparse(url)
        return {
            "scheme": p.scheme or ALL_URL_KEYS["scheme"][0],
            "netloc": get_extention(parsed=p, options=ALL_URL_KEYS["netloc"]),
            "path": p.path or "",
            "params": p.params or "",
            "query": dictquery(p),
            "fragment": p.fragment or "",
        }

    # Last resort
    return {
        "scheme": ALL_URL_KEYS["scheme"][0],
        "netloc": {},
        "path": "",
        "params": "",
        "query": {},
        "fragment": "",
    }


def parse_url(*args,url=None,parsed=None,**kwargs):
    
    for arg in args:
        if isinstance(arg,str):
            url = arg
            parsed = domain_mgr.check_domains(url)
        elif isinstance(arg,dict) and parsed == None:
            parsed=arg
    if not url and parsed:
        url = parsed.get('full_url')
    parsed_url = domain_mgr.urlparse(url)
    parsed = domain_mgr.check_domains(url)
    full_domain = parsed.get('full_domain')
    parsed['path'] = get_domain_path(url)
    full_url = get_full_url(parsed_url=parsed)
    parsed['full_url'] = full_url
    parsed_url = _parse_url(url=full_url)
    parsed_url.update(parsed)
    return parsed_url
