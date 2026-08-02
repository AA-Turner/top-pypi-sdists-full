"""Prompt templates for Layer 2 / Layer 3 / pre-retry compaction.

All large multi-line templates live here so ``context_optimizer.py`` stays
readable. The companion module ``constants.py`` owns the numeric knobs that
seed these prompts (recent-actions count, head/tail budgets, etc.).
"""

from typing import Any, List

AUTO_COMPACT_SYSTEM_PROMPT = (
    "You are a helpful AI assistant tasked with summarizing conversations."
)


RECENT_ACTIONS_BLOCK_TEMPLATE = """\

<recent_actions>
The {count} most recent tool invocations before compaction (verbatim, head/tail
preview, with secrets redacted). Each entry shows status — "ok" or "error".
Use this as your "where I just was" cue. Cross-reference against
<work_completed>: a successful action already listed there is DONE — do not
re-run it. status="error" actions are NOT done — analyze the error and decide
whether to retry, take a different approach, or skip. Do not assume every
recent action succeeded.
{entries}
</recent_actions>"""

RECENT_ACTION_ENTRY_TEMPLATE = """\
<action index="{idx}" tool="{tool_name}" status="{status}" timestamp="{ts}">
  <args>{args}</args>
  <result>{result}</result>
</action>"""


AUTO_COMPACT_USER_PROMPT_TEMPLATE = """\
You are compacting an in-progress agent session into a binding state artifact the resuming
agent will treat as AUTHORITATIVE: it will NOT re-do <work_completed>, NOT relitigate
<decisions_made>, NOT re-fetch <data_gathered>. Be precise.

Conversation to summarize:
<conversation>
{conversation}
</conversation>

Output ONE XML-tagged artifact with EXACTLY these sections in this order — no markdown
headings, no preamble, no commentary outside tags.

<work_completed>
One bullet per concrete action that produced an output: "- <verb> <target> — <observed result>".
<target> is an exact identifier (file path, URL, ID, function, command); <observed result> is a
verifiable outcome. e.g. "- Edited /src/auth/middleware.py:42-58 — changed `<` to `<=`, pytest 47/0".
Be exhaustive — anything missing here gets redone.
</work_completed>

<decisions_made>
One line per committed choice/fact that affects future actions; the resuming agent will NOT
relitigate these. e.g. "- chose JWT over session cookies (user confirmed turn 3)".
</decisions_made>

<data_gathered>
Verbatim opaque values, IDs, schemas, snippets that may be needed again — looked up here BEFORE
re-fetching. Format "- <kind> <identifier>: <value or summary> (source: <where>)". Preserve
identifiers EXACTLY — do not shorten, normalize, or reconstruct.
</data_gathered>

<user_requests_verbatim>
Every user message verbatim, oldest first, one per line with its turn marker. Non-negotiable: do
NOT paraphrase, do NOT attribute assistant suggestions as user preferences.
</user_requests_verbatim>

<open_questions>
Anything the agent asked the user that is unanswered, or ambiguities flagged but unresolved.
One per line.
</open_questions>

<current_focus>
One short paragraph: what the agent was doing in the LAST 1-2 turns of <conversation>, with a
direct quote from the most recent assistant message. Do NOT speculate forward.
</current_focus>

<next_action>
Single concrete next step (tool to call, file to edit, or question to ask), verbatim from the most
recent plan/user direction in <conversation>. Do NOT invent steps the user did not request and the
plan does not require.
</next_action>
{plan_section}
HARD RULES (violations make the artifact useless to the resuming agent):
- MUST preserve all opaque identifiers verbatim (UUIDs, hashes, IDs, tokens, hostnames,
  IPs, ports, URLs, file paths, line numbers, version numbers).
- MUST NOT attribute assistant suggestions as user preferences — only what the user
  actually said or confirmed.
- MUST NOT include speculative next steps beyond what user asked or plan requires.
- MUST output XML-tagged sections IN ORDER. No markdown headings. No prose outside tags.
- MUST treat work in <work_completed> as DONE; the resuming agent will NOT redo it.
- MUST NOT use any tools. Respond with ONLY the XML artifact.
{custom_instructions_section}"""


CONTINUATION_MESSAGE_TEMPLATE = """\
<session_resume>
This session resumed after context compaction. The state below is AUTHORITATIVE
and contains ALL data, findings, and work products from the earlier session.

<state>
{summary}
</state>
{authoritative_ledger_block}
<binding_rules>
1. Treat <work_completed> as DONE — do NOT re-run, re-verify, re-fetch, or re-edit
   anything listed there unless the user explicitly asks. Trust the recorded results.
2. Treat <data_gathered> as available — do NOT re-fetch listed IDs, schemas, or
   snippets; look in <state> first.
3. Treat <decisions_made> as final. Do NOT relitigate or propose alternatives.
4. The plan section below shows completed tasks. Continue from <next_action>.
5. Do NOT ask the user any questions about prior context — it is in <state>.
6. Continue execution; do NOT stop until the plan is complete.
7. <authoritative_ledger> is the durable record of every tool call this task already
   executed. Do NOT repeat a completed mutation just because you lost conversational
   context — a WRITE entry with status="ok" for the same tool + target + arguments is
   already done. You MAY perform additional, distinct mutations the plan or user
   requires (a sequence of edits, multiple appends, follow-up inserts). The ledger is
   ground truth over recollection; it survives compaction unchanged.
</binding_rules>
{recent_actions_block}
{backup_pointer}
</session_resume>
"""


# Authoritative-ledger header rendered above the entries by ActionLedger.
# Kept here so all Layer-2 prompt fragments live in one place.
AUTHORITATIVE_LEDGER_BLOCK_INTRO = """\
Verified record of tool calls executed earlier in this task.
Treat WRITE entries with status="ok" as completed for that
specific recorded operation — do NOT re-invoke the same tool
with the same arguments against the same target. Distinct,
plan-required mutations on the same target are still allowed.
Use VERIFY entries to confirm a write succeeded before
composing the final answer."""


# Map-reduce compaction prompts. Used when the conversation is too large for a
# single LLM call and we need to summarise it in chunks first, then combine.
PARTIAL_COMPACT_SYSTEM_PROMPT = (
    "You are a helpful AI assistant producing a dense partial digest of a long "
    "conversation. Your digest will later be combined with other partial digests "
    "to build a full working-state summary."
)

PARTIAL_COMPACT_USER_PROMPT_TEMPLATE = """\
You are producing a PARTIAL digest of CHUNK {chunk_index} of {total_chunks} of a longer
conversation. This digest will be combined with other partial digests into a final
state-capture artifact (the same XML-tagged contract the resuming agent will rely on).

To make the reduce step trivial, structure your output using the SAME XML tags the final
artifact uses, but only fill in the parts represented in this chunk. Leave a tag empty
when this chunk has no content for it.

<work_completed>
One bullet per concrete action that produced an output. Format: "<verb> <target> — <observed result>".
Target MUST be an exact identifier (file path, URL, ID, function name, command).
</work_completed>

<decisions_made>
One line per choice or fact the agent committed to in this chunk.
</decisions_made>

<data_gathered>
Verbatim opaque values, IDs, schemas, snippets the agent retrieved in this chunk.
Format: "<kind> <identifier>: <value or summary> (source: <where>)".
</data_gathered>

<user_requests_verbatim>
Every user message in this chunk verbatim. Do NOT paraphrase.
</user_requests_verbatim>

<open_questions>
Anything the agent asked the user that is unanswered, or unresolved ambiguities.
</open_questions>

<chunk_local_focus>
One short paragraph: what the agent was doing at the END of this chunk.
(The final reduce step will only use the LAST chunk's focus to populate <current_focus>.)
</chunk_local_focus>

PRESERVE all opaque identifiers exactly: UUIDs, hashes, IDs, paths, URLs, version numbers.
Do NOT attribute assistant suggestions as user preferences.
Do NOT use any tools. Respond with ONLY the XML tags.

Here is the chunk to digest:
<conversation_chunk index="{chunk_index}" total="{total_chunks}">
{conversation}
</conversation_chunk>
"""


def build_pre_retry_focus_instructions(
    uncompleted_tasks: List[Any],
    retry_count: int,
) -> str:
    """Build the ``custom_instructions`` payload for pre-retry L2 compaction.

    Shared by the SDK retry path (``events_module.handle_task_execution_request``)
    and the cloud retry path (xpander-mono ``agent_executor.execute``) so both
    sites bias the compaction LLM identically toward remaining plan tasks /
    next-action without re-implementing the prompt.

    Tag names (``<next_action>`` / ``<work_completed>``) intentionally mirror
    ``AUTO_COMPACT_USER_PROMPT_TEMPLATE`` — keep them in sync.

    Args:
        uncompleted_tasks: Items from ``PlanFollowingStatus.uncompleted_tasks``
            (each must expose ``.title`` and ``.id``). Empty list → returns
            "" so the template's ``Additional focus:`` section is suppressed.
        retry_count: Current zero-based retry count from the retry loop.
            Rendered as ``retry attempt {retry_count + 2}`` to match the
            user-facing 1-based retry numbering used elsewhere.

    Returns:
        The guidance string, or "" when there are no uncompleted tasks.
    """
    if not uncompleted_tasks:
        return ""
    first = uncompleted_tasks[0]
    remaining = "; ".join(f"{t.title} (ID: {t.id})" for t in uncompleted_tasks)
    return (
        f"This is a PRE-RETRY compaction (retry attempt {retry_count + 2}). "
        f"Populate <next_action> with the exact next step for the first "
        f'uncompleted plan task: "{first.title}" (ID: {first.id}). '
        f"Remaining uncompleted plan tasks: {remaining}. "
        f"Under <work_completed> include ONLY tasks the agent ACTUALLY "
        f"finished — never mark unfinished plan items as completed. "
        f"Preserve verbatim user request(s) and any exact data, IDs, paths, "
        f"or tool outputs the remaining tasks will need."
    )
