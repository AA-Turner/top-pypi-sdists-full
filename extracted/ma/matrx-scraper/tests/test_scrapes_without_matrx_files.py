"""matrx-files is an OPTIONAL extra (`matrx-scraper[files]`): the scraper imports and scrapes without it.

Break caught: a module-scope ``from matrx_files import ...`` anywhere on the scrape path, which
makes every host that ships only the HTTP lane (Matrx 2's tools service) carry matrx-files and its
dependency tree. The only thing that lane used it for was saving the ad-block filter list, which
now goes through plain file I/O to the very same place (``BASE_DIR/temp/scraper/``).

Runs in a fresh interpreter whose import system refuses ``matrx_files``, exactly as if it were
not installed. The page fetch and the filter-list download are stubbed (no network); the parse,
the ad-block filter and the file write are real.
"""

from __future__ import annotations

import json
import subprocess
import sys
import textwrap
from pathlib import Path

_CHILD = textwrap.dedent(
    r"""
    import asyncio, importlib.abc, json, sys
    from pathlib import Path

    class _NoMatrxFiles(importlib.abc.MetaPathFinder):
        def find_spec(self, name, path, target=None):
            if name == "matrx_files" or name.startswith("matrx_files."):
                raise ModuleNotFoundError(f"No module named {name!r}", name=name)

    sys.meta_path.insert(0, _NoMatrxFiles())
    home = Path(sys.argv[1])

    from matrx_utils.conf import configure_settings
    configure_settings(type("S", (), {"BASE_DIR": home}))

    import requests

    class _List:
        status_code = 200
        text = "! test list\n||ads.blocked-example.com^\n"

    requests.get = lambda url, timeout=10: _List()

    from matrx_scraper import orchestrator
    from matrx_scraper.scraper import ContentType, RequestType, Response

    html = (
        "<html><head><title>Plain page</title></head><body><h1>Hello</h1>"
        "<p>Some visible text content for the page, long enough to count as a page.</p>"
        "<img src='https://ads.blocked-example.com/banner.png' alt='ad'>"
        "<img src='https://cdn.allowed-example.com/photo.png' alt='photo'>"
        "</body></html>"
    )

    async def fake_fetch(url, request_type=RequestType.NORMAL, proxy=None, user_agent=None):
        return Response(
            request_url=url, proxy_used=False, request_type=RequestType.NORMAL,
            content_type=ContentType.HTML, extension="", content_type_raw="text/html",
            response_url=url, response_headers={"content-type": "text/html"}, title="Plain page",
            status_code=200, content=html,
        )

    orchestrator.fetch = fake_fetch
    result = asyncio.run(orchestrator.scrape("https://example.com/", use_proxy=False, escalate=False))
    from matrx_scraper.parser.utils import DomainFilter
    domain_filter = DomainFilter("easylist")
    saved = home / "temp" / "scraper" / "easylist-filters.txt"
    print(json.dumps({
        "matrx_files_loaded": any(m == "matrx_files" or m.startswith("matrx_files.") for m in sys.modules),
        "success": result.success,
        "failure_reason": result.failure_reason,
        "text": result.text_data or "",
        "blocks_ad": domain_filter.should_block("https://ads.blocked-example.com/banner.png"),
        "allows_other": not domain_filter.should_block("https://cdn.allowed-example.com/photo.png"),
        "saved_list": saved.read_text() if saved.exists() else None,
    }))
    """
)


def test_scrape_runs_and_saves_the_filter_list_with_matrx_files_absent(tmp_path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, "-c", _CHILD, str(tmp_path)],
        capture_output=True,
        text=True,
        timeout=120,
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stderr[-4000:]
    out = json.loads(proc.stdout.strip().splitlines()[-1])

    assert out["matrx_files_loaded"] is False
    assert out["success"] is True, out["failure_reason"]
    assert "Hello" in out["text"]
    assert out["blocks_ad"] is True
    assert out["allows_other"] is True
    assert out["saved_list"] is not None and "||ads.blocked-example.com^" in out["saved_list"]
