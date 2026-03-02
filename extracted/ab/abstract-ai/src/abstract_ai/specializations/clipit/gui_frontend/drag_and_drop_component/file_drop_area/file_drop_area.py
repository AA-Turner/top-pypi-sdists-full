import inspect
from PyQt5 import QtWidgets, QtCore

# 1) Constructor signature(s)
print(inspect.signature(QtWidgets.QListWidgetItem.__init__))
# e.g. __init__(self, *args, **kwargs)  # overloaded under the hood

# 2) All public members (methods, signals, properties, …)
all_members = [m for m in dir(QtWidgets.QListWidgetItem) if not m.startswith('_')]
print("All members:", all_members)

# 3) Which of those are callables?
methods = [m for m in all_members
           if callable(getattr(QtWidgets.QListWidgetItem, m))]
print("Methods & signals:", methods)

# 4) Which are non-callable properties?
props = [m for m in all_members
         if not callable(getattr(QtWidgets.QListWidgetItem, m))]
print("Attributes/properties:", props)

# 5) If you want to know what “roles” you can pass to item.data()/setData():
roles = [(name, getattr(QtCore.Qt, name))
         for name in dir(QtCore.Qt) if name.endswith('Role')]
print("Data roles:", roles)
from ..imports import *
logger = get_logFile('clipit_logs')


class FileDropArea(QtWidgets.QWidget):
    function_selected = QtCore.pyqtSignal(dict)
    file_selected     = QtCore.pyqtSignal(dict)

    def __init__(self, log_widget: QtWidgets.QTextEdit, parent=None):
        super().__init__(parent)

        # ─── Ensure the parent accepts drops ────────────────────────────────
        self.setAcceptDrops(True)

        self.log_widget = log_widget

        # Map ".ext" → QCheckBox
        self.ext_checks: dict[str, QtWidgets.QCheckBox] = {}
        self._last_raw_paths: list[str] = []
        self.functions: list[dict] = []
        self.python_files: list[dict] = []
        self.allowed_extensions = {
            '.py', '.txt', '.md', '.csv', '.tsv', '.log',
            '.xls', '.xlsx', '.ods', '.parquet', '.geojson', '.shp'
        }

        # ─── Main vertical layout ─────────────────────────────────────────
        lay = QtWidgets.QVBoxLayout(self)

        # 1) “Browse Files…” button
        browse_btn = get_push_button(text="Browse Files…",action=self.browse_files)

        # 2) Extension‐filter row
        self.ext_row = QtWidgets.QScrollArea(widgetResizable=True)
        self.ext_row.setFixedHeight(45)
        self.ext_row.setVisible(False)
        self.ext_row_w = QtWidgets.QWidget()
        self.ext_row.setWidget(self.ext_row_w)
        self.ext_row_lay = QtWidgets.QHBoxLayout(self.ext_row_w)
        self.ext_row_lay.setContentsMargins(4, 4, 4, 4)
        self.ext_row_lay.setSpacing(10)


        # 3) Tab widget to switch between “List View” and “Text View”
        self.view_tabs = QtWidgets.QTabWidget()


        # ─── 3a) List View Tab ─────────────────────────────────────────────
        list_tab = QtWidgets.QWidget()
        list_layout = get_layout(parent=list_tab)

        # Function list (QListWidget) inside List View
        self.function_list = QtWidgets.QListWidget()
        self.function_list.setVisible(False)
        self.function_list.setAcceptDrops(False)  # ensure drops go to parent
        self.function_list.itemClicked.connect(self.on_function_clicked)

        # Python file list (QListWidget) inside List View
        self.python_file_list = QtWidgets.QListWidget()
        self.python_file_list.setVisible(False)
        self.python_file_list.setAcceptDrops(False)
        self.python_file_list.itemClicked.connect(self.on_python_file_clicked)

        add_widgets(list_layout,
                    {"widget":self.python_file_list},
                    {"widget":self.function_list}
                    )


        self.view_tabs.addTab(list_tab, "List View")

        # ─── 3b) Text View Tab ─────────────────────────────────────────────
        text_tab = QtWidgets.QWidget()
        text_layout = QtWidgets.QVBoxLayout(text_tab)

        # QTextEdit for raw‐text inside Text View
        self.text_view = QtWidgets.QTextEdit()
        self.text_view.setReadOnly(True)
        self.text_view.setVisible(False)
        self.text_view.setAcceptDrops(False)  # ensure drops go to parent
        add_widgets(text_layout,
                    {"widget":self.text_view}
                    )
        self.view_tabs.addTab(text_tab, "Text View")

        # 4) Status label
        self.status = QtWidgets.QLabel("No files selected.", alignment=QtCore.Qt.AlignCenter)
        self.status.setStyleSheet("color: #333; font-size: 12px;")

        add_widgets(lay,
                    {"widget":browse_btn,"kargs":{"alignment":QtCore.Qt.AlignHCenter}},
                    {"widget":self.view_tabs},
                    {"widget":self.ext_row},
                    {"widget":self.status}
                    )
    # ────────────────────────────────────────────────────────────────────────
    # dragEnterEvent / dropEvent (parent still handles all drops)
    # ────────────────────────────────────────────────────────────────────────
    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        try:
            urls = event.mimeData().urls()
            paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
            self._log(f"Received raw drop paths: {paths!r}")

            if not paths:
                raise ValueError("No local files detected on drop.")

            filtered = self.filter_paths(paths)
            if not filtered:
                return

            self.process_files(filtered)

        except Exception as e:
            tb = traceback.format_exc()
            self.status.setText(f"⚠️ Error during drop: {e}")
            self._log(f"dropEvent ERROR:\n{tb}")

    # ────────────────────────────────────────────────────────────────────────
    # Expand directories, exclude unwanted files
    # ────────────────────────────────────────────────────────────────────────
    def filter_paths(self, paths: list[str]) -> list[str]:
        filtered = collect_filepaths(
            paths,
            exclude_dirs=set(list(DEFAULT_EXCLUDE_DIRS) + ["backups", "backup", "node_modules", "__pycache__", "logs", "log"]),
            exclude_file_patterns=['__init__', "*.zip"]
        )
        self._log(f"_filtered_file_list returned {len(filtered)} path(s): {filtered!r}")

        if not filtered:
            self.status.setText("⚠️ No valid files detected in drop.")
            self._log("No valid paths after filtering.")
            return []

        self._log(f"Proceeding to process {len(filtered)} file(s).")
        return filtered

    # ────────────────────────────────────────────────────────────────────────
    # Main processing logic: read files, then update both tabs
    # ────────────────────────────────────────────────────────────────────────
    def process_files(self, raw_paths: list[str]) -> None:
        """
        1. Expand directories → all_paths
        2. Rebuild extension row
        3. Filter by checked extensions
        4. Read & parse files
        5. Populate “List View” widgets and the “Text View” widget
        """
        self._last_raw_paths = raw_paths

        # 1) Expand directories
        all_paths = collect_filepaths(
            raw_paths,
            exclude_dirs=set(list(DEFAULT_EXCLUDE_DIRS) + ["backups", "backup", "node_modules", "__pycache__", "logs", "log"]),
            exclude_file_patterns=['__init__', "*.zip"]
        )
        self._log(f"{len(all_paths)} total path(s) after expansion")

        # 2) Rebuild extension‐filter row
        self._rebuild_ext_row(all_paths)

        # 3) Filter by checked extensions
        if self.ext_checks:
            visible_exts = {ext for ext, cb in self.ext_checks.items() if cb.isChecked()}
            self._log(f"Visible extensions: {visible_exts}")
            filtered_paths = [
                p for p in all_paths
                if os.path.isdir(p) or os.path.splitext(p)[1].lower() in visible_exts
            ]
        else:
            filtered_paths = all_paths

        if not filtered_paths:
            self.status.setText("⚠️ No files match current extension filter.")
            return

        self.status.setText(f"Reading {len(filtered_paths)} file(s)…")
        self._log(f"Reading {len(filtered_paths)} file(s)")
        QtWidgets.QApplication.processEvents()

        # 4) Read & parse each file
        combined_text_lines: list[str] = []
        self.functions = []
        self.python_files = []

        for idx, p in enumerate(filtered_paths, 1):
            combined_text_lines.append(f"=== {p} ===\n")
            try:
                text = read_file_as_text(p)
                combined_text_lines.append(text or "")
                if p.endswith('.py'):
                    self.python_files.append({'path': p, 'text': text})
                    self._parse_functions(p, text)
            except Exception as exc:
                combined_text_lines.append(f"[Error reading {os.path.basename(p)}: {exc}]\n")
                self._log(f"Error reading {p} → {exc}")

            if idx < len(filtered_paths):
                combined_text_lines.append("\n\n――――――――――――――――――\n\n")

        # 5) Populate List View and Text View
        self._populate_list_view()
        self._populate_text_view(combined_text_lines)

        self.status.setText("Files processed. Switch tabs to view.")

    # ────────────────────────────────────────────────────────────────────────
    # Rebuild the extension‐filter row
    # ────────────────────────────────────────────────────────────────────────
    def _rebuild_ext_row(self, paths: list[str]) -> None:
        exts = {os.path.splitext(p)[1].lower() for p in paths if os.path.isfile(p)}
        exts.discard("")

        if not exts:
            self.ext_row.setVisible(False)
            self.ext_checks.clear()
            return

        self._clear_layout(self.ext_row_lay)

        new_checks: dict[str, QtWidgets.QCheckBox] = {}
        for ext in sorted(exts):
            cb = QtWidgets.QCheckBox(ext)
            prev_cb = self.ext_checks.get(ext)
            cb.setChecked(prev_cb.isChecked() if prev_cb else True)
            cb.stateChanged.connect(self._apply_ext_filter)
            self.ext_row_lay.addWidget(cb)
            new_checks[ext] = cb

        self.ext_checks = new_checks
        self.ext_row.setVisible(True)

    def _apply_ext_filter(self) -> None:
        """Re‐run processing when an extension checkbox changes."""
        if self._last_raw_paths:
            self.process_files(self._last_raw_paths)

    # ────────────────────────────────────────────────────────────────────────
    # Populate the “List View” tab (two QListWidget)s
    # ────────────────────────────────────────────────────────────────────────
    def _populate_list_view(self) -> None:
        # Function list
        self.function_list.clear()
        if self.functions:
            for func in self.functions:
                self.function_list.addItem(f"{func['name']} ({func['file']})")
            self.function_list.setVisible(True)
        else:
            self.function_list.setVisible(False)

        # Python file list
        self.python_file_list.clear()
        if self.python_files:
            for file_info in self.python_files:
                self.python_file_list.addItem(os.path.basename(file_info['path']))
            self.python_file_list.setVisible(True)
        else:
            self.python_file_list.setVisible(False)

    # ────────────────────────────────────────────────────────────────────────
    # Populate the “Text View” tab (QTextEdit)
    # ────────────────────────────────────────────────────────────────────────
    def _populate_text_view(self, combined_lines: list[str]) -> None:
        if combined_lines:
            self.text_view.setPlainText("".join([str(combine) for combine in combined_lines]))
            self.text_view.setVisible(True)
        else:
            self.text_view.clear()
            self.text_view.setVisible(False)

    # ────────────────────────────────────────────────────────────────────────
    # Parse Python files for function definitions (unchanged from before)
    # ────────────────────────────────────────────────────────────────────────
    def _parse_functions(self, file_path: str, text: str) -> None:
        try:
            tree = ast.parse(text, filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_code = "\n".join(text.splitlines()[node.lineno-1:node.end_lineno])
                    imports = self._extract_imports(tree)
                    self.functions.append({
                        'name': node.name,
                        'file': file_path,
                        'line': node.lineno,
                        'code': func_code,
                        'imports': imports
                    })
        except SyntaxError as e:
            self._log(f"Syntax error in {file_path}: {e}")

    def _extract_imports(self, tree: ast.AST) -> list[str]:
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"from {module} import {alias.name}")
        return imports

    # ────────────────────────────────────────────────────────────────────────
    # Handle clicks in “List View” tab
    # ────────────────────────────────────────────────────────────────────────
    def on_function_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        index = self.function_list.row(item)
        function_info = self.functions[index]
        self.function_selected.emit(function_info)

    def on_python_file_clicked(self, item: QtWidgets.QListWidgetItem) -> None:
        index = self.python_file_list.row(item)
        file_info = self.python_files[index]
        self.file_selected.emit(file_info)

    # ────────────────────────────────────────────────────────────────────────
    # Copy function dependencies to clipboard (unchanged)
    # ────────────────────────────────────────────────────────────────────────
    def map_function_dependencies(self, function_info: dict) -> None:
        combined_lines = []
        combined_lines.append(f"=== Function: {function_info['name']} ===\n")
        combined_lines.append(function_info['code'])
        combined_lines.append("\n\n=== Imports ===\n")
        combined_lines.extend(function_info['imports'])

        project_files = collect_filepaths(
            [os.path.dirname(function_info['file'])],
            exclude_dirs=DEFAULT_EXCLUDE_DIRS,
            exclude_file_patterns=DEFAULT_EXCLUDE_FILE_PATTERNS
        )
        combined_lines.append("\n\n=== Project Reach ===\n")
        for file_path in project_files:
            if file_path != function_info['file'] and file_path.endswith('.py'):
                combined_lines.append(f"--- {file_path} ---\n")
                try:
                    text = read_file_as_text(file_path)
                    combined_lines.append(text)
                except Exception as exc:
                    combined_lines.append(f"[Error reading {os.path.basename(file_path)}: {exc}]\n")
                combined_lines.append("\n")

        QtWidgets.QApplication.clipboard().setText("\n".join(combined_lines))
        self.status.setText(f"✅ Copied function {function_info['name']} and dependencies to clipboard!")
        self._log(f"Copied function {function_info['name']} with dependencies")

    # ────────────────────────────────────────────────────────────────────────
    # Copy import chain to clipboard (unchanged)
    # ────────────────────────────────────────────────────────────────────────
    def map_import_chain(self, file_info: dict) -> None:
        try:
            module_paths, imports = get_py_script_paths([file_info['path']])
            combined_lines = []
            combined_lines.append(f"=== Import Chain for {file_info['path']} ===\n")
            combined_lines.append("Modules:\n")
            if module_paths:
                combined_lines.extend(f"- {p}" for p in module_paths)
            else:
                combined_lines.append("- None\n")
            combined_lines.append("\nImports:\n")
            if imports:
                combined_lines.extend(f"- {imp}" for imp in imports)
            else:
                combined_lines.append("- None\n")

            QtWidgets.QApplication.clipboard().setText("\n".join(combined_lines))
            self.status.setText(f"✅ Copied import chain for {os.path.basename(file_info['path'])} to clipboard!")
            self._log(f"Copied import chain for {file_info['path']}")
        except Exception as e:
            tb = traceback.format_exc()
            self.status.setText(f"⚠️ Error mapping import chain: {e}")
            self._log(f"map_import_chain ERROR:\n{tb}")

    # ────────────────────────────────────────────────────────────────────────
    # “Browse Files…” button
    # ────────────────────────────────────────────────────────────────────────
    def browse_files(self) -> None:
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Select Files to Copy",
            "",
            "All Supported Files (" + " ".join(f"*{ext}" for ext in self.allowed_extensions) + ");;All Files (*)"
        )
        if files:
            filtered = self.filter_paths(files)
            if filtered:
                self.process_files(filtered)

    # ────────────────────────────────────────────────────────────────────────
    # Logging helper
    # ────────────────────────────────────────────────────────────────────────
    def _log(self, message: str) -> None:
        timestamp = QtCore.QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        logger.info(f"[{timestamp}] {message}")
        self.log_widget.append(f"[{timestamp}] {message}")

    # ────────────────────────────────────────────────────────────────────────
    # Clear a QLayout recursively
    # ────────────────────────────────────────────────────────────────────────
    def _clear_layout(self, layout: QtWidgets.QLayout) -> None:
        if layout is None:
            return
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
