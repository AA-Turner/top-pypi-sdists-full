"""Parameter classes for AG Grid renderer configurations."""

from typing import Any, Mapping, Sequence

from reflex.vars.base import Var

from .base import JS_EXPRESSION, AgGridParamsBase, AgGridResourceBase


class DetailGridOptions(AgGridResourceBase):
    """Options for detail grid in master detail setup."""

    # Column definitions for the detail grid
    column_defs: (
        Sequence[Mapping[str, Any]] | Var[Sequence[Mapping[str, Any]]] | None
    ) = None

    # Default column definition for the detail grid
    default_col_def: Mapping[str, Any] | Var[Mapping[str, Any]] | None = None

    # Enable pagination in the detail grid
    pagination: bool | Var[bool] | None = None

    # Number of rows per page in the detail grid
    pagination_page_size: int | Var[int] | None = None

    # Enable sorting in the detail grid
    sortable: bool | Var[bool] | None = None

    # Enable filtering in the detail grid
    filterable: bool | Var[bool] | None = None

    # Row height for the detail grid
    row_height: int | Var[int] | None = None

    # Enable row selection in the detail grid
    row_selection: str | dict | Var[str] | Var[dict] | None = None


class DetailCellRendererParams(AgGridParamsBase):
    """Parameters for detail cell renderer in master detail setup."""

    # Options for the detail grid
    detail_grid_options: (
        DetailGridOptions | dict | Var[DetailGridOptions] | Var[dict] | None
    ) = None

    # Function to get data for the detail row
    get_detail_row_data: JS_EXPRESSION | None = None

    # Template for the detail row
    detail_row_template: str | Var[str] | None = None

    # Custom renderer for the detail row
    detail_cell_renderer: JS_EXPRESSION | None = None

    # Whether to refresh the detail grid when the master row data changes
    refresh_strategy: str | Var[str] | None = None


class LoadingCellRendererParams(AgGridParamsBase):
    """Parameters for loading cell renderer."""

    # Loading text to display
    loading_message: str | Var[str] | None = None

    # Custom loading renderer
    loading_renderer: JS_EXPRESSION | None = None

    # Loading icon or spinner component
    loading_icon: str | Var[str] | None = None


class FullWidthCellRendererParams(AgGridParamsBase):
    """Parameters for full width cell renderer."""

    # Custom full width renderer
    full_width_renderer: JS_EXPRESSION | None = None

    # Template for full width rows
    full_width_template: str | Var[str] | None = None

    # CSS class for full width rows
    full_width_css_class: str | Var[str] | None = None
