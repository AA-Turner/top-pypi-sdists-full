"""Rbeast shims: the optional import and the Python 3.13 noise filter.

Rbeast 0.1.25 on Python 3.13 reports ``Exception ignored in
PyObject_HasAttrString(): SystemError: ... bad argument to internal
function`` on every ``beast()`` call (results unaffected). ``quiet_rbeast``
must drop exactly that and nothing else, and every call site must survive
an uninstalled Rbeast.
"""
import logging
import sys
import types
from pathlib import Path

import numpy as np
import pytest

from geocif.ml import beast_compat
from geocif.ml.trend import segment_aware_trend

RBEAST_ERR_MSG = (
    "Exception ignored in PyObject_HasAttrString(); consider using "
    "PyObject_HasAttrStringWithError(), PyObject_GetOptionalAttrString() "
    "or PyObject_GetAttrString():"
)


def _unraisable(exc, err_msg):
    return types.SimpleNamespace(
        exc_type=type(exc), exc_value=exc, exc_traceback=None,
        err_msg=err_msg, object=None,
    )


def test_quiet_rbeast_drops_only_the_rbeast_report(monkeypatch):
    seen = []
    record = seen.append  # bind once: a fresh bound method never passes `is`
    monkeypatch.setattr(sys, "unraisablehook", record)
    with beast_compat.quiet_rbeast():
        sys.unraisablehook(_unraisable(
            SystemError("dictobject.c:4114: bad argument to internal function"),
            RBEAST_ERR_MSG,
        ))
        sys.unraisablehook(_unraisable(ValueError("unrelated"),
                                       "Exception ignored in: <function Bad.__del__>"))
        sys.unraisablehook(_unraisable(SystemError("some other SystemError"), None))
    assert [type(u.exc_value) for u in seen] == [ValueError, SystemError]
    assert sys.unraisablehook is record, "previous hook not restored"


def test_quiet_rbeast_restores_hook_when_the_call_raises(monkeypatch):
    def sentinel(unraisable):
        return None

    monkeypatch.setattr(sys, "unraisablehook", sentinel)
    with pytest.raises(RuntimeError):
        with beast_compat.quiet_rbeast():
            raise RuntimeError("beast blew up")
    assert sys.unraisablehook is sentinel


def test_import_rbeast_returns_none_and_warns_once(monkeypatch, caplog):
    monkeypatch.setitem(sys.modules, "Rbeast", None)  # makes `import Rbeast` raise
    monkeypatch.setattr(beast_compat, "_IMPORT_WARNED", False)
    with caplog.at_level(logging.WARNING, logger=beast_compat.logger.name):
        assert beast_compat.import_rbeast() is None
        assert beast_compat.import_rbeast() is None
    warnings = [r for r in caplog.records if "Rbeast is not importable" in r.getMessage()]
    assert len(warnings) == 1


def test_segment_aware_trend_without_rbeast_is_plain_ols(monkeypatch, caplog):
    monkeypatch.setitem(sys.modules, "Rbeast", None)
    monkeypatch.setattr(beast_compat, "_IMPORT_WARNED", False)
    years = np.arange(2000, 2012, dtype=float)
    yields = 1.0 + 0.1 * (years - 2000.0)
    with caplog.at_level(logging.WARNING):
        intercept, slope, cp_used, n_used = segment_aware_trend(years, yields)
    assert cp_used is None
    assert n_used == 12
    assert slope == pytest.approx(0.1)
    assert intercept + slope * 2000.0 == pytest.approx(1.0)
    assert "Rbeast is not importable" in caplog.text


def test_segment_aware_trend_too_short_needs_no_rbeast(monkeypatch):
    monkeypatch.setitem(sys.modules, "Rbeast", None)
    intercept, slope, cp_used, n_used = segment_aware_trend([2001.0], [2.5])
    assert (intercept, slope, cp_used, n_used) == (2.5, 0.0, None, 1)


# --- source-level contracts for the call sites -----------------------------

ROOT = Path(__file__).resolve().parents[1] / "geocif"


def _function_source(path, name):
    body = path.read_text(encoding="utf-8", errors="ignore")
    start = body.index(f"def {name}(")
    rest = body[start + 1:]
    end = rest.find("\ndef ")
    return body[start:] if end < 0 else body[start:start + 1 + end]


def test_every_beast_call_is_guarded():
    for rel in ("ml/trend.py", "ml/yield_anomaly_beast.py",
                "production_analysis/_common.py"):
        src = (ROOT / rel).read_text(encoding="utf-8")
        assert src.count("rb.beast(") >= 1, rel
        assert src.count("with quiet_rbeast():") == src.count("rb.beast("), \
            f"{rel}: an rb.beast() call is not wrapped in quiet_rbeast()"


def test_breakpoint_diagnostics_are_switchable_and_log_skips():
    src = _function_source(ROOT / "yield_outlook.py", "_generate_breakpoint_plots")
    assert 'parser.getboolean("BEAST", "breakpoint_plots", fallback=True)' in src
    assert "except Exception:\n                continue" not in src, \
        "regions must not be dropped silently"
    assert "region(s) skipped" in src
