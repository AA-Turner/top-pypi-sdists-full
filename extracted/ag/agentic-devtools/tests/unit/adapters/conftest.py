"""Shared provider-agnostic fixtures for adapter unit tests.

Provides reusable fixtures that any adapter test module can request without
duplicating setup. Provider-specific fixtures belong in provider subdirectory
conftest files (e.g., ``github_adapter/conftest.py``).
"""

from __future__ import annotations

import json
import re
import subprocess
from typing import Any, cast

import pytest
import requests

from agentic_devtools.adapters.base import IssueDetailWithRaw, NormalizedIssue
from agentic_devtools.adapters.github_provider import GitHubProvider
from tests.unit.adapters.mock_adapter import MockAdapter


@pytest.fixture()
def mock_adapter() -> MockAdapter:
    """Return a default MockAdapter instance with no overrides."""
    return MockAdapter()


@pytest.fixture()
def sample_issue_data() -> IssueDetailWithRaw:
    """Return a canonical IssueDetailWithRaw for assertions and normalize input."""
    return IssueDetailWithRaw(
        issue_id="SAMPLE-1",
        title="Sample issue for testing",
        description="A detailed description of the sample issue.",
        status="open",
        labels=["enhancement", "test"],
        url="https://example.test/issues/SAMPLE-1",
        comments=[],
        provider="mock",
    )


@pytest.fixture()
def sample_normalized_issue() -> NormalizedIssue:
    """Return a pre-built NormalizedIssue for assertion targets."""
    return NormalizedIssue(
        issue_id="SAMPLE-1",
        title="Sample issue for testing",
        description="A detailed description of the sample issue.",
        status="open",
        url="https://example.test/issues/SAMPLE-1",
        provider="mock",
        labels=["enhancement", "test"],
        comments=[],
    )


# ======================================================================
# Stateful fake `gh` CLI backend for the shared GitHub contract leg
# ======================================================================


class _FakeGitHubBackend:
    """A stateful in-memory emulation of the subset of ``gh api`` calls that
    ``GitHubProvider`` issues.  Backs the ``run_command`` callable so the shared
    provider-contract scenarios can exercise the full create/resolve/link/label
    flow without any real subprocess or network access.
    """

    def __init__(self, owner_repo: str = "org/repo") -> None:
        self.owner_repo = owner_repo
        self.issues: dict[str, dict[str, Any]] = {}
        self._next_number = 1
        self._next_db = 1000
        self.call_count = 0
        # parent_number -> set of child integer database IDs
        self.sub_issues: dict[str, set[int]] = {}
        # set of (issue_db_id, blocked_by_db_id) integer pairs for blocked-by idempotency
        self.dependencies: set[tuple[int, int]] = set()

    # -- subprocess-compatible entry point --

    def run(
        self,
        args: list[str],
        capture_output: bool = True,
        text: bool = True,
        shell: bool = False,
        input: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        self.call_count += 1
        return self._route(list(args), input)

    # -- routing --

    def _route(self, args: list[str], input_str: str | None) -> subprocess.CompletedProcess[str]:
        if "/search/issues" in args:
            return self._search(args)

        method = args[args.index("--method") + 1] if "--method" in args else "GET"
        path = next((a for a in args if a.startswith("/repos/")), "")

        if path.endswith("/issues") and method == "POST":
            return self._create(input_str)
        if path.endswith("/sub_issues"):
            parent = path.split("/")[-2]
            if method == "POST":
                return self._add_sub_issue(parent, input_str)
            return self._get_sub_issues(parent)
        if path.endswith("/dependencies/blocked_by") and method == "POST":
            issue_number = path.split("/")[-3]
            return self._add_blocked_by(issue_number, input_str)
        if path.endswith("/labels"):
            number = path.split("/")[-2]
            if method == "POST":
                return self._add_labels(number, input_str)
            return self._get_labels(number)
        number = path.split("/")[-1]
        if method == "PATCH" and path.endswith(f"/issues/{number}"):
            return self._patch_issue(number, input_str)
        return self._resolve(number)

    # -- handlers --

    def _create(self, input_str: str | None) -> subprocess.CompletedProcess[str]:
        payload = json.loads(input_str) if input_str else {}
        number = str(self._next_number)
        self._next_number += 1
        db = self._next_db
        self._next_db += 1
        node_id = f"I_kwDO{db}"
        url = f"https://github.com/{self.owner_repo}/issues/{number}"
        labels = set(payload.get("labels", []) or [])
        self.issues[number] = {
            "id": db,
            "node_id": node_id,
            "labels": labels,
            "body": payload.get("body", ""),
            "html_url": url,
        }
        return self._resp({"number": int(number), "html_url": url, "id": db, "node_id": node_id})

    def _get_sub_issues(self, parent: str) -> subprocess.CompletedProcess[str]:
        child_db_ids = self.sub_issues.get(parent, set())
        items: list[dict[str, Any]] = []
        for num, data in self.issues.items():
            if data["id"] in child_db_ids:
                items.append({"id": data["id"], "number": int(num), "node_id": data["node_id"]})
        return self._resp(items)

    def _add_sub_issue(self, parent: str, input_str: str | None) -> subprocess.CompletedProcess[str]:
        payload = json.loads(input_str) if input_str else {}
        child_db_id = payload.get("sub_issue_id", 0)
        existing = self.sub_issues.setdefault(parent, set())
        existing.add(int(child_db_id))
        return self._resp({})

    def _add_blocked_by(self, issue_number: str, input_str: str | None) -> subprocess.CompletedProcess[str]:
        """Handle POST /repos/.../issues/{number}/dependencies/blocked_by idempotently."""
        payload = json.loads(input_str) if input_str else {}
        blocked_by_db_id = int(payload.get("issue_id", 0))
        issue_data = self.issues.get(issue_number)
        if issue_data is None:
            return subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="Not Found")
        issue_db_id = issue_data["id"]
        pair = (issue_db_id, blocked_by_db_id)
        if pair in self.dependencies:
            msg = json.dumps({"message": "Dependency already exists"})
            return subprocess.CompletedProcess(args=[], returncode=1, stdout=msg, stderr=msg)
        self.dependencies.add(pair)
        return self._resp({})

    def _patch_issue(self, number: str, input_str: str | None) -> subprocess.CompletedProcess[str]:
        """Handle PATCH /repos/.../issues/{number}: replace stored labels when provided."""
        payload = json.loads(input_str) if input_str else {}
        data = self.issues.get(number)
        if data is None:
            return subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="Not Found")
        if "labels" in payload:
            data["labels"] = set(payload["labels"])
        return self._resp(
            {"id": data["id"], "html_url": data["html_url"], "node_id": data["node_id"], "number": int(number)}
        )

    def _resolve(self, number: str) -> subprocess.CompletedProcess[str]:
        data = self.issues.get(number)
        if data is None:
            return self._resp({"id": 0, "html_url": "", "node_id": ""})
        return self._resp(
            {"id": data["id"], "html_url": data["html_url"], "node_id": data["node_id"], "number": int(number)}
        )

    def _get_labels(self, number: str) -> subprocess.CompletedProcess[str]:
        data = self.issues.get(number, {"labels": set()})
        return self._resp([{"name": n} for n in sorted(data["labels"])])

    def _add_labels(self, number: str, input_str: str | None) -> subprocess.CompletedProcess[str]:
        payload = json.loads(input_str) if input_str else {}
        data = self.issues.setdefault(number, {"id": 0, "node_id": "", "labels": set(), "body": "", "html_url": ""})
        for lbl in payload.get("labels", []):
            data["labels"].add(lbl)
        return self._resp([{"name": n} for n in sorted(data["labels"])])

    def _search(self, args: list[str]) -> subprocess.CompletedProcess[str]:
        q = ""
        if "-f" in args:
            val = args[args.index("-f") + 1]
            if val.startswith("q="):
                q = val[2:]
        match = re.search(r"agdt-orch-key:([a-f0-9]{64})", q)
        items: list[dict[str, Any]] = []
        if match:
            marker = f"agdt-orch-key:{match.group(1)}"
            for num, data in self.issues.items():
                if marker in (data.get("body") or ""):
                    items.append(
                        {
                            "number": int(num),
                            "html_url": data["html_url"],
                            "id": data["id"],
                            "node_id": data["node_id"],
                        }
                    )
                    break
        return self._resp({"items": items})

    def _resp(self, data: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(args=["gh"], returncode=0, stdout=json.dumps(data), stderr="")


# ======================================================================
# Stateful fake Jira session for the shared Jira contract leg
# ======================================================================


class _FakeJiraResponse:
    """Minimal stand-in for ``requests.Response`` used by the Jira contract leg."""

    def __init__(self, status_code: int = 200, json_data: Any = None, text: str = "") -> None:
        self.status_code = status_code
        self._json = json_data if json_data is not None else {}
        self.text = text

    def json(self) -> Any:
        return self._json

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.HTTPError(f"HTTP {self.status_code}")


class _FakeJiraSession:
    """A stateful in-memory emulation of the Jira REST API subset used by
    ``JiraProvider``.  Enables the shared provider-contract scenarios to run
    against Jira without any real HTTP transport.
    """

    def __init__(self) -> None:
        self.headers: dict[str, str] = {}
        self.verify: Any = True
        self.issues: dict[str, dict[str, Any]] = {}
        self._counter = 0
        self.request_calls: list[tuple[str, str, dict[str, Any]]] = []

    @property
    def call_count(self) -> int:
        return len(self.request_calls)

    def request(self, method: str, url: str, **kwargs: Any) -> _FakeJiraResponse:
        self.request_calls.append((method, url, kwargs))
        return self._route(method, url, kwargs)

    # -- routing --

    def _route(self, method: str, url: str, kwargs: dict[str, Any]) -> _FakeJiraResponse:
        path = url.split("/rest/api/2", 1)[1]
        base_path, _, query = path.partition("?")

        if base_path == "/field" and method == "GET":
            return _FakeJiraResponse(
                200,
                [
                    {
                        "id": "customfield_10008",
                        "name": "Epic Link",
                        "schema": {"custom": "com.pyxis.greenhopper.jira:gh-epic-link"},
                    }
                ],
            )
        if base_path == "/issue" and method == "POST":
            return self._create(kwargs)
        if base_path == "/issueLink" and method == "POST":
            return self._add_link(kwargs)
        if base_path == "/search" and method == "GET":
            return _FakeJiraResponse(200, {"issues": []})
        if base_path.startswith("/issue/"):
            key = base_path[len("/issue/") :]
            if method == "GET":
                return self._get_issue(key, query)
            if method == "PUT":
                return self._put_issue(key, kwargs)
        return _FakeJiraResponse(200, {})

    # -- handlers --

    def _create(self, kwargs: dict[str, Any]) -> _FakeJiraResponse:
        fields = kwargs.get("json", {}).get("fields", {})
        project_key = fields.get("project", {}).get("key", "PROJ")
        self._counter += 1
        key = f"{project_key}-{self._counter}"
        issuetype = fields.get("issuetype", {}).get("name", "Task")
        self.issues[key] = {
            "id": str(10000 + self._counter),
            "issuetype": issuetype,
            "labels": list(fields.get("labels", []) or []),
            "epic_field": None,
            "parent": None,
            "issuelinks": [],
        }
        return _FakeJiraResponse(201, {"key": key, "id": self.issues[key]["id"]})

    def _add_link(self, kwargs: dict[str, Any]) -> _FakeJiraResponse:
        payload = kwargs.get("json", {})
        inward = payload.get("inwardIssue", {}).get("key")
        outward = payload.get("outwardIssue", {}).get("key")
        issue = self.issues.setdefault(
            inward, {"id": "0", "issuetype": "Task", "labels": [], "epic_field": None, "parent": None, "issuelinks": []}
        )
        issue["issuelinks"].append({"type": {"name": "Blocks"}, "outwardIssue": {"key": outward}})
        return _FakeJiraResponse(201, {})

    def _get_issue(self, key: str, query: str) -> _FakeJiraResponse:
        issue = self.issues.get(
            key, {"id": "0", "issuetype": "Task", "labels": [], "epic_field": None, "parent": None, "issuelinks": []}
        )
        fields_param = ""
        if query.startswith("fields="):
            fields_param = query[len("fields=") :]

        if fields_param == "issuetype":
            return _FakeJiraResponse(200, {"fields": {"issuetype": {"name": issue["issuetype"]}}})
        if fields_param == "labels":
            return _FakeJiraResponse(200, {"fields": {"labels": list(issue["labels"])}})
        if fields_param == "issuelinks":
            return _FakeJiraResponse(200, {"fields": {"issuelinks": list(issue["issuelinks"])}})
        if "," in fields_param and "parent" in fields_param:
            epic_field = fields_param.split(",")[0]
            return _FakeJiraResponse(200, {"fields": {epic_field: issue["epic_field"], "parent": issue["parent"]}})
        return _FakeJiraResponse(200, {"key": key, "id": issue["id"]})

    def _put_issue(self, key: str, kwargs: dict[str, Any]) -> _FakeJiraResponse:
        issue = self.issues.setdefault(
            key, {"id": "0", "issuetype": "Task", "labels": [], "epic_field": None, "parent": None, "issuelinks": []}
        )
        payload = kwargs.get("json", {})
        fields = payload.get("fields", {})
        for field_id, value in fields.items():
            if field_id == "issuetype" and isinstance(value, dict):
                issue["issuetype"] = value.get("name", issue["issuetype"])
            elif field_id == "parent" and isinstance(value, dict):
                issue["parent"] = value
            elif field_id.startswith("customfield_"):
                issue["epic_field"] = value
        update = payload.get("update", {})
        for op in update.get("labels", []):
            if "add" in op:
                issue["labels"].append(op["add"])
        return _FakeJiraResponse(204, {})


# ======================================================================
# Contract-provider factory helpers (used by the provider test files)
# ======================================================================


def build_github_contract_provider() -> tuple[GitHubProvider, _FakeGitHubBackend]:
    """Return a (GitHubProvider, backend) pair wired to a stateful fake ``gh``
    CLI backend, so the shared provider-contract scenarios run directly against
    the production :class:`GitHubProvider` (no test-only compatibility layer).
    """
    backend = _FakeGitHubBackend()
    provider = GitHubProvider(owner_repo=backend.owner_repo, run_command=backend.run)
    return provider, backend


def build_jira_contract_provider() -> tuple[Any, _FakeJiraSession]:
    """Return a (JiraProvider, session) pair wired to a stateful fake Jira
    session for the shared contract leg.
    """
    from agentic_devtools.adapters.jira_provider import JiraProvider

    session = _FakeJiraSession()
    provider = JiraProvider(
        project_key="CONTRACT", base_url="https://jira.test", session=cast(requests.Session, session)
    )
    return provider, session
