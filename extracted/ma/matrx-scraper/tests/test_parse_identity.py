"""Seeded identity corpus for the page parse: a change that alters ANY parse output goes red.

Every stage's result is pinned through what a caller receives from the three
entry points — ``_parse_html_sync`` (the extraction-rules dict + links),
``ParserOrchestrator.parse_content`` (overview, text, main content and its
selector, every stage's removal details, hashes, links; ``organized_data`` is
covered through the first) and ``clean_page_content`` — over a compact corpus
built for the cases a shared parse tree could break: scripts, iframes, malformed
nesting, big tables, a stage removing what a later stage would read, listing and
article pages, the content filter's text rule at and around its length, string
classes on transformer-made tags, entities, processing instructions, literal
wrapper tag names, plus seeded random pages.

Run twice — with no ad-block list (the fetch fails, nothing saved) and with one
served by the single per-process fetch — so the ad-domain media filter is pinned
both ways; plus the content filter with a PARTIAL text rule (no default rule has
one). The expected hashes in fixtures/parse_identity_expected.json were produced by
the parser BEFORE the one-tree rewrite (2026-11-15) and must only ever be regenerated
for an output change someone means to make:
``python packages/matrx-scraper/tests/test_parse_identity.py --write``.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from pathlib import Path

import pytest

EXPECTED = Path(__file__).parent / "fixtures" / "parse_identity_expected.json"
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def _bench(n: int) -> str:
    body = "".join(
        f'<div class="item"><h2>Heading {i}</h2><p>Some paragraph text number {i} with <a href="/p/{i}">a link</a>'
        f' and <b>bold</b>.</p><img src="/i{i}.png" alt="x"><ul><li>a</li><li>b</li></ul></div>'
        for i in range(n)
    )
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": "x"})
    return (
        f'<html><head><title>T</title><meta name="description" content="d"><script type="application/ld+json">{ld}'
        f"</script></head><body><nav><a href='/'>home</a></nav>{body}<footer>(c) 2026 call 555-123-4567</footer>"
        "</body></html>"
    )


def corpus() -> list[tuple[str, str]]:
    para = "<p>" + "Real article sentence with words. " * 40 + "</p>"
    pages = {
        "bench20": _bench(20),
        "bench60": _bench(60),
        "article": "<html><head><title>Story</title><meta property='og:image' content='https://example.test/i.png'>"
        "<link rel=canonical href='https://example.test/s'></head><body><header class='site-header'><nav>a b c</nav>"
        "</header><h1>Big headline</h1><p class='dek'>Dek</p><article>" + para + "<div class='share-buttons'>share"
        "</div>" + para + "<aside class='related-stories'>rel</aside><figure><img src='/a.jpg'><figcaption>cap"
        "</figcaption></figure><table><tr><th>h</th></tr><tr><td>1</td></tr></table><pre><code>x=1</code></pre>"
        "</article><footer>foot</footer></body></html>",
        "scripts": "<html><head><script>var x='<div class=ad>Advertisement</div>';</script><style>p{}</style></head>"
        "<body><div><script>if(a<b){}</script>text<script type='application/ld+json'>{\"@type\":\"Article\","
        "\"image\":\"https://example.test/i.jpg\"}</script></div><article>" + para + "<script>t()</script></article>"
        "</body></html>",
        "iframes": "<html><body><iframe src='https://www.youtube.com/embed/abc' width=560 height=315></iframe>"
        "<iframe data-src='https://player.vimeo.com/video/1'></iframe><iframe srcdoc='<p>inner</p>'></iframe>"
        "<p>after</p></body></html>",
        "malformed": "<p>a<div>b</p>c</div><a href=/x><a href=/y>nested</a></a><table>stray<tr><td>1<td>2</table>"
        "<li>orphan1<li>orphan2<ul><li>ok</ul><li>orphan3" + "<span>" * 120 + "deep" + "</div>" * 30,
        "table": "<html><body><table><thead><tr>"
        + "".join(f"<th>h{j}</th>" for j in range(12))
        + "</tr></thead>"
        + "".join("<tr>" + "".join(f"<td>r{i}c{j}</td>" for j in range(12)) + "</tr>" for i in range(40))
        + "</table><table role=presentation><tr><td><table><tr><td>nested</td></tr></table></td></tr></table>"
        "</body></html>",
        "noise_eats_main": "<html><body><nav class='site-nav'><article><p>" + "nav text " * 80 + "</p></article>"
        "</nav><div aria-hidden=true><main>" + para + "</main></div><main>" + para + "<a href='/m'>m</a></main>"
        "</body></html>",
        "filter_eats_root": "<html><body><div class='sidebar'><article>" + para + "</article></div><div class=content>"
        "<div class='advertisement'>Advertisement</div><div>Advertisement</div><span> Advertisement </span>"
        "<p>Ad<b>vertisement</b></p>" + para + "</div></body></html>",
        "text_rule": "<html><body>"
        + "".join(
            f"<div><span>{'Advertisement'[:k]}</span><!--c--><span>{'Advertisement'[k:]}</span></div>" for k in range(14)
        )
        + "<div><script>Advertisement</script></div><template>Advertisement</template></body></html>",
        "classes": "<html><body><div class='Promo x'>a</div><div class='header footer'>b</div><div class='mysocial'>c"
        "</div><div class='w3-sidebar'>f</div><div role='navigation banner'>g</div><div id='read-next'>h</div>"
        "<div name='nav-x'>i</div><div hidden>j</div><div style='DISPLAY: none'>k</div><div aria-hidden='TRUE'>m"
        "</div><p class='text-muted small'>n</p>" + para + "</body></html>",
        "carousel": "<html><body><bsp-carousel><h2 class='Carousel-title' data-override-title='T'>t</h2>"
        "<div class='Carousel-slide' data-slidenumber=1><span class='CarouselSlide-infoDescription'>d1</span>"
        "<picture><source srcset='/a.jpg 1x'><img src='/a.jpg'></picture></div></bsp-carousel>" + para + "</body></html>",
        "listing_roles": "<html><body><div role=main>"
        + "".join(f"<article><h2>t{i}</h2><p>{'word ' * 130}</p></article>" for i in range(6))
        + "</div><div itemprop=articleBody>" + para + para + "</div></body></html>",
        "headline_outside": "<html><body><div class='hero'><h1>Big</h1><p class=dek>dek</p></div>"
        "<div class='post-content'>" + para + para + "</div></body></html>",
        "media": "<html><body><ol><li>one<ol><li>a</li><li>b<ul><li>deep</li></ul></li></ol></li></ol><figure>"
        "<img src='/f.jpg' alt='f'><figcaption>cap</figcaption></figure><audio src='/a.mp3' controls></audio>"
        "<video poster='/p.jpg'><source src='/v.mp4' type='video/mp4'></video><p>inline <code>x</code></p>"
        "</body></html>",
        "entities": "<!DOCTYPE html><?xml version='1.0'?><html><body><p>&amp; &lt;b&gt; &nbsp; &#x1F600;</p>"
        "<p title='a&quot;b'>q</p><!-- a -- b -->" + para + "</body></html>",
        "wrapper_names": "<html><body><contentfilter type=x>kept</contentfilter><noiseremover>n</noiseremover>"
        + para + "</body></html>",
        "fragment": "<p>only fragment <a href='https://example.test/z'>z</a></p>",
        "ad_media": "<html><body><p>Story text before the ads.</p><img src='https://ads.blocked-example.com/b.png' alt='ad'>"
        "<img src='https://cdn.example.test/photo.png' alt='photo'><img src='https://sub.ib.adnxs-example.com/t.gif'>"
        "<picture><source srcset='https://ads.blocked-example.com/p.webp 1x'><img src='/local.jpg'></picture>"
        "<figure><img src='https://ads.blocked-example.com/f.jpg'><figcaption>ad cap</figcaption></figure>"
        "<img data-src='https://ads.blocked-example.com/lazy.jpg' src='data:image/gif;base64,R0lGOD'>"
        "<video src='https://ads.blocked-example.com/v.mp4'></video><iframe src='https://ads.blocked-example.com/i'>"
        "</iframe>" + para + "</body></html>",
        "partial_text": "<html><body><div>vert</div><span>xverty</span><p>ver</p><div><b>ve</b><i>rt</i></div>"
        "<p>Read more</p><p>Read mor</p>" + para + "</body></html>",
        "empty": "",
    }
    rnd = random.Random(20261115)
    tags = ["div", "p", "span", "a", "article", "main", "section", "aside", "nav", "header", "footer", "table",
            "tr", "td", "ul", "li", "script", "iframe", "img", "code", "pre", "h2", "form", "noscript"]
    attrs = ["class='article-body'", "class='ad'", "class='share'", "role='article'", "role='navigation'",
             "itemprop='articleBody'", "id='content'", "hidden", "aria-hidden='true'", "style='display:none'",
             "href='/x'", "src='/i.jpg'", "class='Promo'"]
    for k in range(8):
        parts = []
        for _ in range(rnd.randint(20, 300)):
            t = rnd.choice(tags)
            a = " ".join(rnd.sample(attrs, rnd.randint(0, 2)))
            parts.append(rnd.choice([f"<{t} {a}>", f"</{t}>", f"<{t} {a}>" + "Longer sentence of text. " * rnd.randint(0, 20)
                                     + f"</{t}>", "\n ", "Advertisement"]))
        pages[f"rand{k}"] = "<html><head><title>R</title></head><body>" + "".join(parts) + "</body></html>"
    return sorted(pages.items())


def _digest(value) -> str:
    text = _UUID.sub("<uuid>", json.dumps(value, default=repr, ensure_ascii=False, sort_keys=False))
    return hashlib.sha256(text.encode()).hexdigest()


def outputs() -> dict[str, str]:
    from matrx_scraper.clean_content import clean_page_content
    from matrx_scraper.parser.core import ParserOrchestrator, _parse_html_sync

    result: dict[str, str] = {}
    for name, html in corpus():
        url = f"https://example.test/{name}"
        runs = {
            "parse": lambda: _parse_html_sync(html, url),
            "full": lambda: {k: v for k, v in ParserOrchestrator().parse_content(html, url).items() if k != "organized_data"},
            "clean": lambda: clean_page_content(html, url),
        }
        for kind, run in runs.items():
            try:
                value = run()
            except Exception as exc:  # a page that fails must keep failing the same way
                value = f"EXC {type(exc).__name__}: {exc}"
            result[f"{name}/{kind}"] = _digest(value)
    return result


AD_LIST = "! test list\n||ads.blocked-example.com^\n||adnxs-example.com^\n"
#: A content filter with a PARTIAL text rule — the default overrides have none, so
#: this pins that branch of the compiled filter.
PARTIAL_TEXT_CONFIG = [
    {"attribute": "text", "exact": ["Advertisement"], "partial": ["vert", "Read more"], "regex": []},
    {"attribute": "class", "exact": [], "partial": ["ad", "share"], "regex": []},
]


def _fresh_lists(tmp_dir: Path, fetch) -> None:
    """A process that has loaded no ad-block list yet, saving to ``tmp_dir``, whose
    one fetch is ``fetch`` (never the network)."""
    from matrx_scraper.parser import utils

    class _Temp(utils.LocalTempFiles):
        @property
        def temp_dir(self) -> Path:
            return tmp_dir

    utils.DomainFilter._instances = {}
    utils.AdblockConfigLoader._instance = None
    getattr(utils, "_FILTER_LIST_STATUS", {}).clear()
    utils.default_file_manager = lambda: _Temp("scraper")
    utils.httpx.get = fetch


def _serve_list(url, **_kwargs):
    return type("R", (), {"status_code": 200, "text": AD_LIST})()


def _fail_fetch(url, **_kwargs):
    raise OSError("no network in tests")


def filter_outputs() -> dict[str, str]:
    from bs4 import BeautifulSoup

    from matrx_scraper.parser.scrape_filter import ScrapeFilter

    result = {}
    for name, html in corpus():
        for remove in (False, True):
            soup = BeautifulSoup(html, "lxml")
            try:
                value = str(ScrapeFilter().filter_soup(soup, content_filter_config=PARTIAL_TEXT_CONFIG, remove=remove))
            except Exception as exc:
                value = f"EXC {type(exc).__name__}: {exc}"
            result[f"{name}/filter_partial_text/{int(remove)}"] = _digest(value)
    return result


def all_outputs(tmp_dir: Path) -> dict[str, str]:
    """No list (fetch fails, no saved copy) — then a list served by the one fetch."""
    _fresh_lists(tmp_dir / "absent", _fail_fetch)
    out = {f"no_list/{k}": v for k, v in outputs().items()}
    _fresh_lists(tmp_dir / "present", _serve_list)
    out.update({f"list/{k}": v for k, v in outputs().items()})
    out.update(filter_outputs())
    return out


@pytest.fixture
def _restore_lists():
    from matrx_scraper.parser import utils

    saved = (utils.DomainFilter._instances, utils.AdblockConfigLoader._instance, utils.default_file_manager, utils.httpx.get)
    yield
    utils.DomainFilter._instances, utils.AdblockConfigLoader._instance, utils.default_file_manager, utils.httpx.get = saved
    utils._FILTER_LIST_STATUS.clear()


def test_parse_outputs_are_identical_to_the_frozen_corpus(tmp_path, _restore_lists):
    expected = json.loads(EXPECTED.read_text(encoding="utf-8"))
    got = all_outputs(tmp_path)
    changed = sorted(k for k in expected if got.get(k) != expected[k])
    assert set(got) == set(expected), "the corpus changed; regenerate only for an intended change"
    assert not changed, f"parse output changed for {len(changed)} of {len(expected)} cases: {changed[:12]}"
    # The list really was in force: an ad image is dropped only with it.
    assert got["list/ad_media/parse"] != got["no_list/ad_media/parse"]


if __name__ == "__main__":
    if "--write" in sys.argv:
        import tempfile

        EXPECTED.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp:
            EXPECTED.write_text(json.dumps(all_outputs(Path(tmp)), indent=1, sort_keys=True) + "\n", encoding="utf-8")
        print("wrote", EXPECTED)
