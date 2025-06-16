from ..imports import *
class JSBridge(QtCore.QObject):
    """
    A QObject that exposes a slot 'receiveInspectData' to JavaScript via QWebChannel.
    Whenever JavaScript calls `window.pyBridge.receiveInspectData(payload)`, this slot runs.
    """
    @QtCore.pyqtSlot(str)
    def receiveInspectData(self, payload_json: str):
        """
        payload_json: a JSON‐string sent from JavaScript.
        We simply print it or dispatch it to FileDropArea.
        For example, payload_json might be: '{"files":["/path/a.py","/path/b.py"]}'.
        """
        try:
            data = json.loads(payload_json)
        except json.JSONDecodeError:
            print("JSBridge: Invalid JSON received:", payload_json)
            return

        # Example: assume data["files"] is a list of file paths:
        if "files" in data and isinstance(data["files"], list):
            file_paths: List[str] = data["files"]
            # Here, you'd forward to wherever you want. For demo, let's just print:
            print("JSBridge got files:", file_paths)
            # If you have a global reference to the FileDropArea, you could do:
            # self.parent().drop_area.process_files(file_paths)
        else:
            print("JSBridge: unexpected payload:", data)
