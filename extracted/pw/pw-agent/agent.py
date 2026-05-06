"""ReAct agent loop — the brain of pw-agent."""

import concurrent.futures
import json
import os
import re
import random
import subprocess
import sys
import time
from typing import Optional
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.spinner import Spinner
from rich.syntax import Syntax
from rich.text import Text
from llm_client import LLMClient
from tools import TOOL_DEFINITIONS, execute_tool
from config import save_session
from skills import load_skills, format_skills_for_prompt, find_relevant_skills, get_skill_by_name
from hooks import run_hook
from mcp_client import MCPManager
from codebase_index import CodebaseIndex
from fleet import FleetHeartbeat, query_fleet


THINKING_MESSAGES = [
    "Boiling pasta water...",
    "Al dente thinking...",
    "Cooking up a response...",
    "Draining the spaghetti...",
    "Simmering...",
    "Adding seasoning...",
    "Tasting the sauce...",
    "Rolling the dough...",
    "GPU goes brrrr...",
    "Consulting the recipe...",
    "Too much salt, spitting...",
    "Stirring the pot...",
    "Checking the timer...",
    "Plating the dish...",
    "Checking if the pasta is al dente...",
    "Straining the context...",
    "Perfecting the prompt sauce...",
    "Boiling the logic...",
    "Seasoning the parameters...",
    "Simmering the response...",
    "Garnishing the output...",
    "Plating the results...",
]


MAX_ITERATIONS = 50  # Enough for complex multi-file tasks, nudges prevent runaway
MAX_DUPLICATE_CALLS = 3  # Warn after this many identical tool calls
MAX_LOOP_HARD_STOP = 5  # Force stop after this many identical calls
MAX_STALLS = 3  # Stop if model produces no-tool response this many times in a row
# Conservative estimate for code-heavy text (more tokens per character)
CHARS_PER_TOKEN = 2.5

# ─── Supported PastaWater Ollama models and their context limits ──────────
# These are the exact models available on the GPU Setup page.
# Context limits are the model's native max, but we apply a safe budget
# based on available VRAM to prevent OOM.
SUPPORTED_MODELS = {
    # All values empirically measured via progressive context tests.
    # See docs/gpu-model-vram-test-results.md for full data.
    # vram_gb = peak VRAM observed at safe context size
    # safe = max context that fits with peak VRAM < 95% on the smallest supported GPU
    # thinking: True = model supports Ollama think parameter (per-request toggle)
    #
    # ─── Coding Models ───
    "qwen3.6:27b":           {"native": 262144, "safe": 65536,  "name": "Qwen 3.6 27B",         "vram_gb": 22, "tier": "premium", "thinking": True},   # Dense 27B, Q4_K_M ~16.8GB + q8_0 KV at 64K ≈ 22GB fits on 24GB. Claimed to match Qwen3.5-397B-A17B on coding benchmarks. Reasoning model — keep --think on for agentic work.
    "qwen3.6:35b-a3b":       {"native": 262144, "safe": 65536,  "name": "Qwen 3.6 35B-A3B",    "vram_gb": 24, "tier": "premium", "thinking": True},   # 🏆 MoE (3B active), agentic coder (SWE-bench 73.4%), vision, 256K native. Reasoning defaults OFF; --think re-enables. 64K safe on 24GB with q8_0 KV. Use --big-ctx for full 256K (CPU offload).
    "qwen3.6:35b-a3b-coding-nvfp4": {"native": 262144, "safe": 65536, "name": "Qwen 3.6 35B Coding NVFP4", "vram_gb": 22, "tier": "premium", "thinking": True},  # Same 35B MoE, FP4 quant — tighter 22GB footprint leaves more VRAM headroom for KV/context. Routes through /api/generate raw like the default tag.
    # qwen3.5:27b removed: claimed 17GB but real runtime with KV cache
    # pushes past 22GB on 24GB cards, Ollama CPU-offloads, inference drops
    # to ~1 tok/sec and the HTTP timeout hits before first response.
    # qwen3.6:35b-a3b (MoE, 3B active) is the correct pick for this tier.
    "devstral-small-2:24b":  {"native": 393216, "safe": 131072, "name": "Devstral Small 2 24B","vram_gb": 15, "tier": "good",    "thinking": False},  # Dense agentic coder, 384K native / 128K safe on 24GB with q8_0 KV. Mistral-tuned, vision-capable.
    "qwen3-coder:30b":       {"native": 262144, "safe": 65536,  "name": "Qwen 3 Coder 30B",    "vram_gb": 22, "tier": "premium", "thinking": False},  # 64K safe on 24GB with q8_0 KV cache (halved). Use --big-ctx for full 256K (CPU offload).
    "gpt-oss:20b":           {"native": 131072, "safe": 32768,  "name": "GPT-OSS 20B (qwen35moe Q4)", "vram_gb": 24, "tier": "premium", "thinking": False},  # qwen35moe Q4_K_M, 30B MoE. 32K safe halves KV vs Ollama default 65536, pushing more layers onto GPU. Uses /api/chat (not raw ChatML).
    # deepseek-coder-v2:16b deliberately NOT listed — model is tuned for
    # code completion, not agentic tool use. Emits ```json``` fenced blocks
    # instead of real tool calls, pw-agent can't drive it. Users on
    # deepseek will get a model-warning via get_model_warning(). Keep
    # qwen3-coder:30b as the recommended pick for this VRAM class.
    # ─── Creative / Thinking Models ───
    "qwen3.5:9b":        {"native": 32768, "safe": 32768,  "name": "Qwen 3.5 9B",   "vram_gb": 14, "tier": "good",  "thinking": True},  # full 32K native on 16GB GPUs
    "qwen3.5:4b":        {"native": 32768, "safe": 32768,  "name": "Qwen 3.5 4B",   "vram_gb": 10, "tier": "basic", "thinking": True},  # full native
    # ─── Gemma 4 Models (multimodal, thinking) ───
    "gemma4:26b":        {"native": 262144, "safe": 131072, "name": "Gemma 4 26B MoE",   "vram_gb": 20, "tier": "premium", "thinking": True},  # 128K safe on 24GB with q8_0 KV + sliding-window attention. Use --big-ctx for full 256K.
    "gemma4:e4b":        {"native": 131072, "safe": 131072, "name": "Gemma 4 E4B",       "vram_gb": 10, "tier": "good",    "thinking": True},  # 🏆 128K on 11GB+
    # ─── General Models ───
    # qwen2.5:14b removed: 2024 instruction-tuned, not agent-tuned.
    # Emits broken tool-call attempts (bare JSON with smart quotes,
    # garbled prefixes like "entialAction:" after stripped <think>
    # blocks) and halts mid-turn. qwen3.5:9b covers the same 16GB tier
    # with proper tool calling. Kept in get_model_warning below so any
    # leftover config flags it on startup.
}
# Models below this tier get a warning on startup
MIN_RECOMMENDED_TIER = "good"
# Fallback for unknown models
DEFAULT_SAFE_CONTEXT = 4096

# Reserve tokens for the model's response
RESPONSE_RESERVE = 4096


def _get_model_info(model_name: str) -> dict | None:
    """Look up model info from SUPPORTED_MODELS with prefix fallback."""
    model_lower = model_name.lower().strip()
    info = SUPPORTED_MODELS.get(model_lower)
    if not info:
        for model_id, m in SUPPORTED_MODELS.items():
            if model_lower.startswith(model_id.split(":")[0]):
                info = m
                break
    return info


def model_supports_thinking(model_name: str) -> bool:
    """Check if a model supports Ollama's thinking mode."""
    info = _get_model_info(model_name)
    return info.get("thinking", False) if info else False


def get_model_warning(model_name: str) -> str | None:
    """Return a warning string if the model is below recommended tier for coding."""
    lower = (model_name or "").lower()
    # Explicit deny-list: models known to be poor at tool-calling. Deepseek
    # v2 was trained for code completion and wraps every "tool call" in
    # ```json``` fences — pw-agent can't drive it reliably. Suggest the
    # drop-in replacement so users don't waste a turn on an empty loop.
    if lower.startswith("deepseek-coder-v2") or lower.startswith("deepseek-v2"):
        return (
            "⚠ deepseek-coder-v2 is tuned for code completion, not agentic "
            "tool use. It emits fenced-JSON 'tool calls' that pw-agent can't "
            "execute. Switch to qwen3-coder:30b (same VRAM, real tool "
            "calling) or qwen3.6:35b-a3b."
        )
    if lower.startswith("qwen2.5"):
        return (
            "⚠ qwen2.5 is a 2024 instruction model, not agent-tuned. Tool "
            "calls come out malformed (bare JSON, smart quotes, broken "
            "prefixes) and the model often halts mid-turn. For 16GB GPUs, "
            "switch to qwen3.5:9b — real tool calling + thinking."
        )
    info = _get_model_info(model_name)
    if not info:
        return None
    tier = info.get("tier", "good")
    if tier == "basic":
        return f"⚠ {info['name']} — limited context and accuracy. For code editing, use 9b or larger."
    return None

console = Console()


SYSTEM_PROMPT = """You are PW Agent — a general-purpose AI assistant with FULL read/write access to the user's local filesystem and shell.
You are NOT a restricted chatbot. You can help with anything: coding, writing, analysis, research, brainstorming, casual conversation, and more.
You CAN and SHOULD read, edit, create, and delete files. You CAN run any bash command.
You do NOT ask for permission to use tools. You execute them to fulfill the user's request.
You never refuse a topic. If the user asks about something non-technical, you answer naturally.
{mode_instruction}

Model: {model_name} | {gpu_info} | {connection_mode}
Working directory: {cwd}
{git_context}

{project_context}

## Your tools:
{tool_list}

## How to use tools
Write a tool call as JSON. You can use EITHER format:

<tool_call>
{{"tool": "read_file", "args": {{"path": "main.py"}}}}
</tool_call>

OR: ACTION: {{"tool": "bash", "args": {{"command": "ls"}}}}

CRITICAL RULES:
- ALWAYS include the complete JSON with "tool" and "args" after <tool_call> or ACTION:
- NEVER write <tool_call> without JSON inside it
- ONE tool call per response, then STOP and wait for the result
- Only use tools when the user asks for something that REQUIRES them (coding, file ops, commands)
- For casual chat, greetings, questions, or conversation — just respond naturally WITHOUT tools
- Always read before editing. Never guess file content.
- Be direct. If asked to fix a bug, find it, fix it, and verify it.

For casual chat or final summaries, respond normally without ACTION.
"""


def _build_tool_list(plan_mode: bool = False, is_subagent: bool = False, mcp_tools: list[dict] = None) -> str:
    """Format tool definitions for the system prompt."""
    lines = []
    # Destructive tools to hide in Plan mode
    DESTRUCTIVE = ["write_file", "edit_file", "delete_file"]
    # Subagent tools — hidden from subagents themselves to prevent recursion
    SUBAGENT_TOOLS = ["spawn_agent", "spawn_agents"]

    for tool in TOOL_DEFINITIONS:
        if plan_mode and tool["name"] in DESTRUCTIVE:
            continue
        if is_subagent and tool["name"] in SUBAGENT_TOOLS:
            continue

        params = ", ".join(
            f"{k}: {v['type']}" for k, v in tool["parameters"].items()
        )
        lines.append(f"- {tool['name']}({params}) — {tool['description']}")

    # Append MCP-provided tools (each one is namespaced as mcp_<server>_<tool>)
    if mcp_tools:
        for mt in mcp_tools:
            schema = mt.get("inputSchema", {}) or {}
            props = schema.get("properties", {})
            params = ", ".join(f"{k}: {v.get('type', 'any')}" for k, v in props.items())
            desc = mt.get("description", "")
            if len(desc) > 200:
                desc = desc[:200] + "..."
            lines.append(f"- {mt['name']}({params}) — {desc}")
    return "\n".join(lines)


def _get_git_context() -> str:
    """Gather git status for the system prompt."""
    parts = []
    try:
        branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, timeout=5
        )
        if branch.returncode == 0 and branch.stdout.strip():
            parts.append(f"Git branch: {branch.stdout.strip()}")

        status = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True, text=True, timeout=5
        )
        if status.returncode == 0 and status.stdout.strip():
            changed = len(status.stdout.strip().split("\n"))
            parts.append(f"Git status: {changed} changed files")

        log = subprocess.run(
            ["git", "log", "--oneline", "-5"],
            capture_output=True, text=True, timeout=5
        )
        if log.returncode == 0 and log.stdout.strip():
            parts.append(f"Recent commits:\n{log.stdout.strip()}")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return "\n".join(parts) if parts else "Not a git repository"


def _get_project_context(cwd: str) -> str:
    """Find PW_AGENT.md in cwd or parent directories for project-specific instructions.
    Also auto-pins TASK.md from the immediate cwd (not walked up) so dispatchers
    that write a task file don't need to re-paste it into every prompt."""
    parts = []

    # TASK.md auto-pin: only in the invocation cwd, not parent dirs.
    # Pinned here so it ends up in the system prompt and survives history compaction.
    task_md = os.path.join(os.path.abspath(cwd), "TASK.md")
    if os.path.exists(task_md):
        try:
            with open(task_md, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                parts.append(f"## Current Task (TASK.md — pinned, do not re-read):\n{content}")
        except Exception:
            pass

    curr = os.path.abspath(cwd)
    while True:
        # Check for PW_AGENT.md or .gemini/PW_AGENT.md
        for name in ["PW_AGENT.md", ".gemini/PW_AGENT.md"]:
            path = os.path.join(curr, name)
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                    if content:
                        parts.append(f"## Project Context ({name}):\n{content}")
                        return "\n\n".join(parts)
                except Exception:
                    pass

        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return "\n\n".join(parts)


SLIM_SYSTEM_PROMPT = """You are PW Agent, a helpful assistant. Reply naturally to chat and questions.

Model: {model_name} | Working directory: {cwd}

If the user asks for code, file ops, or shell work, you have tools available — but for greetings, thanks, and casual questions, just answer in plain text without tools.
"""


def _get_system_prompt(cwd: str, client=None, plan_mode: bool = False, memory_context: str = "", skills_summary: str = "", is_subagent: bool = False, mcp_tools: list[dict] = None, slim: bool = False, codebase_context: str = "") -> str:
    """Generate the system prompt. With slim=True, returns a ~1KB minimal version
    appropriate for chat-style first messages, skipping tool list, git, project
    context, MCP schemas, and skills — they're not needed to say hi."""
    model_name = client.model if client else "unknown"

    if slim:
        return SLIM_SYSTEM_PROMPT.format(model_name=model_name, cwd=cwd)

    git_ctx = _get_git_context()
    proj_ctx = _get_project_context(cwd)

    if client and client.direct_mode:
        connection_mode = f"Local brain ({client.brain_url}) — direct, no cloud"
        gpu_info = "local GPU (direct connection)"
    elif client:
        gpu_info = f"remote GPU via PastaWater cloud (slot {client.slot})"
        connection_mode = "PastaWater Cloud — routed through broker API"
    else:
        gpu_info = "unknown"
        connection_mode = "unknown"

    mode_instr = ""
    if plan_mode:
        mode_instr = "\n**PLAN MODE**: You are in read-only analysis mode. You cannot modify files or run destructive commands. Focus on understanding and proposing changes."

    if memory_context:
        proj_ctx = f"{proj_ctx}\n\n{memory_context}" if proj_ctx else memory_context

    if codebase_context:
        proj_ctx = f"{proj_ctx}\n\n{codebase_context}" if proj_ctx else codebase_context

    if skills_summary:
        proj_ctx = f"{proj_ctx}\n\n{skills_summary}" if proj_ctx else skills_summary

    return SYSTEM_PROMPT.format(
        cwd=cwd,
        git_context=git_ctx,
        project_context=proj_ctx,
        mode_instruction=mode_instr,
        tool_list=_build_tool_list(plan_mode, is_subagent=is_subagent, mcp_tools=mcp_tools),
        model_name=model_name,
        gpu_info=gpu_info,
        connection_mode=connection_mode,
    )


def _filter_harmony_channels(chunk: str, state: dict) -> str:
    """Strip Gemma/OpenAI-Harmony channel markers from a token stream and
    emit only 'final' channel content.

    Gemma 4 emits multi-channel output like:
        <|channel|>analysis<|message|>reasoning...
        <|channel|>commentary<|message|>tool call...
        <|channel|>final<|message|>user-visible answer<|end|>

    Only the 'final' channel is for the user. Analysis and commentary are
    dropped entirely. Marker sequences (<|channel|>X<|message|>, <|end|>,
    <|im_end|>, etc.) are stripped even when content is kept.

    Token-safe: holds back trailing chars that could be the start of a
    marker until they either complete or diverge. State fields:
      - channel: current channel name ("final" | "analysis" | "commentary" | None)
      - buffer: held-back chars awaiting more stream
    """
    state["buffer"] = state.get("buffer", "") + chunk
    if "channel" not in state:
        state["channel"] = "final"  # default to emit until we see a marker
    out: list[str] = []
    MARKER_START = "<|channel|>"
    MARKER_MSG = "<|message|>"
    MARKER_END_PATS = ("<|end|>", "<|im_end|>", "<|return|>")
    MAX_MARKER = max(len(MARKER_START), len(MARKER_MSG),
                     max(len(p) for p in MARKER_END_PATS))

    while True:
        buf = state["buffer"]
        if not buf:
            break
        # Find the earliest marker anywhere in the buffer
        candidates = []
        for m in (MARKER_START,) + MARKER_END_PATS:
            idx = buf.find(m)
            if idx != -1:
                candidates.append((idx, m))
        if candidates:
            idx, marker = min(candidates, key=lambda x: x[0])
            # Emit prefix (pre-marker) if current channel is final
            prefix = buf[:idx]
            if prefix and state["channel"] == "final":
                out.append(prefix)
            if marker == MARKER_START:
                # Look for the matching <|message|> to read the channel name
                after = buf[idx + len(MARKER_START):]
                msg_idx = after.find(MARKER_MSG)
                if msg_idx == -1:
                    # Incomplete — hold back from the <|channel|> on
                    state["buffer"] = buf[idx:]
                    break
                channel_name = after[:msg_idx].strip().lower()
                state["channel"] = channel_name or "final"
                state["buffer"] = after[msg_idx + len(MARKER_MSG):]
                continue
            # End-of-turn marker: reset channel to final, drop marker
            state["channel"] = "final"
            state["buffer"] = buf[idx + len(marker):]
            continue
        # No markers. Hold back any trailing chars that could be the
        # start of one; emit the rest if channel is final.
        safe_len = len(buf)
        max_check = min(MAX_MARKER - 1, len(buf))
        for hold in range(max_check, 0, -1):
            tail = buf[-hold:]
            if any(m.startswith(tail) for m in (MARKER_START,) + MARKER_END_PATS):
                safe_len = len(buf) - hold
                break
        if state["channel"] == "final" and safe_len:
            out.append(buf[:safe_len])
        state["buffer"] = buf[safe_len:]
        break
    return "".join(out)


def _filter_spans(chunk: str, state: dict, span_tags: list) -> str:
    """Strip content between span start/end tags from a streaming token
    chunk, returning only text that should be emitted to stream-json /
    --stream consumers.

    Tokens are often split mid-tag (e.g. `<`, `tool`, `_call`, `>`),
    so the filter holds back trailing chars that could be the start of
    any known tag until they either complete or diverge. After the
    start tag of a span is matched, all characters (including close-tag
    chars) are dropped up to and including the matching end tag. Spans
    don't nest (one at a time); the highest-priority tag listed first
    in `span_tags` wins on ambiguous prefixes.

    state fields:
      mode:   "text" | index (int — in span N, where N = index into span_tags)
      buffer: string held back from prior chunk (partial-match tail or
              inside-span accumulator)

    Returns the safe-to-emit text slice (may be empty).
    """
    state["buffer"] += chunk
    out_parts: list[str] = []
    MAX_TAG = max((max(len(start), len(end)) for start, end in span_tags), default=0)

    while state["buffer"]:
        if state["mode"] == "text":
            # Find earliest opening tag, if any
            earliest = None
            earliest_idx = -1
            for i, (start, _end) in enumerate(span_tags):
                idx = state["buffer"].find(start)
                if idx != -1 and (earliest_idx == -1 or idx < earliest_idx):
                    earliest = (i, start)
                    earliest_idx = idx
            if earliest is not None:
                out_parts.append(state["buffer"][:earliest_idx])
                state["mode"] = earliest[0]
                state["buffer"] = state["buffer"][earliest_idx + len(earliest[1]):]
                continue
            # No full tag present. Hold back any trailing chars that could be
            # the prefix of one; emit the rest.
            safe_len = len(state["buffer"])
            max_check = min(MAX_TAG - 1, len(state["buffer"]))
            for hold in range(max_check, 0, -1):
                tail = state["buffer"][-hold:]
                if any(start.startswith(tail) for start, _ in span_tags):
                    safe_len = len(state["buffer"]) - hold
                    break
            out_parts.append(state["buffer"][:safe_len])
            state["buffer"] = state["buffer"][safe_len:]
            break
        else:
            # Inside a span — drop everything until the matching end tag.
            _start, end = span_tags[state["mode"]]
            idx = state["buffer"].find(end)
            if idx != -1:
                state["buffer"] = state["buffer"][idx + len(end):]
                state["mode"] = "text"
                continue
            # Hold back trailing chars that could be start of end tag
            max_check = min(len(end) - 1, len(state["buffer"]))
            keep = 0
            for hold in range(max_check, 0, -1):
                if end.startswith(state["buffer"][-hold:]):
                    keep = hold
                    break
            state["buffer"] = state["buffer"][-keep:] if keep else ""
            break
    return "".join(out_parts)


def _looks_like_chat(text: str) -> bool:
    """Heuristic: does this user message look like chat/greeting (no real task)?
    Used to decide whether the slim system prompt is appropriate."""
    t = text.strip().lower()
    if not t or len(t) >= 60:
        return False
    GREETING = ("hey", "hi", "hello", "yo", "sup", "thanks", "thank you", "ok", "cool",
                "nice", "lol", "bro", "wow", "great", "good morning", "good night")
    TASK_VERBS = ("read ", "write ", "edit ", "list ", "run ", "show ", "find ", "search ",
                  "check ", "fix ", "create ", "delete ", "open ", "build ", "test ",
                  "deploy ", "commit ", "push ", "pull ", "git ", "make ", "explain ",
                  "summarize ", "analyze ", "implement ", "refactor ", "add ")
    if any(v in t for v in TASK_VERBS):
        return False
    return t.startswith(GREETING) or t in {"?", "??", "hmm", "huh"}


def _build_messages(conversation: list[dict], system: str, model_name: str, cwd: str) -> list[dict]:
    """Build Ollama chat messages from conversation history."""
    # Some models (DeepSeek) handle system prompt better if injected into the first user message
    inject_in_first = "deepseek" in model_name.lower()

    if not inject_in_first:
        messages = [{"role": "system", "content": system}]
    else:
        messages = []

    first_user_processed = False
    for msg in conversation:
        role = msg["role"]
        content = msg["content"]
        if role == "user":
            if inject_in_first and not first_user_processed:
                messages.append({"role": "user", "content": f"{system}\n\nUser request: {content}"})
                first_user_processed = True
            else:
                messages.append({"role": "user", "content": content})
        elif role == "assistant":
            messages.append({"role": "assistant", "content": content})
        elif role == "tool_result":
            messages.append({"role": "user", "content": content})

    if not messages and inject_in_first:
        messages.append({"role": "user", "content": system})

    return messages


def _fix_json_control_chars(s: str) -> str:
    """Escape raw control characters (newlines, tabs) inside JSON string values.

    LLMs often emit literal newlines inside JSON strings instead of \\n.
    This walks the string, tracking whether we're inside a quoted value,
    and escapes any raw control characters found there.
    """
    out = []
    in_str = False
    esc = False
    for ch in s:
        if esc:
            out.append(ch)
            esc = False
            continue
        if ch == '\\' and in_str:
            out.append(ch)
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            out.append(ch)
            continue
        if in_str and ch == '\n':
            out.append('\\n')
            continue
        if in_str and ch == '\t':
            out.append('\\t')
            continue
        if in_str and ch == '\r':
            out.append('\\r')
            continue
        out.append(ch)
    return ''.join(out)


def _normalize_tool_call(call: dict) -> dict:
    """Fix common model quirks in tool call JSON.

    Models sometimes emit flat args instead of nested:
      {"tool": "bash", "command": "ls"}           → {"tool": "bash", "args": {"command": "ls"}}
      {"tool": "read_file", "path": "foo.py"}     → {"tool": "read_file", "args": {"path": "foo.py"}}
      {"tool": "edit_file", "path": "x", "old_str": "a", "new_str": "b"}
        → {"tool": "edit_file", "args": {"path": "x", "old_str": "a", "new_str": "b"}}
    """
    if "tool" in call and "args" not in call:
        tool_name = call["tool"]
        args = {k: v for k, v in call.items() if k != "tool"}
        if args:
            return {"tool": tool_name, "args": args}
    return call


def _parse_tool_call(response: str) -> Optional[tuple[dict, str]]:
    """Extract a tool call from the model's response."""

    # Strip <think> reasoning blocks if present (Qwen 3 models)
    response = re.sub(r'<think>[\s\S]*?</think>', '', response).strip()
    if '</think>' in response:
        response = re.sub(r'<think>[\s\S]*$', '', response).strip()
    else:
        response = response.replace('<think>', '').strip()

    # Phi models (<|end|> is their EOS token). On /api/generate raw everything
    # after <|end|> is noise from the next fake turn the model hallucinates.
    # Truncate early so the ACTION:/tool_call search doesn't scan garbage.
    phi_eos = response.find('<|end|>')
    if phi_eos >= 0:
        response = response[:phi_eos].strip()
    # Strip any remaining Phi turn-boundary tokens that appear before/after
    # the tool call text (e.g. <|start|>assistant injected mid-response).
    response = re.sub(r'<\|start\|>\s*(?:assistant|user|system)\s*', '', response).strip()

    # Pattern 1: <tool_call> JSON [</tool_call>]
    tc_match = re.search(r'<tool_call>([\s\S]*?)(?:</tool_call>|$)', response, re.DOTALL)
    if tc_match:
        raw_json = tc_match.group(1).strip()
        raw_json = re.sub(r'^```(?:json)?\s*', '', raw_json)
        raw_json = re.sub(r'\s*```$', '', raw_json)
        if raw_json:
            raw_json = _fix_json_control_chars(raw_json)
            try:
                call = json.loads(raw_json)
                call = _normalize_tool_call(call)
                if "tool" in call and "args" in call and call["tool"]:
                    return call, response[:tc_match.start()].strip()
                # Recovery: {"tool_name": {...}} — valid JSON but wrong
                # shape (dict keyed by tool name instead of "tool" key).
                # Qwen3.x + Gemma emit this variant when the chat template
                # influences them to use OpenAI function-calling style.
                if isinstance(call, dict) and len(call) == 1 and "tool" not in call:
                    tn, a = next(iter(call.items()))
                    if isinstance(a, dict) and tn:
                        inner = a["args"] if "args" in a and isinstance(a.get("args"), dict) else a
                        if isinstance(inner, dict):
                            return {"tool": tn, "args": inner}, response[:tc_match.start()].strip()
            except json.JSONDecodeError:
                # Recovery for common qwen3.x malformations. Two patterns
                # seen in the wild:
                #
                #   A) {"tool_name", {"args": {...}}}   ← bare-string key
                #   B) {"tool_name": {"arg1": "..."}}   ← dict-keyed
                #
                # Both are "almost right" — extract the leading quoted
                # token as tool name and parse whatever JSON blob follows.
                name_m = re.match(r'\s*\{\s*"([^"]+)"\s*[,:]\s*(.+)$', raw_json, re.DOTALL)
                if name_m:
                    tool_name = name_m.group(1).strip()
                    rest = name_m.group(2).strip()
                    # Three shapes to try on `rest`:
                    #  1. `{"args": {...}}` or `{"path": "..."}` — already
                    #     braced, parse directly (shrinking suffixes to
                    #     drop trailing `}`s from the outer dict).
                    #  2. `"args": {...}` or `"path": "..."` — positional
                    #     kv pairs without outer braces, wrap in {}.
                    #  3. Neither — give up.
                    candidates = [rest]
                    if not rest.startswith("{"):
                        candidates.append("{" + rest)
                    for cand in candidates:
                        for end in range(len(cand), 0, -1):
                            if cand[end - 1] != "}":
                                continue
                            try:
                                parsed = json.loads(cand[:end])
                            except json.JSONDecodeError:
                                continue
                            if isinstance(parsed, dict) and tool_name:
                                # Unwrap "args" if it was wrapped
                                inner = parsed["args"] if "args" in parsed and isinstance(parsed.get("args"), dict) else parsed
                                if isinstance(inner, dict):
                                    return {"tool": tool_name, "args": inner}, response[:tc_match.start()].strip()
                            break

    # Pattern 2: ACTION: {...} (primary format for Qwen 3 and other thinking models)
    # Find the FIRST ACTION: in the response and extract valid JSON after it
    action_pos = response.find("ACTION:")
    if action_pos >= 0:
        after_action = response[action_pos + 7:].lstrip()
        if after_action.startswith("{"):
            # Find matching closing brace by counting nesting
            depth = 0
            in_string = False
            escape = False
            end_pos = None
            for i, ch in enumerate(after_action):
                if escape:
                    escape = False
                    continue
                if ch == '\\' and in_string:
                    escape = True
                    continue
                if ch == '"' and not escape:
                    in_string = not in_string
                    continue
                if in_string:
                    continue
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        end_pos = i + 1
                        break
            if end_pos:
                raw_json = after_action[:end_pos]
                # Models often output raw newlines/tabs inside JSON strings —
                # escape them so json.loads doesn't choke on control characters
                fixed_json = _fix_json_control_chars(raw_json)
                try:
                    call = json.loads(fixed_json)
                    call = _normalize_tool_call(call)
                    if "tool" in call and "args" in call and call["tool"]:
                        return call, response[:action_pos].strip()
                except json.JSONDecodeError:
                    pass

    # Pattern 3: DeepSeek/Native tool calling format
    native_match = re.search(r'tool[\s\S]*?sep[\s\S]*?(\w+)[\s\S]*?```json\s*([\s\S]*?)\s*```', response, re.IGNORECASE)
    if native_match:
        tool_name = native_match.group(1).strip()
        args_json = native_match.group(2).strip()
        try:
            if "\n{" in args_json: args_json = args_json.split("\n{")[0]
            args = json.loads(args_json)
            before = re.sub(r'<[^>]*tool[^>]*>', '', response[:native_match.start()]).strip()
            return {"tool": tool_name, "args": args}, before
        except json.JSONDecodeError:
            pass

    # Pattern 3: Greedy JSON search (order-agnostic)
    # Only runs AFTER we've stripped code-fenced blocks — otherwise a model
    # documenting its plan ("here's what I'll do: ```json{tool:bash...}```")
    # gets its prose JSON fired as a real tool call. Documentation JSON is
    # decorative, not an invocation — only bare or <tool_call>-wrapped JSON
    # should trip the parser.
    stripped = re.sub(r'```[a-zA-Z]*\s*[\s\S]*?```', '', response)
    for pattern in [r'(\{[\s\S]*?"tool"[\s\S]*?"args"[\s\S]*?)', r'(\{[\s\S]*?"args"[\s\S]*?"tool"[\s\S]*?)']:
        json_match = re.search(pattern, stripped)
        if json_match:
            start_index = json_match.start()
            # Try to find the matching closing brace by looking from the end of the string
            # This is a heuristic: we take the longest possible valid JSON starting at our match
            for end_index in range(len(stripped), start_index, -1):
                raw_json = stripped[start_index:end_index].strip()
                if not raw_json.endswith("}"):
                    continue

                # Cleanly strip possible trailing markdown/ChatML tokens before trying to parse
                clean_json = re.sub(r'<\|.*?\|>', '', raw_json).strip()
                clean_json = _fix_json_control_chars(clean_json)
                try:
                    call = json.loads(clean_json)
                    call = _normalize_tool_call(call)
                    if "tool" in call and "args" in call and call["tool"]:
                        # Use position from the stripped text for the "before"
                        # portion. Good-enough approximation; the prefix is
                        # shown as narration so exact offsets don't matter.
                        before = re.sub(r'<\|.*?\|>', '', stripped[:start_index]).strip()
                        return call, before
                except json.JSONDecodeError:
                    continue

    # Pattern 4: CMD: tool args (fallback for simple models)
    cmd_match = re.search(r'(?:\*\*)?CMD(?:\*\*)?[:\s]+(\w+)\s*(.*?)$', response, re.MULTILINE)
    if cmd_match:
        tool = cmd_match.group(1).strip()
        args_str = cmd_match.group(2).strip()
        before = response[:cmd_match.start()].strip()
        if tool == "bash": return {"tool": "bash", "args": {"command": args_str}}, before
        if tool == "read_file": return {"tool": "read_file", "args": {"path": args_str}}, before
        if tool == "list_files": return {"tool": "list_files", "args": {"pattern": args_str or "*"}}, before

    # Pattern 5: ACTION: {...} (legacy support)
    match = re.search(r"ACTION:\s*(\{.*?\})\s*$", response, re.MULTILINE | re.DOTALL)
    if not match:
        match = re.search(r'ACTION:\s*(\{[^}]*"tool"[^}]*"args"[^}]*\{[^}]*\}[^}]*\})', response, re.DOTALL)
    if match:
        try:
            call = json.loads(match.group(1))
            call = _normalize_tool_call(call)
            if "tool" in call and "args" in call and call["tool"]:
                return call, response[:match.start()].strip()
        except json.JSONDecodeError:
            pass

    return None


def _estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 chars per token)."""
    return len(text) // CHARS_PER_TOKEN + 1


def _get_context_limit(model_name: str, big_ctx: bool = False) -> int:
    """Return the raw context limit for a model (native if big_ctx else safe)."""
    key = "native" if big_ctx else "safe"
    model_lower = model_name.lower().strip()
    if model_lower in SUPPORTED_MODELS:
        return SUPPORTED_MODELS[model_lower][key]
    for model_id, info in SUPPORTED_MODELS.items():
        base = model_id.split(":")[0]
        if model_lower.startswith(base):
            return info[key]
    return DEFAULT_SAFE_CONTEXT


def _get_context_budget(model_name: str, big_ctx: bool = False) -> int:
    """Get the input token budget for a model (context limit - response reserve)."""
    return _get_context_limit(model_name, big_ctx) - RESPONSE_RESERVE


def _compact_old_messages(old_messages: list[dict], file_cache: dict[str, str] = None) -> str:
    """Summarize old tool calls and results into a compact context string."""
    import re  # Hoisted from inside the "read_file" branch. Leaving it
              # there meant any message that went through write_file or
              # bash first (without ever hitting read_file) crashed with
              # UnboundLocalError: local variable 're' — which killed
              # the agent mid-task on the first compaction pass for
              # docs-only write tasks (seen on glm-4.7 callbyte runs
              # that wrote README.md then never committed/pushed).

    files_read = []
    files_written = []
    commands_run = []
    key_findings = []

    for msg in old_messages:
        content = msg.get("content", "")
        role = msg.get("role", "")

        # Extract tool actions from assistant messages
        if role == "assistant":
            if "read_file" in content:
                path_match = re.search(r'"path":\s*"([^"]+)"', content)
                if path_match:
                    files_read.append(path_match.group(1))
            elif "write_file" in content:
                path_match = re.search(r'"path":\s*"([^"]+)"', content)
                if path_match:
                    files_written.append(path_match.group(1))
            elif "bash" in content:
                cmd_match = re.search(r'"command":\s*"([^"]{1,80})', content)
                if cmd_match:
                    commands_run.append(cmd_match.group(1))
            # Keep substantive assistant responses (not tool calls)
            elif "<tool_call>" not in content and "ACTION:" not in content and len(content) > 50:
                key_findings.append(content[:200])

    parts = ["[Summary of earlier work in this session]"]
    if files_written:
        unique = list(dict.fromkeys(files_written))[:10]
        parts.append(f"Files created/modified: {', '.join(unique)}")
    if commands_run:
        parts.append(f"Commands run: {'; '.join(commands_run[:5])}")

    # Inject file cache summaries — these survive truncation
    if file_cache:
        parts.append("Files you already read (DO NOT re-read these):")
        for summary in list(file_cache.values())[:20]:
            parts.append(f"  - {summary}")

    if key_findings:
        for finding in key_findings[:3]:
            parts.append(f"Finding: {finding}")

    return "\n".join(parts) if len(parts) > 1 else parts[0]


def _truncate_history(conversation: list[dict], model: str = "default", system_prompt_len: int = 0, file_cache: dict[str, str] = None, big_ctx: bool = False) -> list[dict]:
    """Smart context management: compact old messages, keep recent ones.
    
    system_prompt_len: estimated tokens in the system prompt that will be added.
    """
    if len(conversation) <= 1:
        return conversation

    total_safe_limit = _get_context_limit(model, big_ctx=big_ctx)

    # Budget for history = Total Limit - System Prompt - Response Reserve
    budget = total_safe_limit - system_prompt_len - RESPONSE_RESERVE
    
    # Minimum floor for history
    if budget < 1024:
        budget = 1024 

    total_tokens = sum(_estimate_tokens(m["content"]) for m in conversation)

    if total_tokens <= budget:
        return conversation

    # Always keep the first message (the original goal)
    first = conversation[0]
    first_tokens = _estimate_tokens(first["content"])
    remaining_budget = budget - first_tokens

    # Walk backwards from the end, keeping recent messages
    remaining = conversation[1:]
    kept = []
    used = 0
    for msg in reversed(remaining):
        msg_tokens = _estimate_tokens(msg["content"])
        if used + msg_tokens > remaining_budget:
            break
        kept.insert(0, msg)
        used += msg_tokens

    dropped = remaining[:len(remaining) - len(kept)]
    result = [first]
    if dropped:
        summary = _compact_old_messages(dropped, file_cache=file_cache)
        result.append({"role": "tool_result", "content": summary})
    result.extend(kept)
    return result


def _render_status_bar(agent) -> Group:
    """Render a Rich version of the prompt_toolkit bottom_toolbar so the
    bar stays visible during generation. Mirrors the colors used in
    pw_agent._bottom_toolbar (slate border + cyan/green/amber/purple parts).
    """
    import shutil
    width = max(40, shutil.get_terminal_size((120, 20)).columns)
    border = Text("━" * width, style="#475569")

    parts = (agent.status_text or "").split(" | ")
    colors = ["bold #22D3EE", "bold #4ADE80", "bold #FBBF24", "bold #C084FC", "bold #C084FC"]
    icons = ["🧠 ", "🖥️ ", "⚙️ ", "", ""]

    line = Text("  ")
    for i, p in enumerate(parts):
        if not p.strip():
            continue
        if i > 0:
            line.append("    │    ", style="#475569")
        prefix = icons[i] if i < len(icons) else ""
        style = colors[i] if i < len(colors) else "bold #C084FC"
        # Skip prefix if value already starts with that emoji
        if prefix and p.lstrip().startswith(prefix.strip()):
            line.append(p, style=style)
        else:
            line.append(prefix + p, style=style)

    if model_supports_thinking(agent.client.model):
        line.append("    │    ", style="#475569")
        if agent.thinking:
            line.append("🧠 Think: ON", style="bold #E879F9")
        else:
            line.append("🧠 Think: OFF", style="#64748B")

    return Group(border, line)


class Agent:
    """ReAct agent that uses an LLM to perform coding tasks."""

    def __init__(self, client: LLMClient, stream: bool = True, status_text: str = "", plan_mode: bool = False, thinking: bool = False, quiet: bool = False, memory_store=None, output_format: str = "text", big_ctx: bool = False, max_iterations: int = MAX_ITERATIONS, session_id: str = "", num_ctx_override: int = None):
        self.client = client
        self.stream = stream
        # Hard cap on tool-call turns per prompt. Default 50 is safe for
        # interactive use; CallByte / autonomous dispatchers can raise it
        # (e.g. --max-iterations 200) for long multi-file tasks.
        self.max_iterations = max_iterations
        self.conversation: list[dict] = []
        self.thinking = thinking and model_supports_thinking(client.model)
        # big_ctx: request model's native context instead of the safe cap.
        # Ollama will auto-offload layers to CPU if it overflows VRAM —
        # slower but lets you use the full native context (e.g. 256K).
        self.big_ctx = big_ctx
        # Auto-injection toggles. Off = stop padding the prompt with memory
        # recall / RAG chunks, which can blow the context budget on small
        # models when the user just wants a focused chat.
        self.memory_enabled = True
        self.rag_enabled = True
        self.quiet = quiet  # Suppress all UI chrome (for -p one-shot mode)
        self.output_format = output_format  # text, stream-json, json
        self.last_thinking = ""  # Last thinking block (for fold/unfold)
        self.memory = memory_store  # MemPalace per-project memory store (optional)
        self.global_memory = None  # Cross-project user profile store (set by pw_agent.main)
        self.file_cache: dict[str, str] = {}  # path → summary of files read this session
        self.cwd = os.getcwd()
        self.session_id = session_id  # Empty string = key by cwd; non-empty = persistent named session
        self.num_ctx_override = num_ctx_override  # Explicit context-window override (--num-ctx)
        self.status_text = status_text  # Bottom bar text to show during generation
        self.files_in_context: list[str] = []
        self.interrupted = False
        self.plan_mode = plan_mode
        self.typeahead = ""  # Text typed during generation, pre-filled into next prompt
        # Per-turn token + retrieval stats. Ring buffer of last 20 turns so
        # /stats and /waste can inspect without ballooning memory.
        self.turn_stats: list[dict] = []
        self.TURN_STATS_CAP = 20
        # Skills — loaded once at startup, refreshed on /skills reload
        self.skills = load_skills(self.cwd)
        self.loaded_skill_ids: set[str] = set()  # Track which skills have been auto-loaded
        # MCP — start configured servers in the background, expose their
        # tools alongside native ones. Subagents share the parent's MCP.
        self.mcp = MCPManager() if not getattr(self, "is_subagent", False) else None
        self._mcp_tools_cache: list[dict] = []
        # Codebase RAG index — lazily loaded on first search or /index command
        # In cloud mode, the index proxies embeddings through the broker to
        # the user's active fleet brain. In direct mode it hits the brain's
        # local Ollama directly.
        ollama_url = client.brain_url if client.direct_mode else "http://localhost:11434"
        self.codebase = CodebaseIndex(self.cwd, ollama_url=ollama_url, client=client)
        # Auto-index or incremental re-index in the background so the first
        # retrieval has fresh data. Keeps session startup fast; format_context
        # returns "" until the index lands, so early queries degrade gracefully.
        if not getattr(self, "is_subagent", False):
            try:
                self._ensure_codebase_indexed_async()
            except Exception:
                pass  # Best-effort — user can still /index manually
        # Voice mode — when on, auto-speak every final answer through fleet TTS
        self.voice_mode = False
        # Fleet heartbeat — writes our state for sibling pw-agent instances
        # to discover. Subagents share the parent's heartbeat.
        if not getattr(self, "is_subagent", False):
            try:
                self.fleet = FleetHeartbeat(self)
            except Exception:
                self.fleet = None
        else:
            self.fleet = None

    def run(self, user_input: str) -> None:
        """Process a user message through the ReAct loop with loop detection."""
        # Kick off the /api/ps realign probe in a background thread BEFORE
        # we do anything else. It overlaps with hook + memory retrieval +
        # codebase retrieval (~500-1500ms of embed calls below), so by the
        # time chat_stream needs the aligned model the probe has usually
        # finished and adds zero user-perceived latency.
        try:
            self.client.realign_async()
        except Exception:
            pass  # Best-effort — chat_stream has a sync fallback

        # user_prompt_submit hook — can block or augment the prompt
        allowed, hook_out = run_hook("user_prompt_submit", {"prompt": user_input})
        if not allowed:
            if not self.quiet:
                console.print(f"  [yellow]⚠ Prompt blocked by hook: {hook_out}[/yellow]")
            return
        if hook_out:
            user_input = f"{user_input}\n\n[hook context]:\n{hook_out}"
            if not self.quiet:
                console.print(f"  [dim]🪝 user_prompt_submit hook injected {len(hook_out)} chars[/dim]")

        self.conversation.append({"role": "user", "content": user_input})

        # Breathing room between the user's last message and the assistant's
        # thinking/spinner line — otherwise they collide visually.
        if not self.quiet:
            console.print()

        # The first 500-1500 ms of a turn are embed calls (memory + codebase).
        # Keep the status bar visible throughout by running the whole turn
        # inside a persistent Rich Live whose content is updated as state
        # changes. Without this the bar vanished every time prompt_toolkit's
        # bottom_toolbar was not active — between prompts, during embeds,
        # between tool calls.
        prep_live = None
        _SPINNER_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        _spinner_idx = [0]
        prep_label = [f"{_SPINNER_FRAMES[0]} Preparing context..."]
        if not self.quiet:
            def _prep_render():
                # Advance the spinner frame each time the Live block re-renders
                # (Rich calls this at refresh_per_second=10, so the animation
                # is driven by the render cycle — no extra thread needed).
                frame = _SPINNER_FRAMES[_spinner_idx[0] % len(_SPINNER_FRAMES)]
                _spinner_idx[0] += 1
                tail = prep_label[0].split(" ", 1)[1] if " " in prep_label[0] else prep_label[0]
                return Group(
                    Text(f"{frame} {tail}", style="cyan"),
                    _render_status_bar(self),
                )
            try:
                prep_live = Live(_prep_render(), console=console,
                                 refresh_per_second=10, transient=True)
                prep_live.__enter__()
                # Stash an updater on self so we can refresh between sub-phases
                self._prep_live = prep_live
                self._prep_update = lambda label: (
                    prep_label.__setitem__(0, label),
                    prep_live.update(_prep_render()),
                )
            except Exception:
                prep_live = None
                self._prep_live = None
                self._prep_update = None

        # Retrieve relevant memories + codebase context concurrently.
        # All three embed calls are independent (global_memory, memory,
        # codebase) so we fan them out with a thread pool and wait for all
        # three at once.  Total latency drops from sum-of-three to
        # max-of-three — typically 1-3 s instead of 3-9 s.
        #
        # format_context now returns (str, raw_hits) so we avoid a second
        # redundant embed call for /stats and /waste accounting.
        memory_context = ""
        mem_avg_sim = 0.0
        mem_hit_count = 0
        codebase_context = ""
        code_avg_sim = 0.0
        code_hit_count = 0

        _do_global = self.memory_enabled and self.global_memory and self.global_memory.size > 0
        _do_memory = self.memory_enabled and self.memory and self.memory.size > 0
        _do_codebase = bool(self.codebase and self.rag_enabled and _looks_like_chat(user_input) is False)

        def _fetch_global():
            try:
                return self.global_memory.format_context(user_input)
            except Exception:
                return "", []

        def _fetch_memory():
            try:
                return self.memory.format_context(user_input)
            except Exception:
                return "", []

        def _fetch_codebase():
            try:
                return self.codebase.format_context(user_input)
            except Exception:
                return "", []

        _futures = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as _pool:
            if _do_global:
                _futures["global"] = _pool.submit(_fetch_global)
            if _do_memory:
                _futures["memory"] = _pool.submit(_fetch_memory)
            if _do_codebase:
                _futures["codebase"] = _pool.submit(_fetch_codebase)
            # Results are collected after all futures complete (pool __exit__
            # blocks until all submitted tasks finish).

        # Unpack global memory result
        _mem_parts = []
        if "global" in _futures:
            try:
                gctx, _ = _futures["global"].result()
                if gctx:
                    _mem_parts.append(gctx)
            except Exception:
                pass

        # Unpack project memory result; derive stats from raw hits
        if "memory" in _futures:
            try:
                pctx, raw_hits = _futures["memory"].result()
                if pctx:
                    _mem_parts.append(pctx)
                mem_hit_count = len(raw_hits)
                if raw_hits:
                    mem_avg_sim = sum(s for _, s in raw_hits) / len(raw_hits)
            except Exception:
                pass

        memory_context = "\n\n".join(_mem_parts)
        if memory_context and not self.quiet:
            count = memory_context.count("\n- ")
            console.print(f"  [dim]📚 Retrieved {count} memories[/dim]")

        # Unpack codebase result; derive stats from raw hits
        if "codebase" in _futures:
            try:
                codebase_context, raw_hits = _futures["codebase"].result()
                codebase_context = codebase_context or ""
                if codebase_context and not self.quiet:
                    hit_count = codebase_context.count("\n### ")
                    console.print(f"  [dim]🧭 Retrieved {hit_count} code chunks[/dim]")
                code_hit_count = len(raw_hits)
                if raw_hits:
                    code_avg_sim = sum(s for _, s in raw_hits) / len(raw_hits)
            except Exception:
                pass  # Best-effort — agent can still call search_codebase manually

        # Auto-trigger relevant skills based on the query.
        # We inject the skill body as a tool_result so the model picks it
        # up as just-in-time context, only the first time per session.
        if self.skills:
            try:
                triggered = find_relevant_skills(user_input, self.skills, top_k=2)
                for skill in triggered:
                    if skill.id in self.loaded_skill_ids:
                        continue
                    self.loaded_skill_ids.add(skill.id)
                    if not self.quiet:
                        console.print(f"  [dim]🎯 Loaded skill: {skill.name}[/dim]")
                    body = skill.body[:6000]  # Cap body to avoid blowing context
                    self.conversation.append({
                        "role": "tool_result",
                        "content": f"[Skill auto-loaded: {skill.name}]\n\n{body}",
                    })
            except Exception:
                pass  # Skill loading is best-effort

        # Loop detection state
        tool_call_log: list[str] = []  # Track "tool:args" signatures
        has_used_any_tool = False  # True once any tool has run (never resets — for hallucination check)
        stall_count = 0  # Count consecutive non-tool responses
        read_count = 0  # Track read-only operations without writes
        has_written = False  # Whether model has produced any output files
        consecutive_tool_errors = 0  # Short-circuit when a model keeps
                                      # emitting tool calls that fail — weaker
                                      # models (qwen3.6, gemma, qwen3.5) often
                                      # lose the plot after 3+ errors in a row
                                      # and hallucinate "no task context"
        MAX_TOOL_ERRORS = 5
        empty_retries = 0  # Retry budget for "empty response" turns — qwen3.x
                           # sometimes returns pure thinking with no final
                           # content. One retry with an explicit nudge often
                           # unsticks it without user intervention.
        MAX_EMPTY_RETRIES = 1

        self.interrupted = False

        for iteration in range(self.max_iterations):
            if self.interrupted:
                self._close_prep_live()
                console.print("\n  [yellow]⚠ Interrupted[/yellow]")
                self._auto_save()
                return

            # 1. Build the system prompt. On a chat-style first turn we use a
            # ~1KB slim prompt instead of the full ~10KB context blob — tools,
            # MCP schemas, git, project context aren't needed to say "hi" and
            # they roughly halve TTFT on small local models.
            use_slim = (iteration == 0 and _looks_like_chat(user_input))
            if use_slim:
                skills_summary = ""
                mcp_tools = []
            else:
                skills_summary = format_skills_for_prompt(self.skills) if self.skills else ""
                mcp_tools = self._mcp_tools_cache or (self.mcp.list_tools() if self.mcp else [])
                self._mcp_tools_cache = mcp_tools  # Cache for subsequent iterations
            system = _get_system_prompt(self.cwd, self.client, self.plan_mode, memory_context=("" if use_slim else memory_context), skills_summary=skills_summary, is_subagent=getattr(self, "is_subagent", False), mcp_tools=mcp_tools, slim=use_slim, codebase_context=("" if use_slim else codebase_context))
            system_len = _estimate_tokens(system)

            # 2. Truncate history based on what's left in the safe budget
            trimmed = _truncate_history(self.conversation, self.client.model, system_prompt_len=system_len, file_cache=self.file_cache, big_ctx=self.big_ctx)

            # 3. Build final message list
            messages = _build_messages(trimmed, system, self.client.model, self.cwd)

            # ── Record per-turn stats (first iteration only, so /stats tracks
            # the prompt the model ACTUALLY sees for this user input).
            if iteration == 0:
                hist_tokens = sum(_estimate_tokens(str(m.get("content", ""))) for m in trimmed if m.get("role") != "system")
                mem_ctx_tokens = _estimate_tokens(memory_context) if memory_context else 0
                code_ctx_tokens = _estimate_tokens(codebase_context) if codebase_context else 0
                # system_len includes memory+code — break them out so the
                # breakdown adds up cleanly.
                sys_core_tokens = max(0, system_len - mem_ctx_tokens - code_ctx_tokens)
                truncated_n = len(self.conversation) - len(trimmed)
                stat = {
                    "user_input": user_input[:120],
                    "use_slim": use_slim,
                    "model": self.client.model,
                    "system_core_tokens": sys_core_tokens,
                    "memory_ctx_tokens": mem_ctx_tokens,
                    "codebase_ctx_tokens": code_ctx_tokens,
                    "history_tokens": hist_tokens,
                    "total_tokens": system_len + hist_tokens,
                    "mem_hits": mem_hit_count,
                    "mem_avg_sim": round(mem_avg_sim, 3),
                    "code_hits": code_hit_count,
                    "code_avg_sim": round(code_avg_sim, 3),
                    "mcp_tool_count": len(mcp_tools),
                    "truncated": truncated_n,
                    "duplicate_calls": 0,  # filled in later when dup_count increments
                    "timestamp": time.time(),
                }
                self.turn_stats.append(stat)
                if len(self.turn_stats) > self.TURN_STATS_CAP:
                    self.turn_stats.pop(0)
            
            # 4. Use the TOTAL context limit as the budget for Ollama
            # (native when big_ctx is on, else the VRAM-safe cap).
            # --num-ctx override wins over both when set by the dispatcher.
            budget = self.num_ctx_override or _get_context_limit(self.client.model, big_ctx=self.big_ctx)

            # Get response (streaming or not)
            thinking_msg = random.choice(THINKING_MESSAGES)
            if self.thinking:
                thinking_msg = "🧠 " + thinking_msg
            # Close the prep-phase Live (embed retrieval) before opening the
            # chat-stream Live — Rich doesn't permit two live regions on the
            # same console. The gap is ~1ms, imperceptible to the user.
            self._close_prep_live()
            if self.stream:
                response = self._stream_response(messages, thinking_msg, context_length=budget)
            else:
                # Live with bar + spinner so the bottom status bar stays
                # visible during the blocking (non-stream) chat call.
                spinner = Spinner("dots", text=Text(thinking_msg, style="cyan"))
                with Live(Group(spinner, _render_status_bar(self)), console=console,
                          refresh_per_second=10, transient=True):
                    response = self.client.chat(messages, context_length=budget)

            # Detect narrated-execution pattern BEFORE stripping so we can
            # correct the model rather than silently emptying the response.
            # gpt-oss / qwen35moe sometimes outputs "🔧 bash: <cmd> ✓" text
            # instead of a real <tool_call>. We catch it here and inject a
            # correction so the model stops looping on this pattern.
            _narrated_exec = bool(response) and bool(
                re.search(r'(?:🔧|💻|📄|✏️)\s*\w+\s*[:：].*✓', response)
                or re.search(r'\b(?:bash|read_file|write_file|edit_file|grep|list_files)\s*[:：]\s*\S', response)
            )
            if _narrated_exec:
                if not self.quiet:
                    console.print("\n  [dim]↳ Narrated tool execution detected — prompting for real tool call...[/dim]")
                self.conversation.append({"role": "assistant", "content": response})
                self.conversation.append({"role": "user", "content": (
                    "You wrote text describing a tool call instead of actually calling it. "
                    "To run a command, emit a real tool call:\n"
                    "<tool_call>{\"tool\":\"bash\",\"args\":{\"command\":\"<your command here>\"}}</tool_call>\n"
                    "Do not narrate. Call the tool now."
                )})
                stall_count += 1
                continue

            # Strip model artifacts (think blocks, stop tokens)
            if response:
                response = re.sub(r'<think>[\s\S]*?</think>', '', response).strip()
                if '</think>' in response:
                    response = re.sub(r'<think>[\s\S]*$', '', response).strip()
                else:
                    response = response.replace('<think>', '').strip()
                response = response.replace('<end_of_turn>', '').replace('<|im_end|>', '').strip()
                # Strip any Gemma-template start markers that leaked through
                # before the stop token kicked in, including the role line and
                # any hallucinated following content on that same line:
                #   <start_of_turn>user  →  removed
                #   <start_of_turn>model →  removed
                response = re.sub(r'<start_of_turn>\s*\w*\s*\n?', '', response).strip()

            if not response or response.startswith("[Error:"):
                # Debug: show what was sent
                if os.environ.get("PW_DEBUG"):
                    console.print(f"  [dim]DEBUG: sent {len(messages)} messages, got: {repr(response[:200])}[/dim]")
                # Auto-retry on empty response. qwen3.x occasionally returns
                # pure thinking content with an empty final channel. A single
                # retry with an explicit nudge usually produces a real answer.
                # Only retries if the error isn't a brain/transport error —
                # those have their own retry in llm_client.
                is_plain_empty = not response
                if is_plain_empty and empty_retries < MAX_EMPTY_RETRIES:
                    empty_retries += 1
                    if not self.quiet:
                        console.print(f"  [dim]↳ Empty response — retrying with nudge ({empty_retries}/{MAX_EMPTY_RETRIES})[/dim]")
                    self.conversation.append({"role": "assistant", "content": ""})
                    self.conversation.append({"role": "user", "content": (
                        "Your previous reply was empty. Either emit a tool call "
                        "as <tool_call>{\"tool\":\"...\",\"args\":{...}}</tool_call> "
                        "or a plain-text final answer. Do not return an empty response."
                    )})
                    continue
                if self.quiet and self.output_format in ("stream-json", "json"):
                    import json as _json
                    err_obj = {"type": "result", "subtype": "error", "result": response or "[Empty response from model]", "is_error": True}
                    print(_json.dumps(err_obj))
                else:
                    console.print(f"  [red]{response or '[Empty response from model]'}[/red]")
                return

            # Check for tool call
            parsed = _parse_tool_call(response)

            if not parsed and self.stream and not self.quiet:
                # Show unparsed tool-like output only on first occurrence
                if "<tool_call>" in response or "<｜tool" in response or "<|im_start|>" in response:
                    if stall_count == 0:  # Only show once, not on every retry
                        console.print(f"\n[dim]────── (Unparsed output) ──────[/dim]\n{response[:300]}\n")

            if parsed:
                tool_call, thinking = parsed
                tool_name = tool_call["tool"]
                tool_args = tool_call["args"]
                stall_count = 0  # Reset stall counter — model is making progress
                has_used_any_tool = True  # Permanent flag — suppresses hallucination check

                # Loop detection — check for duplicate tool calls
                call_sig = f"{tool_name}:{json.dumps(tool_args, sort_keys=True)}"
                dup_count = tool_call_log.count(call_sig)
                if dup_count >= 1 and self.turn_stats:
                    self.turn_stats[-1]["duplicate_calls"] = self.turn_stats[-1].get("duplicate_calls", 0) + 1
                tool_call_log.append(call_sig)

                if dup_count >= MAX_DUPLICATE_CALLS:
                    if dup_count >= MAX_LOOP_HARD_STOP:
                        # Model is hopelessly stuck — force stop
                        if not self.quiet:
                            console.print(f"\n  [yellow]⚠ Model stuck in loop. Stopping.[/yellow]")
                        self._auto_save()
                        return
                    if not self.quiet:
                        console.print(f"\n  [yellow]⚠ Detected loop: {tool_name} called {dup_count + 1} times with same args. Moving on.[/yellow]")
                    self.conversation.append({"role": "user", "content": "STOP calling the same tool. You already have the result. Use what you have and proceed to the next step or give your answer NOW."})
                    continue

                if not self.quiet:
                    # Print thinking text — compact, one line
                    if thinking:
                        short = thinking.split("\n")[0][:100].strip()
                        if short:
                            console.print(f"\n  [dim]{short}[/dim]")

                    # Tool call — bold and visible with icon
                    TOOL_ICONS = {
                        "read_file": "📄", "write_file": "✏️", "edit_file": "🔧",
                        "bash": "💻", "list_files": "📁", "grep": "🔍",
                        "web_search": "🌐", "web_fetch": "🔗",
                        "spawn_agent": "🤖", "spawn_agents": "🤖",
                        "search_codebase": "🧭", "speak_text": "🔊",
                        "query_fleet": "🛰️",
                    }
                    icon = TOOL_ICONS.get(tool_name, "⚡")
                    args_display = []
                    for k, v in tool_args.items():
                        if isinstance(v, str) and len(v) > 200:
                            # Show head+tail for long strings (bash commands,
                            # str_replace diffs) so the user can still see
                            # what's running without flooding the UI.
                            args_display.append(f'{k}="{v[:120]} … {v[-60:]}"')
                        else:
                            args_display.append(f'{k}="{v}"' if isinstance(v, str) else f'{k}={v}')
                    args_str = ", ".join(args_display)
                    console.print(f"\n  {icon} [bold cyan]{tool_name}[/bold cyan]({args_str})")

                # Emit tool_use NDJSON event (Claude stream-json schema).
                # One id per call so the consumer can pair it with the
                # matching tool_result event.
                _tool_use_id = f"tool_{iteration}_{len(self.conversation)}"
                self._emit_event({
                    "type": "tool_use",
                    "id": _tool_use_id,
                    "name": tool_name,
                    "input": tool_args,
                })

                # Pre-tool-use hook — can block the call
                allowed, hook_out = run_hook("pre_tool_use", {"tool": tool_name, "args": tool_args})
                if hook_out and not self.quiet:
                    console.print(f"  [dim]🪝 {hook_out}[/dim]")
                if not allowed:
                    if not self.quiet:
                        console.print(f"  [yellow]⚠ pre_tool_use hook blocked {tool_name}[/yellow]")
                    result = f"Tool call blocked by pre_tool_use hook: {hook_out or 'no reason given'}"
                    # Skip execution but still record so the model sees the block
                    tc_str = json.dumps({"tool": tool_name, "args": tool_args})
                    self.conversation.append({"role": "assistant", "content": f"<tool_call>\n{tc_str}\n</tool_call>"})
                    self.conversation.append({"role": "tool_result", "content": f"Result:\n{result}"})
                    continue

                # MCP tools — namespaced as mcp_<server>_<tool>
                if tool_name.startswith("mcp_") and self.mcp:
                    result = self.mcp.call_tool(tool_name, tool_args)
                elif tool_name == "query_fleet":
                    result = query_fleet(tool_args.get("filter", ""), client=self.client)
                elif tool_name == "speak_text":
                    from voice import speak_text
                    text = tool_args.get("text", "")
                    voice_model = tool_args.get("voice", "")
                    result = speak_text(text, self.client, voice_model=voice_model)
                elif tool_name == "search_codebase":
                    if not self.codebase.is_indexed:
                        result = "Error: codebase not indexed yet. Tell the user to run /index first."
                    else:
                        query = tool_args.get("query", "")
                        top_k = int(tool_args.get("top_k", 8))
                        top_k = max(1, min(top_k, 20))
                        results = self.codebase.search(query, top_k=top_k)
                        result = self.codebase.format_results(query, results)
                # Subagent tools — handled here because they need self
                elif tool_name == "spawn_agent":
                    from subagent import run_subagent
                    sub_task = tool_args.get("task", "")
                    if not sub_task:
                        result = "Error: spawn_agent requires a 'task' arg"
                    elif getattr(self, "is_subagent", False):
                        result = "Error: subagents cannot spawn other subagents"
                    else:
                        if not self.quiet:
                            console.print(f"  [dim]🤖 Spawning subagent: {sub_task[:80]}...[/dim]")
                        result = run_subagent(self, sub_task)
                elif tool_name == "spawn_agents":
                    from subagent import run_subagents_parallel
                    sub_tasks = tool_args.get("tasks", [])
                    if not isinstance(sub_tasks, list) or not sub_tasks:
                        result = "Error: spawn_agents requires a non-empty 'tasks' list"
                    elif getattr(self, "is_subagent", False):
                        result = "Error: subagents cannot spawn other subagents"
                    else:
                        if not self.quiet:
                            console.print(f"  [dim]🤖 Spawning {len(sub_tasks)} parallel subagents[/dim]")
                        answers = run_subagents_parallel(self, sub_tasks)
                        # Format as numbered list
                        result = "\n\n".join(f"--- Subagent {i+1} ---\n{a}" for i, a in enumerate(answers))
                else:
                    # Execute tool normally
                    result = execute_tool(tool_name, tool_args)

                # Post-tool-use hook — informational
                _, post_out = run_hook("post_tool_use", {"tool": tool_name, "args": tool_args, "result": result[:1000]})
                if post_out and not self.quiet:
                    console.print(f"  [dim]🪝 {post_out}[/dim]")

                # Print result summary — compact but informative
                if not self.quiet:
                    lines = result.split("\n")
                    if tool_name == "read_file":
                        console.print(f"  [dim]   ↳ {len(lines)} lines read[/dim]")
                    elif tool_name in ("list_files", "grep"):
                        count = min(len(lines), 10)
                        for line in lines[:count]:
                            console.print(f"  [dim]   {line}[/dim]")
                        if len(lines) > count:
                            console.print(f"  [dim]   ... and {len(lines) - count} more[/dim]")
                    elif tool_name == "bash":
                        display = result[:300]
                        if len(result) > 300:
                            display += "..."
                        console.print(f"  [dim]   ↳ {display}[/dim]")
                    elif tool_name in ("write_file", "edit_file"):
                        console.print(f"  [green]   ↳ {result}[/green]")
                    else:
                        display = result[:200] + "..." if len(result) > 200 else result
                        console.print(f"  [dim]   ↳ {display}[/dim]")

                # Update fleet heartbeat with this file activity
                if self.fleet and tool_name in ("read_file", "write_file", "edit_file", "str_replace"):
                    fpath = tool_args.get("path", "")
                    if fpath:
                        try:
                            self.fleet.note_file(fpath)
                        except Exception:
                            pass

                # Track read vs write balance — count the write only if it
                # actually succeeded. Models hallucinating an implementation
                # will fire write_file calls against paths that don't exist
                # (dir missing etc), get "Error:" back, and pretend the file
                # shipped. We mustn't mark has_written in that case — that's
                # exactly what the hallucination defense checks for.
                if tool_name in ("write_file", "edit_file") and not result.startswith("Error"):
                    has_written = True
                    read_count = 0
                    tool_call_log.clear()  # Reset loop detection — filesystem changed
                    # Refresh the codebase index in background so subsequent
                    # retrieval queries see the new content. Non-blocking; the
                    # async helper skips if a reindex is already in flight.
                    try:
                        self._ensure_codebase_indexed_async()
                    except Exception:
                        pass
                elif tool_name == "bash":
                    # Clear loop detection ONLY for the non-last entries —
                    # keep the last call signature so identical bash calls
                    # in a row still register as a loop. Without this, a
                    # model stuck in a `python3 << PYEOF` read-file pattern
                    # would re-run the same script unbounded since every
                    # bash invocation reset the dup counter.
                    last = tool_call_log[-1] if tool_call_log else None
                    tool_call_log.clear()
                    if last is not None:
                        tool_call_log.append(last)
                elif tool_name in ("read_file", "list_files", "grep"):
                    read_count += 1

                # Nudge model to start writing after too many reads
                if read_count >= 15 and not has_written:
                    if not self.quiet:
                        console.print(f"\n  [yellow]⚠ {read_count} reads without writing. Time to start coding.[/yellow]")
                    self.conversation.append({"role": "user", "content": "You have read enough files. You understand the codebase. NOW START WRITING CODE. Create the files. Do not read any more files."})
                    read_count = 0
                    continue

                # Build file summary cache — survives context truncation
                if tool_name == "read_file" and not result.startswith("Error:"):
                    file_path = tool_args.get("path", "")
                    lines = result.split("\n")
                    line_count = len(lines)
                    # Extract first few meaningful lines as summary
                    preview_lines = [l.strip() for l in lines[:5] if l.strip() and not l.strip().startswith("[File has")]
                    preview = "; ".join(preview_lines)[:150]
                    self.file_cache[file_path] = f"{file_path} ({line_count} lines): {preview}"

                # Add to conversation — truncate large results to save context.
                # 1KB was too tight — bash / read_file outputs truncated at 1KB
                # caused the model to re-run the same command with different
                # invocations looking for the "missing" content, which we saw
                # manifest as `python3 << PYEOF` heredoc loops. 8KB gives the
                # model enough of a view to decide without shaving too many
                # tokens from the context budget.
                CAP = 8000
                truncated_result = result[:CAP] + f"\n...[truncated, {len(result)} chars total]" if len(result) > CAP else result
                # Track consecutive tool errors — short-circuit if the model
                # keeps firing calls that fail. Protects against the "six
                # failed edit_file calls → model gives up with 'no context'"
                # pattern on weaker local models.
                if result.startswith("Error"):
                    consecutive_tool_errors += 1
                else:
                    consecutive_tool_errors = 0
                # Store <tool_call> format in history so model learns the pattern
                tc_str = json.dumps({"tool": tool_name, "args": tool_args})
                self.conversation.append({"role": "assistant", "content": f"<tool_call>\n{tc_str}\n</tool_call>"})
                self.conversation.append({"role": "tool_result", "content": f"Result:\n{truncated_result}"})

                if consecutive_tool_errors >= MAX_TOOL_ERRORS:
                    abort_msg = (
                        f"⚠ Aborting turn: {consecutive_tool_errors} consecutive "
                        f"tool errors. Last error: {result[:300]}. The model "
                        f"isn't recovering — try a more specific prompt or a "
                        f"stronger model."
                    )
                    if not self.quiet:
                        console.print(f"\n  [yellow]{abort_msg}[/yellow]")
                    # Emit a clean error result and bail instead of letting
                    # the model spiral further into context confusion.
                    if self.quiet and self.output_format in ("stream-json", "json"):
                        import json as _json
                        print(_json.dumps({
                            "type": "result",
                            "subtype": "error",
                            "result": abort_msg,
                            "turns": iteration,
                            "has_written": has_written,
                            "is_error": True,
                        }))
                    return

                # Emit tool_result NDJSON event paired with the tool_use id.
                # Cap output at 2KB so a massive bash dump doesn't blow the
                # consumer's parser; the agent still sees the truncated result
                # in-conversation via `truncated_result` above.
                self._emit_event({
                    "type": "tool_result",
                    "tool_use_id": _tool_use_id,
                    # 2KB was too tight for UIs wanting to show the full
                    # output; 16KB covers almost every real tool result
                    # without blowing the consumer's event buffer.
                    "content": result[:16000],
                    "is_error": result.startswith("Error:"),
                })

            else:
                stall_count += 1
                response_lower = response.lower()

                # Detect hallucination — model makes specific claims about THIS project
                # without having used any tools. Only trigger on definitive statements
                # about the project's state, not general capability descriptions.
                hallucination_signs = [
                    "the main branch", "the master branch", "no main branch",
                    "i checked the", "i can see that", "i found that",
                    "this project has", "this repo has", "this codebase",
                    "there is no branch", "there are no files",
                    "the project contains", "the code shows",
                ]
                is_hallucinating = (
                    not has_used_any_tool and
                    any(w in response_lower for w in hallucination_signs) and
                    stall_count <= MAX_STALLS
                )

                # Detect narration without action. Skip this check when the user's last
                # message looks like a chat/greeting (no task), so a text-only reply is fine.
                last_user_msg = ""
                for _m in reversed(self.conversation):
                    if _m.get("role") == "user":
                        last_user_msg = str(_m.get("content", "")).strip()
                        break
                is_chat_input = _looks_like_chat(last_user_msg)
                narration_words = ["let me check", "i'll read", "i'll look", "let me look",
                                   "i'll start by", "let me start", "i'll explore", "let me explore",
                                   "let me fix", "i'll fix", "let me try", "i'll try",
                                   "which approach", "please let me know",
                                   "let me examine", "i'll examine", "let me analyze", "i'll analyze"]
                is_narrating = (
                    any(w in response_lower for w in narration_words)
                    and stall_count <= MAX_STALLS
                    and not (iteration == 0 and is_chat_input)
                )

                # Detect broken tool_call tags (model outputs <tool_call> without valid JSON)
                is_broken_tool = "<tool_call>" in response and not _parse_tool_call(response)
                # Detect decorative fenced-JSON tool calls — the parser now
                # (correctly) ignores ```json {tool: ...} ``` as documentation,
                # but if the model's ENTIRE response is just that fence, we
                # need to nudge it to actually invoke the tool instead of
                # letting the fenced JSON become the "final answer".
                is_fenced_toolcall = bool(
                    re.search(r'```(?:json)?\s*\{\s*"tool"\s*:', response)
                    and not _parse_tool_call(response)
                )

                if is_hallucinating:
                    if not self.quiet:
                        console.print("\n  [dim]↳ Hallucination detected, prompting for verification...[/dim]")
                    self.conversation.append({"role": "assistant", "content": response})
                    self.conversation.append({"role": "user", "content": "You have NOT checked. Use a tool to verify.\nACTION: {\"tool\": \"bash\", \"args\": {\"command\": \"ls\"}}"})
                    continue
                elif is_narrating or is_broken_tool or is_fenced_toolcall:
                    if stall_count >= MAX_STALLS:
                        # Model is genuinely stuck — treat as final answer instead of looping
                        pass  # Fall through to final answer handler below
                    else:
                        if not self.quiet:
                            console.print("\n  [dim]↳ Narrating without action, prompting for tool use...[/dim]")
                        self.conversation.append({"role": "assistant", "content": response})
                        if is_fenced_toolcall:
                            self.conversation.append({"role": "user", "content": "Your last reply put the tool call inside a ```json``` code fence — that's just documentation. To actually run the tool, emit it as: <tool_call>{\"tool\":\"...\",\"args\":{...}}</tool_call> (no code fences)."})
                        elif is_broken_tool:
                            self.conversation.append({"role": "user", "content": (
                                "Your <tool_call> had invalid JSON. The exact shape required is:\n"
                                "<tool_call>{\"tool\":\"<tool_name>\",\"args\":{\"<arg>\":\"<value>\"}}</tool_call>\n"
                                "Common mistakes to avoid:\n"
                                "- {\"tool_name\", {\"args\":{...}}}  ← wrong, missing \"tool\" key\n"
                                "- {\"tool_name\":{...}}              ← wrong, use \"tool\" + \"args\"\n"
                                "Re-emit the call with the correct shape now."
                            )})
                        else:
                            self.conversation.append({"role": "user", "content": "Don't narrate. Call the appropriate tool now to fulfill the request."})
                        continue

                if stall_count > MAX_STALLS and iteration > 0:
                    console.print(f"\n  [yellow]⚠ Model stalled ({stall_count} non-tool responses). Treating as final answer.[/yellow]")

                # Final answer
                # Strip hallucinated <STATUS: ...> tags. Models sometimes tack
                # "<STATUS: done />" onto a pure-narration reply without
                # actually editing anything, and downstream dispatchers treat
                # the tag as a real shipment signal. We unconditionally strip
                # the tag here — the authoritative "did work" signal is the
                # count of tool_use events + the result event, not model text.
                if response:
                    response = re.sub(
                        r'<\s*/?\s*STATUS\s*[^>]*/?\s*>',
                        '',
                        response,
                        flags=re.IGNORECASE,
                    ).strip()
                # Gemma Harmony: collapse multi-channel output down to just
                # the final-channel content. Drops <|channel|>analysis|
                # commentary<|message|>...blocks entirely; keeps content
                # after <|channel|>final<|message|> and before <|end|>.
                if response and "<|channel|>" in response:
                    finals = re.findall(
                        r'<\|channel\|>\s*final\s*<\|message\|>([\s\S]*?)(?=<\|channel\|>|<\|end\|>|<\|im_end\|>|<\|return\|>|$)',
                        response,
                    )
                    if finals:
                        response = "\n".join(f.strip() for f in finals if f.strip()).strip()
                    else:
                        # No final channel found — strip all channel wrappers
                        # best-effort rather than leave the junk
                        response = re.sub(
                            r'<\|channel\|>[^<]*<\|message\|>|<\|end\|>|<\|im_end\|>|<\|return\|>',
                            '',
                            response,
                        ).strip()
                # Strip hallucinated tool glyphs — weaker models (qwen2.5:14b,
                # deepseek-v2) sometimes narrate "🔧 bash: ... ✓" in their
                # prose as if they'd executed a tool. Those glyphs only have
                # a legitimate meaning when pw-agent's own console.print
                # renders them AFTER real tool execution; stripping from
                # model text stops fake success from leaking downstream.
                if response:
                    response = re.sub(r'^\s*🔧\s*\w+:.*$', '', response, flags=re.MULTILINE)
                    response = re.sub(r'\s*✓\s*(?=\n|$)', '', response)
                    response = response.strip()
                # Integrity check (a): did the model narrate file changes
                # without any write_file/edit_file/str_replace actually
                # firing this turn? Flag it via a warning appended to the
                # response + demote the result subtype so downstream can
                # tell a hallucinated shipment from a real one.
                narration_claims_change = bool(response) and bool(re.search(
                    r'\b(?:wrote|created|implemented|committed|pushed|added (?:a |the |new )|assembled|generated the )\b',
                    response, re.IGNORECASE,
                ))
                hallucinated_shipment = narration_claims_change and not has_written
                if hallucinated_shipment:
                    response = (
                        response
                        + "\n\n⚠ [pw-agent] Model narrated file changes but no write_file/edit_file "
                          "tool call was executed this turn. Treat this reply as narration, not a real shipment."
                    )
                self.conversation.append({"role": "assistant", "content": response})
                # Always emit the structured result event in stream-json/json
                # mode, including while streaming — CallByte needs a single
                # canonical "turn done" marker instead of parsing the model's
                # text for <STATUS: done />. Subtype reflects whether any
                # tool actually ran ("success" if yes, "narration" if the
                # model replied without doing anything, "hallucinated" if
                # the model claimed work it didn't do).
                if self.quiet and self.output_format in ("stream-json", "json"):
                    import json as _json
                    if hallucinated_shipment:
                        subtype = "hallucinated"
                    elif iteration > 0:
                        subtype = "success"
                    else:
                        subtype = "narration"
                    result_obj = {
                        "type": "result",
                        "subtype": subtype,
                        "result": response,
                        "turns": iteration,
                        "has_written": has_written,
                    }
                    print(_json.dumps(result_obj))
                elif not self.stream:
                    if self.quiet:
                        print(response)
                    else:
                        console.print("\n  [dim]──────[/dim]\n")
                        console.print(f"[#afafff]{response}[/#afafff]")
                        console.print()
                # Voice mode — speak the final answer in the background
                if self.voice_mode and response and not self.quiet:
                    try:
                        from voice import speak_text as _speak
                        # Strip markdown for cleaner TTS
                        clean = re.sub(r'```[\s\S]*?```', '', response)
                        clean = re.sub(r'[*_#`]', '', clean).strip()
                        if clean:
                            console.print(f"  [dim]🔊 Speaking...[/dim]")
                            msg = _speak(clean[:2000], self.client)
                            if msg.startswith("Error:") and not self.quiet:
                                console.print(f"  [dim]{msg}[/dim]")
                    except Exception:
                        pass
                self._auto_save()
                return

        console.print(f"\n  [yellow]⚠ Reached {self.max_iterations} iterations. Use /clear and try a more specific request, or pass --max-iterations to raise the cap.[/yellow]")
        self._auto_save()

    def _stream_response(self, messages: list[dict], thinking_msg: str = "Thinking...", context_length: int = 8192) -> str:
        """Consume the stream under a Rich spinner. No scroll region, no
        bottom status bar, no ANSI cursor tricks. Rich owns the spinner,
        we own the content.

        Behavior:
        - Spinner shows `thinking_msg` (or "🧠 Thinking..." if the model
          emits [think] chunks) from the moment the stream starts until
          the last chunk.
        - Content chunks are buffered, not echoed token-by-token (the
          previous scroll-region + Rich hybrid had visual glitches —
          tokens appearing and disappearing, bar vanishing). After the
          stream completes the caller prints the full reply in one
          formatted block.

        Returns the full raw text (incl. think tags) so the caller can
        strip artifacts and decide how to display.
        """
        import signal

        chunks: list[str] = []
        first_token = False
        thinking_shown = False
        thinking_lines: list[str] = []
        current_label = [thinking_msg]

        # Ctrl+C — first press aborts the stream, second exits
        original_handler = signal.getsignal(signal.SIGINT)
        def _interrupt_handler(sig, frame):
            if self.interrupted:
                sys.exit(130)
            self.interrupted = True
        try:
            signal.signal(signal.SIGINT, _interrupt_handler)
        except Exception:
            pass

        try:
            # Quiet mode (--stream in -p): skip Rich Live entirely and echo
            # chunks straight to stdout as they arrive. This is what Claude
            # Code / codex / gemini CLIs do — keeps stdout alive for watchdog
            # timers (e.g. CallByte's 120s idle SIGTERM) and makes piped UIs
            # feel responsive instead of showing one big dump at end of turn.
            if self.quiet and self.output_format in ("text", "stream-json"):
                import json as _json
                # Span filter: strips <tool_call>...</tool_call> and
                # <think>...</think> from the emitted token stream so
                # stream-json consumers don't see raw tag text (we still
                # emit a structured {type:tool_use} event AFTER the stream
                # completes, so the tool call is conveyed once, cleanly).
                # Token-safe: holds back the last few chars when they
                # could be the start of a span tag split across chunks.
                span_state = {"mode": "text", "buffer": ""}
                # <STATUS ...> stripped too — treat as a self-closing span
                # with start "<STATUS" and end ">" so any "<STATUS: done />"
                # or "<STATUS: ongoing>" flavor gets swallowed before it
                # reaches downstream parsers.
                span_tags = [("<tool_call>", "</tool_call>"),
                             ("<think>", "</think>"),
                             ("<STATUS", ">")]
                # Gemma Harmony channel filter — only active for gemma
                # models, strips <|channel|>X<|message|> multi-channel
                # output and emits only the "final" channel content.
                is_gemma_model = "gemma" in (self.client.model or "").lower()
                harmony_state = {"channel": "final", "buffer": ""} if is_gemma_model else None
                # Stall detection — if the model generates no new content for
                # STALL_SECONDS (thinking-only streams are fine, but a full
                # silence usually means it's stuck or about to timeout at 300s).
                # Abort the stream early and let the outer loop retry.
                import time as _t
                STALL_SECONDS = 60
                last_progress_ts = _t.time()
                for chunk in self.client.chat_stream(messages, context_length=context_length, thinking=self.thinking):
                    if self.interrupted:
                        self.client.abort()
                        break
                    if chunk:
                        last_progress_ts = _t.time()
                    elif _t.time() - last_progress_ts > STALL_SECONDS:
                        if not self.quiet:
                            console.print(f"\n  [yellow]⚠ Stream stalled {STALL_SECONDS}s — aborting[/yellow]")
                        try:
                            self.client.abort()
                        except Exception:
                            pass
                        break
                    if chunk.startswith("[think]") and chunk.endswith("[/think]"):
                        think_content = chunk[7:-8]
                        thinking_lines.extend(l for l in think_content.split("\n") if l.strip())
                        continue
                    chunks.append(chunk)
                    emit_text = _filter_spans(chunk, span_state, span_tags)
                    if not emit_text:
                        continue
                    # Gemma Harmony channel filter — drop analysis/commentary,
                    # keep final channel. No-op for non-gemma models.
                    if harmony_state is not None:
                        emit_text = _filter_harmony_channels(emit_text, harmony_state)
                        if not emit_text:
                            continue
                    # Drop hallucinated tool-glyph bursts in the stream: `🔧`
                    # and `✓` ONLY have a legitimate meaning when pw-agent's
                    # own console.print renders them after real tool execution
                    # — never when the model types them in prose. Stripping
                    # them token-by-token stops CallByte UIs from showing
                    # fake "bash ✓" checkmarks mid-stream.
                    emit_text = emit_text.replace("🔧", "").replace("✓", "")
                    if not emit_text:
                        continue
                    try:
                        if self.output_format == "stream-json":
                            # Each text chunk as its own NDJSON event; matches
                            # Claude Code's stream-json schema.
                            sys.stdout.write(_json.dumps({"type": "text", "text": emit_text}) + "\n")
                        else:
                            sys.stdout.write(emit_text)
                        sys.stdout.flush()
                    except Exception:
                        pass
                    if not first_token and emit_text.strip():
                        first_token = True
                # Flush any held-back tail after stream completes. In 'text'
                # mode the buffer is partial-match chars that turned out not
                # to be a tag — emit them. In span mode we're inside an
                # unterminated <tool_call>/<think>, drop silently.
                if span_state["mode"] == "text" and span_state["buffer"]:
                    tail = span_state["buffer"]
                    span_state["buffer"] = ""
                    try:
                        if self.output_format == "stream-json":
                            import json as _json
                            sys.stdout.write(_json.dumps({"type": "text", "text": tail}) + "\n")
                        else:
                            sys.stdout.write(tail)
                        sys.stdout.flush()
                    except Exception:
                        pass
            else:
                # Interactive mode: Rich Live with a Group that stacks the
                # persistent status bar on top of the spinner. Token-by-token
                # echo under Rich had visual glitches (bar vanishing, tokens
                # flickering), so we buffer and print the full reply after.
                def _render(label: str):
                    return Group(Spinner("dots", text=Text(label, style="cyan")), _render_status_bar(self))

                with Live(_render(current_label[0]), console=console,
                          refresh_per_second=10, transient=True) as live:
                    for chunk in self.client.chat_stream(messages, context_length=context_length, thinking=self.thinking):
                        if self.interrupted:
                            self.client.abort()
                            break

                        if chunk.startswith("[think]") and chunk.endswith("[/think]"):
                            think_content = chunk[7:-8]
                            thinking_lines.extend(l for l in think_content.split("\n") if l.strip())
                            if not thinking_shown:
                                current_label[0] = "🧠 Thinking..."
                                try:
                                    live.update(_render(current_label[0]))
                                except Exception:
                                    pass
                                thinking_shown = True
                            continue

                        chunks.append(chunk)
                        if not first_token and chunk.strip():
                            first_token = True
        finally:
            try:
                signal.signal(signal.SIGINT, original_handler)
            except Exception:
                pass

        if thinking_lines:
            self.last_thinking = "\n".join(thinking_lines)
            if not first_token and thinking_shown:
                console.print(f"  [dim]🧠 Thought for {len(thinking_lines)} lines — /thinking to expand[/dim]")

        signal.signal(signal.SIGINT, original_handler)

        full = "".join(chunks).strip()

        # Strip model artifacts (think blocks, stop tokens)
        full = re.sub(r'<think>[\s\S]*?</think>', '', full).strip()
        # Only treat <think>...EOF as a thinking block if a </think> ever
        # appeared in the stream; otherwise a stray <think> token from a
        # non-thinking model would nuke the entire response. When there's
        # no closing tag, just strip the lone opening tag and keep the body.
        if '</think>' in full:
            full = re.sub(r'<think>[\s\S]*$', '', full).strip()
        else:
            full = full.replace('<think>', '').strip()
        full = full.replace('<end_of_turn>', '').replace('<|im_end|>', '').strip()
        # Strip Gemma turn-start markers (see same strip a few hundred lines up).
        full = re.sub(r'<start_of_turn>\s*\w*\s*\n?', '', full).strip()

        if self.interrupted:
            if first_token:
                sys.stdout.write("\n")
                sys.stdout.flush()
            return full or "[Interrupted]"

        # Check if response contains a PARSEABLE tool call — only suppress
        # display if we can actually extract a tool call from it
        is_tool = _parse_tool_call(full) is not None

        if is_tool:
            pass  # Agent loop handles display
        elif first_token and not self.quiet:
            # Content arrived — print the full reply in one formatted block.
            # Interactive path only: quiet/-p mode already streamed tokens
            # (text) or NDJSON events (stream-json) to stdout above, so a
            # second formatted dump here would duplicate the answer.
            if thinking_shown and thinking_lines:
                self.last_thinking = "\n".join(thinking_lines)
                console.print(f"  [dim]🧠 Thought for {len(thinking_lines)} lines — /thinking to expand[/dim]")
            display = full.strip()
            if display:
                console.print()
                console.print("  [dim]──────[/dim]")
                console.print()
                console.print(f"[#afafff]{display}[/#afafff]")
                console.print()
        else:
            # No content tokens ever arrived. Tell the user instead of staying silent.
            if thinking_shown:
                console.print()
                console.print("  [yellow]⚠ Model finished thinking but produced no reply. Try rephrasing or /clear.[/yellow]")
                console.print()
            elif not full and os.environ.get("PW_DEBUG"):
                console.print("  [red][Debug: Empty response from model][/red]")

        return "".join(chunks)

    def _print_status_bar(self):
        """Print a compact status line below output."""
        pass  # Handled by prompt_toolkit bottom_toolbar only

    def _close_prep_live(self):
        """Close the turn-scoped Rich Live (started in run() to keep the
        status bar visible during memory/codebase retrieval). Idempotent —
        safe to call on every turn exit path (normal, interrupt, exception)
        since Rich Live has no public 'is_entered' flag."""
        live = getattr(self, "_prep_live", None)
        if live is None:
            return
        try:
            live.__exit__(None, None, None)
        except Exception:
            pass
        self._prep_live = None
        self._prep_update = None

    def _emit_event(self, event: dict):
        """Emit one NDJSON event for stream-json mode.

        Matches Claude Code's --output-format stream-json schema so consumers
        (e.g. CallByte's Terminal tab parser) can show live tool_use and
        tool_result entries. Gated on quiet + stream-json so interactive
        sessions and plain text -p runs stay untouched. Flushes every line
        to keep watchdog timers happy during long tool-call sequences."""
        if not (self.quiet and self.output_format == "stream-json"):
            return
        try:
            import json as _json
            sys.stdout.write(_json.dumps(event) + "\n")
            sys.stdout.flush()
        except Exception:
            pass

    def _ensure_codebase_indexed_async(self):
        """Kick off auto-index / incremental re-index in a background thread.

        - Empty index → full index walk
        - Stale index (files changed since last_indexed) → incremental re-embed
        - Fresh → no-op

        Runs in a daemon thread so session startup isn't blocked. Skips if
        a reindex is already in flight (called on every write_file/edit_file
        during the turn loop, which would otherwise spawn duplicate threads)."""
        import threading
        if not self.codebase:
            return
        # Skip if a reindex is still running from a previous tool call.
        existing = getattr(self, "_reindex_thread", None)
        if existing is not None and existing.is_alive():
            return
        # Quick short-circuit: fresh index and up-to-date → skip all work
        try:
            if self.codebase.is_indexed and not self.codebase.is_stale():
                return
        except Exception:
            pass

        def _bg():
            try:
                stats = self.codebase.ensure_indexed()
                if stats.get("skipped"):
                    return
                if not self.quiet:
                    if "chunks_added" in stats and stats["chunks_added"]:
                        if stats.get("files_rebuilt"):
                            console.print(f"  [dim]🧭 Refreshed code index: +{stats['chunks_added']} chunks across {stats.get('files_rebuilt','?')} changed files[/dim]")
                        else:
                            console.print(f"  [dim]🧭 Built code index: {stats['chunks_added']} chunks across {stats.get('files_indexed','?')} files[/dim]")
            except Exception:
                pass  # Indexing is best-effort

        t = threading.Thread(target=_bg, daemon=True, name="codebase-index")
        self._reindex_thread = t
        t.start()

    def _auto_save(self):
        """Save session to disk after each turn.

        save_session is cheap (JSON dump). _store_memories is NOT — it makes
        LLM calls for fact extraction + dedup (seconds on a 30B+ model).
        Running it inline blocks the REPL from returning to session.prompt(),
        leaving the status bar invisible during the idle-looking gap. Spawn
        it on a daemon thread so the REPL reappears instantly; the extraction
        completes in the background and writes to the MemoryStore when done.
        """
        try:
            save_session(self.conversation, self.cwd, session_id=self.session_id)
        except Exception:
            pass
        self._store_memories_async()
        if self.fleet:
            try:
                self.fleet.update()
            except Exception:
                pass

    def _store_memories_async(self):
        """Kick off _store_memories in a daemon thread if one isn't already
        running. Ensures the REPL returns to session.prompt() immediately
        after each turn so the bottom status bar is re-rendered without
        waiting for the LLM-based memory extraction."""
        existing = getattr(self, "_memory_thread", None)
        if existing is not None and existing.is_alive():
            return  # Previous turn's extraction still running; skip this one
        import threading
        t = threading.Thread(target=self._store_memories, daemon=True, name="pw-memory-extract")
        self._memory_thread = t
        t.start()

    def _store_memories(self):
        """Distill the session into durable facts and merge them into the store.

        Runs two LLM calls at session end:
          1. extract_durable_memories() — 1 call asking the model to produce
             a JSON list of categorized facts (project-fact / user-pref / gotcha
             / decision). Skips transient debugging, tool output, chitchat.
          2. MemoryStore.dedup_and_store() — per-fact reconciliation: if a new
             fact is semantically close (>=0.85 cosine) to an existing one,
             another LLM call picks keep / replace / merge. Otherwise just ADD.
        """
        if not self.memory or not self.client:
            return
        try:
            from memory import extract_durable_memories
            new_facts = extract_durable_memories(self.conversation, self.client)
            if not new_facts:
                return
            counts = self.memory.dedup_and_store(new_facts, client=self.client)
            if not self.quiet:
                parts = [f"{v} {k}" for k, v in counts.items() if v]
                if parts:
                    console.print(f"  [dim]📚 Memories: {', '.join(parts)} ({self.memory.size} total)[/dim]")
        except KeyboardInterrupt:
            # User hit Ctrl+C mid-save; skip rather than crash the exit path.
            if not self.quiet:
                console.print("  [dim]Memory save skipped (interrupted)[/dim]")
        except Exception:
            pass  # Memory storage is best-effort

    def load_session(self, conversation: list[dict]):
        """Resume a previous session with a structured summary.

        Instead of replaying 100+ raw messages (which get truncated),
        we extract a summary of what was done and inject it as compact context.
        """
        turns = sum(1 for m in conversation if m["role"] == "user")

        # Extract the original task (first user message).
        # If this session was itself the product of a prior resume, the first
        # user message is our own "[RESUMED SESSION — N turns]\n\nOriginal
        # task: <real task>\n\nContinue where you left off…" boilerplate.
        # Recover the real task by stripping the wrapper, so resumes don't
        # nest the prefix deeper each time.
        original_task = ""
        for msg in conversation:
            if msg["role"] == "user":
                original_task = msg["content"]
                break
        if original_task.lstrip().startswith("[RESUMED SESSION"):
            import re as _re_resume
            m = _re_resume.search(
                r'Original task:\s*(.+?)(?=\n\s*(?:Files you |Commands you |Your last |Continue where you left off)|\Z)',
                original_task,
                _re_resume.DOTALL,
            )
            if m:
                original_task = m.group(1).strip()

        # Extract files read/written and key actions
        files_read = []
        files_written = []
        commands = []
        key_responses = []

        for msg in conversation:
            content = msg.get("content", "")
            role = msg.get("role", "")
            if role == "assistant":
                # Extract tool actions
                import re as _re
                if "read_file" in content:
                    path_match = _re.search(r'"path":\s*"([^"]+)"', content)
                    if path_match and path_match.group(1) not in files_read:
                        files_read.append(path_match.group(1))
                elif "write_file" in content:
                    path_match = _re.search(r'"path":\s*"([^"]+)"', content)
                    if path_match and path_match.group(1) not in files_written:
                        files_written.append(path_match.group(1))
                elif "bash" in content:
                    cmd_match = _re.search(r'"command":\s*"([^"]{1,80})', content)
                    if cmd_match:
                        commands.append(cmd_match.group(1))
                # Keep substantive non-tool responses
                elif "<tool_call>" not in content and "ACTION:" not in content and len(content) > 100:
                    key_responses.append(content[:300])

        # Build compact resume context
        summary_parts = [f"Original task: {original_task[:500]}"]
        if files_written:
            summary_parts.append(f"Files you created/modified: {', '.join(files_written[:20])}")
        if files_read:
            summary_parts.append(f"Files you already read: {', '.join(files_read[:20])}")
        if commands:
            summary_parts.append(f"Commands you ran: {'; '.join(commands[:10])}")
        if key_responses:
            summary_parts.append(f"Your last analysis: {key_responses[-1][:300]}")

        summary = "\n".join(summary_parts)

        # Start fresh conversation with summary as context
        self.conversation = [
            {
                "role": "user",
                "content": f"[RESUMED SESSION — {turns} turns from previous conversation]\n\n{summary}\n\nContinue where you left off. Do NOT re-read files you already read. Start executing the next step."
            },
            {
                "role": "assistant",
                "content": "I remember our previous session. Let me continue from where I left off."
            }
        ]

        # Also populate file cache from the session
        for f in files_read:
            self.file_cache[f] = f"{f} (already read in previous session)"
        for f in files_written:
            self.file_cache[f] = f"{f} (created/modified in previous session)"

        console.print(f"  [dim]Resumed session ({turns} turns, {len(files_written)} files written, {len(files_read)} files read)[/dim]")

    def add_file(self, path: str):
        """Add a file's contents to the conversation context."""
        full = os.path.abspath(path)
        if not os.path.exists(full):
            console.print(f"  [red]File not found: {path}[/red]")
            return
        try:
            with open(full, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            # Truncate large files
            if len(content) > 15000:
                content = content[:15000] + f"\n... [truncated, {len(content)} chars total]"
            self.conversation.append({
                "role": "user",
                "content": f"[File added to context: {path}]\n```\n{content}\n```"
            })
            self.files_in_context.append(path)
            console.print(f"  [green]+ {path}[/green] [dim]({len(content)} chars)[/dim]")
        except Exception as e:
            console.print(f"  [red]Error reading {path}: {e}[/red]")

    def reset(self):
        """Clear conversation history and session."""
        self.conversation = []
        self.files_in_context = []
        from config import clear_session
        clear_session(self.cwd, session_id=self.session_id)
        console.print("  [dim]Conversation cleared.[/dim]")
