from ...imports import *
def _filtered_file_list(self, raw_paths: List[str]) -> List[str]:
    """
    Recursively collect files under directories (excluding node_modules/__pycache__, etc).
    Always returns a flat List[str].
    """
    filtered = collect_filepaths(
        raw_paths,
        exclude_dirs=DEFAULT_EXCLUDE_DIRS,
        exclude_file_patterns=DEFAULT_EXCLUDE_FILE_PATTERNS
    )
    self._log(f"_filtered_file_list: Expanded to {len(filtered)} file(s).")
    return filtered
