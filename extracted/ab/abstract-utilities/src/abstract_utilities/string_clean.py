"""
string_clean.py

This module provides functions for cleaning and manipulating strings.

Usage:
    import abstract_utilities.string_clean as string_clean

Functions:
- quoteIt(st: str, ls: list) -> str: Quotes specific elements in a string.
- eatInner(x: str or list, ls: list) -> any: Removes characters from the inner part of a string or list.
- eatOuter(x: str or list, ls: list) -> any: Removes characters from the outer part of a string or list.
- eatAll(x: str or list, ls: list) -> any: Removes characters from both the inner and outer parts of a string or list.
- safe_split(obj, ls): Safely splits a string using multiple delimiters.
- clean_spaces(obj: str) -> str: Removes leading spaces and tabs from a string.
- truncate_text(text, max_chars): Truncates a text to a specified maximum number of characters, preserving the last complete sentence or word.

This module is part of the `abstract_utilities` package.

Author: putkoff
Date: 05/31/2023
Version: 0.1.2
"""
import os
def quoteIt(st: str, ls: list) -> str:
    """
    Quotes specific elements in a string.

    Args:
        st (str): The input string.
        ls (list): The list of elements to quote.

    Returns:
        str: The modified string with quoted elements.
    """
    lsQ = ["'", '"']
    for i in range(len(ls)):
        for k in range(2):
            if lsQ[k] + ls[i] in st:
                st = st.replace(lsQ[k] + ls[i], ls[i])
            if ls[i] + lsQ[k] in st:
                st = st.replace(ls[i] + lsQ[k], ls[i])
        st = st.replace(ls[i], '"' + str(ls[i]) + '"')
    return st


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
def safe_split(obj, ls):
    """
    Safely splits a string using multiple delimiters.

    Args:
        obj: The input string.
        ls: The list of delimiters.

    Returns:
        any: The split string or original object if splitting is not possible.
    """
    for k in range(len(ls)):
        if type(ls[k]) is list:
            if ls[k][0] in obj or ls[k][1] == 0:
                obj = obj.split(ls[k][0])[ls[k][1]]
        else:
            obj = obj.split(ls[0])[ls[1]]
            return obj
    return obj


def clean_spaces(obj: str) -> str:
    """
    Removes leading spaces and tabs from a string.

    Args:
        obj (str): The input string.

    Returns:
        str: The string with leading spaces and tabs removed.
    """
    if len(obj) == 0:
        return obj
    while obj[0] in [' ', '\t']:
        obj = obj[1:]
    return obj
def truncate_text(text, max_chars):
    """
    Truncates a text to a specified maximum number of characters, preserving the last complete sentence or word.

    Args:
        text (str): The input text.
        max_chars (int): The maximum number of characters.

    Returns:
        str: The truncated text.
    """
    if len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    # Find the last complete sentence
    last_sentence_end = max(truncated.rfind('.'), truncated.rfind('!'), truncated.rfind('?'))
    # If a complete sentence is found, truncate up to its end
    if last_sentence_end != -1:
        truncated = truncated[:last_sentence_end + 1]
    else:
        # If no complete sentence is found, find the last complete word
        last_word_end = truncated.rfind(' ')

        # If a complete word is found, truncate up to its end
        if last_word_end != -1:
            truncated = truncated[:last_word_end]
    return truncated

def url_join(*paths):
    final_url = os.path.join(*paths)
    for i,path in enumerate(paths):
        if i == 0:
            final_path = path  # Note: Fixed bug; original code had `final_path = paths`
        else:
            final_path = eatOuter(final_path, '/')
            path = eatInner(path, '/')
            final_path = f"{final_path}/{path}"
    return final_path
       
    
def capitalize(string):
    return string[:1].upper() + string[1:].lower() if string else string
