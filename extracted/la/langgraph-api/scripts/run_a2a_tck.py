#!/usr/bin/env python3

from __future__ import annotations

import argparse
import contextlib
import json
import logging
import os
import subprocess
import sys
import urllib.error
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

if TYPE_CHECKING:
    from collections.abc import Iterator

REPO_ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = REPO_ROOT / "a2a-conformance-baseline.yml"
TCK_REPO_URL = "https://github.com/a2aproject/a2a-tck.git"
TCK_REF = "5996b79f9cefa6fc390980e383e358a66fb9e49e"
TCK_CACHE_DIR = Path.home() / ".cache" / "a2a-tck"
TCK_REPORT_PATH = Path("reports") / "compatibility.json"
DEFAULT_BASE_URL = "http://localhost:9123"
DEFAULT_GRAPH_ID = "agent_simple"
DEFAULT_TRANSPORT = "jsonrpc"
ASSISTANT_NAME = "a2a-tck-compliance-agent"
ENTRY_FIELDS = frozenset({"id", "reason", "owner", "ticket"})
UNTRIAGED_PLACEHOLDER = "TODO"
HTTP_TIMEOUT_SECONDS = 30
PYTEST_TESTS_FAILED = 1

logger = logging.getLogger(__name__)


class RequirementStatus(StrEnum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"
    NOT_TESTED = "NOT TESTED"


class ConformanceError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class TckCheckout:
    ref: str
    root: Path

    def ensure(self) -> None:
        try:
            if (self.root / ".git").exists():
                self._git("fetch", "--tags", "origin")
            else:
                self.root.parent.mkdir(parents=True, exist_ok=True)
                _run(["git", "clone", TCK_REPO_URL, str(self.root)])
            self._git("reset", "--hard", self.ref)
            _run(["uv", "pip", "install", "-e", str(self.root)])
        except subprocess.CalledProcessError as error:
            detail = (error.stderr or b"").decode(errors="replace").strip()
            raise ConformanceError(
                f"Could not provision the TCK at {self.ref}: {detail}"
            ) from error

    def _git(self, *args: str) -> None:
        _run(["git", *args], cwd=self.root)


@dataclass(frozen=True, slots=True)
class ConformanceReport:
    failed: frozenset[str]
    passed: frozenset[str]
    skipped: frozenset[str]
    not_tested: frozenset[str] = frozenset()

    @property
    def unmeasured(self) -> frozenset[str]:
        return self.skipped | self.not_tested

    @property
    def measured(self) -> frozenset[str]:
        return self.passed | self.failed

    @classmethod
    def load(cls, path: Path) -> ConformanceReport:
        if not path.exists():
            raise ConformanceError(
                f"No compatibility report at {path}. The TCK writes one only when at least one "
                f"requirement was recorded, so an absent report means nothing ran — not that "
                f"everything passed."
            )
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ConformanceError(
                f"Compatibility report {path} is not valid JSON: {error}"
            ) from error
        per_requirement = document.get("per_requirement")
        if not per_requirement:
            raise ConformanceError(
                f"Compatibility report {path} recorded no requirements."
            )
        grouped: dict[RequirementStatus, set[str]] = {
            status: set() for status in RequirementStatus
        }
        for requirement_id, result in per_requirement.items():
            grouped[_status_of(requirement_id, result)].add(requirement_id)
        return cls(
            failed=frozenset(grouped[RequirementStatus.FAIL]),
            passed=frozenset(grouped[RequirementStatus.PASS]),
            skipped=frozenset(grouped[RequirementStatus.SKIPPED]),
            not_tested=frozenset(grouped[RequirementStatus.NOT_TESTED]),
        )


@dataclass(frozen=True, slots=True)
class BaselineEntry:
    id: str
    reason: str
    owner: str
    ticket: str


@dataclass(frozen=True, slots=True)
class Verdict:
    regressions: tuple[str, ...]
    stale: tuple[str, ...]
    unenforced: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not (self.regressions or self.stale or self.unenforced)


@dataclass(frozen=True, slots=True)
class Baseline:
    entries: tuple[BaselineEntry, ...]

    @classmethod
    def load(cls, path: Path) -> Baseline:
        if not path.exists():
            raise ConformanceError(f"Missing baseline file {path}.")
        document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        listed = document.get("expected_failures") or []
        return cls(
            tuple(_parse_entry(path, index, item) for index, item in enumerate(listed))
        )

    @property
    def requirement_ids(self) -> frozenset[str]:
        return frozenset(entry.id for entry in self.entries)

    def judge(self, report: ConformanceReport) -> Verdict:
        baselined = self.requirement_ids
        return Verdict(
            regressions=tuple(sorted(report.failed - baselined)),
            stale=tuple(sorted(report.passed & baselined)),
            unenforced=tuple(sorted(baselined - report.measured)),
        )


def _status_of(requirement_id: str, result: object) -> RequirementStatus:
    raw = result.get("status") if isinstance(result, Mapping) else None
    try:
        return RequirementStatus(raw)
    except ValueError as exc:
        raise ConformanceError(
            f"Unrecognised status {raw!r} for {requirement_id}. The TCK report format changed; "
            f"update this runner rather than ignoring the requirement."
        ) from exc


def _parse_entry(path: Path, index: int, item: object) -> BaselineEntry:
    label = f"{path.name} entry {index}"
    if not isinstance(item, Mapping):
        raise ConformanceError(f"{label} is not a mapping.")
    missing = sorted(ENTRY_FIELDS - set(item))
    if missing:
        raise ConformanceError(f"{label} is missing {', '.join(missing)}.")
    values = {field: str(item[field]).strip() for field in ENTRY_FIELDS}
    unfilled = sorted(
        field
        for field, value in values.items()
        if not value or value == UNTRIAGED_PLACEHOLDER
    )
    if unfilled:
        raise ConformanceError(
            f"{label} ({values['id'] or '?'}) leaves {', '.join(unfilled)} untriaged. "
            f"A baselined requirement needs a reason, an owner and a ticket."
        )
    return BaselineEntry(**values)


def _run(command: list[str], *, cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd, check=True, capture_output=True)


def _request(url: str, *, method: str, payload: dict[str, str] | None = None) -> bytes:
    body = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"} if body else {},
        method=method,
    )
    with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
        return response.read()


@contextlib.contextmanager
def sut_assistant(base_url: str, graph_id: str) -> Iterator[str]:
    try:
        created = json.loads(
            _request(
                f"{base_url}/assistants",
                method="POST",
                payload={"name": ASSISTANT_NAME, "graph_id": graph_id},
            )
        )
    except urllib.error.URLError as error:
        raise ConformanceError(
            f"Could not reach {base_url}. Start the server with 'make start' first."
        ) from error
    assistant_id = created["assistant_id"]
    logger.info("Created TCK assistant %s on graph %r", assistant_id, graph_id)
    try:
        yield assistant_id
    finally:
        try:
            _request(f"{base_url}/assistants/{assistant_id}", method="DELETE")
        except (urllib.error.URLError, OSError) as error:
            logger.warning(
                "Could not delete TCK assistant %s (%s). Delete it manually.",
                assistant_id,
                error,
            )
        else:
            logger.info("Deleted TCK assistant %s", assistant_id)


def invoke_tck(
    checkout: Path, *, sut_url: str, transport: str, level: str | None, verbose: bool
) -> None:
    (checkout / TCK_REPORT_PATH).unlink(missing_ok=True)
    command = [
        sys.executable,
        "run_tck.py",
        f"--sut-host={sut_url}",
        f"--transport={transport}",
    ]
    if level:
        command.append(f"--level={level}")
    if verbose:
        command.append("--verbose")
    logger.info("Running: %s", " ".join(command))
    completed = subprocess.run(command, cwd=checkout, check=False, env=os.environ)
    if completed.returncode > PYTEST_TESTS_FAILED:
        raise ConformanceError(
            f"The TCK exited {completed.returncode}, which means the run itself broke "
            f"rather than requirements failing. Nothing was measured."
        )


def propose_baseline(report: ConformanceReport) -> str:
    return yaml.safe_dump(
        {
            "expected_failures": [
                {
                    "id": requirement_id,
                    "reason": UNTRIAGED_PLACEHOLDER,
                    "owner": UNTRIAGED_PLACEHOLDER,
                    "ticket": UNTRIAGED_PLACEHOLDER,
                }
                for requirement_id in sorted(report.failed)
            ]
        },
        sort_keys=False,
    )


def describe(report: ConformanceReport, verdict: Verdict) -> str:
    total = len(report.measured | report.unmeasured)
    lines = [
        f"measured={len(report.measured)}/{total} "
        f"(passed={len(report.passed)} failed={len(report.failed)}) "
        f"unmeasured={len(report.unmeasured)} "
        f"(skipped={len(report.skipped)} not-tested={len(report.not_tested)})"
    ]
    if report.unmeasured:
        lines.append(
            f"{len(report.unmeasured)} of {total} requirements were never exercised, so any "
            f"pass rate here is computed over {len(report.measured)} requirements only."
        )
    for requirement_id in verdict.regressions:
        lines.append(f"REGRESSION {requirement_id} failed and is not in the baseline")
    for requirement_id in verdict.stale:
        lines.append(f"STALE {requirement_id} now passes - delete its baseline entry")
    for requirement_id in verdict.unenforced:
        lines.append(
            f"UNENFORCED {requirement_id} is baselined but was not measured, so its "
            f"entry proved nothing this run"
        )
    if verdict.ok:
        lines.append("Conformance gate passed.")
    return "\n".join(lines)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the A2A TCK and gate on the baseline"
    )
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--graph-id", default=DEFAULT_GRAPH_ID)
    parser.add_argument("--transport", default=DEFAULT_TRANSPORT)
    parser.add_argument("--level", choices=["must", "should", "may"], default=None)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--propose-baseline", action="store_true")
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    arguments = parse_arguments()
    base_url = arguments.base_url.rstrip("/")

    try:
        TckCheckout(ref=TCK_REF, root=TCK_CACHE_DIR).ensure()
        with sut_assistant(base_url, arguments.graph_id) as assistant_id:
            invoke_tck(
                TCK_CACHE_DIR,
                sut_url=f"{base_url}/a2a/{assistant_id}",
                transport=arguments.transport,
                level=arguments.level,
                verbose=arguments.verbose,
            )
            report = ConformanceReport.load(TCK_CACHE_DIR / TCK_REPORT_PATH)
        if arguments.propose_baseline:
            sys.stdout.write(propose_baseline(report))
            return 0
        verdict = Baseline.load(BASELINE_PATH).judge(report)
    except ConformanceError as error:
        sys.exit(str(error))

    logger.info("%s", describe(report, verdict))
    if arguments.level:
        logger.warning(
            "--level %s ran a subset of the suite, so the baseline was not fully "
            "exercised. The gate is not enforced for this run.",
            arguments.level,
        )
        return 0
    return 0 if verdict.ok else 1


if __name__ == "__main__":
    sys.exit(main())
