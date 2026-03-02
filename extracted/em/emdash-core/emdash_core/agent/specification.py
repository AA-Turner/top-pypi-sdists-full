"""Specification agent for generating detailed feature specs."""

import json
import os
import re
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from .toolkit import AgentToolkit
from .runner import SafeJSONEncoder
from .providers import get_provider
from .providers.factory import DEFAULT_MODEL
from ..templates import load_template_for_agent
from .spec_schema import Spec, SPEC_TEMPLATE
from .events import AgentEventEmitter, EventType, NullEmitter


# Tool schema for asking clarification questions (OpenAI function calling format)
ASK_CLARIFICATION_TOOL = {
    "type": "function",
    "function": {
        "name": "ask_clarification",
        "description": "Ask the user a clarification question when you need more information to write the spec. Use this instead of outputting JSON questions.",
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to ask the user",
                },
                "context": {
                    "type": "string",
                    "description": "Brief context explaining why you're asking",
                },
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional suggested answers to help the user",
                },
            },
            "required": ["question"],
        },
    },
}


SUBMIT_SPEC_TOOL = {
    "type": "function",
    "function": {
        "name": "submit_spec",
        "description": "Submit the final specification in markdown format.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Feature name/title",
                },
                "content": {
                    "type": "string",
                    "description": "Markdown content of the spec including problem, solution, implementation steps, related files, edge cases, etc.",
                },
            },
            "required": ["title", "content"],
        },
    },
}


class SpecificationAgent:
    """Agent that generates detailed feature specifications."""

    MAX_TOOL_RESULT_SIZE = 8000
    MAX_CLARIFICATION_ROUNDS = 10

    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        verbose: bool = True,
        max_iterations: int = 30,
        project_md_path: Optional[str] = None,
        show_tool_results: bool = False,
        emitter: Optional[AgentEventEmitter] = None,
        interactive: bool = True,
    ):
        """Initialize the specification agent.

        Args:
            model: LLM model to use (e.g., "minimax", "gpt-4o-mini")
            verbose: Whether to print progress
            max_iterations: Maximum tool call iterations
            project_md_path: Path to PROJECT.md file
            show_tool_results: Whether to print full tool results (--verbose)
            emitter: Event emitter for unified message stream
            interactive: Whether to allow interactive prompts (False for JSON mode)
        """
        self.provider = get_provider(model)
        self.toolkit = AgentToolkit(enable_session=True)
        self.model = model
        self.verbose = verbose
        self.show_tool_results = show_tool_results
        self.max_iterations = max_iterations
        self.context_limit = self.provider.get_context_limit()
        self.console = Console()
        self.messages: list[dict] = []
        self.emitter = emitter or NullEmitter(agent_name="SpecificationAgent")
        self.interactive = interactive
        self.project_context = self._load_project_md(project_md_path)

    def _load_project_md(self, path: Optional[str] = None) -> str:
        """Load PROJECT.md if it exists."""
        search_paths = [
            path,
            "PROJECT.md",
            "./PROJECT.md",
            "../PROJECT.md",
        ]

        for p in search_paths:
            if p and os.path.exists(p):
                with open(p, "r") as f:
                    content = f.read()
                if self.verbose:
                    self.console.print(f"[dim]Loaded project context from {p}[/dim]")
                return content

        return ""

    def generate_spec(self, feature_description: str) -> Spec:
        """Generate a specification for a feature.

        Args:
            feature_description: Description of the feature to spec

        Returns:
            The generated specification
        """
        # Emit session start
        self.emitter.emit(EventType.SESSION_START, {
            "agent_name": "Specification Agent",
            "model": self.model,
            "feature": feature_description,
        })

        if self.verbose:
            self.console.print(
                Panel(
                    f"[cyan]Generating specification for:[/cyan]\n{feature_description}",
                    title="[bold]Specification Agent[/bold]",
                    border_style="cyan",
                )
            )

        # Build initial context
        spec_template = load_template_for_agent("spec")
        system_content = f"""{spec_template}

## Spec Format
Write your spec as free-form markdown. Include:

{SPEC_TEMPLATE}
"""
        if self.project_context:
            system_content = f"""## PROJECT.md - READ THIS FIRST

This is the project's constitution. Use this vocabulary and these concepts in your spec.

{self.project_context}

---

{system_content}"""
        else:
            if self.verbose:
                self.console.print("[yellow]Warning: No PROJECT.md found. Spec may not use project-native terminology.[/yellow]")

        self.messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Create a specification for this feature:\n\n{feature_description}\n\nMANDATORY SEQUENCE:\n1. Call plan_exploration with the feature goal and use_case=\"spec\"\n2. Follow the recommended tools in order - do NOT skip steps\n3. Use ask_clarification if you need to ask me any questions\n4. Submit the final spec using submit_spec with title and markdown content"},
        ]

        # Add ask_clarification tool to the toolkit tools
        # Filter out write tools - spec agent should only explore, not modify files
        WRITE_TOOLS = {'write_to_file', 'apply_diff', 'delete_file', 'execute_command'}
        read_only_schemas = [
            schema for schema in self.toolkit.get_all_schemas()
            if schema.get('function', {}).get('name') not in WRITE_TOOLS
        ]
        tools = read_only_schemas + [ASK_CLARIFICATION_TOOL, SUBMIT_SPEC_TOOL]
        clarification_rounds = 0

        # Main loop: explore, clarify, generate
        iterations = 0
        while iterations < self.max_iterations:
            iterations += 1

            response = self.provider.chat(self.messages, tools=tools)
            self.messages.append(self.provider.format_assistant_message(response))

            if response.tool_calls:
                # Execute tool calls
                for tool_call in response.tool_calls:
                    # Handle ask_clarification specially
                    if tool_call.name == "ask_clarification":
                        clarification_rounds += 1
                        if clarification_rounds > self.MAX_CLARIFICATION_ROUNDS:
                            result = {"answer": "No more questions needed. Please generate the specification with the information you have."}
                        else:
                            result = self._handle_clarification_tool(tool_call)
                        result_json = json.dumps(result, cls=SafeJSONEncoder)
                        self.messages.append(
                            self.provider.format_tool_result(tool_call.id, result_json)
                        )
                    elif tool_call.name == "submit_spec":
                        try:
                            args = json.loads(tool_call.arguments)
                        except json.JSONDecodeError:
                            args = {}

                        title = args.get("title", "Untitled Spec")
                        content = args.get("content", "")

                        if not content:
                            error_result = {"success": False, "error": "Content is required"}
                            result_json = json.dumps(error_result, cls=SafeJSONEncoder)
                            self.messages.append(
                                self.provider.format_tool_result(tool_call.id, result_json)
                            )
                            continue

                        spec = Spec(title=title, content=content)
                        success_result = {"success": True}
                        result_json = json.dumps(success_result, cls=SafeJSONEncoder)
                        self.messages.append(
                            self.provider.format_tool_result(tool_call.id, result_json)
                        )
                        self.emitter.emit_response(spec.to_markdown())
                        self.emitter.emit(EventType.SESSION_END, {"success": True})
                        return spec
                    else:
                        result = self._execute_tool_call(tool_call)
                        result_json = json.dumps(result, cls=SafeJSONEncoder)
                        self.messages.append(
                            self.provider.format_tool_result(tool_call.id, result_json)
                        )
            else:
                # Check if response was truncated due to max_tokens
                if response.stop_reason == "max_tokens":
                    if self.verbose:
                        self.console.print("[yellow]Response truncated (max_tokens). Requesting continuation...[/yellow]")
                    self.messages.append({
                        "role": "user",
                        "content": "Your response was cut off. Please continue generating the specification.",
                    })
                    continue

                content = (response.content or "").strip()
                if content:
                    # Try to parse as markdown spec
                    spec = Spec.from_markdown(content)
                    if spec.content:
                        self.emitter.emit_response(spec.to_markdown())
                        self.emitter.emit(EventType.SESSION_END, {"success": True})
                        return spec

                # Response doesn't match required format
                self.messages.append({
                    "role": "user",
                    "content": "Please submit the spec using submit_spec with a title and markdown content.",
                })
                continue

        # Max iterations - generate what we have
        if self.verbose:
            self.console.print("[yellow]Max iterations reached, generating specification...[/yellow]")

        self.messages.append({
            "role": "user",
            "content": "Generate the specification NOW. Submit it using submit_spec with title and content.",
        })

        response = self.provider.chat(self.messages, tools=[SUBMIT_SPEC_TOOL])
        if response.tool_calls:
            for tool_call in response.tool_calls:
                if tool_call.name == "submit_spec":
                    try:
                        args = json.loads(tool_call.arguments)
                        title = args.get("title", "Untitled Spec")
                        content = args.get("content", "")
                        spec = Spec(title=title, content=content)
                        success_result = {"success": True}
                        result_json = json.dumps(success_result, cls=SafeJSONEncoder)
                        self.messages.append(
                            self.provider.format_tool_result(tool_call.id, result_json)
                        )
                        self.emitter.emit_response(spec.to_markdown())
                        self.emitter.emit(EventType.SESSION_END, {"success": True})
                        return spec
                    except Exception:
                        error_result = {"success": False, "error": "Invalid spec."}
                        result_json = json.dumps(error_result, cls=SafeJSONEncoder)
                        self.messages.append(
                            self.provider.format_tool_result(tool_call.id, result_json)
                        )
                        break

        raise ValueError("Failed to generate a valid specification.")

    def _handle_clarification_tool(self, tool_call) -> dict:
        """Handle the ask_clarification tool call by prompting the user."""
        try:
            args = json.loads(tool_call.arguments)
        except json.JSONDecodeError:
            args = {}

        question = args.get("question", "What would you like to clarify?")
        context = args.get("context", "")
        options = args.get("options", [])

        # Emit clarification event
        self.emitter.emit_clarification(question, context, options)

        # In non-interactive mode, auto-select first option or provide default
        if not self.interactive:
            if options:
                answer = options[0]  # Use first suggested option
            else:
                answer = "Please proceed with your best judgment based on the codebase analysis."

            # Emit clarification response
            self.emitter.emit(EventType.CLARIFICATION_RESPONSE, {"answer": answer, "auto": True})

            return {
                "answer": answer,
                "note": "Auto-selected in non-interactive mode",
                "instruction": "Now submit the specification using submit_spec.",
            }

        # Display the question nicely (interactive mode)
        self.console.print()
        self.console.print(Panel(
            f"[bold]{question}[/bold]" +
            (f"\n\n[dim]{context}[/dim]" if context else ""),
            title="[yellow]Clarification Needed[/yellow]",
            border_style="yellow",
        ))

        # Show options if available
        if options:
            self.console.print("[dim]Suggested options:[/dim]")
            for i, opt in enumerate(options, 1):
                self.console.print(f"  [cyan]{i}.[/cyan] {opt}")
            self.console.print()

        # Get answer from user
        answer = Prompt.ask("[bold green]Your answer[/bold green]")

        # Emit clarification response
        self.emitter.emit(EventType.CLARIFICATION_RESPONSE, {"answer": answer})

        return {
            "answer": answer,
            "instruction": "Now submit the specification using submit_spec.",
        }

    def _truncate_data(self, data: dict) -> dict:
        """Truncate data to fit within size limits."""
        serialized = json.dumps(data, cls=SafeJSONEncoder)
        if len(serialized) <= self.MAX_TOOL_RESULT_SIZE:
            return data

        truncated = {}
        for key, value in data.items():
            if isinstance(value, list) and len(value) > 10:
                truncated[key] = value[:10]
                truncated[f"{key}_truncated"] = True
                truncated[f"{key}_total"] = len(value)
            elif isinstance(value, dict):
                truncated[key] = self._truncate_data(value)
            else:
                truncated[key] = value

        return truncated

    def _execute_tool_call(self, tool_call) -> dict:
        """Execute a tool call and return the result."""
        name = tool_call.name
        try:
            args = json.loads(tool_call.arguments)
        except json.JSONDecodeError:
            args = {}

        # Emit tool start event
        self.emitter.emit_tool_start(name, args)

        result = self.toolkit.execute(name, **args)

        # Build summary for the event
        summary = None
        if result.success and result.data and isinstance(result.data, dict):
            if "results" in result.data:
                summary = f"{len(result.data['results'])} results"
            elif "summary" in result.data:
                s = result.data["summary"]
                if isinstance(s, dict):
                    summary = f"{s.get('function_count', 0)} functions, {s.get('class_count', 0)} classes"
        elif not result.success:
            summary = result.error

        # Emit tool result event
        self.emitter.emit_tool_result(
            name=name,
            success=result.success,
            summary=summary,
            data=result.data if self.show_tool_results else None,
        )

        if self.verbose:
            self._print_tool_call(name, args, result)

        if result.success:
            data = self._truncate_data(result.data)
            return {
                "success": True,
                "data": data,
                "suggestions": result.suggestions,
            }
        else:
            return {
                "success": False,
                "error": result.error,
                "suggestions": result.suggestions,
            }

    def _print_tool_call(self, name: str, args: dict, result):
        """Print concise tool call info."""
        status = "[green]✓[/green]" if result.success else "[red]✗[/red]"

        args_str = ""
        if args:
            key_args = []
            for k, v in list(args.items())[:2]:
                if isinstance(v, str) and len(v) > 30:
                    v = v[:30] + "..."
                key_args.append(f"{k}={v}")
            args_str = f" ({', '.join(key_args)})"

        result_str = ""
        if result.success and result.data and isinstance(result.data, dict):
            if "results" in result.data:
                result_str = f" → {len(result.data['results'])} results"
            elif "summary" in result.data:
                s = result.data["summary"]
                if isinstance(s, dict):
                    result_str = f" → {s.get('function_count', 0)} functions, {s.get('class_count', 0)} classes"

        self.console.print(f"  {status} [cyan]{name}[/cyan]{args_str}{result_str}")

        # Print full results if --verbose flag is set
        if self.show_tool_results and result.success and result.data:
            self.console.print()
            self.console.print(f"  [dim]─── {name} result ───[/dim]")
            result_json = json.dumps(result.data, indent=2, default=str)
            # Truncate very long results
            if len(result_json) > 3000:
                result_json = result_json[:3000] + "\n... (truncated)"
            self.console.print(f"  [dim]{result_json}[/dim]")
            self.console.print()


def slugify(text: str) -> str:
    """Convert text to a slug for directory names."""
    # Lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug[:50]  # Limit length
