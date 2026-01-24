import sys

from PyQt6.QtCore import QPySequenceRange, QPyTableRange, QRangeModel, Qt
from PyQt6.QtWidgets import (QApplication, QGridLayout, QLabel, QListView,
        QTableView, QTreeView, QVBoxLayout, QWidget)


class ViewContainer(QVBoxLayout):
    """ A container for a view. """

    def __init__(self, title, py_range, parent=None):
        """ Initialise the view. """

        super().__init__(parent)

        self._py_range = py_range

        if isinstance(py_range, QPySequenceRange):
            py_range.dataChanged.connect(self._on_sequence_changed)
            view = QListView()

        if isinstance(py_range, QPyTableRange):
            py_range.dataChanged.connect(self._on_table_changed)
            view = QTableView()
            view.horizontalHeader().setVisible(False)
            view.verticalHeader().setVisible(False)

        model = QRangeModel(py_range)
        view.setModel(model)
        view.selectionModel().currentChanged.connect(
                self._on_selection_changed)

        self._data_view = QLabel()

        self.addWidget(
                QLabel(f'<b>{title}</b>',
                        alignment=Qt.AlignmentFlag.AlignHCenter))
        self.addWidget(view)
        self.addWidget(self._data_view)

    def _on_selection_changed(self, current, _):
        """ Handle the changed selection. """

        self._set_data_view(current.row(), current.column())

    def _on_sequence_changed(self, index):
        """ Handle the changed Python sequence. """

        self._set_data_view(index)

    def _on_table_changed(self, row, column):
        """ Handle the changed Python table. """

        self._set_data_view(row, column)

    def _set_data_view(self, row, column=-1):
        """ Set the view of an element from the Python data. """

        datum = self._py_range.data()[row]
        if isinstance(self._py_range, QPyTableRange):
            datum = datum[column]

        self._data_view.setText(f"Selected data: {repr(datum)}")


# Instances of this type are unknown to PyQt.
class Data:
    """ Wrap an arbitrary Python object. """

    def __init__(self, data):
        """ Initialise the object. """

        self._data = data

    def __str__(self):
        """ Return a string representation of the data to be used in views. """

        return str(self._data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    gallery = QWidget()
    layout = QGridLayout()

    ro_seq_data = QPySequenceRange(
            ("Foo", 1, True, 5.6, Data("A string"), Data(100)))
    layout.addLayout(ViewContainer("Read-only Sequence", ro_seq_data), 0, 0)

    fixed_seq_data = QPySequenceRange(["Cat", 9, False], editable=True)
    layout.addLayout(ViewContainer("Fixed Size Sequence", fixed_seq_data), 0,
            1)

    ro_table_data = QPyTableRange(
            (
                ("Foo", 1, True, 5.6, Data("A string"), Data(100)),
                ("Bar", 2, False, 6.6, Data("Another string"), Data(200)),
            ))
    layout.addLayout(ViewContainer("Read-only Table", ro_table_data), 1, 0)

    fixed_table_data = QPyTableRange(
            (
                ["Cat", 9, False],
                ["Dog", 1, True],
            ),
            editable=True)
    layout.addLayout(ViewContainer("Fixed Size Table", fixed_table_data), 1, 1)

    gallery.setLayout(layout)
    gallery.resize(1400, 600)
    gallery.show()

    sys.exit(app.exec())
