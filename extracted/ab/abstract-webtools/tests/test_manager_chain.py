"""Regression tests for the manager dependency chain.

The manager classes used to "daisy chain" into one another: every factory
(``get_req_mgr`` / ``get_soup_mgr`` / ...) and every constructor rebuilt the
whole url -> request -> soup chain from scratch, and ``get_soup_mgr`` even
discarded an already-populated ``req_mgr`` and triggered a fresh network fetch.

These tests pin the fixed behaviour: when source code (or an already-built
manager) is supplied, the chain is reused and the page is fetched **zero**
times. They load the real manager modules under a controlled namespace with
light fakes for the heavy network siblings, so they run with only ``requests``
and ``beautifulsoup4`` installed (no selenium/playwright/etc.).

Run directly: ``python tests/test_manager_chain.py``
"""
import importlib.util
import json
import logging
import os
import re
import sys
import time
import types

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

BASE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "src", "abstract_webtools", "managers",
)

HTML = "<html><head><title>T</title></head><body><a href='/a'>A</a></body></html>"


def _pkg(name):
    m = types.ModuleType(name)
    m.__path__ = []
    sys.modules[name] = m
    return m


def _build_fake_namespace():
    """Register abstract_webtools.managers.* with light fakes for heavy deps."""
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

        def get_relative_href(self, base, href):
            return href

        def is_valid_url(self, url=None):
            return True

        def make_valid(self, href, base=None):
            return href

        def url_join(self, url=None, path=None):
            return (url or "") + "/" + (path or "")

    def get_url_mgr(url=None, url_mgr=None):
        return url_mgr or urlManager(url)

    def get_url(url=None, url_mgr=None):
        return get_url_mgr(url=url, url_mgr=url_mgr).url

    um.urlManager = urlManager
    um.get_url_mgr = get_url_mgr
    um.get_url = get_url

    ua = _pkg("abstract_webtools.managers.userAgentManager")

    class _UA:
        user_agent = "UA"

        def generate_for_url(self, url):
            return {"User-Agent": self.user_agent}

    def get_ua_mgr(user_agent=None, ua_mgr=None, **k):
        return ua_mgr or _UA()

    # requestManager pulls stdlib/3rd-party names via star-imports off its
    # siblings; expose them here so the real module loads unmodified.
    for k, v in dict(
        requests=requests, logging=logging, json=json, re=re, time=time,
        HTTPAdapter=HTTPAdapter, BeautifulSoup=BeautifulSoup,
        UserAgentManager=_UA, get_ua_mgr=get_ua_mgr,
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


def _load_modules():
    _build_fake_namespace()
    rm = _load_into_pkg(
        "abstract_webtools.managers.requestManager",
        "requestManager/requestManager.py",
    )
    sm = _load_into_pkg(
        "abstract_webtools.managers.soupManager", "soupManager/soupManager.py"
    )
    lm = _load_into_pkg(
        "abstract_webtools.managers.linkManager", "linkManager/linkManager.py"
    )
    _pkg("abstract_webtools.managers.middleManager")
    _pkg("abstract_webtools.managers.middleManager.src")
    spec = importlib.util.spec_from_file_location(
        "abstract_webtools.managers.middleManager.src.UnifiedWebManager",
        os.path.join(BASE, "middleManager/src/UnifiedWebManager.py"),
    )
    uw = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = uw
    spec.loader.exec_module(uw)
    return rm, sm, lm, uw


def run():
    rm, sm, lm, uw = _load_modules()

    fetches = {"n": 0}

    def fake_try_request(self):
        fetches["n"] += 1
        return HTML

    rm.requestManager.try_request = fake_try_request

    # get_req_mgr reuses a supplied manager verbatim (no rebuild/refetch)
    fetches["n"] = 0
    r1 = rm.requestManager(url="http://x", source_code=HTML)
    n0 = fetches["n"]
    assert rm.get_req_mgr(req_mgr=r1) is r1
    assert fetches["n"] == n0

    # get_source short-circuits on raw source code
    fetches["n"] = 0
    assert rm.get_source(source_code=HTML) == HTML
    assert fetches["n"] == 0

    # get_soup_mgr threads source through and never drops it
    fetches["n"] = 0
    g = sm.get_soup_mgr(source_code=HTML)
    assert g.source_code == HTML
    assert g.soup.title.text == "T"
    assert fetches["n"] == 0

    # the headline bug: a populated req_mgr must not be refetched
    r2 = rm.requestManager(url="http://x", source_code=HTML)
    base = fetches["n"]
    g2 = sm.get_soup_mgr(req_mgr=r2)
    assert g2.source_code == HTML
    assert fetches["n"] == base

    # higher managers share one chain
    fetches["n"] = 0
    link = lm.linkManager(url="http://x", source_code=HTML)
    assert link.source_code == HTML
    assert link.soup.title.text == "T"
    assert fetches["n"] == 0

    fetches["n"] = 0
    u = uw.UnifiedWebManager(url="http://x", source_code=HTML)
    assert u.soup.title.text == "T"
    assert u.source_code == HTML
    assert u.link_mgr.source_code == HTML
    assert fetches["n"] == 0


def test_manager_chain_reuses_without_refetch():
    run()


if __name__ == "__main__":
    run()
    print("OK: manager chain reuses dependencies without refetching")
