import reacton
from react_ipywidgets.core import Element

from domino_code_assist import action

from .load_data.data_source import DataSourcePanel
from .transform.transform_action_ui import (
    FilterPanelView,
    GroupByPanelView,
    MergePanelView,
    SelectColumnsPanelView,
)

_ui_for_action = {
    action.ActionDownloadDataSource: DataSourcePanel,
    action.ActionFilter: FilterPanelView,
    action.ActionSelectColumns: SelectColumnsPanelView,
    action.ActionDropColumns: SelectColumnsPanelView,
    action.ActionGroupBy: GroupByPanelView,
    action.ActionMerge: MergePanelView,
}


@reacton.component
def EditAction(columns, dtypes, on_action, action_obj) -> Element:
    return _ui_for_action[action_obj.__class__](
        columns,
        dtypes,
        action_obj,
        on_action,
    )  # type: ignore
