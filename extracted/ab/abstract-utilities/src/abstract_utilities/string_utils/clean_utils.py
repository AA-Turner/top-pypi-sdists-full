from .eat_utils import eatAll
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
def clean_line(line):
    return eatAll(line,[' ','','\t','\n'])
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
