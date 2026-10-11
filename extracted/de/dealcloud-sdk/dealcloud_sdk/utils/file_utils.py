"""
File utilities for reading various data formats.

These utilities provide consistent file reading across CSV, Excel,
and other tabular data formats with automatic encoding detection.
All paths use **fsspec** so local paths and URIs (``s3://``, ``file://``, etc.)
share one pattern.
"""

import locale
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Literal, Optional, Union

import fsspec
import pandas as pd

if TYPE_CHECKING:
    import polars as pl

logger = logging.getLogger(__name__)


# File format constants
SUPPORTED_CSV_EXTENSIONS = ('.csv', '.tsv', '.txt')
SUPPORTED_EXCEL_EXTENSIONS = ('.xlsx', '.xlsm', '.xls', '.ods')
ALL_SUPPORTED_EXTENSIONS = SUPPORTED_CSV_EXTENSIONS + SUPPORTED_EXCEL_EXTENSIONS


def _path_str(filepath: Union[str, Path]) -> str:
    return str(filepath)


def _data_basename(filepath: Union[str, Path]) -> str:
    s = _path_str(filepath).rstrip("/")
    return s.rsplit("/", 1)[-1].split("?", 1)[0]


def _data_suffix(filepath: Union[str, Path]) -> str:
    return Path(_data_basename(filepath)).suffix.lower()


def detect_encoding(filepath: Union[str, Path]) -> str:
    """
    Detect file encoding by trying common encodings.

    Args:
        filepath: Path or URI to the file to check

    Returns:
        Detected encoding string (e.g., 'utf-8', 'latin-1')

    Example:
        encoding = detect_encoding("data.csv")
        df = read_csv("data.csv", encoding=encoding)
    """
    path_str = _path_str(filepath)

    # Try common encodings in order of preference
    encodings = [
        'utf-8',
        'utf-8-sig',  # UTF-8 with BOM
        'latin-1',
        'cp1252',  # Windows encoding
        locale.getpreferredencoding(False),
    ]

    for encoding in encodings:
        try:
            with fsspec.open(path_str, 'r', encoding=encoding) as f:
                # Try to read the first few lines to verify encoding works
                f.readline()
                return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue

    # If all else fails, return utf-8 with error handling
    return 'utf-8'


def is_supported_file(filepath: Union[str, Path]) -> bool:
    """
    Check if a file is a supported data format.

    Args:
        filepath: Path or URI to check

    Returns:
        True if file extension is supported

    Example:
        if is_supported_file("data.xlsx"):
            df = read_file("data.xlsx")
    """
    return _data_suffix(filepath) in ALL_SUPPORTED_EXTENSIONS


def should_skip_file(filepath: Union[str, Path]) -> bool:
    """
    Check if a file should be skipped during processing.

    Skips hidden files, temporary files, and system files.

    Args:
        filepath: Path or URI to check

    Returns:
        True if file should be skipped

    Example:
        for f in files:
            if should_skip_file(f):
                continue
            process(f)
    """
    filename = _data_basename(filepath)

    # Skip hidden files (Unix-style)
    if filename.startswith('.'):
        return True

    # Skip temporary Excel files
    if filename.startswith('~$'):
        return True

    # Skip zip files
    if filename.lower().endswith('.zip'):
        return True

    return False


def _pandas_to_polars(df: pd.DataFrame) -> "pl.DataFrame":
    """Convert a pandas DataFrame to Polars (requires ``dealcloud-sdk[polars]``)."""
    try:
        import polars as pl
    except ImportError as e:
        raise ImportError(
            "Polars is not installed. Install with: pip install dealcloud-sdk[polars]"
        ) from e
    return pl.from_pandas(df)


def read_csv(
    filepath: Union[str, Path],
    encoding: Optional[str] = None,
    output: Literal["pandas", "polars"] = "pandas",
    **kwargs,
) -> Union[pd.DataFrame, "pl.DataFrame"]:
    """
    Read a CSV file with automatic encoding detection.

    Args:
        filepath: Path or URI to CSV file
        encoding: Encoding to use (auto-detected if not specified)
        output: ``\"pandas\"`` (default) or ``\"polars\"`` for a Polars DataFrame
        **kwargs: Additional arguments passed to pd.read_csv

    Returns:
        pandas or Polars DataFrame per ``output``

    Example:
        df = read_csv("data.csv")
        df = read_csv("data.csv", delimiter=";")
        pl_df = read_csv("data.csv", output="polars")
    """
    path_str = _path_str(filepath)

    if encoding is None:
        encoding = detect_encoding(path_str)

    try:
        with fsspec.open(path_str, 'r', encoding=encoding) as f:
            pdf = pd.read_csv(f, low_memory=False, **kwargs)
    except UnicodeError:
        # Fallback with error handling
        logger.warning(
            f"Encoding {encoding} failed for {path_str}, using utf-8 with error replacement"
        )
        with fsspec.open(path_str, 'r', encoding='utf-8', errors='replace') as f:
            pdf = pd.read_csv(f, low_memory=False, **kwargs)

    if output == "polars":
        return _pandas_to_polars(pdf)
    return pdf


def read_excel(
    filepath: Union[str, Path],
    sheet_name: Union[str, int] = 0,
    output: Literal["pandas", "polars"] = "pandas",
    **kwargs,
) -> Union[pd.DataFrame, "pl.DataFrame"]:
    """
    Read an Excel file with appropriate engine based on format.

    Supports .xlsx, .xlsm, .xls, and .ods formats.

    Args:
        filepath: Path or URI to Excel file
        sheet_name: Sheet name or index to read (default: first sheet)
        output: ``\"pandas\"`` (default) or ``\"polars\"``
        **kwargs: Additional arguments passed to pd.read_excel

    Returns:
        pandas or Polars DataFrame per ``output``

    Example:
        df = read_excel("data.xlsx")
        df = read_excel("data.xlsx", sheet_name="Sheet2")
        pl_df = read_excel("data.xlsx", output="polars")
    """
    path_str = _path_str(filepath)
    file_lower = path_str.lower()

    try:
        with fsspec.open(path_str, 'rb') as f:
            if file_lower.endswith(('.xlsx', '.xlsm')):
                pdf = pd.read_excel(
                    f, engine='openpyxl', sheet_name=sheet_name, **kwargs
                )
            elif file_lower.endswith('.xls'):
                pdf = pd.read_excel(
                    f, engine='xlrd', sheet_name=sheet_name, **kwargs
                )
            elif file_lower.endswith('.ods'):
                pdf = pd.read_excel(
                    f, engine='odf', sheet_name=sheet_name, **kwargs
                )
            else:
                # Try auto-detection
                try:
                    pdf = pd.read_excel(f, sheet_name=sheet_name, **kwargs)
                except ValueError:
                    logger.warning(
                        f"Could not auto-detect Excel format for {path_str}, trying openpyxl"
                    )
                    f.seek(0)
                    pdf = pd.read_excel(
                        f, engine='openpyxl', sheet_name=sheet_name, **kwargs
                    )
    except Exception as e:
        logger.error(f"Failed to read Excel file {path_str}: {e}")
        raise ValueError(
            f"Unsupported file format or corrupted file: {path_str}. Error: {e}"
        ) from e

    if output == "polars":
        return _pandas_to_polars(pdf)
    return pdf


def read_file(
    filepath: Union[str, Path],
    output: Literal["pandas", "polars"] = "pandas",
    **kwargs,
) -> Union[pd.DataFrame, "pl.DataFrame"]:
    """
    Read a data file, automatically detecting format and encoding.

    Supports CSV, TSV, and Excel formats (.xlsx, .xlsm, .xls, .ods).
    Automatically skips hidden and temporary files.

    Args:
        filepath: Path or URI to data file
        output: ``\"pandas\"`` (default) or ``\"polars\"``
        **kwargs: Additional arguments passed to read_csv / read_excel

    Returns:
        pandas or Polars DataFrame per ``output``

    Raises:
        ValueError: If file is hidden/temporary or format is unsupported

    Example:
        df = read_file("data.xlsx")
        df = read_file("data.csv")
        pl_df = read_file("data.csv", output="polars")
    """
    path_str = _path_str(filepath)

    # Skip hidden and temporary files
    if should_skip_file(path_str):
        raise ValueError(f"Skipping hidden or temporary file: {_data_basename(path_str)}")

    # Route to appropriate reader
    suffix = _data_suffix(path_str)

    if suffix in SUPPORTED_CSV_EXTENSIONS:
        return read_csv(path_str, output=output, **kwargs)
    if suffix in SUPPORTED_EXCEL_EXTENSIONS:
        return read_excel(path_str, output=output, **kwargs)
    raise ValueError(f"Unsupported file format: {suffix}")


def get_data_files(
    directory: Union[str, Path],
    recursive: bool = True,
) -> list[Path]:
    """
    Get all supported data files in a directory (local filesystem via fsspec).

    Args:
        directory: Directory to search
        recursive: If True, search subdirectories

    Returns:
        List of file paths for supported data files

    Example:
        files = get_data_files("/path/to/data")
        for f in files:
            df = read_file(f)
    """
    d = str(Path(directory).resolve())
    fs = fsspec.filesystem('file')
    if recursive:
        candidates = [p for p in fs.find(d) if fs.isfile(p)]
    else:
        candidates = [p for p in fs.glob(f"{d}/*") if fs.isfile(p)]
    out: list[Path] = []
    for p in sorted(candidates):
        if is_supported_file(p) and not should_skip_file(p):
            out.append(Path(p))
    return out

