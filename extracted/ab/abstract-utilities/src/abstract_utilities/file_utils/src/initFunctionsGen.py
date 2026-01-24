# attach_functions.py  — single helper you can import anywhere
# attach_dynamic.py
from __future__ import annotations
from .find_collect import get_files_and_dirs
from ..imports import *
ABSPATH = os.path.abspath(__file__)
ABSROOT = os.path.dirname(ABSPATH)

def caller_path():
    frame = inspect.stack()[1]
    return os.path.abspath(frame.filename)
def _is_defined_here(mod: types.ModuleType, obj: object) -> bool:
    try:
        return inspect.getmodule(obj) is mod
    except Exception:
        return False

def _collect_callables(mod: types.ModuleType) -> Dict[str, Callable]:
    out: Dict[str, Callable] = {}
    names = getattr(mod, "__all__", None)
    if names:
        # trust the author's export list
        for n in names:
            fn = getattr(mod, n, None)
            if callable(fn):
                out[n] = fn
        return out
    # otherwise, discover top-level callables defined in this module
    for n in dir(mod):
        if n.startswith("_"):
            continue
        obj = getattr(mod, n, None)
        if callable(obj) and _is_defined_here(mod, obj):
            out[n] = obj
    return out

def _import_module_by_name(name: str) -> Optional[types.ModuleType]:
    try:
        return importlib.import_module(name)
    except Exception:
        return None

def _import_module_by_path(pkg_name: str, base_dir: str, filename: str) -> Optional[types.ModuleType]:
    mod_name = f"{pkg_name}.functions"
    path = os.path.join(base_dir, filename)
    spec = importlib.util.spec_from_file_location(mod_name, path)
    if not spec or not spec.loader:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod

def _walk_functions_package(pkg_name: str, pkg_mod: types.ModuleType) -> List[types.ModuleType]:
    """Import all immediate submodules in the functions/ package."""
    mods: List[types.ModuleType] = [pkg_mod]
    pkg_dir = os.path.dirname(pkg_mod.__file__ or "")
    for info in pkgutil.iter_modules([pkg_dir]):
        # only import direct children (no recursion here; easy to add if you need)
        child_name = f"{pkg_mod.__name__}.{info.name}"
        m = _import_module_by_name(child_name)
        if m:
            mods.append(m)
    return mods

def _discover_functions(base_pkg: str, *, hot_reload: bool) -> List[Tuple[str, Callable, str]]:
    """
    Returns a list of (export_name, callable, module_basename).
    Works if you have base_pkg.functions.py or base_pkg/functions/ package.
    """
    # Prefer normal import of '<base_pkg>.functions'
    fqn = f"{base_pkg}.functions"
    mod = _import_module_by_name(fqn)

    if mod is None:
        # fallback: sibling functions.py, even without being a package
        base = _import_module_by_name(base_pkg)
        if not base or not getattr(base, "__file__", None):
            return []
        base_dir = os.path.dirname(base.__file__)
        if os.path.isfile(os.path.join(base_dir, "functions.py")):
            mod = _import_module_by_path(base_pkg, base_dir, "functions.py")
        else:
            return []

    if hot_reload:
        try:
            mod = importlib.reload(mod)  # type: ignore[arg-type]
        except Exception:
            pass

    results: List[Tuple[str, Callable, str]] = []
    modules: List[types.ModuleType]

    if hasattr(mod, "__path__"):  # it's a package: import children
        modules = _walk_functions_package(base_pkg, mod)
    else:
        modules = [mod]

    for m in modules:
        exported = _collect_callables(m)
        module_basename = m.__name__.split(".")[-1]
        for name, fn in exported.items():
            results.append((name, fn, module_basename))
    return results

def attach_functions(
    obj_or_cls,
    base_pkg: str | None = None,
    hot_reload: bool = True,
    prefix_with_module: bool = False,
    include_private: bool = True,
    only_defined_here: bool = True,   # don't attach stuff imported from elsewhere
) -> list[str]:
    """
    Attach all free functions found in <base_pkg>.functions (module or package)
    to the *class* of obj_or_cls. Returns the list of attached attribute names.
    """
    cls = obj_or_cls if inspect.isclass(obj_or_cls) else obj_or_cls.__class__
    # Derive "<package>.functions" from the class's module unless you pass base_pkg
    caller_mod = cls.__module__
    pkg_root = (base_pkg or caller_mod.rsplit(".", 1)[0]).rstrip(".")
    funcs_pkg_name = f"{pkg_root}.functions"

    def _import(name: str) -> ModuleType | None:
        try:
            if hot_reload and name in sys.modules:
                return importlib.reload(sys.modules[name])
            return importlib.import_module(name)
        except Exception:
            return None

    def _is_pkg(m: ModuleType) -> bool:
        return hasattr(m, "__path__")

    mod = _import(funcs_pkg_name)
    if mod is None:
        # Nothing to attach (no functions.py or functions/ next to your class)
        setattr(cls, "_attached_functions", tuple())
        return []

    modules: list[ModuleType] = [mod]
    if _is_pkg(mod):
        # attach from every submodule under functions/
        for it in pkgutil.iter_modules(mod.__path__):
            sub = _import(f"{funcs_pkg_name}.{it.name}")
            if sub is not None:
                modules.append(sub)

    attached: list[str] = []
    for m in modules:
        for name, obj in vars(m).items():
            # only callables (skip classes), and keep them sane
            if not callable(obj) or isinstance(obj, type):
                continue
            if only_defined_here and getattr(obj, "__module__", None) != m.__name__:
                continue
            if not include_private and name.startswith("_"):
                continue
            if name.startswith("__") and name.endswith("__"):
                continue
            attr = f"{m.__name__.rsplit('.', 1)[-1]}__{name}" if prefix_with_module else name
            try:
                setattr(cls, attr, obj)  # set on CLASS → becomes bound method on instances
                attached.append(attr)
            except Exception:
                # don't explode if one name collides; keep going
                continue

    # handy for debugging
    try:
        setattr(cls, "_attached_functions", tuple(attached))
    except Exception:
        pass
    return attached




def isTab(item):
    item_lower =  item.lower()
    for key in ['console','tab']:
        if item_lower.endswith(key):
            return True
    return False
def get_dir(root,item):
    if None in [root]:
        return None
    path = root
    if item != None:
        path = os.path.join(path,item)
    return path
def isDir(root,item=None):
    path = get_dir(root,item)
    if path:
        return os.path.isdir(path)
def check_dir_item(root,item=None):
    return (item and isTab(item) and isDir(root,item))
def get_dirs(root = None):
    root = root or ABSROOT
    dirpaths = [get_dir(root,item) for item in os.listdir(root) if check_dir_item(root,item)]
    return dirpaths
def ifFunctionsInFile(root):
    items = [os.path.join(root, "functions"),os.path.join(root, "functions.py")]
    for item in items:
        if os.path.exists(item):
            return item
        

def get_for_all_tabs(root = None):
    root = root or caller_path()
    if os.path.isfile(root):
        root = os.path.dirname(root)
    all_tabs = get_files_and_dirs(root,allowed_patterns='*Tab')[0]
    
    for ROOT in all_tabs:
        if os.path.isdir(ROOT):
            [apply_inits(os.path.join(ROOT,func)) for func in os.listdir(ROOT) if 'functions'  == os.path.splitext(func)[0]]
        
      
            

def apply_inits(ROOT):
        filepaths=[ROOT]
        TAB_DIR = os.path.dirname(ROOT)
        INIT_FUNCS_PAPTH = os.path.join(TAB_DIR, "initFuncs.py")
        if_fun_dir=False
##        if os.path.isfile(ROOT):
##            dirname= os.path.dirname(ROOT)
##            basename= os.path.basename(ROOT)
##            functions_dir = os.path.join(dirname,'functions')
##            functions_path = os.path.join(functions_dir,basename)
##            input(get_clean_imports(ROOT))
##            
##            os.makedirs(functions_dir,exist_ok=True)
##            shutil.move(ROOT,functions_path)
##            ROOT=functions_dir
        if os.path.isdir(ROOT):
            INIT_PATH = os.path.join(ROOT, "__init__.py")
            
            filepaths = get_files_and_dirs(directory=ROOT,allowed_exts='py',add=True)[-1]
            if_fun_dir=True
    
   
        
        # Parse top-level def names
        def extract_funcs(path: str):
            funcs = []
            for line in read_from_file(path).splitlines():
                m = re.match(r"^def\s+([A-Za-z_]\w*)\s*\(self", line)
                if m:
                    funcs.append(m.group(1))
            return funcs
        
        # Build functions/__init__.py that re-exports all discovered functions
        import_lines = []
        all_funcs = []
        for fp in filepaths:
            module = os.path.splitext(os.path.basename(fp))[0]
            funcs = extract_funcs(fp)
            if funcs:
                import_lines.append(f"from .{module} import ({', '.join(funcs)})")
                all_funcs.extend(funcs)
        if if_fun_dir:
            functions_init = "\n".join(import_lines) + ("\n" if import_lines else "")
            write_to_file(contents=functions_init, file_path=INIT_PATH)

        # Prepare the tuple literal of function names for import + loop
        uniq_funcs = sorted(set(all_funcs))
        func_tuple = ", ".join(uniq_funcs) + ("," if len(uniq_funcs) == 1 else "")
        
        # Generate apiConsole/initFuncs.py using the safer setattr-loop
        init_funcs_src = textwrap.dedent(f"""\
            
            
            from abstract_utilities import get_logFile
            from .functions import ({func_tuple})
            logger=get_logFile(__name__)
            def initFuncs(self):
                try:
                    for f in ({func_tuple}):
                        setattr(self, f.__name__, f)
                except Exception as e:
                    logger.info(f"{{e}}")
                return self
        """)

        write_to_file(contents=init_funcs_src, file_path=INIT_FUNCS_PAPTH)

def call_for_all_tabs():
    root = get_caller_dir(2)
    
    get_for_all_tabs(root)
