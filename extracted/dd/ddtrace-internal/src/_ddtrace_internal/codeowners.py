"""Parse CODEOWNERS files and match paths against their rules.

Extracted from dd-trace-py (``ddtrace/internal/codeowners.py``) as the first
module of the package split; the supported surface is ``Codeowners`` -- its
constructor and ``of()``. Everything else here is internal.
"""

import re
from pathlib import Path
from typing import Optional


def _close_char_class(regex: str, *, in_char_class: bool) -> tuple[str, bool]:
    """Append a closing ``]``: a plain literal outside a character class."""
    if in_char_class:
        return regex + "]", False
    return regex + re.escape("]"), in_char_class


def _is_full_segment_double_star(index: int, pattern: str) -> bool:
    """Whether the ``*`` at ``pattern[index]`` opens a full-segment ``**``.

    A ``**`` only matches across path segments when it is anchored on both
    sides by pattern edges or slashes (``**/x``, ``a/**/b``, ``a/**``);
    otherwise it degrades to per-segment ``[^/]*`` matching.
    """
    if index + 1 >= len(pattern) or pattern[index + 1] != "*":
        return False
    left_anchored = index == 0
    leading_slash = index > 0 and pattern[index - 1] == "/"
    right_anchored = index + 2 == len(pattern)
    trailing_slash = index + 2 < len(pattern) and pattern[index + 2] == "/"
    return (left_anchored or leading_slash) and (right_anchored or trailing_slash)


def path_to_regex(pattern: str) -> re.Pattern[str]:
    """Translate a CODEOWNERS pattern into an anchored regular expression.

    Ported from https://github.com/sbdchd/codeowners/blob/c95e13d384ac09cfa1c23be1a8601987f41968ea/codeowners/__init__.py

    Copyright (c) 2019-2020 Steve Dignam

    Permission is hereby granted, free of charge, to any person obtaining
    a copy of this software and associated documentation files (the
    "Software"), to deal in the Software without restriction, including
    without limitation the rights to use, copy, modify, merge, publish,
    distribute, sublicense, and/or sell copies of the Software, and to
    permit persons to whom the Software is furnished to do so, subject to
    the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
    OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
    WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    ported from https://github.com/hmarr/codeowners/blob/d0452091447bd2a29ee508eebc5a79874fb5d4ff/match.go#L33

    MIT License

    Copyright (c) 2020 Harry Marr
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    regex = ""

    slash_pos = pattern.find("/")
    anchored = slash_pos > -1 and slash_pos != len(pattern) - 1

    regex += r"\A" if anchored else r"(?:\A|/)"

    matches_dir = pattern[-1] == "/"
    pattern_trimmed = pattern.strip("/")

    in_char_class = False
    escaped = False

    iterator = enumerate(pattern_trimmed)
    for i, ch in iterator:
        if escaped:
            regex += re.escape(ch)
            escaped = False
            continue

        if ch == "\\":
            escaped = True
        elif ch == "*":
            if _is_full_segment_double_star(i, pattern_trimmed):
                regex += ".*"

                next(iterator, None)
                next(iterator, None)
                continue
            regex += "[^/]*"
        elif ch == "?":
            regex += "[^/]"
        elif ch == "[":
            in_char_class = True
            regex += ch
        elif ch == "]":
            regex, in_char_class = _close_char_class(regex, in_char_class=in_char_class)
        else:
            regex += re.escape(ch)

    if in_char_class:
        raise ValueError(f"unterminated character class in pattern {pattern}")

    regex += "/" if matches_dir else r"(?:\Z|/)"
    return re.compile(regex)


class Codeowners:
    """Provide interface to parse CODEOWNERS file and match a given path against it."""

    KNOWN_LOCATIONS = (
        "CODEOWNERS",
        ".github/CODEOWNERS",
        "docs/CODEOWNERS",
        ".gitlab/CODEOWNERS",
    )

    def __init__(self, path: Optional[str] = None, cwd: Optional[str] = None):
        """Initialize Codeowners object.

        :param path: path to CODEOWNERS file otherwise try to use any from known locations
        """
        self.patterns: list[tuple[re.Pattern[str], list[str]]] = []
        self.path: Optional[str] = None

        path = path or self.location(cwd)

        if path is None:
            raise ValueError("CODEOWNERS file not found")

        self.path = path
        self.parse()

    def location(self, cwd: Optional[str] = None) -> Optional[str]:
        """Return the location of the CODEOWNERS file."""
        base = Path(cwd or Path.cwd())
        for location in self.KNOWN_LOCATIONS:
            candidate = base / location
            if candidate.is_file():
                return str(candidate)
        return None

    def parse(self) -> None:
        """Parse CODEOWNERS file and store the lines and regexes."""
        if self.path is None:
            return

        with Path(self.path).open() as f:
            patterns: list[tuple[re.Pattern[str], list[str]]] = []
            for raw_line in f:
                line = raw_line.strip()

                if "#" in line:
                    # Strip out the comment from the line
                    line = line.split("#", 1)[0].strip()

                if line == "":
                    continue

                if line.startswith("[") and line.endswith("]"):
                    # found a code owners section
                    continue
                if line.startswith("^[") and line.endswith("]"):
                    # found an optional code owners section
                    continue

                elements = line.split()
                if len(elements) < 2:
                    continue

                path = elements[0]

                try:
                    pattern = path_to_regex(path)
                except (ValueError, IndexError):
                    continue

                owners = [owner for owner in elements[1:] if owner]

                if not owners:
                    continue
                patterns.append((pattern, owners))
            # Order is important. The last matching pattern has the most precedence.
            patterns.reverse()
            self.patterns = patterns

    def of(self, path: str) -> list[str]:
        """Return code owners for a given path.

        :param path: path to check
        :return: list of file code owners identified by the given path
        """
        for pattern, owners in self.patterns:
            if pattern.search(path):
                return owners
        return []
