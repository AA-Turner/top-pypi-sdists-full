import requests

def get_correct_url(url=None) -> str:
    """
    Try candidates (HEAD request). 
    Return first that resolves with 200.
    """

    response = requests.get(url, stream=True, timeout=6, allow_redirects=True)
    
    if response.status_code == 200:
        return url

    return None
def domain_exists(url=None) -> str:
    """
    Try candidates (HEAD request). 
    Return first that resolves with 200.
    """

    response = requests.get(url, stream=True, timeout=6, allow_redirects=True)
    
    if response.status_code == 200:
        return True
    
    return False
def get_correct_urls(candidates=None) -> str:
    """
    Try candidates (HEAD request). 
    Return first that resolves with 200.
    """

    urls = []
    for candidate in candidates:
        url  = get_correct_url(url=candidate)
        if url:
            urls.append(url)
    return urls
