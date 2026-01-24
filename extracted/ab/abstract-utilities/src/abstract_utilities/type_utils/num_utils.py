from .imports import *
def get_num_list() -> list:
    """
    Generates a list of numbers as strings.
    
    Returns:
        list: A list of numbers as strings.
    """
    return list('0123456789')

def getInts(string=False,listObj=False):
    obj=12345678909
    if string:
        obj = str(obj)
    if listObj:
        obj = list(obj)
    return obj


