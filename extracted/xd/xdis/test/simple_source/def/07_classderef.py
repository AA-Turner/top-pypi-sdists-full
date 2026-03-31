# From 3.4 ctypes/__init__.py
# For opcode LOAD_CLASSDEREF

def CFUNCTYPE(argtypes) -> type[CFunctionType]:
    class CFunctionType(object):
        _argtypes_ = argtypes
    return CFunctionType
