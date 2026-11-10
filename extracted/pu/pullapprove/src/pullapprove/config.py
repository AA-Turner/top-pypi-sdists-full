from __future__ import annotations

import os
import posixpath
import re
import tomllib
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    import sre_parse
from collections.abc import Generator, Iterable
from enum import StrEnum
from pathlib import Path
from typing import Any, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator,
    model_validator,
)
from wcmatch import glob

from .checklists import Checklist


def _resolve_config_filename_prefix() -> str:
    """The name every config file starts with, for this process.

    Defaults to CODEREVIEW. An instance can rename it with
    PULLAPPROVE_CONFIG_PREFIX, which renames the config file itself
    (REVIEW -> REVIEW.toml, REVIEW.template.toml). Because discovery matches
    on this prefix, an instance only ever sees files named for its own prefix
    -- so two instances can watch the same repo without seeing each other's
    configs, which is how unreleased config features get tried out on a repo
    that production also watches.

    Read once at import: this is a per-process constant, not runtime state.

    Two operational constraints this doesn't (and can't) enforce:

    Prefixes must not be prefixes of one another. Matching is `startswith`
    (see is_config_filename), and a suffix after the prefix is legitimate --
    CODEREVIEW.template.toml and CODEREVIEW-BASE.toml are both real config
    names -- so a REVIEW instance would also pick up REVIEW_DEV.toml. An
    instance only knows its own prefix, so pick names that don't overlap
    (REVIEW and DEV_REVIEW, not REVIEW and REVIEW_DEV).

    Changing the prefix on a live instance means clearing its cached configs.
    Config rows are keyed by (repo, sha) with no record of which prefix
    discovered them, so a sha already processed under the old prefix keeps
    serving from cache and the new prefix's files are never fetched.
    """
    # `or` rather than a get() default: an explicitly empty value
    # (`PULLAPPROVE_CONFIG_PREFIX=` in a .env or compose file -- a normal way to
    # write "unset") is not a missing key, and would name the config ".toml".
    prefix = os.environ.get("PULLAPPROVE_CONFIG_PREFIX", "").strip() or "CODEREVIEW"

    # A bad prefix would silently match nothing (i.e. every repo looks
    # unconfigured), so refuse to start instead.
    if prefix.endswith(".toml"):
        raise ValueError(
            f"PULLAPPROVE_CONFIG_PREFIX should be a name without an extension, not {prefix!r}. "
            f"The config file is named after it (e.g. {prefix[: -len('.toml')]!r} -> {prefix!r})."
        )
    if "\\" in prefix or prefix != posixpath.basename(prefix):
        raise ValueError(
            f"PULLAPPROVE_CONFIG_PREFIX should be a filename prefix, not a path: {prefix!r}"
        )

    return prefix


CONFIG_FILENAME_PREFIX = _resolve_config_filename_prefix()
CONFIG_FILENAME = f"{CONFIG_FILENAME_PREFIX}.toml"


def is_config_filename(basename: str) -> bool:
    """Whether a filename is a config file (CODEREVIEW.toml,
    CODEREVIEW.template.toml).

    The prefix half is what isolates instances: an instance running a renamed
    prefix (see PULLAPPROVE_CONFIG_PREFIX) never even discovers another
    instance's configs. The extension half keeps a neighbor like CODEREVIEW.md
    from being treated as one.
    """
    return basename.startswith(CONFIG_FILENAME_PREFIX) and basename.endswith(".toml")


def is_config_path(path: str) -> bool:
    """Whether a repo-relative path names a config file."""
    return is_config_filename(posixpath.basename(path))


_REPEAT_OPS = {sre_parse.MAX_REPEAT, sre_parse.MIN_REPEAT}


def _has_nested_quantifiers(data: Any) -> bool:
    """Detect patterns like (a+)+ that cause catastrophic backtracking."""
    for op, av in data:
        if op in _REPEAT_OPS:
            if _contains_quantifier(av[2]):
                return True
        elif op == sre_parse.SUBPATTERN:
            if _has_nested_quantifiers(av[-1]):
                return True
        elif op == sre_parse.BRANCH:  # noqa: SIM102
            if any(_has_nested_quantifiers(branch) for branch in av[1]):
                return True
    return False


def _contains_quantifier(data: Any) -> bool:
    for op, av in data:
        if op in _REPEAT_OPS:
            return True
        elif op == sre_parse.SUBPATTERN:
            if _contains_quantifier(av[-1]):
                return True
        elif op == sre_parse.BRANCH:  # noqa: SIM102
            if any(_contains_quantifier(branch) for branch in av[1]):
                return True
    return False


_TEAM_REF_SEGMENT = r"[a-zA-Z0-9][a-zA-Z0-9\-_.]*"
_TEAM_REF_RE = re.compile(rf"^{_TEAM_REF_SEGMENT}(/{_TEAM_REF_SEGMENT})+$")

# Fields that hold reviewer identities (plain usernames, `$aliases`, and
# `@team` refs) rather than paths/code/labels. Team refs only expand here.
USER_LIST_FIELDS = ("authors", "reviewers", "alternates", "cc")

# Roster fields where "!" performs compile-time subtraction (remove from the
# resolved list) rather than surviving as a match-time predicate. `authors`
# is deliberately excluded — its "!" entries are consumed by `matches_author`.
ROSTER_FIELDS = ("reviewers", "alternates", "cc")


def _split_team_ref(value: str) -> tuple[str, str] | None:
    """Split a value into `(prefix, ref)` if it has team-reference shape
    (`@org/team` or `!@org/team`), `prefix` being `"!"` or `""`. Returns
    `None` for anything else, so callers fall back to their own handling of
    plain values.
    """
    if value.startswith("!@"):
        return "!", value[2:]
    if value.startswith("@"):
        return "", value[1:]
    return None


def is_unexpanded_ref(value: str) -> bool:
    """True if the value is a `$alias` or `@team` reference (optionally
    negated with a leading `!`) that has not been expanded — as opposed to a
    plain username. Only an offline compile (`teams=None`) leaves such values
    in user-list fields.
    """
    return value.removeprefix("!").startswith(("$", "@"))


def _validate_team_refs(values: list[str]) -> list[str]:
    """Team references (`@org/team`, `!@org/team`) need at least two
    slash-separated segments. This only checks shape — membership is resolved
    later, at compile time, against the caller-provided `teams` mapping.

    Any other value containing "@" is rejected too — that shape is reserved
    for team references (and, in future, email-style identifiers), so it
    can't be confused with a plain username.
    """
    for value in values:
        split = _split_team_ref(value)
        if split is None:
            if "@" in value:
                raise ValueError(
                    f"Invalid value '{value}': email addresses are not "
                    "supported here — use the platform username"
                )
            continue

        _prefix, ref = split
        if not _TEAM_REF_RE.match(ref):
            raise ValueError(
                f"Invalid team reference '{value}': team references need the "
                "'org/team' form"
            )
    return values


def _expand_team_ref(
    ref: str, teams: dict[str, list[str]] | None, prefix: str
) -> list[str]:
    """Expand a single team reference (without its `@`/`!@`) to member usernames.

    `teams=None` is the offline/CLI mode: the library never calls out to
    GitHub/GitLab itself, so with no mapping provided the reference passes
    through unexpanded rather than erroring. With a `teams` mapping (even an
    empty one), an unresolvable ref is a loud config error, matching how
    unknown `$aliases` are handled.
    """
    if teams is None:
        return [f"{prefix}@{ref}"]

    members = teams.get(ref.lower())
    if members is None:
        raise ValueError(f"Unknown team: {prefix}@{ref}")

    return [f"{prefix}{member}" for member in members]


def _expand_aliases(
    values: list[str],
    aliases: dict[str, list[str]],
    teams: dict[str, list[str]] | None = None,
    expand_teams: bool = False,
    _seen: set[str] | None = None,
    _path: list[str] | None = None,
) -> list[str]:
    """Replace alias references in a list with their mapped values recursively.

    Team references (`@org/team`) are only expanded when `expand_teams` is
    True — user-list fields (reviewers, alternates, authors, cc). Elsewhere
    (paths, code, labels) a leading `@` is a literal string, e.g. npm-style
    scoped path patterns like `@vendor/pkg/**`. Teams are always leaf nodes —
    their values are plain usernames, never other refs — so expanding one
    never recurses further.
    """
    if _seen is None:
        _seen = set()
    if _path is None:
        _path = []

    expanded: list[str] = []
    for value in values:
        # Support negated aliases like "!$team" -> ["!alice", "!bob"]
        if value.startswith("!$"):
            prefix = "!"
            alias_ref = value[2:]
        elif value.startswith("$"):
            prefix = ""
            alias_ref = value[1:]
        elif expand_teams and (team_ref := _split_team_ref(value)) is not None:
            team_prefix, ref = team_ref
            expanded.extend(_expand_team_ref(ref=ref, teams=teams, prefix=team_prefix))
            continue
        else:
            expanded.append(value)
            continue

        if alias_ref in _seen:
            # Cycle detected, raise an error with the cycle path
            cycle_path = _path[_path.index(alias_ref) :] + [alias_ref]
            raise ValueError(
                f"Circular reference detected in aliases: {' -> '.join(cycle_path)}"
            )
        if alias_ref in aliases:
            _seen.add(alias_ref)
            _path.append(alias_ref)
            # Recursively expand the alias values
            nested_expanded = _expand_aliases(
                aliases[alias_ref],
                aliases=aliases,
                teams=teams,
                expand_teams=expand_teams,
                _seen=_seen,
                _path=_path,
            )
            if prefix:
                expanded.extend(prefix + v for v in nested_expanded)
            else:
                expanded.extend(nested_expanded)
            _path.pop()
            _seen.remove(alias_ref)
        else:
            # Unknown alias — surface it loudly instead of silently dropping the
            # reference (a typo'd alias would otherwise vanish reviewers/paths).
            raise ValueError(f"Unknown alias: {prefix}${alias_ref}")

    # Remove duplicates while preserving order
    return list(dict.fromkeys(expanded))


def _apply_negations(values: list[str]) -> list[str]:
    """Compile-time subtraction for roster fields (`ROSTER_FIELDS`): a "!name"
    entry removes "name" from the resolved list instead of surviving as a
    match-time rule (contrast `authors`, handled by `matches_author`).

    A list still holding an unexpanded `@team` ref (offline compile, i.e.
    teams=None) is returned untouched — it isn't fully resolved yet, so
    subtraction can't run, and the partially-resolved config must round-trip
    unchanged. `$aliases` must already be expanded by the caller.

    The wildcard+negation error fires BEFORE that early return: it's a check
    on the written form (`"*"` alongside any `"!"` entry, team ref or not),
    so an offline compile must reject it the same way the server will — a
    `pullapprove check` that passes locally can't then error in production.
    """
    if "*" in values and any(v.startswith("!") for v in values):
        raise ValueError(
            'Negation cannot be combined with "*" in reviewers/alternates/cc '
            "(wildcard exclusion is not supported)"
        )

    if any(_split_team_ref(v) is not None for v in values):
        return values

    negations = {v[1:].lower() for v in values if v.startswith("!")}
    return [v for v in values if not v.startswith("!") and v.lower() not in negations]


def _validate_review_counts(label: str, data: dict[str, Any]) -> None:
    """Compile-time rejection of negative require/request/author_value.
    Shared by scopes and large_scale_change (which has no author_value —
    the `.get` default passes trivially there).

    These are compile-time checks (not field validators) because negative
    values were previously accepted, so compiled configs stored inside old
    processing results must keep parsing (where they keep their old
    behavior: a negative require always passed, a negative request
    requested nobody).
    """
    for field in ("require", "request", "author_value"):
        if data.get(field, 0) < 0:
            raise ValueError(f"{label}: {field} cannot be negative")


def _validate_global_require(*, label: str, scope: dict[str, Any]) -> None:
    """Global scopes need require >= 1: a satisfied global scope passes every
    file it matches, and require = 0 (the default) is satisfied before anyone
    reviews. Compile-time, like _validate_review_counts, so compiled configs
    stored inside old processing results keep parsing.
    """
    if (
        scope.get("ownership") == OwnershipChoices.GLOBAL
        and scope.get("require", 0) < 1
    ):
        raise ValueError(
            f"{label}: global scopes need require >= 1 "
            "(0 would pass every file it matches)"
        )


# How directly a config points at a person, most specific first. Which one
# wins is decided in `_resolve_reviewer_alternate_overlap`.
_MENTIONED_BY_USERNAME = 3
_MENTIONED_BY_ALIAS = 2
_MENTIONED_BY_TEAM = 1


def _mentions_by_username_or_alias(
    values: list[str], *, aliases: dict[str, list[str]]
) -> dict[str, int]:
    """Each login a user list, as written, mentions by username or through an
    alias, keyed by lowercased login, with its most specific mention.

    Team refs are skipped, whether written in the field or inside an alias:
    a team mention is the lowest level, so it never needs looking up. Negated
    entries are subtractions, not mentions.
    """
    flattened: list[tuple[str, int]] = []
    for value in values:
        if value.startswith("$"):
            # An alias flattens to usernames, plus any team refs and
            # negations written inside it.
            flattened.extend(
                (alias_value, _MENTIONED_BY_ALIAS)
                for alias_value in _expand_aliases([value], aliases)
            )
        else:
            flattened.append((value, _MENTIONED_BY_USERNAME))

    mentions: dict[str, int] = {}
    for value, level in flattened:
        if value.startswith("!") or _split_team_ref(value) is not None:
            continue
        key = value.lower()
        mentions[key] = max(mentions.get(key, 0), level)
    return mentions


def _resolve_reviewer_alternate_overlap(
    *,
    entry: dict[str, Any],
    written: dict[str, list[str]],
    aliases: dict[str, list[str]],
) -> None:
    """Someone in both `reviewers` and `alternates` is requested only if
    `reviewers` mentions them at least as specifically as `alternates` does:
    a username beats an alias, an alias beats a team, and a tie leaves them
    a reviewer. Whoever `alternates` outranks is dropped from the compiled
    `reviewers`, so for this scope they are an alternate: they count, but
    are never requested.

    The compiled lists decide who is in both. `written`, the two fields
    before expansion, decides how specifically each one mentions them. An
    unexpanded team ref left by an offline compile is not a login, so it is
    never dropped.
    """
    if not entry.get("reviewers") or not entry.get("alternates"):
        return

    reviewer_mentions = _mentions_by_username_or_alias(
        written["reviewers"], aliases=aliases
    )
    alternate_mentions = _mentions_by_username_or_alias(
        written["alternates"], aliases=aliases
    )

    # A reviewer with no username or alias mention got there through a team.
    # Only a username or alias mention in `alternates` can outrank that.
    compiled_alternates = {login.lower() for login in entry["alternates"]}
    outranked = {
        login
        for login, level in alternate_mentions.items()
        if login in compiled_alternates
        and level > reviewer_mentions.get(login, _MENTIONED_BY_TEAM)
    }
    if not outranked:
        return

    entry["reviewers"] = [
        login for login in entry["reviewers"] if login.lower() not in outranked
    ]


def _compile_review_fields(
    *,
    entry: dict[str, Any],
    label: str,
    aliases: dict[str, list[str]],
    teams: dict[str, list[str]] | None,
) -> None:
    """Compile a raw scope, or the large-scale change, in place: expand
    aliases, apply "!" subtraction, reject what can never work, and settle
    who is both a reviewer and an alternate. Only the fields the entry has
    are touched. `label` names it in error messages ("Scope 'app'",
    "large_scale_change").
    """
    # Reviewers and alternates as written: once expanded, a list no longer
    # says whether a login was typed in or came from an alias or a team.
    written = {
        field: entry[field] for field in ("reviewers", "alternates") if field in entry
    }

    # Team refs only expand in user-list fields — paths/code/labels keep a
    # leading "@" literal.
    for field in (
        "paths",
        "code",
        "authors",
        "reviewers",
        "alternates",
        "cc",
        "labels",
    ):
        if field in entry:
            entry[field] = _expand_aliases(
                entry[field],
                aliases,
                teams=teams,
                expand_teams=field in USER_LIST_FIELDS,
            )

    # Apply compile-time "!" subtraction to roster fields.
    # `_apply_negations` leaves a field with an unexpanded team ref
    # (offline compile, i.e. teams=None) untouched.
    for field in ROSTER_FIELDS:
        if field in entry:
            entry[field] = _apply_negations(entry[field])
            _reject_bot_reviewers(entry[field], where=f"{label} {field}")

    # The "*" wildcard is only meaningful in `reviewers` — everywhere
    # else it's matched as a literal username and silently does
    # nothing: in `alternates` the scope stays pending forever, in
    # `authors` the scope never applies to any PR, in `cc` nobody is
    # notified. Reject it at compile time (after alias expansion, so
    # `$alias` indirection can't smuggle it in) rather than as a
    # ScopeModel validator, because compiled configs stored inside
    # old processing results must keep parsing.
    # Messages must stay under ~130 chars: they become the git-host
    # commit status description, which the adapters slice to 140.
    for field, hint in (
        (
            "authors",
            "remove it (a scope with no authors applies to any author)",
        ),
        (
            "alternates",
            "add it to reviewers instead (wildcard reviewers are never auto-requested)",
        ),
        ("cc", "remove it"),
    ):
        if "*" in entry.get(field, []):
            raise ValueError(f'{label}: "*" is not supported in {field} — {hint}')

    _validate_review_counts(label, entry)

    _resolve_reviewer_alternate_overlap(entry=entry, written=written, aliases=aliases)


def _roster_shortfall(
    *, reviewers: list[str], alternates: list[str], require: int
) -> str | None:
    """Why `require` approvals can never come from these reviewers and
    alternates, or None if they can."""
    all_reviewers = reviewers + alternates

    # Skip if wildcard - anyone can review
    if "*" in all_reviewers:
        return None

    # Skip if aliases or team refs (possibly negated with "!") are not yet
    # expanded. Re-validation after compilation only re-checks refs that
    # actually resolve — an offline compile (teams=None) leaves refs
    # unexpanded, so this same skip fires again there too.
    if any(is_unexpanded_ref(r) for r in all_reviewers):
        return None

    if len(all_reviewers) < require:
        return f"has require={require} but only {len(all_reviewers)} reviewers/alternates specified"

    return None


def _resolve_extends_path(extending_path: str, extends_ref: str) -> str:
    """Resolve an `extends` reference to a canonical repo-relative config key.

    - `/x` is repo-root-relative.
    - everything else (`../x`, `dir/x`, bare `x`) is relative to the extending
      file's directory.

    Raises if the reference escapes above the repo root.
    """
    if extends_ref.startswith("/"):
        resolved = posixpath.normpath(extends_ref.lstrip("/"))
    else:
        base_dir = posixpath.dirname(extending_path)
        resolved = posixpath.normpath(posixpath.join(base_dir, extends_ref))

    if resolved == ".." or resolved.startswith("../"):
        raise ValueError(
            f"Invalid extends path: '{extends_ref}' points above the repo root"
        )

    return resolved


def scope_line_range(*, content: str, scope_name: str) -> tuple[int, int] | None:
    """The first and last line (1-indexed) of the `[[scopes]]` table that
    declares a scope, or None when it isn't written as its own table (an
    inline `scopes = [...]`, say).

    TOML parsers don't report positions, so this splits the text at its table
    headers and parses each `[[scopes]]` block on its own.
    """
    # Only `\n` ends a line, as in git and editors (`splitlines` also splits
    # on characters like U+2028).
    lines = content.split("\n")

    # Every table header starts a block, except a scope's own sub-tables
    # (`[[scopes.checklist.items]]`), which belong to the scope above them. A
    # line inside a multi-line string is never a header, whatever it starts
    # with.
    block_starts = [
        index
        for index, starts_outside in enumerate(_lines_outside_strings(lines))
        if starts_outside
        and _table_header(lines[index])
        and not _table_header(lines[index]).startswith(("[scopes.", "[[scopes."))
    ]
    block_ends = block_starts[1:] + [len(lines)]

    for start, end in zip(block_starts, block_ends):
        if not _table_header(lines[start]).startswith("[[scopes]]"):
            continue
        try:
            block = tomllib.loads("\n".join(lines[start:end]))
        except tomllib.TOMLDecodeError:
            continue
        if block["scopes"][0].get("name") != scope_name:
            continue

        # Blank lines and comments at the end lead into the next table.
        while end > start + 1 and (
            not lines[end - 1].strip() or lines[end - 1].lstrip().startswith("#")
        ):
            end -= 1
        return start + 1, end

    return None


def _table_header(line: str) -> str:
    """A table header line without the whitespace and quotes TOML allows in
    it (`[[ "scopes" ]]` is `[[scopes]]`), or "" for any other line."""
    stripped = line.strip()
    if not stripped.startswith("["):
        return ""
    return re.sub(r"[\s\"']", "", stripped)


def _lines_outside_strings(lines: list[str]) -> list[bool]:
    """For each line, whether it starts outside a multi-line string. Comments
    and single-line strings are skipped, so a `\"\"\"` inside one of them
    doesn't open anything."""
    starts_outside = []
    open_multiline = ""  # `"""` or `'''` while inside one
    for line in lines:
        starts_outside.append(not open_multiline)
        index = 0
        while index < len(line):
            if open_multiline == '"""':
                if line[index] == "\\":
                    index += 2
                elif line.startswith('"""', index):
                    open_multiline = ""
                    # Up to two quotes may sit right before the delimiter.
                    while line.startswith('"', index + 3):
                        index += 1
                    index += 3
                else:
                    index += 1
            elif open_multiline == "'''":
                close = line.find("'''", index)
                if close == -1:
                    break
                open_multiline = ""
                index = close + 3
                while line.startswith("'", index):
                    index += 1
            elif line.startswith(('"""', "'''"), index):
                open_multiline = line[index : index + 3]
                index += 3
            elif line[index] == "#":
                break
            elif line[index] == '"':
                # A basic string ends at the next unescaped quote.
                index += 1
                while index < len(line) and line[index] != '"':
                    index += 2 if line[index] == "\\" else 1
                index += 1
            elif line[index] == "'":
                # A literal string has no escapes.
                close = line.find("'", index + 1)
                index = len(line) if close == -1 else close + 1
            else:
                index += 1
    return starts_outside


def matches_path_patterns(*, path: Path, patterns: list[str]) -> bool:
    """Whether `path` matches any of the config's path globs.

    The one definition of the config's glob semantics.
    """
    # TODO paths shouldn't start with /
    return glob.globmatch(
        path,
        patterns,
        flags=glob.GLOBSTAR | glob.BRACE | glob.NEGATE | glob.IGNORECASE | glob.DOTGLOB,
    )


def _anchor_path(base_dir: str, pattern: str) -> str:
    """Anchor a scope path glob at `base_dir` (the owning config's directory).

    Scope paths are written relative to the config they live in. A leading `/`
    makes a pattern repo-root-absolute (escape hatch); a leading `!` negation is
    preserved. With an empty `base_dir` (root config) the pattern is unchanged.
    """
    negate = pattern.startswith("!")
    if negate:
        pattern = pattern[1:]

    if pattern.startswith("/"):
        anchored = pattern.lstrip("/")
    elif base_dir:
        anchored = f"{base_dir}/{pattern}"
    else:
        anchored = pattern

    return f"!{anchored}" if negate else anchored


class OwnershipChoices(StrEnum):
    EMPTY = ""
    APPEND = "append"
    GLOBAL = "global"


# A GitHub App has two names: the login it posts as (`name[bot]`) and the slug
# that owns its check runs (`name`). The suffix is how the engine tells a bot
# from a person -- a `[bot]` account never counts as a human and never sits in
# a roster, no declaration needed.
BOT_LOGIN_SUFFIX = "[bot]"


def is_bot_login(username: str) -> bool:
    """The engine rule, in one place: a `[bot]` account is never a person."""
    return username.lower().endswith(BOT_LOGIN_SUFFIX)


def _split_check_ref(ref: str) -> tuple[str, str]:
    """An `unless` ref as (producer slug lowercased, check name).

    Split on the FIRST `/`: App slugs cannot contain one, check names can.
    Both parts are stripped -- the validator checks THIS function's output, so
    a ref that validates is exactly a ref that matches at runtime.
    """
    producer, _, name = ref.partition("/")
    return producer.strip().lower(), name.strip()


def _reject_bot_reviewers(values: list[str], *, where: str) -> None:
    """Reject any `[bot]` account listed in a roster surface (a scope's
    reviewers/alternates/cc, or large_scale_change.reviewers/alternates).

    A bot is never a person, so it can never sit in a roster: bots that open
    pull requests are routed with `authors`, and bots that attest are
    referenced from `unless`. Checked after alias expansion so `$alias`
    indirection can't smuggle one in. `where` names the surface; the message
    becomes the git-host commit status, so it stays under ~130 chars.
    """
    for entry in values:
        if is_bot_login(entry):
            raise ValueError(
                f"{where}: '{entry}' is a bot and cannot be listed as a reviewer"
            )


def _first_case_insensitive_duplicate(values: Iterable[str]) -> str | None:
    """The first value whose lowercased form was already seen, else None."""
    seen: set[str] = set()
    for value in values:
        if value.lower() in seen:
            return value
        seen.add(value.lower())
    return None


class ScopeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Required fields
    name: str = Field(min_length=1)
    paths: list[str] = Field(min_length=1)

    # Optional fields

    # Expanded version of lines could be dict
    # with fnmatch, regex, exclude patterns, etc?
    code: list[str] = []

    # This only filtering field that can't be used with raw diff/files...
    # If we get into that, the others are:
    # - labels
    # - ref
    # - statuses
    # - dates
    # - body
    # - title
    # - other scopes
    # (this is how I ended up with expressions...
    # I'm not trying to build a general purpose workflow tool,
    # but I do need to support the legit use cases and AI/bot review is one, so is team hierarchy)
    authors: list[str] = []

    # (defaults should be the "empty" values)
    description: str = ""
    reviewers: list[str] = []
    alternates: list[str] = []
    cc: list[str] = []

    # Review scoring
    # Negative values are rejected at compile time (_validate_review_counts)
    require: int = 0
    author_value: int = 0

    # The checks that can attest this scope's review requirement away. Each ref
    # is "producer/check-name" -- the slug of the App that produces the check,
    # then the check run's name, split on the first "/". When every listed
    # check has completed successfully on the current head commit, the scope is
    # waived: its requirement drops to zero and the evidence is stored on the
    # result. Failed, skipped, pending, missing -- the requirement stands
    # unchanged; passing is the only state that subtracts.
    #
    # Deliberately placed next to the `require` it undermines, so reading a
    # scope always reveals whether its human review is removable. A list is
    # implicitly "all must pass" -- OR, thresholds, and 2-of-3 belong in the
    # producer, which can post one combined check.
    unless: list[str] = []

    # How scopes are combined
    ownership: OwnershipChoices = OwnershipChoices.EMPTY

    # Actionable items
    request: int = 0
    labels: list[str] = []
    instructions: str = ""

    # Approval checklist
    checklist: Checklist | None = None

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, name: str) -> str:
        if "," in name:
            raise ValueError("Scope name cannot contain commas")
        return name

    @field_validator(*USER_LIST_FIELDS, mode="after")
    @classmethod
    def validate_team_ref_shape(cls, values: list[str]) -> list[str]:
        return _validate_team_refs(values)

    @field_validator("unless", mode="after")
    @classmethod
    def validate_unless_refs(cls, values: list[str]) -> list[str]:
        """A check name alone is worthless -- any workflow with `checks: write`
        can post any name -- so a bare name is a parse error, not a default.
        Messages stay under ~130 chars: they become the git-host commit status.
        """
        for ref in values:
            producer, name = _split_check_ref(ref)
            if "/" not in ref or not producer or not name:
                raise ValueError(
                    f"unless: '{ref}' must be 'producer/check-name' -- the App "
                    "slug that produces the check, then the check's name"
                )
            # To most users PullApprove *is* "the check" on their PRs.
            # PullApprove never creates these checks, it only reads them -- and
            # a config waiting on our own status would deadlock politely.
            if producer == "pullapprove":
                raise ValueError(
                    f"unless: '{ref}' references PullApprove itself -- "
                    "PullApprove never creates checks, it only reads them"
                )
        return values

    @field_validator("code", mode="after")
    @classmethod
    def validate_code_patterns(cls, code: list[str]) -> list[str]:
        for pattern in code:
            try:
                parsed = sre_parse.parse(pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern}': {e}") from None
            if _has_nested_quantifiers(parsed):
                raise ValueError(
                    f"Regex pattern '{pattern}' contains nested quantifiers, "
                    "which can cause catastrophic backtracking."
                )
        return code

    @model_validator(mode="after")
    def validate_reviewers_for_require(self) -> ScopeModel:
        if reason := _roster_shortfall(
            reviewers=self.reviewers,
            alternates=self.alternates,
            require=self.require,
        ):
            raise ValueError(reason)
        return self

    def named_usernames(self) -> set[str]:
        """Everyone in `reviewers` or `alternates`, lowercased because every
        username comparison here is case-insensitive. A "*" entry is kept as
        is; it never matches a real username."""
        return {r.lower() for r in self.reviewers + self.alternates}

    def counts_toward(self, username: str) -> bool:
        """Whether this person's review counts for this scope.

        Everyone it names, plus everybody when `reviewers` holds the
        wildcard. A wildcard in `alternates` does not count everybody: the
        wildcard describes the scope's `reviewers`, not its backups.
        """
        if "*" in self.reviewers:
            return True
        return username.lower() in self.named_usernames()

    def author_points(self, author_username: str) -> int:
        """`author_value` if the scope names the author, reviewer or
        alternate. Being covered by the wildcard earns nothing."""
        if author_username.lower() in self.named_usernames():
            return self.author_value
        return 0

    def unless_refs(self) -> list[tuple[str, str]]:
        """Each `unless` entry as (producer slug lowercased, check name)."""
        return [_split_check_ref(ref) for ref in self.unless]

    def unsolvable_reason(self, author_username: str) -> str | None:
        """
        Explain why this scope can never pass for a PR authored by this user,
        or None if it can.

        Messages must stay under ~130 chars: they flow into the git-host
        commit status description, which the adapters slice to 140.
        """
        if "*" in self.reviewers:
            # Anyone can review, so any require is satisfiable
            return None

        # Count eligible reviewers (excluding author who can't self-approve)
        eligible_reviewers = self.named_usernames() - {author_username.lower()}
        max_possible_points = len(eligible_reviewers) + self.author_points(
            author_username
        )

        if self.require > 0 and max_possible_points < self.require:
            if not eligible_reviewers:
                return (
                    "PR author is the only reviewer/alternate and cannot self-approve"
                )
            return f"require={self.require} but only {max_possible_points} possible approvals (excluding author)"

        return None

    def ownership_marker(self) -> str:
        """The glyph a non-default ownership puts in front of the scope name.

        Split out from printed_name so a renderer that styles the marker apart
        from the name doesn't have to know which glyph goes with which mode.
        """
        match self.ownership:
            case OwnershipChoices.APPEND:
                return "+"
            case OwnershipChoices.GLOBAL:
                return "*"

        return ""

    def printed_name(self) -> str:
        return self.ownership_marker() + self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ScopeModel):
            return NotImplemented
        return self.name == other.name

    def matches_path(self, path: Path) -> bool:
        return matches_path_patterns(path=path, patterns=self.paths)

    def matches_code(self, code: str) -> Generator[dict[str, int]]:
        patterns = getattr(self, "_code_regex_patterns", [])
        if not patterns:
            patterns = [re.compile(pattern, re.MULTILINE) for pattern in self.code]
            self._code_regex_patterns = patterns

        for pattern in patterns:
            for match in pattern.finditer(code):
                start_index = match.start()
                end_index = match.end()

                start_line = code.count("\n", 0, start_index) + 1
                start_col = start_index - code.rfind("\n", 0, start_index)

                end_line = code.count("\n", 0, end_index) + 1
                end_col = end_index - code.rfind("\n", 0, end_index)

                yield {
                    "start_line": start_line,
                    "start_col": start_col,
                    "end_line": end_line,
                    "end_col": end_col,
                }

    def matches_author(self, author_username: str) -> bool:
        if not self.authors:
            # No authors specified, so assume it matches
            return True

        # An offline compile (teams=None) leaves `@org/team` refs as written,
        # and comparing a username to one would quietly give the wrong answer
        for author in self.authors:
            if is_unexpanded_ref(author):
                raise ValueError(
                    f"Scope {self.name} lists {author} in authors, "
                    "and its members haven't been looked up"
                )

        author_username_lower = author_username.lower()

        negated_authors = [a[1:].lower() for a in self.authors if a.startswith("!")]
        authors = [a.lower() for a in self.authors if not a.startswith("!")]

        if author_username_lower in negated_authors:
            # If the author is in the negated list, return False
            return False

        if not authors:
            # Negation-only: everyone not negated matches
            return True

        return author_username_lower in authors


# The scope a large-scale change is reviewed as (LargeScaleChangeModel.as_scope).
LARGE_SCALE_CHANGE_SCOPE_NAME = "Large-scale change"


class LargeScaleChangeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Note, an LSC only applies to diffs, not raw files,
    # because we have to know what *changed*.

    # Reviewed as a scope (see as_scope), so each field means what it means
    # on a scope. There has to be at least one reviewer, so a PR that turns
    # out to be an LSC errors until the config names some.
    # Negative values are rejected at compile time (_validate_review_counts)
    require: int = 1
    request: int = 0
    reviewers: list[str] = []
    alternates: list[str] = []
    # min_paths: int = 300
    # min_lines: int = 3000
    labels: list[str] = []

    @field_validator("reviewers", "alternates", mode="after")
    @classmethod
    def validate_team_ref_shape(cls, values: list[str]) -> list[str]:
        return _validate_team_refs(values)

    def as_scope(self) -> ScopeModel:
        """The scope a large-scale change is reviewed as, in place of the
        scopes its diff was too large to match. It covers every path, and is
        scored, requested and shown like any other scope.

        Raises ValueError when no set of reviewers could ever approve it.
        Messages must stay under ~130 chars: they become the git-host commit
        status description.
        """
        # A scope can get by on alternates alone, so this can too.
        if not self.reviewers and not self.alternates:
            raise ValueError(
                "Large-scale change: configuration required (no reviewers defined)"
            )

        # ScopeModel rejects this too, but its message wouldn't say where the
        # problem is.
        if reason := _roster_shortfall(
            reviewers=self.reviewers,
            alternates=self.alternates,
            require=self.require,
        ):
            raise ValueError(f"Large-scale change: {reason}")

        return ScopeModel(
            name=LARGE_SCALE_CHANGE_SCOPE_NAME,
            paths=["**/*"],
            reviewers=self.reviewers,
            alternates=self.alternates,
            require=self.require,
            request=self.request,
            labels=self.labels,
        )


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Nothing is technically required
    extends: list[str] = []
    template: bool = False
    aliases: dict[str, list[str]] = {}
    large_scale_change: LargeScaleChangeModel | None = None
    scopes: list[ScopeModel] = []

    @field_validator("scopes", mode="after")
    @classmethod
    def validate_unique_scope_names(cls, scopes: list[ScopeModel]) -> list[ScopeModel]:
        if dup := _first_case_insensitive_duplicate(scope.name for scope in scopes):
            raise ValueError(f"Duplicate scope name: {dup}")
        return scopes

    @field_validator("extends", mode="before")
    @classmethod
    def validate_extends(cls, extends: list[str]) -> list[str]:
        for i, path in enumerate(extends):
            basename = Path(path).name
            if not basename.startswith(CONFIG_FILENAME_PREFIX):
                raise ValueError(
                    f"Invalid extends path: {path}. It should start with '{CONFIG_FILENAME_PREFIX}'."
                )
        return extends

    def compiled_config(
        self,
        config_path: Path,
        other_configs: ConfigModels,
        teams: dict[str, list[str]] | None = None,
    ) -> ConfigModel:
        """
        Resolve `extends` and replace aliases, returning the effective config.

        Two phases: flatten the whole extends chain into one merged (raw,
        unexpanded) config, then expand aliases once. Expanding after the full
        merge is what makes transitive inheritance and cross-chain alias
        scoping work — an alias defined anywhere in the chain resolves anywhere.

        `teams` maps team refs (any case, without the leading `@`) to member
        usernames, and is only consulted for user-list fields (reviewers,
        alternates, authors, cc, large_scale_change.reviewers/alternates). Keys are
        lowercased here, so callers don't need to normalize case themselves.
        With `teams=None` (the default), `@org/team` references in those
        fields pass through unexpanded — the offline/CLI mode, since this
        library never calls out to GitHub/GitLab itself. That
        partially-resolved config is only sanctioned for offline use;
        anything that needs real reviewer usernames must pass a `teams`
        mapping.

        Pure function of the raw `self` and `other_configs` (it never reads its
        own anchored output), so it is safe to call uncached.
        """

        if teams is not None:
            teams = {key.lower(): members for key, members in teams.items()}

        compiled_data = self._merged_data(config_path, other_configs)

        # A large-scale change is reviewed as a scope, so it compiles by a
        # scope's rules.
        for scope in compiled_data["scopes"]:
            label = f"Scope '{scope['name']}'"
            _compile_review_fields(
                entry=scope,
                label=label,
                aliases=compiled_data["aliases"],
                teams=teams,
            )
            _validate_global_require(label=label, scope=scope)
        if large_scale_change := compiled_data.get("large_scale_change"):
            _compile_review_fields(
                entry=large_scale_change,
                label="large_scale_change",
                aliases=compiled_data["aliases"],
                teams=teams,
            )

        # Anchor each scope's paths at the directory tagged during flattening
        # (after alias expansion, so any `$path-alias` is resolved first). The
        # transient tag is popped so it never reaches the model.
        # Paths are relative to the config that owns the scope, `/` for
        # repo-root-absolute.
        for entry in compiled_data["scopes"]:
            anchor_dir = entry.pop("_anchor_dir", "")
            entry["paths"] = [_anchor_path(anchor_dir, p) for p in entry["paths"]]
            entry.pop("_declared_in", None)

        # The compiled config is the self-contained effective config: extends
        # are already merged in and aliases already expanded, so drop both. This
        # keeps stored results lean and makes the compiled form standalone (it
        # can never dangle on a missing extends target or re-expand differently).
        compiled_data["extends"] = []
        compiled_data["aliases"] = {}

        return ConfigModel.from_data(
            data=compiled_data,
            path=config_path,
        )

    def _merged_data(
        self,
        config_path: Path,
        other_configs: ConfigModels,
        _in_progress: list[str] | None = None,
        _seen: set[str] | None = None,
    ) -> dict[str, Any]:
        """
        Flatten the `extends` chain into one merged, *unexpanded* config dict.

        Parents are merged before this config (so a child can specialize), with
        aliases unioned child-wins and the large-scale-change config taken from
        the child if set else the first parent that defines one.

        `_in_progress` is the current ancestor path, used to detect circular
        extends. `_seen` is every config already merged into this flatten, used
        to merge a shared ancestor only once (diamond dedup).
        """
        if _in_progress is None:
            _in_progress = []
        if _seen is None:
            _seen = set()

        config_path_str = str(config_path)
        if config_path_str in _in_progress:
            cycle = _in_progress[_in_progress.index(config_path_str) :] + [
                config_path_str
            ]
            raise ValueError(
                f"Circular reference detected in extends: {' -> '.join(cycle)}"
            )
        _in_progress.append(config_path_str)

        inherited_scopes: list[dict[str, Any]] = []
        inherited_aliases: dict[str, list[str]] = {}
        inherited_lsc: dict[str, Any] | None = None

        for extend_path in self.extends:
            resolved_path = _resolve_extends_path(config_path_str, extend_path)
            if resolved_path not in other_configs:
                raise ValueError(
                    f"Config not found: '{extend_path}' (resolved to '{resolved_path}')"
                )
            if resolved_path in _seen:
                # Already merged via another branch (diamond) — skip the dup.
                continue

            parent_data = other_configs[resolved_path]._merged_data(
                Path(resolved_path), other_configs, _in_progress, _seen
            )
            inherited_scopes = inherited_scopes + parent_data["scopes"]
            inherited_aliases = inherited_aliases | parent_data["aliases"]
            inherited_lsc = inherited_lsc or parent_data["large_scale_change"]

        merged = self.model_dump()
        # Which file each scope is written in (see `declaring_config_path`).
        for entry in merged["scopes"]:
            entry["_declared_in"] = config_path_str
        merged["scopes"] = inherited_scopes + merged["scopes"]
        merged["aliases"] = inherited_aliases | merged["aliases"]
        merged["large_scale_change"] = merged["large_scale_change"] or inherited_lsc

        # Tag each scope with the directory its paths should anchor at. A scope's
        # paths are relative to the config that owns it, so the first
        # non-template config to consume a scope claims it: a non-template's own
        # scopes (and any it inherits from a template) anchor at its directory,
        # while a template defers to its consumer. `setdefault` means an
        # already-tagged scope (from a non-template ancestor) keeps its anchor.
        if not self.template:
            base_dir = posixpath.dirname(config_path_str)
            for entry in merged["scopes"]:
                entry.setdefault("_anchor_dir", base_dir)

        _seen.add(config_path_str)
        _in_progress.pop()

        return merged

    @classmethod
    def from_filesystem(cls, path: Path | str) -> ConfigModel:
        with open(path, "rb") as f:
            return cls.from_data(tomllib.load(f), path)

    @classmethod
    def from_content(cls, content: str, path: Path | str) -> ConfigModel:
        return cls.from_data(tomllib.loads(content), path)

    @classmethod
    def from_data(cls, data: dict[str, Any], path: Path | str) -> ConfigModel:
        return cls(**data)


class _ConfigModelsBase(RootModel):
    """Shared storage and accessors for a set of configs keyed by repo path."""

    root: dict[str, ConfigModel]

    @classmethod
    def from_config_models(cls, models: dict[str, ConfigModel]) -> Self:
        """Build from a dict of already-constructed configs keyed by path."""
        configs = cls(root={})
        for path, config_model in models.items():
            configs.root[str(Path(path))] = config_model
        return configs

    def get_config_models(self) -> dict[str, ConfigModel]:
        return dict(self.root.items())

    def __bool__(self) -> bool:
        return bool(self.root)

    def __getitem__(self, key: str) -> ConfigModel:
        return self.root[key]

    def __contains__(self, key: str) -> bool:
        return key in self.root

    def __len__(self) -> int:
        return len(self.root)

    def closest_config_path(self, file_path: Path) -> str | None:
        """The path of the closest non-template config governing this file,
        or None when nothing governs it."""
        for parent in file_path.parents:
            parent_config_path = str(parent / CONFIG_FILENAME)
            config = self.root.get(parent_config_path)
            if config is not None and not config.template:
                return parent_config_path
        return None


class ConfigModels(_ConfigModelsBase):
    """Configs exactly as loaded from the repo — extends unresolved, aliases
    unexpanded, paths unanchored. Build the set up, then call `compiled()`."""

    def declared_check_names(self) -> set[str]:
        """Every check-run name an effective (non-template) scope's `unless`
        references, across the whole config set.

        Collected from an offline compile (`teams=None`, the `team_refs`
        precedent) so a template's refs count only where a consumer actually
        inherits them -- an unconsumed template must not make every pull
        request fetch (or error on) checks that nothing evaluates. `unless`
        refs are literal strings (aliases and teams never expand inside
        them), so the offline compile is exact. Empty for the common case (no
        `unless` anywhere), which is what lets the processor skip fetching
        check runs entirely.
        """
        return {
            name
            for config in self.compiled().root.values()
            if not config.template
            for scope in config.scopes
            for _, name in scope.unless_refs()
        }

    @classmethod
    def from_configs_data(cls, data: dict[str, Any]) -> ConfigModels:
        """Load configs from a dict of parsed config data keyed by path."""
        configs = cls(root={})

        for path, config_data in data.items():
            config = ConfigModel.from_data(config_data, Path(path))
            configs.add_config(config, Path(path))

        return configs

    @classmethod
    def from_contents(cls, contents: dict[str, str]) -> ConfigModels:
        """Load configs from a dict of raw TOML content keyed by path."""
        configs = cls(root={})

        for path, content in contents.items():
            configs.add_config(ConfigModel.from_content(content, path), Path(path))

        return configs

    def add_config(self, config: ConfigModel, path: Path) -> None:
        self.root[str(path)] = config

    def declaring_config_path(self, *, config_path: str, scope_name: str) -> str | None:
        """The config in `config_path`'s extends chain that declares a scope,
        or None when nothing in the chain does."""
        merged = self.root[config_path]._merged_data(Path(config_path), self)
        for entry in merged["scopes"]:
            if entry["name"] == scope_name:
                return entry["_declared_in"]
        return None

    def team_refs(self) -> set[str]:
        """Collect every team ref (lowercase, no leading `@`/`!`) that
        `compiled(teams=...)` would actually try to expand: refs written
        directly in a user-list field (scopes' `USER_LIST_FIELDS` and
        `large_scale_change.reviewers`/`alternates`), plus any refs reachable from those
        fields through `$alias`/`!$alias` chains.

        Meant for callers that need to know which teams to fetch/sync before
        calling `compiled(teams=...)`.

        Implemented as an offline compile (`teams=None`): aliases expand but
        team refs pass through unexpanded, so whatever refs remain in the
        compiled user-list fields are — by construction — exactly the refs a
        real compile will try to expand. A ref that only appears in a
        non-user-list field (e.g. an npm-style `@vendor/pkg/**` in `paths`)
        or inside an alias nothing references never survives into a compiled
        user-list field, so it is never collected. Raises the same config
        errors `compiled()` would (unknown alias, circular refs, ...), just
        earlier.
        """
        # Cheap pre-check: a team ref can only enter a compile as a literal
        # `@`/`!@` value in a user-list field or an alias value. Most repos
        # have none, and skipping the compile keeps this near-free for them.
        candidate_lists: list[list[str]] = []
        for config in self.root.values():
            candidate_lists.extend(config.aliases.values())
            for scope in config.scopes:
                for field in USER_LIST_FIELDS:
                    candidate_lists.append(getattr(scope, field))
            if config.large_scale_change:
                candidate_lists.append(config.large_scale_change.reviewers)
                candidate_lists.append(config.large_scale_change.alternates)
        if not any(
            _split_team_ref(value) is not None
            for values in candidate_lists
            for value in values
        ):
            return set()

        refs: set[str] = set()

        def collect_refs(values: list[str]) -> None:
            for value in values:
                if (split := _split_team_ref(value)) is not None:
                    refs.add(split[1].lower())

        for config in self.compiled(teams=None).get_config_models().values():
            if config.template:
                continue
            for scope in config.scopes:
                for field in USER_LIST_FIELDS:
                    collect_refs(getattr(scope, field))
            if config.large_scale_change:
                collect_refs(config.large_scale_change.reviewers)
                collect_refs(config.large_scale_change.alternates)

        return refs

    def compiled(
        self, teams: dict[str, list[str]] | None = None
    ) -> CompiledConfigModels:
        """Resolve the whole set into its effective, PR-independent form.

        Each non-template config is compiled once — extends merged, aliases
        expanded, paths anchored. Templates are NOT compiled standalone: a
        template scope may reference an alias the consuming config provides, and
        its paths anchor at the consumer. They are carried through untouched
        (folded into each consumer during that consumer's compile, and kept in
        the set for display).

        `teams` maps team refs (any case, without the leading `@`) to member
        usernames; passed straight through to each config's `compiled_config`
        (see there for case normalization and the `teams=None` vs provided
        semantics).

        The result is an immutable `CompiledConfigModels` — there is no way to
        compile it again, so the non-idempotent path anchoring can never
        double-apply.
        """
        effective: dict[str, ConfigModel] = {}
        for path, config in self.root.items():
            if config.template:
                effective[path] = config
            else:
                effective[path] = config.compiled_config(
                    config_path=Path(path), other_configs=self, teams=teams
                )

        return CompiledConfigModels.from_config_models(effective)


class CompiledConfigModels(_ConfigModelsBase):
    """The effective configs used for matching: every non-template config is
    fully resolved. Produced by `ConfigModels.compiled()`; never recompiled."""

    def closest_config(self, file_path: Path) -> ConfigModel:
        """Return the closest non-template config governing this file."""
        config_path = self.closest_config_path(file_path)
        if config_path is None:
            raise ValueError(f"No config found for {file_path}")
        return self.root[config_path]

    def get_default_large_scale_change(self) -> LargeScaleChangeModel:
        """The primary (repo-root) config's large-scale-change section, if any.

        The primary was compiled by `compiled()`, so its reviewers/labels are
        already alias-expanded (e.g. ["$backend"] -> usernames). A `template =
        true` repo root is a misconfiguration (templates are meant to be
        extended, not be the primary); it is passed through uncompiled, so its
        LSC would read with aliases unexpanded.
        """
        if CONFIG_FILENAME in self.root and (
            lsc := self.root[CONFIG_FILENAME].large_scale_change
        ):
            return lsc

        return LargeScaleChangeModel()

    def filter_for_pullrequest(self, author_username: str) -> CompiledConfigModels:
        """
        Overlay PR-dependent scope gating: drop scopes that author rules disable
        for this pull request.

        This is the only PR-dependent step. The configs are already compiled, so
        each config's scopes are self-contained and dropping one is a plain list
        filter — no re-inheritance. Templates are passed through (they are never
        matched directly; their scopes already live in each consumer).
        """
        effective: dict[str, ConfigModel] = {}
        for config_path, config in self.root.items():
            if config.template:
                # Templates are never matched directly; pass them through.
                effective[config_path] = config
                continue

            kept_scopes = [
                scope
                for scope in config.scopes
                if scope.matches_author(author_username)
            ]
            effective[config_path] = config.model_copy(update={"scopes": kept_scopes})

        return CompiledConfigModels.from_config_models(effective)
