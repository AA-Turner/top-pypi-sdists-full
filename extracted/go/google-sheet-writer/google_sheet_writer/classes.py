import time
from collections import defaultdict
from typing import Callable, NamedTuple, Optional, TypeVar

from gspread.cell import Cell
from gspread.utils import (
    a1_range_to_grid_range,
    absolute_range_name,
    rowcol_to_a1,
)
from gspread_formatting import (
    BooleanCondition,
    CellFormat,
    Color,
    ColorStyle,
    DataValidationRule,
    TextFormat,
    batch_updater,
    get_conditional_format_rules,
)

WORKAROUND = "___workaround"
BATCH_UPDATE_CHUNK_SIZE = 500
CURSOR_FUNCTIONS = (
    "add_block",
    "hblock",
    "hblock_n",
    "vblock",
    "vblock_n",
    "shift",
    "clone",
    "clone_shift",
)


class Cf:
    LEFT = CellFormat(horizontalAlignment="LEFT")
    CENTER = CellFormat(horizontalAlignment="CENTER")
    RIGHT = CellFormat(horizontalAlignment="RIGHT")
    TOP = CellFormat(verticalAlignment="TOP")
    MIDDLE = CellFormat(verticalAlignment="MIDDLE")
    BOTTOM = CellFormat(verticalAlignment="BOTTOM")
    BOLD = CellFormat(textFormat=TextFormat(bold=True))
    ITALIC = CellFormat(textFormat=TextFormat(italic=True))
    WRAP = CellFormat(wrapStrategy="WRAP")
    CHECKBOX = DataValidationRule(
        BooleanCondition("BOOLEAN", ["TRUE", "FALSE"]),
        showCustomUi=True,
    )

    def font_size(n: int):
        return CellFormat(textFormat=TextFormat(fontSize=n))

    def font_family(name: str):
        return CellFormat(textFormat=TextFormat(fontFamily=name))

    def text_color(color: Color):
        return CellFormat(
            textFormat=TextFormat(foregroundColorStyle=ColorStyle(rgbColor=color))
        )

    def background_color(color: Color):
        return CellFormat(backgroundColor=color)


def color_from_hex(hex):
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    return Color(r / 255, g / 255, b / 255)


def a1_range_to_list_of_cells(a1_range, orientation="horizontal"):
    result = []
    grid_range = a1_range_to_grid_range(a1_range)
    start_x = grid_range["startColumnIndex"] + 1
    end_x_not_inclusive = grid_range["endColumnIndex"] + 1
    start_y = grid_range["startRowIndex"] + 1
    end_y_not_inclusive = grid_range["endRowIndex"] + 1
    if orientation == "horizontal":
        moving_y = start_y
        while moving_y < end_y_not_inclusive:
            line = []
            moving_x = start_x
            while moving_x < end_x_not_inclusive:
                line.append(Cell(moving_y, moving_x))
                moving_x += 1
            moving_y += 1
            result.append(line)
    elif orientation == "vertical":
        moving_x = start_x
        while moving_x < end_x_not_inclusive:
            line = []
            moving_y = start_y
            while moving_y < end_y_not_inclusive:
                line.append(Cell(moving_y, moving_x))
                moving_y += 1
            moving_x += 1
            result.append(line)
    else:
        raise Exception(
            f"orientation must be horizontal or vertical, was: {orientation}"
        )
    return result


def make_address(worksheet, cell):
    return f"'{worksheet.ws.title}'!{cell_to_a1(cell)}"


class Checkbox:
    def __init__(self, val=False):
        self.val = val

    def __repr__(self):
        return f"Checkbox({self.val})"


class BlockCoords(NamedTuple):
    init_x: int
    init_y: int
    max_x: int
    max_y: int
    min_x: int
    min_y: int
    end_x: int
    end_y: int


CursorType = TypeVar("T", bound="Cursor")


class Cursor:
    def __init__(self, wks, x=1, y=1):
        self.wks = wks
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("x and y must be integers")
        self.x = x
        self.y = y

    def clone(self):
        return Cursor(self.wks, self.x, self.y)

    def set_value(self, cell, val):
        if isinstance(val, FCell):
            rc = rowcol_to_a1(cell.row, cell.col)
            if val.merge_shift_y:
                if val.fmt is None:
                    val.fmt = Cf.MIDDLE
                else:
                    val.fmt += Cf.MIDDLE
            if val.fmt:
                self.wks.set_cell_format(f"{rc}:{rc}", val.fmt)
            if val.hidden:
                self.hide_col()
            if val.hidden_row:
                self.hide_row()
            if val.align:
                self.align_column(val.align)
            if val.width:
                self.set_col_width(val.width)
            if val.height:
                self.set_row_height(val.height)
            if val.merge_shift_x or val.merge_shift_y:
                merge_shift_x = val.merge_shift_x or 0
                merge_shift_y = val.merge_shift_y or 0
                shifted = self.clone_shift(x=merge_shift_x, y=merge_shift_y)
                self.merge_until(shifted)
            if val.dv_rule:
                rc = rowcol_to_a1(cell.row, cell.col)
                if isinstance(val.dv_rule, Callable):
                    dv_rule = val.dv_rule(self)
                else:
                    dv_rule = val.dv_rule
                self.wks.parent.fmt[self.wks.ws.title]["dv_cell_ranges"].append(
                    (f"{rc}:{rc}", dv_rule)
                )
            val = val.cell
        if isinstance(val, Checkbox):
            rc = rowcol_to_a1(cell.row, cell.col)
            self.wks.parent.fmt[self.wks.ws.title]["dv_cell_ranges"].append(
                (f"{rc}:{rc}", Cf.CHECKBOX)
            )
            cell.value = "TRUE" if val.val else "FALSE"
        elif val is None:
            pass
        elif isinstance(val, Callable):
            cell.value = val(self)
        else:
            cell.value = val

    def set(
        self,
        cursor: Optional[CursorType] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ):
        if cursor:
            assert x is None
            assert y is None
            assert self.wks == cursor.wks
            self.x = cursor.x
            self.y = cursor.y
        else:
            if x is not None:
                self.x = x
            if y is not None:
                self.y = y
        return self

    def shift(self, x: int = 0, y: int = 0):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("x and y must be integers")
        self.x += x
        self.y += y
        return self

    def clone_shift(self, x: int = 0, y: int = 0):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("x and y must be integers")
        return Cursor(self.wks, self.x + x, self.y + y)

    def replace(self, x: Optional[int] = None, y: Optional[int] = None):
        if (x is not None and not isinstance(x, int)) or (
            y is not None and not isinstance(y, int)
        ):
            raise ValueError("x and y must be integers")
        new_x = self.x if x is None else x
        new_y = self.y if y is None else y
        return Cursor(self.wks, new_x, new_y)

    def as_cell(self, fixed_row=False, fixed_col=False, full=False):
        col = col_to_a(self.x)
        row = str(self.y)
        if fixed_row:
            row = "$" + row
        if fixed_col:
            col = "$" + col
        formatted = col + row
        if full:
            formatted = f"'{self.wks.ws.title}'!{formatted}"
        return formatted

    def as_cell_full(self, **kwargs):
        kwargs["full"] = True
        return self.as_cell(**kwargs)

    def __repr__(self):
        return f"Cursor({self.wks.ws.title} {self.x}, {self.y})"

    def __format__(self, spec):
        full = "f" in spec
        if "p" in spec:
            if "pr" in spec:
                fixed_row = True
                fixed_col = False
            elif "pc" in spec:
                fixed_row = False
                fixed_col = True
            else:
                fixed_row = True
                fixed_col = True
        else:
            fixed_row = False
            fixed_col = False
        return self.as_cell(full=full, fixed_col=fixed_col, fixed_row=fixed_row)

    def set_col_width(self, width):
        self.wks.parent.fmt[self.wks.ws.title]["column_widths"][self.x] = width

    def set_row_height(self, height):
        self.wks.parent.fmt[self.wks.ws.title]["row_heights"][self.y] = height

    def freeze_col(self):
        self.wks.parent.fmt[self.wks.ws.title]["freeze_col"] = self.x

    def freeze_row(self):
        self.wks.parent.fmt[self.wks.ws.title]["freeze_row"] = self.y

    def align_column(self, alignment="CENTER"):
        cf = CellFormat(horizontalAlignment=alignment)
        self.wks.parent.fmt[self.wks.ws.title]["cell_ranges"].append(
            (col_to_a(self.x), cf)
        )

    def hide_col(self):
        self.wks.parent.fmt[self.wks.ws.title]["hidden_cols"].add(self.x)

    def hide_row(self):
        self.wks.parent.fmt[self.wks.ws.title]["hidden_rows"].add(self.y)

    def merge_until(self, cell):
        self.wks.parent.fmt[self.wks.ws.title]["merged_cells"].append(
            (self.x, cell.x, self.y, cell.y)
        )

    def hblock(self, *args, **kwargs):
        kwargs["horizontal"] = True
        kwargs["add_newline"] = False
        return self.add_block(*args, **kwargs)

    def hblock_n(self, *args, **kwargs):
        kwargs["horizontal"] = True
        kwargs["add_newline"] = True
        return self.add_block(*args, **kwargs)

    def vblock(self, *args, **kwargs):
        kwargs["horizontal"] = False
        kwargs["add_newline"] = False
        return self.add_block(*args, **kwargs)

    def vblock_n(self, *args, **kwargs):
        kwargs["horizontal"] = False
        kwargs["add_newline"] = True
        return self.add_block(*args, **kwargs)

    def add_block(
        self,
        data=None,
        horizontal=False,
        add_newline=False,
    ):
        init_x = self.x
        init_y = self.y
        assert data is not None
        new_cells = []
        for val in data:
            cell = Cell(self.y, self.x)
            self.set_value(cell, val)
            if horizontal:
                self.x += 1
            else:
                self.y += 1
            new_cells.append(cell)
        max_x = max(cell.col for cell in new_cells)
        max_y = max(cell.row for cell in new_cells)
        min_x = min(cell.col for cell in new_cells)
        min_y = min(cell.row for cell in new_cells)
        self.wks.parent.cells[self.wks.ws.title].extend(new_cells)
        if add_newline:
            self.x = init_x
            self.y = max_y + 1
        else:
            self.x = max_x + 1
            self.y = init_y
        return BlockCoords(
            init_x=init_x,
            init_y=init_y,
            max_x=max_x,
            max_y=max_y,
            min_x=min_x,
            min_y=min_y,
            end_x=self.x,
            end_y=self.y,
        )


def cell_to_a1(cell):
    if isinstance(cell, Cursor):
        return cell.as_cell()
    return rowcol_to_a1(cell.row, cell.col)


class FCell:
    def __init__(
        self,
        cell,
        fmt=None,
        width=None,
        height=None,
        hidden=False,
        hidden_row=False,
        align=None,
        dv_rule=None,
        merge_shift_y=None,
        merge_shift_x=None,
    ):
        self.cell = cell
        self.fmt = fmt
        self.width = width
        self.height = height
        self.hidden = hidden
        self.hidden_row = hidden_row
        self.align = align
        self.dv_rule = dv_rule
        self.merge_shift_y = merge_shift_y
        self.merge_shift_x = merge_shift_x


class Worksheet:
    def __init__(
        self,
        ws,
        parent,
        defer=False,
        hidden=False,
        init_format=None,
        force_max_col=1,
        force_max_row=1,
    ):
        self.ws = ws
        self.parent = parent
        self.cursor = Cursor(self)
        self.defer = defer
        self.hidden = hidden
        self.init_format = init_format
        self.force_max_col = force_max_col
        self.force_max_row = force_max_row
        for func in CURSOR_FUNCTIONS:

            def func_gen(name):
                def _func(*args, **kwargs):
                    return getattr(self.cursor, name)(*args, **kwargs)

                return _func

            setattr(self, func, func_gen(func))

    def hide_gridlines(self):
        self.parent.fmt[self.ws.title]["hide_gridlines"] = True

    def spawn_cursor(self, x=1, y=1):
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("x and y must be integers")
        return Cursor(self, x=x, y=y)

    def add_to_conditional_formatting(self, rules):
        self.parent.fmt[self.ws.title]["conditional_format_rules"].extend(rules)

    def set_conditional_formatting(self, rules):
        self.parent.fmt[self.ws.title]["conditional_format_rules"] = rules

    def set_cell_format(self, range_, cell_format):
        self.parent.fmt[self.ws.title]["cell_ranges"].insert(0, (range_, cell_format))

    def add_to_batch_clear(self, rng):
        self.parent.batch_clear_ranges.append(absolute_range_name(self.ws.title, rng))

    def max_col(self):
        return max(c.col for c in self.parent.cells[self.ws.title])

    def max_row(self):
        return max(c.row for c in self.parent.cells[self.ws.title])


def new_fmt():
    return {
        "conditional_format_rules": [],
        "cell_ranges": [],
        "merged_cells": [],
        "dv_cell_ranges": [],
        "hide_gridlines": False,
        "column_widths": {},
        "row_heights": {},
        "freeze_col": 0,
        "freeze_row": 0,
        "hidden_cols": set(),
        "hidden_rows": set(),
    }


def hide_req(worksheet, id_, rows=False):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": worksheet.ws.id,
                "dimension": "ROWS" if rows else "COLUMNS",
                "startIndex": id_ - 1,
                "endIndex": id_,
            },
            "properties": {
                "hiddenByUser": True,
            },
            "fields": "hiddenByUser",
        }
    }


def delete_req(worksheet, id_min, id_max, rows=False):
    return {
        "deleteDimension": {
            "range": {
                "sheetId": worksheet.ws.id,
                "dimension": "ROWS" if rows else "COLUMNS",
                "startIndex": id_min,
                "endIndex": id_max,
            },
        }
    }


def merge_req(worksheet, start_col, end_col, start_row, end_row):
    return {
        "mergeCells": {
            "mergeType": "MERGE_ALL",
            "range": {
                "sheetId": worksheet.ws.id,
                "startRowIndex": start_row - 1,
                "endRowIndex": end_row,
                "startColumnIndex": start_col - 1,
                "endColumnIndex": end_col,
            },
        }
    }


def hide_gridlines_req(worksheet):
    return {
        "updateSheetProperties": {
            "properties": {
                "sheetId": worksheet.ws.id,
                "gridProperties": {
                    "hideGridlines": True,
                },
            },
            "fields": "gridProperties.hideGridlines",
        }
    }


def col_to_a(col):
    return rowcol_to_a1(row=1, col=col).replace("1", "")


class _StubWs:
    """Placeholder for a worksheet not yet created in Google Sheets.

    Supports the subset of gspread.Worksheet attributes used during the
    data-building phase (before submit).  After _flush_worksheet_ops the
    stub is replaced with a real gspread Worksheet object.

    Each stub gets a unique negative ``id`` so that GridRange objects
    created during data building can be patched to the real sheet ID
    after the sheets are actually created.
    """

    _next_id = -1

    def __init__(self, title):
        self.title = title
        self.id = _StubWs._next_id
        _StubWs._next_id -= 1
        self.col_count = 60
        self.row_count = 200


def _set_sheet_size(ws, row_count, col_count):
    """Update the cached grid dimensions on a worksheet (real or stub)."""
    if isinstance(ws, _StubWs):
        ws.row_count = row_count
        ws.col_count = col_count
    else:
        ws._properties["gridProperties"]["rowCount"] = row_count
        ws._properties["gridProperties"]["columnCount"] = col_count


class GoogleSheetWriter:
    def __init__(self, gc, spreadsheet_id, throttle=1, submit_order=None):
        self.gc = gc
        self.spreadsheet_id = spreadsheet_id
        self.spreadsheet = self.gc.open_by_key(self.spreadsheet_id)
        self.worksheets = None
        self.cells = defaultdict(list)
        self.batch_clear_ranges = []
        self.formatter = batch_updater(self.spreadsheet)
        self.fmt = defaultdict(lambda: new_fmt())
        self.throttle = throttle
        self.ignore = set()  # this is for debugging large tables, where you generate the cells, but don't submit them, preserving user-entered data
        self.submit_order = submit_order
        self._pending_deletes = []  # (name, real_gspread_ws) to delete
        self._pending_creates = []  # names to create

    def batch_clear(self):
        if not self.batch_clear_ranges:
            return
        body = {"ranges": self.batch_clear_ranges}
        response = self.spreadsheet.values_batch_clear(body=body)
        self.batch_clear_ranges = []
        return response

    def get_worksheet(self, name, remove=False, defer=False, hidden=False):
        if self.worksheets is None:
            self.worksheets = {
                ws.title: Worksheet(ws, self) for ws in self.spreadsheet.worksheets()
            }

        if name in self.worksheets and remove and name not in self.ignore:
            real_ws = self.worksheets[name].ws
            if not isinstance(real_ws, _StubWs):
                self._pending_deletes.append((name, real_ws))
            self.worksheets.pop(name, None)

        if name not in self.worksheets:
            stub = _StubWs(name)
            self.worksheets[name] = Worksheet(stub, self, defer=defer, hidden=hidden)
            self._pending_creates.append(name)
        else:
            ws_wrapper = self.worksheets[name]
            ws_wrapper.defer = defer
            ws_wrapper.hidden = hidden

        return self.worksheets[name]

    def _flush_worksheet_ops(self):
        """Batch all pending worksheet creates/deletes into one API call.

        Uses rename-then-delete to avoid name conflicts when recreating
        sheets (remove=True).  After the batch, refreshes the worksheet
        list so all Worksheet wrappers hold real gspread objects.
        """
        if not self._pending_deletes and not self._pending_creates:
            return

        reqs = []

        # Rename sheets scheduled for deletion to avoid name collisions
        # with newly created sheets that reuse the same name.
        for i, (name, real_ws) in enumerate(self._pending_deletes):
            reqs.append(
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": real_ws.id,
                            "title": f"___to_delete_{i}",
                        },
                        "fields": "title",
                    }
                }
            )

        # Create new sheets large enough for data (min 200x60 so that
        # conditional formatting ranges aren't clipped — shrinking to
        # exact data size happens later in _format via delete_req).
        for name in self._pending_creates:
            cells = self.cells.get(name, [])
            ws_wrapper = self.worksheets[name]
            if cells:
                max_col = max(max(c.col for c in cells), ws_wrapper.force_max_col, 60)
                max_row = max(max(c.row for c in cells), ws_wrapper.force_max_row, 200)
            else:
                max_col = max(60, ws_wrapper.force_max_col)
                max_row = max(200, ws_wrapper.force_max_row)
            reqs.append(
                {
                    "addSheet": {
                        "properties": {
                            "title": name,
                            "sheetType": "GRID",
                            "gridProperties": {
                                "rowCount": max_row,
                                "columnCount": max_col,
                            },
                        }
                    }
                }
            )

        # Delete the renamed sheets
        for _name, real_ws in self._pending_deletes:
            reqs.append({"deleteSheet": {"sheetId": real_ws.id}})

        n_create = len(self._pending_creates)
        n_delete = len(self._pending_deletes)
        print(f"Batch worksheet management: {n_create} create, {n_delete} delete...")
        self._chunked_batch_update(reqs)

        # Refresh worksheet objects so stubs are replaced with real
        # gspread Worksheet objects (needed by gspread_formatting).
        if self._pending_creates:
            real_ws_map = {ws.title: ws for ws in self.spreadsheet.worksheets()}
            for name in self._pending_creates:
                if name in real_ws_map and name in self.worksheets:
                    stub = self.worksheets[name].ws
                    real_ws = real_ws_map[name]
                    self.worksheets[name].ws = real_ws
                    # Patch GridRange.sheetId in conditional formatting
                    # rules that were built against the stub's temporary
                    # negative ID.
                    if isinstance(stub, _StubWs):
                        self._patch_stub_ids(name, stub.id, real_ws.id)

        self._pending_deletes = []
        self._pending_creates = []
        self.sleep()

    def _patch_stub_ids(self, ws_name, stub_id, real_id):
        """Replace temporary stub sheet IDs with real IDs in stored format rules."""
        fmt = self.fmt.get(ws_name)
        if not fmt:
            return
        for rule in fmt.get("conditional_format_rules", []):
            for grid_range in getattr(rule, "ranges", []):
                if grid_range.sheetId == stub_id:
                    grid_range.sheetId = real_id

    def _chunked_batch_update(self, reqs):
        """Execute batch_update in chunks to stay within API limits."""
        if not reqs:
            return
        for i in range(0, len(reqs), BATCH_UPDATE_CHUNK_SIZE):
            chunk = reqs[i : i + BATCH_UPDATE_CHUNK_SIZE]
            self.spreadsheet.batch_update({"requests": chunk})

    def sleep(self):
        if self.throttle:
            time.sleep(self.throttle)

    def _format(self, extra_reqs=None):
        reqs = list(extra_reqs or [])
        for name in self.fmt:
            if name in self.ignore:
                continue
            ws = self.worksheets[name]
            fmt_dict = self.fmt[name]
            cells = self.cells[name]
            max_cells_col = max(max([c.col for c in cells]), ws.force_max_col)
            max_cells_row = max(max([c.row for c in cells]), ws.force_max_row)
            col_count = ws.ws.col_count
            row_count = ws.ws.row_count
            if col_count > max_cells_col:
                reqs.append(delete_req(ws, max_cells_col, col_count))
            if row_count > max_cells_row:
                reqs.append(delete_req(ws, max_cells_row, row_count, rows=True))
            if ws.init_format:
                ws.init_format(ws, max_col=max_cells_col, max_row=max_cells_row)

            hidden_cols = fmt_dict["hidden_cols"]
            if hidden_cols:
                for col in hidden_cols:
                    reqs.append(hide_req(ws, col))
            hidden_rows = fmt_dict["hidden_rows"]
            if hidden_rows:
                for row in hidden_rows:
                    reqs.append(hide_req(ws, row, rows=True))

            if fmt_dict["hide_gridlines"]:
                reqs.append(hide_gridlines_req(ws))

            cw = fmt_dict["column_widths"]
            column_widths = [(col_to_a(col), cw[col]) for col in cw]
            if column_widths:
                self.formatter.set_column_widths(ws.ws, column_widths)

            rh = fmt_dict["row_heights"]
            row_heights = [(f"{row}:{row}", rh[row]) for row in rh]
            if row_heights:
                self.formatter.set_row_heights(ws.ws, row_heights)

            merged_cells = fmt_dict["merged_cells"]
            if merged_cells:
                for tup in merged_cells:
                    reqs.append(merge_req(ws, tup[0], tup[1], tup[2], tup[3]))

            if cr := fmt_dict["cell_ranges"]:
                for rng in cr:
                    if isinstance(rng[1], Cf):
                        import pdb

                        pdb.set_trace()
                    self.formatter.format_cell_range(ws.ws, rng[0], rng[1])

            if dv := fmt_dict["dv_cell_ranges"]:
                for rng in dv:
                    self.formatter.set_data_validation_for_cell_range(
                        ws.ws, rng[0], rng[1]
                    )

            if fmt_dict["freeze_col"] or fmt_dict["freeze_row"]:
                self.formatter.set_frozen(
                    ws.ws, rows=fmt_dict["freeze_row"], cols=fmt_dict["freeze_col"]
                )

            if fmt_dict["conditional_format_rules"]:
                print(f"Applying conditional formatting for {ws.ws.title}...")
                rules = get_conditional_format_rules(ws.ws)
                rules.clear()
                rules.extend(fmt_dict["conditional_format_rules"])
                rules.save()
                self.sleep()

        # Merge gspread_formatting's accumulated requests with our
        # structural requests into a single batch_update call.
        format_reqs = list(self.formatter.requests)
        del self.formatter.requests[:]
        all_reqs = format_reqs + reqs
        if all_reqs:
            print(f"Applying formatting and structure ({len(all_reqs)} requests)...")
            self._chunked_batch_update(all_reqs)
            self.sleep()

    def submit(self):
        # Phase 1: Batch worksheet creation/deletion (1-2 API calls)
        self._flush_worksheet_ops()

        # Phase 2: Batch clear user-specified ranges (1 API call)
        if self.batch_clear_ranges:
            print("Clearing user-specified ranges...")
            self.batch_clear()

        # Phase 3: Determine submission order
        self.submit_order = self.submit_order or []
        deferred = []
        normal = []
        for name in self.worksheets:
            if name not in self.cells:
                continue
            if name in self.submit_order:
                continue
            elif self.worksheets[name].defer:
                deferred.append(name)
            else:
                normal.append(name)
        self.submit_order.extend(normal)
        self.submit_order.extend(deferred)

        # Phase 4: Expand sheets that are too small for their data.
        # Only expand here — shrinking to exact size happens later in
        # _format (via delete_req) AFTER conditional formatting is applied.
        size_reqs = []
        for name in self.submit_order:
            if name in self.ignore:
                continue
            cells = self.cells.get(name, [])
            if not cells:
                continue
            ws = self.worksheets[name]
            max_col = max(max(c.col for c in cells), ws.force_max_col)
            max_row = max(max(c.row for c in cells), ws.force_max_row)
            needs_expand = ws.ws.col_count < max_col or ws.ws.row_count < max_row
            if needs_expand:
                new_col = max(ws.ws.col_count, max_col)
                new_row = max(ws.ws.row_count, max_row)
                size_reqs.append(
                    {
                        "updateSheetProperties": {
                            "properties": {
                                "sheetId": ws.ws.id,
                                "gridProperties": {
                                    "rowCount": new_row,
                                    "columnCount": new_col,
                                },
                            },
                            "fields": "gridProperties.rowCount,gridProperties.columnCount",
                        }
                    }
                )
                _set_sheet_size(ws.ws, new_row, new_col)

        if size_reqs:
            print(f"Setting sheet sizes ({len(size_reqs)} sheets)...")
            self._chunked_batch_update(size_reqs)
            self.sleep()

        # Phase 5: Batch write all cell values (2 API calls: clear + update)
        clear_ranges = []
        value_data = []
        total_cells = 0
        sheets_to_write = []
        for name in self.submit_order:
            if name in self.ignore:
                continue
            cells = self.cells.get(name, [])
            if not cells:
                continue
            ws_title = self.worksheets[name].ws.title
            clear_ranges.append(f"'{ws_title}'")

            max_row = max(c.row for c in cells)
            max_col = max(c.col for c in cells)
            n_cells = max_row * max_col
            total_cells += n_cells
            print(f"  Preparing {ws_title} ({max_row}x{max_col} = {n_cells} cells)...")
            grid = [["" for _ in range(max_col)] for _ in range(max_row)]
            for cell in cells:
                if cell.value is not None:
                    grid[cell.row - 1][cell.col - 1] = cell.value

            range_str = f"'{ws_title}'!A1:{rowcol_to_a1(max_row, max_col)}"
            value_data.append({"range": range_str, "values": grid})
            sheets_to_write.append(ws_title)

        if clear_ranges:
            print(f"Clearing {len(clear_ranges)} sheets...")
            self.spreadsheet.values_batch_clear(body={"ranges": clear_ranges})

        if value_data:
            print(f"Writing {len(value_data)} sheets ({total_cells} cells total)...")
            self.spreadsheet.values_batch_update(
                body={
                    "valueInputOption": "USER_ENTERED",
                    "data": value_data,
                }
            )
            self.sleep()

        # Phase 6: Batch formatting + hide worksheets (1 API call)
        hide_reqs = []
        for name in self.submit_order:
            if name in self.ignore:
                continue
            if self.worksheets[name].hidden:
                hide_reqs.append(
                    {
                        "updateSheetProperties": {
                            "properties": {
                                "sheetId": self.worksheets[name].ws.id,
                                "hidden": True,
                            },
                            "fields": "hidden",
                        }
                    }
                )

        self._format(extra_reqs=hide_reqs)

        print(
            f"Finished! View results at https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit"
        )
