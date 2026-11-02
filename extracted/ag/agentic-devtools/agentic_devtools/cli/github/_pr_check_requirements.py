"""Private, fail-closed effective required-check evidence for a supplied PR snapshot."""

import json
import re
import subprocess
from urllib.parse import quote

from ..subprocess_utils import run_safe


def _resolve_required_checks(repo: str, base_branch: str, head_sha: str) -> dict:
    """Resolve effective rules and all check-run attempts for the supplied head.

    The caller must supply its current PR base branch and full head SHA. No PR
    state is fetched or changed here. ``complete`` certifies validated API
    evidence, not readiness. ``ready`` additionally requires every required
    (context, integration ID) pair and every actual newest run to be green.
    ``requiredChecks`` contains matching newest runs; ``checkRuns`` contains
    newest runs for all exact pairs, including non-required checks. Missing,
    blocking, or uncertain evidence is explained in ``diagnostics``.

    Positive integer integration IDs are recognized through exact matches to
    check-run app IDs, never through context-only matching or an app allowlist.
    Old attempts are retained only during validation and newest-run selection.
    """
    evidence: dict = {
        "ready": False,
        "complete": False,
        "repo": repo,
        "baseBranch": base_branch,
        "headSha": head_sha,
        "requiredChecks": [],
        "checkRuns": [],
        "diagnostics": [],
    }

    def require(valid: bool, diagnostic: str) -> None:
        if not valid:
            raise ValueError(diagnostic)

    def fetch_pages(endpoint: str) -> list:
        response = run_safe(
            ["gh", "api", endpoint, "--paginate", "--slurp"],
            capture_output=True,
            text=True,
            shell=False,
            timeout=60,
        )
        require(response.returncode == 0, f"{endpoint}: {response.stderr or f'exit code {response.returncode}'}")
        pages = json.loads(response.stdout)
        require(isinstance(pages, list) and bool(pages), f"{endpoint}: expected a non-empty slurped page array")
        return pages

    def validate_snapshot() -> None:
        require(
            isinstance(repo, str)
            and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9_.-][A-Za-z0-9_.-]*", repo) is not None
            and repo.split("/", 1)[1] not in {".", ".."},
            "Invalid repo: expected owner/repository",
        )
        require(
            isinstance(base_branch, str)
            and bool(base_branch)
            and base_branch != "@"
            and not re.search(r"[\x00-\x20\x7f~^:?*\\\[]|\.\.|@\{|//|^/|/$|\.$|^-", base_branch)
            and not any(part.startswith(".") or part.endswith(".lock") for part in base_branch.split("/")),
            "Missing or invalid base branch",
        )
        require(
            isinstance(head_sha, str) and re.fullmatch(r"[0-9a-fA-F]{40}", head_sha) is not None,
            "Missing or invalid full head SHA",
        )

    def parse_rules(pages: list) -> set[tuple[str, int]]:
        require(all(isinstance(page, list) for page in pages), "Malformed effective rules page: expected a list")
        rules = [rule for page in pages for rule in page]
        require(
            all(isinstance(rule, dict) and isinstance(rule.get("type"), str) and bool(rule["type"]) for rule in rules),
            "Malformed effective rule: expected a rule type",
        )
        parameters = [rule.get("parameters") for rule in rules if rule["type"] == "required_status_checks"]
        require(
            all(isinstance(p, dict) and isinstance(p.get("required_status_checks"), list) for p in parameters),
            "Malformed required_status_checks parameters",
        )
        requirements = [requirement for p in parameters for requirement in p["required_status_checks"]]
        require(
            all(
                isinstance(r, dict) and isinstance(r.get("context"), str) and bool(r["context"].strip())
                for r in requirements
            ),
            "Malformed required check context",
        )
        require(
            all(type(r.get("integration_id")) is int and r["integration_id"] > 0 for r in requirements),
            "Uncertain required check integration_id",
        )
        return {(r["context"], r["integration_id"]) for r in requirements}

    def parse_runs(pages: list) -> dict[tuple[str, int], dict]:
        require(all(isinstance(page, dict) for page in pages), "Malformed check-runs page: expected an object")
        require(
            all(type(page.get("total_count")) is int and page["total_count"] >= 0 for page in pages),
            "Malformed check-runs total_count",
        )
        total = pages[0]["total_count"]
        require(all(page["total_count"] == total for page in pages), "Inconsistent check-runs total_count across pages")
        require(all(isinstance(page.get("check_runs"), list) for page in pages), "Malformed check_runs list")
        runs = [run for page in pages for run in page["check_runs"]]
        require(all(isinstance(run, dict) for run in runs), "Malformed check-run object")
        require(
            all(
                type(run.get("id")) is int
                and run["id"] > 0
                and isinstance(run.get("name"), str)
                and bool(run["name"].strip())
                for run in runs
            ),
            "Malformed check-run ID or name",
        )
        require(all(run.get("head_sha") == head_sha for run in runs), "Check-run is not bound to supplied head")
        require(
            all(
                isinstance(run.get("app"), dict) and type(run["app"].get("id")) is int and run["app"]["id"] > 0
                for run in runs
            ),
            "Uncertain check-run integration_id",
        )
        by_id = {run["id"]: run for run in runs}
        require(all(by_id[run["id"]] == run for run in runs), "Conflicting payloads for duplicate check-run ID")
        require(
            len(by_id) == total,
            f"Incomplete check-run evidence: received {len(by_id)} distinct IDs, advertised {total}",
        )
        # Ascending numeric IDs ensure the final assignment for each pair is its newest attempt.
        return {(run["name"], run["app"]["id"]): run for run in sorted(by_id.values(), key=lambda run: run["id"])}

    try:
        validate_snapshot()
        prefix = f"/repos/{repo}"
        required = parse_rules(fetch_pages(f"{prefix}/rules/branches/{quote(base_branch, safe='')}?per_page=100"))
        newest = parse_runs(fetch_pages(f"{prefix}/commits/{head_sha}/check-runs?per_page=100&filter=all"))
        evidence["complete"] = True
        evidence["checkRuns"] = list(newest.values())
        evidence["requiredChecks"] = [newest[pair] for pair in sorted(required) if pair in newest]
        evidence["diagnostics"] = [
            f"Missing required check {name!r} with integration_id {integration}"
            for name, integration in sorted(required - newest.keys())
        ] + [
            f"Blocking check {name!r} integration_id {integration}, run {run['id']}: "
            f"status={run.get('status')!r}, conclusion={run.get('conclusion')!r}"
            for (name, integration), run in newest.items()
            if run.get("status") != "completed" or run.get("conclusion") not in ("success", "neutral", "skipped")
        ]
        evidence["ready"] = not evidence["diagnostics"]
    except (OSError, subprocess.SubprocessError, ValueError, TypeError) as exc:
        evidence["diagnostics"].append(f"Required-check resolution failed: {exc}")
    return evidence
