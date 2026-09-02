from ..imports import *
def get_imp(line):
    lis = [li for li in line.split(' ') if li and li.startswith('.')]
    if lis and len(lis) >0:
        lis = lis[0]
        lis = len(lis) - len(eatInner(lis,['.']))
        return lis
    return 0
def extract_imports(path,strings=None):
    strings = make_list(strings or ['from','import'])
    funcs = []
    lines = read_from_file(path).splitlines()
    return [line for line in lines if [string for string in strings if string and eatAll(line,[' ','\n','\t']) and eatAll(line,[' ','\n','\t']).startswith(string)]]

def extract_froms(path: str):
    funcs = []
    for line in read_from_file(path).splitlines():
        m = re.match(r"^from\s+([A-Za-z_]\w*)\s*", line)
        if m:
            funcs.append(m.group(1))
    return funcs
def extract_selfs(path: str):
    funcs = []
    for line in read_from_file(path).splitlines():
        m = re.match(r"^def\s+([A-Za-z_]\w*)\s*\(self", line)
        if m:
            funcs.append(m.group(1))
    return funcs
def extract_funcs(path: str):
    funcs = []
    for line in read_from_file(path).splitlines():
        m = re.match(r"^def\s+([A-Za-z_]\w*)\s*\(", line)
        if m:
            funcs.append(m.group(1))
    return funcs
def extract_class(path: str):
    funcs = []
    for line in read_from_file(path).splitlines():
        m = re.match(r"^class\s+([A-Za-z_]\w*)\s*\(", line) or re.match(r"^class\s+([A-Za-z_]\w*)\s*\:", line)
        if m:
            funcs.append(m.group(1))
    return funcs
def get_all_py_file_paths(directory,*args,**kwargs):
    globs = collect_globs(directory,*args,allowed_exts='.py',**kwargs)
    globs = [glo for glo in globs.get('files') if glo]
    return globs
