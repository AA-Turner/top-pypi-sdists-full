from PyQt5 import QtWidgets, QtCore
import sys
from abstract_webtools import *
from abstract_utilities.class_utils import *
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

        # Signals
        self.add_url_btn.clicked.connect(self.add_url_to_list)
        self.get_source_btn.clicked.connect(self.on_get_source_click)
        self.get_soup_btn.clicked.connect(self.on_get_soup_click)
    def add_url_to_list(self):
        url = self.url_input.text().strip()
        if url:
            self.url_listbox.addItem(url)
            self.url_input.clear()
    def get_selected_url(self):
        selected_items = self.url_listbox.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

    def on_get_source_click(self):
        url = self.get_selected_url()
        if url:
            result = get_source(url)
            self.url_text_edit.setPlainText(result)
        else:
            QtWidgets
    def on_get_soup_click(self):
        url = self.get_selected_url()
        if url:
            result = get_soup('https://example.com')
            input(result)
            self.url_text_edit.setPlainText(result)
        else:
            QtWidgets
# Entry point
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    urls_tab = UrlsTab()
    window.setCentralWidget(urls_tab)
    window.setWindowTitle("URL Manager")
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec_())

soup_mgr = soupManager('https://example.com')
all_tags_and_attribute = soup_mgr.get_all_tags_and_attribute_names()
all_tags = all_tags_and_attribute.get('tags')
all_attributes = all_tags_and_attribute.get('attributes')
for tag in all_tags:
    input(soup_mgr.soup.find_all(tag))
