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
        self.session = PromptSession(
            key_bindings=self.kb,
            style=repl_style,
        )
        
        @self.kb.add(Keys.ControlC)
        def _(event):
            if event.app.current_buffer.text:
                event.app.current_buffer.reset()
            else:
                # Proper exit
                event.app.exit(result=None)

    def _get_toolbar(self):
        status = "WORKING" if getattr(self.agent, "_is_running", False) else "IDLE"
        status_class = "status.working" if status == "WORKING" else "status.idle"
        # Minimal toolbar - no background bar if possible, just text at the very bottom
        return HTML(
            f" <{status_class}>[SAGE {status}]</{status_class}> "
            f" <style fg='#444444'>· Ctrl+C twice to exit</style>"
        )

    async def _run_agent_task(self, text: str):
        self.agent._is_running = True
        try:
            # Run in thread so PT can still process input
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.execute_fn, text)
        finally:
            self.agent._is_running = False

    async def run(self):
        # Gemini CLI style: Standard terminal logs with a pinned bottom toolbar/prompt
        with patch_stdout():
            while True:
                try:
                    # prompt_async allows the agent thread to print logs while we wait for input
                    text = await self.session.prompt_async(
                        HTML(f"<style fg='#00aa00'><b>{self.prompt_text}</b></style>"),
                        bottom_toolbar=self._get_toolbar,
                    )
                    
                    if text is None:
                        break

                    cleaned = text.strip()
                    if cleaned:
                        if getattr(self.agent, "_is_running", False):
                            # Hint mode
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

def run_repl(agent: Any, execute_fn: Callable[[str], None]):
    """Entry point to start the async REPL."""
    repl = SageREPL(agent, execute_fn)
    try:
        asyncio.run(repl.run())
    except (KeyboardInterrupt, SystemExit):
        pass
