import ipyvuetify as v
import reacton
import traitlets


class ButtonClipboardWidget(v.VuetifyTemplate):
    template_file = (__file__, "button_clipboard.vue")

    pathname = traitlets.Unicode("").tag(sync=True)
    show_clipboard_message = traitlets.Bool(False).tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)


@reacton.component
def ButtonClipboard(pathname: str, disabled: bool = False):
    return ButtonClipboardWidget.element(pathname=pathname, disabled=disabled)
