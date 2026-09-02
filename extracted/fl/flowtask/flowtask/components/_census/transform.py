"""
Census data transformation helpers.

Provides:
- Sentinel value → NaN mapping (the six Census NA sentinels).
- Label normalization (``!!`` → ``__``, lowercase, strip non-ASCII).
- Suffix-based column filtering (``E``, ``PE``, etc.) with end-of-name anchoring.
- Geography column renaming to snake_case.
- Variables catalog DataFrame builder (shared by CensusData and CensusVariables).
"""

from __future__ import annotations

import logging
import re
from typing import Any, TYPE_CHECKING

import pandas as pd

from flowtask.exceptions import ComponentError

if TYPE_CHECKING:
    pass

# ---------------------------------------------------------------------------
# Module-level compiled regex for variable code filtering
# ---------------------------------------------------------------------------

_PSEUDO_VAR_NAMES: frozenset[str] = frozenset({"for", "in", "ucgid"})
_REAL_VAR_PATTERN = re.compile(r"^[A-Z]+\d")

# ---------------------------------------------------------------------------
# Sentinel values
# ---------------------------------------------------------------------------

SENTINEL_VALUES: tuple[int, ...] = (
    -666666666,
    -888888888,
    -999999999,
    -222222222,
    -333333333,
    -555555555,
)

_SENTINEL_SET: set[float] = {float(v) for v in SENTINEL_VALUES}

# ---------------------------------------------------------------------------
# Geography column name mapping (Census API → snake_case)
# ---------------------------------------------------------------------------

_GEO_COLUMN_MAP: dict[str, str] = {
    "zip code tabulation area": "zcta",
    "state": "state",
    "county": "county",
    "tract": "tract",
    "block group": "block_group",
    "place": "place",
    "congressional district": "congressional_district",
    "school district (unified)": "school_district_unified",
}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def apply_sentinels(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    """Replace Census sentinel values with NaN and log per-column counts.

    The caller is responsible for calling ``pd.to_numeric(errors='coerce')``
    on the DataFrame before this function — sentinel values arrive as strings
    from the Census API.

    Args:
        df: A DataFrame whose numeric columns may contain sentinel values.
        logger: A logger instance (used to emit INFO messages per affected column).

    Returns:
        The same DataFrame with sentinel values replaced by NaN (modified in place,
        but the modified DataFrame is also returned for convenience).
    """
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            continue
        mask = df[col].isin(_SENTINEL_SET)
        count = mask.sum()
        if count > 0:
            logger.info(
                "Column '%s': replaced %d sentinel value(s) with NaN.",
                col,
                count,
            )
            df.loc[mask, col] = float("nan")
    return df


def normalize_label(s: str) -> str:
    """Normalize a Census variable label to a valid Python identifier.

    The label is split on ``!!`` separators first.  Each section is lowercased,
    stripped of non-ASCII characters, and any non-``[a-z0-9]`` character is
    replaced by ``_``; runs of ``_`` within a section are collapsed to one.
    Finally the sections are joined with ``__``.  Leading / trailing ``_``
    within each section are stripped.

    Example:
        ``"Estimate!!SEX AND AGE!!Total population!!Male"``
        → ``"estimate__sex_and_age__total_population__male"``

    Args:
        s: The raw Census label string.

    Returns:
        The normalized label as a Python-safe identifier.
    """
    if not s:
        return s

    sections = s.split("!!")
    normalized_sections: list[str] = []
    for section in sections:
        part = section.lower()
        # Strip non-ASCII.
        part = part.encode("ascii", "ignore").decode("ascii")
        # Replace non-identifier characters with underscore.
        part = re.sub(r"[^a-z0-9_]", "_", part)
        # Collapse runs of underscores.
        part = re.sub(r"_+", "_", part)
        # Strip leading/trailing underscores from each section.
        part = part.strip("_")
        if part:
            normalized_sections.append(part)

    return "__".join(normalized_sections)


def filter_by_suffix(
    df: pd.DataFrame,
    suffixes: list[str],
    always_keep: list[str],
) -> pd.DataFrame:
    """Keep only columns whose names end with one of the given suffixes.

    Columns listed in ``always_keep`` (e.g. ``["GEO_ID", "NAME", "zcta"]``)
    are retained unconditionally.

    The suffix match is anchored at the end of the column name with a
    non-letter boundary so that ``"E"`` does not accidentally match ``"EA"``
    or ``"PE"``.

    Args:
        df: The Census data DataFrame.
        suffixes: A list of suffix strings to keep (e.g. ``["E", "PE"]``).
        always_keep: A list of column names to always retain.

    Returns:
        A DataFrame containing only the selected columns.

    Raises:
        ComponentError: If no variable columns remain after filtering.
    """
    if not suffixes:
        raise ComponentError(
            "keep_suffixes must contain at least one suffix (e.g. ['E', 'PE']).",
            status=406,
        )

    # Build a regex that matches the end of column names.
    # We use a word-boundary-like approach: the suffix must be followed by the
    # end of the string and must NOT be preceded by a letter that would extend
    # the suffix (e.g. "E" at the end is fine; "EA" is not "E").
    suffix_pattern = re.compile(
        r"(?<![A-Za-z])(" + "|".join(re.escape(s) for s in suffixes) + r")$"
    )

    always_keep_set = set(always_keep)
    kept = [
        col
        for col in df.columns
        if col in always_keep_set or suffix_pattern.search(col)
    ]

    variable_cols = [c for c in kept if c not in always_keep_set]
    if not variable_cols:
        raise ComponentError(
            f"No variable columns matched the requested suffixes {suffixes!r}. "
            f"Available columns (sample): {list(df.columns[:10])}",
            status=406,
        )

    return df[kept]


def rename_geography_column(df: pd.DataFrame, geography: str) -> pd.DataFrame:
    """Rename the Census API geography column to its snake_case equivalent.

    The Census API uses awkward column names like ``"zip code tabulation area"``.
    This function renames them to the spec's snake_case convention.

    Idempotent: if the column has already been renamed, the DataFrame is
    returned unchanged.

    Args:
        df: The Census data DataFrame.
        geography: The geography type string (e.g. ``"zcta"``, ``"county"``).

    Returns:
        The DataFrame with the geography column renamed.
    """
    # Build reverse map: snake_case → also snake_case (idempotent)
    # plus the raw Census names.
    rename_map: dict[str, str] = {}
    for census_name, snake_name in _GEO_COLUMN_MAP.items():
        rename_map[census_name] = snake_name

    # If the target name is already present, nothing to do.
    target = _GEO_COLUMN_MAP.get(geography, geography)
    if target in df.columns:
        return df

    return df.rename(columns=rename_map)


# ---------------------------------------------------------------------------
# Variables catalog builder (shared by CensusData and CensusVariables)
# ---------------------------------------------------------------------------


def _build_variables_df(variables_json: dict[str, Any]) -> pd.DataFrame:
    """Build the variables catalog DataFrame from ``/variables.json`` payload.

    This function is shared by both ``CensusData`` and ``CensusVariables``
    to avoid duplication.

    Args:
        variables_json: The parsed ``/variables.json`` response dict.

    Returns:
        A DataFrame with columns:
        ``code, label, concept, predicate_type, group, normalized_label``.
        Pseudo-variables (``for``, ``in``, ``ucgid``) are excluded.
    """
    raw_vars: dict[str, Any] = variables_json.get("variables", {})
    records: list[dict[str, str]] = []

    for code, meta in raw_vars.items():
        # Skip pseudo-variables.
        if code.lower() in _PSEUDO_VAR_NAMES:
            continue
        if not _REAL_VAR_PATTERN.match(code):
            continue
        label = meta.get("label", "")
        records.append({
            "code": code,
            "label": label,
            "concept": meta.get("concept", ""),
            "predicate_type": meta.get("predicateType", ""),
            "group": meta.get("group", ""),
            "normalized_label": normalize_label(label),
        })

    if not records:
        return pd.DataFrame(
            columns=["code", "label", "concept", "predicate_type", "group",
                     "normalized_label"]
        )
    return pd.DataFrame(records)
