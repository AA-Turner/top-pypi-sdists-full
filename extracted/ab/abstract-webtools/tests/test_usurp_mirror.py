"""Regression test for usurpManager's full-site mirroring.

usurpManager must grab the *entire* site and associate everything so the saved
copy renders offline with styles intact: HTML pages, stylesheets (following
``@import`` and ``url(...)`` including @font-face / CDN fonts), ``srcset``,
inline ``style`` attributes and ``<style>`` blocks, scripts, images and other
linked assets — every reference rewritten to a relative local path, and shared
assets fetched only once.

The real usurpit module is loaded under a controlled namespace with a fake
in-memory site served through a fake session, so this runs with only
``requests`` + ``beautifulsoup4`` installed.

Run directly: ``python tests/test_usurp_mirror.py``
"""
import hashlib
import importlib.util
import os
import re
import shutil
import sys
import tempfile
import time
import types
from urllib.parse import urldefrag, urljoin, urlparse

import requests
from bs4 import BeautifulSoup

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
        self.user_agent = "UA"
        self.operating_system = "linux"

    def get_user_agent(self):
        return self.user_agent

    def generate_headers(self, **k):
        return {"User-Agent": self.user_agent}


class _URLM:
    def __init__(self, url=None):
        self.url = url


class _ReqM:
    def __init__(self, url=None, **k):
        self.url = url
        self.url_mgr = _URLM(url)
        self.ua_mgr = _UA()
        self.user_agent = "UA"
        self.session = requests.Session()


SITE = {
    "http://site.test/": """<html><head>
   <link rel="stylesheet" href="/css/app.css?v=2">
   <link rel="icon" href="favicon.ico">
   <style>.hero{background:url('/img/bg.png')}</style>
 </head><body>
   <img src="/img/logo.png" srcset="/img/logo.png 1x, /img/logo@2x.png 2x">
   <div style="background:url(/img/inline.png)"></div>
   <script src="/js/app.js"></script>
   <a href="/about">About</a>
   <a href="https://external.test/page">ext</a>
   <a href="/files/doc.pdf">doc</a>
 </body></html>""",
    "http://site.test/about": """<html><head>
   <link rel="stylesheet" href="/css/app.css?v=2"></head>
   <body><img src="/img/logo.png"><a href="/">home</a></body></html>""",
    "http://site.test/css/app.css?v=2": (
        "@import \"/css/base.css\";\n"
        ".x{background:url('../img/sprite.png')} "
        "@font-face{src:url('https://cdn.test/font.woff2')}"
    ),
    "http://site.test/css/base.css": "body{background:url('/img/body.png')}",
}


class _FakeResp:
    def __init__(self, url):
        self.url = url
        self.headers = {}
        self._text = SITE.get(url, "")
        self.status_code = 200
        if url.endswith('.css') or 'app.css' in url:
            self.headers['Content-Type'] = 'text/css'
        self._content = self._text.encode() if url in SITE else b"BINARY:" + url.encode()

    @property
    def text(self):
        return self._text

    def raise_for_status(self):
        pass

    def iter_content(self, n):
        yield self._content


def _load_usurpit():
    _pkg("abstract_webtools")
    mgrs = _pkg("abstract_webtools.managers")

    def get_req_mgr(url=None, url_mgr=None, **k):
        return _ReqM(url=url)

    def get_ua_mgr(user_agent=None, ua_mgr=None, **k):
        return ua_mgr or _UA()

    for k, v in dict(
        get_req_mgr=get_req_mgr, get_ua_mgr=get_ua_mgr, requestManager=_ReqM,
        soupManager=object, get_soup_mgr=lambda **k: None, BeautifulSoup=BeautifulSoup,
        urljoin=urljoin, urlparse=urlparse, os=os, time=time, requests=requests,
        write_to_file=lambda **k: None,
        make_list=lambda x: x if isinstance(x, list) else [x],
    ).items():
        setattr(mgrs, k, v)

    spec = importlib.util.spec_from_file_location(
        "abstract_webtools.managers.usurpManager.usurpit",
        os.path.join(BASE, "usurpManager/usurpit.py"),
    )
    usp = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = usp
    spec.loader.exec_module(usp)
    return usp, get_req_mgr


def run():
    usp, get_req_mgr = _load_usurpit()

    hits = {}

    class _FakeSession(requests.Session):
        def get(self, url, **k):
            u, _ = urldefrag(url)
            hits[u] = hits.get(u, 0) + 1
            return _FakeResp(u)

    out = tempfile.mkdtemp(prefix="usurp_mirror_")
    try:
        r = get_req_mgr(url="http://site.test/")
        r.session = _FakeSession()
        site = usp.usurpManager("http://site.test/", req_mgr=r, output_dir=out, max_depth=3)
        site.main()

        def exists(p):
            return os.path.isfile(os.path.join(out, p))

        css_name = "css/app__%s.css" % hashlib.md5(b"v=2").hexdigest()[:8]

        # 1) every page + asset mirrored, incl @import target, css url() sprite,
        #    inline/style-block images, srcset variant, favicon, js, linked pdf,
        #    and the cross-domain @font-face woff2 under _external/.
        for p in ["index.html", "about.html", css_name, "css/base.css",
                  "img/logo.png", "img/logo@2x.png", "img/bg.png", "img/inline.png",
                  "favicon.ico", "js/app.js", "img/sprite.png", "img/body.png",
                  "files/doc.pdf", "_external/cdn.test/font.woff2"]:
            assert exists(p), f"missing mirrored file: {p}"

        # 2) html references rewritten to relative local paths; external left alone
        idx = open(os.path.join(out, "index.html")).read()
        assert "http://site.test" not in idx
        assert 'css/app__' in idx
        assert '"/img/logo.png"' not in idx
        assert 'srcset="img/logo.png 1x, img/logo@2x.png 2x"' in idx
        assert "url(img/inline.png)" in idx or "url('img/inline.png')" in idx
        assert 'href="about.html"' in idx
        assert 'https://external.test/page' in idx
        assert 'href="files/doc.pdf"' in idx

        # 3) CSS @import + url() rewritten, nested + cross-domain refs resolved
        base_css = open(os.path.join(out, "css/base.css")).read()
        assert "../img/body.png" in base_css
        app_css = open(os.path.join(out, css_name)).read()
        assert "base.css" in app_css and "http://site.test" not in app_css
        assert "../_external/cdn.test/font.woff2" in app_css

        # 4) shared assets fetched exactly once (consistent url_map)
        assert hits["http://site.test/css/app.css?v=2"] == 1
        assert hits["http://site.test/img/logo.png"] == 1
    finally:
        shutil.rmtree(out, ignore_errors=True)


def run_depth():
    """Default crawl is unlimited-depth (captures the whole site); an explicit
    max_depth still bounds it."""
    usp, get_req_mgr = _load_usurpit()

    n = 9  # chain deeper than the previous default of 5
    chain = {f"http://s.test/p{i}": f"<html><body><a href='/p{i+1}'>n</a></body></html>"
             for i in range(n - 1)}
    chain[f"http://s.test/p{n - 1}"] = "<html><body>end</body></html>"
    chain["http://s.test/"] = "<html><body><a href='/p0'>start</a></body></html>"

    class _Resp:
        def __init__(self, u):
            self._t = chain.get(u, "")
            self.headers = {}
            self.status_code = 200

        @property
        def text(self):
            return self._t

        def raise_for_status(self):
            pass

        def iter_content(self, n):
            yield b""

    class _Sess(requests.Session):
        def get(self, url, **k):
            u, _ = urldefrag(url)
            return _Resp(u)

    # default => unlimited: reaches every deep page
    out = tempfile.mkdtemp(prefix="usurp_depth_")
    try:
        r = get_req_mgr(url="http://s.test/")
        r.session = _Sess()
        site = usp.usurpManager("http://s.test/", req_mgr=r, output_dir=out)
        assert site.MAX_DEPTH is None  # default is unlimited
        res = site.main()
        for i in range(n):
            assert f"http://s.test/p{i}" in res["pages"], f"missed /p{i}"
    finally:
        shutil.rmtree(out, ignore_errors=True)

    # explicit cap is honored
    out2 = tempfile.mkdtemp(prefix="usurp_depth2_")
    try:
        r2 = get_req_mgr(url="http://s.test/")
        r2.session = _Sess()
        site2 = usp.usurpManager("http://s.test/", req_mgr=r2, output_dir=out2, max_depth=2)
        res2 = site2.main()
        assert "http://s.test/p1" in res2["pages"]
        assert "http://s.test/p2" not in res2["pages"]
    finally:
        shutil.rmtree(out2, ignore_errors=True)


def test_usurp_mirrors_full_site_with_styles():
    run()


def test_default_crawl_is_unlimited_depth():
    run_depth()


if __name__ == "__main__":
    run()
    run_depth()
    print("OK: usurpManager mirrors the full site (pages, css/@import/fonts, "
          "srcset, inline styles) with references rewritten, and crawls the "
          "whole site by default (unlimited depth)")
