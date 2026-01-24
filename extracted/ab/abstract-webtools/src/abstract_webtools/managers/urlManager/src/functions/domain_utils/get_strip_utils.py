import os
from ..imports import *

def get_http(domain):
    
    http=None
    if domain.startswith('http'):
        http = 'http'
        if domain.startswith('https'):
            http = f"{http}s"
    return http
def strip_http(domain,http=None):
    http = http or get_http(domain)
   
    domain = domain[len(http or ''):]
    
    domain = eatAll(domain,[':','/'])
    return domain

    
def get_www(domain,http=None):
    http = http or get_http(domain)
    domain = strip_http(domain = domain,http=http)
    if domain.startswith('www.'):
        return True
    return False   
def strip_www(domain,http=None):
    http = http or get_http(domain)
    
    domain = strip_http(domain = domain,http=http)
    
    www = get_www(domain,http=None)
    if www:
        domain = domain[len('www.'):]
    if http:
        
        domain = f"{http}://{domain}"
    return domain

def get_http_www(domain):
    http = get_http(domain)
    www = get_www(domain,http=http)
    return {"http":http,"www":www}
def strip_http_www(domain,http=None):
    domain = strip_www(domain,http=http)
    domain = strip_http(domain,http=http)
    return domain
def get_stripped_domain(domain,http=None):
    url,params = get_url_params(domain,get_url=True)
    url = strip_http_www(url,http=http)
    return url.split('/')
def get_url_params(url,get_url=False):
    params = {}
    if '?' in url:
        url,nuparams = url.split('?')
        nuparams = nuparams.split('&')
        for param in nuparams:
            param_spl = param.split('=')
            key = param_spl[0]
            params[key]=None
            if len(param_spl) >1:
               params[key] = '='.join(param_spl[1:])
    if get_url:
        return url,params
    return params
def get_cleaned_url(url):
    url,params = get_url_params(url,get_url=True)
    return url
def get_domain_paths(domain,http=None):
    domain = strip_http_www(domain,http=http)
    domain_paths = domain.split('/')
    paths = domain_paths[1:] if len(domain_paths)>1 else []
    return {"domain":domain_paths[0],"path":'/'.join(paths)}
def get_domain(domain,http=None):
    domain_ext = get_domain_paths(domain,http=http)
    return domain_ext.get("domain")
def get_domain_path(domain,http=None):
    domain_ext = get_domain_paths(domain,http=http)
    return domain_ext.get("path")
def get_domain_name_ext(domain,http=None):
    domain = get_domain(domain,http=http)
    domain_ext = os.path.splitext(domain)
    return {"name":domain_ext[0],"ext":domain_ext[-1]}
def get_extension(domain=None,http=None,parsed=None,options=None):
    if parsed:
        try:
            domain = parsed.netloc
            http = parsed.scheme
        except:
            pass
    domain_ext = get_domain_name_ext(domain,http=http)
    return domain_ext.get("ext")
def get_domain_name(domain,http=None):
    domain_ext = get_domain_name_ext(domain,http=http)
    return domain_ext.get("name")
def get_url_js(url):
    www = get_http_www(url)
    http = get_http(url)
    domain = get_domain(url)
    stripped_domain = get_stripped_domain(url,http=http)
    params = get_url_params(url)
    domain_name_ext = get_domain_name_ext(url,http=http)
    domain_paths = get_domain_paths(url,http=http)
    cleaned_url = get_cleaned_url(url)
    return {"www":www,"http":http,"domain":domain,"cleaned_url":cleaned_url,"stripped_domain":stripped_domain,"params":params,"domain_name_ext":domain_name_ext,"domain_paths":domain_paths}

get_extention = get_extension

input(for_dl_video("https://www.instagram.com/reel/DRXv6QOkd64/"))
