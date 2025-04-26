#!/usr/bin/env python3
import re

# The stars/questionmarks are already escaped in the pattern
REGEX_MULTI_STARS = re.compile(r"\\\*(?:\\\*)+")
REGEX_SINGLE_STARS = re.compile(r"\\\*")
REGEX_SINGLE_QUESTIONMARK = re.compile(r"\\\?")

def translate_glob_to_regex(pattern: str) -> str:
    # fnmatch.translate(pattern) is BS, since it makes a * mathc everything (including path separators), which leads to unexpected matching rules.
    # So I use this homebrew solution and hope it does not break.

    # First escape all dots and other characters
    pattern = re.escape(pattern)

    # Two or more consecutive stars should match anything
    pattern = REGEX_MULTI_STARS.sub(".*", pattern)

    # A single star should match anything except a path separator
    pattern = REGEX_SINGLE_STARS.sub("[^/]*", pattern)

    # A single question mark should match any character except a path separator
    pattern = REGEX_SINGLE_QUESTIONMARK.sub("[^/]", pattern)

    return pattern


if __name__ == "__main__":
    # For debugging, you can execute this file directly
    for test in ["*", "*.md", "**.md", "***.md", "**/*.md", "*/**/*.*", "*****", "+-[]{}().test", "?.md", "???"]:
        print(test, "->", translate_glob_to_regex(test))
