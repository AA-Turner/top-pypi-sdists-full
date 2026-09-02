"""Playwright-driven Copilot autofix suggestion applier for EMU/SSO repos.

Drives the real GitHub PR Conversation UI in an authenticated browser to apply
Copilot code-review *autofix* suggestions that the GraphQL/REST/HTML discovery
tiers cannot recover inside a SWICA GitHub EMU (Enterprise Managed Users) tenant,
where raw bearer-token page fetches are blocked by SAML SSO.

Auth is Cypress-style (NOT a persisted ``storageState``): a committed
``user_credentials.json`` holds ``{{ENV_NAME}}`` placeholders, real values are
injected at runtime from environment variables (GitHub Actions secrets), and a
fresh login is performed on every run. The MFA code is generated programmatically
from the TOTP seed via ``pyotp``.

Playwright and pyotp are *optional* dependencies imported lazily (see the
``[browser]`` extra in ``pyproject.toml``). When they are missing, the lazy
``_require_*`` helpers raise :class:`BrowserAutofixUnavailable` so callers can
fail open.

STABILITY NOTE: This module depends on the IdP login DOM and GitHub's
Conversation-tab suggestion DOM. All selectors are centralized below and
marked with ``[BROWSER-SELECTOR]`` so format changes are easy to locate and
update (mirroring the ``[SCRAPE-FORMAT]`` markers in ``apply_thread_autofix``).
"""

from __future__ import annotations

import contextlib
import json
import logging
import os
import re
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..subprocess_utils import run_safe

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Centralized selectors  ([BROWSER-SELECTOR])
# ---------------------------------------------------------------------------

# GitHub EMU sign-in starts at the enterprise SSO page
# (https://github.com/enterprises/<slug>/sso) whose "Continue" button hands off
# to the tenant IdP. For SWICA the IdP is confirmed to be Microsoft Entra ID
# (login.microsoftonline.com, OIDC). The IdP domain is overridable via the
# AGDT_BROWSER_IDP_DOMAIN environment variable (for non-Entra tenants) and is
# used by perform_idp_login() to verify the post-Continue redirect landed on the
# expected IdP. The enterprise slug is overridable via AGDT_BROWSER_GH_ENTERPRISE.
DEFAULT_IDP_DOMAIN = "login.microsoftonline.com"
DEFAULT_GH_ENTERPRISE = "swica"

# GitHub EMU SSO interstitial ([BROWSER-SELECTOR])
BUTTON_CONTINUE = "Continue"

# Microsoft Entra ID login DOM ([BROWSER-SELECTOR])
SELECTOR_USERNAME_INPUT = 'input[type="email"]'
SELECTOR_PASSWORD_INPUT = 'input[type="password"]'  # nosec B105 - DOM selector, not a credential
SELECTOR_TOTP_INPUT = 'input[name="otc"]'
BUTTON_NEXT = "Next"
BUTTON_SIGN_IN = "Sign in"
BUTTON_VERIFY = "Verify"
BUTTON_STAY_SIGNED_IN = "Yes"

# GitHub Copilot Code Review suggestion DOM, Conversation tab ([BROWSER-SELECTOR]).
# Verified live 2026-06-23 on a real CCR autofix PR: each suggestion exposes a
# "Commit suggestion" button carrying this stable test id; clicking it opens a
# Primer "Commit suggestion" dialog whose PRIMARY submit button is
# "Apply Suggestion" and whose commit-message textbox is pre-filled. An
# "Outdated" badge does NOT remove the button, so the loop drains every
# suggestion regardless of commit order.
SELECTOR_COMMIT_SUGGESTION_BUTTON = '[data-testid="commit-suggestion-button"]'
BUTTON_APPLY_SUGGESTION = "Apply Suggestion"
TEXTBOX_COMMIT_MESSAGE = "Commit message"

# Per-suggestion commit/rescan loop cap (one commit per suggestion; the AI PR
# loop squashes them later). Rarely more than a handful.
DEFAULT_MAX_DRAIN_ITERATIONS = 20
DEFAULT_COMMIT_MESSAGE = "Apply Copilot autofix suggestions from code review"


# ---------------------------------------------------------------------------
# Exceptions and credential model
# ---------------------------------------------------------------------------


class BrowserAutofixUnavailable(RuntimeError):
    """Raised when optional browser dependencies (playwright/pyotp) are missing."""


class BrowserCredentialError(RuntimeError):
    """Raised when credentials cannot be loaded or a placeholder env var is unset."""


@dataclass
class BrowserCredentials:
    """Resolved login credentials for a fresh IdP authentication."""

    username: str
    password: str
    totp_secret: str


# ---------------------------------------------------------------------------
# Credential loading (Cypress-style placeholder resolution)
# ---------------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")


def _default_credentials_path() -> Path:
    """Return the path to the committed credentials template next to this module."""
    return Path(__file__).with_name("user_credentials.json")


def _resolve_secret(raw: str) -> str:
    """Resolve a ``{{ENV_NAME}}`` placeholder from the environment.

    A literal value (no placeholder) is returned unchanged. A placeholder that
    references an unset/empty environment variable raises
    :class:`BrowserCredentialError` (never logging the value itself).
    """
    match = _PLACEHOLDER_RE.fullmatch(raw.strip())
    if match is None:
        return raw
    env_name = match.group(1)
    value = os.environ.get(env_name, "")
    if not value:
        raise BrowserCredentialError(f"Environment variable {env_name!r} is not set")
    return value


def load_credentials(path: str | os.PathLike[str] | None = None) -> BrowserCredentials:
    """Load and resolve credentials from a placeholder JSON file.

    The file must contain ``username``, ``password`` and ``2fa_secret`` keys,
    each either a literal value or a ``{{ENV_NAME}}`` placeholder.
    """
    cred_path = Path(path) if path is not None else _default_credentials_path()
    try:
        raw_text = cred_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise BrowserCredentialError(f"Cannot read credentials file {cred_path}: {exc}") from exc
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise BrowserCredentialError(f"Invalid JSON in credentials file {cred_path}: {exc}") from exc
    if not isinstance(data, dict):
        raise BrowserCredentialError(
            f"Credentials file {cred_path} must contain a JSON object with username/password/2fa_secret fields"
        )
    try:
        username = _resolve_secret(str(data["username"]))
        password = _resolve_secret(str(data["password"]))
        totp_secret = _resolve_secret(str(data["2fa_secret"]))
    except KeyError as exc:
        raise BrowserCredentialError(f"Missing credential field: {exc}") from exc
    return BrowserCredentials(username=username, password=password, totp_secret=totp_secret)


# ---------------------------------------------------------------------------
# Lazy optional-dependency imports
# ---------------------------------------------------------------------------


def _require_pyotp() -> Any:
    """Import ``pyotp`` lazily, raising BrowserAutofixUnavailable when missing."""
    try:
        import pyotp
    except ImportError as exc:
        raise BrowserAutofixUnavailable(
            "pyotp is not installed; install the optional 'browser' extra: pip install 'agentic-devtools[browser]'"
        ) from exc
    return pyotp


def generate_totp(secret: str) -> str:
    """Generate the current 6-digit TOTP code from a base32 seed."""
    pyotp = _require_pyotp()
    return str(pyotp.TOTP(secret).now())


def _require_sync_playwright() -> Any:
    """Import Playwright's ``sync_playwright`` lazily, raising when missing."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise BrowserAutofixUnavailable(
            "playwright is not installed; install the optional 'browser' extra: "
            "pip install 'agentic-devtools[browser]' && playwright install chromium"
        ) from exc
    return sync_playwright


# ---------------------------------------------------------------------------
# Page interaction helpers (page is a duck-typed Playwright Page)
# ---------------------------------------------------------------------------


def _click_if_present(page: Any, name: str) -> bool:
    """Click the first button matching ``name`` if it exists.

    Returns whether a button was clicked.
    """
    locator = page.get_by_role("button", name=name)
    if locator.count() > 0:
        locator.first.click()
        return True
    return False


def _github_enterprise_slug() -> str:
    """Return the GitHub EMU enterprise slug for the SSO sign-in URL.

    Overridable via the ``AGDT_BROWSER_GH_ENTERPRISE`` environment variable;
    defaults to :data:`DEFAULT_GH_ENTERPRISE`.
    """
    return os.environ.get("AGDT_BROWSER_GH_ENTERPRISE", "").strip() or DEFAULT_GH_ENTERPRISE


def _idp_domain() -> str:
    """Return the expected IdP domain for the SSO login handoff.

    Overridable via the ``AGDT_BROWSER_IDP_DOMAIN`` environment variable (for
    non-Entra tenants); defaults to :data:`DEFAULT_IDP_DOMAIN`.
    """
    return os.environ.get("AGDT_BROWSER_IDP_DOMAIN", "").strip() or DEFAULT_IDP_DOMAIN


def perform_idp_login(page: Any, credentials: BrowserCredentials, *, base_url: str = "https://github.com") -> None:
    """Drive a fresh GitHub EMU SSO + IdP (Microsoft Entra ID) login.

    [BROWSER-SELECTOR] The flow is: GitHub enterprise SSO "Continue" -> Entra
    username -> Next -> password -> Sign in -> TOTP -> Verify -> Stay signed in.
    Optional button clicks are guarded by presence checks so the flow is
    resilient to pages that skip those prompts (e.g. no "Stay signed in?" page).

    After the "Continue" hand-off, the flow waits until the browser lands on the
    expected IdP domain (see :func:`_idp_domain`) before filling tenant
    selectors, so failures are clear when the IdP flow changes or redirects
    differently.
    """
    slug = _github_enterprise_slug()
    page.goto(f"{base_url}/enterprises/{slug}/sso")
    _click_if_present(page, BUTTON_CONTINUE)
    page.wait_for_url(f"**{_idp_domain()}/**")
    page.fill(SELECTOR_USERNAME_INPUT, credentials.username)
    _click_if_present(page, BUTTON_NEXT)
    page.fill(SELECTOR_PASSWORD_INPUT, credentials.password)
    _click_if_present(page, BUTTON_SIGN_IN)
    page.fill(SELECTOR_TOTP_INPUT, generate_totp(credentials.totp_secret))
    _click_if_present(page, BUTTON_VERIFY)
    _click_if_present(page, BUTTON_STAY_SIGNED_IN)


def count_commit_suggestion_buttons(page: Any) -> int:
    """Count Copilot "Commit suggestion" buttons currently rendered on the page.

    Matches the stable ``data-testid`` rather than the visible label. An
    "Outdated" badge does not remove the button, so outdated-but-uncommitted
    suggestions are still counted (and remain committable).
    """
    return int(page.locator(SELECTOR_COMMIT_SUGGESTION_BUTTON).count())


def _commit_last_suggestion(page: Any, message: str) -> None:
    """Commit the bottom-most suggestion via its "Commit suggestion" dialog.

    Bottom-to-top: the last button in DOM order targets the lowest hunk, so
    committing it first does not shift the anchors of the suggestions above it.

    [BROWSER-SELECTOR] Clicking opens a Primer "Commit suggestion" dialog whose
    commit-message textbox is pre-filled (overwritten with ``message`` when that
    field is present); the primary submit button is "Apply Suggestion".
    """
    page.locator(SELECTOR_COMMIT_SUGGESTION_BUTTON).last.click()
    message_box = page.get_by_role("textbox", name=TEXTBOX_COMMIT_MESSAGE)
    if message_box.count() > 0:
        message_box.fill(message)
    page.get_by_role("button", name=BUTTON_APPLY_SUGGESTION).click()


def _wait_for_settle(page: Any) -> None:
    """Wait for the page to re-render after a commit (dialog closes, new HEAD)."""
    page.wait_for_load_state("networkidle")


def drain_commit_rescan(
    page: Any,
    *,
    dry_run: bool,
    message: str = DEFAULT_COMMIT_MESSAGE,
    max_iterations: int = DEFAULT_MAX_DRAIN_ITERATIONS,
) -> dict:
    """Commit Copilot suggestions one-by-one, bottom-to-top, rescanning between.

    Each iteration commits the bottom-most suggestion (the page re-renders
    against the new HEAD), then rescans, until none remain or ``max_iterations``
    is reached. In ``dry_run`` mode, counts the suggestions that WOULD be
    committed (single pass) and commits nothing.

    Multiple commits are expected and fine — the AI PR loop squashes them later.
    Because an "Outdated" badge does not remove the commit button, the loop
    drains every suggestion regardless of commit order.
    """
    total_candidates = 0
    commits = 0
    iterations = 0
    cap_hit = False
    for iterations in range(1, max_iterations + 1):
        pending = count_commit_suggestion_buttons(page)
        if pending == 0:
            break
        if dry_run:
            logger.info(
                "[BROWSER-APPLY] dry-run: %d suggestion(s) would be committed (bottom-to-top)",
                pending,
            )
            total_candidates += pending
            break
        _commit_last_suggestion(page, message)
        total_candidates += 1
        commits += 1
        _wait_for_settle(page)
        if iterations == max_iterations:
            cap_hit = True
    if cap_hit:
        remaining = count_commit_suggestion_buttons(page)
        if remaining > 0:
            logger.warning(
                "[BROWSER-APPLY] max_iterations cap (%d) reached with %d suggestion(s) still unapplied; "
                "re-run to apply the rest",
                max_iterations,
                remaining,
            )
    return {
        "candidates": total_candidates,
        "commits": commits,
        "iterations": iterations,
        "dry_run": dry_run,
    }


# ---------------------------------------------------------------------------
# Browser lifecycle and high-level entry points
# ---------------------------------------------------------------------------


@contextlib.contextmanager
def _authenticated_page(credentials: BrowserCredentials, *, headless: bool = True) -> Iterator[Any]:
    """Launch a headless browser, perform a fresh IdP login, and yield the page."""
    sync_playwright = _require_sync_playwright()
    playwright = sync_playwright().start()
    try:
        browser = playwright.chromium.launch(headless=headless)
        try:
            context = browser.new_context()
            page = context.new_page()
            perform_idp_login(page, credentials)
            yield page
        finally:
            browser.close()
    finally:
        playwright.stop()


def _pr_conversation_url(repo: str, pr_number: int) -> str:
    """Build the URL of the PR Conversation tab (where CCR suggestions render)."""
    return f"https://github.com/{repo}/pull/{pr_number}"


def count_browser_autofix_candidates(
    repo: str,
    pr_number: int,
    *,
    credentials_path: str | os.PathLike[str] | None = None,
) -> int:
    """Authenticate, open the PR conversation page, and count suggestion buttons.

    Used by the discovery ``browser_strategy`` to detect candidates without
    committing. Raises :class:`BrowserAutofixUnavailable` when optional deps are
    missing and :class:`BrowserCredentialError` when credentials cannot resolve.
    """
    credentials = load_credentials(credentials_path)
    with _authenticated_page(credentials) as page:
        page.goto(_pr_conversation_url(repo, pr_number))
        return count_commit_suggestion_buttons(page)


def _resolve_threads(pr_number: int, repo: str, comment_ids: list[int]) -> dict:
    """Resolve review threads for applied comments, reusing the existing logic."""
    from agentic_devtools.cli.github.apply_thread_autofix import _resolve_thread_for_comment

    resolved: list[int] = []
    failed: list[int] = []
    for comment_id in comment_ids:
        if _resolve_thread_for_comment(pr_number, repo, comment_id):
            resolved.append(comment_id)
        else:
            failed.append(comment_id)
    return {"resolved": resolved, "failed": failed}


def _fetch_pr_head_sha(pr_number: int, repo: str) -> str | None:
    """Best-effort fetch the current PR head SHA via the gh CLI.

    Returns the 40-character SHA string on success, or ``None`` when the gh
    CLI is unavailable, returns a non-zero exit code, or produces empty output.
    Never raises — callers treat the return value as informational.
    """
    try:
        result = run_safe(
            ["gh", "pr", "view", str(pr_number), "--repo", repo, "--json", "headRefOid", "--jq", ".headRefOid"],
            capture_output=True,
            text=True,
            shell=False,
        )
    except Exception as exc:
        logger.debug("[BROWSER-APPLY] could not fetch PR head SHA: %s", exc)
        return None
    if result.returncode != 0:
        logger.debug(
            "[BROWSER-APPLY] gh pr view exited %d when fetching head SHA: %s",
            result.returncode,
            (result.stderr or "").strip(),
        )
        return None
    sha = result.stdout.strip()
    return sha if sha else None


def apply_pr_suggestions_via_browser(
    pr_number: int,
    repo: str,
    *,
    dry_run: bool = False,
    resolve: bool = True,
    message: str = DEFAULT_COMMIT_MESSAGE,
    comment_ids: list[int] | None = None,
    credentials_path: str | os.PathLike[str] | None = None,
    headless: bool = True,
) -> dict:
    """Apply Copilot autofix suggestions on a PR by driving the browser UI.

    In ``dry_run`` mode, authenticates, navigates and counts the suggestions it
    WOULD apply (bottom-to-top) without committing. Otherwise applies and commits
    them and (when ``resolve`` and ``comment_ids`` are provided) resolves the
    corresponding review threads.

    When one or more commits are created via the GitHub UI, the function
    best-effort fetches the updated PR head SHA via ``gh pr view`` and stores it
    in ``result["commit"]``. This mirrors the non-browser strategy, so downstream
    logs and state can reference the produced commit. On failure the field is
    ``None`` (never raises).
    """
    credentials = load_credentials(credentials_path)
    result: dict = {
        "strategy": "browser",
        "dry_run": dry_run,
        "applied": 0,
        "commits": 0,
        "files_changed": [],
        "resolution": None,
        "commit": None,
        "error": None,
    }
    with _authenticated_page(credentials, headless=headless) as page:
        page.goto(_pr_conversation_url(repo, pr_number))
        drain = drain_commit_rescan(page, dry_run=dry_run, message=message)
    result["applied"] = drain["candidates"]
    result["commits"] = drain["commits"]
    if dry_run:
        logger.info(
            "[BROWSER-APPLY] dry-run complete: %d candidate suggestion(s) on PR #%d (no commit)",
            drain["candidates"],
            pr_number,
        )
        return result
    if drain["commits"] > 0:
        result["commit"] = _fetch_pr_head_sha(pr_number, repo)
    if resolve and comment_ids:
        result["resolution"] = _resolve_threads(pr_number, repo, comment_ids)
    elif resolve:
        logger.warning(
            "[BROWSER-APPLY] resolve=True but no comment_ids provided; skipping thread "
            "resolution — Copilot threads on PR #%d may remain open despite applied suggestions",
            pr_number,
        )
    return result
