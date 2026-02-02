from .imports import *
# ============================================================
# Endpoint lookup
# ============================================================
def get_endpoint_help(call_url=None,name=None,domain=None,api_prefix=None,endpoints_prefix=None,api_url=None,endpoints_url=None):
    if not call_url:
        call_url,method = get_endpoint(name=name,domain=domain,api_prefix=api_prefix,endpoints_prefix=endpoints_prefix,api_url=api_url,endpoints_url=endpoints_url)
    return postRequest(f"{call_url}?help=true")
def match_endpoint(name,endpoints=None,domain=None):
    """
    Locate endpoint containing the substring `name`.
    Returns full URL: domain + /prefix/.../name
    """
    domain = domain or ""
    endpoints = endpoints or []
    matches = [e for e in endpoints if name in e[0]]
    if matches:
        url = matches[0][0]
        method = matches[0][-1]
        if domain:
            url = join(domain,url)
        return url,method
    return None,None

def get_endpoints(domain=None,api_prefix=None,endpoints_prefix=None,api_url=None,endpoints_url=None,**kwargs):
    if not endpoints_url and not api_url and not domain:
        return None
    api_prefix = api_prefix or 'api'
    endpoints_prefix = endpoints_prefix or 'endpoints'
    if not endpoints_url and not api_url:
        api_url = join_url(domain,api_prefix)
    if not endpoints_url:
        endpoints_url = join_url(api_url,endpoints_prefix)
    return postRequest(endpoints_url)
def get_endpoint(name,domain=None,api_prefix=None,endpoints_prefix=None,api_url=None,endpoints_url=None):
    domain = domain or DOMAIN
    api_prefix = api_prefix or API_PREFIX
    endpoints_prefix = endpoints_prefix or ENDPOINTS_PREFIX
    api_url = api_url or API_URL
    endpoints_url = endpoints_url or ENDPOINTS_URL
    endpoints = get_endpoints(domain=domain,api_prefix=api_prefix,endpoints_prefix=endpoints_prefix,api_url=api_url,endpoints_url=endpoints_url)
  
    endpoint,method = match_endpoint(name=name,endpoints=endpoints,domain=domain)
    return endpoint,method
