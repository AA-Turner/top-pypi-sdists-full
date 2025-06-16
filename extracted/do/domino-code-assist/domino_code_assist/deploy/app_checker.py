from typing import Callable

import ipyvuetify as iv
import reacton
import traitlets


class AppCheckerWidget(iv.VuetifyTemplate):
    template_file = (__file__, "app_checker.vue")

    url = traitlets.Unicode("").tag(sync=True)
    online = traitlets.Bool(False).tag(sync=True)
    running = traitlets.Bool(False).tag(sync=True)
    dev = traitlets.Bool(False).tag(sync=True)


@reacton.component
def AppChecker(url: str, online: bool, running: bool, on_online: Callable[[bool], None], dev: bool):
    return AppCheckerWidget.element(url=url, online=online, running=running, on_online=on_online, dev=dev)
