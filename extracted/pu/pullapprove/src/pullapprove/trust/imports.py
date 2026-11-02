"""Trust rule: hunks that only add, remove, or reorder import statements."""

from __future__ import annotations

import re

from ..diff import DiffCode, DiffFile, DiffHunk
from .helpers import change_suffix, extension
from .labels import Trust
from .linescan import collapse_ws

# File extension -> (import prefixes, multi-line bracket or None for single-line).
IMPORT_CONFIG: dict[str, tuple[tuple[str, ...], str | None]] = {
    # `export { … }` is intentionally NOT here: adding/removing an export changes
    # the module's public API and must stay visible for review, unlike an import.
    **dict.fromkeys(
        ["js", "jsx", "ts", "tsx", "mjs", "mts", "cjs", "cts"],
        (("import ", "import{"), "{"),
    ),
    "py": (("import ", "from "), "("),
    "go": (("import ",), "("),
    "rs": (("use ",), "{"),
    **dict.fromkeys(
        ["java", "kt", "kts", "scala", "groovy", "gradle"], (("import ",), None)
    ),
    **dict.fromkeys(
        ["c", "cc", "cpp", "cxx", "h", "hpp", "m", "mm"], (("#include",), None)
    ),
    "rb": (("require ", "require_relative "), None),
    "cs": (("using ",), None),
    **dict.fromkeys(["swift", "dart"], (("import ",), None)),
}

_CLOSING_BRACKET = {"(": ")", "{": "}"}

# The extensions IMPORT_CONFIG groups under the JS/TS and C-family entries
# above, repeated here so the reorder and source-swap checks below can key off
# the language without re-deriving it from IMPORT_CONFIG's shared tuples.
_JS_TS_EXTS = frozenset(["js", "jsx", "ts", "tsx", "mjs", "mts", "cjs", "cts"])
_C_EXTS = frozenset(["c", "cc", "cpp", "cxx", "h", "hpp", "m", "mm"])


def _has_trailing_statement(text: str) -> bool:
    """True if a `;` separates more code, e.g. `import x; doThing()`.

    A lone import ends at most with a trailing `;`; anything after the first one
    is a second statement we must not hide as import churn.
    """
    semicolon = text.find(";")
    return semicolon != -1 and bool(text[semicolon + 1 :].strip())


def _is_dynamic_import(text: str) -> bool:
    """A JS/TS dynamic `import(...)` call — `import` followed (after optional
    space) by `(`. It's executable code (lazy/conditional loading), not a static
    import declaration, so it must not be hidden as import churn."""
    return text.startswith("import") and text[len("import") :].lstrip().startswith("(")


def _is_import_line(content: str, prefixes: tuple[str, ...]) -> bool:
    stripped = content.strip()
    return (
        bool(stripped)
        and stripped.startswith(prefixes)
        and not _has_trailing_statement(stripped)
        and not _is_dynamic_import(stripped)
    )


def _imports_only(
    lines: list[DiffCode], prefixes: tuple[str, ...], bracket: str | None
) -> bool:
    """True if this side is entirely import statements (handling multi-line)."""
    if bracket is None:
        return all(
            not line.content.strip() or _is_import_line(line.content, prefixes)
            for line in lines
        )

    # Heuristic, not a real parser: we track multi-line continuation by counting
    # brackets, which a bracket inside a string or comment would throw off. Import
    # statements rarely contain those, and a miscount only fails to label (safe).
    close = _CLOSING_BRACKET[bracket]
    depth = 0
    for line in lines:
        text = line.content.strip()
        if not text:
            continue
        # A JS/TS dynamic `import(...)` call is executable code, not a static
        # import. Skipped for `(`-bracket languages (Go), where `import (` opens a
        # grouped import rather than a call.
        if bracket != "(" and _is_dynamic_import(text):
            return False
        # No import line — including the one that closes a multi-line import
        # (which starts at depth > 0) — may carry a trailing statement, or the
        # executable code after the `;` would be hidden as import churn.
        if _has_trailing_statement(text):
            return False
        # Outside a bracketed block, every line must start a new import.
        if depth == 0 and not text.startswith(prefixes):
            return False
        depth += text.count(bracket) - text.count(close)
        if depth < 0:
            return False
    return depth == 0


def _sorted_imports(lines: list[DiffCode], bracket: str | None) -> list[str]:
    """The full import statements on this side, sorted — a bracket-spanned
    multi-line import is joined into one string so it compares by its complete
    text (members included), not just its opening line. (Callers pass only
    import-and-blank lines, guaranteed by `_imports_only`.)"""
    statements: list[str] = []
    current: list[str] = []
    depth = 0
    for line in lines:
        text = line.content.strip()
        if not text:
            continue
        current.append(text)
        if bracket is not None:
            depth += text.count(bracket) - text.count(_CLOSING_BRACKET[bracket])
        if depth <= 0:  # statement complete (single-line, or the closing bracket)
            statements.append(collapse_ws(" ".join(current)))
            current = []
            depth = 0
    if current:  # an unclosed trailing group (defensive; shouldn't occur)
        statements.append(collapse_ws(" ".join(current)))
    return sorted(statements)


def _is_import_reorder(
    added: list[DiffCode], removed: list[DiffCode], bracket: str | None
) -> bool:
    """Same set of whole import statements, just in a different order (an empty
    result on both sides is not a reorder — there's nothing to reorder)."""
    added_imports = _sorted_imports(added, bracket)
    return bool(added_imports) and added_imports == _sorted_imports(removed, bracket)


def _is_side_effect_import(statement: str) -> bool:
    """A JS/TS side-effect import — `import 'spec';` — binds no names. Unlike
    `import x from 'spec'`, its only purpose is running the module's top-level
    code, so two of them (`import './polyfills'; import './init-sentry';`) can
    depend on running in a particular order even though the *set* of specifiers
    is unchanged."""
    after_import = statement[len("import") :].lstrip()
    return after_import.startswith(("'", '"'))


def _reorder_is_trivial(statements: list[str], ext: str) -> bool:
    """False when reordering these (already-confirmed-identical-as-a-set)
    import statements can change behavior, so the reorder must still be
    declined rather than trusted.

    - C/C++/Obj-C `#include`: can define macros/typedefs or trigger conditional
      compilation that a later include depends on — order is always
      potentially meaningful, so reorders are never trusted for this family.
    - JS/TS: trivial unless the reordered lines include a bare side-effect
      import (see `_is_side_effect_import`).
    """
    if ext in _C_EXTS:
        return False
    if ext in _JS_TS_EXTS:
        return not any(_is_side_effect_import(stmt) for stmt in statements)
    return True


# Languages where `_import_source` can reliably split "module" from "names" —
# i.e. a paired add/remove commonly keeps the module and only varies the
# imported names. Extending this to every configured language is out of scope
# for now; for the rest, `_same_import_sources` can't tell a name-only edit
# from a module swap, so it stays permissive (matching the prior behavior).
_SOURCE_AWARE_EXTS = frozenset({"py"}) | _JS_TS_EXTS | _C_EXTS


def _import_source(statement: str, ext: str) -> str | None:
    """The module/path this single import statement pulls from, or None if we
    can't confidently identify it (fail safe: an unparsed statement must not
    be treated as matching another one)."""
    if ext == "py":
        if statement.startswith("from "):
            module, _, _ = statement[len("from ") :].partition(" import")
            return module.strip() or None
        if statement.startswith("import "):
            token = re.split(r"[,\s]", statement[len("import ") :], maxsplit=1)[0]
            return token or None
        return None
    if ext in _JS_TS_EXTS:
        match = re.search(r"""from\s*(['"])(.*?)\1""", statement)
        if match:
            return match.group(2)
        # No `from` clause: a bare side-effect import, where the quoted spec
        # itself IS the source (`import 'spec';`).
        after_import = statement[len("import") :].lstrip()
        match = re.match(r"""(['"])(.*?)\1""", after_import)
        return match.group(2) if match else None
    if ext in _C_EXTS:
        match = re.search(r'["<]([^">]+)[">]', statement)
        return match.group(1) if match else None
    return None


def _same_import_sources(
    added: list[DiffCode], removed: list[DiffCode], bracket: str | None, ext: str
) -> bool:
    """True only if every added and removed import statement resolves to the
    same set of source modules — i.e. the hunk adds/removes names within an
    unchanged set of modules, not a swap to a different module
    (`-from foo import bar` / `+from evil import bar`)."""
    if ext not in _SOURCE_AWARE_EXTS:
        # We can't split "module" from "names" for this language, so we can't
        # confirm a paired modification keeps the same source rather than
        # swapping to a different module — e.g. Ruby `require 'safe'` ->
        # `require 'evil'`, which executes a different file. Decline (show it)
        # rather than trust the swap blindly; pure add/remove/reorder still
        # label via their own paths.
        return False
    added_sources = {_import_source(s, ext) for s in _sorted_imports(added, bracket)}
    removed_sources = {
        _import_source(s, ext) for s in _sorted_imports(removed, bracket)
    }
    # A statement we couldn't parse (None) is a hard stop — fail safe, don't trust.
    if None in added_sources or None in removed_sources:
        return False
    return added_sources == removed_sources


def _imports(file: DiffFile, hunk: DiffHunk) -> Trust | None:
    ext = extension(file)
    config = IMPORT_CONFIG.get(ext)
    if not config:
        return None
    prefixes, bracket = config
    added, removed = hunk.added_lines, hunk.removed_lines
    if not added and not removed:
        return None
    # `from __future__ import …` is a compiler directive, not a plain import:
    # adding one changes the whole module's semantics, and moving one below
    # another import is a SyntaxError — never trivial, so decline the hunk.
    if any("__future__" in line.content for line in (*added, *removed)):
        return None
    if not _imports_only(added, prefixes, bracket) or not _imports_only(
        removed, prefixes, bracket
    ):
        return None
    if added and removed and _is_import_reorder(added, removed, bracket):
        # Same statements, different order. Whether that's trustworthy depends
        # on the language — if not, decline outright rather than falling
        # through to the "modified" check below, which only compares source
        # modules and would trivially pass a same-statement reorder.
        statements = _sorted_imports(added, bracket)
        if not _reorder_is_trivial(statements, ext):
            return None
        return Trust.IMPORTS_REORDERED
    suffix = change_suffix(hunk)
    # A "modified" hunk (both sides non-empty, not a pure reorder) is only
    # trustworthy when it's adding/removing names within the same set of
    # source modules — not swapping to a different module.
    if suffix == "modified" and not _same_import_sources(added, removed, bracket, ext):
        return None
    # change_suffix yields added/removed/modified — each a real Trust member.
    return Trust(f"imports:{suffix}")
