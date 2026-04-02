"""Abstract base class for TacoDataFrame backends.

Each backend (PyArrow, Polars, Pandas) implements this interface
with their native DataFrame APIs.

Cascade Filter Navigation:
    When cascade filters are applied (level>0), filtered views are stored
    in _filtered_level_views. The read() method checks this dict and queries
    DuckDB instead of reading physical __meta__ files, ensuring only filtered
    children are returned.

I/O Logic:
    Physical file reading is delegated to _meta_io module for testability.
    This class handles orchestration and TacoDataFrame construction.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from tacoreader._exceptions import TacoNavigationError


class TacoDataFrame(ABC):
    """Abstract base for hierarchical DataFrame navigation.

    Each backend implements:
    - DataFrame operations (filter, select, head, tail, etc.)
    - Hierarchical navigation (read())
    - Properties (columns, shape)
    - Factory method (from_arrow classmethod)

    Shared across all backends:
    - read() navigation logic (with cascade filter support)
    - _get_position() key resolution

    I/O operations delegated to:
    - _meta_io.read_meta_from_archive()
    - _meta_io.read_meta_from_folder()
    - _meta_io.query_filtered_children()
    """

    def __init__(
        self,
        data: Any,
        format_type: str,
        duckdb: Any = None,
        filtered_level_views: dict[int, str] | None = None,
        current_level: int = 0,
    ):
        """Initialize with backend-specific data structure.

        Args:
            data: PyArrow Table, Polars DataFrame, or Pandas DataFrame
            format_type: "zip", "folder", or "tacocat"
            duckdb: DuckDB connection for filtered view queries (optional)
            filtered_level_views: Dict mapping level -> filtered view name (optional)
            current_level: Current hierarchy level for navigation (default 0)
        """
        self._data = data
        self._format_type = format_type
        self._duckdb = duckdb
        self._filtered_level_views = filtered_level_views or {}
        self._current_level = current_level

    @classmethod
    @abstractmethod
    def from_arrow(
        cls,
        arrow_table,
        format_type: str,
        duckdb: Any = None,
        filtered_level_views: dict[int, str] | None = None,
        current_level: int = 0,
    ) -> TacoDataFrame:
        """Convert PyArrow Table to backend-specific TacoDataFrame."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        """Number of rows."""
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """String representation with format info."""
        pass

    @abstractmethod
    def __getitem__(self, key):
        """Subscripting (row/column access)."""
        pass

    @property
    @abstractmethod
    def columns(self):
        """Column names."""
        pass

    @property
    @abstractmethod
    def shape(self):
        """Shape tuple: (rows, columns)."""
        pass

    @abstractmethod
    def head(self, n: int):
        """First n rows."""
        pass

    @abstractmethod
    def tail(self, n: int):
        """Last n rows."""
        pass

    @abstractmethod
    def _get_row(self, position: int) -> dict:
        """Get row as dictionary (backend-specific).

        PyArrow: table.to_pylist()[position]
        Polars: df.row(position, named=True)
        Pandas: df.iloc[position].to_dict()
        """
        pass

    @abstractmethod
    def _to_arrow_for_stats(self):
        """Convert current data to PyArrow for stats functions."""
        pass

    def _get_position(self, key: int | str) -> int:
        """Convert key to integer position.

        Uses PyArrow for efficient ID search regardless of backend.
        """
        if isinstance(key, int):
            if key < 0 or key >= len(self):
                raise TacoNavigationError(
                    f"Position {key} out of range [0, {len(self) - 1}]"
                )
            return key

        # Search by ID using PyArrow
        import pyarrow.compute as pc

        arrow_table = self._to_arrow_for_stats()

        if "id" not in arrow_table.column_names:
            raise TacoNavigationError("Cannot search by ID: 'id' column not found")

        id_col = arrow_table.column("id")
        mask = pc.equal(id_col, key)

        for i, val in enumerate(mask):
            if val.as_py():
                return i

        raise TacoNavigationError(f"ID '{key}' not found")

    def read(self, key: int | str) -> TacoDataFrame | str:
        """Navigate to child level by position or ID.

        FILE samples: returns GDAL VSI path as string
        FOLDER samples:
          - If filtered views exist for child level -> query DuckDB
          - Otherwise -> read physical __meta__ file

        Args:
            key: Integer position (0-indexed) or string ID

        Returns:
            GDAL VSI path (str) for FILE, TacoDataFrame for FOLDER

        Raises:
            TacoNavigationError: If key not found or data corrupted
        """
        position = self._get_position(key)
        row = self._get_row(position)

        if row["type"] == "FILE":
            return row["internal:gdal_vsi"]

        # FOLDER: check for cascade filter path
        child_level = self._current_level + 1

        if child_level in self._filtered_level_views and self._duckdb is not None:
            return self._read_from_filtered_view(row, child_level)

        return self._read_from_meta_file(row)

    def _read_from_filtered_view(self, row: dict, child_level: int) -> TacoDataFrame:
        """Read children from DuckDB filtered view.

        Used when cascade filters have been applied. Queries DuckDB
        to get only children that matched the filter.
        """
        from tacoreader.dataframe._meta_io import query_filtered_children

        children_table = query_filtered_children(
            duckdb=self._duckdb,
            parent_row=row,
            filtered_view=self._filtered_level_views[child_level],
            format_type=self._format_type,
        )

        return self.__class__.from_arrow(
            children_table,
            self._format_type,
            duckdb=self._duckdb,
            filtered_level_views=self._filtered_level_views,
            current_level=child_level,
        )

    def _read_from_meta_file(self, row: dict) -> TacoDataFrame:
        """Read children from physical __meta__ file.

        Used when no filtered views exist for child level.
        Delegates I/O to _meta_io module.
        """
        from tacoreader.dataframe._meta_io import (
            read_meta_from_archive,
            read_meta_from_folder,
        )

        vsi_path = row["internal:gdal_vsi"]

        if vsi_path.startswith("/vsisubfile/"):
            children_table = read_meta_from_archive(vsi_path)
        else:
            children_table = read_meta_from_folder(vsi_path)

        return self.__class__.from_arrow(
            children_table,
            self._format_type,
            duckdb=self._duckdb,
            filtered_level_views=self._filtered_level_views,
            current_level=self._current_level + 1,
        )