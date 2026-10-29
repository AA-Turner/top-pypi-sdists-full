"""The docs step of `plato vault mint token`: before the computer-use walk, a cheap model with web
search reads the vendor's developer docs and answers with a short :class:`DocsPlan` (where to make
the OAuth app, the scopes for a refresh token, the endpoints, a "who am I" URL). The plan goes into
this run's walker goal only; nothing is stored, so no per-vendor recipe builds up. A missing or
failed plan never stops the mint: the walker still has its own web tools.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
from collections.abc import Callable
from contextlib import suppress
from urllib.parse import urlparse

from pydantic import ValidationError

from plato.cli.vault import app_portal, pi_browser
from plato.cli.vault.mint_models import DocsPlan, DocsReply, VaultItem
from plato.cli.vault.prompts import GoalTemplate, render_prompt

DOCS_MODEL = "haiku"
DOCS_TOOLS = "WebSearch,WebFetch"
DOCS_TIMEOUT_S = 300
DOCS_TAG = "@@VAULT "


class DocsError(RuntimeError):
    """The docs step gave no usable plan."""


def docs_command(agent: str, goal: str) -> list[str]:
    """``claude -p`` on the docs model with web search and fetch only, and no MCP server."""
    return [
        agent,
        "-p",
        goal,
        "--model",
        DOCS_MODEL,
        "--tools",
        DOCS_TOOLS,
        "--allowedTools",
        DOCS_TOOLS,
        "--permission-mode",
        "dontAsk",
        "--strict-mcp-config",
        "--mcp-config",
        '{"mcpServers":{}}',
    ]


def docs_goal(login_key: str, item: VaultItem, vendor_domains: list[str], hint: str | None) -> str:
    """The docs model's goal: the vendor by its login key and hosts. No account name, no secret."""
    host = urlparse(item.login_url).hostname if item.login_url else None
    return render_prompt(
        GoalTemplate.mint_docs,
        login_key=login_key,
        login_host=host or "(no login URL)",
        vendor_domains=", ".join(vendor_domains) or "(none given)",
        hint=f"Note from the person who ran this: {hint}" if hint else "",
        schema=json.dumps(DocsPlan.model_json_schema(), separators=(",", ":")),
    )


def parse_docs(output: str) -> DocsPlan:
    """The last ``@@VAULT {"plan": ...}`` line of the docs model's reply."""
    for raw in reversed(output.splitlines()):
        idx = raw.find(DOCS_TAG)
        if idx < 0:
            continue
        try:
            reply = DocsReply.model_validate_json(raw[idx + len(DOCS_TAG) :])
        except ValidationError as e:
            raise DocsError(f"the plan does not fit the schema ({e.error_count()} errors)") from None
        if reply.plan is None:
            raise DocsError(f"the docs model found no way: {reply.reason or 'no reason given'}")
        return reply.plan
    raise DocsError("the docs model ended without a @@VAULT plan line")


def run_in_group(cmd: list[str], *, timeout: float, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    """``cmd`` in a session of its own: a timeout kills claude-seat and the claude it started
    together (as :func:`pi_browser.run_pi_agent` does), then raises ``TimeoutExpired``. A Ctrl-C
    (or any other exit before it ends) kills the group the same way before it raises."""
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        start_new_session=True,
    )
    pi_browser.LIVE_AGENTS.add(proc.pid)  # new session: the pgid is the pid
    try:
        out, err = proc.communicate(timeout=timeout)
    except BaseException:
        # A timeout, or a Ctrl-C: the group is in a session of its own, so the terminal's
        # signal does not reach it, and the abort cleanup does not exist yet at this step.
        with suppress(ProcessLookupError, PermissionError):
            os.killpg(proc.pid, signal.SIGKILL)
        proc.communicate()
        raise
    finally:
        pi_browser.LIVE_AGENTS.discard(proc.pid)
    return subprocess.CompletedProcess(cmd, proc.returncode, stdout=out, stderr=err)


def read_docs(
    goal: str,
    tools: app_portal.PortalTools,
    runner: Callable[..., subprocess.CompletedProcess[str]] = run_in_group,
) -> tuple[DocsPlan | None, str | None]:
    """(the plan, None), or (None, why there is none). Never raises: the walk goes on without it."""
    if tools.agent is None:
        return None, "no claude CLI for the docs step"
    try:
        proc = runner(docs_command(tools.agent, goal), timeout=DOCS_TIMEOUT_S, env=app_portal.agent_env())
    except subprocess.TimeoutExpired:
        return None, f"the docs step took over {DOCS_TIMEOUT_S} s"
    except OSError as e:
        return None, f"the docs step did not start ({type(e).__name__})"
    if proc.returncode != 0:
        return None, f"the docs step exited {proc.returncode}"
    try:
        return parse_docs(proc.stdout), None
    except DocsError as e:
        return None, str(e)


def plan_text(plan: DocsPlan | None) -> str:
    """The plan as the walker reads it, or the instruction to look the docs up itself."""
    if plan is None:
        return "Find how in the vendor's own developer docs (WebSearch, WebFetch)."
    lines = [
        "Another model read the vendor's developer docs for you. Use it as a map, not as truth: when a page",
        "differs, trust the page and check the docs yourself (WebSearch, WebFetch).",
        f"- Where to make the app: {plan.portal_url}",
        *(f"- {step}" for step in plan.steps),
    ]
    if plan.scopes:
        lines.append(f"- Scopes: {' '.join(plan.scopes)}")
    if plan.refresh_token:
        lines.append(f"- Refresh token: {plan.refresh_token}")
    for name, value in (
        ("Authorize URL", plan.authorize_url),
        ("Token URL", plan.token_url),
        ("Who-am-I URL for vault.check", plan.check_url),
    ):
        if value:
            lines.append(f"- {name}: {value}")
    lines.append(f"- Docs: {', '.join(plan.docs)}")
    return "\n".join(lines)
