"""Target / task type detection for a single target column.

``suggest_model_type(target_column)`` returns one of
``"binary" | "multiclass" | "multilabel" | "regression"`` based on the
column's values + dtype + structure. Designed to run BEFORE training
(no Featrix model required) so callers — UIs, notebook helpers, the QA
harness, the SP prep step — can pick the right predictor type without
guessing.

Detection strategy:

1. If ``featrix.detectors.detect.detect_column_type_detailed`` is
   importable, use it as the primary signal (this is the same detector
   the server uses for column-encoder selection, so the result is
   internally consistent with what training would do).
2. Map the detector's codec name + cardinality to a task type via the
   table in ``_codec_to_task()``.
3. If the detector isn't on the import path (customer machine with only
   ``featrixsphere`` installed from PyPI), fall back to ``_pure_pandas_detect()``
   which handles the same edge cases at slightly lower fidelity.

Edge cases the function handles explicitly:

- **Multilabel-as-Python-list**: cells are ``list`` / ``tuple`` / ``set`` /
  ``np.ndarray`` → multilabel.
- **Multilabel-as-JSON-string**: cells are strings like
  ``'["Bob","Bill"]'`` (common when a CSV preserves a JSON list
  per cell, including the doubled-quote ``""...""`` escape) → multilabel,
  using ``json.loads`` then ``ast.literal_eval`` as fallback for
  Python-repr syntax (``"['Bob', 'Bill']"``).
- **Multilabel-as-delimited-string**: ``"a,b,c"`` or ``"a;b;c"`` etc. →
  multilabel, with the detected separator returned in the result so
  callers can pass it to ``MultiLabelCodec``.
- **Binary-as-int**: int column with exactly 2 unique values (e.g.
  ``{0, 1}``) → binary.
- **Multiclass-as-low-card-int**: int column with 3..20 unique values
  → multiclass (could be ordinal — flagged in ``reasoning``).
- **Regression-as-int**: int column with >50 unique values (age, count)
  → regression. ``is_integer`` flag returned so callers can pick the
  right loss / output head.
- **Degenerate**: all-null or single-unique → ``task_type=None`` so the
  caller can warn / drop.
"""
from __future__ import annotations

import ast
import json
import logging
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Public API
__all__ = ["suggest_model_type"]


# ---------------------------------------------------------------------------
# Public entry
# ---------------------------------------------------------------------------

def suggest_model_type(
    target_column: pd.Series,
    *,
    col_name: str = "target",
) -> Dict[str, Any]:
    """Detect the likely task type for a target column.

    Args:
        target_column: pandas Series (one column from the user's DataFrame).
        col_name: Optional column name for logging / reasoning text.

    Returns:
        Dict with the following keys (always present, may be None):

        ``task_type`` — one of ``"binary"``, ``"multiclass"``,
          ``"multilabel"``, ``"regression"``, or ``None`` (degenerate).
        ``confidence`` — 0.0 to 1.0. Treat ≥0.8 as decided, 0.5–0.8 as
          plausible, <0.5 as ambiguous.
        ``reasoning`` — one-line human-readable description of the decision.
        ``n_unique`` — distinct non-null values; for multilabel, distinct
          labels across all rows.
        ``n_null`` — null-count.
        ``is_integer`` — for regression: True if all values are integers
          (so caller can route to an integer-aware regression head /
          format predictions without trailing decimals).
        ``detected_separator`` — for multilabel: the delimiter found
          (``","`` / ``";"`` / ``"|"`` / ``"\t"`` / ``"json"`` / ``"python_repr"``
          / ``None`` for in-memory list cells). Pass this to the codec.
        ``avg_labels_per_row`` — for multilabel: mean labels per row.
        ``codec`` — for diagnostics: the underlying Featrix codec name
          that ``detect_column_type_detailed`` returned, when available.
    """
    s = target_column

    # Degenerate cases first — cheap, unambiguous
    n_null = int(s.isna().sum())
    s_nn = s.dropna()
    if len(s_nn) == 0:
        return _result(task_type=None, confidence=0.0,
                       reasoning="Column is entirely null",
                       n_unique=0, n_null=n_null)

    # 1) Multilabel-as-structure FIRST, before any nunique() / hashing —
    #    pandas raises TypeError on list / set / ndarray cells.
    structural = _detect_multilabel_structural(s_nn)
    if structural is not None:
        return structural

    # Now safe to call nunique() — the remaining branches need it.
    n_unique = int(s_nn.nunique())
    if n_unique == 1:
        return _result(task_type=None, confidence=0.0,
                       reasoning=f"Only one unique value ({s_nn.iloc[0]!r}) — degenerate",
                       n_unique=1, n_null=n_null)

    # 2) Multilabel-as-string: JSON-list, Python-repr, or delimited.
    if s_nn.dtype == object or pd.api.types.is_string_dtype(s_nn):
        string_ml = _detect_multilabel_string(s_nn, n_null=n_null)
        if string_ml is not None:
            return string_ml

    # 3) Defer to the server-side detector when available. It already handles
    #    bool / int / float / categorical / multi_label / scalar with the same
    #    rules training uses, so the suggestion stays consistent with what the
    #    SP prep step would do downstream.
    try:
        from featrix.detectors.detect import detect_column_type_detailed
        codec, conf, _all_conf = detect_column_type_detailed(s, col_name)
        result = _codec_to_task(codec, s_nn, n_null=n_null, detector_conf=conf)
        result["codec"] = codec
        return result
    except ImportError:
        # Customer machine without featrix.detectors — fall back to the local
        # pure-pandas detector. Logged at DEBUG so it doesn't spam.
        logger.debug(
            "featrix.detectors.detect not importable; using pure-pandas fallback"
        )

    return _pure_pandas_detect(s_nn, n_null=n_null)


# ---------------------------------------------------------------------------
# Multilabel detection
# ---------------------------------------------------------------------------

# Limit how many cells we eyeball when sniffing string-list / delimiter format.
# Large enough to make the "≥50% match" signal reliable on real datasets;
# small enough that a 10M-row column doesn't slow us down.
_SAMPLE_SIZE = 200


def _detect_multilabel_structural(s_nn: pd.Series) -> Optional[Dict[str, Any]]:
    """Multilabel where cells are Python collections (list/tuple/set/ndarray).

    Returns a result dict, or None if not a structural multilabel.
    """
    sample = s_nn.head(_SAMPLE_SIZE)
    n_collection = 0
    for v in sample:
        if isinstance(v, (list, tuple, set, frozenset, np.ndarray)):
            n_collection += 1
    if n_collection < 0.5 * len(sample):
        return None

    # Materialize per-row label counts + global label vocabulary
    label_counts: List[int] = []
    all_labels: set = set()
    for v in s_nn:
        if isinstance(v, (list, tuple, set, frozenset)):
            label_counts.append(len(v))
            all_labels.update(_as_hashable(item) for item in v)
        elif isinstance(v, np.ndarray):
            label_counts.append(int(v.size))
            all_labels.update(_as_hashable(item) for item in v.tolist())
        else:
            label_counts.append(1)
            all_labels.add(_as_hashable(v))

    avg = float(np.mean(label_counts)) if label_counts else 0.0
    return _result(
        task_type="multilabel",
        confidence=1.0,
        reasoning=(
            f"Cells contain collections ({type(sample.iloc[0]).__name__}); "
            f"avg {avg:.2f} labels/row across {len(all_labels)} distinct labels"
        ),
        n_unique=len(all_labels),
        n_null=int(s_nn.isna().sum()),
        detected_separator=None,
        avg_labels_per_row=avg,
    )


def _detect_multilabel_string(s_nn: pd.Series, *, n_null: int) -> Optional[Dict[str, Any]]:
    """Multilabel where cells are strings encoding a list.

    Handles three forms in order: JSON-list ``'["a","b"]'``, Python-repr
    ``"['a', 'b']"``, and delimited ``'a,b,c'`` / ``'a;b;c'`` / ``'a|b'``
    / ``'a\\tb'``. Returns None if none of those patterns dominate.
    """
    sample = s_nn.head(_SAMPLE_SIZE).astype(str)

    # 2a) JSON list — starts with '[' and parses as a list of scalars.
    json_hits = 0
    json_parses: List[List[Any]] = []
    for v in sample:
        parsed = _try_json_list(v)
        if parsed is not None:
            json_hits += 1
            json_parses.append(parsed)
    if json_hits >= 0.5 * len(sample) and json_parses:
        return _multilabel_from_parses(s_nn, parser=_try_json_list,
                                       separator="json", n_null=n_null)

    # 2b) Python repr — ``"['a', 'b']"`` syntax. Same shape, different escape.
    repr_hits = 0
    for v in sample:
        if _try_python_repr_list(v) is not None:
            repr_hits += 1
    if repr_hits >= 0.5 * len(sample):
        return _multilabel_from_parses(s_nn, parser=_try_python_repr_list,
                                       separator="python_repr", n_null=n_null)

    # 2c) Single-char delimiters. Pick the one with the highest hit rate
    # and an avg-labels-per-row > 1.5 (otherwise it's just a single-label
    # column that happens to contain commas — e.g., free-form notes).
    best_sep = None
    best_avg = 0.0
    best_hit_rate = 0.0
    for sep in (",", ";", "|", "\t"):
        contains = sample.str.contains(sep, regex=False, na=False)
        hit_rate = float(contains.mean())
        if hit_rate < 0.5:
            continue
        # Split and count labels per row
        split_lens = sample.str.split(sep).map(
            lambda parts: sum(1 for p in parts if str(p).strip())
        )
        avg = float(split_lens.mean())
        if avg > 1.5 and hit_rate > best_hit_rate:
            best_sep, best_avg, best_hit_rate = sep, avg, hit_rate
    if best_sep is None:
        return None

    # Build the vocab + per-row counts across the FULL column, not just the sample.
    all_labels: set = set()
    label_counts: List[int] = []
    for v in s_nn.astype(str):
        parts = [p.strip() for p in v.split(best_sep) if p.strip()]
        label_counts.append(len(parts))
        all_labels.update(parts)
    avg = float(np.mean(label_counts)) if label_counts else 0.0
    return _result(
        task_type="multilabel",
        confidence=min(1.0, 0.6 + 0.2 * (avg - 1.5)),
        reasoning=(
            f"Delimited string column (sep={best_sep!r}); avg {avg:.2f} labels/row "
            f"across {len(all_labels)} distinct labels"
        ),
        n_unique=len(all_labels),
        n_null=n_null,
        detected_separator=best_sep,
        avg_labels_per_row=avg,
    )


def _try_json_list(v: str) -> Optional[List[Any]]:
    """Return the parsed list if v is a JSON-list string, else None."""
    s = v.strip()
    if not (s.startswith("[") and s.endswith("]")):
        return None
    try:
        parsed = json.loads(s)
    except (json.JSONDecodeError, ValueError):
        return None
    return parsed if isinstance(parsed, list) else None


def _try_python_repr_list(v: str) -> Optional[List[Any]]:
    """Return the parsed list if v is a Python-repr-list string, else None.

    ``ast.literal_eval`` is safe — it only evaluates literals, not arbitrary
    code. Handles ``"['a', 'b']"`` (single-quoted) and tuples
    (``"('a', 'b')"``).
    """
    s = v.strip()
    if not ((s.startswith("[") and s.endswith("]")) or
            (s.startswith("(") and s.endswith(")"))):
        return None
    try:
        parsed = ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return None
    return list(parsed) if isinstance(parsed, (list, tuple)) else None


def _multilabel_from_parses(
    s_nn: pd.Series,
    parser,
    separator: str,
    n_null: int,
) -> Dict[str, Any]:
    """Walk the full column with `parser` and build the multilabel result."""
    all_labels: set = set()
    label_counts: List[int] = []
    for v in s_nn.astype(str):
        parsed = parser(v)
        if parsed is None:
            label_counts.append(1)
            all_labels.add(v)
        else:
            label_counts.append(len(parsed))
            all_labels.update(_as_hashable(item) for item in parsed)
    avg = float(np.mean(label_counts)) if label_counts else 0.0
    return _result(
        task_type="multilabel",
        confidence=min(1.0, 0.7 + 0.15 * max(0.0, avg - 1.0)),
        reasoning=(
            f"List-encoded string column ({separator}); avg {avg:.2f} labels/row "
            f"across {len(all_labels)} distinct labels"
        ),
        n_unique=len(all_labels),
        n_null=n_null,
        detected_separator=separator,
        avg_labels_per_row=avg,
    )


# ---------------------------------------------------------------------------
# Codec → task mapping (when featrix.detectors is available)
# ---------------------------------------------------------------------------

def _codec_to_task(
    codec: str,
    s_nn: pd.Series,
    *,
    n_null: int,
    detector_conf: float,
) -> Dict[str, Any]:
    """Map a Featrix codec name + the column to a task type.

    The detector returns codec names like ``"scalar"`` / ``"set"`` /
    ``"multi_label"`` etc. Those describe how the COLUMN gets encoded as
    a feature. For TARGET-column purposes we need a further mapping to
    binary / multiclass / multilabel / regression — that's this function.
    """
    n_unique = int(s_nn.nunique())

    # Multi-label is unambiguous from the codec.
    if codec == "multi_label":
        return _result(
            task_type="multilabel",
            confidence=detector_conf,
            reasoning=f"Codec=multi_label (detector confidence {detector_conf:.2f})",
            n_unique=n_unique,
            n_null=n_null,
            detected_separator=None,
            avg_labels_per_row=None,
        )

    # Scalar → regression OR low-card multiclass / binary.
    if codec == "scalar":
        return _scalar_to_task(s_nn, n_null=n_null, detector_conf=detector_conf)

    # Hybrid scalar+set: low-card numeric. Detector kept both options open;
    # for a TARGET we treat low-card int as multiclass (ordinal).
    if codec in ("hybrid_scalar_set", "set", "hybrid_string_set"):
        if n_unique == 2:
            return _result(
                task_type="binary", confidence=1.0,
                reasoning=f"Codec={codec}, exactly 2 unique values",
                n_unique=2, n_null=n_null,
            )
        return _result(
            task_type="multiclass",
            confidence=min(1.0, detector_conf),
            reasoning=f"Codec={codec}, {n_unique} unique values",
            n_unique=n_unique, n_null=n_null,
        )

    # Free string / json / url / email / phone / etc. on a TARGET column is
    # unusual. Fall back to cardinality-based multiclass classification with
    # low confidence so callers can surface a warning.
    return _result(
        task_type="multiclass" if n_unique <= 50 else "regression",
        confidence=0.4,
        reasoning=(
            f"Codec={codec} is unusual for a target column; defaulting to "
            f"{'multiclass' if n_unique <= 50 else 'regression'} "
            f"({n_unique} unique values)"
        ),
        n_unique=n_unique, n_null=n_null,
    )


def _scalar_to_task(
    s_nn: pd.Series,
    *,
    n_null: int,
    detector_conf: float,
) -> Dict[str, Any]:
    """Decide binary / multiclass / regression for a numeric scalar column."""
    n_unique = int(s_nn.nunique())
    is_int = _is_integer_series(s_nn)
    is_bool = pd.api.types.is_bool_dtype(s_nn)

    if is_bool or n_unique == 2:
        return _result(
            task_type="binary", confidence=1.0,
            reasoning=(
                "Boolean dtype" if is_bool else
                f"Numeric column with exactly 2 unique values "
                f"({sorted(s_nn.unique().tolist())[:2]})"
            ),
            n_unique=2, n_null=n_null,
        )

    # Heuristic cutoff: low-card int → multiclass (ordinal). High-card int
    # or any float with >20 unique → regression.
    if is_int and n_unique <= 20:
        return _result(
            task_type="multiclass",
            confidence=0.85,
            reasoning=(
                f"Integer scalar with {n_unique} unique values (low cardinality); "
                "treating as multiclass — could be ordinal regression depending on intent"
            ),
            n_unique=n_unique, n_null=n_null,
            is_integer=True,
        )

    if n_unique > 20:
        return _result(
            task_type="regression",
            confidence=1.0,
            reasoning=(
                f"{'Integer' if is_int else 'Float'} scalar with {n_unique} unique values"
            ),
            n_unique=n_unique, n_null=n_null,
            is_integer=is_int,
        )

    # 3-20 unique floats: weird; could be regression-with-coarse-grid.
    return _result(
        task_type="regression",
        confidence=0.6,
        reasoning=(
            f"Float scalar with only {n_unique} unique values — likely coarse "
            f"regression; treat as multiclass if the values are categorical labels"
        ),
        n_unique=n_unique, n_null=n_null,
        is_integer=False,
    )


# ---------------------------------------------------------------------------
# Pure-pandas fallback (used when featrix.detectors isn't importable)
# ---------------------------------------------------------------------------

def _pure_pandas_detect(s_nn: pd.Series, *, n_null: int) -> Dict[str, Any]:
    """Detect task type using only pandas + numpy.

    Used on customer machines that have featrixsphere but not the server-side
    featrix.detectors module. Multilabel by structure / string is handled
    above; this routes binary / multiclass / regression.
    """
    n_unique = int(s_nn.nunique())
    is_int = _is_integer_series(s_nn)
    is_float = pd.api.types.is_float_dtype(s_nn)
    is_bool = pd.api.types.is_bool_dtype(s_nn)
    is_numeric = pd.api.types.is_numeric_dtype(s_nn)

    if is_bool or n_unique == 2:
        return _result(
            task_type="binary", confidence=1.0,
            reasoning=(
                "Boolean dtype" if is_bool
                else f"Exactly 2 unique values: {sorted(s_nn.unique().tolist())[:2]}"
            ),
            n_unique=2, n_null=n_null,
        )

    if is_numeric:
        if is_int and n_unique <= 20:
            return _result(
                task_type="multiclass", confidence=0.85,
                reasoning=f"Integer column with {n_unique} unique values (low cardinality)",
                n_unique=n_unique, n_null=n_null, is_integer=True,
            )
        if n_unique > 20:
            return _result(
                task_type="regression", confidence=1.0,
                reasoning=f"{'Integer' if is_int else 'Float'} column with {n_unique} unique values",
                n_unique=n_unique, n_null=n_null, is_integer=is_int,
            )
        return _result(
            task_type="regression", confidence=0.6,
            reasoning=f"Float column with only {n_unique} unique values (coarse regression?)",
            n_unique=n_unique, n_null=n_null, is_integer=False,
        )

    # Non-numeric, non-multilabel → multiclass by unique count.
    return _result(
        task_type="multiclass",
        confidence=1.0 if n_unique <= 50 else 0.6,
        reasoning=f"Non-numeric column with {n_unique} unique values",
        n_unique=n_unique, n_null=n_null,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_integer_series(s: pd.Series) -> bool:
    """True if every non-null value is an integer (dtype int, or float with
    all-integer values like 1.0, 2.0). Pandas often loads CSV integer
    columns as float64 when there are nulls; we want to call those integer.
    """
    if pd.api.types.is_integer_dtype(s):
        return True
    if pd.api.types.is_float_dtype(s):
        # Floats that happen to be all-integer values (1.0, 2.0, 3.0, …)
        try:
            arr = s.to_numpy()
            arr = arr[~np.isnan(arr)]
            return bool(np.all(arr == arr.astype(np.int64)))
        except (TypeError, ValueError):
            return False
    return False


def _as_hashable(v):
    """Coerce numpy scalars / pandas NA to a hashable Python value for set ops."""
    if isinstance(v, (np.generic,)):
        return v.item()
    return v


def _result(
    *,
    task_type: Optional[str],
    confidence: float,
    reasoning: str,
    n_unique: int,
    n_null: int,
    is_integer: Optional[bool] = None,
    detected_separator: Optional[str] = None,
    avg_labels_per_row: Optional[float] = None,
    codec: Optional[str] = None,
) -> Dict[str, Any]:
    """Build a uniform result dict so every code path returns the same keys."""
    return {
        "task_type": task_type,
        "confidence": float(confidence),
        "reasoning": reasoning,
        "n_unique": int(n_unique),
        "n_null": int(n_null),
        "is_integer": is_integer,
        "detected_separator": detected_separator,
        "avg_labels_per_row": avg_labels_per_row,
        "codec": codec,
    }
