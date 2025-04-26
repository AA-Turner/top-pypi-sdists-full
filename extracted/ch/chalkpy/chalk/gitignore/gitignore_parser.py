from __future__ import annotations

# Inlined from https://github.com/mherrmann/gitignore_parser/blob/master/gitignore_parser.py
import os
import re
from os.path import dirname
from pathlib import Path
from typing import Callable, List, NamedTuple, Optional, Tuple, Union


def _handle_negation(file_path: Union[str, Path], rules: List[IgnoreRule]):
    for rule in reversed(rules):
        if rule.match(str(file_path)):
            if rule.negation:
                return False
            else:
                return True
    return False


def parse_gitignore(
    full_path: Union[str, Path], base_dir: Optional[str] = None
) -> Tuple[Callable[[Union[str, Path]], bool], bool]:
    if base_dir is None:
        base_dir = dirname(full_path)
    rules: List[IgnoreRule] = []
    with open(full_path) as ignore_file:
        counter = 0
        for line in ignore_file:
            counter += 1
            line = line.rstrip("\n")
            rule = _rule_from_pattern(line, base_path=Path(base_dir).resolve(), source=(str(full_path), counter))
            if rule:
                rules.append(rule)

    has_negation = any(r.negation for r in rules)
    if has_negation:
        # We have negation rules. We can't use a simple "any" to evaluate them.
        # Later rules override earlier rules.
        return lambda file_path: _handle_negation(file_path, rules), has_negation
    else:
        return lambda file_path: any(r.match(str(file_path)) for r in rules), has_negation


def _rule_from_pattern(pattern: str, base_path: Optional[Path] = None, source: Optional[Tuple[str, int]] = None):
    """
    Take a .gitignore match pattern, such as "*.py[cod]" or "**/*.bak",
    and return an IgnoreRule suitable for matching against files and
    directories. Patterns which do not match files, such as comments
    and blank lines, will return None.
    Because git allows for nested .gitignore files, a base_path value
    is required for correct behavior. The base path should be absolute.
    """
    if base_path and base_path != Path(base_path).resolve():
        raise ValueError("base_path must be absolute")
    # Store the exact pattern for our repr and string functions
    orig_pattern = pattern
    # Early returns follow
    # Discard comments and separators
    if pattern.strip() == "" or pattern[0] == "#":
        return
    # Discard anything with more than two consecutive asterisks
    if pattern.find("***") > -1:
        return
    # Strip leading bang before examining double asterisks
    if pattern[0] == "!":
        negation = True
        pattern = pattern[1:]
    else:
        negation = False
    # Discard anything with invalid double-asterisks -- they can appear
    # at the start or the end, or be surrounded by slashes
    for m in re.finditer(r"\*\*", pattern):
        start_index = m.start()
        if (
            start_index != 0
            and start_index != len(pattern) - 2
            and (pattern[start_index - 1] != "/" or pattern[start_index + 2] != "/")
        ):
            return

    # Special-casing '/', which doesn't match any files or directories
    if pattern.rstrip() == "/":
        return

    directory_only = pattern[-1] == "/"
    # A slash is a sign that we're tied to the base_path of our rule
    # set.
    anchored = "/" in pattern[:-1]
    if pattern[0] == "/":
        pattern = pattern[1:]
    if pattern[0] == "*" and len(pattern) >= 2 and pattern[1] == "*":
        pattern = pattern[2:]
        anchored = False
    if pattern[0] == "/":
        pattern = pattern[1:]
    if pattern[-1] == "/":
        pattern = pattern[:-1]
    # patterns with leading hashes are escaped with a backslash in front, unescape it
    if pattern[0] == "\\" and pattern[1] == "#":
        pattern = pattern[1:]
    # trailing spaces are ignored unless they are escaped with a backslash
    i = len(pattern) - 1
    striptrailingspaces = True
    while i > 1 and pattern[i] == " ":
        if pattern[i - 1] == "\\":
            pattern = pattern[: i - 1] + pattern[i:]
            i = i - 1
            striptrailingspaces = False
        else:
            if striptrailingspaces:
                pattern = pattern[:i]
        i = i - 1
    regex = _fnmatch_pathname_to_regex(pattern, directory_only)
    if anchored:
        regex = f"^{regex}"
    regex = f"(?ms){regex}"
    return IgnoreRule(
        pattern=orig_pattern,
        regex=regex,
        negation=negation,
        directory_only=directory_only,
        anchored=anchored,
        base_path=Path(base_path) if base_path else None,
        source=source,
    )


_whitespace_re = re.compile(r"(\\ )+$")


class IgnoreRule(NamedTuple):
    pattern: str
    regex: str  # Basic values
    negation: bool
    directory_only: bool
    anchored: bool  # Behavior flags
    base_path: Optional[Path]  # Meaningful for gitignore-style behavior
    source: Optional[Tuple[str, int]]  # (file, line) tuple for reporting

    def __str__(self):
        return self.pattern

    def __repr__(self):
        return "".join(["IgnoreRule('", self.pattern, "')"])

    def match(self, abs_path: str):
        matched = False
        if self.base_path:
            rel_path = str(Path(abs_path).resolve().relative_to(self.base_path))
        else:
            rel_path = str(Path(abs_path))
        if rel_path.startswith("./"):
            rel_path = rel_path[2:]
        if re.search(self.regex, rel_path):
            matched = True
        return matched


# Frustratingly, python's fnmatch doesn't provide the FNM_PATHNAME
# option that .gitignore's behavior depends on.
def _fnmatch_pathname_to_regex(pattern: str, directory_only: bool):
    """
    Implements fnmatch style-behavior, as though with FNM_PATHNAME flagged;
    the path separator will not match shell-style '*' and '.' wildcards.
    """
    i, n = 0, len(pattern)

    seps = [re.escape(os.sep)]
    if os.altsep is not None:
        seps.append(re.escape(os.altsep))
    seps_group = "[" + "|".join(seps) + "]"
    nonsep = r"[^{}]".format("|".join(seps))

    res = []
    while i < n:
        c = pattern[i]
        i += 1
        if c == "*":
            try:
                if pattern[i] == "*":
                    i += 1
                    res.append(".*")
                    if pattern[i] == "/":
                        i += 1
                        res.append("".join([seps_group, "?"]))
                else:
                    res.append("".join([nonsep, "*"]))
            except IndexError:
                res.append("".join([nonsep, "*"]))
        elif c == "?":
            res.append(nonsep)
        elif c == "/":
            res.append(seps_group)
        elif c == "[":
            j = i
            if j < n and pattern[j] == "!":
                j += 1
            if j < n and pattern[j] == "]":
                j += 1
            while j < n and pattern[j] != "]":
                j += 1
            if j >= n:
                res.append("\\[")
            else:
                stuff = pattern[i:j].replace("\\", "\\\\")
                i = j + 1
                if stuff[0] == "!":
                    stuff = "".join(["^", stuff[1:]])
                elif stuff[0] == "^":
                    stuff = "".join("\\" + stuff)
                res.append("[{}]".format(stuff))
        else:
            res.append(re.escape(c))
    if directory_only:
        res.append(r"/.*$")
    else:
        res.append("(/.*|[^/]*)$")

    return "".join(res)
