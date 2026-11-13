"""What verl's capture declares it cannot hold (`run.samples.plan(unsupported=...)`, D8), from the trainer's config and
tokenizer: ids Probe numbered (hermes gives none, D3), reasoning without a think-end token (D4), both only when verl
runs its tool loop, and, in every layout, files a reward function attaches where no rollout handle reaches it (the
trainer process, or the remote reward manager's actor; D11)."""

from __future__ import annotations

from typing import Any

from .reasoning import has_think_token

#: Tool parsers that give no call id at the pinned commit (`tool_parser.py:108-129`); Kimi's does (`:643`).
PARSERS_WITHOUT_IDS = frozenset({"hermes"})
#: The reward manager that calls the reward function in its own Ray actor (`reward_manager/remote.py:25-37`).
REMOTE_REWARD_MANAGER = "remote"


def build_unsupported(config: Any, tokenizer: Any) -> dict[str, str]:
    """`CaptureField` -> why, for this run's layout; empty when verl's capture holds every field."""
    unsupported: dict[str, str] = {}
    files_reason = _get_reward_files_gap(config)
    if files_reason:
        unsupported["environment_files"] = files_reason
    multi_turn = _get(config, "actor_rollout_ref", "rollout", "multi_turn")
    # verl's tool agent loop: the multi-turn switch, tools (`agent_loop.py:627`), or the default loop named
    is_tool_loop = any(_get(multi_turn, name) for name in ("enable", "tool_config_path", "function_tool_path"))
    if not is_tool_loop and _get(config, "actor_rollout_ref", "rollout", "agent", "default_agent_loop") != "tool_agent":
        return unsupported
    parser = _get(multi_turn, "format")
    if isinstance(parser, str) and parser in PARSERS_WITHOUT_IDS:
        unsupported["tool_call_ids"] = (f"numbered by Probe (probe-<turn>-<i>): verl's {parser} tool parser gives no "
                                        "call id; results follow call order, so each link is exact")
    if tokenizer is not None and not has_think_token(tokenizer):
        unsupported["reasoning"] = ("verl is token-in/token-out and this model's tokenizer has no think-end token, "
                                    "so reasoning cannot be told apart from content")
    return unsupported


def _get_reward_files_gap(config: Any) -> str | None:
    """Why files the reward function attaches cannot be linked in this layout, else None (D11)."""
    reward_model = _get(config, "reward", "reward_model")
    if _get(reward_model, "enable") and not _get(reward_model, "enable_resource_pool"):
        return ("files the reward function attaches are not linked: with a reward model on the trainer's GPUs verl "
                "scores in the trainer process, where no rollout handle reaches it; files the rollout's tools attach are")
    # `reward.reward_manager.name` is what runs: `main_ppo` never reads the legacy `reward_model.reward_manager`, and
    # fully-async migrates it there first (`fully_async_main.py:237`); `importlib` names a user class
    manager = _get(config, "reward", "reward_manager", "name")
    is_registered = _get(config, "reward", "reward_manager", "source") in (None, "register")
    if manager == REMOTE_REWARD_MANAGER and is_registered:
        return ("files the reward function attaches are not linked: verl's remote reward manager runs it in a "
                "RewardComputeWorker actor, which gets neither the rollout's context nor its handle; files the "
                "rollout's tools attach are")
    return None


def _get(config: Any, *names: str) -> Any:
    for name in names:
        if config is None:
            return None
        try:
            config = config.get(name) if hasattr(config, "get") else getattr(config, name, None)
        except Exception:  # noqa: BLE001 -- a config that cannot say
            return None
    return config
