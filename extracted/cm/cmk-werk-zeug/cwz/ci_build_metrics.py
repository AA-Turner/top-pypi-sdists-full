#!/usr/bin/env python3

"""ci-build-metrics - Fetch and extract insights from finished CI build info
and generate queryable details
"""

import asyncio
import gzip
import hashlib
import inspect
import json
import logging
import multiprocessing
import re
from argparse import ArgumentParser
from argparse import Namespace as Args
from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
    Set,
)
from contextlib import contextmanager, suppress
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, NewType, TextIO, cast

import yaml
from cwz.jenkins_utils.client import (
    AugmentedJenkinsClient,
    Build,
    BuildStages,
    Cause,
    JobResult,
    StageInfo,
    apply_common_jenkins_cli_args,
    extract_credentials,
)
from pydantic import BaseModel, ConfigDict, ValidationError, model_validator  # noqa: F401
from rich import print as rich_print
from rich import traceback
from rich.console import Console
from trickkiste.logging_helper import apply_common_logging_cli_args, setup_logging
from trickkiste.misc import date_from, date_str, parse_age  # ,dur_str

CACHE_PATH = Path("~").expanduser() / ".cache" / "ci_metrics"
BUILD_LOG_FILENAME = "build_log.txt"
BUILD_INFO_FILENAME = "build_info.json"
BUILD_STAGES_FILENAME = "build_stages.json"
DIGEST_FILENAME = "digest.json"
INDEX_FILENAME = "index.json"
KNOWN_ISSUES_FILENAME = "known_issues.yaml"
REPORT_FILENAME = "report.json"
FAILED_BUILDS_FILENAME = "failed-builds.ods"
# note: `/cv/` is explicitly not excluded here since this tool is not Sauron but
#       about identifying CI issues, which are relevant in /cv/, too
SHERIFF_FILTER = "^(Testing/|qa-kpis/|docs.checkmk.com/|cma/|docs/)"
DB_ENGINE_STRING = (
    # "postgresql+psycopg2://ci_build_metrics:ci_build_metrics@localhost:5432/ci_build_metrics"
    "postgresql+psycopg2://ci_user:ci_pw@localhost:5432/ci_build_metrics_db"
)
BUILD_RESULT_COLOR = {
    "FAILURE": "bold red",
    "SUCCESS": "green",
    "ABORTED": "gray",
    "UNSTABLE": "bold yellow",
}

PatternHash = NewType("PatternHash", str)
Matchings = Mapping[PatternHash, Sequence[tuple[int, str]]]
MutableMatchings = MutableMapping[PatternHash, MutableSequence[tuple[int, str]]]


def parse_arguments() -> Args:
    """parse command line arguments and return argument object"""
    parser = ArgumentParser("ci-metrics")

    apply_common_logging_cli_args(parser)
    apply_common_jenkins_cli_args(parser)

    parser.set_defaults(func=lambda *_: parser.print_usage())
    parser.add_argument(  # fixme: currently used for printing only
        "--jenkins-url", type=str, default="https://ci.lan.tribe29.com"
    )
    parser.add_argument("--base-dir", type=lambda p: Path(p).expanduser(), default=CACHE_PATH)
    parser.add_argument(
        "--builds-dir", type=lambda p: Path(p).expanduser(), default=CACHE_PATH / "builds"
    )
    parser.add_argument("--max-processes", type=int, default=10)  # fixme: get actual numbers
    parser.add_argument("--max-results", type=int)
    parser.add_argument(
        "--known-issues-file",
        type=lambda p: Path(p).expanduser(),
        default=Path(__file__).parent.parent / KNOWN_ISSUES_FILENAME,
    )
    parser.add_argument(
        "--report-file",
        type=lambda p: Path(p).expanduser(),
        default=REPORT_FILENAME,
    )
    parser.add_argument(
        "--failed-builds-file",
        type=lambda p: Path(p).expanduser(),
        default=FAILED_BUILDS_FILENAME,
    )

    def add_common_args(subparser: ArgumentParser) -> None:
        """Arguments we want to have for all sub-parsers for consistency and easy propagation
        in fn_updte(). Note that not all arguments are used by every function"""
        subparser.add_argument("-v", "--verbose", action="store_true")
        subparser.add_argument("--markdown", action="store_true")
        subparser.add_argument("--date-from", type=str)
        subparser.add_argument("--date-to", type=str)
        subparser.add_argument("--rebuild", action="store_true")
        subparser.add_argument("--refresh", action="store_true")
        subparser.add_argument("--include", type=str)
        subparser.add_argument("--exclude", type=str, default=SHERIFF_FILTER)

    subparsers = parser.add_subparsers(
        help="available commands",
        metavar="CMD",
        required=True,
    )
    parser_fetch = subparsers.add_parser(
        "fetch",
        aliases=["f"],
        help="Fetch build info of completed builds and store them locally",
    )
    parser_fetch.set_defaults(func=_fn_fetch)
    add_common_args(parser_fetch)

    parser_create_digests = subparsers.add_parser(
        "create-digests",
        aliases=["d"],
        help="Store critical data about (mostly failed) builds in a digest file",
    )
    parser_create_digests.set_defaults(func=_fn_create_digests)
    add_common_args(parser_create_digests)
    parser_create_digests.add_argument("builds", type=str, nargs="*")

    parser_index = subparsers.add_parser(
        "index",
        help="Create an index data set for the infos we need for fast querying",
    )
    parser_index.set_defaults(func=_fn_create_index)
    add_common_args(parser_index)

    parser_fuse = subparsers.add_parser(
        "fuse",
        help="Enrich digests with information gathered from other digests",
    )
    parser_fuse.set_defaults(func=_fn_fuse)
    add_common_args(parser_fuse)

    parser_export = subparsers.add_parser(
        "export",
        aliases=["e"],
        help="Export all data to a Postgres DB",
    )
    parser_export.set_defaults(func=_fn_export)
    add_common_args(parser_export)

    parser_update = subparsers.add_parser(
        "update",
        help="Combines fetch, create-digests and index for convenience",
    )
    parser_update.set_defaults(func=_fn_update)
    add_common_args(parser_update)

    parser_issue_figures = subparsers.add_parser(
        "issue-figures",
        help="Show some numbers about usage of each issue",
    )
    parser_issue_figures.set_defaults(func=_fn_issue_figures)
    add_common_args(parser_issue_figures)
    parser_issue_figures.add_argument(
        "--regex-filter", type=str, help="sub-string each regex must contain"
    )

    parser_info = subparsers.add_parser(
        "info",
        aliases=["i"],
        help="Show information about a build",
    )
    parser_info.set_defaults(func=_fn_info)
    parser_info.add_argument("builds", type=str, nargs="+")

    parser_report = subparsers.add_parser(
        "report",
        help="Create an experimental report",
    )
    parser_report.set_defaults(func=_fn_report)
    add_common_args(parser_report)
    parser_report.add_argument("--match-count", type=str, help="'0', '>=', '>', '1'")
    parser_report.add_argument("--sort-by", type=str)
    parser_report.add_argument("--result", type=str, default="~success")
    parser_report.add_argument("--regex-filter", type=str, help="string regex must contain")
    parser_report.add_argument("--print-totals-only", action="store_true")

    # parser_report.add_argument("--node", type=str)
    # parser_report.add_argument("--show-graph", action="store_true")

    parser_spreadsheet = subparsers.add_parser(
        "spreadsheet",
        help="Create ODF document from report file",
    )
    parser_spreadsheet.set_defaults(func=_fn_spreadsheet)
    add_common_args(parser_spreadsheet)

    return parser.parse_args()


def log() -> logging.Logger:
    """Convenience function retrieves 'our' logger"""
    return logging.getLogger("trickkiste.ci-metrics")


class Issue(BaseModel):
    """This is what's being taken from known_issues.yaml"""

    regex: str  # fixme: should be a list
    dismiss: int = 1  # 0: ignore, 1: normal, 2: dont list as unused
    category: None | str = None
    family: None | str = None
    ticket: None | str = None  # fixme: should be a list
    comment: None | str = None


class FinishedBuildDigest(BaseModel):
    """This is what's being written to the DB"""

    # Don't allow None as valid value - later it will be checked in order
    # to decide whether or not to update the digest

    model_config = ConfigDict(extra="forbid")

    # combination of job_path / number
    build_id: str
    number: int

    result: JobResult  # | None

    timestamp: int
    duration_total_sec: int
    duration_queue_sec: int
    duration_execution_sec: int  # | None = None
    first_timestamp: int  # | None = None

    stages: Sequence[StageInfo]  # | None = None

    without_build_log: bool  # | None = None

    commit_id: str
    # is_cv_build: bool
    console_log_line_count: int
    console_log_bytes_count: int  # | None = None
    parameters: Mapping[str, str | bool]

    # 'child' builds - incomplete as taken from the logs
    upstream_builds_extracted: Sequence[str]

    # 'child' builds - populated by _fn_fuse, using other builds
    upstream_builds_inferred: Sequence[str] = []

    # 'parent' builds
    # this is ambigeous - builds might be startet by an upstream build
    # but later used by another one, which will be affected, too.
    downstream_builds: Sequence[str]  # | None = None
    causes: Sequence[str]  # | None = None

    # issues: list[Issue]
    fail_causes: Matchings  # | None = None

    build_node: str  # | None = None
    # artifacts

    @property
    def duration_wait_total_sec(self) -> int:
        return (self.first_timestamp or self.timestamp) - self.timestamp

    def is_direct_production(self) -> bool:
        """Returns whether or not a build is a 'production' build, i.e.
        'should not fail' (in contrast to CV builds which are made to fail)
        """
        return (
            not self.build_id.startswith("Testing")
            and (
                any(
                    c.startswith(p)
                    for p in (
                        "Started by timer",
                        "Started by an SCM change",
                    )
                    for c in self.causes
                )
                or self.parameters.get("GERRIT_EVENT_TYPE") == "change-merged"
                or not any(
                    s in self.build_id
                    for s in (
                        "/cv/",
                        "/change_validation/",
                        "gerrit",
                        "Gerrit",
                        "/builders/",
                        "winagt-",
                    )
                )
            )
            and not self.is_direct_cv()
        )

    def is_direct_cv(self) -> bool:
        return self.parameters.get("GERRIT_EVENT_TYPE") in {
            "comment-added",
            "patchset-created",
        } and not any(c.startswith("Replayed #") for c in self.causes)

    def upstream_builds(self) -> Sequence[str]:
        return sorted(set((*self.upstream_builds_extracted, *self.upstream_builds_inferred)))

    @model_validator(mode="before")
    @classmethod
    def correct_node(cls, obj):  # type: ignore[no-untyped-def]
        """Refactor init to match our expectations"""
        if "time_in_queue_sec" in obj:
            obj["duration_queue_sec"] = obj["time_in_queue_sec"]
            del obj["time_in_queue_sec"]
        if "duration_sec" in obj:
            obj["duration_total_sec"] = obj["duration_sec"]
            del obj["duration_sec"]
        if "matches" in obj:
            obj["fail_causes"] = obj["matches"]
            del obj["matches"]
        if "upstream_builds" in obj:
            obj["upstream_builds_extracted"] = obj["upstream_builds"]
            del obj["upstream_builds"]
        if "path" in obj:
            obj["build_id"] = obj["path"]
            del obj["path"]
        if "is_cv_build" in obj:
            del obj["is_cv_build"]
        return obj


class MatchMaker:
    """Fixme This maps a path and a pattern to a list of lines of matches"""

    def __init__(self, known_issues_path: Path) -> None:
        log().debug("load known issues table from %s..", known_issues_path)
        self._known_issues = {
            self.str_hash(item.regex): item
            for item in map(
                Issue.model_validate, load_file(known_issues_path, cast(list[dict[str, Any]], []))
            )
        }

    def keys(self) -> Set[PatternHash]:
        return self._known_issues.keys()

    def active_issues(
        self, matches: Matchings, filter_regexes: None | Set[PatternHash] = None
    ) -> Matchings:
        """Returns pattern-hashes for regexes in @matches which findings are not empty
        and which are currently referenced in known issues"""
        return {
            regex_hash: lines
            for regex_hash, lines in matches.items()
            if not filter_regexes or regex_hash in filter_regexes
            if lines and regex_hash in self.keys()
        }

    def resolve(self, regex_hash: PatternHash) -> str:
        return self._known_issues[regex_hash].regex

    def get(self, regex_hash: PatternHash) -> None | Issue:
        with suppress(KeyError):
            return self._known_issues[regex_hash]
        return None

    def regexes_containting(self, string: None | str) -> None | Set[PatternHash]:
        return (
            set(
                regex_hash
                for regex_hash, issue in self._known_issues.items()
                if string in issue.regex
            )
            if string
            else None
        )

    def __call__(self, lines: list[str], matches: Matchings) -> Matchings:
        """Returns lines of occurrence for each known regular expression from know_issues"""
        return {
            **matches,
            **{
                regex_hash: (
                    existing_match
                    if existing_match is not None
                    else [
                        (i, line.strip())
                        for i, line in enumerate(lines)
                        if re.search(issue.regex, line)  # fixme: compiled regex?
                    ]
                )
                for regex_hash, issue in self._known_issues.items()
                for existing_match in (matches.get(regex_hash),)
            },
        }

    def str_hash(self, string: str) -> PatternHash:
        return PatternHash(hashlib.blake2b(string.encode(), digest_size=3).hexdigest())


class BuildIndex:
    """Lookup container for fast querying - holds only redundant data we need to avoid reading
    all digests.
    Updated via `index` subcommand"""

    class IndexElement(BaseModel):
        """Smalll subset of FinishedBuildDigest used for fast lookup.
        Don't store too much in here: if the index file becomes too large, loading it becomes
        slow than just reading the digest files"""

        result: JobResult
        timestamp: int
        match_count: int  # fixme: should be Sequence[str]?

    def __init__(self, base_dir: Path, builds_dir: Path) -> None:
        self._index_file_path = base_dir / INDEX_FILENAME
        self._builds_dir = builds_dir
        log().debug("read cached build digests from %s..", self._index_file_path)
        self._index_store = {
            key: BuildIndex.IndexElement(**value)
            for key, value in load_file(self._index_file_path, cast(dict[str, Any], {})).items()
        }

    def rebuild(self, matchmaker: MatchMaker) -> None:
        start_dates: MutableMapping[str, Mapping[str, Any]] = {}

        for digest_path in self._builds_dir.rglob(f"{DIGEST_FILENAME}"):
            build_id = "/".join(digest_path.relative_to(self._builds_dir).parent.parts)
            if build_id in start_dates:
                continue
            digest = digest_from(digest_path)
            start_dates[build_id] = BuildIndex.IndexElement(
                result=digest.result,
                timestamp=digest.timestamp,
                match_count=len(matchmaker.active_issues(digest.fail_causes)),
            ).model_dump()
        store_file(self._index_file_path, start_dates)

    def has(self, key: str) -> bool:
        return key in self._index_store

    def query(
        self,
        from_timestamp: None | int = None,
        to_timestamp: None | int = None,
        job_pattern: None | str = None,  # noqa: ARG002
        match_count: None | str = None,
        sort_by: None | str = None,
        restrict_result: None | str = None,
    ) -> Mapping[str, FinishedBuildDigest]:
        _results = list(filter(bool, map(str.strip, (restrict_result or "").upper().split(","))))
        allow_result = [res.upper() for res in _results if "~" not in res]
        disallow_result = [res.upper().strip("~") for res in _results if "~" in res]
        log().debug(
            "query: allow_result=%r, disallow_result=%r"
            ", match_count=%r, from_timestamp=%r, to_timestamp=%r",
            allow_result,
            disallow_result,
            match_count,
            from_timestamp,
            to_timestamp,
        )
        query_result = sorted(
            (
                (job_name, digest)
                for job_name, digest in self._index_store.items()
                if match_count is None
                or (
                    (match_count == "0" and not digest.match_count)
                    or (match_count == "1" and digest.match_count == 1)
                    or (match_count == ">=" and digest.match_count >= 1)
                    or (match_count == ">" and digest.match_count > 1)
                )
                if from_timestamp is None or digest.timestamp >= from_timestamp
                if to_timestamp is None or digest.timestamp <= to_timestamp
                if not allow_result or digest.result in allow_result
                if not disallow_result or digest.result not in disallow_result
            ),
            key=lambda e: getattr(e[1], sort_by or "timestamp"),
        )
        return {
            name: digest_from(self._builds_dir / name / DIGEST_FILENAME)
            for name, digest in query_result
        }


def print_build_info(
    digest: FinishedBuildDigest,
    index: int,
    matchmaker: MatchMaker,
    builds_dir: Path,
    jenkins_url: str,
    show_upstream_builds: bool,
    show_downstream_builds: bool,
    show_parameters: bool,
    show_matches: bool,
    show_causes: bool,
) -> None:
    build_id_color = BUILD_RESULT_COLOR.get(digest.result)
    build_url = build_url_from(digest.build_id, jenkins_url)
    issues = matchmaker.active_issues(digest.fail_causes)
    log_path_color = "bright_magenta" if digest.result == "SUCCESS" or issues else "red"
    issue_count_color = (
        "bright_red" if len(issues) == 0 else "bright_green" if len(issues) == 1 else "yellow"
    )
    rich_print(
        f"[not bold default]{index:4}:"
        f" [{build_id_color} link={build_url}]{digest.result[0]} {digest.build_id:<75}[/]"
        f" [bold blue]{'CV' if digest.is_direct_cv() else '  '}[/]"
        f" [bold blue]{'PR' if digest.is_direct_production() else '  '}[/]"
        f" c:[bright_cyan]{digest.commit_id[:6]}[/]"
        f" t:[bright_cyan]{date_str(digest.timestamp)}[/]"
        f" d:[bright_cyan]{dur_str(digest.duration_total_sec, fixed=True)}[/]"
        f" w:[bright_cyan]{digest.duration_wait_total_sec:>5}s[/]"
        f" m:[{issue_count_color}]{len(issues)}[/]"
        f" [bright_cyan]{f'{digest.console_log_line_count:_}':>11}[/]l"  # fixme: without_build_log
        # fixme, add console_log_bytes_count
        f" [{log_path_color} link={build_url}]{build_log_path_from(builds_dir, digest.build_id)}[/][/]"
    )
    if show_causes:
        for cause in digest.causes:
            rich_print(f"  - cause: {cause}")
    if show_upstream_builds:
        for bid in set(
            list(digest.upstream_builds_extracted) + list(digest.upstream_builds_inferred)
        ):
            rich_print(f"  - upstream: [bold link={build_url_from(bid, jenkins_url)}]{bid}[/]")
    if show_downstream_builds:
        for bid in digest.downstream_builds:
            rich_print(f"  - downstream: [bold link={build_url_from(bid, jenkins_url)}]{bid}[/]")
    if show_parameters:
        for key, value in digest.parameters.items():
            rich_print(f"  - param {key}={value}")
    if show_matches:
        bla = [(line, p_hash) for p_hash, lines in issues.items() for line in lines]
        for line, p_hash in sorted(bla):
            rich_print(
                f"  - |[cyan]{matchmaker.resolve(p_hash)[:30]:<32}[/]| L{line[0]:_}: {line[1]}"
            )


def dur_str(seconds: float, fixed: bool = False) -> str:
    """Turns a duration defined by @seconds into a string like '1d:2h:3m'
    If @fixed is True, numbers will be 0-padded for uniform width.
    Negative values for @seconds are not supported (yet)
    >>> dur_str(42)
    '42s'
    >>> dur_str(12345)
    '3h:25m:45s'
    """
    if not fixed and not seconds:
        return "0s"
    digits = 2 if fixed else 1
    hours = (
        f"{int(seconds // 3600):0{digits}d}h"
        if fixed or (seconds >= 3600 and (seconds % 86400))
        else ""
    )
    minutes = (
        f"{int(seconds // 60 % 60):0{digits}d}m"
        if fixed or (seconds >= 60 and (seconds % 3600))
        else ""
    )
    seconds_str = (
        f"{int(seconds % 60):0{digits}d}s" if not fixed and ((seconds % 60) or seconds == 0) else ""
    )
    return ":".join(e for e in (hours, minutes, seconds_str) if e)


def link(href: str, text: str, markdown: bool, width: int = 0) -> str:
    padding = " " * max(0, width - len(text))
    return f"[{text}]({href})" if markdown else rf"[bright_cyan link={href}]\[{text}][/]{padding}"


def store_file(path: Path, data: Mapping[str, Any]) -> None:
    """Store a JSON or YAML file atomically"""
    path.parent.mkdir(exist_ok=True, parents=True)
    temp_path = path.parent / f"{path.name}.temp"
    with temp_path.open("w") as open_file:
        if path.suffix == ".json":
            json.dump(data, open_file, indent=2)
        elif path.suffix == ".yaml":
            yaml.dump(data, open_file, indent=2)
    temp_path.rename(path)


def load_file[T](path: Path, default: T) -> T:
    """Load a JSON or YAML file and terminate the process on error"""
    with suppress(FileNotFoundError):
        with path.open() as open_file:
            if path.suffix == ".json":
                try:
                    result = json.load(open_file)
                except json.JSONDecodeError as exc:
                    log().error("Could not read %s: %s", open_file.name, exc)
                    raise SystemExit(1) from exc
            elif path.suffix == ".yaml":
                try:
                    result = yaml.safe_load(open_file)
                except Exception as exc:
                    log().error("Could not read %s: %s", open_file.name, exc)
                    raise SystemExit(1) from exc
            return cast(T, result)
    return default


def build_stages_from(path: Path) -> Sequence[StageInfo]:
    with suppress(FileNotFoundError):
        with open_compressed(path) as open_file:
            return BuildStages(**json.load(open_file)).stages
    return []


def commit_id_from(lines: Sequence[str]) -> str:
    """Returns commit ID extract from a build log"""
    commit_id_regex = "([0-9a-fA-F]{40})"
    for pattern in (
        re.compile(pattern)
        for pattern in (
            rf"CUSTOM_GIT_REF:........... │{commit_id_regex}│",
            rf"branches_str:............. │{commit_id_regex}│",
            rf"refspec:.................. │{commit_id_regex}│",
            rf".*Checking out Revision {commit_id_regex} \(.*\).*",
            rf"git fetch .* {commit_id_regex}",
            rf"git checkout {commit_id_regex}",
            rf"git checkout -f {commit_id_regex} # timeout",
        )
    ):
        with suppress(StopIteration):
            # only process first 800 lines - later lines can be for other repos
            return next(
                str(m.groups()[-1]) for line in lines[:800] if (m := re.search(pattern, line))
            )
    return "------"


def upstream_builds_from(lines: Sequence[str]) -> Sequence[str]:
    """Returns an (likely incomplete) list of upstream builds collected from hints found
    in the build log"""
    result = set()
    for line in lines:
        if match := re.search(r"(build candidate: '|existing:)\[(.*)\]'", line):
            details = {
                k.strip(): v.strip()
                for e in match.groups()[1].split(",")
                for k, v in (e.split(":", maxsplit=1),)
                if e.strip()
            }
            result.add(f"{details['path']}/{details['number']}")
    return sorted(result)


def downstream_builds_from(causes: Sequence[Cause]) -> Sequence[str]:
    """Returns downstream builds taken from build causes. Only real downstream
    builds are considered, ignoring replay/retrigger builds"""
    result = set()
    for cause in causes:
        match cause.type:
            case "Cause$UpstreamCause" | "BuildUpstreamCause":
                result.add(f"{cause.upstreamProject}/{cause.upstreamBuild}")
            case "RebuildCause":
                ...
            case _:
                assert cause.upstreamProject is None
    return sorted(result)


def is_cv_build_from(lines: Sequence[str], build_id: str) -> bool:
    """Returns whether we can guess from the build log this is a CV build indicated
    by a downstream build being 'Triggered by Gerrit', but not 'in silent mode'
    This is redundant (since it could be taken from the 'root cause' but we might not
    have it here yet and we can use it for consistency checks later."""
    if "/cv/" in build_id:
        return True
    with suppress(StopIteration):
        gerrit_trigger_line = next(line for line in lines[:100] if "Triggered by Gerrit" in line)
        if "in silent mode" not in gerrit_trigger_line:
            return True
    return False


def build_node_from(lines: Sequence[str]) -> str:
    for line in lines:
        if match := re.match(r"^Running on (\S+) in .*$", line):
            return match.group(1)
        if match := re.match(r"^Building (remotely )?on (\S+) .*$", line):
            return match.group(2)
        if match := re.match(r"^‘(.*)’ is offline$", line):
            return match.group(1)
    return "------"


def start_time_from(lines: Sequence[str]) -> int:
    for line in lines:
        if match := re.match(r"^\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d*Z)\]", line):
            return int(ts.timestamp()) if (ts := date_from(match.group(1))) else 0
    return 0


def short_path(path: Path) -> str:
    with suppress(ValueError):
        return str(path.relative_to(Path().cwd()))
    return str(path).replace(str(Path.home()), "~")


def build_log_path_from(builds_dir: Path, build_id: str) -> str:
    return short_path(builds_dir / build_id / f"{BUILD_LOG_FILENAME}.gz")


def build_url_from(build_id: str, jenkins_url: str) -> str:
    parts = build_id.split("/")
    return f"{'/job/'.join((jenkins_url, *parts[:-1]))}/{parts[-1]}/"


@contextmanager
def open_compressed(path: Path, mode: str = "rt") -> Iterator[TextIO]:
    """When opening a file with given @path try to open {path}.gz instead
    see https://docs.python.org/3/library/gzip.html
    """
    compressed_filepath = path.parent / (
        f"{path.name}.gz" if path.suffix not in {".gz", ".bz2"} else path.name
    )
    if "w" in mode:
        with gzip.open(compressed_filepath, mode, encoding="utf-8", compresslevel=1) as open_file:
            log().debug(
                "open compressed %s instead of %s for writing",
                short_path(compressed_filepath),
                path.name,
            )
            yield cast(TextIO, open_file)
    else:
        with gzip.open(compressed_filepath, mode, encoding="utf-8") as open_file:
            log().debug(
                "open compressed %s instead of %s for reading",
                short_path(compressed_filepath),
                path.name,
            )
            yield cast(TextIO, open_file)


def last_saturday() -> datetime:
    """Sheriff want's to cover all builds since takeover, including Sat and
    Sun of last week"""
    delta = ((today := date.today()).weekday() - 5) % 7
    return datetime.combine(today - timedelta(days=delta), datetime.min.time())


def effective_calendar_week() -> int:
    """Returns the current calendar week but effectively starting on
    Saturday of last week"""
    return (last_saturday().isocalendar().week) % 52 + 1


def timestamp_from(date_or_age: None | str, default: None | int) -> None | int:
    """Returns a timestamp from anything that can be seen as such and None if @date_or_str
    is empty. @default will be returned if @date_or_str is None"""
    if date_or_age is None:
        return default
    if not date_or_age:
        return None
    with suppress(ValueError):
        if (date := date_from(int(date_or_age))) is None:  # age string
            return None
        return int(date.timestamp())
    with suppress(ValueError):
        if (date := date_from(date_or_age)) is None:  # date string
            return None
        return int(date.timestamp())
    with suppress(ValueError):
        return int(datetime.now().timestamp() - parse_age(date_or_age))  # age
    raise ValueError(
        f"{date_or_age} cannot be parsed as date or age"
        " (try '2d', '3h', '2025-10-10T01:02:03Z', '1758173336'..)"
    )


def build_info_from(build_info_path: Path) -> Build:
    with open_compressed(build_info_path, "rt") as build_info_file:
        return Build.model_validate(json.load(build_info_file))


def digest_from(digest_path: Path) -> FinishedBuildDigest:
    try:
        with digest_path.open() as digest_file:
            return FinishedBuildDigest.model_validate_json(digest_file.read())
    except FileNotFoundError:
        raise
    except Exception as exc:
        log().error("Could not read %s: %s", digest_path, exc)
        raise


def path_matches(build_id: str | Path, include: None | str, exclude: None | str) -> bool:
    """Returns whether given @build_id matches @include/@exclude"""
    _build_id = build_id.as_posix() if isinstance(build_id, Path) else build_id
    return bool(
        (not include or re.search(include, _build_id))
        and not (exclude and re.search(exclude, _build_id))
    )


async def _fn_fetch(cli_args: Args) -> None:
    """Makes build logs, info and run info for Jenkins builds which match certain criteria
    available locally (in a compressed but unmodified manner)
    Criteria are: availability, time constraints, only failed jobs are being stored"""
    cli_args.builds_dir.mkdir(exist_ok=True, parents=True)

    # this defines the second to which we look back in time
    start_timestamp = timestamp_from(cli_args.date_from, default=int(last_saturday().timestamp()))
    rich_print(
        "[bold blue]Fetching logs and info of finished builds starting from "
        f"{date_str(start_timestamp) if start_timestamp else 'the beginning'}..[/]"
    )

    jobs_visited = 0
    build_infos_downloaded = 0
    build_logs_downloaded = 0

    log().info("connect..")
    # fixme: use cli_args.jenkins_url
    async with AugmentedJenkinsClient(
        **extract_credentials(cli_args.credentials), timeout=cli_args.timeout
    ) as jenkins_client:
        # TODO (frans): fetch running builds in order to avoid repeated downloads of build info
        #               for running builds
        async for node_path, node in jenkins_client.traverse_job_tree(ignored_pattern=None):
            if node.type == "Folder":  # or node_path[0] != "checkmk":
                continue
            jobs_visited += 1
            job_full_name = "/".join(node_path)
            job_info = await jenkins_client.job_info(job_full_name)
            rich_print(f"traversing [bright_cyan link={job_info.url}]{job_info.path}[/]..")

            for build_nr in sorted((b.number for b in job_info.builds), reverse=True):
                build_dir = cli_args.builds_dir / job_full_name / str(build_nr)

                if build_dir.exists():
                    log().debug("skip already available %s:%d", job_full_name, build_nr)
                    continue
                build_infos_downloaded += 1

                # we need raw data to later store it
                build_info = Build.model_validate(
                    raw_build_info := await jenkins_client.raw_build_info(job_full_name, build_nr)
                )

                if start_timestamp is not None and build_info.timestamp < start_timestamp:
                    # as soon as we find a too old build, we can abort looking for more
                    break

                assert build_info.inProgress == raw_build_info["building"]

                if build_info.inProgress or raw_build_info["building"]:
                    # we're only interested in finished builds
                    continue

                raw_build_stages = await jenkins_client.raw_build_stages(job_full_name, build_nr)

                build_log = None
                try:
                    rich_print(
                        f" - [link={build_info.url}]{str(build_nr):>6}[/]"
                        f" {date_from(build_info.timestamp)}"
                        f" dur:{dur_str(build_info.duration_total_sec):>10}"
                        f", [{BUILD_RESULT_COLOR.get(str(build_info.result))}]{build_info.result:<8}"
                    )

                    if build_info.result == "SUCCESS":
                        # we store successful builds for later - no use yet
                        continue

                    build_logs_downloaded += 1
                    build_log = await jenkins_client.build_console_output(job_full_name, build_nr)

                finally:
                    # Write all we got about a job to FS in an "atomic" way (all at once)
                    build_dir.mkdir(parents=True, exist_ok=True)

                    with open_compressed(build_dir / BUILD_INFO_FILENAME, "wt") as info_file:
                        info_file.write(json.dumps(raw_build_info))
                    with open_compressed(build_dir / BUILD_STAGES_FILENAME, "wt") as stages_file:
                        stages_file.write(json.dumps(raw_build_stages))
                    if build_log:
                        with open_compressed(build_dir / BUILD_LOG_FILENAME, "wt") as log_file:
                            log_file.write(build_log)

    rich_print(
        f"visited {jobs_visited} jobs, downloaded {build_infos_downloaded} build infos,"
        f" {build_logs_downloaded} build logs,"
    )


async def _fn_create_digests(cli_args: Args) -> None:
    # main thread!

    def queue_multiprocess() -> Iterator[FinishedBuildDigest]:
        with multiprocessing.Pool(cli_args.max_processes) as pool:
            yield from pool.imap(create_digest, __fn_create_digests(cli_args, matchmaker))

    def queue_single() -> Iterator[FinishedBuildDigest]:
        """For debugging purposes - don't use `multiprocessing` but process everything build
        by build in one process"""
        for args in __fn_create_digests(cli_args, matchmaker):
            yield create_digest(args)

    rich_print("[bold blue]Create and update digests from build info..[/]")

    matchmaker = MatchMaker(cli_args.known_issues_file)

    for i, new_digest in enumerate(
        queue_single() if (cli_args.builds or cli_args.max_processes < 2) else queue_multiprocess()
    ):
        if new_digest.result is None:
            log().warning("result for %s is None", new_digest.build_id)
            continue
        digest_path = cli_args.builds_dir / new_digest.build_id / DIGEST_FILENAME
        log().debug("store %s..", short_path(digest_path))
        store_file(digest_path, new_digest.model_dump())
        print_build_info(
            new_digest,
            i,
            matchmaker,
            cli_args.builds_dir,
            cli_args.jenkins_url,
            show_upstream_builds=cli_args.verbose,
            show_downstream_builds=cli_args.verbose,
            show_parameters=cli_args.verbose,
            show_matches=cli_args.verbose,
            show_causes=cli_args.verbose,
        )


def create_digest(
    args: tuple[Build, Path, str, None | FinishedBuildDigest, Path],
) -> FinishedBuildDigest:
    """Populates and returns a FinishedBuildDigest - this is the numbercuncher function which
    inspects the build log and takes long"""

    build_info, build_path, build_id, current, known_issues_file_path = args
    matchmaker = MatchMaker(known_issues_file_path)

    log_lines, without_build_log = [], True
    try:
        with open_compressed(build_path / BUILD_LOG_FILENAME, "rt") as log_file:
            log_lines = log_file.readlines()
            without_build_log = False
    except FileNotFoundError:
        log().debug("no build log available for %s - only process build info", build_path)

    stages = (current and current.stages) or build_stages_from(
        build_path / BUILD_STAGES_FILENAME
    )  # fixme
    # stages = build_stages_from(build_path / BUILD_STAGES_FILENAME)
    assert stages is not None
    assert not stages or stages[0].timestamp

    # every first line contains the (slightly modified) shortDescription of the first cause
    # then follow indented lines with the root causes of their parent (downstream) builds:
    # |Started by upstream project "checkmk/master/cv/test-gui-crawl-f12less" build number 146
    # |originally caused by:
    # | Triggered by Gerrit: https://review.lan.tribe29.com/c/check_mk/+/114935
    # |Started by upstream project "checkmk/master/cv/test-gui-e2e-f12less-cee" build number 203
    # |originally caused by:
    # | Triggered by Gerrit: https://review.lan.tribe29.com/c/check_mk/+/114935

    # 'child' builds - redundant and incomplete, should be consistent with
    # downstream buildsof other builds
    # fixme: those have to be merged in case upstream_builds_from() changes
    upstream_builds = (
        upstream_builds_from(log_lines) if current is None else current.upstream_builds_extracted
    )
    assert upstream_builds is not None

    # 'parent' builds - information taken from causes and only incomplete insofar as
    # some downstream builds just 'consume' this build and can be considered downstream, too
    downstream_builds = downstream_builds_from(build_info.causes)
    assert downstream_builds is not None

    # is_cv_build = is_cv_build_from(log_lines, build_id) if current is None else current.is_cv_build
    # assert is_cv_build is not None

    first_log_timestamp = (current and current.first_timestamp) or start_time_from(log_lines)
    # print(first_log_timestamp , date_str(first_log_timestamp))
    # print(stages[0].timestamp, date_str(stages[0].timestamp))
    # print(stages)
    assert not stages or first_log_timestamp <= (stages[0].timestamp or 0)
    first_timestamp = first_log_timestamp or stages[0].timestamp if stages else 0
    # assert first_timestamp or (not log_lines and not stages)
    assert first_timestamp is not None

    # build_node = build_node_from(log_lines) if current is None else current.build_node
    build_node = (None if current is None else current.build_node) or build_node_from(log_lines)
    assert build_node is not None, f"build node {build_path}"

    commit_id = current and current.commit_id or commit_id_from(log_lines)
    assert commit_id is not None

    fail_causes = current and current.fail_causes or {}
    if build_info.result != "SUCCESS" and (missing_keys := matchmaker.keys() - fail_causes.keys()):
        log().debug(
            "process %d missing regexes in %s lines", len(missing_keys), f"{len(log_lines):_}"
        )
        fail_causes = matchmaker(log_lines, fail_causes)

    assert build_info.result is not None, build_path  # for mypy..

    return FinishedBuildDigest(
        build_id=build_id,
        number=build_info.number,
        result=build_info.result,
        timestamp=build_info.timestamp,
        duration_total_sec=build_info.duration_total_sec,
        duration_queue_sec=build_info.duration_queue_sec,
        duration_execution_sec=build_info.duration_execution_sec,
        first_timestamp=first_timestamp,
        stages=stages,
        without_build_log=without_build_log,
        commit_id=commit_id,
        # is_cv_build=is_cv_build,
        console_log_line_count=len(log_lines),
        console_log_bytes_count=sum(map(len, log_lines)),
        parameters=build_info.parameters,
        upstream_builds_extracted=upstream_builds,
        upstream_builds_inferred=[] if current is None else current.upstream_builds_inferred,
        downstream_builds=downstream_builds,
        causes=[cause.shortDescription for cause in build_info.causes],
        fail_causes=fail_causes,
        build_node=build_node,
    )


def __fn_create_digests(
    cli_args: Args, matchmaker: MatchMaker
) -> Iterator[tuple[Build, Path, str, None | FinishedBuildDigest, Path]]:
    """Creates and updates digests from build info / logs"""
    # main thread!

    def traverse(
        build_info_paths: Iterable[Path], min_timestamp: None | int
    ) -> Iterable[tuple[Build, Path]]:
        """Yields build info and path to build in time decending order"""
        log().info("gather locally stored build instances..")

        def next_build(builds_iter: Iterator[Path]) -> tuple[Build, Path, Iterator[Path]]:
            return build_info_from(next_path := next(builds_iter)), next_path, builds_iter

        folders: dict[Path, list[Path]] = {}
        for build_info_path in build_info_paths:
            folders.setdefault(build_info_path.parent.parent, []).append(build_info_path)

        next_builds = [
            next_build(builds_iter)
            for builds in folders.values()
            for builds_iter in (iter(sorted(builds, key=lambda p: int(p.parts[-2]), reverse=True)),)
        ]
        while next_builds:
            next_builds.sort(key=lambda x: x[0].timestamp)
            build_info, build_info_path, builds_iter = next_builds.pop()
            if min_timestamp is None or build_info.timestamp >= min_timestamp:
                yield build_info, build_info_path.parent
                with suppress(StopIteration):
                    next_builds.append(next_build(builds_iter))

    from_timestamp = timestamp_from(cli_args.date_from, default=None)

    def build_info_path_from(arg: str) -> Path:
        path = Path(arg)
        if path.name.startswith(BUILD_INFO_FILENAME):
            if path.is_absolute():
                if path.exists():
                    return path
        elif (cli_args.builds_dir / path / f"{BUILD_INFO_FILENAME}.gz").exists():
            return cli_args.builds_dir / path / f"{BUILD_INFO_FILENAME}.gz"
        raise RuntimeError(f"Provided path {arg} does not exist")

    builds_to_process = (
        [
            path
            for path in cli_args.builds_dir.rglob(f"{BUILD_INFO_FILENAME}*")
            if path_matches(
                path.relative_to(cli_args.builds_dir), cli_args.include, cli_args.exclude
            )
        ]
        if not cli_args.builds
        else list(map(build_info_path_from, cli_args.builds))
    )

    log().info(
        "process %d builds collected via: include=%r, exclude=%r, date-from=%s",
        len(builds_to_process),
        cli_args.include,
        cli_args.exclude,
        date_from(from_timestamp) if from_timestamp else "inf",
    )

    num_processed = 0

    for i, (build_info, build_path) in enumerate(traverse(builds_to_process, from_timestamp)):
        build_id = "/".join(build_path.relative_to(cli_args.builds_dir).parts)

        digest_path = build_path / DIGEST_FILENAME
        percent_done = 100 / len(builds_to_process) * i

        digest = None
        if not cli_args.rebuild:
            with suppress(FileNotFoundError, ValidationError):
                digest = digest_from(digest_path)
                if not cli_args.refresh:
                    # we skip further investigation if all digest values are non-None and all known
                    # pattern have already been searched for
                    if all(value is not None for value in digest.__dict__.values()) and (
                        digest.result == "SUCCESS"
                        or digest.without_build_log
                        or digest.fail_causes.keys() >= matchmaker.keys()
                    ):
                        log().info("%d (%.2f%%): %s up to date", i, percent_done, build_id)
                        continue

        log().info(
            "%d (%.2f%%): process %s %s",
            i,
            percent_done,
            date_str(build_info.timestamp),
            build_id,
        )

        yield build_info, build_path, build_id, digest, cli_args.known_issues_file

        num_processed += 1
        if cli_args.max_results and num_processed == cli_args.max_results:
            break


async def _fn_create_index(cli_args: Args) -> None:
    """Creates and persists an index containing (static) query data (like timestamp) for fast lookup."""
    rich_print("[bold blue]Create index for already processed builds..[/]")
    matchmaker = MatchMaker(cli_args.known_issues_file)
    BuildIndex(cli_args.base_dir, cli_args.builds_dir).rebuild(matchmaker)


async def _fn_fuse(cli_args: Args) -> None:
    """For now only collect 'upstream_builds_inferred' and update all digest files"""
    rich_print("[bold blue]Combine upstream/downstream build causes among builds..[/]")

    log().info("read all digests..")
    all_digest = {
        (digest := digest_from(digest_path)).build_id: digest
        for digest_path in list(cli_args.builds_dir.rglob(f"{DIGEST_FILENAME}"))  # fixme
    }

    log().info("make assumptions..")

    def check_parent_cv(digest):
        for parent_build_id in digest.downstream_builds:
            if parent_digest := all_digest.get(parent_build_id):
                assert (
                    digest.is_direct_cv() == parent_digest.is_direct_cv()
                    or parent_digest.is_direct_cv()
                ), f"check_parent_cv {digest.build_id} {parent_build_id}"
                check_parent_cv(parent_digest)

    def check_children_cv(digest):
        for child_build_id in digest.upstream_builds():
            if child_digest := all_digest.get(child_build_id):
                assert (
                    digest.is_direct_cv() == child_digest.is_direct_cv()
                    or not child_digest.is_direct_cv()
                ), f"check_children_cv {digest.build_id} {child_build_id}"
                check_children_cv(child_digest)

    for build_id, digest in all_digest.items():
        try:
            # fixme: wrong! (there must be a 'production build' rather than 'cv build flag'
            # check_children_cv(digest)
            check_parent_cv(digest)
            # for u in digest.upstream_builds():
        except Exception as exc:
            print(build_id)
            print(exc)
            raise SystemExit(1)

    log().info("infer upstream builds from downstream builds")
    for build_id, digest in all_digest.items():
        for downstream_build_id in digest.downstream_builds:
            if downstream_build_id not in all_digest:
                log().debug("cannot set upstream build for non-existing %s", downstream_build_id)
                continue
            all_digest[downstream_build_id].upstream_builds_inferred = sorted(
                set(list(all_digest[downstream_build_id].upstream_builds_inferred) + [build_id])
            )

    # write back all digests
    for build_id, digest in all_digest.items():
        if not digest.upstream_builds_inferred:
            continue
        digest_path = cli_args.builds_dir / build_id / DIGEST_FILENAME
        assert digest_path.exists()
        store_file(digest_path, digest.model_dump())


async def _fn_export(cli_args: Args) -> None:
    """Export all FinishedBuild digests to an SQL database"""
    rich_print("[bold blue]Export build info to PostgreSQL database..[/]")

    from sqlalchemy import (  # noqa: PLC0415
        ARRAY,
        Boolean,
        DateTime,
        Integer,
        Interval,
        PrimaryKeyConstraint,
        String,
        Text,
        create_engine,
    )
    from sqlalchemy.orm import (  # noqa: PLC0415
        DeclarativeBase,
        Mapped,
        Session,
        mapped_column,
    )

    class Base(DeclarativeBase): ...

    class IssueDBItem(Base):
        """The DB counterpart for an Issue instance"""

        __tablename__ = "known_issues"

        # short identifier for a regex
        regex_hash: Mapped[str] = mapped_column(String, primary_key=True)
        # the actual regex matching a failure string from build log
        regex: Mapped[str] = mapped_column(String)
        # failure category (network, timeout, test failure, ..)
        category: Mapped[str] = mapped_column(String)

        # associated ticket
        ticket: Mapped[str] = mapped_column(String)

        family: Mapped[str] = mapped_column(String)
        comment: Mapped[str] = mapped_column(String)

        @classmethod
        def from_pydantic(cls, regex_hash: str, issue: Issue) -> "IssueDBItem":
            """Turns a Issue instance into something more usable for querying"""
            return cls(
                regex_hash=regex_hash,
                regex=issue.regex,
                category=issue.category,
                ticket=issue.ticket,
                family=issue.family,
                comment=issue.comment,
            )

        def to_pydantic(self) -> Issue:
            """Only needed for validation"""
            return Issue(
                regex=self.regex,
                category=self.category,
                family=self.family,
                ticket=self.ticket,
                comment=self.comment,
            )

    class FinishedBuildDigestDBItem(Base):
        """The DB counterpart for an FinishedBuildDigest instance"""

        __tablename__ = "finished_builds"

        build_id: Mapped[str] = mapped_column(String, primary_key=True)
        # path to Jenkins job
        job_path: Mapped[str] = mapped_column(String)
        # Jenkins job build number
        number: Mapped[int] = mapped_column(Integer)
        # SUCCESS, FAILURE, ABORTED..
        result: Mapped[JobResult] = mapped_column(String)
        # start timestamp of a build
        timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=False))
        # total build duration
        duration: Mapped[timedelta] = mapped_column(Interval)
        duration_queue: Mapped[timedelta] = mapped_column(Interval)
        duration_execution: Mapped[timedelta] = mapped_column(Interval)
        # duration on top of actual execution duration
        duration_wait_total: Mapped[timedelta] = mapped_column(Interval)
        parameters: Mapped[str] = mapped_column(Text)
        without_build_log: Mapped[bool] = mapped_column(Boolean)
        # git commit id
        commit_id: Mapped[str] = mapped_column(String)
        fail_causes: Mapped[list[str]] = mapped_column(ARRAY(String))
        # size of build log in lines
        console_log_line_count: Mapped[int] = mapped_column(Integer)  # fixme should be optional
        # size of build log in bytes
        console_log_bytes_count: Mapped[int] = mapped_column(Integer)  # fixme should be optional
        # producer builds
        upstream_builds: Mapped[list[str]] = mapped_column(ARRAY(String))
        # consumer builds
        downstream_builds: Mapped[list[str]] = mapped_column(ARRAY(String))
        # whether or not this is a change avalidation build
        # is_cv_build: Mapped[bool] = mapped_column(Boolean)
        is_implicit_cv: Mapped[bool] = mapped_column(Boolean)
        is_implicit_production: Mapped[bool] = mapped_column(Boolean)
        # list of Jira build causes
        causes: Mapped[list[str]] = mapped_column(ARRAY(String))
        build_node: Mapped[str] = mapped_column(String)
        # fixme: add stages

        def to_pydantic(self) -> FinishedBuildDigest:
            """Only needed for validation"""
            fail_causes: MutableMatchings = {}
            for hash_lineno_line in self.fail_causes:
                regex_hash, lineno_line, line = hash_lineno_line.split(":", maxsplit=2)
                fail_causes.setdefault(PatternHash(regex_hash), []).append(
                    (int(lineno_line), line.strip())
                )

            return FinishedBuildDigest(
                build_id=self.build_id,
                number=self.number,
                result=self.result,
                timestamp=int(self.timestamp.timestamp()),
                duration_total_sec=self.duration.total_seconds(),
                duration_queue_sec=self.duration_queue.total_seconds(),
                duration_execution_sec=self.duration_execution.total_seconds(),
                first_timestamp=(
                    int(self.timestamp.timestamp()) + self.duration_wait_total.total_seconds()
                ),
                stages=[],
                without_build_log=self.without_build_log,
                commit_id=self.commit_id,
                fail_causes=fail_causes,
                console_log_line_count=self.console_log_line_count,
                console_log_bytes_count=self.console_log_bytes_count,
                parameters=json.loads(self.parameters),
                upstream_builds_extracted=self.upstream_builds,
                upstream_builds_inferred=[],
                downstream_builds=self.downstream_builds,
                # is_cv_build=self.is_cv_build,
                causes=self.causes,
                build_node=self.build_node,
            )

        @classmethod
        def from_pydantic(cls, digest: FinishedBuildDigest) -> "FinishedBuildDigestDBItem":
            """Turns a FinishedBuildDigest instance into something more usable for querying"""
            return cls(
                build_id=digest.build_id,
                job_path=digest.build_id.rsplit("/", maxsplit=1)[0],
                number=digest.number,
                # timestamp=digest.timestamp,
                timestamp=date_from(
                    digest.timestamp
                ),  # datetime.utcfromtimestamp(digest.timestamp),
                # duration_total_sec=digest.duration_total_sec,
                duration=timedelta(seconds=digest.duration_total_sec),
                duration_queue=timedelta(seconds=digest.duration_queue_sec),
                duration_execution=timedelta(seconds=digest.duration_execution_sec),
                duration_wait_total=timedelta(seconds=digest.duration_wait_total_sec),
                result=digest.result,
                parameters=json.dumps(digest.parameters),
                without_build_log=digest.without_build_log,
                commit_id=digest.commit_id,
                fail_causes=[
                    f"{regex}:{line_no}:{line.strip()}"
                    for regex, lines in digest.fail_causes.items()
                    for line_no, line in lines
                ],
                console_log_line_count=digest.console_log_line_count,
                console_log_bytes_count=digest.console_log_bytes_count,
                upstream_builds=digest.upstream_builds_extracted,  # modified!
                downstream_builds=digest.downstream_builds,
                is_implicit_cv=digest.is_direct_cv(),  # fixme: imlicit!
                is_implicit_production=digest.is_direct_production(),  # fixme: imlicit!
                causes=digest.causes,
                build_node=digest.build_node,
            )

    class RegexMatchingItem(Base):
        __tablename__ = "regex_matchings"

        # build_id (job path + build number) and regex_hash connecting @finished_builds and @known_issues
        __table_args__ = (PrimaryKeyConstraint("build_id", "regex_hash"),)

        build_id: Mapped[str] = mapped_column(String, nullable=False)
        regex_hash: Mapped[str] = mapped_column(String, nullable=False)

        # line numbers and lines of build log matching the regex referenced with @regex_hash
        matching_line_numbers: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
        matching_lines: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)

    log().info("connect to DB..")
    engine = create_engine(DB_ENGINE_STRING, echo=False)
    # engine = create_engine("sqlite:///:memory:", echo=False)
    FinishedBuildDigestDBItem.__table__.drop(engine, checkfirst=True)  # type: ignore[attr-defined]
    IssueDBItem.__table__.drop(engine, checkfirst=True)  # type: ignore[attr-defined]
    RegexMatchingItem.__table__.drop(engine, checkfirst=True)  # type: ignore[attr-defined]
    Base.metadata.create_all(engine)

    log().info("collect and pre-process build digests..")
    matchmaker = MatchMaker(cli_args.known_issues_file)
    all_issues = {
        regex_hash: Issue(
            regex=issue.regex,
            dismiss=1,
            category=issue.category or "",
            family=issue.family or "",
            ticket=issue.ticket or "",
            comment=issue.comment or "",
        )
        for regex_hash in matchmaker.keys()
        if (issue := matchmaker.get(regex_hash))
    }
    all_digests = [
        digest_from(digest_path)
        for digest_path in list(cli_args.builds_dir.rglob(f"{DIGEST_FILENAME}"))  # [:200]
        # if digest_from(digest_path).result != "SUCCESS"
    ]
    # make digests fit for use in an SQL database
    for digest in all_digests:
        # remove empty fail_causes elements - this is redundant but needed to compare
        # a re-imported digest with the (now modified) original one.
        digest.first_timestamp = digest.first_timestamp or digest.timestamp
        digest.fail_causes = {
            k: [(line_no, line.replace("\x00", " ").strip()) for line_no, line in lines]
            for k, lines in digest.fail_causes.items()
            if lines
        }
        digest.upstream_builds_extracted = sorted(
            list(digest.upstream_builds_extracted) + list(digest.upstream_builds_inferred)
        )
        digest.upstream_builds_inferred = []
        digest.console_log_bytes_count = min(digest.console_log_bytes_count, 2_147_483_647)  # yes
        digest.stages = []

    log().info("export %d build digests to DB..", len(all_digests))
    with Session(engine) as session:
        for regex_hash, issue in all_issues.items():
            db_item = IssueDBItem.from_pydantic(regex_hash, issue)
            if (reimported_issue := db_item.to_pydantic()) != issue:
                rich_print(f"before: {issue}")
                rich_print(f"after:  {reimported_issue}")
                raise SystemExit(1)
            session.add(db_item)
        session.commit()

        for digest in all_digests:
            db_item = FinishedBuildDigestDBItem.from_pydantic(digest)
            for regex_hash, matchings in digest.fail_causes.items():
                matching_line_numbers, matching_lines = zip(*matchings)
                session.add(
                    RegexMatchingItem(
                        build_id=digest.build_id,
                        regex_hash=regex_hash,
                        matching_line_numbers=matching_line_numbers,
                        matching_lines=matching_lines,  # [l.replace("\x00", " ") for l in matching_lines],
                    )
                )
                session.commit()

            if (reimported_digest := db_item.to_pydantic()) != digest:
                rich_print(f"before: {digest}")
                rich_print(yaml.dump(digest.model_dump()))
                print("--")
                rich_print(f"after:  {reimported_digest}")
                rich_print(yaml.dump(reimported_digest.model_dump()))
                raise SystemExit(1)
            session.add(FinishedBuildDigestDBItem.from_pydantic(digest))
            session.commit()

        session.commit()

        # validate data
        _imported_issues = {
            item.regex_hash: item.to_pydantic() for item in session.query(IssueDBItem).all()
        }
        # fixme
        # assert sorted(imported_issues.items()) == sorted(all_issues.items())
        _imported_digests = [
            item.to_pydantic() for item in session.query(FinishedBuildDigestDBItem).all()
        ]
        # fixme
        # assert sorted(imported_digests, key=lambda e: e.build_id) == sorted(
        #    all_digests, key=lambda e: e.build_id
        # )


async def _fn_update(cli_args: Args) -> None:
    rich_print("[bold blue]Fetch -> create digests -> update index -> fuse -> export[/]")

    cli_args.date_from = None
    cli_args.builds = None
    await _fn_fetch(cli_args)
    await _fn_create_digests(cli_args)
    await _fn_create_index(cli_args)
    await _fn_fuse(cli_args)
    await _fn_export(cli_args)


async def _fn_info(cli_args: Args) -> None:
    """Prints detailed info about a distinct build"""
    build_paths = [
        build.replace("/job/", "/")
        .replace(cli_args.jenkins_url, "")
        .replace("/console", "")
        .strip(" /")
        for build in cli_args.builds
    ]
    log().info("show info for: %s", build_paths)
    matchmaker = MatchMaker(cli_args.known_issues_file)

    for i, name in enumerate(build_paths):
        with (cli_args.builds_dir / name / DIGEST_FILENAME).open() as digest_file:
            digest = FinishedBuildDigest.model_validate_json(digest_file.read())
        print_build_info(
            digest,
            i,
            matchmaker,
            cli_args.builds_dir,
            cli_args.jenkins_url,
            show_upstream_builds=True,
            show_downstream_builds=True,
            show_parameters=True,
            show_matches=True,
            show_causes=True,
        )


async def _fn_issue_figures(cli_args: Args) -> None:
    """Prints out how often regexes from 'known issues' are being used respecting the provided
    time range and filter criteria"""
    matchmaker = MatchMaker(cli_args.known_issues_file)
    filter_regexes = matchmaker.regexes_containting(cli_args.regex_filter)
    if not filter_regexes and cli_args.regex_filter:
        print(f"{cli_args.regex_filter} not found")
        raise SystemExit(1)

    regex_counts: dict[PatternHash, list[int]] = {}
    regex_sample: dict[PatternHash, list[tuple[str, str]]] = {}
    from_timestamp = timestamp_from(cli_args.date_from, default=int(last_saturday().timestamp()))
    to_timestamp = timestamp_from(cli_args.date_to, default=None)

    # fixme: use index
    matching_digests = {
        digest.build_id: filtered_issues
        for digest_path in cli_args.builds_dir.rglob(f"{DIGEST_FILENAME}")
        for digest in (digest_from(digest_path),)
        if path_matches(
            digest_path.relative_to(cli_args.builds_dir), cli_args.include, cli_args.exclude
        )
        if not from_timestamp or digest.timestamp >= from_timestamp
        if not to_timestamp or digest.timestamp <= to_timestamp
        if (filtered_issues := matchmaker.active_issues(digest.fail_causes, filter_regexes))
    }

    # collect numbers and findings
    for build_id, filtered_issues in matching_digests.items():
        for regex_hash, lines in filtered_issues.items():
            regex_counts.setdefault(regex_hash, [0])[0] += 1
            regex_sample.setdefault(regex_hash, []).append((build_id, lines[0][1]))

    # print out findings
    for regex_hash, count in sorted(regex_counts.items(), key=lambda x: x[1], reverse=False):
        issue = matchmaker.get(regex_hash)
        assert issue
        if issue.dismiss in {0, 3}:
            # fixme: make optional
            continue
        if issue.category == "Code":
            # fixme: make optional
            continue
        # fixme: should be optional
        if count[0] < 10:  # noqa: PLR2004
            # we're only interested in real issues
            continue

        ticket_str = (
            link(
                f"https://jira.lan.tribe29.com/browse/{issue.ticket}",
                issue.ticket,
                cli_args.markdown,
            )
            if issue.ticket
            else r"[yellow bold]\[no ticket][/]"
        )
        show_matches = cli_args.verbose or filter_regexes
        category_color = {
            "ci": "bright_red",
            "load": "dodger_blue1",
            "gerrit": "pale_green3",
            "timeout": "bright_magenta",
            "network io": "salmon1",
            "flaky test": "bright_magenta",
            "code": "cyan",
        }.get(str(issue.category).lower(), "bold yellow")
        rich_print(
            "[bold white]*[/][not bold]"
            f" {ticket_str} count: [bright_cyan]{count[0]:4}[/]"
            f" category: [{category_color}]{str(issue.category):10}[/]"
            f" regex: [cyan]{regex_hash}[/]="
            f"`[white {'bold' if show_matches else ''}]{issue.regex[: max(0, Console().width - 42)]}[/]`[/]"
        )

        # fixme: sort
        # fixme: add date
        if show_matches:
            for build_id, example_log_line in regex_sample[regex_hash]:
                rich_print(
                    "  [bold white]-[/]"
                    f" `[italic not bold deep_sky_blue3]{example_log_line.strip()[: max(0, Console().width - 10)]}[/]`"
                )
                rich_print(
                    "[not bold default]    in"
                    f" {link(build_url_from(build_id, cli_args.jenkins_url), build_id, cli_args.markdown, 70)}"
                    f" [bright_magenta]{build_log_path_from(cli_args.builds_dir, build_id)}[/][/]"
                )
                if not cli_args.verbose or not filter_regexes:
                    break

    rich_print(
        f"processed {len(matching_digests)} digests collected via:"
        f" include={cli_args.include or None!r}, exclude={cli_args.exclude or None!r},"
        f" date-from={date_from(from_timestamp) if from_timestamp else 'inf'},"
        f" date-to={date_from(to_timestamp) if to_timestamp else 'inf'}"
        f" regex-filter: {cli_args.regex_filter}"
    )


async def _fn_report(cli_args: Args) -> None:
    """Lists all builds matching certain criteria"""
    matchmaker = MatchMaker(cli_args.known_issues_file)
    from_timestamp = timestamp_from(cli_args.date_from, default=int(last_saturday().timestamp()))
    to_timestamp = timestamp_from(cli_args.date_to, default=None)
    filter_regexes = matchmaker.regexes_containting(cli_args.regex_filter)
    if not filter_regexes and cli_args.regex_filter:
        print(f"{cli_args.regex_filter} not found")
        raise SystemExit(1)

    rich_print(
        f"start: {from_timestamp}/{date_from(from_timestamp) if from_timestamp else 'inf'}"
        f", to: {to_timestamp}/{date_from(to_timestamp) if to_timestamp else 'inf'}"
        f", sort-by: {cli_args.sort_by}"
        f", match-count: {cli_args.match_count}"
        f", regex-filter: {cli_args.regex_filter}",
    )
    build_index = BuildIndex(cli_args.base_dir, cli_args.builds_dir)
    matching_digests = build_index.query(
        match_count=cli_args.match_count,
        from_timestamp=from_timestamp,
        to_timestamp=to_timestamp,
        sort_by=cli_args.sort_by,
        restrict_result=cli_args.result,
    )
    log().info("got %d results", len(matching_digests))
    spreadsheet_info: dict[str, list[tuple[str | None, ...]]] = {}

    no_fail_causes = 0  # number of builds we don't have identified issues for
    build_count, failure_count = 0, 0
    build_time_spent, failure_time_spent = 0, 0

    for i, (build_id, digest) in enumerate(matching_digests.items()):
        identified_issues = matchmaker.active_issues(digest.fail_causes, filter_regexes)
        if not path_matches(build_id, cli_args.include, cli_args.exclude):
            continue
        if filter_regexes and not identified_issues:
            continue

        if digest.causes[0].startswith("Started by user"):  # fixme: make configurable
            continue
        build_count += 1
        build_time_spent += digest.duration_total_sec

        if digest.result == "SUCCESS":
            continue

        failure_count += 1
        failure_time_spent += digest.duration_total_sec

        # fixme: here we need a way to say: ignore CV builds which failed for a 'Code' reason
        #        but take others into account

        if digest.is_direct_cv():  # fixme: make configurable
            continue

        if not identified_issues and digest.result != "SUCCESS":  # type: ignore[comparison-overlap]
            no_fail_causes += 1

        if not cli_args.print_totals_only:
            print_build_info(
                digest,
                i,
                matchmaker,
                cli_args.builds_dir,
                cli_args.jenkins_url,
                show_upstream_builds=cli_args.verbose,
                show_downstream_builds=cli_args.verbose,
                show_parameters=cli_args.verbose,
                show_matches=cli_args.verbose,
                show_causes=cli_args.verbose,
            )

        # lookup first matching line
        # fixme: turn into attribute
        first_match_regex, first_match_line = None, None
        for p_hash, lines in (_item for _item in digest.fail_causes.items() if _item[1]):
            first_line = min(lines)
            if first_match_line is None or first_line < first_match_line:
                first_match_regex, first_match_line = p_hash, first_line

        issue = first_match_regex and matchmaker.get(first_match_regex)
        line = (first_match_line[1] if first_match_line else "").strip()

        spreadsheet_info.setdefault(date_str(digest.timestamp, "%Y-%m-%d %A"), []).append(
            (
                date_str(digest.timestamp, "%H:%M:%S"),
                build_url_from(build_id, cli_args.jenkins_url),
                (issue and issue.category) or "",
                (issue and issue.ticket) or "",
                (issue and issue.regex) or "",
                (issue and issue.family) or "",
                line,
                dur_str(digest.duration_total_sec),
                dur_str(digest.duration_wait_total_sec),
            )
        )

    log().info("safe report to %s", cli_args.report_file)
    store_file(cli_args.report_file, spreadsheet_info)
    if not cli_args.print_totals_only:
        rich_print(
            f"Unidentified: {no_fail_causes} / total: {sum(len(b) for b in spreadsheet_info.values())}"
        )
    if build_count and build_time_spent:
        rich_print(
            f"builds: {build_count}, total duration: {dur_str(build_time_spent)}"
            f", failed builds: {failure_count} ({100 / build_count * failure_count:.1f}%)"
            f", total failed duration: {dur_str(failure_time_spent)}"
            f" ({100 / build_time_spent * failure_time_spent:.1f}%)"
        )

    rich_print(
        f"processed {len(matching_digests)} digests collected via:"
        f" include={cli_args.include or None!r}, exclude={cli_args.exclude or None!r},"
        f" date-from={date_from(from_timestamp) if from_timestamp else 'inf'},"
        f" date-to={date_from(to_timestamp) if to_timestamp else 'inf'}"
        f" restrict-result={cli_args.result}"
        f" regex-filter: {cli_args.sort_by}"
        f" sort-by: {cli_args.regex_filter}"
    )

    if no_fail_causes:
        raise SystemExit(1)


async def _fn_spreadsheet(cli_args: Args) -> None:
    rich_print("[bold blue]Create spreadsheet..[/]")

    from odf.opendocument import (  # type: ignore[import-untyped] # noqa: PLC0415
        OpenDocumentSpreadsheet,
    )
    from odf.style import (  # type: ignore[import-untyped] # noqa: PLC0415
        Style,
        TableColumnProperties,
        TableRowProperties,
        TextProperties,
    )
    from odf.table import (  # type: ignore[import-untyped] # noqa: PLC0415
        Table,
        TableCell,
        TableColumn,
        TableRow,
    )
    from odf.text import A, P  # type: ignore[import-untyped] # noqa: PLC0415

    log().info("load report from %s", cli_args.report_file)
    days = load_file(cli_args.report_file, cast(Mapping[str, Sequence[str]], {}))

    doc = OpenDocumentSpreadsheet()
    table = Table(parent=doc.spreadsheet, name=f"KW{effective_calendar_week}")

    headerstyle = Style(name="Header", family="table-cell")
    headerstyle.addElement(TextProperties(fontweight="bold", fontsize="12pt"))
    doc.styles.addElement(headerstyle)

    boldstyle = Style(name="Bold", family="table-cell")
    boldstyle.addElement(
        TextProperties(
            fontweight="bold",
        )
    )
    doc.styles.addElement(boldstyle)

    monospacestyle = Style(name="Monospace", family="table-cell")
    monospacestyle.addElement(TextProperties(fontfamily="Courier New", fontweight="medium"))

    doc.automaticstyles.addElement(monospacestyle)

    rowstyle = Style(name="RowHeight20", family="table-row")
    rowstyle.addElement(TableRowProperties(rowheight="20pt", useoptimalrowheight="false"))
    doc.automaticstyles.addElement(rowstyle)

    tr = TableRow(parent=table)

    for i, (title, width) in enumerate(
        (
            ("Started", 3),
            ("Duration", 3),
            ("In queue", 3),
            ("Build URL", 12),
            ("Reason", 2),
            ("Count", 2),
            ("Problem Ticket", 3),
            ("Details", 10),
            ("Verbatim", 40),
        )
    ):
        widthwide = Style(
            parent=doc.automaticstyles, name=f"header_style{i}", family="table-column"
        )
        widthwide.addElement(TableColumnProperties(columnwidth=f"{width}cm"))

        table.addElement(TableColumn(numbercolumnsrepeated=1, stylename=widthwide))
        TableCell(parent=tr, stylename=headerstyle).addElement(P(text=title))

    for day_str, builds in sorted(days.items()):
        tr = TableRow(parent=table, stylename=rowstyle)
        TableCell(parent=tr, stylename=boldstyle).addElement(P(text=day_str))
        for build in sorted(builds):
            timestamp, url, category, ticket, regex, family, line, duration, waiting_in_queue = (
                cast(Sequence[str], build)
            )
            details = family or regex
            assert url
            tr = TableRow(parent=table, stylename=rowstyle)
            TableCell(parent=tr).addElement(P(text=timestamp))
            TableCell(parent=tr).addElement(P(text=duration))
            TableCell(parent=tr).addElement(P(text=waiting_in_queue))
            p = P()
            p.addElement(A(href=url, text=url.replace("/job/", "/").split("/", maxsplit=3)[-1]))
            TableCell(parent=tr).addElement(p)
            TableCell(parent=tr).addElement(P(text=category if category != "unknown" else ""))
            TableCell(parent=tr)  # CNT
            p = P()
            if ticket := ticket.strip():
                p.addElement(A(href=f"https://jira.lan.tribe29.com/browse/{ticket}", text=ticket))
            TableCell(parent=tr).addElement(p)
            TableCell(parent=tr).addElement(P(text=details))
            TableCell(parent=tr, stylename=monospacestyle).addElement(
                P(text="".join(c for c in line or "" if c.isprintable()))
            )

    log().info("save spreadsheet to %s", cli_args.failed_builds_file)
    doc.save(cli_args.failed_builds_file)


def check_integrity(cli_args: Args):
    def implicit_cv(
        digest: FinishedBuildDigest, digests: Mapping[str, FinishedBuildDigest]
    ) -> bool:
        return (
            any(
                implicit_cv(parent, digests)
                for parent_id in digest.downstream_builds
                if (parent := digests.get(parent_id))
            )
            or digest.is_direct_cv()
        )

    def implicit_production(
        digest: FinishedBuildDigest, digests: Mapping[str, FinishedBuildDigest]
    ) -> bool:
        return (
            any(
                implicit_production(parent, digests)
                for parent_id in digest.downstream_builds
                if (parent := digests.get(parent_id))
            )
            or digest.is_direct_production()
        )

    def missing_downstream(
        digest: FinishedBuildDigest, digests: Mapping[str, FinishedBuildDigest]
    ) -> set[str]:
        return {
            parent_id for parent_id in digest.downstream_builds if parent_id not in digests
        }.union(
            *(
                missing_downstream(parent, digests)
                for parent_id in digest.downstream_builds
                if (parent := digests.get(parent_id))
            )
        )

    def downstream_builds(
        digest: FinishedBuildDigest, digests: Mapping[str, FinishedBuildDigest]
    ) -> list[str]:
        return [
            p
            for parent_id in digest.downstream_builds
            if (parent := digests.get(parent_id))
            for p in (parent_id, *downstream_builds(parent, digests))
        ]

    # digest: FinishedBuildDigest
    count_direct_cv = 0
    count_direct_production = 0
    count_implicit_cv = 0
    count_implicit_production = 0

    all_digest = {
        (digest := digest_from(digest_path)).build_id: digest
        for digest_path in cli_args.builds_dir.rglob(f"{DIGEST_FILENAME}")
    }

    for build_id, digest in all_digest.items():
        # continue
        gerrit_event_type = digest.parameters.get("GERRIT_EVENT_TYPE")
        gerrit_change_number = digest.parameters.get("GERRIT_CHANGE_NUMBER")
        causes = digest.causes
        is_replayed = any(c.startswith("Replayed #") for c in digest.causes)
        is_started_by_user = any(c.startswith("Started by user") for c in digest.causes)
        is_direct_cv = digest.is_direct_cv()
        is_direct_production = digest.is_direct_production()
        is_implicit_cv = implicit_cv(digest, all_digest)
        is_implicit_production = implicit_production(digest, all_digest)
        count_direct_cv += is_direct_cv
        count_direct_production += is_direct_production
        count_implicit_cv += is_implicit_cv
        count_implicit_production += is_implicit_production
        parent_builds = {
            parent_id: parent
            for parent_id in downstream_builds(digest, all_digest)
            if (parent := all_digest.get(parent_id))
        }

        params = digest.parameters

        if is_implicit_cv and is_direct_production:
            digest.is_direct_production()

        assert not is_implicit_cv or not is_direct_production, build_id

        if not (
            is_implicit_cv
            or is_implicit_production
            or is_started_by_user
            or (missing_downstream_builds := missing_downstream(digest, all_digest))
            or "/builders/" in digest.build_id
            or digest.build_id.startswith("Testing/")
        ):
            print(f"{build_id:<30} {causes}")
            if "checkmk/master/winagt-test-integration" in build_id:
                print(build_id)

        assert gerrit_event_type in {
            None,
            "comment-added",
            "patchset-created",
            "change-merged",
            "ref-updated",
        }, digest.parameters.get("GERRIT_EVENT_TYPE")
        assert all(
            any(
                s.startswith(p)
                for p in (
                    "Started by timer",
                    "Started by upstream project",
                    "Started by user",
                    "Retriggered by user",
                    "Replayed #",
                    "Triggered by Gerrit: ",
                    "Started by an SCM change",
                    # "Started by user",
                    "Rebuilds build #",
                )
            )
            for s in digest.causes
        ), digest.causes

        assert not is_direct_cv or not any(
            c.startswith(t) for t in ("Started by user",) for c in digest.causes
        )
        assert not is_direct_cv or any(
            c.startswith(t)
            for t in ("Triggered by Gerrit", "Retriggered by user")
            for c in digest.causes
        )
        assert not is_direct_cv or not is_direct_production

        # if any(c.startswith("Started by user") for c in self.causes):
        #    return False
        # if not (gerrit_event_type := self.parameters.get("GERRIT_EVENT_TYPE")):
        #    return False

        # return any(
        #    (c.startswith("Triggered by Gerrit") or c.startswith("Retriggered by user"))
        #    #and "in silent mode" not in c
        #    for c in digest.causes) and gerrit_event_type != "change-merged"

        # assert not (digest.is_direct_cv() and digest.is_direct_production())
        # assert (not digest.is_direct_cv()) or digest.causes[0].startswith("Triggered by Gerrit: ")
        my_cv = (gerrit_event_type in {"comment-added", "patchset-created"}) and not is_replayed
        # assert  (my_cv == is_direct_cv) or "cma/" in build_id
        cv_from_path = "/cv/" in digest.build_id or "/change_validation/" in digest.build_id
        # assert not cv_from_path or my_cv
        # assert "ref-updated" != gerrit_event_type
        # assert digest.is_direct_cv() == (gerrit_event_type in {"comment-added", "patchset-created", "xref-updated"})

    # if any(c.startswith("Started by user") for c in digest.causes):
    #    return False
    # if not (gerrit_event_type := self.parameters.get("GERRIT_EVENT_TYPE")):
    #    return False
    # r = any((c.startswith("Triggered by Gerrit") or c.startswith("Retriggered by user"))
    #        and "in silent mode" not in c for c in self.causes) and gerrit_event_type != "change-merged"
    # assert not r or len(self.causes) == 1, f"b {self.build_id} {self.causes}"
    # if ("checkmk/" in self.build_id and
    #    not "/2.2.0/" in self.build_id and
    #    not "builders/build-cmk-distro-package" in self.build_id and
    #    not "builders/trigger-cmk-distro-package" in self.build_id
    # ):
    #    if not self.causes[0].startswith("Started by upstream"):
    #        assert r == ("/cv/" in self.build_id or "/change_validation/" in self.build_id), f"a {self.build_id} {r}"
    # if r and self.parameters.get("GERRIT_EVENT_TYPE") not in {"comment-added", "patchset-created"}:
    #    print (self.build_id, self.parameters.get("GERRIT_EVENT_TYPE"))
    # return r
    print(
        f"{count_direct_cv=}, {count_direct_production=}, {count_implicit_cv=}, {count_implicit_production=} {count_implicit_cv + count_implicit_production}/{len(all_digest)}"
    )


def main() -> None:
    """See main docstring"""
    traceback.install()
    cli_args = parse_arguments()
    setup_logging(log(), level=cli_args.log_level, show_tid=True)
    # check_integrity(cli_args)
    # return

    with suppress(KeyboardInterrupt):
        if inspect.iscoroutinefunction(cli_args.func):
            asyncio.run(cli_args.func(cli_args))
        else:
            cli_args.func(cli_args)


if __name__ == "__main__":
    main()
