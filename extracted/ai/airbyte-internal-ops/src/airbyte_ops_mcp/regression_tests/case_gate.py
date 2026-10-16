# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""The static half of the gate that lets a reproduction-case PR merge unreviewed.

A case PR merges without human review once `sandbox-case-validate.yml` has
run this gate and reproduced the case, so the gate -- not a reviewer -- keeps
a bad case off `main`. It answers `n/a` for a PR that touches no case, `pass`
or `fail`:

1. **Scope**: the PR only adds regular files with known case file names, all
   inside one new `regression_cases/<connector>/<case>/` directory. Changing
   an existing case needs a human, or a later fix could weaken the case it is
   judged by.
2. **Shape**: the case loads; its `origin.json` names a published release of
   airbytehq/airbyte whose source is at `affected_ref`, a commit on `master`;
   the sandbox validates `sandbox/` offline; and the static support check says
   the twin covers the catalog's streams at `affected_ref`.

The case is read from git objects at the PR head, never from a working tree,
so the gate's own code can come from a checkout of `main`.

The reproduction itself needs the sandbox and Docker, so it is a case run with
goal `reproduced`: both the affected release and its unmodified source must
violate the case.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal, NamedTuple

from airbyte_ops_mcp.github_api import is_commit_ancestor_of
from airbyte_ops_mcp.regression_tests.repro_case import (
    IMAGE_PATTERN,
    SANDBOX_COMMAND_TIMEOUT_SECONDS,
    SHA_PATTERN,
    CaseOrigin,
    ReproCase,
    check_case_origin,
)
from airbyte_ops_mcp.regression_tests.sandbox_support import (
    SandboxDiscovery,
    connector_files,
    manifest_stream_names,
    run_sandbox_support_check,
)

CASES_DIR = "regression_cases"
# The only files a case may hold, relative to its directory.
CASE_FILES = frozenset(
    {
        "sandbox/dataset.json",
        "sandbox/behavior.json",
        "config.template.json",
        "catalog.json",
        "state.json",
        "expectations.json",
        "origin.json",
    }
)
REGULAR_FILE_MODE = "100644"
# The saas-sandbox commit the workflows run, relative to the code checkout.
SANDBOX_PIN_FILE = ".github/saas-sandbox-ref"
# Cases reproduce bugs in public airbytehq/airbyte connectors only: their
# `affected_ref` is built from source, so it must be a reviewed commit.
TRUSTED_REPO = "airbyte"
TRUSTED_BRANCH = "master"
NAME_PATTERN = re.compile(r"[A-Za-z0-9_-]+")

GateStatus = Literal["n/a", "pass", "fail"]
OriginChecker = Callable[[CaseOrigin, str], list[str]]
AncestorCheck = Callable[[str, str, str, str, str | None], bool]


class Change(NamedTuple):
    """One entry of `git diff --raw`: status letter, new file mode, path."""

    status: str
    mode: str
    path: str


@dataclass
class GateReport:
    status: GateStatus
    connector: str | None = None
    case: str | None = None
    case_dir: str | None = None
    affected_image: str | None = None
    affected_ref: str | None = None
    problems: list[str] = field(default_factory=list)
    support: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _git(repo_dir: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo_dir), *arguments],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def changed_paths(repo_dir: Path, base_ref: str, head_ref: str) -> list[Change]:
    """Every change `head_ref` makes since its merge base with `base_ref`."""
    fields = _git(
        repo_dir,
        "diff",
        "--raw",
        "-z",
        "--no-renames",
        "--no-abbrev",
        f"{base_ref}...{head_ref}",
    ).split("\0")
    changes = []
    # `-z` output alternates `:<old mode> <new mode> <old sha> <new sha> <status>`
    # and the path, so a path cannot smuggle in a fake entry.
    for meta, path in zip(fields[0::2], fields[1::2], strict=False):
        if not meta:
            break
        _, new_mode, _, _, status = meta.lstrip(":").split(" ")
        changes.append(Change(status[:1], new_mode, path))
    return changes


def exists_at(repo_dir: Path, ref: str, path: str) -> bool:
    return bool(_git(repo_dir, "ls-tree", ref, "--", path).strip())


def merge_bases(repo_dir: Path, base_ref: str, head_ref: str) -> list[str]:
    return _git(repo_dir, "merge-base", "--all", base_ref, head_ref).split()


def case_problems(
    connector: str, case: str, relative_paths: Sequence[str]
) -> list[str]:
    """Bad names, and files a case may not hold (paths relative to the case)."""
    problems = [
        f"{name!r} is not a valid name ([A-Za-z0-9_-]+)"
        for name in (connector, case)
        if not NAME_PATTERN.fullmatch(name)
    ]
    unknown = sorted(path for path in relative_paths if path not in CASE_FILES)
    if unknown:
        problems.append(
            "files a case may not hold: "
            + ", ".join(unknown)
            + f" (allowed: {', '.join(sorted(CASE_FILES))})"
        )
    return problems


def _has_control_characters(path: str) -> bool:
    return any(ord(char) < 32 or ord(char) == 127 for char in path)


def case_scope(
    changes: Sequence[Change], exists_at_base: Callable[[str], bool]
) -> tuple[str | None, str | None, list[str]]:
    """The `(connector, case)` a PR adds, or why it is not a single new case.

    Returns no case and no problems for a PR that touches no case at all.
    """
    # Problems quote paths into logs and a PR comment; a newline in one could
    # forge a workflow command there.
    odd_paths = [c.path for c in changes if _has_control_characters(c.path)]
    if odd_paths:
        return (
            None,
            None,
            ["paths with control characters: " + ", ".join(map(repr, odd_paths))],
        )
    in_cases = [c for c in changes if c.path.startswith(f"{CASES_DIR}/")]
    if not in_cases:
        return None, None, []
    problems = []
    others = sorted(c.path for c in changes if not c.path.startswith(f"{CASES_DIR}/"))
    if others:
        problems.append(
            "a case PR may only add a case, but it also changes " + ", ".join(others)
        )
    cases = {tuple(c.path.split("/")[1:3]) for c in in_cases if c.path.count("/") >= 3}
    loose = sorted(c.path for c in in_cases if c.path.count("/") < 3)
    if loose:
        problems.append(
            f"files outside a {CASES_DIR}/<connector>/<case>/ directory: "
            + ", ".join(loose)
        )
    if len(cases) != 1:
        problems.append(f"a case PR must add exactly one case, not {len(cases)}")
        return None, None, problems
    ((connector, case),) = cases
    prefix = f"{CASES_DIR}/{connector}/{case}/"
    problems += case_problems(
        connector,
        case,
        [c.path.removeprefix(prefix) for c in in_cases if c.path.startswith(prefix)],
    )
    not_added = sorted(f"{c.path} ({c.status})" for c in in_cases if c.status != "A")
    if not_added:
        problems.append(
            "a case PR may only add files; changing a case needs human review: "
            + ", ".join(not_added)
        )
    # Symlinks (120000), executables (100755) and submodules (160000) are
    # refused: a case is data only.
    odd_modes = sorted(
        f"{c.path} ({c.mode})"
        for c in in_cases
        if c.status == "A" and c.mode != REGULAR_FILE_MODE
    )
    if odd_modes:
        problems.append(
            f"case files must be regular files (mode {REGULAR_FILE_MODE}): "
            + ", ".join(odd_modes)
        )
    if exists_at_base(f"{CASES_DIR}/{connector}/{case}"):
        problems.append(
            f"{CASES_DIR}/{connector}/{case} already exists on the base branch; "
            "changing a case needs human review"
        )
    return connector, case, problems


def extract_case(repo_dir: Path, ref: str, case_path: str, destination: Path) -> None:
    """Write the regular files under `case_path` at `ref` into `destination`.

    Reads git objects directly instead of `git archive`, whose
    `.gitattributes` handling (`export-ignore`, `export-subst`) could make the
    gate check different bytes than the ones that merge.
    """
    entries = _git(repo_dir, "ls-tree", "-r", "-z", ref, "--", case_path).split("\0")
    for entry in filter(None, entries):
        meta, _, path = entry.partition("\t")
        mode, kind, sha = meta.split(" ")
        if kind != "blob" or mode != REGULAR_FILE_MODE:
            raise ValueError(f"{path} is not a regular file (mode {mode})")
        target = destination / path.removeprefix(f"{case_path}/")
        target.parent.mkdir(parents=True, exist_ok=True)
        blob = subprocess.run(
            ["git", "-C", str(repo_dir), "cat-file", "blob", sha], capture_output=True
        )
        if blob.returncode != 0:
            raise ValueError(
                f"could not read {path}: {blob.stderr.decode(errors='replace').strip()}"
            )
        target.write_bytes(blob.stdout)


def trusted_origin_problems(
    origin: CaseOrigin,
    connector_name: str,
    token: str | None,
    *,
    check_origin: Callable[[CaseOrigin, str, str | None], list[str]] = (
        check_case_origin
    ),
    is_ancestor: AncestorCheck = is_commit_ancestor_of,
) -> list[str]:
    """`check_case_origin`, plus the trust rules for a case that merges unreviewed."""
    if origin.repo != TRUSTED_REPO:
        return [
            f"origin.json `repo` is {origin.repo!r}; only {TRUSTED_REPO!r} "
            "cases merge without review"
        ]
    problems = check_origin(origin, connector_name, token)
    if not is_ancestor(
        "airbytehq", origin.repo, origin.affected_ref, TRUSTED_BRANCH, token
    ):
        problems.append(
            f"affected_ref {origin.affected_ref} is not on "
            f"airbytehq/{origin.repo} {TRUSTED_BRANCH}"
        )
    return problems


def read_sandbox_pin(path: Path) -> str:
    """The pinned saas-sandbox commit; raises `ValueError` if it is not one SHA."""
    try:
        pin = path.read_text().strip()
    except OSError as exc:
        raise ValueError(f"cannot read the saas-sandbox pin {path}: {exc}") from exc
    if not SHA_PATTERN.fullmatch(pin):
        raise ValueError(f"{path} must hold one full 40-character commit SHA")
    return pin


def sandbox_ref_problems(origin: CaseOrigin, sandbox_ref: str) -> list[str]:
    """Whether the case was validated on the saas-sandbox commit the runs use.

    Every refusal starts with `origin.json sandbox_ref`, so an author can tell
    "refresh against the current pin and retry" from a broken case.
    """
    if origin.sandbox_ref is None:
        return [
            "origin.json sandbox_ref is missing; set it to the current "
            f"saas-sandbox pin {sandbox_ref}"
        ]
    if origin.sandbox_ref != sandbox_ref:
        return [
            f"origin.json sandbox_ref {origin.sandbox_ref} is not the current "
            f"saas-sandbox pin {sandbox_ref}"
        ]
    return []


def sandbox_input_problems(case: ReproCase, executable: str = "sandbox") -> list[str]:
    """Validate the case's sandbox files offline with the installed CLI."""
    resolved = shutil.which(executable)
    if resolved is None:
        return [f"`{executable}` CLI not found on PATH"]
    checks = [("dataset", case.dataset_path)]
    if case.behavior_path is not None:
        checks.append(("behavior", case.behavior_path))
    problems = []
    for kind, path in checks:
        try:
            result = subprocess.run(
                [resolved, kind, "validate", str(path)],
                capture_output=True,
                text=True,
                timeout=SANDBOX_COMMAND_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            problems.append(
                f"{path.relative_to(case.directory)} could not be validated: {exc}"
            )
            continue
        if result.returncode != 0:
            reason = (result.stderr or result.stdout).strip().splitlines()
            problems.append(
                f"{path.relative_to(case.directory)} is invalid: "
                + (reason[-1] if reason else f"exit {result.returncode}")
            )
    return problems


def _case_config(case: ReproCase) -> tuple[dict[str, Any], list[str]]:
    """The case's connector config, which decides the hosts read from config."""
    try:
        config = json.loads(case.config_template_path.read_text())
    except (OSError, ValueError) as exc:
        return {}, [f"config.template.json cannot be read: {exc}"]
    if not isinstance(config, dict):
        return {}, ["config.template.json is not a JSON object"]
    return config, []


def _catalog_streams(case: ReproCase) -> list[str]:
    catalog = json.loads(case.catalog_path.read_text())
    return [entry["stream"]["name"] for entry in catalog.get("streams", [])]


def check_case(
    case_dir: Path,
    connector: str,
    *,
    check_origin: OriginChecker,
    sandbox_ref: str,
    connector_dir: Path | None = None,
    discovery: SandboxDiscovery | None = None,
) -> GateReport:
    """The shape checks for one case directory; `sandbox_ref` is the pin."""
    report = GateReport(
        status="fail", connector=connector, case=case_dir.name, case_dir=str(case_dir)
    )
    try:
        case = ReproCase.load(case_dir)
    except ValueError as exc:
        report.problems.append(str(exc))
        return report
    if case.origin is None:
        report.problems.append("origin.json is required for a case that auto-merges")
    else:
        report.affected_image = case.origin.affected_image
        report.affected_ref = case.origin.affected_ref
        report.problems += sandbox_ref_problems(case.origin, sandbox_ref)
        try:
            report.problems += check_origin(case.origin, connector)
        # Fail closed: an origin that could not be confirmed does not pass.
        except Exception as exc:
            report.problems.append(f"could not check origin.json: {exc}")
    report.problems += sandbox_input_problems(case)
    if case.origin is not None:
        ref = case.origin.affected_ref
        new_streams = list(case.expectations.new_streams)
        files = None
        if new_streams:
            try:
                files = connector_files(connector, ref, connector_dir)
            # Fail closed: an absence that could not be confirmed does not pass.
            except Exception as exc:
                report.problems.append(
                    f"could not read the connector at {ref} for new_streams: {exc}"
                )
            else:
                report.problems += new_stream_problems(new_streams, ref, *files)
        # The affected release defines no requests for a new stream to check.
        streams = [s for s in _catalog_streams(case) if s not in new_streams]
        check = case.expectations.command == "check"
        config, config_problems = _case_config(case)
        report.problems += config_problems
        support = run_sandbox_support_check(
            connector_name=connector,
            streams=streams,
            connector_dir=connector_dir,
            ref=ref,
            discovery=discovery,
            check_streams=check,
            # A CHECK reads its own streams, whatever the catalog configures.
            host_only=not streams and not check,
            files=files,
            config=config,
        )
        if new_streams:
            # Neither this check nor the `reproduced` runs (both on the affected
            # release) exercise the twin for them; a later fix run decides.
            support["new_streams_unchecked"] = new_streams
        report.support = support
        if support["result"] != "supported":
            report.problems.append(
                f"the static support check says {support['result']}: "
                + "; ".join(support.get("reasons") or ["no reason given"])
            )
    report.status = "fail" if report.problems else "pass"
    return report


def new_stream_problems(
    new_streams: Sequence[str],
    affected_ref: str,
    metadata: dict[str, Any],
    manifest: dict[str, Any] | None,
) -> list[str]:
    """Why the declared new streams are not confirmed absent from the affected release.

    A side that shows no sign of a declared stream violates the case, so the
    declaration must be true: the stream is not in the manifest at
    `affected_ref`, and the connector defines no streams outside it.
    """
    try:
        defined = manifest_stream_names(metadata, manifest)
    # Fail closed: a manifest that does not resolve confirms nothing.
    except Exception as exc:
        return [f"new_streams cannot be confirmed at {affected_ref}: {exc}"]
    if defined is None:
        return [
            f"new_streams needs a manifest-only connector at {affected_ref} to "
            "confirm the affected release does not define them"
        ]
    return [
        f"new_streams names {stream!r}, which the manifest at {affected_ref} defines"
        for stream in new_streams
        if stream in defined
    ]


def _default_origin_checker(github_token: str | None) -> OriginChecker:
    return lambda origin, connector: trusted_origin_problems(
        origin, connector, github_token
    )


def run_case_gate(
    repo_dir: Path,
    base_ref: str,
    head_ref: str = "HEAD",
    *,
    sandbox_ref: str,
    require_case: bool = False,
    github_token: str | None = None,
    connector_dir: Path | None = None,
    check_origin: OriginChecker | None = None,
    discovery: SandboxDiscovery | None = None,
) -> GateReport:
    """Scope, then shape, for the case a PR adds; it is read at `head_ref`."""
    bases = merge_bases(repo_dir, base_ref, head_ref)
    if len(bases) != 1:
        # With several merge bases, the diff against one of them need not be
        # what the squash merge changes.
        return GateReport(
            status="fail",
            problems=[f"{head_ref} has {len(bases)} merge bases with {base_ref}"],
        )
    connector, case, problems = case_scope(
        changed_paths(repo_dir, base_ref, head_ref),
        # A case deleted on the base since the PR branched still exists at the
        # merge base, and adding to it would land a partial case.
        lambda path: any(exists_at(repo_dir, ref, path) for ref in (base_ref, *bases)),
    )
    if connector is None and not problems:
        if require_case:
            return GateReport(status="fail", problems=["the PR adds no case"])
        return GateReport(status="n/a")
    if connector is None or case is None or problems:
        return GateReport(
            status="fail", connector=connector, case=case, problems=problems
        )
    case_path = f"{CASES_DIR}/{connector}/{case}"
    with tempfile.TemporaryDirectory() as scratch:
        case_dir = Path(scratch) / case
        try:
            extract_case(repo_dir, head_ref, case_path, case_dir)
        except ValueError as exc:
            return GateReport(
                status="fail", connector=connector, case=case, problems=[str(exc)]
            )
        report = check_case(
            case_dir,
            connector,
            check_origin=check_origin or _default_origin_checker(github_token),
            sandbox_ref=sandbox_ref,
            connector_dir=connector_dir,
            discovery=discovery,
        )
    report.case_dir = case_path
    return report


def run_case_dir_gate(
    case_dir: Path,
    *,
    sandbox_ref: str,
    github_token: str | None = None,
    connector_dir: Path | None = None,
    check_origin: OriginChecker | None = None,
    discovery: SandboxDiscovery | None = None,
) -> GateReport:
    """The shape checks for a case directory on disk, without a PR's scope.

    The connector is the name of the directory holding the case, as in
    `regression_cases/<connector>/<case>/`.
    """
    linked = case_dir.is_symlink()
    case_dir = case_dir.resolve()
    connector = case_dir.parent.name
    entries = list(case_dir.rglob("*"))
    problems = case_problems(
        connector,
        case_dir.name,
        [path.relative_to(case_dir).as_posix() for path in entries if path.is_file()],
    )
    links = sorted(
        path.relative_to(case_dir).as_posix() for path in entries if path.is_symlink()
    )
    if linked:
        links.insert(0, ".")
    if links:
        problems.append("case files must not be symlinks: " + ", ".join(links))
    if problems:
        return GateReport(
            status="fail",
            connector=connector,
            case=case_dir.name,
            case_dir=str(case_dir),
            problems=problems,
        )
    return check_case(
        case_dir,
        connector,
        check_origin=check_origin or _default_origin_checker(github_token),
        sandbox_ref=sandbox_ref,
        connector_dir=connector_dir,
        discovery=discovery,
    )


_OUTPUT_PATTERNS = {
    "connector": NAME_PATTERN,
    "case": NAME_PATTERN,
    "affected_image": IMAGE_PATTERN,
    "affected_ref": SHA_PATTERN,
}


def gate_step_outputs(report: GateReport) -> dict[str, str]:
    """The report as GitHub step outputs that PR content cannot forge.

    `GITHUB_OUTPUT` is parsed line by line, so a newline in a value could add
    an output. Scalars must match their pattern (else they are left empty),
    `problems` is one JSON line, and `status` comes last so nothing written
    before it can override it.
    """
    outputs: dict[str, str] = {}
    for key, pattern in _OUTPUT_PATTERNS.items():
        value = getattr(report, key)
        outputs[key] = value if value and pattern.fullmatch(value) else ""
    outputs["problems"] = json.dumps(report.problems)
    outputs["status"] = report.status
    return outputs
