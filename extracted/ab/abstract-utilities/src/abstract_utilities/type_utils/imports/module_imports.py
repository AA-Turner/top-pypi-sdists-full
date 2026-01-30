
def get_keys(mapping,typ=None):
    typ = typ or set
    if isinstance(mapping,dict):
        mapping = mapping.keys()
    return typ(mapping)
def make_key_map(dict_obj):
    return {k:get_keys(v) for k,v in dict_obj.items()}
