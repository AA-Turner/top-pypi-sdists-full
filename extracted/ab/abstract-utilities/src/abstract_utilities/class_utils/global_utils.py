import importlib, sys,os
from .caller_utils import get_initial_caller
def file_to_module_name(path):
    path = os.path.realpath(path)
    # Find a path that exists in sys.path
    for base in sys.path:
        base = os.path.realpath(base)
        if path.startswith(base):
            rel = os.path.relpath(path, base)
            mod = os.path.splitext(rel)[0]
            return mod.replace(os.sep, ".")
    # fallback (never should be used)
    return os.path.splitext(os.path.basename(path))[0]
def get_globals_from_path(module_path: str=None):
    module_path = module_path or get_initial_caller()
    module_name = file_to_module_name(module_path)
    if module_name not in sys.modules:
        importlib.import_module(module_name)
    return sys.modules[module_name].__dict__
def global_registry(name:str,glob:dict):
    global_ledger = if_none_default(string='global_ledger',glob=globals(),default={"registry_names":[],"registry_index":[]})
    if name not in global_ledger['registry_names']:
        if glob == None:
            return None
        global_ledger['registry_names'].append(name)
        global_ledger['registry_index'].append(glob)
    length = len(global_ledger['registry_names']) 
    change_glob('global_ledger',global_ledger)
    for i in range(0,length):
        if name == global_ledger['registry_names'][i]:
            return i
def get_registry_number(name:str):
    return global_registry(name=name,glob=None)
def update_registry(var:str,val:any,name:str):
    global_ledger=get_globes(string='global_ledger',glob=globals())
    change_glob(var=var,val=val,glob=get_global_from_registry(name))
    global_ledger['registry_index'][get_registry_number(name)] = get_global_from_registry(name)
    change_glob(var='global_ledger',val=global_ledger)
def get_global_from_registry(name:str):
    global_ledger=get_globes(string='global_ledger',glob=globals())
    return global_ledger['registry_index'][get_registry_number(name)]
def return_globals() -> dict:
    """
    Returns the global variables.

    Args:
        globs (dict, optional): The dictionary of global variables. Defaults to the current globals.

    Returns:
        dict: The global variables dictionary.
    """
    return globals()
def get_true_globals():
    return sys.modules['__main__'].__dict__
def change_glob(var: str, val: any, glob: dict = None) -> any:
    if glob is None:
        glob = get_true_globals()
    glob[var] = val
    return val

def get_globes(string: str='', glob: dict=None):
    if glob is None:
        glob = get_true_globals()
    return glob.get(string)
def if_none_default(string: str, default: any, glob: dict=None, typ=None):
    if glob is None:
        glob = get_true_globals()
    piece = get_globes(string=string, glob=glob)
    if piece is None or (typ and not isinstance(piece, typ)):
        piece = default
    return change_glob(var=string, val=piece, glob=glob)
