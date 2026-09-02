"""SweetSpotScore FlowComponent (FEAT-190, spec Module 8 / FEAT-191).

DAG node: DataFrame(s) in -> enriched DataFrame out. Wraps ``ScoringEngine``
(column-value criteria) and/or ``SweetSpotScorer`` (spatial criteria) for
pipeline use. No LLM, no agent, no dataset-manager dependency — the scoring
policy is provided via inline YAML component config or an external
YAML/JSON ``policy_file`` (FEAT-191, kept simple for v1, per spec Key
Constraints).

Example YAML (spatial, FEAT-190):

```yaml
SweetSpotScore:
  depends:
    - QueryToPandas_pois
    - QueryToPandas_census
  candidates:
    source: 0              # index into depends list
    lat_col: latitude
    lon_col: longitude
    id_col: store_id
  layers:
    - name: hotels
      source: 1
      lat_col: lat
      lon_col: lng
      attribute_cols: [rooms]
  policy:
    profile: pizza_midmarket
    criteria:
      - name: hotels
        dataset: hotels
        feature_type: gravity
        params: {k: 5, attribute: rooms, kernel: gaussian, bandwidth_m: 2000}
        value_fn: {kind: sigmoid, center: 500, steepness: 0.005}
        weight: 0.4
    aggregation: weighted_mean
```

Example YAML (column-value shorthand, FEAT-191). ``policy_file`` and
``policy`` are mutually exclusive — if both are set, ``policy_file`` takes
precedence and ``policy`` is ignored (a warning is logged). Use ONE of the
two forms below:

```yaml
# Form A: external policy file
SweetSpotScore:
  policy_file: scoring/store_ranking.yaml
  include_breakdown: true
```

```yaml
# Form B: inline policy block
SweetSpotScore:
  include_breakdown: true
  policy:
    profile: store_ranking
    criteria:
      - column: revenue
        weight: 0.5
      - column: rent
        weight: 0.2
        direction: lower_better
```
"""
from collections.abc import Callable
import asyncio
from typing import Optional

import numpy as np
import pandas as pd
from navconfig import BASE_DIR
from pydantic import ValidationError

from ...interfaces.flow import FlowComponent
from ...exceptions import ComponentError
from ...interfaces.scoring import (
    CandidateGrid,
    Criterion,
    HardFilter,
    POILayer,
    ScoreResult,
    ScoringPolicy,
)


class SweetSpotScore(FlowComponent):
    """DAG node: DataFrame(s) in, enriched DataFrame out.

    Supports three scoring modes, resolved automatically from the
    normalized policy at ``start()`` time (spec K4):

    - **Column-value-only**: every criterion/filter reads a DataFrame
      column directly (``ScoringEngine.score()`` called directly, no
      scipy/h3 import).
    - **Spatial-only**: existing FEAT-190 path, unchanged
      (``SweetSpotScorer.score()``).
    - **Mixed**: a unified feature matrix is assembled from both sources,
      then ``ScoringEngine.score()`` is called directly.
    """

    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        # Scoring config, extracted from YAML component arguments.
        self._policy_config: dict = kwargs.pop("policy", {})
        self._policy_file: Optional[str] = kwargs.pop("policy_file", None)
        self._candidates_config: dict = kwargs.pop("candidates", {})
        self._layers_config: list = kwargs.pop("layers", [])
        self._include_breakdown: bool = kwargs.pop("include_breakdown", False)
        self._scorer = None
        self._df: list = []
        # Populated in start(): the frozen, normalized ScoringPolicy plus
        # the criterion/filter-index -> column-name maps used by run() to
        # decide the column-value vs. spatial code path (spec Module 3/5).
        self._policy: Optional[ScoringPolicy] = None
        self._column_criteria: dict[int, str] = {}
        self._column_filters: dict[int, str] = {}
        super(SweetSpotScore, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            if isinstance(self.input, list):
                self._df = self.input  # multiple predecessor DataFrames
            else:
                self._df = [self.input]  # single predecessor DataFrame
        else:
            raise ComponentError(
                "SweetSpotScore requires input DataFrames", status=404
            )

        from .layers import load_policy_file, normalize_policy

        try:
            if self._policy_file:
                if self._policy_config:
                    self._logger.warning(
                        "SweetSpotScore: both 'policy_file' and 'policy' were "
                        "provided; 'policy_file' takes precedence and the "
                        "inline 'policy' block will be ignored."
                    )
                raw_policy = load_policy_file(self._policy_file, BASE_DIR)
            elif self._policy_config:
                raw_policy = self._policy_config
            else:
                raise ComponentError(
                    "SweetSpotScore requires either 'policy' (inline) or "
                    "'policy_file' (external YAML/JSON) configuration."
                )
            normalized = normalize_policy(raw_policy)
        except FileNotFoundError as exc:
            raise ComponentError(
                f"SweetSpotScore: policy_file not found: {exc}"
            ) from exc
        except ValueError as exc:
            raise ComponentError(
                f"SweetSpotScore: policy configuration error: {exc}"
            ) from exc

        # Separate column-value criteria/filters from spatial ones, and
        # strip the `_column` (and any other `_`-prefixed) metadata before
        # constructing the frozen ScoringPolicy. Column-value entries get a
        # placeholder `feature_type` (the engine never dispatches on it —
        # see spec K2/OQ2) so they validate against the spatial-only
        # `Criterion.feature_type`/`HardFilter.feature_type` Literal.
        column_criteria: dict[int, str] = {}
        clean_criteria = []
        for idx, criterion in enumerate(normalized.get("criteria", [])):
            column = criterion.get("_column")
            clean = {k: v for k, v in criterion.items() if not k.startswith("_")}
            if column is not None:
                column_criteria[idx] = column
                clean.setdefault("dataset", "__column__")
                clean["feature_type"] = "count_within_radius"
                clean.setdefault("params", {})
            clean_criteria.append(clean)

        column_filters: dict[int, str] = {}
        clean_filters = []
        for idx, hard_filter in enumerate(normalized.get("filters", [])):
            column = hard_filter.get("_column")
            clean = {k: v for k, v in hard_filter.items() if not k.startswith("_")}
            if column is not None:
                column_filters[idx] = column
                clean.setdefault("dataset", "__column__")
                clean["feature_type"] = "count_within_radius"
                clean.setdefault("params", {})
            clean_filters.append(clean)

        try:
            self._policy = ScoringPolicy(
                **{**normalized, "criteria": clean_criteria, "filters": clean_filters}
            )
        except ValidationError as exc:
            raise ComponentError(
                f"SweetSpotScore: invalid policy configuration: {exc}"
            ) from exc

        self._column_criteria = column_criteria
        self._column_filters = column_filters

        # Only spin up the spatial scorer facade (``SweetSpotScorer``) when
        # ``run()`` will actually take the all-spatial branch and call
        # ``self._scorer.score(...)`` directly — column-only policies must
        # NOT trigger a scipy/h3 import anywhere in their code path (spec
        # K3), and mixed policies use ``extractor_registry`` directly
        # (``_extract_spatial_feature``) instead of the scorer facade, so
        # constructing it there would be wasted work.
        is_all_spatial = not column_criteria and not column_filters and (
            self._policy.criteria or self._policy.filters
        )
        if is_all_spatial:
            # Lazy import: avoid pulling scipy/sklearn at component
            # registration time — only needed once the component actually
            # runs a spatial criterion.
            from flowtask.interfaces.scoring import SweetSpotScorer

            self._scorer = SweetSpotScorer()

        await super(SweetSpotScore, self).start(**kwargs)
        return True

    def _fill_column_features(
        self, matrix: np.ndarray, df: pd.DataFrame, mapping: dict[int, str]
    ) -> None:
        """Fill the given columns of ``matrix`` from ``df`` column values, in place.

        Args:
            matrix: Pre-allocated ``(N, C)`` feature/filter matrix.
            df: The primary input DataFrame.
            mapping: ``{column_index: column_name}`` for the column-value
                criteria/filters to fill.

        Raises:
            ComponentError: if a referenced column is missing or non-numeric.
        """
        for idx, column in mapping.items():
            if column not in df.columns:
                raise ComponentError(
                    f"SweetSpotScore: column {column!r} not found in input "
                    f"DataFrame. Available columns: {list(df.columns)}"
                )
            series = df[column]
            if not pd.api.types.is_numeric_dtype(series):
                raise ComponentError(
                    f"SweetSpotScore: column {column!r} is not numeric "
                    f"(dtype={series.dtype})."
                )
            values = series.to_numpy(dtype=float)
            nan_mask = np.isnan(values)
            if nan_mask.any():
                self._logger.warning(
                    "SweetSpotScore: column %r has %d NaN value(s), "
                    "replaced with 0.0",
                    column,
                    int(nan_mask.sum()),
                )
                values = np.nan_to_num(values, nan=0.0)
            matrix[:, idx] = values

    async def _extract_spatial_feature(
        self,
        candidates: CandidateGrid,
        layers: dict[str, POILayer],
        spec: Criterion | HardFilter,
    ) -> np.ndarray:
        """Compute one spatial criterion/filter's raw feature column.

        Mirrors ``SweetSpotScorer``'s internal extraction step, but uses the
        public ``extractor_registry`` directly (spec Module 3 Implementation
        Notes) so a single spatial column can be computed for the "mixed"
        code path without going through a full ``SweetSpotScorer.score()``
        call.

        Args:
            candidates: The candidate grid.
            layers: ``{dataset_name: POILayer}`` mapping.
            spec: A ``Criterion`` or ``HardFilter``.

        Returns:
            A numpy array of shape ``(N,)`` with raw feature values.
        """
        from flowtask.interfaces.scoring import extractor_registry

        # Ensure concrete extractors are registered (idempotent, cheap
        # after the first call).
        import flowtask.interfaces.scoring.extractors  # noqa: F401

        try:
            poi_layer = layers[spec.dataset]
        except KeyError as exc:
            raise ValueError(
                f"No POILayer found for dataset {spec.dataset!r}. "
                f"Available datasets: {sorted(layers.keys())}"
            ) from exc
        extractor_cls = extractor_registry.get(spec.feature_type)
        extractor = extractor_cls()
        return await extractor.compute(candidates, poi_layer, spec.params)

    async def run(self):
        from .layers import build_candidate_grid, build_poi_layers

        df = self._df[0]
        n_criteria = len(self._policy.criteria)
        n_filters = len(self._policy.filters)
        has_spatial_criteria = len(self._column_criteria) < n_criteria
        has_spatial_filters = len(self._column_filters) < n_filters

        # The framework-agnostic scoring package (models/service/extractors)
        # deliberately raises plain built-in exceptions (ValueError, KeyError,
        # pydantic's ValidationError) — it has no dependency on flowtask's
        # DAG runtime (spec G2). This is the boundary where those errors get
        # translated into a DAG-friendly ComponentError with a message that
        # names this component, instead of an opaque KeyError/IndexError
        # surfacing several frames deep from a misconfigured YAML (e.g. a
        # `dataset` name with no matching `layers` entry, or an out-of-range
        # `source` index). ComponentErrors raised directly below (e.g. from
        # `_fill_column_features`) are intentionally NOT in this tuple, so
        # they propagate unwrapped instead of being double-wrapped.
        try:
            if not has_spatial_criteria and not has_spatial_filters:
                # Column-value-only path (spec K3/K4): no CandidateGrid/
                # POILayer, no scipy/h3 import anywhere in this branch.
                feature_matrix = np.zeros((len(df), n_criteria))
                self._fill_column_features(feature_matrix, df, self._column_criteria)
                filter_matrix = None
                if n_filters:
                    filter_matrix = np.zeros((len(df), n_filters))
                    self._fill_column_features(filter_matrix, df, self._column_filters)

                from flowtask.interfaces.scoring import ScoringEngine

                result = ScoringEngine().score(
                    feature_matrix, self._policy, filter_matrix=filter_matrix
                )
            elif not self._column_criteria and not self._column_filters:
                # All-spatial — existing FEAT-190 path, unchanged (AC7).
                candidates = build_candidate_grid(self._df, self._candidates_config)
                layers = build_poi_layers(self._df, self._layers_config)
                result = await self._scorer.score(candidates, layers, self._policy)
            else:
                # Mixed — unify column-value + spatial columns into one
                # feature matrix, in policy.criteria/policy.filters order.
                candidates = build_candidate_grid(self._df, self._candidates_config)
                layers = build_poi_layers(self._df, self._layers_config)

                feature_matrix = np.zeros((len(df), n_criteria))
                self._fill_column_features(feature_matrix, df, self._column_criteria)
                for idx, criterion in enumerate(self._policy.criteria):
                    if idx not in self._column_criteria:
                        feature_matrix[:, idx] = await self._extract_spatial_feature(
                            candidates, layers, criterion
                        )

                filter_matrix = None
                if n_filters:
                    filter_matrix = np.zeros((len(df), n_filters))
                    self._fill_column_features(filter_matrix, df, self._column_filters)
                    for idx, hard_filter in enumerate(self._policy.filters):
                        if idx not in self._column_filters:
                            filter_matrix[:, idx] = await self._extract_spatial_feature(
                                candidates, layers, hard_filter
                            )

                from flowtask.interfaces.scoring import ScoringEngine

                result = ScoringEngine().score(
                    feature_matrix, self._policy, filter_matrix=filter_matrix
                )
        except (KeyError, IndexError, ValueError, ValidationError) as exc:
            raise ComponentError(
                f"SweetSpotScore: configuration or scoring error: {exc}"
            ) from exc

        self._result = self._enrich_dataframe(df, result)
        self.add_metric("NUM_ROWS", self._result.shape[0])
        self.add_metric("NUM_COLUMNS", self._result.shape[1])
        return self._result

    def _enrich_dataframe(self, df: pd.DataFrame, result: ScoreResult) -> pd.DataFrame:
        """Merge a ``ScoreResult`` into a copy of the original DataFrame.

        Adds ``sweetspot_score`` (float, 0-100), ``sweetspot_rank`` (int,
        1-based, descending — ties share the same rank via
        ``method="min"``), and ``sweetspot_filtered`` (bool). When
        ``include_breakdown`` is enabled, also adds
        ``sweetspot_{criterion_name}_utility``/``_contribution`` columns
        per criterion (spec Module 4).

        Args:
            df: The primary input DataFrame (never mutated — a copy is
                returned).
            result: The ``ScoreResult`` produced by scoring.

        Returns:
            A new, enriched DataFrame.
        """
        enriched = df.copy()

        base_columns = ("sweetspot_score", "sweetspot_rank", "sweetspot_filtered")
        for col in base_columns:
            if col in enriched.columns:
                self._logger.warning(
                    "SweetSpotScore: column %r already exists in the input "
                    "DataFrame, overwriting.",
                    col,
                )

        enriched["sweetspot_score"] = result.scores
        enriched["sweetspot_rank"] = (
            enriched["sweetspot_score"]
            .rank(ascending=False, method="min")
            .astype(int)
        )
        enriched["sweetspot_filtered"] = result.filtered_out

        if self._include_breakdown:
            for criterion in self._policy.criteria:
                name = criterion.name
                for suffix, field in (
                    ("utility", "utility"),
                    ("contribution", "contribution"),
                ):
                    col_name = f"sweetspot_{name}_{suffix}"
                    if col_name in enriched.columns:
                        self._logger.warning(
                            "SweetSpotScore: column %r already exists in "
                            "the input DataFrame, overwriting.",
                            col_name,
                        )
                    enriched[col_name] = [
                        row[name][field] for row in result.breakdown
                    ]

        return enriched

    async def close(self):
        pass
