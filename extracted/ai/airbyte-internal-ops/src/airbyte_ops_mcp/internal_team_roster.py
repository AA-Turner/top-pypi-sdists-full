# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Internal team roster: generation and lookup.

This module provides two main capabilities:
1. **Generation** (used by CI cron job): Fetches Slack and GitHub org member data,
   cross-references by email, and produces a sorted JSON roster artifact.
2. **Lookup** (used by MCP tools at runtime): Fetches the latest roster artifact
   from GitHub Actions and searches it by any key field.

The roster artifact is a JSON array of person records sorted by Slack display name.
Each record contains Slack and GitHub identity fields joined by email address.
"""

from __future__ import annotations

import csv
import io
import json
import sys
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests
from slack_sdk import WebClient

from airbyte_ops_mcp.github_api import (
    GITHUB_API_BASE,
    resolve_ci_trigger_github_token,
)

ROSTER_REPO_OWNER = "airbytehq"
ROSTER_REPO_NAME = "airbyte-ops-mcp"
ROSTER_WORKFLOW_NAME = "internal_team_roster.yml"
ROSTER_ARTIFACT_NAME = "internal-team-roster"

_ROSTER_CACHE: list[dict[str, str | int | None]] | None = None
_ROSTER_CACHE_TIME: float = 0.0
_ROSTER_CACHE_TTL_SECONDS: float = 3600.0


def _fetch_slack_members(token: str) -> list[dict[str, str | None]]:
    """Fetch all members from a Slack workspace.

    Uses the Slack SDK WebClient with pagination.

    Args:
        token: Slack Bot User OAuth Token with users:read scope.
            If the token also has users:read.email, the email field will be populated.

    Returns:
        List of dicts with keys: slack_id, slack_display_name, slack_real_name, slack_email.
    """
    client = WebClient(token=token)
    members: list[dict[str, str | None]] = []
    cursor: str | None = None

    while True:
        kwargs: dict[str, str | int] = {"limit": 200}
        if cursor:
            kwargs["cursor"] = cursor

        response = client.users_list(**kwargs)

        for member in response.get("members", []):
            if (
                member.get("deleted")
                or member.get("is_bot")
                or member.get("id") == "USLACKBOT"
            ):
                continue

            profile = member.get("profile", {})
            display_name = (
                profile.get("display_name")
                or profile.get("real_name")
                or member.get("name")
                or ""
            )
            real_name = profile.get("real_name") or member.get("real_name") or ""
            members.append(
                {
                    "slack_id": member.get("id"),
                    "slack_display_name": display_name,
                    "slack_real_name": real_name,
                    "slack_email": profile.get("email"),
                }
            )

        cursor = response.get("response_metadata", {}).get("next_cursor")
        if not cursor:
            break

    return members


def _fetch_github_org_members(
    token: str,
    org: str = "airbytehq",
) -> list[dict[str, str | int | None]]:
    """Fetch all members from a GitHub organization.

    Tries /orgs/{org}/members first (requires read:org scope).
    Falls back to /orgs/{org}/public_members if that returns empty
    (works with any valid GitHub token).

    For each member, fetches detailed user info to get name and email.

    Args:
        token: GitHub API token.
        org: GitHub organization name.

    Returns:
        List of dicts with keys: github_id, github_handle, github_name,
        github_public_email.
    """
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    member_logins: list[str] = []
    for endpoint in ["members", "public_members"]:
        page = 1
        while True:
            response = requests.get(
                f"{GITHUB_API_BASE}/orgs/{org}/{endpoint}",
                headers=headers,
                params={"per_page": "100", "page": str(page)},
                timeout=30,
            )
            if response.status_code == 403:
                break
            response.raise_for_status()
            page_members = response.json()

            if not page_members:
                break

            member_logins.extend(m["login"] for m in page_members)
            page += 1

        if member_logins:
            print(
                f"Fetched {len(member_logins)} GitHub org members "
                f"via /orgs/{org}/{endpoint}",
                file=sys.stderr,
            )
            break

    members: list[dict[str, str | int | None]] = []
    for login in member_logins:
        user_response = requests.get(
            f"{GITHUB_API_BASE}/users/{login}",
            headers=headers,
            timeout=30,
        )
        user_response.raise_for_status()
        user_data = user_response.json()

        members.append(
            {
                "github_id": user_data.get("id"),
                "github_handle": user_data.get("login"),
                "github_name": user_data.get("name"),
                "github_public_email": user_data.get("email"),
            }
        )

    # Enrich members with commit emails derived from recent commits in
    # selected repositories via the GitHub commits API.
    commit_emails = _fetch_github_commit_emails(headers, member_logins, org=org)
    emails_found = 0
    for member in members:
        handle = member.get("github_handle")
        if isinstance(handle, str) and handle in commit_emails:
            member["github_commit_email"] = commit_emails[handle]
            emails_found += 1
        else:
            member["github_commit_email"] = None

    print(
        f"Enriched {emails_found}/{len(members)} GitHub members with commit emails",
        file=sys.stderr,
    )

    return members


# Repositories to search for commit author emails.
# The `airbyte` monorepo covers most open-source contributors while
# `airbyte-platform-internal` captures platform engineers who primarily
# commit to the private repo.
_COMMIT_EMAIL_REPOS = ("airbyte", "airbyte-platform-internal")


def _fetch_github_commit_emails(
    headers: dict[str, str],
    member_logins: list[str],
    org: str = "airbytehq",
) -> dict[str, str]:
    """Extract `@airbyte.io` work emails from recent commits.

    For each org member, queries `/repos/{org}/{repo}/commits?author={login}`
    across the repos listed in `_COMMIT_EMAIL_REPOS` to find their most
    recent commit and extract the author email.  This reveals work emails even
    when the user has not set a public email on their GitHub profile.

    This mirrors the approach used by the existing
    `tools/bin/match_github_user_to_slack` script in the `airbyte` and
    `airbyte-platform-internal` repositories.

    Only `@airbyte.io` emails are kept — personal email addresses are
    discarded since they cannot reliably link to a Slack account.

    Args:
        headers: GitHub API request headers (with auth token).
        member_logins: List of GitHub usernames to query.
        org: GitHub organization that owns the repos to search.

    Returns:
        Dict mapping GitHub login → `@airbyte.io` commit email string.
    """
    commit_emails: dict[str, str] = {}

    for repo in _COMMIT_EMAIL_REPOS:
        # Only query members we haven't resolved yet.
        remaining = [login for login in member_logins if login not in commit_emails]
        if not remaining:
            break

        for login in remaining:
            try:
                response = requests.get(
                    f"{GITHUB_API_BASE}/repos/{org}/{repo}/commits",
                    headers=headers,
                    params={"author": login, "per_page": "1"},
                    timeout=30,
                )
                if response.status_code == 403:
                    # Rate-limited — stop querying this repo entirely.
                    print(
                        f"GitHub API rate limit hit while querying {repo}",
                        file=sys.stderr,
                    )
                    break
                if response.status_code != 200:
                    continue

                commits = response.json()
                if not commits:
                    continue

                commit_data = commits[0].get("commit", {})
                author = commit_data.get("author", {})
                email = author.get("email", "")
                if email and email.lower().endswith("@airbyte.io"):
                    commit_emails[login] = email.lower()
            except (requests.RequestException, ValueError, KeyError):
                continue

    return commit_emails


# Relative path (from repo root) to the companion CSV containing curated
# GitHub handle → @airbyte.io email mappings.
_GITHUB_TO_AIRBYTE_IO_EMAIL_PATH = "data/github_to_airbyte_io_email.csv"

# Candidate repo-root locations when installed from a cloned checkout.
_REPO_ROOT_CANDIDATES: tuple[Path, ...] = (
    # Editable / dev install: src/airbyte_ops_mcp → repo root is 2 levels up.
    Path(__file__).parent.parent.parent,
    # Fallback: cwd (works inside CI where checkout is the working directory).
    Path.cwd(),
)


def _load_github_to_airbyte_io_email(
    github_token: str | None = None,
) -> dict[str, str]:
    """Load the static GitHub handle → `@airbyte.io` email mapping.

    Resolution order:

    1. **Local file** — look for the CSV in the cloned repo checkout.
    2. **GitHub API** — fetch the file from the default branch via the
       GitHub Contents API (requires *github_token*).
    3. **Warn** — if neither source is available, log a warning and return
       an empty mapping so roster generation can continue without the
       static fallback.

    Returns:
        Dict mapping GitHub login → `@airbyte.io` email.
    """
    # --- 1. Try local file discovery ---
    for root in _REPO_ROOT_CANDIDATES:
        candidate = root / _GITHUB_TO_AIRBYTE_IO_EMAIL_PATH
        if candidate.is_file():
            return _parse_github_to_airbyte_io_csv(candidate.read_text())

    # --- 2. Try GitHub Contents API ---
    if github_token:
        url = (
            f"{GITHUB_API_BASE}/repos/{ROSTER_REPO_OWNER}/{ROSTER_REPO_NAME}"
            f"/contents/{_GITHUB_TO_AIRBYTE_IO_EMAIL_PATH}"
        )
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Accept": "application/vnd.github.raw+json",
        }
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            return _parse_github_to_airbyte_io_csv(resp.text)
        print(
            f"Warning: GitHub API returned {resp.status_code} fetching "
            f"{_GITHUB_TO_AIRBYTE_IO_EMAIL_PATH}.",
            file=sys.stderr,
        )

    # --- 3. Warn and return empty ---
    print(
        f"Warning: Could not locate {_GITHUB_TO_AIRBYTE_IO_EMAIL_PATH}. "
        "Static GitHub→Slack mapping will be skipped.",
        file=sys.stderr,
    )
    return {}


def load_github_to_airbyte_io_email(
    github_token: str | None = None,
) -> dict[str, str]:
    """Load the curated GitHub login to Airbyte email mapping."""
    return _load_github_to_airbyte_io_email(github_token)


def _parse_github_to_airbyte_io_csv(text: str) -> dict[str, str]:
    """Parse the `github_to_airbyte_io_email` CSV text into a dict.

    Returns:
        Dict mapping GitHub login → `@airbyte.io` email.
    """
    mapping: dict[str, str] = {}
    for row in csv.DictReader(io.StringIO(text)):
        handle = row.get("github_handle", "").strip()
        email = row.get("slack_email", "").strip()
        if handle and email:
            mapping[handle] = email
    return mapping


def _normalize_name(name: str) -> str:
    """Normalize a name for case-insensitive comparison."""
    return " ".join(name.lower().split())


def generate_roster(
    slack_token: str,
    github_token: str,
    github_org: str = "airbytehq",
) -> list[dict[str, str | int | None]]:
    """Generate the internal team roster by joining Slack and GitHub data.

    Cross-references Slack members and GitHub org members using:
    1. Email matching — Slack profile email vs GitHub public email
    2. Commit-email matching — Slack profile email vs email extracted from
       recent commits in selected repos (via the commits API), revealing work
       emails even without a public email set
    3. Exact name matching — Slack real_name/display_name vs GitHub name
    4. Static mapping — curated `github_to_airbyte_io_email.csv` companion
       file for members whose handles don't align with automated strategies

    Returns a list of person records sorted by tier then name:
    1. Matched across both Slack and GitHub
    2. Slack members with @airbyte.io email
    3. GitHub members with @airbyte.io email
    4. Everyone else

    Args:
        slack_token: Slack Bot User OAuth Token.
        github_token: GitHub API token.
        github_org: GitHub organization name.

    Returns:
        List of person dicts sorted by slack_display_name.
    """
    slack_members = _fetch_slack_members(slack_token)
    github_members = _fetch_github_org_members(github_token, org=github_org)
    github_to_airbyte_io_email = _load_github_to_airbyte_io_email(
        github_token=github_token,
    )

    # Build indexes for matching GitHub members by email, name, and
    # static mapping.
    github_by_email: dict[str, dict[str, str | int | None]] = {}
    github_by_commit_email: dict[str, dict[str, str | int | None]] = {}
    github_by_name: dict[str, dict[str, str | int | None]] = {}
    github_by_static_email: dict[str, dict[str, str | int | None]] = {}
    for gh_member in github_members:
        email = gh_member.get("github_public_email")
        if email and isinstance(email, str):
            github_by_email[email.lower()] = gh_member
        commit_email = gh_member.get("github_commit_email")
        if commit_email and isinstance(commit_email, str):
            github_by_commit_email[commit_email.lower()] = gh_member
        gh_name = gh_member.get("github_name")
        if gh_name and isinstance(gh_name, str):
            normalized = _normalize_name(gh_name)
            if normalized not in github_by_name:
                github_by_name[normalized] = gh_member
        gh_handle = gh_member.get("github_handle")
        if isinstance(gh_handle, str) and gh_handle in github_to_airbyte_io_email:
            static_email = github_to_airbyte_io_email[gh_handle].lower()
            github_by_static_email[static_email] = gh_member

    roster: list[dict[str, str | int | None]] = []
    matched_github_ids: set[int | str] = set()
    email_matches = 0
    commit_email_matches = 0
    name_matches = 0
    static_matches = 0

    for slack_member in slack_members:
        record: dict[str, str | int | None] = {
            "slack_id": slack_member.get("slack_id"),
            "slack_display_name": slack_member.get("slack_display_name"),
            "slack_email": slack_member.get("slack_email"),
            "github_id": None,
            "github_handle": None,
            "github_public_email": None,
        }

        gh_match: dict[str, str | int | None] | None = None
        match_method: str | None = None

        # Pass 1: Match by public email.
        slack_email = slack_member.get("slack_email")
        if slack_email and isinstance(slack_email, str):
            gh_match = github_by_email.get(slack_email.lower())
            if gh_match:
                match_method = "email"

        # Pass 2: Match by commit email (from push events).
        if gh_match is None and slack_email and isinstance(slack_email, str):
            gh_match = github_by_commit_email.get(slack_email.lower())
            if gh_match:
                match_method = "commit_email"

        # Pass 3: Exact name match.
        if gh_match is None:
            slack_real_name = slack_member.get("slack_real_name", "")
            slack_display = slack_member.get("slack_display_name", "")
            if slack_real_name and isinstance(slack_real_name, str):
                gh_match = github_by_name.get(_normalize_name(slack_real_name))
            if gh_match is None and slack_display and isinstance(slack_display, str):
                gh_match = github_by_name.get(_normalize_name(slack_display))
            if gh_match:
                match_method = "name"

        # Pass 4: Static mapping (curated GitHub handle → Slack email).
        if gh_match is None and slack_email and isinstance(slack_email, str):
            gh_match = github_by_static_email.get(slack_email.lower())
            if gh_match:
                match_method = "static"

        if match_method == "email":
            email_matches += 1
        elif match_method == "commit_email":
            commit_email_matches += 1
        elif match_method == "name":
            name_matches += 1
        elif match_method == "static":
            static_matches += 1

        if gh_match:
            record["github_id"] = gh_match.get("github_id")
            record["github_handle"] = gh_match.get("github_handle")
            record["github_public_email"] = gh_match.get("github_public_email")
            gh_id = gh_match.get("github_id")
            if gh_id is not None:
                matched_github_ids.add(gh_id)

        roster.append(record)

    for gh_member in github_members:
        gh_id = gh_member.get("github_id")
        if gh_id is not None and gh_id in matched_github_ids:
            continue
        roster.append(
            {
                "slack_id": None,
                "slack_display_name": None,
                "slack_email": None,
                "github_id": gh_member.get("github_id"),
                "github_handle": gh_member.get("github_handle"),
                "github_public_email": gh_member.get("github_public_email"),
            }
        )

    def _sort_key(r: dict[str, str | int | None]) -> tuple[int, str]:
        has_slack = r.get("slack_id") is not None
        has_github = r.get("github_handle") is not None
        slack_email = str(r.get("slack_email") or "")
        gh_email = str(r.get("github_public_email") or "")
        is_airbyte_slack = slack_email.lower().endswith("@airbyte.io")
        is_airbyte_gh = gh_email.lower().endswith("@airbyte.io")

        if has_slack and has_github:
            tier = 0
        elif has_slack and is_airbyte_slack:
            tier = 1
        elif has_github and is_airbyte_gh:
            tier = 2
        else:
            tier = 3

        name = (r.get("slack_display_name") or r.get("github_handle") or "").lower()
        return (tier, name)

    roster.sort(key=_sort_key)

    total_matched = email_matches + commit_email_matches + name_matches + static_matches
    print(
        f"Roster matching stats: {total_matched} total matched "
        f"({email_matches} by public email, "
        f"{commit_email_matches} by commit email, "
        f"{name_matches} by exact name, "
        f"{static_matches} by static mapping), "
        f"{len(slack_members)} Slack members, "
        f"{len(github_members)} GitHub members",
        file=sys.stderr,
    )

    return roster


def _download_latest_artifact(
    owner: str = ROSTER_REPO_OWNER,
    repo: str = ROSTER_REPO_NAME,
    workflow_name: str = ROSTER_WORKFLOW_NAME,
    artifact_name: str = ROSTER_ARTIFACT_NAME,
    token: str | None = None,
) -> list[dict[str, str | int | None]]:
    """Download and parse the latest roster artifact from GitHub Actions.

    Finds the most recent successful workflow run and downloads the artifact.

    Args:
        owner: Repository owner.
        repo: Repository name.
        workflow_name: Workflow file name.
        artifact_name: Name of the artifact to download.
        token: GitHub API token. If None, resolved from environment.

    Returns:
        Parsed roster data (list of person dicts).

    Raises:
        RuntimeError: If no artifact is found or download fails.
    """
    if token is None:
        # The Actions API requires `actions:read` permission.  The CI
        # workflow-trigger PAT (GITHUB_CI_WORKFLOW_TRIGGER_PAT) carries
        # this scope, whereas the default `gh auth token` / GITHUB_TOKEN
        # used elsewhere in the MCP server typically does not — causing
        # a 404 on private-repo Actions endpoints.
        token = resolve_ci_trigger_github_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    runs_url = (
        f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/workflows/{workflow_name}/runs"
    )
    runs_response = requests.get(
        runs_url,
        headers=headers,
        params={"status": "success", "per_page": "1", "branch": "main"},
        timeout=30,
    )
    runs_response.raise_for_status()
    runs_data = runs_response.json()

    workflow_runs = runs_data.get("workflow_runs", [])
    if not workflow_runs:
        raise RuntimeError(
            f"No successful runs found for workflow '{workflow_name}' "
            f"in {owner}/{repo}."
        )

    run_id = workflow_runs[0]["id"]

    artifacts_url = (
        f"{GITHUB_API_BASE}/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
    )
    artifacts_response = requests.get(artifacts_url, headers=headers, timeout=30)
    artifacts_response.raise_for_status()
    artifacts_data = artifacts_response.json()

    target_artifact = None
    for artifact in artifacts_data.get("artifacts", []):
        if artifact["name"] == artifact_name:
            target_artifact = artifact
            break

    if target_artifact is None:
        raise RuntimeError(
            f"Artifact '{artifact_name}' not found in run {run_id} of {owner}/{repo}."
        )

    download_url = target_artifact["archive_download_url"]
    download_response = requests.get(download_url, headers=headers, timeout=60)
    download_response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(download_response.content)) as zf:
        names = zf.namelist()
        json_files = [n for n in names if n.endswith(".json")]
        if not json_files:
            raise RuntimeError(f"No JSON files found in artifact '{artifact_name}'.")
        with zf.open(json_files[0]) as f:
            data = json.loads(f.read())

    if isinstance(data, dict) and "members" in data:
        return data["members"]
    if isinstance(data, list):
        return data
    raise RuntimeError(
        f"Unexpected artifact format in '{artifact_name}': "
        f"expected a list or dict with 'members' key."
    )


def fetch_roster(
    token: str | None = None,
) -> list[dict[str, str | int | None]]:
    """Fetch the latest internal team roster from the CI artifact.

    Uses an in-memory cache with a 1-hour TTL to avoid re-downloading
    the artifact on every call.

    Args:
        token: GitHub API token. If None, resolved from environment.

    Returns:
        List of person dicts sorted by slack_display_name.
    """
    global _ROSTER_CACHE, _ROSTER_CACHE_TIME

    now = time.monotonic()
    if (
        _ROSTER_CACHE is not None
        and (now - _ROSTER_CACHE_TIME) < _ROSTER_CACHE_TTL_SECONDS
    ):
        return _ROSTER_CACHE

    roster = _download_latest_artifact(token=token)
    _ROSTER_CACHE = roster
    _ROSTER_CACHE_TIME = now
    return roster


def search_roster(
    roster: list[dict[str, str | int | None]],
    query: str,
) -> list[dict[str, str | int | None]]:
    """Search the roster by any field value.

    Performs case-insensitive partial matching against all string fields
    and exact matching against numeric fields (github_id).

    Args:
        roster: The roster data (list of person dicts).
        query: Search string to match against any field.

    Returns:
        List of matching person records.
    """
    query_lower = query.lower().strip()
    results: list[dict[str, str | int | None]] = []

    for person in roster:
        for _key, value in person.items():
            if value is None:
                continue
            if isinstance(value, str) and query_lower in value.lower():
                results.append(person)
                break
            if isinstance(value, int) and query_lower == str(value):
                results.append(person)
                break

    return results


def summarize_roster(
    roster_path: Path,
) -> str:
    """Produce a human-readable summary of a roster JSON artifact.

    Categorises members into *matched* (both Slack and GitHub), *Slack-only*,
    and *GitHub-only*, then formats the results as a plain-text report suitable
    for CI logs.

    Args:
        roster_path: Path to a roster JSON file produced by
            `generate_roster` (via the `generate` CLI command).

    Returns:
        Multi-line summary string.
    """
    data = json.loads(roster_path.read_text())
    members: list[dict[str, str | int | None]] = data["members"]

    matched = [m for m in members if m.get("github_id") and m.get("slack_id")]
    slack_only = [m for m in members if m.get("slack_id") and not m.get("github_id")]
    github_only = [m for m in members if m.get("github_id") and not m.get("slack_id")]

    lines: list[str] = [
        "=== ROSTER SUMMARY ===",
        f"Total members: {len(members)}",
        f"Matched (Slack + GitHub): {len(matched)}",
        f"Slack only (no GitHub match): {len(slack_only)}",
        f"GitHub only (no Slack match): {len(github_only)}",
        "",
        f"=== UNMATCHED GITHUB MEMBERS ({len(github_only)}) ===",
    ]
    for m in sorted(github_only, key=lambda x: (x.get("github_handle") or "").lower()):
        handle = m.get("github_handle", "?")
        email = m.get("github_public_email") or "no public email"
        lines.append(f"  @{handle} ({email})")

    lines.append("")
    lines.append(f"=== UNMATCHED SLACK MEMBERS ({len(slack_only)}) ===")
    for m in sorted(
        slack_only, key=lambda x: (x.get("slack_display_name") or "").lower()
    ):
        name = m.get("slack_display_name") or m.get("slack_email") or "?"
        email = m.get("slack_email") or "no email"
        lines.append(f"  {name} ({email})")

    return "\n".join(lines)


def generate_roster_to_file(
    output_path: Path,
    slack_token: str,
    github_token: str,
    github_org: str = "airbytehq",
) -> int:
    """Generate the roster and write it as JSON to *output_path*.

    This is a convenience wrapper around `generate_roster` that handles
    serialisation and returns the member count.

    Args:
        output_path: Destination for the roster JSON artifact.
        slack_token: Slack Bot User OAuth Token.
        github_token: GitHub API token.
        github_org: GitHub organization name.

    Returns:
        Number of members written.
    """
    roster = generate_roster(
        slack_token=slack_token,
        github_token=github_token,
        github_org=github_org,
    )

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(roster),
        "members": roster,
    }

    output_path.write_text(json.dumps(output, indent=2))

    print(
        f"Roster generated: {len(roster)} members written to {output_path}",
        file=sys.stderr,
    )
    return len(roster)
