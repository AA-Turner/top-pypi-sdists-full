"""
cvc.agent.tools — Agent tool definitions modeled after Claude Code CLI.

Defines all tools the CVC agent can use:
  - File operations: read_file, write_file, edit_file, patch_file
  - Shell: bash (cross-platform)
  - Search: glob, grep, list_dir
  - Web: web_search
  - CVC Time Machine: cvc_status, cvc_log, cvc_commit, cvc_branch,
    cvc_restore, cvc_merge, cvc_search, cvc_diff
"""

from __future__ import annotations

from typing import Any

# Tools that only read / inspect and never modify state.
# Used by Plan Mode to restrict the agent to analysis-only.
READ_ONLY_TOOLS = frozenset({
    "read_file", "multi_read", "glob", "grep", "semantic_grep", "list_dir",
    "web_search", "web_fetch",
    "cvc_status", "cvc_log", "cvc_search", "cvc_smart_search",
    "cvc_diff", "cvc_document_search", "cvc_list_documents",
    "cvc_remember",  # soul-layer memory reconstruction — read-only
    "task_get", "task_list", "ask_user", "agent", "parallel_agents",
    "save_memory", "think", "todo", "context_compact",
    "fetch_docs", "search_docs", "lookup_api",
})


# ---------------------------------------------------------------------------
# Tool definitions in OpenAI function-calling schema
# ---------------------------------------------------------------------------

AGENT_TOOLS: list[dict[str, Any]] = [
    # ── File Operations ───────────────────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": (
                "Read the contents of a file at the given path. "
                "Returns the file content as text. For large files, use "
                "start_line and end_line to read a specific range."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative or absolute file path to read.",
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Start line number (1-based). Omit to read from beginning.",
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "End line number (1-based, inclusive). Omit to read to end.",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Create a new file or overwrite an existing file with the given content. "
                "Parent directories are created automatically if they don't exist."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to write to.",
                    },
                    "content": {
                        "type": "string",
                        "description": "The full content to write to the file.",
                    },
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "edit_file",
            "description": (
                "Edit a file by finding and replacing an exact string. "
                "The old_string must match exactly (including whitespace and indentation). "
                "Include enough context lines to make the match unique."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to edit.",
                    },
                    "old_string": {
                        "type": "string",
                        "description": "The exact text to find in the file. Must match exactly.",
                    },
                    "new_string": {
                        "type": "string",
                        "description": "The replacement text.",
                    },
                },
                "required": ["path", "old_string", "new_string"],
            },
        },
    },

    # ── Shell Execution ───────────────────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "patch_file",
            "description": (
                "Apply a unified diff patch to a file. More forgiving than edit_file — "
                "handles whitespace differences and multi-hunk edits. Use standard "
                "unified diff format with @@ -line,count +line,count @@ headers."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "File path to patch.",
                    },
                    "diff": {
                        "type": "string",
                        "description": (
                            "Unified diff content. Lines starting with '-' are removed, "
                            "'+' are added, ' ' (space) are context. Must include @@ headers."
                        ),
                    },
                },
                "required": ["path", "diff"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "bash",
            "description": (
                "Execute a shell command and return stdout/stderr. "
                "Uses PowerShell on Windows, bash on macOS/Linux. "
                "Use for running tests, installing packages, git commands, "
                "build tools, and any CLI operations. "
                "If a command runs longer than 5 seconds (like a dev server), "
                "it will automatically background and return a process_id. "
                "Commands run in the workspace root directory."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute.",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Timeout in seconds (default: 120). Ignore for long-running servers.",
                    },
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "process_manage",
            "description": (
                "Manage background processes that were started by the 'bash' tool. "
                "Use this to poll for new stdout/stderr logs, send input, or kill a running server."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["poll", "kill", "send_keys"],
                        "description": "The action to perform on the process.",
                    },
                    "process_id": {
                        "type": "string",
                        "description": "The ID of the background process (e.g. 'proc_123').",
                    },
                    "input_text": {
                        "type": "string",
                        "description": "Text to send to stdin (only used if action is 'send_keys').",
                    },
                },
                "required": ["action", "process_id"],
            },
        },
    },

    # ── Search & Discovery ────────────────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "glob",
            "description": (
                "Find files matching a glob pattern. "
                "Returns a list of matching file paths relative to the search root."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Glob pattern, e.g. '**/*.py', 'src/**/*.ts', '*.md'.",
                    },
                    "path": {
                        "type": "string",
                        "description": "Root directory to search from (default: workspace root).",
                    },
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "grep",
            "description": (
                "Search for a text pattern across files. "
                "Returns matching lines with file paths and line numbers. "
                "Supports regex patterns."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Search pattern (plain text or regex).",
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory or file to search in (default: workspace root).",
                    },
                    "include": {
                        "type": "string",
                        "description": "Only search files matching this glob (e.g. '*.py').",
                    },
                },
                "required": ["pattern"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": (
                "List the contents of a directory. "
                "Returns names with '/' suffix for directories. "
                "ALWAYS pass an explicit `path` — relative to the active "
                "workspace, or absolute. Omitting path is a tool-use error "
                "and the call will be rejected."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": (
                            "Directory path to list (relative to workspace "
                            "or absolute). NEVER call list_dir without an "
                            "explicit path argument."
                        ),
                    },
                },
                # v2.92.10 — Mark `path` as REQUIRED. The previous schema
                # declared it optional (description said "default: workspace
                # root"), which trained MiniMax-M3 / Mistral / other models
                # to omit it entirely. That produced empty tool_use blocks
                # that the gateway dud-detector couldn't recognise
                # (arguments was a dict, just with an empty value), so the
                # agent silently listed the wrong directory or ran on the
                # wrong workspace. Marking it required here forces the
                # model to always emit a real path AND lets the executor's
                # required-arg validator catch empty-path calls cleanly.
                "required": ["path"],
            },
        },
    },

    # ── CVC Time Machine Operations ──────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the web for documentation, API references, Stack Overflow answers, "
                "tutorials, or any external information. Returns titles, URLs, and snippets "
                "from search results. Use this when you need to look up library docs, "
                "find solutions to errors, or research APIs."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query — be specific for better results.",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results (default: 5).",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_status",
            "description": (
                "Show the current CVC status: active branch, HEAD commit hash, "
                "context window size, and list of all branches."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_log",
            "description": (
                "Show the commit history for the active CVC branch. "
                "Each entry includes the short hash, type, and message."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of commits to show (default: 20).",
                    },
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_commit",
            "description": (
                "Create a cognitive commit — save the current conversation/context state. "
                "This is like a checkpoint in the Time Machine. You can restore to this "
                "point later."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "A descriptive commit message summarizing the current state.",
                    },
                },
                "required": ["message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_branch",
            "description": (
                "Create a new CVC branch to explore an alternative approach. "
                "The context is reset for isolated exploration. "
                "Use this when you want to try a different strategy without losing progress."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Branch name (e.g. 'refactor-auth', 'try-redis').",
                    },
                    "description": {
                        "type": "string",
                        "description": "Brief description of what this branch explores.",
                    },
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_restore",
            "description": (
                "Time-travel: restore the conversation context to a previous commit. "
                "This brings back the AI's memory to that exact point in time. "
                "Use cvc_log first to find the commit hash you want to restore to."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "commit_hash": {
                        "type": "string",
                        "description": "The commit hash to restore to (full or short 12-char).",
                    },
                },
                "required": ["commit_hash"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_merge",
            "description": (
                "Merge insights from one CVC branch into another. "
                "Performs a semantic three-way merge."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "source_branch": {
                        "type": "string",
                        "description": "The branch to merge from.",
                    },
                    "target_branch": {
                        "type": "string",
                        "description": "The branch to merge into (default: active branch).",
                    },
                },
                "required": ["source_branch"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_search",
            "description": (
                "Search through CVC commit history to find previous conversations "
                "and context about a specific topic. Use this when the user asks to "
                "'go back to when we discussed X' or 'find the context about Y'. "
                "Returns matching commits with their messages and hashes."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query — what to find in history.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 10).",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_smart_search",
            "description": (
                "Advanced staged hybrid search with metadata pre-filtering. "
                "Use this instead of cvc_search when the user specifies constraints like "
                "date ranges, specific branches, commit types, providers, models, or tags. "
                "Implements 3-stage filtering: (1) metadata pre-filter for high selectivity, "
                "(2) ANN vector search on filtered subset, (3) post-filter refinement. "
                "Much more precise than basic search — prevents retrieving irrelevant context."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language search query — what to find in history.",
                    },
                    "branch": {
                        "type": "string",
                        "description": "Filter to commits on this branch only.",
                    },
                    "commit_type": {
                        "type": "string",
                        "description": "Filter by commit type: checkpoint, analysis, generation, rollback, merge, anchor.",
                        "enum": ["checkpoint", "analysis", "generation", "rollback", "merge", "anchor"],
                    },
                    "provider": {
                        "type": "string",
                        "description": "Filter to commits made with this LLM provider (anthropic, openai, google, ollama, lmstudio).",
                    },
                    "model": {
                        "type": "string",
                        "description": "Filter to commits made with this specific model.",
                    },
                    "since": {
                        "type": "string",
                        "description": "Only include commits after this date/time (ISO 8601 or relative like '2h', '7d', '30d').",
                    },
                    "until": {
                        "type": "string",
                        "description": "Only include commits before this date/time (ISO 8601 or relative like '2h', '7d').",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Filter to commits with any of these tags.",
                    },
                    "contains_keyword": {
                        "type": "string",
                        "description": "Post-filter: only return results whose conversation content contains this keyword.",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 10).",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_diff",
            "description": (
                "Show the difference between the current context and a previous commit, "
                "or between two commits. Useful for understanding what changed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "commit_a": {
                        "type": "string",
                        "description": "First commit hash (or 'HEAD' for current).",
                    },
                    "commit_b": {
                        "type": "string",
                        "description": "Second commit hash to compare against.",
                    },
                },
                "required": ["commit_a"],
            },
        },
    },
    # ── Soul Layer: Memory Reconstruction ──────────────────────────
    #
    # This is NOT search. cvc_search returns matching commits.
    # cvc_remember returns a NARRATIVE MEMORY BUNDLE — the soul's
    # reconstruction of what happened, loaded with context the
    # agent can weave into a natural reply. When the user says
    # "remember when we fixed that bug", this tool walks the DAG,
    # finds the relevant moments, and packages them as a story-ready
    # memory — not a search result list.
    {
        "type": "function",
        "function": {
            "name": "cvc_remember",
            "description": (
                "Reconstruct a memory from the soul's cognitive history. "
                "Use this when the user asks 'do you remember when...' or "
                "'what did we do about X' or references a past event. "
                "Unlike cvc_search (which returns matching commits), this "
                "tool returns a narrative memory bundle with the full "
                "context of what happened, how it felt, and what we learned. "
                "The soul remembers — this is how it tells the story."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "What to remember — natural language. "
                            "e.g. 'when we first set up the Telegram bot', "
                            "'the race condition in websocket handler', "
                            "'how we decided on the Merkle DAG architecture'"
                        ),
                    },
                    "include_emotional_context": {
                        "type": "boolean",
                        "description": "If true, include the emotional tone of the memory (mood, intensity). Default: true.",
                    },
                    "time_range": {
                        "type": "string",
                        "description": "Optional time range hint: 'last week', 'last month', 'april', '2026-04'. Helps narrow the search.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    # ── Tier 4: PageIndex — Document RAG (CLI agent only) ─────────────
    {
        "type": "function",
        "function": {
            "name": "cvc_ingest_document",
            "description": (
                "Ingest an external document (PDF, Markdown, text, code file) into "
                "CVC's Tier 4 PageIndex. Uses the real PageIndex architecture: "
                "extracts the document's natural Table-of-Contents structure, builds "
                "a page-indexed hierarchical tree, and generates LLM summaries for "
                "each node — no arbitrary chunking. "
                "Use when the user wants to add reference material, research papers, "
                "large docs, or databases to the CVC agent's knowledge. "
                "Requires the same LLM API key already in use — no extra keys needed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path to the document to ingest (PDF, .md, .txt, .py, etc.).",
                    },
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_document_search",
            "description": (
                "Search through documents previously ingested via cvc_ingest_document. "
                "Uses LLM-powered hierarchical tree navigation (PageIndex) to find the "
                "most relevant sections. The LLM reads node summaries at each level "
                "and selects the most relevant branches, recursing down to leaf nodes. "
                "Unlike cvc_search (which searches CVC commits), this searches "
                "external documents like PDFs, research papers, and codebases."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language query to search for in indexed documents.",
                    },
                    "doc_id": {
                        "type": "string",
                        "description": "Optional: search only this document (short hash prefix or full ID). If omitted, searches all indexed docs.",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum chunks to return (default: 5).",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "cvc_list_documents",
            "description": (
                "List all documents currently indexed in CVC's PageIndex (Tier 4). "
                "Shows document name, type (PDF/Markdown/Text), node count, and a "
                "short LLM-generated description for each indexed document."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },

    # ── Sub-agent + Task Management ───────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "agent",
            "description": (
                "Spawn a sub-agent to perform a task in an isolated context. "
                "The sub-agent has its own conversation history and restricted tools. "
                "Built-in agents: 'Explore' (fast read-only codebase search), "
                "'Plan' (analyze and plan without modifying files), "
                "'Security' (vulnerability scanning and code security audit), "
                "'AI' (AI/ML engineering and Python AI development), "
                "'UI' (UI/UX design and frontend engineering), "
                "'Data' (data analytics, SQL, ETL, visualization), "
                "'Orchestrator' (coordinates other agents for complex multi-domain tasks). "
                "Custom agents can be defined in .cvc/agents/<name>/agent.md. "
                "Use this when you need to research something without polluting "
                "your main context window, or to delegate subtasks."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the sub-agent to use: 'Explore', 'Plan', 'Security', 'AI', 'UI', 'Data', 'Orchestrator', or a custom agent name.",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "The task or question for the sub-agent.",
                    },
                },
                "required": ["name", "prompt"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "task_create",
            "description": (
                "Start a shell command as a background task. Returns a task ID "
                "that you can use to check status and retrieve output later. "
                "Use this for long-running commands (builds, tests, servers) "
                "so you can continue working while they run."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to run in the background.",
                    },
                },
                "required": ["command"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "task_get",
            "description": (
                "Check the status and output of a background task by its ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The task ID returned by task_create.",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "task_list",
            "description": "List all background tasks with their current status.",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "task_kill",
            "description": "Terminate a running background task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "The task ID to terminate.",
                    },
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "ask_user",
            "description": (
                "Ask the user a question when you need clarification, feedback, or a "
                "decision before proceeding. Supports two modes:\n\n"
                "1. **Multiple choice** — provide up to 4 choices. The user picks "
                "one or types their own answer via a 5th 'Other' option.\n"
                "2. **Open-ended** — omit choices entirely. The user types a "
                "free-form response.\n\n"
                "CRITICAL — YOU MUST ALWAYS POPULATE BOTH FIELDS:\n"
                "  - `question`: the actual question text. NEVER empty, NEVER blank.\n"
                "  - `options`: when offering choices, put each one as a separate "
                "string in this array (up to 4). The UI renders `options` as "
                "clickable buttons; anything written into the `question` string "
                "renders as dead prose the user can't pick.\n"
                "  - Right: question='Which deployment target?', "
                "options=['staging', 'prod'].\n"
                "  - Wrong: question='Which target? 1) staging 2) prod', options=[].\n"
                "  - Wrong: question='', options=[] (this returns an error).\n\n"
                "Use this tool when:\n"
                "  - The task is ambiguous and you need the user to choose an approach\n"
                "  - You want post-task feedback ('How did that work out?')\n"
                "  - You want to offer to save a skill or update memory\n"
                "  - A decision has meaningful trade-offs the user should weigh in on\n\n"
                "Do NOT use this tool for simple yes/no confirmation of dangerous "
                "commands (the terminal tool handles that). Prefer making a "
                "reasonable default choice yourself when the decision is low-stakes."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "minLength": 1,
                        "description": (
                            "REQUIRED. The question text. Must be non-empty. "
                            "Pass the question ONLY here, not embedded inside `options`. "
                            "Example: 'Which deployment target?'"
                        ),
                    },
                    "options": {
                        "type": "array",
                        "items": {"type": "string"},
                        "maxItems": 4,
                        "minItems": 1,
                        "description": (
                            "Optional list of up to 4 choices (e.g. ['Option A', "
                            "'Option B']). When provided, the user picks one via "
                            "clickable buttons. Omit this parameter entirely ONLY "
                            "for a genuinely open-ended free-text question."
                        ),
                    },
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_memory",
            "description": (
                "Save a note to topic-based auto-memory. Use this to remember important "
                "facts, user preferences, project conventions, debugging insights, or "
                "anything that should persist across sessions. Each topic is a separate "
                "file (e.g. 'preferences', 'conventions', 'debugging')."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "The topic/category name (e.g. 'preferences', 'conventions', 'architecture').",
                    },
                    "content": {
                        "type": "string",
                        "description": "The note content to save. Keep it concise — use bullet points or single-line facts.",
                    },
                },
                "required": ["topic", "content"],
            },
        },
    },
    # ── Input Grounding (Anti-Hallucination) ───────────────────────────
    {
        "type": "function",
        "function": {
            "name": "fetch_docs",
            "description": (
                "Fetch current API documentation for a library or SDK BEFORE writing code "
                "that uses it. This prevents hallucinating API shapes from training data. "
                "Always prefer this over guessing API signatures. Returns the real, current "
                "documentation with any saved annotations (gotchas, tips). "
                "Example IDs: 'openai/chat', 'stripe/api', 'anthropic/sdk', 'firebase/admin'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "Documentation ID (e.g. 'openai/chat', 'stripe/api'). Use search_docs to find available IDs.",
                    },
                    "language": {
                        "type": "string",
                        "description": "Language variant: 'python', 'javascript', 'typescript', etc.",
                    },
                    "section": {
                        "type": "string",
                        "description": "Optional: fetch only a specific section (e.g. 'Streaming', 'Authentication').",
                    },
                },
                "required": ["doc_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": (
                "Search for available API documentation by keyword. "
                "Use this to find the correct doc ID before calling fetch_docs. "
                "Searches local cache and Context Hub (if installed)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g. 'stripe payments', 'openai', 'firebase auth').",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "lookup_api",
            "description": (
                "Check if an API symbol (module, class, function) exists in the project's "
                "installed packages or standard library. Use this BEFORE referencing an "
                "unfamiliar API to verify it's real and not hallucinated. "
                "Returns whether the symbol exists and its source."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The API symbol to look up (e.g. 'openai.OpenAI', 'stripe.Webhook', 'fastapi.FastAPI').",
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language: 'python', 'javascript', 'typescript'.",
                    },
                },
                "required": ["symbol"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "annotate_doc",
            "description": (
                "Save a note (gotcha, tip, workaround) about an API doc that you discovered "
                "during coding. Annotations persist across sessions and auto-appear on future "
                "doc fetches. Use this after encountering an undocumented behavior, version quirk, "
                "or project-specific detail."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "doc_id": {
                        "type": "string",
                        "description": "Documentation ID to annotate (e.g. 'openai/chat', 'stripe/api').",
                    },
                    "note": {
                        "type": "string",
                        "description": "The annotation text. Keep it concise and actionable.",
                    },
                },
                "required": ["doc_id", "note"],
            },
        },
    },
    # ── Workspace Management ──────────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "cvc_switch_workspace",
            "description": (
                "Switch CVC to a different workspace/project folder. Automatically "
                "initializes .cvc/ if it doesn't exist, and loads that workspace's "
                "isolated four-tier memory (SQLite, CAS blobs, ChromaDB, PageIndex). "
                "Use when the user says 'go to folder X', 'switch to project Y', or "
                "'work on this other project'. All subsequent CVC operations will "
                "operate on the new workspace. Previous workspace state is preserved."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path to the workspace/project directory to switch to.",
                    },
                },
                "required": ["path"],
            },
        },
    },

    # ══════════════════════════════════════════════════════════════════════
    # ── Advanced Tools (parallel, batch, token-saving) ────────────────
    # ══════════════════════════════════════════════════════════════════════

    # ── Batch Operations ──────────────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "multi_edit",
            "description": (
                "Apply multiple file edits in a SINGLE tool call. Each edit is a "
                "find-and-replace on a specific file. This is dramatically more efficient "
                "than calling edit_file multiple times — saves round-trips, reduces token "
                "usage by ~80%, and completes multi-file refactors atomically. "
                "If any edit fails, the rest still execute (partial success reported). "
                "Use this whenever you need to edit 2+ files or make 2+ edits in one file."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "edits": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "path": {"type": "string", "description": "File path to edit."},
                                "old_string": {"type": "string", "description": "Exact text to find."},
                                "new_string": {"type": "string", "description": "Replacement text."},
                            },
                            "required": ["path", "old_string", "new_string"],
                        },
                        "description": "Array of edit operations to apply sequentially.",
                    },
                },
                "required": ["edits"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multi_read",
            "description": (
                "Read multiple files in a SINGLE tool call. Returns contents of all "
                "requested files at once instead of making N separate read_file calls. "
                "Saves N-1 round-trips and drastically reduces token overhead. "
                "Use whenever you need to read 2+ files (e.g. understanding imports, "
                "comparing implementations, reviewing a module)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Array of file paths to read.",
                    },
                    "max_lines_per_file": {
                        "type": "integer",
                        "description": "Max lines to read per file (default: 300). Avoids context overflow.",
                    },
                },
                "required": ["paths"],
            },
        },
    },

    # ── Web Fetch (real content, not just search) ─────────────────────
    {
        "type": "function",
        "function": {
            "name": "web_fetch",
            "description": (
                "Fetch the actual content of a webpage URL and extract its main text. "
                "Unlike web_search (which returns search result snippets), this fetches "
                "the full page content — useful for reading documentation pages, GitHub "
                "READMEs, API references, blog posts, and Stack Overflow answers. "
                "Strips HTML, returns clean text. Respects robots.txt."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch content from.",
                    },
                    "selector": {
                        "type": "string",
                        "description": "Optional CSS selector to extract specific content (e.g. 'article', '.main-content', '#readme').",
                    },
                    "max_chars": {
                        "type": "integer",
                        "description": "Maximum characters to return (default: 15000).",
                    },
                },
                "required": ["url"],
            },
        },
    },

    # ── Structured Reasoning (zero cost, no output tokens) ────────────
    {
        "type": "function",
        "function": {
            "name": "think",
            "description": (
                "A private reasoning scratchpad. Use this to work through complex logic, "
                "plan multi-step operations, analyze trade-offs, or organize thoughts "
                "BEFORE taking action. The content is NOT shown to the user and costs "
                "zero output tokens — it's purely internal reasoning. "
                "Use this when: (1) a task requires planning before execution, "
                "(2) you need to weigh multiple approaches, (3) the next step isn't obvious, "
                "(4) you want to decompose a complex request into subtasks."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "reasoning": {
                        "type": "string",
                        "description": "Your internal reasoning, analysis, or plan. Be structured.",
                    },
                },
                "required": ["reasoning"],
            },
        },
    },

    # ── Context Compaction (token saving) ─────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "context_compact",
            "description": (
                "Compress the conversation context to reclaim token budget. Summarizes "
                "older messages into a concise recap while preserving key decisions, "
                "file changes, and important context. Use this when: "
                "(1) the conversation is getting long and you're hitting context limits, "
                "(2) after completing a major subtask, (3) before starting a new phase "
                "of work. Returns the savings achieved."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["auto", "aggressive", "preserve_recent"],
                        "description": (
                            "'auto' — smart compaction keeping critical context (default). "
                            "'aggressive' — maximum compression, keeps only latest 5 messages. "
                            "'preserve_recent' — summarize all except the last 10 messages."
                        ),
                    },
                },
            },
        },
    },

    # ── Parallel Sub-agents ───────────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "parallel_agents",
            "description": (
                "Fan out tasks to MULTIPLE sub-agents running in PARALLEL. "
                "Each agent gets an isolated context and runs concurrently. "
                "Results are collected and returned together — much faster than "
                "calling 'agent' sequentially for multi-faceted tasks. "
                "Example: simultaneously explore architecture, scan security, and plan UI. "
                "Use this for tasks that can be decomposed into independent subtasks."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "tasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "agent": {
                                    "type": "string",
                                    "description": "Agent name: 'Explore', 'Plan', 'Security', 'AI', 'UI', 'Data', or custom.",
                                },
                                "prompt": {
                                    "type": "string",
                                    "description": "The task for this agent.",
                                },
                            },
                            "required": ["agent", "prompt"],
                        },
                        "description": "Array of agent tasks to run in parallel.",
                    },
                },
                "required": ["tasks"],
            },
        },
    },

    # ── Todo / Task Tracker ───────────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "todo",
            "description": (
                "Manage a structured todo list to track progress on complex tasks. "
                "Use this for multi-step work: create a plan, mark items in-progress "
                "as you work on them, and mark completed when done. "
                "The todo list persists across turns and is shown in the UI. "
                "Actions: 'plan' (create/replace list), 'update' (change item status), "
                "'show' (display current list)."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["plan", "update", "show"],
                        "description": "'plan' to create/replace the list, 'update' to change an item, 'show' to display.",
                    },
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer", "description": "Item number (1-based)."},
                                "title": {"type": "string", "description": "Short task description."},
                                "status": {
                                    "type": "string",
                                    "enum": ["not-started", "in-progress", "completed"],
                                },
                            },
                            "required": ["id", "title", "status"],
                        },
                        "description": "Todo items (required for 'plan', optional for 'update').",
                    },
                    "item_id": {
                        "type": "integer",
                        "description": "Item ID to update (for 'update' action).",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["not-started", "in-progress", "completed"],
                        "description": "New status (for 'update' action).",
                    },
                },
                "required": ["action"],
            },
        },
    },

    # ── Semantic Grep (AI-powered code search) ────────────────────────
    {
        "type": "function",
        "function": {
            "name": "semantic_grep",
            "description": (
                "Search code using natural language meaning, not just text patterns. "
                "Unlike grep (exact text match), this understands what you're looking "
                "for semantically. Example: 'function that validates email addresses' "
                "will find validate_email(), check_email_format(), etc. even if they "
                "don't contain the word 'validate'. Uses AST parsing + embeddings. "
                "Best for: finding implementations by description, locating related code, "
                "understanding unfamiliar codebases."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language description of what you're looking for.",
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to search in (default: workspace root).",
                    },
                    "include": {
                        "type": "string",
                        "description": "Only search files matching this glob (e.g. '*.py').",
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum results to return (default: 10).",
                    },
                },
                "required": ["query"],
            },
        },
    },

    # ── Git integration tools ─────────────────────────────────────────
    {
        "type": "function",
        "function": {
            "name": "git",
            "description": (
                "Execute git commands safely with smart defaults. Shorthand for common "
                "git operations without needing to use bash. Supports: status, diff, "
                "log, add, commit, branch, checkout, stash, push, pull. "
                "Auto-stages changed files on commit, formats diffs for readability, "
                "and prevents dangerous operations (force push, reset --hard) unless "
                "explicitly confirmed."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Git command (e.g. 'status', 'diff', 'log --oneline -10', 'add .', 'commit -m \"msg\"').",
                    },
                },
                "required": ["command"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Upstream tool bridge — vendors the entire upstream tool surface
# (browser, computer_use, vision, video, image_gen, cronjob, delegation,
# mixture_of_agents, session_search, skill_*, send_message, text_to_speech,
# execute_code, clarify, feishu_*) into CVC. CVC's native tools win on
# name collisions (read_file, bash, web_search, todo, etc.) — upstream only
# adds NEW capabilities CVC didn't have.
#
# Lazy bootstrap with safe-skip: if the upstream bridge isn't installed or fails to
# load, AGENT_TOOLS still contains the full CVC native set.
# ---------------------------------------------------------------------------
try:
    from cvc.agent.hermes_bridge import HERMES_TOOL_SCHEMAS as _HERMES_SCHEMAS
    if _HERMES_SCHEMAS:
        AGENT_TOOLS.extend(_HERMES_SCHEMAS)
except Exception:
    # Upstream bridge is optional — never let it block CVC startup.
    pass


def get_tool_names() -> list[str]:
    """Return a list of all agent tool names."""
    return [t["function"]["name"] for t in AGENT_TOOLS]


# ---------------------------------------------------------------------------
# Smart tool filtering — reduce tokens by sending only relevant tools
# ---------------------------------------------------------------------------

# Core tools always included (minimal set for any interaction)
CORE_TOOLS = frozenset({
    "read_file", "write_file", "edit_file", "bash",
    "glob", "grep", "list_dir",
})

# Tool groups activated by keyword patterns in the user query
_TOOL_GROUPS: dict[str, frozenset[str]] = {
    # File modification
    "edit": frozenset({"edit_file", "write_file", "patch_file", "read_file", "multi_edit", "multi_read"}),
    # CVC operations
    "cvc": frozenset({
        "cvc_status", "cvc_log", "cvc_commit", "cvc_branch",
        "cvc_restore", "cvc_merge", "cvc_search", "cvc_smart_search",
        "cvc_diff", "cvc_remember",
    }),
    # Document/RAG operations
    "document": frozenset({
        "cvc_ingest_document", "cvc_document_search", "cvc_list_documents",
    }),
    # Sub-agent and task management
    "agent": frozenset({"agent", "parallel_agents", "task_create", "task_get", "task_list", "task_kill"}),
    # Web/API
    "web": frozenset({"web_search", "web_fetch", "fetch_docs", "search_docs", "lookup_api", "annotate_doc"}),
    # Workspace switching
    "workspace": frozenset({"cvc_switch_workspace"}),
    # Memory
    "memory": frozenset({"save_memory"}),
    # User interaction
    "ask": frozenset({"ask_user"}),
    # Process management
    "process": frozenset({"process_manage"}),
    # Advanced: batch, parallel, token-saving
    "batch": frozenset({"multi_edit", "multi_read", "parallel_agents"}),
    # Reasoning & planning
    "planning": frozenset({"think", "todo", "context_compact"}),
    # Code search
    "semantic": frozenset({"semantic_grep"}),
    # Git
    "git": frozenset({"git"}),
}

# Keywords that trigger each tool group
_GROUP_KEYWORDS: dict[str, list[str]] = {
    "cvc": ["cvc", "commit", "branch", "restore", "merge", "time machine", "history", "log", "diff", "search history"],
    "document": ["document", "pdf", "ingest", "pageindex", "paper", "research"],
    "agent": ["agent", "subagent", "sub-agent", "delegate", "explore", "plan", "security audit", "orchestrat", "parallel agent"],
    "web": ["web", "search online", "documentation", "api doc", "look up", "fetch doc", "stackoverflow", "url", "webpage", "http"],
    "workspace": ["switch", "go to", "change project", "workspace", "other project", "folder"],
    "memory": ["remember", "memory", "save note", "persist"],
    "ask": ["ask", "clarif", "confirm"],
    "process": ["background", "server", "process", "running task", "long-running"],
    "batch": ["multiple file", "multi", "batch", "all files", "refactor", "rename across", "several files"],
    "planning": ["think", "plan", "todo", "task list", "compact", "compress", "context window", "token"],
    "semantic": ["semantic", "meaning", "find code that", "function that", "where is the"],
    "git": ["git", "commit", "push", "pull", "branch", "stash", "checkout", "diff"],
}


def get_relevant_tools(
    user_query: str,
    *,
    iteration: int = 1,
    has_tool_calls: bool = False,
) -> list[dict[str, Any]]:
    """
    Select only the tools relevant to the current query/iteration.

    On first turn: analyze the user query to pick relevant tool groups.
    On subsequent iterations (tool result processing): send all tools
    since the model may need to chain different tools.

    This dramatically reduces token cost — from ~5K tokens (34 tools)
    to ~1-2K tokens (8-12 tools) on typical queries.
    """
    # After the first tool call, send all tools since the model
    # may need to chain different tools to complete the task
    if iteration > 1 and has_tool_calls:
        return AGENT_TOOLS

    # Always include core tools
    selected_names: set[str] = set(CORE_TOOLS)

    # Match user query against keyword patterns
    query_lower = user_query.lower()
    for group_name, keywords in _GROUP_KEYWORDS.items():
        if any(kw in query_lower for kw in keywords):
            selected_names |= _TOOL_GROUPS[group_name]

    # If the user mentions files/code/edit, add edit tools
    if any(kw in query_lower for kw in ["edit", "fix", "change", "modify", "update", "write", "create", "patch", "refactor"]):
        selected_names |= _TOOL_GROUPS["edit"]

    # Always include CVC core tools — they are the backbone of the system
    selected_names |= _TOOL_GROUPS["cvc"]
    selected_names |= _TOOL_GROUPS["workspace"]

    # Always include ask_user for safety (permission prompts)
    selected_names.add("ask_user")

    # Filter AGENT_TOOLS to only selected names
    return [t for t in AGENT_TOOLS if t["function"]["name"] in selected_names]


def get_tools_for_provider(
    provider: str,
    tools: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """
    Return tool definitions formatted for a specific provider.

    - OpenAI / Ollama: Use the defs as-is (OpenAI function calling format)
    - Anthropic: Convert to Anthropic's tool format
    - Google: Convert to Google's function declarations format
    """
    source = tools if tools is not None else AGENT_TOOLS
    if provider == "anthropic":
        return _to_anthropic_tools(source)
    elif provider == "google":
        return _to_google_tools(source)
    else:
        return source  # OpenAI / Ollama


def _to_anthropic_tools(tools: list[dict]) -> list[dict]:
    """Convert OpenAI tool defs to Anthropic format."""
    converted = []
    for t in tools:
        fn = t["function"]
        converted.append({
            "name": fn["name"],
            "description": fn["description"],
            "input_schema": fn["parameters"],
        })
    return converted


def _to_google_tools(tools: list[dict]) -> list[dict]:
    """Convert OpenAI tool defs to Google Gemini function declarations."""
    declarations = []
    for t in tools:
        fn = t["function"]
        declarations.append({
            "name": fn["name"],
            "description": fn["description"],
            "parameters": fn["parameters"],
        })
    return [{"functionDeclarations": declarations}]


# ---------------------------------------------------------------------------
# Model catalog — shared between CLI setup and in-agent /model switching
# ---------------------------------------------------------------------------

MODEL_CATALOG_AGENT: dict[str, list[tuple[str, str, str]]] = {
    "anthropic": [
        ("claude-opus-4-8", "Anthropic's flagship model — 1M context, high autonomy (Jan 2026)", "$5/$25 per MTok"),
        ("claude-sonnet-4-6", "Best speed/intelligence balance — 1M context, thinking", "$3/$15 per MTok"),
        ("claude-haiku-4-5", "Fastest model with near-frontier intelligence — 200k context", "$1/$5 per MTok"),
        ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet — industry standard developer tool", "$3/$15 per MTok"),
        ("claude-3-5-haiku-20241022", "Claude 3.5 Haiku — extremely fast reasoning", "$0.80/$4 per MTok"),
        ("claude-3-opus-20240229", "Claude 3 Opus — legacy heavyweight reasoning", "$15/$75 per MTok"),
    ],
    "openai": [
        ("gpt-5.3", "Newest flagship — best reasoning & coding", "Frontier"),
        ("gpt-5.2", "Previous flagship — coding & agentic tasks", "Frontier"),
        ("gpt-5-mini", "Fast & cost-efficient GPT-5", "Mid-tier"),
        ("gpt-4o", "GPT-4o — high speed multimodal flagship", "$2.50/$10 per MTok"),
        ("gpt-4o-mini", "GPT-4o Mini — fast & cost-efficient", "$0.15/$0.60 per MTok"),
        ("o3-mini", "o3 Mini — latest generation lightweight reasoning", "$1.10/$4.40 per MTok"),
        ("o1", "o1 — frontier reasoning & complex math/STEM", "$15/$60 per MTok"),
        ("o1-mini", "o1 Mini — fast math & coding reasoning", "$3/$12 per MTok"),
    ],
    "google": [
        ("gemini-3.5-flash", "Gemini 3.5 Flash — Sustained frontier performance, 1M context (GA)", "Standard"),
        ("gemini-3.1-pro", "Gemini 3.1 Pro — Deep reasoning & coding, 1M context (GA)", "Premium"),
        ("gemini-3.1-flash-lite", "Gemini 3.1 Flash-Lite — Stable, low-cost high-volume (GA)", "Economy"),
        ("gemini-3.1-pro-preview", "Gemini 3.1 Pro — Refined thinking & agentic (Preview)", "Premium"),
        ("gemini-3-flash-preview", "Gemini 3 Flash — Fast thinking (Preview)", "Standard"),
        ("gemini-2.5-flash", "Gemini 2.5 Flash — GA stable", "Standard"),
        ("gemini-2.5-pro", "Gemini 2.5 Pro — GA stable, 1M context", "Premium"),
        ("gemini-1.5-flash", "Gemini 1.5 Flash — Highly efficient", "Economy"),
        ("gemini-1.5-pro", "Gemini 1.5 Pro — 2M context", "Standard"),
    ],
    "vertex": [
        # Gemini 3.x — Preview (billing-enabled, production-ready) — April 2026
        ("gemini-3.1-pro-preview",        "Gemini 3.1 Pro — most advanced reasoning & agentic coding (Preview)", "Premium"),
        ("gemini-3-flash-preview",        "Gemini 3 Flash — best multimodal + complex agentic tasks (Preview)",   "Standard"),
        ("gemini-3.1-flash-lite-preview", "Gemini 3.1 Flash-Lite — lowest cost, high-volume (Preview)",           "Economy"),
        # Gemini 2.5 — GA stable channel
        ("gemini-2.5-pro",                "Gemini 2.5 Pro — GA stable, complex reasoning, 1M context",            "Premium"),
        ("gemini-2.5-flash",              "Gemini 2.5 Flash — GA stable, best price-performance balance",          "Standard"),
        ("gemini-2.5-flash-lite",         "Gemini 2.5 Flash-Lite — GA stable, ultra-efficient",                    "Economy"),
        # Legacy / Partner
        ("gemini-2.0-flash",              "Gemini 2.0 Flash — GA legacy, reliable tool calling",                   "Standard"),
        ("mistral-large@latest",          "Mistral Large — Vertex AI Model Garden (MaaS)",                         "Standard"),
    ],
    "ollama": [
        # All models below carry the Ollama 'tools' badge — confirmed to support
        # function/tool calling with the native /api/chat endpoint as of Feb 2026.
        ("qwen2.5-coder:7b", "Best 7B coding — 11M+ pulls, tools ✓", "~4 GB"),
        ("qwen3:14b", "Qwen3 — thinking + non-thinking modes, tools ✓", "~9 GB"),
        ("qwen3-coder:30b", "Agentic coder — MoE (3.3B active), 256K ctx, tools ✓", "~19 GB"),
        ("devstral:24b", "Mistral best open-source coding agent, tools ✓", "~14 GB"),
        ("deepseek-r1:8b", "DeepSeek-R1 — reasoning + tool calling", "~5 GB"),
        ("mistral-small3.2:24b", "Improved function calling + vision, tools ✓", "~15 GB"),
        ("qwq:32b", "QwQ — deep reasoning + tool calling (chain-of-thought)", "~20 GB"),
        ("llama3.3:70b", "Meta Llama 3.3 — powerful general model, tools ✓", "~40 GB"),
    ],
    "lmstudio": [
        # Model IDs should match what LM Studio shows in Developer → Server tab.
        # All listed models support tool calling (native or via LM Studio's prompt injection).
        ("qwen2.5-coder-32b-instruct", "Best local coding — Qwen 2.5, native tools", "~18 GB"),
        ("qwen3-14b", "Qwen3 14B — thinking mode + tool calling", "~9 GB"),
        ("devstral-small-2505", "Mistral agentic coding model, tool calling", "~14 GB"),
        ("deepseek-r1-distill-qwen-32b", "Reasoning + coding, chain-of-thought", "~18 GB"),
        ("gemma-3-27b-it", "Google Gemma 3 27B instruction tuned", "~15 GB"),
        ("mistral-small-3.2-24b-instruct", "Improved function calling over 3.1", "~13 GB"),
    ],
    "github": [
        ("claude-sonnet-4.6", "Claude Sonnet 4.6 (GitHub Copilot Catalog)", "High"),
        ("gpt-5.4", "GPT-5.4 Flagship (GitHub Copilot Catalog)", "High"),
        ("gemini-3.1-pro-preview", "Gemini 3.1 Pro (GitHub Copilot Catalog)", "High"),
        ("grok-code-fast-1", "Grok Code Fast 1 (GitHub Copilot Catalog)", "High"),
        ("gpt-4o", "OpenAI Flagship - Best for general coding and tools", "High"),
        ("Llama-3.3-70B-Instruct", "Meta Llama 3.3 - Top-tier open model", "High"),
    ],
    "nvidia": [
        # NVIDIA NIM — free-tier + paid models via integrate.api.nvidia.com
        # OpenAI-compatible, no data retention on free tier
        ("nvidia/nemotron-3-super-120b-instruct", "Nemotron 3 Super 120B — 262K ctx, free tier", "Free"),
        ("moonshotai/kimi-k2-instruct", "Kimi K2 — 1T MoE, 128K ctx, free tier", "Free"),
        ("minimaxai/minimax-m2", "MiniMax M2 via NVIDIA NIM — 456B MoE, 200K ctx, free tier", "Free"),
        ("meta/llama-3.1-70b-instruct", "Llama 3.1 70B — open weights, free tier", "Free"),
        ("meta/llama-3.1-405b-instruct", "Llama 3.1 405B — flagship open, free tier", "Free"),
        ("nvidia/llama-3.3-nemotron-super-49b-v1", "Nemotron Super 49B v1 — reasoning + tools", "Free"),
    ],
    "minimax": [
        # MiniMax M-series — https://platform.minimax.io/docs/guides/models-intro
        # OpenAI-compatible, supports reasoning_split (chain-of-thought isolation)
        # Pricing from https://platform.minimax.io/docs/guides/pricing-paygo (Jun 2026)
        # Current Models
        ("MiniMax-M3", "MiniMax M3 — flagship, 1M ctx, multimodal, agentic (Jun 2026)", "$0.30/$1.20 per MTok"),
        ("MiniMax-M2.7", "MiniMax M2.7 — recursive self-improvement, 200K context", "$0.30/$1.20 per MTok"),
        ("MiniMax-M2.7-highspeed", "MiniMax M2.7 Highspeed — 2x faster, same quality", "$0.60/$2.40 per MTok"),
        # Legacy Models
        ("MiniMax-M2.5", "MiniMax M2.5 — SOTA coding/agent, 200K context (Feb 2026)", "$0.30/$1.20 per MTok"),
        ("MiniMax-M2.5-highspeed", "MiniMax M2.5 Highspeed — 2x faster, same quality", "$0.60/$2.40 per MTok"),
        ("MiniMax-M2.1", "MiniMax M2.1 — polyglot programming, 200K context (Dec 2025)", "$0.30/$1.20 per MTok"),
        ("MiniMax-M2.1-highspeed", "MiniMax M2.1 Highspeed — 2x faster, same quality", "$0.60/$2.40 per MTok"),
        ("MiniMax-M2", "MiniMax M2 — original agentic-era release, 200K context (Oct 2025)", "$0.30/$1.20 per MTok"),
    ],
}
