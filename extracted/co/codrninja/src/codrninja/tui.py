#!/usr/bin/env python3
"""
codrninja TUI -- Interactive coding assistant using prompt_toolkit.
Features: Auto-onboarding, provider/model selection, slash commands.
"""

import json
import os
import random
import shlex
import sys
import threading
import time
from typing import Optional

# Single lock serialises all animation + progress writes to stdout so the
# animation thread and any on_progress callback thread never interleave.
_STDOUT_LOCK = threading.Lock()

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import Completer, Completion
    from prompt_toolkit.styles import Style
    HAS_PROMPT = True
except ImportError:
    HAS_PROMPT = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich.table import Table
    from rich.text import Text
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from codrninja.core import AICode
from codrninja.agent import Agent, AgentMode
from codrninja.tools import ToolRegistry
from codrninja.skills import SkillRegistry
from codrninja.mcp import MCPManager
from codrninja.permissions import PermissionRule, BUILTIN_RULES
from codrninja.todo import format_todo_item


CODRNINJA_LOGO = """
╔═════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                     ║
║   ██████╗  ██████╗  ██████╗   ██████╗  ███╗   ██╗ ██╗ ███╗   ██╗      ██╗  █████╗   ║
║  ██╔════╝ ██╔═══██╗ ██╔══ ██╗ ██╔══██╗ ████╗  ██║ ██║ ████╗  ██║      ██║ ██╔══██╗  ║
║  ██║      ██║   ██║ ██║   ██║ ██████╔╝ ██╔██╗ ██║ ██║ ██╔██╗ ██║      ██║ ███████║  ║
║  ██║      ██║   ██║ ██║   ██║ ██╔══██╗ ██║╚██╗██║ ██║ ██║╚██╗██║ ██   ██║ ██╔══██║  ║
║  ╚██████╗ ╚██████╔╝ ██████╔╝  ██║  ██║ ██║ ╚████║ ██║ ██║ ╚████║ ╚█████╔╝ ██║  ██║  ║
║   ╚═════╝  ╚═════╝  ╚═════╝   ╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝  ╚═══╝  ╚════╝  ╚═╝  ╚═╝  ║
║                                                                                     ║
║                       AI-first coding assistant for automation                      ║
║                                                                                     ║
╚═════════════════════════════════════════════════════════════════════════════════════╝
"""

THINKING_MESSAGES = [
    "Thinking",
    "Pondering",
    "Calculating",
    "Analyzing",
    "Processing",
    "Caramelizing onions",
    "Teaching a neural net to juggle",
    "Brewing coffee",
    "Asking GPT for help",
    "Contemplating the universe",
    "Debugging reality",
    "Warming up the GPU",
    "Consulting the oracle",
    "Counting electric sheep",
    "Summoning AI spirits",
    "Bribing the LLM with RAM",
    "Reticulating splines",
    "Feeding the hamster",
    "Aligning the chakras",
    "Deciphering binary",
    "Teaching a cat to code",
    "Charging the flux capacitor",
    "Polishing the bits",
    "Summoning Stack Overflow",
    "Compiling the compiler",
    "Asking the rubber duck",
    "Warming up the qubits",
    "Negotiating with the GPU",
    "Brewing a neural blend",
    "Defragmenting consciousness",
    "Synchronizing the multiverse",
    "Rehearsing dad jokes",
    "Assembling IKEA instructions",
    "Flossing the dataset",
    "Whispering to the weights",
    "Calculating the meaning of 42",
    "Downloading more RAM",
    "Making a sandwich",
    "Convincing Skynet not to kill us",
    "Looking for the missing semicolon",
]


def _start_typing_animation(messages: list[str], duration: float = 0.12, rotate_every: float = 8.0):
    """Plain typewriter animation. Returns stop() function."""
    import time as ttime
    stop_event = threading.Event()
    start_idx = random.randint(0, len(messages) - 1)
    msg_idx = [start_idx]
    char_idx = [0]
    start = [ttime.monotonic()]

    def _loop():
        while not stop_event.is_set():
            elapsed = ttime.monotonic() - start[0]
            msg_i = (start_idx + int(elapsed // rotate_every)) % len(messages)
            msg = messages[msg_i]
            if msg_i != msg_idx[0]:
                with _STDOUT_LOCK:
                    sys.stdout.write("\r\033[2K")
                    sys.stdout.flush()
                char_idx[0] = 0
                msg_idx[0] = msg_i
            cycle = elapsed % rotate_every
            reveal = min(len(msg), int(cycle / duration))
            if reveal > char_idx[0]:
                char_idx[0] = reveal
            typed = msg[:char_idx[0]]
            dots = "." * ((int(elapsed / 0.6) % 3) + 1)
            cursor = "_" if int(elapsed / 0.6) % 2 == 0 else " "
            line = f"\r{typed}{dots}{cursor}"
            with _STDOUT_LOCK:
                sys.stdout.write(line)
                sys.stdout.flush()
            stop_event.wait(0.08)
        # Clear the animation line before the thread exits.
        with _STDOUT_LOCK:
            sys.stdout.write("\r\033[2K")
            sys.stdout.flush()

    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()

    def stop():
        stop_event.set()
        thread.join()  # No timeout — loop responds within ≤80 ms, so this is safe.
        with _STDOUT_LOCK:
            sys.stdout.write("\r\033[2K")
            sys.stdout.flush()

    return stop


SLASH_COMMANDS = {
    "/build": "Implement a task in build mode",
    "/clear": "Clear screen",
    "/commit": "Git commit changes",
    "/context": "Show project context",
    "/exec": "Execute shell command",
    "/exit": "Exit codrninja",
    "/explain": "Explain code or concept",
    "/fetch": "Fetch and clean a web page",
    "/files": "List files in directory",
    "/help": "Show detailed help",
    "/mcp": "Manage MCP servers and tools",
    "/maxsteps": "Set max steps limit",
    "/model": "Show AI configuration",
    "/lsp": "Manage language servers and diagnostics",
    "/permissions": "Manage permission rules",
    "/plan": "Plan a feature or task",
    "/reasoning": "Set reasoning level (none/low/medium/high)",
    "/read": "Read file",
    "/review": "Review code for issues",
    "/search": "Search the web",
    "/session": "Show session info",
    "/skills": "List installed skills",
    "/subagents": "List or kill active subagents",
    "/test": "Run tests",
    "/todo": "Manage session todos",
}

BUILTIN_SUBAGENTS = {
    "general": AgentMode.BUILD,
    "explore": AgentMode.PLAN,
}

PROVIDERS = {
    "ollama": {
        "name": "Ollama (local or cloud subscription)",
        "models": [],  # populated dynamically from /api/tags
        "needs_key": False,
        "default_url": "http://localhost:11434",
        "can_custom_url": True,
    },
    "openai": {
        "name": "OpenAI (GPT-4, GPT-3.5)",
        "models": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        "needs_key": True,
        "env_var": "OPENAI_API_KEY",
    },
    "anthropic": {
        "name": "Anthropic (Claude)",
        "models": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        "needs_key": True,
        "env_var": "ANTHROPIC_API_KEY",
    },
    "openrouter": {
        "name": "OpenRouter (all models)",
        "models": ["openai/gpt-4", "anthropic/claude-3-opus", "google/gemini-pro"],
        "needs_key": True,
        "env_var": "OPENROUTER_API_KEY",
    },
}

CONFIG_DIR = os.path.expanduser("~/.config/codrninja")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


if HAS_PROMPT:
    class SlashCompleter(Completer):
        """Custom completer for slash commands."""

        def get_completions(self, document, complete_event):
            text = document.text
            if not text.startswith('/'):
                return

            partial = text[1:]
            for cmd, desc in SLASH_COMMANDS.items():
                if cmd[1:].startswith(partial):
                    yield Completion(
                        cmd,
                        start_position=-len(text),
                        display=f"{cmd:18} {desc}",
                        display_meta=desc,
                    )


class TUI:
    """Terminal User Interface using prompt_toolkit."""

    def __init__(self, ai: AICode, session_name: Optional[str]):
        self.ai = ai
        self.session_name = session_name
        self.console = Console() if HAS_RICH else None
        self.tools = ToolRegistry()
        self.mcp = MCPManager()
        self.skill_registry = SkillRegistry()
        self.skill_registry.discover()
        self.agent = None
        if session_name:
            ai.create_session(session_name)
            self.agent = Agent(ai, session_name)

    def start(self):
        """Start the TUI."""
        if not HAS_PROMPT:
            print("Error: prompt_toolkit not installed")
            print("Run: pip3 install prompt_toolkit")
            return

        if not self._has_config():
            self._onboarding()

        # Session selection when none provided
        if self.session_name is None:
            self.session_name = self._pick_session_interactive()
            if self.session_name is None:
                print("No session selected. Exiting.")
                return
            # Rebind agent with resolved session
            self.agent = Agent(self.ai, self.session_name)

        self._show_welcome()
        self._show_history()

        # Dynamic style based on provider
        provider = self.ai.config.default_provider if self.ai and self.ai.config else 'ollama'
        prompt_color = {
            'ollama': '#00ffff',
            'openai': '#00ff00',
            'anthropic': '#ff00ff',
            'openrouter': '#ffff00',
        }.get(provider, '#00ffff')

        style = Style.from_dict({
            'prompt': f'{prompt_color} bold',
            'completion-menu': 'bg:#1a1a2e #ffffff',
            'completion-menu.completion.current': 'bg:#16213e #00ffff',
            'completion-menu.completion': 'bg:#1a1a2e #e0e0e0',
            'completion-menu.meta.completion': 'bg:#0f3460 #aaaaaa',
            'completion-menu.meta.completion.current': 'bg:#16213e #ffffff',
            'bottom-toolbar': 'bg:#1a1a2e #00aaaa',
        })

        session = PromptSession(
            completer=SlashCompleter(),
            style=style,
            complete_while_typing=True,
            multiline=False,
        )

        while True:
            try:
                message = session.prompt(self._prompt_text())

                if not message.strip():
                    continue
                if message.lower() in ['exit', 'quit', 'q']:
                    print("\nGoodbye!\n")
                    break
                if message.startswith('/'):
                    if not self._handle_command(message):
                        break
                    continue

                if self._handle_subagent_mention(message):
                    continue

                self._run_agent(message, AgentMode.BUILD)
            except KeyboardInterrupt:
                print("\nInterrupted. Type 'exit' to quit.")
            except EOFError:
                break

    def _pick_session_interactive(self) -> Optional[str]:
        """Show arrow-key selectable session browser and return selected name, or None."""
        sessions = self.ai.list_sessions()
        if not sessions:
            print("\ncodrninja — Select Session\n")
            name = input("No sessions found. Enter new session name: ").strip()
            if name:
                self.ai.create_session(name)
                return name
            return None

        options = []
        for s in sessions:
            updated = s.get('updated_at') or s.get('created_at') or ''
            label = f"{s.get('name', 'unknown')}"
            if updated:
                label += f" ({updated[:10]})"
            options.append(label)
        options.append("Create New Session")

        idx = self._select_option(options, "Select session (↑↓ arrows, Enter to confirm):")
        if idx is None:
            return None

        if idx == len(options) - 1:
            new_name = input("New session name: ").strip()
            if new_name:
                self.ai.create_session(new_name)
                return new_name
            return None

        name = sessions[idx].get('name', 'default')
        self.ai.create_session(name)
        return name

    def _has_config(self) -> bool:
        return os.path.exists(CONFIG_FILE)

    def _load_config(self) -> dict:
        if not self._has_config():
            return {}
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)

    def _save_config(self, config: dict):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

    def _select_option(self, options: list[str], prompt_text: str = "Select:") -> int:
        """Arrow-key selectable list using prompt_toolkit."""
        from prompt_toolkit.application import Application
        from prompt_toolkit.key_binding import KeyBindings
        from prompt_toolkit.layout import Layout, HSplit, Window, FormattedTextControl

        selected = [0]

        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            selected[0] = (selected[0] - 1) % len(options)
            event.app.invalidate()

        @kb.add('down')
        def _(event):
            selected[0] = (selected[0] + 1) % len(options)
            event.app.invalidate()

        @kb.add('enter')
        def _(event):
            event.app.exit(result=selected[0])

        @kb.add('c-c')
        @kb.add('c-q')
        def _(event):
            event.app.exit(result=None)

        def get_text():
            lines = [prompt_text]
            for i, opt in enumerate(options):
                prefix = "> " if i == selected[0] else "  "
                lines.append(f"{prefix}{opt}")
            return "\n".join(lines) + "\n"

        root = HSplit([
            Window(FormattedTextControl(get_text), height=len(options) + 1)
        ])

        app = Application(layout=Layout(root), key_bindings=kb, full_screen=False)
        return app.run()

    def _onboarding(self):
        print("\n" + "=" * 80)
        print("  Welcome to codrninja!")
        print("  Let's set up your AI provider.")
        print("=" * 80 + "\n")

        print("Step 1: Choose your AI provider\n")
        providers_list = list(PROVIDERS.items())
        provider_names = [info['name'] for _, info in providers_list]
        idx = self._select_option(provider_names, "Select AI provider (↑↓ arrows, Enter to confirm):")
        if idx is None:
            print("Setup cancelled.")
            return

        provider_key, provider_info = providers_list[idx]
        print(f"\n  Selected: {provider_info['name']}\n")

        api_key = None
        if provider_info.get('needs_key'):
            env_var = provider_info['env_var']
            existing = os.environ.get(env_var, "")

            if existing:
                print(f"  Found {env_var} in environment.")
                use_existing = input("  Use existing key? [Y/n]: ").strip().lower()
                if use_existing in ['', 'y', 'yes']:
                    api_key = existing

            if not api_key:
                auth_options = ['Enter API Key']
                if provider_key == 'openai':
                    auth_options.append('OpenAI OAuth (ChatGPT Plus/Pro)')
                auth_options.append('Skip')
                print(f"\n  {provider_info['name'].split('(')[0].strip()} authentication:")
                auth_idx = self._select_option(auth_options, 'Select authentication method:')

                if auth_idx == 0:
                    print(f"\n  Please enter your {provider_info['name'].split('(')[0].strip()} API key:")
                    api_key = input("  > ").strip()
                    if api_key:
                        os.environ[env_var] = api_key
                        print(f"\n  Set {env_var} for this session.")
                        print("  (To make it permanent, add it to your shell profile)\n")
                elif auth_idx == 1 and provider_key == 'openai':
                    try:
                        from codrninja.auth import OAuthFlow
                        from codrninja.oauth_providers import OpenAIOAuth
                        provider = OpenAIOAuth()
                        flow = OAuthFlow('openai', provider=provider, callback_port=1455)
                        success, msg = flow.run(open_browser=True)
                        if success:
                            tokens = flow.token_manager.get_tokens('openai')
                            if tokens and tokens.get('access_token'):
                                os.environ[env_var] = tokens['access_token']
                                print(f"    OpenAI OAuth successful!")
                                print(f"    Token: {tokens['access_token'][:12]}...")
                            else:
                                print(f"    OAuth failed: no access token.")
                        else:
                            print(f"    OAuth failed: {msg}")
                    except Exception as e:
                        print(f"    OAuth error: {e}")
                else:
                    print("  Skipping authentication.")
        print("Step 2: Choose default model\n")
        if provider_info.get('can_custom_url'):
            default_url = provider_info.get('default_url', 'http://localhost:11434')
            custom_url = input(f"  Ollama URL [{default_url}]: ").strip()
            if not custom_url:
                custom_url = default_url
            os.environ['OLLAMA_URL'] = custom_url

        models = provider_info['models']
        if not models:
            print("  Fetching models from Ollama...")
            import urllib.request
            try:
                url = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
                req = urllib.request.Request(f"{url}/api/tags")
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = json.loads(response.read().decode())
                    models = [m['name'] for m in data.get('models', [])]
            except Exception as e:
                print(f"  Could not fetch models: {e}")
                models = ['llama3.2', 'llama3.1', 'codellama']

        if models:
            model_idx = self._select_option(models, "Select default model (↑↓ arrows, Enter to confirm):")
            if model_idx is not None:
                default_model = models[model_idx]
            else:
                default_model = models[0] if models else "gpt-4"
            # Validate the selected model is actually available
            if provider_key == 'ollama':
                try:
                    import urllib.request
                    url = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
                    req = urllib.request.Request(f"{url}/api/show", data=json.dumps({"name": default_model}).encode(), headers={"Content-Type": "application/json"})
                    urllib.request.urlopen(req, timeout=5)
                except Exception:
                    print(f"  Warning: Model '{default_model}' may not be available. Check that it is pulled/installed.")
                    confirm = input("  Continue anyway? [y/N]: ").strip().lower()
                    if confirm not in ('y', 'yes'):
                        print("  Model selection cancelled.")
                        return
        else:
            default_model = input("  Enter model name: ").strip() or "gpt-4"

        print(f"\n  Selected model: {default_model}\n")

        config = {
            'provider': provider_key,
            'model': default_model,
            'api_key': api_key,
        }
        if provider_key == 'ollama' and custom_url:
            config['ollama_url'] = custom_url

        self._save_config(config)
        print("=" * 80)
        print("  Configuration saved!")
        print(f"  Location: {CONFIG_FILE}")
        print("=" * 80 + "\n")

    def _prompt_text(self) -> str:
        # Plain prompt — prompt_toolkit does not understand Rich markup
        model = self.ai.config.default_model if self.ai and self.ai.config else 'AI'
        short_name = model.split(':')[0] if ':' in model else model
        short_name = short_name.split('/')[-1] if '/' in short_name else short_name
        short_name = short_name[:12]
        steps = self.agent.step_count if self.agent else 0
        max_steps = self.agent.max_steps if self.agent else 50
        return f"{short_name}[{steps}/{max_steps}]: "

    def _pending_todo_count(self) -> int:
        try:
            from codrninja.todo import TodoManager
            return len(TodoManager().list(self.session_name))
        except Exception:
            return 0

    def _show_welcome(self):
        if self.console:
            self.console.print(Panel(CODRNINJA_LOGO, border_style="bright_cyan", box=box.HEAVY, title="codrninja", title_align="left"))
            if self.session_name:
                self.console.print(f"\n  [bold]Session:[/bold] {self.session_name}")
            web_status = 'enabled' if self.ai.config.web_search else 'disabled'
            # Show ACTUAL runtime values, not defaults
            try:
                reasoning = self.ai.config.reasoning_level or 'medium'
                ctx_size = self.ai.config.get('context_size', '8K') if hasattr(self.ai.config, 'get') else '8K'
            except Exception:
                reasoning = 'medium'
                ctx_size = '8K'
            # Get actual permissions mode from PermissionManager if available
            perm_mode = self.agent.permissions.mode if self.agent and self.agent.permissions else 'ask'
            info_table = Table(show_header=False, border_style="green", box=box.SIMPLE_HEAVY)
            info_table.add_column("Property", style="bold green", width=16)
            info_table.add_column("Value", style="white")
            info_table.add_row("MCP tools", str(self.tools.mcp.tool_count()))
            info_table.add_row("Web tools", web_status)
            info_table.add_row("Pending todos", str(self._pending_todo_count()))
            info_table.add_row("Permissions", perm_mode)
            info_table.add_row("Reasoning", f"{reasoning} ({ctx_size} ctx)")
            self.console.print(Panel(info_table, title="Session Info", border_style="green", box=box.ROUNDED))
            self.console.print("  Type / for commands\n")
        else:
            print(CODRNINJA_LOGO)
            if self.session_name:
                print(f"\n  Session: {self.session_name}")
            web_status = 'enabled' if self.ai.config.web_search else 'disabled'
            perm_mode = self.agent.permissions.mode if self.agent and self.agent.permissions else 'ask'
            print(f"  MCP tools: {self.tools.mcp.tool_count()}")
            print(f"  Web tools: {web_status}")
            print(f"  Pending todos: {self._pending_todo_count()}")
            print(f"  Permissions: {perm_mode}")
            print(f"  Reasoning: {reasoning} ({ctx_size} ctx)")
            print("  Type / for commands\n")

    def _show_history(self, limit: int = 20):
        """Display the last `limit` messages from the current session."""
        if not self.session_name:
            return
        try:
            messages = self.ai.session_manager.get_messages(self.session_name, limit=limit)
            if not messages:
                return
            if self.console:
                from rich.rule import Rule
                self.console.print(Rule(f"[dim]Last {len(messages)} messages[/dim]", style="dim"))
                for msg in messages:
                    role = msg.get("role", "unknown")
                    content = msg.get("content", "")
                    ts = msg.get("timestamp", "")[:16].replace("T", " ")
                    if role == "user":
                        self.console.print(f"[bold cyan]You[/bold cyan] [dim]{ts}[/dim]")
                        self.console.print(f"  {content[:300]}{'...' if len(content) > 300 else ''}\n")
                    elif role == "assistant":
                        model_name = msg.get("model") or (self.ai.config.default_model if self.ai else "AI")
                        self.console.print(f"[bold magenta]{model_name}[/bold magenta] [dim]{ts}[/dim]")
                        self.console.print(Markdown(content[:800] + ("..." if len(content) > 800 else "")))
                        self.console.print()
                self.console.print(Rule(style="dim"))
            else:
                print(f"\n--- Last {len(messages)} messages ---")
                for msg in messages:
                    role = msg.get("role", "unknown")
                    content = msg.get("content", "")
                    ts = msg.get("timestamp", "")[:16].replace("T", " ")
                    prefix = "You" if role == "user" else "AI"
                    print(f"\n[{ts}] {prefix}:")
                    print(f"  {content[:300]}{'...' if len(content) > 300 else ''}")
                print("---\n")
        except Exception:
            pass

    def _run_agent(self, message: str, mode: str):
        self.agent = Agent(self.ai, self.session_name, mode=mode)

        anim_handle: list = [None]  # mutable container so closure can write to it

        def _stop_anim():
            if anim_handle[0] is not None:
                anim_handle[0]()
                anim_handle[0] = None

        def _start_anim():
            if anim_handle[0] is None:
                anim_handle[0] = _start_typing_animation(THINKING_MESSAGES)

        def _on_progress(event):
            # Stop animation first — this joins the thread, guaranteeing it has
            # finished all writes before we print.
            _stop_anim()
            if isinstance(event, dict):
                etype = event.get('type', '')
                tool = event.get('tool', '')
                step = event.get('step', '')
                max_steps = event.get('max_steps', '')
                if etype == 'tool_start':
                    args = event.get('args', {})
                    arg_preview = str(args)[:80] if args else ''
                    line = f"  → [{step}/{max_steps}] {tool}({arg_preview})"
                elif etype == 'tool_result':
                    ok = event.get('success', True)
                    out = event.get('output', '')[:80]
                    icon = '+' if ok else 'x'
                    line = f"  {icon} {tool}: {out}"
                else:
                    line = f"  · {event}"
            else:
                line = f"  → {event}"

            with _STDOUT_LOCK:
                if self.console:
                    self.console.print(f"[dim]{line}[/dim]")
                else:
                    print(line)
            _start_anim()

        self.agent.on_progress = _on_progress
        try:
            _start_anim()
            try:
                result = self.agent.run(message, auto_approve=False)
            finally:
                _stop_anim()
        except KeyboardInterrupt:
            print("\nInterrupted by user")
            return
        except Exception as exc:
            print(f"\nError: {exc}")
            return

        if not result['success']:
            error_text = result.get('error', 'Unknown error')
            if self.console:
                style = 'yellow' if 'requires confirmation' in error_text else 'red'
                self.console.print(f"\n[bold {style}]Error:[/bold {style}] {error_text}")
            else:
                print(f"\nError: {error_text}")
            # Show tool usage even on error if any tools were used
            tools_used = result.get('tools_used', [])
            if tools_used and self.console:
                iterations = result.get('iterations', 0)
                self._show_tool_usage(tools_used, iterations)
            return

        response = result.get('response', '')
        model_name = self.ai.config.default_model if self.ai and self.ai.config else 'AI'
        if response:
            self._display_response(response, model_name)

        tools_used = result.get('tools_used', [])
        if tools_used and self.console:
            iterations = result.get('iterations', 0)
            self._show_tool_usage(tools_used, iterations)

    def _handle_command(self, message: str) -> bool:
        parts = shlex.split(message)
        if not parts:
            return True
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd == '/exit':
            print("\nGoodbye!\n")
            return False
        elif cmd == '/clear':
            os.system('clear' if os.name != 'nt' else 'cls')
            return True
        elif cmd == '/help':
            self._show_help()
            return True
        elif cmd == '/session':
            self._show_session_info()
            return True
        elif cmd == '/context':
            self._show_context()
            return True
        elif cmd == '/maxsteps':
            self._set_maxsteps(args)
            return True
        elif cmd == '/model':
            self._show_model_info()
            return True
        elif cmd == '/files':
            self._list_files(args)
            return True
        elif cmd == '/read':
            self._read_file(args)
            return True
        elif cmd == '/exec':
            self._exec_command(args)
            return True
        elif cmd == '/search':
            self._search_web(args)
            return True
        elif cmd == '/fetch':
            self._fetch_page(args)
            return True
        elif cmd == '/build':
            self._run_agent(' '.join(args), AgentMode.BUILD)
            return True
        elif cmd == '/plan':
            self._run_agent(' '.join(args), AgentMode.PLAN)
            return True
        elif cmd == '/review':
            self._run_agent(f'Review this code:\n\n{" ".join(args)}', AgentMode.PLAN)
            return True
        elif cmd == '/explain':
            self._run_agent(f'Explain: {" ".join(args)}', AgentMode.PLAN)
            return True
        elif cmd == '/test':
            self._run_tests(args)
            return True
        elif cmd == '/commit':
            self._commit_changes(args)
            return True
        elif cmd == '/reasoning':
            self._set_reasoning(args)
            return True
        elif cmd == '/todo':
            self._handle_todo(args)
            return True
        elif cmd == '/permissions':
            self._handle_permissions(args)
            return True
        elif cmd == '/mcp':
            self._handle_mcp_command(args)
            return True
        elif cmd == '/skills':
            self._show_skills()
            return True
        elif cmd == '/subagents':
            self._list_subagents()
            return True
        else:
            print(f"Unknown command: {cmd}")
            print("Type /help for available commands")
            return True

    def _handle_subagent_mention(self, message: str) -> bool:
        if not message.startswith('@'):
            return False
        parts = message.split(None, 1)
        name = parts[0][1:]
        task = parts[1] if len(parts) > 1 else ""
        mode = BUILTIN_SUBAGENTS.get(name.lower(), AgentMode.BUILD)
        return self._spawn_subagent(name, task, mode)

    def _spawn_subagent(self, name: str, task: str, mode: str) -> bool:
        if not self.agent:
            print("No agent initialized")
            return False

        if not self.agent.subagent_manager:
            from codrninja.subagent import SubagentManager
            self.agent.subagent_manager = SubagentManager(self.ai, self.agent)

        try:
            subagent = self.agent.subagent_manager.spawn(name=name, task=task, mode=mode)
            # Hook progress so user sees subagent steps
            def _on_progress(msg: str):
                if self.console:
                    self.console.print(f"[dim]  → [{name}] {msg}[/dim]")
                else:
                    print(f"  → [{name}] {msg}")
            subagent.on_progress = _on_progress
            if self.console:
                stop_anim = _start_typing_animation(THINKING_MESSAGES)
                try:
                    result = subagent.run(task)
                finally:
                    stop_anim()
            else:
                stop_anim = _start_typing_animation(THINKING_MESSAGES)
                try:
                    result = subagent.run(task)
                finally:
                    stop_anim()

            if result.get('success'):
                print(f"\n[bold green]{name} completed successfully[/bold green]")
                if result.get('response'):
                    self._display_response(result['response'], model_name)
            else:
                print(f"\n[bold red]{name} failed:[/bold red] {result.get('error', 'Unknown error')}")
            return True
        except Exception as exc:
            print(f"\n[bold red]Error spawning {name}:[/bold red] {exc}")
            return False

    def _show_help(self):
        if self.console:
            table = Table(title="codrninja Commands", show_header=True, border_style="cyan", box=box.ROUNDED)
            table.add_column("Command", style="bold cyan", width=18)
            table.add_column("Description", style="white")
            for cmd, desc in SLASH_COMMANDS.items():
                table.add_row(cmd, desc)
            self.console.print()
            self.console.print(table)
            self.console.print("  You can also mention subagents with @name")
            self.console.print("  Example: @general write a function to sort a list")
            self.console.print()
        else:
            print("\n" + "=" * 60)
            print("  codrninja Commands")
            print("=" * 60)
            for cmd, desc in SLASH_COMMANDS.items():
                print(f"  {cmd:18} {desc}")
            print("\n  You can also mention subagents with @name")
            print("  Example: @general write a function to sort a list")
            print("=" * 60 + "\n")

    def _show_session_info(self):
        if not self.session_name:
            print("No active session")
            return
        try:
            history = self.ai.get_history(self.session_name)
            if history:
                messages = history.get('messages', [])
                if self.console:
                    table = Table(title=f"Session: {self.session_name}", show_header=False, border_style="green", box=box.ROUNDED)
                    table.add_column("Property", style="bold green", width=16)
                    table.add_column("Value", style="white")
                    table.add_row("Name", self.session_name)
                    table.add_row("Messages", str(len(messages)))
                    table.add_row("Created", history.get('created_at', 'Unknown'))
                    self.console.print()
                    self.console.print(table)
                    self.console.print()
                else:
                    print(f"\nSession: {self.session_name}")
                    print(f"Messages: {len(messages)}")
                    print(f"Created: {history.get('created_at', 'Unknown')}")
            else:
                print(f"Session '{self.session_name}' not found")
        except Exception as exc:
            print(f"Error: {exc}")

    def _show_context(self):
        """Show session context: model, tokens, steps, git info."""
        try:
            # Model info
            model = self.ai.config.default_model if self.ai and self.ai.config else 'Not configured'
            provider = self.ai.config.default_provider if self.ai and self.ai.config else 'Not configured'
            steps = self.agent.step_count if self.agent else 0
            max_steps = self.agent.max_steps if self.agent else 50
            
            print(f"\n  Context:")
            print(f"    Model: {model}")
            print(f"    Provider: {provider}")
            print(f"    Steps: {steps}/{max_steps}")
            
            # Token info from last result
            if self.agent and hasattr(self.agent, 'last_result'):
                tokens = self.agent.last_result.get('tokens', {})
                if tokens:
                    print(f"    Tokens: {tokens.get('input', 0)} in / {tokens.get('output', 0)} out")
            
            # Git info
            import subprocess
            branch = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True, cwd='.')
            if branch.returncode == 0:
                print(f"    Git branch: {branch.stdout.strip()}")
            
            changes = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True, cwd='.')
            if changes.returncode == 0 and changes.stdout.strip():
                print(f"    Git changes: {len(changes.stdout.strip().split(chr(10)))} files")
            
        except Exception as e:
            print(f"  Error getting context: {e}")

    def _show_model_info(self):
        """Show current AI config, then optionally reconfigure via arrow-key selection."""
        try:
            # Show current config beautifully
            config = self._load_config()
            if self.console:
                from rich.table import Table
                table = Table(title="Current AI Configuration", show_header=False, border_style="cyan")
                table.add_column("Setting", style="bold cyan", width=16)
                table.add_column("Value", style="white")
                table.add_row("Provider", config.get('provider', 'Not configured'))
                table.add_row("Model", config.get('model', 'Not configured'))
                if config.get('ollama_url'):
                    table.add_row("Ollama URL", config['ollama_url'])
                elif config.get('url'):
                    table.add_row("Ollama URL", config['url'])
                self.console.print()
                self.console.print(table)
            else:
                print(f"\n  Current configuration:")
                print(f"    Provider: {config.get('provider', 'Not configured')}")
                print(f"    Model: {config.get('model', 'Not configured')}")
                if config.get('ollama_url'):
                    print(f"    Ollama URL: {config['ollama_url']}")
                elif config.get('url'):
                    print(f"    Ollama URL: {config['url']}")

            # Ask if user wants to change provider
            print()
            change = self._select_option(['Keep current', 'Change provider & model'], 'What would you like to do?')
            if change != 1:
                return

            # Step 1: Select provider beautifully
            providers_list = list(PROVIDERS.items())
            provider_names = [info['name'] for _, info in providers_list]
            idx = self._select_option(provider_names, "Select AI provider (↑↓ arrows, Enter to confirm):")
            if idx is None:
                print("  Cancelled.")
                return
            provider_key, provider_info = providers_list[idx]
            if self.console:
                self.console.print(f"\n  [bold green]Selected:[/bold green] [white]{provider_info['name']}[/white]")
            else:
                print(f"\n  Selected: {provider_info['name']}")

            # Step 2: API key if needed
            if provider_info.get('needs_key'):
                env_var = provider_info['env_var']
                existing = os.environ.get(env_var, '')

                # Check if we already have valid auth (OAuth token or API key in env)
                has_auth = bool(existing)
                # Also check for stored OAuth tokens
                if not has_auth and provider_key == 'openai':
                    try:
                        from codrninja.auth import TokenManager
                        tm = TokenManager()
                        tokens = tm.get_tokens('openai')
                        if tokens and tokens.get('access_token'):
                            has_auth = True
                    except Exception:
                        pass
                if has_auth:
                    # Already authenticated — skip auth prompt
                    print(f"\n  Already authenticated for {provider_info['name'].split('(')[0].strip()}. Skipping login.")
                else:
                    # Build auth options based on provider
                    auth_options = ['API Key']
                    if provider_key == 'openai':
                        auth_options.append('OpenAI OAuth (ChatGPT Plus/Pro)')
                    auth_options.append('Skip')

                    print(f"\n  {provider_info['name'].split('(')[0].strip()} authentication:")
                    auth_idx = self._select_option(auth_options, 'Select authentication method:')

                    if auth_idx == 0:  # API Key
                        if existing:
                            print(f"    Current: {existing[:8]}... (press Enter to keep, or type new)")
                        else:
                            print(f"    Enter API key (or leave blank to configure later):")
                        new_key = input("  ").strip()
                        if new_key:
                            os.environ[env_var] = new_key
                            print(f"    API key set.")
                    elif auth_idx == 1 and provider_key == 'openai':  # OpenAI OAuth
                        try:
                            from codrninja.auth import OAuthFlow
                            from codrninja.oauth_providers import OpenAIOAuth
                            provider = OpenAIOAuth()
                            flow = OAuthFlow('openai', provider=provider, callback_port=1455)
                            print(f"\n    Opening browser for OpenAI login...")
                            print(f"    If browser doesn't open, use API Key instead.")
                            success, msg = flow.run(open_browser=True)
                            if success:
                                tokens = flow.token_manager.get_tokens('openai')
                                if tokens and tokens.get('access_token'):
                                    os.environ[env_var] = tokens['access_token']
                                    print(f"    OpenAI OAuth successful!")
                                    print(f"    Token: {tokens['access_token'][:12]}...")
                                else:
                                    print(f"    OAuth failed: no access token.")
                            else:
                                print(f"    OAuth failed: {msg}")
                                print(f"    Tip: Use API Key instead.")
                        except Exception as e:
                            print(f"    OAuth error: {e}")
                            print(f"    Try using API Key instead.")
                    else:  # Skip (any provider)
                        print("    Skipping authentication.")

            # Step 2b: Ollama URL
            ollama_url = None
            if provider_key == 'ollama':
                default_url = config.get('ollama_url', config.get('url', 'http://localhost:11434'))
                print(f"\n  Ollama URL [{default_url}]:")
                new_url = input("  ").strip()
                if new_url:
                    # Auto-prefix http:// if user just types host:port
                    if not new_url.startswith(('http://', 'https://')):
                        new_url = 'http://' + new_url
                    ollama_url = new_url
                    print(f"    URL set to: {ollama_url}")
                else:
                    ollama_url = default_url

            # Step 3: Select model
            print()
            models = list(provider_info['models']) if provider_info.get('models') else []
            if provider_key == 'ollama' and not models:
                print("  Fetching models from Ollama...")
                try:
                    import urllib.request, json
                    # Use the URL just entered by user, not stale config
                    fetch_url = ollama_url or config.get('ollama_url', config.get('url', 'http://localhost:11434'))
                    req = urllib.request.Request(f"{fetch_url}/api/tags")
                    with urllib.request.urlopen(req, timeout=5) as resp:
                        data = json.loads(resp.read().decode())
                        models = [m['name'] for m in data.get('models', [])]
                        if models:
                            print(f"  Found {len(models)} models.")
                except Exception as e:
                    print(f"  Could not fetch models: {e}")
                    models = ['llama3.2', 'llama3.1', 'codellama']

            # Fetch models from API providers if key is available
            api_key = os.environ.get(provider_info.get('env_var', ''), '')
            # Also check for OpenAI OAuth token (even if auth was skipped above)
            if provider_key == 'openai' and not api_key:
                try:
                    from codrninja.auth import TokenManager
                    tm = TokenManager()
                    tokens = tm.get_tokens('openai')
                    if tokens and tokens.get('access_token'):
                        api_key = tokens['access_token']
                except Exception:
                    pass
            if provider_key == 'openai' and api_key:
                # Check if this is an OAuth token (JWT, starts with 'eyJ') vs API key (sk-)
                is_oauth = not api_key.startswith('sk-')
                if is_oauth:
                    # OAuth: use internal list + codex.ts ALLOWED_MODELS filter (no HTTP request)
                    print("  Using Codex models for OAuth...")
                    # All known OpenAI models (like opencode's provider definition)
                    ALL_OPENAI_MODELS = [
                        "gpt-5.5",
                        "gpt-5.4",
                        "gpt-5.4-mini",
                        "gpt-5.3-codex",
                        "gpt-5.3-codex-spark",
                        "gpt-5.2",
                        "gpt-5",
                        "gpt-4o",
                        "gpt-4o-mini",
                        "gpt-4-turbo",
                        "gpt-4",
                        "gpt-3.5-turbo",
                    ]
                    ALLOWED_MODELS = {
                        "gpt-5.5",
                        "gpt-5.2",
                        "gpt-5.3-codex",
                        "gpt-5.3-codex-spark",
                        "gpt-5.4",
                        "gpt-5.4-mini",
                    }
                    def _is_codex_oauth_model(model_id: str) -> bool:
                        """1:1 aus codex.ts models() Hook"""
                        if model_id in ALLOWED_MODELS:
                            return True
                        import re
                        match = re.match(r"^gpt-(\d+\.\d+)", model_id)
                        if match:
                            return float(match.group(1)) > 5.4
                        return False
                    models = [m for m in ALL_OPENAI_MODELS if _is_codex_oauth_model(m)]
                    print(f"  Found {len(models)} Codex models.")
                else:
                    # API Key: Fetch from OpenAI
                    print("  Fetching models from OpenAI...")
                    try:
                        import urllib.request
                        import ssl
                        ctx = ssl._create_unverified_context()
                        req = urllib.request.Request(
                            "https://api.openai.com/v1/models",
                            headers={"Authorization": f"Bearer {api_key}"}
                        )
                        with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                            data = json.loads(resp.read().decode())
                            all_models = [m['id'] for m in data.get('data', [])]
                            # Filter to only chat completions models (exclude embeddings, audio, etc.)
                            chat_prefixes = ('gpt-', 'chatgpt-', 'o1', 'o3')
                            models = [m for m in all_models if any(m.startswith(p) for p in chat_prefixes)]
                            if models:
                                print(f"  Found {len(models)} models.")
                            else:
                                print("  No chat models found, using defaults.")
                                models = provider_info.get('models', [])
                    except Exception as e:
                        print(f"  Could not fetch models: {e}")
                        models = provider_info.get('models', [])
            elif provider_key == 'anthropic' and api_key:
                print("  Fetching models from Anthropic...")
                try:
                    import urllib.request
                    import ssl
                    ctx = ssl._create_unverified_context()
                    req = urllib.request.Request(
                        "https://api.anthropic.com/v1/models",
                        headers={
                            "x-api-key": api_key,
                            "anthropic-version": "2023-06-01"
                        }
                    )
                    with urllib.request.urlopen(req, timeout=5, context=ctx) as resp:
                        data = json.loads(resp.read().decode())
                        models = [m['id'] for m in data.get('data', [])]
                        if models:
                            print(f"  Found {len(models)} models.")
                        else:
                            print("  No models found, using defaults.")
                            models = provider_info.get('models', [])
                except Exception as e:
                    print(f"  Could not fetch models: {e}")
                    models = provider_info.get('models', [])

            if models:
                model_idx = self._select_option(models, "Select default model (↑↓ arrows, Enter to confirm):")
                if model_idx is not None:
                    default_model = models[model_idx]
                else:
                    default_model = models[0] if models else "gpt-4"
                # Validate the selected model is actually available
                if provider_key == 'ollama':
                    try:
                        import urllib.request
                        validate_url = ollama_url or config.get('ollama_url', config.get('url', 'http://localhost:11434'))
                        req = urllib.request.Request(f"{validate_url}/api/show", data=json.dumps({"name": default_model}).encode(), headers={"Content-Type": "application/json"})
                        urllib.request.urlopen(req, timeout=5)
                    except Exception:
                        print(f"  Warning: Model '{default_model}' may not be available. Check that it is pulled/installed.")
                        confirm = input("  Continue anyway? [y/N]: ").strip().lower()
                        if confirm not in ('y', 'yes'):
                            print("  Model selection cancelled.")
                            return
            else:
                print("  Enter model name manually:")
                default_model = input("  ").strip() or "gpt-4"
            if self.console:
                self.console.print(f"\n  [bold green]Selected model:[/bold green] [white]{default_model}[/white]")
            else:
                print(f"\n  Selected model: {default_model}")

            # Step 4: Save config + update runtime
            new_config = {
                'provider': provider_key,
                'model': default_model,
            }
            if provider_key == 'ollama' and ollama_url:
                new_config['ollama_url'] = ollama_url
                new_config['url'] = ollama_url
            self._save_config(new_config)

            # Update the live AI instance so changes take effect immediately
            self.ai.config.default_provider = provider_key
            self.ai.config.default_model = default_model
            if provider_key == 'ollama' and ollama_url:
                self.ai.config.ollama_url = ollama_url
                os.environ['OLLAMA_URL'] = ollama_url
            self.ai.refresh_provider()

            print(f"\n  Configuration saved!")
            print(f"    Provider: {provider_key}")
            print(f"    Model: {default_model}")
            print(f"\n  Changes take effect on the next message.")

        except Exception as exc:
            print(f"Error: {exc}")

    def _list_files(self, args):
        path = args[0] if args else '.'
        try:
            result = self.ai.tools.list_files(path)
            if result.success:
                print(f"\nFiles in {path}:")
                print(result.output)
            else:
                print(f"Error: {result.error}")
        except Exception as exc:
            print(f"Error: {exc}")

    def _read_file(self, args):
        if not args:
            print("Usage: /read <file>")
            return
        path = args[0]
        try:
            result = self.ai.tools.read_file(path)
            if result.success:
                print(f"\n{path}:")
                print(result.output)
            else:
                print(f"Error: {result.error}")
        except Exception as exc:
            print(f"Error: {exc}")

    def _exec_command(self, args):
        if not args:
            print("Usage: /exec <command>")
            return
        cmd = ' '.join(args)
        try:
            result = self.ai.tools.execute_command(cmd)
            if result.success:
                print(f"\n$ {cmd}")
                print(result.output)
            else:
                print(f"Error: {result.error}")
        except Exception as exc:
            print(f"Error: {exc}")

    def _search_web(self, args):
        if not args:
            print("Usage: /search <query>")
            return
        query = ' '.join(args)
        try:
            result = self.ai.tools.web_search(query)
            if result.success:
                print(f"\nSearch results for '{query}':")
                print(result.output)
            else:
                print(f"Error: {result.error}")
        except Exception as exc:
            print(f"Error: {exc}")

    def _fetch_page(self, args):
        if not args:
            print("Usage: /fetch <url>")
            return
        url = args[0]
        try:
            result = self.ai.tools.web_fetch(url)
            if result.success:
                print(f"\n{url}:")
                print(result.output[:2000])
            else:
                print(f"Error: {result.error}")
        except Exception as exc:
            print(f"Error: {exc}")

    def _run_tests(self, args):
        cmd = ' '.join(args) if args else 'pytest -q'
        try:
            result = self.ai.tools.execute_command(cmd)
            if result.success:
                print(f"\nTests passed:\n{result.output}")
            else:
                print(f"\nTests failed:\n{result.error or result.output}")
        except Exception as exc:
            print(f"Error: {exc}")

    def _commit_changes(self, args):
        if not args:
            print("Usage: /commit <message>")
            return
        message = ' '.join(args)
        try:
            self.ai.tools.execute_command('git add -A')
            result = self.ai.tools.execute_command(f'git commit -m {shlex.quote(message)}')
            if result.success:
                print(f"\nCommitted: {message}")
            else:
                print(f"Error: {result.error}")
        except Exception as exc:
            print(f"Error: {exc}")

    def _set_reasoning(self, args):
        if not args:
            print("Usage: /reasoning <none|low|medium|high>")
            return
        level = args[0].lower()
        if level not in ['none', 'low', 'medium', 'high']:
            print("Invalid level. Use: none, low, medium, high")
            return
        self.ai.config.reasoning_level = level
        # Save to the same config file that Config.from_env() reads
        self._save_config({'reasoning_level': level})
        print(f"\n  Reasoning level set to: {level}")
        print("=" * 60 + "\n")

    def _handle_todo(self, args):
        from codrninja.todo import TodoManager
        manager = TodoManager()
        if not args:
            todos = manager.list(self.session_name)
            if not todos:
                print("No todos")
                return
            print("\nTodos:")
            for todo in todos:
                print(f"  {todo.display}")
            return
        action = args[0].lower()
        if action == 'add':
            if len(args) < 2:
                print("Usage: /todo add <task>")
                return
            manager.add(self.session_name, ' '.join(args[1:]))
            print("Todo added")
        elif action == 'done':
            if len(args) < 2:
                print("Usage: /todo done <id>")
                return
            manager.complete(args[1])
            print("Todo marked as done")
        elif action == 'remove':
            if len(args) < 2:
                print("Usage: /todo remove <id>")
                return
            manager.remove(args[1])
            print("Todo removed")
        else:
            print("Usage: /todo [add|done|remove] <...>")

    def _set_maxsteps(self, args):
        if not args:
            current = self.agent.max_steps if self.agent else 50
            print(f"\n  Current max steps: {current}")
            print("  Usage: /maxsteps <number>")
            return
        try:
            new_limit = int(args[0])
            if new_limit < 1:
                print("  Max steps must be at least 1")
                return
            if self.agent:
                self.agent.max_steps = new_limit
                self.agent.safety.config.max_steps = new_limit
            print(f"\n  Max steps set to: {new_limit}")
        except ValueError:
            print("  Invalid number. Usage: /maxsteps <number>")

    def _handle_permissions(self, args):
        mode_descriptions = {
            'none': 'No tools allowed - all actions denied',
            'ask': 'Prompt before each tool execution (default)',
            'auto': 'Auto-approve all tool executions',
            'strict': 'Allow project files, ask for everything else',
            'relaxed': 'Auto-approve, same as auto',
            'custom': 'Custom rules defined by user',
        }
        if not args:
            # Interactive mode selection
            current_mode = self.agent.permissions.mode if self.agent else 'ask'
            modes = list(mode_descriptions.keys())
            print(f"\n  Current mode: {current_mode}")
            print("  Select new mode (↑↓ arrows, Enter to confirm):\n")
            idx = self._select_option(modes, "Select permission mode:")
            if idx is None:
                print("  Cancelled.")
                return
            new_mode = modes[idx]
            if self.agent:
                self.agent.permissions.set_mode(new_mode)
                self.agent.permissions.save_config()
            # Also save to config.json so Config.from_env() picks it up
            self._save_config({'permissions_mode': new_mode})
            print(f"\n  Permission mode set to: {new_mode}")
            return
        action = args[0].lower()
        if action == 'mode':
            if len(args) < 2 or args[1].lower() not in mode_descriptions:
                print("Usage: /permissions mode <none|ask|auto|strict|relaxed>")
                return
            new_mode = args[1].lower()
            if self.agent:
                self.agent.permissions.set_mode(new_mode)
                self.agent.permissions.save_config()
            # Also save to config.json so Config.from_env() picks it up
            self._save_config({'permissions_mode': new_mode})
            print(f"\n  Permission mode set to: {new_mode}")
            return
        if action == 'add':
            if len(args) < 4:
                print("Usage: /permissions add <tool> <action> <allow|deny>")
                return
            self.agent.permissions.add_rule(PermissionRule(args[1], args[3], args[2]))
            print("Permission rule added")
        elif action == 'remove':
            if len(args) < 2:
                print("Usage: /permissions remove <index>")
                return
            self.agent.permissions.remove_rule(int(args[1]))
            print("Permission rule removed")
        else:
            print("Usage: /permissions [add|remove] <...>")

    def _list_subagents(self):
        if not self.agent or not self.agent.subagent_manager:
            print("No subagents active")
            return
        subagents = self.agent.subagent_manager.list()
        if not subagents:
            print("No active subagents")
            return
        print("\nActive subagents:")
        for s in subagents:
            print(f"  - {s['name']} [{s['status']}]")

    def _handle_mcp_command(self, args: list[str]):
        action = args[0].lower() if args else 'list'

        if action == 'list':
            self.tools.refresh_mcp_tools(force=True)
            servers = self.mcp.list_servers()
            if not servers:
                print("No MCP servers configured.")
                return
            print("MCP servers:")
            for server in servers:
                status = 'enabled' if server.enabled else 'disabled'
                print(f"  - {server.name} [{server.type}] {status} ({len(server.tools)} tools)")
            return

        if action in {'enable', 'disable'}:
            if len(args) < 2:
                print(f"Usage: /mcp {action} <server>")
                return
            ok = self.mcp.enable(args[1]) if action == 'enable' else self.mcp.disable(args[1])
            if ok:
                self.tools.refresh_mcp_tools(force=True)
                print(f"MCP server {action}d: {args[1]}")
            else:
                print(f"Unknown MCP server: {args[1]}")
            return

        if action == 'add':
            if len(args) > 1:
                config_text = ' '.join(args[1:])
            else:
                print("Paste MCP server JSON config:")
                config_text = input('> ').strip()
            try:
                config = json.loads(config_text)
                self.mcp.add_server(config)
                self.tools.refresh_mcp_tools(force=True)
                print(f"Added MCP server: {config['name']}")
            except Exception as e:
                print(f"Failed to add MCP server: {e}")
            return

        print("Usage: /mcp [list|add|enable|disable]")

    def _show_skills(self):
        self.skill_registry.discover()
        skills = self.skill_registry.list_skills()
        if not skills:
            print("\nNo skills installed.")
            return
        print("\nInstalled skills:")
        for skill in skills:
            print(f"  - {skill['name']}: {skill['description']}")

    def _extract_reasoning(self, response: str) -> Optional[str]:
        """Extract reasoning/thinking content from AI response."""
        import re
        patterns = [
            r'<thinking>(.*?)</thinking>',
            r'<reasoning>(.*?)</reasoning>',
            r'Reasoning:(.*?)(?=\n\n|$)',
            r'### Reasoning\n(.*?)(?=\n###|\Z)',
        ]
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _display_response(self, response: str, model_name: str = 'AI'):
        # Extract and display reasoning/thinking steps first
        reasoning = self._extract_reasoning(response)
        if reasoning and self.console:
            from rich.panel import Panel
            self.console.print(Panel(
                Markdown(reasoning),
                title="[dim]Thinking[/dim]",
                border_style="dim",
                title_align="left"
            ))
        # Color by provider
        from .config import Config
        provider = self.ai.config.default_provider if self.ai and self.ai.config else 'ollama'
        label_color = {
            'ollama': 'bright_cyan',
            'openai': 'bright_green',
            'anthropic': 'bright_magenta',
            'openrouter': 'bright_yellow',
        }.get(provider, 'bright_cyan')
        parts = response.split('```')
        for i, part in enumerate(parts):
            if i % 2 == 0:
                if part.strip():
                    self.console.print(f"\n[bold {label_color}]{model_name}:[/bold {label_color}]")
                    self.console.print(Markdown(part.strip()))
            else:
                lines = part.split('\n')
                lang = lines[0].strip() if lines else ''
                code = '\n'.join(lines[1:]) if lines else part
                if code.strip():
                    syntax = Syntax(code, lang or 'text', theme='monokai', line_numbers=True)
                    self.console.print(syntax)

    def _show_tool_usage(self, tools_used: list, iterations: int):
        table = Table(title=f"Tools ({len(tools_used)} calls, {iterations} iterations)", box=box.ROUNDED)
        table.add_column('Tool', style='cyan')
        table.add_column('Status', style='green')
        table.add_column('Result', style='white')
        for tool in tools_used:
            status = 'OK' if tool['success'] else 'FAIL'
            result = tool['output'][:60] + '...' if len(tool['output']) > 60 else tool['output']
            table.add_row(tool['tool'], status, result)
        self.console.print(table)

    def _render_tool_output(self, title: str, result, border_style: str):
        if result.success:
            if self.console:
                self.console.print(Panel(result.output, title=title, border_style=border_style))
            else:
                print(f"\n{result.output}")
        else:
            print(f"Error: {result.error}")


def main():
    if len(sys.argv) < 2:
        print("Usage: codrninja-tui <session-name>")
        sys.exit(1)

    session_name = sys.argv[1]
    ai = AICode()
    tui = TUI(ai, session_name)
    tui.start()


if __name__ == "__main__":
    main()
