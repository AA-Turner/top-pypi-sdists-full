"""Scoring contract types (FEAT-190).

Framework-agnostic Pydantic models for the SweetSpot spatial scoring engine.
This module has ZERO dependency on agents, LLM clients, dataset managers, or
the flowtask DAG runtime (spec G2, AC9, AC11).

Only lightweight dependencies are imported here: ``pydantic``, ``numpy`` and
``pandas``. Heavy dependencies (``scipy``, ``h3``) MUST NOT be imported in
this module — see spec §6 Codebase Contract / Does NOT Exist.
"""
from __future__ import annotations

from typing import Any, Literal, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

Direction = Literal["higher_better", "lower_better"]


class ValueFunction(BaseModel):
    """Raw scalar → [0,100] mapping config.

    May be non-monotone (spec D2), e.g. a threshold band value function that
    rewards a "sweet spot" range rather than a strictly increasing/decreasing
    curve.
    """

    kind: Literal["threshold", "linear", "sigmoid", "gaussian_decay", "quantile"]
    bands: Optional[list[tuple[float, float]]] = None
    center: Optional[float] = None
    steepness: Optional[float] = None


class ExtractorParams(BaseModel):
    """Parameters consumed by a feature extractor (spec Module 5)."""

    radius_m: Optional[float] = None
    k: int = 1
    attribute: Optional[str] = None
    kernel: Optional[Literal["gaussian", "exponential"]] = None
    bandwidth_m: Optional[float] = None


class Criterion(BaseModel):
    """A single scoring criterion: extractor + value function + weight.

    Note:
        ``direction`` only affects ``value_fn.kind in ("linear", "sigmoid")``.
        For ``"threshold"`` and ``"gaussian_decay"`` value functions,
        directionality is already encoded in the configured bands/center
        (spec D2/D3a), so ``direction`` has no effect on the computed
        utility for those kinds — see ``ScoringEngine._apply_value_function``.
    """

    name: str
    dataset: str
    feature_type: Literal["count_within_radius", "nearest_distance", "gravity"]
    params: ExtractorParams
    value_fn: ValueFunction
    weight: float
    direction: Direction = "higher_better"


class HardFilter(BaseModel):
    """Non-compensatory veto — boolean mask applied BEFORE scoring (spec D5)."""

    dataset: str
    feature_type: Literal["count_within_radius", "nearest_distance", "gravity"]
    params: ExtractorParams
    op: Literal["lte", "gte"]
    value: float


class ScoringPolicy(BaseModel):
    """Declarative, frozen, auditable scoring policy (spec G3).

    Frozen so that a policy's provenance hash (``ScoreResult.policy_hash``,
    spec AC10) is always trustworthy: once constructed, a ``ScoringPolicy``
    cannot be mutated.

    ``criteria``/``filters`` are declared as ``tuple[...]`` rather than
    ``list[...]``. Pydantic's ``model_config = {"frozen": True}`` only
    blocks *reassigning* a field (``policy.profile = "x"``) — it does NOT
    deep-freeze mutable containers, so a ``list`` field would still allow
    ``policy.criteria.append(...)`` to silently mutate a "frozen" policy in
    place (and desync its ``policy_hash`` from its contents). ``tuple`` is
    immutable, so this class of bug is not just discouraged but structurally
    impossible. Plain lists passed in at construction time are coerced to
    tuples by pydantic validation, so callers may still write
    ``ScoringPolicy(criteria=[...])``.
    """

    model_config = {"frozen": True}

    profile: str
    criteria: tuple[Criterion, ...] = Field(default_factory=tuple)
    filters: tuple[HardFilter, ...] = Field(default_factory=tuple)
    aggregation: Literal["weighted_mean", "weighted_geomean"] = "weighted_mean"


class POILayer(BaseModel):
    """A set of points-of-interest with coordinates and optional attributes."""

    model_config = {"arbitrary_types_allowed": True}

    name: str
    latitudes: np.ndarray
    longitudes: np.ndarray
    attributes: dict[str, np.ndarray] = Field(default_factory=dict)

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        name: str,
        lat_col: str = "latitude",
        lon_col: str = "longitude",
        attribute_cols: Optional[list[str]] = None,
    ) -> "POILayer":
        """Build a ``POILayer`` from a DataFrame.

        Follows the flowtask geometry contract used by ``NearByStores`` and
        ``MarketClustering``: plain ``latitude``/``longitude`` float columns.

        Args:
            df: Source DataFrame.
            name: Layer name (e.g. the dataset name).
            lat_col: Name of the latitude column.
            lon_col: Name of the longitude column.
            attribute_cols: Optional list of extra columns to carry as
                per-point attributes (e.g. ``rooms`` for a gravity model).

        Returns:
            A populated ``POILayer``.
        """
        attrs: dict[str, np.ndarray] = {}
        if attribute_cols:
            for col in attribute_cols:
                attrs[col] = df[col].to_numpy()
        return cls(
            name=name,
            latitudes=df[lat_col].to_numpy(),
            longitudes=df[lon_col].to_numpy(),
            attributes=attrs,
        )


class CandidateGrid(BaseModel):
    """Candidate locations to score.

    Either explicit points (``from_dataframe``) or H3 hex centroids
    (``from_h3``, implemented in TASK-128 / ``flowtask.interfaces.scoring.spatial``).
    """

    model_config = {"arbitrary_types_allowed": True}

    latitudes: np.ndarray
    longitudes: np.ndarray
    ids: Optional[list[str]] = None
    h3_resolution: Optional[int] = None

    @classmethod
    def from_h3(
        cls,
        bbox: tuple[float, float, float, float],
        resolution: int = 8,
    ) -> "CandidateGrid":
        """Tessellate a bounding box into H3 hex centroids.

        Delegates to ``flowtask.interfaces.scoring.spatial.h3_tessellate``
        (TASK-126), imported lazily here so that this module stays
        importable without h3 installed (spec AC11) — h3 is only required
        at call time, not at import time.

        Args:
            bbox: ``(min_lat, min_lng, max_lat, max_lng)``.
            resolution: H3 resolution (0-15). Higher = smaller hexes.

        Returns:
            A ``CandidateGrid`` with one candidate per H3 cell centroid.

        Raises:
            ImportError: if the ``h3`` package is not installed.
        """
        from .spatial import h3_tessellate

        return h3_tessellate(bbox, resolution=resolution)

    @classmethod
    def from_dataframe(
        cls,
        df: pd.DataFrame,
        lat_col: str = "latitude",
        lon_col: str = "longitude",
        id_col: Optional[str] = None,
    ) -> "CandidateGrid":
        """Build a ``CandidateGrid`` from a DataFrame of explicit candidates.

        Args:
            df: Source DataFrame.
            lat_col: Name of the latitude column.
            lon_col: Name of the longitude column.
            id_col: Optional column with candidate identifiers.

        Returns:
            A populated ``CandidateGrid``.
        """
        ids = df[id_col].tolist() if id_col else None
        return cls(
            latitudes=df[lat_col].to_numpy(),
            longitudes=df[lon_col].to_numpy(),
            ids=ids,
        )


class ScoreResult(BaseModel):
    """Scoring output with mandatory policy provenance hash (spec OQ5→YES)."""

    model_config = {"arbitrary_types_allowed": True}

    scores: np.ndarray
    breakdown: list[dict[str, Any]]
    filtered_out: np.ndarray
    policy_hash: str
    candidate_ids: Optional[list[str]] = None
