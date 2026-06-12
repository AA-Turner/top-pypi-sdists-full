from .UnifiedWebManager import UnifiedWebManager
# ---- add this helper somewhere near UnifiedWebManager ----
class _ToolProxy:
    """
    Lazy, attribute-access proxy over a UnifiedWebManager.
    Does NOT eagerly call get_all_tools(); properties are resolved on demand.
    Also supports minimal dict-like behavior.
    """
    __slots__ = ("_mgr",)
    _KEYS = ("url", "url_mgr", "source_code", "req_mgr", "soup", "soup_mgr")

    def __init__(self, mgr: "UnifiedWebManager"):
        self._mgr = mgr

    def __getattr__(self, name):
        if name in self._KEYS or hasattr(self._mgr, name):
            return getattr(self._mgr, name)
        raise AttributeError(f"{type(self).__name__!r} has no attribute {name!r}")

    # optional niceties
    def to_dict(self):
        # snapshot (this will evaluate the properties)
        return {k: getattr(self._mgr, k) for k in self._KEYS}

    def __getitem__(self, key):
        if key in self._KEYS:
            return getattr(self._mgr, key)
        raise KeyError(key)

    def keys(self): return list(self._KEYS)
    def items(self): return [(k, getattr(self._mgr, k)) for k in self._KEYS]
    def values(self): return [getattr(self._mgr, k) for k in self._KEYS]

    def __repr__(self):
        # don’t force evaluation; just show which tools exist
        return f"<ToolProxy url={self._mgr._url!r}>"

# ---- update the wrappers to use the proxy by default ----
def get_url_tools(url=None, url_mgr=None, return_dict: bool = False):
    mgr = UnifiedWebManager(url=url, url_mgr=url_mgr)
    if return_dict:
        return {'url': mgr.url, 'url_mgr': mgr.url_mgr}
    return _ToolProxy(mgr)

def get_req_tools(url=None, url_mgr=None, source_code=None, req_mgr=None, return_dict: bool = False):
    mgr = UnifiedWebManager(url=url, url_mgr=url_mgr, source_code=source_code, req_mgr=req_mgr)
    if return_dict:
        return {'url': mgr.url, 'url_mgr': mgr.url_mgr, 'source_code': mgr.source_code, 'req_mgr': mgr.req_mgr}
    return _ToolProxy(mgr)

def get_soup_tools(url=None, url_mgr=None, source_code=None, req_mgr=None, soup=None, soup_mgr=None,
                   target_manager=None, return_dict: bool = False):
    mgr = UnifiedWebManager(url=url, url_mgr=url_mgr, source_code=source_code, req_mgr=req_mgr, soup_mgr=soup_mgr, soup=soup)
    if target_manager:
        return mgr.endow_to_manager(target_manager)
    if return_dict:
        return mgr.get_all_tools()  # keeps old behavior if requested
    return _ToolProxy(mgr)          # << faux manager by default
