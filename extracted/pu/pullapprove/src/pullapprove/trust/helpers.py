"""Small diff-model accessors and language-syntax tables shared across the
trust rules. The comment-syntax tables live here (not in comments.py) so the
tokenizer can derive from the same source without an import cycle — the
comments rule and the token-delta rules must never disagree about what starts
a comment."""

from __future__ import annotations

from ..diff import DiffFile, DiffHunk

# Languages grouped by their line-comment prefix. NOTE: CSS is deliberately NOT
# here — it has no `//` line comment (only `/* */`), and a `//` in a CSS value
# (e.g. a protocol-relative `url(//cdn/…)`) would otherwise read as a comment and
# hide a real value change. CSS lives in the block-comment table below only.
_SLASH_LANGS = "js jsx ts tsx mjs mts cjs cts rs go java kt kts scala swift c cc cpp cxx h hpp cs m mm zig v dart groovy gradle"
# NOTE: YAML/TOML are intentionally absent. A `#` there can be a comment, part of a
# value (`url: …/#frag`), OR literal text inside a `|`/`>` block scalar — too
# ambiguous to classify safely, so these data/config formats are declined for
# content rules (the whitespace guard in strip_inline_comment only covers the
# value-fragment case, not block scalars).
_HASH_LANGS = "py rb sh bash zsh fish pl pm r jl ex exs cr nim coffee mk cmake tf hcl"
_DASH_LANGS = "lua hs sql"
_SEMI_LANGS = "lisp clj cljs cljc edn scm rkt"
_PERCENT_LANGS = "erl hrl"

# File extension -> the line-comment prefixes that language uses.
LINE_COMMENT_PREFIXES: dict[str, tuple[str, ...]] = {
    **dict.fromkeys(_SLASH_LANGS.split(), ("//",)),
    **dict.fromkeys(_HASH_LANGS.split(), ("#",)),
    **dict.fromkeys(_DASH_LANGS.split(), ("--",)),
    **dict.fromkeys(_SEMI_LANGS.split(), (";",)),
    **dict.fromkeys(_PERCENT_LANGS.split(), ("%",)),
}

# File extension -> (open, close) block-comment delimiters. `css` is block-only.
BLOCK_COMMENT_DELIMITERS: dict[str, tuple[str, str]] = {
    **dict.fromkeys(_SLASH_LANGS.split(), ("/*", "*/")),
    "css": ("/*", "*/"),
    **dict.fromkeys(["html", "xml", "svg"], ("<!--", "-->")),
}


def extension(file: DiffFile) -> str:
    """The file's extension, without the dot. Plain string ops — every rule calls
    this per hunk, and it's just the text after the last `.` in the basename."""
    name = file.new_path.rsplit("/", 1)[-1]
    _, dot, ext = name.rpartition(".")
    return ext if dot and _ else ""


def leading_indent(text: str) -> str:
    """The leading-whitespace prefix of `text`. Indentation is semantic in Python
    (a dedent moves a statement to another block), so rules that compare
    whitespace-normalized lines must keep it, or an indent-only change would read
    as trivial and be hidden."""
    return text[: len(text) - len(text.lstrip())]


def change_suffix(hunk: DiffHunk) -> str:
    """`added`, `removed`, or `modified` based on which sides changed."""
    has_added = bool(hunk.added_lines)
    has_removed = bool(hunk.removed_lines)
    if has_added and has_removed:
        return "modified"
    return "added" if has_added else "removed"
