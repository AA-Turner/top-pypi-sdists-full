from .src import *
def get_solcatcher_call_url_method(name):
    call_url,method = get_endpoint(name=name,domain=DOMAIN,api_prefix=API_PREFIX,endpoints_prefix=ENDPOINTS_PREFIX,api_url=API_URL,endpoints_url=ENDPOINTS_URL)
    return call_url,method
def get_solcatcher_call_url(name):
    call_url,method = get_solcatcher_call_url_method(name)
    return call_url
def make_solcatcher_api_call(endpoint,**kwargs):
    call_url,method = get_solcatcher_call_url_method(endpoint)
    if 'POST' in method:
        return postRequest(call_url,**kwargs)
    else:
        return getRequest(call_url,**kwargs)
