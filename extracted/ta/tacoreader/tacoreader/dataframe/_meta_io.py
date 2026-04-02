"""I/O functions for __meta__ Parquet files.

Pure functions for reading hierarchical metadata and building VSI paths.
Extracted from TacoDataFrame for testability and clarity.

Functions:
    read_meta_from_archive: Read __meta__ from ZIP/TacoCat byte offset
    read_meta_from_folder: Read __meta__ from filesystem/remote
    query_filtered_children: Query DuckDB for cascade-filtered children
"""

from io import BytesIO
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from tacoreader._exceptions import TacoNavigationError
from tacoreader._format import is_remote
from tacoreader._remote_io import download_bytes, download_range
from tacoreader._vsi import parse_vsi_subfile, strip_vsi_prefix


def read_meta_from_archive(vsi_path: str) -> pa.Table:
    """Read __meta__ from ZIP or TacoCat archive.

    Parses /vsisubfile/ path, reads Parquet from byte offset,
    and builds VSI paths for children pointing back to archive.

    Args:
        vsi_path: /vsisubfile/{offset}_{size},{archive_path}

    Returns:
        PyArrow Table with children metadata + internal:gdal_vsi column

    Raises:
        TacoNavigationError: If children missing internal:offset or internal:size
    """
    # Parse /vsisubfile/ path
    root_path, offset, size = parse_vsi_subfile(vsi_path)
    original_path = strip_vsi_prefix(root_path)

    # Read Parquet bytes from offset
    if is_remote(original_path):
        parquet_bytes = download_range(original_path, offset, size)
    else:
        with open(original_path, "rb") as f:
            f.seek(offset)
            parquet_bytes = f.read(size)

    children_table = pq.read_table(BytesIO(parquet_bytes))

    # Build VSI paths for children
    vsi_paths = _build_archive_vsi_paths(children_table, root_path)

    vsi_array = pa.array(vsi_paths, type=pa.string())
    return children_table.append_column("internal:gdal_vsi", vsi_array)


def read_meta_from_folder(vsi_path: str) -> pa.Table:
    """Read __meta__ from FOLDER format.

    Reads Parquet from filesystem or remote storage, and builds
    direct paths to children using their id.

    Args:
        vsi_path: Direct path to folder (may end with /__meta__)
                  May contain VSI prefix like /vsicurl/ for remote paths.

    Returns:
        PyArrow Table with children metadata + internal:gdal_vsi column

    Raises:
        TacoNavigationError: If children missing id column
    """
    # Strip VSI prefix for I/O operations
    io_path = strip_vsi_prefix(vsi_path)

    # Read Parquet from __meta__
    children_table = _read_parquet_from_folder(io_path)

    # Determine parent path for child path construction
    parent_path = vsi_path
    if parent_path.endswith("/__meta__"):
        parent_path = parent_path[:-9]

    # Build paths using id
    vsi_paths = _build_folder_vsi_paths(children_table, parent_path)

    vsi_array = pa.array(vsi_paths, type=pa.string())
    return children_table.append_column("internal:gdal_vsi", vsi_array)


def query_filtered_children(
    duckdb,
    parent_row: dict,
    filtered_view: str,
    format_type: str,
) -> pa.Table:
    """Query DuckDB for cascade-filtered children.

    Used when cascade filters have been applied. Queries DuckDB to get
    only children that matched the filter, instead of reading physical
    __meta__ which contains ALL children.

    Args:
        duckdb: DuckDB connection
        parent_row: Parent row dict with internal:current_id
                    (and internal:source_file for tacocat)
        filtered_view: Name of filtered view (e.g., "filtered_1_abc123")
        format_type: "zip", "folder", or "tacocat"

    Returns:
        PyArrow Table with filtered children
    """
    from tacoreader._constants import (
        METADATA_CURRENT_ID,
        METADATA_PARENT_ID,
        METADATA_SOURCE_FILE,
    )

    parent_id = parent_row[METADATA_CURRENT_ID]

    # TacoCat needs source_file in WHERE condition
    if format_type == "tacocat":
        source_file = parent_row[METADATA_SOURCE_FILE]
        source_file_escaped = source_file.replace("'", "''")
        query = f"""
            SELECT * FROM {filtered_view}
            WHERE "{METADATA_PARENT_ID}" = {parent_id}
            AND "{METADATA_SOURCE_FILE}" = '{source_file_escaped}'
        """
    else:
        query = f"""
            SELECT * FROM {filtered_view}
            WHERE "{METADATA_PARENT_ID}" = {parent_id}
        """

    return duckdb.execute(query).fetch_arrow_table()


def _build_archive_vsi_paths(table: pa.Table, root_path: str) -> list[str]:
    """Build /vsisubfile/ paths for archive children.

    Each child in ZIP/TacoCat has internal:offset and internal:size
    that point to its data within the archive.
    """
    vsi_paths = []
    rows = table.to_pylist()

    for i, row in enumerate(rows):
        if "internal:offset" not in row or "internal:size" not in row:
            raise TacoNavigationError(
                f"Missing required metadata in ZIP/TacoCat format.\n"
                f"Row {i} (id={row.get('id', 'unknown')}) is missing "
                f"'internal:offset' or 'internal:size'.\n"
                f"Dataset may be corrupted or created with incompatible version."
            )

        child_offset = row["internal:offset"]
        child_size = row["internal:size"]
        vsi_paths.append(f"/vsisubfile/{child_offset}_{child_size},{root_path}")

    return vsi_paths


def _build_folder_vsi_paths(table: pa.Table, parent_path: str) -> list[str]:
    """Build direct paths for folder children.

    Each child in FOLDER format is a subdirectory named by its id.
    """
    vsi_paths = []
    rows = table.to_pylist()

    for i, row in enumerate(rows):
        if "id" not in row:
            raise TacoNavigationError(
                f"Missing 'id' in FOLDER format.\n"
                f"Row {i} (type={row.get('type', 'unknown')}) has no 'id'.\n"
                f"Dataset may be corrupted or created with incompatible version."
            )

        vsi_paths.append(f"{parent_path}/{row['id']}")

    return vsi_paths


def _read_parquet_from_folder(io_path: str) -> pa.Table:
    """Read Parquet from folder path (local or remote)."""
    if is_remote(io_path):
        if io_path.endswith("/__meta__"):
            meta_bytes = download_bytes(io_path)
        else:
            meta_bytes = download_bytes(io_path, "__meta__")
        return pq.read_table(BytesIO(meta_bytes))
    else:
        meta_path = (
            io_path
            if io_path.endswith("/__meta__")
            else str(Path(io_path) / "__meta__")
        )
        return pq.read_table(meta_path)