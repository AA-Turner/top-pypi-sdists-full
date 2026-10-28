"""`probe/_shared/handoff.py` is frozen: it changes only on purpose, with its version.

It is the one piece of updater code a newer release cannot replace on a
machine that is already stuck: stage 1 of every update runs the INSTALLED
release's copy, and the lifeboat runs a copy kept outside every release
(`~/.local/state/probe/lifeboat/{current,known-good}/handoff.py`), which a
release may replace only with a higher HANDOFF_VERSION. A change that slipped
in unnoticed would reach every machine and could not be taken back by
shipping a fix. So its bytes are pinned here, like the pi shim's
(`test_pi_pins.FROZEN_SHIM`).

TO CHANGE IT, DELIBERATELY: raise `HANDOFF_VERSION` in handoff.py, then set
`FROZEN_HANDOFF` below to `(<the new version>, "<sha256 of the new file>")`
(`sha256sum agent/src/probe/_shared/handoff.py`). Say in the PR why, and what
an older lifeboat copy does with the new files it may meet.
"""

from __future__ import annotations

import ast
import hashlib
import sys
from pathlib import Path

from probe._shared import handoff

#: (HANDOFF_VERSION, sha256 of handoff.py): see the module docstring.
FROZEN_HANDOFF = (3, "e35fb7f3a32dea1043eecc66ea377037d32d7f578abfe4abc312960d626fe456")

SOURCE = Path(handoff.__file__)


def test_the_hand_off_changes_only_with_its_version():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert (handoff.HANDOFF_VERSION, digest) == FROZEN_HANDOFF, (
        f"{SOURCE} changed (sha256 {digest}, HANDOFF_VERSION {handoff.HANDOFF_VERSION}). It is frozen: "
        "every machine's lifeboat and stage 1 run it, and a stuck machine cannot be given another copy. "
        "If the change is deliberate, raise HANDOFF_VERSION in handoff.py and set FROZEN_HANDOFF in "
        f"{Path(__file__).name} to (<new version>, <new sha256>)."
    )


def test_it_imports_only_the_standard_library_and_nothing_of_probe():
    """The lifeboat runs it with `python -I -S`, outside every release."""
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            assert node.level == 0, "no relative imports: it runs as a script"
            imported.add((node.module or "").split(".")[0])
    imported.discard("__future__")
    optional = {"certifi"}  # tried for a CA bundle where it is importable, never needed
    assert imported - optional <= set(sys.stdlib_module_names), imported - set(sys.stdlib_module_names)
    assert "probe" not in imported
