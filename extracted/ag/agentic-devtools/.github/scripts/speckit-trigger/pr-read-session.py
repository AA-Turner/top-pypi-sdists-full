#!/usr/bin/env python3
"""Serve pooled SpecKit PR reads in one process for the lifetime of the caller."""

from __future__ import annotations

import json
import sys
from typing import Any
from urllib.parse import urlencode

from agentic_devtools.cli.ci.github_provider import _gh_api


def _handle_request(request: dict[str, Any]) -> object:
    operation = request.get("operation")
    repo = request.get("repo")
    if not isinstance(repo, str) or not repo:
        raise ValueError("repo must be a non-empty string")

    if operation in {"find-open-pr", "find-open-pr-state"}:
        branch = request.get("branch")
        if not isinstance(branch, str) or not branch:
            raise ValueError("branch must be a non-empty string")
        owner = repo.split("/", 1)[0]
        params = urlencode({"state": "open", "head": f"{owner}:{branch}", "per_page": 100})
        pulls = json.loads(_gh_api(f"/repos/{repo}/pulls?{params}"))
        if not isinstance(pulls, list):
            raise ValueError("Pull request list response must be an array")
        items = pulls
        if not items:
            return None
        if operation == "find-open-pr":
            return {"url": items[0]["html_url"], "number": items[0]["number"]}

        number = items[0]["number"]
        pr = json.loads(_gh_api(f"/repos/{repo}/pulls/{number}"))
        return {"number": number, "isDraft": pr["draft"], "labels": pr["labels"]}

    if operation == "previous-phase-pr":
        phase = request.get("phase")
        issue = request.get("issue")
        if not isinstance(phase, str) or not phase.isdigit():
            raise ValueError("phase must contain only digits")
        if not isinstance(issue, str) or not issue:
            raise ValueError("issue must be a non-empty string")
        query = f'repo:{repo} is:pr is:merged label:speckit:phase-{phase} "Relates to #{issue}"'
        params = urlencode({"q": query, "per_page": 1})
        results = json.loads(_gh_api(f"/search/issues?{params}"))
        if not isinstance(results, dict) or not isinstance(results.get("items"), list):
            raise ValueError("Previous-phase search response must contain an items array")
        items = results["items"]
        if not items:
            return None
        url = items[0].get("html_url")
        if not isinstance(url, str) or not url:
            raise ValueError("Previous-phase search result is missing html_url")
        return {"url": url}

    if operation == "pr-state":
        number = request.get("number")
        if not isinstance(number, str) or not number.isdigit():
            raise ValueError("number must contain only digits")
        pr = json.loads(_gh_api(f"/repos/{repo}/pulls/{number}"))
        return {"isDraft": pr["draft"], "labels": pr["labels"]}

    raise ValueError(f"unsupported operation: {operation!r}")


def main() -> int:
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                raise ValueError("request must be a JSON object")
            result = _handle_request(request)
        except Exception as exc:
            result = {"error": str(exc)}
        print(json.dumps(result, separators=(",", ":")), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
