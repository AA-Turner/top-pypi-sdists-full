from typing import Callable, List, Optional

import ipyvuetify as v
import reacton
import traitlets


class DfSelectWidget(v.VuetifyTemplate):
    template_file = (__file__, "df_select.vue")

    label = traitlets.Unicode("").tag(sync=True)
    items = traitlets.List().tag(sync=True)
    value = traitlets.Unicode(allow_none=True).tag(sync=True)
    hide_details = traitlets.Bool(False).tag(sync=True)
    error_messages = traitlets.List(allow_none=True).tag(sync=True)
    messages = traitlets.List(allow_none=True).tag(sync=True)
    error = traitlets.Bool(False).tag(sync=True)


@reacton.component
def DfSelect(
    label: str,
    items: List,
    value: Optional[str],
    on_value: Callable[[Optional[str]], None],
    hide_details: bool = False,
    error_messages: Optional[List[str]] = None,
    messages: Optional[List[str]] = [],
    error: bool = False,
):
    return DfSelectWidget.element(
        label=label, items=items, value=value, on_value=on_value, hide_details=hide_details, error_messages=error_messages, messages=messages, error=error
    )
