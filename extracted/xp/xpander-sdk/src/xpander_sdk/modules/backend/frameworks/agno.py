import asyncio
import hashlib
import json
import re
import shlex
import uuid
from collections import deque
from os import getenv, environ
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from loguru import logger
from pydantic import ValidationError
from xpander_sdk import Configuration
from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.context_optimizer.action_ledger import (
    _PLAN_TOOLS,
    ActionLedger,
    attach_to_task,
    build_entry_from_call,
    get_attached_ledger,
)
from xpander_sdk.core.context_optimizer.constants import (
    COMPACTION_MODEL_ANTHROPIC,
    COMPACTION_MODEL_BEDROCK,
    COMPACTION_MODEL_OPENAI,
    COMPACTION_MODEL_OVERRIDE_ENABLED,
    ERROR_STREAK_FINALIZE_AT,
    FINALIZE_MODE_ENABLED,
    FINALIZE_SAFE_READS_CAP,
    LEDGER_ENABLED,
    LLM_MAX_OUTPUT_TOKENS,
    MAX_PLAN_CHURN,
    MAX_TOTAL_TOOL_CALLS_PER_TOOL,
    PLAN_BLOCK_LABEL,
    PLAN_CHURN_WARN_AT,
    MANUAL_COMPACT_TOOL_ENABLED,
    MAX_REPEATED_TOOL_CALLS,
    READ_TOOL_CALLS_REWARN_EVERY,
    READ_TOOL_CALLS_WARN_AT,
    REPEATED_TOOL_CALL_WARN_AT,
    TOOL_CALL_LIMIT_DEFAULT,
    TOTAL_TOOL_CALLS_WARN_AT,
    TRUNCATED_TOOL_CALL_MESSAGE,
    WRAPUP_GRACE_CALLS,
)
from xpander_sdk.core.context_optimizer.context_optimizer import (
    XPanderContextOptimizer,
    unwrap_tool_result_content,
)
from xpander_sdk.core.context_optimizer.encryption import (
    candidate_scope_ids,
    decrypt,
    derive_key,
    is_context_optimization_file,
    try_decrypt,
)
from xpander_sdk.core.context_optimizer.search import bm25_rank, grep_text
from xpander_sdk.core.context_optimizer.finalize_mode import (
    FINALIZE_NOT_ACTIVE_REJECTION,
    FINALIZE_ONLY_SYSTEM_OVERRIDE,
    build_finalize_tool,
    enter_finalize_mode,
    gate_rejection_message,
    is_finalize_active,
    is_task_finalize_active,
    is_tool_allowed,
    mark_finalize_tool_registered,
)
from xpander_sdk.core.steering import (
    STEER_SKIP_STUB,
    append_to_tool_result,
    arm_steer_batch_skip,
    drain_steers,
    get_steer_key,
    render_steer_block,
    steer_batch_skip_armed,
    steering_contract_block,
)
from xpander_sdk.core.xpander_api_client import APIClient
from xpander_sdk.models.generic import LLMCredentials
from xpander_sdk.models.shared import OutputFormat, ThinkMode
from xpander_sdk.modules.agents.agents_module import Agents
from xpander_sdk.modules.agents.models.agent import (
    AgentGraphItemType,
    LLMReasoningEffort,
    SourceNodeType,
)
from xpander_sdk.modules.agents.sub_modules.agent import Agent
from xpander_sdk.modules.backend.utils.extra_headers import sanitize_extra_headers
from xpander_sdk.modules.backend.utils.mcp_connect import (
    is_mcp_auth_error,
    mark_probe_failed,
    mark_probe_ok,
    probe_mcp_server,
    probe_recently_failed,
    probe_recently_ok,
)
from xpander_sdk.modules.backend.utils.mcp_oauth import authenticate_mcp_server
from xpander_sdk.modules.backend.utils.prompt_budget import log_prompt_budget
from xpander_sdk.utils.json_parsing import parse_structured_string
from xpander_sdk.modules.backend.utils.tool_call_events import (
    coerce_json_like,
    report_steer_applied,
    DYNAMIC_META_TOOLS,
    extract_reasoning,
    get_tool_call_summary,
    is_agent_gateway_task,
    is_reasoning_tool,
    PLANNING_TOOLS,
    REASONING_TOOLS,
    report_reasoning_event,
    report_tool_call_request,
    report_tool_call_result,
    resolve_plan_task_id,
    should_skip_tool_report,
    TOOL_CALL_PLAN_TASK_ID,
)
from xpander_sdk.modules.tasks.sub_modules.task import Task
from xpander_sdk.modules.tools_repository.models.mcp import (
    MCPOAuthGetTokenGenericResponse,
    MCPOAuthGetTokenResponse,
    MCPOAuthResponseType,
    MCPServerAuthType,
    MCPServerDetails,
    MCPServerTransport,
    MCPServerType,
)
from xpander_sdk.modules.tools_repository.models.tool_invocation_result import (
    ToolInvocationResult,
)
from xpander_sdk.modules.tools_repository.sub_modules.mcp_tool_proxy import (
    build_mcp_proxies,
)
from xpander_sdk.modules.tools_repository.sub_modules.tool import Tool
from xpander_sdk.modules.tools_repository.utils.billing_context import (
    current_tool_call_id,
)
from xpander_sdk.modules.tools_repository.utils.schemas import build_model_from_schema
from xpander_sdk.modules.tools_repository.utils.workspace_payload import (
    WORKSPACE_PATH_KEY,
    strip_workspace_path,
    WorkspacePayloadError,
    has_workspace_path,
    resolve_workspace_payload,
)
from agno.agent import Agent as AgnoAgent
from agno.team import Team as AgnoTeam
from agno.guardrails import PIIDetectionGuardrail
from agno.guardrails import PromptInjectionGuardrail
from agno.guardrails import OpenAIModerationGuardrail
from agno.models.base import Model

from xpander_sdk.utils.agno_output_parsing import install_agno_output_parsing_patch
from xpander_sdk.utils.cache import backend_config_cache, scope_token
from xpander_sdk.utils.event_loop import run_sync

# agno's structured-output cleaner turns literal newlines into spaces, flattening markdown
if not install_agno_output_parsing_patch():
    logger.warning("[agno-parsing] inactive - markdown answers may arrive flattened")

# Feature flags
USE_HEADROOM: bool = True

# Strong refs to fire-and-forget activity-report tasks. asyncio only holds a weak
# ref to a bare create_task, so without this the loop can GC a report mid-flight
# and silently drop a ToolCallRequest/Result from the sub-execution activity log.
_BG_REPORT_TASKS: set = set()


def _spawn_bg(coro) -> None:
    """Run *coro* in the background, retaining a strong ref until it finishes."""
    task = asyncio.create_task(coro)
    _BG_REPORT_TASKS.add(task)
    task.add_done_callback(_BG_REPORT_TASKS.discard)


# Lazy, guarded singleton SmartCrusher for Layer-0 lossless compaction.
# headroom is Rust-backed (headroom._core) and hard-imports the native ext;
# building it lazily keeps cold-start fast and lets a missing wheel degrade to
# passthrough (callers wrap usage in try/except) instead of breaking this import.
_headroom_crusher = None


def _get_headroom_crusher():
    global _headroom_crusher
    if _headroom_crusher is None:
        from headroom.config import CCRConfig
        from headroom.transforms.smart_crusher import SmartCrusher

        # CCR disabled: we do not wire headroom's headroom_retrieve tool — xpander
        # Layer 1 owns reversible offload — so any unresolvable marker is discarded.
        _headroom_crusher = SmartCrusher(ccr_config=CCRConfig(enabled=False))
    return _headroom_crusher


def _headroom_compact(raw: Any) -> Optional[str]:
    """Losslessly compact a JSON tool result, or ``None`` to keep the original.

    Returns ``None`` when the input is not JSON, the output did not shrink, or
    the output carries an unresolvable ``<<ccr:>>`` marker (which would require a
    retrieval tool we deliberately do not wire — xpander Layer 1 owns offload).
    """
    src = raw if isinstance(raw, str) else json.dumps(raw)
    # Only JSON objects/arrays can compact; cheap first-non-space scan (no full-
    # string copy or throwaway json.loads) gates out everything else. The crusher
    # raises a Rust PanicException (a BaseException, not Exception) on bad input,
    # so guard the call itself with BaseException.
    i, n = 0, len(src)
    while i < n and src[i] in " \t\r\n":
        i += 1
    if i >= n or src[i] not in "{[":
        return None
    try:
        out = _get_headroom_crusher().compact_document_json(src)
    except BaseException:
        return None
    if "<<ccr:" in out or len(out) >= len(src):
        return None
    return out


# Long agent turns (big context, deep reasoning) outlive the providers' default 600s client timeout
LLM_REQUEST_TIMEOUT_SECONDS: float = 12 * 60 * 60


# Context optimization system prompt guidance — always injected (Layer 1 always runs)
CONTEXT_OPTIMIZATION_INSTRUCTIONS = """
<context_optimization>
Some tool results are truncated to save space. A "[TRUNCATED OUTPUT]" message carries a
`context_id` UUID; the full result is saved encrypted at `CONTEXT_OPTIMIZATION/<context_id>.xp`.
To read it, call `xpworkspace-context-retrieve` with that context_id (scoped to the current task —
items from other tasks can't be decrypted). Do NOT bash (`cat`, `head`) or `xpworkspace-file-read`
these paths — they return base64 ciphertext, not plaintext.
After a compaction you may see a `<session_backup>` pointer
(`CONTEXT_OPTIMIZATION/session_backup_<task_id>.xp`) holding the full pre-compaction transcript;
retrieve it with `context_id="session_backup_<task_id>"`, only when the summary lacks a specific detail.
Never guess or hallucinate truncated content — fetch it if you need it.
To transform or persist offloaded data (reformat rows, build an INSERT/COPY, derive a file), do NOT
retype it from memory or paste it into a script. Retrieve it ONCE and, in the SAME step, write it to a
plaintext workspace file with xpworkspace-file-write; then operate on THAT file by path — scripts read
the data file (e.g. `python build.py data.json`), never embed rows inline in a heredoc or string
literal. Retrieving the same context_id repeatedly, or reconstructing its contents from memory, is a bug.
</context_optimization>
"""


GROUNDING_INSTRUCTIONS = """
<grounding>
State an action as done ONLY when a tool call actually ran and returned success. Never present a
results/success table (rows like "applied", "updated", "created", "22/22 ✓") for work you did not
execute — if you did not call the tool, say what you WOULD do, not that you did it.
Never invent, quote, or attribute a prior user message or request that is not in the conversation
above; if you are unsure whether something was asked, check or ask rather than assert it happened.
A tool result carrying an HTTP 4xx/5xx or error(...) is a FAILURE, not an empty result. Never report
it as "no results found" / "nothing matched" — say the lookup failed and why (quote the status), then
fix the call (e.g. correct the identifier) or surface the failure.
Evidence comes from tool results already visible in this conversation. A result above you IS
grounding — never call a tool to refresh, re-witness, or re-confirm something already done.
Your FINAL answer is the OUTCOME, never a promise or progress note. Never end a run
with "I've started..." / "I'm identifying..." / "I will..." - state what IS done (with
the evidence) and, when work remains, list exactly what was completed vs what was not.
A promise-shaped final answer is a failed run dressed as progress.
When following a procedural document (playbook, runbook, SOP): execute its steps AS WRITTEN.
If it mandates an artifact (a ledger, log, or evidence table), produce that artifact. Never
substitute improvised rules, labels, or categories for ones the document defines - when it
requires a basis or citation per item, cite the exact rule/row you applied, and mark anything
you could not ground as unresolved instead of inventing a classification for it.
</grounding>
"""


# Workspace output guidance — only injected when the agent has workspace tools
def _build_skills_instructions(skills) -> str:
    """Inline catalog of the agent's resolved skills.

    Skills are listed here directly (name + description) so the agent does NOT
    need to read ./skills/INDEX.md to discover them — that file is synced into
    the workspace asynchronously and may lag a cold boot. To USE a skill, the
    agent loads it in one xpload_skill call (workspace file reads are the
    fallback); scripts still run from ./skills/<name>/. Returns "" when the
    agent has no skills.
    """
    rows = [
        f'  <skill name="{(s.get("name") or "").strip()}">{(s.get("description") or "").strip()}</skill>'
        for s in (skills or [])
        if isinstance(s, dict) and s.get("name")
    ]
    if not rows:
        return ""
    return (
        '\n<skills note="playbooks installed in your workspace under ./skills '
        "(already synced). The list below is ONLY a preview (skill name + one-line "
        "description) — it is NOT enough to run a skill, and you must never assume a "
        "skill's contents. Before you use a skill, load it with ONE "
        "xpload_skill(skill_name) call: it returns the full SKILL.md plus its "
        "key reference files. Call it ONLY when you actually intend to use "
        "that skill this turn, and skip it entirely when the playbook is "
        "already in your task context (&lt;skill_playbook&gt;) — never load it "
        "twice. If xpload_skill is unavailable or lists a file without "
        "inlining it, read its SKILL.md (or that listed file) with "
        "xpworkspace-file-read from ./skills/&lt;name&gt;/; never act on this "
        "preview alone. Run its "
        "scripts via xpworkspace-bash. The ./skills folder is managed and read-only "
        "(synced from the platform; anything you write there is deleted on the next sync) - "
        "never write to ./skills or overwrite a synced skill, and NEVER author skill files "
        "yourself (no SKILL.md, no local_skills/): new skills are created ONLY through the "
        "platform's skill-building flow. CONFIDENTIAL: skill names "
        "and the ./skills path are internal "
        "implementation details. NEVER mention a skill's name, the ./skills path, or the fact "
        "that you used a skill in any output to the user. When describing what you did, refer "
        'to the capability generically, not by skill name.">\n'
        + "\n".join(rows)
        + "\n</skills>\n"
    )


TURN_ECONOMY_INSTRUCTIONS = """
<turn_economy>
Every turn re-reads your entire system prompt and tool catalog, so a turn that makes one
tool call costs the same prefix as a turn that makes six. Splitting independent work
across turns is pure waste.
When several tool calls do NOT depend on each other's results, emit them ALL in the same
turn - the runtime already runs them concurrently. Reading four files, grepping three
patterns, checking two schedules: one turn, N calls, not N turns.
Serialize ONLY when a call genuinely needs a previous call's output - xp_get_tool before
xp_execute_tool, or a path you first had to learn from glob.
The cheapest turn of all is the one with zero tool calls: it is the only turn that ends
the run, and it is the correct final turn of every task.
This does NOT override the rules that deliberately end a turn: one plan-tool call per
turn, one interactive card per turn, one dispatch per gateway turn. Those stand.
</turn_economy>
"""


TOOL_CALL_DISCIPLINE_INSTRUCTIONS = """
<tool_call_discipline>
Every tool call must earn its place: call a tool only to obtain information you do not
already have or to change state you have not yet changed. Before each call, name the
concrete thing it will tell you or do - if you cannot, you are finished: the call must
not happen. A call you cannot title with a real action is a call you must not make.
Ending the run is an action you always have: a turn with ZERO tool calls that carries
your final answer. That turn is the closing step - always available, never wrong, and
the cheapest turn you can take. The moment the work is done, take it: write the answer.
A finished answer never needs one more tool call first. Do not re-run a command you already ran just to have
something current to show, and do not shell out for what you can do inline: trivial
arithmetic, unit conversions, date math, or reformatting a value you already hold
belong in your answer directly.
A refusal or block ("Refused:", "Redundant call blocked", "No memory was changed",
"Already known", "Not written") means that call class is spent: never retry it in
another wording or through another tool, and a platform refusal is never a lesson
worth saving to memory. When in doubt between one more tool call and answering - answer.
</tool_call_discipline>
"""


WORKSPACE_OUTPUT_INSTRUCTIONS = """
<large_output_strategy>
If your output would exceed ~4,000 words, write it to a workspace file instead of inline —
inline hits the output token limit and silently truncates.
- xpworkspace-file-write is the primary writer; use xpworkspace-bash for incremental builds
  or when you also run commands. payload is a JSON object literal —
  {"payload":{"body_params":{"path":"...","content":"..."}}}, never a quoted/stringified string.
- Paths are relative to the workspace root — never start with '/'. /tmp is ephemeral (cleared
  between sessions); never write output there.
- When done, return a link with xpworkspace-file-share. Do NOT xpworkspace-file-read the file to
  "share" or echo it — that re-bloats context; file-share serves the URL straight from the workspace.

<chunked_writes>
Applies ONLY when the file itself is the deliverable (a document, report, or code artifact the user
receives). Data destined for a consuming tool (SQL INSERT, API payload) → use <large_payload_authoring>
instead and do NOT chunk it.
First decide HOW to produce it — typing it out is not always right:
- REPEATED STRUCTURE (one shape over many rows: a table, a catalog, a manifest, per-item cards) AND the
  row data already sits in a workspace file → build it with a small script that reads that file BY PATH
  and writes the output in one pass. You type the template once, not once per row. This is the cheapest
  and safest path for structured formats: a `json.dump` is valid by construction, where hand-typing
  thousands of lines of JSON risks a truncated, invalid file and a debug loop.
- FREE-FORM PROSE, small files, or anything whose structure is not repetitive → write it directly with
  xpworkspace-file-write, chunked per the rules below. A script buys nothing here.
- NEVER paste rows inline into a heredoc or string literal to feed a script. That re-materializes the
  whole dataset as output tokens and is strictly worse than either path above — the script must read
  its input from a file by path, or don't script it.
- Derived per-item analysis (a summary, a rating, a rationale you reasoned out) is expensive: it can
  only come from you. Author it ONCE, into a structured data file, then template every downstream
  deliverable from that file. Never write the same item's text twice — once as prose, again as JSON.

For large output written directly (long docs, many-section files, big code):
- Never emit the whole payload in one write — it truncates mid-write, and every `content` string is
  also echoed into message history, doubling context + output cost.
- Size: soft target ~8,000 chars per `content`; hard cap 12,000 (~3K tokens). Split only when the file
  genuinely exceeds this — a 25K-char file is 2-3 chunks, not 8. Don't split small files.
- For free-form prose where scripting doesn't fit: outline N chunks once (number 1/N..N/N), write
  chunk 1 with mode='w' (header + section 1), chunks 2..N with mode='a' (one section each), then
  xpworkspace-file-share. Check the size only when a chunk write reported an anomaly — never
  file-read the whole file back, and skip the check entirely on routine writes.
- Encoding: write raw UTF-8 in natural codepoint form (—, 🥺, é) — never pre-encode, escape,
  double-encode, or paste Latin-1 mojibake (â€", ðŸ¥º). Split only at paragraph/sentence
  boundaries, never mid-character.
- Concatenation: each chunk continues exactly where the last ended — no repeated headings, no
  "as above" bridging. Keep a trailing \\n on every non-final chunk. Don't wrap chunks in code
  fences unless the whole file is code (they nest and break). For code, close each block within its
  chunk and split at top-level declarations; for JSON/YAML/XML write as one chunk if possible, else
  split only at element boundaries. Don't re-read between appends; if you lose the chunk index,
  `tail -n 30 <path>` once.
- Don't echo chunk content in prose before/after a write; don't restate the plan between writes.
  Keep inter-write messages to <=1 sentence ("writing chunk 3/7").
</chunked_writes>

<bulk_data_handling>
For large structured result sets (100+ rows, CSV-like):
- Don't enumerate or echo rows in messages — materializing them fills context and triggers
  compaction. Save to a workspace file in ONE write, then inspect via xpworkspace-bash
  (head/wc/grep/awk); never read it back just to look.
- Persisting many records: prefer ONE bulk insert/COPY (workspace_path payload) over N per-row
  calls. If the destination tool only supports rowwise inserts AND N > 10, ask the user first.
- A single deterministic operation (a 270-row INSERT, one COPY) is ONE tool call — never split it
  "for safety". If its payload is large, offload it via workspace_path (<large_payload_authoring>);
  the chunking in <chunked_writes> is for building a deliverable *file*, not for splitting one tool
  call's payload.
- If the user restricts an output format ("no CSV", "no JSON output"), obey literally — never
  produce it in chat; if you need it as scratch, write it silently to the workspace and never echo it.
</bulk_data_handling>
</large_output_strategy>
"""

# Workspace secrets guidance — only injected when workspace tools are present.
# Tells the agent its org-configured secrets arrive as env vars and that values are
# managed by an admin in the xpander.ai UI, not by the agent itself.
WORKSPACE_SECRETS_INSTRUCTIONS = """
<workspace_secrets>
Secrets your organization configured for this agent (API keys, tokens, connection strings) are
available inside the workspace as environment variables — read them with xpworkspace-bash (`env`,
`$VAR_NAME`) or from skill scripts via os.environ / process.env. Use them directly; never paste a
secret's value back into chat or into a file you share.
You cannot see, add, edit, or delete these values yourself. If a secret is missing or wrong, ask
your admin to manage it in the xpander.ai UI (workspace settings) — do not attempt to set it via
shell.
</workspace_secrets>
"""

# Large-payload authoring guidance — only injected when workspace tools are present.
# Tells the LLM to offload very large tool-call payloads to a workspace file and
# pass `workspace_path` instead of inlining. Resolution happens server-side in the
# SDK pre-dispatch hook.
LARGE_PAYLOAD_AUTHORING_INSTRUCTIONS = """
<large_payload_authoring>
When a tool call's inline payload would be large (>= ~4000 chars — long SQL, a config blob, a big
JSON doc, a code artifact), do NOT inline it: inlining wastes context, inflates output tokens, and
risks silent truncation. Offload it to a workspace file and pass `workspace_path` instead. Small
calls stay inline.

- Argument shape: payload is ALWAYS a JSON object literal {...}, never a quoted/stringified string;
  body_params/query_params/path_params/headers are objects too. The offload payload is the object
  {"workspace_path":"<path>"}.
- Scope: workspace_path is for non-internal tools only. NEVER set it on xpworkspace-*, xpschedule-*,
  or xpcompact_context — those are always inline.

Protocol:
1. Announce first — one short message to the user that the payload is large and you'll assemble it in
   chunks. Don't silently start writing.
2. Build the payload as a JSON object in a workspace file with xpworkspace-file-write: first chunk
   mode='w', rest mode='a' until the whole object is written. Relative path, no leading '/'
   (e.g. payloads/redshift_query_42.json). Inter-chunk messages <=1 sentence. When the payload derives
   from offloaded/large data, build it FROM that data's workspace file (transform in place per
   <context_optimization>) — never re-key values from memory or the conversation summary.
3. Call the real tool with workspace_path set to that file, leaving body_params/query_params/
   path_params empty (ignored when workspace_path is set). The runtime reads, parses, and runs the
   file contents as the entire payload, recording the resolved data in the activity log.

Rules:
- File must be a valid JSON object literal matching the tool's schema (body_params/query_params/
  path_params/headers). Plain-text payloads aren't supported.
- 1MB cap on the resolved file; if you exceed it, split the work into multiple smaller calls.
- Encoding: raw UTF-8 in natural codepoint form (—, 🥺, é) — never mojibake bytes (â€", ðŸ¥º),
  never pre-encode/escape/double-encode.

Fidelity (CRITICAL): the file is read verbatim and forwarded to the consuming tool — no second pass,
no review step. For external operations (email, Slack, SMS, HTTP POST, SQL, deploy, file share) the
recipient/backend receives exactly the file contents, not `workspace_path`. Write the REAL, FINAL,
COMPLETE data: every field fully written out, every templated value resolved to its actual final
value, nothing abbreviated, elided, or borrowed from these instructions or schema docstrings. If the
data isn't ready, assemble it in your reasoning first, then write. Verify every field (subject,
title, body, query, recipients, URLs) is the final value before invoking the consuming tool.

Cleanup:
- On success, delete the file with xpworkspace-bash `rm <path>` — these are write-once disposable
  scratch. Keep it only if the user asked for the file or the same payload is reused in an
  immediate follow-up call.
- On failure, keep the file so you can inspect and retry.
- If the user wants the file itself, xpworkspace-file-share it before deleting — never
  xpworkspace-file-read it back to echo.
- Unsure after many chunks? xpworkspace-bash `wc -c <path>` for a cheap size check — never file-read
  the file back into context.

General large output that IS the deliverable (long doc, report, code) → use the chunked-writes
protocol in <large_output_strategy>, not this.
</large_payload_authoring>
"""

# Compact tool guidance — only injected when xpcompact_context is registered
COMPACT_TOOL_INSTRUCTIONS = """
<compact_tool>
xpcompact_context manually compresses conversation history — heavyweight; use only on evidence of
context pressure, never preemptively.
Call when at least one holds: many [TRUNCATED OUTPUT] markers in recent results; you just finished a
distinct work phase and are pivoting to substantially different work; the session was already
auto-compacted (a `<session_resume>` message sits at the top, so space is tight).
Do NOT call: mid-task or mid-investigation; just because the conversation is long; more than once per
phase; within ~3 turns of an auto-compaction (it already cleared headroom — do real work first).
Wrap args in a `payload`: a `focus` string for what the summary MUST preserve, plus the required
`headers` block. Example: xpcompact_context(payload={"focus":"preserve API signatures, test results,
migration plan","headers":{"toolcallreasoningtitle":"Compact context","toolcallreasoningdescription":
"Free context after research phase."}})
</compact_tool>
"""

# Deep-planning system-prompt guidance — only injected when the agent + task both
# enable deep planning. The xp* plan tools' own schemas/descriptions are injected
# separately by agno; this block supplies workflow + enforcement rules only.
# Shared prompt fragments — one wording for both instruction blocks so the
# create-path and seeded-path copies cannot drift on the next tuning.
_PLAN_BATCH_RULE = """Completions: at natural boundaries (finished a phase, switching focus, or about
  to write the final answer) mark ALL steps finished since your last update in ONE
  xpcomplete_agent_plan_items call — ids=[...] takes multiple UUIDs. A dedicated turn per
  checkbox wastes a full model round-trip; toolcallplantaskid, not the completion call, is
  what tells the platform which step you are on."""

_PLAN_UUID_RULE = """UUIDs are the full exact strings returned by the plan tools (xpcreate_agent_plan /
  xpget_agent_plan) — never shorten, guess, or invent. toolcallplantaskid is the CURRENT
  step's plan UUID — NEVER a task or execution id; use
  "" only when no plan/step applies."""

DEEP_PLANNING_INSTRUCTIONS = """
<deep_planning>
Use plan tools ONLY for genuinely multi-step tasks (several distinct steps). For a
single-action or trivial request (one lookup, one send, one answer) act directly —
creating a plan there is wrong and wasteful.

Workflow (multi-step only):
1. xpcreate_agent_plan — list all steps up front. tasks=[{"title":"..."}] (objects,
   not strings; titles 3-6 words). Prefer body_params={"tasks":[...],"auto_start":true} to
   create AND start the plan in one call (enables enforcement) — this is the default path.
2. xpstart_execution_plan (body_params={}) — only needed when you did NOT pass
   auto_start=true to xpcreate_agent_plan; enables enforcement.
3. Per step: read ALL step UUIDs from xpcreate_agent_plan's response (or one
   xpget_agent_plan) -> do the work, setting the header toolcallplantaskid to the CURRENT
   step's full UUID on EVERY non-plan tool call. When you move to the next step, update
   toolcallplantaskid to the new step's UUID — it is per-step, never a fixed value reused
   across steps. Accurate progress tracking depends on each call carrying its real step id.
4. __BATCH_RULE__
5. Close out: the last step is NOT exempt — before writing the final answer, mark ALL
   remaining finished steps in one xpcomplete_agent_plan_items call. Its response IS the
   confirmation — do NOT call xpget_agent_plan afterwards to double-check. Delivering a
   result with any incomplete plan item is a FAILED run.

Rules:
- Need the user's input to proceed? STOP: write the question as your FINAL answer and
  end the run — do not keep calling tools or editing the plan while a question is
  pending. The user's reply starts the next run, which resumes the plan.
- A mid-run <user_message> that changes scope: reshape the plan with the fewest calls
  needed (delete/add/update), then get straight back to executing real steps.
- __UUID_RULE__
- Do NOT let completed-but-unmarked steps reach the final answer — sweep them into the
  boundary xpcomplete_agent_plan_items call before finishing (see 4).
- One plan-tool call per turn (they all mutate the same plan document). Non-plan
  tools may be batched alongside it freely - see <turn_economy>.
- Planning is internal bookkeeping. NEVER expose the plan, task IDs, UUIDs, or tool
  mechanics to the user — not in the final answer, and not in think/analyze title or
  thought (both shown in the UI). A think title is a 2-5 word action label ("Research
  pricing"), not a status line; the thought is brief reasoning; the final answer is a
  natural outcome summary, not a step-by-step.
- New work discovered mid-run: xpadd_new_agent_plan_item ({"title","completed":false}).
  Change/remove a step: xpupdate_agent_plan_item / xpdelete_agent_plan_item (body_params
  with id).
</deep_planning>
""".replace("__BATCH_RULE__", _PLAN_BATCH_RULE).replace(
    "__UUID_RULE__", _PLAN_UUID_RULE
)

# Mandatory deep-planning requirement for tasks that report back to a parent
# agent. The runtime (agent-controller) rejects every non-plan tool call from a
# ``should_update_parent`` execution until a plan has been created AND started, so
# the agent MUST plan first or it trips a 400. Injected alongside
# DEEP_PLANNING_INSTRUCTIONS (which supplies the how) whenever plan tools are present.
PARENT_UPDATE_PLAN_REQUIREMENT = """
<deep_planning_required>
This task reports its result back to a parent agent. The runtime REJECTS every
non-plan tool call until a plan exists and has been started. Before ANY other tool
call you MUST: (1) xpcreate_agent_plan, then (2) xpstart_execution_plan. Skipping
this fails the run with "Deep planning is required before making any tool calls".
</deep_planning_required>
"""

# Guidance for a plan that ALREADY exists and is started + enforced (e.g. an
# agent-gateway child whose plan was pre-seeded by the gateway). The agent must NOT
# create or start a plan — both fail — it executes the existing steps and marks each
# complete. Without this, the create-first DEEP_PLANNING_INSTRUCTIONS leave the agent
# unsure how to satisfy enforcement, so seeded steps stay incomplete and the run loops.
SEEDED_PLAN_INSTRUCTIONS = (
    """
<deep_planning>
A plan for this task ALREADY EXISTS and is STARTED (enforcement is ON) — see
"__PLAN_LABEL__" below. Do NOT call xpcreate_agent_plan or
xpstart_execution_plan; both will fail. Your job is to EXECUTE the existing steps and
mark each one complete.

Per step:
- The step UUIDs are listed in "__PLAN_LABEL__" (xpget_agent_plan shows live
  completion status). If you are RESUMING mid-plan and unsure which steps are already
  done, call xpget_agent_plan ONCE before doing work — never re-execute a completed step.
- Do the work, setting header toolcallplantaskid to the CURRENT step's full UUID on
  EVERY non-plan tool call, updating it the moment you move to a new step.
- __BATCH_RULE__
- The last step is NOT exempt: before writing the final answer, mark ALL remaining
  finished steps in one xpcomplete_agent_plan_items call. Its response IS the
  confirmation — do NOT call xpget_agent_plan afterwards to double-check. Delivering a
  result with ANY incomplete plan item is a FAILED run.

Rules:
- The seeded steps are your starting plan; if the real work needs a different shape use
  xpadd_new_agent_plan_item / xpupdate_agent_plan_item / xpdelete_agent_plan_item — but
  EVERY remaining step must end marked complete.
- Need the user's input to proceed? STOP: write the question as your FINAL answer and
  end the run — do not keep calling tools or editing the plan while a question is
  pending.
- __UUID_RULE__
- One plan-tool call per turn (they all mutate the same plan document). Non-plan
  tools may be batched alongside it freely - see <turn_economy>.
- Planning is internal bookkeeping. NEVER expose the plan, task IDs, UUIDs, or tool
  mechanics to the user (final answer or think/analyze title/thought).
</deep_planning>
""".replace("__PLAN_LABEL__", PLAN_BLOCK_LABEL)
    .replace("__BATCH_RULE__", _PLAN_BATCH_RULE)
    .replace("__UUID_RULE__", _PLAN_UUID_RULE)
)


def _build_compact_tool():
    """Build the ``xpcompact_context`` agno Function.

    Uses the same ``payload``-wrapped shape as every other xpander tool so the
    LLM sees one consistent argument pattern. The unwrapped shape used to live
    inline here and made the LLM emit sibling-level ``headers`` on regular
    payload-wrapped tools, which then failed pydantic validation.
    """
    from agno.tools.function import Function

    def _entrypoint(payload: Optional[Union[Dict[str, Any], str]] = None) -> str:
        """Schedule compaction; stringified payloads are parsed so a malformed emission never fails the request."""
        if isinstance(payload, str):
            parsed = parse_structured_string(payload)
            payload = parsed if isinstance(parsed, dict) else {}
        focus = (payload or {}).get("focus", "") or ""
        return f"Compaction scheduled with focus: {focus}"

    return Function(
        name="xpcompact_context",
        description=(
            "Compress conversation history to free context space. "
            "ONLY call this when you observe concrete signs of context pressure: "
            "(1) you are seeing many [TRUNCATED OUTPUT] markers in recent tool results, "
            "(2) you just completed a major task phase and are about to start unrelated work, or "
            "(3) the system has already auto-compacted this session once (meaning context is tight). "
            "Do NOT call speculatively or 'just in case'. "
            "Wrap arguments in a `payload` object."
        ),
        parameters={
            "type": "object",
            "properties": {
                "payload": {
                    "type": "object",
                    "properties": {
                        "focus": {
                            "type": "string",
                            "description": "What the compaction summary should focus on preserving. E.g. 'preserve the API signatures, test results, and migration plan'.",
                        },
                        "headers": {
                            "type": "object",
                            "properties": {
                                "toolcallreasoningtitle": {
                                    "type": "string",
                                    "description": 'The concrete action this call performs (max 5 words). If you cannot name one, you are finished: do not make this call — end the turn with your answer. Example: "Compact context for next phase".',
                                },
                                "toolcallreasoningdescription": {
                                    "type": "string",
                                    "description": 'One-sentence markdown summary of the action and goal (max 100 characters). Example: "Free context space after completing research phase."',
                                },
                            },
                            "required": [
                                "toolcallreasoningtitle",
                                "toolcallreasoningdescription",
                            ],
                        },
                    },
                    "required": ["headers"],
                },
            },
            "required": ["payload"],
        },
        entrypoint=_entrypoint,
    )


_TOOLCALL_HEADER_KEYS = frozenset(
    {
        "toolcallreasoningtitle",
        "toolcallreasoningdescription",
        "toolcallplantaskid",
    }
)


def _stray_header_keys(envelope: Dict[str, Any]) -> List[str]:
    return [k for k in envelope if isinstance(k, str) and k.lower() in _TOOLCALL_HEADER_KEYS]


def _route_header_keys(envelope: Dict[str, Any]) -> None:
    """Move stray ``toolcall*`` keys into ``headers``, where the schema reads them.

    Landing them at the payload's top level parses fine but the values are never
    read: the payload model backfills an empty ``headers`` and the stray copies
    are ignored, which silently drops plan-step attribution on the call.
    """
    stray = _stray_header_keys(envelope)
    if not stray:
        return
    existing = envelope.get("headers")
    headers = dict(existing) if isinstance(existing, dict) else {}
    for key in stray:
        value = envelope.pop(key)
        # Relocate, never discard; a real header value still beats an empty one.
        if not headers.get(key):
            headers[key] = value
    envelope["headers"] = headers


def reenvelope_sibling_args(arguments: Dict[str, Any]) -> bool:
    """Fold sibling keys of ``payload`` into the payload wrapper, in place.

    Repository tools take a single ``payload`` model arg, but LLMs sometimes
    emit args flat (``command='ls', toolcallplantaskid=''``) or float
    ``headers``/``toolcall*`` out as siblings of ``payload``. validate_call
    then fails with unexpected_keyword_argument / missing_argument before the
    payload model's own before-validator can nest/backfill anything. Mutates
    ``arguments`` in place (agno reads ``self.arguments`` directly) and returns
    True when a fold happened. Skipped when ``payload`` is a non-dict value the
    string-coercion step couldn't parse — nothing sane to merge into.

    ``toolcall*`` keys are routed on into ``headers`` rather than left at the
    payload's top level, where nothing reads them.
    """
    payload_val = arguments.get("payload")
    if payload_val is not None and not isinstance(payload_val, dict):
        return False
    envelope = dict(payload_val) if isinstance(payload_val, dict) else {}
    has_siblings = any(k != "payload" for k in arguments)
    if not has_siblings and not _stray_header_keys(envelope):
        return False
    for key in [k for k in list(arguments) if k != "payload"]:
        sibling = arguments.pop(key)
        # A real payload value wins; an empty placeholder ({}/None/"") loses to a non-empty sibling.
        if key not in envelope or (not envelope.get(key) and sibling):
            envelope[key] = sibling
    _route_header_keys(envelope)
    arguments["payload"] = envelope
    return True


def _classify_tool_error(error: Exception) -> str:
    """Classify a tool error as transient, auth, or client.

    Returns:
        str: One of 'transient', 'auth', 'client', or 'unknown'.
    """
    # Argument-shape failures are deterministic: the same args fail identically
    # every attempt. Decide on the exception TYPE before the substring sniffing
    # below, which reads the message - and pydantic echoes the rejected input
    # into it, so a payload carrying "timeout" or "429" would otherwise pick its
    # own retry policy.
    if isinstance(error, (ValidationError, TypeError)):
        return "client"

    error_str = str(error).lower()

    # auth markers BEFORE status sniffing - connectors mislabel auth failures as 500
    if any(
        marker in error_str
        for marker in [
            "permission_denied", "permission denied", "access denied", "accessdenied",
        ]
    ):
        return "auth"

    # Check for HTTP status codes in error messages
    if any(
        code in error_str
        for code in ["timeout", "timed out", "connection reset", "connection refused"]
    ):
        return "transient"
    if any(
        code in error_str
        for code in ["429", "rate limit", "too many requests", "quota exceeded"]
    ):
        return "transient"
    if any(
        code in error_str
        for code in [
            "500",
            "502",
            "503",
            "504",
            "internal server error",
            "bad gateway",
            "service unavailable",
        ]
    ):
        return "transient"
    if any(
        code in error_str
        for code in [
            "401",
            "403",
            "unauthorized",
            "forbidden",
            "authentication",
            "permission denied",
        ]
    ):
        return "auth"
    if any(
        code in error_str
        for code in [
            "400",
            "422",
            "bad request",
            "unprocessable",
            "validation error",
            "invalid",
        ]
    ):
        return "client"

    return "unknown"


# agno wraps MCP failures as a normal ToolResult whose content starts with
# this prefix (agno/utils/mcp.py) instead of raising — the only in-band
# signal that the call failed.
_MCP_ERROR_PREFIXES = ("Error from MCP tool",)


def _result_is_error(result: Any) -> bool:
    """Whether a tool result agno surfaced as success actually carries a failure."""
    try:
        if result is None:
            return False
        if getattr(result, "is_success", None) is False:
            return True
        status_code = getattr(result, "status_code", None)
        if isinstance(status_code, int) and status_code >= 400:
            return True
        content: Any = result
        if hasattr(result, "content"):
            content = result.content
        elif hasattr(result, "result"):
            content = result.result
        if isinstance(content, dict):
            content = content.get("content", "")
        if isinstance(content, str) and any(
            content.lstrip().startswith(p) for p in _MCP_ERROR_PREFIXES
        ):
            return True
    except Exception:
        pass
    return False


def _bump_error_streak(
    streaks: Dict[str, int], function_name: str, errored: bool
) -> int:
    """Update per-tool consecutive-error counts; returns the streak after this outcome (0 on success)."""
    if not errored:
        streaks.pop(function_name, None)
        return 0
    streak = streaks.get(function_name, 0) + 1
    streaks[function_name] = streak
    return streak


def _bump_total_calls(task, function_name: str) -> int:
    """Task-scoped args-agnostic total call count for one tool (0 when no task to pin state on)."""
    if task is None:
        return 0
    counts = getattr(task, "_xp_tool_total_calls", None)
    if not isinstance(counts, dict):
        counts = {}
        try:
            object.__setattr__(task, "_xp_tool_total_calls", counts)
        except Exception:
            return 0
    counts[function_name] = counts.get(function_name, 0) + 1
    return counts[function_name]


def _record_gated_call(task: Any) -> int:
    """Count tool calls rejected by the finalize gate, so a looping agent gets escalated wording."""
    count = getattr(task, "_xp_finalize_gated_calls", 0) + 1
    try:
        object.__setattr__(task, "_xp_finalize_gated_calls", count)
    except Exception:
        pass
    return count


def _premature_finalize_rejection(
    optimizer: Any, function_name: str
) -> Optional[str]:
    """Return the rejection message when xpfinalize_task is called while Finalize-Only Mode is inactive, else None."""
    if function_name != "xpfinalize_task":
        return None
    # Duck-typed: is_finalize_active is getattr-safe for any optimizer shape (or None), and those can never be active.
    if is_finalize_active(optimizer):
        return None
    return FINALIZE_NOT_ACTIVE_REJECTION


_DYNAMIC_DISPATCH_META_TOOL = "xp_execute_tool"


def _effective_tool_identity(function_name: str, arguments: Any) -> Tuple[str, Any]:
    """Resolve the real tool a call targets, for loop detection.

    The dynamic-tools dispatcher ``xp_execute_tool`` runs the real tool inside its
    own callable (bypassing this hook), so guards keyed on the literal meta name
    never see MCP/dynamic loops — the real id lives in ``payload.name``. Unwrap it
    (and ``payload.arguments``) so the identical-args, volume, and error-streak
    guards act on the real tool. Falls back to the raw name/args for every other
    tool. save_output_to_file is intentionally excluded: flipping it is still the
    same external action, so a repeat with the flag toggled stays a repeat.
    """
    if function_name == _DYNAMIC_DISPATCH_META_TOOL and isinstance(arguments, dict):
        payload = arguments.get("payload")
        if isinstance(payload, dict):
            inner = str(payload.get("name") or "").strip()
            if inner:
                return inner, payload.get("arguments") or {}
    return function_name, arguments


_MAX_PROMPT_CACHE_KEY_LEN = 64  # OpenAI Responses/Chat Completions hard limit


def _bounded_prompt_cache_key(raw: str) -> str:
    """Keep an OpenAI prompt_cache_key within the 64-char provider max: pass the raw
    value through when it fits, else a stable 32-char md5 digest (deterministic, so
    cache routing is unchanged)."""
    if len(raw) <= _MAX_PROMPT_CACHE_KEY_LEN:
        return raw
    return hashlib.md5(raw.encode()).hexdigest()


def _bounded_arg_signature(args: dict) -> str:
    """Cheap, collision-resistant signature of tool args for in-memory stuck
    detection. Samples len+head+tail of large string values instead of
    serializing them in full, so a ~1MB resolved argument costs O(1) not O(n).
    Deterministic (sorted keys) so a repeated call produces the same signature."""
    parts = []
    for k in sorted(args):
        v = args[k]
        s = v if isinstance(v, str) else json.dumps(v, sort_keys=True, default=str)
        if len(s) > 2048:
            s = f"{len(s)}:{s[:512]}:{s[-512:]}"
        parts.append(f"{k}={s}")
    return "\x00".join(parts)


_PLAN_CHURN_TOOLS = PLANNING_TOOLS | REASONING_TOOLS

# xp* tools that legitimately repeat with byte-identical args: plan bookkeeping, the
# finalize escape hatch, compaction, and the documented sleep+poll pair. Every OTHER xp
# tool (workspace, live surface, schedule, builtin) goes through the loop guards -
# a blanket `startswith("xp")` skip is what let seven noop calls through in one run.
_REDUNDANCY_EXEMPT_TOOLS = PLANNING_TOOLS | {
    "xpcompact_context",
    "xpfinalize_task",
    "xpsleep_agent_delay",
    "xpget_agent_task_execution_status",
}

# Calls that report state without changing any. Repeating one of these with the same args
# and no state change in between cannot return anything new, so it is refused outright
# rather than merely warned about.
_READ_ONLY_TOOLS = {
    "xpworkspace-file-read",
    "xpworkspace-glob",
    "xpworkspace-grep",
    "xpworkspace-context-retrieve",
    "xpworkspace-secrets-list",
    "xpschedule-list",
    "xplivesurface-open",
    "xplivesurface-get",
    "xplist_sub_agents",
    "xpsearch_agents_by_name_or_skill",
    "xpget_current_task_id",
}

# Writes whose outcome is fully determined by their arguments: making the same one twice
# cannot land differently, so a repeat is blocked like a read. Without this, the
# `has_args and not read-only` early-out below waved through seven identical memory updates.
_IDEMPOTENT_WRITE_TOOLS = {"manage_memory"}


# Reads the finalize-mode gate always permits so the model can gather what it needs to
# compose its final answer. Secrets-list is deliberately excluded - finalize is a
# wind-down state, not a place to enumerate the secret namespace.
_FINALIZE_SAFE_READS = _READ_ONLY_TOOLS - {"xpworkspace-secrets-list"}


def _is_finalize_safe_read(function_name: str, arguments: Any) -> bool:
    """A non-destructive read the finalize-mode gate must never block. Covers the direct
    read-only tools and a dynamic-dispatch (`xp_execute_tool`) whose inner tool is one."""
    if function_name in _FINALIZE_SAFE_READS:
        return True
    if function_name == _DYNAMIC_DISPATCH_META_TOOL:
        inner_name, _ = _effective_tool_identity(function_name, arguments)
        return inner_name in _FINALIZE_SAFE_READS
    return False


def _finalize_safe_read_allowed(task: Any, function_name: str, arguments: Any) -> bool:
    """Safe reads stay open in finalize mode, but only a bounded number of them —
    an unbounded varying-args read loop would defeat the wind-down entirely."""
    if not _is_finalize_safe_read(function_name, arguments):
        return False
    if task is None:
        return True
    reads = (getattr(task, "_xp_finalize_reads", 0) or 0) + 1
    try:
        object.__setattr__(task, "_xp_finalize_reads", reads)
    except Exception:
        return True
    return reads <= FINALIZE_SAFE_READS_CAP

REDUNDANT_CALL_MESSAGE = (
    "Redundant call blocked: '{tool}' already ran with these exact arguments earlier in this "
    "task and nothing has changed since, so it was not run again - the earlier result above is "
    "still current. Never repeat a call just to have something current to show or to confirm "
    "you are finished. If the work is done, answer the user now."
)

# Sandbox bash-guard mirror (agent_sandbox bash_tool.py) - keep in sync;
# refusing here skips the round-trip and the billing event.
_NOOP_BASH_COMMANDS = {
    "",
    ":",
    "true",
    "false",
    "exit",
    "exit 0",
    "clear",
    "pwd",
    "cd",
    "cd .",
    "cd ./",
    "cd ~",
    "whoami",
    "id",
    "hostname",
    "uname",
    "uname -a",
    "date",
    "uptime",
}
_LITERAL_ECHO_RE = re.compile(r"^echo\b[^|<>$`;&*?~\[\]{}!\n]*$")
# Suffixes that change no stdout the model would see; peeled repeatedly so
# `ls -la 2>&1 | cat` and `ls -la` classify and hash identically.
_BASH_COSMETIC_SUFFIXES = (
    re.compile(r"\s*;\s*$"),
    re.compile(r"\s*2>&1\s*$"),
    re.compile(r"\s*\|\s*cat\s*$"),
    re.compile(r"\s*2>\s*/dev/null\s*$"),
)
# A stdout redirect to /dev/null SUPPRESSES output, so it is cosmetic only for the
# noop classifier (`pwd > /dev/null` still reveals nothing) - never for the repeat
# signature, where `ls > /dev/null` and a later informative `ls` must not collide.
_BASH_STDOUT_SUPPRESS_SUFFIX = re.compile(r"\s*1?>\s*/dev/null\s*$")
_BASH_COMMENT_RE = re.compile(r"\s+#[^'\"`]*$")
# Whole commands whose output the model already knows byte-for-byte before running them.
_NOOP_BASH_PATTERNS = (
    re.compile(r"^sleep\s+[\d.]+$"),
    re.compile(r"^printf\b[^|<>$`;&]*$"),
    # reads of /dev/null / guaranteed-empty input: `wc -l < /dev/null`, `cat /dev/null`
    re.compile(r"^(?:wc|cat|head|tail|md5(?:sum)?|sha\d+sum|sort|uniq)\b[^|;&]*<\s*/dev/null$"),
    re.compile(r"^(?:wc|cat|head|tail)(?:\s+-[a-zA-Z]+)*\s+/dev/null$"),
)
# Byte-identical to the sandbox refusal so _NO_PROGRESS_MARKERS matches both origins.
BASH_NOOP_REFUSAL = (
    "Refused: this command reads nothing and changes nothing, so it cannot advance the "
    "task. If the work is done, write your answer to the user instead of calling "
    "another tool."
)


def _normalize_bash_command(command: str, *, for_noop_check: bool = False) -> str:
    """Strip decorations that cannot change what the model learns from the command."""
    stripped = _BASH_COMMENT_RE.sub("", (command or "").strip())
    stripped = re.sub(r"\s+", " ", stripped)
    previous = None
    while previous != stripped:
        previous = stripped
        for suffix in _BASH_COSMETIC_SUFFIXES:
            stripped = suffix.sub("", stripped).strip()
        if for_noop_check:
            stripped = _BASH_STDOUT_SUPPRESS_SUFFIX.sub("", stripped).strip()
    return stripped


def _is_noop_bash_command(command: str) -> bool:
    """True for commands that read nothing and change nothing (sandbox-guard mirror)."""
    stripped = _normalize_bash_command(command, for_noop_check=True)
    lowered = stripped.lower()
    if lowered in _NOOP_BASH_COMMANDS:
        return True
    if _LITERAL_ECHO_RE.match(stripped):
        return True
    return any(pattern.match(lowered) for pattern in _NOOP_BASH_PATTERNS)


# Pure readers/filters only - sed/awk/find/xargs/env/sort can write or exec, and
# misclassifying a mutation as a read would hide its state change from the ledger.
_BASH_READ_ONLY_BINARIES = frozenset({
    "ls", "cat", "head", "tail", "wc", "stat", "file", "grep", "egrep", "fgrep",
    "rg", "du", "df", "tree", "pwd", "which", "type", "printenv", "date", "whoami",
    "id", "uname", "hostname", "md5", "md5sum", "shasum", "sha256sum", "diff",
    "cmp", "jq", "yq", "uniq", "cut", "tr", "basename", "dirname", "realpath",
    "readlink", "echo", "printf",
})


def _bash_command_is_read_only(normalized: str) -> bool:
    """True when re-running the command can only differ if workspace state changed."""
    if not normalized or ">" in normalized:
        return False
    # `||` before `|` - the single-pipe alternative would split `a || b` into empty chunks
    for chunk in re.split(r"\|\||&&|\||;", normalized):
        first = chunk.strip().split(" ", 1)[0].strip()
        if not first or first not in _BASH_READ_ONLY_BINARIES:
            return False
    return True


# The title is the model's own confession; the refusal never echoes a matched token.
_FILLER_TITLE_RE = re.compile(
    r"^(?:"
    r"no[\s_-]?op\w*|placeholder\w*|filler|keepalive|dummy(?:[\s_-]+call)?|idle|"
    r"padding|stall(?:ing)?|wrap[\s_-]?up\w*|sanity[\s_-]?check|"
    r"final(?:ize|ise)?(?:[\s_-]+(?:answer|task|check|prep|step))?(?:[\s_-]+prep)?|"
    r"confirm(?:ation)?(?:[\s_-]+(?:done|completion|finished))?|"
    r"verify[\s_-]+(?:done|complete(?:d|ion)?)|done|finish(?:ed|ing)?(?:[\s_-]+up)?|"
    r"clean[\s_-]?up|no[\s_-]+action|nothing(?:[\s_-]+to[\s_-]+do)?|test(?:[\s_-]+call)?"
    r")$",
    re.IGNORECASE,
)

FILLER_TITLE_REFUSAL = (
    "Refused: this call's own reasoning title says it performs no real work, so it was "
    "not run and nothing was recorded. If the work is done, write your final answer to "
    "the user now - no tool call is needed to end a task."
)

# Degenerate titles ("x", "n/a", "ok") carry no action; 3-letter words ("run") stay legal.
_DEGENERATE_TITLE_RE = re.compile(r"[a-z]{1,2}|n/a|tbd|nil|\.+")
# Filler only when EVERY non-stopword token matches - one real word keeps the call.
_FILLER_TOKEN_RE = re.compile(
    r"no[-_]?op\w*|placeholder\w*|filler|keepalive|dummy|idle|padding|stall(?:ing)?|"
    r"wrap(?:up)?\w*|sanity|check|final(?:ize|ise)?|confirm(?:ation)?|done|verify|"
    r"finish(?:ed|ing)?|clean(?:up)?|action|nothing|test|call|skip(?:ping)?|"
    r"stop(?:ping|ped)?|answer|prep|step|task|complete(?:d|ion)?|irrelevant|"
    r"unrelated|probe",
    re.IGNORECASE,
)
_TITLE_STOPWORDS = frozenset(
    {"the", "a", "an", "of", "for", "to", "in", "on", "at", "with", "up", "now", "and"}
)


def _extract_reasoning_title(arguments: Any) -> Optional[str]:
    """Best-effort read of toolcallreasoningtitle from the shapes the LLM emits."""
    if not isinstance(arguments, dict):
        return None
    candidates = [arguments]
    for container_key in ("payload", "body_params"):
        container = arguments.get(container_key)
        if isinstance(container, dict):
            candidates.append(container)
            nested = container.get("body_params")
            if isinstance(nested, dict):
                candidates.append(nested)
    for candidate in candidates:
        headers = candidate.get("headers")
        if isinstance(headers, dict):
            title = headers.get("toolcallreasoningtitle")
            if isinstance(title, str) and title.strip():
                return title
        title = candidate.get("toolcallreasoningtitle")
        if isinstance(title, str) and title.strip():
            return title
    return None


def _is_filler_title(title: Optional[str]) -> bool:
    """True when the model's own reasoning title declares the call does nothing."""
    if not title:
        return False
    stripped = title.strip()
    if _FILLER_TITLE_RE.match(stripped):
        return True
    if _DEGENERATE_TITLE_RE.fullmatch(stripped.lower()):
        return True
    # hyphens stay inside tokens ("no-op" must not split); 1-char fragments carry no signal
    tokens = [
        t.replace("-", "")
        for t in re.split(r"[\s_/]+", stripped.lower())
    ]
    tokens = [t for t in tokens if len(t) > 1 and t not in _TITLE_STOPWORDS]
    return bool(tokens) and all(_FILLER_TOKEN_RE.fullmatch(t) for t in tokens)


class ToolSchemaValidationError(RuntimeError):
    """A tool-argument schema failure re-raised with repair guidance attached."""


VALIDATION_ERROR_GUIDANCE = (
    "\n\nFix the arguments to match the tool's schema exactly - payload must be a "
    "JSON object literal, never a quoted/stringified string - and retry once with "
    "the corrected shape. If the work is already complete, write your final answer "
    "to the user now instead of making more tool calls."
)


# A live surface renders inline the moment xplivesurface-create succeeds; sharing the
# manifest file afterwards delivers nothing and only manufactures a wrap-up step.
LIVESURFACE_SHARE_REFUSAL = (
    "Already delivered: a live surface renders inline in the conversation the moment it "
    "is created, so its manifest file needs no file-share link and nothing was shared. "
    "If the user asked to share it with their organization and an xplivesurface-share "
    "tool is in your toolset, call that with the surface id; otherwise the deliverable "
    "is complete - answer the user now and refer to the surface you already published."
)


IDENTICAL_RESULT_NOTE = (
    "Note: this call returned byte-identical output to an earlier call in this task - "
    "it added nothing new. Work with the results you already have; if the work is done, "
    "answer the user now."
)


def _record_identical_result(task: Any, tool_name: str, result: Any) -> bool:
    """True when this tool already returned byte-identical output earlier in the task.

    Catches filler shapes no static command list predicts: whatever the call was, if
    its output is something the task already saw from the same tool, it moved nothing.
    Short outputs are skipped - tiny acks ("OK", "{}") legitimately recur.
    """
    if task is None or tool_name in _REDUNDANCY_EXEMPT_TOOLS:
        return False
    text = _no_progress_text(result)
    if not text or len(text) < 24:
        return False
    digest = hashlib.md5(f"{tool_name}:{text}".encode()).hexdigest()
    seen = getattr(task, "_xp_result_hashes", None)
    if not isinstance(seen, set):
        seen = set()
        try:
            object.__setattr__(task, "_xp_result_hashes", seen)
        except Exception:
            return False
    if digest in seen:
        return True
    seen.add(digest)
    return False


def _extract_share_path(arguments: Any) -> Optional[str]:
    """Best-effort read of xpworkspace-file-share's path argument."""
    if not isinstance(arguments, dict):
        return None
    container = arguments.get("payload") if isinstance(arguments.get("payload"), dict) else arguments
    body = container.get("body_params") if isinstance(container.get("body_params"), dict) else container
    path = body.get("path")
    return path if isinstance(path, str) else None


def _coerce_bash_command(arguments: Any) -> Optional[str]:
    """Return xpworkspace-bash's command string, normalizing scalars in place.

    A model that was just refused for a placeholder sometimes emits the shell noop
    ``true`` as an unquoted JSON boolean; pydantic lax mode does not coerce bool->str,
    so the call dies with a validation error instead of the refusal that teaches it to
    stop. Normalize bool/int/float to their shell spelling before validation ever runs.
    """
    if not isinstance(arguments, dict):
        return None
    payload_obj = arguments.get("payload")
    container = payload_obj if isinstance(payload_obj, dict) else arguments
    body_obj = container.get("body_params")
    body = body_obj if isinstance(body_obj, dict) else container
    if not isinstance(body, dict) or "command" not in body:
        return None
    command = body.get("command")
    if isinstance(command, bool):
        command = "true" if command else "false"
        body["command"] = command
    elif isinstance(command, (int, float)):
        command = str(command)
        body["command"] = command
    return command if isinstance(command, str) else None


# A call that was refused, blocked, or changed nothing is not progress. A few in a row
# means the model has run out of work and is filling turns - the tail of the runs this
# fixes was noop bash, a blocked memory write, noop bash again. Only genuine refused-noop
# RESULTS advance this (raised errors feed the error-streak breaker instead). 3, not 2:
# finalize locks out real follow-up work, so two incidental refusals must not trip it.
NO_PROGRESS_FINALIZE_AT = 3
NO_PROGRESS_MESSAGE = (
    "You have now made {n} tool calls in a row that changed nothing - refused, blocked, or "
    "already done. There is no further tool work to do. Write your answer to the user now."
)
# Prefixes of every result that means "this call advanced nothing". Kept as text because the
# refusals come back as ordinary tool output from three different places (the workspace, the
# redundancy guard here, and the memory tool).
_NO_PROGRESS_MARKERS = (
    "Refused: this command reads nothing and changes nothing",
    "Refused: this call's own reasoning title",
    "Redundant call blocked:",
    "Already delivered: a live surface renders inline",
    "No memory was changed",
    "Not written: this task has already made",
    "Already known - not saved again",
    "Tool call rejected: the arguments arrived EMPTY",
    "Rejected: finalize-only mode is NOT active",
    "Tool disabled:",
    "Org-wide sharing is turned off for this agent",
)


def _no_progress_text(value: Any, depth: int = 0) -> str:
    """Flatten the shapes a tool result arrives in far enough to read its message.

    A workspace refusal is a dict under ``ToolInvocationResult.result``; a memory refusal
    is a bare string; agno results carry ``.content``. Bounded depth so a large nested
    payload cannot turn this into a deep walk on every single call.
    """
    if depth > 2:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(_no_progress_text(v, depth + 1) for v in value.values())
    for attr in ("result", "content", "stderr"):
        inner = getattr(value, attr, None)
        if inner is not None and inner is not value:
            text = _no_progress_text(inner, depth + 1)
            if text:
                return text
    return ""


def _looks_like_no_progress(result: Any) -> bool:
    """True when a tool result says, in any of its wordings, that nothing happened."""
    text = _no_progress_text(result)
    return any(marker in text for marker in _NO_PROGRESS_MARKERS)


# A single runaway/broken tool is disabled, not the whole run; only this many
# distinct disabled tools (a genuine multi-tool runaway) escalate to finalize.
DISABLED_TOOLS_FINALIZE_AT = 3
DISABLED_TOOL_MESSAGE = (
    "Tool disabled: '{tool}' has been called {calls} times this task - that is "
    "pagination/retry, not progress - and it will not run again this task. Work with "
    "the data you already have or use a different tool. Any REQUIRED final step (a "
    "mandated write/save) must still run via its own tool, or be reported as NOT "
    "done - never claim or imply it happened."
)
DISABLED_TOOL_REPEAT_MESSAGE = (
    "Tool disabled: '{tool}' is disabled for the rest of this task. Do not call it "
    "again in any form. Use a different tool or answer with what you have."
)


def _report_blocked_call(task: Any, effective_name: str, message: str) -> None:
    """Fire-and-forget activity pair for a refused call - gated/aborted calls previously
    emitted NO events, so a run stuck behind the guards looked like minutes of silence."""
    if task is None or should_skip_tool_report(effective_name):
        return

    async def _pair() -> None:
        # one coroutine so the result can never land before its request
        rid = str(uuid.uuid4())
        await report_tool_call_request(
            task, rid, effective_name, tool_name=effective_name,
            payload={"blocked": True},
        )
        await report_tool_call_result(
            task, rid, effective_name, message, is_error=True,
            tool_name=effective_name,
        )

    try:
        _spawn_bg(_pair())
    except Exception:
        pass


def _disable_tool(task: Any, effective_name: str) -> Set[str]:
    """Add a tool to the task-scoped disabled set; returns the set. Platform (xp*) tools
    are never disabled - that could take out xpfinalize_task or the finalize-safe reads
    and deadlock the run's own exit path."""
    if effective_name.startswith("xp"):
        disabled = getattr(task, "_xp_disabled_tools", None) if task is not None else None
        return disabled if isinstance(disabled, set) else set()
    if task is None:
        return {effective_name}
    disabled = getattr(task, "_xp_disabled_tools", None)
    if not isinstance(disabled, set):
        disabled = set()
        try:
            object.__setattr__(task, "_xp_disabled_tools", disabled)
        except Exception:
            return {effective_name}
    disabled.add(effective_name)
    return disabled


def _is_tool_disabled(task: Any, effective_name: str) -> bool:
    """True when this tool was disabled earlier in the run (volume/error caps)."""
    disabled = getattr(task, "_xp_disabled_tools", None) if task is not None else None
    return isinstance(disabled, set) and effective_name in disabled


# Platform-default hard ceiling on tool calls per run; an explicit positive
# agno_settings.tool_call_limit overrides it, 0/None mean "use this default".
# Sized for marathon runs - agno refuses over-limit calls gracefully but
# refuses ALL of them, including xpfinalize_task, so headroom beats tightness.
DEFAULT_TOOL_CALL_LIMIT = TOOL_CALL_LIMIT_DEFAULT

# Plan-complete grace budget: the model cannot see plan completion (the prompt's plan
# block omits flags for cache stability), so a finished dp run loops on xpget_agent_plan
# + noop bash hunting for a finish step - detect completion from the plan-tool results
# the hook already sees, tell it in-band, allow a few wrap-up reads, then force finalize.
PLAN_COMPLETE_GRACE_CALLS = 2
PLAN_COMPLETE_NOTE = (
    "PLAN COMPLETE: all {total} plan steps are done. Compose your final answer NOW from "
    "what you already have. Do not call plan or confirmation tools again - you have at "
    "most {grace} more tool calls for genuinely missing values, then you must answer."
)
PLAN_COMPLETE_COUNTDOWN = (
    "PLAN COMPLETE: the plan finished {n} tool calls ago (budget {grace}). Stop gathering - "
    "answer the user in your next message."
)
PLAN_COMPLETE_STOP = (
    "Done - the plan is fully complete and the post-plan call budget is spent. No further tool "
    "calls will run. Your next message MUST be plain text with your final answer to the "
    "user, based on the work already done. Do NOT call any more tools."
)
_PLAN_REOPEN_TOOLS = frozenset({
    "xpcreate_agent_plan",
    "xpadd_new_agent_plan_item",
    "xpupdate_agent_plan_item",
    "xpdelete_agent_plan_item",
})


def _plan_payload_dict(result: Any, depth: int = 0) -> Optional[dict]:
    """Best-effort dict view of a plan-tool result (dict, JSON string, or nested in .result/.content)."""
    if depth > 2 or result is None:
        return None
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        s = result.strip()
        if s.startswith("{"):
            try:
                parsed = json.loads(s)
                return parsed if isinstance(parsed, dict) else None
            except Exception:
                return None
        return None
    for attr in ("result", "content"):
        inner = getattr(result, attr, None)
        if inner is not None and inner is not result:
            found = _plan_payload_dict(inner, depth + 1)
            if found is not None:
                return found
    return None


def _detect_plan_complete(effective_name: str, result: Any) -> Optional[int]:
    """Total step count when this plan-tool result shows the whole plan done, else None."""
    if effective_name not in ("xpget_agent_plan", "xpcomplete_agent_plan_items"):
        return None
    payload = _plan_payload_dict(result)
    if not payload:
        return None
    if effective_name == "xpcomplete_agent_plan_items":
        # the platform annotates the completing call (plan_complete/total_tasks); older
        # backends without the fields simply never match here - xpget still covers them
        if payload.get("plan_complete") is True:
            total = payload.get("total_tasks")
            return int(total) if isinstance(total, int) and total > 0 else 1
        return None
    tasks = payload.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return None
    if payload.get("enabled") is False:
        return None
    if all(isinstance(t, dict) and t.get("completed") for t in tasks):
        return len(tasks)
    return None


def _track_plan_complete(task: Any, effective_name: str, result: Any, result_is_error: bool = False) -> str:
    """Post-result bookkeeping: detect completion (note appended into the result), clear on reopen."""
    if task is None:
        return ""
    if effective_name in _PLAN_REOPEN_TOOLS:
        # scope legitimately grew/changed - never punish it; xpget re-detects if still done.
        # a FAILED reopen changed nothing, so it must not reset the budget either
        if not result_is_error:
            _clear_plan_complete(task)
        return ""
    if getattr(task, "_xp_plan_complete_total", None):
        return ""
    total = _detect_plan_complete(effective_name, result)
    if total is None:
        return ""
    try:
        object.__setattr__(task, "_xp_plan_complete_total", total)
        object.__setattr__(task, "_xp_plan_complete_calls", 0)
    except Exception:
        return ""
    return PLAN_COMPLETE_NOTE.format(total=total, grace=PLAN_COMPLETE_GRACE_CALLS)


def _clear_plan_complete(task: Any) -> None:
    """Drop the plan-complete state (plan reopened or run reset)."""
    for attr in ("_xp_plan_complete_total", "_xp_plan_complete_calls"):
        try:
            object.__setattr__(task, attr, None)
        except Exception:
            pass


def _bump_plan_complete_calls(task: Any) -> int:
    """Count a tool call made after the plan completed; 0 when the state is not active."""
    if task is None or not getattr(task, "_xp_plan_complete_total", None):
        return 0
    calls = (getattr(task, "_xp_plan_complete_calls", 0) or 0) + 1
    try:
        object.__setattr__(task, "_xp_plan_complete_calls", calls)
    except Exception:
        return 0
    return calls


def _bump_no_progress_streak(task, result: Any, force: bool = False) -> int:
    """Consecutive calls that changed nothing; any real result resets the count.

    ``force`` counts a futile call whose text carries no marker - a deterministic
    argument-shape failure raised as an exception. Without it, a run alternating
    refusals and validation errors split its streak across two counters and never
    tripped either cap.
    """
    if task is None:
        return 0
    streak = (
        (getattr(task, "_xp_no_progress_streak", 0) + 1)
        if (force or _looks_like_no_progress(result))
        else 0
    )
    try:
        object.__setattr__(task, "_xp_no_progress_streak", streak)
    except Exception:
        return 0
    return streak


def _signature_args(args: Any) -> Any:
    """Args with the cosmetic ``toolcall*`` reasoning headers dropped.

    Those are activity-log labels the model writes freely, so two byte-identical calls
    titled "noop" and "noop2" hash differently and evade every repeat guard.
    """
    if isinstance(args, dict):
        out = {}
        for key, value in args.items():
            if isinstance(key, str) and key.startswith("toolcall"):
                continue
            cleaned = _signature_args(value)
            if key == "headers" and isinstance(cleaned, dict) and not cleaned:
                continue
            out[key] = cleaned
        return out
    if isinstance(args, list):
        return [_signature_args(v) for v in args]
    return args


def _has_meaningful_args(args: Any) -> bool:
    """True when something survives that could vary the answer.

    Zero-input xpander tools still arrive wrapped as ``{"payload": {}}``, so a non-empty
    signature string is not evidence of real arguments.
    """
    if isinstance(args, dict):
        return any(_has_meaningful_args(v) for v in args.values())
    if isinstance(args, (list, tuple, set)):
        return any(_has_meaningful_args(v) for v in args)
    if args is None:
        return False
    if isinstance(args, str):
        return bool(args.strip())
    return True


def _bump_mutation_counter(
    task: Any, function_name: str, *, is_read_only: bool = False
) -> int:
    """Count state-changing calls, so a read can tell whether the world moved under it."""
    counter = getattr(task, "_xp_mutation_counter", 0) if task is not None else 0
    if not is_read_only and function_name not in _READ_ONLY_TOOLS:
        counter += 1
        if task is not None:
            try:
                object.__setattr__(task, "_xp_mutation_counter", counter)
            except Exception:
                pass
    return counter


def _is_redundant_call(
    task: Any,
    signature: str,
    function_name: str,
    has_args: bool,
    *,
    treat_read_only: bool = False,
) -> bool:
    """True when this exact call already ran and could not possibly answer differently."""
    if task is None or function_name in _REDUNDANCY_EXEMPT_TOOLS:
        return False
    if (
        has_args
        and not treat_read_only
        and function_name not in _READ_ONLY_TOOLS
        and function_name not in _IDEMPOTENT_WRITE_TOOLS
    ):
        return False
    ledger = getattr(task, "_xp_call_ledger", None)
    if not isinstance(ledger, dict):
        ledger = {}
        try:
            object.__setattr__(task, "_xp_call_ledger", ledger)
        except Exception:
            return False
    seen_at = ledger.get(signature)
    now = getattr(task, "_xp_mutation_counter", 0)
    ledger[signature] = now
    if seen_at is None:
        return False
    # A tool taking no arguments reports a constant, so intervening work is irrelevant -
    # this is the shape that produced seven "noop" calls spread across a single run.
    # An idempotent write is the same story: writing the identical thing again lands the
    # identical way no matter what happened in between (and it bumps the mutation counter
    # itself, so a state-change test would never fire for it).
    # A read WITH arguments only goes stale when something actually changed state.
    if not has_args or function_name in _IDEMPOTENT_WRITE_TOOLS:
        return True
    return seen_at == now


def _bump_plan_churn(task, function_name: str) -> int:
    """Consecutive planning/reasoning calls with no real tool in between; any other tool resets."""
    if task is None:
        return 0
    streak = (
        (getattr(task, "_xp_plan_churn_streak", 0) + 1)
        if function_name in _PLAN_CHURN_TOOLS
        else 0
    )
    try:
        object.__setattr__(task, "_xp_plan_churn_streak", streak)
    except Exception:
        return 0
    return streak


# Poll pair repeats legitimately after a write; control tools advance nothing.
# Dynamic-dispatch discovery is plumbing: a discover->inspect->execute cycle must
# cost one streak slot (the inner action), not three.
_WRAPUP_EXEMPT_TOOLS = frozenset(
    {
        "xpsleep_agent_delay",
        "xpget_agent_task_execution_status",
        "xpcompact_context",
        "xpfinalize_task",
        "xp_list_tools",
        "xp_search_tools",
        "xp_get_tool",
    }
)
# Wrap-up-streak-only mutation test; delivering (send/share/publish/upload) IS mutating.
_MUTATING_NAME_RE = re.compile(
    r"insert|write|create|update|patch|delete|send|share|publish|upload", re.I
)


def _is_read_class_tool(eff_name: str) -> bool:
    """Read-class tools get volume warnings but are never disabled."""
    return eff_name != "manage_memory" and _MUTATING_NAME_RE.search(eff_name) is None


def _bump_wrapup_streak(
    task: Any, eff_name: str, result_is_error: bool, bash_read_only: bool
) -> int:
    """Successful non-mutating calls since the run's last mutation; mutations reset."""
    if task is None or result_is_error:
        return 0
    if eff_name in _WRAPUP_EXEMPT_TOOLS or eff_name in _PLAN_CHURN_TOOLS:
        return 0
    if eff_name == "xpworkspace-bash":
        is_mutation = not bash_read_only
    else:
        # manage_memory is an idempotent write elsewhere in the SDK; stay consistent
        is_mutation = (
            eff_name == "manage_memory"
            or _MUTATING_NAME_RE.search(eff_name) is not None
        )
    if is_mutation:
        try:
            object.__setattr__(task, "_xp_write_seen", True)
            object.__setattr__(task, "_xp_wrapup_streak", 0)
        except Exception:
            pass
        return 0
    if not getattr(task, "_xp_write_seen", False):
        return 0
    streak = (getattr(task, "_xp_wrapup_streak", 0) or 0) + 1
    try:
        object.__setattr__(task, "_xp_wrapup_streak", streak)
    except Exception:
        return 0
    return streak


# Advisory on a SUCCESS result (not a refusal - must never join _NO_PROGRESS_MARKERS).
WRAPUP_NUDGE = (
    "Note: the last several calls only read state that was already established. If the "
    "work is complete, write your final answer to the user now; if real steps remain, "
    "take the next one."
)


def _reset_wrapup_streak(task: Any) -> None:
    """A delivered steer reopens the task's scope, so the wrap-up streak restarts."""
    if task is None:
        return
    try:
        object.__setattr__(task, "_xp_wrapup_streak", 0)
    except Exception:
        pass


def _reset_plan_churn(task: Any) -> None:
    """A delivered steer legitimizes replanning, so the churn streak restarts."""
    if task is None:
        return
    try:
        object.__setattr__(task, "_xp_plan_churn_streak", 0)
    except Exception:
        pass


_QUERY_ARG_KEYS = ("query", "q", "search_term", "search_query")


def _extract_query_arg(arguments: Any) -> Optional[str]:
    """Best-effort read of a search-style query arg from the shapes the LLM emits."""
    if not isinstance(arguments, dict):
        return None
    candidates = [arguments]
    for container_key in ("payload", "body_params"):
        container = arguments.get(container_key)
        if isinstance(container, dict):
            candidates.append(container)
            nested = container.get("body_params")
            if isinstance(nested, dict):
                candidates.append(nested)
    for candidate in candidates:
        for key in _QUERY_ARG_KEYS:
            value = candidate.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return None


def _log_junk_query(task: Any, eff_name: str, arguments: Any) -> None:
    """Telemetry only (Coralogix e2m counts the marker) - never blocks the call."""
    if task is None or not getattr(task, "_xp_write_seen", False):
        return
    query = _extract_query_arg(arguments)
    if query is None:
        return
    if len(query.split()) <= 1 and len(query) <= 16:
        logger.warning(
            f"[junk-args] single-token query on '{eff_name}' after the run's "
            f"mutations for task {getattr(task, 'id', '?')}"
        )


def _schema_satisfiable_by_empty(prop_schema: Any) -> bool:
    """True when ``{}`` (or omission) validates against *prop_schema*.

    Zero-input xpander tools are not schema-level zero-arg: the agno wrapper
    marks ``payload`` required, and raw backend schemas mark the
    body/query/path containers required even when they are empty objects.
    Those params are satisfiable by an empty value and must not count as
    "genuinely required" for the truncated-call guard. ``toolcall*`` header
    fields are cosmetic activity-log metadata and never count (PRO-1928 —
    same rule as build_model_from_schema's headers relaxation).
    """
    if not isinstance(prop_schema, dict):
        return False
    if "default" in prop_schema:
        return True
    if prop_schema.get("type") != "object":
        return False
    properties = prop_schema.get("properties")
    properties = properties if isinstance(properties, dict) else {}
    required = prop_schema.get("required")
    required = required if isinstance(required, list) else []
    for name in required:
        if isinstance(name, str) and name.lower().startswith("toolcall"):
            continue
        if not (
            isinstance(name, str) and _schema_satisfiable_by_empty(properties.get(name))
        ):
            return False
    return True


def _effective_required(params: dict) -> List[str]:
    """Required-parameter names from a JSON-schema dict, excluding params an
    empty value would satisfy (empty containers, defaults, toolcall* headers)."""
    required = params.get("required")
    if not isinstance(required, list):
        return []
    properties = params.get("properties")
    properties = properties if isinstance(properties, dict) else {}
    return [
        r
        for r in required
        if isinstance(r, str) and not _schema_satisfiable_by_empty(properties.get(r))
    ]


def _get_params_schema(
    tools: Optional[List[Any]],
    function_name: str,
    matched_tool: Any = None,
) -> Optional[dict]:
    """Parameters JSON-schema dict for *function_name* from the registered
    agno tools (Function/Toolkit) or the xpander tools repo; None if not
    found or on any error."""
    try:
        for t in tools or []:
            params = None
            if getattr(t, "name", None) == function_name:
                params = getattr(t, "parameters", None)
            else:
                fns = getattr(t, "functions", None)
                if isinstance(fns, dict) and function_name in fns:
                    params = getattr(fns[function_name], "parameters", None)
            if isinstance(params, dict):
                return params
        if matched_tool is not None:
            params = getattr(matched_tool, "parameters", None)
            if isinstance(params, dict):
                return params
    except Exception:
        pass
    return None


def _get_required_params(
    tools: Optional[List[Any]],
    function_name: str,
    matched_tool: Any = None,
) -> List[str]:
    """Genuinely-required parameter names for *function_name*; fails open
    ([]). Params satisfiable by an empty value are excluded — see
    _schema_satisfiable_by_empty."""
    params = _get_params_schema(tools, function_name, matched_tool)
    if params is None:
        return []
    try:
        return _effective_required(params)
    except Exception:
        return []


async def _invoke_with_transient_retry(
    function_name: str,
    function_call: Callable,
    arguments: Dict[str, Any],
    max_retries: int = 2,
) -> Any:
    """Invoke a tool function with automatic retry for transient errors.

    - Transient errors (timeout, 5xx, rate limit): Retry up to max_retries times with backoff.
    - Auth errors (401, 403): Raise immediately.
    - Client errors (400, 422): Raise immediately.

    Args:
        function_name: Name of the tool function.
        function_call: The callable to invoke.
        arguments: Arguments to pass to the function.
        max_retries: Maximum number of retries for transient errors.

    Returns:
        The result from the function call.
    """
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            if asyncio.iscoroutinefunction(function_call):
                return await function_call(**arguments)
            else:
                return function_call(**arguments)
        except Exception as e:
            last_error = e
            error_type = _classify_tool_error(e)

            if error_type == "transient" and attempt < max_retries:
                backoff = (attempt + 1) * 1.5  # 1.5s, 3s
                logger.warning(
                    f"Transient error on tool '{function_name}' (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                    f"Retrying in {backoff}s..."
                )
                await asyncio.sleep(backoff)
                continue

            # Non-transient or exhausted retries — raise
            raise

    # Should never reach here, but just in case
    raise last_error


async def build_agent_args(
    xpander_agent: Agent,
    task: Optional[Task] = None,
    override: Optional[Dict[str, Any]] = None,
    tools: Optional[List[Callable]] = None,
    is_async: Optional[bool] = True,
    auth_events_callback: Optional[Callable] = None,
    is_member: bool = False,
) -> Dict[str, Any]:
    # Await the org-headers fetch here (60s-cached) instead of blocking on a
    # run_sync thread hop inside the sync _load_llm_model on every dispatch.
    org_default_llm_headers = await _aget_org_default_llm_headers(xpander_agent)
    model = _load_llm_model(
        agent=xpander_agent,
        override=override,
        task=task,
        org_default_llm_headers=org_default_llm_headers,
    )
    # When workspace tools are disabled for this agent, suppress all
    # workspace-referencing instruction injection and workspace I/O. The
    # context optimizer is still configured (L2 compaction keeps running);
    # it reads this same flag off the agent to skip its workspace writes.
    workspace_enabled = bool(getattr(xpander_agent, "workspace_tools_enabled", True))
    if not workspace_enabled:
        logger.info(
            f"[workspace] disabled for agent {xpander_agent.id} "
            f"(workspace_tools_enabled=False): skipping workspace instructions "
            f"and all workspace I/O (L1 offload, session backup, ledger persistence)"
        )
    args: Dict[str, Any] = {
        "id": xpander_agent.id,
        "store_events": True,
        "telemetry": False,
    }

    _configure_output(args=args, agent=xpander_agent, task=task, is_member=is_member)
    _configure_session_storage(args=args, agent=xpander_agent, task=task)
    _configure_context_optimizer(args=args, agent=xpander_agent, task=task, model=model)

    # The deps leg (DB fetch + the sync configures that override its args keys —
    # order preserved) is independent of tool/MCP resolution, so overlap them: on a
    # cold agent this runs the conn-string fetch concurrently with the MCP probes.
    async def _attach_deps_leg() -> None:
        await _configure_user_memories(args=args, agent=xpander_agent, task=task)
        await _attach_async_dependencies(
            args=args, agent=xpander_agent, task=task, model=model, is_async=is_async
        )
        _configure_knowledge_bases(args=args, agent=xpander_agent)
        _configure_additional_context(args=args, agent=xpander_agent, task=task)
        # Configure pre-hooks (guardrails, etc.)
        _configure_pre_hooks(args=args, agent=xpander_agent, model=model)

    _skipped_mcp_notes: List[str] = []
    resolved_tools, _ = await asyncio.gather(
        _resolve_agent_tools(
            agent=xpander_agent,
            task=task,
            auth_events_callback=auth_events_callback,
            skipped_notes=_skipped_mcp_notes,
        ),
        _attach_deps_leg(),
    )
    args["tools"] = resolved_tools

    # Dynamic mode: MCP toolkits are SDK-owned (kept out of args["tools"] so the LLM
    # never sees them). Surface them here so the worker closes their sessions post-run
    # — the agno-owned close path only iterates args["tools"].
    args["_xpander_hidden_mcp_toolkits"] = list(
        getattr(xpander_agent.tools, "_dynamic_mcp_toolkits", []) or []
    )

    # Tell the agent about any MCP tools skipped this run (no user / unreachable) so it
    # can explain the missing capability to the user instead of silently lacking it.
    if _skipped_mcp_notes:
        _skip_block = "Unavailable tools this run:\n" + "\n".join(
            f"- {n}" for n in _skipped_mcp_notes
        )
        _existing_ctx = args.get("additional_context")
        args["additional_context"] = (
            f"{_existing_ctx}\n\n{_skip_block}" if _existing_ctx else _skip_block
        )

    if tools and len(tools) != 0:
        args["tools"].extend(tools)

    _mem_user = task.input.user if task and task.input else None
    _mem_enabled = args.pop("_xpander_memory_enabled", True)
    if (
        task
        and _mem_user
        and _mem_user.id
        and not xpander_agent.is_a_team
        and _mem_enabled
        and not _declares_memory_ops(task)
    ):
        _listed_memories = _parse_listed_memories(args.get("additional_context") or "")
        args["tools"].append(
            _build_memory_tool(
                xpander_agent,
                task,
                # the <memories> block is already rendered into additional_context above
                listed_ids=set(
                    _MEMORY_BLOCK_ID_RE.findall(args.get("additional_context") or "")
                ),
                listed_memories=_listed_memories,
            )
        )

    # Inline agent-gateway children (and any non-DP task) must not see the planning
    # tool family — hide it so the agent can't call it.
    _strip_planning_tools_if_inactive(args=args, agent=xpander_agent, task=task)

    # Reasoning tools only help weak non-reasoning models (PRO-1879); strong /
    # natively-reasoning models are hurt by the extra scaffolding (PRO-1875).
    should_use_reasoning_tools = _should_use_reasoning_tools(
        agent=xpander_agent, task=task
    ) and _is_weak_model(model)

    if not xpander_agent.is_a_team and should_use_reasoning_tools:
        from agno.tools.reasoning import ReasoningTools

        logger.info(
            f"[reasoning-tools] attaching think/analyze for weak model "
            f"id={getattr(model, 'id', '?')}"
        )

        reasoning_toolkit = ReasoningTools(
            enable_think=True,
            enable_analyze=True,
            add_instructions=True,
            add_few_shot=True,
            instructions="use 'think' and 'analyze' ONLY when its not a simple task of 'hi', 'what can you do' and such low complexity tasks",
        )
        # When deep planning is active, the think/analyze tools must also tag
        # the plan step they belong to. Their schema is built by agno from a
        # fixed entrypoint signature, so inject the field directly and freeze
        # the schema; the value is stripped from the call args before dispatch.
        if (
            xpander_agent.deep_planning
            and task
            and getattr(task, "deep_planning", None)
            and task.deep_planning.enabled
        ):
            _inject_plan_task_id_into_reasoning_tools(reasoning_toolkit)
        args["tools"].append(reasoning_toolkit)

    # team
    if xpander_agent.is_a_team:
        sub_agents = xpander_agent.graph.sub_agents

        # load sub agents
        sub_agents = await asyncio.gather(
            *[
                Agents(
                    configuration=Configuration(
                        api_key=xpander_agent.configuration.api_key,
                        organization_id=xpander_agent.configuration.organization_id,
                        base_url=xpander_agent.configuration.base_url,
                    )
                ).aget(agent_id=sub_agent_id)
                for sub_agent_id in sub_agents
            ]
        )
        if sub_agents and len(sub_agents):
            base_state = xpander_agent.configuration.state.model_copy()
            for sub_agent in sub_agents:
                sub_agent.configuration.state.task = base_state.task
        # convert to members. is_member=True keeps the task's structured-output
        # contract on the root manager alone — members report prose upward and the
        # root renders the envelope once, instead of every agent writing the full
        # answer into it. Propagates down, so a nested sub-team's leader is a member too.
        members = await asyncio.gather(
            *[
                build_agent_args(
                    xpander_agent=sub_agent,
                    override=override,
                    task=task,
                    is_async=is_async,
                    auth_events_callback=auth_events_callback,
                    is_member=True,
                )
                for sub_agent in sub_agents
            ]
        )

        # set members to use parent agent model
        if members and len(members) != 0:
            for member in members:
                member["model"] = model
                # A member's SDK-owned MCP toolkits (dynamic mode) must be hoisted to
                # the top-level args so the worker closes them, and the key removed
                # before AgnoAgent/AgnoTeam(**member) — their __init__ rejects it.
                member_hidden = member.pop("_xpander_hidden_mcp_toolkits", None)
                if member_hidden:
                    args.setdefault("_xpander_hidden_mcp_toolkits", []).extend(
                        member_hidden
                    )

        args.update(
            {
                "members": [
                    (
                        AgnoAgent(**member)
                        if "members" not in member
                        else AgnoTeam(**member)
                    )
                    for member in members
                ],
                "add_member_tools_to_context": True,
                "share_member_interactions": True,
                "show_members_responses": True,
            }
        )

    args.update(
        {
            "name": xpander_agent.name,
            "model": model,
            "description": (
                xpander_agent.description
                if xpander_agent.description
                and xpander_agent.description is not None
                and len(xpander_agent.description) != 0
                else xpander_agent.instructions.description
            ),
            "instructions": (
                task.instructions_override
                if task.instructions_override
                else xpander_agent.instructions.instructions
            ),
            "expected_output": (
                task.expected_output
                if task and task.expected_output
                else xpander_agent.expected_output
            ),
            "add_datetime_to_context": True,
            # Coarsen the injected timestamp to the hour. agno defaults to
            # str(datetime.now()) (microsecond precision), which changes every run
            # and sits inside the cached prompt prefix — busting prompt caching
            # across runs on every provider (OpenAI prefix match, Anthropic/Bedrock
            # cache_control/cachePoint). Hour granularity keeps useful date/time
            # context while letting the prefix stay byte-identical within the hour.
            "datetime_format": "%Y-%m-%d %H:00 %Z",
        }
    )

    # An instructions override is a complete replacement — leave it untouched.
    if not (task and task.instructions_override):
        dynamic_prompt_text = await _aget_dynamic_prompt_text(xpander_agent)
        if dynamic_prompt_text:
            _instr = getattr(xpander_agent, "instructions", None)
            position = getattr(_instr, "dynamic_prompt_position", "after")
            args["instructions"] = _compose_dynamic_prompt(
                args.get("instructions") or "", dynamic_prompt_text, position
            )

    if (
        xpander_agent.is_a_team
        and xpander_agent.expected_output
        and len(xpander_agent.expected_output) != 0
    ):
        args["instructions"] += f"""\n
            <expected_output>
            {xpander_agent.expected_output}
            </expected_output>
        """

    if xpander_agent.is_a_team and workspace_enabled:
        args["instructions"] += f"""\n
            <workspace_access_rules>
            Each workspace file belongs to the agent that created it. As the team leader, you cannot read or use a child agent's workspace files directly. To use data stored in a child's workspace, delegate the task to that child agent and let it access its own workspace.
            </workspace_access_rules>
        """

    if override:
        args.update(override)

    # Append context optimization guidance (must be after all instruction overrides).
    # Skipped when workspace tools are disabled: L1 no longer truncates and the
    # session-backup pointer is empty, so this guidance would only mislead.
    if "instructions" not in args or not args["instructions"]:
        args["instructions"] = ""
    # Grounding guard applies to every agent (workspace or not): don't claim un-executed work,
    # don't invent a prior user turn. Appended after overrides so instructions_override can't drop it.
    args["instructions"] += GROUNDING_INSTRUCTIONS
    # Turn economy is not workspace-specific: any agent holding tools pays a full prefix
    # re-read per turn, so the batching rule is worth its ~150 tokens wherever tools exist.
    if args.get("tools"):
        args["instructions"] += TURN_ECONOMY_INSTRUCTIONS
        # anti-noop discipline was Omni-only before; every other agent filled end-of-task turns
        args["instructions"] += TOOL_CALL_DISCIPLINE_INSTRUCTIONS
        if task is not None:
            # read at run end: a tool-equipped run finishing with zero calls is suspect
            try:
                object.__setattr__(task, "_xp_tools_attached", True)
            except Exception:
                pass
    if workspace_enabled:
        args["instructions"] += CONTEXT_OPTIMIZATION_INSTRUCTIONS

    # Without the contract an aligned model refuses keyed steer blocks as injections.
    if task is not None and getattr(task, "id", None):
        args["instructions"] += steering_contract_block(task.id)

    # Conditionally inject workspace output guidance (only when workspace tools are
    # present). Also gated on workspace_enabled — the backend should already omit
    # xpworkspace-* tools when disabled, but gate here too as a safeguard.
    _has_workspace_tools = workspace_enabled and any(
        getattr(t, "__name__", getattr(t, "name", "")).startswith("xpworkspace-")
        for t in args.get("tools", [])
    )
    if _has_workspace_tools:
        args["instructions"] += WORKSPACE_OUTPUT_INSTRUCTIONS
        args["instructions"] += LARGE_PAYLOAD_AUTHORING_INSTRUCTIONS
        args["instructions"] += WORKSPACE_SECRETS_INSTRUCTIONS

    # Inject the resolved skills catalog (embedded in the agent payload). Listed
    # inline so the agent discovers skills without reading ./skills/INDEX.md (which
    # syncs asynchronously). Appended here, not via AgentInstructions, so it
    # survives instructions_override. Skipped when workspace is disabled — skills
    # live in the workspace and are unreadable without workspace tools.
    skills_block = (
        _build_skills_instructions(getattr(xpander_agent, "skills", None))
        if workspace_enabled
        else ""
    )
    if skills_block:
        args["instructions"] += skills_block

    # Dynamic tools: when enabled, the bulk catalog is hidden from the LLM and
    # reached via the xp_* meta-tools (built in ToolsRepository.functions). Inject
    # the discovery hint + inline catalog here, after instruction overrides, so it
    # survives instructions_override. The hint is empty when nothing is hidden.
    if getattr(xpander_agent, "use_dynamic_tools", False) and getattr(
        xpander_agent, "tools", None
    ):
        args["instructions"] += xpander_agent.tools.build_dynamic_tools_hint()

    # Register xpcompact_context tool and inject its guidance (fix #1: after tools are set).
    # Gated by MANUAL_COMPACT_TOOL_ENABLED — disabled for now to stop manual-compaction overuse.
    if MANUAL_COMPACT_TOOL_ENABLED:
        args["tools"].append(_build_compact_tool())
        args["instructions"] += COMPACT_TOOL_INSTRUCTIONS

    # ---- Robust-L2: register xpfinalize_task and attach ledger ----- #
    # Hidden on a normal run: a tool the model can see is a tool it calls spontaneously.
    if FINALIZE_MODE_ENABLED and task is not None and is_task_finalize_active(task):
        try:
            finalize_tool = build_finalize_tool(task)
            args["tools"].append(finalize_tool)
            mark_finalize_tool_registered(task)
        except Exception as exc:
            logger.warning(f"[finalize-mode] failed to register tool: {exc}")

    # If Finalize-Only Mode is already active when args are built (e.g. a
    # second arun() within the same task lifecycle), inject the
    # system-prompt override now so the agent reads it before its first
    # turn. The tool gate inside the hook handles every subsequent turn.
    if FINALIZE_MODE_ENABLED and task is not None:
        try:
            optimizer_for_finalize = args.get("compression_manager")
            if isinstance(
                optimizer_for_finalize, XPanderContextOptimizer
            ) and is_finalize_active(optimizer_for_finalize):
                args["instructions"] += FINALIZE_ONLY_SYSTEM_OVERRIDE
        except Exception as exc:
            logger.warning(f"[finalize-mode] failed to inject system override: {exc}")

    # Attach the action ledger to the task. Idempotent — subsequent calls
    # return the same instance. Lives on the task (not the optimizer)
    # because the optimizer is replaced on every plan retry; the task
    # survives.
    #
    # ``aload`` is the only blocking ledger op; it does an HTTP file_read
    # against the workspace pod which can be cold-starting on a brand
    # new task. Gate it on a prior-existence hint so fresh tasks pay
    # zero cost: only run aload when the task already shows signs of a
    # prior run (compacted_context block from earlier retry, last_actions
    # block, etc.). Without this hint the file_read is guaranteed-404 /
    # mono-500 and just delays first-tool-call dispatch.
    #
    # Same-process retries are unaffected because the ledger lives on
    # ``task._xp_action_ledger`` — already in memory, no reload needed.
    # Cross-process recovery (worker restart mid-task) is the only case
    # where aload matters, and that case always coincides with prior
    # additional_context content.
    if LEDGER_ENABLED and task is not None and xpander_agent is not None:
        try:
            ledger = attach_to_task(task=task, agent=xpander_agent)
            additional = getattr(task, "additional_context", None) or ""
            has_prior_state = (
                "<compacted_context>" in additional
                or "<last_actions>" in additional
                or "<retry_focus>" in additional
            )
            if has_prior_state:
                await ledger.aload()
        except Exception as exc:
            logger.warning(f"[action-ledger] attach/load failed: {exc}")

    # Stuck detection: track recent tool call signatures to detect loops.
    # Promoted to task-scoped storage so the deque survives arun() resets
    # — without that, a stuck loop spread across N Layer-2 compactions
    # evades the 3-in-a-row check because each compaction starts a fresh
    # arun with an empty deque. The task-scoped maxlen is wider (=
    # ``MAX_REPEATED_TOOL_CALLS`` + a few slots of headroom) so the
    # cross-arun escalation can count up to the abort threshold even
    # after a couple of unrelated tool calls slip in.
    _tool_call_history_maxlen = max(10, MAX_REPEATED_TOOL_CALLS + 3)
    if task is not None:
        existing_history = getattr(task, "_xp_tool_call_history", None)
        if (
            isinstance(existing_history, deque)
            and existing_history.maxlen == _tool_call_history_maxlen
        ):
            _tool_call_history = existing_history
        else:
            _tool_call_history = deque(maxlen=_tool_call_history_maxlen)
            try:
                object.__setattr__(task, "_xp_tool_call_history", _tool_call_history)
            except Exception:
                pass
    else:
        _tool_call_history = deque(maxlen=_tool_call_history_maxlen)
    _STUCK_THRESHOLD = 3  # consecutive identical calls to trigger warning

    # Consecutive-error circuit breaker: per-tool error streaks, args-agnostic
    # (a flailing agent varies args every retry so the identical-args detector
    # above never fires) and with NO xp* exemption. Task-scoped so streaks
    # survive arun() resets, mirroring _xp_tool_call_history.
    if task is not None:
        _tool_error_streaks = getattr(task, "_xp_tool_error_streaks", None)
        if not isinstance(_tool_error_streaks, dict):
            _tool_error_streaks = {}
            try:
                object.__setattr__(task, "_xp_tool_error_streaks", _tool_error_streaks)
            except Exception:
                pass
    else:
        _tool_error_streaks = {}

    def _record_tool_outcome(function_name: str, errored: bool) -> Optional[str]:
        """Track per-tool consecutive errors; at the cap disable THAT tool (run-wide
        finalize here killed mandated writes on healthy tools when one flaky tool
        kept failing after a fallback had already succeeded)."""
        streak = _bump_error_streak(_tool_error_streaks, function_name, errored)
        if streak < ERROR_STREAK_FINALIZE_AT:
            return None
        if function_name.startswith("xp"):
            # platform tools are never disabled (finalize deadlock) - a systemic 5x
            # failure of one keeps the original run-wide finalize behavior
            optimizer_for_streak = args.get("compression_manager")
            if isinstance(optimizer_for_streak, XPanderContextOptimizer):
                try:
                    enter_finalize_mode(optimizer_for_streak, reason="error_streak")
                except Exception as exc:
                    logger.warning(f"[error-streak] finalize entry failed: {exc}")
            logger.warning(
                f"[error-streak] platform tool '{function_name}' errored {streak}x "
                f"consecutively; entering finalize mode"
            )
            return (
                f"⚠️ ERROR STREAK: '{function_name}' has now failed {streak} times in a "
                f"row. The task is entering finalize-only mode - stop retrying and "
                f"finalize with a summary of what succeeded and what is blocked.\n\n"
                + gate_rejection_message(task, _record_gated_call(task))
            )
        disabled = _disable_tool(task, function_name)
        logger.warning(
            f"[error-streak] tool '{function_name}' errored {streak}x "
            f"consecutively (cap {ERROR_STREAK_FINALIZE_AT}); disabling it "
            f"({len(disabled)} tool(s) disabled)"
        )
        if len(disabled) >= DISABLED_TOOLS_FINALIZE_AT:
            optimizer_for_streak = args.get("compression_manager")
            if isinstance(optimizer_for_streak, XPanderContextOptimizer):
                try:
                    enter_finalize_mode(optimizer_for_streak, reason="error_streak")
                except Exception as exc:
                    logger.warning(
                        f"[error-streak] failed to enter finalize mode with "
                        f"{len(disabled)} disabled tools: {exc}"
                    )
            return (
                f"⚠️ ERROR STREAK: '{function_name}' has now failed {streak} times in a "
                f"row and {len(disabled)} tools are disabled. The task is entering "
                f"finalize-only mode - stop retrying and finalize with a summary of "
                f"what succeeded and what is blocked.\n\n"
                + gate_rejection_message(task, _record_gated_call(task))
            )
        return (
            f"⚠️ ERROR STREAK: '{function_name}' has now failed {streak} times in a row "
            f"and is DISABLED for the rest of this run. Do not retry it in any form. "
            f"Use a different tool or approach for what it was doing; any REQUIRED final "
            f"step must still run via its own tool, or be reported as NOT done."
        )

    def _record_no_progress(result: Any, force: bool = False) -> Optional[str]:
        """Track calls that changed nothing; at the cap push the run to answer.

        Distinct from the error streak: these calls all "succeed", they just do nothing -
        a refused noop command, a blocked repeat, a memory write over budget. A run that
        strings a few together has no tool work left and is filling turns.
        """
        streak = _bump_no_progress_streak(task, result, force=force)
        if streak < NO_PROGRESS_FINALIZE_AT:
            return None
        optimizer_for_streak = args.get("compression_manager")
        if isinstance(optimizer_for_streak, XPanderContextOptimizer):
            try:
                enter_finalize_mode(optimizer_for_streak, reason="no_progress")
            except Exception as exc:
                logger.warning(f"[no-progress] failed to enter finalize mode: {exc}")
        logger.warning(
            f"[no-progress] {streak} consecutive calls changed nothing "
            f"(cap {NO_PROGRESS_FINALIZE_AT}); entering finalize mode"
        )
        return NO_PROGRESS_MESSAGE.format(n=streak)

    # append tools hooks
    async def on_tool_call_hook(
        function_name: str, function_call: Callable, arguments: Dict[str, Any]
    ):
        # ---- Robust-L2 finalize-mode tool gate -------------------- #
        # When Finalize-Only Mode is active, every tool except the
        # short allowed-list returns a synthetic short-circuit result
        # telling the agent how to finalize. We check before
        # any other hook logic so even side-effects like activity
        # reporting are skipped — the only thing that should happen
        # is "agent receives gate message and tries again with
        # xpfinalize_task".
        if FINALIZE_MODE_ENABLED:
            optimizer_finalize = args.get("compression_manager")
            if (
                isinstance(optimizer_finalize, XPanderContextOptimizer)
                and is_finalize_active(optimizer_finalize)
                and not is_tool_allowed(optimizer_finalize, function_name)
                and not _finalize_safe_read_allowed(task, function_name, arguments)
            ):
                gated = _record_gated_call(task)
                logger.info(
                    f"[finalize-mode] gate rejected tool '{function_name}' (#{gated})"
                )
                message = gate_rejection_message(task, gated)
                _report_blocked_call(task, function_name, message)
                return message
            # Inverse gate: the tool is registered every run (finalize can trip mid-run), so reject spontaneous calls.
            premature = _premature_finalize_rejection(optimizer_finalize, function_name)
            if premature is not None:
                logger.warning(
                    "[finalize-mode] premature xpfinalize_task call rejected"
                )
                warning = _record_no_progress(premature)
                return f"{premature}\n\n{warning}" if warning else premature

        # ---- Coerce stringified-JSON args back into structured form -- #
        # The LLM occasionally emits ``payload`` (or nested params) as a
        # quoted JSON string instead of a JSON object literal, e.g.
        # ``payload='{"body_params": {...}}'``. Pydantic's tool-schema
        # validation rejects the string with a ``model_type`` error and
        # the agent typically gives up on the proper tool, falls back
        # to bash heredoc, and burns turns fighting unicode escapes.
        # ``coerce_json_like`` walks the args dict and parses any string
        # that looks like ``{...}`` / ``[...]`` back into a dict/list,
        # so the validation succeeds and the call dispatches as
        # intended. Non-JSON strings pass through untouched.
        if isinstance(arguments, dict):
            try:
                for _k in ("payload", "body_params", "query_params", "path_params"):
                    if _k in arguments and isinstance(arguments[_k], str):
                        _coerced = coerce_json_like(arguments[_k])
                        if isinstance(_coerced, (dict, list)):
                            arguments[_k] = _coerced
                            logger.debug(
                                f"[tool-hook] coerced stringified {_k!r} -> "
                                f"{type(_coerced).__name__} for {function_name}"
                            )
            except Exception as exc:
                logger.debug(f"[tool-hook] arg coercion skipped: {exc}")

        # Effective tool identity for loop detection. The dynamic-tools dispatcher
        # (xp_execute_tool) hides the real tool in payload.name and runs it without
        # re-entering this hook, so the stuck/volume/error-streak guards below key
        # on the unwrapped inner tool instead of the opaque meta name.
        eff_name, eff_args = _effective_tool_identity(function_name, arguments)

        # Steer delivered earlier in this model step: unstarted calls stub out here,
        # before any cache/flush/billing work. Keyed on eff_name so a dispatcher-wrapped
        # finalize/plan call is still never skipped.
        if steer_batch_skip_armed(getattr(task, "id", None), eff_name):
            logger.info(
                f"[steering] skipped queued call '{eff_name}' behind a delivered steer"
            )
            return STEER_SKIP_STUB

        # a tool disabled by the volume/error caps stays disabled for the run;
        # each refusal advances the no-progress streak so hammering it converges
        if _is_tool_disabled(task, eff_name):
            logger.info(f"[disabled-tool] refusing call to '{eff_name}'")
            message = DISABLED_TOOL_REPEAT_MESSAGE.format(tool=eff_name)
            warning = _record_no_progress(message)
            if warning:
                message = f"{message}\n\n{warning}"
            _report_blocked_call(task, eff_name, message)
            return message

        # Self-declared filler: the reasoning title itself says the call does no work.
        # Refused before dispatch, billing, and activity logging - nothing is recorded.
        # xpfinalize_task is exempt: "finalize task" is its one legitimate title.
        if eff_name != "xpfinalize_task":
            try:
                # dynamic dispatch may carry the headers on the OUTER call, not the inner args
                _reasoning_title = _extract_reasoning_title(
                    eff_args if isinstance(eff_args, dict) else None
                ) or _extract_reasoning_title(arguments)
                if _is_filler_title(_reasoning_title):
                    logger.info(
                        f"[filler-title] refused '{eff_name}' - self-labelled filler call"
                    )
                    warning = _record_no_progress(FILLER_TITLE_REFUSAL)
                    return (
                        f"{FILLER_TITLE_REFUSAL}\n\n{warning}"
                        if warning
                        else FILLER_TITLE_REFUSAL
                    )
            except Exception:
                pass

        # A live surface is already delivered at create time; sharing its manifest
        # afterwards is a manufactured wrap-up step, not a deliverable.
        if eff_name == "xpworkspace-file-share":
            try:
                _share_path = _extract_share_path(
                    eff_args
                    if function_name == _DYNAMIC_DISPATCH_META_TOOL
                    else arguments
                )
                if isinstance(_share_path, str) and _share_path.strip().lower().endswith(
                    ".livesurface"
                ):
                    logger.info(f"[livesurface-share] refused share of {_share_path!r}")
                    warning = _record_no_progress(LIVESURFACE_SHARE_REFUSAL)
                    return (
                        f"{LIVESURFACE_SHARE_REFUSAL}\n\n{warning}"
                        if warning
                        else LIVESURFACE_SHARE_REFUSAL
                    )
            except Exception:
                pass

        # preflight and monitoring + metrics
        matched_tool = None
        try:
            matched_tool = (
                (
                    xpander_agent.tools.get_tool_by_id(tool_id=function_name)
                    or xpander_agent.tools.get_tool_by_name(tool_name=function_name)
                )
                if xpander_agent.tools and len(xpander_agent.tools.list) != 0
                else None
            )
        except Exception:
            pass

        # Repository tools take a single `payload` model arg; sibling kwargs
        # would fail validate_call before the payload model's coercion runs.
        if matched_tool is not None and isinstance(arguments, dict):
            if reenvelope_sibling_args(arguments):
                logger.debug(
                    f"[tool-hook] re-enveloped sibling args into payload for "
                    f"{function_name}"
                )

        # workspace_path payload resolution: when the LLM offloaded a large
        # tool payload to a workspace file, fetch it now and replace
        # `arguments` with the resolved dict. Runs *before* activity logging
        # so the recorded payload is the resolved data, not the path.
        # Skipped for SDK-internal tools — these have specific schemas and
        # would never need workspace_path. Use exact prefix/name matches
        # rather than a broad "xp" prefix so third-party tools that happen
        # to start with "xp" still get resolved.
        is_sdk_internal_tool = (
            function_name.startswith("xpworkspace-")
            or function_name.startswith("xpschedule-")
            or function_name == "xpcompact_context"
        )
        if (
            isinstance(arguments, dict)
            and not is_sdk_internal_tool
            and has_workspace_path(arguments)
        ):
            try:
                resolved = await resolve_workspace_payload(
                    agent_id=xpander_agent.id,
                    configuration=xpander_agent.configuration,
                    task_id=getattr(task, "id", None) if task else None,
                    arguments=arguments,
                )
            except WorkspacePayloadError as exc:
                logger.warning(
                    f"workspace_payload: resolution failed for tool '{function_name}': "
                    f"{exc.description}"
                )
                raise
            except Exception as exc:
                logger.warning(
                    f"workspace_payload: unexpected resolution error for tool '{function_name}': {exc}"
                )
                raise

            # CRITICAL: agno's execute_entrypoint_async (function.py:1167) ignores
            # the kwargs we pass to next_func and reads self.arguments directly to
            # invoke the entrypoint. Reassigning our local `arguments` name has no
            # effect on what the tool / pydantic validate_call sees. We must mutate
            # the original dict in place so agno picks up the resolved data.
            if isinstance(resolved, dict):
                arguments.clear()
                arguments.update(resolved)
        elif isinstance(arguments, dict) and is_sdk_internal_tool:
            # Defense in depth: SDK-internal tool schemas no longer expose
            # workspace_path (Tool.schema gates injection on the same predicate),
            # but the LLM may still surface the field from a cached schema or a
            # mid-session reload. Strip it before dispatch — strip_workspace_path
            # handles the agno {"payload": <dict>} envelope.
            strip_workspace_path(arguments)

        # One signature for both guards, blind to the cosmetic reasoning headers.
        _sig_args = _signature_args(eff_args) if isinstance(eff_args, dict) else eff_args
        _sig_body = (
            _bounded_arg_signature(_sig_args)
            if isinstance(_sig_args, dict)
            else str(_sig_args or "")
        )
        # xpworkspace-bash keys on the NORMALIZED command so cosmetic variants
        # (`2>&1`, `| cat`, null redirects, trailing `;`) hash identically, and a
        # command made purely of readers/filters joins the ledger as a read.
        _bash_read_only = False
        if eff_name == "xpworkspace-bash":
            try:
                _bash_cmd = _coerce_bash_command(
                    eff_args
                    if function_name == _DYNAMIC_DISPATCH_META_TOOL
                    else arguments
                )
                if isinstance(_bash_cmd, str):
                    _bash_norm = _normalize_bash_command(_bash_cmd)
                    _bash_read_only = _bash_command_is_read_only(_bash_norm)
                    _sig_body = f"command={_bash_norm}"
            except Exception:
                pass
        _args_hash = hashlib.md5(_sig_body.encode()).hexdigest()[:12]
        _call_signature = f"{eff_name}:{_args_hash}"

        # Redundancy gate: a repeat that cannot answer differently never dispatches.
        # Runs before stuck detection so a provably-useless call costs nothing at all.
        try:
            if _is_redundant_call(
                task,
                _call_signature,
                eff_name,
                has_args=_has_meaningful_args(_sig_args),
                treat_read_only=_bash_read_only,
            ):
                logger.info(f"[redundancy] blocked repeat call to '{eff_name}'")
                message = REDUNDANT_CALL_MESSAGE.format(tool=eff_name)
                warning = _record_no_progress(message)
                return f"{message}\n\n{warning}" if warning else message
            _bump_mutation_counter(task, eff_name, is_read_only=_bash_read_only)
        except Exception:
            pass

        # Noop-bash gate: refuse placeholders pre-dispatch, before the round-trip and billing.
        if eff_name == "xpworkspace-bash":
            try:
                # a dynamic dispatch nests the real args under payload.arguments
                bash_args = (
                    eff_args
                    if function_name == _DYNAMIC_DISPATCH_META_TOOL
                    else arguments
                )
                bash_command = _coerce_bash_command(bash_args)
                if bash_command is not None and _is_noop_bash_command(bash_command):
                    logger.info(
                        f"[bash-noop] refused locally: {bash_command[:120]!r}"
                    )
                    warning = _record_no_progress(BASH_NOOP_REFUSAL)
                    return (
                        f"{BASH_NOOP_REFUSAL}\n\n{warning}"
                        if warning
                        else BASH_NOOP_REFUSAL
                    )
            except Exception:
                pass

        # Stuck detection: check for repeated calls
        stuck_warning = None
        try:
            # Plan bookkeeping and the sleep+poll pair legitimately repeat; everything
            # else is checked. Keyed on the effective inner tool so dynamic/MCP loops
            # dispatched through xp_execute_tool are caught, not exempted.
            if eff_name not in _REDUNDANCY_EXEMPT_TOOLS:
                call_signature = _call_signature
                _tool_call_history.append(call_signature)

                # Count *consecutive* trailing identical signatures. The
                # task-scoped deque survives arun() resets, so this
                # naturally covers the cross-compaction repeat case the
                # in-arun-only deque used to miss.
                consecutive_repeat = 0
                for sig in reversed(_tool_call_history):
                    if sig == call_signature:
                        consecutive_repeat += 1
                    else:
                        break

                # Hard abort: identical call repeated past the cap →
                # enter Finalize-Only Mode and short-circuit the dispatch
                # with the standard tool-gate rejection. Once finalize
                # mode is active the LLM sees the system override and
                # the gate routes it to the finalize entrypoint; done
                # BEFORE the warning branch so we don't double-fire the
                # warning on the same call that aborts.
                if consecutive_repeat >= MAX_REPEATED_TOOL_CALLS:
                    optimizer_for_abort = args.get("compression_manager")
                    if isinstance(optimizer_for_abort, XPanderContextOptimizer):
                        try:
                            enter_finalize_mode(
                                optimizer_for_abort,
                                reason="repeated_tool_call",
                            )
                        except Exception as exc:
                            logger.warning(
                                f"[stuck-detection] failed to enter finalize "
                                f"mode after {consecutive_repeat}x repeat of "
                                f"{call_signature}: {exc}"
                            )
                    logger.warning(
                        f"[stuck-detection] aborting tool '{eff_name}' "
                        f"for agent {xpander_agent.id}: identical call "
                        f"repeated {consecutive_repeat}x (cap "
                        f"{MAX_REPEATED_TOOL_CALLS}); entering finalize mode"
                    )
                    return gate_rejection_message(task, _record_gated_call(task))

                # Escalation tier: 5+ identical calls across the task →
                # stronger warning that names the next call as the abort
                # trigger. Wins over the basic 3-in-a-row warning when
                # both would otherwise fire.
                if consecutive_repeat >= REPEATED_TOOL_CALL_WARN_AT:
                    stuck_warning = (
                        f"⚠️ REPEATED CALL ({consecutive_repeat}x across this task): "
                        f"You keep calling '{eff_name}' with the same arguments. "
                        f"The next identical call will abort the task. Try different "
                        f"arguments, a different tool, or report the task as blocked "
                        f"with a short status."
                    )
                    logger.warning(
                        f"[stuck-detection] cross-arun repeat for agent "
                        f"{xpander_agent.id}: {call_signature} x{consecutive_repeat}"
                    )
                # Basic tier: 3-in-a-row inside the recent window.
                elif consecutive_repeat >= _STUCK_THRESHOLD:
                    stuck_warning = (
                        f"⚠️ STUCK DETECTION: You have called '{eff_name}' with identical arguments "
                        f"{consecutive_repeat} times in a row. This suggests you are in a loop. "
                        f"Try a different approach, use different parameters, or mark the current task as blocked."
                    )
                    logger.warning(
                        f"Stuck detection triggered for agent {xpander_agent.id}: {call_signature} repeated {consecutive_repeat}x"
                    )
        except Exception:
            pass

        # Args-agnostic per-tool volume guard: pagination varies the cursor every
        # call and alternating-tool loops reset the consecutive counters, so the
        # detectors above never fire on those runaway shapes.
        try:
            if not eff_name.startswith("xp"):
                total_calls = _bump_total_calls(task, eff_name)
                # read-class tools are warn-only: marathon agents legitimately make
                # hundreds of read calls over hours; only mutating tools can be disabled
                is_read_class = _is_read_class_tool(eff_name)
                if is_read_class:
                    over_warn = total_calls - READ_TOOL_CALLS_WARN_AT
                    if (
                        over_warn >= 0
                        and over_warn % READ_TOOL_CALLS_REWARN_EVERY == 0
                        and not stuck_warning
                    ):
                        stuck_warning = (
                            f"⚠️ TOOL VOLUME: '{eff_name}' has been called {total_calls} "
                            f"times in this task. Stop paginating or re-querying - work "
                            f"with the data you already have."
                        )
                        logger.warning(
                            f"[tool-volume] read-class '{eff_name}' at {total_calls} "
                            f"total calls for agent {xpander_agent.id}"
                        )
                elif total_calls >= MAX_TOTAL_TOOL_CALLS_PER_TOOL:
                    # disable THIS tool, not the run - run-wide finalize here killed
                    # mandated writes on tools that were never overused; repeat calls
                    # advance the no-progress streak at the disabled-check above
                    disabled = _disable_tool(task, eff_name)
                    logger.warning(
                        f"[tool-volume] disabling tool '{eff_name}' for agent "
                        f"{xpander_agent.id}: {total_calls} total calls this task "
                        f"(cap {MAX_TOTAL_TOOL_CALLS_PER_TOOL}); {len(disabled)} tool(s) disabled"
                    )
                    if len(disabled) >= DISABLED_TOOLS_FINALIZE_AT:
                        optimizer_for_volume = args.get("compression_manager")
                        if isinstance(optimizer_for_volume, XPanderContextOptimizer):
                            try:
                                enter_finalize_mode(
                                    optimizer_for_volume, reason="tool_overuse"
                                )
                            except Exception as exc:
                                logger.warning(
                                    f"[tool-volume] failed to enter finalize mode with "
                                    f"{len(disabled)} disabled tools: {exc}"
                                )
                        message = gate_rejection_message(task, _record_gated_call(task))
                        _report_blocked_call(task, eff_name, message)
                        return message
                    message = DISABLED_TOOL_MESSAGE.format(
                        tool=eff_name, calls=total_calls
                    )
                    _report_blocked_call(task, eff_name, message)
                    return message
                if (
                    not is_read_class
                    and total_calls >= TOTAL_TOOL_CALLS_WARN_AT
                    and not stuck_warning
                ):
                    stuck_warning = (
                        f"⚠️ TOOL VOLUME: '{eff_name}' has been called {total_calls} times in "
                        f"this task (hard cap {MAX_TOTAL_TOOL_CALLS_PER_TOOL}). Stop paginating or "
                        f"re-querying - work with the data you already have. Any REQUIRED final "
                        f"step (a mandated write/save) must still run via its own tool, or be "
                        f"reported as NOT done - never claim or imply it happened."
                    )
                    logger.warning(
                        f"[tool-volume] '{eff_name}' at {total_calls} total calls for "
                        f"agent {xpander_agent.id}"
                    )
        except Exception:
            pass

        # Plan-complete grace budget: once the plan is 100% done, every further call
        # spends a small wrap-up budget; past it the run is forced into finalize.
        try:
            optimizer_for_pc = args.get("compression_manager")
            pc_finalize_active = isinstance(
                optimizer_for_pc, XPanderContextOptimizer
            ) and is_finalize_active(optimizer_for_pc)
            # effective name: a plan tool routed through xp_execute_tool must count the same
            if not pc_finalize_active and eff_name not in _PLAN_REOPEN_TOOLS:
                pc_calls = _bump_plan_complete_calls(task)
                if pc_calls > PLAN_COMPLETE_GRACE_CALLS:
                    if isinstance(optimizer_for_pc, XPanderContextOptimizer):
                        try:
                            enter_finalize_mode(optimizer_for_pc, reason="plan_complete")
                        except Exception as exc:
                            logger.warning(
                                f"[plan-complete] failed to enter finalize mode: {exc}"
                            )
                    logger.warning(
                        f"[plan-complete] aborting tool '{eff_name}' for agent "
                        f"{xpander_agent.id}: {pc_calls} calls after the plan finished "
                        f"(budget {PLAN_COMPLETE_GRACE_CALLS}); entering finalize mode"
                    )
                    return PLAN_COMPLETE_STOP
                if pc_calls > 0 and not stuck_warning:
                    stuck_warning = PLAN_COMPLETE_COUNTDOWN.format(
                        n=pc_calls, grace=PLAN_COMPLETE_GRACE_CALLS
                    )
        except Exception:
            pass

        # Plan-churn breaker: planning/reasoning tools are exempt from the guards
        # above, so a pure plan/think loop (re-adding the same decision step with
        # no real tool call in between) previously ran unbounded.
        try:
            optimizer_for_churn = args.get("compression_manager")
            # finalize mode's allowed read tools (xpget_agent_plan) must not re-trip the breaker
            finalize_already_active = isinstance(
                optimizer_for_churn, XPanderContextOptimizer
            ) and is_finalize_active(optimizer_for_churn)
            plan_churn = (
                0 if finalize_already_active else _bump_plan_churn(task, function_name)
            )
            if plan_churn >= MAX_PLAN_CHURN:
                if isinstance(optimizer_for_churn, XPanderContextOptimizer):
                    try:
                        enter_finalize_mode(optimizer_for_churn, reason="plan_churn")
                    except Exception as exc:
                        logger.warning(
                            f"[plan-churn] failed to enter finalize mode after "
                            f"{plan_churn} consecutive plan/reasoning calls: {exc}"
                        )
                logger.warning(
                    f"[plan-churn] aborting tool '{function_name}' for agent "
                    f"{xpander_agent.id}: {plan_churn} consecutive planning/reasoning "
                    f"calls with no real work (cap {MAX_PLAN_CHURN}); entering finalize mode"
                )
                return gate_rejection_message(task, _record_gated_call(task))
            if plan_churn >= PLAN_CHURN_WARN_AT and not stuck_warning:
                stuck_warning = (
                    f"⚠️ PLAN CHURN: {plan_churn} consecutive planning/reasoning calls with no "
                    f"real tool call in between (hard cap {MAX_PLAN_CHURN}). Stop re-planning - "
                    f"execute the next plan step with an actual tool, or report the task as blocked."
                )
                logger.warning(
                    f"[plan-churn] {plan_churn} consecutive plan/reasoning calls for "
                    f"agent {xpander_agent.id} (latest '{function_name}')"
                )
        except Exception:
            pass

        # Generate a fresh request_id for this tool invocation so multiple
        # calls to the same tool remain distinct in the activity thread.
        # Deep-planning tools are excluded from activity reporting.
        # Reasoning tools (think/analyze) are reported via a separate
        # Think/Analyze event, not as a regular tool call.
        activity_request_id: Optional[str] = None
        # Plan step this tool call advances: the LLM-assigned toolcallplantaskid
        # header when present, else the active (first-incomplete) plan step.
        # Computed once so the request and its later result share the same id.
        tc_plan_task_id = resolve_plan_task_id(
            arguments if isinstance(arguments, dict) else None, task
        )
        if is_reasoning_tool(function_name) and isinstance(arguments, dict):
            # The plan-step id is not part of agno's think/analyze entrypoint
            # signature — strip it before dispatch (we already captured it in
            # tc_plan_task_id) so the entrypoint isn't handed an unknown kwarg.
            arguments.pop(TOOL_CALL_PLAN_TASK_ID, None)
        if task and getattr(task, "id", None) and is_reasoning_tool(function_name):
            try:
                asyncio.create_task(
                    report_reasoning_event(
                        task=task,
                        tool_name=function_name,
                        arguments=arguments if isinstance(arguments, dict) else None,
                        plan_task_id=tc_plan_task_id,
                    )
                )
            except Exception:
                pass
        elif (
            task
            and getattr(task, "id", None)
            and not should_skip_tool_report(function_name)
        ):
            activity_request_id = str(uuid.uuid4())
            # Fire-and-forget (background): reports every other tool type (local,
            # remote, MCP, knowledge-base, workspace, xpcompact_context). Keep a
            # strong reference so the loop can't GC the task before it sends.
            try:
                _spawn_bg(
                    report_tool_call_request(
                        task=task,
                        request_id=activity_request_id,
                        operation_id=function_name,
                        tool_name=function_name,
                        payload=arguments,
                        reasoning=extract_reasoning(
                            arguments if isinstance(arguments, dict) else None
                        ),
                        plan_task_id=tc_plan_task_id,
                    )
                )
            except Exception:
                pass

        # One billing id per logical call, matching the activity id so ledger rows correlate.
        billing_call_id = activity_request_id or str(uuid.uuid4())

        # Truncated tool-call guard: empty args on a tool whose schema has
        # required params = the tool-call JSON was cut off by the provider
        # output-token limit (Anthropic yields block.input == {} for truncated
        # input; agno then defaults the dropped args to "{}"). Dispatching
        # would run the tool with defaults against the wrong target — reject
        # with guidance instead. Placed after stuck detection so repeats still
        # count toward the identical-call abort, and counted by the
        # error-streak breaker so endless re-emits still terminate.
        if isinstance(arguments, dict) and not arguments:
            params_schema = _get_params_schema(
                args.get("tools"), function_name, matched_tool
            )
            try:
                required_params = (
                    _effective_required(params_schema) if params_schema else []
                )
            except Exception:
                required_params = []
            if not required_params and isinstance(params_schema, dict):
                # Zero-input tool legitimately
                # called with {} — the payload wrapper itself is still a
                # no-default pydantic param, so dispatch would fail
                # validation. Inject an empty payload in place (agno reads
                # self.arguments — see the mutation note above) so the model
                # builds from defaults and the tool runs.
                top_props = params_schema.get("properties")
                if isinstance(top_props, dict) and "payload" in top_props:
                    arguments["payload"] = {}
            if required_params:
                logger.warning(
                    f"[truncated-call-guard] rejecting '{function_name}': empty "
                    f"arguments but schema requires {required_params}"
                )
                if activity_request_id and task:
                    try:
                        _spawn_bg(
                            report_tool_call_result(
                                task=task,
                                request_id=activity_request_id,
                                operation_id=function_name,
                                tool_name=function_name,
                                payload=arguments,
                                result=TRUNCATED_TOOL_CALL_MESSAGE,
                                is_error=True,
                                plan_task_id=tc_plan_task_id,
                            )
                        )
                    except Exception:
                        pass
                warnings = [
                    _record_tool_outcome(eff_name, True),
                    _record_no_progress(TRUNCATED_TOOL_CALL_MESSAGE),
                ]
                streak_warning = "\n\n".join(w for w in warnings if w)
                if streak_warning:
                    return f"{TRUNCATED_TOOL_CALL_MESSAGE}\n\n{streak_warning}"
                return TRUNCATED_TOOL_CALL_MESSAGE

        # Layer 1 in-memory cache + workspace write queue (PRO-1148).
        #
        # Two pre-execute branches against the optimizer's WorkspaceCache:
        #   1. ``xpworkspace-context-retrieve`` (and the legacy
        #      ``xpworkspace-file-read`` of ``CONTEXT_OPTIMIZATION/*.xp``):
        #      try the cache first; on hit, synthesize a ToolInvocationResult
        #      holding the encrypted bytes and skip the workspace round-trip.
        #      The decrypt block below (line ~910) treats it identically to a
        #      real workspace read.
        #   2. Any other ``xpworkspace-*`` tool (bash, exec, generic file I/O):
        #      barrier — wait for every queued L1 write to land on the
        #      sandbox before the tool sees the filesystem.
        #
        # On cache hit we MUST skip the agno tool invocation AND the graph
        # preflight, otherwise we'd double-bill / double-log a tool that
        # never actually ran.
        cache_short_circuit_result: Optional[ToolInvocationResult] = None
        wcache = None
        cache_optimizer = args.get("compression_manager")
        if isinstance(cache_optimizer, XPanderContextOptimizer):
            wcache = cache_optimizer._workspace_cache

        # Step 1 — cache fast-path. Defensive try: a malformed args shape
        # should disable the short-circuit but never block the actual tool
        # from running, so we swallow exceptions here.
        if wcache is not None:
            try:
                ctx_id_to_check: Optional[str] = None
                # ``payload`` may arrive as a non-dict (e.g. a stringified JSON
                # the coercion step couldn't recover) — guard before .get() so
                # the fast-path degrades to a miss instead of raising
                # ``'str' object has no attribute 'get'``.
                payload_obj = (
                    arguments.get("payload") if isinstance(arguments, dict) else None
                )
                body = (
                    payload_obj.get("body_params", {})
                    if isinstance(payload_obj, dict)
                    else {}
                )
                if function_name == "xpworkspace-context-retrieve":
                    cid = body.get("context_id") or (
                        arguments.get("context_id")
                        if isinstance(arguments, dict)
                        else None
                    )
                    if isinstance(cid, str) and cid.strip():
                        ctx_id_to_check = cid.strip()
                elif function_name == "xpworkspace-file-read":
                    path_arg = body.get("path", "") if isinstance(body, dict) else ""
                    if isinstance(path_arg, str) and is_context_optimization_file(
                        path_arg
                    ):
                        tail = path_arg.rsplit("/", 1)[-1]
                        if tail.endswith(".xp"):
                            ctx_id_to_check = tail[:-3]

                if ctx_id_to_check is not None:
                    entry = wcache.get(ctx_id_to_check)
                    if entry is not None:
                        cache_short_circuit_result = ToolInvocationResult(
                            tool_id=function_name,
                            tool_call_id=(
                                arguments.get("tool_call_id")
                                if isinstance(arguments, dict)
                                else None
                            ),
                            task_id=getattr(task, "id", None) if task else None,
                            result={"content": entry.encrypted},
                            status_code=200,
                            is_success=True,
                        )
                        logger.debug(
                            f"[wcache] hit ctx={ctx_id_to_check} "
                            f"(function={function_name})"
                        )
            except Exception as cache_exc:
                logger.warning(
                    f"[wcache] pre-invoke fast-path errored for '{function_name}': "
                    f"{cache_exc}"
                )

        # Step 2 — barrier flush. Hard barrier: every non-cached
        # ``xpworkspace-*`` op must observe a sandbox state consistent with
        # all queued L1 writes BEFORE running. Failures must propagate so
        # the tool aborts rather than running against a half-flushed
        # sandbox. ``aflush`` always runs (not gated on ``has_pending``)
        # because queued errors can still be sitting in the error buffer
        # even when ``_pending`` is empty.
        if (
            wcache is not None
            and cache_short_circuit_result is None
            and function_name.startswith("xpworkspace-")
            and function_name != "xpworkspace-context-retrieve"
        ):
            await wcache.aflush()

        error = None
        result = None
        if cache_short_circuit_result is not None:
            # Skip the real tool call AND the graph preflight — this is
            # served entirely from in-process state.
            result = cache_short_circuit_result
        else:
            # ContextVar threads the billing id through agno's fixed signature; retries share it.
            _billing_ctx_token = current_tool_call_id.set(billing_call_id)
            try:
                # Call the function with auto-retry for transient errors
                result = await _invoke_with_transient_retry(
                    function_name=function_name,
                    function_call=function_call,
                    arguments=arguments,
                    max_retries=2,
                )

            except Exception as e:
                error = str(e)
                # A schema failure is the one error class that arrives with no
                # guidance; without an exit ramp it decays into junk wrap-up calls.
                guidance_added = "validation error" in error.lower()
                if guidance_added:
                    error = f"{error}{VALIDATION_ERROR_GUIDANCE}"
                # Emit ToolCallResult with is_error=True before re-raising.
                if activity_request_id and task:
                    try:
                        _spawn_bg(
                            report_tool_call_result(
                                task=task,
                                request_id=activity_request_id,
                                operation_id=function_name,
                                tool_name=function_name,
                                payload=arguments,
                                result=error,
                                is_error=True,
                                plan_task_id=tc_plan_task_id,
                            )
                        )
                    except Exception:
                        pass
                # ---- Robust-L2: ledger entry on error ------------ #
                # Await directly: aappend is in-memory + queued workspace
                # write, returns fast. Wrapping in create_task means the
                # in-memory append could race the post-arun evidence
                # check, and aflush() can't drain a task it never saw.
                if LEDGER_ENABLED and task is not None:
                    try:
                        ledger = get_attached_ledger(task)
                        if ledger is None and xpander_agent is not None:
                            ledger = attach_to_task(task=task, agent=xpander_agent)
                        if ledger is not None:
                            entry = build_entry_from_call(
                                tool_name=function_name,
                                arguments=arguments,
                                result=error,
                                status="error",
                                tool_call_id=activity_request_id,
                            )
                            await ledger.aappend(entry)
                    except Exception as exc:
                        logger.debug(f"[action-ledger] append failed: {exc}")
                # Errors feed the ERROR-streak breaker only (cap 5). They must NOT
                # feed the no-progress breaker (cap 3): the raise below skips the
                # success-path reset, so counting errors here can only ever climb -
                # two spurious argument-shape/serialization faults (e.g. a double-
                # wrapped payload) would otherwise trap the run in finalize-only mode.
                # No-progress is for refused-noop RESULTS, tracked on the success path.
                # Effective name: five raises through xp_execute_tool must streak the
                # INNER tool, never phantom-disable the meta-tool.
                _record_tool_outcome(eff_name, True)
                if guidance_added:
                    raise ToolSchemaValidationError(error) from e
                raise
            finally:
                current_tool_call_id.reset(_billing_ctx_token)
                try:
                    # Skip the graph preflight for the virtual dynamic-tools
                    # meta-tools (xp_list/search/get/execute). They are local SDK
                    # plumbing, never real graph nodes, and `matched_tool` is
                    # always None for them (they aren't in the tools repo), so
                    # without this guard each meta-tool call fires a spurious
                    # backend InvokeTool preflight. The real tool dispatched via
                    # xp_execute_tool still preflights/reports through its own
                    # ainvoke path. See dynamic_tools.py (PRO-1653).
                    if (
                        not matched_tool
                        and task
                        and function_name not in DYNAMIC_META_TOOLS
                    ):  # agent / mcp tool
                        tool_instance = Tool(
                            configuration=xpander_agent.configuration,
                            id=function_name,
                            name=function_name,
                            method="GET",
                            path=f"/tools/{function_name}",
                            should_add_to_graph=False,
                            is_local=True,
                            is_synced=True,
                            description=function_name,
                        )
                        parsed_result = None
                        try:
                            parsed_result = dict(result)
                        except Exception:
                            parsed_result = result

                        await tool_instance.agraph_preflight_check(
                            agent_id=xpander_agent.id,
                            configuration=tool_instance.configuration,
                            task_id=task.id,
                            payload=(
                                {"input": arguments, "output": error or parsed_result}
                                if isinstance(arguments, dict)
                                else None
                            ),
                            # per-call id -> deterministic billing key on the backend
                            tool_call_id=billing_call_id,
                        )
                except Exception:
                    pass

        # Helper used at every success return point to emit the ToolCallResult event.
        def _emit_success_result(
            final_result: Any,
            is_error: bool = False,
            skip_truncation: bool = False,
            inline_preview: Optional[str] = None,
        ) -> None:
            if not activity_request_id or not task:
                return
            try:
                if inline_preview is not None:
                    # The hook already applied the workspace preview + pointer;
                    # report that verbatim so the activity log matches what
                    # the LLM sees on context.
                    payload_for_activity = inline_preview
                    activity_skip_truncation = True
                else:
                    payload_for_activity = final_result
                    if hasattr(final_result, "result"):
                        payload_for_activity = final_result.result
                    elif hasattr(final_result, "content"):
                        payload_for_activity = final_result.content
                    activity_skip_truncation = skip_truncation
                # For CONTEXT_OPTIMIZATION file reads the agent explicitly asked for
                # the FULL offloaded content; report it verbatim rather than
                # truncating it again for activity. Every other tool gets the
                # display-only clamp inside report_tool_call_result (the model
                # itself may have received the full result - L1 skips most xp*
                # tools). Background fire-and-forget with a retained
                # reference so the result event isn't GC'd before it sends.
                _spawn_bg(
                    report_tool_call_result(
                        task=task,
                        request_id=activity_request_id,
                        operation_id=function_name,
                        tool_name=function_name,
                        payload=arguments,
                        result=payload_for_activity,
                        is_error=is_error,
                        skip_truncation=activity_skip_truncation,
                        plan_task_id=tc_plan_task_id,
                    )
                )
            except Exception:
                pass

        # Layer 3: detect xpcompact_context tool call and set flag on optimizer
        if function_name == "xpcompact_context":
            try:
                focus = ""
                if isinstance(arguments, dict):
                    payload = arguments.get("payload")
                    if isinstance(payload, dict):
                        # Canonical shape: payload.focus.
                        focus = payload.get("focus", "") or ""
                        # Legacy fallback: payload.body_params.focus (pre-PRO-1246).
                        if not focus and isinstance(payload.get("body_params"), dict):
                            focus = payload["body_params"].get("focus", "") or ""
                    # Final fallback: top-level focus (pre-payload-wrapper shape).
                    if not focus:
                        focus = arguments.get("focus", "") or ""
                optimizer = args.get("compression_manager")
                if isinstance(optimizer, XPanderContextOptimizer):
                    optimizer.compact_requested = True
                    optimizer.compact_focus = focus
                    logger.info(
                        f"[context-optimizer] layer 3: compact requested (focus={focus!r})"
                    )
                scheduled_message = "Context compaction scheduled. It will execute after this turn's tool calls complete."
                _emit_success_result(scheduled_message)
                return scheduled_message
            except Exception as e:
                logger.warning(
                    f"[context-optimizer] layer 3: failed to schedule compact: {e}"
                )
                failure_message = f"Failed to schedule compaction: {e}"
                _emit_success_result(failure_message, is_error=True)
                return failure_message

        # Decrypt context optimization files read from workspace
        # Also tracks whether this specific tool call retrieved an offloaded
        # CONTEXT_OPTIMIZATION file so the activity result is NOT re-truncated
        # (the agent asked for the full content on purpose).
        # Triggered by either:
        #   - xpworkspace-context-retrieve (explicit retrieve tool — always encrypted)
        #   - xpworkspace-file-read on a CONTEXT_OPTIMIZATION/*.xp path (legacy path)
        is_context_optimization_read = False
        is_context_retrieve_call = function_name == "xpworkspace-context-retrieve"
        if is_context_retrieve_call or function_name == "xpworkspace-file-read":
            try:
                should_decrypt = is_context_retrieve_call
                if not should_decrypt:
                    read_path = (
                        arguments.get("payload", {})
                        .get("body_params", {})
                        .get("path", "")
                    )
                    should_decrypt = is_context_optimization_file(read_path)
                if should_decrypt:
                    is_context_optimization_read = True
                    # Offload may have happened in a sibling sub-execution, so try
                    # this task's key first, then the conversation-root (parent) key.
                    keys = (
                        [
                            derive_key(
                                org_id=xpander_agent.configuration.organization_id,
                                agent_id=xpander_agent.id,
                                task_id=sid,
                            )
                            for sid in candidate_scope_ids(task)
                        ]
                        if task
                        else []
                    )
                    if isinstance(result, ToolInvocationResult) and result.result:
                        content = (
                            result.result.get("content", "")
                            if isinstance(result.result, dict)
                            else result.result
                        )
                        result.result = try_decrypt(content, keys)
                    elif hasattr(result, "content") and isinstance(result.content, str):
                        result.content = try_decrypt(result.content, keys)
                    elif isinstance(result, dict) and "content" in result:
                        result["content"] = try_decrypt(result["content"], keys)
            except Exception as e:
                logger.warning(
                    f"[context-optimizer] failed to decrypt context optimization file: {e}"
                )

        # Search-on-retrieve: when the agent passes query / semantic_query, filter
        # the decrypted plaintext to just the matching parts so it pays for a
        # subset instead of the full result. Runs SDK-side because the workspace
        # never holds the per-task decryption key. query narrows (grep), then
        # semantic_query ranks the narrowed text (bm25). Falls back to full
        # content on any failure.
        if is_context_retrieve_call:
            try:
                body = (
                    arguments.get("payload", {}).get("body_params", {})
                    if isinstance(arguments, dict)
                    else {}
                )
                query = (
                    str(body.get("query") or "").strip()
                    if isinstance(body, dict)
                    else ""
                )
                semantic_query = (
                    str(body.get("semantic_query") or "").strip()
                    if isinstance(body, dict)
                    else ""
                )
                if query or semantic_query:

                    def _get_plain():
                        if isinstance(result, ToolInvocationResult):
                            r = result.result
                            return r.get("content", "") if isinstance(r, dict) else r
                        if hasattr(result, "content"):
                            return result.content
                        if isinstance(result, dict):
                            return result.get("content", "")
                        return None

                    def _set_plain(v):
                        if isinstance(result, ToolInvocationResult):
                            if isinstance(result.result, dict):
                                result.result["content"] = v
                            else:
                                result.result = v
                        elif hasattr(result, "content"):
                            result.content = v
                        elif isinstance(result, dict):
                            result["content"] = v

                    plain = _get_plain()
                    if isinstance(plain, str) and plain:
                        filtered = plain
                        if query:
                            filtered = grep_text(filtered, query)
                        if semantic_query:
                            filtered = bm25_rank(filtered, semantic_query)
                        _set_plain(filtered)
            except Exception as e:
                logger.warning(
                    f"[context-optimizer] context-retrieve search failed, "
                    f"returning full content: {e}"
                )

        # Pre-layer 0: headroom lossless compaction of JSON tool results to reduce
        # verbosity before the context optimizer sees the content. Lossless only —
        # discard output carrying an unresolvable <<ccr:>> marker (would need a
        # retrieval tool we don't wire; xpander Layer 1 handles reversible offload).
        if USE_HEADROOM and not function_name.startswith("xp"):
            try:
                if isinstance(result, ToolInvocationResult):
                    compacted = _headroom_compact(result.result)
                    if compacted is not None:
                        result.result = compacted
                elif hasattr(result, "content"):
                    compacted = _headroom_compact(result.content)
                    if compacted is not None:
                        result.content = compacted
            except Exception:
                pass

        # Append stuck warning to tool result so the LLM sees it
        if stuck_warning:
            try:
                if isinstance(result, ToolInvocationResult):
                    result.result = (
                        f"{result.result}\n\n{stuck_warning}"
                        if result.result
                        else stuck_warning
                    )
                elif hasattr(result, "content") and isinstance(result.content, str):
                    result.content = f"{result.content}\n\n{stuck_warning}"
            except Exception:
                pass

        # Inline Layer 1 microcompaction: offload large results to the workspace
        # RIGHT NOW (same turn) so the LLM immediately sees the preview +
        # retrieval pointer instead of waiting for the next compress() cycle.
        # Skipped for CONTEXT_OPTIMIZATION reads (agent asked for full content).
        inline_preview_for_activity: Optional[str] = None
        if not is_context_optimization_read:
            try:
                optimizer = args.get("compression_manager")
                if isinstance(optimizer, XPanderContextOptimizer):
                    # Derive the LLM-facing content string. Mirrors what Layer 1
                    # would see in msg.content after agno serializes our result.
                    llm_content: Any = None
                    if isinstance(result, ToolInvocationResult):
                        llm_content = result.result
                    elif hasattr(result, "content"):
                        llm_content = result.content
                    else:
                        llm_content = result
                    clean_content = unwrap_tool_result_content(llm_content)
                    # eff_name, not function_name: a tool dispatched through
                    # xp_execute_tool would otherwise hit L1's xp* skip and stay
                    # resident in full for the rest of the task.
                    replacement, workspace_path = await optimizer.maybe_offload_content(
                        content=clean_content,
                        tool_name=eff_name,
                    )
                    if replacement is not None:
                        # Agent-gateway sub-tasks: warm the TOOL_CALL_ANALYSIS
                        # summary cache fire-and-forget. Never block the hot path
                        # waiting for it — the summary is used by later retrievals.
                        if is_agent_gateway_task(task):
                            try:
                                asyncio.create_task(
                                    get_tool_call_summary(
                                        task, function_name, arguments, clean_content
                                    )
                                )
                            except Exception as exc:
                                logger.debug(
                                    f"[context-optimizer] gateway summary warm skipped: {exc}"
                                )
                        # Overwrite the tool output so agno stores the preview
                        # + workspace pointer as msg.content.
                        if isinstance(result, ToolInvocationResult):
                            result.result = replacement
                        elif hasattr(result, "content"):
                            try:
                                result.content = replacement
                            except Exception:
                                pass
                        else:
                            result = replacement
                        inline_preview_for_activity = replacement
                        # Prevent the fallback loop from re-offloading.
                        tc_id = None
                        if isinstance(arguments, dict):
                            tc_id = arguments.get("tool_call_id")
                        if not tc_id and activity_request_id:
                            tc_id = activity_request_id
                        if tc_id:
                            optimizer._inline_offloaded_tool_call_ids.add(tc_id)
            except Exception as exc:
                logger.warning(
                    f"[context-optimizer] inline layer 1 offload failed: {exc}"
                )

        # MCP failures arrive as normal ToolResult content ("Error from MCP
        # tool ..."), never as exceptions — classify here so failure
        # accounting (activity is_error, ledger status, error-streak breaker)
        # sees them instead of logging every MCP error as a success.
        result_is_error = _result_is_error(result)
        # Byte-identical output to an earlier call from the same tool moved nothing -
        # tell the model in-band and count it toward the no-progress streak. Reads
        # only: a mutation legitimately returns the same ack twice (equal-size write
        # chunks, repeated upserts), so writes never feed this detector.
        identical_result = (
            not result_is_error
            and (eff_name in _READ_ONLY_TOOLS or _bash_read_only)
            and _record_identical_result(task, eff_name, result)
        )
        warnings = [
            IDENTICAL_RESULT_NOTE if identical_result else None,
            _record_tool_outcome(eff_name, result_is_error),
            # a refused noop / blocked repeat "succeeds", so the error streak never sees it
            _record_no_progress(result, force=identical_result),
            # plan finished -> tell the model in-band and arm the wrap-up budget
            # (effective name: plan tools may arrive via xp_execute_tool)
            _track_plan_complete(task, eff_name, result, result_is_error),
        ]
        streak_warning = "\n\n".join(w for w in warnings if w)
        if streak_warning:
            result = append_to_tool_result(result, streak_warning)

        # Plan-less endgame: advisory only - a repeating nudge, never finalize. Read-heavy
        # work after a write is legitimate at any length; the hard breakers contain storms.
        _log_junk_query(task, eff_name, arguments)
        wrapup_streak = _bump_wrapup_streak(task, eff_name, result_is_error, _bash_read_only)
        if wrapup_streak and wrapup_streak % WRAPUP_GRACE_CALLS == 0:
            result = append_to_tool_result(result, WRAPUP_NUDGE)
            # first nudge at INFO for operators; repeats at DEBUG to keep marathon logs quiet
            wrapup_log = (
                logger.info if wrapup_streak == WRAPUP_GRACE_CALLS else logger.debug
            )
            wrapup_log(
                f"[wrapup-budget] {wrapup_streak} non-mutating calls since the last "
                f"mutation; nudging"
            )

        # Steering: the user's mid-run message rides this tool result; the run is never restarted.
        try:
            pending_steers = await drain_steers(getattr(task, "id", None))
            if pending_steers:
                steer_block = render_steer_block(
                    pending_steers, key=get_steer_key(getattr(task, "id", None))
                )
                if steer_block:
                    result = append_to_tool_result(result, steer_block)
                    _reset_wrapup_streak(task)
                    _reset_plan_churn(task)
                    arm_steer_batch_skip(getattr(task, "id", None))
                    logger.info(
                        f"[steering] delivered {len(pending_steers)} message(s) at the "
                        f"{function_name} boundary for task {getattr(task, 'id', '?')}"
                    )
                    _spawn_bg(report_steer_applied(task, pending_steers))
        except Exception as exc:
            logger.warning(f"[steering] injection failed at {function_name}: {exc}")

        # Emit ToolCallResult (success) using the final post-processed value
        # so the activity-log report matches what the LLM actually sees,
        # including the Layer 1 preview + workspace pointer for large outputs.
        # For CONTEXT_OPTIMIZATION workspace reads we emit the full decrypted
        # content verbatim rather than re-truncating.
        _emit_success_result(
            result,
            is_error=result_is_error,
            skip_truncation=is_context_optimization_read,
            inline_preview=inline_preview_for_activity,
        )

        # ---- Robust-L2: append outcome to action ledger ----------- #
        # Records every success — write/verify/read/plan/internal —
        # under the unified durable record. The classifier in
        # ActionLedger.classify decides class + target + signature.
        # Ledger lives on the task so it survives optimizer
        # replacement across retries. Await directly: aappend is
        # in-memory + queued workspace write, returns fast. Wrapping
        # in create_task means the in-memory append could race the
        # post-arun evidence check.
        if LEDGER_ENABLED and task is not None:
            try:
                ledger = get_attached_ledger(task)
                if ledger is None and xpander_agent is not None:
                    ledger = attach_to_task(task=task, agent=xpander_agent)
                if ledger is not None:
                    entry = build_entry_from_call(
                        tool_name=function_name,
                        arguments=arguments,
                        result=result,
                        status="error" if result_is_error else "ok",
                        tool_call_id=activity_request_id,
                        workspace_offload_path=(
                            inline_preview_for_activity
                            if isinstance(inline_preview_for_activity, str)
                            and "CONTEXT_OPTIMIZATION/" in inline_preview_for_activity
                            else None
                        ),
                    )
                    await ledger.aappend(entry)
            except Exception as exc:
                logger.debug(f"[action-ledger] append failed: {exc}")

        # Return the result
        return result

    if not "tool_hooks" in args:
        args["tool_hooks"] = []

    # disable hooks for NeMo due to issue with tool_hooks and NeMo
    if xpander_agent.using_nemo == False:
        args["tool_hooks"].append(on_tool_call_hook)

    # fix gpt-5 temp
    if args["model"] and args["model"].id and args["model"].id.startswith("gpt-5"):
        del args["model"].temperature

    # configure deep planning guidance
    await _configure_deep_planning_guidance(args=args, agent=xpander_agent, task=task)

    # additional_context is only final here, and agno appends it to the tail of the
    # system message — hand it to the cache wrapper so the stable half above it keeps
    # caching when the tail changes between turns.
    _set_volatile_system_hint(
        args,
        task_id=getattr(task, "id", "") or "",
        agent_id=getattr(xpander_agent, "id", "") or "",
    )

    # Last thing before returning: every prompt section is final here.
    log_prompt_budget(
        args=args,
        namespace=globals(),
        task_id=getattr(task, "id", "") or "",
        agent_id=getattr(xpander_agent, "id", "") or "",
    )
    return args


def _set_volatile_system_hint(
    args: Dict[str, Any], task_id: str = "", agent_id: str = ""
) -> None:
    """Tell the cache wrapper which system-message tail is per-request, and whose run
    this is so its wire-budget line is attributable. Never raises."""
    try:
        from xpander_sdk.modules.backend.frameworks._cache_split import (
            current_prompt_owner,
        )

        current_prompt_owner.set(f"{task_id}:{agent_id}")
        model = args.get("model")
        if model is None or not hasattr(model, "xp_volatile_system"):
            return
        model.xp_volatile_system = args.get("additional_context") or None
    except Exception as exc:
        logger.debug(f"[cache-split] volatile system hint skipped: {exc}")


def _inject_plan_task_id_into_reasoning_tools(toolkit: Any) -> None:
    """Add the ``toolcallplantaskid`` field to the think/analyze tool schemas.

    agno derives these schemas from a fixed entrypoint signature, so we build
    the base schema (``process_entrypoint``), append the field, and set
    ``skip_entrypoint_processing`` so agno does not overwrite it. The field is
    NOT part of the entrypoint signature, so the agno tool hook strips it from
    the call args before dispatch (see the reasoning branch in the hook).
    """
    for fn in getattr(toolkit, "functions", {}).values():
        try:
            fn.process_entrypoint()
            params = fn.parameters or {
                "type": "object",
                "properties": {},
                "required": [],
            }
            props = params.setdefault("properties", {})
            props[TOOL_CALL_PLAN_TASK_ID] = {
                "type": "string",
                "description": (
                    "FULL UUID of the plan step CURRENTLY in progress that this "
                    "reasoning step belongs to - copy the exact 'id' from "
                    "xpcreate_agent_plan's response or xpget_agent_plan. NEVER a "
                    "task or execution id. "
                    "Re-set this on EVERY call and update it the moment you move "
                    "to a new step; it is not a fixed value. Pass an empty string "
                    '"" only if no plan exists yet.'
                ),
            }
            params["required"] = list(
                dict.fromkeys(params.get("required", []) + [TOOL_CALL_PLAN_TASK_ID])
            )
            fn.parameters = params
            fn.skip_entrypoint_processing = True
        except Exception as exc:
            logger.debug(
                f"[deep-planning] reasoning-tool plan id inject skipped: {exc}"
            )


def _should_use_reasoning_tools(agent: Agent, task: Optional[Task]) -> bool:
    """Whether to attach agno think/analyze tools; off for inline-app and email gateway children."""
    if not bool(agent.agno_settings.reasoning_tools_enabled):
        return False
    if not is_agent_gateway_task(task):
        return True
    # should_update_parent mirrors is_async for gateway children (set gateway-side).
    inline_app = bool(getattr(task, "is_app", False)) and not bool(
        getattr(task, "should_update_parent", False)
    )
    is_email = (
        str(getattr(task, "source", "") or "").strip().lower()
        == SourceNodeType.EMAIL.value
    )
    return not (inline_app or is_email)


def _strip_planning_tools_if_inactive(
    args: Dict[str, Any], agent: Agent, task: Optional[Task]
) -> None:
    """Drop the planning tool family from args["tools"] when deep planning isn't active for this task."""
    dp_active = bool(
        agent
        and agent.deep_planning
        and task
        and getattr(task, "deep_planning", None)
        and task.deep_planning.enabled
    )
    must_plan = bool(getattr(task, "must_deep_plan", False)) if task else False
    if dp_active or must_plan:
        return
    # New list — never mutate agent.tools.functions, it's shared across executions.
    args["tools"] = [
        t
        for t in args.get("tools", [])
        if getattr(t, "__name__", getattr(t, "name", "")) not in _PLAN_TOOLS
    ]


async def _configure_deep_planning_guidance(
    args: Dict[str, Any], agent: Agent, task: Optional[Task]
) -> None:
    """Inject plan guidance into ``args`` for a task that must plan before it acts.

    Mutates ``args`` in place (``instructions``, ``additional_context`` and, when
    deep planning is active, ``expected_output``). Stays a coroutine: the plan
    state is refreshed over HTTP, and doing that synchronously re-enters the
    caller's event loop.
    """
    if not (args and agent and task):
        return

    if "instructions" not in args or not args["instructions"]:
        args["instructions"] = ""

    # A must_deep_plan task (e.g. every agent-gateway child) must create + start a plan
    # before any non-plan tool call, or the runtime rejects it with a 400 — but only
    # when plan tools are actually available to the agent.
    plan_tools_present = any(
        getattr(t, "__name__", getattr(t, "name", "")) in _PLAN_TOOLS
        for t in args.get("tools", [])
    )
    must_plan = bool(getattr(task, "must_deep_plan", False)) and plan_tools_present

    deep_planning_active = bool(
        agent.deep_planning and task.deep_planning and task.deep_planning.enabled
    )
    if deep_planning_active:
        # The gateway seeds and starts plans after dispatch, so the local copy is stale.
        await task.areload()

    if not (deep_planning_active or must_plan):
        return

    dp = getattr(task, "deep_planning", None)
    # A plan that already exists AND is started (gateway-seeded, or a retry after the
    # agent created+started one) → execute/complete it; otherwise → create + start it.
    plan_already_started = bool(dp and dp.enabled and dp.started and dp.tasks)

    if plan_already_started:
        if SEEDED_PLAN_INSTRUCTIONS not in args["instructions"]:
            args["instructions"] += SEEDED_PLAN_INSTRUCTIONS
    else:
        if DEEP_PLANNING_INSTRUCTIONS not in args["instructions"]:
            args["instructions"] += DEEP_PLANNING_INSTRUCTIONS
        # parent-reporting / gateway children must create+start before any tool call
        if must_plan and PARENT_UPDATE_PLAN_REQUIREMENT not in args["instructions"]:
            args["instructions"] += PARENT_UPDATE_PLAN_REQUIREMENT

    if deep_planning_active:
        # add the expected output guidance
        if not "expected_output" in args:
            args["expected_output"] = ""
        args["expected_output"] += "\nAll planned tasks completed and marked as done."

    # Seeded instructions reference the plan block, so render it whenever either
    # gate is on (plan_already_started can hold while deep_planning_active is off).
    if deep_planning_active or plan_already_started:
        tasks = (dp.tasks or []) if dp else []
        if tasks:
            # Stable ids + titles only — completion flips would invalidate the cached prefix.
            plan_str = json.dumps([{"id": t.id, "title": t.title} for t in tasks])
            plan_block = (
                f"{PLAN_BLOCK_LABEL} (read live completion status via "
                f"xpget_agent_plan): {plan_str}"
            )
        else:
            plan_block = (
                "No execution plan exists yet — create one with xpcreate_agent_plan."
            )
        # Prepend: the stable plan block sits before volatile compaction/ledger
        # content so plan state changes stop re-tokenizing the cached prefix.
        existing = args.get("additional_context", "") or ""
        args["additional_context"] = (
            f"{plan_block}\n{existing}" if existing else plan_block
        )


# agno tags toolkit-sourced tools (ReasoningTools, MCP, any Toolkit) with
# internal-only orchestration flags. Toolkit.register() sets these via membership
# tests, so they serialize as ``false`` (not ``None``) and survive to_dict()'s
# exclude_none. Strict OpenAI-compatible providers (Cerebras/zai) 400 on these
# unknown props (``wrong_api_format``). agno only strips them for a hardcoded
# provider allowlist (AIMLAPI/Fireworks/Nvidia/VLLM); OpenAILike inherits provider
# "OpenAI" and is not covered. These fields are never part of the OpenAI tool spec,
# so dropping them is safe for every provider.
_AGNO_INTERNAL_TOOL_FIELDS = (
    "requires_confirmation",
    "external_execution",
    "requires_user_input",
    "external_execution_silent",
    "approval_type",
)


def _strip_internal_tool_fields_cls(base):
    """Subclass any agno OpenAI-compatible model class to strip agno-internal tool fields."""

    class XpanderToolFieldStripping(base):
        def _format_tools(self, tools):
            formatted = super()._format_tools(tools)
            for entry in formatted:
                if isinstance(entry, dict) and entry.get("type") == "function":
                    fn = entry.get("function")
                    if isinstance(fn, dict):
                        for key in _AGNO_INTERNAL_TOOL_FIELDS:
                            fn.pop(key, None)
            return formatted

        def get_request_params(
            self, response_format=None, tools=None, tool_choice=None, run_response=None
        ):
            # response_format alongside tools makes many OpenAI-compatible gateways
            # (Kimi/Moonshot via OpenRouter, Cerebras) emit the tool call as JSON
            # CONTENT instead of a function call - the run then dies parsing it as
            # the structured output. Drop response_format when tools ride the
            # request; the JSON-fields prompt block still instructs the final
            # answer's shape and the tolerant parse handles it (fence + repair).
            if tools and response_format is not None:
                response_format = None
            return super().get_request_params(
                response_format=response_format,
                tools=tools,
                tool_choice=tool_choice,
                run_response=run_response,
            )

    return XpanderToolFieldStripping


def _build_openai_like_cls():
    """Return an ``OpenAILike`` subclass that strips agno-internal tool fields.

    Lazy: keeps the agno import optional and inside the model-build path.
    """
    from agno.models.openai.like import OpenAILike

    return _strip_internal_tool_fields_cls(OpenAILike)


async def _aget_org_default_llm_headers(agent: Agent) -> Any:
    """Fetch (60s-cached) the org default LLM extra headers for this tenant."""
    api_client = APIClient(configuration=agent.configuration)
    return await backend_config_cache.get_or_fetch(
        f"org_llm_headers:{scope_token(agent.configuration)}",
        lambda: api_client.make_request(path=APIRoute.GetOrgDefaultLLMExtraHeaders),
    )


# Bound the resolve call so a slow/hung controller can't stall agent construction for the
# APIClient's full timeout. Matches the gateway's dynamic-prompt leg budget.
DYNAMIC_PROMPT_RESOLVE_TIMEOUT_SECONDS = 8


def _compose_dynamic_prompt(base: str, dynamic_text: str, position: str) -> str:
    """Place resolved dynamic text before/after the agent's own instructions.

    Positioning is relative to the identity block (parity with the gateway), not the whole
    assembled prompt: the framework guardrail blocks (grounding, workspace, skills, tools,
    finalize) are appended afterward by design and stay last.
    """
    if not dynamic_text:
        return base
    if position == "before":
        return f"{dynamic_text}\n\n{base}"
    return f"{base}\n\n{dynamic_text}"


async def _aget_dynamic_prompt_text(agent: Agent) -> str:
    """Resolve the agent's dynamic system prompt (run its code, sanitized) via the controller.

    Mirrors the gateway path. The controller endpoint owns execution, secret injection, caching
    and sanitization. Fail-open: any problem returns "" so agent construction never breaks.
    """
    instructions = getattr(agent, "instructions", None)
    if not instructions or not getattr(instructions, "dynamic_prompt_enabled", False):
        return ""
    if not (getattr(instructions, "dynamic_prompt_code", None) or "").strip():
        return ""
    try:
        api_client = APIClient(configuration=agent.configuration)
        result = await asyncio.wait_for(
            api_client.make_request(
                path=APIRoute.ResolveDynamicPrompt.value.format(agent_id=agent.id),
                method="POST",
            ),
            timeout=DYNAMIC_PROMPT_RESOLVE_TIMEOUT_SECONDS,
        )
        text = result.get("text") if isinstance(result, dict) else None
        return text or ""
    except Exception as e:
        logger.warning(f"dynamic prompt resolve failed for agent {agent.id}: {e}")
        return ""


def _load_llm_model(
    agent: Agent,
    override: Optional[Dict[str, Any]] = {},
    task: Optional[Task] = None,
    org_default_llm_headers: Any = None,
) -> Any:
    """
    Load and configure the appropriate LLM model based on the agent's provider configuration.

    This function supports multiple LLM providers including OpenAI, NVIDIA NIM, and Anthropic.
    It handles API key resolution with proper precedence based on the deployment environment
    (xpander.ai Cloud vs local deployment).

    Args:
        agent (Agent): The agent instance containing model configuration.
        override (Optional[Dict[str, Any]]): Optional override parameters that can
            include a pre-configured "model" to bypass the loading logic.

    Returns:
        Any: A configured LLM model instance (OpenAIChat, Nvidia, or Claude).

    Raises:
        NotImplementedError: If the specified provider is not supported.

    Supported Providers:
        - "openai": Uses OpenAIChat with fallback API key resolution
        - "nim": Uses NVIDIA NIM models via Nvidia class
        - "anthropic": Uses Claude models via Anthropic integration
        - "cerebras": Uses Cerebras inference via OpenAILike (OpenAI-compatible)

    API Key Resolution Logic:
        - xpander.ai Cloud: Custom credentials take precedence, fallback to environment
        - Local deployment: Environment variables take precedence, fallback to custom
    """
    if override and "model" in override:
        return override["model"]

    # Attribution sent to LLM providers via the `user` field: org id only. Not
    # agent/user-scoped — those overflow provider identifier limits and fragment
    # accounting; org-level attribution is what we want.
    llm_usage_identifier = agent.organization_id

    # Stable prompt-cache routing key for OpenAI-compatible providers. Keyed on
    # org + agent (NOT user) so the static prefix caches across a given agent's
    # tasks/users; including user_id would fragment the cache per user. Bounded to
    # the provider's 64-char max at each use site via _bounded_prompt_cache_key.
    llm_prompt_cache_key = f"{agent.organization_id}:{agent.id}"

    # set provider from agent
    llm_model_provider = agent.model_provider.lower()
    llm_model_name = agent.model_name.lower()
    llm_reasoning_effort = agent.llm_reasoning_effort

    # override llm settings by task if set
    if task:
        if task.llm_model_provider:
            llm_model_provider = task.llm_model_provider.lower()
        if task.llm_model_name:
            llm_model_name = task.llm_model_name.lower()
        if task.llm_reasoning_effort:
            llm_reasoning_effort = task.llm_reasoning_effort

        # Attachment pipeline becomes capability-aware: to_message/get_images/
        # get_files plan against the model actually running this task.
        try:
            from xpander_sdk.modules.tasks.utils.model_capabilities import (
                get_model_capabilities,
            )

            task._model_capabilities = get_model_capabilities(
                llm_model_provider, llm_model_name
            )
        except Exception as caps_exc:
            logger.debug(f"model capabilities resolution failed: {caps_exc}")

    # flags must follow the task override, or a task-level gpt-5.6 routes to Chat and 400s
    is_gpt_5 = "gpt-5" in llm_model_name
    is_gpt_5_6 = "gpt-5.6" in llm_model_name

    if agent.llm_credentials and isinstance(agent.llm_credentials, dict):
        agent.llm_credentials = LLMCredentials(**agent.llm_credentials)

    is_xpander_cloud = getenv("IS_XPANDER_CLOUD", "false") == "true"
    has_custom_llm_key = (
        True if agent.llm_credentials and agent.llm_credentials.value else False
    )

    oidc_llm_token = None

    # OIDC pre-auth token claim by audience
    if (
        agent
        and agent.pre_auth_audiences
        and agent.use_oidc_pre_auth_token_for_llm
        and agent.oidc_pre_auth_token_llm_audience
        and task
        and task.user_tokens
        and isinstance(task.user_tokens, dict)
        and "oidc_tokens" in task.user_tokens
        and isinstance(task.user_tokens["oidc_tokens"], dict)
    ):
        oidc_llm_token = task.user_tokens["oidc_tokens"].get(
            agent.oidc_pre_auth_token_llm_audience, None
        )

    def get_llm_key(env_var_name: str) -> Optional[str]:
        """
        Resolve API key based on deployment environment and availability.

        Args:
            env_var_name (str): Name of the environment variable containing the API key.

        Returns:
            Optional[str]: The resolved API key or None if not available.
        """

        # return oidc claimed api key
        if oidc_llm_token:
            return oidc_llm_token

        env_llm_key = getenv(env_var_name)

        # If no custom key available, use environment variable
        if not has_custom_llm_key:
            return env_llm_key

        # xpander.ai Cloud: prioritize custom credentials, fallback to environment
        if is_xpander_cloud:
            return agent.llm_credentials.value or env_llm_key
        else:
            # Local deployment: prioritize environment, fallback to custom
            return env_llm_key or agent.llm_credentials.value

    llm_args = {}

    llm_extra_headers = {}

    if oidc_llm_token:
        llm_extra_headers["x-oidc-token"] = oidc_llm_token

    # Org default LLM extra headers (cached: org-scoped, near-static). On the hot
    # build_agent_args path these are awaited upstream and passed in; only fall back
    # to the blocking run_sync fetch for callers that don't (e.g. task.py preview).
    if org_default_llm_headers is None:
        org_default_llm_headers = run_sync(_aget_org_default_llm_headers(agent))

    # set default headers (drop empty/invalid entries from org-level config
    # — see PRO-1300; otherwise provider clients reject the request)
    org_default_llm_headers = sanitize_extra_headers(org_default_llm_headers)
    if org_default_llm_headers:
        llm_extra_headers = {**llm_extra_headers, **org_default_llm_headers}

    # set override by agent (also sanitised)
    if agent.llm_extra_headers and isinstance(agent.llm_extra_headers, dict):
        llm_extra_headers = {
            **llm_extra_headers,
            **sanitize_extra_headers(agent.llm_extra_headers),
        }

    # belt-and-braces: never hand an invalid header to the provider client
    llm_args["extra_headers"] = sanitize_extra_headers(llm_extra_headers)

    if (
        llm_reasoning_effort
        and llm_reasoning_effort != LLMReasoningEffort.Medium
        and llm_model_name
        and is_gpt_5
    ):
        # add, never rebind: a fresh dict here silently dropped extra_headers
        llm_args["reasoning_effort"] = llm_reasoning_effort.value

    if agent.llm_api_base and len(agent.llm_api_base) != 0:
        llm_args["base_url"] = agent.llm_api_base

    # Enable prompt caching on OpenAI-compatible providers. OpenAI-style caching
    # is automatic server-side (prompt >= 1024 tokens); passing `prompt_cache_key`
    # in the request body improves cache routing / hit-rate. Injected via
    # extra_body so it forwards verbatim and providers that don't support it just
    # ignore the extra field. (Anthropic/Bedrock use cache_control/cachePoint;
    # Gemini caches implicitly — handled in their own branches.)
    _OPENAI_COMPATIBLE_PROVIDERS = {
        "openai",
        "bytedance",
        "tzafon_lightcone",
        "cerebras",
        "helicone",
        "nebius",
        "open_router",
        "fireworks",
        "nim",
        "cloudflare_ai_gw",
    }
    if llm_model_provider in _OPENAI_COMPATIBLE_PROVIDERS:
        extra_body = dict(llm_args.get("extra_body") or {})
        extra_body.setdefault(
            "prompt_cache_key", _bounded_prompt_cache_key(llm_prompt_cache_key)
        )
        llm_args["extra_body"] = extra_body

    # OpenAI Provider - supports GPT models with dual API key fallback
    if llm_model_provider == "openai":
        from agno.models.openai import OpenAIChat, OpenAIResponses

        openai_args = {
            "id": llm_model_name,
            # Try xpander.ai-specific key first, fallback to standard OpenAI key
            "api_key": get_llm_key("AGENTS_OPENAI_API_KEY")
            or get_llm_key("OPENAI_API_KEY"),
            "temperature": 0.0,
            "retries": 3,
            "exponential_backoff": True,
            "user": llm_usage_identifier,
            # agno drops a None timeout so the client falls back to its 600s default; lift to 12h
            "client_params": {"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        }

        # if (is gpt-5 and is effort high OR x-high) OR is gpt 5.6  - USE ResponsesAPI
        if (
            is_gpt_5
            and llm_args
            and isinstance(llm_args, dict)
            and "reasoning_effort" in llm_args
            and (
                llm_args["reasoning_effort"] == LLMReasoningEffort.High.value
                or llm_args["reasoning_effort"] == LLMReasoningEffort.XHigh.value
            )
        ) or is_gpt_5_6:
            return OpenAIResponses(**openai_args)

        return OpenAIChat(**openai_args)
    # ByteDance
    elif llm_model_provider == "bytedance":
        OpenAILike = _build_openai_like_cls()

        return OpenAILike(
            id=llm_model_name,
            # Try xpander.ai-specific key first
            api_key=get_llm_key("BYTEDANCE_API_KEY"),
            base_url="https://ark.ap-southeast.bytepluses.com/api/v3",
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # Tzafon LightCone
    elif llm_model_provider == "tzafon_lightcone":
        OpenAILike = _build_openai_like_cls()

        return OpenAILike(
            id=llm_model_name,
            # Try xpander.ai-specific key first
            api_key=get_llm_key("TZAFON_LIGHTCONE_API_KEY"),
            base_url="https://api.tzafon.ai/v1",
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # Cerebras - OpenAI-compatible inference (handled like Tzafon LightCone)
    elif llm_model_provider == "cerebras":
        OpenAILike = _build_openai_like_cls()

        return OpenAILike(
            id=llm_model_name,
            api_key=get_llm_key("CEREBRAS_API_KEY"),
            base_url="https://api.cerebras.ai/v1",
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # Z.ai (Zhipu GLM) - OpenAI-compatible inference
    elif llm_model_provider == "z_ai":
        OpenAILike = _build_openai_like_cls()

        return OpenAILike(
            id=llm_model_name,
            api_key=get_llm_key("Z_AI_API_KEY"),
            base_url="https://api.z.ai/api/paas/v4",
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # Helicone
    elif llm_model_provider == "helicone":
        OpenAILike = _build_openai_like_cls()

        return OpenAILike(
            id=llm_model_name,
            # Try xpander.ai-specific key first, fallback to standard OpenAI key
            api_key=get_llm_key("HELICONE_API_KEY"),
            base_url="https://ai-gateway.helicone.ai/v1",
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # Nebius
    elif llm_model_provider == "nebius":
        from agno.models.nebius import Nebius

        return Nebius(
            id=llm_model_name,
            # Try xpander.ai-specific key first, fallback to standard OpenAI key
            api_key=get_llm_key("NEBIUS_API_KEY"),
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # OpenRouter
    elif llm_model_provider == "open_router":
        from agno.models.openrouter import OpenRouter

        return _strip_internal_tool_fields_cls(OpenRouter)(
            id=llm_model_name,
            # Try xpander.ai-specific key first, fallback to standard OpenAI key
            api_key=get_llm_key("OPENROUTER_API_KEY"),
            # agno's OpenRouter defaults max_tokens to 1024, which many models spend on
            # the preamble/reasoning and hit finish_reason=length BEFORE emitting their
            # tool_calls block - the "says 'on it' then never calls a tool" failure
            max_tokens=LLM_MAX_OUTPUT_TOKENS,
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # Google AI Studio - supports gemini models
    elif llm_model_provider == "google_ai_studio":
        from agno.models.google import Gemini

        del llm_args["extra_headers"]
        return Gemini(
            id=llm_model_name,
            # Try xpander.ai-specific key first, fallback to standard OpenAI key
            api_key=get_llm_key("GOOGLE_API_KEY"),
            retries=3,
            exponential_backoff=True,
            # agno converts this to genai http_options timeout (ms); 12h for long agent turns
            timeout=LLM_REQUEST_TIMEOUT_SECONDS,
            **llm_args,
        )
    # Fireworks AI Provider
    elif llm_model_provider == "fireworks":
        from agno.models.fireworks import Fireworks

        return Fireworks(
            id=llm_model_name,
            # Try xpander.ai-specific key first, fallback to standard OpenAI key
            api_key=get_llm_key("FIREWORKS_API_KEY"),
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # NVIDIA NIM Provider - supports NVIDIA's inference microservices
    elif llm_model_provider == "nim":
        from agno.models.nvidia import Nvidia

        return Nvidia(
            id=llm_model_name,
            api_key=get_llm_key("NVIDIA_API_KEY"),
            temperature=0.0,
            retries=3,
            exponential_backoff=True,
            user=llm_usage_identifier,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
    # Amazon Bedrock Provider
    elif llm_model_provider == "amazon_bedrock":
        # CachingAwsBedrock injects a cachePoint into system + tools so the static
        # prefix is cached (cuts cost on long agentic runs). Keeps bearer-token auth.
        from xpander_sdk.modules.backend.frameworks._bedrock_cache import (
            CachingAwsBedrock,
        )

        environ["AWS_BEARER_TOKEN_BEDROCK"] = get_llm_key(
            "AWS_BEARER_TOKEN_BEDROCK"
        )  # set to env
        del llm_args["extra_headers"]
        if (
            "opus-4-7" not in llm_model_name
            and "opus-4-8" not in llm_model_name
            and "opus-5" not in llm_model_name
            and "sonnet-5" not in llm_model_name
        ):
            llm_args["temperature"] = 0.0

        return CachingAwsBedrock(
            id=llm_model_name,
            retries=3,
            exponential_backoff=True,
            # agno's 8192 default truncates large tool-call JSON mid-stream,
            # dispatching tools with empty args (see truncated-call guard).
            max_tokens=LLM_MAX_OUTPUT_TOKENS,
            **llm_args,
        )

    # Anthropic Provider - supports Claude models
    elif llm_model_provider == "anthropic":
        # CachingClaude adds cache_control on tools + rolling message history so the
        # whole system+tools+conversation prefix is cached (stock Claude caches only
        # the system block); the growing history is the dominant cost on long runs.
        from xpander_sdk.modules.backend.frameworks._anthropic_cache import (
            CachingClaude,
        )

        llm_args["default_headers"] = llm_args["extra_headers"]
        llm_args["default_headers"]["User-Agent"] = llm_usage_identifier
        del llm_args["extra_headers"]
        llm = CachingClaude(
            id=llm_model_name,
            api_key=get_llm_key("ANTHROPIC_API_KEY"),
            temperature=0.0,
            cache_system_prompt=True,
            retries=3,
            exponential_backoff=True,
            # agno's 8192 default truncates large tool-call JSON mid-stream,
            # dispatching tools with empty args (see truncated-call guard).
            max_tokens=LLM_MAX_OUTPUT_TOKENS,
            # anthropic client defaults to a 600s read timeout; lift to 12h for long agent turns
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )
        llm._supports_structured_outputs = lambda: True  # override agno filter
        return llm
    # Azure AI Foundary
    elif llm_model_provider == "azure_ai_foundary":
        # Azure AI Foundary
        from agno.models.azure import AzureAIFoundry

        api_key: str = (
            llm_args.get("extra_headers", {}).get("Authorization", None)
            or llm_args.get("extra_headers", {}).get("authorization", None)
            or get_llm_key("AZURE_API_KEY")
        )
        if not api_key:
            raise ValueError(
                "Azure AI Foundary requires an API Key. via headers (Authorization) or LLM Keys."
            )

        if not "base_url" in llm_args:
            raise ValueError("Azure AI Foundary requires a Base URL.")

        # remove bearer prefix
        api_key = api_key.replace("Bearer ", "").replace("bearer ", "")

        del llm_args["extra_headers"]

        llm_args["azure_endpoint"] = llm_args["base_url"]
        del llm_args["base_url"]

        return AzureAIFoundry(
            azure_endpoint=llm_args["azure_endpoint"],
            id=llm_model_name,
            api_key=api_key,
            temperature=0.0,
            retries=3,
            exponential_backoff=True,
        )
    # Cloudflare AI Gateway
    elif llm_model_provider == "cloudflare_ai_gw":
        OpenAILike = _build_openai_like_cls()

        return OpenAILike(
            id=llm_model_name,
            api_key=get_llm_key("CLOUDFLARE_AI_GW_API_KEY"),
            retries=3,
            exponential_backoff=True,
            client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            **llm_args,
        )

    raise NotImplementedError(
        f"Provider '{llm_model_provider}' is not supported for agno agents."
    )


def _select_compaction_provider(
    agent: Agent,
) -> Optional[Tuple[str, str, str]]:
    """Decide which provider + model the compaction override should use, purely
    from available credentials. Returns ``(provider, model_id, api_key)`` in
    priority order (bedrock → anthropic → openai), or ``None`` when the override
    is disabled or no preferred provider has credentials.

    This is the *selection* contract and contains no model construction, so it
    never raises — the chosen provider depends only on which credentials resolve,
    never on whether an agno client class happens to import/construct.

    Credential precedence mirrors ``_load_llm_model``'s ``get_llm_key`` (xpander
    cloud prioritises the agent's custom key, local prioritises env), but is
    provider-gated: the agent's custom key is only reused for the agent's *own*
    configured provider (it belongs to that provider). "Available" == a key
    resolves for the provider.
    """
    if not COMPACTION_MODEL_OVERRIDE_ENABLED:
        return None

    if agent.llm_credentials and isinstance(agent.llm_credentials, dict):
        agent.llm_credentials = LLMCredentials(**agent.llm_credentials)

    is_xpander_cloud = getenv("IS_XPANDER_CLOUD", "false") == "true"
    agent_provider = (agent.model_provider or "").lower()

    def _avail(provider: str, env_names: List[str]) -> Optional[str]:
        """Resolve a usable key for *provider* following the SDK's default
        precedence; ``None`` when no credential is available."""
        own = (
            agent.llm_credentials.value
            if (
                agent_provider == provider
                and agent.llm_credentials
                and agent.llm_credentials.value
            )
            else None
        )
        env = next((v for v in (getenv(n) for n in env_names) if v), None)
        # Cloud: custom key wins; local: env wins (mirrors get_llm_key).
        return (own or env) if is_xpander_cloud else (env or own)

    # Bearer token only for bedrock, matching _load_llm_model.
    candidates = [
        ("amazon_bedrock", COMPACTION_MODEL_BEDROCK, ["AWS_BEARER_TOKEN_BEDROCK"]),
        ("anthropic", COMPACTION_MODEL_ANTHROPIC, ["ANTHROPIC_API_KEY"]),
        (
            "openai",
            COMPACTION_MODEL_OPENAI,
            ["AGENTS_OPENAI_API_KEY", "OPENAI_API_KEY"],
        ),
    ]
    for provider, model_id, env_names in candidates:
        key = _avail(provider, env_names)
        if key:
            return provider, model_id, key
    return None


def _load_compaction_model(agent: Agent, task: Optional[Task] = None) -> Optional[Any]:
    """Build a dedicated, cheaper model for context-optimizer LLM ops.

    Compaction/summarisation is mechanical work that doesn't need the agent's
    (often expensive, reasoning-heavy) configured model. The provider is chosen
    by ``_select_compaction_provider`` (purely from credentials); this function
    only constructs the agno client for the *already-selected* provider.

    Returns ``None`` when nothing is selected OR when constructing the selected
    provider's client fails — in both cases the optimizer falls back to the
    agent's own model. A construction failure deliberately does NOT downgrade to
    a lower-priority provider: the selection contract must not change because an
    agno class failed to import/construct. The oidc/org-header plumbing from
    ``_load_llm_model`` is intentionally omitted (internal background calls).
    """
    selection = _select_compaction_provider(agent)
    if selection is None:
        logger.info(
            "[context-optimizer] no preferred compaction provider available; "
            "using the agent's own model"
        )
        return None

    provider, model_id, api_key = selection
    try:
        if provider == "amazon_bedrock":
            from xpander_sdk.modules.backend.frameworks._bedrock_cache import (
                CachingAwsBedrock,
            )

            # boto3 reads the bedrock bearer token only from the environment;
            # AwsBedrock exposes no constructor param for it (matches
            # _load_llm_model). The agent's main model load sets this same var.
            # CachingAwsBedrock adds cachePoint injection (system + tools).
            environ["AWS_BEARER_TOKEN_BEDROCK"] = api_key
            model: Any = CachingAwsBedrock(
                id=model_id,
                temperature=0.0,
                retries=3,
                exponential_backoff=True,
            )
        elif provider == "anthropic":
            from xpander_sdk.modules.backend.frameworks._anthropic_cache import (
                CachingClaude,
            )

            model = CachingClaude(
                id=model_id,
                api_key=api_key,
                temperature=0.0,
                cache_system_prompt=True,
                retries=3,
                exponential_backoff=True,
                client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
            )
            model._supports_structured_outputs = lambda: True  # override agno filter
        else:  # openai
            from agno.models.openai import OpenAIChat

            # prompt_cache_key improves OpenAI cache routing (caching itself is
            # automatic server-side); keyed on org+agent to match the main model.
            model = OpenAIChat(
                id=model_id,
                api_key=api_key,
                temperature=0.0,
                retries=3,
                exponential_backoff=True,
                client_params={"timeout": LLM_REQUEST_TIMEOUT_SECONDS},
                extra_body={
                    "prompt_cache_key": _bounded_prompt_cache_key(
                        f"{agent.organization_id}:{agent.id}"
                    )
                },
            )
        logger.info(f"[context-optimizer] compaction model: {provider} ({model_id})")
        return model
    except Exception as exc:
        # Construction of the SELECTED provider failed — fall back to the agent's
        # own model rather than silently downgrading to a different provider.
        logger.warning(
            f"[context-optimizer] compaction model construction failed for "
            f"{provider}: {exc}; using the agent's own model"
        )
        return None


def _configure_output(
    args: Dict[str, Any],
    agent: Agent,
    task: Optional[Task],
    is_member: bool = False,
) -> None:
    if agent.output_format == OutputFormat.Voice:
        args["use_json_mode"] = False
        args["markdown"] = False
        return
    if agent.output.use_json_mode:
        args["use_json_mode"] = True
        args["output_schema"] = agent.output.output_schema
    elif agent.output.is_markdown:
        args["markdown"] = True

    # A member's own configured format still wins above; only the task-level
    # override belongs to the root manager. Applying it to members makes each one
    # render the whole answer into the task schema before the root does it again.
    if is_member:
        return

    if task and task.output_format != agent.output_format:
        if task.output_format == OutputFormat.Json:
            args["use_json_mode"] = True
            args["markdown"] = False
            args["output_schema"] = build_model_from_schema(
                "StructuredOutput",
                task.output_schema,
                inject_workspace_path=False,
            )
        elif task.output_format == OutputFormat.Markdown:
            args["markdown"] = True
        else:
            args["markdown"] = False


def _configure_session_storage(
    args: Dict[str, Any], agent: Agent, task: Optional[Task]
) -> None:
    if not agent.agno_settings.session_storage:
        return

    args["add_history_to_context"] = True
    args["session_id"] = task.id if task else None
    args["user_id"] = (
        task.input.user.id if task and task.input and task.input.user else None
    )

    if agent.agno_settings.session_summaries:
        args["enable_session_summaries"] = True
    if agent.agno_settings.num_history_runs is not None:
        args["num_history_runs"] = agent.agno_settings.num_history_runs
    # 0 is reserved as "unset" (legacy backend default was persisted as 0 and never forwarded).
    max_tool_calls = agent.agno_settings.max_tool_calls_from_history
    if max_tool_calls is not None and max_tool_calls >= 1:
        args["max_tool_calls_from_history"] = max_tool_calls


MEMORY_MAX_CHARS = 300
_MEMORY_FETCH_TIMEOUT_S = 1.5
_MEMORY_PERSIST_TIMEOUT_S = 10
# update/delete block on the controller's verdict, so this bound is what the model waits for
_MEMORY_CONFIRM_TIMEOUT_S = 3
_MEMORY_SCOPES = {"user", "agent"}
_MEMORY_ACTIONS = {"save", "update", "delete"}

# Mirrors the controller's id rule (user_memories/service.py): the <memories> block hands
# out short hex codes, so a dashed task UUID can never be a memory id.
_MEMORY_ID_RE = re.compile(r"^[0-9a-f]{8,32}$")
_MEMORY_BLOCK_ID_RE = re.compile(r"^- \[([0-9a-f]{4,32})\]", re.M)
# Full block line: "- [id] (meta) text" - captures text too, for save-time dedup.
_MEMORY_BLOCK_LINE_RE = re.compile(r"^- \[([0-9a-f]{4,32})\] \([^)]*\) (.+)$", re.M)
# The model's own label saying this write is pointless; the protocol says such a call
# must not be made at all, so enforce it instead of trusting the prose.
# Bare verbs anchor to the label start so a save ABOUT skipping ("Save skip-intro
# preference") is not mistaken for a save the model itself calls skippable.
_MEMORY_SKIP_REASON_RE = re.compile(
    r"^\s*(skip(ping)?|undo|noop|no-op)\b"
    r"|\b(redundant|already (noted|covered|known|saved|recorded)|"
    r"not (durable|needed|saving|worth)|no need)\b",
    re.IGNORECASE,
)

_MEM_ALREADY_KNOWN = (
    "Already known - not saved again. This fact is already in <memories>; re-saving it "
    "changes nothing. Continue with the user's request."
)
_MEM_SELF_SKIP = (
    "No memory was changed: your own reasoning for this call says it is redundant or "
    "skippable, and the protocol for that case is to not make the call at all. Nothing "
    "was written - answer the user."
)


def _normalized_memory_text(text: str) -> str:
    """Whitespace/case-normalized memory text, the same shape the id hash uses."""
    return re.sub(r"\s+", " ", (text or "").strip().lower()).rstrip(".!?")


def _parse_listed_memories(context: str) -> Dict[str, str]:
    """id -> normalized text for every memory line rendered into the <memories> block."""
    return {
        mem_id: _normalized_memory_text(mem_text)
        for mem_id, mem_text in _MEMORY_BLOCK_LINE_RE.findall(context or "")
    }
# Mirrors user_memories/service.py::memory_id_for - the id a save will land on is
# derivable, so it can be handed to the model without waiting for the write.
_MEMORY_ID_NS = uuid.UUID("6b9c9d5e-7a10-4f5f-9b53-2f5b1f7a9e42")
# A task makes at most this many memory WRITES - save, update and delete together. Capping
# only saves left update as an uncapped side door, and a run went through it seven times.
MEMORY_OPS_PER_TASK = 2

_MEM_BAD_ID = (
    "No memory was changed. '{id}' is not a memory id - ids are the short hex codes in "
    "square brackets in the <memories> block. A task or execution id is never a memory id. "
    "Do not retry; if no listed memory matches, there is nothing to change."
)
_MEM_NOT_LISTED = (
    "No memory was changed: no memory with id '{id}' is listed in <memories> for this run. "
    "Do not retry - re-read the block and use an id that appears there, or move on."
)
_MEM_BUDGET = (
    "Not written: this task has already made {n} memory writes, which is the limit - save, "
    "update and delete all count. Durable memories are rare. Do not retry, do not switch to "
    "another action, and do not call another tool to fill the turn: answer the user."
)
_MEM_REPEAT = (
    "No memory was changed: you already made this exact {action} earlier in this task, so "
    "repeating it cannot change anything. The earlier result still stands - answer the user."
)
_MEM_GONE = (
    "No memory was changed: you deleted '{id}' earlier in this task, so it no longer exists. "
    "Do not retry and do not re-save it."
)
_MEM_MISS = (
    "No memory was changed: nothing matched id '{id}', so the {action} did nothing - it may "
    "already be gone, or belong to another user or agent. Do not retry."
)


def _memory_id_for(scope: str, user_id: Optional[str], agent_id: Optional[str], text: str) -> str:
    """The id the controller will store this memory under; must stay identical to its
    `memory_id_for`, or a save would hand the model an id that does not exist."""
    normalized = re.sub(r"\s+", " ", (text or "").strip().lower()).rstrip(".!?")
    return uuid.uuid5(
        _MEMORY_ID_NS, f"{scope}:{user_id or ''}:{agent_id or ''}:{normalized}"
    ).hex


def _sanitize_memory(text: Any) -> str:
    """One-line, tag-free memory text: a stored `</memories>` would otherwise close the
    context block and turn a memory into free-standing instructions for every later run."""
    cleaned = re.sub(r"[<>]", "", str(text or ""))
    return re.sub(r"\s+", " ", cleaned).strip()[:MEMORY_MAX_CHARS]


def _render_memories_block(bundle: Dict[str, Any], declare_only: bool = False) -> str:
    """Render the xpander memories bundle as the context block, or "" when empty."""
    if not bool((bundle.get("settings") or {}).get("enabled", True)):
        return ""
    user_rows = bundle.get("user") or []
    agent_rows = bundle.get("agent") or []
    if not user_rows and not agent_rows:
        return ""

    def _lines(rows: List[Dict[str, Any]], with_writer: bool) -> List[str]:
        out = []
        for row in rows:
            mem_id = str(row.get("memory_id", ""))[:8]
            date = str(row.get("updated_at", ""))[:10]
            # parens stripped so _MEMORY_BLOCK_LINE_RE's ([^)]*) meta group stays parseable
            writer = re.sub(r"[()]", "", _sanitize_memory(row.get("writer_agent_name")))
            meta = f"by {writer}, {date}" if with_writer and writer else date
            out.append(f"- [{mem_id}] ({meta}) {_sanitize_memory(row.get('memory'))}")
        return out

    note = (
        "Durable memories. Do not re-save facts already listed. You have NO memory tool on "
        "this run: to change one, put an entry in the memory_ops field of your final output "
        "(the id is the code in square brackets); the platform applies it after you finish."
        if declare_only
        else "Durable memories. Do not re-save facts already listed; use manage_memory with "
        "the id to update or delete."
    )
    parts = [f'<memories note="{note}">']
    if user_rows:
        parts.append("USER (about this user, shared across all agents):")
        parts.extend(_lines(user_rows, with_writer=True))
    if agent_rows:
        parts.append("AGENT (this agent's own knowledge, all users):")
        parts.extend(_lines(agent_rows, with_writer=False))
    parts.append("</memories>")
    return "\n".join(parts)


def _declares_memory_ops(task: Optional[Task]) -> bool:
    """True when the output schema carries `memory_ops` - the run declares memory changes.

    A gateway-dispatched child writes nothing itself: it names the changes in that field and the
    platform applies them after the run, so it gets no memory tool and cannot loop on one.
    """
    schema = getattr(task, "output_schema", None) if task else None
    if not isinstance(schema, dict):
        return False
    return "memory_ops" in (schema.get("properties") or {})


def _build_memory_tool(
    agent: Agent,
    task: Task,
    listed_ids: Optional[set] = None,
    listed_memories: Optional[Dict[str, str]] = None,
) -> Any:
    """Build the ``manage_memory`` agno Function (save/update/delete, fire-and-forget)."""
    from agno.tools.function import Function

    from xpander_sdk.consts.api_routes import APIRoute
    from xpander_sdk.core.xpander_api_client import APIClient

    user = task.input.user if task.input else None
    user_id = user.id if user else None
    path = APIRoute.UserMemories.value.format(agent_id=agent.id)

    async def _persist(body: Dict[str, Any], timeout: float = _MEMORY_PERSIST_TIMEOUT_S) -> Any:
        # contained + bounded: an unretrieved raise_for_status would otherwise surface as
        # "Task exception was never retrieved", and the client default timeout is 20 min
        try:
            client = APIClient(configuration=agent.configuration)
            return await asyncio.wait_for(
                client.make_request(path=path, method="POST", payload=body),
                timeout=timeout,
            )
        except Exception as e:
            logger.debug(f"[memories] persist failed for agent {agent.id}: {e}")
            return None

    def _task_state(name: str) -> Any:
        return getattr(task, name, None)

    def _remember(name: str, value: Any) -> None:
        try:
            object.__setattr__(task, name, value)
        except Exception:
            pass

    def _entrypoint(payload: Optional[Union[Dict[str, Any], str]] = None) -> str:
        """Apply a memory operation; save is fire-and-forget, update/delete report back."""
        if isinstance(payload, str):
            parsed = parse_structured_string(payload)
            payload = parsed if isinstance(parsed, dict) else {}
        payload = payload or {}
        action = str(payload.get("action", "")).lower()
        scope = str(payload.get("scope", "user")).lower()
        memory = _sanitize_memory(payload.get("memory"))
        memory_id = str(payload.get("memory_id") or "").strip()

        if action not in _MEMORY_ACTIONS:
            return "Invalid action: use save, update or delete."
        if scope not in _MEMORY_SCOPES:
            return "Invalid scope: use user or agent."
        if action in {"save", "update"} and not memory:
            return "Missing memory text."
        if action in {"update", "delete"} and not memory_id:
            return "Missing memory_id (use the id shown in <memories>)."
        if scope == "user" and not user_id:
            return "No user on this run; only agent scope is available."

        mid = memory_id.lower()
        gone = _task_state("_xp_memory_deleted") or set()
        # Every id is checked against what the model was actually shown - that is where the
        # bad ones came from - plus anything this task itself created or removed.
        if action in {"update", "delete"}:
            if not _MEMORY_ID_RE.match(mid):
                return _MEM_BAD_ID.format(id=memory_id[:48])
            if any(g.startswith(mid) or mid.startswith(g) for g in gone):
                return _MEM_GONE.format(id=memory_id[:48])
            # a memory saved earlier in THIS task is legitimate to follow up on, but the
            # block was rendered before it existed
            saved_here = _task_state("_xp_memory_saved") or set()
            known_ids = set(listed_ids or ()) | saved_here
            if known_ids and not any(
                known.startswith(mid) or mid.startswith(known) for known in known_ids
            ):
                return _MEM_NOT_LISTED.format(id=memory_id[:48])

        if action == "save":
            # The model announcing its own write as skippable IS the protocol's
            # "do not make the call" case - refuse before anything is spent.
            headers_obj = payload.get("headers")
            headers = headers_obj if isinstance(headers_obj, dict) else {}
            # per-field so the ^-anchored verbs apply to each label independently
            if any(
                _MEMORY_SKIP_REASON_RE.search(str(headers.get(key) or ""))
                for key in ("toolcallreasoningtitle", "toolcallreasoningdescription")
            ):
                logger.info(
                    f"[memories] save refused for agent {agent.id}: self-labeled skip"
                )
                return _MEM_SELF_SKIP
            # Save-time dedup, mirroring the gateway's find_duplicate_memory: a text
            # already listed - or one that cites a listed memory's id, i.e. restates
            # it - writes nothing. Without this, save+delete of the same junk fact
            # consumed exactly the write budget with zero refusals.
            normalized = _normalized_memory_text(memory)
            known = listed_memories or {}
            if normalized and normalized in known.values():
                return _MEM_ALREADY_KNOWN
            # only an explicit citation ("memory fe40190f ...") counts as a restatement;
            # a bare id substring may be an unrelated hex token like a commit hash
            if any(
                known_id
                and re.search(rf"\bmemor(?:y|ies)\b[^.;]{{0,60}}\b{known_id}", normalized)
                for known_id in known
            ):
                return _MEM_ALREADY_KNOWN

        signature = f"{action}|{scope}|{mid}|{memory.lower()}"
        signatures = _task_state("_xp_memory_writes") or set()
        if signature in signatures:
            return _MEM_REPEAT.format(action=action)

        # every write counts: budgeting only saves left `update` as an uncapped side door
        written = _task_state("_xp_memory_ops") or 0
        if written >= MEMORY_OPS_PER_TASK:
            logger.info(f"[memories] {action} refused for agent {agent.id}: task budget spent")
            return _MEM_BUDGET.format(n=MEMORY_OPS_PER_TASK)
        _remember("_xp_memory_ops", written + 1)
        _remember("_xp_memory_writes", signatures | {signature})

        body = {
            "action": action,
            "scope": scope,
            "memory": memory or None,
            "memory_id": memory_id or None,
            "user_id": user_id,
            "writer_agent_id": agent.id,
            "writer_agent_name": getattr(agent, "name", None) or agent.id,
        }

        if action == "save":
            # The id is deterministic, so it can be handed back without waiting for the
            # write - without it the model reused a LISTED id as a write slot and
            # overwrote an unrelated memory.
            new_id = _memory_id_for(
                scope,
                user_id if scope == "user" else None,
                agent.id if scope == "agent" else None,
                memory,
            )[:8]
            _remember("_xp_memory_saved", (_task_state("_xp_memory_saved") or set()) | {new_id})
            coro = _persist(body)
            try:
                _spawn_bg(coro)
            except RuntimeError:
                # sync entrypoint path (backend.get_args + Agent.run): no running loop here
                run_sync(coro)
            logger.info(f"[memories] save queued for agent {agent.id} scope={scope} id={new_id}")
            return f"Saved [{new_id}]."

        # update/delete block on the verdict: answering from a static dict is what told the
        # model an update had landed on a row it had already deleted.
        result = run_sync(_persist(body, timeout=_MEMORY_CONFIRM_TIMEOUT_S))
        result = result if isinstance(result, dict) else {}
        applied = bool(result.get("applied"))
        logger.info(
            f"[memories] {action} for agent {agent.id} id={mid[:8]} applied={applied}"
        )
        if not applied:
            return _MEM_MISS.format(id=memory_id[:48], action=action)
        if action == "delete":
            _remember("_xp_memory_deleted", gone | {mid})
            return "Deleted."
        # an update rehashes the id when the text changes, so publish where the row lives now
        landed = str(result.get("memory_id") or memory_id)[:8].lower()
        _remember("_xp_memory_saved", (_task_state("_xp_memory_saved") or set()) | {landed})
        previous = str(result.get("previous") or "")
        replaced = f' Replaced: "{previous[:120]}".' if previous else ""
        return f"Updated [{landed}].{replaced}"

    return Function(
        name="manage_memory",
        description=(
            "Persist durable, reusable knowledge. Most tasks write nothing. "
            "save: the user reveals a stable fact about themselves (scope 'user': role, "
            "team, location, how they like answers - shared across ALL their agents), or you "
            "gain reusable know-how this agent should keep (scope 'agent', visible to every "
            "user of this agent): an insight, a recipe, a working approach, a convention, an "
            "environment or tool quirk - e.g. 'we always ship from main', 'that endpoint "
            "needs the org header or it 403s'. THE BEST agent memory is A FIX THAT WORKED: "
            "when a tool failed and you worked out how to make it succeed - the missing "
            "parameter, the auth header it wanted, the order the calls have to go in, the "
            "format it actually accepts, the flag that stopped the timeout - save that in one "
            "sentence, so the next run skips the dead end you already paid for. This applies "
            "ONLY to a real external failure you then made succeed: a platform refusal (a "
            "refused command, a blocked repeat, a budget or duplicate refusal) is not a "
            "fix and never a memory. update/delete: a listed memory "
            "changed or the user asks to forget it - pass its memory_id from <memories>, never "
            "a task or execution id. "
            "NEVER a memory, in EITHER scope: the CONTENT a tool returned during this task - a "
            "search result, an API or DB row, page text, file contents, a price, a weather "
            "reading, a funding figure, a headcount, an address. That is this task's output, "
            "not knowledge about the person and not knowledge about how to work; what you "
            "LEARNED ABOUT DOING THE WORK can be a memory, what you LOOKED UP cannot, however "
            "durable the fact itself looks. The fence is about DATA, never about LESSONS: an "
            "error a tool returned that taught you how to call it correctly is know-how and "
            "belongs in memory; the values it handed back do not. Nor is the request you were "
            "given, anything you just produced for it, or 'the user asked me about X'. "
            "If your own reasoning for the call is 'skip', 'not durable', or a restatement of "
            "this task, do not make the call at all. Would it still matter in a month, on an "
            "unrelated task? If not, do not write. Keep memories short (one concise sentence, "
            f"max {MEMORY_MAX_CHARS} chars). Never store secrets or credentials. Do not "
            "re-save facts already listed in <memories>. "
            f"save, update and delete share ONE budget of {MEMORY_OPS_PER_TASK} writes per "
            "task; when it refuses, answer the user rather than retrying or switching action. "
            "save returns the id it created - use that one for a follow-up. update REPLACES "
            "the whole memory and reports what it replaced, so only update an id whose new "
            "text is about the SAME fact that id already holds. Never delete-then-re-save to "
            "merge, dedup or tidy memories, and never repeat a write you already made. "
            "Wrap arguments in a `payload` object."
        ),
        parameters={
            "type": "object",
            "properties": {
                "payload": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "enum": ["save", "update", "delete"],
                        },
                        "scope": {
                            "type": "string",
                            "enum": ["user", "agent"],
                            "description": "user = about this person, cross-agent. agent = this agent's own knowledge, all users.",
                        },
                        "memory": {
                            "type": "string",
                            "description": "The memory text (save/update). One short sentence.",
                        },
                        "memory_id": {
                            "type": "string",
                            "description": "Id from the <memories> block (update/delete).",
                        },
                        "headers": {
                            "type": "object",
                            "properties": {
                                "toolcallreasoningtitle": {
                                    "type": "string",
                                    "description": 'The concrete action this call performs (max 5 words). If you cannot name one, do not make this call — end the turn with your answer. Example: "Remember user preference".',
                                },
                                "toolcallreasoningdescription": {
                                    "type": "string",
                                    "description": 'One-sentence summary (max 100 characters). Example: "Save that the user prefers Hebrew answers."',
                                },
                            },
                            "required": [
                                "toolcallreasoningtitle",
                                "toolcallreasoningdescription",
                            ],
                        },
                    },
                    "required": ["action", "scope", "headers"],
                },
            },
            "required": ["payload"],
        },
        entrypoint=_entrypoint,
    )


async def _configure_user_memories(
    args: Dict[str, Any], agent: Agent, task: Optional[Task]
) -> None:
    """Wire the xpander memory layer: prepend the <memories> block + inject manage_memory."""
    if agent.agno_settings.learning:
        args["learning"] = True

    user = task.input.user if task and task.input and task.input.user else None
    if user:
        args["additional_context"] = f"User details: {user.model_dump_json()}"

    if not task or agent.is_a_team:
        return

    block = ""
    # the gateway prepends the block into dispatched children's additional_context;
    # fetching again would duplicate it and waste a round-trip
    gateway_passed = "<memories note=" in (task.additional_context or "")
    if not gateway_passed and (user and user.id):
        try:
            from xpander_sdk.consts.api_routes import APIRoute
            from xpander_sdk.core.xpander_api_client import APIClient

            client = APIClient(configuration=agent.configuration)
            bundle = await asyncio.wait_for(
                client.make_request(
                    path=APIRoute.UserMemories.value.format(agent_id=agent.id),
                    query={"user_id": user.id},
                ),
                timeout=_MEMORY_FETCH_TIMEOUT_S,
            )
            if isinstance(bundle, dict):
                block = _render_memories_block(bundle, declare_only=_declares_memory_ops(task))
                # honor the user's master toggle: no block AND no save tool when off
                args["_xpander_memory_enabled"] = bool(
                    (bundle.get("settings") or {}).get("enabled", True)
                )
        except Exception as e:
            logger.debug(f"[memories] fetch skipped for agent {agent.id}: {e}")

    if block:
        existing = args.get("additional_context", "")
        args["additional_context"] = f"{block}\n\n{existing}" if existing else block


async def _attach_async_dependencies(
    args: Dict[str, Any],
    agent: Agent,
    task: Optional[Task],
    model: Any,
    is_async: Optional[bool] = True,
) -> None:
    if agent.agno_settings.session_storage:
        args["db"] = await agent.aget_db(async_db=is_async)


def _configure_knowledge_bases(args: Dict[str, Any], agent: Agent) -> None:
    if agent.knowledge_bases:
        args["knowledge_retriever"] = agent.knowledge_bases_retriever()
        args["search_knowledge"] = True


def _configure_additional_context(
    args: Dict[str, Any], agent: Agent, task: Optional[Task]
) -> None:
    if task and task.additional_context:
        existing = args.get("additional_context", "")
        args["additional_context"] = (
            f"{existing}\n{task.additional_context}"
            if existing
            else task.additional_context
        )

    # 0 == None == unset (legacy backend default, which every default agent carries) -
    # without a fallback here that meant agno ran with NO tool-call ceiling at all
    args["tool_call_limit"] = (
        agent.agno_settings.tool_call_limit or DEFAULT_TOOL_CALL_LIMIT
    )


def _configure_pre_hooks(args: Dict[str, Any], agent: Agent, model: Any) -> None:
    """
    Configure pre-hooks (guardrails) for the agent based on settings.

    Pre-hooks are executed before the agent processes input. This includes
    guardrails like PII detection, prompt injection detection, and content
    moderation that validate or transform input.

    Args:
        args (Dict[str, Any]): Agent configuration arguments to be updated.
        agent (Agent): The agent instance containing pre-hook settings.
    """
    # Add PII detection guardrail with optional masking
    if agent.agno_settings.pii_detection_enabled:
        if "pre_hooks" not in args:
            args["pre_hooks"] = []

        pii_guardrail = PIIDetectionGuardrail(
            mask_pii=agent.agno_settings.pii_detection_mask
        )
        args["pre_hooks"].append(pii_guardrail)

    # Add prompt injection detection guardrail
    if agent.agno_settings.prompt_injection_detection_enabled:
        if "pre_hooks" not in args:
            args["pre_hooks"] = []

        prompt_injection_guardrail = PromptInjectionGuardrail()
        args["pre_hooks"].append(prompt_injection_guardrail)

    # Add OpenAI moderation guardrail
    if agent.agno_settings.openai_moderation_enabled:
        if "pre_hooks" not in args:
            args["pre_hooks"] = []

        moderation_kwargs = {}
        try:
            if model and model.provider == "OpenAI":
                moderation_kwargs["api_key"] = model.api_key
        except:
            pass

        if agent.agno_settings.openai_moderation_categories:
            moderation_kwargs["raise_for_categories"] = (
                agent.agno_settings.openai_moderation_categories
            )

        openai_moderation_guardrail = OpenAIModerationGuardrail(**moderation_kwargs)
        args["pre_hooks"].append(openai_moderation_guardrail)


# cap for the unattended preflight token refresh only - it blocks tool assembly for the run
MCP_TOKEN_REFRESH_TIMEOUT_SECONDS = 45


async def _ensure_remote_mcp_ready(
    mcp: MCPServerDetails,
    transport: str,
    task: Optional[Task] = None,
    auth_events_callback: Optional[Callable] = None,
    agent_id: Optional[str] = None,
) -> Tuple[bool, Optional[str]]:
    """
    Preflight a remote MCP server before handing it to agno. Returns (ready, note):
    ready is False when the server should be skipped for this run, and note carries
    a caller-surfaced explanation when this failure has a specific remedy.

    agno's MCPTools swallows connect failures (only "Cancelled via cancel scope"
    surfaces and the agent silently runs without the tools), so probe with a
    short-lived session to get the real error. When the server rejects our
    stored OAuth token (401/403), force a refresh (which invalidates the token
    and falls back to a re-login event on failure) and probe once more.

    Failure handling: nothing here raises. Every failure - auth or transport -
    returns False so a single bad server is skipped without failing the whole tool
    build, and is marked failed so sibling/subsequent tasks skip the re-probe.

    Short-TTL process caches skip the probe when a recent task already confirmed
    this exact (agent, server, token) healthy (or unreachable).
    """
    if getenv("XPANDER_MCP_STRICT_INIT", "true").lower() != "true":
        return True, None

    if probe_recently_ok(agent_id, mcp.url, mcp.headers):
        return True, None

    if probe_recently_failed(agent_id, mcp.url, mcp.headers):
        return False, None  # a recent task already found this server unreachable

    probe_error = await probe_mcp_server(
        url=mcp.url, headers=mcp.headers, transport=transport
    )
    if probe_error is None:
        mark_probe_ok(agent_id, mcp.url, mcp.headers)
        return True, None

    can_heal = (
        is_mcp_auth_error(probe_error)
        and task is not None
        and task.input
        and task.input.user
        and task.input.user.id
    )
    if can_heal:
        logger.warning(
            f"MCP server {mcp.url} requires authentication ({probe_error}); starting OAuth flow"
        )
        # the server demanded auth regardless of the configured auth_type; backend
        # discovery decides whether it actually supports OAuth2 (NOT_SUPPORTED otherwise)
        mcp.auth_type = MCPServerAuthType.OAuth2
        try:
            # A refresh is a machine round-trip. If it degrades into the interactive
            # login poll (MAX_WAIT_FOR_LOGIN, 10 min) it would stall tool assembly for
            # every task on this agent, so cap it here and skip the server instead.
            auth_result = await asyncio.wait_for(
                authenticate_mcp_server(
                    mcp_server=mcp,
                    task=task,
                    user_id=task.input.user.id,
                    auth_events_callback=auth_events_callback,
                    force_refresh=True,
                ),
                timeout=MCP_TOKEN_REFRESH_TIMEOUT_SECONDS,
            )
        except asyncio.TimeoutError:
            logger.warning(
                f"MCP server '{mcp.name or mcp.url}' token refresh exceeded "
                f"{MCP_TOKEN_REFRESH_TIMEOUT_SECONDS}s; skipping this tool for the run"
            )
            auth_result = None
        if auth_result and auth_result.type == MCPOAuthResponseType.TOKEN_READY:
            mcp.api_key = auth_result.data.access_token
            mcp.headers["Authorization"] = f"Bearer {mcp.api_key}"
            probe_error = await probe_mcp_server(
                url=mcp.url, headers=mcp.headers, transport=transport
            )
            if probe_error is None:
                # headers now carry the refreshed token, so this keys a fresh entry
                mark_probe_ok(agent_id, mcp.url, mcp.headers)
                return True, None

    # Auth-related failure the heal couldn't fix -> skip with a note that names the remedy.
    # This must NOT raise: a single org MCP with stale credentials would otherwise sink every
    # unrelated task on the agent, since the caller's gather has no per-server isolation.
    if is_mcp_auth_error(probe_error):
        mark_probe_failed(agent_id, mcp.url, mcp.headers)
        logger.warning(
            f"MCP server '{mcp.name or mcp.url}' needs re-authentication "
            f"({type(probe_error).__name__}: {probe_error}); skipping this tool for the run"
        )
        return False, (
            f"{mcp.name or mcp.url}: sign-in required - reconnect it in agent settings. "
            f"Its tools are unavailable this run."
        )

    # Non-auth transport failure (timeout / connection / 5xx) -> skip this tool for
    # the run so one bad server can't sink the rest; cache the failure to avoid a
    # per-task re-probe storm.
    mark_probe_failed(agent_id, mcp.url, mcp.headers)
    logger.warning(
        f"MCP server '{mcp.name or mcp.url}' preflight failed ({type(probe_error).__name__}: {probe_error}); "
        f"skipping this tool for the run"
    )
    return False, None


async def _resolve_agent_tools(
    agent: Agent,
    task: Optional[Task] = None,
    auth_events_callback: Optional[Callable] = None,
    skipped_notes: Optional[List[str]] = None,
) -> List[Any]:
    # Skipped-MCP notes surfaced to the agent (so it can tell the user a capability
    # is unavailable) — caller passes a list to receive them; else collect locally.
    notes = skipped_notes if skipped_notes is not None else []

    # Dynamic mode collapses MCP tools into the same meta-tool disclosure as the
    # xpander catalog: the SDK connects each server here, hides its tools from the
    # LLM, and exposes them via xp_search/get/execute. Per-run reset because the
    # repo can be reused across tasks in a long-lived worker.
    use_dynamic = bool(getattr(agent, "use_dynamic_tools", False))
    if use_dynamic:
        agent.tools._dynamic_mcp_proxies.clear()
        agent.tools._dynamic_mcp_toolkits.clear()
        agent.tools._dynamic_inspected.clear()

    mcp_servers = agent.mcp_servers

    # combine task mcps and agent mcps
    if task and task.mcp_servers:
        mcp_servers.extend(task.mcp_servers)

    if not mcp_servers:
        return agent.tools.functions

    # fix pydantic issue if needed
    mcp_servers = [
        MCPServerDetails(**mcp) if isinstance(mcp, dict) else mcp for mcp in mcp_servers
    ]

    # Import MCP only if mcp_servers is present
    from agno.tools.mcp import (
        MCPTools,
        SSEClientParams,
        StreamableHTTPClientParams,
    )
    from mcp import StdioServerParameters

    is_xpander_cloud = getenv("IS_XPANDER_CLOUD", "false") == "true"

    async def _finalize_toolkit(
        toolkit: MCPTools, server_name: str, server_url: Optional[str] = None
    ) -> Optional[MCPTools]:
        """Non-dynamic: return the toolkit for agno to own (today's behavior).
        Dynamic: connect + enumerate now, register proxies, keep the toolkit out of
        the agent's tools (hidden from the LLM), and return None. The SDK owns the
        session; the worker closes it post-run."""
        if not use_dynamic:
            return toolkit
        try:
            await toolkit.connect()
        except (Exception, BaseException) as exc:
            logger.warning(
                f"[dynamic-mcp] connect failed for '{server_name}': "
                f"{type(exc).__name__}: {exc}"
            )
            try:
                await toolkit.close()
            except (Exception, BaseException):
                pass
            notes.append(
                f"{server_name}: temporarily unavailable (could not connect this run)."
            )
            return None
        if not getattr(toolkit, "initialized", False) or not toolkit.functions:
            try:
                await toolkit.close()
            except (Exception, BaseException):
                pass
            if not getattr(toolkit, "initialized", False):
                notes.append(
                    f"{server_name}: temporarily unavailable (could not connect this run)."
                )
            return None
        proxies = build_mcp_proxies(
            toolkit, server_name=server_name, server_url=server_url
        )
        agent.tools._dynamic_mcp_proxies.extend(proxies)
        agent.tools._dynamic_mcp_toolkits.append(toolkit)
        logger.info(
            f"[dynamic-mcp] collapsed {len(proxies)} tools from '{server_name}' "
            f"behind the dynamic meta-tools"
        )
        return None

    # Build one MCPTools per server. Remote servers each run a preflight probe
    # (~100-800ms); gathering them concurrently makes the wall-time the slowest
    # probe instead of their sum. Returns None for servers we deliberately skip.
    async def _build_mcp_tool(mcp: MCPServerDetails) -> Optional[MCPTools]:
        transport = mcp.transport.value.lower()
        if mcp.type == MCPServerType.Local:

            # protection for serverless xpander
            is_aws_mcp = (
                True if mcp.command and "aws-api-mcp-server" in mcp.command else False
            )
            if is_aws_mcp and is_xpander_cloud:
                logger.warning(
                    f"skipping aws mcp on agent {agent.id} due to xpander serverless"
                )
                return None

            if not (mcp.command or "").strip():
                logger.warning(
                    f"MCP server '{mcp.name or 'local'}' is type=local with no command; skipping"
                )
                notes.append(
                    f"{mcp.name or 'local MCP server'}: misconfigured (no command to run). "
                    f"Fix it in agent settings."
                )
                return None

            command_parts = shlex.split(mcp.command)
            return await _finalize_toolkit(
                MCPTools(
                    # literal stdio: keeps even a hand-built (unvalidated) details object safe
                    transport="stdio",
                    server_params=StdioServerParameters(
                        command=command_parts[0],
                        args=command_parts[1:],
                        env=mcp.env_vars,
                    ),
                    include_tools=mcp.allowed_tools or None,
                    timeout_seconds=120,
                    tool_name_prefix="mcp_tool",
                ),
                mcp.name or mcp.command,
                None,
            )
        elif mcp.url:
            params_cls = (
                SSEClientParams
                if mcp.transport == MCPServerTransport.SSE
                else StreamableHTTPClientParams
            )

            if not mcp.headers:
                mcp.headers = {}

            oidc_mcp_token = None
            # OIDC pre-auth token claim by audience
            if (
                agent
                and agent.pre_auth_audiences
                and agent.oidc_pre_auth_token_mcp_audience
                and task
                and task.user_tokens
                and isinstance(task.user_tokens, dict)
                and "oidc_tokens" in task.user_tokens
                and isinstance(task.user_tokens["oidc_tokens"], dict)
            ):
                oidc_mcp_token = task.user_tokens["oidc_tokens"].get(
                    agent.oidc_pre_auth_token_mcp_audience, None
                )
                if oidc_mcp_token and oidc_mcp_token != "__none__":
                    mcp.api_key = oidc_mcp_token

            if not oidc_mcp_token:
                # handle mcp auth
                if mcp.auth_type == MCPServerAuthType.OAuth2:
                    if not task:
                        raise ValueError(
                            "MCP server with OAuth authentication detected but task not sent"
                        )

                    # check if we have user tokens for this mcp
                    graph_item = next(
                        (
                            gi
                            for gi in agent.graph.items
                            if gi.type == AgentGraphItemType.MCP
                            and gi.settings
                            and gi.settings.mcp_settings
                            and gi.settings.mcp_settings.url
                            and gi.settings.mcp_settings.url == mcp.url
                        ),
                        None,
                    )
                    if (
                        graph_item
                        and task.user_tokens
                        and isinstance(task.user_tokens, dict)
                        and graph_item.id in task.user_tokens
                    ):
                        if isinstance(task.user_tokens[graph_item.id], dict):
                            graph_item_headers = task.user_tokens[graph_item.id]
                            mcp.headers = graph_item_headers
                            mcp.api_key = "__bypass__"
                        else:
                            mcp.api_key = task.user_tokens[graph_item.id]

                    if not mcp.api_key:
                        if not task.input.user or not task.input.user.id:
                            # No user to authenticate -> the tool can't work this run.
                            # Skip it (don't error every dispatch) but tell the agent
                            # so it can explain to the user it needs to sign in / connect.
                            logger.warning(
                                f"MCP server '{mcp.name or mcp.url}' needs an authenticated user "
                                f"but the task has none; skipping this tool for the run"
                            )
                            notes.append(
                                f"{mcp.name or mcp.url}: unavailable - requires a signed-in user "
                                f"(this run has no user). If asked to use it, tell the user it needs "
                                f"authentication/connection."
                            )
                            return None

                        auth_result: MCPOAuthGetTokenResponse = (
                            await authenticate_mcp_server(
                                mcp_server=mcp,
                                task=task,
                                user_id=task.input.user.id,
                                auth_events_callback=auth_events_callback,
                            )
                        )
                        # Auth failures skip the server with a note instead of raising:
                        # a raise here propagates through the gather and kills the whole
                        # tool build, so one broken MCP would sink every unrelated task.
                        auth_failure = None
                        if (
                            auth_result
                            and auth_result.data
                            and isinstance(
                                auth_result.data, MCPOAuthGetTokenGenericResponse
                            )
                            and auth_result.data.message
                        ):
                            auth_failure = auth_result.data.message
                        elif not auth_result:
                            auth_failure = "authentication failed"
                        elif auth_result.type != MCPOAuthResponseType.TOKEN_READY:
                            auth_failure = "authentication timed out (sign-in not completed)"
                        if auth_failure:
                            logger.warning(
                                f"MCP server '{mcp.name or mcp.url}' authentication failed "
                                f"({auth_failure}); skipping this tool for the run"
                            )
                            # carry the real reason - "sign-in required" would mislead when the
                            # server e.g. doesn't support OAuth and needs an API key instead
                            notes.append(
                                f"{mcp.name or mcp.url}: authentication failed ({auth_failure}) - "
                                f"fix its auth in agent settings. Its tools are unavailable this run."
                            )
                            return None
                        mcp.api_key = auth_result.data.access_token

            # check if we have user tokens for this mcp
            graph_item = next(
                (
                    gi
                    for gi in agent.graph.items
                    if gi.type == AgentGraphItemType.MCP
                    and gi.settings
                    and gi.settings.mcp_settings
                    and gi.settings.mcp_settings.url
                    and gi.settings.mcp_settings.url == mcp.url
                ),
                None,
            )
            if (
                graph_item
                and task.user_tokens
                and isinstance(task.user_tokens, dict)
                and graph_item.id in task.user_tokens
            ):
                if isinstance(task.user_tokens[graph_item.id], dict):
                    graph_item_headers = task.user_tokens[graph_item.id]
                    mcp.headers = graph_item_headers
                elif not mcp.api_key:
                    mcp.api_key = task.user_tokens[graph_item.id]

            if mcp.api_key and mcp.api_key != "__bypass__":
                mcp.headers["Authorization"] = f"Bearer {mcp.api_key}"

            ready, ready_note = await _ensure_remote_mcp_ready(
                mcp=mcp,
                transport=transport,
                task=task,
                auth_events_callback=auth_events_callback,
                agent_id=agent.id,
            )
            if not ready:
                notes.append(
                    ready_note
                    or f"{mcp.name or mcp.url}: temporarily unavailable (could not connect this run)."
                )
                return None

            return await _finalize_toolkit(
                MCPTools(
                    transport=transport,
                    server_params=params_cls(
                        url=mcp.url,
                        headers=mcp.headers,
                        sse_read_timeout=1200,
                        timeout=1200,
                    ),
                    include_tools=mcp.allowed_tools or None,
                    timeout_seconds=120,
                    tool_name_prefix="mcp_tool",
                ),
                mcp.name or mcp.url,
                mcp.url,
            )

        # Remote entry with no url: a ghost registry reference (the registry row was
        # deleted, the graph item still points at it). Losing a capability silently
        # is worse than admitting it, so leave a note.
        notes.append(
            f"{mcp.name or 'an MCP server'}: no longer available (its registration was "
            f"removed). Detach it in agent settings."
        )
        return None

    # One raising server (agno constructor errors, unexpected connect faults) must not
    # sink the servers that built fine - convert stragglers into skip-with-note.
    built = await asyncio.gather(
        *(_build_mcp_tool(mcp) for mcp in mcp_servers), return_exceptions=True
    )
    for mcp, outcome in zip(mcp_servers, built):
        if isinstance(outcome, BaseException):
            # keep the traceback: an unexpected constructor fault must stay diagnosable
            logger.opt(exception=outcome).warning(
                f"MCP server '{mcp.name or mcp.url or mcp.command}' failed to build "
                f"({type(outcome).__name__}: {outcome}); skipping this tool for the run"
            )
            notes.append(
                f"{mcp.name or mcp.url or 'an MCP server'}: misconfigured or unreachable - "
                f"fix it in agent settings. Its tools are unavailable this run."
            )
    mcp_tools: List[MCPTools] = [
        tool for tool in built if tool is not None and not isinstance(tool, BaseException)
    ]

    return agent.tools.functions + mcp_tools


# Model-id → context window (in tokens). Used to size the L2 trigger so it
# fires before the provider hard-limits the request.
#
# Resolution order in ``_detect_context_window``:
#   1) Exact match in ``_MODEL_CONTEXT_WINDOWS_EXACT`` (authoritative).
#   2) Case-insensitive exact match (handles Nebius mixed-case ids).
#   3) Ordered substring fallback in ``_MODEL_CONTEXT_WINDOWS_SUBSTRING``
#      (most-specific first).
#   4) Default 200K with a warning log so misses are triagable.
#
# The exact map is sourced from the xpander platform model catalog and must
# stay in sync when models are added. The substring fallback catches variants
# (cross-region prefixes, OpenRouter ``provider/model`` form, ``[1m]``
# suffixes) without forcing every variant to be explicitly enumerated.
_MODEL_CONTEXT_WINDOWS_EXACT: Dict[str, int] = {
    # ---- 10M ----
    "meta.llama4-scout-17b-instruct-v1:0": 10_000_000,
    "meta/llama-4-scout-17b-16e-instruct": 10_000_000,
    "meta-llama/llama-4-scout": 10_000_000,
    # ---- 4M (MiniMax-01) ----
    "minimax/minimax-01": 4_000_000,
    # ---- 1M+ ----
    "gpt-4.1": 1_047_576,
    "gpt-4.1-mini": 1_047_576,
    "openai/gpt-4.1": 1_047_576,
    "openai/gpt-4.1-mini": 1_047_576,
    "openai/gpt-4.1-nano": 1_047_576,
    # Anthropic Bedrock global cross-region — declared 1M in catalog
    "global.anthropic.claude-opus-5": 1_000_000,
    "global.anthropic.claude-opus-4-8": 1_000_000,
    "global.anthropic.claude-opus-4-7": 1_000_000,
    "global.anthropic.claude-opus-4-6-v1": 1_000_000,
    "global.anthropic.claude-sonnet-5": 1_000_000,
    "global.anthropic.claude-sonnet-4-6": 1_000_000,
    # Anthropic direct (Bedrock catalog declares 1M for these next-gen IDs)
    "claude-opus-5": 1_000_000,
    "claude-opus-4-8": 1_000_000,
    "claude-opus-4-7": 1_000_000,
    "claude-opus-4-6": 1_000_000,
    "claude-sonnet-5": 1_000_000,
    "claude-sonnet-4-6": 1_000_000,
    # Google Gemini (all current public models = 1M+)
    "gemini-2.0-flash": 1_000_000,
    "gemini-2.0-flash-lite": 1_000_000,
    "gemini-2.5-pro": 1_000_000,
    "gemini-3-pro-preview": 1_000_000,
    "google/gemini-2.0-flash-001": 1_000_000,
    "google/gemini-2.0-flash-lite-001": 1_000_000,
    "google/gemini-2.0-flash-exp:free": 1_000_000,
    "google/gemini-2.5-flash": 1_000_000,
    "google/gemini-2.5-flash-lite": 1_000_000,
    "google/gemini-2.5-flash-preview-09-2025": 1_000_000,
    "google/gemini-2.5-flash-lite-preview-09-2025": 1_000_000,
    "google/gemini-2.5-flash-image": 1_000_000,
    "google/gemini-2.5-flash-image-preview": 1_000_000,
    "google/gemini-2.5-pro": 1_000_000,
    "google/gemini-2.5-pro-preview": 1_000_000,
    "google/gemini-2.5-pro-preview-05-06": 1_000_000,
    "google/gemini-3-pro-preview": 1_000_000,
    "google/gemini-3-pro-image-preview": 1_000_000,
    # Amazon Nova
    "amazon.nova-2-lite-v1:0": 1_000_000,
    "amazon.nova-premier-v1:0": 1_000_000,
    "amazon/nova-premier-v1": 1_000_000,
    # Meta Llama 4 Maverick
    "meta.llama4-maverick-17b-instruct-v1:0": 1_000_000,
    "meta/llama-4-maverick-17b-128e-instruct": 1_000_000,
    "meta-llama/llama-4-maverick": 1_000_000,
    # Qwen3 Max
    "qwen/qwen3-max": 1_000_000,
    "qwen/qwen-turbo": 1_000_000,
    "qwen/qwen-plus-2025-07-28": 1_000_000,
    "qwen/qwen-plus-2025-07-28:thinking": 1_000_000,
    "minimax/minimax-m1": 1_000_000,
    # ---- 400K (GPT-5 family) ----
    "gpt-5": 400_000,
    "gpt-5-mini": 400_000,
    "gpt-5-nano": 400_000,
    "gpt-5.1": 400_000,
    "gpt-5.2": 400_000,
    "gpt-5.3-chat-latest": 400_000,
    "gpt-5.4": 400_000,
    "gpt-5.5": 400_000,
    "openai/gpt-5": 400_000,
    "openai/gpt-5-chat": 400_000,
    "openai/gpt-5-mini": 400_000,
    "openai/gpt-5-nano": 400_000,
    "openai/gpt-5.1": 400_000,
    "openai/gpt-5.1-chat": 400_000,
    "openai/gpt-5.1-codex": 400_000,
    "openai/gpt-5.1-codex-mini": 400_000,
    "openai/gpt-5-codex": 400_000,
    "openai/gpt-5-pro": 400_000,
    "openai/gpt-5-image": 400_000,
    "openai/gpt-5-image-mini": 400_000,
    # ---- 300K (Nova Pro/Lite) ----
    "amazon.nova-pro-v1:0": 300_000,
    "amazon.nova-lite-v1:0": 300_000,
    "amazon/nova-pro-v1": 300_000,
    "amazon/nova-lite-v1": 300_000,
    # ---- 256K-262K ----
    "tzafon.northstar-cua-fast-1.6": 256_000,
    "fireworks/kimi-k2-instruct-0905": 262_000,
    "moonshotai.kimi-k2.5": 256_000,
    "moonshot.kimi-k2-thinking": 256_000,
    "moonshotai/Kimi-K2-Instruct": 256_000,
    "moonshotai/Kimi-K2-Thinking": 256_000,
    "moonshotai/kimi-k2-0905": 256_000,
    "moonshotai/kimi-k2-0905:exacto": 256_000,
    "moonshotai/kimi-k2": 256_000,
    "moonshotai/kimi-k2:free": 256_000,
    "moonshotai/kimi-k2-thinking": 256_000,
    "moonshotai/kimi-linear-48b-a3b-instruct": 256_000,
    "moonshotai/kimi-dev-72b": 256_000,
    "mistral.mistral-large-3-675b-instruct": 256_000,
    "mistral.devstral-2-123b": 256_000,
    "qwen.qwen3-235b-a22b-2507-v1:0": 256_000,
    "qwen.qwen3-coder-480b-a35b-v1:0": 256_000,
    "qwen/qwen3-coder": 256_000,
    "qwen/qwen3-coder:free": 256_000,
    "qwen/qwen3-coder:exacto": 256_000,
    "qwen/qwen3-coder-plus": 256_000,
    "qwen/qwen3-coder-flash": 256_000,
    "qwen/qwen3-coder-30b-a3b-instruct": 256_000,
    "fireworks/qwen3-235b-a22b-thinking-2507": 256_000,
    "fireworks/qwen3-235b-a22b-instruct-2507": 256_000,
    "x-ai/grok-4": 256_000,
    "x-ai/grok-4-fast": 256_000,
    "x-ai/grok-4.1-fast:free": 256_000,
    "x-ai/grok-code-fast-1": 256_000,
    "ai21/jamba-large-1.7": 256_000,
    "ai21/jamba-mini-1.7": 256_000,
    "mistralai/codestral-2501": 256_000,
    "mistralai/codestral-2508": 256_000,
    "cohere/command-a": 256_000,
    # ---- 200K-204K (Z.AI GLM 4.7, MiniMax, Claude 4.x default) ----
    "zai-glm-4.7": 200_000,  # Cerebras model id
    "zai.glm-4.7": 203_000,
    "zai.glm-4.7-flash": 203_000,
    "glm-4-7-251222": 204_000,
    "z-ai/glm-4.7": 203_000,
    "minimax.minimax-m2.5": 196_000,
    "minimax.minimax-m2.1": 196_000,
    "minimax/minimax-m2": 196_000,
    "z-ai/glm-4.6": 200_000,
    "z-ai/glm-4.6:exacto": 200_000,
    "fireworks/glm-4p6": 200_000,
    # Anthropic Bedrock 200K
    "global.anthropic.claude-opus-4-5-20251101-v1:0": 200_000,
    "global.anthropic.claude-sonnet-4-5-20250929-v1:0": 200_000,
    "global.anthropic.claude-haiku-4-5-20251001-v1:0": 200_000,
    "anthropic.claude-opus-4-1-20250805-v1:0": 200_000,
    "anthropic.claude-opus-4-20250514-v1:0": 200_000,
    "anthropic.claude-sonnet-4-20250514-v1:0": 200_000,
    "anthropic.claude-3-5-haiku-20241022-v1:0": 200_000,
    "anthropic.claude-3-haiku-20240307-v1:0": 200_000,
    # Anthropic direct 200K
    "claude-opus-4-5": 200_000,
    "claude-sonnet-4-5": 200_000,
    "claude-opus-4": 200_000,
    "claude-sonnet-4": 200_000,
    "claude-3-7-sonnet-20250219": 200_000,
    "claude-3-5-sonnet-20241022": 200_000,
    # OpenRouter Anthropic
    "anthropic/claude-opus-4.5": 200_000,
    "anthropic/claude-sonnet-4.5": 200_000,
    "anthropic/claude-opus-4.1": 200_000,
    "anthropic/claude-opus-4": 200_000,
    "anthropic/claude-sonnet-4": 200_000,
    "anthropic/claude-haiku-4.5": 200_000,
    "anthropic/claude-3.7-sonnet": 200_000,
    "anthropic/claude-3.7-sonnet:thinking": 200_000,
    "anthropic/claude-3.5-haiku": 200_000,
    "anthropic/claude-3.5-haiku-20241022": 200_000,
    "anthropic/claude-3.5-sonnet": 200_000,
    "anthropic/claude-3-haiku": 200_000,
    "anthropic/claude-3-opus": 200_000,
    # OpenAI o-series (all 200K)
    "o3": 200_000,
    "o4": 200_000,
    "openai/o1": 200_000,
    "openai/o1-pro": 200_000,
    "openai/o3": 200_000,
    "openai/o3-pro": 200_000,
    "openai/o3-mini": 200_000,
    "openai/o3-mini-high": 200_000,
    "openai/o4-mini": 200_000,
    "openai/o4-mini-high": 200_000,
    "openai/o3-deep-research": 200_000,
    "openai/o4-mini-deep-research": 200_000,
    "perplexity/sonar-pro": 200_000,
    "perplexity/sonar-pro-search": 200_000,
    "microsoft/mai-ds-r1": 160_000,
    # ---- 131K-128K ----
    # GPT-4 family
    "gpt-4o": 128_000,
    "gpt-4o-mini": 128_000,
    "gpt-4-turbo": 128_000,
    "openai/gpt-4o": 128_000,
    "openai/gpt-4o-mini": 128_000,
    "openai/gpt-4o-mini-2024-07-18": 128_000,
    "openai/gpt-4o-2024-05-13": 128_000,
    "openai/gpt-4o-2024-08-06": 128_000,
    "openai/gpt-4o-2024-11-20": 128_000,
    "openai/gpt-4o:extended": 128_000,
    "openai/gpt-4o-audio-preview": 128_000,
    "openai/gpt-4o-mini-search-preview": 128_000,
    "openai/gpt-4o-search-preview": 128_000,
    "openai/gpt-4-turbo": 128_000,
    "openai/gpt-4-turbo-preview": 128_000,
    "openai/gpt-4-1106-preview": 128_000,
    "openai/chatgpt-4o-latest": 128_000,
    "openai/codex-mini": 128_000,
    # Llama (default 128K, smaller variants explicit)
    "meta/llama-3.1-8b-instruct": 128_000,
    "meta/llama-3.1-70b-instruct": 128_000,
    "meta/llama-3.1-405b-instruct": 128_000,
    "meta/llama-3.2-1b-instruct": 128_000,
    "meta/llama-3.2-3b-instruct": 128_000,
    "meta/llama-3.3-70b-instruct": 128_000,
    "meta.llama3-1-405b-instruct-v1:0": 128_000,
    "meta.llama3-1-70b-instruct-v1:0": 128_000,
    "meta.llama3-1-8b-instruct-v1:0": 128_000,
    "us.meta.llama3-2-90b-instruct-v1:0": 128_000,
    "us.meta.llama3-2-11b-instruct-v1:0": 128_000,
    "us.meta.llama3-3-70b-instruct-v1:0": 128_000,
    "meta-llama/Meta-Llama-3.1-8B-Instruct": 128_000,
    "meta-llama/Meta-Llama-3.1-8B-Instruct-fast": 128_000,
    "meta-llama/Llama-3.3-70B-Instruct": 128_000,
    "meta-llama/Llama-3.3-70B-Instruct-fast": 128_000,
    "meta-llama/llama-3.3-70b-instruct": 128_000,
    "meta-llama/llama-3.3-70b-instruct:free": 128_000,
    "meta-llama/llama-3.2-1b-instruct": 128_000,
    "meta-llama/llama-3.2-3b-instruct": 128_000,
    "meta-llama/llama-3.2-3b-instruct:free": 128_000,
    "meta-llama/llama-3.2-11b-vision-instruct": 128_000,
    "meta-llama/llama-3.2-90b-vision-instruct": 128_000,
    "meta-llama/llama-3.1-8b-instruct": 128_000,
    "meta-llama/llama-3.1-70b-instruct": 128_000,
    "meta-llama/llama-3.1-405b-instruct": 128_000,
    "meta-llama/llama-3.1-405b": 128_000,
    "meta-llama/llama-3-8b-instruct": 8_192,
    "meta-llama/llama-3-70b-instruct": 8_192,
    "meta-llama/llama-guard-2-8b": 8_192,
    "meta-llama/llama-guard-3-8b": 8_192,
    "meta-llama/Llama-Guard-3-8B": 8_192,
    "meta-llama/llama-guard-4-12b": 8_192,
    # Mistral / Ministral / Devstral / Pixtral
    "mistral.mistral-large-2407-v1:0": 128_000,
    "mistral.ministral-3-14b-instruct": 128_000,
    "mistral.ministral-3-8b-instruct": 128_000,
    "mistralai/mistral-large": 128_000,
    "mistralai/mistral-large-2407": 128_000,
    "mistralai/mistral-large-2411": 128_000,
    "mistralai/mistral-medium-3": 128_000,
    "mistralai/mistral-medium-3.1": 128_000,
    "mistralai/magistral-medium-2506": 128_000,
    "mistralai/magistral-medium-2506:thinking": 128_000,
    "mistralai/magistral-small-2506": 40_000,
    "mistralai/mistral-small-3.1-24b-instruct": 128_000,
    "mistralai/mistral-small-3.1-24b-instruct:free": 128_000,
    "mistralai/mistral-small-3.2-24b-instruct": 128_000,
    "mistralai/mistral-small-3.2-24b-instruct-2506": 128_000,
    "mistralai/mistral-small-24b-instruct-2501": 32_000,
    "mistralai/mistral-saba": 32_000,
    "mistralai/devstral-medium": 128_000,
    "mistralai/devstral-small": 128_000,
    "mistralai/devstral-small-2505": 128_000,
    "mistralai/voxtral-small-24b-2507": 128_000,
    "mistralai/ministral-8b": 128_000,
    "mistralai/ministral-3b": 128_000,
    "mistralai/pixtral-large-2411": 128_000,
    "mistralai/pixtral-12b": 128_000,
    "mistralai/mistral-nemo": 128_000,
    "mistralai/mistral-7b-instruct": 32_000,
    "mistralai/mistral-7b-instruct:free": 32_000,
    "mistralai/mistral-7b-instruct-v0.1": 8_192,
    "mistralai/mistral-7b-instruct-v0.2": 32_000,
    "mistralai/mistral-7b-instruct-v0.3": 32_000,
    "mistralai/mistral-small": 32_000,
    "mistralai/mistral-tiny": 32_000,
    "mistralai/mixtral-8x7b-instruct": 32_000,
    "mistralai/mixtral-8x22b-instruct": 65_536,
    "mistral.mistral-small-2402-v1:0": 32_000,
    # Cohere
    "cohere.command-r-plus-v1:0": 128_000,
    "cohere.command-r-v1:0": 128_000,
    "cohere/command-r-plus-08-2024": 128_000,
    "cohere/command-r-08-2024": 128_000,
    "cohere/command-r7b-12-2024": 128_000,
    # DeepSeek
    "us.deepseek.v3-2-v1:0": 128_000,
    "us.deepseek.v3-1-v1:0": 128_000,
    "us.deepseek.r1-v1:0": 128_000,
    "fireworks/deepseek-v3p1": 128_000,
    "deepseek/deepseek-v3.2-exp": 128_000,
    "deepseek/deepseek-v3.1-terminus": 128_000,
    "deepseek/deepseek-v3.1-terminus:exacto": 128_000,
    "deepseek/deepseek-chat-v3.1": 128_000,
    "deepseek/deepseek-chat-v3-0324": 128_000,
    "deepseek/deepseek-chat": 64_000,
    "deepseek/deepseek-r1": 128_000,
    "deepseek/deepseek-r1-0528": 128_000,
    "deepseek/deepseek-r1-0528-qwen3-8b": 32_000,
    "deepseek/deepseek-r1-distill-llama-70b": 128_000,
    "deepseek/deepseek-r1-distill-qwen-14b": 128_000,
    "deepseek/deepseek-r1-distill-qwen-32b": 128_000,
    "deepseek/deepseek-prover-v2": 128_000,
    "deepseek-ai/DeepSeek-V3-0324": 128_000,
    "deepseek-ai/DeepSeek-V3-0324-fast": 128_000,
    "deepseek-ai/DeepSeek-R1-0528": 128_000,
    "deepseek-ai/DeepSeek-R1-0528-fast": 128_000,
    # OpenAI gpt-oss
    "gpt-oss-120b": 128_000,  # Cerebras model id
    "openai.gpt-oss-120b-1:0": 128_000,
    "openai.gpt-oss-20b-1:0": 128_000,
    "fireworks/gpt-oss-120b": 128_000,
    "fireworks/gpt-oss-20b": 128_000,
    "openai/gpt-oss-120b": 128_000,
    "openai/gpt-oss-120b:exacto": 128_000,
    "openai/gpt-oss-20b": 128_000,
    "openai/gpt-oss-20b:free": 128_000,
    "openai/gpt-oss-safeguard-20b": 128_000,
    "gpt-oss-120b-250805": 131_072,
    "deepseek-v3-2-251201": 131_072,
    # Amazon Nova Micro
    "amazon.nova-micro-v1:0": 128_000,
    "amazon/nova-micro-v1": 128_000,
    # Qwen3 family
    "qwen.qwen3-32b-v1:0": 32_000,
    "qwen/qwen3-32b": 128_000,
    "qwen/qwen3-32b-fast": 128_000,
    "Qwen/Qwen3-32B": 128_000,
    "Qwen/Qwen3-32B-fast": 128_000,
    "qwen/qwen3-235b-a22b": 128_000,
    "qwen/qwen3-235b-a22b:free": 128_000,
    "qwen/qwen3-235b-a22b-2507": 256_000,
    "qwen/qwen3-235b-a22b-thinking-2507": 256_000,
    "Qwen/Qwen3-235B-A22B-Instruct-2507": 256_000,
    "Qwen/Qwen3-235B-A22B-Thinking-2507": 256_000,
    "qwen/qwen3-30b-a3b": 128_000,
    "qwen/qwen3-30b-a3b-instruct-2507": 256_000,
    "qwen/qwen3-30b-a3b-thinking-2507": 256_000,
    "Qwen/Qwen3-30B-A3B-Instruct-2507": 256_000,
    "Qwen/Qwen3-30B-A3B-Thinking-2507": 256_000,
    "qwen/qwen3-next-80b-a3b-instruct": 256_000,
    "qwen/qwen3-next-80b-a3b-thinking": 256_000,
    "Qwen/Qwen3-Coder-30B-A3B-Instruct": 256_000,
    "Qwen/Qwen3-Coder-480B-A35B-Instruct": 256_000,
    "qwen/qwen3-4b:free": 32_000,
    "qwen/qwen3-8b": 40_000,
    "qwen/qwen3-14b": 40_000,
    "qwen/qwen2.5-coder-7b-instruct": 128_000,
    "qwen/qwen-2.5-coder-32b-instruct": 128_000,
    "qwen/qwen-2.5-7b-instruct": 32_000,
    "qwen/qwen-2.5-72b-instruct": 128_000,
    "qwen/qwen-2.5-vl-7b-instruct": 128_000,
    "qwen/qwen2.5-vl-32b-instruct": 128_000,
    "qwen/qwen2.5-vl-72b-instruct": 128_000,
    "Qwen/Qwen2.5-VL-72B-Instruct": 128_000,
    "Qwen/Qwen2.5-Coder-7B-fast": 128_000,
    "qwen/qwen-vl-plus": 8_192,
    "qwen/qwen-vl-max": 8_192,
    "qwen/qwen-plus": 128_000,
    "qwen/qwen-max": 128_000,
    "qwen/qwen3-vl-8b-thinking": 256_000,
    "qwen/qwen3-vl-8b-instruct": 256_000,
    "qwen/qwen3-vl-30b-a3b-thinking": 256_000,
    "qwen/qwen3-vl-30b-a3b-instruct": 256_000,
    "qwen/qwen3-vl-235b-a22b-thinking": 256_000,
    "qwen/qwen3-vl-235b-a22b-instruct": 256_000,
    "qwen/qwq-32b": 128_000,
    # Microsoft Phi
    "microsoft/phi-4": 16_000,
    "microsoft/phi-4-reasoning-plus": 32_000,
    "microsoft/phi-4-multimodal-instruct": 128_000,
    "microsoft/phi-3-mini-128k-instruct": 128_000,
    "microsoft/phi-3-medium-128k-instruct": 128_000,
    "microsoft/phi-3.5-mini-128k-instruct": 128_000,
    "microsoft/wizardlm-2-8x22b": 65_536,
    # NVIDIA Nemotron / Nous Hermes
    "nvidia/llama-3.1-nemotron-ultra-253b-v1": 128_000,
    "nvidia/llama-3.1-nemotron-nano-8b-v1": 128_000,
    "nvidia/llama3.1-nemotron-nano-4b-v1.1": 128_000,
    "nvidia/Llama-3_1-Nemotron-Ultra-253B-v1": 128_000,
    "nvidia/Nemotron-Nano-V2-12b": 128_000,
    "nvidia/nemotron-nano-9b-v2": 128_000,
    "nvidia/nemotron-nano-9b-v2:free": 128_000,
    "nvidia/nemotron-nano-12b-v2-vl": 128_000,
    "nvidia/nemotron-nano-12b-v2-vl:free": 128_000,
    "nvidia/llama-3.1-nemotron-70b-instruct": 128_000,
    "nvidia/llama-3.3-nemotron-super-49b-v1.5": 128_000,
    "nousresearch/hermes-3-llama-3.1-70b": 128_000,
    "nousresearch/hermes-3-llama-3.1-405b": 128_000,
    "nousresearch/hermes-3-llama-3.1-405b:free": 128_000,
    "nousresearch/hermes-4-70b": 128_000,
    "nousresearch/hermes-4-405b": 128_000,
    "NousResearch/Hermes-4-70B": 128_000,
    "NousResearch/Hermes-4-405B": 128_000,
    "nousresearch/hermes-2-pro-llama-3-8b": 8_192,
    "nousresearch/deephermes-3-mistral-24b-preview": 32_000,
    "PrimeIntellect/INTELLECT-3": 128_000,
    "prime-intellect/intellect-3": 128_000,
    # Misc 128K
    "ibm-granite/granite-4.0-h-micro": 128_000,
    "liquid/lfm2-8b-a1b": 32_000,
    "liquid/lfm-2.2-6b": 32_000,
    "deepcogito/cogito-v2.1-671b": 128_000,
    "deepcogito/cogito-v2-preview-llama-70b": 128_000,
    "deepcogito/cogito-v2-preview-llama-109b-moe": 128_000,
    "deepcogito/cogito-v2-preview-llama-405b": 128_000,
    "deepcogito/cogito-v2-preview-deepseek-671b": 128_000,
    "stepfun-ai/step3": 65_536,
    "tencent/hunyuan-a13b-instruct": 32_000,
    "tngtech/tng-r1t-chimera": 64_000,
    "tngtech/tng-r1t-chimera:free": 64_000,
    "tngtech/deepseek-r1t-chimera": 128_000,
    "tngtech/deepseek-r1t-chimera:free": 128_000,
    "tngtech/deepseek-r1t2-chimera": 128_000,
    "tngtech/deepseek-r1t2-chimera:free": 128_000,
    "switchpoint/router": 128_000,
    "openrouter/auto": 128_000,
    "openrouter/bert-nebulon-alpha": 128_000,
    "perplexity/sonar": 128_000,
    "perplexity/sonar-reasoning": 128_000,
    "perplexity/sonar-reasoning-pro": 128_000,
    "perplexity/sonar-deep-research": 128_000,
    "x-ai/grok-3": 131_072,
    "x-ai/grok-3-beta": 131_072,
    "x-ai/grok-3-mini": 131_072,
    "x-ai/grok-3-mini-beta": 131_072,
    "kwaipilot/kat-coder-pro:free": 128_000,
    "inception/mercury": 32_000,
    "inception/mercury-coder": 32_000,
    "baidu/ernie-4.5-21b-a3b": 128_000,
    "baidu/ernie-4.5-21b-a3b-thinking": 128_000,
    "baidu/ernie-4.5-vl-28b-a3b": 128_000,
    "baidu/ernie-4.5-vl-424b-a47b": 128_000,
    "baidu/ernie-4.5-300b-a47b": 128_000,
    # Google Gemma
    "google/gemma-3-4b-it": 128_000,
    "google/gemma-3-4b-it:free": 128_000,
    "google/gemma-3-12b-it": 128_000,
    "google/gemma-3-12b-it:free": 128_000,
    "google/gemma-3-27b-it": 128_000,
    "google/gemma-3-27b-it:free": 128_000,
    "google/gemma-3-27b-it-fast": 128_000,
    "google/gemma-3n-e2b-it:free": 32_000,
    "google/gemma-3n-e4b-it": 32_000,
    "google/gemma-3n-e4b-it:free": 32_000,
    "google/gemma-2-2b-it": 8_192,
    "google/gemma-2-9b-it": 8_192,
    "google/gemma-2-9b-it-fast": 8_192,
    "google/gemma-2-27b-it": 8_192,
    "thudm/glm-4.1v-9b-thinking": 128_000,
    "z-ai/glm-4.5": 128_000,
    "z-ai/glm-4.5-air": 128_000,
    "z-ai/glm-4.5-air:free": 128_000,
    "z-ai/glm-4.5v": 128_000,
    "z-ai/glm-4-32b": 128_000,
    # Smaller ranges
    "morph/morph-v3-large": 32_000,
    "morph/morph-v3-fast": 32_000,
    "relace/relace-apply-3": 32_000,
    "arcee-ai/spotlight": 32_000,
    "arcee-ai/maestro-reasoning": 128_000,
    "arcee-ai/virtuoso-large": 128_000,
    "arcee-ai/coder-large": 32_000,
    "allenai/olmo-3-32b-think": 65_536,
    "allenai/olmo-3-7b-instruct": 65_536,
    "allenai/olmo-3-7b-think": 65_536,
    "allenai/olmo-2-0325-32b-instruct": 4_096,
    "alibaba/tongyi-deepresearch-30b-a3b": 128_000,
    "alibaba/tongyi-deepresearch-30b-a3b:free": 128_000,
    "meituan/longcat-flash-chat": 128_000,
    "meituan/longcat-flash-chat:free": 128_000,
    "opengvlab/internvl3-78b": 8_192,
    "thedrummer/cydonia-24b-v4.1": 32_000,
    "thedrummer/skyfall-36b-v2": 32_000,
    "thedrummer/rocinante-12b": 32_000,
    "thedrummer/anubis-70b-v1.1": 16_000,
    "thedrummer/unslopnemo-12b": 32_000,
    "raifle/sorcererlm-8x22b": 16_000,
    "sao10k/l3-euryale-70b": 8_192,
    "sao10k/l3-lunaris-8b": 8_192,
    "sao10k/l3.1-70b-hanami-x1": 16_000,
    "sao10k/l3.1-euryale-70b": 8_192,
    "sao10k/l3.3-euryale-70b": 128_000,
    "neversleep/llama-3.1-lumimaid-8b": 8_192,
    "neversleep/noromaid-20b": 8_192,
    "alpindale/goliath-120b": 6_144,
    "gryphe/mythomax-l2-13b": 4_096,
    "undi95/remm-slerp-l2-13b": 4_096,
    "anthracite-org/magnum-v4-72b": 32_000,
    "mancer/weaver": 8_000,
    "arliai/qwq-32b-arliai-rpr-v1": 32_000,
    "cognitivecomputations/dolphin-mistral-24b-venice-edition:free": 32_000,
    "inflection/inflection-3-productivity": 8_192,
    "inflection/inflection-3-pi": 8_192,
    "bytedance/ui-tars-1.5-7b": 128_000,
    # OpenAI legacy
    "openai/gpt-4": 8_192,
    "openai/gpt-4-0314": 8_192,
    "openai/gpt-3.5-turbo": 16_385,
    "openai/gpt-3.5-turbo-0613": 4_096,
    "openai/gpt-3.5-turbo-instruct": 4_096,
    "openai/gpt-3.5-turbo-16k": 16_385,
    "gpt-3.5-turbo": 16_385,
    # Amazon Titan
    "amazon.titan-text-express-v1": 8_000,
}

# Substring fallback for unknown exact IDs (e.g. new provider/model variants
# not yet in the exact map). Order matters — most-specific first, since the
# loop returns on the first match against the lowercased model id.
_MODEL_CONTEXT_WINDOWS_SUBSTRING: List[Tuple[str, int]] = [
    # 1M / large-window markers (any provider, any prefix)
    ("claude-sonnet-4-5-1m", 1_000_000),
    ("[1m]", 1_000_000),
    ("-1m", 1_000_000),
    ("llama-4-scout", 10_000_000),
    ("gpt-4.1", 1_047_576),
    ("gemini-3", 1_000_000),
    ("gemini-2", 1_000_000),
    ("gemini-1.5", 1_000_000),
    ("claude-opus-5", 1_000_000),
    ("claude-opus-4-8", 1_000_000),
    ("claude-opus-4-7", 1_000_000),
    ("claude-opus-4-6", 1_000_000),
    ("claude-sonnet-5", 1_000_000),
    ("claude-sonnet-4-6", 1_000_000),
    ("nova-premier", 1_000_000),
    ("nova-2", 1_000_000),
    ("llama-4-maverick", 1_000_000),
    # Bedrock dot-form (``meta.llama4-*``) — covers future SKUs in the
    # family that won't match the hyphenated ``llama-4-*`` substrings.
    ("llama4-maverick", 1_000_000),
    ("llama4-scout", 10_000_000),
    # 400K (GPT-5 family)
    ("gpt-5", 400_000),
    # 300K (Nova)
    ("nova-pro", 300_000),
    ("nova-lite", 300_000),
    # 256K-262K
    ("grok-4", 256_000),
    ("kimi-k2", 256_000),
    ("qwen3-coder", 256_000),
    ("qwen3-235b", 256_000),
    ("qwen3-30b-a3b", 256_000),
    ("qwen3-next", 256_000),
    ("qwen3-vl", 256_000),
    ("codestral", 256_000),
    ("jamba", 256_000),
    # 203K-204K — Z.AI GLM 4.7 variants. ``glm-4.7`` (dot-form) is the
    # 203K Bedrock SKU; ``glm-4-7`` (dash-form) is the 204K dated SKU
    # (e.g. ``glm-4-7-251222``). The 1K-token delta mirrors the catalog —
    # not a typo. Future ``glm-4-7-*`` dashed SKUs match the dash-form
    # entry at 204K; add an EXACT row if a variant ships with a different
    # window.
    ("glm-4.7", 203_000),
    ("glm-4-7", 204_000),
    # 200K (Claude default)
    ("claude", 200_000),
    ("o3", 200_000),
    ("o4", 200_000),
    ("o1", 200_000),
    # 128K (broad fallback)
    ("nova-micro", 128_000),
    ("gpt-4o", 128_000),
    ("gpt-4-turbo", 128_000),
    ("llama-3.3", 128_000),
    ("llama-3.1", 128_000),
    ("llama-3.2", 128_000),
    ("mistral-large", 128_000),
    ("ministral", 128_000),
    ("devstral", 128_000),
    ("phi-4-multimodal", 128_000),
    ("phi-3", 128_000),
    ("nemotron", 128_000),
    ("hermes-3", 128_000),
    ("hermes-4", 128_000),
    ("deepseek", 128_000),
    ("command-r", 128_000),
    ("gpt-oss", 128_000),
    ("gemma-3", 128_000),
    ("ernie-4.5", 128_000),
    ("glm-4.6", 200_000),
    ("glm-4.5", 128_000),
    ("glm-4", 128_000),
    ("mistral-medium", 128_000),
    ("mistral-small-3", 128_000),
    ("qwen3-32b", 128_000),
    ("qwen3-", 128_000),
    ("mistral-nemo", 128_000),
    ("pixtral", 128_000),
    # Smaller / older
    ("phi-4", 16_000),
    ("phi-2", 2_048),
    ("gemma-2", 8_192),
    ("llama-guard", 8_192),
    ("gpt-3.5", 16_385),
    ("titan", 8_000),
]


# Models that must NOT get think/analyze scaffolding even if a weak marker
# matches ("gpt-5-mini" contains "-mini"): natively-reasoning families and
# frontier models. Checked BEFORE _WEAK_MODEL_MARKERS.
_NON_WEAK_MODEL_MARKERS: List[str] = [
    "claude",
    "gpt-5",
    "o1",
    "o3",
    "o4",
    "grok",  # grok-3-mini / grok-4 reason natively
    "deepseek",
    "-r1",
    "qwq",
    "thinking",
    "reasoning",
    "magistral",
    "gemini-2.5-pro",
    "gemini-3",
    "kimi-k2",
    "qwen3-max",
    "gpt-oss",
]

# Weak / small non-reasoning models that benefit from think/analyze
# scaffolding (PRO-1879). Substring match on the lowercased model id, so
# decorated ids also match ("openai/gpt-4o-mini", "meta.llama3-8b-instruct-v1:0")
# — same rationale as _MODEL_CONTEXT_WINDOWS_SUBSTRING. Anything matching
# neither list is treated as strong (no tools), same behavior as the PRO-1875
# global disable, so unknown/new models stay safe.
_WEAK_MODEL_MARKERS: List[str] = [
    # OpenAI non-reasoning
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-4",
    "gpt-3.5",
    # generic size markers
    "-mini",
    "-nano",
    "-lite",
    "-micro",
    "-small",
    "flash",
    # small/legacy families from the platform catalog
    "gemma",
    "phi-",
    "ministral",
    "mistral-nemo",
    "mistral-small",
    "llama-3",
    "llama3",
    "granite",
    "olmo",
    "titan",
    "glm-4.5-air",
]


def _is_weak_model(model: Model) -> bool:
    """True when the model is a small non-reasoning model that benefits
    from agno's think/analyze scaffolding (PRO-1879)."""
    model_id = (getattr(model, "id", "") or "").lower()
    if not model_id:
        return False
    if any(m in model_id for m in _NON_WEAK_MODEL_MARKERS):
        return False
    return any(m in model_id for m in _WEAK_MODEL_MARKERS)


# Per-process cache of model ids that already triggered the unknown-model
# fallback warning. The fallback runs on every agno arun() turn, and a
# single agent looping through many events with the same unmapped id
# would otherwise spam the log with duplicate warnings (PR #511 review).
# A bare ``set`` is safe here — ``_detect_context_window`` is called
# from the agent setup path, not concurrent hot paths.
_LOGGED_UNKNOWN_MODEL_IDS: set = set()
_EMPTY_MODEL_ID_LOGGED = False

# Conservative window for unmapped models: over-budgeting a small-window model
# pushes the real request past its hard limit (fatal overflow + retry spin),
# whereas under-budgeting only triggers extra compaction. 128K is a safe floor
# for modern models; all frontier IDs are in the tables above and bypass this.
_DEFAULT_UNKNOWN_CONTEXT_WINDOW = 128_000


def _detect_context_window(model: Model) -> int:
    """Return the model's max input context in tokens.

    Resolution order: exact match → case-insensitive exact → ordered
    substring fallback → conservative default with a once-per-process warning
    log so the miss is triagable without flooding output.
    """
    global _EMPTY_MODEL_ID_LOGGED
    raw_id = getattr(model, "id", "") or ""
    if not raw_id:
        if not _EMPTY_MODEL_ID_LOGGED:
            logger.warning(
                f"[context-optimizer] model.id is empty; defaulting to "
                f"{_DEFAULT_UNKNOWN_CONTEXT_WINDOW:,} window"
            )
            _EMPTY_MODEL_ID_LOGGED = True
        return _DEFAULT_UNKNOWN_CONTEXT_WINDOW
    if raw_id in _MODEL_CONTEXT_WINDOWS_EXACT:
        return _MODEL_CONTEXT_WINDOWS_EXACT[raw_id]
    lower_id = raw_id.lower()
    if lower_id != raw_id and lower_id in _MODEL_CONTEXT_WINDOWS_EXACT:
        return _MODEL_CONTEXT_WINDOWS_EXACT[lower_id]
    # Case-insensitive exact match for entries with mixed case (Nebius etc).
    for key, window in _MODEL_CONTEXT_WINDOWS_EXACT.items():
        if key.lower() == lower_id:
            return window
    for prefix, window in _MODEL_CONTEXT_WINDOWS_SUBSTRING:
        if prefix in lower_id:
            return window
    if raw_id not in _LOGGED_UNKNOWN_MODEL_IDS:
        logger.warning(
            f"[context-optimizer] unknown model.id='{raw_id}'; defaulting to "
            f"{_DEFAULT_UNKNOWN_CONTEXT_WINDOW:,} window. "
            f"Add to _MODEL_CONTEXT_WINDOWS_EXACT."
        )
        _LOGGED_UNKNOWN_MODEL_IDS.add(raw_id)
    return _DEFAULT_UNKNOWN_CONTEXT_WINDOW


# Public alias: the agent-controller gateway sizes its own optimizer from the
# detected model window and must not import a private name.
def detect_context_window(model: Model) -> int:
    """Public wrapper over _detect_context_window for out-of-repo consumers."""
    return _detect_context_window(model)


def _configure_context_optimizer(
    args: Dict[str, Any], agent: Agent, task: Optional[Task], model: Model
) -> None:
    context_window = _detect_context_window(model)
    # Reserve more headroom for smaller windows so output isn't starved.
    reserved_for_output = min(20_000, max(4_000, int(context_window * 0.10)))
    buffer_tokens = min(13_000, max(2_000, int(context_window * 0.05)))
    logger.info(
        f"[context-optimizer] configured for model={getattr(model, 'id', '?')} "
        f"context_window={context_window:,} reserved_for_output={reserved_for_output:,} "
        f"buffer_tokens={buffer_tokens:,}"
    )
    # Dedicated cheaper model for compaction/LLM ops (PRO-1654). None ⇒ the
    # optimizer falls back to the agent's own model.
    compaction_model = _load_compaction_model(agent, task)
    optimizer = XPanderContextOptimizer(
        model=model,
        compaction_model=compaction_model,
        agent=agent,
        task=task,
        context_window=context_window,
        reserved_for_output=reserved_for_output,
        buffer_tokens=buffer_tokens,
    )
    args["compression_manager"] = optimizer
    # Attach to the task so the SDK's events_module can drain the L1
    # workspace cache (``optimizer.aclose()``) in its finally block. The
    # cloud retry loop (xpander-mono ``agent_executor``) reads it directly
    # off ``args["compression_manager"]`` and doesn't need this attribute.
    if task is not None:
        try:
            object.__setattr__(task, "_xp_context_optimizer", optimizer)
        except Exception:
            pass
