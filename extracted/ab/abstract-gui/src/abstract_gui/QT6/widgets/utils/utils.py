def qt_full_type_name(obj):
    """Return the full module path + class name."""
    if obj is None:
        return "<None>"
    cls = type(obj)
    return f"{cls.__module__}.{cls.__name__}"
def is_widget(obj):
    isit = 'widget' in qt_full_type_name(obj).lower()
    if not isit and isinstance(obj,list) or isinstance(obj,tuple):
        for ob in obj:
            if 'widget' in qt_full_type_name(ob).lower():
                return True    
def value_is_widget(key,obj):
    return key == 'widget' and is_widget(obj)
def findTheWidget(*args,**kwargs):
    for arg in args:
        if is_widget(arg):
            return arg
    for key,value in kwargs.items():
        if is_widget(value):
            return value

