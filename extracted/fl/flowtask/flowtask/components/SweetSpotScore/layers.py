"""Layer-building helpers for the SweetSpotScore component (FEAT-190/FEAT-191).

Translates raw pandas DataFrames + inline YAML config into the scoring
interface's contract types (``CandidateGrid``, ``POILayer``,
``ScoringPolicy``). No LLM, no agent, no dataset-manager dependency.
"""
import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from flowtask.interfaces.scoring import CandidateGrid, POILayer, ScoringPolicy


def build_candidate_grid(
    dataframes: list[pd.DataFrame], config: dict[str, Any]
) -> CandidateGrid:
    """Build a ``CandidateGrid`` from one of the component's input DataFrames.

    Args:
        dataframes: The component's input DataFrames (``self._df``), indexed
            in the order they arrive from ``depends``.
        config: The ``candidates`` block of the YAML component config, e.g.
            ``{"source": 0, "lat_col": "latitude", "lon_col": "longitude",
            "id_col": "store_id"}``.

    Returns:
        A populated ``CandidateGrid``.
    """
    source_idx = config.get("source", 0)
    df = dataframes[source_idx]
    return CandidateGrid.from_dataframe(
        df,
        lat_col=config.get("lat_col", "latitude"),
        lon_col=config.get("lon_col", "longitude"),
        id_col=config.get("id_col"),
    )


def build_poi_layers(
    dataframes: list[pd.DataFrame], config: list[dict[str, Any]]
) -> dict[str, POILayer]:
    """Build the ``{dataset_name: POILayer}`` mapping from input DataFrames.

    Args:
        dataframes: The component's input DataFrames (``self._df``), indexed
            in the order they arrive from ``depends``.
        config: The ``layers`` block of the YAML component config — a list
            of per-layer dicts, e.g. ``[{"name": "hotels", "source": 1,
            "lat_col": "lat", "lon_col": "lng", "attribute_cols": ["rooms"]}]``.

    Returns:
        A mapping of layer name to ``POILayer``, keyed by the ``dataset``
        field referenced by ``Criterion``/``HardFilter`` entries in the policy.
    """
    layers: dict[str, POILayer] = {}
    for layer_config in config:
        name = layer_config["name"]
        df = dataframes[layer_config.get("source", 0)]
        layers[name] = POILayer.from_dataframe(
            df,
            name=name,
            lat_col=layer_config.get("lat_col", "latitude"),
            lon_col=layer_config.get("lon_col", "longitude"),
            attribute_cols=layer_config.get("attribute_cols"),
        )
    return layers


def load_policy(config: dict[str, Any]) -> ScoringPolicy:
    """Build a ``ScoringPolicy`` from the inline YAML ``policy`` config block.

    Pydantic validates and constructs the nested ``Criterion``/``HardFilter``/
    ``ValueFunction``/``ExtractorParams`` models directly from the raw dicts.

    Args:
        config: The ``policy`` block of the YAML component config.

    Returns:
        A frozen ``ScoringPolicy``.
    """
    return ScoringPolicy(**config)


def load_policy_file(path: str, base_dir: Path) -> dict:
    """Load a scoring policy from an external YAML/JSON file (FEAT-191).

    ``path`` is resolved relative to ``base_dir`` unless it is already an
    absolute path (same convention as ``PowerPointSlide``'s file-loading
    helper). The returned dict is the raw, un-normalized policy config —
    normalization (shorthand expansion) happens separately in
    :func:`normalize_policy`.

    Args:
        path: Path to the policy file, absolute or relative to ``base_dir``.
        base_dir: Base directory used to resolve relative paths (typically
            ``navconfig.BASE_DIR``).

    Returns:
        The raw policy config as a dict.

    Raises:
        FileNotFoundError: if the resolved file does not exist.
        ValueError: if the file extension is not ``.yaml``/``.yml``/``.json``.
    """
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = Path(base_dir) / file_path

    if not file_path.exists():
        raise FileNotFoundError(
            f"SweetSpotScore policy_file not found: {file_path}"
        )

    suffix = file_path.suffix.lower()
    if suffix not in (".yaml", ".yml", ".json"):
        raise ValueError(
            f"Unsupported policy_file extension {suffix!r} for {file_path} — "
            "expected .yaml, .yml, or .json"
        )

    with file_path.open("r", encoding="utf-8") as f:
        if suffix in (".yaml", ".yml"):
            return yaml.safe_load(f)
        return json.load(f)


def _normalize_criterion(criterion: dict[str, Any]) -> dict[str, Any]:
    """Expand a single criterion shorthand, or pass through a spatial one.

    A spatial criterion (already carrying ``feature_type``) is returned
    unchanged — this also makes normalization idempotent, since a
    column-value criterion normalized once carries the
    ``feature_type: "column_value"`` sentinel and matches this branch on a
    second pass.
    """
    if "feature_type" in criterion:
        return dict(criterion)

    if "column" not in criterion:
        raise ValueError(
            f"Criterion must declare either 'column' (simple shorthand) or "
            f"'feature_type' (full spec): {criterion}"
        )

    column = criterion["column"]
    return {
        "name": column,
        "dataset": "__column__",
        "feature_type": "column_value",
        "params": {},
        "value_fn": criterion.get("value_fn", {"kind": "linear"}),
        "weight": criterion["weight"],
        "direction": criterion.get("direction", "higher_better"),
        "_column": column,
    }


def _normalize_filter(hard_filter: dict[str, Any]) -> dict[str, Any]:
    """Expand a single hard-filter shorthand, or pass through a spatial one."""
    if "feature_type" in hard_filter:
        return dict(hard_filter)

    if "column" not in hard_filter:
        raise ValueError(
            f"Filter must declare either 'column' (simple shorthand) or "
            f"'feature_type' (full spec): {hard_filter}"
        )

    column = hard_filter["column"]
    return {
        "dataset": "__column__",
        "feature_type": "column_value",
        "params": {},
        "op": hard_filter["op"],
        "value": hard_filter["value"],
        "_column": column,
    }


def normalize_policy(raw_config: dict[str, Any]) -> dict[str, Any]:
    """Expand simple shorthand criteria/filters into full Criterion/HardFilter dicts.

    Walks ``raw_config["criteria"]`` and ``raw_config["filters"]``, expanding
    any entry that uses the ``{column, weight}`` (or ``{column, op, value}``)
    shorthand into a full dict compatible with ``Criterion``/``HardFilter``,
    tagged with a ``_column`` metadata key for use by the component. Entries
    already carrying ``feature_type`` (spatial criteria/filters) pass through
    unchanged. Idempotent: normalizing an already-normalized dict returns an
    equivalent dict.

    Args:
        raw_config: The raw ``policy``/``policy_file`` config dict.

    Returns:
        A normalized dict, ready for ``_column``-stripping and
        ``ScoringPolicy(**config)`` construction.
    """
    normalized: dict[str, Any] = dict(raw_config)

    normalized["criteria"] = [
        _normalize_criterion(c) for c in raw_config.get("criteria", [])
    ]

    if "filters" in raw_config:
        normalized["filters"] = [
            _normalize_filter(f) for f in raw_config.get("filters", [])
        ]

    return normalized
