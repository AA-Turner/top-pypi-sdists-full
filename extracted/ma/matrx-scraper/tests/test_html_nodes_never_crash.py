"""A page can never segfault the process that reads it.

2026-10-16: ``flatten_tel_links`` selected ``a[href^="tel:"], a[href^="TEL:"]``; selectolax returned every phone link
twice (one entry per selector) and the second ``replace_with`` wrote to freed memory. Exit 139 — the workflow worker
died nine times and the API server three in 25 minutes, all on one brewery's single phone link. A segfault cannot be
caught, so the crash cases run in a child interpreter and the test reads its exit code: before the fix these exit
-11 (SIGSEGV); after it they exit 0 with the right text.
"""

from __future__ import annotations

import asyncio
import subprocess
import sys

import pytest

#: The page that crashed production, reduced: two copies of one phone link (header + footer), icon spans inside.
PHONE_PAGE = """<html><body>
<header><nav role="navigation"><ul class="menu"><li><a href="/">Home</a></li></ul></nav>
<ul><li><a href="tel:775-420-4256"><span class="ltx-ic icon icon-call"></span><span class="txt">775.420.4256</span></a></li></ul>
</header>
<main><h1>Parlay Brewing</h1><p>Small-batch beer brewed in Reno, poured fresh in our taproom every day of the week.</p>
<p>Questions? <a href="TEL:+17754204256">Call us</a> or <a href="tel:775">(</a><a href="tel:775">775) 420-4256</a>.</p></main>
<footer role="contentinfo"><svg><script>x()</script><title>i</title></svg>
<ul><li><a href="tel:775-420-4256"><span class="ltx-ic icon icon-call"></span><span class="txt">775.420.4256</span></a></li></ul>
<p>123 Main Street, Reno, NV 89501</p></footer>
</body></html>"""


def _run(code: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120)


def test_one_phone_link_flattens_without_crashing() -> None:
    r = _run(
        "from selectolax.parser import HTMLParser\n"
        "from matrx_scraper.clean_content import flatten_tel_links\n"
        "t = HTMLParser('<p><a href=\"tel:1\">111</a></p>')\n"
        "flatten_tel_links(t)\n"
        "print(t.body.html)\n"
    )
    assert r.returncode == 0, f"exit {r.returncode} (-11 is the segfault): {r.stderr[-600:]}"
    assert r.stdout.strip() == "<body><p>111</p></body>"


def test_production_page_cleans_without_crashing() -> None:
    import json

    r = _run(
        "import json, sys\n"
        "from matrx_scraper.clean_content import clean_page_content, contact_footer_text\n"
        f"html = {PHONE_PAGE!r}\n"
        "print(json.dumps([clean_page_content(html, 'https://example.com/'), contact_footer_text(html)]))\n"
    )
    assert r.returncode == 0, f"exit {r.returncode} (-11 is the segfault): {r.stderr[-600:]}"
    text, footer = json.loads(r.stdout.strip().splitlines()[-1])
    assert "Small-batch beer" in text
    assert "Call us +17754204256" in text  # a worded link keeps its number
    assert "(775) 420-4256" in text  # a number split across links reads as one
    assert "<a" not in text and "tel:" not in text
    assert footer and "775.420.4256" in footer and "x()" not in footer


def test_each_live_node_visits_each_node_once_and_never_a_freed_one() -> None:
    from selectolax.parser import HTMLParser

    from matrx_scraper.html_nodes import decompose_all, each_live_node

    tree = HTMLParser('<nav role="navigation"><nav id="inner"><a>x</a></nav></nav><p>keep</p>')
    nodes = tree.css("nav, [role=navigation], #inner")
    assert len(nodes) > len({n.mem_id for n in nodes})  # the group really lists one element twice

    seen: list[str] = []

    def step(node: object) -> bool:
        seen.append(node.attributes.get("id") or node.tag)  # type: ignore[attr-defined]
        node.decompose()  # type: ignore[attr-defined]
        return True

    assert each_live_node(nodes, step) == 1  # the outer nav only: its duplicate and its insides are skipped
    assert seen == ["nav"]
    assert tree.body.html == "<body><p>keep</p></body>"

    tree = HTMLParser('<header><nav><a>x</a></nav></header><footer><script>s</script></footer><p>keep</p>')
    # Listed per selector: the inner <nav> comes first (removed), then <header> and <footer>; the <script> inside the
    # removed footer is skipped, never touched.
    assert decompose_all(tree.css("nav, header, footer, script")) == 3
    assert tree.body.html == "<body><p>keep</p></body>"


def test_run_isolated_turns_a_segfault_into_an_error_and_the_caller_lives() -> None:
    from matrx_scraper.isolated import IsolatedCallFailed, run_isolated

    with pytest.raises(IsolatedCallFailed) as crash:
        asyncio.run(run_isolated("ctypes:string_at", 0))  # reads address 0: a real SIGSEGV in the child
    assert crash.value.signal_name == "SIGSEGV"
    assert "died (SIGSEGV)" in str(crash.value)

    with pytest.raises(IsolatedCallFailed) as raised:
        asyncio.run(run_isolated("json:loads", "not json"))
    assert "JSONDecodeError" in raised.value.reason and raised.value.signal_name is None

    out = asyncio.run(run_isolated("matrx_scraper.clean_content:page_prepass", PHONE_PAGE))
    assert "tel:" not in out["html"] and "775.420.4256" in out["footer"]


def test_run_isolated_kills_a_child_that_never_answers() -> None:
    from matrx_scraper.isolated import IsolatedCallFailed, run_isolated

    with pytest.raises(IsolatedCallFailed, match="no answer within 0.5s"):
        asyncio.run(run_isolated("time:sleep", 30, limit_seconds=0.5))
