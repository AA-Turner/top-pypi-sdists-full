from ..imports import *

class UnifiedWebManager:
    """
    Unified middleware that ties together URL, request, and soup managers.
    Lazily initializes components based on provided inputs.
    
    Args:
        url (str or None): The base URL.
        source_code (str or bytes or None): Pre-fetched source code.
        url_mgr (urlManager or None): Existing URL manager.
        req_mgr (requestManager or None): Existing request manager.
        soup_mgr (soupManager or None): Existing soup manager.
        parse_type (str): Parser type for BeautifulSoup (default: "html.parser").
    """
    def __init__(self, url=None, source_code=None, url_mgr=None, req_mgr=None, soup_mgr=None,soup=None, parse_type="html.parser"):
        self.url_mgr = get_url_mgr(url=url,url_mgr=url_mgr)
        self.url = get_url(url=url,url_mgr=self.url_mgr)
        self.req_mgr = get_source(url=self.url,url_mgr=self.url_mgr,source_code=source_code,req_mgr=req_mgr)
        self.source_code = get_source(url=self.url,url_mgr=self.url_mgr,source_code=source_code,req_mgr=self.req_mgr)
        self.soup_mgr = get_soup_mgr(url=self.url,url_mgr=self.url_mgr,source_code=self.source_code,req_mgr=self.req_mgr,soup_mgr=soup_mgr,soup=soup,parse_type=parse_type)
        self.soup = get_soup(url=self.url,url_mgr=self.url_mgr,req_mgr=self.req_mgr,source_code=self.source_code,soup_mgr=self.soup_mgr)

    @property
    def url_mgr(self):
        if self.url_mgr is None:
            if self.url is None:
                logging.warning("No URL provided; URL manager cannot be created.")
                return None
            self.url_mgr = urlManager(url=self.url)
        return self.url_mgr

    @property
    def url(self):
        if self.url is None and self.url_mgr:
            self.url = self.url_mgr.url
        return self.url

    @property
    def req_mgr(self):
        if self.req_mgr is None:
            self.req_mgr = requestManager(
                url=self.url,
                url_mgr=self.url_mgr,
                source_code=self.source_code
            )
        return self.req_mgr

    @property
    def source_code(self):
        if self.source_code is None and self.req_mgr:
            self.source_code = self.req_mgr.source_code
        return self.source_code

    @property
    def soup_mgr(self):
        if self.soup_mgr is None:
            self.soup_mgr = soupManager(
                url=self.url,
                url_mgr=self.url_mgr,
                req_mgr=self.req_mgr,
                source_code=self.source_code
            )
        return self.soup_mgr

    @property
    def soup(self):
        if self.soup is None:
            source = self.source_code
            if source is None:
                logging.warning("No source code available; Soup cannot be created.")
                return None
            if isinstance(source, bytes):
                source = source.decode('utf-8', errors='ignore')
            self.soup = BeautifulSoup(source, self.parse_type)
        return self.soup

    def update_url(self, url):
        """Update the URL and reset dependent managers."""
        self.url = url
        self.url_mgr = None
        self.req_mgr = None
        self.soup_mgr = None
        self.source_code = None
        self.soup = None

    def update_source_code(self, source_code):
        """Update the source code and reset dependent managers."""
        self.source_code = source_code
        self.req_mgr = None
        self.soup_mgr = None
        self.soup = None

    # Convenience methods for direct access
    def get_all_tools(self):
        """Return a dict with all components (similar to original getters)."""
        return {
            'url': self.url,
            'url_mgr': self.url_mgr,
            'source_code': self.source_code,
            'req_mgr': self.req_mgr,
            'soup': self.soup,
            'soup_mgr': self.soup_mgr
        }
    def endow_to_manager(self, target_manager, all_tools=None):
        """
        Endow (assign) the attributes from all_tools to the target manager instance.
        
        Args:
            target_manager: The instance (e.g., another manager class) to endow attributes to.
            all_tools (dict or None): Optional dict of tools/attributes. If None, uses self.get_all_tools().
        """
        if all_tools is None:
            all_tools = self.get_all_tools()
        for key, value in all_tools.items():
            setattr(target_manager, key, value)
        return target_manager
# Wrapper functions for backward compatibility
def get_url_tools(url=None, url_mgr=None):
    mgr = UnifiedWebManager(url=url, url_mgr=url_mgr)
    return {'url': mgr.url, 'url_mgr': mgr.url_mgr}

def get_req_tools(url=None, url_mgr=None, source_code=None, req_mgr=None):
    mgr = UnifiedWebManager(url=url, url_mgr=url_mgr, source_code=source_code, req_mgr=req_mgr)
    return {'url': mgr.url, 'url_mgr': mgr.url_mgr, 'source_code': mgr.source_code, 'req_mgr': mgr.req_mgr}

def get_soup_tools(url=None, url_mgr=None, source_code=None, req_mgr=None, soup=None, soup_mgr=None,target_manager=None):
    mgr = UnifiedWebManager(url=url, url_mgr=url_mgr, source_code=source_code, req_mgr=req_mgr, soup_mgr=soup_mgr)
    if soup is not None:
        mgr.soup = soup  # Allow overriding
    if target_manager:
        mgr.endow_to_manager(target_manager, all_tools=None)
        return target_manager
    return mgr.get_all_tools()


