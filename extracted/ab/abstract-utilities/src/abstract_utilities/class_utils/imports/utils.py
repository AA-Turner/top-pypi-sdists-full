from .imports import *
def remove_key(js: dict, key: any) -> dict:
    """Remove a key from a dictionary. If the key is not present,
    no action is taken."""
    js.pop(key, None)
    return js
def if_none_change(obj, default):
    """Return a default value if the provided object is None."""
    if obj == None:
        obj = default
    return obj
def has_attribute(module, function):
    """Check if a specific function exists in a given module."""
    try:
        bool_it = hasattr(module, function)
    except:
        bool_it =None
    return bool_it
def get_type_list() -> list:
    """Get a list of common Python types."""
    return ['None','str','int','float','bool','list','tuple','set','dict','frozenset','bytearray','bytes','memoryview','range','enumerate','zip','filter','map','property','slice','super','type','Exception','object']
def get_set_attr(parent,attr_name,value=None,valueFunc=None,default=False,*args,**kwargs):
    attr_value = getattr(parent,attr_name,default)
    if attr_value == False:
        if value is None and valueFunc is not None:
            value = valueFunc(*args,**kwargs)
        setattr(parent,attr_name,value)
        attr_value = getattr(parent,attr_name,default)
    return attr_value
def get_dir(mod):
    """
    Retrieves the directory of a module.

    Args:
        mod: The module.

    Returns:
        list: The list of attributes and methods in the module.
    """
    return dir(mod)
