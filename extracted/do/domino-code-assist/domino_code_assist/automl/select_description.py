import ipyvuetify as v
import solara
import traitlets


class SelectDescriptionWidget(v.VuetifyTemplate):
    template_file = (__file__, "select_description.vue")

    label = traitlets.Unicode().tag(sync=True)
    items = traitlets.List(allow_none=True).tag(sync=True)
    value = traitlets.Any().tag(sync=True)


@solara.component()
def SelectDescription(label, items, value, on_value):
    return SelectDescriptionWidget.element(label=label, value=value, items=items, on_value=on_value)
