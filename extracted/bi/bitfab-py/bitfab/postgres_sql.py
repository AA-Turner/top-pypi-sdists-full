from __future__ import annotations

import re

UNRECORDED_VERBS = frozenset(
    {
        "begin",
        "commit",
        "rollback",
        "savepoint",
        "release",
        "start",
        "end",
        "abort",
        "set",
        "reset",
        "show",
        "discard",
        "deallocate",
        "listen",
        "unlisten",
        "notify",
        "prepare",
    }
)
PASSED_THROUGH_VERBS = UNRECORDED_VERBS | {"copy"}
READ_VERBS = frozenset({"select", "values", "table", "explain", "fetch"})
CTE_WRITE_VERBS = ("insert", "update", "delete", "merge")

_LEADING_NOISE = re.compile(r"\A(?:\s+|--[^\n]*(?:\n|\Z)|/\*.*?\*/|\()*", re.DOTALL)
_FIRST_KEYWORD = re.compile(r"[A-Za-z_]+")
_COMMENTS = re.compile(r"--[^\n]*|/\*.*?\*/", re.DOTALL)
_STRINGS = re.compile(r"'(?:[^']|'')*'")
_CTE_WRITE = re.compile(r"\b(" + "|".join(CTE_WRITE_VERBS) + r")\b", re.IGNORECASE)
_NAME_PART = r'(?:"[^"]+"|[A-Za-z_][\w$]*)'
_TABLE_AFTER = re.compile(
    r"\b(?:from|into|update|join)\s+(?:only\s+)?("
    + _NAME_PART
    + r"(?:\s*\.\s*"
    + _NAME_PART
    + r")*)",
    re.IGNORECASE,
)
_NAME_PARTS = re.compile(_NAME_PART)
_NOT_TABLES = frozenset({"select", "values", "lateral", "only"})


def _without_comments_and_strings(sql: str) -> str:
    return _STRINGS.sub("''", _COMMENTS.sub(" ", sql))


def statement_verb(sql: str) -> str:
    rest = sql[_LEADING_NOISE.match(sql).end() :]  # type: ignore[union-attr]
    keyword = _FIRST_KEYWORD.match(rest)
    if keyword is None:
        return ""
    verb = keyword.group(0).lower()
    if verb != "with":
        return verb
    found = _CTE_WRITE.search(_without_comments_and_strings(rest))
    return found.group(1).lower() if found else "select"


SYSTEM_SCHEMAS = ("pg_catalog.", "information_schema.")


def is_system_table(table: str | None) -> bool:
    return table is not None and table.lower().startswith(SYSTEM_SCHEMAS)


def is_read_verb(verb: str) -> bool:
    return verb in READ_VERBS


def statement_table(sql: str) -> str | None:
    for found in _TABLE_AFTER.finditer(_without_comments_and_strings(sql)):
        parts = [part.replace('"', "") for part in _NAME_PARTS.findall(found.group(1))]
        if parts[0].lower() in _NOT_TABLES:
            continue
        return ".".join(parts)
    return None
