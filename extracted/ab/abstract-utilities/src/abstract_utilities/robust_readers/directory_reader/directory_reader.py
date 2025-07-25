import os
from typing import *
from ..file_filtering import *
from ..file_handlers import *
# ─── Example walker ──────────────────────────────────────────────────────────
_logger = get_logFile(__name__)


def read_directory(
    root_path: str,
    *,
    allowed_exts:     Set[str] = DEFAULT_ALLOWED_EXTS,
    unallowed_exts:   Set[str] = DEFAULT_UNALLOWED_EXTS,
    exclude_types:    Set[str] = DEFAULT_EXCLUDE_TYPES,
    exclude_dirs:     List[str] = DEFAULT_EXCLUDE_DIRS,
    exclude_patterns: List[str] = DEFAULT_EXCLUDE_PATTERNS,
) -> Dict[str, Union[pd.DataFrame, str]]:
    allowed = make_allowed_predicate(
        allowed_exts   = allowed_exts,
        unallowed_exts = unallowed_exts,
        exclude_types  = exclude_types,
        extra_dirs     = exclude_dirs,
        extra_patterns = exclude_patterns,
    )
    files=[]
    
    root_paths = make_list(root_path)
    for root_path in root_paths:
        if os.path.isdir(root_path):
            root_paths = [item for item in glob.glob(os.path.join(f"{root_path}","**"),recursive=True) if allowed(item)]
            directories = [item for item in root_paths if os.path.isdir(item) and allowed(item)]
            files+=[item for item in root_paths if os.path.isfile(item) and allowed(item)]
            
            for directory in directories:
                files+=collect_files(
                    directory,
                    allowed_exts     = allowed_exts,
                    unallowed_exts   = unallowed_exts,
                    exclude_types    = exclude_types,
                    exclude_dirs     = exclude_dirs,
                    exclude_patterns = exclude_patterns,
                )
        else:
            files+=[item for item in make_list(root_path) if os.path.isfile(item) and allowed(item)]
    
    collected = {}
    for full_path in files:
        ext = Path(full_path).suffix.lower()

        # ——— 1) Pure-text quick reads —————————————
        if ext in {'.txt', '.md', '.csv', '.tsv', '.log'}:
            try:
                with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                    collected[full_path] = f.read()
            except Exception as e:
                _logger.warning(f"Failed to read {full_path} as text: {e}")
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
            _logger.debug(f"get_df failed for {full_path}: {e}")

        # ——— 3) Fallback to generic text extractor ————
        try:
            parts = read_file_as_text(full_path)  # List[str]
            combined = "\n\n".join(parts)
            collected[full_path] = combined
            #_logger.info(f"Read fallback text for: {full_path}")
        except Exception as e:
            _logger.warning(f"Could not read {full_path} at all: {e}")

    return collected
