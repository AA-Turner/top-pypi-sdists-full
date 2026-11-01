"""OverviewCsp: what an overview page may load, read from `allowlist.json` beside this file.

The one allowlist: the server's overview HTML linter and the dashboard's frame CSP
(`dashboard/src/shared/generated/overview-csp.generated.ts`) both derive from it.
"""

from __future__ import annotations

import json
from pathlib import Path

ALLOWLIST_PATH = Path(__file__).with_name("allowlist.json")


def load_allowlist() -> dict[str, list[str]]:
    """The raw allowlist: `script_src`, `style_src`, `font_src` host lists."""
    return json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
