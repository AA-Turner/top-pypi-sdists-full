from abstract_utilities import *
import os, re, textwrap
ABSPATH = os.path.abspath(__file__)
ABSROOT = os.path.dirname(ABSPATH)
def clean_imports():
    alls = str(list(set("""os,re,subprocess,sys,re,traceback,pydot, enum, inspect, sys, traceback, threading,json,traceback,logging,requests""".replace('\n','').replace(' ','').replace('\t','').split(','))))[1:-1].replace('"','').replace("'",'')
    input(alls)
def isTab(item):
    item_lower =  item.lower()
    for key in ['console','tab']:
        if item_lower.endswith(key):
            return True
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
    return item and isTab(item) and isDir(root,item)
def get_dirs(root = None):
    root = root or ABSROOT
    dirpaths = [get_dir(root,item) for item in os.listdir(root) if check_dir_item(root,item)]
    return dirpaths
def ifFunctionsInFile(root):
    items = [os.path.join(root, "functions"),os.path.join(root, "functions.py")]
    for item in items:
        if os.path.exists(item):
            return item
        

def getInitForAllTabs(root = None):
    all_tabs = get_dirs(root = root)
    for ROOT in all_tabs:
        FUNCS_DIR = ifFunctionsInFile(ROOT)
        if FUNCS_DIR == None:
            for ROOT in get_dirs(root = ROOT):
                apply_inits(ROOT)
        else: 
            apply_inits(ROOT)
            

def apply_inits(ROOT):
    FUNCS_DIR = ifFunctionsInFile(ROOT)
    
    if_fun_dir = isDir(FUNCS_DIR)
    if if_fun_dir != None:

        if if_fun_dir:

        # Only .py files, skip __init__.py
            filepaths = [
                os.path.join(FUNCS_DIR, item)
                for item in os.listdir(FUNCS_DIR)
                if item.endswith(".py") and item != "__init__.py"
                   and os.path.isfile(os.path.join(FUNCS_DIR, item))
            ]
        else:
            filepaths = [FUNCS_DIR]
        
        # Parse top-level def names
        def extract_funcs(path: str):
            funcs = []
            for line in read_from_file(path).splitlines():
                m = re.match(r"^def\s+([A-Za-z_]\w*)\s*\(", line)
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
            write_to_file(contents=functions_init, file_path=os.path.join(FUNCS_DIR, "__init__.py"))

        # Prepare the tuple literal of function names for import + loop
        uniq_funcs = sorted(set(all_funcs))
        func_tuple = ", ".join(uniq_funcs) + ("," if len(uniq_funcs) == 1 else "")
        
        # Generate apiConsole/initFuncs.py using the safer setattr-loop
        init_funcs_src = textwrap.dedent(f"""\
            

            from .functions import ({func_tuple})

            def initFuncs(self):
                try:
                    for f in ({func_tuple}):
                        setattr(self, f.__name__, f)
                except Exception as e:
                    logger.info(f"{{e}}")
                return self
        """)

        write_to_file(contents=init_funcs_src, file_path=os.path.join(ROOT, "initFuncs.py"))

