from typing import Callable, List, Optional

import ipyvuetify as vy
import ipywidgets
import reacton
import solara as sol
import traitlets

from domino_code_assist import util


class DrawerWidget(vy.VuetifyTemplate):
    template_file = (__file__, "drawer.vue")

    is_open = traitlets.Bool(False).tag(sync=True)
    content = traitlets.Any().tag(sync=True, **ipywidgets.widget_serialization)
    title = traitlets.Unicode().tag(sync=True)
    on_apply = traitlets.Callable(default_value=lambda: None, allow_none=True)
    show_default_buttons = traitlets.Bool(True).tag(sync=True)
    edit = traitlets.Bool(False).tag(sync=True)
    apply_disabled = traitlets.Bool(False).tag(sync=True)
    show_var_out = traitlets.Bool(False).tag(sync=True)
    var_out = traitlets.Unicode().tag(sync=True)
    valid_variable_name = traitlets.Bool(True).tag(sync=True)
    width = traitlets.Unicode("unset").tag(sync=True)
    warning_widget = traitlets.Any().tag(sync=True, **ipywidgets.widget_serialization)
    class_ = traitlets.Unicode("").tag(sync=True)

    def vue_apply(self, *ignored):
        self.on_apply()


@reacton.component
def RightDrawer(
    open: bool,
    on_open: Callable[[bool], None],
    title: str,
    children: List[reacton.core.Element] = None,
    show_default_buttons: bool = True,
    on_apply: Optional[Callable[[], None]] = None,
    edit: bool = False,
    apply_disabled: bool = False,
    show_var_out: bool = False,
    var_out: str = "",
    on_var_out: Optional[Callable[[str], None]] = lambda *_: None,
    width: str = "unset",
    warning_widget: Optional[reacton.core.Element] = None,
    class_: str = "",
):
    valid_variable_name = util.is_valid_variable_name(var_out)

    content = None
    if children and len(children) == 1:
        content = children[0]
    elif children:
        content = sol.Div(children=children)
    return DrawerWidget.element(
        is_open=open,
        on_is_open=on_open,
        content=content,
        title=title,
        show_default_buttons=show_default_buttons,
        on_apply=on_apply,
        edit=edit,
        apply_disabled=(show_var_out and not valid_variable_name) or apply_disabled,
        show_var_out=show_var_out,
        var_out=var_out,
        on_var_out=on_var_out,
        valid_variable_name=valid_variable_name,
        width=width,
        warning_widget=warning_widget,
        class_=class_,
    )
