import re
from sql_metadata import Parser
from colorama import Fore


def _flatten(d, parent_key=""):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}.{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(_flatten(v, new_key))
        else:
            items[new_key] = v
    return items

def clean_spacing(text):
    text = re.sub("\\{\\{", "{{ ", text)
    text = re.sub("\\}\\}", " }}", text)
    text = re.sub("\\{\\{\\s+", "{{ ", text)
    text = re.sub("\\s+\\}\\}", " }}", text)
    return text


def create_replacements(**kwargs):
    replacements = {}
    for k, v in kwargs.items():
        replacement = {"{{{{{k}}}}}".format(k=k): v, "{{{{ {k} }}}}".format(k=k): v}
        replacements.update(replacement)
    return replacements

def flatten_inputs(**kwargs):
    return _flatten(kwargs)


def pretty_encode_sql(
    query, keyword_color=Fore.LIGHTCYAN_EX, quote_color=Fore.LIGHTMAGENTA_EX
):
    p = Parser(query)

    keywords = list(set([t.value for t in p.tokens if t.is_keyword]))

    bold_start = "\033[1m"
    bold_end = "\033[0m"

    replacements = {k: bold_start + keyword_color + k + bold_end for k in keywords}

    for keyword, formatted_keyword in replacements.items():
        query = re.sub(r"\b{k}\b".format(k=keyword), formatted_keyword, query)

    quotes = [
        # single_quotes
        "'{t}'".format(t=text)
        for text in list(set(re.findall("'([^']*)'", query)))
    ] + [
        # double quotes
        '"{t}"'.format(t=text)
        for text in list(set(re.findall('"([^"]*)"', query)))
    ]

    replacements = {q: quote_color + q + Fore.RESET for q in quotes}

    for quote, formatted_quote in replacements.items():
        query = re.sub(quote, formatted_quote, query)

    return query
