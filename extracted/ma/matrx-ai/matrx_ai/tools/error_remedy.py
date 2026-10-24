"""What a tool failure MEANS, said to the agent that has to act on it.

A tool result is read by a model, and the model then tells a person what
happened. So an error envelope that carries only the database's wording is not
neutral — it is the sentence the person hears.

2026-09-12 23:24: the Masterwork Conductor tried to change how a desk's Writer
thinks. The write hit ``agent.definition``'s provenance CHECK — *"This write
declares actor_tier=code, but names no actor_system … x-matrx-actor-system on
the client channel, or the app.actor_system GUC on a server channel"* — which is
a missing HEADER on OUR write path. The envelope handed the model that text plus
the executor's generic *"Check the error details and try with different
parameters"*, and the Conductor told the Expert:

    "I am blocked by system policy … edits to any agent's contract must come
    from an authorized human channel."

Nothing about her request was disallowed. So: a failure class we can NAME gets
one line of cause and one line of remedy attached here, in front of the raw
text, and the raw text is still carried verbatim after it. Matching runs over
:func:`matrx_utils.error_text.classification_text` — never ``str(exc)`` — because
the rendered text can carry the caller's own payload (a document, a transcript),
and a ladder that matches on a payload tells a person something false about
their own words.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from matrx_utils.error_text import classification_text


@dataclass(frozen=True)
class ErrorRemedy:
    """One line of cause, one line of remedy, for a failure class we know."""

    cause: str
    remedy: str

    def prefix(self, raw_message: str) -> str:
        """The envelope message: the diagnosis first, the raw text kept after it."""
        return f"{self.cause} {self.remedy}\n\nUnderlying error: {raw_message}"


#: A write that reached Postgres without naming the system that made it. The
#: CHECK is right (an AI write must say which agent/system it is); the write path
#: forgot to declare. Never a permission, policy or entitlement refusal.
UNDECLARED_ACTOR_SYSTEM = ErrorRemedy(
    cause=(
        "This failed on a PLATFORM DEFECT, not on policy or permission: the write "
        "reached the database without naming which system made it (the "
        "app.actor_system declaration is missing on this code path). Nothing about "
        "the request is disallowed, and no approval, human channel or extra "
        "authorization is required."
    ),
    remedy=(
        "Retry the identical call once. If it fails the same way, say plainly that a "
        "platform defect is blocking the change (the tool's write path must declare "
        "its actor system) and report it — never tell the person the edit is "
        "forbidden, needs a human channel, or needs approval."
    ),
)

_UNDECLARED_ACTOR_MARKERS: tuple[str, ...] = (
    "names no actor_system",
    "actor_system on a server channel",
    "x-matrx-actor-system",
)

_EXECUTOR_GENERIC_PLACEHOLDER = "Check the error details and try with different parameters."


def error_remedy_for(message: str | None) -> ErrorRemedy | None:
    """The remedy for a failure class we can name, or None.

    ``message`` is any rendered error text; only its bounded
    :func:`classification_text` head is ever matched.
    """
    if not message:
        return None
    text = classification_text(str(message)).lower()
    if any(marker.lower() in text for marker in _UNDECLARED_ACTOR_MARKERS):
        return UNDECLARED_ACTOR_SYSTEM
    return None


def annotate_tool_error(error: Any) -> Any:
    """Attach cause + remedy to a ``ToolError`` whose class we recognize.

    Mutates and returns the error so the caller can inline it. A class we do not
    recognize is left exactly as it was — this never invents a diagnosis.

    A tool's OWN ``suggested_action`` is kept and the remedy is APPENDED after
    it as ``"<tool's own> Also: <remedy>"``: the tool names the next call with
    its argument names, which this generic ladder cannot know, so overwriting
    it would hand the model a vaguer instruction than the one it had.
    The executor's own catch-all placeholder is not a tool's instruction and
    is replaced.
    """
    remedy = error_remedy_for(getattr(error, "message", None))
    if remedy is None:
        return error
    error.message = remedy.prefix(error.message)
    own = (getattr(error, "suggested_action", None) or "").strip()
    if not own:
        error.suggested_action = remedy.remedy
    elif own == _EXECUTOR_GENERIC_PLACEHOLDER:
        error.suggested_action = remedy.remedy
    elif remedy.remedy not in own:
        error.suggested_action = f"{own} Also: {remedy.remedy}"
    error.is_retryable = True
    return error


# ── KNOWN SHELL FAILURES: one recovery line per terminal failure we recognize ──


def shell_recovery_hint(error_text: str, command: str) -> str | None:
    """Pattern-match common terminal failures and return a hint that tells
    the agent EXACTLY how to recover. Pure additive — never replaces the
    original error, just appends actionable guidance. (Moved here from the
    shell tool 2026-10-23 so every known failure lives in this one file.)
    """
    text = (error_text or "").lower()
    cmd = (command or "").lower()

    # Git HTTPS auth failure — the most common one we've seen.
    if "could not read username for 'https://github.com'" in text or (
        "fatal: authentication" in text and "github" in cmd
    ):
        return (
            "Git is asking for HTTPS credentials but the sandbox has none. Two ways to fix:\n"
            "  1. Register a GitHub token via the orchestrator's credentials API:\n"
            '       POST /sandboxes/{id}/credentials  body: {"kind":"github","token":"<pat>"}\n'
            "     The sandbox configures git's credential helper; subsequent clones/pulls work.\n"
            "  2. OR clone via SSH: change the URL to git@github.com:<owner>/<repo>.git and ensure\n"
            "     ~/.ssh/id_ed25519 is configured (the sandbox's ssh setup populates a key on\n"
            "     boot for orchestrator-spawned sandboxes).\n"
            "  3. OR for read-only public repos, append ``|| true`` to skip auth — but that\n"
            "     only works for genuinely-public repos."
        )

    # SSH auth failure.
    if "permission denied (publickey)" in text:
        return (
            "SSH key auth failed. The sandbox has no key registered for the target host. "
            "Drop a private key in /home/agent/.ssh/id_ed25519 (chmod 600) and the matching "
            "public key into the remote's authorized_keys. For GitHub specifically, prefer "
            "the /credentials API (token-based) — it's simpler than SSH key plumbing."
        )

    # No internet egress (rare but happens during ops work).
    if "could not resolve host" in text or "name or service not known" in text:
        return (
            "DNS resolution failed inside the sandbox. The sandbox network may be misconfigured "
            "or the orchestrator's network policy may have changed. Try `cat /etc/resolv.conf` "
            "and `curl -v https://1.1.1.1` to confirm; if both fail, ping the operator to "
            "check the orchestrator's docker network."
        )

    # Out-of-disk on the sandbox volume.
    if "no space left on device" in text:
        return (
            "The sandbox volume is full. List large directories with `du -sh /home/agent/* | sort -h` "
            "and clean up. Reset the sandbox (FE Inspector → Reset, optionally with 'wipe volume') "
            "if you want a fresh /home/agent."
        )

    # pandas without a Parquet engine (every Hugging Face dataset is Parquet).
    if "unable to find a usable engine" in text and "pyarrow" in text:
        return (
            "pandas has no Parquet engine. Run `pip install pyarrow` and call again. For a "
            "Hugging Face dataset you can also skip the file: "
            "https://datasets-server.huggingface.co/rows?dataset=<id>&config=<cfg>&split=<split> "
            "returns the rows as JSON."
        )

    # Python ModuleNotFoundError.
    if "modulenotfounderror" in text:
        return (
            "Module not installed. Inside a sandbox, `pip install <pkg>` (or `uv pip install`) is "
            "always available — go ahead and install it. The sandbox is the boundary; don't ask "
            "the user to install for you."
        )

    return None


# ── KNOWN OUTCOMES: what a tool's OUTPUT means, success or not ─────────────────
#
# A tool can "succeed" and still hand the agent a dead end: on 2026-10-24
# (conversation 577db529) a shell_python fetch of lmarena.ai returned status 403
# and Cloudflare's "Just a moment..." page inside a perfectly successful result.
# Nothing told the agent that a plain HTTP client will keep getting that wall and
# a real browser will not. Each rule below names one such outcome and the next
# step; the executor appends its notice to EVERY tool result (``model_notices``,
# streamed and persisted), so a new rule reaches every tool at once.
#
# A rule is ADDITIVE: it never changes the output, never retries on its own, and
# matches only markers specific enough that a normal page or log cannot trip it.

#: Bounded head of a result we ever scan — a hint is not worth a full scan of a
#: multi-megabyte output.
_OUTCOME_SCAN_CHARS = 200_000

#: Text-bearing keys of a structured tool output (shell_execution, web reads, …).
_OUTPUT_TEXT_KEYS: tuple[str, ...] = ("stdout", "stderr", "content", "text", "html", "body")

#: Markers that only a bot-protection interstitial carries, anywhere in the text.
_BOT_WALL_STRONG_MARKERS: tuple[str, ...] = (
    "challenges.cloudflare.com",
    "/cdn-cgi/challenge-platform",
    "cf_chl_opt",
    "_incapsula_resource",
    "px-captcha",
    "captcha-delivery.com",
)

#: Tools that open a page in a real browser, in the order we recommend them.
_BROWSER_TOOLS: tuple[str, ...] = ("cloud_browser", "desktop_browser", "load_browser_tools")

#: A challenge page's title is the phrase plus a vendor suffix at most.
_WALL_TITLE_MAX_CHARS = 60

_TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def _result_text(result: Any) -> str:
    """Every text the agent will read from this result, bounded."""
    parts: list[str] = []
    output = getattr(result, "output", None)
    if isinstance(output, dict):
        parts.extend(str(output[k]) for k in _OUTPUT_TEXT_KEYS if output.get(k))
    elif isinstance(output, str):
        parts.append(output)
    error = getattr(result, "error", None)
    if error is not None and getattr(error, "message", None):
        parts.append(str(error.message))
    return "\n".join(parts)[:_OUTCOME_SCAN_CHARS]


def _bot_wall_in(text: str) -> str | None:
    """The bot-protection wall this text shows, named, or None."""
    from matrx_scraper.challenge_census import BLOCK_TITLE_MARKERS, CHALLENGE_TITLE_MARKERS

    lowered = text.lower()
    markers = tuple(
        m for m in (*CHALLENGE_TITLE_MARKERS, *BLOCK_TITLE_MARKERS) if m != "cloudflare"
    )
    for raw_title in _TITLE_RE.findall(text):
        title = " ".join(raw_title.split()).lower()
        # The wall's title IS the phrase ("Just a moment...", "Access Denied"); an
        # article ABOUT it ("Fixing 'access denied' errors") only contains it.
        if len(title) <= _WALL_TITLE_MAX_CHARS and title.startswith(markers):
            return f"a bot-protection page titled {' '.join(raw_title.split())[:80]!r}"
    marker = next((m for m in _BOT_WALL_STRONG_MARKERS if m in lowered), None)
    return f"a bot-protection challenge ({marker})" if marker else None


def _browser_next_step(active_tools: frozenset[str] | None) -> str:
    if active_tools is None:
        return "Open the page with cloud_browser — a real browser that passes these checks."
    tool = next((t for t in _BROWSER_TOOLS if t in active_tools), None)
    if tool == "load_browser_tools":
        return "Call load_browser_tools, then open the page in that real browser."
    if tool:
        return f"Open the page with {tool} — a real browser that passes these checks."
    return (
        "No browser tool is attached to this run: tell the person this site needs a "
        "browser, or find the same data from an official API or dataset."
    )


def known_outcome_notices(result: Any, *, active_tools: frozenset[str] | None) -> list[str]:
    """The NOTICE lines for every known outcome this result shows (usually none)."""
    text = _result_text(result)
    if not text:
        return []
    notices: list[str] = []
    wall = _bot_wall_in(text)
    if wall:
        notices.append(
            f"NOTICE: a fetch here got {wall}, not the page. A plain HTTP client (curl, "
            f"requests, web) will keep getting it — do not retry the same way. "
            f"{_browser_next_step(active_tools)}"
        )
    return notices


__all__ = [
    "UNDECLARED_ACTOR_SYSTEM",
    "ErrorRemedy",
    "annotate_tool_error",
    "error_remedy_for",
    "known_outcome_notices",
    "shell_recovery_hint",
]
