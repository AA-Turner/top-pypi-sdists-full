# table_factory_headers_config.py
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QLabel, QWidget, QAbstractItemView, QHeaderView
from PyQt6.QtCore import Qt
from abstract_utilities import is_number
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


