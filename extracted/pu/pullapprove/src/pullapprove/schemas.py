"""
JSON shapes for matches, shared by `pullapprove match --json` and the
PullApprove API.

These describe the match layer: which scopes, paths and code a set of
files or a diff matched, before any reviews are counted. The API's
per-PR results wrap these same shapes with a status, so the keys (scope
name, path, code location_id) line up between the two.
"""

from __future__ import annotations

from typing import TypedDict

from .config import ScopeModel
from .matches import ChangeMatches, ScopeCodeMatch, ScopePathMatch


class ScopeSchema(TypedDict):
    """The scope config behind a match."""

    name: str
    description: str
    ownership: str
    require: int
    reviewers: list[str]
    alternates: list[str]
    paths: list[str]
    code: list[str]
    checklist: bool


class PathMatchSchema(TypedDict):
    path: str
    scopes: list[str]


class CodeMatchSchema(TypedDict):
    path: str
    scopes: list[str]
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    location_id: str


class MatchesSchema(TypedDict):
    scopes: dict[str, ScopeSchema]
    paths: dict[str, PathMatchSchema]
    code: dict[str, CodeMatchSchema]


def scope_schema(scope: ScopeModel) -> ScopeSchema:
    return {
        "name": scope.name,
        "description": scope.description,
        "ownership": str(scope.ownership),
        "require": scope.require,
        "reviewers": scope.reviewers,
        "alternates": scope.alternates,
        "paths": scope.paths,
        "code": scope.code,
        "checklist": scope.checklist is not None,
    }


def path_match_schema(path_match: ScopePathMatch) -> PathMatchSchema:
    return {
        "path": path_match.path,
        "scopes": path_match.scopes,
    }


def code_match_schema(code_match: ScopeCodeMatch) -> CodeMatchSchema:
    return {
        "path": code_match.path,
        "scopes": code_match.scopes,
        "start_line": code_match.start_line,
        "end_line": code_match.end_line,
        "start_column": code_match.start_column,
        "end_column": code_match.end_column,
        "location_id": code_match.location_id,
    }


def matches_schema(*, matches: ChangeMatches, all_paths: list[str]) -> MatchesSchema:
    """Everything a set of files or a diff matched.

    `all_paths` is every file that was looked at, so files no scope owns
    show up in `paths` with empty `scopes`.
    """
    paths: dict[str, PathMatchSchema] = {}
    for path in sorted(all_paths):
        if path in matches.paths:
            path_match = matches.paths[path]
        else:
            # Matches only keep the paths some scope owns
            path_match = ScopePathMatch(path=path, scopes=[])
        paths[path] = path_match_schema(path_match)

    code_matches = sorted(
        matches.code.values(),
        key=lambda c: (c.path, c.start_line, c.start_column),
    )
    code: dict[str, CodeMatchSchema] = {}
    for code_match in code_matches:
        code[code_match.location_id] = code_match_schema(code_match)

    scopes: dict[str, ScopeSchema] = {}
    for scope in matches.scopes.values():
        scopes[scope.name] = scope_schema(scope)

    return {
        "scopes": scopes,
        "paths": paths,
        "code": code,
    }
