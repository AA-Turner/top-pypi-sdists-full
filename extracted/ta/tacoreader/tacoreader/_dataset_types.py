"""Internal types for TacoDataset.

Groups related attributes to reduce complexity in TacoDataset.

Types:
    DatasetOrigin: Immutable source information (path, format, collection)
    QueryState: Mutable query state (view name, RSUT compliance, filters)
"""

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class DatasetOrigin:
    """Immutable dataset source information.
    
    Created once during load(), shared by reference across all child datasets
    from sql()/filter_*() operations. Frozen because this data never changes
    after initial load.
    
    Attributes:
        path: Original path to dataset (local or cloud URL)
        format: Storage format determining VSI construction and navigation
        vsi_base_path: Base path for GDAL VSI construction, format-specific:
            - ZIP: path to .tacozip file
            - FOLDER: path to dataset directory
            - TacoCat: path to parent directory containing ZIPs
        collection: Complete parsed COLLECTION.json with all metadata
    """
    path: str
    format: Literal["zip", "folder", "tacocat"]
    vsi_base_path: str
    collection: dict[str, Any]
    
    @property
    def field_schema(self) -> dict[str, Any]:
        """Field schema extracted from collection metadata."""
        return self.collection.get("taco:field_schema", {})


@dataclass
class QueryState:
    """Mutable state that changes with each query operation.
    
    Created fresh for each sql()/filter_*() call. Tracks the current
    query context including view references, RSUT compliance, and
    cascade filter state.
    
    Attributes:
        view_name: Current DuckDB view for queries. Starts as "data",
            becomes "view_<uuid>" after sql() calls for chaining.
        joined_levels: Level tables referenced in query chain (e.g., {"level1"}).
            Tracks which levels were touched, used for debugging.
        rsut_compliant: Whether dataset maintains structural homogeneity.
            False after cascade filters or sql() removing navigation columns.
        filtered_level_views: Views created by cascade filters, keyed by level.
            Enables TacoDataFrame.read() to query DuckDB instead of physical __meta__.
            Example: {1: "filtered_1_abc123", 2: "filtered_2_abc123"}
        extent_modified: True after any filtering operation. Signals that
            extent from COLLECTION.json no longer reflects actual data bounds.
        sort_by: Column name to sort by in flatten() (uses flat view prefixed names,
            e.g. "l0:stac:time_start"). None means no sorting.
        sort_descending: Sort direction. True = DESC, False = ASC (default).
        limit_n: Maximum number of rows to return in flatten(). None = no limit.
    """
    view_name: str = "data"
    joined_levels: set[str] = field(default_factory=set)
    rsut_compliant: bool = True
    filtered_level_views: dict[int, str] = field(default_factory=dict)
    extent_modified: bool = False
    sort_by: str | None = None
    sort_descending: bool = False
    limit_n: int | None = None