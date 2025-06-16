from typing import Optional

import ipyvuetify as v
import solara
import traitlets


class MarkedWidget(v.VuetifyTemplate):
    template_file = (__file__, "marked.vue")
    md = traitlets.Unicode(allow_none=True).tag(sync=True)


@solara.component
def Marked(md: Optional[str]):
    return MarkedWidget.element(md=md)
