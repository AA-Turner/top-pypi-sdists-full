"""Resource definitions for ag-grid."""

import dataclasses
from types import SimpleNamespace
from typing import Any

import reflex as rx
from reflex.components.props import PropsBase
from reflex.vars import StringVar
from reflex.vars.base import Var
from reflex.vars.function import ArgsFunctionOperation

from reflex_enterprise.utils import arrow_func


def value_func_factory(
    return_expr: str | Var[str],
    known_components: list[str] | None = None,
) -> ArgsFunctionOperation | StringVar:
    """Create a value getter function."""
    if isinstance(return_expr, str):
        if "params." not in return_expr:
            # When the expression does not reference `params`, treat it as a component name.
            return Var.create(return_expr)
        # Otherwise, treat it as a verbatim js expression.
        return_expr = Var(return_expr)
    return ArgsFunctionOperation.create(args_names=["params"], return_expr=return_expr)


class AGFilters(SimpleNamespace):
    """Built-in Filters for ag-grid."""

    text = "agTextColumnFilter"
    number = "agNumberColumnFilter"
    date = "agDateColumnFilter"
    set = "agSetColumnFilter"
    multi = "agMultiColumnFilter"


class AGAggregations(SimpleNamespace):
    """Built-in Aggregations for ag-grid."""

    sum = "sum"
    count = "count"
    min = "min"
    max = "max"
    avg = "avg"
    first = "first"
    last = "last"


class AGEditors(SimpleNamespace):
    """Built-in Editors for ag-grid."""

    text = "agTextCellEditor"
    large_text = "agLargeTextCellEditor"
    select = "agSelectCellEditor"
    rich_select = "agRichSelectCellEditor"
    number = "agNumberCellEditor"
    date = "agDateCellEditor"
    date_string = "agDateStringCellEditor"
    checkbox = "agCheckboxCellEditor"


@dataclasses.dataclass(kw_only=True)
class RendererParams:
    """Renderer params for ag-grid."""

    value: str
    data: dict[str, Any]
    node: Any
    column: Any
    context: Any
    valueFormatted: str  # noqa: N815


def _none_cond(value: str | Var[str], default: Any = None) -> str | Var[str]:
    """Return a conditional expression for None values."""
    return rx.cond(value, value, default)


def _formatted_value(params: RendererParams) -> str | Var[str]:
    """Return formatted value for ag-grid cells."""
    return _none_cond(
        params.valueFormatted,
        _none_cond(params.value, ""),
    )


class AGRenderers(SimpleNamespace):
    """Renderers for ag-grid."""

    @arrow_func
    @staticmethod
    def link(params: RendererParams):
        """Link renderer for AgGrid cells."""
        return rx.link(
            _formatted_value(params),
            href=_none_cond(params.value, ""),
        )

    @arrow_func
    @staticmethod
    def link_external(params: RendererParams):
        """Link renderer for AgGrid cells with external link."""
        return rx.link(
            _formatted_value(params),
            href=_none_cond(params.value, ""),
            target="_blank",
        )

    @arrow_func
    @staticmethod
    def image(params: RendererParams):
        """Image renderer for AgGrid cells."""
        return rx.image(
            src=_none_cond(params.value, ""),
            alt=_formatted_value(params),
        )

    # Built-in AG Grid renderers
    checkbox_cell = "agCheckboxCellRenderer"
    group_cell = "agGroupCellRenderer"
    loading_cell = "agLoadingCellRenderer"
    skeleton_cell = "agSkeletonCellRenderer"
    animate_show_change_cell = "agAnimateShowChangeCellRenderer"
    animate_slide_cell = "agAnimateSlideCellRenderer"
    rich_select_cell = "agRichSelectCellRenderer"
    popup_cell = "agPopupCellRenderer"


class AGStatusPanels(SimpleNamespace):
    """Built-in Status panels for ag-grid."""

    total: str = "agTotalRowCountComponent"
    filtered: str = "agFilteredRowCountComponent"
    filtered_total: str = "agTotalAndFilteredRowCountComponent"
    selected: str = "agSelectedRowCountComponent"
    aggregation: str = "agAggregationComponent"


class StatusPanelDef(PropsBase):
    """Status panel definition for ag-grid."""

    status_panel: str | Var[str]
    status_panel_params: dict[str, Any] | Var[dict[str, Any]] | None = None
    align: str | Var[str] | None = None
    key: str | Var[str] | None = None


class ToolPanelDef(PropsBase):
    """Tool panel definition for ag-grid."""

    id: str
    label_key: str
    label_default: str
    min_width: int | Var[int] | None = None
    max_width: int | Var[int] | None = None
    width: int | Var[int] | None = None


class SideBarDef(PropsBase):
    """Side bar definition for ag-grid."""

    tool_panels: list[str | ToolPanelDef] | Var[list[str | ToolPanelDef]]
    default_tool_panel: str | Var[str] | None = None
    hidden_by_default: bool | Var[bool] = False
    position: str | Var[str] | None = None


def get_builtin_components() -> list[str]:
    """Get all AG Grid built-in component names from resource definitions.

    Returns:
        List of built-in AG Grid component names.
    """
    components = []

    # Collect from AGFilters
    for attr_name in dir(AGFilters):
        if not attr_name.startswith("_"):
            attr_value = getattr(AGFilters, attr_name)
            if isinstance(attr_value, str):
                components.append(attr_value)

    # Collect from AGEditors
    for attr_name in dir(AGEditors):
        if not attr_name.startswith("_"):
            attr_value = getattr(AGEditors, attr_name)
            if isinstance(attr_value, str):
                components.append(attr_value)

    # Collect from AGRenderers
    for attr_name in dir(AGRenderers):
        if not attr_name.startswith("_"):
            attr_value = getattr(AGRenderers, attr_name)
            if isinstance(attr_value, str):
                components.append(attr_value)

    # Collect from AGStatusPanels
    for attr_name in dir(AGStatusPanels):
        if not attr_name.startswith("_"):
            attr_value = getattr(AGStatusPanels, attr_name)
            if isinstance(attr_value, str):
                components.append(attr_value)

    return components
