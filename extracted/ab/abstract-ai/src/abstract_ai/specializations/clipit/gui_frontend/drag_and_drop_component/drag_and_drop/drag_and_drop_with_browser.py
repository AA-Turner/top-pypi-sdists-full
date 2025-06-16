from ..imports import *

class DragDropWithWebBrowser(QtWidgets.QWidget):
    def __init__(self,
                 *,
                 FileDropArea,
                 FileSystemTree,
                 JSBridge,
                 url: str = None
                 ):
        super().__init__()
        self.resize(800, 600)

        self.web_view = QtWebEngineWidgets.QWebEngineView(self)

        if url:
            # Load exactly what was passed on the command line
            self.web_view.load(QtCore.QUrl(url))
        else:
            # Fallback to local HTML
            html_path = os.path.normpath(
                os.path.join(os.path.dirname(__file__), "..", "html", "drop-n-copy.html")
            )
            self.web_view.load(QtCore.QUrl.fromLocalFile(html_path))
        self.setWindowTitle("ClipIt - File Browser + Drag/Drop + Browser Inspect + Logs")
       
        self.FileDropArea=FileDropArea 
        self.JSBridge = JSBridge
        self.FileSystemTree = FileSystemTree
        # 1) Top‐level layout
        main_layout = QtWidgets.QVBoxLayout(self)

        # 2) Toolbar (optional—copy from your existing code)
        toolbar = QtWidgets.QToolBar()
        toolbar.setMovable(False)
        self.toggle_logs_action = QtWidgets.QAction("Show Logs", self)
        self.toggle_logs_action.setCheckable(True)
        self.toggle_logs_action.triggered.connect(self._toggle_logs)
        toolbar.addAction(self.toggle_logs_action)
        main_layout.addWidget(toolbar)

        # 3) Splitter: left=FileSystemTree, right=another splitter (vertical)
        outer_splitter = QtWidgets.QSplitter(self)
        outer_splitter.setOrientation(QtCore.Qt.Horizontal)

        # --- Left pane: FileSystemTree ---
        self.log_widget = QtWidgets.QTextEdit()
        self.log_widget.setReadOnly(True)
        self.log_widget.hide()

        self.tree_wrapper = self.FileSystemTree(log_widget=self.log_widget, parent=self)
        outer_splitter.addWidget(self.tree_wrapper)

        # --- Right pane: vertical splitter for Browser + DropArea + Logs ---
        vertical_splitter = QtWidgets.QSplitter(self)
        vertical_splitter.setOrientation(QtCore.Qt.Vertical)

        # 3a) QWebEngineView to load local HTML
        self.web_view = QtWebEngineWidgets.QWebEngineView(self)
        # Construct the absolute path to drop-n-copy.html
        html_path = os.path.join(
            os.path.dirname(__file__),
            "..",  # up to gui_frontend
            "html",  # assuming you copied drop-n-copy.html here
            "drop-n-copy.html"
        )
        html_path = os.path.normpath(html_path)

        # Convert to file:// URL
        self.web_view.load(QtCore.QUrl.fromLocalFile(html_path))
        vertical_splitter.addWidget(self.web_view)

        # 3b) FileDropArea (your existing widget) below the browser
        self.drop_area = self.FileDropArea(log_widget=self.log_widget, parent=self)
        vertical_splitter.addWidget(self.drop_area)

        # 3c) Log console at the very bottom (initially hidden)
        vertical_splitter.addWidget(self.log_widget)

        # Stretch factors: give most of the space to web_view and drop_area
        vertical_splitter.setStretchFactor(0, 3)  # web_view
        vertical_splitter.setStretchFactor(1, 3)  # drop_area
        vertical_splitter.setStretchFactor(2, 1)  # logs

        outer_splitter.addWidget(vertical_splitter)
        outer_splitter.setStretchFactor(0, 1)
        outer_splitter.setStretchFactor(1, 3)

        main_layout.addWidget(outer_splitter)
        self.setLayout(main_layout)

        # 4) Set up QWebChannel so JavaScript can call into Python
        self._setup_web_channel()

        # 5) Connect tree signals
        self.tree_wrapper.tree.doubleClicked.connect(self.on_tree_double_click)
        self.drop_area.function_selected.connect(self.on_function_selected)
        self.drop_area.file_selected.connect(self.on_file_selected)

    def _toggle_logs(self, checked: bool):
        if checked:
            self.log_widget.show()
            self.toggle_logs_action.setText("Hide Logs")
            self._log("Logs shown.")
        else:
            self._log("Logs hidden.")
            self.log_widget.hide()
            self.toggle_logs_action.setText("Show Logs")

    def _setup_web_channel(self):
        """
        Expose a JSBridge object to JavaScript under the name 'pyBridge'.
        In your HTML, you can then do:
          new QWebChannel(qt.webChannelTransport, function(channel) {
              window.pyBridge = channel.objects.pyBridge;
          });
        and call `pyBridge.receiveInspectData(JSON.stringify({...}))`.
        """
        self.channel = QtWebChannel.QWebChannel(self.web_view.page())
        self.bridge = self.JSBridge(parent=self)
        self.channel.registerObject("pyBridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

    def on_tree_copy(self, paths: List[str]):
        self._log(f"Copy Selected triggered on {len(paths)} path(s).")
        self.drop_area.process_files(paths)

    def on_tree_double_click(self, index: QtCore.QModelIndex):
        model = self.tree_wrapper.model
        path = model.filePath(index)
        if path:
            self._log(f"Double-clicked: {path}")
            self.drop_area.process_files([path])

    def on_function_selected(self, function_info: dict):
        self._log(f"Function selected: {function_info['name']} from {function_info['file']}")
        self.drop_area.map_function_dependencies(function_info)

    def on_file_selected(self, file_info: dict):
        self._log(f"Python file selected: {file_info['path']}")
        self.drop_area.map_import_chain(file_info)

    def _log(self, message: str):
        """Write to the shared log widget with a timestamp."""
        timestamp = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        # You can also log to a file if you’ve set up a logger
        self.log_widget.append(f"[{timestamp}] {message}")
