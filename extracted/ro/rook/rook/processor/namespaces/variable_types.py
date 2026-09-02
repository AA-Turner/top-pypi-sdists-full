import collections

LIST_TYPE = [list, tuple, set, frozenset]
DICT_TYPE = [dict, ]
try:
    import numpy
    LIST_TYPE.append(numpy.ndarray)
except ImportError:
    numpy = None

LIST_NAMES = ('deque', 'UserList')

DICT_NAMES = ('ChainMap', 'Counter', 'OrderedDict', 'defaultdict', 'UserDict')

for list_name in LIST_NAMES:
    try:
        LIST_TYPE.append(getattr(collections, list_name))
    except AttributeError:
        pass  # lgtm - ignore missing type

for dict_name in DICT_NAMES:
    try:
        DICT_TYPE.append(getattr(collections, dict_name))
    except AttributeError:
        pass  # lgtm - ignore missing type

LIST_TYPE = tuple(LIST_TYPE)
DICT_TYPE = tuple(DICT_TYPE)
