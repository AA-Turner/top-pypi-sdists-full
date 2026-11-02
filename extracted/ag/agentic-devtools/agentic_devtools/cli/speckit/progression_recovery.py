"""Evidence-based recovery of stranded SpecKit workflow dispatches."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from agentic_devtools.cli.ci.agent_assignment import _gh_api_call, _validate_repo_format
from agentic_devtools.cli.ci.credential_roles import require_default_repo_workflow_token
from agentic_devtools.cli.ci.retry import retry_with_backoff
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError
from agentic_devtools.cli.speckit.cloud_agent_guard import (
    _call_api,
    _cloud_agent_pr_matches,
    parse_cloud_agent_marker,
)


class ProgressionRecovery:
    """Inspect provider evidence, reserve one replay, or record a terminal failure.

    Reservations are written before dispatch so ambiguous API failures cannot
    cause repeated dispatches. An unfulfilled reservation becomes a terminal
    failure after two hours; processing is retained on every API error.
    """

    def __init__(
        self,
        repo: str,
        token: str,
        *,
        api_call: Callable[..., str] = _gh_api_call,
        now: datetime | None = None,
    ) -> None:
        normalized = _validate_repo_format(repo) if isinstance(repo, str) else None
        if (
            normalized is None
            or not re.fullmatch(r"[\w.-]+/[\w.-]+", normalized)
            or any(component in {".", ".."} for component in normalized.split("/"))
        ):
            raise ValueError("GITHUB_REPOSITORY must be in owner/repo format")
        if not isinstance(token, str) or not token.strip():
            raise ValueError("a workflow GitHub token is required")
        self.root = f"/repos/{normalized}"
        self.token = token.strip()
        self.api_call = api_call
        self.now = now or datetime.now(UTC)
        # Cache historical evidence, but re-read changes since this scan began
        # before every guard. The overlap covers GitHub's second-resolution dates.
        self._scan_since = (self.now - timedelta(seconds=1)).isoformat().replace("+00:00", "Z")
        self._pulls_cache: list[dict] | None = None
        self._runs_cache: list[dict] | None = None

    @staticmethod
    def _mapping(value: Any) -> dict:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise RuntimeError("invalid GitHub metadata object")
        return value

    @staticmethod
    def _text(value: Any) -> str:
        if value is None:
            return ""
        if not isinstance(value, str):
            raise RuntimeError("invalid GitHub metadata text")
        return value

    @staticmethod
    def _phase_was_superseded(requested: int, completed: int) -> bool:
        return completed > requested or (completed == requested and requested < 3)

    @staticmethod
    def _time(value: Any) -> datetime:
        if not isinstance(value, str):
            raise ValueError("missing durable processing timestamp")
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.tzinfo is None:
            raise ValueError("durable processing timestamp must include a timezone")
        return result

    @classmethod
    def _newest(cls, entries: list[dict], error: str) -> dict:
        """Select the newest entry, breaking same-second ``created_at`` ties on id.

        GitHub timestamps have second precision and the API lists older IDs first,
        so the timestamp alone would keep the older of two same-second entries.
        """
        for entry in entries:
            identity = entry.get("id")
            if isinstance(identity, bool) or not isinstance(identity, int) or identity <= 0:
                raise RuntimeError(error)
        return max(entries, key=lambda item: (cls._time(item.get("created_at")), item["id"]))

    @staticmethod
    def _trusted(comment: dict) -> bool:
        user = comment.get("user")
        return isinstance(user, dict) and user.get("login") in {"github-actions[bot]", "AMARSNIK_swica"}

    def _read(self, endpoint: str, key: str | None = None) -> Any:
        payload = _call_api(self.api_call, self.root + endpoint, token=self.token)
        decoder = json.JSONDecoder()
        documents = []
        rest = payload.strip()
        while rest:
            document, offset = decoder.raw_decode(rest)
            documents.append(document)
            rest = rest[offset:].strip()
        if not documents:
            raise RuntimeError("empty GitHub inspection response")
        if key == "object":
            if len(documents) != 1 or not isinstance(documents[0], dict):
                raise RuntimeError("invalid GitHub object response")
            return documents[0]
        rows = []
        for document in documents:
            items = document.get(key) if key and isinstance(document, dict) else document
            if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
                raise RuntimeError("invalid GitHub list response")
            rows.extend(items)
        return rows

    def _write(self, endpoint: str, method: str, body: dict | None = None) -> str:
        # Do not retry side effects: a transport failure may mean the write succeeded.
        return self.api_call(self.root + endpoint, method=method, body=body, token=self.token)

    def _cached_pulls(self) -> list[dict]:
        """Cache history and refresh every PR updated since this scan began."""
        if self._pulls_cache is None:
            self._pulls_cache = self._read("/pulls?state=all&per_page=100")
        else:
            pulls = {pr["number"]: pr for pr in self._pulls_cache}
            changed = self._read(f"/issues?state=all&since={self._scan_since}&per_page=100")
            for issue in changed:
                if "pull_request" in issue:
                    number = issue["number"]
                    pulls[number] = self._read(f"/pulls/{number}", "object")
            self._pulls_cache = list(pulls.values())
        return self._pulls_cache

    def _cached_runs(self) -> list[dict]:
        """Cache history, refreshing new runs and preexisting active runs."""
        if self._runs_cache is None:
            self._runs_cache = self._read(
                "/actions/workflows/speckit-phase-progression.yml/runs?per_page=100", "workflow_runs"
            )
        else:
            recent = self._read(
                f"/actions/workflows/speckit-phase-progression.yml/runs?created=%3E%3D{self._scan_since}&per_page=100",
                "workflow_runs",
            )
            # Reruns retain their original created_at, so the recent window alone
            # cannot reveal an old completed run becoming active again.
            for status in ("in_progress", "queued", "requested", "waiting", "pending"):
                recent.extend(
                    self._read(
                        f"/actions/workflows/speckit-phase-progression.yml/runs?status={status}&per_page=100",
                        "workflow_runs",
                    )
                )
            runs = {run["id"]: run for run in recent}
            for run in self._runs_cache:
                number = run["id"]
                if number not in runs:
                    runs[number] = (
                        self._read(f"/actions/runs/{number}", "object") if run["status"] != "completed" else run
                    )
            # Recent evidence first preserves the newest matching last_run_url.
            self._runs_cache = list(runs.values())
        return self._runs_cache

    def processing_issues(self) -> list[int]:
        """Return open processing issue numbers, excluding pull requests."""
        return [
            row["number"]
            for row in self._read("/issues?state=open&labels=speckit%3Aprocessing&per_page=100")
            if "pull_request" not in row
        ]

    @retry_with_backoff()
    def _root_issue(self, number: int) -> bool:
        owner, repo = self.root.removeprefix("/repos/").split("/")
        response = self._mapping(
            json.loads(
                self.api_call(
                    "/graphql",
                    method="POST",
                    body={
                        "query": (
                            "query($owner:String!,$repo:String!,$number:Int!){"
                            "repository(owner:$owner,name:$repo){issue(number:$number){parent{number}}}}"
                        ),
                        "variables": {"owner": owner, "repo": repo, "number": number},
                    },
                    token=self.token,
                )
            )
        )
        if response.get("errors"):
            raise RuntimeError("issue parent inspection failed")
        data = self._mapping(response.get("data"))
        repository = self._mapping(data.get("repository"))
        issue = self._mapping(repository.get("issue"))
        if "parent" not in issue:
            raise RuntimeError("issue parent inspection was incomplete")
        self._mapping(issue["parent"])
        return issue["parent"] is None

    def inspect(self, number: int) -> dict:
        """Read fresh issue, timeline, comments, phase PRs, and progression runs."""
        if isinstance(number, bool) or not isinstance(number, int) or number <= 0:
            raise ValueError("issue number must be a positive integer")
        issue = self._read(f"/issues/{number}", "object")
        if issue.get("number") != number or issue.get("state") not in {"open", "closed"}:
            raise RuntimeError("invalid issue identity/state response")
        labels = issue.get("labels")
        if not isinstance(labels, list) or not all(
            isinstance(label, dict) and isinstance(label.get("name"), str) for label in labels
        ):
            raise RuntimeError("invalid issue labels response")
        tree = self._read("/git/trees/main?recursive=1", "object")
        if tree.get("truncated") is not False or not isinstance(tree.get("tree"), list):
            raise RuntimeError("canonical spec tree inspection was incomplete")
        if not all(isinstance(entry, dict) and isinstance(entry.get("path"), str) for entry in tree["tree"]):
            raise RuntimeError("canonical spec tree contains invalid paths")
        spec_pattern = re.compile(rf"^specs/(?:.*/)?0*{number}(?:-[^/]+)?(?:/|$)")
        initial_state = not any(spec_pattern.match(entry["path"]) for entry in tree["tree"])
        return {
            "issue": issue,
            "labels": {label["name"] for label in labels},
            "initial_state": initial_state,
            "root_issue": self._root_issue(number),
            "events": self._read(f"/issues/{number}/events?per_page=100"),
            "comments": self._read(f"/issues/{number}/comments?per_page=100"),
            "pulls": self._cached_pulls(),
            "runs": self._cached_runs(),
        }

    def classify(self, evidence: dict) -> dict:
        """Make a secret-free decision using durable evidence, never updated_at."""
        issue = self._mapping(evidence["issue"])
        number = issue["number"]
        labels = evidence["labels"]
        result: dict[str, Any] = {"issue_number": number, "status": "skip", "reason": "inactive"}
        if issue.get("state") != "open" or "speckit:processing" not in labels or "speckit:completed" in labels:
            return result
        if any(label.startswith("speckit:agent-assigned-phase-") for label in labels):
            return {**result, "reason": "active-cloud-assignment"}
        if "speckit:agent-fallback" in labels:
            return {**result, "reason": "managed-by-agent-fallback-cleanup"}
        comments = [entry for entry in evidence["comments"] if self._trusted(entry)]
        cloud_markers = [
            entry
            for entry in comments
            if (marker := parse_cloud_agent_marker(entry.get("body"))) is not None and marker["issue"] == number
        ]
        if cloud_markers:
            assigned_at = max(self._time(entry.get("created_at")) for entry in cloud_markers)
            if self.now - assigned_at < timedelta(hours=2):
                return {**result, "reason": "recent-cloud-assignment-marker"}
        durable_dispatches = [
            entry for entry in comments if "speckit:progression-dispatch" in self._text(entry.get("body"))
        ]
        events = [
            event
            for event in evidence["events"]
            if event.get("event") == "labeled" and self._mapping(event.get("label")).get("name") == "speckit:processing"
        ]
        age_markers = durable_dispatches + cloud_markers
        if not events and not age_markers:
            raise RuntimeError("no durable speckit:processing label event or dispatch marker")
        event = self._newest(events or age_markers, "invalid processing label event identity")
        started = self._time(event.get("created_at"))
        epoch = str(event["id"]) if events else f"dispatch-{event['id']}"
        dispatches = [entry for entry in durable_dispatches if self._time(entry.get("created_at")) >= started]
        reason = "phase or required hierarchy/spec-directory inputs are not proven"
        inputs = None
        if dispatches:
            latest = self._newest(dispatches, "invalid durable dispatch marker identity")
            dispatch_matches = re.findall(
                r"<!-- speckit:progression-dispatch schema_version=1 (\{[^\n]*?\}) -->",
                latest["body"],
            )
            try:
                candidate = json.loads(dispatch_matches[0]) if len(dispatch_matches) == 1 else None
                inputs = self._validate_inputs(candidate, number)
            except ValueError, TypeError:
                reason = "trusted dispatch marker has malformed or incomplete inputs"
            started = max(started, self._time(latest["created_at"]))
            epoch += f"-dispatch-{latest['id']}"
            if inputs is not None and any(
                f"speckit:phase-{phase}-complete" in labels and self._phase_was_superseded(int(inputs["phase"]), phase)
                for phase in range(1, 6)
            ):
                inputs = None
                reason = "recorded dispatch phase is already complete"
        related = []
        pr_issues = {}
        for pr in evidence["pulls"]:
            head = self._mapping(pr.get("head"))
            marker = parse_cloud_agent_marker(pr.get("body"))
            source_issue = re.match(r"speckit/(\d+)/phase-([1-5])-", self._text(head.get("ref")))
            if isinstance(pr.get("number"), int):
                if marker:
                    pr_issues[pr["number"]] = int(marker["issue"])
                elif source_issue:
                    pr_issues[pr["number"]] = int(source_issue.group(1))
            branch = re.fullmatch(
                rf"speckit/{number}/phase-([1-5])-(specify|clarify|plan|tasks|analyze)",
                self._text(head.get("ref")),
            )
            relevant = (
                bool(branch)
                or (marker is not None and marker["issue"] == number)
                or bool(source_issue and int(source_issue.group(1)) == number)
            )
            if not relevant:
                continue
            # A PR only counts as phase evidence (and can clear a superseded recorded
            # dispatch below) when it was actually merged — which requires passing this
            # repository's own branch-protection/CI gates — or when it comes from the
            # trusted legacy author, or carries an authenticated Cloud Agent marker (bot
            # login, exact marker, and expected base branch). Otherwise any contributor
            # could open (and later close) a PR with a forged marker or phase branch name
            # to manufacture false phase evidence and get a stale issue marked failed.
            merged = bool(pr.get("merged_at")) or pr.get("merged") is True
            authenticated_marker = marker is not None and _cloud_agent_pr_matches(
                pr, issue_number=int(marker["issue"]), phase=int(marker["phase"])
            )
            if not (merged or self._trusted(pr) or authenticated_marker):
                continue
            related.append(pr)
            if inputs is not None and merged:
                merged_phase = int(marker["phase"]) if marker else int(cast(re.Match[str], source_issue).group(2))
                if self._phase_was_superseded(int(inputs["phase"]), merged_phase):
                    inputs = None
                    reason = "recorded dispatch phase is already merged or superseded"
            if pr.get("state") != "open" or (marker is None and branch is None):
                continue
            if marker:
                authoritative = bool(cloud_markers) and (
                    parse_cloud_agent_marker(
                        self._newest(cloud_markers, "invalid cloud assignment marker identity").get("body")
                    )
                    == marker
                )
                if authoritative and _cloud_agent_pr_matches(pr, issue_number=number, phase=int(marker["phase"])):
                    return {**result, "reason": "open-cloud-phase-pr"}
            else:
                branch = cast(re.Match[str], branch)
                phase = int(branch.group(1))
                expected_names = {1: "specify", 2: "clarify", 3: "plan", 4: "tasks", 5: "analyze"}
                pr_labels = {self._mapping(label)["name"] for label in pr.get("labels", [])}
                if (
                    branch.group(2) == expected_names[phase]
                    and f"speckit:phase-{phase}" in pr_labels
                    and self._trusted(pr)
                    and self._mapping(pr.get("base")).get("ref") == "main"
                ):
                    return {**result, "reason": "open-phase-pr"}
        last_run = None
        later_run = False
        linked_run_ids = {
            match
            for entry in comments
            for match in re.findall(
                rf"https://github\.com/{re.escape(self.root.removeprefix('/repos/'))}/actions/runs/(\d+)\b",
                self._text(entry.get("body")),
            )
        }
        related_pr_numbers = {pr["number"] for pr in related if isinstance(pr.get("number"), int)}
        for run in evidence["runs"]:
            title = self._text(run.get("display_title"))
            title_issue = re.search(r"\bissue #(\d+)\b", title, re.IGNORECASE)
            head_issue = re.match(r"speckit/(\d+)/", self._text(run.get("head_branch")))
            title_pr = re.search(r"\bPR #(\d+)\b", title, re.IGNORECASE)
            source_number = pr_issues.get(int(title_pr.group(1))) if title_pr else None
            matched = head_issue or title_issue
            matched_number = int(matched.group(1)) if matched else source_number
            run_prs = run.get("pull_requests", [])
            if not isinstance(run_prs, list):
                raise RuntimeError("invalid workflow run pull request metadata")
            linked = str(run.get("id")) in linked_run_ids or any(
                self._mapping(pr).get("number") in related_pr_numbers for pr in run_prs
            )
            referenced_issues = [pr_issues.get(self._mapping(pr).get("number")) for pr in run_prs]
            references_identified = bool(referenced_issues) and all(issue is not None for issue in referenced_issues)
            identified = matched_number is not None or references_identified
            matches = linked or matched_number == number or number in referenced_issues
            if matches and last_run is None:
                last_run = run.get("html_url")
            if matches and re.search(r"\bphase [2-5]\b", title):
                later_run = True
            if run.get("status") != "completed" and (matches or not identified):
                return {**result, "reason": "active-progression-run"}
        result.update(epoch=epoch, last_run_url=last_run)
        reservations = [
            entry
            for entry in comments
            if f"<!-- speckit:progression-recovery schema_version=1 epoch={epoch} " in self._text(entry.get("body"))
        ]
        if reservations:
            reserved = max(self._time(entry.get("created_at")) for entry in reservations)
            if self.now - reserved < timedelta(hours=2):
                return {**result, "reason": "recovery-already-reserved"}
            return {**result, "status": "failed", "reason": "prior recovery attempt did not produce live work"}
        if self.now - started < timedelta(hours=2):
            return {**result, "reason": "processing-is-recent"}
        phase_evidence = (
            related
            or later_run
            or any(label.startswith(("speckit:phase-", "speckit:level-", "speckit:agent-")) for label in labels)
            or any(
                entry.get("event") in {"labeled", "unlabeled"}
                and self._text(self._mapping(entry.get("label")).get("name")).startswith(
                    ("speckit:phase-", "speckit:agent-")
                )
                for entry in evidence["events"]
            )
            or bool(cloud_markers)
        )
        if (
            not dispatches
            and not phase_evidence
            and "speckit" in labels
            and evidence.get("initial_state") is True
            and evidence.get("root_issue") is True
            and self._trusted({"user": event.get("actor")})
        ):
            levels = labels & {"epic", "feature", "task"}
            issue_type = self._mapping(issue.get("type"))
            type_name = self._text(issue_type.get("name")).lower()
            if type_name in {"epic", "feature", "task"}:
                levels.add(type_name)
            if len(levels) == 1 and levels != {"task"}:
                inputs = {
                    "issue_number": str(number),
                    "phase": "1",
                    "hierarchy_level": next(iter(levels)),
                    "spec_dir": "",
                    "spec_context": "",
                }
        if inputs is None:
            if not dispatches and evidence.get("root_issue") is not True:
                reason = "initial issue has a parent or unknown parent context; exact dispatch inputs are missing"
            return {**result, "status": "failed", "reason": reason}
        return {**result, "status": "replay", "reason": "exact-dispatch-inputs", "inputs": inputs}

    @staticmethod
    def _validate_inputs(value: Any, number: int) -> dict[str, str]:
        old_keys = {"issue_number", "phase", "hierarchy_level", "spec_dir"}
        new_keys = old_keys | {"spec_context"}
        if not isinstance(value, dict) or set(value) not in (old_keys, new_keys):
            raise ValueError("dispatch input keys are incomplete")
        if not all(isinstance(item, str) for item in value.values()):
            raise ValueError("dispatch inputs must be strings")
        value = {**value, "spec_context": value.get("spec_context", "")}
        if value["issue_number"] != str(number) or value["phase"] not in {"1", "2", "3"}:
            raise ValueError("dispatch issue/phase mismatch")
        if value["hierarchy_level"] not in {"auto", "epic", "feature", "task"}:
            raise ValueError("dispatch hierarchy is not a valid workflow input")
        path = value["spec_dir"]
        if path and (
            not re.fullmatch(r"specs/[\w./-]+", path) or any(part in {"", ".", ".."} for part in path.split("/"))
        ):
            raise ValueError("spec directory must be a safe repository-relative path")
        spec_context = value["spec_context"]
        if spec_context and (
            not re.fullmatch(r"specs/[\w./-]+/spec\.md", spec_context)
            or any(part in {"", ".", ".."} for part in spec_context.split("/"))
        ):
            raise ValueError("spec context must be a safe repository-relative spec.md path")
        return value

    def _unchanged(
        self, number: int, decision: dict, reservation_id: int | None = None, reservation_marker: str = ""
    ) -> bool:
        evidence = self.inspect(number)
        if reservation_id is not None:
            competing = [
                entry
                for entry in evidence["comments"]
                if self._trusted(entry) and self._text(entry.get("body")).strip() == reservation_marker
            ]
            if not any(entry.get("id") == reservation_id for entry in competing):
                raise RuntimeError("recovery reservation could not be read back")
            if any(
                isinstance(entry.get("id"), bool) or not isinstance(entry.get("id"), int) or entry["id"] <= 0
                for entry in competing
            ):
                raise RuntimeError("invalid recovery reservation identity")
            reservation_ids = {entry["id"] for entry in competing}
            if reservation_id != min(reservation_ids):
                return False
            # Only the lowest-ID writer may ignore this epoch/input's competing
            # reservations; unrelated reservations and live-work guards remain.
            evidence["comments"] = [entry for entry in evidence["comments"] if entry.get("id") not in reservation_ids]
        current = self.classify(evidence)
        return (
            current["status"] in {"replay", "failed"}
            and current.get("epoch") == decision.get("epoch")
            and current.get("inputs") == decision.get("inputs")
            and current["reason"] == decision["reason"]
        )

    def recover(self, number: int) -> dict:
        """Recheck guards before writes and preserve processing on API failures."""
        decision = self.classify(self.inspect(number))
        if decision["status"] == "skip":
            return decision
        if not self._unchanged(number, decision):
            return {"issue_number": number, "status": "skip", "reason": "state-changed"}
        issue_path = f"/issues/{number}"
        if decision["status"] == "replay":
            digest = hashlib.sha256(json.dumps(decision["inputs"], sort_keys=True).encode()).hexdigest()
            marker = (
                f"<!-- speckit:progression-recovery schema_version=1 epoch={decision['epoch']} "
                f"inputs_sha256={digest} -->"
            )
            receipt = json.loads(self._write(issue_path + "/comments", "POST", {"body": marker}))
            if not isinstance(receipt, dict) or not isinstance(receipt.get("id"), int):
                raise RuntimeError("invalid recovery reservation response")
            if not self._unchanged(number, decision, receipt["id"], marker):
                return {"issue_number": number, "status": "skip", "reason": "state-changed"}
            self._write(
                "/actions/workflows/speckit-phase-progression.yml/dispatches",
                "POST",
                {"ref": "main", "inputs": decision["inputs"]},
            )
            return {**decision, "status": "replayed"}
        self._write(issue_path + "/labels", "POST", {"labels": ["speckit:failed"]})
        body = f"SpecKit recovery for issue #{number}: replay was not safe: {decision['reason']}."
        if decision.get("last_run_url"):
            body += f"\nLast observed progression run: {decision['last_run_url']}"
        self._write(issue_path + "/comments", "POST", {"body": body})
        if not self._unchanged(number, decision):
            return {"issue_number": number, "status": "skip", "reason": "state-changed"}
        self._write(issue_path + "/labels/speckit%3Aprocessing", "DELETE")
        return decision


def _error_reason(exc: Exception, token: str) -> str:
    """Describe a provider failure without leaking the workflow credential."""
    message = str(exc)
    if token:
        message = message.replace(token, "[redacted]")
    return f"{type(exc).__name__}: {message[:500]}"


def recover_stranded_progressions_command() -> None:
    """Scan processing issues and print JSON; fail if any issue inspection/write fails."""
    results = []
    token = ""
    try:
        token = os.environ.get("GITHUB_TOKEN", "").strip() or os.environ.get("GH_TOKEN", "").strip()
        token = token or require_default_repo_workflow_token("recover SpecKit progressions")
        worker = ProgressionRecovery(os.environ.get("GITHUB_REPOSITORY", ""), token)
        numbers = worker.processing_issues()
    except (RuntimeError, ValueError, TypeError, KeyError, RetryableError, ProviderRateLimitError) as exc:
        print(json.dumps([{"status": "error", "reason": _error_reason(exc, token)}]))
        sys.exit(1)
    for number in numbers:
        try:
            results.append(worker.recover(number))
        except (RuntimeError, ValueError, TypeError, KeyError, RetryableError, ProviderRateLimitError) as exc:
            results.append({"issue_number": number, "status": "error", "reason": _error_reason(exc, token)})
    print(json.dumps(results))
    if any(result["status"] == "error" for result in results):
        sys.exit(1)
