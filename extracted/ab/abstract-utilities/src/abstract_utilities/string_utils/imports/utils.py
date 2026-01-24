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
def capitalize(string):
    return string[:1].upper() + string[1:].lower() if string else string
def get_from_kwargs(*args,**kwargs):
    del_kwarg = kwargs.get('del_kwargs',False)
    values = {}
    for key in args:
        if key:
            key = str(key)
            if key in kwargs:
                values[key] = kwargs.get(key)
                if del_kwarg:
                    del kwargs[key]
    return values,kwargs
def get_lines(string,strip=True):
    lines = string.split('\n')
    if strip:
        lines = [line for line in lines if line]
    return lines
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
