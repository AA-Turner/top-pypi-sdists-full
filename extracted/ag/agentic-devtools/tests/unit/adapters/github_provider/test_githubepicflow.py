"""Tests for GitHubProvider epic creation flow."""

from __future__ import annotations

import json
import subprocess

from agentic_devtools.adapters.github_provider import GitHubProvider


class TestGitHubEpicFlow:
    """Verify full epic creation flow: 1 parent + 5 children with links."""

    def test_create_epic_with_children_and_links(self):
        """Create 1 epic + 5 children with parent_id; each child is auto-linked at creation time."""
        call_log = []
        issue_counter = {"n": 0}

        def mock_run(*args, **kwargs):
            call_log.append(args[0] if args else kwargs.get("args", []))
            argv = list(args[0] if args else kwargs.get("args", []))
            method = argv[argv.index("--method") + 1] if "--method" in argv else "GET"
            path = next((a for a in argv if a.startswith("/repos/")), "")
            # Sub-issue idempotency check GETs a list; return an empty list so the
            # link is treated as absent and the POST proceeds.
            if path.endswith("/sub_issues") and method == "GET":
                return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="[]", stderr="")
            issue_counter["n"] += 1
            num = issue_counter["n"]
            data = {
                "number": num,
                "html_url": f"https://github.com/org/repo/issues/{num}",
                "id": 1000 + num,
                "node_id": f"I_kwDO{num}",
            }
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=json.dumps(data), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)

        # Create parent epic
        parent_result = provider.create_issue("Epic Title", "Epic body", "epic", dry_run=False)
        assert parent_result.status == "created"
        parent_id = parent_result.identifier
        _ = parent_result.metadata["database_id"]

        # Create 5 children with parent_id — each create auto-links the child.
        children = []
        for i in range(5):
            result = provider.create_issue(f"Child {i}", f"Body {i}", "feature", parent_id=parent_id, dry_run=False)
            assert result.status == "created"
            children.append(result)

        # Verify counts
        assert len(children) == 5
        # 1 epic create POST
        # + 5 children × (1 create POST + 1 resolve GET + 1 sub_issues GET + 1 sub_issues POST) = 20
        # Total = 21 calls
        assert len(call_log) == 21

        # Verify that each child triggered a sub_issues POST (auto-link via parent_id).
        sub_issue_posts = [
            c
            for c in call_log
            if "--method" in c and c[c.index("--method") + 1] == "POST" and any(a.endswith("/sub_issues") for a in c)
        ]
        assert len(sub_issue_posts) == 5, "Each child create_issue must auto-link via parent_id"

    def test_create_epic_with_dependencies(self):
        """Create issues and wire blocking dependencies via the REST dependencies API."""
        call_log = []
        issue_store: dict[str, dict] = {}
        issue_counter = {"n": 0}

        def mock_run(*args, **kwargs):
            call_log.append(args[0] if args else kwargs.get("args", []))
            argv = list(args[0] if args else kwargs.get("args", []))
            method = argv[argv.index("--method") + 1] if "--method" in argv else "GET"
            path = next((a for a in argv if a.startswith("/repos/")), "")

            if path.endswith("/issues") and method == "POST":
                issue_counter["n"] += 1
                num = issue_counter["n"]
                db_id = 2000 + num
                issue_store[str(num)] = {"id": db_id, "number": num}
                data = {
                    "number": num,
                    "html_url": f"https://github.com/org/repo/issues/{num}",
                    "id": db_id,
                    "node_id": f"I_kwDOdep{num}",
                }
            elif path.endswith("/dependencies/blocked_by") and method == "POST":
                data = {}
            else:
                # GET /repos/org/repo/issues/{number} — resolve call
                num_str = path.split("/")[-1]
                stored = issue_store.get(num_str, {})
                data = {
                    "number": int(num_str) if num_str.isdigit() else 0,
                    "id": stored.get("id", 0),
                    "node_id": f"I_kwDOdep{num_str}",
                    "html_url": f"https://github.com/org/repo/issues/{num_str}",
                }
            return subprocess.CompletedProcess(args=args[0], returncode=0, stdout=json.dumps(data), stderr="")

        provider = GitHubProvider(owner_repo="org/repo", run_command=mock_run)

        # Create 3 issues — identifiers are numeric issue numbers ("1", "2", "3").
        issues = []
        for i in range(3):
            result = provider.create_issue(f"Issue {i}", f"Body {i}", "task", dry_run=False)
            issues.append(result)

        # Wire dependencies using issue numbers: issue[1] blocked by issue[0],
        # issue[2] blocked by issue[1].
        dep1 = provider.add_blocked_by(issues[1].identifier, issues[0].identifier, dry_run=False)
        assert dep1.status == "linked"
        dep2 = provider.add_blocked_by(issues[2].identifier, issues[1].identifier, dry_run=False)
        assert dep2.status == "linked"

        # Verify that the blocked_by calls posted to the REST dependencies endpoint.
        dep_posts = [c for c in call_log if any("/dependencies/blocked_by" in str(a) for a in c)]
        assert len(dep_posts) == 2
