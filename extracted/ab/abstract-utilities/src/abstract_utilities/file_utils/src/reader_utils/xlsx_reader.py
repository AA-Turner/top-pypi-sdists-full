"""
xlsx_reader
===========
Dependency-free reader for ``.xlsx`` (OOXML / SpreadsheetML) workbooks.

``.xlsx`` is an open format: a ZIP archive of XML parts.  This reads it with
nothing but the standard library (``zipfile`` + ``xml.etree.ElementTree``) —
no pandas, no openpyxl.  It returns plain Python values (str / int / float /
bool / None), so callers that only need the *data* pay zero third-party cost.

It does NOT attempt to reproduce the whole Excel object model (styles, formulas
as objects, charts).  It reads cell *values* — cached formula results included —
which is what a "reader" needs.  Dates are returned as their raw serial numbers
unless ``convert_dates=True`` (best-effort, based on the cell number format).
"""
import re
import zipfile
import datetime
import xml.etree.ElementTree as ET

# OOXML namespaces
_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_PKG_REL = "http://schemas.openxmlformats.org/package/2006/relationships"

_COL_RE = re.compile(r"[A-Za-z]+")

# number-format ids Excel treats as dates/times by default (built-ins)
_BUILTIN_DATE_FMTS = {14, 15, 16, 17, 18, 19, 20, 21, 22, 45, 46, 47}
_EPOCH_1900 = datetime.datetime(1899, 12, 30)  # Excel's day 0 (1900 leap bug)


def _q(ns, tag):
    return f"{{{ns}}}{tag}"


def _col_to_index(cell_ref):
    """'AB12' -> 27 (zero-based column index)."""
    m = _COL_RE.match(cell_ref or "")
    if not m:
        return 0
    idx = 0
    for ch in m.group().upper():
        idx = idx * 26 + (ord(ch) - ord("A") + 1)
    return idx - 1


def _text_of(node, ns):
    """Concatenate every <t> descendant (handles rich-text runs)."""
    return "".join(t.text or "" for t in node.iter(_q(ns, "t")))


def _read_shared_strings(zf):
    try:
        data = zf.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    root = ET.fromstring(data)
    return [_text_of(si, _MAIN) for si in root.findall(_q(_MAIN, "si"))]


def _read_date_style_flags(zf):
    """Return a list where index = cellXfs position, value = True if date-formatted."""
    try:
        data = zf.read("xl/styles.xml")
    except KeyError:
        return []
    root = ET.fromstring(data)

    # custom numFmt id -> format code
    custom = {}
    numfmts = root.find(_q(_MAIN, "numFmts"))
    if numfmts is not None:
        for nf in numfmts.findall(_q(_MAIN, "numFmt")):
            try:
                custom[int(nf.get("numFmtId"))] = (nf.get("formatCode") or "")
            except (TypeError, ValueError):
                pass

    flags = []
    cell_xfs = root.find(_q(_MAIN, "cellXfs"))
    if cell_xfs is None:
        return flags
    for xf in cell_xfs.findall(_q(_MAIN, "xf")):
        try:
            fmt_id = int(xf.get("numFmtId", "0"))
        except ValueError:
            fmt_id = 0
        is_date = fmt_id in _BUILTIN_DATE_FMTS
        if not is_date and fmt_id in custom:
            code = custom[fmt_id].lower()
            # crude but effective: date/time format codes use these tokens
            if any(tok in code for tok in ("y", "m", "d", "h", "s")) and "general" not in code:
                is_date = True
        flags.append(is_date)
    return flags


def _serial_to_datetime(serial):
    try:
        return _EPOCH_1900 + datetime.timedelta(days=float(serial))
    except (TypeError, ValueError):
        return serial


def _coerce_number(text):
    if text is None or text == "":
        return None
    try:
        f = float(text)
    except ValueError:
        return text
    i = int(f)
    return i if f == i else f


def _sheet_name_map(zf):
    """Ordered [(sheet_name, worksheet_part_path), ...] from workbook + rels."""
    try:
        wb = ET.fromstring(zf.read("xl/workbook.xml"))
        rels = ET.fromstring(zf.read("xl/_rels/workbook.xml.rels"))
    except KeyError:
        # fall back to whatever sheet parts exist
        parts = sorted(n for n in zf.namelist()
                       if n.startswith("xl/worksheets/") and n.endswith(".xml"))
        return [(f"Sheet{i+1}", p) for i, p in enumerate(parts)]

    rid_to_target = {}
    for rel in rels.findall(_q(_PKG_REL, "Relationship")):
        target = rel.get("Target") or ""
        if not target.startswith("/"):
            target = "xl/" + target.lstrip("./")
        else:
            target = target.lstrip("/")
        rid_to_target[rel.get("Id")] = target

    out = []
    sheets = wb.find(_q(_MAIN, "sheets"))
    if sheets is not None:
        for sh in sheets.findall(_q(_MAIN, "sheet")):
            name = sh.get("name") or f"Sheet{len(out)+1}"
            rid = sh.get(_q(_REL, "id"))
            target = rid_to_target.get(rid)
            if target:
                out.append((name, target))
    return out


def _read_worksheet(zf, part, shared, date_flags, convert_dates):
    root = ET.fromstring(zf.read(part))
    sheet_data = root.find(_q(_MAIN, "sheetData"))
    rows = []
    if sheet_data is None:
        return rows
    for row in sheet_data.findall(_q(_MAIN, "row")):
        cells = {}
        max_col = -1
        for c in row.findall(_q(_MAIN, "c")):
            ref = c.get("r") or ""
            col = _col_to_index(ref)
            max_col = max(max_col, col)
            ctype = c.get("t")
            v = c.find(_q(_MAIN, "v"))
            if ctype == "s":  # shared string
                idx = int(v.text) if v is not None and v.text else 0
                val = shared[idx] if 0 <= idx < len(shared) else ""
            elif ctype == "inlineStr":
                is_node = c.find(_q(_MAIN, "is"))
                val = _text_of(is_node, _MAIN) if is_node is not None else ""
            elif ctype == "str":  # formula string result
                val = v.text if v is not None else ""
            elif ctype == "b":  # boolean
                val = bool(int(v.text)) if v is not None and v.text else False
            elif ctype == "e":  # error
                val = v.text if v is not None else None
            else:  # number (or date serial)
                val = _coerce_number(v.text if v is not None else None)
                if convert_dates and val is not None:
                    try:
                        s = int(c.get("s", "0"))
                    except ValueError:
                        s = 0
                    if s < len(date_flags) and date_flags[s]:
                        val = _serial_to_datetime(val)
            cells[col] = val
        rows.append([cells.get(i) for i in range(max_col + 1)] if max_col >= 0 else [])
    return rows


def read_xlsx(path, sheet=None, as_dicts=False, convert_dates=False):
    """Read an ``.xlsx`` workbook using only the standard library.

    Args:
        path:          path to the .xlsx file.
        sheet:         sheet name or zero-based index. Default ``None`` reads
                       the first sheet.
        as_dicts:      if True, use the first row as headers and return a list
                       of dicts; otherwise a list of row-lists.
        convert_dates: best-effort convert date-formatted serials to datetime.

    Returns:
        list of rows (list of lists), or list of dicts if ``as_dicts``.
    """
    with zipfile.ZipFile(path) as zf:
        shared = _read_shared_strings(zf)
        date_flags = _read_date_style_flags(zf) if convert_dates else []
        names = _sheet_name_map(zf)
        if not names:
            return []
        if sheet is None:
            _, part = names[0]
        elif isinstance(sheet, int):
            _, part = names[sheet]
        else:
            match = [p for (n, p) in names if n == sheet]
            if not match:
                raise KeyError(f"sheet {sheet!r} not found; have {[n for n, _ in names]}")
            part = match[0]
        rows = _read_worksheet(zf, part, shared, date_flags, convert_dates)

    if as_dicts:
        if not rows:
            return []
        header = [("" if h is None else str(h)) for h in rows[0]]
        out = []
        for r in rows[1:]:
            out.append({header[i] if i < len(header) else f"col{i}":
                        (r[i] if i < len(r) else None) for i in range(len(header))})
        return out
    return rows


def read_xlsx_all_sheets(path, as_dicts=False, convert_dates=False):
    """Return ``{sheet_name: rows}`` for every sheet in the workbook."""
    with zipfile.ZipFile(path) as zf:
        shared = _read_shared_strings(zf)
        date_flags = _read_date_style_flags(zf) if convert_dates else []
        names = _sheet_name_map(zf)
        result = {}
        for name, part in names:
            rows = _read_worksheet(zf, part, shared, date_flags, convert_dates)
            if as_dicts and rows:
                header = [("" if h is None else str(h)) for h in rows[0]]
                rows = [
                    {header[i] if i < len(header) else f"col{i}":
                     (r[i] if i < len(r) else None) for i in range(len(header))}
                    for r in rows[1:]
                ]
            result[name] = rows
    return result


__all__ = ["read_xlsx", "read_xlsx_all_sheets"]
