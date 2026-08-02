def get_field(obj, field_name):
    try:
        cls = obj.getClass()
        while cls is not None:
            try:
                field = cls.getDeclaredField(field_name)
                field.setAccessible(True)
                return field.get(obj)
            except Exception:
                cls = cls.getSuperclass()
    except Exception:
        return getattr(obj, field_name, None)
    return None

def set_field(obj, field_name, value):
    try:
        cls = obj.getClass()
        while cls is not None:
            try:
                field = cls.getDeclaredField(field_name)
                field.setAccessible(True)
                field.set(obj, value)
                return True
            except Exception:
                cls = cls.getSuperclass()
    except Exception:
        try:
            setattr(obj, field_name, value)
            return True
        except Exception:
            pass
    return False

def call_method(obj, method_name, *args):
    # Try looking up the Python attribute first
    attr = None
    try:
        attr = getattr(obj, method_name, None)
    except Exception:
        pass

    if attr is not None and callable(attr):
        # Call it directly without catching all exceptions so user errors are not hidden
        return attr(*args)

    try:
        cls = obj.getClass()
        while cls is not None:
            methods = cls.getDeclaredMethods()
            for m in methods:
                if m.getName() == method_name:
                    param_types = m.getParameterTypes()
                    if len(param_types) == len(args):
                        try:
                            m.setAccessible(True)
                            try:
                                return m.invoke(obj, *args)
                            except Exception:
                                return m.invoke(obj, args)
                        except Exception:
                            pass
            cls = cls.getSuperclass()
    except Exception:
        pass
    
    raise AttributeError(f"Method '{method_name}' not found on {obj} or could not be invoked.")
