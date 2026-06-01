"""Claude Code subprocess LLM client (v0.1.148 / #353).

Lets users with a Claude Max / Pro subscription run efterlev without
paying per-token API costs, by routing LLM calls through the locally-
installed `claude` CLI. The CLI authenticates via OAuth against the
user's Claude subscription (when no `ANTHROPIC_API_KEY` env var
overrides it), so calls bill against the flat subscription instead
of the Anthropic Messages API.

Implementation: subprocess invocation of `claude --print
--output-format json --model <m> --append-system-prompt <s>`, piping
the user message in on stdin. Parses the JSON envelope (`result`
field carries the assistant text; `usage.input_tokens` / `output_tokens`
expose token counts) and returns it as `LLMResponse`.

Caveats (surfaced in /setup wizard + LIMITATIONS.md):

- **Subscription terms judgment-call**. Anthropic's Pro/Max ToS
  doesn't explicitly bless third-party tool integrations using
  subscription auth, but Hermes/OpenClaw/similar tools do this and
  it's widely understood as accepted use. Users decide.
- **Requires `claude` binary installed and signed-in**. We detect at
  call time and raise a clear error if it's missing. `/doctor`
  surfaces the check.
- **`ANTHROPIC_API_KEY` is stripped from the subprocess env** so a
  system-wide API key doesn't accidentally route subscription-backend
  calls through pay-per-token billing (v0.1.149 / #354). The user's
  shell env stays untouched; other tools / other efterlev backends
  still see the var.
- **Streaming degrades**. `claude --print` returns the full text
  after generation completes; we surface that via `on_chunk` as a
  single callback at the end (same shape as Bedrock Converse, which
  also doesn't true-stream).
- **Cost telemetry**: `total_cost_usd` is reported as 0.0 (the
  subscription is flat-rate; no per-call billing). Receipts.log
  entries record zero token cost; this is correct, not a bug.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from efterlev.errors import AgentError
from efterlev.llm.base import LLMMessage, LLMResponse

# Env vars `claude` reads for API-key auth. When the user picks the
# claude_code backend they're opting into subscription OAuth; we strip
# these from the subprocess env so a system-wide ANTHROPIC_API_KEY
# doesn't accidentally route calls through pay-per-token billing.
# The user's shell env is untouched — other tools / other backends
# still see whatever they're configured to see. v0.1.149 / #354.
_API_KEY_ENV_VARS_TO_STRIP = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
)


def _subprocess_env_for_claude() -> dict[str, str]:
    """Return a copy of os.environ with API-key vars removed.

    Lets users keep ANTHROPIC_API_KEY exported globally for other tools
    (or for switching back to the `anthropic` backend) without having
    to unset it every time they want efterlev to use the subscription.
    """
    env = dict(os.environ)
    for var in _API_KEY_ENV_VARS_TO_STRIP:
        env.pop(var, None)
    return env


def _hash_prompt(system: str, messages: list[LLMMessage]) -> str:
    import hashlib

    h = hashlib.sha256()
    h.update(system.encode("utf-8"))
    for m in messages:
        h.update(b"\x00")
        h.update(m.content.encode("utf-8"))
    return h.hexdigest()


_DEFAULT_TIMEOUT_SECONDS = 300.0


def _timeout_from_env() -> float:
    """Per-call timeout from EFTERLEV_LLM_TIMEOUT (seconds), default 300.

    Invalid / non-positive values fall back to the default rather than
    raising — a typo in an env var shouldn't crash the agent pipeline.
    """
    raw = os.environ.get("EFTERLEV_LLM_TIMEOUT", "").strip()
    if not raw:
        return _DEFAULT_TIMEOUT_SECONDS
    try:
        value = float(raw)
    except ValueError:
        return _DEFAULT_TIMEOUT_SECONDS
    return value if value > 0 else _DEFAULT_TIMEOUT_SECONDS


@dataclass
class ClaudeCodeClient:
    """LLMClient that subprocesses the local `claude` CLI in --print mode.

    Stateless — every `complete()` call spawns a fresh `claude` process.
    No session/conversation handle is kept between calls (efterlev's
    agents are stateless per call anyway).

    `fallback_model`: matches the AnthropicClient / AnthropicBedrockClient
    field for uniformity; not currently used by `claude --print` (the
    CLI doesn't expose its own fallback flag for --print mode).
    """

    fallback_model: str | None = None
    # Bin path override for tests / non-default installs.
    binary_path: str = "claude"
    # Per-call timeout in seconds. v0.1.175 / #381: configurable via
    # EFTERLEV_LLM_TIMEOUT (seconds) so a slow subscription backend or an
    # unusually large prompt can be given more headroom without a code
    # change. Default 300s. Gap-agent calls on Sonnet/Haiku typically take
    # 30-90s; the default catches genuine hangs without truncating a
    # legitimate long classification. (The real fix for the Opus-on-
    # subscription latency trap is the Sonnet default in `efterlev init`;
    # this knob is defensive depth.)
    timeout_seconds: float = field(default_factory=lambda: _timeout_from_env())

    def complete(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int = 4096,
        on_chunk: Callable[[str], None] | None = None,
    ) -> LLMResponse:
        # Validate the call shape before touching the filesystem so unit tests
        # that don't have `claude` installed still exercise the precondition
        # checks. (CI doesn't ship the Claude Code CLI.)
        if not messages:
            raise AgentError("claude_code: messages list cannot be empty")

        binary = shutil.which(self.binary_path) or self.binary_path
        if not shutil.which(self.binary_path):
            raise AgentError(
                "claude_code backend selected but the `claude` binary is not on "
                "PATH. Install Claude Code (https://claude.com/claude-code) and "
                "sign in with your Pro/Max account, then re-run."
            )
        # Concatenate user messages with separators; efterlev agents only
        # ever send a single user message today, but the protocol allows
        # multiple — preserve all of them.
        user_text = "\n\n".join(m.content for m in messages)

        cmd = [
            binary,
            "--print",
            "--output-format",
            "json",
            "--model",
            model,
            "--append-system-prompt",
            system,
            # `--max-turns 1` keeps the CLI from invoking tools or chaining
            # responses; we want a single completion, not an agent loop.
            "--max-turns",
            "1",
        ]
        try:
            proc = subprocess.run(  # nosemgrep — binary from shutil.which, fixed-shape args
                cmd,
                input=user_text,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
                # v0.1.149 / #354: strip API-key env vars so subscription
                # OAuth takes effect even when the user has a system-wide
                # ANTHROPIC_API_KEY set for other tools.
                env=_subprocess_env_for_claude(),
            )
        except subprocess.TimeoutExpired as e:
            raise AgentError(
                f"claude_code: `claude --print` timed out after "
                f"{self.timeout_seconds}s. The model may be overloaded or "
                "the prompt may be too long for subscription throughput."
            ) from e

        if proc.returncode != 0:
            raise AgentError(
                f"claude_code: `claude --print` exited {proc.returncode}. "
                f"stderr: {proc.stderr.strip()[:500] or '(empty)'}"
            )

        try:
            envelope: dict[str, Any] = json.loads(proc.stdout)
        except json.JSONDecodeError as e:
            raise AgentError(
                f"claude_code: response from `claude --print` was not valid "
                f"JSON: {e}. First 200 chars of stdout: {proc.stdout[:200]!r}"
            ) from e

        # The --output-format json envelope shape:
        #   {"type":"result","subtype":"success","is_error":false,
        #    "result":"<assistant text>",
        #    "usage":{"input_tokens":N,"output_tokens":M, ...},
        #    "total_cost_usd":0,  # 0 on subscription; non-zero on API key
        #    ...}
        if envelope.get("is_error"):
            api_status = envelope.get("api_error_status")
            err_text = envelope.get("result", "(no error text)")
            hint = ""
            if api_status == 401:
                # v0.1.149+: API-key env vars are stripped by
                # `_subprocess_env_for_claude`, so a 401 usually means
                # the subscription session is stale rather than an
                # env-var override.
                hint = (
                    " — your Claude Code subscription session may be expired. "
                    "Run `claude` interactively once to refresh OAuth, then retry."
                )
            raise AgentError(
                f"claude_code: claude --print returned an error "
                f"(api_error_status={api_status}): {err_text}{hint}"
            )

        text = envelope.get("result")
        if not isinstance(text, str):
            raise AgentError(
                "claude_code: response envelope missing 'result' field "
                f"(got keys: {sorted(envelope.keys())[:8]})"
            )

        # v0.1.151 / #356: do NOT trust the envelope's usage block on
        # subscription. Observed customer output: 180 input tokens /
        # 441,085 output tokens for a single /report pipeline run — the
        # numbers don't reflect actual Anthropic API token counts (the
        # input is way undercounted, output is way overcounted, likely
        # character count rather than tokens). Multiplying these by
        # Anthropic API rates produced a fake "$6.62" cost for a run
        # that actually billed $0 against the subscription.
        #
        # Forcing tokens=0 makes the cost-summary correctly show $0
        # contribution from subscription-backed calls. The banner's
        # cost line treats backend=="claude_code" as "subscription
        # (no per-call billing)" via format_cost_summary, so the user
        # sees a meaningful message instead of a misleading dollar
        # figure.
        input_tokens = 0
        output_tokens = 0

        # Surface the cached text via on_chunk for parity with the streaming
        # backends — gap-agent's progress reporter expects to see at least
        # one chunk to fire the per-KSI extraction.
        if on_chunk is not None and text:
            on_chunk(text)

        # `prompt_hash` is the sha256 of system+messages as we sent them.
        # Independent of what claude --print returns in `session_id`.
        prompt_hash = _hash_prompt(system, messages)

        # `model` not always echoed back by claude --print; default to what
        # we requested so provenance pins something meaningful.
        envelope_model = envelope.get("model")
        served_model = envelope_model if isinstance(envelope_model, str) else model
        return LLMResponse(
            text=text,
            model=served_model,
            prompt_hash=prompt_hash,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )


def claude_cli_available() -> bool:
    """Return True if a `claude` binary is on PATH. Used by /doctor and
    /setup to validate the prerequisite for the claude_code backend."""
    return shutil.which("claude") is not None
