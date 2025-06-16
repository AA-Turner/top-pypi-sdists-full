# pyqt_gui.py

from PyQt5 import QtCore, QtGui, QtWidgets


class ProgressFrame(QtWidgets.QGroupBox):
    def __init__(self, parent=None):
        super().__init__("PROGRESS", parent)
        layout = QtWidgets.QHBoxLayout()

        # Progress Text (read-only QLineEdit)
        self.progress_text = QtWidgets.QLineEdit("Awaiting Prompt")
        self.progress_text.setReadOnly(True)
        self.progress_text.setFixedHeight(24)
        self.progress_text.setMinimumWidth(200)

        # Progress Bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setFixedHeight(24)
        self.progress_bar.setMaximumWidth(100)

        # Query Count (read-only QLineEdit)
        self.query_count = QtWidgets.QLineEdit("0")
        self.query_count.setReadOnly(True)
        self.query_count.setFixedHeight(24)
        self.query_count.setMinimumWidth(50)

        # Query Title Frame with QLineEdit
        title_frame = QtWidgets.QFrame()
        title_layout = QtWidgets.QHBoxLayout(title_frame)
        title_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.query_title = QtWidgets.QLineEdit("title of prompt")
        self.query_title.setFixedHeight(24)
        self.query_title.setMinimumWidth(200)
        title_layout.addWidget(self.query_title)

        # Response Nav Frame: back, number, forward
        resp_nav_frame = QtWidgets.QFrame()
        resp_nav_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        resp_nav_layout = QtWidgets.QHBoxLayout(resp_nav_frame)
        self.resp_back_btn = QtWidgets.QPushButton("<-")
        self.resp_number = QtWidgets.QLineEdit("0")
        self.resp_number.setFixedWidth(40)
        self.resp_forward_btn = QtWidgets.QPushButton("->")
        self.resp_back_btn.setFixedHeight(24)
        self.resp_number.setFixedHeight(24)
        self.resp_forward_btn.setFixedHeight(24)
        resp_nav_layout.addWidget(self.resp_back_btn)
        resp_nav_layout.addWidget(self.resp_number)
        resp_nav_layout.addWidget(self.resp_forward_btn)

        # Assemble layouts
        left_layout = QtWidgets.QVBoxLayout()
        row1 = QtWidgets.QHBoxLayout()
        row1.addWidget(self.progress_text)
        row1.addWidget(self.progress_bar)
        row1.addWidget(self.query_count)
        left_layout.addLayout(row1)

        row2 = QtWidgets.QHBoxLayout()
        row2.addWidget(title_frame)
        row2.addWidget(resp_nav_frame)
        left_layout.addLayout(row2)

        self.setLayout(left_layout)


class OutputOptionsFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setSpacing(20)

        btn_submit = QtWidgets.QPushButton("SUBMIT QUERY")
        btn_clear_requests = QtWidgets.QPushButton("CLEAR REQUESTS")
        btn_clear_chunks = QtWidgets.QPushButton("CLEAR CHUNKS")
        btn_gen_readme = QtWidgets.QPushButton("GEN README")

        for btn in (btn_submit, btn_clear_requests, btn_clear_chunks, btn_gen_readme):
            btn.setFixedHeight(32)
            btn.setMinimumWidth(120)
            layout.addWidget(btn)

        # Optional: connect signals here, e.g.
        # btn_submit.clicked.connect(self.on_submit)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setLayout(layout)


class NavigationBar(QtWidgets.QWidget):
    def __init__(self, name: str, section: bool = True, parent=None):
        super().__init__(parent)
        nav_layout = QtWidgets.QHBoxLayout(self)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        push_spacer1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        nav_layout.addItem(push_spacer1)

        label = name.upper() + (" SECTION" if section else "")
        self.back_btn = QtWidgets.QPushButton("<-")
        self.number_edit = QtWidgets.QLineEdit("0")
        self.number_edit.setFixedWidth(40)
        self.forward_btn = QtWidgets.QPushButton("->")
        for widget in (self.back_btn, self.number_edit, self.forward_btn):
            widget.setFixedHeight(24)
            nav_layout.addWidget(widget)

        push_spacer2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        nav_layout.addItem(push_spacer2)
        self.setLayout(nav_layout)


class PromptTab(QtWidgets.QWidget):
    def __init__(self, title: str, with_subsection: bool = False, parent=None):
        super().__init__(parent)
        v_layout = QtWidgets.QVBoxLayout(self)
        # Section navigation
        v_layout.addWidget(NavigationBar(title, section=True))
        if with_subsection:
            v_layout.addWidget(NavigationBar(title, section=False))
        # Data frame for multiline text
        frame = QtWidgets.QGroupBox(f"{title} DATA")
        frame_layout = QtWidgets.QVBoxLayout(frame)
        self.text_edit = QtWidgets.QTextEdit()
        frame_layout.addWidget(self.text_edit)
        v_layout.addWidget(frame)
        self.setLayout(v_layout)


class InstructionsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v_layout = QtWidgets.QVBoxLayout(self)
        # Section navigation
        v_layout.addWidget(NavigationBar("instructions", section=True))
        # Main instructions frame (with two sections: boolean text and sub_layout)
        frame = QtWidgets.QGroupBox("INSTRUCTIONS")
        frame_layout = QtWidgets.QVBoxLayout(frame)

        # Upper row: multiline for "instructions"
        self.instructions_edit = QtWidgets.QTextEdit()
        self.instructions_edit.setPlaceholderText("instructions")
        frame_layout.addWidget(self.instructions_edit)

        # Lower row: other boolean instruction fields
        sub_layout_widget = QtWidgets.QWidget()
        sub_layout = QtWidgets.QGridLayout(sub_layout_widget)
        instruction_keys = [
            "additional_responses", "suggestions", "abort", "database_query",
            "notation", "generate_title", "additional_instruction", "request_chunks", "prompt_as_previous", "token_adjustment"
        ]
        for idx, key in enumerate(instruction_keys):
            checkbox = QtWidgets.QCheckBox(key.replace('_', ' ').title())
            row = idx // 2
            col = idx % 2
            sub_layout.addWidget(checkbox, row, col)
        frame_layout.addWidget(sub_layout_widget)

        v_layout.addWidget(frame)
        self.setLayout(v_layout)


class PromptTabsWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create and add tabs
        self.addTab(PromptTab("request", with_subsection=False), "REQUEST")
        self.addTab(PromptTab("prompt_data", with_subsection=False), "PROMPT DATA")
        self.addTab(PromptTab("chunks", with_subsection=True), "CHUNKS")
        self.addTab(PromptTab("query", with_subsection=True), "QUERY")
        self.addTab(InstructionsTab(), "INSTRUCTIONS")


class SettingsTab(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(widget)

        # Token Percentage Frame
        token_frame = QtWidgets.QGroupBox("Token Percentage")
        token_layout = QtWidgets.QGridLayout(token_frame)
        token_keys = ['prompt percentage', 'completion percentage']
        for i, key in enumerate(token_keys):
            label = QtWidgets.QLabel(key.title())
            combo = QtWidgets.QComboBox()
            combo.addItems([str(i) for i in range(0, 101)])
            combo.setCurrentText("50")
            token_layout.addWidget(label, i, 0)
            token_layout.addWidget(combo, i, 1)
        grid.addWidget(token_frame, 0, 0, 1, 2)

        # API Options Frame
        api_frame = QtWidgets.QGroupBox("API Options")
        api_layout = QtWidgets.QFormLayout(api_frame)
        api_keys = ["Header", "API Key", "API Env"]
        for key in api_keys:
            line_edit = QtWidgets.QLineEdit()
            api_layout.addRow(key + ":", line_edit)
        grid.addWidget(api_frame, 1, 0, 1, 2)

        # Type Options Frame
        type_frame = QtWidgets.QGroupBox("Type Options")
        type_layout = QtWidgets.QFormLayout(type_frame)
        # Role combo
        role_combo = QtWidgets.QComboBox()
        roles = ['assistant', 'Elaborative', 'Socratic', 'Concise', 'Friendly/Conversational',
                 'Professional/Formal', 'Role-Playing', 'Teaching', "Debative/Devil's Advocate",
                 'Creative/Brainstorming', 'Empathetic/Supportive']
        role_combo.addItems(roles)
        type_layout.addRow("Role:", role_combo)
        # Response type combo
        resp_combo = QtWidgets.QComboBox()
        resp_combo.addItems(['instruction', 'json', 'bash', 'text'])
        type_layout.addRow("Response Type:", resp_combo)
        grid.addWidget(type_frame, 2, 0, 1, 2)

        # Prompt Options Frame (just one checkbox)
        prompt_frame = QtWidgets.QGroupBox("Prompt Options")
        prompt_layout = QtWidgets.QHBoxLayout(prompt_frame)
        self.prompt_as_received_cb = QtWidgets.QCheckBox("Prompt As Received")
        self.prompt_as_received_cb.setChecked(True)
        prompt_layout.addWidget(self.prompt_as_received_cb)
        grid.addWidget(prompt_frame, 3, 0, 1, 2)

        # Tokens Frame (display only)
        tokens_frame = QtWidgets.QGroupBox("Tokens")
        tokens_layout = QtWidgets.QVBoxLayout(tokens_frame)
        for label_text in ['completion tokens available', 'completion tokens desired', 'completion tokens used']:
            sub_frame = QtWidgets.QFrame()
            sub_layout = QtWidgets.QHBoxLayout(sub_frame)
            label = QtWidgets.QLabel(label_text.title())
            line_edit = QtWidgets.QLineEdit("0")
            line_edit.setReadOnly(True)
            line_edit.setFixedWidth(60)
            sub_layout.addWidget(label)
            sub_layout.addWidget(line_edit)
            tokens_layout.addWidget(sub_frame)
        grid.addWidget(tokens_frame, 4, 0, 1, 2)

        # Title Frame
        title_frame = QtWidgets.QGroupBox("Title")
        title_layout = QtWidgets.QHBoxLayout(title_frame)
        self.title_bool_cb = QtWidgets.QCheckBox("Title")
        self.title_bool_cb.setChecked(True)
        self.title_input = QtWidgets.QLineEdit()
        title_layout.addWidget(self.title_bool_cb)
        title_layout.addWidget(self.title_input)
        grid.addWidget(title_frame, 5, 0, 1, 2)

        # Model Select Frame
        model_frame = QtWidgets.QGroupBox("Model Select")
        model_layout = QtWidgets.QFormLayout(model_frame)
        self.endpoint_input = QtWidgets.QLineEdit()
        self.endpoint_input.setReadOnly(True)
        model_layout.addRow("Endpoint:", self.endpoint_input)
        self.model_combo = QtWidgets.QComboBox()
        # Placeholder items; in practice populate from ModelManager
        self.model_combo.addItems(["model1", "model2", "model3"])
        model_layout.addRow("Model:", self.model_combo)
        self.max_tokens_display = QtWidgets.QLineEdit("8200")
        self.max_tokens_display.setReadOnly(True)
        model_layout.addRow("Tokens:", self.max_tokens_display)
        grid.addWidget(model_frame, 6, 0, 1, 2)

        # Enable Instructions Frame (checkboxes grid)
        instr_frame = QtWidgets.QGroupBox("Enable Instructions")
        instr_layout = QtWidgets.QGridLayout(instr_frame)
        instruction_keys = ["instructions", "additional_responses", "suggestions", "abort",
                            "database_query", "notation", "generate_title", "additional_instruction", "request_chunks", "prompt_as_previous", "token_adjustment"]
        for idx, key in enumerate(instruction_keys):
            cb = QtWidgets.QCheckBox(key.replace('_', ' ').title())
            if key in ['instructions', 'generate_title', 'suggestions']:
                cb.setChecked(True)
            row = idx // 4
            col = idx % 4
            instr_layout.addWidget(cb, row, col)
        grid.addWidget(instr_frame, 7, 0, 1, 2)

        # Test Tools Frame
        test_frame = QtWidgets.QGroupBox("Test Tools")
        test_layout = QtWidgets.QHBoxLayout(test_frame)
        self.test_run_cb = QtWidgets.QCheckBox("test run")
        self.test_file_cb = QtWidgets.QCheckBox("test files")
        self.test_file_input = QtWidgets.QLineEdit()
        self.test_browse_btn = QtWidgets.QPushButton("Browse")
        test_layout.addWidget(self.test_run_cb)
        test_layout.addWidget(self.test_file_cb)
        test_layout.addWidget(self.test_file_input)
        test_layout.addWidget(self.test_browse_btn)
        grid.addWidget(test_frame, 8, 0, 1, 2)

        # File Options Frame
        file_frame = QtWidgets.QGroupBox("File Options")
        file_layout = QtWidgets.QVBoxLayout(file_frame)
        for key in ['auto chunk title', 'reuse chunk data', 'append chunks', 'scan mode all']:
            cb = QtWidgets.QCheckBox(key.replace('_', ' ').title())
            file_layout.addWidget(cb)
        grid.addWidget(file_frame, 9, 0, 1, 2)

        widget.setLayout(grid)
        self.setWidget(widget)
        self.setWidgetResizable(True)


class ResponsesTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v_layout = QtWidgets.QVBoxLayout(self)
        # Collate Responses & JSON to String checkboxes
        h_layout = QtWidgets.QHBoxLayout()
        self.collate_cb = QtWidgets.QCheckBox("Collate Responses")
        self.json_to_string_cb = QtWidgets.QCheckBox("JSON to String")
        h_layout.addWidget(self.collate_cb)
        h_layout.addWidget(self.json_to_string_cb)

        # Response Key Combo Box
        self.response_key_combo = QtWidgets.QComboBox()
        key_frame = QtWidgets.QGroupBox("Response Key")
        key_layout = QtWidgets.QHBoxLayout(key_frame)
        key_layout.addWidget(self.response_key_combo)

        v_layout.addLayout(h_layout)
        v_layout.addWidget(key_frame)

        # File text multiline
        self.file_text_edit = QtWidgets.QTextEdit()
        self.file_text_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        v_layout.addWidget(self.file_text_edit)

        self.setLayout(v_layout)


class FilesTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v_layout = QtWidgets.QVBoxLayout(self)

        # Chunk title input
        title_layout = QtWidgets.QHBoxLayout()
        self.chunk_title_input = QtWidgets.QLineEdit()
        title_layout.addWidget(QtWidgets.QLabel("Chunk Title:"))
        title_layout.addWidget(self.chunk_title_input)
        v_layout.addLayout(title_layout)

        # Buttons: CHUNK_DATA, RESPONSE_DATA
        btn_layout = QtWidgets.QHBoxLayout()
        self.chunk_data_btn = QtWidgets.QPushButton("CHUNK_DATA")
        self.response_data_btn = QtWidgets.QPushButton("RESPONSE_DATA")
        btn_layout.addWidget(self.chunk_data_btn)
        btn_layout.addWidget(self.response_data_btn)
        v_layout.addLayout(btn_layout)

        # File text multiline
        self.file_text_edit = QtWidgets.QTextEdit()
        self.file_text_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        v_layout.addWidget(self.file_text_edit)

        self.setLayout(v_layout)


class QueryTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v_layout = QtWidgets.QVBoxLayout(self)

        # Database Query & Perform Query checkboxes
        h_layout = QtWidgets.QHBoxLayout()
        self.database_query_cb = QtWidgets.QCheckBox("Database Query")
        self.perform_query_cb = QtWidgets.QCheckBox("Perform Query")
        h_layout.addWidget(self.database_query_cb)
        h_layout.addWidget(self.perform_query_cb)
        v_layout.addLayout(h_layout)

        # Table configuration combo
        table_frame = QtWidgets.QFrame()
        table_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        table_layout = QtWidgets.QHBoxLayout(table_frame)
        self.table_combo = QtWidgets.QComboBox()
        # Placeholder: populate with actual table names
        self.table_combo.addItems(["table1", "table2", "table3"])
        table_layout.addWidget(QtWidgets.QLabel("Table:"))
        table_layout.addWidget(self.table_combo)
        v_layout.addWidget(table_frame)

        # Buttons: CHUNK_DATA, RESPONSE_DATA
        btn_layout = QtWidgets.QHBoxLayout()
        self.chunk_data_btn = QtWidgets.QPushButton("CHUNK_DATA")
        self.response_data_btn = QtWidgets.QPushButton("RESPONSE_DATA")
        btn_layout.addWidget(self.chunk_data_btn)
        btn_layout.addWidget(self.response_data_btn)
        v_layout.addLayout(btn_layout)

        # File text multiline
        self.file_text_edit = QtWidgets.QTextEdit()
        self.file_text_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        v_layout.addWidget(self.file_text_edit)

        self.setLayout(v_layout)


class UrlsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v_layout = QtWidgets.QVBoxLayout(self)

        # URL input and button
        url_input_layout = QtWidgets.QHBoxLayout()
        self.url_input = QtWidgets.QLineEdit()
        self.add_url_btn = QtWidgets.QPushButton("Add URL")
        url_input_layout.addWidget(self.url_input)
        url_input_layout.addWidget(self.add_url_btn)
        v_layout.addLayout(url_input_layout)

        # URL listbox
        self.url_listbox = QtWidgets.QListWidget()
        v_layout.addWidget(self.url_listbox)

        # GET SOUP, GET SOURCE, CHUNK_DATA buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.get_soup_btn = QtWidgets.QPushButton("GET SOUP")
        self.get_source_btn = QtWidgets.QPushButton("GET SOURCE")
        self.chunk_data_btn = QtWidgets.QPushButton("CHUNK_DATA")
        btn_layout.addWidget(self.get_soup_btn)
        btn_layout.addWidget(self.get_source_btn)
        btn_layout.addWidget(self.chunk_data_btn)
        v_layout.addLayout(btn_layout)

        # Chunk title input
        chunk_title_frame = QtWidgets.QFrame()
        chunk_title_layout = QtWidgets.QHBoxLayout(chunk_title_frame)
        self.chunk_title_input = QtWidgets.QLineEdit()
        chunk_title_layout.addWidget(QtWidgets.QLabel("Chunk Title:"))
        chunk_title_layout.addWidget(self.chunk_title_input)
        v_layout.addWidget(chunk_title_frame)

        # URL text multiline
        self.url_text_edit = QtWidgets.QTextEdit()
        self.url_text_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        v_layout.addWidget(self.url_text_edit)

        self.setLayout(v_layout)


class FeedbackTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QtWidgets.QVBoxLayout(self)

        # Response Frame
        response_frame = QtWidgets.QGroupBox("Response")
        response_layout = QtWidgets.QVBoxLayout(response_frame)
        self.response_edit = QtWidgets.QTextEdit()
        self.response_edit.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        response_layout.addWidget(self.response_edit)
        main_layout.addWidget(response_frame)

        # Other feedback fields
        fields = ["request_chunks", "abort", "additional_responses", "suggestions", "notation", "other"]
        for field in fields:
            frame = QtWidgets.QGroupBox(field.replace('_', ' ').title())
            layout = QtWidgets.QVBoxLayout(frame)
            if field in ["request_chunks", "abort", "additional_responses"]:
                line = QtWidgets.QLineEdit()
                layout.addWidget(line)
            else:
                multiline = QtWidgets.QTextEdit()
                multiline.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                layout.addWidget(multiline)
            main_layout.addWidget(frame)

        self.setLayout(main_layout)


class UtilitiesTabsWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addTab(SettingsTab(), "SETTINGS")
        self.addTab(ResponsesTab(), "RESPONSES")
        self.addTab(FilesTab(), "FILES")
        self.addTab(QueryTab(), "QUERY")
        self.addTab(UrlsTab(), "URLS")
        self.addTab(FeedbackTab(), "FEEDBACK")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatGPT Console")
        self.resize(1200, 800)

        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setSpacing(20)

        # 1) Progress Frame
        self.progress_frame = ProgressFrame()
        main_layout.addWidget(self.progress_frame)

        # 2) Output Options
        self.output_options = OutputOptionsFrame()
        main_layout.addWidget(self.output_options)

        # 3) Main horizontal split: Prompt Tabs (left) + Utilities Tabs (right)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Prompt Tabs
        self.prompt_tabs = PromptTabsWidget()
        splitter.addWidget(self.prompt_tabs)

        # Utilities Tabs
        self.utilities_tabs = UtilitiesTabsWidget()
        splitter.addWidget(self.utilities_tabs)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        main_layout.addWidget(splitter)

        self.setCentralWidget(central_widget)

        # Optional: status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

main()

