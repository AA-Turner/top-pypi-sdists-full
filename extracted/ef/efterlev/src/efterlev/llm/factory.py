"""Default LLM client factory.

`get_default_client()` is the entry point for agents. It looks for
`.efterlev/config.toml` in cwd; if found, dispatches on the configured
backend (`anthropic` or `bedrock` per SPEC-11). If not found, falls
back to hard-coded anthropic defaults — preserving v0 behavior for
tests and one-off scripts that don't have a workspace.

`get_client_from_config(llm_config)` is the explicit-config variant for
callers that have already loaded their config (typical CLI path).

Fallback-model selection: when the config has a non-empty
`fallback_model`, both backends try it once after primary-model retries
are exhausted before surfacing the error. Set `fallback_model = ""` in
config to disable.
"""

from __future__ import annotations

from pathlib import Path

from efterlev.config import LLMConfig, load_config
from efterlev.errors import AgentError, ConfigError
from efterlev.llm.anthropic_client import AnthropicClient
from efterlev.llm.base import LLMClient
from efterlev.llm.bedrock_client import AnthropicBedrockClient

# CLAUDE.md: default model is claude-opus-4-7; switch to sonnet only for
# latency during demo. Agents can override per-call, but the default lives
# here so changing it is a one-line edit.
DEFAULT_MODEL = "claude-opus-4-7"
DEFAULT_FALLBACK_MODEL = "claude-sonnet-4-6"


def get_client_from_config(
    llm_config: LLMConfig,
    *,
    workspace_root: Path | None = None,
    cache_mode: str | None = None,
) -> LLMClient:
    """Construct an `LLMClient` matching the supplied config.

    Dispatches on `llm_config.backend`. The Pydantic validator on
    `LLMConfig` guarantees the backend/region invariants, so we don't
    re-check them here beyond what's needed for a clear error.

    Cache wrapping (v0.1.147 → v0.1.151): wraps the backend in
    `CachingLLMClient` per the resolution rules in
    `maybe_wrap_with_cache`. `workspace_root` locates the cache dir;
    pass None to skip the wrap entirely (one-off scripts).
    `cache_mode` is typically `Config.cache.mode` from the workspace
    config; env var `EFTERLEV_LLM_CACHE` overrides it.
    """
    from efterlev.llm.cache import maybe_wrap_with_cache

    fallback = llm_config.fallback_model or None
    inner: LLMClient
    if llm_config.backend == "bedrock":
        if not llm_config.region:
            # The validator should have caught this, but defense in depth:
            # never construct a Bedrock client without a region.
            raise AgentError(
                "LLMConfig.region is required for backend='bedrock' "
                "but was unset; check `.efterlev/config.toml`."
            )
        inner = AnthropicBedrockClient(
            region=llm_config.region,
            fallback_model=fallback,
        )
    elif llm_config.backend == "claude_code":
        # v0.1.148 / #353: subprocess `claude --print` for Pro/Max
        # subscription users.
        from efterlev.llm.claude_code_client import ClaudeCodeClient

        inner = ClaudeCodeClient(fallback_model=fallback)
    elif llm_config.backend == "openai":
        # v0.1.211: OpenAI Chat Completions for customers without Claude
        # access; graduated on gpt-5.4-mini at v0.1.213. See LIMITATIONS.md
        # "OpenAI backend".
        from efterlev.llm.openai_client import OpenAIClient

        # The workspace-default fallback_model is a Claude short-form ID
        # (claude-sonnet-4-6), which OpenAI 404s. Only honor an OpenAI-shaped
        # fallback so a stale/default fallback can't turn a recoverable
        # primary error into a confusing cross-provider failure. Backstops
        # init writing fallback="" for this backend (covers hand-edited
        # configs too).
        openai_fallback = fallback if (fallback or "").startswith("gpt") else None
        inner = OpenAIClient(fallback_model=openai_fallback)
    elif llm_config.backend == "bedrock_openai":
        # v0.1.216: OpenAI models served on AWS Bedrock via the Mantle
        # (Responses-API) endpoint. Needs a region; the model id is
        # `openai.gpt-5.4` etc. See llm/mantle_client.py.
        if not llm_config.region:
            raise AgentError(
                "LLMConfig.region is required for backend='bedrock_openai' "
                "but was unset; check `.efterlev/config.toml`."
            )
        from efterlev.llm.mantle_client import BedrockOpenAIClient

        # Only honor an `openai.`-shaped fallback; the workspace-default
        # Claude fallback would 404 on the Mantle endpoint (same guard as the
        # direct-openai backend).
        mantle_fallback = fallback if (fallback or "").startswith("openai.") else None
        inner = BedrockOpenAIClient(region=llm_config.region, fallback_model=mantle_fallback)
    else:
        inner = AnthropicClient(fallback_model=fallback)
    if workspace_root is None:
        return inner
    return maybe_wrap_with_cache(inner, workspace_root=workspace_root, default_mode=cache_mode)


def get_default_client() -> LLMClient:
    """Return the default LLM client.

    Reads `.efterlev/config.toml` from cwd (or the closest ancestor)
    and dispatches on backend. Falls back to anthropic-with-Sonnet-fallback
    defaults when no config file is reachable — preserves v0 behavior
    for ad-hoc scripts and unit tests.

    Honors `EFTERLEV_LLM_CACHE` when a workspace config is found
    (v0.1.147 / #352). When falling back to bare defaults (no workspace),
    cache wrapping is skipped — there's no workspace dir to host the
    cache.
    """
    from efterlev.llm.cache import maybe_wrap_with_cache

    config_path = _find_workspace_config(Path.cwd())
    if config_path is not None:
        try:
            config = load_config(config_path)
            # workspace_root is the directory ABOVE .efterlev/ (config_path is
            # `<root>/.efterlev/config.toml`).
            workspace_root = config_path.parent.parent
            return get_client_from_config(
                config.llm, workspace_root=workspace_root, cache_mode=config.cache.mode
            )
        except ConfigError:
            # Malformed config under a workspace dir is a real bug worth
            # surfacing — but the LLM factory isn't the right place to do
            # that. Fall back to defaults silently here; the CLI will
            # surface the malformed config when it runs `load_config`
            # directly elsewhere.
            pass
    inner: LLMClient = AnthropicClient(fallback_model=DEFAULT_FALLBACK_MODEL)
    # Defaults path: try cwd as the workspace root so cache wrapping
    # still works for `EFTERLEV_LLM_CACHE=on efterlev agent gap --target .`
    # without a workspace config. No workspace config means we don't have
    # a persisted cache_mode; only the env var is honored.
    return maybe_wrap_with_cache(inner, workspace_root=Path.cwd())


def _find_workspace_config(start: Path) -> Path | None:
    """Walk up from `start` looking for a `.efterlev/config.toml`.

    Returns the first one found, or None if we hit the filesystem root.
    The walk lets agents work from anywhere inside a workspace, not just
    its root — matching how `git` and similar dev tools resolve their
    config.
    """
    current = start.resolve()
    while True:
        candidate = current / ".efterlev" / "config.toml"
        if candidate.is_file():
            return candidate
        if current.parent == current:
            return None
        current = current.parent
