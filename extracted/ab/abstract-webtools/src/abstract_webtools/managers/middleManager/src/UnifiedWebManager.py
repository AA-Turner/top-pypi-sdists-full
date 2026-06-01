import logging
from bs4 import BeautifulSoup
from ...urlManager import (
    get_url,
    get_url_mgr)
from ...requestManager import (
    get_source,
    get_req_mgr)
from ...soupManager import (
   get_soup,
    get_soup_mgr
   )

logging.basicConfig(level=logging.INFO)

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
        soup (BeautifulSoup or None): Pre-parsed soup object.
        parse_type (str): Parser type for BeautifulSoup (default: "html.parser").
    """
    def __init__(self, url=None, source_code=None, url_mgr=None, req_mgr=None, soup_mgr=None, soup=None, parse_type="html.parser"):
        self._url = url
        self._source_code = source_code
        self._url_mgr = url_mgr
        self._req_mgr = req_mgr
        self._soup_mgr = soup_mgr
        self._soup = soup
        self._parse_type = parse_type

    @property
    def url_mgr(self):
        if self._url_mgr is None:
            if self._url is None:
                logging.warning("No URL provided; URL manager cannot be created.")
                return None
            self._url_mgr = get_url_mgr(url=self._url)
        return self._url_mgr

    @property
    def url(self):
        if self._url is None and self.url_mgr is not None:
            self._url = get_url(url_mgr=self.url_mgr)
        return self._url

    @property
    def req_mgr(self):
        if self._req_mgr is None:
            self._req_mgr = get_req_mgr(url=self.url, url_mgr=self.url_mgr, source_code=self._source_code)
        return self._req_mgr

    @property
    def source_code(self):
        if self._source_code is None and self.req_mgr is not None:
            self._source_code = get_source(req_mgr=self.req_mgr)
        return self._source_code

    @property
    def soup_mgr(self):
        if self._soup_mgr is None:
            self._soup_mgr = get_soup_mgr(url=self.url, url_mgr=self.url_mgr, source_code=self.source_code, req_mgr=self.req_mgr)
        return self._soup_mgr

    @property
    def soup(self):
        if self._soup is None:
            source = self.source_code
            if source is None:
                logging.warning("No source code available; Soup cannot be created.")
                return None
            if isinstance(source, bytes):
                source = source.decode('utf-8', errors='ignore')
            self._soup = get_soup(source_code=source, parse_type=self._parse_type)
        return self._soup

    def update_url(self, url):
        """Update the URL and reset dependent managers."""
        self._url = url
        self._url_mgr = None
        self._req_mgr = None
        self._soup_mgr = None
        self._source_code = None
        self._soup = None

    def update_source_code(self, source_code):
        """Update the source code and reset dependent managers."""
        self._source_code = source_code
        self._req_mgr = None
        self._soup_mgr = None
        self._soup = None

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

def get_soup_tools(url=None, url_mgr=None, source_code=None, req_mgr=None, soup=None, soup_mgr=None, target_manager=None):
    mgr = UnifiedWebManager(url=url, url_mgr=url_mgr, source_code=source_code, req_mgr=req_mgr, soup_mgr=soup_mgr, soup=soup)
    if target_manager:
        return mgr.endow_to_manager(target_manager)
    return mgr.get_all_tools()
