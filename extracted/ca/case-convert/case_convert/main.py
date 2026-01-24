import re
from os import path


def _load_general_words():
    res = []
    with open(path.join(path.dirname(__file__), "general_words.txt"), 'r') as reader:
        line = reader.readline().strip()
        while line:
            res.append(line)
            line = reader.readline().strip()
    return res


def _get_regex_delimiter(delimiters):
    if _REGEX_DELIMITER.get(delimiters) is None:
        pattern = "|".join(delimiters)
        _REGEX_DELIMITER[delimiters] = re.compile(pattern)
    return _REGEX_DELIMITER[delimiters]


def _get_words(string: str, options):
    words = _get_regex_delimiter(options.get('delimiter', _DEFAULT_DELIMITER)).split(string)
    # result = input.split(buildRegex(options.delimiter));
    i = 0

    while i < len(words):
        if words[i] == "":
            del words[i]
        else:
            for general_word in _GENERAL_WORDS:
                word_separated = False
                if len(words[i]) > len(general_word) + 2:
                    start_upper_case = str.isupper(words[i][len(general_word) - 1])
                    still_upper_case = str.isupper(words[i][len(general_word) + 1])
                    word_separated = start_upper_case != still_upper_case

                if general_word not in options.get("blacklist", []) and \
                        words[i].lower().startswith(general_word.lower()) and \
                        word_separated:
                    words = words[:i] + [general_word, words[i][len(general_word):]] + words[i + 1:]
            tmp = _REGEX_UPPER_DELIMITER.findall(words[i])
            if len(tmp) > 1:
                words = words[:i] + tmp + words[i + 1:]
            i += 1
    return words


_REGEX_UPPER_DELIMITER = re.compile("([A-Z]*[a-z0-9]+(?=[A-Z]|$)|[A-Z]+(?=$))")
_DEFAULT_DELIMITER = " -_"
_REGEX_DELIMITER = {}
_GENERAL_WORDS = _load_general_words()


def capital_word(string):
    if string == "":
        return ""
    return string[0].upper() + string[1:].lower()


def camel_case(string, **kwargs):
    """:return the string formatted with dash-case"""
    if type(string) != str:
        return ""
    tmp = pascal_case(string, **kwargs)
    return tmp[0].lower() + tmp[1:]


def kebab_case(string, **kwargs):
    """:return the string formatted with dash-case"""
    if type(string) != str:
        return ""
    return "-".join(_get_words(string, kwargs)).lower()


def pascal_case(string, **kwargs):
    """:return the string formatted with dash-case"""
    if type(string) != str:
        return ""
    return "".join(map(lambda s: capital_word(s), _get_words(string, kwargs)))


def snake_case(string, **kwargs):
    """:return the string formatted with dash-case"""
    if type(string) != str:
        return ""
    return "_".join(_get_words(string, kwargs)).lower()


def upper_case(string, **kwargs):
    """:return the string formatted with dash-case"""
    if type(string) != str:
        return ""
    return "_".join(_get_words(string, kwargs)).upper()
