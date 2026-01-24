from .src import *
seleniumManager = seleneumManager
def normalize_url(url, base_url=None):
    manager = seleniumManager(url)
    base_url = manager.base_url
    if url.startswith(base_url):
        url = url[len(base_url):]
    normalized_url = urljoin(base_url, url.split('#')[0])
    if not normalized_url.startswith(base_url):
        return None
    return normalized_url
