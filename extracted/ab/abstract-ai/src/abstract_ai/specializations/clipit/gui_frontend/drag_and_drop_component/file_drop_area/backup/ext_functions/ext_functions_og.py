from ...imports import *

def log_it(self, message: str):        # minimal stub
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    self.log_widget.append(f"[{ts}] {message}")

def _filtered_file_list(self, raw_paths: List[str]) -> List[str]:
    """
    Recursively collect files under directories (excluding node_modules/__pycache__, etc).
    """
    from abstract_utilities.robust_reader import collect_filepaths
    filtered = collect_filepaths(
        raw_paths,
        exclude_dirs=DEFAULT_EXCLUDE_DIRS,
        exclude_file_patterns=DEFAULT_EXCLUDE_FILE_PATTERNS
    )
    self._log(f"_filtered_file_list: Expanded to {len(filtered)} file(s).")
    return filtered

def process_files(self, file_paths: List[str]):
    """
    Same as before, except we log each major step.
    """
    valid_paths = collect_filepaths(file_paths)
    self._log(f"process_files: valid_paths '{valid_paths}'")
    if not valid_paths:
        self.status.setText("⚠️ No valid files detected.")
        self._log("process_files: No valid paths found.")
        return

    count = len(valid_paths)
    status_msg = f"Reading {count} file(s)…"
    self.status.setText(status_msg)
    self._log(status_msg)
    QtWidgets.QApplication.processEvents()
    
    combined_parts = []
    for idx, path in enumerate(valid_paths):
        header = f"=== {path} ===\n"
        combined_parts.append(header)
        self._log(f"process_files: Reading '{path}'")
        try:
            from abstract_utilities.robust_reader import read_file_as_text
            content_str = read_file_as_text(path)
            combined_parts.append(str(content_str))
        except Exception as e:
            err_line = f"[Error reading {os.path.basename(path)}: {e}]\n"
            combined_parts.append(err_line)
            self._log(f"process_files ERROR: {e}")

        if idx < count - 1:
            combined_parts.append("\n\n――――――――――――――――――\n\n")

    final_output = "".join(combined_parts)

    clipboard = QtWidgets.QApplication.clipboard()
    clipboard.setText(final_output, mode=clipboard.Clipboard)

    success_msg = f"✅ Copied {count} file(s) to clipboard!"
    self.status.setText(success_msg)
    self._log(success_msg)
