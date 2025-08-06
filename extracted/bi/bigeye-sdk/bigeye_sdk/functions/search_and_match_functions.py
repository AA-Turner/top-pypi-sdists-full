from __future__ import annotations

import re
from itertools import product
from typing import List, Tuple, Dict

from rapidfuzz import fuzz


def create_regex_searchable_string(search_string: str) -> str:
    regex_string = f"^{search_string.replace('*', '.+')}$"
    escape_parens = regex_string.replace('(', "\\(").replace(')', "\\)")
    return escape_parens


def wildcard_search(search_string: str, content: List[str], is_raw_regex: bool = False) -> List[str]:
    r: List[str] = []
    search_string = search_string if is_raw_regex else create_regex_searchable_string(search_string)
    for s in content:
        if re.search(search_string, s):
            r.append(s)
    return r


def fuzzy_match(search_string: str,
                contents: List[str],
                min_match_score: int = 75) -> List[Tuple[str, str]]:
    """

    Args:
        search_string: string to fuzzy match on
        contents: list of strings to match against
        min_match_score: whole number percentage score

    Returns: List of tuples (search_string, match)

    """
    r = fuzzy_match_lists(strings1=[search_string], strings2=contents, min_match_score=min_match_score)
    return r


def fuzzy_match_lists(strings1: List[str],
                      strings2: List[str],
                      min_match_score: int) -> List[Tuple[str, str]]:
    """

    Args:
        strings1: list of strings to match on
        strings2: list of strings to match against
        min_match_score: whole number percentage score

    Returns: List of tuples (search_string, match) ordered by % of match.

    """
    cartesien = set(product(set(strings1), set(strings2)))
    l: List[Tuple[str, str, int]] = []

    for i in cartesien:
        r = fuzz.token_set_ratio(i[0], i[1])
        if r >= min_match_score:
            l.append((i[0], i[1], r))

    l.sort(key=lambda x: x[2], reverse=True)
    return [(i[0], i[1]) for i in l]


def cleanse_line(l: str) -> str:
    r = l
    r = re.sub(r'\s*#(.*)\s*#(.*)|#(.*)[^#]*', '', r)  # remove comments
    r = r.strip()  # strip all leading and trailing spaces.emoves comments and strips spcaces.
    return r


def lines_match(search: str, content: str) -> bool:
    c = content
    if len(content.strip()) > 1 and len(search.strip()) > 1 and content.strip()[0] == '-' and search.strip()[0] != '-':
        "matching object without list indicator"
        c = content.strip()[1:]
    if ':' in content and ':' not in search:
        "matching value against dictionary"
        c = c.split(':')[-1]  # split on : to take value of yaml k/v pair.
    is_match = cleanse_line(search) == cleanse_line(c)
    return is_match


def update_for_namespace_is_none(search_line: str, content: List[str], matching_lines: Dict[int, str]) -> dict:
    if namespace_not_in_file(content="".join(content)):
        matching_lines[1] = search_line

    return matching_lines


def namespace_not_in_file(content: str) -> bool:
    return re.search('namespace:', content) is None


def is_only_comment(l: str) -> bool:
    p = re.compile(r'\s*#(.*)\s*#(.*)|#(.*)[^#]*')
    return re.fullmatch(p, l.strip()) is not None and not cleanse_line(l)


def search_lines_in_source_lines(
        search_lines: List[str],
        source_lines: Dict[int, str]) -> List[Dict[int, str]]:
    """
    Search for lines (full block) within another set of lines.  Accommodates new lines in the source if not within
    the search block of lines -- capture yaml serialization differences.
    Args:
        search_lines: Block of lines to search for.
        source_lines: Block of lines to search within.

    Returns: A list of line blocks that match the search criteria.

    """

    matching_lines_sets: List[Dict[int, str]] = []
    matching_lines: Dict[int, str] = {}

    search_line_matched_ix = 0

    """Need a specific case for namespace when the key is not in the yaml file and that is the search line"""
    if search_lines[0] == "namespace: None":
        matching_lines = update_for_namespace_is_none(
            search_line=search_lines[0], content=list(source_lines.values()), matching_lines=matching_lines
        )

    if matching_lines:
        matching_lines_sets.append(matching_lines)


    def get_current_search_string():
        return search_lines[search_line_matched_ix]

    for line_number, line in source_lines.items():

        if search_line_matched_ix < len(search_lines):
            """for testing"""
            css = get_current_search_string()

        if lines_match(search=search_lines[0], content=line):
            "restarting when we find a line matching the first."
            matching_lines = {line_number: line}
            search_line_matched_ix = 1
        elif lines_match(search=get_current_search_string(), content=line):
            "appending lines that match."
            search_line_matched_ix = search_line_matched_ix + 1
            matching_lines[line_number] = line
        elif (line.isspace() or is_only_comment(line)) and not get_current_search_string().isspace() \
                and matching_lines:
            "skipping unexpected newlines in match"
            pass
        elif not lines_match(search=get_current_search_string(), content=line):
            "resetting if we find a line that doesnt match."
            search_line_matched_ix = 0
            matching_lines = {}

        if matching_lines and len(matching_lines) == len(search_lines):
            "when the match line count is equal to search line count"
            if any(lines_match(search=a, content=b)
                   for a, b in zip(search_lines, matching_lines.values())):
                matching_lines_sets.append(matching_lines)

            search_line_matched_ix = 0
            matching_lines = {}

    return matching_lines_sets
