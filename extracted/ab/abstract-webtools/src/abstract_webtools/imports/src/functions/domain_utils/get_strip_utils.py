from ..imports import *
import os


def get_http(domain: str | None) -> str | None:
    """Return 'http' or 'https' if detected, otherwise None."""
    if not domain:
        return None
    domain = str(domain).strip()
    if domain.startswith("https"):
        return "https"
    if domain.startswith("http"):
        return "http"
    return None


def strip_http(domain: str | None, http: str | None = None) -> str | None:
    """Remove http(s):// from domain if present."""
    if not domain:
        return None
    http = http or get_http(domain)
    try:
        if http:
            domain = domain[len(http) + 3 :] if "://" in domain else domain[len(http):]
        domain = eatAll(domain, [":", "/"])
        return domain.strip()
    except Exception:
        return domain


def get_www(domain: str | None, http: str | None = None) -> bool:
    """Return True if domain starts with www."""
    if not domain:
        return False
    domain = strip_http(domain,http)
    return bool(domain and domain.startswith("www."))

def strip_www(domain: str | None, http: str | None = None) -> str | None:
    """Remove leading www. and restore http prefix if any."""
    if not domain:
        return None
    http = http or get_http(domain)
    domain = strip_http(domain, http)
    try:
        if domain and domain.startswith("www."):
            domain = domain[len("www.") :]
        if http:
            domain = f"{http}://{domain}"
        return domain.strip()
    except Exception:
        return domain



def get_http_www(domain: str | None) -> dict:
    """Return dict with detected http and www info."""
    if not domain:
        return {"http": None, "www": False}
    http = get_http(domain)
    www = get_www(domain, http)
    return {"http": http, "www": www}


def strip_http_www(domain) -> str | None:
    """Remove both http(s) and www."""
    if not domain:
        return None
    http = get_http(domain)
    domain = strip_www(domain, http)
    domain = strip_http(domain, http)
    return domain


def get_stripped_domain(domain: str | None, http: str | None = None) -> list[str] | None:
    """Return list of domain parts, safely."""
    if not domain:
        return None
    domain = strip_http_www(domain, http)
    domain,params = get_url_params(domain,clean_url=True)
    return domain.split("/") if domain else None

def get_domain_paths(domain: str | None, http: str | None = None) -> dict:
    """Return {'domain': <domain>, 'path': <path>} even if None."""
    if not domain:
        return {"domain": None, "path": ""}

    return get_url_paths_params(domain, http).get("paths")





def get_domain_path(domain: str | None, http: str | None = None) -> str:
    """Extract path component from URL."""
    domain_paths = get_domain_paths(domain, http=http)
    return '/'.join(domain_paths)


def get_domain_name_ext(domain: str | None, http: str | None = None) -> dict:
    """Return {'name': name, 'ext': ext} safely."""
    if not domain:
        return {"name": None, "ext": None}
    domain_only = get_domain(domain, http)
    if not domain_only:
        return {"name": None, "ext": None}
    name, ext = os.path.splitext(domain_only)
    return {"name": name or None, "ext": ext or None}




def get_url_paths_params(domain,http=None):

    domain_vars = {}
    domain_vars["original_url"] = domain
    domain_vars["http"]= get_http(domain=domain)
    domain_vars["www"]= get_www(domain=domain,http=domain_vars.get("http"))
    
    
    domain_spl = domain.split('?')
    domain_vars['clean_url']= domain_spl[0]
    params= {}
    domain_vars['param']=''
    if len(domain_spl)>1:
        url = domain_spl[0]
        raw_params = domain_spl[-1]
        domain_vars['param'] = raw_params
        for raw_param in raw_params.split('&'):
            key_value = raw_param.split('=')
            key = key_value[0]
            domain_vars[key]= None
            if len(key_value)>1:
                domain_vars[key]= '='.join(key_value[1:])
    domain_vars['params']=params
    
    stripped_url = strip_http_www(domain=domain)

    domain_spl = stripped_url.split("/")
    domain = domain_spl[0]
    domain_vars['domain'] = domain
    name,ext = os.path.splitext(domain)
    domain_vars['name'] = name
    domain_vars['ext'] = ext
    paths = []
    if len(domain_spl)>1:
        paths = domain_spl[1:]
    domain_vars['paths'] = [path for path in paths if path]
    domain_vars['path'] = '/'.join(domain_vars['paths'])
    return domain_vars
def get_extension(domain: str | None = None, http: str | None = None, parsed=None, options=None) -> str | None:
    """Get file extension safely, even if parsed URL object is missing."""
    try:
        if parsed:
            domain = getattr(parsed, "netloc", domain)
            http = getattr(parsed, "scheme", http)
    except Exception:
        pass
    return get_url_paths_params(domain=domain, http=http).get("ext")


def get_domain_name(domain: str | None, http: str | None = None) -> str | None:
    """Get domain name without extension."""
    return get_url_paths_params(domain=domain, http=http).get("name")
def get_url_path(domain: str | None, http: str | None = None):
    return get_url_paths_params(domain=domain, http=http).get("path")
def get_url_paths(domain: str | None, http: str | None = None):
    return get_url_paths_params(domain=domain, http=http).get("paths")
def get_cleaned_url(domain: str | None, http: str | None = None):
    return get_url_paths_params(domain=domain, http=http).get("clean_url")
def get_domain(domain: str | None, http: str | None = None) -> str | None:
    """Extract bare domain from URL."""
    return get_url_paths_params(domain, http).get("domain")
def get_params(domain: str | None, http: str | None = None) -> str | None:
    """Extract bare domain from URL."""
    return get_url_paths_params(domain, http).get("params")
def get_param(domain: str | None, http: str | None = None) -> str | None:
    """Extract bare domain from URL."""
    return get_url_paths_params(domain, http).get("param")
def get_video_url(url=None,video_url=None):
    return get_cleaned_url(video_url or url)
    
# Backward compatibility alias

get_extention = get_extension

