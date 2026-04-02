"""TacoDataset - metadata container with lazy SQL interface.

Provides STAC-like metadata with DuckDB connection for lazy SQL queries.
Queries are not executed until .data is accessed.

Backend-agnostic: Uses factory pattern to create TacoDataFrame instances
without importing specific backend implementations.

Two branches:
    sql/   → ds.sql(query)    → native DataFrame (immediate)
    nav/   → ds.filter_*(...) → TacoDataset (navigable)
"""

from contextlib import suppress
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict, PrivateAttr

from tacoreader._constants import (
    DEFAULT_VIEW_NAME,
    LEVEL_VIEW_PREFIX,
    STATS_SUPPORTED_COLUMNS,
    STATS_WEIGHT_COLUMN,
)
from tacoreader._dataset_types import DatasetOrigin, QueryState
from tacoreader._exceptions import TacoQueryError
from tacoreader._logging import get_logger
from tacoreader.schema import PITSchema

if TYPE_CHECKING:
    import numpy as np

    from tacoreader.dataframe.base import TacoDataFrame

logger = get_logger(__name__)


class TacoDataset(BaseModel):
    """TACO dataset with lazy SQL interface.

    Metadata container backed by DuckDB for lazy query execution. Queries
    create views without materializing data until .data is accessed.

    Connection Management:
        Datasets own their DuckDB connection. Use context manager for
        automatic cleanup:

            with tacoreader.load("data.taco") as ds:
                result = ds.sql("SELECT * FROM l2 WHERE ...")

        Child datasets from filter_*() share the parent's connection.
        Without explicit close(), connection persists until process exit.

    Attributes:
        id: Dataset identifier
        version: Dataset version string
        description: Human-readable description
        tasks: List of ML tasks this dataset supports
        extent: Spatial and temporal bounds
        providers: Data providers metadata
        licenses: License identifiers
        title: Optional display title
        curators: Optional curator information
        keywords: Optional search keywords
        pit_schema: Position-Isomorphic Tree schema
    """

    id: str
    version: str
    description: str
    tasks: list[str]
    extent: dict[str, Any]
    providers: list[dict[str, Any]]
    licenses: list[str]
    title: str | None = None
    curators: list[dict[str, Any]] | None = None
    keywords: list[str] | None = None
    pit_schema: PITSchema

    _origin: DatasetOrigin = PrivateAttr()
    _duckdb: Any = PrivateAttr(default=None)
    _owns_connection: bool = PrivateAttr(default=True)
    _query: QueryState = PrivateAttr()
    _dataframe_backend: str = PrivateAttr(default="pyarrow")

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def field_schema(self) -> dict[str, Any]:
        """Field schema from collection metadata."""
        return self._origin.field_schema

    @property
    def collection(self) -> dict[str, Any]:
        """Complete COLLECTION.json content with all metadata."""
        return self._origin.collection.copy()

    def close(self):
        """Close DuckDB connection and cleanup views.

        Only closes if this dataset owns the connection. Children from
        filter_*() share the parent's connection and skip cleanup.
        """
        if not hasattr(self, "_duckdb") or self._duckdb is None:
            return

        if hasattr(self, "_query") and self._query.view_name != DEFAULT_VIEW_NAME:
            with suppress(Exception):
                self._duckdb.execute(f"DROP VIEW IF EXISTS {self._query.view_name}")

        if hasattr(self, "_owns_connection") and self._owns_connection:
            with suppress(Exception):
                self._duckdb.close()
            self._duckdb = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def _check_rsut_compliance(self) -> bool:
        """Verify Invariant 3: structural homogeneity at level-1."""
        if self.pit_schema.root["type"] == "FILE":
            return True
        if self.pit_schema.max_depth() == 0:
            return True

        query = """
            WITH parent_children AS (
                SELECT
                    l0."internal:current_id" as parent_id,
                    STRING_AGG(l1.id, '|' ORDER BY l1.id) as children_sig
                FROM level0 l0
                LEFT JOIN level1 l1 ON l1."internal:parent_id" = l0."internal:current_id"
                GROUP BY l0."internal:current_id"
            )
            SELECT COUNT(DISTINCT children_sig) <= 1 as is_homogeneous
            FROM parent_children
        """
        try:
            result = self._duckdb.execute(query).fetchone()
            return bool(result[0]) if result else True
        except Exception:
            return True

    def is_rsut(self) -> bool:
        """Check if dataset maintains RSUT structural homogeneity."""
        return self._query.rsut_compliant

    def verify_rsut(self) -> bool:
        """Re-verify RSUT compliance and update internal state."""
        self._query.rsut_compliant = self._check_rsut_compliance()
        return self._query.rsut_compliant

    @property
    def data(self) -> "TacoDataFrame":
        """Materialize current view to TacoDataFrame.

        Executes DuckDB query and loads data into memory. Removes internal:*
        columns except those needed for navigation. Use .data_raw for all columns.
        """
        return self._materialize(raw=False)

    @property
    def data_raw(self) -> "TacoDataFrame":
        """Materialize current view keeping all internal:* columns."""
        return self._materialize(raw=True)

    def _materialize(self, raw: bool) -> "TacoDataFrame":
        from tacoreader._constants import (
            METADATA_CURRENT_ID,
            METADATA_PARENT_ID,
            METADATA_SOURCE_FILE,
        )
        from tacoreader.dataframe import create_dataframe

        arrow_table = self._duckdb.execute(
            f"SELECT * FROM {self._query.view_name}"
        ).fetch_arrow_table()

        # Filter legacy TACOPAD rows (ZIP alignment padding from TacoToolbox)
        if "id" in arrow_table.column_names:
            import pyarrow.compute as pc
            mask = pc.invert(pc.starts_with(arrow_table.column("id"), "__TACOPAD"))
            arrow_table = arrow_table.filter(mask)

        if not raw:
            keep_internals = {"internal:gdal_vsi"}

            if self._query.filtered_level_views:
                keep_internals.add(METADATA_CURRENT_ID)
                keep_internals.add(METADATA_PARENT_ID)
                if self._origin.format == "tacocat":
                    keep_internals.add(METADATA_SOURCE_FILE)

            columns_to_keep = [
                col for col in arrow_table.column_names
                if not col.startswith("internal:") or col in keep_internals
            ]
            arrow_table = arrow_table.select(columns_to_keep)

        return create_dataframe(
            backend=self._dataframe_backend,
            arrow_table=arrow_table,
            format_type=self._origin.format,
            duckdb=self._duckdb,
            filtered_level_views=self._query.filtered_level_views,
            current_level=0,
        )

    def navigation_columns(self, describe: bool = False) -> list[str] | dict[str, str]:
        """Get columns required for navigation and concat operations.

        Args:
            describe: If True, return dict with column descriptions

        Returns:
            Column names list, or {column: description} dict if describe=True
        """
        from tacoreader._constants import (
            NAVIGATION_COLUMN_DESCRIPTIONS,
            NAVIGATION_COLUMNS_BY_FORMAT,
        )

        columns = NAVIGATION_COLUMNS_BY_FORMAT.get(self._origin.format, frozenset())

        if describe:
            return {col: NAVIGATION_COLUMN_DESCRIPTIONS.get(col, "") for col in sorted(columns)}

        return sorted(columns)

    def sql(self, query: str) -> Any:
        """Execute SQL query and return native DataFrame immediately.

        Flat views available (all columns prefixed by level):
            l0 → root level columns as "l0:col"
            l1 → l1 + l0 columns as "l1:col", "l0:col"
            l2 → l2 + l1 + l0 columns as "l2:col", "l1:col", "l0:col"

        Args:
            query: SQL query string using l0, l1, l2, ... as table names.

        Returns:
            pa.Table / pl.DataFrame / pd.DataFrame depending on tacoreader.use()

        Example:
            files = dataset.sql(\"\"\"
                SELECT "l2:id", "l2:internal:gdal_vsi"
                FROM l2
                WHERE "l0:stac:time_start" LIKE '2020%'
                AND "l1:id" LIKE '%NORTH_PACIFIC%'
            \"\"\")
        """
        from tacoreader.sql import execute_sql
        return execute_sql(self._duckdb, query, self._dataframe_backend)

    def flatten(self, level: int | None = None) -> Any:
        """Return all FILE rows with full ancestral metadata.

        Queries the flat view at target level keeping only FILE rows.
        All ancestor metadata (l0:*, l1:*, ...) is included automatically.
        Internal navigation columns are excluded. gdal_vsi is renamed to 'gdal_vsi'.

        Args:
            level: Target level (None = max_depth, the deepest FILE level)

        Returns:
            pa.Table / pl.DataFrame / pd.DataFrame depending on tacoreader.use()

        Example:
            # All files at deepest level
            files = dataset.flatten()

            # After filtering + sort + limit
            files = (
                dataset
                .filter_bbox(130, 30, 160, 35, level=1)
                .sort("l0:stac:time_start")
                .limit(100)
                .flatten()
            )
        """
        from tacoreader.sql import execute_flatten
        return execute_flatten(
            self._duckdb,
            self._dataframe_backend,
            self.pit_schema,
            self._origin.format,
            self._query.filtered_level_views,
            self._query.view_name,
            level,
            sort_by=self._query.sort_by,
            sort_descending=self._query.sort_descending,
            limit_n=self._query.limit_n,
        )

    def sort(self, by: str, descending: bool = False) -> "TacoDataset":
        """Set sort order for flatten().

        Sorting applies to flat view column names (prefixed).

        Args:
            by: Column name using flat view prefix (e.g. "l0:stac:time_start")
            descending: True for DESC, False for ASC (default)

        Returns:
            self (chainable)

        Example:
            dataset.filter_datetime("2021-01-01/2021-12-31").sort("l0:stac:time_start").flatten()
        """
        self._query.sort_by = by
        self._query.sort_descending = descending
        return self

    def limit(self, n: int) -> "TacoDataset":
        """Limit number of rows returned by flatten().

        Args:
            n: Maximum number of rows

        Returns:
            self (chainable)

        Example:
            dataset.filter_bbox(...).sort("l0:stac:time_start").limit(500).flatten()
        """
        self._query.limit_n = n
        return self

    def read(self, key: int | str) -> "TacoDataFrame | str":
        """Navigate to child level by position or ID.

        Equivalent to dataset.data.read(key).

        Args:
            key: Integer position (0-indexed) or string ID

        Returns:
            GDAL VSI path (str) for FILE, TacoDataFrame for FOLDER
        """
        return self.data.read(key)

    def filter_bbox(
        self,
        minx: float,
        miny: float,
        maxx: float,
        maxy: float,
        geometry_col: str = "auto",
        level: int = 0,
    ) -> "TacoDataset":
        """Filter by bounding box.

        Args:
            minx, miny, maxx, maxy: Bounding box coordinates
            geometry_col: Geometry column name ("auto" for detection)
            level: Hierarchy level (0=direct, >0=cascade through children)

        Returns:
            Filtered TacoDataset
        """
        from tacoreader.nav import apply_bbox_filter
        return apply_bbox_filter(self, minx, miny, maxx, maxy, geometry_col, level)

    def filter_datetime(
        self,
        datetime_range,
        time_col: str = "auto",
        level: int = 0,
    ) -> "TacoDataset":
        """Filter by temporal range.

        Args:
            datetime_range: String range "2023-01-01/2023-12-31", datetime, or tuple
            time_col: Time column name ("auto" for detection)
            level: Hierarchy level (0=direct, >0=cascade through children)

        Returns:
            Filtered TacoDataset
        """
        from tacoreader.nav import apply_datetime_filter
        return apply_datetime_filter(self, datetime_range, time_col, level)

    def _get_stats_column(self, level: int) -> str:
        level_view = f"{LEVEL_VIEW_PREFIX}{level}"
        result = self._duckdb.execute(f"DESCRIBE {level_view}").fetchall()
        columns = {row[0] for row in result}

        for stats_col in STATS_SUPPORTED_COLUMNS:
            if stats_col in columns:
                return stats_col

        raise TacoQueryError(
            f"Level {level} does not contain statistics.\n"
            f"Expected one of: {', '.join(STATS_SUPPORTED_COLUMNS)}\n"
            f"Available columns: {sorted(columns)}"
        )

    def _validate_stats_params(self, level: int, id: str | None) -> None:
        max_depth = self.pit_schema.max_depth()
        if level < 0 or level > max_depth:
            raise TacoQueryError(
                f"Level {level} does not exist.\nAvailable levels: 0 to {max_depth}"
            )

        if level > 0 and id is None:
            raise TacoQueryError(
                f"id is required for level > 0.\n"
                f"Level {level} may have heterogeneous structure across branches.\n"
                f"Specify which sample to aggregate: stats_*(band=..., level={level}, id='...')"
            )

        if level == 0 and id is not None:
            logger.debug(f"id='{id}' ignored for level=0 (aggregates all samples)")

    def _fetch_stats_table(self, level: int, id: str | None, stats_col: str):
        level_view = f"{LEVEL_VIEW_PREFIX}{level}"

        if level == 0:
            query = f'SELECT "{stats_col}", "{STATS_WEIGHT_COLUMN}" FROM {level_view}'
        else:
            parent_level = level - 1
            parent_view = f"{LEVEL_VIEW_PREFIX}{parent_level}"
            query = f"""
                SELECT l."{stats_col}", l."{STATS_WEIGHT_COLUMN}"
                FROM {level_view} l
                INNER JOIN {parent_view} p ON l."internal:parent_id" = p."internal:current_id"
                WHERE p.id = '{id}'
            """

        return self._duckdb.execute(query).fetch_arrow_table()

    def _extract_band(self, result: "np.ndarray", band: int | list[int]) -> "np.ndarray":
        if isinstance(band, int):
            if band < 0 or band >= result.shape[0]:
                raise TacoQueryError(
                    f"Band {band} out of range.\nAvailable bands: 0 to {result.shape[0] - 1}"
                )
            return result[band]
        else:
            for b in band:
                if b < 0 or b >= result.shape[0]:
                    raise TacoQueryError(
                        f"Band {b} out of range.\nAvailable bands: 0 to {result.shape[0] - 1}"
                    )
            return result[list(band)]

    def _compute_stat(self, stat_name: str, band: int | list[int], level: int, id: str | None) -> "np.ndarray":
        self._validate_stats_params(level, id)
        stats_col = self._get_stats_column(level)
        table = self._fetch_stats_table(level, id, stats_col)

        from tacoreader.dataframe._stats import (
            _aggregate_categorical,
            _aggregate_continuous,
            _aggregate_std,
        )

        if stat_name == "std":
            result = _aggregate_std(table, stats_col)
        elif stat_name == "categorical":
            result = _aggregate_categorical(table, stats_col)
        else:
            result = _aggregate_continuous(table, stats_col, stat_name)

        return self._extract_band(result, band)

    def stats_mean(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Aggregate mean values across samples."""
        return self._compute_stat("mean", band, level, id)

    def stats_std(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Aggregate standard deviation using pooled variance formula."""
        return self._compute_stat("std", band, level, id)

    def stats_min(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Get global minimum across samples."""
        return self._compute_stat("min", band, level, id)

    def stats_max(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Get global maximum across samples."""
        return self._compute_stat("max", band, level, id)

    def stats_p25(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Aggregate 25th percentile (approximation via averaging)."""
        return self._compute_stat("p25", band, level, id)

    def stats_p50(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Aggregate 50th percentile / median (approximation via averaging)."""
        return self._compute_stat("p50", band, level, id)

    def stats_median(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Alias for stats_p50()."""
        return self.stats_p50(band, level, id)

    def stats_p75(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Aggregate 75th percentile (approximation via averaging)."""
        return self._compute_stat("p75", band, level, id)

    def stats_p95(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Aggregate 95th percentile (approximation via averaging)."""
        return self._compute_stat("p95", band, level, id)

    def stats_categorical(self, band: int | list[int], level: int = 0, id: str | None = None) -> "np.ndarray":
        """Aggregate categorical probabilities using weighted average."""
        return self._compute_stat("categorical", band, level, id)

    def __repr__(self) -> str:
        lines = [f"<TacoDataset '{self.id}'>"]
        lines.append(f"├── Version: {self.version}")

        desc_short = self.description[:80] + "..." if len(self.description) > 80 else self.description
        lines.append(f"├── Description: {desc_short}")
        lines.append(f"├── Tasks: {', '.join(self.tasks)}")

        spatial = self.extent.get("spatial")
        if spatial:
            extent_str = f"[{spatial[0]:.2f}°, {spatial[1]:.2f}°, {spatial[2]:.2f}°, {spatial[3]:.2f}°]"
            if self._query.extent_modified:
                extent_str += " (filtered)"
            lines.append(f"├── Spatial Extent: {extent_str}")

        temporal = self.extent.get("temporal")
        if temporal:
            start_str = self._format_temporal_string(temporal[0])
            end_str = self._format_temporal_string(temporal[1])
            extent_str = f"{start_str} → {end_str}"
            if self._query.extent_modified:
                extent_str += " (filtered)"
            lines.append(f"├── Temporal Extent: {extent_str}")

        lines.append("│")
        rsut_status = "True" if self._query.rsut_compliant else "False"
        lines.append(f"└── Level 0: {self.pit_schema.root['n']} rows (RSUT: {rsut_status})")

        return "\n".join(lines)

    def _format_temporal_string(self, iso_string: str) -> str:
        clean_str = iso_string.replace("Z", "")

        if "T00:00:00" in clean_str:
            return clean_str.split("T")[0]
        else:
            date_part, time_part = clean_str.split("T")
            if "." in time_part:
                time_part = time_part.split(".")[0]
            return f"{date_part} {time_part}"

    def _repr_html_(self):
        from tacoreader._html import build_html_repr
        return build_html_repr(self)