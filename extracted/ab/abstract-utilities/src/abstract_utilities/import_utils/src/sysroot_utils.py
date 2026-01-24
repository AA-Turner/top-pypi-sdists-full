from ..imports import *
from .dot_utils import *
from .extract_utils import get_all_py_file_paths
def get_py_files(directory=None):
    directory = directory or get_initial_caller_dir()
    return get_all_py_file_paths(directory,add=True)
def ensure_on_path(p: Path):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)
def get_sysroot(filepath,i):
    for j in range(i):
        filepath = os.path.dirname(filepath)
    return filepath

def get_dot_range_sysroot(filepath):
    sysroot = filepath
    while True:
        dot_range = get_dot_range(is_import_or_init(sysroot))
        if dot_range == 0:
            break
        sysroot = get_sysroot(sysroot,dot_range)
    
    return sysroot
def get_import_with_sysroot(file_path, sysroot):
    """
    Rewrite imports like:
        from imports.constants import *
    into:
        from <relative_path>.imports.constants import *
    Where <relative_path> is computed relative to sysroot.
    """


    # Absolute paths
    file_dir = os.path.dirname(os.path.abspath(file_path))
    sysroot = os.path.abspath(sysroot)

    # Compute relative path
    relpath = os.path.relpath(file_dir, sysroot)

    bare_rel = eatAll(relpath,'.')
    
    # Turn filesystem path into dotted python path
    if relpath == ".":
        dotted = ""
    else:
        dotted = ".".join(part for part in relpath.split(os.sep) if part)
    if bare_rel.startswith('/') and dotted.startswith('.'):
        dotted = dotted[1:]


    # Build final rewritten import
    return dotted
def get_all_sysroots(files):
    sysroots=[]
    for glo in files:
        imp = compute_dotted_and_sysroot(glo)
        sysroots.append(imp[-1])
    return sysroots
def get_shortest_sysroot(files):
    sysroots = get_all_sysroots(files)
    return get_shortest_path(*sysroots)
def get_all_py_sysroots(directory=None,files=None):
    py_files = files or get_py_files(directory=directory)
    return [compute_dotted_and_sysroot(glo)[1] for glo in py_files]

def get__imports(directory=None, sysroot=None):
    directory = directory or get_caller_dir(1)
    globs = collect_globs(directory, allowed_exts='.py')
    globs = [glo for glo in globs.get('files') if glo]
    sysroots = [compute_dotted_and_sysroot(glo)[1] for glo in globs]
    # ⭐ Get unified monorepo root
    monorepo_root = get_common_root(sysroots)
    if str(monorepo_root) not in sys.path:
        sys.path.insert(0, str(monorepo_root))
    get_all_imports(directory=directory, sysroot=monorepo_root)
def is_import_or_init(sysroot,likely=None):
    file_data = get_file_parts(sysroot)
    nuroot = sysroot
    dirname = file_data.get('dirname')
    if os.path.isdir(sysroot):
        dirname = sysroot
    ext = file_data.get('ext')
    filename = file_data.get('filename')
    
    candidates = []
    if likely:
        candidates += [os.path.join(dirname,f"{likely}.py"),os.path.join(dirname,likely)]
    candidates += [os.path.join(dirname,f"{filename}.py"),os.path.join(dirname,filename)]
    files: List[Path] = []
    for item in candidates:
        
        if os.path.exists(item):
            if os.path.isdir(item):
                
                nuroot=None
                init_name = '__init__.py'
                rootList = os.listdir(item)
                for basename in rootList:
                    if get_file_parts(basename,'filename') == filename:
                        nuroot = os.path.join(item,basename)
                        break
                if init_name in rootList:
                    nuroot = os.path.join(item,init_name)
                    break
                    
            else:
               nuroot=sysroot
               break

    return nuroot
