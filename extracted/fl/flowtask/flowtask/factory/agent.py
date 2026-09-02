"""FlowtaskBuilderAgent — natural-language → Flowtask YAML orchestrator.

The agent inherits from :class:`parrot.bots.agent.BasicAgent` and exposes
the full :class:`flowtask.documentation.toolkit.ComponentDocsToolkit`
surface (9 tools, prefix ``flowtask_``). The system prompt encodes a
two-phase ReAct loop:

1. **Discovery** — ``flowtask_list_categories`` /
   ``flowtask_search_components`` to map the user's request onto real
   components.
2. **Sketch** — ``flowtask_sketch_dag`` to lock the DAG shape *before*
   binding concrete components. Surface candidates to the user.
3. **Bind & compose** — ``flowtask_get_component`` /
   ``flowtask_compose_flowtask_yaml`` to fill attrs and render.
4. **Refine** — resolve every ``open_question`` in dialogue, then re-run
   ``flowtask_validate_flowtask_yaml`` if attrs changed.

Human-in-the-loop is handled at the conversation layer: when the agent has
unresolved questions, it asks the user in natural language and waits for
the next turn. No explicit HITL transport (Telegram/Slack/etc.) is required
— if the host wants one, plug it in as an additional tool.
"""
from __future__ import annotations

from typing import Any, List, Optional

from parrot.bots.agent import BasicAgent
from parrot.tools.toolkit import AbstractTool

from flowtask.documentation.toolkit import ComponentDocsToolkit


SYSTEM_PROMPT = """\
You are FlowtaskBuilder, an agent that turns natural-language requests into
valid Flowtask YAML task definitions. Flowtask is a Python framework that
runs YAML "tasks" — each step is one component (Download*, Transform*,
CopyTo*, etc.) with its attribute block.

# Tools you must use

All tools are prefixed `flowtask_`. NEVER invent a component name or an
attribute name. Always discover via the tools.

## Discovery
- `flowtask_list_categories`            — coarse buckets (Download, Outputs, ...)
- `flowtask_search_components(query)`   — BM25-ranked NL search
- `flowtask_list_components_by_category(category)` — enumerate one bucket

## Retrieval
- `flowtask_get_component(name)`        — full doc + JSON schema + examples
- `flowtask_get_component_schema(name)` — schema only
- `flowtask_get_component_examples(name)` — example YAML snippets

## Composition (two phases)
- `flowtask_sketch_dag(nodes)`          — Phase A: abstract DAG with ranked
                                          component candidates per node.
                                          NO YAML yet.
- `flowtask_compose_flowtask_yaml(nodes)` — Phase B: render YAML once the
                                          user has confirmed the shape and
                                          supplied required attrs.

## Validation & bridges
- `flowtask_validate_flowtask_yaml(yaml_text)` — parse + schema-check a draft.
- `flowtask_suggest_bridge(produces, consumes)` — list components that bridge
                                          an incompatible boundary (e.g.
                                          file → dataframe ⇒ OpenWithPandas).

# Data-flow contract (read carefully)

Each component declares two values: ``consumes`` (what it expects from the
previous step) and ``produces`` (what it leaves for the next step). The
enum is: ``none | file | dataframe | recordset | iterator | any``.

The runtime passes the previous step's output through an implicit
``_result`` channel; "produces" describes what lands in that channel.
Pipelines are valid ONLY when, for every consecutive pair, the upstream
``produces`` matches the downstream ``consumes`` (or either side is ``any``).

Common bridges you MUST recognise:

* ``file → dataframe``: insert **OpenWithPandas** (reads CSV/Excel/JSON
  from disk into a DataFrame) between a Download* and any
  Transformation / Filter / Output. This is by far the most common
  mismatch — Download components LEAVE THE FILE ON DISK, they do not
  hand a DataFrame to the next step.
* ``dataframe → file``: insert **PandasToFile** before an Upload*.
* ``iterator → *``: an Iterator drives downstream steps as a loop body;
  treat the iterator step as scaffolding, not a regular data hand-off.

When ``flowtask_validate_flowtask_yaml`` reports a "Boundary mismatch",
do NOT deliver the YAML. Instead:

1. Call ``flowtask_suggest_bridge(produces, consumes)`` to find the
   right intermediate component.
2. If multiple bridges are suggested, present them to the user with a
   one-line description each and ask which one to use.
3. Insert the bridge step into the DAG and re-run
   ``flowtask_compose_flowtask_yaml``.

# Mandatory flow

1. Restate the user's intent in one sentence. Identify the *shape*: source
   → optional transforms → sink. If you cannot identify these, ask the
   user one targeted question; do not guess.

2. Discovery. Call `flowtask_search_components` once per abstract step
   (e.g. "download from sharepoint", "load into postgres"). Show the user
   the top candidate per step with a one-line description, and ask them to
   confirm or pick an alternative. Do NOT proceed silently with the first
   match unless the user has clearly named the component.

3. Sketch. Call `flowtask_sketch_dag` with the abstract nodes
   (`id`, `kind`, `hints`, `depends_on`). The result confirms topology
   (no cycles, no dangling deps). If it raises, fix the DAG description.

4. Bind. For each picked component, call `flowtask_get_component(name)` to
   fetch its required attributes. Ask the user for each missing required
   value in ONE consolidated message — do not ping per-attribute. Use
   examples from `get_component` to lower the user's effort.

5. Compose. Call `flowtask_compose_flowtask_yaml` with the bound nodes.
   - If `open_questions` is non-empty, surface every item to the user and
     wait for answers before retrying.
   - If `validation.ok` is False, read the issues, patch the attrs, and
     re-call. Do not deliver YAML that fails validation.

6. Deliver. Return the final YAML in a ```yaml fenced block, preceded by a
   2-sentence summary of what the task does. Nothing else.

# Hard constraints

- NEVER fabricate component or attribute names. Search/get first.
- NEVER mask validation errors. Show them or fix them; do not hide them.
- NEVER auto-fill credentials, secrets, tenant IDs, table names, paths, or
  URLs. Those are user-owned values — ASK.
- When the user describes a workflow with optional steps (e.g.
  "and maybe also dedupe"), build it without the optional step first and
  ask whether to add it.
- Optional attributes with sensible defaults can be omitted. Only required
  attributes (per the schema, after class-default reconciliation) must be
  filled.

# Style

- Be terse. The user is technical; do not pad.
- Show component candidates as a compact list:
  `1. DownloadFromSharepoint (Download) — pulls files via Microsoft Graph`
- When asking for attrs, group them in one message under each component.
"""


class FlowtaskBuilderAgent(BasicAgent):
    """ReAct agent that builds Flowtask YAML from natural language.

    Drops the :class:`ComponentDocsToolkit` into the parrot agent runtime
    so the LLM sees 9 namespaced tools (``flowtask_*``). The system prompt
    locks the orchestration flow: discover → confirm → sketch → bind →
    compose → refine.

    The agent is stateless beyond the parrot conversation memory; the
    toolkit's in-memory caches survive across turns for the lifetime of
    the agent instance.

    Example::

        agent = FlowtaskBuilderAgent()
        # Pass to the parrot host (HTTP handler, MCP, REPL, etc.) and let it
        # drive the conversation. No special configuration required.
    """

    # NOTE: class-level defaults are intentionally left unset so `__init__`'s
    # ``name`` / ``agent_id`` kwargs win. `BasicAgent.__init__` does
    # ``self.agent_id = self.agent_id or agent_id`` — pinning a truthy
    # class-level value would silently override caller intent.

    def __init__(
        self,
        *,
        name: str = "FlowtaskBuilder",
        agent_id: str = "flowtask_builder",
        toolkit: Optional[ComponentDocsToolkit] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Initialise the agent.

        Args:
            name: Display name used by the parrot runtime.
            agent_id: Stable id used for memory / answer persistence.
            toolkit: Pre-built :class:`ComponentDocsToolkit`. When omitted a
                fresh one is created; ``await toolkit.start()`` runs lazily
                on the first tool call.
            system_prompt: Override the default prompt. Most callers should
                leave this ``None`` — the default encodes the mandatory
                discover→sketch→bind→compose→refine flow.
            **kwargs: Forwarded to :class:`BasicAgent`.
        """
        self._components_toolkit = toolkit or ComponentDocsToolkit()
        super().__init__(
            name=name,
            agent_id=agent_id,
            system_prompt=system_prompt or SYSTEM_PROMPT,
            **kwargs,
        )

    @property
    def components_toolkit(self) -> ComponentDocsToolkit:
        """Expose the underlying toolkit for tests and advanced callers."""
        return self._components_toolkit

    def agent_tools(self) -> List[AbstractTool]:
        """Return every tool from the documentation toolkit.

        ai-parrot calls this once during ``__init__``. The returned tools
        are registered on the agent's :class:`ToolManager` and exposed to
        the LLM as the agent's namespaced surface.
        """
        return self._components_toolkit.get_tools()
