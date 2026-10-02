"""Click-Play trial: DataForSEO Labs keywords for site (live).

Expand from a domain/URL into keywords DataForSEO associates with that target.
Volume/CPC/competition come back on each item.

Edit the constants in the ``if __name__`` block and run the file
(Cmd+Shift+B / ``.venv/bin/python`` on this path).

Hits the real API via ``DataForSeoClient`` + ``AsyncHttpTransport``. Costs money.
Credentials: ``DATA_FOR_SEO_EMAIL`` / ``DATA_FOR_SEO_PASSWORD`` in aidream ``.env``.

Endpoint:
  * POST /v3/dataforseo_labs/google/keywords_for_site/live
"""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ in (None, ""):
    _pkg_root = Path(__file__).resolve().parents[2]
    if str(_pkg_root) not in sys.path:
        sys.path.insert(0, str(_pkg_root))
    __package__ = "trials.dataforseo"

import asyncio
from typing import Any

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[4] / ".env")

from matrx_utils import cleanup_async_resources, clear_terminal, vcprint  # noqa: E402

from matrx_seo.providers.dataforseo.contracts import DataForSeoOperationName  # noqa: E402

from .trial_runtime import run_live  # noqa: E402


async def run_keywords_for_site(**task: Any) -> dict[str, Any]:
    return await run_live(
        operation=DataForSeoOperationName.LABS_GOOGLE_KEYWORDS_FOR_SITE,
        endpoint_label="POST /v3/dataforseo_labs/google/keywords_for_site/live",
        task=dict(task),
    )


async def main(test_name: str, args: dict[str, Any]) -> Any:
    vcprint(f"\n[TRIAL] {test_name}", color="magenta")
    if test_name == "keywords_for_site":
        return await run_keywords_for_site(**args)
    raise ValueError(f"Invalid test_name: {test_name}")


# ============================================================================
# EXAMPLE USAGE — edit the constants in this block and run the script.
# ============================================================================


if __name__ == "__main__":
    clear_terminal()

    # --------------------------------------------------------------------
    # Switch — pick the trial to run.
    # Options:
    #   "keywords_for_site"
    # --------------------------------------------------------------------
    test_name = "keywords_for_site"

    TARGET = "openai.com"
    LOCATION_CODE = 2840  # United States
    LANGUAGE_CODE = "en"
    LIMIT = 20
    TAG = "matrx-seo-trial"

    arg_bank = {
        "keywords_for_site": {
            "target": TARGET,
            "location_code": LOCATION_CODE,
            "language_code": LANGUAGE_CODE,
            "limit": LIMIT,
            "tag": TAG,
        },
    }

    vcprint(arg_bank[test_name], "INPUT ARGS", color="cyan")

    result = asyncio.run(main(test_name, arg_bank[test_name]))
    vcprint(result, f"[{test_name}] OUTPUT RESULT", color="green")

    cleanup_async_resources()
