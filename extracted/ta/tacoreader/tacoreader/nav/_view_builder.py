"""TacoDataset construction after filter operations.

Single helper used by both simple (level=0) and cascade (level>0) filters
to avoid duplicating model_construct logic.

Functions:
    build_filtered_dataset: Construct child TacoDataset from filtered view
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tacoreader.dataset import TacoDataset


def build_filtered_dataset(
    dataset: "TacoDataset",
    final_view: str,
    new_n: int,
    rsut_compliant: bool,
    filtered_level_views: dict[int, str],
    joined_levels: set[str],
) -> "TacoDataset":
    """Construct a child TacoDataset from a filtered DuckDB view.

    Shares the parent's DuckDB connection and origin (immutable).
    Creates a fresh QueryState reflecting the new filtered state.

    Args:
        dataset: Parent TacoDataset (source of connection + origin + metadata)
        final_view: Name of the TEMP VIEW to use as new level0
        new_n: Row count of the filtered view (for pit_schema update)
        rsut_compliant: Whether filtered result maintains structural homogeneity
        filtered_level_views: Views created by cascade filters keyed by level.
            Empty dict for simple (level=0) filters.
        joined_levels: Level tables touched during filtering (for debugging)

    Returns:
        Child TacoDataset sharing parent's connection (_owns_connection=False)
    """
    from tacoreader._dataset_types import QueryState
    from tacoreader.dataset import TacoDataset as TDS

    new_query = QueryState(
        view_name=final_view,
        joined_levels=joined_levels,
        rsut_compliant=rsut_compliant,
        filtered_level_views=filtered_level_views,
        extent_modified=True,
    )

    new_schema = dataset.pit_schema.with_n(new_n)

    return TDS.model_construct(
        id=dataset.id,
        version=dataset.version,
        description=dataset.description,
        tasks=dataset.tasks,
        extent=dataset.extent,
        providers=dataset.providers,
        licenses=dataset.licenses,
        title=dataset.title,
        curators=dataset.curators,
        keywords=dataset.keywords,
        pit_schema=new_schema,
        _origin=dataset._origin,
        _duckdb=dataset._duckdb,
        _owns_connection=False,
        _query=new_query,
        _dataframe_backend=dataset._dataframe_backend,
    )