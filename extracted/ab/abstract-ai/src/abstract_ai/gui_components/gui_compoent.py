import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QProgressBar, QGroupBox, QPushButton, QCheckBox, QComboBox, QTextEdit, QTabWidget,
    QListWidget, QFileDialog, QTreeWidget, QTreeWidgetItem, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QImage
from io import BytesIO
import requests
from PIL import Image

# Utility functions adapted from original
def ensure_nested_list(obj):
    if not isinstance(obj, list):
        return [obj]
    return obj

def expandable(size=(None, None), scroll_vertical=False, scroll_horizontal=False):
    # In PyQt, we can use size policies or fixed sizes; return dict for params
    params = {}
    if size[0]:
        params['fixed_width'] = size[0]
    if size[1]:
        params['fixed_height'] = size[1]
    return params

def text_to_key(text, section=''):
    return f"-{text.upper().replace(' ', '_')}{f'_{section.upper()}' if section else ''}-"

# Mock classes from original (simplified)
class AbstractWindowManager:
    def __init__(self):
        pass

class AbstractBrowser:
    def get_scan_browser_layout(self, section='', extra_buttons=[]):
        # Simplified browser layout: file browser with list and buttons
        layout_widget = QWidget()
        v_layout = QVBoxLayout()
        layout_widget.setLayout(v_layout)

        file_list = QListWidget()
        file_list.setObjectName(text_to_key('file list', section=section))
        v_layout.addWidget(file_list)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(lambda: self.browse_files(file_list))
        v_layout.addWidget(browse_btn)

        for btn in extra_buttons:
            v_layout.addWidget(btn)

        return [layout_widget]  # Return as list for consistency

    def browse_files(self, list_widget):
        files = QFileDialog.getOpenFileNames()[0]
        for file in files:
            list_widget.addItem(file)

class RightClickManager:
    def get_right_click(self, key=''):
        # Context menu simulation; return None as PyQt handles via setContextMenuPolicy
        return None

right_click_mgr = RightClickManager()

# Widget creation function (replacement for make_component)
def make_widget(widget_type, parent=None, **kwargs):
    widget = None
    if widget_type == "Button":
        widget = QPushButton(kwargs.get("button_text", "Button"), parent)
        if 'disabled' in kwargs:
            widget.setEnabled(not kwargs['disabled'])
    elif widget_type == "Input":
        widget = QLineEdit(kwargs.get("default_text", ""), parent)
        if 'disabled' in kwargs:
            widget.setReadOnly(kwargs['disabled'])
        if 'size' in kwargs:
            w, h = kwargs['size']
            widget.setFixedSize(w * 10, h * 20)  # Approximate
    elif widget_type == "InputText":
        return make_widget("Input", parent, **kwargs)
    elif widget_type == "ProgressBar":
        widget = QProgressBar(parent)
        widget.setMaximum(100)
        if 'size' in kwargs:
            w, h = kwargs['size']
            widget.setFixedSize(w * 10, h * 20)
    elif widget_type == "Frame":
        widget = QGroupBox(kwargs.get("title", ""), parent)
        inner_layout = QVBoxLayout()
        widget.setLayout(inner_layout)
        if 'layout' in kwargs:
            build_layout(kwargs['layout'], inner_layout)
    elif widget_type == "Checkbox":
        widget = QCheckBox(kwargs.get("title", ""), parent)
        if 'default' in kwargs:
            widget.setChecked(kwargs['default'])
    elif widget_type == "Combo":
        widget = QComboBox(parent)
        if 'values' in kwargs:
            widget.addItems([str(v) for v in kwargs['values']])
        if 'default_value' in kwargs:
            widget.setCurrentText(str(kwargs['default_value']))
        if 'size' in kwargs:
            w, h = kwargs['size']
            widget.setFixedSize(w * 10, h * 20)
    elif widget_type == "Multiline":
        widget = QTextEdit(parent)
        if 'size' in kwargs:
            w, h = kwargs['size']
            widget.setFixedSize(w * 10, h * 20)
        # Simulate right-click if needed
        widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
    elif widget_type == "TabGroup":
        widget = QTabWidget(parent)
        if 'layout' in kwargs:
            for tab in ensure_nested_list(kwargs['layout']):
                tab_widget = QWidget()
                tab_layout = QVBoxLayout()
                tab_widget.setLayout(tab_layout)
                build_layout(tab.get('layout', []), tab_layout)
                widget.addTab(tab_widget, tab.get('title', 'Tab'))
    elif widget_type == "Tab":
        # Return dict for TabGroup
        return {'title': kwargs.get("title", "").upper(), 'layout': ensure_nested_list(kwargs.get("layout", []))}
    elif widget_type == "Column":
        widget = QWidget(parent)
        col_layout = QVBoxLayout()
        widget.setLayout(col_layout)
        if 'layout' in kwargs:
            build_layout(kwargs['layout'], col_layout)
    elif widget_type == "Text":
        widget = QLabel(kwargs.get("title", ""), parent)
    elif widget_type == "Listbox":
        widget = QListWidget(parent)
        if 'values' in kwargs:
            for v in kwargs['values']:
                widget.addItem(str(v))
        if 'size' in kwargs:
            w, h = kwargs['size']
            widget.setFixedSize(w * 10, h * 20)
    elif widget_type == "Tree":
        widget = QTreeWidget(parent)
        if 'headings' in kwargs:
            widget.setHeaderLabels(kwargs['headings'])
    else:
        raise ValueError(f"Unknown widget type: {widget_type}")

    if 'key' in kwargs:
        widget.setObjectName(kwargs['key'])

    # Apply expandable params
    if 'expandable' in kwargs:
        params = kwargs['expandable']
        if 'fixed_width' in params:
            widget.setFixedWidth(params['fixed_width'])
        if 'fixed_height' in params:
            widget.setFixedHeight(params['fixed_height'])

    return widget

# Build layout from nested list
def build_layout(layout_list, parent_layout):
    for row in ensure_nested_list(layout_list):
        row_layout = QHBoxLayout()
        for element in ensure_nested_list(row):
            if isinstance(element, list):
                col_widget = QWidget()
                col_layout = QVBoxLayout()
                col_widget.setLayout(col_layout)
                build_layout(element, col_layout)
                row_layout.addWidget(col_widget)
            else:
                row_layout.addWidget(element)
        parent_layout.addLayout(row_layout)

# Adapted functions from gui_utils.py and others
def get_standard_screen_dimensions(width=0.70, height=0.80):
    screen = QApplication.primaryScreen()
    rect = screen.availableGeometry()
    return int(rect.width() * width), int(rect.height() * height)

window_width, window_height = get_standard_screen_dimensions()

def get_left_right_nav(name, section=True, push=True):
    insert = f"{name} {'section ' if section else ''}"
    back_btn = make_widget("Button", button_text="<-", key=text_to_key(f"{insert}back"))
    number_input = make_widget("Input", default_text='0', key=text_to_key(f"{insert}number"), size=(4,1))
    forward_btn = make_widget("Button", button_text="->", key=text_to_key(f"{insert}forward"))

    nav_widget = QWidget()
    nav_layout = QHBoxLayout()
    nav_widget.setLayout(nav_layout)

    if push:
        nav_layout.addStretch()

    nav_layout.addWidget(back_btn)
    nav_layout.addWidget(number_input)
    nav_layout.addWidget(forward_btn)

    if push:
        nav_layout.addStretch()

    return nav_widget

def generate_bool_text(title, args={}):
    frame = make_widget("Frame", title=title)
    inner_layout = frame.layout()
    multi = make_widget("Multiline", key=text_to_key(title, section='text'), **args)
    inner_layout.addWidget(multi)
    return frame

def get_tab_layout(title, layout=None):
    if not layout:
        layout = make_widget("Multiline", key=text_to_key(title), **expandable(size=(None, 5)))
    tab_dict = make_widget("Tab", title=title, layout=layout)
    return tab_dict

def get_column(layout, args={}):
    col = make_widget("Column", layout=layout, **args)
    return col

def get_tab_group(grouped_tabs, args={}):
    tab_group = make_widget("TabGroup", layout=grouped_tabs, **args)
    return tab_group

def get_right_click_multi(key, args={}):
    multi = make_widget("Multiline", key=key, **args)
    return multi

# From progress_frame.py
def get_progress_frame():
    progress_widget = QWidget()
    h_layout = QHBoxLayout()
    progress_widget.setLayout(h_layout)

    # PROGRESS frame
    progress_group = make_widget("Frame", title='PROGRESS')
    progress_inner = QHBoxLayout()
    progress_group.layout().addLayout(progress_inner)

    progress_text = make_widget("Input", default_text='Awaiting Prompt', key='-PROGRESS_TEXT-', size=(20, 20))
    progress_text.setStyleSheet("background-color: light blue;")
    progress_bar = make_widget("ProgressBar", key='-PROGRESS-', size=(10, 20))
    query_count = make_widget("Input", default_text='0', key=text_to_key("query count"), size=(30, 20), disabled=True)

    progress_inner.addWidget(progress_text)
    progress_inner.addWidget(progress_bar)
    progress_inner.addWidget(query_count)

    h_layout.addWidget(progress_group)

    # query title frame
    query_title_group = make_widget("Frame", title='query title')
    query_title_inner = QHBoxLayout()
    query_title_group.layout().addLayout(query_title_inner)

    title_input = make_widget("Input", default_text="title of prompt", key=text_to_key('title input'), size=(30, 1))

    query_title_inner.addWidget(title_input)
    h_layout.addWidget(query_title_group)

    # response nav frame
    response_nav_group = make_widget("Frame", title="response nav")
    response_nav_inner = QHBoxLayout()
    response_nav_group.layout().addLayout(response_nav_inner)

    nav = get_left_right_nav(name='response text', section=False, push=False)
    response_nav_inner.addWidget(nav)

    h_layout.addWidget(response_nav_group)

    return progress_widget

def get_output_options():
    options_widget = QWidget()
    h_layout = QHBoxLayout()
    options_widget.setLayout(h_layout)

    submit_btn = make_widget("Button", button_text="SUBMIT QUERY", key="-SUBMIT_QUERY-")
    clear_requests = make_widget("Button", button_text="CLEAR REQUESTS", key='-CLEAR_REQUESTS-')
    clear_chunks = make_widget("Button", button_text="CLEAR CHUNKS", key='-CLEAR_CHUNKS-')
    gen_readme = make_widget("Button", button_text="GEN README", key='-GENERATE_README-')

    h_layout.addWidget(submit_btn)
    h_layout.addWidget(clear_requests)
    h_layout.addWidget(clear_chunks)
    h_layout.addWidget(gen_readme)

    return options_widget

# From prompt_tabs.py
prompt_tab_keys = ['request', 'prompt data', 'chunks', 'query', 'instructions']

def get_prompt_tabs(layout_specs={}, args={}):
    tab_group = make_widget("TabGroup", **args)

    for key in prompt_tab_keys:
        layout = layout_specs.get(key, [])
        tab = get_tab_layout(key, layout)
        tab_widget = QWidget()
        tab_layout = QVBoxLayout()
        tab_widget.setLayout(tab_layout)
        build_layout(tab['layout'], tab_layout)
        tab_group.addTab(tab_widget, tab['title'])

    return tab_group

def get_chunked_sections():
    chunk_widget = QWidget()
    v_layout = QVBoxLayout()
    chunk_widget.setLayout(v_layout)

    v_layout.addWidget(get_left_right_nav(name='chunk'))
    v_layout.addWidget(get_left_right_nav(name='chunk', section=False))

    frame = make_widget("Frame", title="chunk data")
    multi = get_right_click_multi(key=text_to_key('chunk sectioned data'), args={"enable_events":True, **expandable()})
    frame.layout().addWidget(multi)
    v_layout.addWidget(frame)

    return chunk_widget

def get_prompt_data_section():
    pd_widget = QWidget()
    v_layout = QVBoxLayout()
    pd_widget.setLayout(v_layout)

    v_layout.addWidget(get_left_right_nav(name='prompt_data'))

    frame = make_widget("Frame", title='prompt data')
    multi = get_right_click_multi(key=text_to_key('prompt_data data'), args={"enable_events":True, **expandable()})
    frame.layout().addWidget(multi)
    v_layout.addWidget(frame)

    return pd_widget

# Similarly for other sections...
# (To save space, implement similar for get_request_section, get_query_section, get_instructions)

# From gui_utilities.py (partial)
def utilities():
    tab_group = make_widget("TabGroup", **expandable(size=(int(0.4*window_width), window_height)))

    # Add tabs for SETTINGS, RESPONSES, Files, QUERY, urls, feedback
    # Implement each as QWidget with layout

    # Example for SETTINGS
    settings_tab = QWidget()
    settings_layout = QVBoxLayout()
    settings_tab.setLayout(settings_layout)
    # Add content from get_settings()
    tab_group.addTab(settings_tab, "SETTINGS")

    # Add other tabs similarly...

    return tab_group

# Main total layout from abstract_ai_gui_shared.py
def get_total_layout():
    main_widget = QWidget()
    main_layout = QVBoxLayout()
    main_widget.setLayout(main_layout)

    main_layout.addWidget(get_progress_frame())
    main_layout.addWidget(get_output_options())

    h_layout = QHBoxLayout()
    main_layout.addLayout(h_layout)

    # Prompt tabs with specs
    layouts = {"query": get_query_section(), "request": get_request_section(), "prompt data": get_prompt_data_section(),
               "instructions": get_instructions(), "chunks": get_chunked_sections()}
    prompt = get_prompt_tabs(layouts, args=expandable(size=(int(0.2*window_width), window_height)))
    h_layout.addWidget(prompt)

    util_col = get_column([utilities()])
    h_layout.addWidget(util_col)

    return main_widget

# Other functions like env_section, swap_commands, currentTokenInfo, etc., can be converted similarly.

# Main app
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Abstract AI GUI - PyQt Version")
        self.setGeometry(100, 100, window_width, window_height)

        central_widget = get_total_layout()
        self.setCentralWidget(central_widget)

        # Connect signals as needed (e.g., buttons to functions)
        # Example: find button by objectName and connect

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
