"""Actions — ONE declaration of named work, many doors (step, tool, directive, mcp),
one router (``run_action``) that sends every call to the Action's ENGINE.

New work is declared with ``declare_action`` (a plain ``async (app, input) -> output``
function plus its doors); ``register_node`` stays the step-only form whose body takes
the node context.

Registered nodes — typed, registered units of work that become graph nodes.

Author via::

    @register_node(
        name="news_api.top_headlines",
        input_schema=NewsInputs,
        output_schema=NewsOutputs,
        determinism=ActionTier.NON_DETERMINISTIC,
    )
    async def top_headlines(ctx, inputs: NewsInputs) -> NewsOutputs: ...

Every decorated function is registered in both the node registry (the bare
dotted name IS the spec_type — the legacy ``action.<name>`` spelling resolves
through the registry alias) and the action registry (so the Studio palette
can list it and ``tool.call`` can resolve it by name). ``@action`` is the
deprecated legacy decorator name — see docs/workflow/NOMENCLATURE.md.
"""

from matrx_graph.actions.decorator import (
    ActionSignatureError,
    action,
    declare_action,
    declare_engine_action,
    step_idempotency_key,
    iter_registered_action_specs,
    register_node,
    resolve_action_executor,
)
from matrx_graph.actions.doors import DOORS, ActionDoor, api_path_for, directive_noun_for, tool_name_for
from matrx_graph.actions.engines import (
    AUTHORITIES,
    DOOR_AUTHORITY,
    ENGINES,
    Authority,
    caller_authority,
    POLICY_DOORS,
    WRITING_ENGINES,
    ActionEngine,
    configure_action_ledger,
    configure_apply_gate,
    ActionStarted,
    REPLAY_MESSAGE,
    last_run_replayed,
    dump_result,
    register_engine,
    registered_engines,
    run_action,
)
from matrx_graph.actions.registry import ActionRegistry, ActionSource, default_action_registry
from matrx_graph.actions.spec import ActionFailed, ActionSpec, build_action_node_spec

__all__ = [
    "ENGINES",
    "POLICY_DOORS",
    "configure_action_ledger",
    "configure_apply_gate",
    "WRITING_ENGINES",
    "AUTHORITIES",
    "DOOR_AUTHORITY",
    "Authority",
    "ActionSource",
    "api_path_for",
    "caller_authority",
    "ActionEngine",
    "ActionStarted",
    "REPLAY_MESSAGE",
    "last_run_replayed",
    "declare_engine_action",
    "dump_result",
    "register_engine",
    "registered_engines",
    "run_action",
    "DOORS",
    "ActionDoor",
    "ActionFailed",
    "ActionRegistry",
    "ActionSignatureError",
    "ActionSpec",
    "action",
    "build_action_node_spec",
    "declare_action",
    "directive_noun_for",
    "step_idempotency_key",
    "tool_name_for",
    "default_action_registry",
    "iter_registered_action_specs",
    "register_node",
    "resolve_action_executor",
]
