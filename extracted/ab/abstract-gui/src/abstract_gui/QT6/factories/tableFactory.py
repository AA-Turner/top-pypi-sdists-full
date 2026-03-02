# table_factory_headers_config.py
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QAbstractItemView, QHeaderView
from PyQt6.QtCore import Qt

# --- small utility: enum resolver by name or pass-through ---
def _enum_from_name(enum_cls, name_or_enum):
    if isinstance(name_or_enum, enum_cls):
        return name_or_enum
    if name_or_enum is None:
        return None
    key = str(name_or_enum).replace(" ", "").replace("-", "").replace("_", "").lower()
    for m in enum_cls:  # iterate members
        if m.name.replace("_", "").lower() == key:
            return m
    raise ValueError(f"Unknown {enum_cls.__name__} member: {name_or_enum!r}")

def _normalize_headers_and_data(
    data: Optional[Iterable],
    headers: Optional[Sequence[str]]
) -> Tuple[List[str], List[List[str]]]:
    data = list(data or [])
    if not data:
        return list(headers or []), []
    if isinstance(data[0], dict):
        if not headers:
            first = list(data[0].keys())
            seen = set(first)
            extra = []
            for row in data[1:]:
                for k in row.keys():
                    if k not in seen:
                        extra.append(k); seen.add(k)
            headers = first + extra
        rows = [[str(d.get(h, "")) for h in headers] for d in data]
        return list(headers), rows
    # list/tuple rows
    if not headers:
        width = max(len(r) for r in data)
        headers = [f"Col {i}" for i in range(width)]
    width = len(headers)
    rows = [[str(r[i]) if i < len(r) else "" for i in range(width)] for r in data]
    return list(headers), rows

def set_table_data(table: QTableWidget, data: Iterable, headers: Optional[Sequence[str]] = None):
    headers, rows = _normalize_headers_and_data(data, headers)
    table.blockSignals(True)
    table.clear()
    table.setColumnCount(len(headers))
    if headers:
        table.setHorizontalHeaderLabels(headers)
    table.setRowCount(len(rows))
    for r, row in enumerate(rows):
        for c, text in enumerate(row):
            table.setItem(r, c, QTableWidgetItem(text))
    table.blockSignals(False)

def createTable(
    parent: QWidget,
    *,
    layout: Optional[QVBoxLayout] = None,
    label: Optional[str] = None,
    attr_name: Optional[str] = None,
    headers: Optional[Sequence[str]] = None,
    headers_config: Optional[Dict[str, Dict[str, Any]]] = None,
    data: Optional[Iterable] = None,
    selection_behavior: QAbstractItemView.SelectionBehavior = QAbstractItemView.SelectionBehavior.SelectRows,
    selection_mode: QAbstractItemView.SelectionMode = QAbstractItemView.SelectionMode.SingleSelection,
    edit_triggers: QAbstractItemView.EditTrigger = (
        QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.EditKeyPressed
    ),
    resize_mode_default: QHeaderView.ResizeMode = QHeaderView.ResizeMode.ResizeToContents,
    stretch_last_section: bool = False,
    props: Optional[Dict[str, Any]] = None,
    connect: Optional[Any] = None,
    connect_signals_names: Optional[List[str]] = None,
    prepend_widget: bool = True,
    **kwargs
) -> QTableWidget:
    # local imports to match your project layout
    from abstract_utilities import make_list
    from .properties_resolver import apply_properties
    from .auto_signals import connect_signals

    layout = layout or QVBoxLayout(parent)
    if label:
        layout.addWidget(QLabel(label))

    table = QTableWidget()
    table.setSelectionBehavior(selection_behavior)
    table.setSelectionMode(selection_mode)
    table.setEditTriggers(edit_triggers)
    table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    # If headers_config provided, derive headers order from dict keys (ordered)
    if headers_config:
        headers = list(headers_config.keys())

    # Seed data
    if data is not None or headers is not None:
        set_table_data(table, data or [], headers=headers)

    # Column-level header config
    hh = table.horizontalHeader()
    if headers_config:
        for col, name in enumerate(headers or []):
            cfg = headers_config.get(name, {})
            # horizontalHeader resize mode
            mode = cfg.get("horizontalHeader")
            if mode is not None:
                mode_enum = _enum_from_name(QHeaderView.ResizeMode, mode)
                hh.setSectionResizeMode(col, mode_enum)
            else:
                hh.setSectionResizeMode(col, resize_mode_default)
            # explicit width
            if "ColumnWidth" in cfg and isinstance(cfg["ColumnWidth"], int):
                table.setColumnWidth(col, int(cfg["ColumnWidth"]))
        # stretch last if asked or keep caller default
        hh.setStretchLastSection(stretch_last_section)
    else:
        # simple default if no per-column config
        hh.setSectionResizeMode(resize_mode_default)
        hh.setStretchLastSection(stretch_last_section)

    if props:
        apply_properties(table, props)

    if not attr_name:
        base = (label or "table").strip().lower().replace(" ", "_").replace(":", "")
        attr_name = f"{base}_table"
    setattr(parent, attr_name, table)

    if connect:
        names = connect_signals_names or [
            "itemSelectionChanged", "currentCellChanged",
            "cellActivated", "cellClicked", "cellDoubleClicked",
            "itemChanged", "cellChanged",
            "customContextMenuRequested",
        ]
        if isinstance(connect, dict):
            kw = dict(connect)
            kw.setdefault("signals", names)
            kw.setdefault("prepend_widget", prepend_widget)
            kw.setdefault("allow_missing", True)
            connect_signals(table, **(kw))
        elif isinstance(connect, list):
            for c in connect:
                if isinstance(c, dict):
                    kw = dict(c)
                    kw.setdefault("signals", names)
                    kw.setdefault("prepend_widget", prepend_widget)
                    kw.setdefault("allow_missing", True)
                    connect_signals(table, **kw)
                else:
                    connect_signals(table, callbacks=c, signals=names,
                                    prepend_widget=prepend_widget, allow_missing=True)
        else:
            connect_signals(table, callbacks=connect, signals=names,
                            prepend_widget=prepend_widget, allow_missing=True)

    layout.addWidget(table)
    return table
