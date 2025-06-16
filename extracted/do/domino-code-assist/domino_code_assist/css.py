import ipyvuetify as v
import reacton


class CssWidget(v.VuetifyTemplate):
    template_file = (__file__, "css.vue")


@reacton.component
def Css():
    return CssWidget.element()
