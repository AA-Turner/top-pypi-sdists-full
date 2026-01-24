import os
def get_abs_dir():
    abs_path = get_initial_caller_dir()
    return os.path.dirname(abs_path)
def join_abs_path(path):
    abs_dir = get_abs_dir()
    return os.path.join(abs_dir,path)
def get_rel_dir():
    return os.getcwd()
def join_rel_path(path):
    rel_dir = get_rel_dir()
    return os.path.join(rel_dir,path) 
def make_directory(directory=None,path=None):
    if directory==None:
        directory=os.getcwd()
    if path:
        directory = os.path.join(base_dir,path)
    os.makedirs(directory,exist_ok=True)
    return directory
def get_paths(*paths):
    all_paths = []
    for path in paths:
        all_paths+=path.split('/')
    return all_paths
def makeAllDirs(*paths):
    full_path= ''
    paths = get_paths(*paths)
    for i,path in enumerate(paths):
        if i == 0:
            full_path = path
            if not full_path.startswith('/'):
                full_path = join_rel_path(full_path)
        else:
            full_path = os.path.join(full_path,path)
        os.makedirs(full_path,exist_ok=True)
    return full_path
def currate_full_path(full_path):
    dirname = os.path.dirname(full_path)
    basename = os.path.basename(full_path)
    full_dirname = makeAllDirs(dirname)
    full_path = os.path.join(full_dirname,basename)
    return full_path
