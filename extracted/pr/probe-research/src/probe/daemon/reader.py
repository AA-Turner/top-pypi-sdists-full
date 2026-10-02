"""What the daemon's `read` tool shows of a file (tuning plan T8).

`render(path, offset, limit)` returns plain text, never raises for a file it
cannot show, and never runs anything a file says:

    text            numbered lines (`offset`, `limit`), each line and the whole
                    answer capped
    CSV / TSV       the header and first rows, and the shape
    JSON            what it is (keys, length) and the document pretty-printed,
                    capped; JSON lines read as text
    Parquet         schema, row count, first rows -- through pyarrow, which the
                    daemon's environment may not have (then it says so)
    NumPy           .npy / .npz: dtype, shape and the first values, read from the
                    format's own header with the standard library (no numpy)

Refused, with why: pickle and the formats built on it (a pickle runs code when
it is loaded; the reader never loads one, and says so instead of showing its
bytes), a NumPy array of Python objects (pickled), images (the model reads
text only), and other binary files. `offset` / `limit` read any file's lines as
text instead of its preview.

Which files may be read at all, and scrubbing what is shown, are the caller's
(`tools.read_file`).
"""

from __future__ import annotations

import ast
import csv
import json
import math
import re
import stat
import struct
import zipfile
from itertools import islice
from pathlib import Path
from typing import IO, Any

#: The most text one answer holds.
MAX_CHARS = 30_000
#: The most characters of one line shown.
MAX_LINE_CHARS = 2_000
#: Lines shown when no `limit` is given, and the most a `limit` may ask for.
DEFAULT_LINES = 2_000
#: Rows a table preview shows.
HEAD_ROWS = 20
#: Files up to this size are counted or parsed whole (rows of a CSV, a JSON
#: document); a bigger one shows its head.
PARSE_BYTES = 20 * 1024 * 1024
#: A NumPy header longer than this is not read (a real one is a few hundred bytes).
NPY_HEADER_BYTES = 64 * 1024
#: The most a preview skips to reach an array's next row; wider rows show the first row only.
NPY_SKIP_BYTES = 1 << 20

IMAGE_SUFFIXES = frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".ico", ".heic"})
#: Formats that run code when loaded: pickle, and the formats that wrap it.
PICKLE_SUFFIXES = frozenset({".pkl", ".pickle", ".joblib", ".dill", ".cloudpickle", ".pt", ".pth", ".ckpt",
                             ".sav"})
_PICKLE_MAGIC = (b"\x80\x02", b"\x80\x03", b"\x80\x04", b"\x80\x05")


def render(path: Path, offset: int | None = None, limit: int | None = None) -> str:
    """The text the `read` tool answers for `path` (already allowed by the caller)."""
    try:
        info = path.stat()
    except (OSError, ValueError):
        return f"not read: no file at {path}"
    if path.is_dir():
        return f"not read: {path} is a folder"
    if not stat.S_ISREG(info.st_mode):  # a FIFO or a device would block the read forever
        return f"not read: {path} isn't a regular file"
    size = info.st_size
    suffix = path.suffix.lower()
    if suffix in IMAGE_SUFFIXES:
        return f"not read: {path.name} is an image - the daemon's model reads text only"
    if suffix in PICKLE_SUFFIXES:
        return _pickle_refusal(path)
    try:
        with path.open("rb") as handle:
            head = handle.read(8192)
    except OSError as exc:
        return f"not read: {path} can't be opened ({type(exc).__name__})"
    if head.startswith(_PICKLE_MAGIC):
        return _pickle_refusal(path)
    if size == 0:
        return f"[{path} · empty file]"
    try:
        if offset is None and limit is None:
            if suffix in (".csv", ".tsv"):
                return _table(path, size, "\t" if suffix == ".tsv" else ",")
            if suffix == ".json":
                return _json(path, size)
            if suffix == ".parquet":
                return _parquet(path, size)
            if suffix == ".npy":
                with path.open("rb") as handle:
                    return f"[{path} · NumPy array, {size:,} bytes]\n" + _npy(handle)
            if suffix == ".npz":
                return _npz(path, size)
        if b"\0" in head:
            return (f"not read: {path.name} is a binary file ({size:,} bytes) - the reader shows text, CSV/TSV, "
                    "JSON, Parquet and NumPy")
        return _text(path, size, offset, limit)
    except _Refused as refused:
        return f"not read: {refused}"
    except Exception as exc:  # noqa: BLE001 -- a malformed file is the reader's answer, never a tool error
        return f"not read: {path.name} couldn't be read as {suffix or 'text'} ({type(exc).__name__}: {exc})"[:500]


class _Refused(Exception):
    """A file the reader will not show, with why."""


def _pickle_refusal(path: Path) -> str:
    return (f"not read: {path.name} is a pickle (or built on one); loading a pickle runs code, so the reader never "
            "loads one.")


# --- text --------------------------------------------------------------------


def _lines(handle: IO[str]):
    """Each line without its newline, cut at MAX_LINE_CHARS (the rest of a long
    line is skipped, never held in memory whole): `(text, was_cut)`."""
    while True:
        line = handle.readline(MAX_LINE_CHARS + 1)
        if not line:
            return
        if line.endswith("\n") or len(line) <= MAX_LINE_CHARS:
            yield line.rstrip("\n"), False
            continue
        while True:  # the rest of an over-long line
            more = handle.readline(1 << 16)
            if not more or more.endswith("\n"):
                break
        yield _head(line, MAX_LINE_CHARS), True


def _text(path: Path, size: int, offset: int | None, limit: int | None) -> str:
    start = max(1, offset or 1)
    count = max(1, min(limit or DEFAULT_LINES, DEFAULT_LINES))
    out: list[str] = []
    used = 0
    last = start - 1
    more = False
    with path.open(encoding="utf-8", errors="replace", newline=None) as handle:
        for number, (line, cut) in enumerate(_lines(handle), 1):
            if number < start:
                continue
            row = f"{number:>6}\t{line}" + (" [... line cut]" if cut else "")
            if number >= start + count or used + len(row) > MAX_CHARS:
                more = True
                break
            out.append(row)
            used += len(row) + 1
            last = number
    if not out:
        return f"[{path} · no line {start}: the file is shorter]"
    head = f"[{path} · lines {start}-{last}]"
    tail = f"\n[more follows: offset={last + 1} reads on]" if more else ""
    return f"{head}\n" + "\n".join(out) + tail


# --- tables ------------------------------------------------------------------


def _head(text: str, width: int) -> str:
    """`text` cut to `width`, without the word the cut lands in: a key has no
    spaces, so a cut never shows a piece of one that the scrubber could not
    recognise (the caller scrubs the whole keys that are left)."""
    if len(text) <= width:
        return text
    return re.sub(r"\S+$", "", text[:width])


def _cell(value: Any, width: int = 40) -> str:
    text = "" if value is None else str(value).replace("\n", " ")
    return text if len(text) <= width else _head(text, width - 1) + "…"


def _grid(header: list[str], rows: list[list[Any]]) -> str:
    """A plain-text table, columns padded to their widest cell (capped)."""
    table = [[_cell(c) for c in header]] + [[_cell(c) for c in row] for row in rows]
    columns = max(len(r) for r in table)
    widths = [max((len(r[k]) for r in table if k < len(r)), default=0) for k in range(columns)]
    return "\n".join("  ".join(r[k].ljust(widths[k]) if k < len(r) else "" for k in range(columns)).rstrip()
                     for r in table)


def _table(path: Path, size: int, delimiter: str) -> str:
    with path.open(encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        head = list(islice(reader, HEAD_ROWS + 1))
        if size <= PARSE_BYTES:
            total, exact = len(head) + sum(1 for _ in reader), True
        else:
            total, exact = None, False
    if not head:
        return f"[{path} · empty table]"
    header, rows = head[0], head[1:]
    if total is None:
        with path.open("rb") as raw:
            total = sum(chunk.count(b"\n") for chunk in iter(lambda: raw.read(1 << 20), b""))
    shape = f"{'' if exact else '~'}{max(total - 1, 0):,} rows × {len(header)} columns"
    shown = f"first {len(rows)} rows" if rows else "no rows"
    return _capped(f"[{path} · {shape} · header and {shown}]\n{_grid(header, rows)}")


def _capped(text: str) -> str:
    if len(text) <= MAX_CHARS:
        return text
    return _head(text, MAX_CHARS) + f"\n[... {len(text) - MAX_CHARS:,} characters cut: read it with offset/limit]"


# --- JSON --------------------------------------------------------------------


def _json(path: Path, size: int) -> str:
    if size > PARSE_BYTES:
        first = _text(path, size, None, 200)
        return f"[{path} · JSON, {size:,} bytes: too big to parse whole; its first lines]\n{first}"
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        return f"[{path} · not valid JSON; read as text]\n" + _text(path, size, None, None)
    if isinstance(data, dict):
        keys = list(data)
        what = f"an object with {len(keys)} keys: {', '.join(map(str, keys[:30]))}" + (" ..." if len(keys) > 30 else "")
    elif isinstance(data, list):
        what = f"an array of {len(data)} items"
    else:
        what = f"a {type(data).__name__}"
    return _capped(f"[{path} · JSON: {what}]\n{json.dumps(data, indent=2, ensure_ascii=False)}")


# --- Parquet -----------------------------------------------------------------


def _import_parquet():
    import pyarrow.parquet as pq  # a heavy optional dependency: imported only when a Parquet file is read

    return pq


def _parquet(path: Path, size: int) -> str:
    try:
        pq = _import_parquet()
    except ImportError:
        return (f"not previewed: {path.name} is Parquet ({size:,} bytes) - reading it needs pyarrow, which isn't "
                "installed.")
    import pyarrow

    if tuple(int(x) for x in re.findall(r"\d+", pyarrow.__version__)[:3]) < (14, 0, 1):
        return (f"not previewed: {path.name} is Parquet, and this pyarrow ({pyarrow.__version__}) can run code "
                "from a crafted file - it needs 14.0.1 or later.")
    parquet = pq.ParquetFile(str(path))
    schema = parquet.schema_arrow
    rows: list[list[Any]] = []
    for batch in parquet.iter_batches(batch_size=HEAD_ROWS):
        rows = [list(r.values()) for r in batch.to_pylist()]
        break
    columns = ", ".join(f"{f.name}: {f.type}" for f in schema)
    return _capped(f"[{path} · Parquet: {parquet.metadata.num_rows:,} rows × {len(schema)} columns · first "
                   f"{len(rows)} rows]\ncolumns: {columns}\n{_grid(schema.names, rows)}")


# --- NumPy -------------------------------------------------------------------

#: dtype kind + item size -> struct letter, for the first values of an array.
_STRUCT = {"b1": "?", "i1": "b", "i2": "h", "i4": "i", "i8": "q", "u1": "B", "u2": "H", "u4": "I", "u8": "Q",
           "f2": "e", "f4": "f", "f8": "d"}
_NAMES = {"b": "bool", "i": "int", "u": "uint", "f": "float", "c": "complex", "U": "str", "S": "bytes",
          "M": "datetime64", "m": "timedelta64", "V": "void"}


def _npy_header(handle: IO[bytes]) -> dict:
    """The dict a .npy file starts with, read as a literal (`ast.literal_eval`
    evaluates no code)."""
    if handle.read(6) != b"\x93NUMPY":
        raise ValueError("not a NumPy .npy file (no magic)")
    major = handle.read(2)[0]
    length = struct.unpack("<H" if major == 1 else "<I", handle.read(2 if major == 1 else 4))[0]
    if length > NPY_HEADER_BYTES:
        raise ValueError(f"a {length:,}-byte header")
    header = ast.literal_eval(handle.read(length).decode("latin1" if major < 3 else "utf-8"))
    if not isinstance(header, dict) or "descr" not in header or "shape" not in header:
        raise ValueError("an unreadable header")
    return header


def _dtype_name(descr: Any) -> str:
    if not isinstance(descr, str):
        return f"structured {descr}"
    kind, size = descr[1:2], descr[2:]
    name = _NAMES.get(kind, descr)
    bits = int(size) * (8 if kind in "biufc" else 1) if size.isdigit() else None
    return f"{name}{bits}" if kind in "iufc" and bits else f"{name} ({descr})"


def _npy(handle: IO[bytes]) -> str:
    header = _npy_header(handle)
    descr, shape, fortran = header["descr"], header["shape"], bool(header.get("fortran_order"))
    if not (isinstance(shape, tuple) and all(isinstance(d, int) and not isinstance(d, bool) and d >= 0
                                             for d in shape)):
        raise ValueError(f"a shape that is not a tuple of sizes: {shape!r}")
    if "O" in str(descr):
        raise _Refused("the array holds Python objects (a pickle); the reader never loads one")
    count = math.prod(shape)
    text = f"dtype {_dtype_name(descr)}, shape {shape}, {count:,} values"
    letter = _STRUCT.get(descr[1:]) if isinstance(descr, str) else None
    if letter is None or fortran or count == 0:
        return text + ("" if count == 0 else " (first values not shown for this dtype or layout)")
    order = ">" if descr[0] == ">" else "<"
    item = struct.calcsize(letter)
    width = math.prod(shape[1:]) if len(shape) > 1 else count
    rows = min(shape[0], 5) if len(shape) > 1 else 1
    take = min(width, 10)
    lines = []
    for row in range(rows):
        if row:
            skip = (width - take) * item  # the rest of the previous row, read in bounded pieces
            if skip > NPY_SKIP_BYTES:
                break
            while skip > 0 and (chunk := handle.read(min(skip, 1 << 16))):
                skip -= len(chunk)
        data = handle.read(take * item)
        values = struct.unpack(f"{order}{len(data) // item}{letter}", data[:len(data) // item * item])
        shown = ", ".join(f"{v:.6g}" if isinstance(v, float) else str(v) for v in values)
        lines.append(f"[{shown}{', ...' if take < width else ''}]")
    first = "first values" if len(shape) <= 1 else f"first {len(lines)} of {shape[0]} rows (flattened)"
    return f"{text}\n{first}:\n" + "\n".join(lines)


def _npz(path: Path, size: int) -> str:
    out = [f"[{path} · NumPy archive, {size:,} bytes]"]
    with zipfile.ZipFile(path) as archive:
        names = [n for n in archive.namelist() if n.endswith(".npy")]
        for name in names[:20]:
            with archive.open(name) as member:
                body = _npy(member)
            out.append(f"{name[:-4]}: {body}")
        if len(names) > 20:
            out.append(f"... and {len(names) - 20} more arrays")
    return _capped("\n".join(out))
