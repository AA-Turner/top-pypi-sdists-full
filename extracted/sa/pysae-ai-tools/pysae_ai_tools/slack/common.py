"""Shared Slack helpers used by ``pysae-ai-tools slack`` subcommands."""

import os
import sys
from pathlib import Path

from ..common.project_config import load_project_config

# Plain-language hints for the Slack API error codes we hit most, so a failed
# post explains itself in the logs instead of leaking a bare error code.
_SLACK_ERROR_HINTS = {
    "channel_not_found": "channel unknown or not visible to this token (empty or wrong channel id?)",
    "not_in_channel": "the token's user/bot is not in this channel — invite it, or pass --join for public channels",
    "is_archived": "the channel is archived",
    "invalid_auth": "the Slack token is invalid",
    "token_expired": "the Slack token has expired — re-resolve it with /env-resolve",
    "token_revoked": "the Slack token was revoked — re-resolve it with /env-resolve",
    "missing_scope": "the token is missing a required OAuth scope",
    "account_inactive": "the Slack account behind this token is deactivated",
    "ratelimited": "Slack rate-limited the request — retry later",
}


def describe_slack_error(code: str) -> str:
    """Return the Slack error ``code`` with a plain-language hint when we know it."""
    hint = _SLACK_ERROR_HINTS.get(code)
    return f"{code} ({hint})" if hint else code


def log_not_posted(reason: str) -> None:
    """Print, on stderr, a clear one-line reason why no Slack message was posted.

    stdout stays reserved for the machine-readable JSON result the skills parse;
    this human line goes to stderr so the cause stays visible even when the caller
    runs the command best-effort (``… || true``) and ignores the exit code.
    """
    print(f"[slack] message not posted — {reason}", file=sys.stderr)


# Slack message metadata event_type stamped on every review-request / AI-validation
# message posted by ``slack post-message --review-project … --review-mr-iid …``.
# ``ask-review`` / ``mark-merged`` match on this structured metadata (immune to
# substring collisions and to unrelated messages that merely cite the MR URL),
# falling back to a footer-scoped URL scan only for legacy messages posted before
# the metadata existed.
REVIEW_METADATA_EVENT_TYPE = "ai_tools_review_request"

# Slack message metadata event_type stamped on the pre-release recap header posted
# by ``code-review-pre-release`` (payload ``{project, tag}``). ``find-thread`` matches
# on it to locate the existing recap thread before posting a fresh one, instead of
# matching the rendered header text by prefix.
PRERELEASE_RECAP_METADATA_EVENT_TYPE = "ai_tools_prerelease_recap"

# Substring uniquely identifying a message our tooling posted. It must be specific
# enough that a human can't reproduce it incidentally: we key on the PyPI link the
# ``--ai-footer`` attribution embeds (``<https://pypi.org/project/pysae-ai-tools|…>``),
# NOT on the bare package name (which a teammate could type in a CLI snippet or quote).
# Used as the legacy-fallback guard so the URL scan only ever matches *our* messages,
# never a human's that happens to cite the same MR link. Must stay a substring of
# ``post_message.AI_FOOTER_TEXT``.
AI_TOOLS_FOOTER_MARKER = "pypi.org/project/pysae-ai-tools"


def resolve_channel(value: str) -> str:
    """Map the ``mep`` channel alias to its ID **from the repo config**, else passthrough.

    ``--channel mep`` (the deploy/MEP broadcast alias used by CI jobs) resolves to the
    current repo's ``slack.mep_channel_id`` (declared in its ``.pysae-ai-tools.yaml`` —
    there is no schema default, every repo sets it). Any other value — a real channel ID
    or unknown name — passes through unchanged, so ``--channel C0123ABCDEF`` keeps working,
    as does ``mep`` itself when the repo declares no ``mep_channel_id``.
    """
    if value.lstrip("#") != "mep":
        return value
    try:
        cfg = load_project_config(Path.cwd())
    except Exception:  # noqa: BLE001 — never fail channel resolution on a bad/absent config
        cfg = None
    return (cfg.slack.mep_channel_id if cfg else None) or value


def get_slack_token() -> str:
    """Return the Slack API token to use for chat/history calls.

    - In CI (``$CI`` set), the bot token is the only viable option — user
      tokens require an interactive OAuth flow.
    - Locally, prefer the user token so messages appear under the
      developer's identity, falling back to the bot token if only that one
      is set.
    """
    if os.environ.get("CI"):
        return os.environ.get("SLACK_BOT_TOKEN", "")
    return os.environ.get("SLACK_USER_TOKEN") or os.environ.get("SLACK_BOT_TOKEN", "")
