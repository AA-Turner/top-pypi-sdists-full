"""Context management functions for the agent runner.

This module contains functions for estimating, compacting, and managing
conversation context during agent runs.
"""

import os
from typing import Optional, TYPE_CHECKING

from ...utils.logger import log

if TYPE_CHECKING:
    from ..toolkit import AgentToolkit
    from ..events import AgentEventEmitter


def estimate_context_tokens(messages: list[dict], system_prompt: Optional[str] = None) -> int:
    """Estimate the current context window size in tokens.

    Args:
        messages: Conversation messages
        system_prompt: Optional system prompt to include in estimation

    Returns:
        Estimated token count for the context
    """
    total_chars = 0

    # Count characters in all messages
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, str):
            total_chars += len(content)
        elif isinstance(content, list):
            # Handle multi-part messages (e.g., with images)
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    total_chars += len(part["text"])

        # Add role overhead (~4 tokens per message for role/structure)
        total_chars += 16

    # Also count system prompt
    if system_prompt:
        total_chars += len(system_prompt)

    # Estimate: ~4 characters per token
    return total_chars // 4


def get_context_breakdown(
    messages: list[dict],
    system_prompt: Optional[str] = None,
) -> tuple[dict, list[dict]]:
    """Get breakdown of context usage by message type.

    Args:
        messages: Conversation messages
        system_prompt: Optional system prompt

    Returns:
        Tuple of (breakdown dict, list of largest messages)
    """
    breakdown = {
        "system_prompt": len(system_prompt) // 4 if system_prompt else 0,
        "user": 0,
        "assistant": 0,
        "tool_results": 0,
    }

    # Track individual message sizes for finding largest
    message_sizes = []

    for i, msg in enumerate(messages):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        # Calculate content size
        if isinstance(content, str):
            size = len(content)
        elif isinstance(content, list):
            size = sum(len(p.get("text", "")) for p in content if isinstance(p, dict))
        else:
            size = 0

        tokens = size // 4

        # Categorize
        if role == "user":
            breakdown["user"] += tokens
        elif role == "assistant":
            breakdown["assistant"] += tokens
        elif role == "tool":
            breakdown["tool_results"] += tokens

        # Track for largest messages
        if tokens > 100:  # Only track substantial messages
            # Try to get a label for this message
            label = f"{role}[{i}]"
            if role == "tool":
                tool_call_id = msg.get("tool_call_id", "")
                # Try to find the tool name from previous assistant message
                for prev_msg in reversed(messages[:i]):
                    if prev_msg.get("role") == "assistant" and "tool_calls" in prev_msg:
                        for tc in prev_msg.get("tool_calls", []):
                            if tc.get("id") == tool_call_id:
                                label = tc.get("function", {}).get("name", "tool")
                                break
                        break

            message_sizes.append({
                "index": i,
                "role": role,
                "label": label,
                "tokens": tokens,
                "preview": content[:100] if isinstance(content, str) else str(content)[:100],
            })

    # Sort by size and get top 5
    message_sizes.sort(key=lambda x: x["tokens"], reverse=True)
    largest = message_sizes[:5]

    return breakdown, largest


def maybe_compact_context(
    messages: list[dict],
    provider: object,
    emitter: "AgentEventEmitter",
    system_prompt: Optional[str] = None,
    threshold: float = 0.8,
    toolkit: Optional["AgentToolkit"] = None,
    strategy: Optional[object] = None,
    thread_id: Optional[str] = None,
) -> "list[dict] | CompactionResult":
    """Proactively compact context if approaching limit.

    When a :class:`CompactionStrategy` is supplied, all compaction logic is
    delegated to it and a :class:`CompactionResult` is returned.  Without a
    strategy the function falls back to the original behaviour and returns a
    plain ``list[dict]`` for backward compatibility.

    Args:
        messages: Current conversation messages
        provider: LLM provider instance
        emitter: Event emitter for notifications
        system_prompt: System prompt for token estimation
        threshold: Trigger compaction at this % of context limit (default 80%)
        toolkit: AgentToolkit for resetting file tracking after compaction
        strategy: Optional CompactionStrategy to delegate to
        thread_id: Thread id for strategy (required when strategy is set)

    Returns:
        A ``CompactionResult`` when *strategy* is provided, otherwise the
        original-or-compacted message list (backward compat).
    """
    from ..compaction_strategy import CompactionResult

    context_limit = provider.get_context_limit()

    # ---- strategy path ----
    if strategy is not None:
        return strategy.compact(
            thread_id=thread_id or "default",
            messages=messages,
            system_prompt=system_prompt or "",
            context_limit=context_limit,
            threshold=threshold,
            toolkit=toolkit,
            emitter=emitter,
        )

    # ---- legacy path (no strategy) ----
    context_tokens = estimate_context_tokens(messages, system_prompt)

    if context_tokens < context_limit * threshold:
        return messages  # No compaction needed

    log.info(
        f"Context at {context_tokens:,}/{context_limit:,} tokens "
        f"({context_tokens/context_limit:.0%}), compacting..."
    )

    return compact_messages_with_llm(
        messages, emitter, target_tokens=int(context_limit * 0.5), toolkit=toolkit
    )


def compact_messages_with_llm(
    messages: list[dict],
    emitter: "AgentEventEmitter",
    target_tokens: int,
    toolkit: Optional["AgentToolkit"] = None,
) -> list[dict]:
    """Use LLM to create a structured state summary.

    This is a SMART compaction that:
    1. Preserves the original user request
    2. Creates a structured understanding of work done
    3. Extracts file knowledge (what files contain, not verbatim content)
    4. Keeps recent messages for immediate context
    5. Clears file tracking so LLM can re-read files if needed

    Args:
        messages: Current conversation messages
        emitter: Event emitter for notifications
        target_tokens: Target token count after compaction
        toolkit: AgentToolkit for resetting file tracking

    Returns:
        Compacted messages list
    """
    from ..providers import get_provider

    # Keep more recent messages (6-8) for better immediate context
    KEEP_RECENT = 6

    if len(messages) <= KEEP_RECENT + 2:
        return messages  # Too few to compact

    # Split messages
    first_msg = messages[0]
    recent_msgs = messages[-KEEP_RECENT:]
    middle_msgs = messages[1:-KEEP_RECENT]

    if not middle_msgs:
        return messages

    # Extract file information from tool results
    files_info = extract_file_knowledge(middle_msgs)

    # Format the middle content for summarization
    middle_content = format_messages_for_summary(middle_msgs)

    # Build a structured summary prompt following the context compaction spec
    prompt = f"""You are compacting a conversation into a structured continuation summary.

The goal is to preserve intent, decisions, and artifacts while removing low-signal details.
This summary will be used to continue work in a new session.

## ORIGINAL REQUEST
{first_msg.get('content', '')[:2000]}

## CONVERSATION TO SUMMARIZE
{middle_content}

## FILES REFERENCED
{files_info}

---

Generate a compacted summary following this EXACT structure:

---

This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Analysis:
1. **Initial Request**: <What the user originally asked for>
2. **Exploration Phase**: <Investigation, comparisons, discoveries made>
3. **Planning / Design Phase**: <Architecture, workflows, plans discussed>
4. **Decisions / Constraints**: <Explicit choices, rejections, constraints>
5. **Implementation Work**: <What was created, modified, or wired up>
6. **Open Issues / Remaining Work**: <What is not finished or unresolved>

Summary:
1. Primary Request and Intent:
   - <Overarching goal>
   - <Hard requirements and explicit constraints>
   - <Any "must", "must not", or "no need for" statements>

2. Key Technical Concepts:
   - <Concept/Entity>: <Brief description of what it does>
   - <Mechanism/Pattern>: <Brief description>

3. Artifacts and Code Sections:
   ∙ <path/to/file or module name>
     ∙ <Type: doc/module/tool/config> - <One-sentence responsibility>
   ∙ <another artifact>
     ∙ <Type> - <Responsibility>

4. Open Tasks / Next Steps:
   - ✅ <completed task>
   - 🔄 <in progress task>
   - ⏳ <pending task>

---

CRITICAL RULES:
- Start with EXACTLY: "This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation."
- Focus on UNDERSTANDING and DECISIONS, not raw data
- Mention artifact NAMES and ROLES, not full implementations
- Do NOT include code dumps - just reference file paths and responsibilities
- If something was discussed but not finalized, say so (use "planned", "discussed", "in progress")
- Omit or merge Analysis phases if they don't apply
- Target 300-800 words - every bullet should add new information
- Do NOT invent artifacts or decisions - respect uncertainty"""

    # Use default model for summarization
    from ..providers.factory import _get_default_model_name
    model_name = _get_default_model_name()
    compaction_provider = get_provider(model_name)

    try:
        emitter.emit_thinking(f"Compacting context with {model_name}...")

        response = compaction_provider.chat(
            messages=[{"role": "user", "content": prompt}],
            system="You are a context compaction specialist. Create structured continuation summaries that preserve user intent, key decisions, and artifact names while removing low-signal content. Follow the exact output structure provided. Be concise - target 300-800 words.",
        )

        summary = response.content or ""

        log.info(
            f"Compacted {len(middle_msgs)} messages into structured summary "
            f"({len(summary)} chars)"
        )

        # CRITICAL: Reset file tracking so LLM can re-read files
        # The summary contains understanding, but if LLM needs actual content
        # it should be able to re-read files
        if toolkit:
            toolkit.partial_reset_for_compaction()
            log.info("Cleared file tracking after compaction - files can be re-read")

        # Build compacted messages with continuation summary
        # The summary already contains the standard continuation note header
        return [
            first_msg,
            {
                "role": "assistant",
                "content": f"""{summary}

---
Note: Context was compacted. I can re-read any files if I need their exact content.""",
            },
            *recent_msgs,
        ]
    except Exception as e:
        log.warning(f"LLM compaction failed: {e}, falling back to truncation")
        # Notify user that compaction failed
        emitter.emit_thinking(f"Compaction failed ({type(e).__name__}), using simple truncation...")
        # Still reset file tracking even on fallback
        if toolkit:
            toolkit.partial_reset_for_compaction()
        return [first_msg] + recent_msgs


def extract_file_knowledge(messages: list[dict]) -> str:
    """Extract file paths and brief descriptions from tool results.

    This identifies which files were read and tries to capture what was learned
    from each file to help the summarization.

    Args:
        messages: Messages to analyze

    Returns:
        Formatted string of file information
    """
    import json as json_module

    files_seen: dict[str, list[str]] = {}  # path -> list of info snippets

    for msg in messages:
        role = msg.get("role", "")

        # Look for tool results
        if role == "tool":
            content = msg.get("content", "")
            try:
                data = json_module.loads(content) if isinstance(content, str) else content
                if isinstance(data, dict) and data.get("success"):
                    result_data = data.get("data", {})

                    # Handle read_file results
                    if "content" in result_data and "file" not in result_data:
                        # Try to find the file path from params
                        pass  # We'll get it from the tool call

                    # Handle search results that mention files
                    if "results" in result_data:
                        for r in result_data["results"][:5]:
                            if isinstance(r, dict):
                                file_path = r.get("file_path") or r.get("file")
                                if file_path and file_path not in files_seen:
                                    files_seen[file_path] = []
            except (json_module.JSONDecodeError, TypeError):
                pass

        # Look for assistant tool calls to find file paths
        if role == "assistant" and "tool_calls" in msg:
            for tc in msg.get("tool_calls", []):
                func = tc.get("function", {})
                name = func.get("name", "")
                args_str = func.get("arguments", "{}")

                if name == "read_file":
                    try:
                        args = json_module.loads(args_str) if isinstance(args_str, str) else args_str
                        path = args.get("path") or args.get("file_path")
                        if path and path not in files_seen:
                            files_seen[path] = []
                    except (json_module.JSONDecodeError, TypeError):
                        pass

    if not files_seen:
        return "No files explicitly read in this segment."

    lines = ["Files explored in this conversation segment:"]
    for path in list(files_seen.keys())[:20]:  # Limit to 20 files
        lines.append(f"  - {path}")

    return "\n".join(lines)


def format_messages_for_summary(messages: list[dict]) -> str:
    """Format messages for summarization prompt.

    Args:
        messages: Messages to format

    Returns:
        Formatted string for summarization
    """
    parts = []
    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        # Handle tool calls in assistant messages
        if role == "assistant" and "tool_calls" in msg:
            tool_calls = msg.get("tool_calls", [])
            tool_info = [
                f"Called: {tc.get('function', {}).get('name', 'unknown')}"
                for tc in tool_calls
            ]
            content = f"{content}\n[Tools: {', '.join(tool_info)}]" if content else f"[Tools: {', '.join(tool_info)}]"

        # Truncate very long content
        if len(content) > 4000:
            content = content[:4000] + "\n[...truncated...]"

        parts.append(f"[{role.upper()}]\n{content}")

    return "\n\n---\n\n".join(parts)


def get_reranked_context(
    toolkit: "AgentToolkit",
    current_query: str,
) -> dict:
    """Get reranked context items based on the current query.

    Args:
        toolkit: Agent toolkit instance
        current_query: Current query for relevance ranking

    Returns:
        Dict with item_count and items list
    """
    try:
        from ...context.service import ContextService
        from ...context.reranker import rerank_context_items

        # Get exploration steps for context extraction
        steps = toolkit.get_exploration_steps()
        if not steps:
            return {"item_count": 0, "items": [], "query": current_query, "debug": "no exploration steps"}

        # Use context service to extract context items from exploration
        service = ContextService(connection=toolkit.connection)
        terminal_id = service.get_terminal_id()

        # Update context with exploration steps
        service.update_context(
            terminal_id=terminal_id,
            exploration_steps=steps,
        )

        # Get context items
        items = service.get_context_items(terminal_id)
        if not items:
            return {"item_count": 0, "items": [], "query": current_query, "debug": f"no items from service ({len(steps)} steps)"}

        # Get max tokens from env (default 15000)
        max_tokens = int(os.getenv("CONTEXT_FRAME_MAX_TOKENS", "15000"))

        # Rerank by query relevance
        if current_query:
            items = rerank_context_items(
                items,
                current_query,
                top_k=50,  # Get more candidates, then filter by tokens
            )

        # Convert to serializable format, limiting by token count
        result_items = []
        total_tokens = 0
        for item in items:
            item_dict = {
                "name": item.qualified_name,
                "type": item.entity_type,
                "file": item.file_path,
                "score": round(item.score, 3) if hasattr(item, 'score') else None,
                "description": item.description[:200] if item.description else None,
                "touch_count": item.touch_count,
                "neighbors": item.neighbors[:5] if item.neighbors else [],
            }
            # Estimate tokens for this item (~4 chars per token)
            item_chars = len(str(item_dict))
            item_tokens = item_chars // 4

            if total_tokens + item_tokens > max_tokens:
                break

            result_items.append(item_dict)
            total_tokens += item_tokens

        return {
            "item_count": len(result_items),
            "items": result_items,
            "query": current_query,
            "total_tokens": total_tokens,
        }

    except Exception as e:
        log.warning(f"Failed to get reranked context: {e}")
        return {"item_count": 0, "items": [], "query": current_query, "debug": str(e)}


def emit_context_frame(
    toolkit: "AgentToolkit",
    emitter: "AgentEventEmitter",
    messages: list[dict],
    system_prompt: Optional[str],
    current_query: str,
    total_input_tokens: int,
    total_output_tokens: int,
) -> None:
    """Emit a context frame event with current exploration state.

    Args:
        toolkit: Agent toolkit instance
        emitter: Event emitter
        messages: Current conversation messages
        system_prompt: System prompt for estimation
        current_query: Current query for reranking
        total_input_tokens: Total input tokens used
        total_output_tokens: Total output tokens used
    """
    # Get exploration steps from toolkit session
    steps = toolkit.get_exploration_steps()

    # Estimate current context window tokens and get breakdown
    context_tokens = 0
    context_breakdown = {}
    largest_messages = []
    if messages:
        context_tokens = estimate_context_tokens(messages, system_prompt)
        context_breakdown, largest_messages = get_context_breakdown(messages, system_prompt)

    # Summarize exploration by tool
    tool_counts: dict[str, int] = {}
    entities_found = 0
    step_details: list[dict] = []

    for step in steps:
        tool_name = getattr(step, 'tool', 'unknown')
        tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1

        # Count entities from the step
        step_entities = getattr(step, 'entities_found', [])
        entities_found += len(step_entities)

        # Collect step details
        params = getattr(step, 'params', {})
        summary = getattr(step, 'result_summary', '')

        # Extract meaningful info based on tool type
        detail = {
            "tool": tool_name,
            "summary": summary,
        }

        # Add relevant params based on tool
        if tool_name == 'read_file' and 'file_path' in params:
            detail["file"] = params['file_path']
        elif tool_name == 'read_file' and 'path' in params:
            detail["file"] = params['path']
        elif tool_name in ('grep', 'semantic_search') and 'query' in params:
            detail["query"] = params['query']
        elif tool_name == 'glob' and 'pattern' in params:
            detail["pattern"] = params['pattern']
        elif tool_name == 'list_files' and 'path' in params:
            detail["path"] = params['path']

        # Add content preview if available
        content_preview = getattr(step, 'content_preview', None)
        if content_preview:
            detail["content_preview"] = content_preview

        # Add token count if available
        token_count = getattr(step, 'token_count', 0)
        if token_count > 0:
            detail["tokens"] = token_count

        # Add entities if any
        if step_entities:
            detail["entities"] = step_entities[:5]  # Limit to 5

        step_details.append(detail)

    exploration_steps = [
        {"tool": tool, "count": count}
        for tool, count in tool_counts.items()
    ]

    # Build context frame data
    adding = {
        "exploration_steps": exploration_steps,
        "entities_found": entities_found,
        "step_count": len(steps),
        "details": step_details[-20:],  # Last 20 steps
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "context_tokens": context_tokens,  # Current context window size
        "context_breakdown": context_breakdown,  # Tokens by message type
        "largest_messages": largest_messages,  # Top 5 biggest messages
    }

    # Get reranked context items
    reading = get_reranked_context(toolkit, current_query)

    # Emit the context frame
    emitter.emit_context_frame(adding=adding, reading=reading)
