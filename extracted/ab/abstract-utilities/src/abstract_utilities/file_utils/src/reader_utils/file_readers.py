# file_reader.py
from .imports import *
from .pdf_utils import *
_logger = get_logFile(__name__)
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
    return isinstance(obj, (pd.DataFrame, gpd.GeoDataFrame))

def create_dataframe(data=None, columns=None) -> pd.DataFrame:
    # … unchanged …
    if is_dataframe(data):
        return data.copy()
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

def read_ods_file(path: str) -> dict[str, pd.DataFrame]:
    # … unchanged …
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
    # … unchanged …
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
    if nrows is not None:
        df = df.head(nrows)
    if condition is not None:
        df = df[condition]
    if indices is not None:
        df = df.iloc[indices]
    return df

def read_shape_file(path: str) -> Union[gpd.GeoDataFrame, None]:
    # … unchanged …
    ext = is_valid_file_path(path)
    if not ext:
        #_logger.error(f"Shape file not found: {path}")
        return None
    ext = ext.lower()
    try:
        if ext in ('.shp', '.cpg', '.dbf', '.shx'):
            return gpd.read_file(path)
        if ext == '.geojson':
            return gpd.read_file(path, driver='GeoJSON')
        if ext == '.prj':
            return read_from_file(path)  # Must return GeoDataFrame
    except Exception as e:
        #_logger.error(f"Failed to read spatial data ({path}): {e}")
        return None
    #_logger.error(f"Unsupported spatial extension: {ext}")
    return None
def pdf_to_text(path, keep_page_breaks=True, ocr_if_empty=True):
    """
    Return the full text of *path* (str or Path) as a single string.

    keep_page_breaks → insert "\f" between pages so you can split later.
    ocr_if_empty     → any page with no text layer is rasterised & OCR'd.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(path)

    all_pages = []

    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""   # might be None
            if (not text.strip()) and ocr_if_empty:
                # rasterise at 300 dpi then Tesseract
                img = convert_from_path(str(path), dpi=300, first_page=i, last_page=i)[0]
                text = pytesseract.image_to_string(img, lang="eng")
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
                sep = {'.csv': ',', '.tsv': '\t', '.txt': None}.get(ext)
                df = pd.read_csv(source, skiprows=skiprows, sep=sep, nrows=nrows)
            elif ext in ('.ods', '.xlsx', '.xls', '.xlsb'):
                engine = source_engine_for_ext(ext)
                if ext == '.ods':
                    df = read_ods_as_excel(source)
                else:
                    df = pd.read_excel(source, skiprows=skiprows, engine=engine, nrows=nrows)
            elif ext == '.json':
                df = safe_read_from_json(source)
                return df
            elif ext == '.parquet':
                df = pd.read_parquet(source)
            elif ext in ('.shp', '.cpg', '.dbf', '.shx', '.geojson', '.prj'):
                return read_shape_file(source)
            elif ext in ['.pdf']:
                df = pdf_to_text(source)
                return df
            else:
                df = read_from_file(source)
                return df

            if not isinstance(df, (dict, list, FileStorage)):
                return filter_df(df, nrows=nrows, condition=condition, indices=indices)
            source = df  # pass on to next block if needed

        except Exception as e:
            #_logger.error(f"Failed to read '{source}': {e}")
            return None

    # ─── If source is FileStorage (uploaded) ───────────────────────────────────
    if isinstance(source, FileStorage):
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
        df = pd.DataFrame(source)
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
            # `content` is either a DataFrame, GeoDataFrame, or a plain‐text string
            if isinstance(content, (pd.DataFrame, gpd.GeoDataFrame)):
                # If GeoDataFrame, convert geometry column to WKT before CSV
                if isinstance(content, gpd.GeoDataFrame):
                    gdf = content.copy()
                    gdf["geometry"] = gdf["geometry"].apply(lambda g: g.wkt if g is not None else "")
                    data = gdf.to_csv(index=False)
                else:
                    data = content.to_csv(index=False)
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
            if isinstance(value, (pd.DataFrame, gpd.GeoDataFrame)):
                if isinstance(value, gpd.GeoDataFrame):
                    gdf = value.copy()
                    gdf["geometry"] = gdf["geometry"].apply(lambda g: g.wkt if g is not None else "")
                    block = f"=== {key} ===\n" + gdf.to_csv(index=False)
                else:
                    block = f"=== {key} ===\n" + value.to_csv(index=False)
            else:
                # It was already plain‐text under that key
                block = f"=== {key} ===\n" + str(value)
            data = block

        return data

    # 2b) If get_df returned a DataFrame or GeoDataFrame directly
    if isinstance(df_or, (pd.DataFrame, gpd.GeoDataFrame)):
        if isinstance(df_or, gpd.GeoDataFrame):
            gdf = df_or.copy()
            gdf["geometry"] = gdf["geometry"].apply(lambda g: g.wkt if g is not None else "")
            data = gdf.to_csv(index=False)
        else:


            data = df_or.to_csv(index=False)

        return data

    # 2c) If get_df returned a list of dicts (rare, but possible)
    if isinstance(df_or, list):
        try:
            temp_df = pd.DataFrame(df_or)
            data = temp_df.to_csv(index=False)
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
