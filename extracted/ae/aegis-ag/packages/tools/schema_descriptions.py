"""Model-visible schema descriptions for built-in tools."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from typing import Any

from .runtime import ToolDefinition

_STRING_ARRAY_SCHEMA: Mapping[str, Any] = {"type": "string"}

_PROPERTY_DESCRIPTIONS: Mapping[str, Mapping[str, str]] = {
    "tool.terminal.exec": {
        "command": "Shell command to run in a bounded subprocess.",
        "cwd": "Working directory override for this command.",
        "timeout_seconds": "Maximum foreground command runtime in seconds.",
        "background": "Start the command as a managed background process.",
        "env": "Additional environment variables for the command.",
    },
    "tool.process.manage": {
        "process_id": "Managed process id returned by a background terminal command.",
        "input": "Text to write to the managed process stdin when action=write.",
        "timeout_seconds": "Maximum time to wait for a process action.",
    },
    "tool.browser.navigate": {"url": "URL to open in the active browser session."},
    "tool.browser.snapshot": {"full": "Capture the full page snapshot instead of the compact view."},
    "tool.browser.type": {"text": "Text to type into the referenced browser element."},
    "tool.browser.scroll": {
        "direction": "Scroll direction.",
        "amount": "Scroll amount in backend-defined units.",
    },
    "tool.browser.press": {"key": "Keyboard key to press, such as Enter or Escape."},
    "tool.browser.vision": {
        "question": "Question for the vision analyzer about the current browser screenshot.",
        "prompt": "Alternate prompt for the vision analyzer.",
        "annotate": "Whether to include visual annotations when supported.",
    },
    "tool.browser.console": {
        "clear": "Clear buffered console entries after reading them.",
        "expression": "JavaScript expression to evaluate in the page context.",
    },
    "tool.clarify": {
        "question": "One concise question to ask the user. In continuity routing, use before durable activity-plan writes only when missing tracking or structure would change what gets stored.",
        "mode": "Use open for free-form input or choice for a bounded option list.",
        "choices": "Choice labels for mode=choice, as an array or newline/comma-delimited string.",
    },
    "tool.cron.manage": {
        "profile_id": "Optional profile scope filter for listing or creating jobs.",
        "clone_id": "Optional clone scope filter for listing or creating jobs.",
    },
    "tool.sub_agents": {
        "action": "Use run|start to launch one bounded sub-agent task or a small task pool.",
        "name": "Optional label for a single sub-agent.",
        "task": "Single sub-agent assignment.",
        "prompt": "Alias for task when launching a single sub-agent.",
        "tasks": "Array of bounded sub-agent assignments for a small parallel pool.",
        "tasks[].name": "Optional label for this sub-agent task.",
        "tasks[].task": "Assignment for this sub-agent task.",
        "tasks[].prompt": "Alias for task in a task-list item.",
        "tasks[].skills": "Skill ids to load for this sub-agent task.",
        "max_concurrency": "Maximum parallel sub-agent tasks to run.",
        "skills": "Skill ids to load for a single sub-agent task.",
    },
    "tool.memory.recall": {
        "action": "Use list|ls to enumerate, inspect with memory_id, lineage with memory_id, or search with query.",
        "memory_id": "Durable memory id to inspect or trace.",
        "query": "Recall search query.",
        "limit": "Maximum number of recall search results.",
    },
    "tool.memory.upload": {
        "action": "Use correct with content, delete with reason, or pin|unpin with memory_id.",
        "memory_id": "Durable memory id to mutate.",
        "content": "Corrected memory content when action=correct.",
        "reason": "Reason for the memory governance change.",
    },
    "tool.message.send": {
        "body": "Outbound message body.",
        "target": "Optional delivery target override.",
        "metadata": "Optional delivery metadata.",
    },
    "tool.todo.manage": {
        "item_id": "Todo item id for inspect, update, complete, reopen, remove, delete, or promote.",
        "title": "Todo title when creating or updating an item.",
        "status": "Todo status when creating or updating an item. Use open, done, or promoted.",
        "notes": "Todo notes when creating or updating an item.",
    },
    "tool.skill.manage": {
        "action": "Use install, enable, disable, create, update, delete, or remove for operator-owned skill changes.",
    },
    "tool.profile.manage": {
        "action": "Use inspect|show|get to read profile continuity or patch|update|set for durable user, identity, preference, boundary, relationship, or recurring-work facts. Patch stable personal facts and user preferences as user state. Patch Aegis display name, persona, personality, initiative, charter, or relationship stance as profile identity or relationship state. When the user self-introduces or answers a naming prompt in any language, patch user_fields.preferred_name before replying. After patch/update/set, use the updated fact naturally; do not report the storage operation unless asked.",
        "display_name": "Profile display name.",
        "name": "Alias for profile display name when patching.",
        "personality_preset": "Personality preset id or label.",
        "initiative": "Initiative posture or guidance for the profile.",
        "charter_text": "Replacement identity charter text.",
        "text": "Generic profile text patch payload for durable identity, user, preference, boundary, relationship, or recurring-work facts.",
        "content": "Generic profile content patch payload for durable identity, user, preference, boundary, relationship, or recurring-work facts.",
        "clear_charter": "Clear the stored identity charter.",
        "user_text": "Replacement or appended user-state text such as self-introduction, company, location, stable preferences, boundaries, or recurring work context.",
        "user_content": "Alias for user_text.",
        "user_fields": "Structured user-state fields to patch, such as preferred_name, current_work, current_city, boundaries, or other stable facts.",
        "user_append": "Append user text instead of replacing it.",
        "user_clear": "Clear the stored user-state text.",
        "relationship_text": "Replacement or appended relationship-continuity text for collaboration rhythm, trust, preferences, and interpersonal context.",
        "relationship_content": "Alias for relationship_text.",
        "relationship_append": "Append relationship text instead of replacing it.",
        "relationship_clear": "Clear the stored relationship-continuity text.",
    },
    "tool.activity.manage": {
        "action": "Use list|ls|show to inspect all activities; inspect with goal_id; create only for followable work with title; focus|activate when resuming or switching to an existing thread; update when scope/status/deadline/checkpoint changes; drop when canceled or no longer worth carrying; delete only accidental or duplicate activity state. Before creating or splitting a durable activity plan, shape one parent outcome plus stable child workstreams; call tool.clarify only if ambiguity in the parent outcome, child boundaries, or durable tracking scope would create a different activity tree. If omitted, title/parent_goal_id implies create, goal_id implies inspect, otherwise list.",
        "goal_id": "Durable activity goal id. Required for inspect, focus|activate, update, and drop|delete; optional as parent when creating a child item.",
        "parent_goal_id": "Parent goal id when creating a child activity. To split a broad followable activity, create the parent first, then create child activities only for stable followable workstreams with this field; use todos for execution steps that do not need durable tracking.",
        "title": "Required for create; optional replacement title for update. Normalize into a concise human-readable outcome; do not copy the user's wording verbatim as a flat goal, and do not use biography, greetings, identity facts, preferences, or relationship notes as activity titles.",
        "status": "Activity progress state for create/update. Use proposed, queued, active, blocked, deferred, completed, done, failed, or dropped; use completed for finished work and dropped for canceled or no-longer-relevant threads.",
        "priority": "Activity priority when creating or updating. Use low, medium, high, or critical.",
        "owner": "Activity owner when creating. Use user, agent, or shared.",
        "dependency_refs": "Dependency references for a new activity.",
        "evidence_refs": "Evidence references for a new activity.",
        "related_memory_ids": "Related durable memory ids for a new activity.",
        "review_checkpoint": "Review checkpoint text for a new activity.",
        "deadline": "Deadline or due date for a new activity.",
        "time_sensitivity": "Time-sensitivity label for a new activity. Use low, normal, high, or urgent; use normal for medium/default urgency, not medium.",
        "reason": "Brief reason for the activity mutation, especially when changing status, focus, title, scope, deadline, checkpoint, or dropping/deleting a thread.",
        "activate": "For create only: whether the new activity should become active immediately; omit to use the runtime default.",
    },
    "tool.procedure.inspect": {
        "action": "Use list|ls|show to enumerate candidates, or inspect with procedure_id.",
        "procedure_id": "Procedure id to inspect.",
        "minimum_support": "Minimum supporting evidence count for listing procedure candidates.",
    },
    "tool.procedure.manage": {
        "action": "Use patch|update with mutable fields, or retire with procedure_id.",
        "procedure_id": "Promoted procedure id to patch or retire.",
        "title": "Replacement procedure title.",
        "summary": "Replacement procedure summary.",
        "content": "Replacement procedure body.",
        "trigger_refs": "Trigger references for the procedure.",
        "status": "Replacement procedure status. Use active, promoted, verified, or retired.",
    },
}


def enrich_builtin_tool_schema(definition: ToolDefinition) -> ToolDefinition:
    """Return a built-in definition with complete model-visible schema guidance."""

    schema = _enrich_schema(definition.tool_id, definition.schema, ())
    return definition if schema == definition.schema else replace(definition, schema=schema)


def _enrich_schema(tool_id: str, schema: Mapping[str, Any], path: tuple[str, ...]) -> Mapping[str, Any]:
    enriched = {str(key): value for key, value in schema.items()}
    properties = enriched.get("properties")
    if isinstance(properties, Mapping):
        enriched["properties"] = {
            str(name): _enrich_property(tool_id, str(name), payload, path)
            for name, payload in properties.items()
        }
    return enriched


def _enrich_property(
    tool_id: str,
    name: str,
    payload: object,
    path: tuple[str, ...],
) -> object:
    if not isinstance(payload, Mapping):
        return payload
    next_path = (*path, name)
    enriched = {str(key): value for key, value in payload.items()}
    description = _description_for(tool_id, next_path)
    if description and not str(enriched.get("description") or "").strip():
        enriched["description"] = description
    if enriched.get("type") == "array" and "items" not in enriched:
        enriched["items"] = _STRING_ARRAY_SCHEMA
    items = enriched.get("items")
    if isinstance(items, Mapping):
        enriched["items"] = _enrich_schema(tool_id, items, (*next_path, "[]"))
    one_of = enriched.get("oneOf")
    if isinstance(one_of, list | tuple):
        enriched["oneOf"] = [_enrich_branch(tool_id, branch, next_path) for branch in one_of]
    properties = enriched.get("properties")
    if isinstance(properties, Mapping):
        enriched["properties"] = {
            str(child): _enrich_property(tool_id, str(child), child_payload, next_path)
            for child, child_payload in properties.items()
        }
    return enriched


def _enrich_branch(tool_id: str, branch: object, path: tuple[str, ...]) -> object:
    if not isinstance(branch, Mapping):
        return branch
    enriched = {str(key): value for key, value in branch.items()}
    if enriched.get("type") == "array" and "items" not in enriched:
        enriched["items"] = _STRING_ARRAY_SCHEMA
    items = enriched.get("items")
    if isinstance(items, Mapping):
        enriched["items"] = _enrich_schema(tool_id, items, (*path, "[]"))
    return enriched


def _description_for(tool_id: str, path: tuple[str, ...]) -> str | None:
    return _PROPERTY_DESCRIPTIONS.get(tool_id, {}).get(_path_key(path))


def _path_key(path: tuple[str, ...]) -> str:
    return ".".join(path).replace(".[]", "[]")


__all__ = ["enrich_builtin_tool_schema"]
