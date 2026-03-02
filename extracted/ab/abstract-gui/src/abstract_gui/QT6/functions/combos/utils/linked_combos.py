# utils_linked_combos.py
from types import SimpleNamespace
from PyQt6.QtWidgets import (
    QHBoxLayout, QLabel, QComboBox, QCompleter
)
from PyQt6.QtCore import Qt

def build_linked_combos(
    mapping: dict,
    *,
    into_layout: QHBoxLayout | None = None,
    type_label: str = "TYPE",
    value_label: str = "Value",
    include_any: bool = True,
    value_source: str = "keys",     # 'keys' (e.g., extensions) or 'values' (e.g., MIME strings)
    editable_value: bool = True,
    case_insensitive: bool = True,
    initial_type: str | None = None,
    initial_value: str | None = None,
):
    """
    Create two linked QComboBoxes:
      - TYPE chooses a category from `mapping` (e.g., 'image', 'video', ...).
      - Value shows only values for that category; blank TYPE shows all values.
    Returns a SimpleNamespace with fields:
      row, type_box, value_box, selection(), set_selection(cat,val), rebuild()
    """

    row = QHBoxLayout()

    # TYPE
    row.addWidget(QLabel(type_label))
    type_box = QComboBox()
    type_box.setEditable(False)
    type_box.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
    if include_any:
        type_box.addItem("")  # blank = Any
    type_box.addItems(sorted(map(str, mapping.keys())))
    row.addWidget(type_box)

    # Value
    row.addWidget(QLabel(value_label))
    value_box = QComboBox()
    value_box.setEditable(editable_value)
    value_box.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
    value_box.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

    # optional completer (over dropdown items)
    comp = QCompleter(value_box.model())
    comp.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive if case_insensitive
                            else Qt.CaseSensitivity.CaseSensitive)
    value_box.setCompleter(comp)

    row.addWidget(value_box)

    # ----- helpers ----------------------------------------------------------
    def _values_for(cat: str | None) -> list[str]:
        """Return the allowed values for a category; if None -> union across all."""
        def _vals_of(c):
            data = mapping.get(c, [])
            if isinstance(data, dict):
                seq = data.keys() if value_source == "keys" else data.values()
            elif isinstance(data, (set, list, tuple)):
                seq = data
            else:
                seq = [data]
            return [str(x) for x in seq]

        if not cat:  # Any -> flatten all
            acc = []
            for c in mapping.keys():
                acc.extend(_vals_of(c))
            # unique + sorted
            return sorted(dict.fromkeys(acc))
        return sorted(dict.fromkeys(_vals_of(cat)))

    def rebuild():
        keep = value_box.currentText()
        cat = (type_box.currentText() or "").strip() or None
        options = _values_for(cat)

        value_box.blockSignals(True)
        value_box.clear()
        value_box.addItems(options)
        # refresh completer model
        value_box.completer().setModel(value_box.model())
        # restore custom entry if needed
        if keep and keep not in options and editable_value:
            value_box.setEditText(keep)
        value_box.blockSignals(False)

    def selection():
        t = (type_box.currentText() or "").strip() or None
        v = (value_box.currentText() or "").strip() or None
        return t, v

    def set_selection(cat: str | None = None, val: str | None = None):
        if cat is not None:
            type_box.setCurrentText(cat)
            rebuild()
        if val is not None:
            if editable_value and value_box.findText(val) == -1:
                value_box.setEditText(val)
            else:
                value_box.setCurrentText(val)

    # wire up
    type_box.currentTextChanged.connect(lambda _=None: rebuild())

    # initial state
    if initial_type:
        type_box.setCurrentText(initial_type)
    rebuild()
    if initial_value:
        set_selection(val=initial_value)

    if into_layout is not None:
        into_layout.addLayout(row)

    return SimpleNamespace(
        row=row,
        type_box=type_box,
        value_box=value_box,
        selection=selection,
        set_selection=set_selection,
        rebuild=rebuild,
    )
