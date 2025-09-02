# attach_from_neighborhood.py
from __future__ import annotations
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path
import sys, types, inspect,traceback
from typing import *
from PyQt6.QtCore import  QThread,pyqtSignal
from abstract_utilities.dynimport import import_symbols_to_parent
import_modules = [
    {"module":'abstract_paths.content_utils.find_content',"symbols":['findContent','getLineNums','findContentAndEdit','findContent','get_line_content']},
    {"module":'abstract_paths.content_utils.find_content',"symbols":['getLineNums','findContentAndEdit','findContent','get_line_content']}
     ]
import_symbols_to_parent(import_modules, update_all=True)
from dataclasses import dataclass
import logging
# Data structures
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
    cfg:Union[bool, List[str]]
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


def _ensure_pkg(name: str, path: Path | None) -> types.ModuleType:
    """Create or return a package module with an optional __path__."""
    mod = sys.modules.get(name)
    if mod is None:
        mod = types.ModuleType(name)
        mod.__package__ = name
        if path is not None:
            # Make it a package (namespace-like) by giving it a __path__
            mod.__path__ = [str(path)]  # type: ignore[attr-defined]
        sys.modules[name] = mod
    return mod

def _exec_module(name: str, file: Path):
    spec = spec_from_file_location(name, str(file))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {file}")
    mod = module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

def attach_from_neighborhood(
    obj_or_cls,
    *,
    base_file: str | Path,
    functions_name: str = "functions",     # "functions" dir or "functions.py"
    imports_name: str = "imports.py",      # sibling imports filename
    include_private: bool = True,
    only_defined_here: bool = True,
    prefix_with_module: bool = False,
) -> list[str]:
    """
    Build a virtual package so modules like `from ..imports import *` work:
      <root_pkg>
        ├── imports (from imports.py)
        └── functions  (from functions.py or functions/..)
    Then attach all top-level callables from functions to the *class*.
    """
    cls = obj_or_cls if inspect.isclass(obj_or_cls) else obj_or_cls.__class__
    base = Path(base_file).resolve()
    root_dir = base.parent

    # 1) Create a unique root package
    root_pkg = f"_dynpkg_{abs(hash(str(root_dir)))}"
    _ensure_pkg(root_pkg, root_dir)  # parent exists & has __path__

    # 2) Load sibling imports.py into <root_pkg>.imports if present
    imp_path = root_dir / imports_name
    if imp_path.exists():
        _exec_module(f"{root_pkg}.imports", imp_path)

    # 3) Load functions (file or package dir) under <root_pkg>.functions
    funcs_attached_from: list[tuple[str, types.ModuleType]] = []

    funcs_dir = root_dir / functions_name
    funcs_file = root_dir / (functions_name if functions_name.endswith(".py")
                             else f"{functions_name}.py")

    if funcs_dir.is_dir():
        # Create package shell for <root_pkg>.functions
        funcs_pkg_name = f"{root_pkg}.functions"
        _ensure_pkg(funcs_pkg_name, funcs_dir)

        # If __init__.py exists, execute it to match real package semantics
        init_py = funcs_dir / "__init__.py"
        if init_py.exists():
            _exec_module(funcs_pkg_name, init_py)

        # Load all direct .py submodules under functions/
        for py in sorted(p for p in funcs_dir.iterdir() if p.suffix == ".py" and p.name != "__init__.py"):
            modname = f"{funcs_pkg_name}.{py.stem}"
            m = _exec_module(modname, py)
            funcs_attached_from.append((py.stem, m))

    elif funcs_file.is_file():
        # Single module mounted as <root_pkg>.functions
        modname = f"{root_pkg}.functions"
        m = _exec_module(modname, funcs_file)
        funcs_attached_from.append(("functions", m))
    else:
        # Nothing to attach; return quietly
        setattr(cls, "_attached_functions", tuple())
        return []

    # 4) Attach callables to the CLASS so they bind on instances
    attached: list[str] = []
    for short_name, mod in funcs_attached_from:
        for name, obj in vars(mod).items():
            if not callable(obj) or isinstance(obj, type):
                continue
            if only_defined_here and getattr(obj, "__module__", None) != mod.__name__:
                continue
            if not include_private and name.startswith("_"):
                continue
            if name.startswith("__") and name.endswith("__"):
                continue
            attr = f"{short_name}__{name}" if prefix_with_module else name
            try:
                setattr(cls, attr, obj)
                attached.append(attr)
            except Exception:
                # Skip conflicts but keep going
                pass

    try:
        setattr(cls, "_attached_functions", tuple(attached))
    except Exception:
        pass

    return attached
class _ExtractWorker(QThread):
    log = pyqtSignal(str)
    done = pyqtSignal(tuple)   # (module_paths: list[str], imports: list[str])

    def __init__(self, params):
        super().__init__()
        self.params = params

    def run(self):
        try:
            py_files = collect_filepaths(**self.params)  # from your lib
            module_paths, imports = get_py_script_paths(py_files)  # your function
            self.done.emit((module_paths, imports))
        except Exception:
            self.log.emit(traceback.format_exc())
            self.done.emit(([], []))
