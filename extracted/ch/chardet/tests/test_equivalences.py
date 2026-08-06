# tests/test_equivalences.py
"""Backward-compatibility shim tests for ``chardet.equivalences``.

The module's contents were split into :mod:`chardet.evaluation` and
:mod:`chardet.output_names` in 7.5.  This file verifies the deprecation
warning fires and the re-exports still resolve to the new modules.
"""

from __future__ import annotations

import importlib
import sys
import warnings


def _reload_equivalences():
    """Force a fresh import of ``chardet.equivalences`` so its module-level warning re-fires."""
    sys.modules.pop("chardet.equivalences", None)
    return importlib.import_module("chardet.equivalences")


def test_import_emits_deprecation_warning():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", DeprecationWarning)
        _reload_equivalences()
    deprecations = [w for w in caught if issubclass(w.category, DeprecationWarning)]
    assert any(
        "chardet.equivalences is deprecated" in str(w.message) for w in deprecations
    ), f"expected deprecation warning, got: {[str(w.message) for w in caught]}"


def test_reexports_resolve_to_new_modules():
    """Names re-exported from the shim are the same objects as the new modules."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        equivalences = _reload_equivalences()
    from chardet import evaluation, output_names  # noqa: PLC0415

    # Evaluation seam
    assert equivalences.is_correct is evaluation.is_correct
    assert equivalences.is_equivalent_detection is evaluation.is_equivalent_detection
    assert equivalences.is_language_equivalent is evaluation.is_language_equivalent
    assert equivalences.SUPERSETS is evaluation.SUPERSETS
    assert equivalences.BIDIRECTIONAL_GROUPS is evaluation.BIDIRECTIONAL_GROUPS
    assert equivalences.LANGUAGE_EQUIVALENCES is evaluation.LANGUAGE_EQUIVALENCES

    # Output-name seam
    assert equivalences.apply_compat_names is output_names.apply_compat_names
    assert (
        equivalences.apply_preferred_superset is output_names.apply_preferred_superset
    )
    assert equivalences.apply_legacy_rename is output_names.apply_legacy_rename
    assert equivalences.PREFERRED_SUPERSET is output_names.PREFERRED_SUPERSET
