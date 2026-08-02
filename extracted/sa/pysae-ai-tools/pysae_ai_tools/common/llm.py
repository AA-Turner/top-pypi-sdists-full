"""Provider-agnostic internal LLM layer.

The tooling makes a handful of small LLM calls (ticket scoring, AC-quality review,
routing eval). Each used to build an ``anthropic.Anthropic`` client inline and call
``messages.create``. This module puts one thin abstraction in front of that, so the
provider is a single decision point instead of being scattered across call sites: an
:class:`LLMClient` with one :meth:`~LLMClient.complete` method returning a normalized
:class:`LLMResponse` (text + token usage), and a registry selected by the
``PYSAE_LLM_PROVIDER`` env var (default ``claude-cli``, which reuses the local
``claude`` CLI's own auth so no ``ANTHROPIC_API_KEY`` is needed).

Adding another provider (OpenAI, …) is one :class:`LLMClient` subclass plus one registry
entry — no call site changes. The concrete providers keep their own API-key env-var
resolution so a caller only overrides it when it has a dedicated key (e.g. a CI budget).
"""

import json
import os
import subprocess
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .winpath import spawnable

# Env var selecting the provider; unset falls back to the keyless claude CLI.
PROVIDER_ENV = "PYSAE_LLM_PROVIDER"
DEFAULT_PROVIDER = "claude-cli"


@dataclass
class LLMUsage:
    """Token counts from one completion, normalized across providers."""

    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0


@dataclass
class LLMResponse:
    """A completion result: the concatenated text plus token usage."""

    text: str
    usage: LLMUsage = field(default_factory=LLMUsage)


def _first_env(names: tuple[str, ...]) -> str | None:
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return None


class LLMClient(ABC):
    """One provider's chat-completion client.

    The base resolves the API key from ``api_key_envs`` (unless one is passed
    explicitly); concrete providers declare their ``name`` and key env vars.
    """

    # Env vars the provider resolves its key from, in preference order.
    api_key_envs: tuple[str, ...] = ()

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or _first_env(self.api_key_envs)

    @property
    @abstractmethod
    def name(self) -> str:
        """Short provider id (matches the ``PYSAE_LLM_PROVIDER`` value)."""

    @abstractmethod
    def complete(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int,
        system: str | None = None,
    ) -> LLMResponse:
        """Run a single completion and return its text + token usage."""


class AnthropicClient(LLMClient):
    """Anthropic Messages API — the canonical provider (skills source format is Claude)."""

    name = "anthropic"
    api_key_envs = ("ANTHROPIC_API_KEY",)

    def _messages_client(self) -> Any:
        if not self._api_key:
            raise RuntimeError(f"no API key for the anthropic LLM provider (set {' or '.join(self.api_key_envs)})")
        import anthropic

        return anthropic.Anthropic(api_key=self._api_key)

    def complete(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int,
        system: str | None = None,
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {"model": model, "max_tokens": max_tokens, "messages": messages}
        if system is not None:
            kwargs["system"] = system
        message = self._messages_client().messages.create(**kwargs)
        text = "".join(getattr(block, "text", "") for block in (getattr(message, "content", None) or []))
        return LLMResponse(text=text, usage=_anthropic_usage(getattr(message, "usage", None)))


def _anthropic_usage(usage: Any) -> LLMUsage:
    if not usage:
        return LLMUsage()
    return LLMUsage(
        input_tokens=int(getattr(usage, "input_tokens", 0) or 0),
        output_tokens=int(getattr(usage, "output_tokens", 0) or 0),
        cache_creation_tokens=int(getattr(usage, "cache_creation_input_tokens", 0) or 0),
        cache_read_tokens=int(getattr(usage, "cache_read_input_tokens", 0) or 0),
    )


def _flatten_messages(messages: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for message in messages:
        content = message.get("content", "")
        if isinstance(content, list):
            content = "".join(block.get("text", "") for block in content if isinstance(block, dict))
        parts.append(str(content))
    return "\n\n".join(parts)


class ClaudeCliClient(LLMClient):
    """Route completions through the local ``claude`` CLI (Claude Code headless).

    The CLI resolves its own auth (subscription or a key configured in Claude
    Code), so this provider declares no ``api_key_envs`` and needs no
    ``ANTHROPIC_API_KEY`` — unlike :class:`AnthropicClient`, which calls the
    Messages API directly. Selected with ``PYSAE_LLM_PROVIDER=claude-cli``.

    Each call spawns ``claude -p`` (a full headless agent run, not a bare model
    call): fine for the tooling's small single-turn scoring/eval prompts, at the
    cost of one process start-up per call.
    """

    name = "claude-cli"
    api_key_envs = ()

    def complete(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int,
        system: str | None = None,
    ) -> LLMResponse:
        cmd = [spawnable("claude"), "-p", "--output-format", "json", "--model", model]
        if system is not None:
            cmd += ["--append-system-prompt", system]
        try:
            proc = subprocess.run(
                cmd,
                input=_flatten_messages(messages),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
        except FileNotFoundError as exc:
            raise RuntimeError("the 'claude' CLI is not installed or not on PATH") from exc
        if proc.returncode != 0:
            raise RuntimeError(f"claude CLI failed (exit {proc.returncode}): {(proc.stderr or '').strip()}")
        try:
            payload = json.loads(proc.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"claude CLI returned non-JSON output: {(proc.stdout or '').strip()[:200]}") from exc
        return LLMResponse(text=str(payload.get("result", "")), usage=_claude_cli_usage(payload.get("usage")))


def _claude_cli_usage(usage: Any) -> LLMUsage:
    if not isinstance(usage, dict):
        return LLMUsage()
    return LLMUsage(
        input_tokens=int(usage.get("input_tokens", 0) or 0),
        output_tokens=int(usage.get("output_tokens", 0) or 0),
        cache_creation_tokens=int(usage.get("cache_creation_input_tokens", 0) or 0),
        cache_read_tokens=int(usage.get("cache_read_input_tokens", 0) or 0),
    )


class CodexCliClient(LLMClient):
    """Route completions through ``codex exec`` (Codex CLI, non-interactive).

    Reuses Codex's own auth, so it declares no ``api_key_envs`` and needs no
    ``ANTHROPIC_API_KEY``. Auto-selected when running under Codex (see
    :func:`_detect_provider`), or forced with ``PYSAE_LLM_PROVIDER=codex-cli``.

    The ``model`` argument is Anthropic-specific at the call sites (e.g.
    ``claude-haiku-4-5``), so it is ignored here: Codex uses its configured
    model, overridable with ``PYSAE_CODEX_MODEL``. Token usage is not exposed by
    ``--output-last-message`` and is left best-effort (zeros).
    """

    name = "codex-cli"
    api_key_envs = ()

    def complete(
        self,
        *,
        model: str,
        messages: list[dict[str, Any]],
        max_tokens: int,
        system: str | None = None,
    ) -> LLMResponse:
        prompt = _flatten_messages(messages)
        if system is not None:
            prompt = f"{system}\n\n{prompt}"
        fd, out_path = tempfile.mkstemp(suffix=".txt", prefix="codex-msg-")
        os.close(fd)
        cmd = [
            spawnable("codex"),
            "exec",
            "--skip-git-repo-check",
            "--sandbox",
            "read-only",
            "--output-last-message",
            out_path,
        ]
        codex_model = os.environ.get("PYSAE_CODEX_MODEL")
        if codex_model:
            cmd += ["--model", codex_model]
        try:
            proc = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
            )
            if proc.returncode != 0:
                raise RuntimeError(f"codex CLI failed (exit {proc.returncode}): {(proc.stderr or '').strip()}")
            text = Path(out_path).read_text(encoding="utf-8", errors="replace")
        except FileNotFoundError as exc:
            raise RuntimeError("the 'codex' CLI is not installed or not on PATH") from exc
        finally:
            Path(out_path).unlink(missing_ok=True)
        return LLMResponse(text=text.strip())


def _detect_provider() -> str | None:
    """Provider inferred from the runtime assistant, when ``PYSAE_LLM_PROVIDER`` is unset.

    Codex injects ``AGENT=codex`` into the processes it spawns (plus
    ``CODEX_SANDBOX`` / ``CODEX_SANDBOX_NETWORK_DISABLED`` inside its sandbox), so
    a call originating from Codex routes to ``codex-cli`` — reusing Codex's auth
    instead of an Anthropic key. Returns ``None`` otherwise (keep the default).
    """
    if os.environ.get("AGENT", "").strip().lower() == "codex":
        return "codex-cli"
    if os.environ.get("CODEX_SANDBOX") or os.environ.get("CODEX_SANDBOX_NETWORK_DISABLED"):
        return "codex-cli"
    return None


_PROVIDERS: dict[str, type[LLMClient]] = {
    "anthropic": AnthropicClient,
    "claude-cli": ClaudeCliClient,
    "codex-cli": CodexCliClient,
}


def get_llm_client(*, api_key: str | None = None, provider: str | None = None) -> LLMClient:
    """Return the configured LLM client.

    Precedence: explicit ``provider`` arg, then ``$PYSAE_LLM_PROVIDER``, then the
    assistant auto-detected from the runtime (Codex → ``codex-cli``, see
    :func:`_detect_provider`), then the default ``claude-cli``. ``api_key``
    overrides the provider's own env-var resolution (e.g. a dedicated CI budget
    key). Raises :class:`ValueError` for an unknown provider.
    """
    resolved = (provider or os.environ.get(PROVIDER_ENV) or _detect_provider() or DEFAULT_PROVIDER).strip().lower()
    client_cls = _PROVIDERS.get(resolved)
    if client_cls is None:
        known = ", ".join(sorted(_PROVIDERS))
        raise ValueError(f"unknown LLM provider {resolved!r} (known: {known})")
    return client_cls(api_key=api_key)
