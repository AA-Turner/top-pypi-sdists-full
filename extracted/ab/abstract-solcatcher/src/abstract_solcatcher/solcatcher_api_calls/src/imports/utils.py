from .module_imports import *
def join_url(*urls):
    full_url = ""
    for i,url in enumerate(urls):
        if i == 0:
            full_url = url
        else:
            url = eatInner(url,['/'])
            full_url = eatOuter(full_url,['/'])
            full_url = f"{full_url}/{url}"
    return full_url
