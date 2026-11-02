from __future__ import annotations

import hashlib
import json
from collections.abc import Generator, Iterator
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .config import (
    CompiledConfigModels,
    ConfigModel,
    LargeScaleChangeModel,
    ScopeModel,
)
from .diff import DiffCode, DiffFile, iterate_diff_parts
from .exceptions import LargeScaleChangeException


def match_path(
    *, path: Path, config: ConfigModel
) -> tuple[ScopePathMatch, list[ScopeModel]]:
    path_match = ScopePathMatch(path=str(path), scopes=[])

    scopes_matching_paths = [
        scope for scope in config.scopes if scope.matches_path(path)
    ]
    code_scopes = [scope for scope in scopes_matching_paths if scope.code]
    path_scopes = [scope for scope in scopes_matching_paths if not scope.code]

    # Set the scopes on the path itself
    for scope in path_scopes:
        path_match.add_scope(scope)

    return path_match, code_scopes


def match_code(
    *, path: str, code: str, scopes: list[ScopeModel], line_offset: int = 0
) -> Generator[ScopeCodeMatch]:
    code_matches: dict[str, ScopeCodeMatch] = {}

    for scope in scopes:
        for match in scope.matches_code(code):
            code_match = ScopeCodeMatch(
                path=path,
                start_line=line_offset + match["start_line"],
                end_line=line_offset + match["end_line"],
                start_column=match["start_col"],
                end_column=match["end_col"],
                scopes=[scope.name],
                location_id="",
            )
            code_match._scopes = [scope]

            if code_match.location_id in code_matches:
                # Just add the scopes to it
                code_matches[code_match.location_id].add_scope(scope)
            else:
                code_matches[code_match.location_id] = code_match

    yield from code_matches.values()


def match_files(configs: CompiledConfigModels, files: Iterator[str]) -> ChangeMatches:
    def _iterate() -> Generator[ScopePathMatch | ScopeCodeMatch]:
        for f in files:
            file_path = Path(f)

            config = configs.closest_config(file_path)

            path_match, code_scopes = match_path(
                path=file_path,
                config=config,
            )

            # Yield the paths first
            yield path_match

            # Then go line by line to find scopes that match lines
            if code_scopes:
                try:
                    code = file_path.read_text()
                    yield from match_code(
                        path=str(file_path),
                        code=code,
                        scopes=code_scopes,
                    )
                except UnicodeDecodeError:
                    # Skip binary files that can't be decoded as text
                    pass
                except FileNotFoundError:
                    # Deleted in the working tree, so there's no code left to
                    # match (a diff still has its removed lines)
                    pass

    return ChangeMatches.from_config_matches(configs, _iterate())


def iterate_diff(
    configs: CompiledConfigModels, diff: Iterator[str] | str
) -> Generator[tuple[DiffFile | DiffCode, list[ScopePathMatch | ScopeCodeMatch]]]:
    # We can still iterate a diff without configs, just by yield the diff objs
    if not configs:
        for diff_obj in iterate_diff_parts(diff):
            yield diff_obj, []

        return

    # Keep track of these as we go and jump between file header
    # and raw code during iteration
    check_code_scopes: list[ScopeModel] = []
    current_code_path = None

    current_code_diffs = []

    # TODO get root config here, check diff size as we go and raise exception?
    # or we need to keep track per LSC? should be a compiled value...

    def yield_code_diffs() -> Generator[
        tuple[DiffCode, list[ScopePathMatch | ScopeCodeMatch]]
    ]:
        # We're passing the entire diff chunk to see if there's a match inside,
        # but if there is, it probably won't match EVERY line in the chunk
        assert current_code_path is not None, "current_code_path must be set"
        current_code_chunk = "\n".join([code.raw() for code in current_code_diffs])
        current_code_line_number = current_code_diffs[0].line_number - 1

        code_matches = match_code(
            path=current_code_path,
            code=current_code_chunk,
            scopes=check_code_scopes,
            line_offset=current_code_line_number,
        )
        code_matches = list(code_matches)

        for diff_line_index, diff_code in enumerate(current_code_diffs):
            subcode_matches: list[ScopePathMatch | ScopeCodeMatch] = [
                code_match
                for code_match in code_matches
                if code_match.start_line
                <= (current_code_line_number + diff_line_index + 1)
                <= code_match.end_line
            ]
            yield diff_code, subcode_matches

    for diff_obj in iterate_diff_parts(diff):
        if isinstance(diff_obj, DiffFile):
            # Yield a code chunk if we finished one
            if current_code_diffs:
                yield from yield_code_diffs()

            current_code_path = None
            current_code_diffs = []

            diff_file = diff_obj
            file_path = Path(diff_file.new_path)
            config = configs.closest_config(file_path)

            path_match, code_scopes = match_path(
                path=file_path,
                config=config,
            )

            current_code_path = str(file_path)
            check_code_scopes = code_scopes

            yield diff_obj, [path_match]
        elif isinstance(diff_obj, DiffCode):
            if check_code_scopes:
                # It will be yielded later
                current_code_diffs.append(diff_obj)
            else:
                # Skip all code lines if we don't care about code
                yield diff_obj, []

    # Yield the last code chunk we saw
    if current_code_diffs:
        yield from yield_code_diffs()


def match_diff(configs: CompiledConfigModels, diff: Iterator[str] | str) -> DiffResults:
    config_paths_modified: set[str] = set()
    changed_paths: set[str] = set()
    additions = 0
    deletions = 0

    def iterate() -> Generator[ScopePathMatch | ScopeCodeMatch]:
        nonlocal additions, deletions
        for diff_obj, matches in iterate_diff(configs, diff):
            # Track additions/deletions during existing iteration
            if isinstance(diff_obj, DiffCode):
                if diff_obj.is_addition():
                    additions += 1
                elif diff_obj.is_deletion():
                    deletions += 1

            if isinstance(diff_obj, DiffFile):
                changed_paths.add(diff_obj.new_path)
                if diff_obj.new_path in configs:
                    config_paths_modified.add(diff_obj.new_path)
                if diff_obj.old_path in configs:
                    config_paths_modified.add(diff_obj.old_path)

            yield from matches

    try:
        return DiffResults(
            matches=ChangeMatches.from_config_matches(configs, iterate()),
            config_paths_modified=list(config_paths_modified),
            changed_paths=sorted(changed_paths),
            additions=additions,
            deletions=deletions,
        )
    except LargeScaleChangeException:
        # Get the large scale change config from CODEREVIEW.toml
        lsc = configs.get_default_large_scale_change()

        return DiffResults(
            matches=ChangeMatches.from_large_scale_change(
                configs=configs,
                large_scale_change=lsc,
            ),
            config_paths_modified=list(config_paths_modified),
            additions=additions,
            deletions=deletions,
        )


class DiffResults(BaseModel):
    """Results from analyzing a diff against configs."""

    model_config = ConfigDict(extra="forbid")

    matches: ChangeMatches
    config_paths_modified: list[str] = Field(default_factory=list)
    # Every file the diff touched. What a result depends on, config-wise, is
    # the compiled config governing each of these; empty for a large-scale
    # change, whose verdict comes from the root config alone and whose
    # iteration stopped at the threshold.
    changed_paths: list[str] = Field(default_factory=list)
    additions: int = 0
    deletions: int = 0


class ChangeMatches(BaseModel):
    """
    The matches for a given diff or set of files.

    This knows nothing about a pull request (branches, commits, etc.)
    """

    model_config = ConfigDict(extra="forbid")

    # Instead we could do
    # - scopes
    #  - config
    #  - paths
    #    - code
    # could add points, reviewers, etc to this
    # but then we're mixing concerns... looking at raw files will just have empty values?

    # Three modes are:
    # - raw files
    # - raw diff
    # - pull request (has reviews)

    configs: dict[str, ConfigModel] = {}

    # The matching LSC, if there is one.
    large_scale_change: LargeScaleChangeModel | None = None

    # All scopes found in the results
    scopes: dict[str, ScopeModel] = {}

    # All evaluated paths
    paths: dict[str, ScopePathMatch] = {}

    # All code matches
    code: dict[str, ScopeCodeMatch] = {}

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump()

    def __bool__(self) -> bool:
        return bool(self.scopes)

    @classmethod
    def from_config_matches(
        cls,
        configs: CompiledConfigModels,
        matches: Iterator[ScopePathMatch | ScopeCodeMatch],
    ) -> ChangeMatches:
        scopes: dict[str, ScopeModel] = {}
        paths: dict[str, ScopePathMatch] = {}
        code: dict[str, ScopeCodeMatch] = {}

        # Where each scope sits in the configs: which config it came from,
        # then its position in that config's scope list. Keyed by object
        # identity, not by name. Two configs may declare the same scope name,
        # and a name key would give one of them the other's position. The
        # matched scopes are the same ScopeModel instances these configs hold,
        # so identity is exact.
        #
        # The `scopes` dict below is keyed by name and so still collapses
        # duplicate names across configs. That is pre-existing; ordering by
        # identity keeps whichever scope survives that collapse in its own
        # declared position rather than making it worse.
        declaration_order = {
            id(scope): (config_index, scope_index)
            for config_index, config in enumerate(configs.root.values())
            for scope_index, scope in enumerate(config.scopes)
        }

        for match in matches:
            # Store seen scopes as we go from all matches
            for scope in match._scopes:
                scopes[scope.name] = scope

            if isinstance(match, ScopePathMatch):
                if not match._scopes:
                    # Right now we don't care about storing anything that doesn't have scopes.
                    # This prevents an unnecessarily huge dump on big repos or PRs.
                    continue

                paths[match.path] = match

            elif isinstance(match, ScopeCodeMatch):
                code_location_id = match.location_id

                # Store it in the code results
                code[code_location_id] = match

            else:
                raise TypeError(f"Unknown match type: {match}")

        # Sort into declaration order. Without this, the order is whichever
        # scope the first changed file matched, which is a property of the
        # diff rather than the configs. Consumers that walk scopes in sequence
        # need declaration order: review requesting counts what the scopes
        # before this one already asked for, so the order decides who gets
        # asked. A scope missing from the map sorts last and keeps its
        # position; the match came from these configs, so this cannot
        # normally happen.
        ordered_scopes = {
            name: scopes[name]
            for name in sorted(
                scopes,
                key=lambda name: declaration_order.get(
                    id(scopes[name]), (len(configs.root), 0)
                ),
            )
        }

        return cls(
            large_scale_change=None,
            scopes=ordered_scopes,
            paths=paths,
            code=code,
            # These are the compiled, effective configs (extends merged, aliases
            # expanded, paths anchored, PR-disabled scopes dropped) — i.e. what
            # actually applied to this diff.
            configs=configs.get_config_models(),
        )

    @classmethod
    def from_large_scale_change(
        cls,
        configs: CompiledConfigModels,
        large_scale_change: LargeScaleChangeModel,
    ) -> ChangeMatches:
        return cls(
            configs=configs.get_config_models(),
            large_scale_change=large_scale_change,
            scopes={},
            paths={},
            code={},
        )


class ScopePathMatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1)
    scopes: list[str]  # Field(min_length=1)
    # code: list[str] = []

    # Store this internally during processing (full reference of scope models)
    _scopes: list[ScopeModel] = []

    def add_scope(self, scope: ScopeModel) -> None:
        if not scope.ownership:
            # Remove any other scopes that don't have special ownership rules
            # (i.e. we only want one primary scope in the end)
            self._scopes = [s for s in self._scopes if s.ownership]

        self._scopes.append(scope)

        self.scopes = [s.name for s in self._scopes]


class ScopeCodeMatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # In a diff match, we could see both sides of the diff, i.e. repeated lines if the before and after both match...
    path: str = Field(min_length=1)
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    scopes: list[str]  # Field(min_length=1)
    location_id: str

    # Store this internally during processing (full reference of scope models)
    _scopes: list[ScopeModel] = []

    def printed_location(self) -> str:
        if self.start_line == self.end_line:
            return f"Ln {self.start_line}, Col {self.start_column}-{self.end_column}"
        else:
            return f"Ln {self.start_line}-{self.end_line}"

    def add_scope(self, scope: ScopeModel) -> None:
        if not scope.ownership:
            # Remove any other scopes that don't have special ownership rules
            # (i.e. we only want one primary scope in the end)
            self._scopes = [s for s in self._scopes if s.ownership]

        self._scopes.append(scope)

        self.scopes = [s.name for s in self._scopes]

    @model_validator(mode="after")
    def compute_location_id(self) -> ScopeCodeMatch:
        # only compute if the caller didn't provide one
        if not self.location_id:
            loc = {
                "path": self.path,
                "start_line": self.start_line,
                "end_line": self.end_line,
                "start_column": self.start_column,
                "end_column": self.end_column,
            }
            raw = json.dumps(loc, sort_keys=True, separators=(",", ":")).encode()
            self.location_id = hashlib.md5(raw).hexdigest()
        return self


# how to store what was reviewed? ideally we could be fine-grained, at some point
# so we need to know who, which scopes, which paths, which codes (location hash) then we can cross reference everything?
