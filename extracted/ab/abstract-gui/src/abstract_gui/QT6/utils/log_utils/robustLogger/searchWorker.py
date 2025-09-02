from ..imports import *
from typing import *
from dataclasses import dataclass
from PyQt6.QtCore import QObject,pyqtSignal,QThread
from abstract_paths import *
# shared.py (after you create the tabs)

def apply_custom_diff(original_lines: List[str], diff_lines: List[str]) -> str:
    # Skip file path if present
    if diff_lines and '/' in diff_lines[0]:
        diff_lines = diff_lines[1:]
    # Split into hunks at ...
    hunks = []
    current_hunk = []
    for line in diff_lines:
        stripped = line.strip()
        if stripped == '...':
            if current_hunk:
                hunks.append(current_hunk)
            current_hunk = []
        else:
            current_hunk.append(line)
    if current_hunk:
        hunks.append(current_hunk)
    patched = list(original_lines)  # copy
    offset = 0
    for hunk in hunks:
        old_hunk = []
        new_hunk = []
        for line in hunk:
            if line.startswith('-'):
                old_hunk.append(line[1:])
            elif line.startswith('+'):
                new_hunk.append(line[1:])
            else:
                old_hunk.append(line)
                new_hunk.append(line)
        hunk_len = len(old_hunk)
        found = False
        for k in range(offset, len(patched) - hunk_len + 1):
            if all(patched[k + m] == old_hunk[m] for m in range(hunk_len)):
                # Replace
                del patched[k : k + hunk_len]
                patched[k:k] = new_hunk
                offset = k + len(new_hunk)
                found = True
                break
        if not found:
            raise ValueError(f"Hunk not found: {hunk}")
    return '\n'.join(patched)

@dataclass
class initSearchParams:
    directory: str
    paths: Union[bool, str] = True
    exts: Union[bool, str, List[str]] = True
    recursive: bool = True
    strings: List[str] = None
    total_strings: bool = False
    parse_lines: bool = False
    spec_line: Union[bool, int] = False
    get_lines: bool = True
    # ————————————————————————————————————————————————————————————————
# Background worker so the UI doesn’t freeze
class initSearchWorker(QThread):
    log = pyqtSignal(str)
    done = pyqtSignal(list)
    def __init__(self, params: initSearchParams):
        super().__init__()
        self.params = params
    def run(self):
        try:
            if findContent is None:
                raise RuntimeError(
                    "Could not import your finder functions. Import error:\n"
                    f"{_IMPORT_ERR if '_IMPORT_ERR' in globals() else 'unknown'}"
                )
            self.log.emit("🔎 Searching…\n")
            results = findContent(
                directory=self.params.directory,
                paths=self.params.paths,
                exts=self.params.exts,
                recursive=self.params.recursive,
                strings=self.params.strings or [],
                total_strings=self.params.total_strings,
                parse_lines=self.params.parse_lines,
                spec_line=self.params.spec_line,
                get_lines=self.params.get_lines
            )
           
            self.done.emit(results)
        except Exception:
            self.log.emit(traceback.format_exc())
            self.done.emit([])
# ————————————————————————————————————————————————————————————————
# Main GUI
# Define SearchParams if not already defined
# Define SearchParams if not already defined
@dataclass
class SearchParams:
    directory: str
    allowed_exts: Union[bool, Set[str]]
    unallowed_exts: Union[bool, Set[str]]
    exclude_types: Union[bool, Set[str]]
    exclude_dirs: Union[bool, List[str]]
    exclude_patterns: Union[bool, List[str]]
    add: bool
    recursive: bool
    strings: List[str]
    total_strings: bool
    parse_lines: bool
    spec_line: Union[bool, int]
    get_lines: bool

class SearchWorker(QThread):
    log = pyqtSignal(str)
    done = pyqtSignal(list)
    def __init__(self, params: SearchParams):
        super().__init__()
        self.params = params
    def run(self):
        self.log.emit("Starting search...\n")
        try:
            results = findContent(
                **self.params
            )
            self.done.emit(results or [])
            logging.info("Search finished: %d hits", len(results or []))
        except Exception as e:
            tb = "".join(traceback.format_exc())
            logging.exception("Worker crashed: %s", e)
            self.log.emit("❌ Worker crashed:\n" + tb)
