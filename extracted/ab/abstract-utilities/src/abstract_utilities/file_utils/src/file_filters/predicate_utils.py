from .ensure_utils import *

def get_globs(items,recursive: bool = True,allowed=None,cfg=None,**kwargs):
    glob_paths = []
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    items = [item for item in make_list(items) if item]
    for item in items:
        pattern = os.path.join(item, "**/*")  # include all files recursively\n
        nuItems = glob.glob(pattern, recursive=recursive)
        if allowed:
            nuItems = [nuItem for nuItem in nuItems if nuItem and allowed(nuItem)]
        glob_paths += nuItems
    return glob_paths
def get_allowed_files(items,allowed=True,cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    return [item for item in items if item and os.path.isfile(item) and allowed(item)]
def get_allowed_dirs(items,allowed=False,cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    return [item for item in items if item and os.path.isdir(item) and allowed(item)]

def get_filtered_files(items,allowed=None,files = [],cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    glob_paths = get_globs(items,allowed=allowed,cfg=cfg,**kwargs)
    return [glob_path for glob_path in glob_paths if glob_path and os.path.isfile(glob_path) and glob_path not in files and allowed(glob_path)]
def get_filtered_dirs(items,allowed=None,dirs = [],cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    glob_paths = get_globs(items,allowed=allowed,cfg=cfg,**kwargs)
    return [glob_path for glob_path in glob_paths if glob_path and os.path.isdir(glob_path) and glob_path not in dirs and allowed(glob_path)]

def get_all_allowed_files(items,allowed=None,cfg=None,**kwargs):
    dirs = get_all_allowed_dirs(items,allowed=allowed,cfg=cfg,**kwargs)
    files = get_allowed_files(items,allowed=allowed,cfg=cfg,**kwargs)
    nu_files = []
    for directory in dirs:
        files += get_filtered_files(directory,allowed=allowed,files=files,cfg=cfg,**kwargs)
    return files
def get_all_allowed_dirs(items,allowed=None,cfg=None,**kwargs):
    allowed = get_allowed_predicate(allowed=allowed,cfg=cfg,**kwargs)
    dirs = get_allowed_dirs(items,allowed=allowed,cfg=cfg,**kwargs)
    nu_dirs=[]
    for directory in dirs:
        nu_dirs += get_filtered_dirs(directory,allowed=allowed,dirs=nu_dirs,cfg=cfg,**kwargs)
    return nu_dirs

