"""Every piece of text the PLATFORM adds to what a model receives — registered, labeled, visible.

Owner rules (Arman, 2026-10-17): never add text to a person's message; nothing shapes a
prompt outside ``send_boundary.prepare_for_send``; the Builder shows everything the model
receives. A platform part that is not registered here has no purpose anyone can see, so it
does not ship (defects 25 + 27, 2026-10-18).

Two registries and one reader:

* ``PLATFORM_PARTS`` — the parts a FIRST send can carry (system additions, the per-turn
  ``<turn_context>`` block, the tail channel). ``platform_parts_in_request`` finds each in a
  captured wire request (the Builder Model view / dry run) and labels it with its id and source.
* ``MID_LOOP_PARTS`` — host-authored turns the executor adds only AFTER a provider response
  (empty reply, loop guard, change claim, required member, retry, queued injection). A dry
  run stops at the first send, so they are listed in the dry run as "may be added mid-loop"
  with their purpose and source. Every ``host_authored_user_turn(..., reason=...)`` in
  matrx_ai names a reason registered here. Guard:
  ``tests/test_every_platform_part_is_registered.py``.

The host (aidream) shows these in the Model view (``aidream/api/utils/preview.py``).
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class PlatformPart:
    id: str
    label: str
    channel: str  # system | turn_context | tail | host_turn | person_turn
    source: str  # where the text is written
    purpose: str


# --------------------------------------------------------------------------- #
# THE BLOCK REGISTRY — one home for every block type (prompt blocks / static    #
# seal P1a, PLAN §5.4). PLATFORM_PARTS, MID_LOOP_PARTS and HOST_TURN_PARTS are  #
# VIEWS of it (below); aidream's INJECTOR_RULES, BLOCK_CENSUS / CLIENT_WIRE_SLOTS #
# and TURN_CONTEXT_SLOT_NOTES name its ids (guard: tests/prompt_blocks/).       #
# --------------------------------------------------------------------------- #

#: Where a block can sit, in cache order (PLAN §3.2). ``Z1_wire`` is the system text added on the
#: wire copy only (never stored); ``P_params`` holds request settings, not text.
ZONES: tuple[str, ...] = (
    "Z0_tools",
    "Z1_system",
    "Z1_wire",
    "Z2_template",
    "Z3_history",
    "Z4_turn_context",
    "Z5_newest_turn",
    "Z6_tail",
    "Z7_mid_loop",
    "P_params",
)
#: Zones that sit ABOVE the default seal line (after the last template message, PLAN §12 D1).
ZONES_ABOVE_SEAL: frozenset[str] = frozenset({"Z0_tools", "Z1_system", "Z1_wire", "Z2_template"})

#: When a block's text is computed and how long it stays (PLAN §5.3).
LIFETIMES: tuple[str, ...] = (
    "assembly",
    "assembly_plus_changes",
    "sticky",
    "every_turn",
    "every_send",
    "on_event",
)
#: The lifetimes whose text may sit above the seal (the snapshot half of ``assembly_plus_changes``).
SEALABLE_LIFETIMES: frozenset[str] = frozenset({"assembly", "assembly_plus_changes"})

DELIVERIES: tuple[str, ...] = ("inline", "on_request", "off")

#: The two door families (aidream ``turn_assembly``): run_ai_task vs ``Agent.execute``.
INTERACTIVE = "interactive"
PROGRAMMATIC = "programmatic"
ALL_DOORS: frozenset[str] = frozenset({INTERACTIVE, PROGRAMMATIC})


@dataclass(frozen=True)
class BlockType:
    """One block type: what it is, who produces its text, where it sits by default and for how long.

    ``producer`` is ``module:qualname`` (or a module for a call-site family). ``zone`` is the DEFAULT
    placement — today's server order. ``known_seal_break`` names the PLAN §3.4 breakers (B-ids; ``W5`` for the Anthropic grammar-ladder
    append, which §3.4 has no B-id for) that change this block's bytes above the seal today — a
    non-sealable lifetime placed there by default, or a sealable one moved by storage / re-fill (B8,
    B11, B14) when the
    default placement puts a non-sealable lifetime above the seal (the default formula's one allowed
    exception, reported by the seal check until P4). ``views`` lists the legacy registries the entry
    is shown through.
    """

    id: str
    label: str
    channel: str
    source: str
    purpose: str
    zone: str
    lifetime: str
    producer: str
    delivery: tuple[str, ...] = ("inline",)
    fetch_tool: str | None = None
    doors: frozenset[str] = ALL_DOORS
    slot: str | None = None
    known_seal_break: tuple[str, ...] = ()
    dormant: bool = False
    views: tuple[str, ...] = ()
    #: The sentence the context viewer shows people for this block (aidream ``BLOCK_CENSUS`` /
    #: ``CLIENT_WIRE_SLOTS`` are views of it). Never sent to a model. ``None``: not in the viewer census.
    viewer_text: str | None = None

    @property
    def census_id(self) -> str:
        """The id the context viewer knows this block by: its per-turn slot, else its block id."""
        return self.slot or self.id

    @property
    def may_sit_above_seal(self) -> bool:
        return self.lifetime in SEALABLE_LIFETIMES

    def as_part(self) -> PlatformPart:
        return PlatformPart(self.id, self.label, self.channel, self.source, self.purpose)


#: Per-turn slots whose text has a recognisable frame on the wire (see ``_patterns``): listed in
#: the ``platform_parts`` view so the Model view labels them and the residual check subtracts them.
_SLOT_FRAME_VIEWS: dict[str, tuple[str, ...]] = {"helpers": ("platform_parts",)}

BLOCK_TYPES: tuple[BlockType, ...] = (
    # ── first send (view: PLATFORM_PARTS) ──
    BlockType(
        "attached_file",
        "Attached file",
        channel="person_turn",
        source="matrx_ai/config/attached_files.py place_attached_files (host: conversation_context/file_blocks.py); an API / MCP document part converted to text: matrx_ai/processing/media_fallback/handler.py _open_with_source_label",
        purpose="an attached file's whole text in its own block at the start of the turn it was attached to, opened by its <attachment/> identity label (the value list names where it is)",
        zone="Z5_newest_turn",
        lifetime="sticky",
        producer="matrx_ai.config.attached_files:place_attached_files",
        views=("platform_parts",),
    ),
    BlockType(
        "held_copy",
        "Held copy",
        channel="person_turn",
        source="matrx_ai/config/attached_files.py place_attached_files (kind held_copy; staged by the host)",
        purpose="a host value's text delivered whole once at the start of its home turn, after its files, opened by its <held_copy/> label and replayed byte-identical on every later send",
        zone="Z5_newest_turn",
        lifetime="sticky",
        producer="matrx_ai.config.attached_files:place_attached_files",
        views=("platform_parts",),
    ),
    BlockType(
        "current_date",
        "Today's date",
        channel="system",
        source="matrx_ai/instructions/core.py render_date_block",
        purpose="the model knows today's date (off with include_date)",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:render_date_block",
        views=("platform_parts",),
    ),
    BlockType(
        "organization_catalog",
        "Organizations",
        channel="system",
        source="matrx_ai/instructions/core.py inject_context_block (host: context catalog)",
        purpose="the organizations, scope types and scopes the person belongs to",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:SystemInstruction.inject_context_block",
        views=("platform_parts",),
    ),
    BlockType(
        "skills",
        "Skills",
        channel="system",
        source="matrx_ai/skills/preamble.py render_preamble",
        purpose="the skills the agent may load",
        zone="Z1_system",
        lifetime="assembly_plus_changes",
        producer="matrx_ai.skills.preamble:render_preamble",
        delivery=("inline", "on_request"),
        fetch_tool="skill",
        slot="skills",
        views=("platform_parts",),
    ),
    BlockType(
        "kind_directives",
        "Kind Directives guidance",
        channel="system",
        source="matrx_ai/instructions/core.py _actions_guidance (set by the host from the agent's actions)",
        purpose="when and how to emit the Kind Directives the agent declares",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:render_kind_directives",
        views=("platform_parts",),
    ),
    BlockType(
        "answer_contract",
        "Final answer format",
        channel="system",
        source="matrx_ai/schema/answer_contract.py json_text_contract (a kind's registered writer: aidream/services/visual_maps/authoring.py ANSWER_CONTRACT_HEAD_TEXT + the kind_visual_map skill guidance)",
        purpose="the provider cannot hold the declared output schema: the answer's shape goes in the system message and the answer is still checked against the schema",
        zone="Z1_wire",
        lifetime="every_send",
        producer="matrx_ai.schema.answer_contract:json_text_contract",
        known_seal_break=("B4", "W5"),
        views=("platform_parts",),
    ),
    BlockType(
        "grounded_json_contract",
        "Grounded JSON contract (Gemini)",
        channel="system",
        source="matrx_ai/providers/google/translator.py _grounded_json_text_contract",
        purpose="a Google Search-grounded Gemini call with a declared output schema: how to write the research digest and the one fenced JSON answer, in the system message of the wire copy",
        zone="Z1_wire",
        lifetime="every_send",
        producer="matrx_ai.providers.google.translator:GoogleTranslator._grounded_json_text_contract",
        known_seal_break=("B4", "W5"),
        views=("platform_parts",),
    ),
    BlockType(
        "attachment_label",
        "Attachment label",
        channel="person_turn",
        source="matrx_ai/config/message_config.py _media_identity_label (and assistant_turn_media._identity_line, the Anthropic not-resent note)",
        purpose="the identity (kind, name, id) of each picture, audio or video the person attached, as its own text part right before the media part",
        zone="Z5_newest_turn",
        lifetime="sticky",
        producer="matrx_ai.config.message_config:_media_identity_label",
        views=("platform_parts",),
    ),
    BlockType(
        "agent_identity",
        "Who made this agent",
        channel="turn_context",
        source="matrx_ai/config/agent_identity.py render_identity (knobs agents.identity; lab = catalog maker)",
        purpose="the agent says it is a collaboration between AI Matrx and the lab of the model answering (Arman 2026-10-26); also appended to realtime voice session instructions",
        zone="Z4_turn_context",
        lifetime="every_send",
        producer="matrx_ai.config.agent_identity:render_identity",
        slot="agent_identity",
        views=("platform_parts",),
    ),
    BlockType(
        "person_context",
        "The person's memory and instructions",
        channel="turn_context",
        source="matrx_ai/config/person_context.py render_person_context (host: aidream services/person_memory; knob agent_memory.person_context_max_chars)",
        purpose="the person's custom instructions (about me, how to respond) and saved memories, on a chat agent's turn; never in a temporary chat without the turn's opt-in, never in a confidential one (CGU-10)",
        zone="Z4_turn_context",
        lifetime="every_send",
        producer="matrx_ai.config.person_context:render_person_context",
        slot="person_context",
        views=("platform_parts",),
    ),
    BlockType(
        "run_environment",
        "Where this agent is running",
        channel="turn_context",
        source="matrx_ai/config/run_environment.py compose_environment_block (signals: client.surface, browser-dom payload, active_sandbox.target_kind, runtime role; tools: the run's live set + registry bindings)",
        purpose="the ENVIRONMENT block: chrome extension, cloud, sandbox or local machine, what each tool family reaches there, the preferred browsing path, and the rule that it outranks a memory written for another environment (2026-11-17)",
        zone="Z4_turn_context",
        lifetime="every_send",
        producer="matrx_ai.config.run_environment:compose_environment_block",
        slot="run_environment",
        views=("platform_parts",),
    ),
    BlockType(
        "turn_context",
        "Per-turn context",
        channel="turn_context",
        source="matrx_ai/config/message_config.py render_turn_context (slots staged by the host)",
        purpose="this turn's live date, selection, value list, platform notes; its own host turn after the newest message on every provider (the end of the system message only for a model the catalog declares strict_role_alternation)",
        zone="Z4_turn_context",
        lifetime="every_turn",
        producer="matrx_ai.config.message_config:MessageList.render_turn_context",
        views=("platform_parts",),
    ),
    BlockType(
        "inherited_history",
        "Inherited conversation",
        channel="turn_context",
        source="matrx_ai/tools/implementations/agent_call.py _inherited_history_note (inside the per-turn context)",
        purpose="a child agent that starts from another conversation (a fork, or include_history) is told how to read it: whose it is, and that its requests were already handled. Part of that contract: always on, no switch, decided by the platform",
        zone="Z4_turn_context",
        lifetime="every_turn",
        producer="matrx_ai.tools.implementations.agent_call:_inherited_history_note",
        slot="inherited_history",
        views=("platform_parts",),
    ),
    BlockType(
        "live_plan",
        "Task list",
        channel="tail",
        source="matrx_ai/config/live_plan.py render_live_plan (with its update reminder after N tool calls)",
        purpose="the agent's own open task list, after a tool result, so it keeps the plan current",
        zone="Z6_tail",
        lifetime="every_send",
        producer="matrx_ai.config.live_plan:render_live_plan",
        slot="live_plan",
        views=("platform_parts",),
    ),
    # ── mid-loop host turns (view: MID_LOOP_PARTS) ──
    BlockType(
        "empty_reply_continuation",
        "Empty reply: ask for the answer",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py _drop_blank_turn_for_continuation",
        purpose="a turn ended with no visible reply: once per run, ask for the answer instead of failing",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "text_tool_call",
        "Tool call written as text",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py (orchestrator/text_tool_calls.py)",
        purpose="a reply typed a tool call as text: once per run, the markup is removed and the model re-asked",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "iteration_ceiling_approaching",
        "Step limit approaching",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py _ceiling_approaching_notice",
        purpose="a run nears its step limit: tells the model how many steps are left so it can finish",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "iteration_ceiling_wrap_up",
        "Step limit reached: write it up",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py _ceiling_wrap_up_notice",
        purpose="a run hit its step limit: one tool-less turn writes what was done and what is left",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "budget_wrap_up",
        "Run budget reached: write it up",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py budget_wrap_up_notice (host: aidream billing.automation_guardrails)",
        purpose="only one more call fits a run's per-run budget: one tool-less turn says what is built, what is left, and offers to continue",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "budget_finish_unit",
        "Run budget nearly reached: finish the unit in hand",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py budget_finish_unit_notice (host: aidream billing.automation_guardrails)",
        purpose="a few calls before the budget wrap-up, once: finish the table or page in hand, start nothing new, so the stop lands at a natural boundary",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "visual_map_repair",
        "Visual map: repair the diagram",
        channel="host_turn",
        source="matrx_ai/orchestrator/visual_map_repair.py repair_notice (+ visual_map_fixes.py REPAIR_TURN_PATCH_TEXT)",
        purpose="a visual map failed validation: one tool-less repair turn names what to fix",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.visual_map_repair",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "strict_json_schema_repair",
        "Structured output: fix the JSON",
        channel="host_turn",
        source="matrx_ai/graph_nodes/_strict_json.py llm_messages_to_pydantic_measured",
        purpose="a strict-JSON answer failed schema validation: one repair turn names the error",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.graph_nodes._strict_json",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "required_member_gate",
        "Required member not consulted",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py (Orchestra required members)",
        purpose="an Orchestra declares members that must be consulted before the final answer",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "answer_check",
        "Answer format: correct the named problems",
        channel="host_turn",
        source="matrx_ai/orchestrator/answer_checks.py correction_notice (executor finishing gate)",
        purpose="an answer breaks a rule of its declared format: once within the correction budget, name the offending text and ask for a corrected answer before persistence",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.answer_checks",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "change_claim_gate",
        "Claimed changes without a write",
        channel="host_turn",
        source="matrx_ai/orchestrator/change_claims.py",
        purpose="the reply says changes were made but no write tool succeeded",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.change_claims",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "loop_guard_approaching",
        "Tool failures: caution",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py loop guard (knobs orchestration.loop_guard)",
        purpose="most recent tool calls failed: change approach before tools are disabled",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "loop_guard_standoff_continue",
        "Tool failures: one more try",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py loop guard standoff verdict",
        purpose="a failing tool is given one reasoned second chance",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "loop_guard_tool_disabled",
        "Tool disabled after failures",
        channel="host_turn",
        source="matrx_ai/orchestrator/loop_guard.py disabled_tool_notice",
        purpose="a tool that kept failing is withdrawn for this run",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.loop_guard",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "loop_guard_tools_disabled",
        "Tools disabled: answer honestly",
        channel="host_turn",
        source="matrx_ai/orchestrator/executor.py loop guard",
        purpose="too many failures: stop calling tools and tell the person what happened",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.executor",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "retry_after_failed_call",
        "Retry after a failed call",
        channel="host_turn",
        source="matrx_ai/orchestrator/recovery_logic.py",
        purpose="a retryable provider finish: name the tools still available",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.orchestrator.recovery_logic",
        views=("mid_loop_parts",),
    ),
    BlockType(
        "injection",
        "Queued message",
        channel="host_turn",
        source="matrx_ai/tools/dynamic_drain.py (reason injection:<kind>)",
        purpose="a message queued for this live conversation (steer, collaborator write-back)",
        zone="Z7_mid_loop",
        lifetime="on_event",
        producer="matrx_ai.tools.dynamic_drain",
        views=("mid_loop_parts",),
    ),
    # ── host turns that start a turn (view: HOST_TURN_PARTS) ──
    BlockType(
        "podcast_extraction",
        "Podcast: read the person's files",
        channel="host_turn",
        source="matrx_ai/agent_runners/podcast_generator.py _EXTRACTION_HOST_TURN_TEXT",
        purpose="the podcast content extractor's activation line; the person's files ride the same turn as her attachments",
        zone="Z5_newest_turn",
        lifetime="on_event",
        producer="matrx_ai.agent_runners.podcast_generator",
        views=("host_turn_parts",),
    ),
    BlockType(
        "inbox_driver",
        "Queued message wakes the thread",
        channel="host_turn",
        source="aidream/services/tooling/inbox_driver.py (the queued row's own text)",
        purpose="a message queued for a thread nobody is in becomes that turn's input, never the person's words",
        zone="Z5_newest_turn",
        lifetime="on_event",
        producer="aidream.services.tooling.inbox_driver",
        views=("host_turn_parts",),
    ),
    BlockType(
        "applets.build fix round",
        "Applet build: fix the last check",
        channel="host_turn",
        source="matrx-frontend features/applets-host/builder/build-session.ts fixHostTurn",
        purpose="the applet builder asks the agent to fix the one check its last answer failed",
        zone="Z5_newest_turn",
        lifetime="on_event",
        producer="matrx-frontend:features/applets-host/builder/build-session.ts",
        views=("host_turn_parts",),
    ),
    BlockType(
        "agent_mail",
        "Agent mail wakes the session",
        channel="host_turn",
        source="aidream/services/agent_messaging/agent_members.py run_agent_turn (the mail notice or the first-turn briefing)",
        purpose="mail for an agent conversation, or its briefing on first add, is delivered as the turn's input without anyone typing it",
        zone="Z5_newest_turn",
        lifetime="on_event",
        producer="aidream.services.agent_messaging.agent_members",
        views=("host_turn_parts",),
    ),
    BlockType(
        "bench_search_results",
        "Bench arm: search results",
        channel="host_turn",
        source="aidream/services/masterworks/bench/arms.py (the corpus search results an arm asked for)",
        purpose="the masterwork bench's research arm asked for corpus searches; their results come back as the next turn",
        zone="Z5_newest_turn",
        lifetime="on_event",
        producer="aidream.services.masterworks.bench.arms",
        views=("host_turn_parts",),
    ),
    BlockType(
        "platform_repair",
        "Repair run: work the chosen problem",
        channel="host_turn",
        source="aidream/services/platform_repair/service.py (HOST_TURN_TEXT)",
        purpose="an admin pressed Start on a known problem without typing; the problem rides the repair_subject context entry",
        zone="Z5_newest_turn",
        lifetime="on_event",
        producer="aidream.services.platform_repair.service",
        views=("host_turn_parts",),
    ),
    BlockType(
        "helper_reattach",
        "Helper resumed after a restart",
        channel="host_turn",
        source="aidream/services/runtime/helper_reattach.py (RESUME_TURN_TEXT)",
        purpose="a helper agent interrupted by a server restart is continued in its own conversation: check what it already did, never repeat a write, then finish",
        zone="Z5_newest_turn",
        lifetime="on_event",
        producer="aidream.services.runtime.helper_reattach",
        views=("host_turn_parts",),
    ),
    BlockType(
        "spend_morning_text",
        "Spend desk: compose the morning text",
        channel="host_turn",
        source='aidream/services/billing/spend_digest/service.py ("COMPOSE MORNING TEXT")',
        purpose="the daily spend text's schedule starts the spend desk in its compose mode; the day's facts ride as variables",
        zone="Z5_newest_turn",
        lifetime="on_event",
        producer="aidream.services.billing.spend_digest.service",
        views=("host_turn_parts",),
    ),
    # ── the rest of the §3.3 inventory (no legacy view; Model view lists them from here) ──
    # Z1 system — frozen after the first completed turn.
    BlockType(
        "intro",
        "Intro",
        channel="system",
        source="matrx_ai/instructions/core.py SystemInstruction.intro",
        purpose="text before the date; no production writer",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:SystemInstruction.__str__",
        dormant=True,
    ),
    BlockType(
        "authored.system",
        "The agent's instructions",
        channel="system",
        source="the agent's system message, variables filled once (matrx_ai/config/unified_config.py replace_variables)",
        purpose="what the author wrote; prompt blocks spliced as <name>...</name>",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.config.unified_config:UnifiedConfig.replace_variables",
        known_seal_break=("B11", "B14"),
    ),
    BlockType(
        "tools_list",
        "Tools/Functions Available",
        channel="system",
        source="matrx_ai/instructions/core.py SystemInstruction._tools_available",
        purpose="a written list of tools; no production writer (the tool array is Z0)",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:SystemInstruction._tools_available",
        dormant=True,
    ),
    BlockType(
        "code_guidelines",
        "Code guidelines",
        channel="system",
        source="matrx_ai/instructions/core.py SystemInstruction._code_guidelines",
        purpose="fixed coding guidance; no production writer",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:SystemInstruction._code_guidelines",
        dormant=True,
    ),
    BlockType(
        "safety_guidelines",
        "Safety guidelines",
        channel="system",
        source="matrx_ai/instructions/core.py SystemInstruction._safety_guidelines",
        purpose="fixed safety guidance; no production writer",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:SystemInstruction._safety_guidelines",
        dormant=True,
    ),
    BlockType(
        "rag_awareness",
        "Knowledge the agent has",
        channel="system",
        source="aidream/services/rag/awareness_injection.py (DB rag_awareness_fragment)",
        purpose="the data stores the agent may search, appended to the system prompt",
        zone="Z1_system",
        lifetime="assembly",
        producer="aidream.services.rag.awareness_injection:awareness_fragment_for_agent",
    ),
    BlockType(
        "minor_safety",
        "Minor-safety note",
        channel="system",
        source="aidream/services/education_compliance/content_safety.py (mandate Holder text, else code default)",
        purpose="the account is under 18: the system section on turn one, the per-turn slot after",
        zone="Z1_system",
        lifetime="assembly_plus_changes",
        producer="aidream.services.education_compliance.content_safety:minor_safety_note_for",
        slot="minor_safety",
    ),
    BlockType(
        "observational_memory",
        "Memory",
        channel="system",
        source="aidream/services/ai_execution/ai_task.py observational-memory pre-hook",
        purpose="prior observations: the system section on turn one, the per-turn slot after",
        zone="Z1_system",
        lifetime="assembly_plus_changes",
        producer="aidream.services.ai_execution.ai_task",
        slot="observational_memory",
        doors=frozenset({INTERACTIVE}),
    ),
    BlockType(
        "outro",
        "Outro",
        channel="system",
        source="matrx_ai/instructions/core.py SystemInstruction.outro",
        purpose="text after every section; no production writer",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:SystemInstruction.__str__",
        dormant=True,
    ),
    BlockType(
        "opening_turn",
        "Opening turn",
        channel="system",
        source="matrx_ai/instructions/core.py render_opening_turn (lifted by config/first_turn_filled.py)",
        purpose="a trailing pure-instruction template user turn, carried in the system text",
        zone="Z1_system",
        lifetime="assembly",
        producer="matrx_ai.instructions.core:render_opening_turn",
    ),
    # Z1 wire-only appends — never stored, added on every send after the frozen text.
    BlockType(
        "conversation_instructions",
        "This conversation's instructions",
        channel="system",
        source="matrx_ai/config/send_boundary.py _apply_conversation_instructions",
        purpose="the person's own instructions for one conversation, after the agent's",
        zone="Z1_wire",
        lifetime="every_send",
        producer="matrx_ai.config.prompt_block_producers:produce_conversation_instructions",
        known_seal_break=("B1",),
    ),
    BlockType(
        "agent_modes",
        "The agent's modes",
        channel="system",
        source="matrx_ai/config/send_boundary.py _apply_agent_modes",
        purpose="the agent's modes, the conversation's current mode and its instructions, after the agent's text",
        zone="Z1_wire",
        lifetime="every_send",
        producer="matrx_ai.config.prompt_block_producers:produce_agent_modes",
        # The B1 class: a wire system append whose bytes change when the conversation's mode changes.
        known_seal_break=("B1",),
        views=("platform_parts",),
    ),
    BlockType(
        "agent_tables",
        "The agent's tables",
        channel="turn_context",
        source="aidream/services/agent_understanding/service.py agent_tables_for_turn (built in the record-scope slot)",
        purpose="the custom tables an agent learns into, its entries, and the open entry's fields with how complete each is; headings and data only",
        zone="Z4_turn_context",
        lifetime="every_turn",
        producer="aidream.services.agent_understanding.service:agent_tables_for_turn",
    ),
    BlockType(
        "dictionary",
        "Custom Dictionary",
        channel="system",
        source="matrx_ai/providers/base_translator.py get_stable_system_text",
        purpose="the Custom Dictionary and term lists attached to the run",
        zone="Z1_wire",
        lifetime="every_send",
        producer="matrx_ai.providers.base_translator:BaseTranslator.get_stable_system_text",
        known_seal_break=("B3",),
    ),
    BlockType(
        "reference_fences",
        "Reference values and picklist descriptions",
        channel="system",
        source="matrx_ai/config/send_boundary.py C10 (config/picklist_runtime.py)",
        purpose="matrx reference fences and picklist hidden descriptions resolved into the text sent",
        zone="Z1_wire",
        lifetime="every_send",
        producer="matrx_ai.config.picklist_runtime",
        known_seal_break=("B6", "B7"),
    ),
    BlockType(
        "turn_context_in_system",
        "Per-turn context in the system message",
        channel="system",
        source="matrx_ai/providers/base_translator.py (strict_role_alternation); anthropic/translator.py (empty conversation)",
        purpose="the per-turn block where the provider cannot take it as its own turn",
        zone="Z1_wire",
        lifetime="every_turn",
        producer="matrx_ai.config.message_config:MessageList.render_turn_context",
        known_seal_break=("B5",),
    ),
    # Z3 history — a frame a translator puts around carried text (the text inside is history).
    BlockType(
        "history_system_note",
        "History system note",
        channel="person_turn",
        source="matrx_ai/providers/system_notes.py history_system_messages_as_notes (Anthropic, Google)",
        purpose="a history system message re-sent in place as a <system_note> in a user turn, where the "
        "provider has no mid-list system role",
        zone="Z3_history",
        lifetime="sticky",
        producer="matrx_ai.providers.system_notes:system_note_text",
    ),
    # Z2 template messages — filled once on turn one, replayed from the stored rows.
    BlockType(
        "authored.template",
        "Template messages",
        channel="template",
        source="the agent's authored messages after the system message (stored as chat.message rows)",
        purpose="what the author wrote as the opening messages; the person's words may be glued onto the last",
        zone="Z2_template",
        lifetime="assembly",
        producer="matrx_ai.config.unified_config:UnifiedConfig.replace_variables",
        known_seal_break=("B8",),
    ),
    # Z4 per-turn slots (render_turn_context), each by its slot name.
    *(
        BlockType(
            slot,
            label,
            channel="turn_context",
            source=source,
            purpose=purpose,
            zone="Z4_turn_context",
            lifetime=lifetime,
            producer=producer,
            slot=slot,
            doors=doors,
            delivery=delivery,
            fetch_tool=fetch,
            views=_SLOT_FRAME_VIEWS.get(slot, ()),
        )
        for slot, label, source, purpose, lifetime, producer, doors, delivery, fetch in (
            (
                "live_date",
                "Today's date now",
                "matrx_ai/config/send_boundary.py _announce_live_date",
                "the instant now, naming the pinned date as the start date when it differs (turn two on)",
                "every_turn",
                "matrx_ai.config.prompt_block_producers:produce_live_date",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "helpers",
                "Helpers",
                "matrx_ai/config/helper_roster.py",
                "the agent's helpers and their live state, restated on every send",
                "every_send",
                "matrx_ai.config.helper_roster",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "active_context",
                "Active context",
                "aidream/services/conversation_context/context_utils.py",
                "the live selection, the surface intro, the record scope, the deferred keys",
                "every_turn",
                "aidream.services.conversation_context.context_utils",
                ALL_DOORS,
                ("inline", "on_request"),
                "context",
            ),
            (
                "context_manifest",
                "Available context",
                "aidream/services/conversation_context/context_objects.py",
                "the <available_context> list of values delivered on request",
                "every_turn",
                "aidream.services.conversation_context.context_objects",
                ALL_DOORS,
                ("on_request",),
                "context",
            ),
            (
                "earlier_turn_context",
                "Earlier turns' context",
                "aidream/services/conversation_context/earlier_turn_context.py",
                "values earlier turns held that differ from now",
                "every_turn",
                "aidream.services.conversation_context.earlier_turn_context",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "sandbox_briefing",
                "Sandbox",
                "aidream/services/sandboxes/sandbox_briefing.py",
                "the armed sandbox",
                "every_turn",
                "aidream.services.sandboxes.sandbox_briefing",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "conversation_attachments",
                "Attached repos and files",
                "aidream/services/conversation_attachments/briefing.py",
                "the repos / files attached to this chat",
                "every_turn",
                "aidream.services.conversation_attachments.briefing",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "system_notes",
                "Surface notes",
                "aidream/services/system_notes/stage.py",
                "the platform notes the surface declares (minus agents.context.system_notes_disabled)",
                "every_turn",
                "aidream.services.system_notes.stage:stage_system_notes",
                frozenset({INTERACTIVE}),
                ("inline",),
                None,
            ),
            (
                "room_view",
                "Group chat view",
                "aidream/services/group_chat/stager.py",
                "what the other participants of a Group Chat said",
                "every_turn",
                "aidream.services.group_chat.stager:stage_room_view",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "remarks",
                "Remarks reply note",
                "aidream/services/comment_replies/reply_note.py",
                "how to answer the person's remarks in their comment threads",
                "every_turn",
                "aidream.services.comment_replies.reply_note:stage_remarks_reply_note",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "coding_session_provenance",
                "Coding session provenance",
                "aidream/services/coding_session_bridge/conversation_responder.py",
                "where a mirrored coding-session turn came from",
                "every_turn",
                "aidream.services.coding_session_bridge.conversation_responder",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "handed_over",
                "Handed over by the Conductor",
                "aidream/services/orchestras/passthrough.py",
                "the values an Orchestra's Conductor handed this member",
                "every_turn",
                "aidream.services.orchestras.passthrough",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "turn_values",
                "This turn's values",
                "matrx_ai/agents/live_structure.py (held conversation per-turn values)",
                "the current framing values on a held conversation whose system text keeps turn one's",
                "every_turn",
                "matrx_ai.agents.live_structure",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "structured_output_contract",
                "Answer contract (per turn)",
                "matrx_ai/providers/unified_client.py capability downgrade",
                "the JSON text contract for a model that cannot enforce a schema",
                "every_send",
                "matrx_ai.schema.answer_contract:json_text_contract",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "prefill",
                "Prefill note",
                "matrx_ai/config/message_flags.py",
                "the assistant-prefill conversion note for a model that cannot prefill",
                "every_send",
                "matrx_ai.config.message_flags",
                ALL_DOORS,
                ("inline",),
                None,
            ),
            (
                "turn_context_now",
                "Per-turn context changes",
                "matrx_ai/config/message_config.py render_turn_context_changes",
                "the turn-context blocks that changed after the turn's first send, restated at the tail",
                "every_send",
                "matrx_ai.config.message_config:MessageList.render_turn_context_changes",
                ALL_DOORS,
                ("inline",),
                None,
            ),
        )
    ),
    BlockType(
        "picked_shapes",
        "Shapes the person picked",
        channel="turn_context",
        source="aidream/services/tooling/output_kinds.py stage_picked_shapes",
        purpose="the reply shapes the person picked in the chat's Can make control, relayed as a directive",
        zone="Z4_turn_context",
        lifetime="every_turn",
        producer="aidream.services.tooling.output_kinds:stage_picked_shapes",
        slot="output_shapes",
        doors=frozenset({INTERACTIVE}),
    ),
    BlockType(
        "chat_core",
        "Core instructions (chat mode)",
        channel="system",
        source="aidream/services/tooling/chat_mode.py stage_core_block (text: System Context items chat_core_*)",
        purpose="what skills are and how to find a skill or a tool, for a chat agent and a converted conversation: "
        "the system section on a chat agent's turn one, the per-turn slot (same bytes every turn) after conversion",
        zone="Z1_system",
        lifetime="assembly_plus_changes",
        producer="aidream.services.tooling.chat_mode:stage_core_block",
        slot="chat_core",
        doors=frozenset({INTERACTIVE}),
    ),
    BlockType(
        "skill_offer",
        "Skills that might fit (chat mode)",
        channel="turn_context",
        source="aidream/services/tooling/chat_offer.py before_provider_call (text: System Context items "
        "skill_offer_header / skill_offer_footer; the list: skill_offer.what_would_be_offered)",
        purpose="the skills a meaning search found for the person's message on a chat-box turn, as a suggestion "
        "list; frozen with the turn at its first send, or restated once at the tail when it arrived late "
        "(chat-agent-skills lane G)",
        zone="Z4_turn_context",
        lifetime="every_turn",
        producer="aidream.services.tooling.chat_offer:before_provider_call",
        delivery=("inline", "on_request"),
        fetch_tool="skill",
        slot="skill_offer",
        doors=frozenset({INTERACTIVE}),
    ),
    # Z0 tools and P request settings — not text, but placed and cached like it.
    BlockType(
        "tools.belt",
        "Tools",
        channel="tools",
        source="aidream/services/tooling/tool_merge.py apply_unified_tools; matrx_ai/tools/declaration_ledger.py",
        purpose="the tool array, append-only per conversation and provider by the declaration ledger",
        zone="Z0_tools",
        lifetime="sticky",
        producer="matrx_ai.tools.declaration_ledger",
        known_seal_break=("B9",),
    ),
    BlockType(
        "tools.web_search",
        "Hosted web search",
        channel="tools",
        source="matrx_ai/providers/anthropic/translator.py (web_search_20250305 after the ledger)",
        purpose="the provider's hosted search tool",
        zone="Z0_tools",
        lifetime="every_send",
        producer="matrx_ai.providers.anthropic.translator",
        known_seal_break=("B10",),
    ),
    *(
        BlockType(
            setting,
            label,
            channel="params",
            source=source,
            purpose=purpose,
            zone="P_params",
            lifetime="every_send",
            producer=producer,
        )
        for setting, label, source, purpose, producer in (
            (
                "response_format",
                "Response format",
                "matrx_ai/config/send_boundary.py (relaxed after the first valid answer)",
                "the declared output schema, enforced on turn one",
                "matrx_ai.config.send_boundary",
            ),
            (
                "cache_marks",
                "Cache marks",
                "matrx_ai/config/cache_marks.py, config/cache_plan.py",
                "where the provider cache marks sit and their TTL",
                "matrx_ai.config.cache_plan",
            ),
            (
                "prompt_cache_key",
                "Prompt cache key",
                "matrx_ai/config/send_boundary.py _set_prompt_cache_key",
                "the per-conversation cache routing key",
                "matrx_ai.config.send_boundary:_set_prompt_cache_key",
            ),
        )
    ),
)

#: VIEW NAMES of the context viewer's two census tables (aidream ``context_blocks``).
BLOCK_CENSUS_VIEW = "block_census"
CLIENT_WIRE_SLOTS_VIEW = "client_wire_slots"

#: What the context viewer shows people for each block, by census id (slot, else block id), and
#: which of its two tables lists it — applied onto ``BlockType.viewer_text`` below. Viewer labels
#: for people, never sent to a model (golden: tests/prompt_blocks/golden/viewer_text.json).
_VIEWER_TEXT: dict[str, tuple[str, str]] = {
    # The per-turn context channel (``MessageList.attach_turn_context`` slots).
    "active_context": (BLOCK_CENSUS_VIEW, "the live selection, the surface intro, the record scope, the deferred keys"),
    "context_manifest": (BLOCK_CENSUS_VIEW, "the <available_context> block of per-value elements"),
    "earlier_turn_context": (BLOCK_CENSUS_VIEW, "values earlier turns held that differ from now"),
    "sandbox_briefing": (BLOCK_CENSUS_VIEW, "the armed sandbox"),
    "conversation_attachments": (BLOCK_CENSUS_VIEW, "the repos / files attached to this chat"),
    "skills": (BLOCK_CENSUS_VIEW, "skills attached after the prompt froze / the <available_skills> preamble"),
    "observational_memory": (BLOCK_CENSUS_VIEW, "prior observations (per-turn slot or system section)"),
    "minor_safety": (BLOCK_CENSUS_VIEW, "the minor-safety note (per-turn slot or system section)"),
    "coding_session_provenance": (BLOCK_CENSUS_VIEW, "where a mirrored coding-session turn came from"),
    "live_date": (BLOCK_CENSUS_VIEW, "today's date when the pinned prompt date is not today"),
    "room_view": (
        BLOCK_CENSUS_VIEW,
        "what the other participants of this Group Chat said, per this participant's view policy",
    ),
    "handed_over": (BLOCK_CENSUS_VIEW, "the values an Orchestra's Conductor handed this member as message text"),
    "remarks": (
        BLOCK_CENSUS_VIEW,
        "how to answer the person's remarks (c3 …) in their comment threads, on a turn that carries them",
    ),
    "system_notes": (
        BLOCK_CENSUS_VIEW,
        "the platform notes the surface declares (System Context items: how replies render, the clickable blocks, …)",
    ),
    "output_shapes": (
        BLOCK_CENSUS_VIEW,
        "the reply shapes the person picked in the chat's \"Can make\" control, relayed as a directive",  # agent-context-text-ok: viewer label for people, never sent to a model
    ),
    "turn_values": (
        BLOCK_CENSUS_VIEW,
        "the current framing values (clock, channel, timezone) on a held conversation, whose system text keeps the first turn's",
    ),
    "helpers": (
        BLOCK_CENSUS_VIEW,
        "the agent's helpers (sub-agents): which are running, finished and reported, failed or waiting on the person, restated on every send",
    ),
    "turn_context_now": (
        BLOCK_CENSUS_VIEW,
        "the turn-context blocks that changed after the turn's first send, restated at the tail",
    ),
    "agent_identity": (
        BLOCK_CENSUS_VIEW,
        "who made the agent: AI Matrx and the lab of the model answering (the organization's identity statement)",
    ),
    "person_context": (
        BLOCK_CENSUS_VIEW,
        "what the person asked the platform to remember: saved memories and custom instructions",
    ),
    "run_environment": (
        BLOCK_CENSUS_VIEW,
        "where the agent is running (chrome extension, cloud, sandbox, local machine) and what its tools reach there",
    ),
    "inherited_history": (BLOCK_CENSUS_VIEW, "the contract of a child agent that starts from another conversation"),
    # Server additions to the system prompt.
    "organization_catalog": (BLOCK_CENSUS_VIEW, "the organizations, scope types and scopes the person belongs to"),
    "rag_awareness": (
        BLOCK_CENSUS_VIEW,
        "the knowledge the agent was told it has (its data-store hint, appended to the system prompt)",
    ),
    "dictionary": (BLOCK_CENSUS_VIEW, "the Custom Dictionary"),
    # Attached INSIDE the model client on its own wire copy, after the host's last step.
    "structured_output_contract": (
        CLIENT_WIRE_SLOTS_VIEW,
        "the JSON text contract for a model that cannot enforce a schema",
    ),
    "prefill": (CLIENT_WIRE_SLOTS_VIEW, "the assistant-prefill conversion note"),
    "live_plan": (
        CLIENT_WIRE_SLOTS_VIEW,
        "the agent's open task list, restated at the end of each send (after the receipt is stamped)",
    ),
}


def _with_viewer_text(entry: BlockType) -> BlockType:
    found = _VIEWER_TEXT.get(entry.census_id)
    if found is None:
        return entry
    view, text = found
    # A new frozen entry from the old one's fields (no dataclass helper: tests/pydantic_migration inventory).
    return BlockType(**{**entry.__dict__, "viewer_text": text, "views": (*entry.views, view)})


BLOCK_TYPES = tuple(_with_viewer_text(b) for b in BLOCK_TYPES)

BLOCKS: dict[str, BlockType] = {b.id: b for b in BLOCK_TYPES}
#: A per-turn slot name → its block (a slot is named by the code that attaches it).
BLOCKS_BY_SLOT: dict[str, BlockType] = {b.slot: b for b in BLOCK_TYPES if b.slot}


def block(block_id: str) -> BlockType:
    """The registered block ``block_id`` (KeyError names it: an unregistered block does not ship)."""
    return BLOCKS[block_id]


def block_for_slot(slot: str) -> BlockType | None:
    return BLOCKS_BY_SLOT.get(slot) or BLOCKS.get(slot)


def block_doors(block_id: str) -> frozenset[str]:
    """The door families a block belongs on (aidream ``INJECTOR_RULES`` reads this, never its own copy)."""
    return BLOCKS[block_id].doors


def placement_violation(block_id: str, *, zone: str, default_formula: bool = False) -> str | None:
    """Why placing ``block_id`` in ``zone`` breaks the lifetime law, or ``None`` when it is lawful.

    A block whose lifetime is not sealable may never sit above the seal; the one exception is the
    DEFAULT formula placing a block flagged ``known_seal_break`` in its own default zone (it
    reproduces today's server order, breaks included, until P4 fixes them).
    """
    entry = BLOCKS.get(block_id)
    if entry is None:
        return f"{block_id!r} is not a registered block"
    if zone not in ZONES:
        return f"{zone!r} is not a zone"
    if zone not in ZONES_ABOVE_SEAL or entry.may_sit_above_seal:
        return None
    if default_formula and entry.known_seal_break and zone == entry.zone:
        return None
    return (
        f"{block_id!r} has lifetime {entry.lifetime!r}, which may not sit above the seal ({zone})"
    )


def _view(name: str) -> dict[str, PlatformPart]:
    return {b.id: b.as_part() for b in BLOCK_TYPES if name in b.views}


#: VIEW — the parts a FIRST send can carry, found in a captured request by the Model view.
PLATFORM_PARTS: dict[str, PlatformPart] = _view("platform_parts")
#: VIEW — host-authored turns the executor adds only AFTER a provider response.
MID_LOOP_PARTS: dict[str, PlatformPart] = _view("mid_loop_parts")
#: VIEW — host-authored turns that START a turn (``HostTurn(reason=...)``): the activation text is
#: not typed by a person, so its reason is registered and shown in the Model view.
HOST_TURN_PARTS: dict[str, PlatformPart] = _view("host_turn_parts")


#: VIEW — the context viewer's census: every block of server text it shows, by census id → the
#: sentence people read (aidream ``context_blocks.BLOCK_CENSUS``).
BLOCK_CENSUS: dict[str, str] = {
    b.census_id: b.viewer_text for b in BLOCK_TYPES if BLOCK_CENSUS_VIEW in b.views and b.viewer_text
}
#: VIEW — the slots attached inside the model client on its own wire copy (aidream
#: ``context_blocks.CLIENT_WIRE_SLOTS``).
CLIENT_WIRE_SLOTS: dict[str, str] = {
    b.census_id: b.viewer_text for b in BLOCK_TYPES if CLIENT_WIRE_SLOTS_VIEW in b.views and b.viewer_text
}


def host_turn_reason_registered(reason: str) -> bool:
    """True when a ``HostTurn`` reason is registered (or is a registered mid-loop reason)."""
    return reason in HOST_TURN_PARTS or mid_loop_reason_registered(reason)


def mid_loop_reason_registered(reason: str) -> bool:
    """True when ``reason`` names a registered mid-loop part (``injection:<kind>`` by prefix)."""
    base = reason.split(":", 1)[0] if reason.startswith("injection:") else reason
    return base in MID_LOOP_PARTS


def _patterns() -> list[tuple[str, re.Pattern[str]]]:
    from matrx_ai.config.agent_identity import IDENTITY_CLOSE, IDENTITY_OPEN
    from matrx_ai.config.person_context import PERSON_CONTEXT_CLOSE, PERSON_CONTEXT_OPEN
    from matrx_ai.config.run_environment import ENVIRONMENT_CLOSE, ENVIRONMENT_OPEN
    from matrx_ai.instructions.core import DATE_BLOCK_CLOSE, DATE_BLOCK_OPEN
    from matrx_ai.schema.answer_contract import GROUNDED_JSON_CONTRACT_OPEN, GROUNDED_JSON_CONTRACT_SCHEMA_LABEL

    return [
        (
            "agent_identity",
            re.compile(re.escape(IDENTITY_OPEN) + r".*?" + re.escape(IDENTITY_CLOSE), re.S),
        ),
        (
            "person_context",
            re.compile(
                re.escape(PERSON_CONTEXT_OPEN) + r".*?" + re.escape(PERSON_CONTEXT_CLOSE), re.S
            ),
        ),
        (
            "run_environment",
            re.compile(re.escape(ENVIRONMENT_OPEN) + r".*?" + re.escape(ENVIRONMENT_CLOSE), re.S),
        ),
        (
            "current_date",
            re.compile(re.escape(DATE_BLOCK_OPEN) + r".*?" + re.escape(DATE_BLOCK_CLOSE), re.S),
        ),
        ("agent_modes", re.compile(r"<agent_modes>.*?</agent_modes>", re.S)),
        ("agent_tables", re.compile(r"<agent_tables>.*?</agent_tables>", re.S)),
        ("organization_catalog", re.compile(r"<org_catalog\b.*?</org_catalog>", re.S)),
        ("skills", re.compile(r"<available_skills>.*?</available_skills>", re.S)),
        ("kind_directives", re.compile(r"## Available Kind Directives\n.*?(?=\n## |\Z)", re.S)),
        (
            "inherited_history",
            re.compile(
                r'<inherited_conversation source="platform">.*?</inherited_conversation>', re.S
            ),
        ),
        (
            "turn_context",
            re.compile(r'<turn_context source="platform"[^>]*>.*?</turn_context>', re.S),
        ),
        ("live_plan", re.compile(r'<your_plan source="platform">.*?</your_plan>', re.S)),
        ("helpers", re.compile(r'<your_helpers source="platform">.*?</your_helpers>', re.S)),
        (
            "grounded_json_contract",
            re.compile(
                r"^" + re.escape(GROUNDED_JSON_CONTRACT_OPEN) + r".*?\n"
                + re.escape(GROUNDED_JSON_CONTRACT_SCHEMA_LABEL) + r"\n[^\n]*",
                re.S | re.M,
            ),
        ),
        # A label that is a whole text part by itself, in every form the producers write: one tag of
        # name="value" attributes and nothing else. Values are html-escaped by the producers, so a raw
        # quote, angle bracket or newline never sits inside one; anything else in the part (a second
        # tag, text between two "/>") is left for the check to report.
        ("attachment_label", re.compile(r'\A\s*<attachment(?: [a-z_]+="[^"<>\n]*")+\s*/>\s*\Z')),
    ]


def without_declared_seal_breaks(text: str) -> str:
    """``text`` with every span of a block DECLARED to break the seal (``known_seal_break``) whose frame is
    recognisable on the wire removed. A change confined to those spans is that block's declared break,
    never prefix drift (``providers/cache_guard``). A breaker with no frame (``conversation_instructions``,
    the person's raw text) cannot be located and is not removed."""
    for part_id, pattern in _patterns():
        entry = BLOCKS.get(part_id)
        if entry is not None and entry.known_seal_break:
            text = pattern.sub("", text)
    return text


def _strings(node: Any, path: str = "") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    if isinstance(node, str):
        out.append((path or "$", node))
    elif isinstance(node, dict):
        for key, value in node.items():
            out.extend(_strings(value, f"{path}.{key}" if path else str(key)))
    elif isinstance(node, list):
        for i, value in enumerate(node):
            out.extend(_strings(value, f"{path}[{i}]"))
    return out


#: An attached file's text block: a whole string opened by its ``<attachment kind="document" ...
#: converted_to="text"/>`` label line. Listed by ``platform_parts_in_request`` only — never removed
#: by ``without_platform_parts`` (the file is the person's attachment, not text the platform wrote
#: around her words; REVIEW-C103 #6: the dry run showed only the value list's one-line note).
_ATTACHED_FILE_TEXT = re.compile(
    r'\A<attachment kind="document"[^\n]*\bconverted_to="text"/>\n', re.S
)


def platform_parts_in_request(
    payload: Any, *, skip_keys: tuple[str, ...] = ("tools",)
) -> list[dict[str, Any]]:
    """Every registered platform part found in a captured request, labeled, verbatim.

    Each entry: ``{id, label, channel, source, purpose, where, text}`` (``where`` is the JSON
    path of the string it sits in). Tool declarations are skipped (they are tools, not text).
    """
    found: list[dict[str, Any]] = []
    patterns = _patterns()
    for where, text in _strings(payload):
        if any(
            where == k or where.startswith(f"{k}[") or where.startswith(f"{k}.") for k in skip_keys
        ):
            continue
        if _ATTACHED_FILE_TEXT.match(text):
            found.append({**asdict(PLATFORM_PARTS["attached_file"]), "where": where, "text": text})
            continue
        for part_id, pattern in patterns:
            for match in pattern.finditer(text):
                part = PLATFORM_PARTS[part_id]
                found.append({**asdict(part), "where": where, "text": match.group(0)})
    return found


def without_platform_parts(text: str) -> str:
    """``text`` with every registered platform part removed (what is left is authored or typed)."""
    for _part_id, pattern in _patterns():
        text = pattern.sub("", text)
    return text


def _wrapper_frames() -> dict[str, tuple[str, str]]:
    """Frames a translator puts AROUND text someone else wrote (the text inside is history or
    authored), by block id. They are never removed with their inside: only once the inside is
    accounted for (``without_empty_wrapper_frames``)."""
    from matrx_ai.providers.system_notes import SYSTEM_NOTE_CLOSE, SYSTEM_NOTE_OPEN

    return {"history_system_note": (SYSTEM_NOTE_OPEN, SYSTEM_NOTE_CLOSE)}


def without_empty_wrapper_frames(text: str) -> str:
    """``text`` with every registered wrapper frame removed whose inside is only whitespace (an
    addition inside a wrapper keeps the wrapper and so stays visible)."""
    for open_tag, close_tag in _wrapper_frames().values():
        if open_tag in text:
            text = re.sub(re.escape(open_tag) + r"\s*" + re.escape(close_tag), "", text)
    return text


def mid_loop_parts() -> list[dict[str, Any]]:
    """The host turns a run MAY add after a provider response, for the Model view."""
    return [asdict(p) for p in MID_LOOP_PARTS.values()]


__all__ = [
    "ALL_DOORS",
    "BLOCKS",
    "BLOCKS_BY_SLOT",
    "BLOCK_CENSUS",
    "BLOCK_CENSUS_VIEW",
    "BLOCK_TYPES",
    "CLIENT_WIRE_SLOTS",
    "CLIENT_WIRE_SLOTS_VIEW",
    "BlockType",
    "DELIVERIES",
    "HOST_TURN_PARTS",
    "INTERACTIVE",
    "LIFETIMES",
    "PROGRAMMATIC",
    "SEALABLE_LIFETIMES",
    "ZONES",
    "ZONES_ABOVE_SEAL",
    "block",
    "block_doors",
    "block_for_slot",
    "placement_violation",
    "host_turn_reason_registered",
    "MID_LOOP_PARTS",
    "PLATFORM_PARTS",
    "PlatformPart",
    "mid_loop_parts",
    "mid_loop_reason_registered",
    "platform_parts_in_request",
    "without_empty_wrapper_frames",
    "without_platform_parts",
]
