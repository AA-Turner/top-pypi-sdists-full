from .imports import *
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

def is_in_list(obj: any, ls: list = []):
    """
    Checks if the given object is present in the list.

    Args:
        obj (any): The object to search for.
        ls (list, optional): The list in which to search. Defaults to an empty list.

    Returns:
        bool: True if the object is in the list, False otherwise.
    """
    if obj in ls:
        return True
def safe_len(obj: str = ''):
    """
    Safely gets the length of the string representation of the given object.

    Args:
        obj (str, optional): The object whose string length is to be determined. Defaults to an empty string.

    Returns:
        int: The length of the string representation of the object. Returns 0 if any exceptions are encountered.
    """
    try:
        length = len(str(obj))
    except:
        length = 0
    return length
def line_contains(string: str = None, compare: str = None, start: int = 0, length: int = None):
    """
    Determines if the substring `compare` is present at the beginning of a section of `string` starting at the index `start` and having length `length`.

    Args:
        string (str, optional): The main string to search within. Defaults to None.
        compare (str, optional): The substring to search for. Defaults to None.
        start (int, optional): The index to start the search from. Defaults to 0.
        length (int, optional): The length of the section to consider for the search. If not specified, the length is determined safely.

    Returns:
        bool: True if the substring is found at the specified position, False otherwise.
    """
    if is_in_list(None,[string,compare]):
        return False
    if length == None:
        length = safe_len(string)
    string = string[start:length]
    if safe_len(compare)>safe_len(string):
        return False
    if string[:safe_len(compare)]==compare:
        return True
    return False

def is_bool(obj:any) -> bool:
    """
    Checks whether the input object is of type 'bool'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'bool', False otherwise.
    """
    return is_instance(obj, bool)
def is_instance(obj:any,typ:any) -> bool:
    """
    Checks whether the input object can be represented as a number.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object can be represented as a number, False otherwise.
    """
    boolIt = False
    try:
        boolIt = isinstance(obj, typ)
        return boolIt
    except:
        return boolIt
def is_list(obj:any) -> bool:
    """
    Checks whether the input object is of type 'list'.

    Args:
        obj: The object to check.

    Returns:
        bool: True if the object is of type 'list', False otherwise.
    """
    return is_instance(obj, list)
def simple_path_join(path_A:str, path_B:str):
    """
    Join two paths using the appropriate file path separator.

    Args:
        path_A (str): The first path to join.
        path_B (str): The second path to join.
    
    Returns:
        str: The joined path.
    """
    return os.path.join(str(path_A), str(path_B))
def is_file(path: str) -> bool:
    """Checks if the provided path is a file.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path is a file, False otherwise.
    """
    return os.path.isfile(path)
def get_home_folder():
    """
    Returns the path to the home directory of the current user.
    
    Returns:
        str: The path to the home directory.
    """
    return os.path.expanduser("~")
def if_not_last_child_join(path:str,child:str):
    """
    Adds a child path to the given path if it's not already present at the end.

    Args:
        path (str): The parent path.
        child (str): The child path to add.
    
    Returns:
        str: The updated path.
    """
    if path.endswith(child):
        return path
    return simple_path_join(path, child)
def path_join(*paths, isfile=False):
    final_path = os.path.join(*paths)
    paths_len = len(paths)
    for i, path in enumerate(paths):
        if i == 0:
            final_path = path  # Note: Fixed bug; original code had `final_path = paths`
        else:
            final_path = os.path.join(final_path, path)
        if isfile and is_last_itter(i, paths_len):  # Note: `is_last_itter` is undefined; assuming it checks if last iteration
            break
        os.makedirs(final_path, exist_ok=True)      
    return final_path
def get_current_path():
    """
    Returns the current working directory.
    
    Returns:
        str: The current working directory.
    """
    return os.getcwd()
def get_slash():
    """
    Returns the appropriate file path separator depending on the current operating system.
    """
    slash = '/'  # Assume a Unix-like system by default
    if slash not in get_current_path():
        slash = '\\'  # Use backslash for Windows systems
    return slash
