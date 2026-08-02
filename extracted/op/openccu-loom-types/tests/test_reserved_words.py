# SPDX-License-Identifier: MIT
# Copyright (C) 2026 OpenCCU-Loom authors.

"""Regression test for the generator's Python-keyword escape.

Before 0.1.1 the generator emitted bare `None = "none"` lines, which is
a SyntaxError because `None` is a reserved word in Python. The fix
appends a trailing underscore to any member name that collides with
the grammar (PEP 8 convention).
"""

from __future__ import annotations

import importlib

import openccu_loom_types
from openccu_loom_types import enums


def test_module_imports_cleanly() -> None:
    """The whole enums module must be importable — no SyntaxError."""
    importlib.reload(enums)


def test_reserved_word_members_get_trailing_underscore() -> None:
    """Every known reserved-word collision must be exposed as
    `MemberName_` (trailing underscore) and keep the original wire
    value.
    """
    assert enums.FailureReason.None_.value == "none"
    assert enums.Quantity.None_.value == ""
    assert enums.RPCServerType.None_.value == "none"
    assert enums.ValueBehavior.None_.value == ""


def test_no_python_keyword_appears_as_bare_member() -> None:
    """Defense against future regressions: walk every enum and assert
    no member name is a Python keyword.
    """
    import keyword

    for cls_name in dir(enums):
        cls = getattr(enums, cls_name)
        if not hasattr(cls, "__members__"):
            continue
        for member_name in cls.__members__:
            assert not keyword.iskeyword(member_name), (
                f"{cls_name}.{member_name} collides with a Python keyword — "
                "generator escape regressed"
            )


def test_package_metadata_present() -> None:
    """Sanity check that the version is exposed."""
    assert openccu_loom_types.__version__
