from .imports import *
def get_alpha():
    return 'abcdefghijklmnopqrstuvwxyz'
def get_alpha_list() -> list:
    """
    Generates a list of all lowercase alphabets.
    
    Returns:
        list: A list of all lowercase alphabets.
    """
    return list(get_alpha())
def is_alpha(char,case_sensative=False):
    alphas = get_alpha()
    if not case_sensative:
        alphas+=alphas.upper()
    return char in alphas
def find_it_alph(ls: list, y: any) -> int:
    """
    Finds the index of an element in a list.

    Args:
        ls (list): The list to search.
        y (any): The element to find.

    Returns:
        int: The index of the element in the list. If not found, returns -1.
    """
    i = 0
    while str(ls[i]) != str(y):
        i += 1
    return i
def get_keys(mapping,typ=None):
    typ = typ or set
    if isinstance(mapping,dict):
        mapping = mapping.keys()
    return typ(mapping)
def make_key_map(dict_obj):
    return {k:get_keys(v) for k,v in dict_obj.items()}

def getAlphas(lower=True,capitalize=False,listObj=False):
    obj = ''
    alphas = get_alpha()
    if lower:
        obj+=alphas
    if capitalize:
        obj+=alphas.upper()
    if listObj:
        obj = list(obj)
    return obj
