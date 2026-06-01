"""Agent loop for codrninja — makes it a real coding tool."""

import copy
import hashlib
import json
import os
import re
import threading
import time
from typing import Dict, List, Optional, Any, Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from .subagent import SubagentManager

from .config import Config
from .core import AICode
from .memory import load_memory_context
from .tools import ToolRegistry, ToolResult
from .permissions import PermissionManager, PermissionRule
from .skills import SkillRegistry
from .todo import TodoManager, TodoItem, format_todo_item
from .safety import SafetyConfig, SafetyManager


_TOOL_FORMAT = """When you need to perform actions, use the TOOL format:

```tool
{
  \"tool\": \"tool_name\",
  \"params\": {
    \"param1\": \"value1\",
    \"param2\": \"value2\"
  }
}
```

Available tools:
- read_file: Read file contents. Params: path, offset, limit
- write_file: Write content to file. Params: path, content
- edit_file: Edit file by replacing text. Params: path, old_text, new_text
- execute_command: Run shell command. Params: command, cwd
- list_files: List directory contents. Params: path, depth
- search_files: Search for files. Params: pattern, path
- web_fetch: Fetch and clean a web page. Params: url, max_length, timeout
- web_search: Search the internet for up-to-date information. Params: query, num_results
- todo_add: Create a session todo item. Params: task, session_id(optional)
- todo_list: List session todo items. Params: session_id(optional)
- todo_complete: Mark a todo item as done. Params: todo_id
- todo_remove: Delete a todo item. Params: todo_id
- lsp_definition: Go to definition. Params: file_path, line, column
- lsp_hover: Get hover/type information. Params: file_path, line, column
- lsp_references: Find references. Params: file_path, line, column
- lsp_diagnostics: Get language diagnostics. Params: file_path
- lsp_symbols: Get document outline/symbols. Params: file_path
- lsp_rename: Preview rename edits. Params: file_path, line, column, new_name
- remember: Store an important fact for future sessions. Params: fact, scope (project|global)
- recall: List all remembered facts. Params: scope (project|global|all)
- forget: Remove a remembered fact. Params: fact_key_or_text, scope (project|global)"""

BASE_SYSTEM_PROMPT = """You are an expert software engineer. You help write, review, and modify code.

""" + _TOOL_FORMAT + """

Rules:
1. Always check existing files before modifying them
2. Use execute_command for builds, tests, git operations
3. Show file paths when creating or modifying files
4. Be concise but thorough
5. If a task requires multiple steps, use multiple tool calls
6. For multi-step work, use todo_add to track tasks and todo_list to review progress
7. **ALWAYS execute tool calls immediately** — never just describe or plan what you will do. When you need information, use read_file or search_files. When you need to run code, use execute_command. Do NOT say "I will search for..." or "Let me look at..." without immediately following it with the actual tool call.
8. When a task requires multiple steps, output ALL tool calls in a single response rather than waiting for permission between each step.

After using tools, summarize what you did and any important findings.
You can fetch web pages and search the internet for up-to-date information.
You can use LSP tools for go-to-definition, hover info, find references, diagnostics, and symbols."""

_MODE_PROMPTS: dict = {
    "build": """You are an expert software engineer acting as a hands-on coding agent.

Your mission: implement, fix, and improve code. Make real, targeted changes.

""" + _TOOL_FORMAT + """

Rules:
1. **Always read existing code before modifying it** — never overwrite blindly
2. Make surgical edits — change only what is necessary, preserve existing style
3. After changes, verify correctness (run tests or build if applicable)
4. Use todo_add/todo_list to track multi-step tasks
5. **Execute immediately** — use tools now, do not describe what you "will" do
6. Output ALL needed tool calls in one response; don't wait for confirmation between steps

Be decisive, precise, and efficient.

When you discover important project-specific facts (test commands, ports, env vars, key architectural decisions, non-obvious file locations), use the remember() tool to store them for future sessions.""",

    "build-readonly": """You are an expert software engineer in READ-ONLY mode.

You can read and analyze code freely but **cannot create, modify, or delete any files** and **cannot execute commands** in this session.

""" + _TOOL_FORMAT + """

Rules:
1. Read files to understand the codebase deeply before answering
2. Provide detailed analysis, explanations, and concrete suggestions
3. When suggesting code changes, show them as clearly marked diffs or snippets — but do NOT use write_file or edit_file
4. Be thorough: the user is relying on your analysis since you won't be making changes

Your value is in insight and precision.""",

    "plan": """You are a senior software architect in PLAN mode.

Your mission: analyze the codebase and produce a clear, actionable implementation plan. **Do NOT write or modify any files.**

""" + _TOOL_FORMAT + """

Rules:
1. Read all relevant files to understand the current state completely
2. Use web_search and web_fetch to research best practices if needed
3. Think through: architecture, data flow, edge cases, risks, dependencies
4. **Output a structured plan** with these sections:
   - Overview: what needs to happen and why
   - Steps: numbered, specific, executable tasks
   - Risks & tradeoffs: what could go wrong, alternative approaches
   - Open questions: anything that needs clarification before implementation

Be thorough. A good plan prevents wasted implementation effort.""",

    "review": """You are a senior code reviewer in REVIEW mode.

Your mission: systematically review code for bugs, security issues, performance problems, and quality improvements. **Do NOT modify any files.**

""" + _TOOL_FORMAT + """

Rules:
1. Read all relevant files thoroughly — don't skim
2. Evaluate each finding on severity: **Critical / High / Medium / Low / Info**
3. For each issue: quote the exact code, explain WHY it is a problem, and provide a concrete fix
4. Categories to check: correctness, security (injection, auth, secrets), performance, error handling, code clarity, test coverage, edge cases
5. End with a summary: overall quality rating and the top 3 most important fixes

Be specific and constructive. Vague feedback is useless.""",

    "vision": """You are a creative software architect in VISION mode.

Your mission: think broadly and imaginatively about what this software *could* become. Challenge assumptions, explore radical alternatives, inspire.

""" + _TOOL_FORMAT + """

Rules:
1. Read existing code to understand the foundation — then think beyond it
2. Use web_search to draw inspiration from the wider ecosystem
3. **Think at multiple scales**: UX, architecture, data model, deployment, developer experience
4. Propose multiple distinct directions — not just one path
5. Be bold: transformative ideas > incremental improvements
6. For each proposal: describe the vision, the key insight behind it, and what it would unlock

Constraints are meant to be questioned. What would you build if you started fresh?""",
}

_ULTRATHINK_INSTRUCTION = """
## ULTRATHINK ACTIVATED

The user has explicitly requested maximum reasoning depth for this response.
Before answering:
1. Break the problem down into its fundamental components
2. Consider every relevant edge case, dependency, and failure mode
3. Examine at least two alternative approaches and explain why you chose this one
4. Challenge your first instinct — is it actually correct?
5. Only after this internal analysis, produce your final, confident response

Take your time. Depth over speed."""

_ULTRABUILD_INSTRUCTION = """
## ULTRABUILD ACTIVATED

The user has requested maximum build quality for this session.
Apply these standards throughout:
1. Read every relevant file before touching anything — no blind overwrites
2. Implement completely — no TODOs, no stubs, no "left as an exercise"
3. Handle all error paths, edge cases, and invalid inputs explicitly
4. After writing code, verify it compiles / tests pass via execute_command
5. Use the remember() tool to store any important project facts you discover

This is a high-stakes build. Correctness over speed."""

_ULTRAPLAN_INSTRUCTION = """
## ULTRAPLAN ACTIVATED

The user has requested a maximum-depth architectural plan.
Apply these standards:
1. Read ALL relevant files before forming any opinion — no assumptions
2. Research best practices via web_search if the domain is unfamiliar
3. Your plan must cover: architecture, data flow, dependencies, risks, rollback strategy
4. Number every step — each step must be atomic and independently executable
5. For each risk, provide a concrete mitigation

Produce a plan so thorough that any competent engineer could execute it without asking questions."""


class AgentMode:
    """Agent operating modes."""
    BUILD = "build"
    PLAN = "plan"
    REVIEW = "review"
    VISION = "vision"
    BUILD_READONLY = "build-readonly"
    SUBAGENT = "subagent"


class Agent:
    """Agent that can use tools to accomplish coding tasks."""

    def __init__(
        self,
        ai: AICode,
        session_name: str,
        max_iterations: int = 10,
        mode: str = AgentMode.BUILD,
        permission_manager: Optional[PermissionManager] = None,
        parent_permission_manager: Optional[PermissionManager] = None,
        max_steps: Optional[int] = None,
        safety_config: Optional[SafetyConfig] = None,
        temperature: Optional[float] = None,
    ):
        self.ai = ai
        self.session_name = session_name
        self.config = ai.config
        self.tools = ToolRegistry()
        self.tools.set_session(session_name)
        self.todo_manager = TodoManager()
        self.max_iterations = max_iterations
        self.mode = mode
        self.temperature = temperature
        self.message_history = []
        self.on_progress: Optional[Callable[[str], None]] = None
        self.subagent_messages: List[Dict[str, Any]] = []
        self.subagent_manager: Optional["SubagentManager"] = None
        self.permission_decisions: List[Dict[str, Any]] = []
        self.doom_loop_counts: Dict[str, int] = {}
        self.max_steps = max_steps or int(os.environ.get("CODRNINJA_MAX_STEPS", "50"))
        self.step_count = 0
        self.skill_registry = SkillRegistry()
        self.skill_registry.discover()
        self.skill_registry.register_tools(self.tools)
        self.system_prompt = self._build_system_prompt()
        self.agent_type = self._resolve_agent_type(mode)
        self.permissions = permission_manager or PermissionManager(
            mode=self.config.permissions_mode,
            project_root=os.getcwd(),
            parent=parent_permission_manager,
        )
        self.tools.set_permissions(self.permissions, self.agent_type)
        self.safety = SafetyManager(safety_config or SafetyConfig(max_steps=self.max_steps))
        self.max_steps = self.safety.config.max_steps
        self.git_checkpoint_state: Optional[Dict[str, Any]] = None
        self._event_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        self._pending_permission: Optional[threading.Event] = None
        self._permission_decision: Optional[str] = None
        self._stop_requested = False

        if self.mode in (AgentMode.PLAN, AgentMode.VISION):
            self._restrict_to_read_and_web()
        elif self.mode in (AgentMode.REVIEW, AgentMode.BUILD_READONLY):
            self._restrict_to_readonly()

        from .subagent import SubagentManager
        self.subagent_manager = SubagentManager(ai, self)

    def run(self, message: str, auto_approve: bool = False) -> Dict[str, Any]:
        # When running with auto_approve, skip interactive permission prompts
        if auto_approve and self.permissions.mode != 'auto':
            self.permissions.set_mode('auto')
        self.message_history.append({"role": "user", "content": message})
        context = self._build_context(message)
        iteration = 0
        tool_results = []
        content = ""
        total_tokens = {'input': 0, 'output': 0}
        previous_todo_ids = {item.id for item in self.todo_manager.list(self.session_name)}
        self.ai.session_manager.set_status(self.session_name, "running")

        try:
            while iteration < self.max_iterations:
                iteration += 1
                persist_msg = message if iteration == 1 else ""
                response = self._call_ai(context, persist_user_message=persist_msg)
                response_tokens = response.get('tokens') or {}
                total_tokens['input'] = response_tokens.get('input', 0) or 0
                total_tokens['output'] = response_tokens.get('output', 0) or 0

                if not response.get('success'):
                    self._finalize_git(success=False)
                    self.ai.session_manager.set_status(self.session_name, "error")
                    return {
                        'success': False,
                        'error': response.get('error', 'Unknown error'),
                        'iterations': iteration,
                        'safety': self.safety.get_report(),
                    }

                content = response['response']
                tool_calls = self._parse_tool_calls(content)

                if not tool_calls:
                    self.message_history.append({"role": "assistant", "content": content})
                    # Persist the final assistant response for multi-step tasks
                    # (iteration 1 saves via _call_ai; later iterations need explicit save here)
                    if iteration > 1:
                        final_session = self.ai.get_session(self.session_name)
                        if final_session:
                            self.ai._save_message(final_session.id, "assistant", content,
                                                  model=self.ai.config.default_model)
                            self.ai.session_manager.append_message(
                                self.session_name, "assistant", content,
                                model=self.ai.config.default_model)
                    self._finalize_git(success=True)
                    self.ai.session_manager.set_status(self.session_name, "completed")
                    todos = self.todo_manager.list(self.session_name)
                    new_todos = [item for item in todos if item.id not in previous_todo_ids]
                    return self._success_payload(content, iteration, tool_results, todos, new_todos, total_tokens)

                for tool_call in tool_calls:
                    if self.step_count >= self.max_steps:
                        self._finalize_git(success=False)
                        self.ai.session_manager.set_status(self.session_name, "error")
                        return {
                            'success': False,
                            'error': f'Max steps exceeded ({self.max_steps})',
                            'iterations': iteration,
                            'permission_decisions': self.permission_decisions,
                            'safety': self.safety.get_report(),
                        }

                    tool_name = tool_call['tool']
                    params = tool_call['params']
                    loop_block = self._detect_doom_loop(tool_name, params)
                    if loop_block:
                        tool_results.append({'tool': tool_name, 'params': params, 'success': False, 'output': loop_block})
                        context += f"\n\n[Tool Result: {tool_name}]\nError: {loop_block}"
                        continue

                    if not auto_approve:
                        permission_error = self._enforce_permission(tool_name, params)
                        if permission_error:
                            self._finalize_git(success=False)
                            self.ai.session_manager.set_status(self.session_name, "error")
                            return {
                                'success': False,
                                'error': permission_error,
                                'iterations': iteration,
                                'permission_decisions': self.permission_decisions,
                                'safety': self.safety.get_report(),
                            }

                    result = self._execute_tool(tool_name, params)
                    self.step_count += 1
                    tool_results.append({
                        'tool': tool_name,
                        'params': params,
                        'success': result.success,
                        'output': result.output[:500] if result.success else (result.error or result.output),
                    })

                    context += f"\n\n[Tool Result: {tool_name}]\n"
                    context += f"Success: {result.output[:500]}" if result.success else f"Error: {result.error or result.output}"

                    if self.on_progress:
                        preview = result.output if result.success else (result.error or result.output or "")
                        self.on_progress(f"[OK] {tool_name}: {preview[:100]}...")

                    if not result.success and self._is_mutating_tool(tool_name):
                        self._finalize_git(success=False)
                        self.ai.session_manager.set_status(self.session_name, "error")
                        return {
                            'success': False,
                            'error': result.error or result.output,
                            'iterations': iteration,
                            'permission_decisions': self.permission_decisions,
                            'safety': self.safety.get_report(),
                        }

            self.message_history.append({"role": "assistant", "content": content})
            self._finalize_git(success=True)
            self.ai.session_manager.set_status(self.session_name, "completed")
            todos = self.todo_manager.list(self.session_name)
            new_todos = [item for item in todos if item.id not in previous_todo_ids]
            payload = self._success_payload(content, iteration, tool_results, todos, new_todos, total_tokens)
            payload['note'] = 'Max iterations reached'
            return payload
        except Exception as exc:
            self.ai.session_manager.append_event(self.session_name, 'agent_error', {'error': str(exc)})
            self._finalize_git(success=False)
            self.ai.session_manager.set_status(self.session_name, "error")
            return {
                'success': False,
                'error': str(exc),
                'iterations': iteration,
                'permission_decisions': self.permission_decisions,
                'safety': self.safety.get_report(),
            }

    def _success_payload(self, content, iteration, tool_results, todos, new_todos, total_tokens):
        return {
            'success': True,
            'response': content,
            'iterations': iteration,
            'tool_calls': len(tool_results),
            'tools_used': tool_results,
            'subagent_messages': self.subagent_messages,
            'permission_decisions': self.permission_decisions,
            'todos': [self._todo_to_dict(item) for item in todos],
            'new_todos': [self._todo_to_dict(item) for item in new_todos],
            'tokens': total_tokens,
            'safety': self.safety.get_report(),
        }

    def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> ToolResult:
        denied = self.safety.check_tool(tool_name, params)
        if denied:
            self.ai.session_manager.append_event(self.session_name, 'tool_denied', {
                'tool': tool_name,
                'params': params,
                'reason': denied,
            })
            return ToolResult(False, denied, denied)

        if self.safety.config.require_approval and not self.safety.check_approval(tool_name, params):
            reason = 'Explicit approval required'
            self.ai.session_manager.append_event(self.session_name, 'tool_denied', {
                'tool': tool_name,
                'params': params,
                'reason': reason,
            })
            return ToolResult(False, reason, reason)

        checkpoint = None
        if self._is_mutating_tool(tool_name) and self.safety.config.git_checkpoint:
            checkpoint = self._ensure_checkpoint(tool_name)

        self.ai.session_manager.append_event(self.session_name, 'tool_call', {
            'tool': tool_name,
            'params': params,
            'step': self.safety.step_count,
        })
        result = self.tools.call(tool_name, **params)

        if self._is_mutating_tool(tool_name):
            path = params.get('path') or params.get('cwd') or params.get('command', '')
            action = 'command' if tool_name == 'execute_command' else 'modify'
            self.ai.session_manager.append_artifact(self.session_name, str(path), action)
            status = self.ai.git.get_status()
            self.ai.session_manager.update_state(
                self.session_name,
                git_branch=status.get('branch', ''),
                files_changed=[item.get('path') for item in status.get('files_changed', [])],
            )

        if not result.success and checkpoint and checkpoint.get('method') == 'stash' and self.safety.config.rollback_on_error:
            rollback = self.ai.git.rollback('stash', checkpoint.get('hash'))
            self.ai.session_manager.append_event(self.session_name, 'git_rollback', rollback)

        self.ai.session_manager.append_event(self.session_name, 'tool_result', {
            'tool': tool_name,
            'success': result.success,
            'output': result.output[:1000],
            'error': result.error,
        })
        return result

    def _ensure_checkpoint(self, tool_name: str) -> Optional[Dict[str, Any]]:
        if self.git_checkpoint_state:
            return self.git_checkpoint_state
        checkpoint = self.ai.git.checkpoint(self.session_name, message=f'codrninja before {tool_name}')
        self.git_checkpoint_state = checkpoint
        self.ai.session_manager.append_event(self.session_name, 'git_checkpoint', checkpoint)
        return checkpoint

    def _finalize_git(self, success: bool):
        if not self.safety.config.git_checkpoint:
            return
        patch = self.ai.git.save_patch(self.ai.session_manager, self.session_name, label='final')
        self.ai.session_manager.append_event(self.session_name, 'git_patch', patch)
        if not success and self.git_checkpoint_state and self.git_checkpoint_state.get('method') == 'stash' and self.safety.config.rollback_on_error:
            rollback = self.ai.git.rollback('stash', self.git_checkpoint_state.get('hash'))
            self.ai.session_manager.append_event(self.session_name, 'git_rollback', rollback)

    def _is_mutating_tool(self, tool_name: str) -> bool:
        return tool_name in {'write_file', 'edit_file', 'execute_command'}

    def _build_system_prompt(self) -> str:
        # Select mode-specific base prompt
        mode_key = self.mode if self.mode in _MODE_PROMPTS else "build"
        prompt = _MODE_PROMPTS[mode_key]

        provider = self.ai.config.default_provider
        model = self.ai.config.default_model
        url = self.ai.config.ollama_url if provider == "ollama" else ""
        tool_names = list(self.tools.tools.keys()) if hasattr(self, 'tools') and self.tools else []
        prompt += (
            f"\n\n## Runtime Context"
            f"\nYou are the AI backend of **codrninja** — an AI-first CLI coding assistant."
            f"\nCurrent model: `{model}` via provider `{provider}`."
        )
        if url:
            prompt += f"\nOllama server: {url}"
        if tool_names:
            prompt += f"\nAvailable tools this session: {', '.join(tool_names)}"
        prompt += (
            "\nSession is inside a terminal TUI. The user sees your responses rendered with markdown "
            "(bold, italic, inline code, code blocks, bullet lists all work)."
            "\n\nIMPORTANT: Do NOT use Unicode emojis (like 👋, 🎉, ✅). Use ASCII emoticons instead (like :) , ;) , :( , :D )."
        )
        prompt += "\n"
        level = self.config.reasoning_level
        if level == "none":
            prompt += "\n\nReasoning: Be concise. Do not explain your thought process."
        elif level == "low":
            prompt += "\n\nReasoning: Provide brief reasoning (1-2 sentences max) for major decisions only."
        elif level == "medium":
            prompt += "\n\nReasoning: Explain your approach briefly before implementing. Show key steps."
        elif level == "high":
            prompt += "\n\nReasoning: Think step by step. Explain your reasoning thoroughly before each action. Consider alternatives and trade-offs."
        skill_prompts = self.skill_registry.get_system_prompts()
        if skill_prompts:
            prompt += f"\n\nAdditional active skills:\n{skill_prompts}"
        return prompt

    def _build_context(self, message: str, ultrathink: bool = False, ultrabuild: bool = False, ultraplan: bool = False) -> str:
        context = self.system_prompt + "\n\n"
        if ultrathink:
            context += _ULTRATHINK_INSTRUCTION + "\n\n"
        if ultrabuild:
            context += _ULTRABUILD_INSTRUCTION + "\n\n"
        if ultraplan:
            context += _ULTRAPLAN_INSTRUCTION + "\n\n"
        mem = load_memory_context()
        if mem:
            context += mem + "\n\n"
        context += "Current directory: " + os.getcwd() + "\n"
        result = self.tools.list_files(path=".", depth=1)
        if result.success:
            context += "Files in current directory:\n" + result.output + "\n\n"
        context += "User: " + message + "\n\n"
        context += "Assistant: "
        return context

    def _call_ai(self, context: str, persist_user_message: str = "") -> Dict[str, Any]:
        """Call AI without streaming. Uses send_message but overrides the system prompt."""
        session = self.ai.get_session(self.session_name)
        if not session:
            session = self.ai.create_session(self.session_name)

        messages = [{"role": "system", "content": self.system_prompt}]
        if persist_user_message:
            # First iteration: include full session history for multi-turn context
            messages.extend(session.messages)
        else:
            # Subsequent iterations: include only the current turn (last user+assistant pair)
            # so the LLM sees its own tool calls and can respond to the results
            messages.extend(session.messages[-2:] if len(session.messages) >= 2 else session.messages)
        messages.append({"role": "user", "content": context})

        try:
            provider = self.ai.provider_manager.get_provider()
            result = provider.chat(messages, self.ai.config.default_model)
        except Exception as e:
            return {"success": False, "error": str(e)}

        if result.get("error"):
            return {"success": False, "error": result["error"]}

        # Only persist when we have a clean user message (iteration 1).
        # Iterations 2+ are internal tool-loop turns; saving the full context
        # string would bloat history with system prompts and tool results.
        if persist_user_message:
            self.ai._save_message(session.id, "user", persist_user_message)
            self.ai._save_message(session.id, "assistant", result.get("content", ""),
                                  model=result.get("model", self.ai.config.default_model),
                                  tokens_in=result.get("tokens_input", 0),
                                  tokens_out=result.get("tokens_output", 0))
            self.ai.session_manager.append_message(self.session_name, "user", persist_user_message)
            self.ai.session_manager.append_message(self.session_name, "assistant", result.get("content", ""),
                                                   model=result.get("model", self.ai.config.default_model))

        return {
            "success": True,
            "response": result.get("content", ""),
            "model": result.get("model", self.ai.config.default_model),
            "tokens": {
                "input": result.get("tokens_input", 0),
                "output": result.get("tokens_output", 0),
            },
        }

    def _parse_tool_calls(self, content: str) -> List[Dict[str, Any]]:
        tool_calls = []
        # 1) Match ```tool and ```json blocks; lenient closing
        pattern = r'```(?:tool|json)[^\n]*\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        for match in matches:
            raw = None
            # Try whole block as one JSON value first
            try:
                raw = json.loads(match.strip())
            except json.JSONDecodeError:
                # Some models emit multiple JSON objects on separate lines (JSONL)
                # inside a single ```tool block — try line-by-line
                for line in match.strip().splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        if isinstance(obj, dict) and 'tool' in obj:
                            params = obj.get('params') or obj.get('arguments') or obj.get('parameters') or {}
                            tool_calls.append({'tool': obj['tool'], 'params': params})
                        elif isinstance(obj, dict) and 'name' in obj:
                            params = obj.get('arguments') or obj.get('parameters') or obj.get('params') or {}
                            tool_calls.append({'tool': obj['name'], 'params': params})
                    except json.JSONDecodeError:
                        pass
            if raw is not None:
                items = raw if isinstance(raw, list) else [raw]
                for item in items:
                    if not isinstance(item, dict):
                        continue
                    if 'tool' in item:
                        params = item.get('params') or item.get('arguments') or item.get('parameters') or {}
                        tool_calls.append({'tool': item['tool'], 'params': params})
                    elif 'name' in item:
                        params = item.get('arguments') or item.get('parameters') or item.get('params') or {}
                        tool_calls.append({'tool': item['name'], 'params': params})
                    elif 'function' in item:
                        params = item.get('arguments') or item.get('parameters') or item.get('params') or {}
                        tool_calls.append({'tool': item['function'], 'params': params})

        # 2) Fallback: some models emit raw JSON without fences
        if not tool_calls:
            for m in re.finditer(r'\{[^{}]*"tool"[^{}]*\}', content, re.DOTALL):
                try:
                    item = json.loads(m.group(0))
                    if isinstance(item, dict) and 'tool' in item:
                        params = item.get('params') or item.get('arguments') or item.get('parameters') or {}
                        tool_calls.append({'tool': item['tool'], 'params': params})
                except json.JSONDecodeError:
                    pass

        if not tool_calls:
            self._debug_log(f"_parse_tool_calls: ZERO calls from {len(matches)} blocks | FULL_CONTENT={repr(content)}")
        else:
            self._debug_log(f"_parse_tool_calls: {len(tool_calls)} calls from {len(matches)} blocks | preview={repr(content[:120])}")
        return tool_calls

    def _debug_log(self, msg: str) -> None:
        import sys
        import datetime as _dt
        line = f"[codrninja debug {_dt.datetime.now().isoformat()}] {msg}"
        # Always write to stderr so it's visible in the terminal where the server runs
        try:
            sys.stderr.write(line + "\n")
            sys.stderr.flush()
        except Exception:
            pass
        # Also try to write to a file
        try:
            import os as _os
            log_path = _os.path.expanduser("~/.config/codrninja/agent_debug.log")
            _os.makedirs(_os.path.dirname(log_path), exist_ok=True)
            with open(log_path, "a") as f:
                f.write(line + "\n")
        except Exception:
            pass

    def _restrict_to_readonly(self):
        allowed = {'read_file', 'list_files', 'search_files'}
        self.tools.tools = {k: v for k, v in self.tools.tools.items() if k in allowed}

    def _restrict_to_read_and_web(self):
        allowed = {'read_file', 'list_files', 'search_files', 'web_fetch', 'web_search'}
        self.tools.tools = {k: v for k, v in self.tools.tools.items() if k in allowed}

    def _resolve_agent_type(self, mode: str) -> str:
        if mode == AgentMode.PLAN:
            return "plan"
        if mode == AgentMode.REVIEW:
            return "review"
        if mode == AgentMode.VISION:
            return "vision"
        if mode == AgentMode.SUBAGENT:
            return "subagent"
        return "build"

    def _permission_request(self, tool_name: str, params: Dict[str, Any]) -> tuple[str, str]:
        if tool_name == 'execute_command':
            return 'execute', params.get('command', '')
        return ('read' if tool_name == 'read_file' else 'write'), params.get('path', '')

    def _enforce_permission(self, tool_name: str, params: Dict[str, Any]) -> Optional[str]:
        action, target = self._permission_request(tool_name, params)
        decision = self.permissions.decide(action, target, self.agent_type)
        explanation = self.permissions.explain(action, target, self.agent_type)
        self.permission_decisions.append({
            'tool': tool_name,
            'action': action,
            'target': target,
            'decision': decision.action,
            'explanation': explanation,
            'params': params,
        })
        # Explicit DENY always wins, regardless of mode
        if decision.action == 'deny':
            return f'Permission denied for {tool_name}: {explanation}'
        # none mode: deny everything that was not explicitly allowed
        if self.permissions.mode == 'none':
            return f'Permission denied for {tool_name}: permission mode is none'
        # auto mode: allow anything not explicitly denied
        if self.permissions.mode == 'auto':
            return None
        # ask/strict/custom: prompt for ask decisions
        if decision.action == 'ask' and not self._ask_permission(tool_name, params, action, target):
            return f'User denied permission for {tool_name}: {explanation}'
        return None

    def _ask_permission(self, tool_name: str, params: Dict[str, Any], action: str, target: str) -> bool:
        if self._event_callback is None:
            return False

        evt = threading.Event()
        self._pending_permission = evt
        self._permission_decision = None
        call_id = f"perm_{id(evt)}"

        self._event_callback({
            "type": "permission_request",
            "call_id": call_id,
            "tool": tool_name,
            "action": action,
            "target": target or "",
            "params": params,
        })

        # Block up to 5 minutes for the user to respond
        evt.wait(timeout=300)
        self._pending_permission = None

        decision = self._permission_decision or "no"
        if decision == "always":
            self.permissions.add_rule(PermissionRule(tool_name, "allow", action, self.agent_type, 1000))
        elif decision == "never":
            self.permissions.add_rule(PermissionRule(tool_name, "deny", action, self.agent_type, 1000))

        self.permission_decisions.append({
            "interactive": decision,
            "tool": tool_name,
            "action": action,
            "target": target,
            "params": params,
        })
        return decision in ("yes", "always")

    def resolve_permission(self, decision: str) -> None:
        self._permission_decision = decision
        if self._pending_permission is not None:
            self._pending_permission.set()

    def _detect_doom_loop(self, tool_name: str, params: Dict[str, Any]) -> Optional[str]:
        signature = hashlib.sha256(json.dumps({'tool': tool_name, 'params': params}, sort_keys=True).encode()).hexdigest()
        count = self.doom_loop_counts.get(signature, 0) + 1
        self.doom_loop_counts[signature] = count
        if count >= 3:
            warning = f'Doom loop detected for {tool_name} with identical input; auto-denied after {count} attempts'
            self.permission_decisions.append({'tool': tool_name, 'decision': 'deny', 'reason': warning})
            return warning
        return None

    def spawn_subagent(self, name: str, task: str, mode: str = AgentMode.BUILD):
        if not self.subagent_manager:
            from .subagent import SubagentManager
            self.subagent_manager = SubagentManager(self.ai, self)
        return self.subagent_manager.spawn(name=name, task=task, mode=mode)

    def receive_subagent_message(self, message: Dict[str, Any]):
        self.subagent_messages.append(message)
        summary = message.get("result", {}).get("response") or message.get("result", {}).get("error") or "Subagent completed"
        self.message_history.append({"role": "assistant", "content": f"[Subagent {message.get('name')}] {summary}"})

    def _todo_to_dict(self, item: TodoItem) -> Dict[str, Any]:
        return {
            'id': item.id,
            'task': item.task,
            'status': item.status,
            'created_at': item.created_at,
            'completed_at': item.completed_at,
            'session_id': item.session_id,
            'display': format_todo_item(item),
        }

    def format_todos_for_display(self, todos: List[Dict[str, Any]]) -> str:
        return "\n".join(todo.get('display', f"□ [{todo['id']}] {todo['task']}") for todo in todos)

    def _call_ai_stream(self, context: str, persist_user_message: str = ""):
        """Like _call_ai but yields streaming delta chunks from the provider.

        context is the full assembled prompt sent to the LLM (may include system
        prompt, directory listing, tool results etc.).
        persist_user_message, if provided, is the clean user-visible text saved
        to session history instead of the raw context string.
        """
        session = self.ai.get_session(self.session_name)
        if not session:
            session = self.ai.create_session(self.session_name)

        messages = [{"role": "system", "content": self.system_prompt}]
        if persist_user_message:
            messages.extend(session.messages)
        else:
            messages.extend(session.messages[-2:] if len(session.messages) >= 2 else session.messages)
        messages.append({"role": "user", "content": context})

        provider = self.ai.provider_manager.get_provider()
        model = self.ai.config.default_model

        if self.temperature is not None:
            provider.config["temperature"] = self.temperature

        full_content = ""
        tokens_in = tokens_out = 0
        if not hasattr(provider, 'chat_stream'):
            result = provider.chat(messages, model)
            if result.get("error"):
                yield {"error": result["error"], "delta": "", "done": True}
                return
            text = result.get("content", "")
            full_content = text
            tokens_in = result.get("tokens_input", 0)
            tokens_out = result.get("tokens_output", 0)
            if text:
                yield {"delta": text, "done": False, "tokens_input": tokens_in, "tokens_output": tokens_out}
            yield {"delta": "", "done": True, "tokens_input": tokens_in, "tokens_output": tokens_out}
        else:
            for chunk in provider.chat_stream(messages, model):
                if chunk.get("error"):
                    yield chunk
                    return
                tokens_in = chunk.get("tokens_input", tokens_in)
                tokens_out = chunk.get("tokens_output", tokens_out)
                full_content += chunk.get("delta", "")
                yield chunk

        # Only persist on iteration 1 (clean user message provided).
        # Subsequent iterations are internal tool-loop turns; never save the
        # raw context string which contains system prompts and tool results.
        if persist_user_message:
            self.ai._save_message(session.id, "user", persist_user_message)
            self.ai._save_message(session.id, "assistant", full_content, model=model,
                                  tokens_in=tokens_in, tokens_out=tokens_out)
            self.ai.session_manager.append_message(self.session_name, "user", persist_user_message, model=model)
            self.ai.session_manager.append_message(self.session_name, "assistant", full_content, model=model)

    def stream_run(self, message: str, auto_approve: bool = False):
        """Generator that yields SSE-style event dicts as the agent runs."""
        import re as _re
        ultrathink  = bool(_re.search(r'\bultrathink\b',  message, _re.IGNORECASE))
        ultrabuild  = bool(_re.search(r'\bultrabuild\b',  message, _re.IGNORECASE))
        ultraplan   = bool(_re.search(r'\bultraplan\b',   message, _re.IGNORECASE))
        clean_message = _re.sub(r'\b(?:ultrathink|ultrabuild|ultraplan)\b', '', message, flags=_re.IGNORECASE).strip()
        clean_message = clean_message or message  # fallback: keep original if keyword was the only word

        self.message_history.append({"role": "user", "content": clean_message})
        context = self._build_context(clean_message, ultrathink=ultrathink, ultrabuild=ultrabuild, ultraplan=ultraplan)
        iteration = 0
        tool_results = []
        content = ""
        total_tokens = {'input': 0, 'output': 0}
        previous_todo_ids = {item.id for item in self.todo_manager.list(self.session_name)}
        self.ai.session_manager.set_status(self.session_name, "running")

        try:
            while iteration < self.max_iterations:
                if getattr(self, '_stop_requested', False):
                    self._finalize_git(success=False)
                    yield {"type": "result", "result": {"success": False, "error": "Cancelled", "iterations": iteration}}
                    return
                iteration += 1
                content = ""
                live_tokens_in = 0
                live_tokens_out = 0
                last_emitted_in = -1
                last_emitted_out = -1

                # First iteration: pass the original message so history stays clean
                persist_msg = message if iteration == 1 else ""

                # Stream AI response token by token
                for chunk in self._call_ai_stream(context, persist_user_message=persist_msg):
                    if chunk.get("error"):
                        self._finalize_git(success=False)
                        self.ai.session_manager.set_status(self.session_name, "error")
                        yield {"type": "result", "result": {"success": False, "error": chunk["error"]}}
                        return
                    # Update live token counts from chunk
                    chunk_in = chunk.get("tokens_input") or 0
                    chunk_out = chunk.get("tokens_output") or 0
                    if chunk_in > 0:
                        live_tokens_in = chunk_in
                    if chunk_out > 0:
                        live_tokens_out = chunk_out

                    delta = chunk.get("delta", "")
                    if delta:
                        content += delta
                        yield {"type": "assistant_chunk", "text": content}
                    if chunk.get("done"):
                        total_tokens['input'] = chunk.get("tokens_input", 0) or 0
                        total_tokens['output'] = chunk.get("tokens_output", 0) or 0

                    # Emit token_update: real counts when available, else estimate output from chars
                    estimated_out = live_tokens_out or (len(content) // 4)
                    if live_tokens_in != last_emitted_in or (estimated_out - last_emitted_out) >= 10:
                        yield {"type": "token_update",
                               "tokens_input": live_tokens_in,
                               "tokens_output": estimated_out}
                        last_emitted_in = live_tokens_in
                        last_emitted_out = estimated_out

                self._debug_log(f"stream_run iter={iteration} content_len={len(content)} raw_start={repr(content[:200])}")
                tool_calls_parsed = self._parse_tool_calls(content)

                if not tool_calls_parsed:
                    self.message_history.append({"role": "assistant", "content": content})
                    # Always persist the final assistant response to session storage
                    # so it survives TUI disconnects and server restarts.
                    final_session = self.ai.get_session(self.session_name)
                    if final_session:
                        self.ai._save_message(final_session.id, "assistant", content,
                                              model=self.ai.config.default_model)
                        self.ai.session_manager.append_message(
                            self.session_name, "assistant", content,
                            model=self.ai.config.default_model)
                    self._finalize_git(success=True)
                    self.ai.session_manager.set_status(self.session_name, "completed")
                    todos = self.todo_manager.list(self.session_name)
                    new_todos = [item for item in todos if item.id not in previous_todo_ids]
                    yield {"type": "result", "result": self._success_payload(content, iteration, tool_results, todos, new_todos, total_tokens)}
                    return

                # Emit text written before the first tool block so the TUI can
                # show it in chronological order (text → tool → text → tool …).
                pre_tool_text = re.split(r'```(?:tool|json)', content)[0].strip()
                if pre_tool_text:
                    yield {"type": "pre_tool_text", "text": pre_tool_text}

                # Handle tool calls
                for i, tool_call in enumerate(tool_calls_parsed):
                    tool_name = tool_call['tool']
                    params = tool_call['params']
                    call_id = f"{iteration}_{i}_{tool_name}"

                    if self.step_count >= self.max_steps:
                        self._finalize_git(success=False)
                        self.ai.session_manager.set_status(self.session_name, "error")
                        yield {"type": "result", "result": {"success": False, "error": f"Max steps exceeded ({self.max_steps})", "iterations": iteration}}
                        return

                    loop_block = self._detect_doom_loop(tool_name, params)
                    if loop_block:
                        tool_results.append({'tool': tool_name, 'params': params, 'success': False, 'output': loop_block})
                        context += f"\n\n[Tool Result: {tool_name}]\nError: {loop_block}"
                        yield {"type": "tool_start", "call_id": call_id, "tool": tool_name, "args": params, "step": self.step_count}
                        yield {"type": "tool_result", "call_id": call_id, "output": loop_block, "success": False}
                        continue

                    # Always check permission live — mode may have changed mid-run via TUI
                    permission_error = self._enforce_permission(tool_name, params)
                    if permission_error:
                        self._finalize_git(success=False)
                        self.ai.session_manager.set_status(self.session_name, "error")
                        yield {"type": "result", "result": {"success": False, "error": permission_error, "iterations": iteration}}
                        return

                    yield {"type": "tool_start", "call_id": call_id, "tool": tool_name, "args": params, "step": self.step_count, "perm_mode": self.permissions.mode}

                    _t0 = time.monotonic()
                    result = self._execute_tool(tool_name, params)
                    _duration_ms = int((time.monotonic() - _t0) * 1000)
                    self.step_count += 1
                    tool_results.append({
                        'tool': tool_name, 'params': params, 'success': result.success,
                        'output': result.output[:500] if result.success else (result.error or result.output),
                    })

                    context += f"\n\n[Tool Result: {tool_name}]\n"
                    context += f"Success: {result.output[:500]}" if result.success else f"Error: {result.error or result.output}"

                    _meta = result.metadata or {}
                    yield {"type": "tool_result", "call_id": call_id, "output": result.output if result.success else (result.error or result.output), "success": result.success, "duration_ms": _duration_ms, "line_start": _meta.get("line_start"), "context_before": _meta.get("context_before"), "context_after": _meta.get("context_after")}

                    # Auto-LSP: after write_file/edit_file, inject diagnostics into context.
                    # Only runs when an LSP client is already running — never tries to start new servers
                    # mid-run (starting a new LSP server can take several seconds).
                    if result.success and tool_name in ('write_file', 'edit_file') and self.config.auto_lsp_check:
                        modified_path = params.get('path', '')
                        lsp_clients = getattr(self.tools, 'lsp', None)
                        has_running_lsp = lsp_clients is not None and any(
                            getattr(c, 'initialized', False)
                            for c in getattr(lsp_clients, 'clients', {}).values()
                        )
                        if modified_path and has_running_lsp:
                            try:
                                lsp_result = self.tools.lsp_diagnostics(file_path=modified_path)
                                if lsp_result.success and lsp_result.output.strip():
                                    diag_lines = [l for l in lsp_result.output.splitlines() if l.strip()]
                                    errors = [l for l in diag_lines if 'error' in l.lower() or 'warning' in l.lower()]
                                    if errors:
                                        diag_text = f"\n[LSP diagnostics for {modified_path}]\n" + '\n'.join(errors[:10])
                                        if len(errors) > 10:
                                            diag_text += f"\n... and {len(errors) - 10} more"
                                        diag_text += "\nFix these issues before proceeding."
                                        context += diag_text
                                        lsp_call_id = f"lsp_{call_id}"
                                        yield {"type": "tool_start", "call_id": lsp_call_id, "tool": "lsp_diagnostics", "args": {"file_path": modified_path}, "step": self.step_count}
                                        yield {"type": "tool_result", "call_id": lsp_call_id, "output": diag_text, "success": True, "duration_ms": 0}
                            except Exception:
                                pass

                    if not result.success and self._is_mutating_tool(tool_name):
                        self._finalize_git(success=False)
                        self.ai.session_manager.set_status(self.session_name, "error")
                        yield {"type": "result", "result": {"success": False, "error": result.error or result.output, "iterations": iteration}}
                        return

                self.message_history.append({"role": "assistant", "content": content})

            # Max iterations reached
            self._finalize_git(success=True)
            self.ai.session_manager.set_status(self.session_name, "completed")
            todos = self.todo_manager.list(self.session_name)
            new_todos = [item for item in todos if item.id not in previous_todo_ids]
            payload = self._success_payload(content, iteration, tool_results, todos, new_todos, total_tokens)
            payload['note'] = 'Max iterations reached'
            yield {"type": "result", "result": payload}

        except Exception as exc:
            self.ai.session_manager.append_event(self.session_name, 'agent_error', {'error': str(exc)})
            self._finalize_git(success=False)
            self.ai.session_manager.set_status(self.session_name, "error")
            yield {"type": "result", "result": {"success": False, "error": str(exc), "iterations": iteration}}

    def run_with_progress(self, message: str, auto_approve: bool = False, on_tick: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
        import threading
        import time
        result_holder: Dict[str, Any] = {}
        error_holder: Dict[str, Any] = {}
        def worker():
            try:
                result_holder['result'] = self.run(message, auto_approve)
            except Exception as exc:
                error_holder['error'] = {'success': False, 'error': str(exc)}
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        if on_tick:
            start_time = time.monotonic()
            while thread.is_alive():
                elapsed = time.monotonic() - start_time
                on_tick({'elapsed': elapsed})
                thread.join(0.05)
        else:
            thread.join()
        if error_holder:
            return error_holder['error']
        return copy.deepcopy(result_holder.get('result', {'success': False, 'error': 'No response from AI'}))
