"""Column definition for ag-grid."""

from typing import Any, Callable, Literal

from reflex.components.props import PropsBase
from reflex.event import EventChain
from reflex.vars.base import Var
from reflex.vars.function import ArgsFunctionOperation

from ..resource import AGEditors, AGFilters
from .base import JS_EXPRESSION, AgGridResourceBase


class ColumnBaseProps(PropsBase):
    """Base column properties for ag-grid."""

    # The field of the row object to get the cell's data from. Deep references into a row object is supported via dot notation, i.e 'address.firstLine'.
    field: str | Var[str] | None = None

    # The unique ID to give the column. This is optional. If missing, the ID will default to the field. If both field and colId are missing, a unique ID will be generated. This ID is used to identify the column in the API for sorting, filtering etc.
    col_id: str | Var[str] | None = None

    # A comma separated string or array of strings containing ColumnType keys which can be used as a template for a column. This helps to reduce duplication of properties when you have a lot of common column properties.
    type: str | Var[str] | None = None

    # The data type of the cell values for this column. Can either infer the data type from the row data (true - the default behaviour), define a specific data type (string), or have no data type (false). If setting a specific data type (string value), this can either be one of the pre-defined data types 'text', 'number', 'boolean', 'date', 'dateString' or 'object', or a custom data type that has been defined in the dataTypeDefinitions grid option. Data type inference only works for the Client-Side Row Model, and requires non-null data. It will also not work if the valueGetter, valueParser or refData properties are defined, or if this column is a sparkline.
    cell_data_type: bool | str | Var[bool] | Var[str] | None = None

    # Function or expression. Gets the value from your data for display.
    value_getter: JS_EXPRESSION | None = None

    # A function or expression to format a value, should return a string.
    value_formatter: JS_EXPRESSION | None = None

    # Provided a reference data map to be used to map column values to their respective value from the map.
    ref_data: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Function to return a string key for a value. This string is used for grouping, Set filtering, and searching within cell editor dropdowns. When filtering and searching the string is exposed to the user, so make sure to return a human-readable value.
    key_creator: JS_EXPRESSION | None = None

    # Custom comparator for values, used by renderer to know if values have changed. Cells whose values have not changed don't get refreshed. By default the grid uses === which should work for most use cases.
    equals: JS_EXPRESSION | None = None

    # CSS class to use for the tool panel cell. Can be a string, array of strings, or function.
    tool_panel_class: str | list[str] | Var[str] | Var[list[str]] | None = None

    # Set to true if you do not want this column or group to appear in the Columns Tool Panel.
    suppress_columns_tool_panel: bool | Var[bool] | None = None

    # Whether to only show the column when the group is open / closed. If not set the column is always displayed as part of the group.
    column_group_show: Literal["open", "closed"] | Var[str] | None = None

    # Icons to use inside the column instead of the grid's default icons. Leave undefined to use defaults.
    icons: dict[str, str] | Var[dict[str, str]] | None = None

    # Set to true if this column is not navigable (i.e. cannot be tabbed into), otherwise false. Can also be a callback function to have different rows navigable.
    suppress_navigable: bool | Var[bool] | None = None

    # Allows the user to suppress certain keyboard events in the grid cell.
    suppress_keyboard_event: Var[Callable] | None = None

    # Pasting is on by default as long as cells are editable (non-editable cells cannot be modified, even with a paste operation). Set to true turn paste operations off.
    suppress_paste: bool | Var[bool] | None = None

    # Set to true to prevent the fillHandle from being rendered in any cell that belongs to this column
    suppress_fill_handle: bool | Var[bool] | None = None

    # Customise the list of menu items available in the context menu.
    context_menu_items: list[str] | Var[list[str]] | None = None

    # Context property that can be used to associate arbitrary application data with this column definition.
    context: Any | None = None


class ColumnAccessibilityProps(PropsBase):
    """Column accessibility properties for ag-grid."""

    # Used for screen reader announcements - the role property of the cells that belong to this column.
    cell_aria_role: str | Var[str] | None = None


class ColumnAggregationProps(PropsBase):
    """Column aggregation properties for ag-grid."""

    # Name of function to use for aggregation. In-built options are: sum, min, max, count, avg, first, last. Also accepts a custom aggregation name or an aggregation function.
    agg_func: str | Var[str] | None = None

    # Same as aggFunc, except only applied when creating a new column. Not applied when updating column definitions.
    initial_agg_func: str | Var[str] | None = None

    # Set to true if you want to be able to aggregate by this column via the GUI. This will not block the API or properties being used to achieve aggregation.
    enable_value: bool | Var[bool] | None = None

    # Aggregation functions allowed on this column e.g. ['sum', 'avg']. If missing, all installed functions are allowed. This will only restrict what the GUI allows a user to select, it does not impact when you set a function via the API.
    allowed_agg_funcs: list[str] | Var[list[str]] | None = None

    # The name of the aggregation function to use for this column when it is enabled via the GUI. Note that this does not immediately apply the aggregation function like aggFunc
    default_agg_func: str | Var[str] | None = None


class ColumnDisplayProps(PropsBase):
    """Column display properties for ag-grid."""

    # Set to true for this column to be hidden.
    hide: bool | Var[bool] | None = None

    # Same as hide, except only applied when creating a new column. Not applied when updating column definitions.
    initial_hide: bool | Var[bool] | None = None

    # Set to true to block making column visible / hidden via the UI (API will still work).
    lock_visible: bool | Var[bool] | None = None

    # Lock a column to position to 'left' or'right' to always have this column displayed in that position. true is treated as 'left'
    lock_position: Literal["left", "right"] | bool | None = None

    # Set to true if you do not want this column to be movable via dragging.
    suppress_movable: bool | Var[bool] | None = None

    # By default, values are formatted using the column's valueFormatter when exporting data from the grid. This applies to CSV and Excel export, as well as clipboard operations and the fill handle. Set to false to prevent values from being formatted for these operations. Regardless of this option, if custom handling is provided for the export operation, the value formatter will not be used.
    use_value_formatter_for_export: bool | Var[bool] | None = None


class ColumnEditingProps(PropsBase):
    """Column editing properties for ag-grid."""

    # Set to true if this column is editable, otherwise false. Can also be a function to have different rows editable.
    editable: bool | Var[bool] | JS_EXPRESSION | None = None

    # Function or expression. Custom function to modify your data based off the new value for saving. Return true if the data changed.
    value_setter: EventChain | Var[EventChain] | None = None

    # Function or expression. Parses the value for saving.
    value_parser: Var[Callable] | None = None

    # Provide your own cell editor component for this column's cells.
    cell_editor: AGEditors | str | Var[AGEditors] | Var[str] | None = None

    # Params to be passed to the cellEditor component.
    cell_editor_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Callback to select which cell editor to be used for a given row within the same column.
    cell_editor_selector: Var[Callable] | None = None

    # Set to true, to have the cell editor appear in a popup.
    cell_editor_popup: bool | None = None

    # Set the position for the popup cell editor. Possible values are
    #   over: Popup will be positioned over the cell
    #   under: Popup will be positioned below the cell leaving the cell value visible.
    cell_editor_popup_position: Literal["over", "under"] | None = None

    # Set to true to have cells under this column enter edit mode after single click.
    single_click_edit: bool | None = None

    # By default, values are parsed using the column's valueParser when importing data to the grid. This applies to clipboard operations and the fill handle. Set to false to prevent values from being parsed for these operations. Regardless of this option, if custom handling is provided for the import operation, the value parser will not be used.
    use_value_parser_for_import: bool | Var[bool] | None = None


class ColumnEventProps(PropsBase):
    """Column event properties for ag-grid."""

    # Callback for after the value of a cell has changed, either due to editing or the application calling api.setValue().
    on_cell_value_changed: EventChain | Var[EventChain] | None = None

    # Callback called when a cell is clicked.
    on_cell_clicked: EventChain | Var[EventChain] | None = None

    # Callback called when a cell is double clicked.
    on_cell_double_clicked: EventChain | Var[EventChain] | None = None

    # Callback called when a cell is right clicked.
    on_cell_context_menu: EventChain | Var[EventChain] | None = None


class ColumnFilterProps(PropsBase):
    """Column filter properties for ag-grid."""

    # Filter component to use for this column. Set to true to use the default filter. Set to the name of a Provided Filter or set to a IFilterComp.
    filter: AGFilters | str | Var[AGFilters] | Var[str] | None = None

    # Params to be passed to the filter component specified in filter.
    filter_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Function or expression. Gets the value for filtering purposes.
    filter_value_getter: JS_EXPRESSION | None = None

    # A function to tell the grid what Quick Filter text to use for this column if you don't want to use the default (which is calling toString on the value).
    get_quick_filter_text: Var[Callable] | None = None

    # Whether to display a floating filter for this column.
    floating_filter: bool | Var[bool] | None = None

    # The custom component to be used for rendering the floating filter. If none is specified the default AG Grid is used.
    floating_filter_component: Any | None = None

    # Params to be passed to floatingFilterComponent.
    floating_filter_component_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Set to true if you do not want this column (filter) or group (filter group) to appear in the Filters Tool Panel.
    suppress_filters_tool_panel: bool | Var[bool] | None = None


class ColumnHeaderProps(PropsBase):
    """Column header properties for ag-grid."""

    # The name to render in the column header.
    header_name: str | Var[str] | None = None

    # Function or expression. Gets the value for display in the header.
    header_value_getter: Var | str | None = None

    # Tooltip for the column header
    header_tooltip: str | Var[str] | None = None

    # An object of CSS values / or function returning an object of CSS values for a particular header.
    header_style: dict[str, Any] | Var[dict[str, Any]] | None = None

    # CSS class to use for the header cell. Can be a string, array of strings, or function.
    header_class: str | list[str] | Var[str] | Var[list[str]] | None = None

    # The custom header group component to be used for rendering the component header. If none specified the default AG Grid is used.
    header_component: Any | None = None

    # The parameters to be passed to the headerComponent.
    header_component_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # If enabled then column header names that are too long for the column width will wrap onto the next line. Default false
    wrap_header_text: bool | None = None

    # If enabled then the column header row will automatically adjust height to accommodate the size of the header cell. This can be useful when using your own headerComponent or long header names in conjunction with wrapHeaderText.
    auto_header_height: bool | None = None

    # Set to an array containing zero, one or many of the following options: 'filterMenuTab' | 'generalMenuTab' | 'columnsMenuTab'. This is used to figure out which menu tabs are present and in which order the tabs are shown.
    menu_tabs: list[str] | Var[list[str]] | None = None

    # Params used to change the behaviour and appearance of the Column Chooser/Columns Menu tab.
    columns_chooser_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Customise the list of menu items available in the column menu.
    main_menu_items: list[str] | Var[list[str]] | None = None

    # Set to true if no menu button should be shown for this column header.
    suppress_header_menu_button: bool | Var[bool] | None = None

    # Set to true to not display the filter button in the column header. Doesn't apply when columnMenu = 'legacy'.
    suppress_header_filter_button: bool | Var[bool] | None = None

    # Set to true to not display the column menu when the column header is right-clicked. Doesn't apply when columnMenu = 'legacy'.
    suppress_header_context_menu: bool | Var[bool] | None = None

    # Suppress the grid taking action for the relevant keyboard event when a header is focused.
    suppress_header_keyboard_event: Var[Callable] | None = None

    # If true, the button in the floating filter that opens the parent filter in a popup will not be displayed. Only applies if floatingFilter = true.
    suppress_floating_filter_button: bool | None = None


class ColumnIntegratedChartProps(PropsBase):
    """Column integrated chart properties for ag-grid."""

    # Defines the chart data type that should be used for a column.
    chart_data_type: str | Var[str] | None = None


class ColumnPinnedProps(PropsBase):
    """Column pinned properties for ag-grid."""

    # Pin a column to one side: right or left. A value of true is converted to 'left'.
    pinned: Literal["left", "right"] | bool | None = None

    # Same as pinned, except only applied when creating a new column. Not applied when updating column definitions.
    initial_pinned: Literal["left", "right"] | bool | None = None

    # Set to true to block the user pinning the column, the column can only be pinned via definitions or API.
    lock_pinned: bool | Var[bool] | None = None


class ColumnPivotProps(PropsBase):
    """Column pivot properties for ag-grid."""

    # Set to true to pivot by this column.
    pivot: bool | Var[bool] | None = None

    # Same as pivot, except only applied when creating a new column. Not applied when updating column definitions.
    initial_pivot: bool | Var[bool] | None = None

    # Set this in columns you want to pivot by. If only pivoting by one column, set this to any number (e.g. 0). If pivoting by multiple columns, set this to where you want this column to be in the order of pivots (e.g. 0 for first, 1 for second, and so on).
    pivot_index: int | Var[int] | None = None

    # Same as pivotIndex, except only applied when creating a new column. Not applied when updating column definitions.
    initial_pivot_index: int | Var[int] | None = None

    # Set to true if you want to be able to pivot by this column via the GUI. This will not block the API or properties being used to achieve pivot.
    enable_pivot: bool | Var[bool] | None = None

    # Only for CSRM, see SSRM Pivoting. Comparator to use when ordering the pivot columns, when this column is used to pivot on. The values will always be strings, as the pivot service uses strings as keys for the pivot groups.
    pivot_comparator: Var[Callable] | None = None


class ColumnRenderingProps(PropsBase):
    """Column rendering properties for ag-grid."""

    # An object of CSS values / or function returning an object of CSS values for a particular cell.
    cell_style: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Class to use for the cell. Can be string, array of strings, or function that returns a string or array of strings.
    cell_class: str | list[str] | Var[str] | Var[list[str]] | None = None

    # Rules which can be applied to include certain CSS classes.
    cell_class_rules: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Provide your own cell Renderer component for this column's cells.
    cell_renderer: ArgsFunctionOperation | str | JS_EXPRESSION | None = None

    # Params to be passed to the cellRenderer component.
    cell_renderer_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Callback to select which cell renderer to be used for a given row within the same column.
    cell_renderer_selector: Var[Callable] | None = None

    # Provide your own cell loading Renderer component for this column's cells when using SSRM.
    loading_cell_renderer: ArgsFunctionOperation | str | JS_EXPRESSION | None = None

    # Params to be passed to the loadingCellRenderer component.
    loading_cell_renderer_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Callback to select which loading renderer to be used for a given row within the same column.
    loading_cell_renderer_selector: Var[Callable] | None = None

    # Set to true to have the grid calculate the height of a row based on contents of this column.
    auto_height: bool | None = None

    # Set to true to have the text wrap inside the cell - typically used with autoHeight.
    wrap_text: bool | None = None

    # Set to true to flash a cell when it's refreshed.
    enable_cell_change_flash: bool | None = None


class ColumnRowDragProps(PropsBase):
    """Column row drag properties for ag-grid."""

    # boolean or Function. Set to true (or return true from function) to allow row dragging.
    row_drag: bool | Var[bool] | Var[Callable] | None = None

    # A callback that should return a string to be displayed by the rowDragComp while dragging a row. If this callback is not set, the rowDragText callback in the gridOptions will be used and if there is no callback in the gridOptions the current cell value will be used.
    row_drag_text: Var[Callable] | None = None

    # boolean or Function. Set to true (or return true from function) to allow dragging for native drag and drop.
    dnd_source: bool | Var[bool] | Var[Callable] | None = None

    # Function to allow custom drag functionality for native drag and drop.
    dnd_source_on_row_drag: Var[Callable] | None = None


class ColumnRowGroupProps(PropsBase):
    """Column row group properties for ag-grid."""

    # Set to true to row group by this column.
    row_group: bool | Var[bool] | None = None

    # Same as rowGroup, except only applied when creating a new column. Not applied when updating column definitions.
    initial_row_group: bool | Var[bool] | None = None

    # Set this in columns you want to group by. If only grouping by one column, set this to any number (e.g. 0). If grouping by multiple columns, set this to where you want this column to be in the group (e.g. 0 for first, 1 for second, and so on).
    row_group_index: int | Var[int] | None = None

    # Same as rowGroupIndex, except only applied when creating a new column. Not applied when updating column definitions.
    initial_row_group_index: int | Var[int] | None = None

    # Set to true if you want to be able to row group by this column via the GUI. This will not block the API or properties being used to achieve row grouping.
    enable_row_group: bool | Var[bool] | None = None

    # Set to true to have the grid place the values for the group into the cell, or put the name of a grouped column to just show that group.
    show_row_group: bool | str | None = None


class ColumnSortProps(PropsBase):
    """Column sort properties for ag-grid."""

    # Set to false to disable sorting which is enabled by default.
    sortable: bool | Var[bool] | None = None

    # If sorting by default, set it here. Set to asc or desc.
    sort: Literal["asc", "desc"] | None = None

    # Same as sort, except only applied when creating a new column. Not applied when updating column definitions.
    initial_sort: Literal["asc", "desc"] | None = None

    # If sorting more than one column by default, specifies order in which the sorting should be applied.
    sort_index: int | Var[int] | None = None

    # Same as sortIndex, except only applied when creating a new column. Not applied when updating column definitions.
    initial_sort_index: int | Var[int] | None = None

    # Array defining the order in which sorting occurs (if sorting is enabled). An array with any of the following in any order ['asc','desc',null]
    sorting_order: (
        list[Literal["asc", "desc", None]]
        | Var[list[Literal["asc", "desc", None]]]
        | None
    ) = None

    # Override the default sorting order by providing a custom sort comparator.
    comparator: Var[Callable] | None = None

    # Set to true if you want the unsorted icon to be shown when no sort is applied to this column.
    un_sort_icon: bool | None = None


class ColumnSpanProps(PropsBase):
    """Column span properties for ag-grid."""

    # By default, each cell will take up the width of one column. You can change this behaviour to allow cells to span multiple columns.
    col_span: Var[Callable] | None = None

    # Set to true to automatically merge cells in this column with equal values. Provide a callback to specify custom merging logic.
    span_rows: bool | Var[bool] | None = None


class ColumnTooltipProps(PropsBase):
    """Column tooltip properties for ag-grid."""

    # The field of the tooltip to apply to the cell.
    tooltip_field: str | Var[str] | None = None

    # Callback that should return the string to use for a tooltip, tooltipField takes precedence if set. If using a custom tooltipComponent you may return any custom value to be passed to your tooltip component.
    tooltip_value_getter: Var[Callable] | None = None

    # Provide your own tooltip component for the column.
    tooltip_component: Any | None = None

    # Params to be passed to the tooltipComponent.
    tooltip_component_params: dict[str, Any] | Var[dict[str, Any]] | None = None


class ColumnWidthProps(PropsBase):
    """Column width properties for ag-grid."""

    # The width for this column. If flex is used, this property is ignored.
    width: int | Var[int] | None = None

    # Same as width, except only applied when creating a new column. Not applied when updating column definitions.
    initial_width: int | Var[int] | None = None

    # The minimum width for this column.
    min_width: int | Var[int] | None = None

    # The maximum width for this column.
    max_width: int | Var[int] | None = None

    # The flex value for this column. If flex is used, the width property is ignored.
    flex: int | Var[int] | None = None

    # Same as flex, except only applied when creating a new column. Not applied when updating column definitions.
    initial_flex: int | Var[int] | None = None

    # Set to false to disable resizing which is enabled by default.
    resizable: bool | Var[bool] | None = None

    # Set to true if you want this column's width to be fixed during 'size to fit' operations.
    suppress_size_to_fit: bool | Var[bool] | None = None

    # Set to true if you do not want this column to be auto-resizable by double clicking it's edge.
    suppress_auto_size: bool | Var[bool] | None = None


class ColumnDef(
    ColumnBaseProps,
    ColumnAccessibilityProps,
    ColumnAggregationProps,
    ColumnDisplayProps,
    ColumnEditingProps,
    ColumnEventProps,
    ColumnFilterProps,
    ColumnHeaderProps,
    ColumnIntegratedChartProps,
    ColumnPinnedProps,
    ColumnPivotProps,
    ColumnRenderingProps,
    ColumnRowDragProps,
    ColumnRowGroupProps,
    ColumnSortProps,
    ColumnSpanProps,
    ColumnTooltipProps,
    ColumnWidthProps,
    AgGridResourceBase,
):
    """Column definition for ag-grid."""

    @classmethod
    def create(cls, known_components: list[str], **props):
        """Create a ColumnDef with known components for component resolution."""
        instance = cls(**props)
        instance._known_components = known_components  # pyright: ignore [reportAttributeAccessIssue]
        return instance


class ColumnGroupBaseProps(PropsBase):
    """Column group base properties for ag-grid."""

    # A list containing a mix of columns and column groups.
    children: (
        list["ColumnDef | ColumnGroupDef"] | Var[list["ColumnDef | ColumnGroupDef"]]
    )

    # The unique ID to give the column. This is optional. If missing, a unique ID will be generated. This ID is used to identify the column group in the API.
    group_id: str | Var[str] | None = None

    # Set to true to keep columns in this group beside each other in the grid. Moving the columns outside of the group (and hence breaking the group) is not allowed.
    marry_children: bool | Var[bool] | None = None

    # Set to true if this group should be opened by default.
    open_by_default: bool | Var[bool] | None = None

    # Whether to only show the column when the group is open / closed. If not set the column is always displayed as part of the group.
    column_group_show: Literal["open", "closed"] | Var[str] | None = None

    # CSS class to use for the tool panel cell. Can be a string, array of strings, or function.
    tool_panel_class: str | list[str] | Var[str] | Var[list[str]] | None = None

    # Set to true if you do not want this column or group to appear in the Columns Tool Panel.
    suppress_columns_tool_panel: bool | Var[bool] | None = None

    # Set to true if you do not want this column (filter) or group (filter group) to appear in the Filters Tool Panel.
    suppress_filters_tool_panel: bool | Var[bool] | None = None

    # Provide your own tooltip component for the column group.
    tooltip_component: Any | None = None

    # Params to be passed to the tooltipComponent.
    tooltip_component_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Context property that can be used to associate arbitrary application data with this column definition.
    context: Any | None = None


class ColumnGroupHeaderProps(PropsBase):
    """Column group header properties for ag-grid."""

    # The name to render in the column header. If not specified and field is specified, the field name will be used as the header name.
    header_name: str | Var[str] | None = None

    # CSS class to use for the header cell. Can be a string, array of strings, or function.
    header_class: str | list[str] | Var[str] | Var[list[str]] | None = None

    # Tooltip for the column header
    header_tooltip: str | Var[str] | None = None

    # If enabled then the column header row will automatically adjust height to accommodate the size of the header cell. This can be useful when using your own headerComponent or long header names in conjunction with wrapHeaderText.
    auto_header_height: bool | None = None

    # The custom header group component to be used for rendering the component header. If none specified the default AG Grid is used.
    header_group_component: Any | None = None

    # The params used to configure the headerGroupComponent.
    header_group_component_params: dict[str, Any] | Var[dict[str, Any]] | None = None

    # Set to true if you don't want the column header for this column to span the whole height of the header container.
    suppress_span_header_height: bool | None = None

    # If true the label of the Column Group will not scroll alongside the grid to always remain visible.
    suppress_sticky_label: bool | None = None


class ColumnGroupDef(
    ColumnGroupHeaderProps,
    ColumnGroupBaseProps,
    AgGridResourceBase,
):
    """Column group definition for ag-grid."""

    @classmethod
    def create(cls, known_components: list[str], **props):
        """Create a ColumnGroupDef with known components for component resolution."""
        instance = cls(**props)
        instance._known_components = known_components  # pyright: ignore [reportAttributeAccessIssue]
        return instance

    def dict(self, *args, **kwargs):
        """Override dict method to exclude None values."""
        kwargs.setdefault("exclude_none", True)

        return super().dict(*args, **kwargs)
