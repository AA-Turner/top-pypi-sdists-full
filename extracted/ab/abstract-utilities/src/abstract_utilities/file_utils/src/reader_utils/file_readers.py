from __future__ import annotations  # keep heavy-proxy type hints lazy (PEP 563)
# file_reader.py
from .imports import (
    imports,
    re,
    os,
    json,
    tempfile,
    shutil,
    Union,
    Dict,
    List,
    get_args,
    datetime,
    Path,
    ezodf,
    gpd,
    pdfplumber,
    pd,
    pytesseract,
    convert_from_path,
    load_dotenv,
    jsonify,
    secure_filename,
    FileStorage,
    make_list,
    get_media_exts,
    is_media_type,
    MIME_TYPES,
    is_str,
    if_not_bool_default,
    get_from_kwargs,
    eatAll,
    eatOuter,
    get_sleep,
    get_caller,
    get_caller_path,
    get_caller_dir,
    SingletonMeta,
    run_pruned_func,
    get_pass_from_key,
    get_password,
    get_print_sudo_cmd,
    get_password_cmd,
    get_sudo_cmd,
    get_raw_password_sudo_cmd,
    get_remote_bash,
    get_remote_ssh,
    get_remote_cmd,
    execute_cmd,
    run_local_cmd,
    run_remote_cmd,
    run_cmd,
    run_ssh_cmd,
    remote_cmd,
    ssh_cmd,
    local_cmd,
    run_any_cmd,
    any_cmd,
    cmd_run,
    PathBackend,
    LocalFS,
    SSHFS,
    REMOTE_RE,
    normalize_items,
    get_output,
    get_cmd_out,
    cmd_input,
    get_output_text,
    get_env_value,
    print_cmd,
    get_sudo_password,
    cmd_run_sudo,
    pexpect_cmd_with_args,
    get_user_pass_host_key,
    execute_cmd_input,
    exec_sudo_capture,
    exec_sudo,
    exec_expect,
    is_remote_file,
    is_remote_dir,
    is_local_file,
    is_local_dir,
    is_file,
    is_dir,
    is_exists,
    check_path_type,
    abstractEnv,
    eatInner,
    safe_split,
    line_contains,
    is_list,
    is_bool,
    get_slash,
    path_join,
    if_not_last_child_join,
    get_home_folder,
    simple_path_join,
    DEFAULT_FILE_NAME,
    DEFAULT_KEY,
    find_and_read_env_file,
    search_for_env_key,
    check_env_file,
    safe_env_load,
    split_eq,
    dotenv_load,
    AbstractEnv,
    get_env_path,
    read_from_file,
    write_to_file,
    get_logFile,
    if_none_default,
    if_none_change,
    get_initial_caller_dir,
    import_tag,
    from_tag,
    DEFAULT_ALLOWED_EXTS,
    DEFAULT_EXCLUDE_TYPES,
    DEFAULT_EXCLUDE_EXTS,
    DEFAULT_EXCLUDE_DIRS,
    DEFAULT_EXCLUDE_PATTERNS,
    AllowedPredicate,
    DEFAULT_EXCLUDE_FILE_PATTERNS,
    DEFAULT_ALLOWED_PATTERNS,
    DEFAULT_ALLOWED_DIRS,
    DEFAULT_ALLOWED_TYPES,
    CANONICAL_MAP,
    DEFAULT_ALLOWED_EXCLUDE_MAP,
    DEFAULT_CANONICAL_MAP,
    ScanConfig,
    SearchParams,
    AllParams,
    get_item_check_cmd,
    get_all_item_check_cmd,
    is_any,
    get_spec_kwargs,
    try_group,
    eatElse,
    clean_line,
    is_line_import,
    is_line_from_import,
    is_from_group_start,
    is_from_group_end,
    clean_imports,
    combine_lone_imports,
    merge_from_import_groups,
    clean_imports_pipeline,
    combine_params,
    get_safe_kwargs,
    create_canonical_map,
    get_safe_canonical_kwargs,
    get_dir_filter_kwargs,
    get_file_filter_kwargs,
    normalize_listlike,
    ensure_exts,
    ensure_patterns,
    ensure_directories,
    get_proper_type_str,
    get_allowed_predicate,
    get_globs,
    get_allowed_files,
    get_allowed_dirs,
    get_filtered_files,
    get_filtered_dirs,
    get_all_allowed_files,
    get_all_allowed_dirs,
    make_allowed_predicate,
    filter_allowed_items,
    derive_all_defaults,
    derive_file_defaults,
    define_defaults,
    get_file_filters,
)
from .pdf_utils import (
    imports,
    re,
    os,
    json,
    tempfile,
    shutil,
    Union,
    Dict,
    List,
    get_args,
    datetime,
    Path,
    ezodf,
    gpd,
    pdfplumber,
    pd,
    pytesseract,
    convert_from_path,
    load_dotenv,
    jsonify,
    secure_filename,
    FileStorage,
    make_list,
    get_media_exts,
    is_media_type,
    MIME_TYPES,
    is_str,
    if_not_bool_default,
    get_from_kwargs,
    eatAll,
    eatOuter,
    get_sleep,
    get_caller,
    get_caller_path,
    get_caller_dir,
    SingletonMeta,
    run_pruned_func,
    get_pass_from_key,
    get_password,
    get_print_sudo_cmd,
    get_password_cmd,
    get_sudo_cmd,
    get_raw_password_sudo_cmd,
    get_remote_bash,
    get_remote_ssh,
    get_remote_cmd,
    execute_cmd,
    run_local_cmd,
    run_remote_cmd,
    run_cmd,
    run_ssh_cmd,
    remote_cmd,
    ssh_cmd,
    local_cmd,
    run_any_cmd,
    any_cmd,
    cmd_run,
    PathBackend,
    LocalFS,
    SSHFS,
    REMOTE_RE,
    normalize_items,
    get_output,
    get_cmd_out,
    cmd_input,
    get_output_text,
    get_env_value,
    print_cmd,
    get_sudo_password,
    cmd_run_sudo,
    pexpect_cmd_with_args,
    get_user_pass_host_key,
    execute_cmd_input,
    exec_sudo_capture,
    exec_sudo,
    exec_expect,
    is_remote_file,
    is_remote_dir,
    is_local_file,
    is_local_dir,
    is_file,
    is_dir,
    is_exists,
    check_path_type,
    abstractEnv,
    eatInner,
    safe_split,
    line_contains,
    is_list,
    is_bool,
    get_slash,
    path_join,
    if_not_last_child_join,
    get_home_folder,
    simple_path_join,
    DEFAULT_FILE_NAME,
    DEFAULT_KEY,
    find_and_read_env_file,
    search_for_env_key,
    check_env_file,
    safe_env_load,
    split_eq,
    dotenv_load,
    AbstractEnv,
    get_env_path,
    read_from_file,
    write_to_file,
    get_logFile,
    if_none_default,
    if_none_change,
    get_initial_caller_dir,
    import_tag,
    from_tag,
    DEFAULT_ALLOWED_EXTS,
    DEFAULT_EXCLUDE_TYPES,
    DEFAULT_EXCLUDE_EXTS,
    DEFAULT_EXCLUDE_DIRS,
    DEFAULT_EXCLUDE_PATTERNS,
    AllowedPredicate,
    DEFAULT_EXCLUDE_FILE_PATTERNS,
    DEFAULT_ALLOWED_PATTERNS,
    DEFAULT_ALLOWED_DIRS,
    DEFAULT_ALLOWED_TYPES,
    CANONICAL_MAP,
    DEFAULT_ALLOWED_EXCLUDE_MAP,
    DEFAULT_CANONICAL_MAP,
    ScanConfig,
    SearchParams,
    AllParams,
    get_item_check_cmd,
    get_all_item_check_cmd,
    is_any,
    get_spec_kwargs,
    try_group,
    eatElse,
    clean_line,
    is_line_import,
    is_line_from_import,
    is_from_group_start,
    is_from_group_end,
    clean_imports,
    combine_lone_imports,
    merge_from_import_groups,
    clean_imports_pipeline,
    combine_params,
    get_safe_kwargs,
    create_canonical_map,
    get_safe_canonical_kwargs,
    get_dir_filter_kwargs,
    get_file_filter_kwargs,
    normalize_listlike,
    ensure_exts,
    ensure_patterns,
    ensure_directories,
    get_proper_type_str,
    get_allowed_predicate,
    get_globs,
    get_allowed_files,
    get_allowed_dirs,
    get_filtered_files,
    get_filtered_dirs,
    get_all_allowed_files,
    get_all_allowed_dirs,
    make_allowed_predicate,
    filter_allowed_items,
    derive_all_defaults,
    derive_file_defaults,
    define_defaults,
    get_file_filters,
    if_none_return,
    write_pdf,
    read_pdf,
    is_pdf_path,
    get_pdf_obj,
    get_separate_pages,
    get_pdf_pages,
    save_pdf,
    split_pdf,
    pdf_to_img_list,
    img_to_txt_list,
    open_pdf_file,
    get_pdfs_in_directory,
    get_all_pdf_in_directory,
    collate_pdfs,
)
_logger = get_logFile(__name__)

import csv as _csv
import io as _io
from .xlsx_reader import (
    read_xlsx,
)


def _is_filestorage(obj):
    """isinstance(obj, FileStorage) that never crashes when werkzeug is absent."""
    try:
        return isinstance(obj, FileStorage)
    except Exception:
        return False


def _rows_to_csv_text(rows):
    """Serialize a list of dicts to CSV text using only the stdlib."""
    if not rows:
        return ""
    fieldnames = []
    for r in rows:
        if isinstance(r, dict):
            for k in r.keys():
                if k not in fieldnames:
                    fieldnames.append(k)
    buf = _io.StringIO()
    writer = _csv.DictWriter(buf, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow({k: (r.get(k, "") if isinstance(r, dict) else "") for k in fieldnames})
    return buf.getvalue()


def _apply_row_filters(rows, nrows=None, skiprows=None, condition=None, indices=None):
    """Apply skiprows, then filter_df (nrows/condition/indices), to a list of dicts."""
    if skiprows is not None:
        if isinstance(skiprows, int):
            rows = rows[skiprows:]
        elif isinstance(skiprows, (list, tuple, set)):
            skip = set(skiprows)
            rows = [r for i, r in enumerate(rows) if i not in skip]
    return filter_df(rows, nrows=nrows, condition=condition, indices=indices)


def _read_csv_as_dicts(path, ext, nrows=None, skiprows=None, condition=None, indices=None):
    """Read .csv/.tsv/.txt into a list of dicts with the stdlib csv module."""
    delimiter = {'.csv': ',', '.tsv': '\t'}.get(ext)
    with open(path, 'r', encoding='utf-8', errors='replace', newline='') as f:
        if delimiter is None:  # .txt -> sniff, else default to comma
            sample = f.read(8192)
            f.seek(0)
            try:
                dialect = _csv.Sniffer().sniff(sample, delimiters=",\t;|")
                reader = _csv.DictReader(f, dialect=dialect)
            except Exception:
                reader = _csv.DictReader(f)
        else:
            reader = _csv.DictReader(f, delimiter=delimiter)
        rows = [dict(r) for r in reader]
    return _apply_row_filters(rows, nrows=nrows, skiprows=skiprows,
                              condition=condition, indices=indices)


def _df_to_csv_text(df):
    """CSV text for a real DataFrame/GeoDataFrame (only call when pd is present)."""
    if gpd and isinstance(df, gpd.GeoDataFrame):
        gdf = df.copy()
        gdf["geometry"] = gdf["geometry"].apply(lambda g: g.wkt if g is not None else "")
        return gdf.to_csv(index=False)
    return df.to_csv(index=False)


def convert_date_string(s):
    # … your existing stub or real implementation …
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None
# file_utils.py (below your existing imports)




def source_engine_for_ext(ext: str) -> str:
    ext = ext.lower()
    mapping = {
        '.parquet': 'pyarrow',
        '.txt':    'python',
        '.csv':    'python',
        '.tsv':    'python',
        '.xlsx':   'openpyxl',
        '.xls':    'xlrd',
        '.xlsb':   'pyxlsb',
        '.ods':    'odf',
        '.geojson':'GeoJSON',
    }
    return mapping.get(ext)

def is_valid_file_path(path: str) -> Union[str, None]:
    if not (isinstance(path, str) and path.strip()):
        return None
    if os.path.isfile(path):
        return os.path.splitext(path)[1].lower()
    return None

def is_dataframe(obj) -> bool:
    types_ = []
    if pd:
        types_.append(pd.DataFrame)
    if gpd:
        types_.append(gpd.GeoDataFrame)
    return bool(types_) and isinstance(obj, tuple(types_))

def create_dataframe(data=None, columns=None) -> pd.DataFrame:
    if is_dataframe(data):
        return data.copy()
    if pd:
        data = data or {}
        if isinstance(data, dict):
            data = [data]
            if columns is None:
                all_keys = set()
                for row in data:
                    if isinstance(row, dict):
                        all_keys.update(row.keys())
                columns = list(all_keys)
            if columns is False:
                columns = None
        try:
            return pd.DataFrame(data, columns=columns)
        except Exception as e:
            #_logger.error(f"Failed to create DataFrame: {e}")
            return pd.DataFrame([], columns=columns)
    # ── stdlib fallback: normalize to a list of dicts ──
    if data is None:
        data = []
    if isinstance(data, dict):
        rows = [data]
    elif isinstance(data, list):
        rows = data
    else:
        rows = [data]
    if columns:
        projected = []
        for row in rows:
            if isinstance(row, dict):
                projected.append({c: row.get(c) for c in columns})
            else:
                projected.append(row)
        return projected
    return rows

def read_ods_file(path: str) -> dict[str, pd.DataFrame]:
    if not (ezodf and pd):
        raise ModuleNotFoundError("Reading .ods requires 'ezodf'/'pandas'; install it to read this format.")
    if not is_valid_file_path(path):
        #_logger.error(f"File not found or invalid: {path}")
        return {}
    try:
        doc = ezodf.opendoc(path)
    except Exception as e:
        #_logger.error(f"Failed to open ODS document: {e}")
        return {}
    sheets: dict[str, pd.DataFrame] = {}
    for sheet in doc.sheets:
        table_rows = []
        for row in sheet.rows():
            row_data = []
            for cell in row:
                if cell.value_type == 'date':
                    row_data.append(convert_date_string(str(cell.value)))
                else:
                    row_data.append(cell.value)
            table_rows.append(row_data)
        df = pd.DataFrame(table_rows)
        sheets[sheet.name] = df
        #_logger.info(f"Processed sheet: {sheet.name}")
    return sheets

def read_ods_as_excel(path: str, xlsx_path: str | None = None) -> pd.DataFrame:
    if not pd:
        raise ModuleNotFoundError("Reading .ods requires 'ezodf'/'pandas'; install it to read this format.")
    if not is_valid_file_path(path):
        #_logger.error(f"File not found or invalid: {path}")
        return pd.DataFrame()
    if xlsx_path is None:
        tmp_dir = tempfile.mkdtemp()
        xlsx_path = os.path.join(tmp_dir, os.path.basename(path) + '.xlsx')
        cleanup_temp = True
    else:
        cleanup_temp = False
    try:
        # You must implement ods_to_xlsx(...) externally
        ods_to_xlsx(path, xlsx_path)
    except Exception as e:
        #_logger.error(f"ODS→XLSX conversion failed: {e}")
        if cleanup_temp:
            shutil.rmtree(tmp_dir)
        return pd.DataFrame()
    try:
        df = pd.read_excel(xlsx_path, engine='openpyxl')
    except Exception as e:
        #_logger.error(f"Failed to read converted XLSX: {e}")
        df = pd.DataFrame()
    finally:
        if cleanup_temp:
            shutil.rmtree(tmp_dir)
    return df

def filter_df(
    df: pd.DataFrame,
    nrows: int | None = None,
    condition: pd.Series | None = None,
    indices: list[int] | None = None
) -> pd.DataFrame:
    if is_dataframe(df):
        if nrows is not None:
            df = df.head(nrows)
        if condition is not None:
            df = df[condition]
        if indices is not None:
            df = df.iloc[indices]
        return df
    if isinstance(df, list):
        if nrows is not None:
            df = df[:nrows]
        if condition is not None and callable(condition):
            df = [r for r in df if condition(r)]
        if indices is not None:
            df = [df[i] for i in indices if -len(df) <= i < len(df)]
        return df
    return df

def read_shape_file(path: str) -> Union[gpd.GeoDataFrame, None]:
    ext = is_valid_file_path(path)
    if not ext:
        #_logger.error(f"Shape file not found: {path}")
        return None
    ext = ext.lower()
    if ext == '.prj':
        return read_from_file(path)  # Must return GeoDataFrame
    if not gpd:
        raise ModuleNotFoundError("Reading shape files requires 'geopandas'; install it to read this format.")
    try:
        if ext in ('.shp', '.cpg', '.dbf', '.shx'):
            return gpd.read_file(path)
        if ext == '.geojson':
            return gpd.read_file(path, driver='GeoJSON')
    except Exception as e:
        #_logger.error(f"Failed to read spatial data ({path}): {e}")
        return None
    #_logger.error(f"Unsupported spatial extension: {ext}")
    return None
import warnings

_PDF_BACKEND_WARNED = False


def _warn_pdf_voided():
    """Emit a single warning when a PDF is encountered without a PDF backend."""
    global _PDF_BACKEND_WARNED
    if not _PDF_BACKEND_WARNED:
        _PDF_BACKEND_WARNED = True
        warnings.warn(
            "PDF reading skipped: no PDF backend installed. Install 'pdfplumber' "
            "(and 'pdf2image' + 'pytesseract' for OCR) to read PDFs; until then "
            "PDF files are voided (returned as None).",
            RuntimeWarning,
            stacklevel=2,
        )


def pdf_to_text(path, keep_page_breaks=True, ocr_if_empty=True):
    """
    Return the full text of *path* (str or Path) as a single string.

    keep_page_breaks → insert "\f" between pages so you can split later.
    ocr_if_empty     → any page with no text layer is rasterised & OCR'd.

    If no PDF backend is installed, the PDF is voided: a single warning is
    emitted and ``None`` is returned (rather than raising).
    """
    if not pdfplumber:                      # backend not installed → void
        _warn_pdf_voided()
        return None

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    all_pages = []

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""   # might be None
            if (not text.strip()) and ocr_if_empty:
                # rasterise at 300 dpi then Tesseract — best effort; if the OCR
                # stack (pdf2image/poppler, pytesseract) is absent, skip it.
                try:
                    img = convert_from_path(str(path), dpi=300, first_page=i, last_page=i)[0]
                    text = pytesseract.image_to_string(img, lang="eng")
                except Exception:
                    pass
            all_pages.append(text)

    sep = "\f" if keep_page_breaks else "\n"
    return sep.join(all_pages)
def get_df(
    source: Union[
        str,
        pd.DataFrame,
        gpd.GeoDataFrame,
        dict,
        list,
        FileStorage
    ],
    nrows: int | None = None,
    skiprows: list[int] | int | None = None,
    condition: pd.Series | None = None,
    indices: list[int] | None = None
) -> Union[pd.DataFrame, gpd.GeoDataFrame, dict[str, Union[pd.DataFrame, str]], None]:
    """
    Load a DataFrame or GeoDataFrame from various sources, then apply optional filters.
    If `source` is a directory, returns read_directory(source) instead (a dict).
    """

    # ─── Check for directory first ─────────────────────────────────────────────
    if isinstance(source, str) and os.path.isdir(source):
        return read_directory(root_path=source)

    # ─── If already a DataFrame/GeoDataFrame, just filter and return ───────────
    if is_dataframe(source):
        #_logger.info("Source is already a DataFrame/GeoDataFrame; applying filters.")
        return filter_df(source, nrows=nrows, condition=condition, indices=indices)

    if source is None:
        #_logger.error("No source provided to get_df().")
        return None

    # ─── Next: If source is a file path, read according to extension ───────────
    if isinstance(source, str) and os.path.isfile(source):
        ext = os.path.splitext(source)[1].lower()
        try:
            #_logger.info(f"Loading file {source} with extension '{ext}'.")
            if ext in ('.csv', '.tsv', '.txt'):
                if pd:
                    sep = {'.csv': ',', '.tsv': '\t', '.txt': None}.get(ext)
                    df = pd.read_csv(source, skiprows=skiprows, sep=sep, nrows=nrows)
                else:
                    return _read_csv_as_dicts(source, ext, nrows=nrows, skiprows=skiprows,
                                              condition=condition, indices=indices)
            elif ext == '.ods':
                if not (ezodf or pd):
                    raise ModuleNotFoundError("Reading .ods requires 'ezodf'/'pandas'; install it to read this format.")
                df = read_ods_as_excel(source)
            elif ext == '.xlsx':
                if pd:
                    engine = source_engine_for_ext(ext)
                    df = pd.read_excel(source, skiprows=skiprows, engine=engine, nrows=nrows)
                else:
                    rows = read_xlsx(source, as_dicts=True)
                    return _apply_row_filters(rows, nrows=nrows, skiprows=skiprows,
                                              condition=condition, indices=indices)
            elif ext in ('.xls', '.xlsb'):
                if not pd:
                    raise ModuleNotFoundError("Reading .xls requires 'pandas' + an Excel engine; install them to read this format.")
                engine = source_engine_for_ext(ext)
                df = pd.read_excel(source, skiprows=skiprows, engine=engine, nrows=nrows)
            elif ext == '.json':
                df = safe_read_from_json(source)
                return df
            elif ext == '.geojson':
                if gpd:
                    return read_shape_file(source)
                with open(source, 'r', encoding='utf-8', errors='replace') as f:
                    return json.load(f)
            elif ext == '.parquet':
                if not pd:
                    raise ModuleNotFoundError("Reading .parquet requires 'pandas' + 'pyarrow'; install them to read this format.")
                df = pd.read_parquet(source)
            elif ext in ('.shp', '.cpg', '.dbf', '.shx', '.prj'):
                if not gpd:
                    raise ModuleNotFoundError("Reading shape files requires 'geopandas'; install it to read this format.")
                return read_shape_file(source)
            elif ext in ['.pdf']:
                df = pdf_to_text(source)
                return df
            else:
                df = read_from_file(source)
                return df

            if not isinstance(df, (dict, list)) and not _is_filestorage(df):
                return filter_df(df, nrows=nrows, condition=condition, indices=indices)
            source = df  # pass on to next block if needed

        except ModuleNotFoundError:
            raise
        except Exception as e:
            #_logger.error(f"Failed to read '{source}': {e}")
            return None

    # ─── If source is FileStorage (uploaded) ───────────────────────────────────
    if _is_filestorage(source):
        if not pd:
            raise ModuleNotFoundError("Reading uploaded spreadsheets requires 'pandas' + an Excel engine; install them to read this format.")
        try:
            filename = secure_filename(source.filename or "uploaded.xlsx")
            #_logger.info(f"Reading uploaded file: {filename}")
            df = pd.read_excel(source.stream, nrows=nrows)
            return filter_df(df, nrows=nrows, condition=condition, indices=indices)
        except Exception as e:
            #_logger.error(f"Failed to read FileStorage: {e}")
            return None

    # ─── If source is dict or list, turn into DataFrame ────────────────────────
    if isinstance(source, (dict, list)):
        #_logger.info("Creating DataFrame from in-memory data structure.")
        if pd:
            df = pd.DataFrame(source)
        else:
            df = create_dataframe(source)
        return filter_df(df, nrows=nrows, condition=condition, indices=indices)

    _logger.error(f"Unsupported source type: {type(source)}")
    return None

def read_any_file(full_path):
    data = None 
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Not a valid path: {full_path!r}")

    # ── If this is a directory, walk it via read_directory(...) ─────────────────
    if os.path.isdir(full_path):
        # read_directory returns a dict: { relative_path: (DataFrame or text) }
        nested_dict: Dict[str, Union[pd.DataFrame, gpd.GeoDataFrame, str]] = read_directory(full_path)

        for rel, content in nested_dict.items():
            # `content` is a DataFrame, GeoDataFrame, list-of-dicts, or plain‐text string
            if is_dataframe(content):
                data = _df_to_csv_text(content)
            elif isinstance(content, list):
                data = _rows_to_csv_text(content)
            else:
                # Already a text blob
                data = content

        return data
    # ── At this point, full_path is guaranteed to be a file ───────────────────────
    ext = os.path.splitext(full_path)[1].lower()

    # 1) PURE TEXT EXTENSION?
    #if ext in SUPPORTED_TEXT_EXTENSIONS:
    try:
        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            raw = f.read()
        data = raw
    except Exception as e:
        raise ValueError(f"Error reading text file {full_path!r}: {e}")

    

    # 2) ANY OTHER FILETYPE → delegate to get_df(...) and convert result to text
    try:
        df_or = get_df(full_path)
    except Exception as e:
        raise ValueError(f"get_df() failed for {full_path!r}: {e}")

    # 2a) If get_df returned a dict (e.g. an ODS with multiple sheets, or a directory)
    if isinstance(df_or, dict):
        # Join each sheet or sub‐file’s DataFrame into one big text block
        for key, value in df_or.items():
            if is_dataframe(value):
                block = f"=== {key} ===\n" + _df_to_csv_text(value)
            elif isinstance(value, list):
                block = f"=== {key} ===\n" + _rows_to_csv_text(value)
            else:
                # It was already plain‐text under that key
                block = f"=== {key} ===\n" + str(value)
            data = block

        return data

    # 2b) If get_df returned a DataFrame or GeoDataFrame directly
    if is_dataframe(df_or):
        data = _df_to_csv_text(df_or)
        return data

    # 2c) If get_df returned a list of dicts (rare, but possible)
    if isinstance(df_or, list):
        if pd:
            try:
                temp_df = pd.DataFrame(df_or)
                data = temp_df.to_csv(index=False)
            except Exception:
                data = repr(df_or)
        else:
            try:
                data = _rows_to_csv_text(df_or)
            except Exception:
                data = repr(df_or)
        return data
    return data or repr(df_or)
def read_file_as_text(paths: Union[str, List[str]]) -> List[str]:
    """
    Given one path or a list of paths, return a list of textual representations
    for each “file” found.  If a given path is:
    
      1) A directory → we call read_directory(...) on it (which skips node_modules,
         __pycache__, *.ini, etc.) and iterate over each (relative_path → content).
      2) A plain‐text file (extension ∈ SUPPORTED_TEXT_EXTENSIONS) → we open it and return its raw text.
      3) Anything else (e.g. .xlsx, .ods, .parquet, .shp, etc.) → we delegate to get_df(...) and then
         convert whatever get_df(...) gives us into CSV or “to_string()” as appropriate.
    
    Returns:
        A list of strings—each string is the “file’s contents” for one actual file.  
        (Ordering is “filesystem walk order” for directories, and “in order of the input list” for files.)
    
    Raises:
        FileNotFoundError if any path in `paths` does not exist.
        ValueError if a file cannot be parsed/read.
    """
    # Ensure we have a list to iterate
    if isinstance(paths, str):
        files_to_process = [paths]
    else:
        files_to_process = list(paths)
    all_data: List[str] = []
    for full_path in files_to_process:
        data = read_any_file(full_path)
        # 2d) Otherwise, fall back to repr()
        all_data.append(data)
    return all_data
