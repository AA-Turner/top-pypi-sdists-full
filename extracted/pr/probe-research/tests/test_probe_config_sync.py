"""The hooks' vendored `_probe_config.py` must match the canonical matcher.

`src/probe/sdk/probe_config.py` is stdlib-only so the plugin hooks, which run
under the SYSTEM python3 with no `probe` package, can carry a byte copy
(`make sync-probe-config`; the lean daemon plugin copies the full plugin's via
`make sync-daemon-plugin`). Two copies that disagree would let the guard and
the CLI answer differently about the same path.
"""

from __future__ import annotations

import filecmp
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_CANONICAL = _ROOT / "src" / "probe" / "sdk" / "probe_config.py"
_COPIES = (
    _ROOT / "plugins" / "probe-research" / "hooks" / "_probe_config.py",
    _ROOT / "plugins" / "probe-research-daemon" / "hooks" / "_probe_config.py",
)


def test_copies_match_canonical() -> None:
    for copy in _COPIES:
        assert copy.is_file(), f"{copy} is missing; run `make sync-plugin`"
        assert filecmp.cmp(_CANONICAL, copy, shallow=False), (
            f"{copy} has drifted from src/probe/sdk/probe_config.py: run `make sync-plugin` "
            "(and add a plugin CHANGELOG line: it ships with the next plugin release)"
        )
