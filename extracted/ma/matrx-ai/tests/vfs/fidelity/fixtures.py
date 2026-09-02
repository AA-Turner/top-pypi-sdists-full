from __future__ import annotations

from typing import Any

# Standard tree used by most fidelity tests.  Keep the structure small but
# diverse enough to exercise every common ls/cat/grep/find branch.
BASIC_TREE: dict[str, Any] = {
    "/a.txt": "hello\n",
    "/b.py": "def f(): pass\n",
    "/c.md": "# header\n",
    "/.dotfile": "secret\n",
    "/sub/": None,
    "/sub/x.txt": "x\n",
    "/sub/y.txt": "y\n",
    "/sub/inner/": None,
    "/sub/inner/deep.py": "def deep(): pass\n",
    "/empty/": None,
}


# Tree used for grep recursion: includes a few different file types and
# multi-line content so we can verify both line-number formatting and the
# `path:line:content` shape.
GREP_TREE: dict[str, Any] = {
    "/a.txt": "alpha\nbeta\nGAMMA\n",
    "/b.txt": "no match here\n",
    "/sub/": None,
    "/sub/c.py": "def alpha():\n    pass\nalpha = 1\n",
    "/sub/d.txt": "alpha at end\n",
    "/empty/": None,
}


# Tree used for error tests: just enough structure to trigger every "wrong
# kind of thing" message we want to verify.
ERROR_TREE: dict[str, Any] = {
    "/a.txt": "hello\n",
    "/sub/": None,
    "/sub/inner.txt": "inner\n",
    "/non-empty/": None,
    "/non-empty/x.txt": "x\n",
    "/empty/": None,
    "/existing/": None,
}
