# --- auto-package bootstrap (run-safe) ---------------------------------
from ..imports import *
from .dot_utils import get_dot_range
from .sysroot_utils import get_sysroot,get_import_with_sysroot,get_py_files,get_all_py_sysroots
from .extract_utils import get_all_py_file_paths
def clean_imports(imports,commaClean=True):
    chars=["*"]
    if not commaClean:
        chars.append(',')
    if isinstance(imports,str):
        imports = imports.split(',')
    return [eatElse(imp,chars=chars) for imp in imports if imp]
def get_dot_range(import_pkg):
    count = 0
    for char in import_pkg:
        if char != '.':
            break
        count+=1
    return count
def get_cleaned_import_list(line,commaClean=True):
    cleaned_import_list=[]
    if IMPORT_TAG in line:
        imports = line.split(IMPORT_TAG)[1]
        cleaned_import_list+=clean_imports(imports,commaClean=commaClean)
    return cleaned_import_list
def get_module_from_import(imp,path=None):
    path = path or os.getcwd()
    i = get_dot_range(imp)
    imp = eatAll(imp,'.')
    sysroot = get_sysroot(path,i)
    return os.path.join(sysroot, imp)

def safe_import(name: str, *, package: str | None = None, member: str | None = None, file: str | None = None):
    """
    Wrapper over importlib.import_module that:
    - if `name` is relative (starts with '.'), ensures `package` is set.
    - if `package` is missing, derives it from `file` (defaults to __file__).
    """
    file = file or __file__
    ensure_package_context(file)
    if name.startswith(".") and not package:
        
            
        pkg_name = get_module_from_import(name,path=None)
        # also set __package__ if we are running as a script
        if __name__ == "__main__" and (not globals().get("__package__")):
            globals()["__package__"] = pkg_name
        package = pkg_name

    mod = importlib.import_module(name, package=package)
    return getattr(mod, member) if member else mod

def dynamic_import(module_path: str, namespace: dict, all_imports = None):
    """
    Emulates:
        from module_path import *
    but includes private (_xxx) names too.
    """
    all_imports = if_none_change(all_imports,True)
    if module_path:
        module = importlib.import_module(module_path)
        # Import literally everything except dunders, unless you want them too.
        names = [n for n in dir(module) if n and ((not all_imports and not n.startswith("_")) or all_imports)]
        for name in names:
            namespace[name] = getattr(module, name)
        return module
def get_monorepo_root(directory=None,files=None):
    directory = directory or get_initial_caller_dir()
    
    py_files = get_all_py_file_paths(directory,add=True)
    sysroots = get_all_py_sysroots(directory=directory,files=py_files)
    monorepo_root = get_common_root(sysroots)
    return monorepo_root
def switch_to_monorepo_root(directory=None,files=None):
    monorepo_root = get_monorepo_root(directory=directory,files=files)
    if str(monorepo_root) not in sys.path:
        sys.path.insert(0, str(monorepo_root))
    return str(monorepo_root)
def get_all_imports(directory=None,sysroot=None,globs=None):
    globs = globs or get_true_globals() or globals()
    directory = directory or get_initial_caller_dir()
    files = collect_globs(directory=directory,allowed_exts='.py').get('files')
    sysroot = sysroot or switch_to_monorepo_root(directory=directory,files=files)
    for glo in files:
        imp = get_import_with_sysroot(glo, sysroot)
        dynamic_import(imp, globs)
def get_all_imports_for_class(self, directory=None, sysroot=None, include_private=True):
    """
    Load all modules under `directory` and assign their exports as attributes
    on the class instance (self).
    """
    directory = directory or get_initial_caller_dir()
    files = collect_globs(directory=directory, allowed_exts='.py').get("files")

    # Compute sysroot (monorepo root)
    sysroot = sysroot or switch_to_monorepo_root(directory=directory, files=files)

    for glo in files:
        mod_path = get_import_with_sysroot(glo, sysroot)
        module = importlib.import_module(mod_path)

        for name in dir(module):
            if name.startswith("__"):
                continue
            if not include_private and name.startswith("_"):
                continue

            setattr(self, name, getattr(module, name))

    return self
