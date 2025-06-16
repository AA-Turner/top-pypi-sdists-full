# controller.py

from PyQt5 import QtCore, QtWidgets
       # The PyQt5 GUI skeleton
              # Same for prompt manager
#from abstract_ai.gpt_classes.gpt_manager.dependencies import InstructionManager, PromptManager, WindowManager, NavigationManager, HistoryManager, ModelManager
                                                 # Update these imports according to your actual project structure
from abstract_ai.gpt_classes.gpt_manager.instruction_section import * 
#from abstract_ai.gpt_classes.gpt_manager.prompt_section import * 
#from abstract_ai.gpt_classes.gpt_manager.response_section import * 
#from abstract_ai.gpt_classes.gpt_manager.test_section import * 
#from abstract_ai.gpt_classes.gpt_manager.url_section import * 
#from abstract_ai.gpt_classes.gpt_manager.window_section import * 
class Controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 1) Instantiate the GUI
        self.gui = MainWindow()
        self.gui.show()

        # 2) Instantiate all managers / dependencies:
        self.instruction_mgr = InstructionManager()   # your own instruction‐manager class
        self.model_mgr = ModelManager()               # your own model‐manager class
        self.prompt_mgr = PromptManager()             # your own prompt‐manager class
        self.window_mgr = WindowManager(self.gui)     # wraps around gui for get_from_value/update_value
        self.navigation_mgr = NavigationManager()
        self.history_mgr = HistoryManager()

        # 3) Initialize data structures (mirroring what your original classes expect)
        self.instruction_data_list = self.instruction_mgr.create_empty_instruction_list()  # or however you init
        self.instruction_pre_keys = list(self.instruction_mgr.default_instructions.keys())
        self.prompt_data_list = [""] * 10            # allocate as many sections as you need
        self.request_data_list = [""] * 10
        self.script_event_js = {"found": None, "section": None}
        self.display_number_tracker = {
            "request": 0,
            "prompt_data": 0,
            "chunk_number": 0,
            "query": 0,
            "chunk section number": 0
        }
        self.chunk_display_keys = ["-CHUNK_TEXT-", "-CHUNK_TOKEN_COUNT-", "-CHUNK_TOKEN_PERCENTAGE-"]
        self.sectioned_chunk_data_key = "-CHUNK_TEXT-"
        self.chunk_history_name = "PROMPT_DATA_HISTORY"
        self.request_history_name = "REQUEST_DATA_HISTORY"
        self.chunk_type = None
        self.url_chunk_type = "URL"
        self.toke_percentage_dropdowns = ["-PROMPT_PERCENTAGE-", "-COMPLETION_PERCENTAGE-"]
        self.instruction_bool_keys = [text_to_key(k, section="BOOL") for k in self.instruction_pre_keys]

        # 4) Connect signals → instruction_management.update_instruction_mgr
        self._wire_instruction_signals()

        # 5) Connect signals → prompt_management methods
        self._wire_prompt_signals()

        # 6) Connect “Submit,” “Clear,” etc. from OutputOptionsFrame if desired
        self.gui.output_options.findChild(QtWidgets.QPushButton, "SUBMIT QUERY").clicked.connect(self.on_submit_query)
        self.gui.output_options.findChild(QtWidgets.QPushButton, "CLEAR CHUNKS").clicked.connect(self.on_clear_chunks)

    def _wire_instruction_signals(self):
        """
        Whenever any instruction‐related checkbox or text edits change, call update_instruction_mgr().
        Assume each instruction checkbox in the GUI has objectName matching text_to_key(key, section="BOOL"),
        and each text area has objectName text_to_key(key, section="TEXT").
        """
        for key in self.instruction_pre_keys:
            bool_key = text_to_key(text=key, section="BOOL")
            text_key = text_to_key(text=key, section="TEXT")

            # 1) Checkbox toggled → update instruction manager
            checkbox = self.window_mgr.get_widget(bool_key, widget_type=QtWidgets.QCheckBox)
            if checkbox:
                checkbox.toggled.connect(lambda checked, k=key: self._on_instruction_bool_changed(k))

            # 2) If the instruction has a text field, also connect textChanged
            if key in self.instruction_mgr.default_instructions:
                text_edit = self.window_mgr.get_widget(text_key, widget_type=QtWidgets.QTextEdit)
                if text_edit:
                    text_edit.textChanged.connect(lambda k=key: self._on_instruction_text_changed(k))

        # 3) If the general “instructions” checkbox itself changes, also call update_instruction_mgr
        main_instructions_cb = self.window_mgr.get_widget(text_to_key("instructions", section="BOOL"), QtWidgets.QCheckBox)
        if main_instructions_cb:
            main_instructions_cb.toggled.connect(lambda: self.update_instruction_mgr())

    def _on_instruction_bool_changed(self, key: str):
        """
        Triggered whenever one of the instruction‐check checkboxes flips.
        We simply delegate to update_instruction_mgr (from instruction_management.py).
        """
        # update the underlying boolean in data structure
        # (instruction_management.update_instruction_mgr() does this internally)
        self.update_instruction_mgr()

    def _on_instruction_text_changed(self, key: str):
        """
        Triggered whenever one of the instruction text fields changes.
        We delegate to update_instruction_mgr so it can pick up the new text.
        """
        self.update_instruction_mgr()

    def _wire_prompt_signals(self):
        """
        Connect the “request” and “prompt_data” QTextEdits and the “-ADD_QUERY-” button
        so that prompt_request_event_check() is called appropriately.
        """
        # 1) Whenever the “REQUEST” tab’s QTextEdit changes, call update_request_data_list()
        request_edit = self.gui.prompt_tabs.findChild(QtWidgets.QTextEdit, "request_data")
        if request_edit:
            request_edit.textChanged.connect(lambda: self._on_request_text_changed())

        # 2) Whenever the “PROMPT DATA” tab’s QTextEdit changes, call update_prompt_data_list()
        prompt_data_edit = self.gui.prompt_tabs.findChild(QtWidgets.QTextEdit, "prompt_data_data")
        if prompt_data_edit:
            prompt_data_edit.textChanged.connect(lambda: self._on_prompt_data_text_changed())

        # 3) The “+ Add Query” functionality (often a button in the GUI)
        add_query_btn = self.window_mgr.get_widget("-ADD_QUERY-", QtWidgets.QPushButton)
        if add_query_btn:
            add_query_btn.clicked.connect(lambda: self._on_add_query())

    def _on_request_text_changed(self):
        # update_request_data_list() comes from prompt_management.py
        self.update_request_data_list()
        self.update_query_display()
        self.fill_lists()          # if you have a method to refresh any displayed lists

    def _on_prompt_data_text_changed(self):
        self.update_prompt_data_list()
        self.update_query_display()
        self.fill_lists()

    def _on_add_query(self):
        """
        Called when user clicks “+ Add Query.” In the original prompt_management.prompt_request_event_check(),
        this triggers update_command logic. We simply call that directly.
        """
        self.event = "-ADD_QUERY-"
        self.prompt_request_event_check()
        self.fill_lists()

    def on_submit_query(self):
        """
        Handle “SUBMIT QUERY” button. Typically, you would gather the assembled prompt
        (via prompt_mgr.create_prompt(...)) and send it to the AI backend.
        """
        current_query = self.window_mgr.get_from_value("-QUERY-")
        # TODO: send current_query to your AI model, then handle response...
        print("Submitting Query:", current_query)
        # Once you get a response, you might call delegate_instruction_text() to update any UI feedback
        # e.g.:
        # self.last_response_content = ai_response_json
        # self.delegate_instruction_text()

    def on_clear_chunks(self):
        """
        Handle “CLEAR CHUNKS” button from the OutputOptionsFrame.
        This should clear all chunk‐related data from the UI.
        """
        self.event = "-CLEAR_CHUNKS-"
        # Invokes chunk_event_check() from prompt_management.py
        self.chunk_event_check()

    # ======================================
    # === Mixin Methods from Uploaded Files
    # ======================================
    #
    # The following methods come from instruction_management.py and prompt_management.py.
    # We “mix them in” by explicitly pointing to them here. Alternatively, you could subclass
    # a common base class that already has them. For clarity, we list them as methods of Controller.
    #
    # --- instruction_management.py methods:
    update_instruction_mgr = update_instruction_mgr
    update_bool_instructions = update_bool_instructions
    restore_instruction_defaults = restore_instruction_defaults
    delegate_instruction_text = delegate_instruction_text
    instruction_event_check = instruction_event_check

    # --- prompt_management.py methods:
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

    # You may also need to provide stubs (or import) for:
    #   - fill_lists()
    #   - navigation_mgr.parse_navigation_event, etc.
    #   - text_to_key(), get_any_value(), safe_json_loads()
    #   - self.last_response_content (for delegate_instruction_text)

    def fill_lists(self):
        """
        Refresh any QListWidget or other “list” UI elements that depend on
        the current request_data_list / prompt_data_list. Implement as needed.
        """
        pass


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
