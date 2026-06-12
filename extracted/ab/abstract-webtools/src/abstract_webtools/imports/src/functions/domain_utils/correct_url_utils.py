from ..imports import *
def get_correct_url(url=None) -> str:
    """
    Try candidates (HEAD request). 
    Return first that resolves with 200.
    """
    try:
        response = requests.get(url, stream=True, timeout=2, allow_redirects=True)
    
        if response.status_code == 200:
            return url
    except Exception as e:
        logger.debug(f"{e}")
    return None
def domain_exists(url=None) -> str:
    """
    Try candidates (HEAD request). 
    Return first that resolves with 200.
    """
    try:
        response = requests.get(url, stream=True, timeout=2, allow_redirects=True)
        
        if response.status_code == 200:
            return True
    except Exception as e:
        logger.debug(f"{e}")
    return False
def get_correct_urls(candidates=None) -> str:
    """
    Try candidates (HEAD request). 
    Return first that resolves with 200.
    """

    urls = []
    try:
        for candidate in candidates:
            url  = get_correct_url(url=candidate)
            if url:
                urls.append(url)
    except Exception as e:
        logger.debug(f"{e}")
    return urls
