from ..imports import MIME_TYPES,make_list,os
from .file_filters import get_globs
def get_file_type(file_path,types=None,default=None):
    mime_types = {}
    if types:
        types = make_list(types)
        for typ in types:
            mime_types[typ] = MIME_TYPES.get(typ)
    else:
        mime_types = MIME_TYPES
    
    if os.path.isfile(file_path):
        basename = os.path.basename(file_path)
        filename,ext = os.path.splitext(basename)
        for file_type,ext_values in mime_types.items():
            if ext in ext_values:
                return file_type
def get_file_map(directory,types=None,default=None):
    if directory and os.path.isfile(directory):
       directory = os.path.dirname(directory)
    all_types = {}
    files = get_globs(directory)
    for file in files:
        file_type = get_file_type(file,types=types,default=default)
        if file_type:
            if file_type not in all_types:
                all_types[file_type] = []
            all_types[file_type].append(file)
    return all_types
