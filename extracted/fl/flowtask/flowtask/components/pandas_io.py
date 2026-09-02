"""
pandas_io — shared read/write helper for pandas DataFrames.

Exposes two public sync functions:
  - ``read_to_dataframe(buf, mime, **opts)`` — read a file/BytesIO into a DataFrame.
  - ``write_from_dataframe(df, fmt, buf, **opts)`` — write a DataFrame to a file/BytesIO.

Also re-exports ``detect_encoding`` and ``ExcelHandler`` from OpenWithBase so that
downstream consumers (CopyFrom*/CopyTo* bases) can import from a single place.

Design notes:
  - Both helpers are **synchronous**.  Pandas I/O is sync; the callers run inside
    async ``run()`` methods where network I/O stays async and parsing stays sync.
  - No new third-party dependencies are introduced.  All engines (openpyxl, xlrd,
    pyxlsb, pyarrow) are already pinned in pyproject.toml.
  - Raise ``ComponentError``, ``EmptyFile``, ``DataNotFound`` from
    ``flowtask.exceptions`` to match the exception contract of OpenWithPandas.
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any
from xml.sax import parse

import pandas
import xlrd

from ..exceptions import ComponentError, DataNotFound, EmptyFile  # noqa: F401
from .OpenWithBase import ExcelHandler, detect_encoding  # noqa: F401

__all__ = [
    "read_to_dataframe",
    "write_from_dataframe",
    "detect_encoding",
    "ExcelHandler",
]

# ---------------------------------------------------------------------------
# MIME → format dispatch
# ---------------------------------------------------------------------------

_MIME_TO_FORMAT: dict[str, str] = {
    "text/csv": "csv",
    "text/plain": "csv",
    "application/csv": "csv",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
    "application/vnd.ms-excel": "xls",
    # Note: both cased and lowercased variants included because
    # _detect_format_from_mime lowercases before lookup.
    "application/vnd.ms-excel.sheet.binary.macroEnabled.12": "xlsb",
    "application/vnd.ms-excel.sheet.binary.macroenabled.12": "xlsb",
    "application/parquet": "parquet",
    "application/x-parquet": "parquet",
    "application/json": "json",
    "text/json": "json",
    "text/html": "html",
    "application/html": "html",
    "text/xml": "xml",
}

# Default engines for Excel formats when the caller does not override.
# These mirror OpenWithPandas.open_excel lines 266-282.
_EXCEL_ENGINE_DEFAULT: dict[str, str] = {
    "xlsx": "openpyxl",
    "xls": "xlrd",
    "xlsb": "pyxlsb",
}


def _detect_format_from_mime(mime: str | None) -> str:
    """Map a MIME type string to an internal format token.

    Unknown or ``None`` MIME defaults to ``"csv"`` to preserve the existing
    OpenWithPandas behaviour.

    Args:
        mime: MIME type string (e.g. ``"text/csv"``).

    Returns:
        One of ``{"csv", "xlsx", "xls", "xlsb", "parquet", "json", "html", "xml"}``.
    """
    if mime is None:
        return "csv"
    return _MIME_TO_FORMAT.get(mime.lower(), "csv")


# ---------------------------------------------------------------------------
# Private format-specific readers
# ---------------------------------------------------------------------------

def _read_csv(
    buf: Any,
    *,
    separator: str = ",",
    decimal: str = ",",
    encoding: str | None = None,
    dtypes: dict | None = None,
    parse_dates: dict | None = None,
    na_values: set | list | None = None,
    filter_nan: bool = True,
    add_columns: dict | None = None,
    limit: int | None = None,
    engine: str = "c",
    skiprows: int | list | None = None,
    **extra: Any,
) -> pandas.DataFrame:
    """Read a CSV file/BytesIO into a DataFrame.

    Mirrors the logic of ``OpenWithPandas.open_csv`` with encoding fallbacks.
    """
    # Copy to avoid mutating the caller's dict in-place via setdefault().
    add_columns = dict(add_columns or {})
    parse_dates_arg = parse_dates or {}
    args = {}
    if dtypes is not None:
        args["dtype"] = dtypes

    add_columns.setdefault("low_memory", False)
    add_columns.setdefault("float_precision", "high")
    if limit is not None and isinstance(limit, int):
        add_columns["nrows"] = limit

    # Detect encoding when buf is a path (not BytesIO)
    resolved_encoding = encoding or "utf-8"
    if isinstance(buf, (str, Path)):
        _, new_enc = detect_encoding(buf, resolved_encoding)
        if new_enc and new_enc != resolved_encoding:
            resolved_encoding = new_enc

    if skiprows is not None:
        extra["skiprows"] = skiprows
    try:
        return pandas.read_csv(
            buf,
            sep=separator,
            quotechar='"',
            decimal=decimal,
            engine=engine,
            keep_default_na=False,
            na_values=na_values,
            na_filter=filter_nan,
            encoding=resolved_encoding,
            skipinitialspace=True,
            **add_columns,
            **parse_dates_arg,
            **args,
            **extra,
        )
    except UnicodeDecodeError:
        # Encoding fallback chain (mirrors OpenWithPandas behaviour).
        # Seek back to 0 before each attempt so BytesIO inputs are not
        # exhausted after the first failed read.
        for enc in ("utf-8", "latin1", "ascii"):
            try:
                if hasattr(buf, "seek"):
                    buf.seek(0)
                return pandas.read_csv(
                    buf,
                    sep=separator,
                    quotechar='"',
                    decimal=decimal,
                    engine=engine,
                    keep_default_na=False,
                    na_values=na_values,
                    na_filter=filter_nan,
                    encoding=enc,
                    skipinitialspace=True,
                    on_bad_lines="warn",
                    **add_columns,
                    **parse_dates_arg,
                    **args,
                    **extra,
                )
            except Exception:
                continue
        raise ComponentError("Cannot open CSV with any known encoding")
    except pandas.errors.EmptyDataError as err:
        raise ComponentError(f"Empty Data in CSV: {err}") from err
    except pandas.errors.ParserError as err:
        raise ComponentError(f"Error parsing CSV: {err}") from err
    except Exception as err:
        raise ComponentError(f"Generic error reading CSV: {err}") from err


def _read_excel(
    buf: Any,
    *,
    engine: str,
    sheet_name: str | int | None = None,
    dtypes: dict | None = None,
    parse_dates: dict | None = None,
    na_values: set | list | None = None,
    filter_nan: bool = True,
    limit: int | None = None,
    add_columns: dict | None = None,
    skiprows: int | list | None = None,
    **extra: Any,
) -> pandas.DataFrame:
    """Read an Excel file (xlsx / xls / xlsb) into a DataFrame.

    Mirrors the ``else`` branch of ``OpenWithPandas.open_excel``.
    """
    add_columns = add_columns or {}
    parse_dates_arg = parse_dates or {}
    arguments: dict[str, Any] = {**extra, **add_columns, **parse_dates_arg}
    if dtypes is not None:
        arguments["dtype"] = dtypes
    # Only forward skiprows when explicitly set (preserves prior behaviour of
    # not passing skiprows=0 to pandas.read_excel for plain Excel reads).
    if skiprows is not None and skiprows != 0:
        arguments["skiprows"] = skiprows
    if limit is not None and isinstance(limit, int):
        arguments["nrows"] = limit
    if sheet_name is not None:
        arguments["sheet_name"] = sheet_name

    try:
        return pandas.read_excel(
            buf,
            na_values=na_values,
            na_filter=filter_nan,
            engine=engine,
            keep_default_na=False,
            **arguments,
        )
    except (IndexError, xlrd.biffh.XLRDError) as err:
        raise ComponentError(f"Excel index error: {err}") from err
    except pandas.errors.EmptyDataError as err:
        raise EmptyFile(f"Empty Excel file: {err}") from err
    except pandas.errors.ParserError as err:
        raise ComponentError(f"Error parsing Excel: {err}") from err
    except TypeError as err:
        err_msg = str(err)
        if "NoneType" in err_msg or "expected str" in err_msg:
            raise ComponentError(
                f"Error reading Excel: file may be corrupted or not a valid "
                f"Excel format (engine={engine}). Detail: {err}"
            ) from err
        raise ComponentError(f"Type error reading Excel: {err}") from err
    except Exception as err:
        raise ComponentError(f"Error reading Excel: {err}") from err


def _read_xml_excel(
    buf: Any,
    *,
    add_columns: dict | None = None,
    skiprows: int = 0,
    rename: bool = False,
    **extra: Any,
) -> pandas.DataFrame:
    """Read an XML-based Excel (SpreadsheetML) file.

    Mirrors the ``text/xml`` branch of ``OpenWithPandas.open_excel``.
    """
    try:
        # parse() is inside the try so SAX errors are wrapped as ComponentError
        # rather than escaping as raw xml.sax.SAXException.
        xmlparser = ExcelHandler()
        parse(buf, xmlparser)
        columns_row = skiprows
        start = columns_row + 1
        if rename and add_columns:
            cols = add_columns
        else:
            cols = xmlparser.tables[0][columns_row]
        return pandas.DataFrame(data=xmlparser.tables[0][start:], columns=cols)
    except (ComponentError, EmptyFile):
        raise
    except pandas.errors.EmptyDataError as err:
        raise EmptyFile(f"Empty XML-Excel file: {err}") from err
    except pandas.errors.ParserError as err:
        raise ComponentError(f"Parsing XML-Excel file: {err}") from err
    except Exception as err:
        raise ComponentError(f"Generic error reading XML-Excel: {err}") from err


def _read_parquet(
    buf: Any,
    **extra: Any,
) -> pandas.DataFrame:
    """Read a Parquet file/BytesIO into a DataFrame."""
    try:
        return pandas.read_parquet(buf, **extra)
    except Exception as err:
        raise ComponentError(f"Error reading Parquet: {err}") from err


def _read_json(
    buf: Any,
    *,
    encoding: str | None = None,
    orient: str = "records",
    **extra: Any,
) -> pandas.DataFrame:
    """Read a JSON file/BytesIO into a DataFrame (records orient by default).

    Mirrors ``OpenWithPandas.open_json``.
    """
    resolved_encoding = encoding or "utf-8"
    try:
        return pandas.read_json(buf, orient=orient, encoding=resolved_encoding)
    except pandas.errors.EmptyDataError as err:
        raise EmptyFile(f"Empty JSON: {err}") from err
    except pandas.errors.ParserError as err:
        raise ComponentError(f"Error parsing JSON: {err}") from err
    except Exception as err:
        raise ComponentError(f"Generic error reading JSON: {err}") from err


def _read_html(
    buf: Any,
    *,
    encoding: str | None = None,
    na_values: set | list | None = None,
    parse_dates: dict | None = None,
    add_columns: dict | None = None,
    **extra: Any,
) -> pandas.DataFrame:
    """Read an HTML table file/BytesIO into a DataFrame.

    Mirrors ``OpenWithPandas.open_html``.
    """
    parse_dates_arg = parse_dates or {}
    args: dict[str, Any] = {**extra}
    # Strip unsupported kwargs that open_html historically strips
    args.pop("dtype", None)
    args.pop("skiprows", None)

    resolved_encoding = encoding or "utf-8"
    try:
        dfs = pandas.read_html(
            buf,
            keep_default_na=False,
            flavor="html5lib",
            na_values=na_values,
            encoding=resolved_encoding,
            **parse_dates_arg,
            **args,
        )
        df = dfs[0] if dfs else None
        add_columns = add_columns or {}
        if "names" in add_columns and df is not None:
            df.columns = add_columns["names"]
        return df
    except pandas.errors.EmptyDataError as err:
        raise EmptyFile(f"Empty HTML: {err}") from err
    except pandas.errors.ParserError as err:
        raise ComponentError(f"Parsing HTML: {err}") from err
    except Exception as err:
        raise ComponentError(f"Generic error reading HTML: {err}") from err


# ---------------------------------------------------------------------------
# Public read function
# ---------------------------------------------------------------------------

def read_to_dataframe(
    buf: Any,
    mime: str | None,
    *,
    separator: str = ",",
    decimal: str = ",",
    file_engine: str | None = None,
    sheet_name: str | int | None = None,
    dtypes: dict | None = None,
    parse_dates: dict | None = None,
    na_values: set | list | None = None,
    encoding: str | None = None,
    filter_nan: bool = True,
    remove_empty_strings: bool = True,
    add_columns: dict | None = None,
    limit: int | None = None,
    skiprows: int = 0,
    rename: bool = False,
    **extra: Any,
) -> pandas.DataFrame:
    """Read a file or BytesIO into a pandas DataFrame.

    This is the single entry-point that replaces the per-format logic inlined
    in ``OpenWithPandas.open_csv / open_excel / open_html / open_json``.

    Args:
        buf: Input source.  May be a ``BytesIO``, ``str``, or ``Path``.
             Pandas natively accepts all three for the formats we support.
        mime: MIME type string (e.g. ``"text/csv"``).  Unknown / ``None``
              defaults to ``"csv"`` to match existing OpenWithPandas behaviour.
        separator: Column separator for CSV (default ``","``).
        decimal: Decimal separator character used when parsing CSV numbers
                 (default ``","``).

            Note:
                ``decimal`` defaults to ``","`` (European locale) for backward
                compatibility with OpenWithPandas.  Pass ``decimal="."`` for
                standard US/UK CSVs.
        file_engine: Pandas engine override for Excel formats
                     (``"openpyxl"`` / ``"xlrd"`` / ``"pyxlsb"`` / ``"calamine"``).
                     Auto-selected from ``_EXCEL_ENGINE_DEFAULT`` when not given.
        sheet_name: Sheet name or index for Excel formats.
        dtypes: Column dtype overrides passed as ``dtype=`` to pandas.
        parse_dates: Extra kwargs for parse_dates support (passed as ``**``).
        na_values: Set/list of additional NA values.
        encoding: Character encoding (default ``"utf-8"``).
        filter_nan: When ``True`` (default), pandas applies NA filtering.
        remove_empty_strings: When ``True``, empty string values in the resulting
                              DataFrame are replaced with ``pd.NA``.
        add_columns: Extra column-renaming / header kwargs forwarded to pandas.
        limit: Row limit (maps to ``nrows=``).
        skiprows: Number of header rows to skip (used by XML-Excel branch).
        rename: Whether to use ``add_columns`` as column names in XML-Excel.
        **extra: Additional kwargs forwarded to the format-specific reader.

    Returns:
        A ``pandas.DataFrame``.

    Raises:
        ComponentError: For parse errors or unsupported MIME types.
        EmptyFile: When the source is empty.
        DataNotFound: Not raised directly; re-exported for callers that check
            for missing data after calling this function.
    """
    fmt = _detect_format_from_mime(mime)

    if fmt == "csv":
        df = _read_csv(
            buf,
            separator=separator,
            decimal=decimal,
            encoding=encoding,
            dtypes=dtypes,
            parse_dates=parse_dates,
            na_values=na_values,
            filter_nan=filter_nan,
            add_columns=add_columns,
            limit=limit,
            skiprows=skiprows if skiprows else None,
            **extra,
        )
    elif fmt in {"xlsx", "xls", "xlsb"}:
        engine = file_engine or _EXCEL_ENGINE_DEFAULT.get(fmt, "calamine")
        df = _read_excel(
            buf,
            engine=engine,
            sheet_name=sheet_name,
            dtypes=dtypes,
            parse_dates=parse_dates,
            na_values=na_values,
            filter_nan=filter_nan,
            limit=limit,
            add_columns=add_columns,
            skiprows=skiprows,
            **extra,
        )
    elif fmt == "xml":
        df = _read_xml_excel(
            buf,
            add_columns=add_columns,
            skiprows=skiprows,
            rename=rename,
            **extra,
        )
    elif fmt == "parquet":
        df = _read_parquet(buf, **extra)
    elif fmt == "json":
        df = _read_json(buf, encoding=encoding, **extra)
    elif fmt == "html":
        df = _read_html(
            buf,
            encoding=encoding,
            na_values=na_values,
            parse_dates=parse_dates,
            add_columns=add_columns,
            **extra,
        )
    else:
        raise ComponentError(f"Unsupported MIME type: {mime!r}")

    if remove_empty_strings and df is not None:
        df = df.replace("", pandas.NA)

    return df


# ---------------------------------------------------------------------------
# Public write function
# ---------------------------------------------------------------------------

def write_from_dataframe(
    df: pandas.DataFrame,
    fmt: str,
    buf: Any,
    *,
    separator: str = ",",
    sheet_name: str = "Sheet1",
    index: bool = False,
    encoding: str = "utf-8",
    compression: str | None = None,
    json_orient: str = "records",
    json_lines: bool = False,
    **extra: Any,
) -> None:
    """Write a pandas DataFrame to a file or BytesIO.

    Args:
        df: Source DataFrame to serialise.
        fmt: Output format token.  Must be one of
             ``{"csv", "xlsx", "parquet", "json"}``.
        buf: Output destination.  May be a ``BytesIO``, ``str``, or ``Path``.
        separator: Column separator for CSV (default ``","``).
        sheet_name: Sheet name for xlsx (default ``"Sheet1"``).
        index: Whether to write the DataFrame index (default ``False``).
        encoding: Character encoding for text formats (default ``"utf-8"``).
        compression: Compression codec for Parquet (default ``"snappy"``).
        json_orient: Orientation for JSON output (default ``"records"``).
        json_lines: When ``True``, write newline-delimited JSON (default ``False``).
        **extra: Ignored; present for forward-compatibility.

    Raises:
        ValueError: When ``fmt`` is not a supported format token.
    """
    if fmt == "csv":
        df.to_csv(buf, sep=separator, index=index, encoding=encoding)
        return

    if fmt == "xlsx":
        with pandas.ExcelWriter(buf, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=index)
        return

    if fmt == "parquet":
        df.to_parquet(buf, compression=compression or "snappy", index=index)
        return

    if fmt == "json":
        text = df.to_json(orient=json_orient, lines=json_lines, force_ascii=False)
        if hasattr(buf, "write"):
            # BytesIO expects bytes; StringIO / file-like text accepts str
            data: bytes | str = text.encode(encoding) if isinstance(buf, BytesIO) else text
            buf.write(data)
        else:
            Path(buf).write_text(text, encoding=encoding)
        return

    raise ValueError(
        f"write_from_dataframe: unsupported fmt {fmt!r}. "
        f"Supported: csv, xlsx, parquet, json"
    )
