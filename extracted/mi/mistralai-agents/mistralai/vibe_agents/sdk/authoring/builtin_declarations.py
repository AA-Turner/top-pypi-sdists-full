"""How a subagent's built-ins merge over its parent's, and the declarations they refuse.

The Harness would refuse a skill or subagent whose built-in is off when the session starts;
refusing it while the agent is built names the authored fields instead. A child that only
inherits skills or subagents is fine: turning the built-in off drops what it inherits.
"""

from collections.abc import Sequence

from mistralai.vibe.harness.app_server.session import BuiltinsConfig, SubagentBuiltinsConfig
from mistralai.vibe_agents.session_workflow import SubagentPolicy

from . import contracts
from . import types as authoring_types
from .errors import SdkError
from .subagent import Subagent


def refuse_subagents_without_their_builtins(
    agent_name: str,
    builtins: authoring_types.Builtins,
    subagents: Sequence[Subagent],
    subagent_policy: SubagentPolicy | None,
) -> None:
    """Refuse the agent's subagents, and each subagent's own skills and subagents, that their built-ins turn off.

    A subagent is checked with its built-ins merged over the ones of the agent that declares it.
    """

    resolved = authoring_types.builtins_to_config(builtins)
    if not resolved.subagents:
        fields = [
            *(["subagents"] if subagents else []),
            *(["subagent_policy"] if subagent_policy is not None else []),
        ]
        if fields:
            raise SdkError(_message(f"Agent {agent_name!r}", fields, "subagents"))
    pending: list[tuple[BuiltinsConfig, Subagent, tuple[str, ...]]] = [
        (resolved, child, (child.name,)) for child in subagents
    ]
    while pending:
        parent, child, path = pending.pop()
        child_builtins = merge_builtins(parent, subagent_builtins_layer(child), path)
        owner = f"Subagent {'/'.join(path)!r}"
        own_switches = set() if child.builtins is None else child.builtins.model_fields_set
        for builtin, declares, enabled in (
            ("skills", bool(child.skills), child_builtins.skills),
            ("subagents", bool(child.subagents), child_builtins.subagents),
        ):
            if declares and not enabled:
                raise SdkError(_message(owner, [builtin], builtin, inherited=builtin not in own_switches))
        pending.extend((child_builtins, nested, (*path, nested.name)) for nested in child.subagents or ())


def refuse_skills_without_their_builtin(
    agent_name: str, builtins: authoring_types.Builtins, harness: contracts.Harness
) -> None:
    """Refuse the agent's skills, of any kind, when its built-ins turn skills off."""

    if builtins.skills:
        return
    if harness.skills or harness.workspace_skills or harness.skill_discovery is not None:
        raise SdkError(_message(f"Agent {agent_name!r}", ["skills"], "skills"))


def subagent_builtins_layer(child: Subagent) -> SubagentBuiltinsConfig | None:
    """Return the built-in switches the child sets; the ones it leaves out inherit."""

    if child.builtins is None:
        return None
    config = authoring_types.builtins_to_config(child.builtins)
    return SubagentBuiltinsConfig.model_validate(
        {name: getattr(config, name) for name in child.builtins.model_fields_set}
    )


def merge_builtins(
    parent: BuiltinsConfig, layer: SubagentBuiltinsConfig | None, path: tuple[str, ...]
) -> BuiltinsConfig:
    """Return the built-ins a child runs with: its own switches over the ones of the agent that declares it."""

    if layer is None:
        return parent
    try:
        return layer.apply(parent)
    except ValueError as error:
        raise SdkError(f"Subagent {'/'.join(path)!r} builtins: {error}") from error


def _message(owner: str, declared: Sequence[str], builtin: str, *, inherited: bool = False) -> str:
    fields = " and ".join(f"{name}=" for name in declared)
    if inherited:
        return (
            f"{owner} sets {fields} but inherits agents.Builtins({builtin}=False), so the model cannot use them. "
            f"Remove {fields}, or pass builtins=agents.Builtins({builtin}=True) to the subagent"
        )
    return (
        f"{owner} sets {fields} but has agents.Builtins({builtin}=False), so the model cannot use them. "
        f"Remove {fields}, or remove {builtin}=False from builtins="
    )
