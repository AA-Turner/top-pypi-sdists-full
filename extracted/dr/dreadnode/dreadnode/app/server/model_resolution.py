import os
import typing as t
from dataclasses import dataclass

if t.TYPE_CHECKING:
    from dreadnode.capabilities.types import AgentDef
    from dreadnode.generators.generator import Generator


_DREADNODE_LLM_BASE_ENV = "DREADNODE_LLM_BASE"
_DREADNODE_LLM_API_KEY_ENV = "DREADNODE_LLM_API_KEY"


@dataclass(frozen=True, slots=True)
class TurnModelConfig:
    """Canonical and execution-time model config for a single chat turn."""

    canonical_model: str
    generator_model: str
    api_base: str | None = None
    api_key: str | None = None

    @property
    def is_platform_proxy(self) -> bool:
        return self.canonical_model.startswith("dn/")


def resolve_canonical_turn_model(
    requested_model: str | None,
    remembered_model: str | None,
    agent_def: "AgentDef | None",
) -> str:
    """Resolve the canonical model id for a turn."""
    if requested_model:
        return requested_model
    if remembered_model:
        return remembered_model
    if agent_def and agent_def.model and agent_def.model != "inherit":
        return agent_def.model
    agent_name = agent_def.name if agent_def else "default"
    raise ValueError(
        f"Agent '{agent_name}' does not define a model. Pass one explicitly before running a turn."
    )


def resolve_turn_model_config(
    requested_model: str | None,
    remembered_model: str | None,
    agent_def: "AgentDef | None",
) -> TurnModelConfig:
    """Resolve canonical and execution-time model config for a turn."""
    canonical_model = resolve_canonical_turn_model(requested_model, remembered_model, agent_def)
    if canonical_model.startswith("dn/"):
        api_base = os.environ.get(_DREADNODE_LLM_BASE_ENV, "").strip() or None
        api_key = os.environ.get(_DREADNODE_LLM_API_KEY_ENV, "").strip() or None
        if not api_base:
            api_base = os.environ.get("LITELLM_PUBLIC_URL", "").strip() or None
        if not api_key:
            api_key = os.environ.get("LITELLM_MASTER_KEY", "").strip() or None
        return TurnModelConfig(
            canonical_model=canonical_model,
            generator_model=canonical_model,
            api_base=api_base,
            api_key=api_key,
        )
    return TurnModelConfig(
        canonical_model=canonical_model,
        generator_model=canonical_model,
    )


def validate_model_environment(config: TurnModelConfig) -> str | None:
    """Return a clean error message if required env vars are missing, else None."""
    if config.is_platform_proxy:
        missing: list[str] = []
        if not config.api_base:
            missing.append(_DREADNODE_LLM_BASE_ENV)
        if not config.api_key:
            missing.append(_DREADNODE_LLM_API_KEY_ENV)
        if missing:
            keys = ", ".join(missing)
            return f"Missing proxy configuration — set {keys} to use {config.canonical_model}"
        return None

    model = config.generator_model
    if isinstance(model, str):
        try:
            from litellm import validate_environment

            from dreadnode.generators.generator import LiteLLMGenerator, get_generator

            parsed_generator = get_generator(model)
            if not isinstance(parsed_generator, LiteLLMGenerator):
                return None
            if parsed_generator.api_key or parsed_generator.params.api_base:
                return None

            model = parsed_generator.model
            result = validate_environment(model)
            if not result.get("keys_in_environment"):
                missing = result.get("missing_keys", [])
                keys = ", ".join(missing) if missing else "the required API key"
                return f"Missing API key — set {keys} to use {model}"
        except Exception:
            return None
    return None


def build_turn_generator(config: TurnModelConfig) -> "str | Generator":
    """Build the effective generator input for a turn or compaction request."""
    if not config.is_platform_proxy:
        return config.generator_model

    from dreadnode.generators.proxy import build_proxy_generator, resolve_dn_model_to_generator

    # A configured local runtime registers a lazy platform-proxy provisioner.
    # ``resolve_turn_model_config`` may run before that provisioner has minted
    # credentials, notably when a guard policy constructs its judge during a
    # mid-session policy swap. Give the shared resolver a chance to provision
    # before treating the missing snapshot as the final configuration.
    if not config.api_base or not config.api_key:
        return resolve_dn_model_to_generator(config.generator_model)

    return build_proxy_generator(
        config.generator_model,
        api_base=config.api_base,
        api_key=config.api_key,
    )
