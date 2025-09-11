import os
def get_file_data(filepath,key=None):
    dirname,basename = os.path.split(filepath)
    filename,ext = os.path.splitext(basename)
    file_data = {
        "dirname":dirname,
        "basename":basename,
        "filename":filename,
        "ext":ext
        }
    if key and key in file_data:
        file_data = file_data.get(key)
    return file_data

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
