"""Professional Async REPL for SAGE with bottom-anchored prompt and live log streaming."""

from __future__ import annotations

import asyncio
import threading
import sys
from typing import Callable, Any

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

# Professional dark theme styling to match Gemini CLI
repl_style = Style.from_dict({
    "bottom-toolbar": "bg:#000000 fg:#888888",
    "bottom-toolbar.text": "fg:#888888",
    "status.working": "fg:#ffcc00 bold",
    "status.idle": "fg:#00ff00 bold",
})

class SageREPL:
    def __init__(
        self,
        agent: Any,
        execute_fn: Callable[[str], None],
        prompt_text: str = "you> ",
    ):
        self.agent = agent
        self.execute_fn = execute_fn
        self.prompt_text = prompt_text
        self.kb = KeyBindings()
        self.paste_registry: dict[str, str] = {}
        self.session = PromptSession(
            key_bindings=self.kb,
            style=repl_style,
        )
        
        # Insert a conditional thinking status container at the top of the layout HSplit
        from prompt_toolkit.layout.containers import Window, ConditionalContainer
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.filters import Condition, is_done
        
        @Condition
        def show_status_filter():
            return getattr(self.agent, "_is_running", False)
            
        def get_status_text():
            import time
            import html
            from sage.core.renderer import get_repl_status
            status = get_repl_status()
            
            is_running = getattr(self.agent, "_is_running", False)
            if not is_running:
                return HTML("")
                
            msg = status.get("message")
            if not msg:
                return HTML("")
            
            # Escape HTML characters to prevent parser crash
            msg_escaped = html.escape(msg)
            
            model_id = status.get("model_id", "")
            elapsed = status.get("elapsed", 0.0)
            if not elapsed and status.get("start_time"):
                elapsed = time.monotonic() - status["start_time"]
            
            # Choose spinner frame
            frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            frame = frames[int(time.monotonic() * 10) % len(frames)]
            
            # Format elapsed time
            elapsed_str = f" {elapsed:.0f}s" if elapsed > 0.5 else ""
            model_str = f" ({model_id})" if model_id else ""
            
            elapsed_escaped = html.escape(elapsed_str)
            model_escaped = html.escape(model_str)
            
            return HTML(
                f"  <style fg='#ffcc00'><b>{frame}</b></style> "
                f"<style fg='#ffcc00'>{msg_escaped}</style>"
                f"<style fg='#888888'>{elapsed_escaped}{model_escaped}</style>"
            )

        status_window = Window(
            content=FormattedTextControl(get_status_text),
            dont_extend_height=True,
            height=1,
        )
        status_container = ConditionalContainer(
            status_window,
            filter=show_status_filter & ~is_done,
        )
        self.session.layout.container.children.insert(0, status_container)

        @self.kb.add(Keys.ControlC)
        def _(event):
            if event.app.current_buffer.text:
                event.app.current_buffer.reset()
            else:
                # Proper exit
                event.app.exit(result=None)

        @self.kb.add(Keys.BracketedPaste)
        def _on_bracketed_paste(event) -> None:
            data = event.data or ""
            char_count = len(data)
            line_count = len(data.splitlines())
            if char_count < 200 and line_count <= 5:
                event.current_buffer.insert_text(data)
                return
            
            placeholder = f"[Pasted {line_count} lines]"
            self.paste_registry[placeholder] = data
            
            try:
                from pathlib import Path
                import time
                import random
                pastes_dir = Path.home() / ".sage" / "pastes"
                pastes_dir.mkdir(parents=True, exist_ok=True)
                timestamp = int(time.time())
                rand_id = random.randint(1000, 9999)
                paste_file = pastes_dir / f"paste_{timestamp}_{rand_id}.txt"
                paste_file.write_text(data, encoding="utf-8")
            except Exception:
                pass
                
            event.current_buffer.insert_text(placeholder)

    def _get_toolbar(self):
        status = "WORKING" if getattr(self.agent, "_is_running", False) else "IDLE"
        status_class = "status.working" if status == "WORKING" else "status.idle"
        # Minimal toolbar - no background bar if possible, just text at the very bottom
        return HTML(
            f" <{status_class}>[SAGE {status}]</{status_class}> "
            f" <style fg='#444444'>· Ctrl+C twice to exit</style>"
        )

    def _get_prompt_message(self):
        return HTML(f"<style fg='#00aa00'><b>{self.prompt_text}</b></style>")

    async def _animate_status(self):
        from sage.core.renderer import get_repl_status
        while True:
            try:
                status = get_repl_status()
                if status.get("message"):
                    if self.session.app and self.session.app.is_running:
                        self.session.app.invalidate()
            except Exception:
                pass
            await asyncio.sleep(0.1)

    async def _run_agent_task(self, text: str):
        self.agent._is_running = True
        try:
            # Run in thread so PT can still process input
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.execute_fn, text)
        except Exception as e:
            import traceback
            print(f"\nREPL Agent Task Error: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
        finally:
            self.agent._is_running = False

    async def run(self):
        # Gemini CLI style: Standard terminal logs with a pinned bottom toolbar/prompt
        from sage.core.renderer import set_repl_active
        set_repl_active(True)
        anim_task = asyncio.create_task(self._animate_status())
        try:
            with patch_stdout():
                while True:
                    try:
                        # prompt_async allows the agent thread to print logs while we wait for input
                        text = await self.session.prompt_async(
                            self._get_prompt_message,
                            bottom_toolbar=self._get_toolbar,
                        )
                        
                        if text is None:
                            break

                        # Expand bracketed paste placeholders back to actual text
                        if self.paste_registry and "[Pasted " in text:
                            for placeholder, real in list(self.paste_registry.items()):
                                if placeholder in text:
                                    text = text.replace(placeholder, real)
                                    del self.paste_registry[placeholder]

                        cleaned = text.strip()
                        if cleaned:
                            if cleaned.startswith("/"):
                                # Catch REPL exit commands immediately
                                if cleaned.lower() in ("/exit", "/quit", "/q"):
                                    break
                                # Execute slash command immediately (even if agent is running)
                                # since slash commands are local CLI operations, not agent prompts.
                                self.execute_fn(cleaned)
                            elif getattr(self.agent, "_is_running", False):
                                # Hint mode (non-slash commands only)
                                if hasattr(self.agent, "hint_queue"):
                                    self.agent.hint_queue.put(cleaned)
                                    print(f"  💡 Hint absorbed: {cleaned[:60]}...")
                            else:
                                # New task mode
                                asyncio.create_task(self._run_agent_task(cleaned))
                                
                    except EOFError:
                        break
                    except KeyboardInterrupt:
                        # Inner catch for safety
                        break
                    except Exception as e:
                        print(f"REPL Error: {e}")
        finally:
            anim_task.cancel()
            set_repl_active(False)

def run_repl(agent: Any, execute_fn: Callable[[str], None]):
    """Entry point to start the async REPL."""
    repl = SageREPL(agent, execute_fn)
    try:
        asyncio.run(repl.run())
    except (KeyboardInterrupt, SystemExit):
        pass
