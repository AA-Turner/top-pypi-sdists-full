"""Regression tests for the videoDownloader + usurpManager daisy-chain revision.

Both managers used to roll their own bare ``requests.Session()`` with a
hardcoded user agent (bypassing the cipher/SSL/proxy/agent stack) and re-fetch
pages they already had. These tests pin the fixed behaviour:

- ``get_managed_session`` returns a configured session without fetching, and
  reuses an existing ``req_mgr``'s session.
- ``VideoDownloader`` pulls its user agent / session from the request stack and
  reuses an injected ``req_mgr``.
- ``usurpManager`` reuses an injected ``req_mgr`` (and its session) instead of
  rebuilding, ``get_verified_mgr`` terminates instead of looping forever, and
  ``process_page`` fetches a page once.

Real manager modules are loaded under a controlled namespace with light fakes
for the heavy network siblings, so this runs with only ``requests`` and
``beautifulsoup4`` installed.

Run directly: ``python tests/test_video_usurp_chain.py``
"""
import importlib.util
import json
import logging
import os
import re
import shutil
import sys
import time
import types
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src", "abstract_webtools", "managers",
)


def _pkg(name):
    m = types.ModuleType(name)
    m.__path__ = []
    sys.modules[name] = m
    return m


class _UA:
    def __init__(self, **k):
        self.user_agent = k.get("user_agent") or "MANAGED-UA"
        self.operating_system = "linux"

    def generate_for_url(self, url):
        return {"User-Agent": self.user_agent}

    def generate_headers(self, **k):
        return {"User-Agent": self.user_agent}

    def get_user_agent(self):
        return self.user_agent


def _get_ua_mgr(user_agent=None, ua_mgr=None, **k):
    return ua_mgr or _UA(user_agent=user_agent)


def _build_fake_namespace():
    _pkg("abstract_webtools")
    _pkg("abstract_webtools.managers")

    um = _pkg("abstract_webtools.managers.urlManager")

    class urlManager:
        def __init__(self, url=None, session=None):
            self.url = url
            self.domain = "x"
            self.protocol = "https"
            self.session = session

        def update_url(self, url):
            self.url = url

    def get_url_mgr(url=None, url_mgr=None):
        return url_mgr or urlManager(url)

    def get_url(url=None, url_mgr=None):
        return get_url_mgr(url=url, url_mgr=url_mgr).url

    um.urlManager = urlManager
    um.get_url_mgr = get_url_mgr
    um.get_url = get_url

    ua = _pkg("abstract_webtools.managers.userAgentManager")
    for k, v in dict(
        requests=requests, logging=logging, json=json, re=re, time=time,
        HTTPAdapter=HTTPAdapter, BeautifulSoup=BeautifulSoup,
        UserAgentManager=_UA, get_ua_mgr=_get_ua_mgr,
    ).items():
        setattr(ua, k, v)

    ci = _pkg("abstract_webtools.managers.cipherManager")
    ci.CipherManager = type(
        "CipherManager", (object,),
        {"__init__": lambda s: setattr(s, "ciphers_string", "X")},
    )
    ssm = _pkg("abstract_webtools.managers.sslManager")
    ssm.SSLManager = type("SSLManager", (object,), {"__init__": lambda s, **k: None})
    tl = _pkg("abstract_webtools.managers.tlsAdapter")
    tl.TLSAdapter = type(
        "TLSAdapter", (HTTPAdapter,),
        {"__init__": lambda s, **k: HTTPAdapter.__init__(s)},
    )
    nm = _pkg("abstract_webtools.managers.networkManager")
    nm.NetworkManager = type(
        "NetworkManager", (object,),
        {"__init__": lambda s, **k: (
            setattr(s, "proxies", {}),
            setattr(s, "tls_adapter", HTTPAdapter()),
        )[0]},
    )
    sel = _pkg("abstract_webtools.managers.seleneumManager")
    sel.get_selenium_source = lambda url: (_ for _ in ()).throw(
        Exception("no selenium in test")
    )


def _load_into_pkg(pkgname, relpath):
    p = sys.modules.get(pkgname) or _pkg(pkgname)
    modname = pkgname + "." + os.path.basename(relpath)[:-3]
    spec = importlib.util.spec_from_file_location(modname, os.path.join(BASE, relpath))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    for n in dir(mod):
        if not n.startswith("_"):
            setattr(p, n, getattr(mod, n))
    return mod


def _load_module(modname, relpath):
    spec = importlib.util.spec_from_file_location(modname, os.path.join(BASE, relpath))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    return mod


def _setup():
    _build_fake_namespace()
    rm = _load_into_pkg(
        "abstract_webtools.managers.requestManager",
        "requestManager/requestManager.py",
    )
    sm = _load_into_pkg(
        "abstract_webtools.managers.soupManager", "soupManager/soupManager.py"
    )

    fetches = {"n": 0}

    def fake_try_request(self):
        fetches["n"] += 1
        return "<html><head><title>T</title></head><body><video src='/v.mp4'></video></body></html>"

    rm.requestManager.try_request = fake_try_request

    # videoDownloader needs a handful of helpers normally provided by the heavy
    # vendored imports tree; stub them.
    imp = _pkg("abstract_webtools.managers.imports")

    class _Lazy:
        def __getattr__(self, n):
            return _Lazy()

        def __call__(self, *a, **k):
            return _Lazy()

    imp.lazy_import = lambda *a, **k: _Lazy()
    imp.get_logFile = lambda *a, **k: logging.getLogger("vid")
    imp.get_time_stamp = lambda *a, **k: 0
    imp.subtract_it = imp.add_it = imp.divide_it = lambda *a, **k: 0
    imp.get_default_videos_dir = lambda *a, **k: "/tmp"
    imp.eatAll = lambda s, c: s
    imp.get_any_value = lambda *a, **k: None
    imp.get_file_parts = lambda p: {}
    imp.make_list = lambda x: x if isinstance(x, list) else [x]
    imp.write_to_file = lambda **k: None

    _load_into_pkg("abstract_webtools.managers.videoDownloader", "videoDownloader/imports.py")
    vd = _load_into_pkg(
        "abstract_webtools.managers.videoDownloader", "videoDownloader/videoDownloader.py"
    )

    # usurpManager star-imports the whole managers package namespace.
    mgrs = sys.modules["abstract_webtools.managers"]
    for k, v in dict(
        get_req_mgr=rm.get_req_mgr, get_ua_mgr=_get_ua_mgr,
        requestManager=rm.requestManager, soupManager=sm.soupManager,
        get_soup_mgr=sm.get_soup_mgr, BeautifulSoup=BeautifulSoup,
        urljoin=urljoin, urlparse=urlparse, os=os, time=time,
        requests=requests, write_to_file=lambda **k: None,
        make_list=lambda x: x if isinstance(x, list) else [x],
    ).items():
        setattr(mgrs, k, v)
    usp = _load_module(
        "abstract_webtools.managers.usurpManager.usurpit", "usurpManager/usurpit.py"
    )

    return rm, sm, vd, usp, fetches


def run():
    rm, sm, vd, usp, fetches = _setup()

    # get_managed_session builds a configured session without fetching
    fetches["n"] = 0
    s = rm.get_managed_session(user_agent="MANAGED-UA")
    assert isinstance(s, requests.Session)
    assert fetches["n"] == 0

    # ...and reuses an existing req_mgr's session
    r = rm.requestManager(url=None, user_agent="MANAGED-UA")
    assert rm.get_managed_session(req_mgr=r) is r.session

    # requestManager(url=None) performs no network fetch
    fetches["n"] = 0
    rm.requestManager(url=None)
    assert fetches["n"] == 0

    # VideoDownloader pulls managed UA + session, no fetch in ctor
    vd.VideoDownloader.send_to_dl = lambda self: None
    fetches["n"] = 0
    v = vd.VideoDownloader(url="http://x/video", download_video=False, get_info=False)
    assert v.user_agent == "MANAGED-UA"
    assert isinstance(v.session, requests.Session)
    assert v.header == {"User-Agent": "MANAGED-UA"}
    assert fetches["n"] == 0

    # ...and reuses an injected req_mgr session
    r3 = rm.requestManager(url=None, user_agent="MANAGED-UA")
    v2 = vd.VideoDownloader(url="http://x/v", download_video=False, req_mgr=r3)
    assert v2.session is r3.session

    import inspect
    assert "session" in inspect.signature(vd.download_image).parameters
    assert "session" in inspect.signature(vd.get_thumbnails).parameters
    assert "req_mgr" in inspect.signature(vd.for_dl_video).parameters

    # usurpManager reuses an injected req_mgr + session, no fetch in ctor
    fetches["n"] = 0
    r4 = rm.requestManager(url=None, user_agent="MANAGED-UA")
    out_dir = os.path.join("/tmp", "usurp_regression_test")
    site = usp.usurpManager("http://x", req_mgr=r4, output_dir=out_dir)
    assert site.req_mgr is r4
    assert site.session is r4.session
    assert "MANAGED-UA" in site.USER_AGENT
    assert fetches["n"] == 0

    # get_verified_mgr terminates (no infinite loop) and reuses its req_mgr
    fetches["n"] = 0
    smgr = usp.get_verified_mgr("http://x")
    assert smgr.req_mgr is not None
    assert fetches["n"] == 1

    # process_page fetches a link-less page exactly once via the managed session
    fetches["n"] = 0

    class _Resp:
        text = "<html><body>no links</body></html>"

    def _counting_get(url, **k):
        fetches["n"] += 1
        return _Resp()

    r4.session.get = _counting_get
    try:
        site.process_page("http://x/page", 0, "x")
        assert fetches["n"] == 1
    finally:
        shutil.rmtree(out_dir, ignore_errors=True)


def test_video_and_usurp_reuse_managed_stack():
    run()


if __name__ == "__main__":
    run()
    print("OK: videoDownloader + usurpManager reuse the managed request stack")
