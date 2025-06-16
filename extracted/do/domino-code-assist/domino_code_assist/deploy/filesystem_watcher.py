from typing import Any, Callable

import ipyvuetify as iv
import reacton
import traitlets


class FileSystemWatcherWidget(iv.VuetifyTemplate):
    template_file = (__file__, "filesystem_watcher.vue")

    server_path = traitlets.Unicode("").tag(sync=True)
    dev = traitlets.Bool(False).tag(sync=True)
    on_connected = traitlets.Callable()
    on_message = traitlets.Callable()

    def vue_on_message(self, data):
        self.on_message(data)

    def vue_on_connected(self, connected):
        self.on_connected(connected)


@reacton.component
def FileSystemWatcher(server_path: str, on_connected: Callable[[bool], None], on_message: Callable[[Any], None], dev: bool):
    return FileSystemWatcherWidget.element(server_path=server_path, on_connected=on_connected, on_message=on_message, dev=dev)
