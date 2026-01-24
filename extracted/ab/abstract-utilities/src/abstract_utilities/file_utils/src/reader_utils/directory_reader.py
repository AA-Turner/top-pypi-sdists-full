from .imports import *
from .file_readers import *
# ─── Example walker ──────────────────────────────────────────────────────────
_logger = get_logFile(__name__)

def read_files(files=None,allowed=None):
    allowed = allowed or make_allowed_predicate()
    files = get_all_files(make_list(files or []),allowed)
    collected = {}
    for full_path in files:
        ext = Path(full_path).suffix.lower()

        # ——— 1) Pure-text quick reads —————————————
        if ext in {'.txt', '.md', '.csv', '.tsv', '.log'}:
            try:
                with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                    collected[full_path] = f.read()
            except Exception as e:
                #_logger.warning(f"Failed to read {full_path} as text: {e}")
                pass
            continue

        # ——— 2) Try your DataFrame loader ——————————
        try:
            df_or_map = get_df(full_path)
            if isinstance(df_or_map, (pd.DataFrame, gpd.GeoDataFrame)):
                collected[full_path] = df_or_map
                #_logger.info(f"Loaded DataFrame: {full_path}")
                continue

            if isinstance(df_or_map, dict):
                for sheet, df in df_or_map.items():
                    key = f"{full_path}::[{sheet}]"
                    collected[key] = df
                    #_logger.info(f"Loaded sheet DataFrame: {key}")
                continue
        except Exception as e:
            #_logger.debug(f"get_df failed for {full_path}: {e}")
            pass
        # ——— 3) Fallback to generic text extractor ————
        try:
            parts = read_file_as_text(full_path)  # List[str]
            combined = "\n\n".join(parts)
            collected[full_path] = combined
            #_logger.info(f"Read fallback text for: {full_path}")
        except Exception as e:
            _logger.warning(f"Could not read {full_path} at all: {e}")

    return collected
def read_directory(*args,**kwargs) -> Dict[str, Union[pd.DataFrame, str]]:
    directories,cfg,allowed,include_files,recursive = get_file_filters(*args,**kwargs)

    return read_files(files=directories[0],allowed=allowed)
