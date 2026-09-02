from .init_imports import *
from .constants import *

def is_line_import(line):
    if line and (line.startswith(FROM_TAG) or line.startswith(IMPORT_TAG)):
        return True
    return False
def is_line_group_import(line):
    if line and (line.startswith(FROM_TAG) and IMPORT_TAG in line):
        return True
    return False

def is_from_line_group(line):
    if line and line.startswith(FROM_TAG) and IMPORT_TAG in line and '(' in line:
        import_spl = line.split(IMPORT_TAG)[-1]
        import_spl_clean = clean_line(line)
        if not import_spl_clean.endswith(')'):
            return True
    return False
def get_unique_name(string,list_obj):
    if isinstance(list_obj,dict):
        list_obj = list(list_obj.keys())
    if string in list_obj:
        nustring = f"{string}"
        for i in range(len(list_obj)):
            nustring = f"{string}_{i}"
            if nustring not in list_obj:
                break
        string = nustring
    return string
