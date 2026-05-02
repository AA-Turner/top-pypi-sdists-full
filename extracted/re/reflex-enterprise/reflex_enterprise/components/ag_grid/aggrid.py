"""Reflex custom component AgGrid."""

import os
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Literal, Mapping, Sequence, TypedDict, cast

import reflex as rx
from reflex.components.el import Div
from reflex.event import EventSpec, no_args_event_spec
from reflex.utils.format import format_ref, to_camel_case, to_snake_case
from reflex.vars.base import LiteralVar, Var
from reflex.vars.function import ArgsFunctionOperation
from reflex.vars.object import ObjectVar

from reflex_enterprise.components.component import ComponentEnterprise
from reflex_enterprise.vars import JSAPIVar, PassthroughAPI

from .constants import (
    AG_GRID_LICENSE_KEY_ENV,
    AG_GRID_VERSION,
    BASE_PKG,
    CHARTS_ENTERPRISE_PKG,
    CHARTS_VERSION,
    COMMUNITY_PKG,
    DEFAULT_THEME,
    ENTERPRISE_PKG,
    THEMES,
)
from .datasource import Datasource, SSRMDatasource
from .resource import (
    AGAggregations,
    AGEditors,
    AGFilters,
    AGRenderers,
    AGStatusPanels,
    SideBarDef,
    StatusPanelDef,
    get_builtin_components,
    value_func_factory,
)
from .resources import ColumnDef, ColumnGroupDef
from .resources.params import (
    DetailCellRendererParams,
    FullWidthCellRendererParams,
    LoadingCellRendererParams,
)
from .utils import format_parameter_prop


class CellEventSpec(TypedDict):
    """Cell event specification."""

    type: str
    data: Mapping[str, Any]
    value: Any
    colDef: Mapping[str, Any]
    rowIndex: int
    rowPinned: Literal["top", "bottom"] | None


class RowEventSpec(TypedDict):
    """Row event specification."""

    type: str
    data: Mapping[str, Any]
    rowIndex: int
    rowPinned: Literal["top", "bottom"] | None


class Column(TypedDict):
    """Column definition."""

    colId: str


class ColumnEventSpec(TypedDict):
    """Column event specification."""

    type: str
    columnId: str
    column: dict


class RowSelectionEventSpec(TypedDict):
    """Row selection event specification."""

    type: str
    data: Mapping[str, Any]
    rowIndex: int


class CellValueChangedEventSpec(TypedDict):
    """Cell value changed event specification."""

    rowIndex: int
    field: str
    newValue: Any
    node_id: str
    colDef: dict
    node: dict


class SelectionChangeEventSpec(TypedDict):
    """Selection change event specification."""

    rows: list[dict]
    source: str
    type: str


def _on_cell_event_spec(event: ObjectVar[CellEventSpec]) -> tuple[Var[CellEventSpec]]:
    return (
        Var.create(
            {
                "type": event.type,
                "data": event.data,
                "value": event.value,
                "colDef": event.colDef,
                "rowIndex": event.rowIndex,
                "rowPinned": event.rowPinned,
            },
        ).to(CellEventSpec),
    )


def _on_row_event_spec(event: ObjectVar[RowEventSpec]) -> tuple[Var[RowEventSpec]]:
    return (
        Var.create(
            {
                "type": event.type,
                "data": event.data,
                "rowIndex": event.rowIndex,
                "rowPinned": event.rowPinned,
            }
        ).to(RowEventSpec),
    )


def _on_column_event_spec(
    event: ObjectVar[ColumnEventSpec],
) -> tuple[Var[ColumnEventSpec]]:
    return (
        Var.create(
            {
                "type": event.type,
                "columnId": event.column.to(Column).colId,
            }
        ).to(ColumnEventSpec),
    )


def _on_row_selected(event: ObjectVar[dict]) -> tuple[Var[RowSelectionEventSpec]]:
    return (
        Var.create(
            {
                "type": event.type,
                "data": event.data,
                "rowIndex": event.rowIndex,
            },
        ).to(RowSelectionEventSpec),
    )


def _on_cell_value_changed(
    event: ObjectVar[CellValueChangedEventSpec],
) -> tuple[Var[CellValueChangedEventSpec]]:
    return (
        Var.create(
            {
                "rowIndex": event.rowIndex,
                "field": event.colDef.field,
                "newValue": event.newValue,
                "node_id": event.node.id,
            }
        ).to(CellValueChangedEventSpec),
    )


class CellRange(TypedDict):
    """Cell range definition."""

    type: str
    startRow: int
    endRow: int
    columns: list[str]


class CellSelectionChangeEventSpec(TypedDict):
    """Cell selection change event specification."""

    range: list[CellRange]
    started: bool
    finished: bool


def _on_cell_selection_change_signature(
    event: ObjectVar[dict],
) -> tuple[Var[list[dict]], Var[bool], Var[bool]]:
    return (
        Var(
            f"""{event}.api.getCellRanges().map((range) => ({{
                startRow: range.startRow.rowIndex,
                endRow: range.endRow.rowIndex,
                columns: range.columns.map((col) => col.colId),
            }}))"""
        ).to(list[dict]),
        event.started,
        event.finished,
    )


def _on_selection_change_signature(
    event: ObjectVar[dict],
) -> tuple[Var[list[dict]], Var[str], Var[str]]:
    return (
        Var(f"{event}.api.getSelectedRows()").to(list[dict]),
        event.source.to(str),
        event.type,
    )


_size_columns_to_fit = ArgsFunctionOperation.create(
    args_names=("event",),
    return_expr=Var("event.api.sizeColumnsToFit()"),
    _var_type=rx.EventChain,
)


class AgGridAPIVar(JSAPIVar):
    """Wrapper for the AgGrid API object as represented in JS."""


@dataclass
class AgGridAPI(PassthroughAPI):
    """API for the AgGrid component."""

    ref: str

    @classmethod
    def create(cls, id: str) -> "AgGridAPI":
        """Create an instance of the AgGridAPI class.

        Args:
            id: The ID of the AgGrid component.

        Returns:
            An instance of the AgGridAPI class.
        """
        return cls(ref=format_ref(id))

    @property
    def _api(self) -> AgGridAPIVar:
        return AgGridAPIVar(f"refs['{self.ref}']?.current?.api")

    def set_grid_option(self, key: str, value: Var) -> EventSpec:
        """Set a grid option."""
        key, value = AgGrid.format_props(
            AgGrid._handle_camelcase_props({key: value})
        ).popitem()
        return self.setGridOption(to_camel_case(key), value)

    def select_rows_by_key(
        self, keys: list[str], node_path_key: str = "key"
    ) -> EventSpec:
        """Select rows by key."""
        keys_var = Var.create(keys)
        script = f"""let api = {self._api!s};
const selected_nodes = [];
let keys_set = new Set({keys_var!s});
api.forEachNode((node) => {{
    if (keys_set.has(node.{node_path_key})) {{
        selected_nodes.push(node);
    }}
}});
api.deselectAll();
api.setNodesSelected({{ nodes: selected_nodes, newValue: true }});
    """
        return rx.event.call_script(script)

    def select_all(self) -> EventSpec:
        """Select all rows."""
        return self.selectAll()

    def deselect_all(self) -> EventSpec:
        """Deselect all rows."""
        return self.deselectAll()

    def log_nodes(self, node_path_key: str | None = None) -> EventSpec:
        """Log the nodes in the grid."""
        node_path_key = "" if node_path_key is None else f".{node_path_key}"
        script = f"""
    let api = {self._api!s};
    console.log("Logging nodes");
    api.forEachNode(function (node) {{
        console.log(node{node_path_key!s});
    }});
    """
        return rx.event.call_script(script)


class AccessoriesOptions(ComponentEnterprise):
    """Accessories options for the AgGrid component."""

    # Specifies the status bar components to use in the status bar.
    status_bar: Var[StatusPanelDef | Mapping[str, Any]]

    # Specifies the side bar components to use in the side bar.
    side_bar: Var[str | Sequence[str] | bool | SideBarDef]

    # For customising the context menu.
    get_context_menu_items: Var[Callable]

    # Set to true to not show the context menu. Use if you don't want to use the default 'right click' context menu.
    suppress_context_menu: Var[bool]

    # When using suppressContextMenu, you can use the onCellContextMenu function to provide your own code to handle cell contextmenu events. This flag is useful to prevent the browser from showing its default context menu.
    prevent_default_on_context_menu: Var[bool]

    # Allows context menu to show, even when ^ Ctrl key is held down. Default: False
    allow_context_menu_with_control_key: Var[bool]

    # Control the display type for the column menu. Default: 'new'
    column_menu: Var[Literal["new", "legacy"]]

    # Only recommended for use if columnMenu = 'legacy'.
    suppress_menu_hide: Var[bool]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the required modules for the accessories options.

        Args:
            props: The component properties.

        Returns:
            The required modules.
        """
        return (
            {
                ENTERPRISE_PKG: {
                    "StatusBarModule",
                    "SideBarModule",
                    "ColumnsToolPanelModule",
                }
            }
            if any(key in props for key in cls.get_props())
            else {}
        )


class ClipboardOptions(ComponentEnterprise):
    """Clipboard options for the AgGrid component."""

    # Set to true to also include headers when copying to clipboard using ^ Ctrl+C clipboard. Default: False
    copy_headers_to_clipboard: Var[bool]

    # Set to true to also include group headers when copying to clipboard using ^ Ctrl+C clipboard. Default: False
    copy_group_headers_to_clipboard: Var[bool]

    # Specify the delimiter to use when copying to clipboard. Default: '\t'
    clipboard_delimiter: Var[str]

    # Set to true to block cut operations within the grid.
    suppress_cut_to_clipboard: Var[bool]

    # Set to true to work around a bug with Excel (Windows) that adds an extra empty line at the end of ranges copied to the clipboard.
    suppress_last_empty_line_on_paste: Var[bool]

    # Set to true to turn off paste operations within the grid.
    suppress_clipboard_paste: Var[bool]

    # Set to true to stop the grid trying to use the Clipboard API, if it is blocked, and immediately fallback to the workaround.
    suppress_clipboard_api: Var[bool]

    # Allows you to process cells for the clipboard. Handy if for example you have Date objects that need to have a particular format if importing into Excel.
    process_cell_for_clipboard: Var[Callable]

    # Allows you to process header values for the clipboard.
    process_header_for_clipboard: Var[Callable]

    # Allows you to process group header values for the clipboard.
    process_group_header_for_clipboard: Var[Callable]

    # Allows you to process cells from the clipboard. Handy if for example you have number fields and want to block non-numbers from getting into the grid.
    process_cell_from_clipboard: Var[Callable]

    # Allows you to get the data that would otherwise go to the clipboard. To be used when you want to control the 'copy to clipboard' operation yourself.
    send_to_clipboard: Var[Callable]

    # Allows complete control of the paste operation, including cancelling the operation (so nothing happens) or replacing the data with other data.
    process_data_from_clipboard: Var[Callable]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the required modules for the clipboard options.

        Args:
            props: The component properties.

        Returns:
            The required modules.
        """
        return (
            {ENTERPRISE_PKG: {"ClipboardModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )


class ColumnDefinitionsOptions(ComponentEnterprise):
    """Column definitions options for the AgGrid component."""

    # Column definitions.
    column_defs: Var[Sequence[Mapping[str, Any]] | Sequence[ColumnDef | ColumnGroupDef]]

    # Default column definition.
    default_col_def: Var[Mapping[str, Any] | None]

    # Default column group definition. [Initial]
    default_col_group_def: Var[Mapping[str, Any]]

    # Default column type definition.
    column_types: Var[Mapping[str, Any]]

    # A mapping of cell data types to their definitions. Cell data types can either override/update the pre-defined data types ('text', 'number', 'boolean', 'date', 'dateString' or 'object'), or can be custom data types.
    data_types_definitions: Var[Mapping[str, Any]]

    # Maintain column order after column_defs is updated. Default: False
    maintain_column_order: Var[bool]

    # Resets pivot column order when impacted by filters, data or configuration changes
    enable_strict_pivot_column_order: Var[bool]

    # If true, then dots in field names (e.g. 'address.firstLine') are not treated as deep references. Allows you to use dots in your field name if you prefer.
    suppress_field_dot_notation: Var[bool]

    @classmethod
    def _format_props(cls, props: dict[str, Any]) -> dict[str, Any]:
        # Prepare known components list once for all column definition processing
        known_components = list(get_builtin_components())
        if "components" in props:
            known_components.extend(props["components"].keys())

        if (column_defs := props.get("column_defs")) is not None:
            if not isinstance(column_defs, Var):
                props["column_defs"] = [
                    (
                        ColumnGroupDef.create(known_components, **col_def)
                        if "children" in col_def
                        else ColumnDef.create(known_components, **col_def)
                    )
                    if isinstance(col_def, dict)
                    else col_def
                    for col_def in column_defs
                ]
            else:
                props["column_defs"] = rx.vars.function.FunctionStringVar.create(
                    "formatColumnDefs"
                ).call(column_defs)

        if (
            default_col_def := props.get("default_col_def")
        ) is not None and not isinstance(default_col_def, Var):
            default_col_def = ColumnDef.create(
                known_components, **default_col_def
            ).dict()
            props["default_col_def"] = default_col_def

        if (column_types := props.get("column_types")) is not None and not isinstance(
            column_types, Var
        ):
            formatted_column_types = {}
            for col_type in column_types:
                col_def = ColumnDef.create(
                    known_components, **column_types[col_type]
                ).dict()
                formatted_column_types[col_type] = col_def
            props["column_types"] = formatted_column_types

        return props


class ColumnHeadersOptions(ComponentEnterprise):
    """Column headers options for the AgGrid component."""

    # The height in pixels for the row containing the column label header. If not specified, it uses the theme value of header-height.
    header_height: Var[int]

    # The height in pixels for the rows containing header column groups. If not specified, it uses header_height.
    group_header_height: Var[int]

    # The height in pixels for the row containing the floating filters. If not specified, it uses the theme value of header-height.
    floating_filters_height: Var[int]

    # The height in pixels for the row containing the columns when in pivot mode. If not specified, it uses header_height.
    pivot_header_height: Var[int]

    # The height in pixels for the row containing header column groups when in pivot mode. If not specified, it uses group_header_height.
    pivot_group_header_height: Var[int]


class ColumnMovingOptions(ComponentEnterprise):
    """Column moving options for the AgGrid component."""

    # Allow reordering and pinning columns by dragging columns from the Columns Tool Panel to the grid.
    allow_drag_from_columns_tool_panel: Var[bool]

    # Set to true to suppress column moving, i.e. to make the columns fixed position.
    suppress_movable_columns: Var[bool]

    # Set to true to suppress moving columns while dragging the Column Header. This option highlights the position where the column will be placed and it will only move it on mouse up.
    suppress_move_when_column_dragging: Var[bool]

    # If true, the ag-column-moving class is not added to the grid while columns are moving. In the default themes, this results in no animation when moving columns. Default: False
    suppress_column_move_animation: Var[bool]

    # If true, when you drag a column out of the grid (e.g. to the group zone) the column is not hidden.
    suppress_drag_leave_hides_columns: Var[bool]


class ColumnPinningOptions(ComponentEnterprise):
    """Column pinning options for the AgGrid component."""

    # Allows the user to process the columns being removed from the pinned section because the viewport is too small to accommodate them. Returns an array of columns to be removed from the pinned areas.
    process_unpinned_columns: Var[Callable]


class ColumnSizingOptions(ComponentEnterprise):
    """Column sizing options for the AgGrid component."""

    # Set to 'shift' to have shift-resize as the default resize operation (same as user holding down ⇧ Shift while resizing).
    col_resize_default: Var[str]

    # Auto-size the columns when the grid is loaded. Can size to fit the grid width, fit a provided width, or fit the cell contents.
    auto_size_strategy: Var[dict]

    # Suppresses auto-sizing columns for columns. In other words, double clicking a column's header's edge will not auto-size.
    suppress_auto_size: Var[bool]

    # Number of pixels to add to a column width after the auto-sizing calculation. Set this if you want to add extra room to accommodate (for example) sort icons, or some other dynamic nature of the header.
    auto_size_padding: Var[int]

    # Set this to True to skip the headerName when autoSize is called by default.
    skip_header_on_auto_size: Var[bool]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the required modules for the column sizing options.

        Args:
            props: The component properties.

        Returns:
            The required modules.
        """
        return (
            {COMMUNITY_PKG: {"ColumnAutoSizeModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )


class ComponentsOptions(ComponentEnterprise):
    """Components options for the AgGrid component."""

    # A map of name to components [Initial]
    components: Var[Mapping[str, Any]]


class EditingOptions(ComponentEnterprise):
    """Editing options for the AgGrid component."""

    # Set to 'fullRow' to enable Full Row Editing. Otherwise leave blank to edit one cell at a time.
    edit_type: Var[str]

    # Set to True to enable single click editing. Default: False
    single_click_edit: Var[bool]

    # Set to True to suppress click editing. Default: False
    suppress_click_edit: Var[bool]

    # Set this to True to stop cell editing when grid loses focus. The default is that the grid stays editing until focus goes onto another cell.
    stop_edit_when_cell_loses_focus: Var[bool]

    # Set to true along with enter_navigate_vertically_after_edit to have Excel-style behaviour for the ↵ Enter key, i.e. pressing the ↵ Enter key will move down to the cell beneath. Default: false
    enter_navigate_vertically: Var[bool]

    # Set to true along with enter_navigate_vertically to have Excel-style behaviour for the ↵ Enter key, i.e. pressing the ↵ Enter key will move down to the cell beneath. Default: false
    enter_navigate_vertically_after_edit: Var[bool]

    # Forces Cell Editing to start when backspace is pressed. This is only relevant for MacOS users.
    enable_cell_editing_on_backspace: Var[bool]

    # Set to true to enable Undo / Redo while editing. [Initial]
    undo_redo_cell_editing: Var[bool]

    # Set the size of the undo / redo stack.
    undo_redo_cell_editing_limit: Var[int]

    # Set to true to stop the grid updating data after Edit, Clipboard and Fill Handle operations. When this is set, it is intended the application will update the data, eg in an external immutable store, and then pass the new dataset to the grid.
    read_only_edit: Var[bool]


class ExportOptions(ComponentEnterprise):
    """Export options for the AgGrid component."""

    # A default configuration object used to export to CSV.
    default_csv_export_params: Var[Mapping[str, Any]]

    # Prevents the user from exporting the grid to CSV.
    suppress_csv_export: Var[bool]

    # A default configuration object used to export to Excel.
    default_excel_export_params: Var[Mapping[str, Any]]

    # Prevents the user from exporting the grid to Excel.
    suppress_excel_export: Var[bool]

    # A list of Excel styles to be used when exporting to Excel with styles. [Initial]
    excel_styles: Var[Sequence[Mapping[str, Any]]]


class FilteringOptions(ComponentEnterprise):
    """Filtering options for the AgGrid component."""

    # Rows are filtered using this text as a Quick Filter. Only supported for Client-Side Row Model.
    quick_filter_text: Var[str]

    # Set to true to turn on the Quick Filter cache, used to improve performance when using the Quick Filter.
    cache_quick_filter: Var[bool]

    # Hidden columns are excluded from the Quick Filter by default. To include hidden columns, set to true.
    include_hidden_columns_in_quick_filter: Var[bool]

    # Changes how the Quick Filter splits the Quick Filter text into search terms.
    quick_filter_parser: Var[Callable]

    # Changes the matching logic for whether a row passes the Quick Filter.
    quick_filter_matcher: Var[Callable]

    # When pivoting, Quick Filter is only applied on the pivoted data (or aggregated data if groupAggFiltering = true). Set to true to apply Quick Filter before pivoting (/aggregating) instead.
    apply_quick_filter_before_pivot_or_agg: Var[bool]

    # Grid calls this method to know if an external filter is present.
    is_external_filter_present: Var[Callable]

    # Should return true if external filter passes, otherwise false.
    does_external_filter_pass: Var[Callable]

    # Set to true to override the default tree data filtering behaviour to instead exclude child nodes from filter results.
    exclude_children_when_tree_data_filtering: Var[bool]

    # When using AG Grid Enterprise, the Set Filter is used by default when filter: true is set on column definitions. Set to true to prevent this and instead use the Text Filter, Number Filter or Date Filter based on the cell data type, the same as when using AG Grid Community. [Initial]
    suppress_set_filter_by_default: Var[bool]

    # Set to true to enable the Advanced Filter.
    enable_advanced_filter: Var[bool]

    # Hidden columns are excluded from the Advanced Filter by default. To include hidden columns, set to true.
    include_hidden_columns_in_advanced_filter: Var[bool]

    # DOM element to use as the parent for the Advanced Filter to allow it to appear outside of the grid. Set to null or undefined to appear inside the grid.
    advanced_filter_parent: Var[Any]

    # Customise the parameters passed to the Advanced Filter Builder.
    advanced_filter_built_params: Var[Mapping[str, Any]]

    # Allows rows to always be displayed, even if they don't match the applied filtering. Return true for the provided row to always be displayed. Only works with the Client-Side Row Model.
    always_pass_filter: Var[Callable]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the required modules for the advanced filter options.

        Args:
            props: The component properties.

        Returns:
            The required modules.
        """
        return (
            {ENTERPRISE_PKG: {"AdvancedFilterModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )


class IntegratedChartsOptions(ComponentEnterprise):
    """Charts options for the AgGrid component."""

    # Set to true to Enable Charts.
    enable_charts: Var[bool]

    # Callback to be used to customise the chart toolbar items.
    get_chart_toolbar_items: Var[Callable]

    # Callback to enable displaying the chart in an alternative chart container.
    create_chart_container: Var[Callable]

    # The list of chart themes that a user can choose from in the chart panel.
    chart_themes: Var[Sequence[str]]

    # A map containing custom chart themes.
    custom_chart_themes: Var[Mapping[str, Any]]

    # Chart theme overrides applied to all themes.
    chart_theme_overrides: Var[Mapping[str, Any]]

    # Allows customisation of the Chart Tool Panels, such as changing the tool panels visibility and order, as well as choosing which charts should be displayed in the chart panel.
    chart_tool_panel_defs: Var[Mapping[str, Any]]

    # Get chart menu items. Only applies when using AG Charts Enterprise.
    chart_menu_items: Var[Callable]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the required modules for the integrated charts options.

        Args:
            props: The component properties.

        Returns:
            The required modules.
        """
        return {}

    def add_imports(self):
        """Add the required imports for the integrated charts options."""
        if self.enable_charts is not None:
            return {
                ENTERPRISE_PKG: "IntegratedChartsModule",
                CHARTS_ENTERPRISE_PKG: "AgChartsEnterpriseModule",
            }
        else:
            return {}

    def add_custom_code(self) -> list[str]:
        """Add custom code for the integrated charts options."""
        if self.enable_charts is not None:
            return [
                "ModuleRegistry.registerModules([IntegratedChartsModule.with(AgChartsEnterpriseModule)]);"
            ]
        else:
            return []


class KeyboardNavigationOptions(ComponentEnterprise):
    """Keyboard navigation options for the AgGrid component."""

    # Allows overriding the element that will be focused when the grid receives focus from outside elements (tabbing into the grid). Returns: True if this function should override the grid's default behavior, False to allow the grid's default behavior.
    focus_grid_inner_elements: Var[Callable]

    # Allows overriding the default behaviour for when user hits navigation (arrow) key when a header is focused. Return the next Header position to navigate to or null to stay on current header.
    navigate_to_next_header: Var[Callable]

    # Allows overriding the default behaviour for when user hits Tab key when a header is focused. Return the next header position to navigate to, true to stay on the current header, or false to let the browser handle the tab behaviour.
    tab_to_next_header: Var[Callable]

    # Allows overriding the default behaviour for when user hits navigation (arrow) key when a cell is focused. Return the next Cell position to navigate to or null to stay on current cell.
    navigate_to_next_cell: Var[Callable]

    # Allows overriding the default behaviour for when user hits Tab key when a cell is focused. Return the next cell position to navigate to, true to stay on the current cell, or false to let the browser handle the tab behaviour.
    tab_to_next_cell: Var[Callable]


class LoadingCellOptions(ComponentEnterprise):
    """Loading cell options for the AgGrid component."""

    # Provide your own loading cell renderer to use when data is loading via a DataSource.
    loading_cell_renderer: Var[Any]

    # Params to be passed to the loadingCellRenderer component.
    loading_cell_renderer_params: Var[LoadingCellRendererParams | Mapping[str, Any]]

    # Callback to select which loading cell renderer to be used when data is loading via a DataSource.
    loading_cell_renderer_selector: Var[Callable]

    @classmethod
    def _format_props(cls, props: dict[str, Any]) -> dict[str, Any]:
        """Format props for loading cell options."""
        format_parameter_prop(props, LoadingCellRendererParams)
        return props


class LocalizationOptions(ComponentEnterprise):
    """Localization options for the AgGrid component."""

    # A map of key->value pairs for localising text within the grid.
    locale_text: Var[Mapping[str, str]]

    # A callback for localising text within the grid.
    get_locale_text: Var[Callable]


class MasterDetailOptions(ComponentEnterprise):
    """Master Detail options for the AgGrid component."""

    # Set to true to enable Master Detail.
    master_detail: Var[bool]

    # Callback to be used with Master Detail to determine if a row should be a master row. If false is returned no detail row will exist for this row.
    is_row_master: Var[Callable]

    # Provide a custom detailCellRenderer to use when a master row is expanded.
    detail_cell_renderer: Var[Any]

    # Specifies the params to be used by the Detail Cell Renderer. Can also be a function that provides the params to enable dynamic definitions of the params.
    detail_cell_renderer_params: Var[
        DetailCellRendererParams | Mapping[str, Any] | Callable
    ]

    # Set fixed height in pixels for each detail row.
    detail_row_height: Var[int]

    # Set to true to have the detail grid dynamically change it's height to fit it's rows.
    detail_row_auto_height: Var[bool]

    # Set to true to have the Full Width Rows embedded in grid's main container so they can be scrolled horizontally.
    embed_full_width_rows: Var[bool]

    # Set to true to keep detail rows for when they are displayed again.
    keep_detail_rows: Var[bool]

    # Sets the number of details rows to keep.
    keep_detail_rows_count: Var[int]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the required modules for the master detail options.

        Args:
            props: The component properties.

        Returns:
            The required modules.
        """
        return (
            {ENTERPRISE_PKG: {"MasterDetailModule", "RowGroupingModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )

    @classmethod
    def _format_props(cls, props: dict[str, Any]) -> dict[str, Any]:
        """Format props for master detail options."""
        format_parameter_prop(props, DetailCellRendererParams)
        return props


class MiscellaneousOptions(ComponentEnterprise):
    """Miscellaneous options for the AgGrid component."""

    # Initial state for the grid. Only read once on initialization. Can be used in conjunction with api.getState() to save and restore grid state.
    initial_state: Var[Any]

    # A list of grids to treat as Aligned Grids. Provide a list if the grids / apis already exist or return via a callback to allow the aligned grids to be retrieved asynchronously. If grids are aligned then the columns and horizontal scrolling will be kept in sync.
    aligned_grids: Var[Sequence[Any] | Callable]

    # Provides a context object that is provided to different callbacks the grid uses. Used for passing additional information to the callbacks used by your application.
    context: Var[Mapping[str, Any]]

    # Change this value to set the tabIndex order of the Grid within your application.
    tab_index: Var[int]

    # The number of rows rendered outside the viewable area the grid renders. Having a buffer means the grid will have rows ready to show as the user slowly scrolls vertically.
    row_buffer: Var[int]

    # Configure the Row Numbers Feature.
    row_number: Var[bool | Mapping[str, Any]]

    # Set to true to turn on the value cache.
    value_cache: Var[bool]

    # Set to true to configure the value cache to not expire after data updates.
    value_cache_never_expire: Var[bool]

    # Set to true to allow cell expressions.
    enable_cell_expressions: Var[bool]

    # Allows overriding what document is used. Currently used by Drag and Drop (may extend to other places in the future). Use this when you want the grid to use a different document than the one available on the global scope. This can happen if docking out components (something which Electron supports)
    get_document: Var[Callable]

    # Disables touch support (but does not remove the browser's efforts to simulate mouse events on touch).
    suppress_touch: Var[bool]

    # Provide a custom drag and drop image component.
    drag_and_drop_image_component: Var[Any]

    # Set to true to not set focus back on the grid after a refresh. This can avoid issues where you want to keep the focus on another part of the browser.
    suppress_focus_after_refresh: Var[bool]

    # Disables change detection.
    suppress_change_detection: Var[bool]

    # Set this to true to enable debug information from the grid and related components. Will result in additional logging being output, but very useful when investigating problems.
    debug: Var[bool]

    @classmethod
    def _format_props(cls, props: dict[str, Any]) -> dict[str, Any]:
        def _get_ref(id: str) -> str:
            """Get the reference for the given ID."""
            return f"refs['{format_ref(id)}']"

        if (aligned_grids := props.get("aligned_grids")) is not None and isinstance(
            aligned_grids, list
        ):
            props["aligned_grids"] = ArgsFunctionOperation.create(
                (),
                Var(f"[{', '.join(_get_ref(_id) for _id in aligned_grids)}]"),
            )
        return props


class OverlayOptions(ComponentEnterprise):
    """Overlay options for the AgGrid component."""

    # Show or hide the loading overlay.
    loading: Var[bool]

    # Provide a HTML string to override the default loading overlay. Supports non-empty plain text or HTML with a single root element.
    overlay_loading_template: Var[str]

    # Provide a custom loading overlay component.
    loading_overlay_component: Var[Any]

    # Customise the parameters provided to the loading overlay component.
    loading_overlay_component_params: Var[Mapping[str, Any]]

    # Set to true to prevent the no-rows overlay being shown when there is no row data.
    suppress_no_rows_overlay: Var[bool]

    # Provide a HTML string to override the default no-rows overlay. Supports non-empty plain text or HTML with a single root element.
    overlay_no_rows_template: Var[str]

    # Provide a custom no rows overlay component.
    no_rows_overlay_component: Var[Any]

    # Customise the parameters provided to the no rows overlay component.
    no_rows_overlay_component_params: Var[Mapping[str, Any]]


class PaginationOptions(ComponentEnterprise):
    """Pagination options for the AgGrid component."""

    # Set whether pagination is enabled.
    pagination: Var[bool]

    # How many rows to load per page. If paginationAutoPageSize is specified, this property is ignored.
    pagination_page_size: Var[int]

    # Determines if the page size selector is shown in the pagination panel or not. Set to an array of values to show the page size selector with custom list of possible page sizes. Set to true to show the page size selector with the default page sizes [20, 50, 100]. Set to false to hide the page size selector.
    pagination_page_size_selector: Var[bool | Sequence[int]]

    # Allows user to format the numbers in the pagination panel, i.e. 'row count' and 'page number' labels. This is for pagination panel only, to format numbers inside the grid's cells (i.e. your data), then use valueFormatter in the column definitions.
    pagination_number_formatter: Var[Callable]

    # Set to true so that the number of rows to load per page is automatically adjusted by the grid so each page shows enough rows to just fill the area designated for the grid. If false, paginationPageSize is used.
    pagination_auto_page_size: Var[bool]

    # Set to true to have pages split children of groups when using Row Grouping or detail rows with Master Detail.
    paginate_child_rows: Var[bool]

    # If true, the default grid controls for navigation are hidden. This is useful if pagination=true and you want to provide your own pagination controls. Otherwise, when pagination=true the grid automatically shows the necessary controls at the bottom so that the user can navigate through the different pages.
    suppress_pagination_panel: Var[bool]


class RenderingOptions(ComponentEnterprise):
    """Rendering options for the AgGrid component."""

    # Set to false to disable Row Animation which is enabled by default.
    animate_rows: Var[bool]

    # Sets the duration in milliseconds of how long a cell should remain in its "flashed" state. If 0, the cell will not flash.
    cell_flash_duration: Var[int]

    # Sets the duration in milliseconds of how long the "flashed" state animation takes to fade away after the timer set by cellFlashDuration has completed.
    cell_fade_duration: Var[int]

    # Set to true to have cells flash after data changes even when the change is due to filtering.
    allow_show_change_after_filter: Var[bool]

    # Switch between layout options. See Printing and Auto Height. Default: normal
    dom_layout: Var[Literal["normal", "autoHeight", "print"]]

    # When true, the order of rows and columns in the DOM are consistent with what is on screen. Disables row animations.
    ensure_dom_order: Var[bool]

    # Return a business key for the node. If implemented, each row in the DOM will have an attribute row-business-key='abc' where abc is what you return as the business key. This is useful for automated testing, as it provides a way for your tool to identify rows based on unique business keys.
    get_business_key_for_node: Var[Callable]

    # Provide a custom gridId for this instance of the grid. Value will be set on the root DOM node using the attribute grid-id as well as being accessible via the gridApi.getGridId() method. [Initial]
    grid_id: Var[str]

    # Callback fired after the row is rendered into the DOM. Should not be used to initiate side effects.
    process_row_post_create: Var[Callable]

    # Set to true to operate the grid in RTL (Right to Left) mode.
    enable_rtl: Var[bool]

    # Set to true so that the grid doesn't virtualise the columns. For example, if you have 100 columns, but only 10 visible due to scrolling, all 100 will always be rendered.
    suppress_column_virtualisation: Var[bool]

    # Set to true so that the grid doesn't virtualise the rows. For example, if you have 100 rows, but only 10 visible due to scrolling, all 100 will always be rendered.
    suppress_row_virtualisation: Var[bool]

    # By default the grid has a limit of rendering a maximum of 500 rows at once (remember the grid only renders rows you can see, so unless your display shows more than 500 rows without vertically scrolling this will never be an issue).
    suppress_max_rendered_row_restrictions: Var[bool]

    # When true, enables the cell span feature allowing for the use of the colDef.spanRows property.
    enable_cell_span: Var[bool]


class RowAggregationOptions(ComponentEnterprise):
    """Row aggregation options for the AgGrid component."""

    # A map of 'function name' to 'function' for custom aggregation functions.
    agg_funcs: Var[Mapping[str, Any]]

    # When provided, an extra row group total row will be inserted into row groups at the specified position, to display when the group is expanded. This row will contain the aggregate values for the group. If a callback function is provided, it can be used to selectively determine which groups will have a total row added.
    group_total_row: Var[Literal["top", "bottom"] | Callable]

    # When provided, an extra grand total row will be inserted into the grid at the specified position. This row displays the aggregate totals of all rows in the grid.
    grand_total_row: Var[Literal["top", "bottom"]]

    # When true, column headers won't include the aggFunc name, e.g. 'sum(Bank Balance)' will just be 'Bank Balance'.
    suppress_agg_func_in_header: Var[bool]

    # When using change detection, only the updated column will be re-aggregated.
    aggregate_only_changed_columns: Var[bool]

    # Set to true so that aggregations are not impacted by filtering.
    suppress_agg_filtered_only: Var[bool]

    # Set to determine whether filters should be applied on aggregated group values.
    group_agg_filtering: Var[bool]

    # If true, and showing footer, aggregate data will always be displayed at both the header and footer levels. This stops the possibly undesirable behaviour of the header details 'jumping' to the footer on expand.
    group_suppress_blank_header: Var[bool]

    # Suppress the sticky behaviour of the total rows, can be suppressed individually by passing 'grand' or 'group'.
    suppress_sticky_total_row: Var[Literal["grand", "group"] | bool]

    # When using aggregations, the grid will always calculate the root level aggregation value.
    always_aggregate_at_root_level: Var[bool]

    # Callback to use when you need access to more then the current column for aggregation.
    get_group_row_agg: Var[Callable]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the modules required for row aggregations options."""
        return (
            {ENTERPRISE_PKG: {"RowGroupingModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )


class RowDragOptions(ComponentEnterprise):
    """Row drag options for the AgGrid component."""

    # Set to true to enable Managed Row Dragging.
    row_drag_managed: Var[bool]

    # Set to true to enable clicking and dragging anywhere on the row without the need for a drag handle.
    row_drag_entire_row: Var[bool]

    # Set to true to enable dragging multiple rows at the same time.
    row_drag_multi_row: Var[bool]

    # Set to true to suppress row dragging.
    suppress_row_drag: Var[bool]

    # Set to true to suppress moving rows while dragging the rowDrag waffle. This option highlights the position where the row will be placed and it will only move the row on mouse up.
    suppress_move_when_row_dragging: Var[bool]

    # A callback that should return a string to be displayed by the rowDragComp while dragging a row. If this callback is not set, the current cell value will be used. If the rowDragText callback is set in the ColDef it will take precedence over this, except when rowDragEntireRow=true.
    row_drag_text: Var[Callable]


class RowFullWidthOptions(ComponentEnterprise):
    """Row full width options for the AgGrid component."""

    # Provide your own cell renderer component to use for full width rows.
    full_width_cell_renderer: Var[Any]

    # Customise the parameters provided to the fullWidthCellRenderer component.
    full_width_cell_renderer_params: Var[
        FullWidthCellRendererParams | Mapping[str, Any]
    ]

    @classmethod
    def _format_props(cls, props: dict[str, Any]) -> dict[str, Any]:
        """Format props for row full width options."""
        format_parameter_prop(props, FullWidthCellRendererParams)
        return props


class RowGroupingOptions(ComponentEnterprise):
    """Row grouping options for the AgGrid component."""

    # Specifies how the results of row grouping should be displayed. The options are:
    #   'singleColumn': single group column automatically added by the grid.
    #   'multipleColumns': a group column per row group is added automatically.
    #   'groupRows': group rows are automatically added instead of group columns.
    #   'custom': informs the grid that group columns will be provided.
    group_display_type: Var[
        Literal["singleColumn", "multipleColumns", "groupRows", "custom"]
    ]

    # Allows specifying the group 'auto column' if you are not happy with the default. If grouping, this column definition is included as the first column in the grid. If not grouping, this column is not included.
    auto_group_column_def: Var[Any]

    # Provide the Cell Renderer to use when groupDisplayType = 'groupRows'.
    group_row_renderer: Var[Any]

    # Customise the parameters provided to the groupRowRenderer component.
    group_row_renderer_params: Var[Mapping[str, Any]]

    # Shows the open group in the group column for non-group rows.
    show_opened_group: Var[bool]

    # Set to true to hide parents that are open. When used with multiple columns for showing groups, it can give a more pleasing user experience.
    group_hide_open_parents: Var[bool]

    # Enable to display the child row in place of the group row when the group only has a single child.
    group_hide_parent_of_single_child: Var[bool | Literal["leafGroupsOnly"]]

    # Allows default sorting of groups.
    initial_group_order_comparator: Var[Callable]

    # Set to true to prevent the grid from creating a '(Blanks)' group for nodes which do not belong to a group, and display the unbalanced nodes alongside group nodes.
    group_allow_unbalanced: Var[bool]

    # When true, preserves the current group order when sorting on non-group columns.
    group_maintain_order: Var[bool]

    # If grouping, set to the number of levels to expand by default, e.g. 0 for none, 1 for first level only, etc. Set to -1 to expand everything.
    group_default_expanded: Var[int]

    # (Client-side Row Model only) Allows groups to be open by default.
    is_group_open_by_default: Var[Callable]

    # Set to true prevent Group Rows from sticking to the top of the grid.
    suppress_group_stickiness: Var[bool]

    # When to show the 'row group panel' (where you drag rows to group) at the top.
    row_group_panel_show: Var[str]

    # Set to true to suppress sort indicators and actions from the row group panel.
    row_group_panel_suppress_sort: Var[bool]

    # If grouping, locks the group settings of a number of columns, e.g. 0 for no group locking. 1 for first group column locked, -1 for all group columns locked.
    group_lock_group_columns: Var[int]

    # By default, dragging a column out of the grid, i.e. to the Row Group Panel, it will be hidden in the grid. This property prevents the column becoming hidden in the grid. Default: false
    suppress_drag_leave_hides_columns: Var[bool]

    # Enable to prevent column visibility changing when grouped columns are changed.
    suppress_group_changes_column_visibility: Var[bool]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Return the columns required for the row pivoting options."""
        return (
            {
                ENTERPRISE_PKG: {
                    "RowGroupingModule",
                }
            }
            if any(key in props for key in cls.get_props())
            else {}
        )


class RowPinningOptions(ComponentEnterprise):
    """Row pinning options for the AgGrid component."""

    # Data to be displayed as pinned top rows in the grid.
    pinned_row_top_data: Var[Sequence[Mapping[str, Any]]]

    # Data to be displayed as pinned bottom rows in the grid.
    pinned_row_bottom_data: Var[Sequence[Mapping[str, Any]]]


class RowPivotingOptions(ComponentEnterprise):
    """Row pivoting options for the AgGrid component."""

    # Set to true to enable pivot mode.
    pivot_mode: Var[bool]

    # When to show the 'pivot panel' (where you drag rows to pivot) at the top. Note that the pivot panel will never show if pivotMode is off.
    pivot_panel_show: Var[str]

    # If pivoting, set to the number of column group levels to expand by default, e.g. 0 for none, 1 for first level only, etc. Set to -1 to expand everything.
    pivot_default_expanded: Var[int]

    # When set and the grid is in pivot mode, automatically calculated totals will appear for each value column in the position specified.
    pivot_row_totals: Var[Literal["before", "after"]]

    # If true, the grid will not swap in the grouping column when pivoting. Useful if pivoting using Server Side Row Model or Viewport Row Model and you want full control of all columns including the group column.
    pivot_suppress_auto_column: Var[bool]

    # The maximum number of generated columns before the grid halts execution. Upon reaching this number, the grid halts generation of columns and triggers a pivotMaxColumnsExceeded event. -1 for no limit.
    pivot_max_generated_columns: Var[int]

    # Callback for the mutation of the generated pivot result column definitions
    process_pivot_result_col_def: Var[Callable]

    # Callback for the mutation of the generated pivot result column group definitions
    process_pivot_result_col_group_def: Var[Callable]

    # When enabled, pivot column groups will appear 'fixed', without the ability to expand and collapse the column groups.
    suppress_expandable_pivot_groups: Var[bool]

    # If true, then row group, pivot and value aggregation will be read-only from the GUI. The grid will display what values are used for each, but will not allow the user to change the selection.
    functions_read_only: Var[bool]

    # Set to true to omit the value Column header when there is only a single value column.
    remove_pivot_header_row_when_single_value_column: Var[bool]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Return the columns required for the row pivoting options."""
        return (
            {
                ENTERPRISE_PKG: {
                    "PivotModule",
                    "RowGroupingModule",
                    "RowGroupingPanelModule",
                    "TreeDataModule",
                }
            }
            if any(key in props for key in cls.get_props())
            else {}
        )


class RowModelOptions(ComponentEnterprise):
    """Row model options for the AgGrid component."""

    # Sets the row model type.
    row_model_type: Var[str]

    # Provide a pure function that returns a string ID to uniquely identify a given row. This enables the grid to work optimally with data changes and updates.
    get_row_id: Var[Callable]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Return the modules required for the row model options."""
        if (row_model_type := props.get("row_model_type")) and not isinstance(
            row_model_type, Var
        ):
            match row_model_type:
                case "clientSide":
                    return {COMMUNITY_PKG: {"ClientSideRowModelModule"}}
                case "infinite":
                    return {COMMUNITY_PKG: {"InfiniteRowModelModule"}}
                case "viewport":
                    return {COMMUNITY_PKG: {"ViewportRowModelModule"}}
                case "serverSide":
                    return {ENTERPRISE_PKG: {"ServerSideRowModelModule"}}
                case _:
                    pass
        return {}


class RowModelClientSideOptions(ComponentEnterprise):
    """Row model client-side options for the AgGrid component."""

    # Set the data to be displayed as rows in the grid.
    row_data: Var[Sequence[Mapping[str, Any]]]

    # When enabled, getRowId() callback is implemented and new Row Data is set, the grid will disregard all previous rows and treat the new Row Data as new data. As a consequence, all Row State (eg selection, rendered rows) will be reset.
    reset_row_data_on_update: Var[bool]

    # How many milliseconds to wait before executing a batch of async transactions.
    async_transaction_wait_millis: Var[int]

    # Prevents Transactions changing sort, filter, group or pivot state when transaction only contains updates. Default: false
    suppress_model_update_after_update_transaction: Var[bool]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Return the modules required for the client-side row model."""
        return (
            {COMMUNITY_PKG: {"ClientSideRowModelModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )


class RowModelInfiniteOptions(ComponentEnterprise):
    """Row model infinite options for the AgGrid component."""

    # Provide the datasource for infinite scrolling.
    datasource: Var[Datasource]

    # How many extra blank rows to display to the user at the end of the dataset, which sets the vertical scroll and then allows the grid to request viewing more rows of data.
    cache_overflow_size: Var[int]

    # How many requests to hit the server with concurrently. If the max is reached, requests are queued. Set to -1 for no maximum restriction on requests.
    max_concurrent_datasource_requests: Var[int]

    # How many rows for each block in the store, i.e. how many rows returned from the server at a time.
    cache_block_size: Var[int]

    # How many blocks to keep in the store. Default is no limit, so every requested block is kept. Use this if you have memory concerns, and blocks that were least recently viewed will be purged when the limit is hit. The grid will additionally make sure it has all the blocks needed to display what is currently visible, in case this property is set to a low value.
    max_blocks_in_cache: Var[int]

    # How many extra blank rows to display to the user at the end of the dataset, which sets the vertical scroll and then allows the grid to request viewing more rows of data.
    infinite_initial_row_count: Var[int]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Return the modules required for the infinite row model."""
        return (
            {COMMUNITY_PKG: {"InfiniteRowModelModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )


class RowModelServiceSideOptions(ComponentEnterprise):
    """Row model server-side options for the AgGrid component."""

    # Provide the serverSideDatasource for server side row model.
    server_side_datasource: Var[SSRMDatasource]

    # How many milliseconds to wait before loading a block. Useful when scrolling over many blocks, as it prevents blocks loading until scrolling has settled.
    block_load_debounce_millis: Var[int]

    # When true, the Server-side Row Model will not use a full width loading renderer, instead using the colDef loadingCellRenderer if present.
    suppress_server_side_full_width_loading_row: Var[bool]

    # When enabled, closing group rows will remove children of that row. Next time the row is opened, child rows will be read from the datasource again. This property only applies when there is Row Grouping. Default: false
    purge_closed_row_nodes: Var[bool]

    # Used to split pivot field strings for generating pivot result columns when pivotResultFields is provided as part of a getRows success.
    server_side_pivot_result_field_separator: Var[str]

    # When enabled, always refreshes top level groups regardless of which column was sorted. This property only applies when there is Row Grouping & sorting is handled on the server.
    server_side_sort_all_levels: Var[bool]

    # When enabled, sorts fully loaded groups in the browser instead of requesting from the server.
    server_side_enable_client_side_sort: Var[bool]

    # When enabled, only refresh groups directly impacted by a filter. This property only applies when there is Row Grouping & filtering is handled on the server.
    server_side_only_refresh_filtered_groups: Var[bool]

    # Set how many loading rows to display to the user for the root level group.
    server_side_initial_row_count: Var[int]

    # Allows setting the child count for a group row.
    get_child_count: Var[Callable]

    # Allows providing different params for different levels of grouping.
    get_server_side_group_level_params: Var[Callable]

    # Allows groups to be open by default.
    is_server_side_group_open_by_default: Var[Callable]

    # Allows cancelling transactions.
    is_apply_server_side_transaction: Var[Callable]

    # SSRM Tree Data: Allows specifying which rows are expandable.
    is_server_side_group: Var[Callable]

    # SSRM Tree Data: Allows specifying group keys.
    get_server_side_group_key: Var[Callable]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Return the modules required for the server-side row model."""
        return (
            {ENTERPRISE_PKG: {"ServerSideRowModelModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )


class RowModelViewportOptions(ComponentEnterprise):
    """Row model viewport options for the AgGrid component."""

    # To use the viewport row model you need to provide the grid with a viewportDatasource.
    viewport_datasource: Var[Any]

    # When using viewport row model, sets the page size for the viewport.
    viewport_row_model_page_size: Var[int]

    # When using viewport row model, sets the buffer size for the viewport.
    viewport_row_model_buffer_size: Var[int]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Return the modules required for the viewport row model."""
        return (
            {ENTERPRISE_PKG: {"ViewportRowModelModule"}}
            if any(key in props for key in cls.get_props())
            else {}
        )


class ScrollingOptions(ComponentEnterprise):
    """Scrolling options for the AgGrid component."""

    # Set to true to always show the horizontal scrollbar. Windows and Mac OS both have settings to control scrollbar visibility. Depending on your browser, you may need to adjust the scrollbar settings in your OS to have this property take effect.
    always_show_horizontal_scroll: Var[bool]

    # Set to true to always show the vertical scrollbar. Windows and Mac OS both have settings to control scrollbar visibility. Depending on your browser, you may need to adjust the scrollbar settings in your OS to have this property take effect.
    always_show_vertical_scroll: Var[bool]

    # Set to true to debounce the vertical scrollbar. Can provide smoother scrolling on slow machines.
    debounce_vertical_scrollbar: Var[bool]

    # Set to true to never show the horizontal scroll. This is useful if the grid is aligned with another grid and will scroll when the other grid scrolls. (Should not be used in combination with alwaysShowHorizontalScroll.)
    suppress_horizontal_scroll: Var[bool]

    # When true, the grid will not scroll to the top when new row data is provided. Use this if you don't want the default behaviour of scrolling to the top every time you load new data.
    suppress_scroll_on_new_data: Var[bool]

    # When true, the grid will not allow mousewheel / touchpad scroll when popup elements are present.
    suppress_scroll_when_popup_are_open: Var[bool]

    # When true, the grid will not use animation frames when drawing rows while scrolling. Use this if the grid is working fast enough that you don't need animation frames and you don't want the grid to flicker.
    suppress_animation_frame: Var[bool]

    # If true, middle clicks will result in click events for cells and rows. Otherwise the browser will use middle click to scroll the grid.
    suppress_middle_click_scroll: Var[bool]

    # If true, mouse wheel events will be passed to the browser. Useful if your grid has no vertical scrolls and you want the mouse to scroll the browser page.
    suppress_prevent_default_on_mouse_wheel: Var[bool]

    # Tell the grid how wide in pixels the scrollbar is, which is used in grid width calculations. Set only if using non-standard browser-provided scrollbars, so the grid can use the non-standard size in its calculations.
    scrollbar_width: Var[int]


class SelectionOptions(ComponentEnterprise):
    """Selection options for the AgGrid component."""

    # Configure cell selection
    cell_selection: Var[bool | dict]

    # Use the RowSelectionOptions object to configure row selection. The string values 'single' and 'multiple' are deprecated.
    row_selection: Var[str | dict]

    # Configure the selection column, used for displaying checkboxes. Note that due to the nature of this column, this type is a subset of ColDef, which does not support several normal column features such as editing, pivoting and grouping.
    selection_column_def: Var[Mapping[str, Any]]

    # If true, cells won't be focusable. This means keyboard navigation will be disabled for grid cells, but remain enabled in other elements of the grid such as column headers, floating filters, tool panels.
    suppress_cell_focus: Var[bool]

    # If true, header cells won't be focusable. This means keyboard navigation will be disabled for grid header cells, but remain enabled in other elements of the grid such as grid cells and tool panels.
    suppress_header_focus: Var[bool]

    # Set to true to be able to select the text within cells. Note: When this is set to true, the clipboard service is disabled and only selected text is copied.
    enable_cell_text_selection: Var[bool]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Return the modules required for the selection options."""
        return (
            {
                COMMUNITY_PKG: {"RowSelectionModule"},
                ENTERPRISE_PKG: {"CellSelectionModule"},
            }
            if any(key in props for key in cls.get_props())
            else {}
        )


class SortingOptions(ComponentEnterprise):
    """Sorting options for the AgGrid component."""

    # Set to true to specify that the sort should take accented characters into account. If this feature is turned on the sort will be slower.
    accented_sort: Var[bool]

    # Set to true to suppress multi-sort when the user shift-clicks a column header.
    suppress_multi_sort: Var[bool]

    # Set to true to always multi-sort when the user clicks a column header, regardless of key presses.
    always_multi_sort: Var[bool]

    # Set to 'ctrl' to have multi sorting work using the ^ Ctrl (or Command ⌘ for Mac) key.
    multi_sort_key: Var[Literal["ctrl", "shift"]]

    # Set to true to suppress sorting of un-sorted data to match original row data.
    suppress_maintain_unsorted_order: Var[bool]

    # Callback to perform additional sorting after the grid has sorted the rows.
    post_sort_rows: Var[Callable]

    # When enabled, sorts only the rows added/updated by a transaction.
    delta_sort: Var[bool]


class StylingOptions(ComponentEnterprise):
    """Styling options for the AgGrid component."""

    # Icons to use inside the grid instead of the grid's default icons.
    icons: Var[Mapping[str, str]]

    # Default row height in pixels.
    row_height: Var[int]

    # Callback version of property rowHeight to set height for each row individually. Function should return a positive number of pixels, or return null/undefined to use the default row height.
    get_row_height: Var[Callable]

    # The style properties to apply to all rows. Set to an object of key (style names) and values (style values).
    row_style: Var[Mapping[str, Any]]

    # Callback version of property rowStyle to set style for each row individually. Function should return an object of CSS values or undefined for no styles.
    get_row_style: Var[Callable]

    # CSS class(es) for all rows. Provide either a string (class name) or array of strings (array of class names).
    row_class: Var[str | Sequence[str]]

    # Callback version of property rowClass to set class(es) for each row individually. Function should return either a string (class name), array of strings (array of class names) or undefined for no class.
    get_row_class: Var[Callable]

    # Rules which can be applied to include certain CSS classes.
    row_class_rules: Var[Mapping[str, Callable]]

    # Set to true to not highlight rows by adding the ag-row-hover CSS class.
    suppress_row_hover_highlight: Var[bool]

    # Set to true to highlight columns by adding the ag-column-hover CSS class.
    column_hover_highlight: Var[bool]


class ThemeOptions(ComponentEnterprise):
    """Theme options for the AgGrid component."""

    # Theme to apply to the grid, or the string "legacy" to opt back into the v32 style of theming where themes were imported as CSS files and applied by setting a class name on the parent element.
    theme: Var[Literal["quartz", "balham", "alpine", "material"]]

    # If your theme uses a font that is available on Google Fonts, pass true to load it from Google's CDN.
    load_theme_google_fonts: Var[bool]

    # An element to insert style elements into when injecting styles into the grid. If undefined, styles will be added to the document head for grids rendered in the main document fragment, or to the grid wrapper element for other grids (e.g. those rendered in a shadow DOM or detached from the document).
    theme_style_container: Var[Any]

    # The CSS layer that this theme should be rendered onto. If your application loads its styles into a CSS layer, use this to load the grid styles into a previous layer so that application styles can override grid styles.
    theme_css_layer: Var[str]


class TooltipOptions(ComponentEnterprise):
    """Tooltip options for the AgGrid component."""

    # Set to true to use the browser's default tooltip instead of using the grid's Tooltip Component.
    enable_browser_tooltips: Var[bool]

    # The delay in milliseconds that it takes for tooltips to show up once an element is hovered over. Note: This property does not work if enableBrowserTooltips is true.
    tooltip_show_delay: Var[int]

    # The delay in milliseconds that it takes for tooltips to hide once they have been displayed. Note: This property does not work if enableBrowserTooltips is true and tooltipHideTriggers includes timeout.
    tooltip_hide_delay: Var[int]

    # Set to true to have tooltips follow the cursor once they are displayed.
    tooltip_mouse_track: Var[bool]

    # This defines when tooltip will show up for Cells, Headers and SetFilter Items.
    #   'standard' - The tooltip always shows up when the items configured with Tooltips are hovered.
    #   'whenTruncated' - The tooltip will only be displayed when the items hovered have truncated (showing ellipsis) values. This property does not work when enableBrowserTooltips={true}.
    tooltip_show_mode: Var[Literal["standard", "whenTruncated"]]

    # The trigger that will cause tooltips to show and hide.
    #   'hover' - The tooltip will show/hide when a cell/header is hovered.
    #   'focus' - The tooltip will show/hide when a cell/header is focused.
    tooltip_trigger: Var[Literal["hover", "focus"]]

    # Set to true to enable tooltip interaction. When this option is enabled, the tooltip will not hide while the tooltip itself it being hovered or has focus.
    tooltip_interactive: Var[bool]


class TreeDataOptions(ComponentEnterprise):
    """Tree data options for the AgGrid component."""

    # Set to true to enable the Grid to work with Tree Data. You must also implement the getDataPath(data) callback.
    tree_data: Var[bool]

    # Callback to be used when working with Tree Data when treeData = true.
    get_data_path: Var[Callable]

    # The name of the field to use in a data item to retrieve the array of children nodes of a node when while using treeData=true. It supports accessing nested fields using the dot notation.
    tree_data_children_field: Var[str]

    # (Client-side Row Model only) Allows groups to be open by default.
    is_group_open_by_default: Var[Callable]

    # Set to true prevent Group Rows from sticking to the top of the grid.
    suppress_group_rows_sticky: Var[bool]

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the list of modules to import based on the props."""
        return (
            {
                ENTERPRISE_PKG: {"TreeDataModule"},
            }
            if any(key in props for key in cls.get_props())
            else {}
        )


class GridOptions(
    AccessoriesOptions,
    ClipboardOptions,
    ColumnDefinitionsOptions,
    ColumnHeadersOptions,
    ColumnMovingOptions,
    ColumnPinningOptions,
    ColumnSizingOptions,
    ComponentsOptions,
    EditingOptions,
    ExportOptions,
    FilteringOptions,
    IntegratedChartsOptions,
    KeyboardNavigationOptions,
    LoadingCellOptions,
    LocalizationOptions,
    MasterDetailOptions,
    MiscellaneousOptions,
    OverlayOptions,
    PaginationOptions,
    RenderingOptions,
    RowAggregationOptions,
    RowDragOptions,
    RowFullWidthOptions,
    RowGroupingOptions,
    RowPinningOptions,
    RowPivotingOptions,
    RowModelOptions,
    RowModelClientSideOptions,
    RowModelInfiniteOptions,
    RowModelServiceSideOptions,
    RowModelViewportOptions,
    ScrollingOptions,
    SelectionOptions,
    SortingOptions,
    StylingOptions,
    ThemeOptions,
    TooltipOptions,
    TreeDataOptions,
):
    """Grid options for the AgGrid component."""

    @classmethod
    def get_modules(cls, props: dict[str, Any]) -> dict[str, set[str]]:
        """Get the list of modules to import based on the props."""
        return {}

    # We need passthrough function here to avoid running a parent method twice when walking the MRO.
    @classmethod
    def _format_props(cls, props: dict[str, Any]) -> dict[str, Any]:
        return props


class StateUpdatedEvent(TypedDict):
    """State updated event for the AgGrid component."""

    # The event that updated the grid state
    source: str

    # The state of the grid
    state: str


def _on_grid_pre_destroyed_spec(event: ObjectVar[dict]) -> tuple[Var[dict]]:
    """Spec for the grid pre-destroyed event."""
    return (event,)


def _on_state_updated_spec(event: ObjectVar[dict]) -> tuple[Var[StateUpdatedEvent]]:
    """Spec for the state updated event."""
    return (
        Var.create({"source": event.source, "state": event.state}).to(
            StateUpdatedEvent
        ),
    )


class FilterOpenedEvent(TypedDict):
    """Filter opened event for the AgGrid component."""

    # The column the filter is opened for
    col_id: str

    # The source of the event
    source: str

    # Type type of event
    type: str


def _on_filter_opened_spec(event: ObjectVar[dict]) -> tuple[Var[FilterOpenedEvent]]:
    """Spec for the filter opened event."""
    return (
        Var.create(
            {
                "col_id": event.column.to(Column).colId,
                "source": event.source,
                "type": event.type,
            }
        ).to(FilterOpenedEvent),
    )


class FilterChangedEvent(TypedDict):
    """Filter changed event for the AgGrid component."""

    # The source of the event
    source: str

    # Whether the filter change was before or after data change
    after_data_change: bool | None

    # Whether the filter change was before or after floating filter change
    after_floating_filter: bool | None

    # The columns affected by the filter change
    col_ids: list[str]

    # Type type of event
    type: str


def _on_filter_changed_spec(event: ObjectVar[dict]) -> tuple[Var[FilterChangedEvent]]:
    """Spec for the filter changed event."""
    return (
        Var.create(
            {
                "source": event.source,
                "after_data_change": event.afterDataChange,
                "after_floating_filter": event.afterFloatingFilter,
                "col_ids": event.columns.to(list[Column]).foreach(
                    lambda col: col.to(Column).colId
                ),
                "type": event.type,
            }
        ).to(FilterChangedEvent),
    )


class FilterInstance(TypedDict):
    """Filter instance for the AgGrid component."""

    # The model applied to the filter.
    applied_model: dict

    # The name/key of the filter.
    filter_name_key: str

    # The type of filter.
    filter_type: str


class FilterModifiedEvent(TypedDict):
    """Filter modified event for the AgGrid component."""

    # Which filter was modified
    filter_instance: FilterInstance

    # The column the filter is applied to
    col_id: str

    # Type type of event
    type: str


def _on_filter_modified_spec(event: ObjectVar[dict]) -> tuple[Var[FilterModifiedEvent]]:
    """Spec for the filter modified event."""
    filter_instance = event.filterInstance.to(dict)
    return (
        Var.create(
            {
                "filter_instance": {
                    "applied_model": filter_instance.get("appliedModel", {}),
                    "filter_name_key": filter_instance.get("filterNameKey", ""),
                    "filter_type": filter_instance.get("filterType", ""),
                },
                "col_id": event.column.to(Column).colId,
                "type": event.type,
            }
        ).to(FilterModifiedEvent),
    )


class FilterUiChangedEvent(TypedDict):
    """Filter UI changed event for the AgGrid component."""

    # The column affected
    col_id: str

    # Type type of event
    type: str


def _on_filter_ui_changed_spec(
    event: ObjectVar[dict],
) -> tuple[Var[FilterUiChangedEvent]]:
    """Spec for the filter UI changed event."""
    return (
        Var.create({"col_id": event.column.to(Column).colId, "type": event.type}).to(
            FilterUiChangedEvent
        ),
    )


class AdvancedFilterBuilderVisibleChangedEvent(TypedDict):
    """Advanced filter builder visible changed event for the AgGrid component."""

    # Indicates whether the Advanced Filter Builder is now visible
    visible: bool

    # Source of the visibility status change: 'ui' or 'api'
    source: str

    # Type type of event
    type: str


def _on_advanced_filter_builder_visible_changed_spec(
    event: ObjectVar[dict],
) -> tuple[Var[AdvancedFilterBuilderVisibleChangedEvent]]:
    """Spec for the advanced filter builder visible changed event."""
    return (
        Var.create(
            {"visible": event.visible, "source": event.source, "type": event.type}
        ).to(AdvancedFilterBuilderVisibleChangedEvent),
    )


class GridEvents(ComponentEnterprise):
    """Grid events for the AgGrid component."""

    # # Event handler for when the grid is ready
    on_grid_ready: rx.EventHandler[no_args_event_spec]

    # Event handler for when the grid is destroyed
    on_grid_pre_destroyed: rx.EventHandler[_on_grid_pre_destroyed_spec]

    # Event handler for when the grid is first rendered
    on_state_updated: rx.EventHandler[_on_state_updated_spec]

    # Event handler for cell click events
    on_cell_clicked: rx.EventHandler[_on_cell_event_spec]

    # Event handler for cell focused events
    on_cell_focused: rx.EventHandler[_on_cell_event_spec]

    # Event handler for cell mouse over events
    on_cell_mouse_over: rx.EventHandler[_on_cell_event_spec]

    # Event handler for cell mouse out events
    on_cell_mouse_out: rx.EventHandler[_on_cell_event_spec]

    # Event handler for cell double click events
    on_cell_double_clicked: rx.EventHandler[_on_cell_event_spec]

    # Event handler for right click on a cell
    on_cell_context_menu: rx.EventHandler[_on_cell_event_spec]

    # Event handler for row data changed events
    on_cell_value_changed: rx.EventHandler[_on_cell_value_changed]

    # Event handler for row click events
    on_row_clicked: rx.EventHandler[_on_row_event_spec]

    # Event handler for row double click events
    on_row_double_clicked: rx.EventHandler[_on_row_event_spec]

    # Event handler for row selected events
    on_row_selected: rx.EventHandler[_on_row_selected]

    # Event handler whenever the row data is updated (clientSide row model)
    on_row_data_updated: rx.EventHandler[rx.event.no_args_event_spec]

    # Event handler for selection change events
    on_selection_changed: rx.EventHandler[_on_selection_change_signature]

    # Event handler for cell selection changed events
    on_cell_selection_changed: rx.EventHandler[_on_cell_selection_change_signature]

    # Event handler for column header clicked events
    on_column_header_clicked: rx.EventHandler[_on_column_event_spec]

    # Event handler for column resized events
    on_column_resized: rx.EventHandler[_on_column_event_spec]

    # Event handler for column moved events
    on_column_moved: rx.EventHandler[_on_column_event_spec]

    # Event handler for column pinned events
    on_column_pinned: rx.EventHandler[_on_column_event_spec]

    # Event handler for column header context menu events
    on_column_header_context_menu: rx.EventHandler[_on_column_event_spec]

    # Event handler for column header focused events
    on_header_focused: rx.EventHandler[_on_column_event_spec]

    # Event handler for first data rendered events
    on_first_data_rendered: rx.EventHandler[_on_cell_event_spec]

    # Filter has been opened.
    on_filter_opened: rx.EventHandler[_on_filter_opened_spec]

    # Filter has been modified and applied.
    on_filter_changed: rx.EventHandler[_on_filter_changed_spec]

    # Filter was modified but not applied (when using enableFilterHandlers = false). Used when filters have 'Apply' buttons.
    on_filter_modified: rx.EventHandler[_on_filter_modified_spec]

    # Filter UI was modified (when using enableFilterHandlers = true).
    on_filter_ui_changed: rx.EventHandler[_on_filter_ui_changed_spec]

    # Floating filter UI modified (when using enableFilterHandlers = true).
    on_floating_filter_ui_changed: rx.EventHandler[_on_filter_ui_changed_spec]

    # Advanced Filter Builder visibility has changed (opened or closed).
    on_advanced_filter_builder_visible_changed: rx.EventHandler[
        _on_advanced_filter_builder_visible_changed_spec
    ]


class AgGrid(GridOptions, GridEvents, ComponentEnterprise):
    """Reflex AgGrid component is a high-performance and highly customizable component that wraps AG Grid, designed for creating rich datagrids."""

    # The library name for the ag-grid-react component
    library = f"{BASE_PKG}@{AG_GRID_VERSION}"

    # The tag name for the AgGridReact component
    tag = "AgGridReact"

    lib_dependencies: list[str] = [
        f"{COMMUNITY_PKG}@{AG_GRID_VERSION}",
        f"{ENTERPRISE_PKG}@{AG_GRID_VERSION}",
        f"{CHARTS_ENTERPRISE_PKG}@{CHARTS_VERSION}",
    ]

    _rename_props: ClassVar[dict[str, str]] = {"id": "gridId"}

    # List of modules to register in the grid.
    _modules: dict[str, set[str]]

    @classmethod
    def create(
        cls,
        *children,
        id: str,
        data_path_key: str | None = None,
        is_server_side_group_key: str | None = None,
        server_side_group_key: str | None = None,
        server_side_group_open_level: int | None = None,
        child_count_key: str | None = None,
        row_id_key: str | None = None,
        community_modules: set[str] | None = None,
        enterprise_modules: set[str] | None = None,
        **props,
    ) -> "AgGrid":
        """Create an instance of the AgGrid component."""
        from reflex.utils.exec import is_prod_mode

        props.setdefault("id", id)

        props = cls._handle_camelcase_props(props)

        modules = {}
        if community_modules:
            modules[COMMUNITY_PKG] = community_modules

        if enterprise_modules:
            modules[ENTERPRISE_PKG] = enterprise_modules

        if "data" in props and "row_data" not in props:
            props["row_data"] = props.pop("data")

        modules = cls.collect_modules(props, modules=modules)

        props = cls.format_props(props)

        props = cls._handle_hierarchical_data(
            data_path_key,
            is_server_side_group_key,
            server_side_group_key,
            server_side_group_open_level,
            child_count_key,
            row_id_key,
            props,
        )

        props = cls._handle_theme(props)

        if "auto_size_strategy" in props:
            props["firstDataRendered"] = _size_columns_to_fit

        grid: AgGrid = cast(AgGrid, super().create(*children, **props))

        if not is_prod_mode():
            if COMMUNITY_PKG in modules:
                modules[COMMUNITY_PKG].add("ValidationModule")
            else:
                modules.setdefault(COMMUNITY_PKG, {"ValidationModule"})

        grid._modules = modules
        return grid

    def _exclude_props(self) -> list[str]:
        return ["_modules"]

    @classmethod
    def _handle_camelcase_props(cls, props: dict[str, Any]) -> dict[str, Any]:
        return {to_snake_case(prop): props[prop] for prop in props}

    @classmethod
    def collect_modules(
        cls,
        props: dict[str, Any],
        modules: dict[str, set[str]] | None = None,
    ) -> dict[str, set[str]]:
        """Collect the modules required for the AgGrid component."""
        if modules is None:
            modules = {}

        for clz in cls._iter_parent_classes_with_method("get_modules"):
            mods: dict[str, set[str]] = clz.get_modules(props)  # pyright: ignore [reportAttributeAccessIssue]
            for mod_grp, modz in mods.items():
                if mod_grp not in modules:
                    modules.setdefault(mod_grp, set())
                modules[mod_grp] |= modz

        # replace community stuff with AllCommunityModules until import work well
        if COMMUNITY_PKG in modules:
            modules[COMMUNITY_PKG] = {"AllCommunityModule"}
        return modules

    @classmethod
    def format_props(cls, props: dict[str, Any]) -> dict[str, Any]:
        """Format the props for the AgGrid component."""
        for clz in cls._iter_parent_classes_with_method("_format_props"):
            props = clz._format_props(props)  # pyright: ignore [reportAttributeAccessIssue]
        return props

    @classmethod
    def _handle_hierarchical_data(
        cls,
        data_path_key: str | None,
        is_server_side_group_key: str | None,
        server_side_group_key: str | None,
        server_side_group_open_level: int | None,
        child_count_key: str | None,
        row_id_key: str | None,
        props: dict,
    ):
        # handle hierarchical data
        if data_path_key is not None:
            props["get_data_path"] = ArgsFunctionOperation.create(
                args_names=("data",),
                return_expr=Var(f"data.{data_path_key}"),
            )

        if is_server_side_group_key is not None:
            props["is_server_side_group"] = ArgsFunctionOperation.create(
                args_names=("data",),
                return_expr=f"data.{is_server_side_group_key}",
            )

        if server_side_group_key is not None:
            props["get_server_side_group_key"] = ArgsFunctionOperation.create(
                args_names=("data",),
                return_expr=f"data.{server_side_group_key}",
            )

        if server_side_group_open_level is not None:
            props["server_side_group_open_level"] = ArgsFunctionOperation.create(
                args_names=("params",),
                return_expr=f"params.rowNode.level < {server_side_group_open_level}",
                _var_type=rx.EventChain,
            )

        if child_count_key is not None:
            props["get_child_count"] = ArgsFunctionOperation.create(
                args_names=("data",),
                return_expr=f"data ? data.{child_count_key} : undefined",
                _var_type=rx.EventChain,
            )

        if row_id_key is not None:
            props["get_row_id"] = ArgsFunctionOperation.create(
                args_names=("params",),
                return_expr=f"params.data.{row_id_key}",
                _var_type=rx.EventChain,
            )
        return props

    @classmethod
    def _handle_theme(cls, props: dict[str, Any]) -> dict[str, Any]:
        theme = props.pop("theme", DEFAULT_THEME)

        if isinstance(theme, str):
            # Static theme - direct lookup (faster)
            theme_config = THEMES[theme] if theme in THEMES else THEMES[DEFAULT_THEME]
            props["class_name"] = rx.color_mode_cond(
                theme_config["light"], theme_config["dark"]
            )
        else:
            # Dynamic theme (Var) - use rx.match built from constants
            match_cases = []
            for theme_name, theme_config in THEMES.items():
                match_cases.append(
                    (
                        theme_name,
                        rx.color_mode_cond(theme_config["light"], theme_config["dark"]),
                    )
                )

            props["class_name"] = rx.match(theme, *match_cases, "")

        return props

    def add_imports(self):
        """Add imports for the AgGrid component."""
        _imports: dict[str, list] = {}

        style_imports = [
            f"{COMMUNITY_PKG}/styles/ag-grid.css",
            f"{COMMUNITY_PKG}/styles/ag-theme-quartz.css",
            f"{COMMUNITY_PKG}/styles/ag-theme-alpine.css",
            f"{COMMUNITY_PKG}/styles/ag-theme-balham.css",
            f"{COMMUNITY_PKG}/styles/ag-theme-material.css",
        ]

        _imports.setdefault("", [])

        _community_imports = [
            "ModuleRegistry",
            *self._modules.get(COMMUNITY_PKG, []),
            "provideGlobalGridOptions",
        ]
        _imports.setdefault(COMMUNITY_PKG, _community_imports)

        _enterprise_imports = self._modules.get(ENTERPRISE_PKG, [])

        if _enterprise_imports:
            _imports.setdefault(
                ENTERPRISE_PKG, [*_enterprise_imports, "LicenseManager"]
            )

        _imports[""].extend(style_imports)
        return _imports

    def add_custom_code(self) -> list[str]:
        """Add custom code for the AgGrid component."""
        codes = []
        if ENTERPRISE_PKG in self._modules:
            ag_grid_license_key = os.getenv(AG_GRID_LICENSE_KEY_ENV)

            if ag_grid_license_key is not None:
                codes.append(f"LicenseManager.setLicenseKey('{ag_grid_license_key}');")
            else:
                codes.append("LicenseManager.setLicenseKey(null);")

        _modules_to_register = Var.create(
            [
                Var(m)
                for m in [
                    *self._modules.get(COMMUNITY_PKG, set()),
                    *self._modules.get(ENTERPRISE_PKG, set()),
                ]
            ]
        )
        register_code = f"ModuleRegistry.registerModules({_modules_to_register!s});"

        def get_known_components() -> list[str]:
            return [
                *get_builtin_components(),
                *(
                    list(self.components._var_value)
                    if isinstance(self.components, LiteralVar)
                    else []
                ),
            ]

        codes.append(register_code)
        codes.append("provideGlobalGridOptions({'theme': 'legacy'});")
        codes.append(
            rf"""function toCamelCase(str) {{ return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase()); }}

// Generic formatter for AG Grid parameters
function createParamsFormatter(jsExpressions, options = {{}}) {{
  const {{
    nestedHandlers = {{}},
    builtInComponents = [],
    isArray = false
  }} = options;

  const processObject = (obj) => {{
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => {{
        const camelKey = toCamelCase(key);

        // Handle nested children arrays for column groups
        if (camelKey === 'children' && Array.isArray(value)) {{
          value = value.map(child => child !== null && typeof child === "object" ? processObject(child) : child);
        }}
        // Handle nested objects
        else if (nestedHandlers[camelKey] && typeof value === 'object' && value !== null) {{
          value = nestedHandlers[camelKey](value);
        }}

        // Handle JS expressions
        if (jsExpressions.includes(camelKey)) {{
          if (typeof value === 'string') {{
            // Built-in component check (if provided)
            if (builtInComponents.length > 0 && builtInComponents.includes(value)) {{
              return [camelKey, value];
            }}

            // Arrow function detection
            if (/\(?[\w,\s]*\)?\s*=>\s*(\{{[\s\S]*\}}|[\s\S]*)/.test(value)) {{
              return [camelKey, eval(value)];
            }}
            // String to function conversion
            return [camelKey, new Function('params', `return ${{value}};`)];
          }} else if (typeof value === 'object' && value !== null) {{
            // Object with "function" property
            if ('function' in value) {{
              return [camelKey, new Function('params', `return ${{value.function}};`)];
            }}
            // Object with "_js_expr" property
            else if ("_js_expr" in value) {{
              return [camelKey, eval(value._js_expr)];
            }}
          }}
        }}

        return [camelKey, value];
      }})
    );
  }};

  return function(input) {{
    if (isArray) {{
      if (!Array.isArray(input)) return input;
      return input.map(obj => obj !== null && typeof obj === "object" ? processObject(obj) : obj);
    }} else {{
      if (!input || typeof input !== 'object') return input;
      return processObject(input);
    }}
  }};
}}

// Create specific formatters using the generic factory
const formatColumnDefs = (() => {{
  // Special handling for formatColumnDefs due to __reflex checks
  const baseFormatter = createParamsFormatter(
    {list(ColumnDef.get_js_expressions(camel_case=True))},
    {{
      builtInComponents: {get_known_components()},
      isArray: true
    }}
  );

  return function(list) {{
    if (typeof __reflex === 'undefined' || typeof window === "undefined") {{
      return [];
    }}
    if (!Array.isArray(list)) {{
      throw new Error("Expected an array of objects");
    }}
    const jsx = __reflex["@emotion/react"]?.jsx;
    const Fragment = __reflex["react"]?.Fragment;

    return baseFormatter(list);
  }};
}})();

const formatDetailCellRendererParams = createParamsFormatter(
  {list(DetailCellRendererParams.get_js_expressions(camel_case=True))},
  {{
    nestedHandlers: {{
      detailGridOptions: createParamsFormatter([], {{
        nestedHandlers: {{
          columnDefs: formatColumnDefs
        }}
      }})
    }}
  }}
);

const formatLoadingCellRendererParams = createParamsFormatter(
  {list(LoadingCellRendererParams.get_js_expressions(camel_case=True))}
);

const formatFullWidthCellRendererParams = createParamsFormatter(
  {list(FullWidthCellRendererParams.get_js_expressions(camel_case=True))}
);

// Keep formatDetailGridOptions for backward compatibility
const formatDetailGridOptions = createParamsFormatter([], {{
  nestedHandlers: {{
    columnDefs: formatColumnDefs
  }}
}});
"""
        )

        return codes

    @property
    def api(self) -> AgGridAPI:
        """Get an API object for the current AgGrid component."""
        ref = self.get_ref()
        if ref:
            return AgGridAPI(ref=ref)
        raise ValueError("API is not available. Make sure the grid has a proper ref.")

    def get_selected_rows(self, callback: rx.EventHandler) -> EventSpec:
        """Get the selected rows in the grid."""
        return self.api.getSelectedRows(callback=callback)

    def select_all(self) -> EventSpec:
        """Select all the rows in the grid."""
        return self.api.select_all()

    def deselect_all(self) -> EventSpec:
        """Deselect all the rows in the grid."""
        return self.api.deselect_all()

    def select_rows_by_key(
        self, keys: list[str], node_path_key: str = "key"
    ) -> EventSpec:
        """Select rows by key."""
        return self.api.select_rows_by_key(keys, node_path_key)

    def log_nodes(self, node_path_key: str | None = None) -> EventSpec:
        """Log the nodes in the grid."""
        return self.api.log_nodes(node_path_key)

    def set_datasource(self, datasource: Datasource):
        """Set the datasource for the grid."""
        return self.api.set_grid_option(
            key="datasource",
            value=Var.create(datasource),
        )

    def set_serverside_datasource(self, datasource: SSRMDatasource):
        """Set the server-side datasource for the grid."""
        return self.api.set_grid_option(
            key="serverSideDatasource",
            value=Var.create(datasource),
        )

    def show_loading_overlay(self) -> EventSpec:
        """Show the loading overlay."""
        return self.api.showLoadingOverlay()

    def show_no_rows_overlay(self) -> EventSpec:
        """Show the no rows overlay."""
        return self.api.showNoRowsOverlay()

    def hide_overlay(self) -> EventSpec:
        """Hide the overlay."""
        return self.api.hideOverlay()

    def redraw_rows(self) -> EventSpec:
        """Redraw the rows in the grid."""
        return self.api.redrawRows()

    def export_data_as_csv(self) -> EventSpec:
        """Export the grid data as a CSV file."""
        return self.api.exportDataAsCsv()


class WrappedAgGrid(AgGrid):
    """Reflex AgGrid component is a high-performance and highly customizable component that wraps AG Grid, designed for creating rich datagrids."""

    @classmethod
    def create(cls, *children, **props):
        """Create an instance of the AgGrid component with good default dimensions."""
        width = props.pop("width", None)
        height = props.pop("height", None)

        grid = super().create(*children, **props)
        wrapped_grid = Div.create(
            grid,
            width=width or "40vw",
            height=height or "25vh",
        )
        wrapped_grid.api = grid.api  # pyright: ignore [reportAttributeAccessIssue]
        wrapped_grid.root = grid  # pyright: ignore [reportAttributeAccessIssue]
        return wrapped_grid


class AgGridNamespace(rx.ComponentNamespace):
    """Namespace for the AgGrid component."""

    api = AgGridAPI.create
    column_def = ColumnDef
    column_group = ColumnGroupDef
    filters = AGFilters
    editors = AGEditors
    aggs = AGAggregations
    renderers = AGRenderers
    status_panels = AGStatusPanels
    size_columns_to_fit = _size_columns_to_fit
    value_func_factory = staticmethod(value_func_factory)
    root = AgGrid.create
    __call__ = WrappedAgGrid.create


ag_grid = AgGridNamespace()
