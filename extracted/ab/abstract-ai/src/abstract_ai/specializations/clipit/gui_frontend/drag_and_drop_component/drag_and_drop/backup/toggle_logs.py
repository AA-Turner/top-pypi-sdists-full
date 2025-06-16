def _toggle_logs(self, checked: bool):
    """
    Show/hide the log console when the toolbar action is toggled.
    """
    input(checked)
    if checked:
        self.log_widget.show()
        self.toggle_logs_action.setText("Hide Logs")
        self._log("Logs shown.")
    else:
        self._log("Logs hidden.")
        self.log_widget.hide()
        self.toggle_logs_action.setText("Show Logs")
