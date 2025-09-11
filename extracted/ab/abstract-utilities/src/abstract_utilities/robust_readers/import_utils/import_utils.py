from pathlib import Path
from typing import *
from types import MethodType
import os,re, sys, importlib, inspect, os, importlib.util, hashlib
from .dot_utils import *
from .function_utils import *
from .sysroot_utils import *
from .utils import *

def safe_import(name: str, package: str | None = None, member: str | None = None):
    """
    Wraps importlib.import_module but also resolves relative imports like '..logPaneTab'.
    If `member` is given, returns that attribute from the module.
    """
    mod = importlib.import_module(name, package=package)
    return getattr(mod, member) if member else mod
def unique_module_name(base: str, path: Path) -> str:
    # Make a stable, unique name per file
    digest = hashlib.md5(str(path.resolve()).encode()).hexdigest()[:8]
    stem = path.stem.replace('-', '_')
    return f"_dyn.{base}.{stem}_{digest}"

def import_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {file_path}")
    mod = importlib.util.module_from_spec(spec)
    # Register before exec to satisfy intra-module relative imports (rare but safe)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod 
def get_imports(files: List[str],self=None) -> Dict[str, Dict[str, Any]]:
    """
    Discover package context from each file's relative-import requirements,
    add the proper sysroot to sys.path once, and import by dotted name.
    Returns: {modname: {"filepath", "sysroot", "module", "class", "funcs", "selfs"}}
    """
    results: Dict[str, Dict[str, Any]] = {}
    seen_sysroots: set[str] = set()
    files = make_list(files)
    for file in files:
        file_p = Path(file).resolve()

        # 1) Use your logic to find a viable sysroot (top where dots won't exceed)
        sysroot_guess = Path(get_dot_range_sysroot(str(file_p))).resolve()
        # 2) Ensure we import with *package* context: we need the directory ABOVE
        #    the topmost package on sys.path, not the package dir itself.
        top_pkg_dir = find_top_package_dir(sysroot_guess) or find_top_package_dir(file_p)
        if not top_pkg_dir:
            raise RuntimeError(f"No package context found for {file_p}; add __init__.py up the tree.")
        sysroot = top_pkg_dir.parent

        if str(sysroot) not in seen_sysroots:
            ensure_on_path(sysroot)
            seen_sysroots.add(str(sysroot))

        # 3) Compute dotted name from sysroot and import
        dotted = dotted_from(file_p, sysroot)
        try:
            mod = importlib.import_module(dotted)
        except Exception as e:
            # Helpful hint if user ran file directly (no package context)
            if "__package__" in dir() and not __package__:
                raise RuntimeError(
                    f"Import failed for {dotted}. If you ran this file directly, "
                    f"bootstrap package context or run via `python -m ...`."
                ) from e
            raise

        # 4) Collect symbols (you can keep your regex readers if you prefer)
        classes = extract_class(str(file_p))
        funcs   = extract_funcs(str(file_p))
        selfs   = extract_selfs(str(file_p))
        
        # stable result key (avoid collisions)
        key = get_unique_name(get_file_data(str(file_p), 'filename'), results)

        results[key] = {
            "filepath": str(file_p),
            "sysroot": str(sysroot),
            "module": mod,
            "class": classes,
            "funcs": funcs,
            "selfs": selfs,
        }

    return results
def inject_symbols_from_module(
    mod,
    into: dict,
    *,
    expose_functions: bool = True,
    expose_classes: bool = True,
    expose_methods: bool = False,
    self: object | None = None,   # <---- NEW
    ctor_overrides: Mapping[str, Tuple[tuple, dict]] | None = None,
    name_prefix: str = "",
    name_filter: Iterable[str] | None = None,
    overwrite: bool = False
) -> Dict[str, Any]:
    """
    Inject functions/classes from `mod` into `into` (usually globals()).
    If expose_methods=True and a `self` object is passed, bind instance methods
    directly onto `self` instead of globals().
    """
    exported: Dict[str, Any] = {}
    ctor_overrides = ctor_overrides or {}

    def allowed(name: str) -> bool:
        return name_filter is None or name in name_filter

    # 1) functions
    if expose_functions:
        for name, obj in vars(mod).items():
            input(name)
            if not allowed(name):
                continue
            if inspect.isfunction(obj) and obj.__module__ == mod.__name__:
                out_name = f"{name_prefix}{name}"
                if overwrite or out_name not in into:
                    into[out_name] = obj
                    exported[out_name] = obj

    # 2) classes (+ optional bound methods)
    if expose_classes or expose_methods:
        for cls_name, cls in vars(mod).items():
            if not allowed(cls_name):
                continue
            if inspect.isclass(cls) and cls.__module__ == mod.__name__:
                if expose_classes:
                    out_name = f"{name_prefix}{cls_name}"
                    if overwrite or out_name not in into:
                        into[out_name] = cls
                        exported[out_name] = cls

                if expose_methods and self is not None:
                    # instantiate class
                    args, kwargs = ctor_overrides.get(cls_name, ((), {}))
                    try:
                        inst = cls(*args, **kwargs)
                    except Exception:
                        continue

                    for meth_name, meth_obj in vars(cls).items():
                        if meth_name.startswith("__"):
                            continue
                        if inspect.isfunction(meth_obj) or inspect.ismethoddescriptor(meth_obj):
                            try:
                                bound = getattr(inst, meth_name)
                            except Exception:
                                continue
                            if callable(bound):
                                # attach directly to the `self` you passed in
                                if not hasattr(self, meth_name) or overwrite:
                                    setattr(self, meth_name, bound)
                                    exported[f"{cls_name}.{meth_name}"] = bound

    return exported
def inject_from_imports_map(
    imports_map: Dict[str, Dict[str, Any]],
    *,
    into: Optional[dict] = None,      # where to put free funcs/classes (defaults to this module's globals)
    attach_self: Optional[object] = None,  # bind names listed in "selfs" onto this object
    prefix_modules: bool = False,     # add "<module>__" prefix to avoid collisions
    overwrite: bool = False,           # allow overwriting existing names
    self:any=None
) -> Dict[str, Any]:
    """
    Emulates: from functions import *   (plus: bind 'self' methods)
    Returns dict of injected_name -> object (including methods bound to attach_self).
    """
    ns = into if into is not None else globals()
    exported: Dict[str, Any] = {}

    for mod_key, info in imports_map.items():
        mod = info.get("module")
        if mod is None:
            continue

        func_names: List[str]  = info.get("funcs", [])
        self_names: List[str]  = info.get("selfs", [])
        class_names: List[str] = info.get("class", [])

        # 1) bind the "selfs" directly onto self
        if self is not None:
            for name in self_names:
                func = getattr(mod, name, None)
                if not callable(func):
                    continue
                # sanity: ensure first param is literally named 'self'
                try:
                    params = list(inspect.signature(func).parameters.values())
                    if not params or params[0].name != "self":
                        continue
                except Exception:
                    continue

                bound = MethodType(func, self)
                if overwrite or not hasattr(self, name):
                    setattr(self, name, bound)
                    exported[f"{mod_key}.self.{name}"] = bound

        # 2) Inject free functions (exclude the ones we just bound to self to avoid dupes)
        for name in func_names:
            if name in self_names:
                continue
            obj = getattr(mod, name, None)
            if inspect.isfunction(obj) and obj.__module__ == mod.__name__:
                out_name = f"{mod_key}__{name}" if prefix_modules else name
                if overwrite or out_name not in ns:
                    ns[out_name] = obj
                    exported[out_name] = obj

        # 3) Inject classes
        for name in class_names:
            cls = getattr(mod, name, None)
            if inspect.isclass(cls) and cls.__module__ == mod.__name__:
                out_name = f"{mod_key}__{name}" if prefix_modules else name
                if overwrite or out_name not in ns:
                    ns[out_name] = cls
                    exported[out_name] = cls

    # optional: control wildcard export from THIS module
    ns["__all__"] = sorted(set(list(ns.get("__all__", [])) + list(exported.keys())))
    return exported
def ifFunctionsInFiles(root: str | None = None, *, expose_methods: bool = True, self=None) -> Dict[str, Any]:
    here = Path(__file__).resolve().parent
    base = Path(root).resolve() if root else here
    candidates = [base / "functions", base / "functions.py"]
    files: List[str] = []
    for item in candidates:
        if item.exists():
            if item.is_dir():
                files = [str(p) for p in item.rglob("*.py") if p.name != "__init__.py"]
            else:
                files = [str(item)]
            break

    exported_all: Dict[str, Any] = {}
    imports_map = get_imports(files)
    
    exported = inject_from_imports_map(
            imports_map,
            self=self
        )
        
    return exported
def attach_self_functions(
    imports_map: Dict[str, Dict[str, Any]],
    self_obj: object,
    *,
    overwrite: bool = False,
    only: Optional[List[str]] = None,     # whitelist of method names to attach
    prefix_modules: bool = False          # attach as core_utils__on_run_code instead of on_run_code
) -> Dict[str, Any]:
    """
    For each module in imports_map, bind names listed in 'selfs' (top-level defs whose
    first param is 'self') directly onto `self_obj`.

    Returns {attached_name: bound_method}.
    """
    attached: Dict[str, Any] = {}

    for mod_key, info in imports_map.items():
        mod = info.get("module")
        if not mod:
            continue

        self_names: List[str] = info.get("selfs", [])
        for name in self_names:
            if only is not None and name not in only:
                continue

            func = getattr(mod, name, None)
            if not callable(func):
                continue

            # sanity check: first param literally named 'self'
            try:
                params = list(inspect.signature(func).parameters.values())
                if not params or params[0].name != "self":
                    continue
            except Exception:
                continue

            bound = MethodType(func, self_obj)
            out_name = f"{mod_key}__{name}" if prefix_modules else name

            if overwrite or not hasattr(self_obj, out_name):
                setattr(self_obj, out_name, bound)
                attached[out_name] = bound

    return attached
