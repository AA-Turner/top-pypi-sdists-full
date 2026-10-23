#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Translate Spark (java.util.regex) ``regexp_replace`` replacement strings to Snowflake.

Spark's ``RegExpReplace`` hands the replacement to ``Matcher.appendReplacement``, whose
syntax is:

* ``$N``      group N. The first digit is always read; further digits are consumed only
              while the number stays <= the pattern's group count ("$10" with two groups
              is group 1 followed by a literal "0").
* ``${name}`` named group ``(?<name>...)``.
* ``\\c``     the literal character ``c`` (so ``\\$`` is a dollar, ``\\\\`` a backslash and
              ``\\1`` the digit "1" -- NOT a backreference).
* anything else is literal. ``$$``, ``$x``, a trailing ``$`` or ``\\``, a malformed
  ``${...}`` and an out-of-range group are errors -- raised only when a row matches.

Snowflake's ``REGEXP_REPLACE`` reads ``\\0``..``\\9`` as single-digit group references
(``\\10`` is group 1 then "0"), ``\\\\`` as a literal backslash, and rejects every other
backslash escape. ``$`` has no meaning there. Measured on Snowflake and on Spark 3.5.3.

The translation below is a direct port of JDK 17 ``Matcher.appendExpandedReplacement``,
emitting Snowflake syntax instead of the expanded text.
"""

from __future__ import annotations

from dataclasses import dataclass

# Snowflake backreferences are a single digit, \0..\9.
SNOWFLAKE_MAX_GROUP_REFERENCE = 9


@dataclass(frozen=True)
class ReplacementTranslation:
    """Result of translating one Java replacement string.

    Exactly one of ``snowflake_replacement`` / ``error`` is set. ``error`` carries the
    message java.util.regex raises for this replacement; like Java, the caller must
    raise it only for rows that match.
    """

    snowflake_replacement: str | None = None
    error: str | None = None

    @property
    def uses_backslash(self) -> bool:
        """Whether the Snowflake replacement has a group reference or escaped backslash.

        Snowflake fails the whole query on either once the pattern has more than 9
        groups ("too many capturing groups").
        """
        return (
            self.snowflake_replacement is not None
            and "\\" in self.snowflake_replacement
        )


def _is_ascii_digit(ch: str) -> bool:
    # Java tests ``ch - '0'`` in 0..9; str.isdigit() would also accept non-ASCII digits.
    return "0" <= ch <= "9"


def _is_ascii_alnum(ch: str) -> bool:
    return _is_ascii_digit(ch) or "a" <= ch <= "z" or "A" <= ch <= "Z"


def java_pattern_groups(pattern: str) -> tuple[int, dict[str, int]] | None:
    """Capturing-group count and named-group indices of a java.util.regex pattern.

    Returns None when the pattern uses a construct this scanner does not model
    (the COMMENTS flag, where ``#`` starts a comment), or is unbalanced. Callers then
    treat the group count as unknown.
    """
    count = 0
    names: dict[str, int] = {}
    class_depth = 0
    i, n = 0, len(pattern)
    while i < n:
        ch = pattern[i]
        if ch == "\\":
            if pattern.startswith("\\Q", i):
                end = pattern.find("\\E", i + 2)
                if end < 0:
                    break  # quoted to end of pattern
                i = end + 2
            else:
                i += 2
            continue
        if class_depth:
            if ch == "[":
                class_depth += 1  # Java supports nested classes / intersections
            elif ch == "]":
                class_depth -= 1
            i += 1
            continue
        if ch == "[":
            class_depth = 1
            i += 1
            if i < n and pattern[i] == "^":
                i += 1
            if i < n and pattern[i] == "]":
                i += 1  # a leading ']' is a literal in Java
            continue
        if ch == "(":
            if pattern.startswith("(?", i):
                if (
                    pattern.startswith("(?<", i)
                    and i + 3 < n
                    and pattern[i + 3] not in "=!"
                ):
                    close = pattern.find(">", i + 3)
                    if close < 0:
                        return None
                    count += 1
                    names[pattern[i + 3 : close]] = count
                    i = close + 1
                    continue
                # Inline flags "(?x)" / "(?x:" turn on COMMENTS mode.
                j = i + 2
                while j < n and (pattern[j].isalpha() or pattern[j] == "-"):
                    if pattern[j] == "x":
                        return None
                    j += 1
            else:
                count += 1
        i += 1
    if class_depth:
        return None
    return count, names


def translate_java_replacement(
    replacement: str,
    group_count: int | None,
    group_names: dict[str, int] | None,
) -> ReplacementTranslation:
    """Translate a Spark/Java replacement string to Snowflake REGEXP_REPLACE syntax.

    ``group_count``/``group_names`` describe the pattern. Pass None when the pattern is
    not a literal: a group reference then consumes exactly one digit and no range check
    is made. That is exact for every pattern Snowflake can use with a backreference
    (it rejects backreferences once a pattern has more than 9 groups), and Snowflake
    itself raises for an out-of-range ``\\N``. Likewise Snowflake rejects ``(?<name>``,
    so with an unknown pattern ``${name}`` resolves to Java's "No group with name".
    """
    out: list[str] = []
    cursor, n = 0, len(replacement)
    while cursor < n:
        ch = replacement[cursor]
        if ch == "\\":
            cursor += 1
            if cursor == n:
                return ReplacementTranslation(
                    error="character to be escaped is missing"
                )
            out.append(_snowflake_literal(replacement[cursor]))
            cursor += 1
        elif ch == "$":
            cursor += 1
            if cursor == n:
                return ReplacementTranslation(
                    error="Illegal group reference: group index is missing"
                )
            ch = replacement[cursor]
            if ch == "{":
                cursor += 1
                start = cursor
                while cursor < n and _is_ascii_alnum(replacement[cursor]):
                    cursor += 1
                name = replacement[start:cursor]
                if not name:
                    return ReplacementTranslation(
                        error="named capturing group has 0 length name"
                    )
                # Java compares the last character it examined, which is the final
                # name character when the string ends inside the braces.
                if cursor == n or replacement[cursor] != "}":
                    return ReplacementTranslation(
                        error="named capturing group is missing trailing '}'"
                    )
                if _is_ascii_digit(name[0]):
                    return ReplacementTranslation(
                        error=f"capturing group name {{{name}}} starts with digit character"
                    )
                if not group_names or name not in group_names:
                    return ReplacementTranslation(
                        error=f"No group with name {{{name}}}"
                    )
                ref = group_names[name]
                cursor += 1
            else:
                if not _is_ascii_digit(ch):
                    return ReplacementTranslation(error="Illegal group reference")
                ref = ord(ch) - ord("0")
                cursor += 1
                # Capture the largest legal group number (Java's greedy-digit rule).
                max_group = (
                    SNOWFLAKE_MAX_GROUP_REFERENCE
                    if group_count is None
                    else group_count
                )
                while cursor < n and _is_ascii_digit(replacement[cursor]):
                    longer = ref * 10 + ord(replacement[cursor]) - ord("0")
                    if longer > max_group:
                        break
                    ref = longer
                    cursor += 1
            if group_count is not None and ref > group_count:
                return ReplacementTranslation(error=f"No group {ref}")
            if ref > SNOWFLAKE_MAX_GROUP_REFERENCE:
                return ReplacementTranslation(
                    error=(
                        f"regexp_replace replacement references group {ref}; "
                        f"Snowflake supports group references 0-"
                        f"{SNOWFLAKE_MAX_GROUP_REFERENCE} only"
                    )
                )
            out.append(f"\\{ref}")
        else:
            out.append(_snowflake_literal(ch))
            cursor += 1
    translation = ReplacementTranslation(snowflake_replacement="".join(out))
    if (
        translation.uses_backslash
        and group_count is not None
        and group_count > SNOWFLAKE_MAX_GROUP_REFERENCE
    ):
        return ReplacementTranslation(
            error=(
                f"regexp_replace pattern has {group_count} capturing groups; "
                f"Snowflake supports group references and backslashes in the "
                f"replacement only for patterns with at most "
                f"{SNOWFLAKE_MAX_GROUP_REFERENCE} groups"
            )
        )
    return translation


def _snowflake_literal(ch: str) -> str:
    # Only a backslash is special in a Snowflake replacement. A digit after a group
    # reference needs no escaping because Snowflake references are one digit long.
    return "\\\\" if ch == "\\" else ch
