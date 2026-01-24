from .imports import *
def update_source_and_url(manager,*args,url=None,source_code=None):
    if url and manager.url != url:
        manager.update_url(url)
    if source_code and hasattr(manager, 'source_code') and source_code != manager.source_code:
        manager.update_source_code(source_code)
    return manager
def make_mgr_updates(*args,url=None,source_code=None,page=None,soup_mgr=None,req_mgr=None,url_mgr=None,**kwargs):
    if page:
        source_code = page.content()
    url_mgr = url_mgr or urlManager(url=url)

    if not soup_mgr and not req_mgr:
        if url or source_code:
            req_mgr = requestManager(url_mgr=url_mgr,source_code=source_code)
            soup_mgr = soupManager(req_mgr=req_mgr)
    if url_mgr:
        url_mgr = update_source_and_url(url_mgr,url=url)    
    if req_mgr:
        req_mgr = update_source_and_url(req_mgr,url=url,source_code=source_code)
    if soup_mgr:
        soup_mgr = update_source_and_url(soup_mgr,url=url,source_code=source_code)
    return soup_mgr,req_mgr,url_mgr
def get_source_code(*args,page=None,url=None,soup_mgr=None,req_mgr=None,url_mgr=None,source_code=None,**kwargs):
    if page:
        source_code = page.content()
    soup_mgr,req_mgr,_ = make_mgr_updates(url=url,source_code=source_code,soup_mgr=soup_mgr,req_mgr=req_mgr,url_mgr=url_mgr,**kwargs)
    if req_mgr:
        return req_mgr.source_code
    elif soup_mgr:
        return soup_mgr.source_code
    else:
        return source_code
