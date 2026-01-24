def make_list(obj:any) -> list:
    """
    Converts the input object to a list. If the object is already a list, it is returned as is.
    
    Args:
        obj: The object to convert.
        
    Returns:
        list: The object as a list.
    """
    if isinstance(obj,str):
        if ',' in obj:
            obj = obj.split(',')
    if isinstance(obj,set) or isinstance(obj,tuple):
        return list(obj)
    if isinstance(obj, list):
        return obj
    return [obj]
def get_keys(mapping,typ=None):
    typ = typ or set
    if isinstance(mapping,dict):
        mapping = mapping.keys()
    return typ(mapping)
def make_key_map(dict_obj):
    return {k:get_keys(v) for k,v in dict_obj.items()}
