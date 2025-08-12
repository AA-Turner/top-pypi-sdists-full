# controller.py
import asyncio
from PyQt5 import QtCore, QtWidgets
import sys


from abstract_ai import ApiManager,ModelManager,PromptManager,InstructionManager,ResponseManager

import json
import openai

class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 1) Build and show the GUI
        self.gui = MainWindow()
        self.gui.show()

        # 2) Instantiate managers
        self.instruction_mgr = InstructionManager()
        self.model_mgr = ModelManager(default_selection=True)
        self.prompt_mgr = PromptManager(
            instruction_mgr=self.instruction_mgr,
            model_mgr=self.model_mgr
        )
        self.api_mgr = ApiManager()
        self.response_mgr = ResponseManager(
            prompt_mgr=self.prompt_mgr,
            api_mgr=self.api_mgr
        )
        self.window_mgr = WindowManager(self.gui)
        self.navigation_mgr = NavigationManager()
        self.history_mgr = HistoryManager()

        # 3) Initialize data structures
        self.instruction_data_list = self.instruction_mgr.create_empty_instruction_list()
        self.instruction_pre_keys = list(self.instruction_mgr.default_instructions.keys())
        self.prompt_data_list = [""] * 10
        self.request_data_list = [""] * 10
        self.script_event_js = {"found": None, "section": None}
        self.display_number_tracker = {
            "request": 0,
            "prompt_data": 0,
            "chunk_number": 0,
            "query": 0,
            "chunk_section_number": 0,
        }

        # Chunk-related defaults
        self.chunk_display_keys = ["-CHUNK_TEXT-", "-CHUNK_TOKEN_COUNT-", "-CHUNK_TOKEN_PERCENTAGE-"]
        self.sectioned_chunk_data_key = "-CHUNK_TEXT-"
        self.chunk_history_name = "PROMPT_DATA_HISTORY"
        self.request_history_name = "REQUEST_DATA_HISTORY"
        self.chunk_type = None
        self.url_chunk_type = "URL"
        self.token_percentage_dropdowns = ["-PROMPT_PERCENTAGE-", "-COMPLETION_PERCENTAGE-"]
        self.instruction_bool_keys = [text_to_key(k, section="BOOL") for k in self.instruction_pre_keys]

        # 4) Set up asyncio event loop for PyQt5
        self.loop = asyncio.get_event_loop()
        if not self.loop.is_running():
            self.loop.run_until_complete(asyncio.sleep(0))

        # 5) Wire up signals
        self._wire_instruction_signals()
        self._wire_prompt_signals()
        self._wire_output_signals()
        self._wire_settings_signals()

        # 6) Initialize model selection in GUI
        self._update_model_combo()

    def _update_model_combo(self):
        """Populate model combo box with available models."""
        model_combo = self.gui.utilities_tabs.findChild(QtWidgets.QComboBox, None, options=QtCore.Qt.FindChildrenRecursively)
        if model_combo and hasattr(self.model_mgr, 'all_model_names'):
            model_combo.clear()
            model_combo.addItems(self.model_mgr.all_model_names)
            current_model = self.model_mgr.selected_model_name
            model_combo.setCurrentText(current_model)

    def _wire_instruction_signals(self):
        """Wire signals for instruction checkboxes and text fields."""
        for key in self.instruction_pre_keys:
            bool_key = text_to_key(text=key, section="BOOL")
            text_key = text_to_key(text=key, section="TEXT")

            checkbox = self.window_mgr.get_widget(bool_key, widget_type=QtWidgets.QCheckBox)
            if checkbox:
                checkbox.toggled.connect(lambda checked, k=key: self._on_instruction_bool_changed(k))

            if key in self.instruction_mgr.default_instructions:
                text_edit = self.window_mgr.get_widget(text_key, widget_type=QtWidgets.QTextEdit)
                if text_edit:
                    text_edit.textChanged.connect(lambda k=key: self._on_instruction_text_changed(k))

        main_instr_cb = self.window_mgr.get_widget(text_to_key("instructions", section="BOOL"), QtWidgets.QCheckBox)
        if main_instr_cb:
            main_instr_cb.toggled.connect(self.update_instruction_mgr)

    def _wire_prompt_signals(self):
        """Wire signals for prompt and request text edits."""
        request_edit = self.gui.prompt_tabs.findChild(QtWidgets.QTextEdit, "request_data")
        if request_edit:
            request_edit.textChanged.connect(self._on_request_text_changed)

        prompt_data_edit = self.gui.prompt_tabs.findChild(QtWidgets.QTextEdit, "prompt_data_data")
        if prompt_data_edit:
            prompt_data_edit.textChanged.connect(self._on_prompt_data_text_changed)

        add_query_btn = self.window_mgr.get_widget("-ADD_QUERY-", QtWidgets.QPushButton)
        if add_query_btn:
            add_query_btn.clicked.connect(self._on_add_query)

    def _wire_output_signals(self):
        """Wire signals for output option buttons."""
        for btn in self.gui.output_options.findChildren(QtWidgets.QPushButton):
            text = btn.text().upper()
            if text == "SUBMIT QUERY":
                btn.clicked.connect(self.on_submit_query)
            elif text == "CLEAR CHUNKS":
                btn.clicked.connect(self.on_clear_chunks)
            elif text == "CLEAR REQUESTS":
                btn.clicked.connect(self.on_clear_requests)
            elif text == "GEN README":
                btn.clicked.connect(self.on_gen_readme)

    def _wire_settings_signals(self):
        """Wire signals for settings tab, e.g., model selection and token percentage."""
        settings_tab = self.gui.utilities_tabs.findChild(QtWidgets.QScrollArea)
        if settings_tab:
            model_combo = settings_tab.findChild(QtWidgets.QComboBox, None, options=QtCore.Qt.FindChildrenRecursively)
            if model_combo:
                model_combo.currentTextChanged.connect(self._on_model_changed)

            token_combos = settings_tab.findChildren(QtWidgets.QComboBox)
            for combo in token_combos:
                if combo.objectName() in self.token_percentage_dropdowns:
                    combo.currentTextChanged.connect(self._on_token_percentage_changed)

    def _on_instruction_bool_changed(self, key: str):
        self.update_instruction_mgr()
        self._update_prompt_manager()

    def _on_instruction_text_changed(self, key: str):
        self.update_instruction_mgr()
        self._update_prompt_manager()

    def _on_request_text_changed(self):
        self.update_request_data_list()
        self.update_query_display()
        self._update_prompt_manager()
        self.fill_lists()

    def _on_prompt_data_text_changed(self):
        self.update_prompt_data_list()
        self.update_query_display()
        self._update_prompt_manager()
        self.fill_lists()

    def _on_add_query(self):
        self.event = "-ADD_QUERY-"
        self.prompt_request_event_check()
        self.fill_lists()

    def _on_model_changed(self, model_name: str):
        self.model_mgr.selected_model_name = model_name
        self.model_mgr.selected_endpoint = self.model_mgr._get_endpoint_by_model(model_name)
        self.model_mgr.selected_max_tokens = self.model_mgr._get_max_tokens_by_model(model_name)
        self._update_prompt_manager()
        self.statusBar().showMessage(f"Model changed to {model_name}", 3000)

    def _on_token_percentage_changed(self):
        completion_combo = self.window_mgr.get_widget("-COMPLETION_PERCENTAGE-", QtWidgets.QComboBox)
        if completion_combo:
            completion_percentage = int(completion_combo.currentText())
            self.prompt_mgr.update_request_and_prompt_data(
                completion_percentage=completion_percentage
            )
            self.statusBar().showMessage(f"Completion percentage set to {completion_percentage}%", 2000)

    def _update_prompt_manager(self):
        """Update PromptManager with current GUI data."""
        request_edit = self.gui.prompt_tabs.findChild(QtWidgets.QTextEdit, "request_data")
        prompt_data_edit = self.gui.prompt_tabs.findChild(QtWidgets.QTextEdit, "prompt_data_data")
        request_data = request_edit.toPlainText() if request_edit else ""
        prompt_data = prompt_data_edit.toPlainText() if prompt_data_edit else ""
        self.prompt_mgr.update_request_and_prompt_data(
            model_mgr=self.model_mgr,
            instruction_mgr=self.instruction_mgr,
            request_data=[request_data],
            prompt_data=[prompt_data],
            instruction_data=[self.instruction_mgr.get_instructions()],
        )
        self.response_mgr.prompt_mgr = self.prompt_mgr

    async def _async_submit_query(self):
        """Asynchronously submit query using ResponseManager."""
        try:
            outputs = await self.response_mgr.initial_query()
            for output in outputs:
                response_content = output.get("response", {}).get("choices", [{}])[0].get("message", {}).get("content", "")
                if isinstance(response_content, str):
                    try:
                        response_content = json.loads(response_content)
                    except json.JSONDecodeError:
                        pass

                response_edit = self.gui.utilities_tabs.findChild(QtWidgets.QTextEdit, "response_edit")
                if response_edit:
                    response_edit.clear()
                    response_edit.setPlainText(json.dumps(response_content, indent=2) if isinstance(response_content, dict) else str(response_content))

                self.last_response_content = output
                self.delegate_instruction_text()

            self.statusBar().showMessage("Query submitted successfully.", 3000)
        except Exception as e:
            self.statusBar().showMessage(f"Query Error: {str(e)}", 5000)

    def on_submit_query(self):
        """Handle Submit Query button click."""
        final_prompt = self.window_mgr.get_from_value("-QUERY-")
        if not final_prompt:
            self.statusBar().showMessage("No prompt to submit.", 3000)
            return

        # Run async query in the event loop
        asyncio.ensure_future(self._async_submit_query())

    def on_clear_chunks(self):
        self.event = "-CLEAR_CHUNKS-"
        self.chunk_event_check()
        self.statusBar().showMessage("Chunks cleared.", 2000)

    def on_clear_requests(self):
        self.request_data_list = [""] * 10
        self.update_request_data_display()
        self._update_prompt_manager()
        self.statusBar().showMessage("Requests cleared.", 2000)

    def on_gen_readme(self):
        # Placeholder for GEN README functionality
        self.statusBar().showMessage("Generating README (not implemented).", 2000)

    # Mixed-in methods from instruction_management.py
    update_instruction_mgr = update_instruction_mgr
    update_bool_instructions = update_bool_instructions
    restore_instruction_defaults = restore_instruction_defaults
    delegate_instruction_text = delegate_instruction_text
    instruction_event_check = instruction_event_check

    # Mixed-in methods from prompt_management.py
    update_prompt_mgr = update_prompt_mgr
    sanitize_prompt_and_request_data = sanitize_prompt_and_request_data
    get_prompt_data_section_number = get_prompt_data_section_number
    get_chunk_token_distribution_number = get_chunk_token_distribution_number
    get_chunk_number = get_chunk_number
    get_spec_section_number_display = get_spec_section_number_display
    update_request_data_list = update_request_data_list
    update_request_data_display = update_request_data_display
    update_prompt_data_list = update_prompt_data_list
    update_prompt_data_display = update_prompt_data_display
    prompt_request_event_check = prompt_request_event_check
    get_adjusted_number = get_adjusted_number
    update_prompt_data = update_prompt_data
    update_request_data = update_request_data
    update_query_display = update_query_display
    update_chunk_info = update_chunk_info
    add_to_chunk = add_to_chunk
    chunk_event_check = chunk_event_check

    def fill_lists(self):
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())

