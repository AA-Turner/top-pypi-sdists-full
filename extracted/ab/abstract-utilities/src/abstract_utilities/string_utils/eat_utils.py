from .imports import *
def eatInner(string: str, list_objects:(str or list)) -> any:
    """
    Removes characters from the inner part of a string or list.

    Args:
        x (str or list): The input string or list.
        ls (list): The list of characters to remove.

    Returns:
        any: The modified string or list.
    """
    if not isinstance(list_objects,list):
        list_objects = [list_objects]
    if not isinstance(string,str):
        string = str(string)
    if string and list_objects:
        for char in string:
            if string:
                if char not in list_objects:
                    return string
                string = string[1:]
    return string


def eatOuter(string: str, list_objects:(str or list)) -> any:
    """
    Removes characters from the outer part of a string or list.

    Args:
        x (str or list): The input string or list.
        ls (list): The list of characters to remove.

    Returns:
        any: The modified string or list.
    """
    if not isinstance(list_objects,list):
        list_objects = [list_objects]
    if not isinstance(string,str):
        string = str(string)
    if string and list_objects:
        for i in range(len(string)):
            if string:
                if string[-1] not in list_objects:
                    return string
                string = string[:-1]
    return string
def eatAll(string: str, list_objects:(str or list)) -> any:
    """
    Removes characters from both the inner and outer parts of a string or list.

    Args:
        x (str or list): The input string or list.
        ls (list): The list of characters to remove.

    Returns:
        any: The modified string or list.
    """
    if not isinstance(list_objects,list):
        list_objects = [list_objects]
    if not isinstance(string,str):
        string = str(string)
    if string and list_objects:
        string = eatInner(string, list_objects)
    if string and list_objects:
        string = eatOuter(string, list_objects)
    return string



def eatElse(
    stringObj,
    chars=None,
    ints=True,
    alpha=True,
    lower=True,
    capitalize=True,
    string=True,
    listObj=True
):
    alpha_ints = get_alpha_ints(
        ints=True,
        alpha=True,
        lower=True,
        capitalize=True,
        string=True,
        listObj=True
        )
    chars = make_list(chars or [])+alpha_ints

    while True:
        if stringObj:
            str_0 = stringObj[0] not in chars
            str_1 = stringObj[-1] not in chars
            str_eat = str_0 or str_1
            if not str_eat:
                return stringObj
            if stringObj and str_0:
                stringObj = stringObj[1:] if len(stringObj) !=1 else ""
            if stringObj and str_1:
                stringObj = stringObj[:-1] if len(stringObj) !=1 else ""   
        else:
            return stringObj
