import logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
logging.getLogger("transformers").setLevel(logging.WARNING)
logging.getLogger("torch").setLevel(logging.WARNING)
logging.getLogger("supabase").setLevel(logging.WARNING)

import queue
import threading
import math
import os

import requests
from rich.text import Text
from textual import events
from nx_terminal import format_worlds_list
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.css.query import NoMatches
from textual.widgets import Input, Static

def _suppress_noisy_logs():
    for name in ("httpx", "sentence_transformers", "transformers", "torch", "supabase"):
        logging.getLogger(name).setLevel(logging.WARNING)


def _message_header(role):
    return {
        "user": "you",
        "assistant": "✦",
        "system": "note",
        "error": "error",
    }[role]


def _message_header_style(role):
    return {
        "user": "rgb(206,201,188)",
        "assistant": "#c8a44a",
        "system": "rgb(176,150,100)",
        "error": "#c8a44a bold",
    }[role]


def _message_body_style(role):
    return {
        "user": "#d9c183",
        "assistant": "#c8a44a",
        "system": "rgb(185,150,68)",
        "error": "#c8a44a",
    }[role]


def _render_message(role, text):
    lines = (text or "").splitlines() or [""]
    rendered = Text()
    rendered.append(_message_header(role), style=_message_header_style(role))
    rendered.append("\n")
    for index, line in enumerate(lines):
        rendered.append(line, style=_message_body_style(role))
        if index < len(lines) - 1:
            rendered.append("\n")
    return rendered


class MessageBlock(Static):
    def __init__(self, role, text=""):
        super().__init__("", classes=f"message {role}")
        self.role = role
        self.set_text(text)

    def set_text(self, text):
        self.update(_render_message(self.role, text))


class NXChatApp(App):
    BINDINGS = [("ctrl+c", "quit", "Quit"), ("ctrl+q", "quit", "Quit")]

    CSS = """
    Screen {
        background: #050505;
        color: #c8a44a;
    }
    #shell {
        width: 100%;
        height: 1fr;
        padding: 0;
    }
    #panel {
        width: 100%;
        border: solid #c8a44a;
        background: #050505;
    }
    #inner {
        layout: horizontal;
        height: 16;
        width: 100%;
    }
    #left {
        width: 28;
        border-right: solid #c8a44a;
        padding: 1 2;
    }
    #right {
        width: 1fr;
        padding: 1 2;
    }
    #stars {
        border-top: solid #c8a44a;
        border-bottom: solid #c8a44a;
        height: 3;
        padding: 0 1;
    }
    #meta {
        height: 5;
        padding: 1 2;
    }
    #output {
        width: 100%;
        height: 1fr;
        background: #050505;
        padding: 1 2 0 2;
    }
    .message {
        width: 1fr;
        margin: 0 0 1 0;
    }
    .user {
        color: #c8a44a;
        text-style: bold;
    }
    .assistant {
        color: #d2b06a;
    }
    .system {
        color: #b89a5e;
    }
    .error {
        color: #c8a44a;
        text-style: bold;
    }
    #composer {
        width: 100%;
        height: auto;
        margin-top: 1;
    }
    #status {
        height: 1;
        color: #b89a5e;
        padding: 0 2;
    }
    #input-star {
        height: 1;
        color: #c8a44a;
    }
    #prompt {
        width: 1fr;
        border: round #c8a44a;
        background: #050505;
        color: #c8a44a;
    }
    #context {
        height: 1;
        color: #b89a5e;
        padding: 0 1;
    }
    """

    CONTEXT_LIMIT = 128000

    TIPS = [
        [("Type your task directly to start", "dim"), ("/help  /mode  /model  /council  /exit", "gold"), ("Sessions saved automatically", "dim")],
        [("Use /model to switch models", "dim"), ("BYOK or use Nexplora credits", "dim"), ("Plan First for complex tasks", "gold")],
        [("Route across every world instantly", "dim"), ("Autonomous execution, reviewable", "dim"), ("$council — 3 models debate hard calls", "gold")],
    ]

    def __init__(self, cfg, stream_chat, save_session, clear_config, load_system_prompt, help_lines,
                 on_start=None, on_user_message=None, on_assistant_message=None, on_command=None, on_save_command=None, on_world_change=None, on_exit=None):
        super().__init__()
        self.cfg = cfg or {}
        self._stream_chat = stream_chat
        self._save_session = save_session
        self._clear_config = clear_config
        self._load_system_prompt = load_system_prompt
        self._help_lines = tuple(help_lines)
        # Mask the account email so screen-shares don't leak it. Same helper
        # the terminal welcome banner uses.
        try:
            from nx_terminal import _mask_email as _mask
        except Exception:
            _mask = lambda s: s
        self._who = _mask(self.cfg.get("account") or "") or ("API key" if self.cfg.get("auth") == "apikey" else "Nexplora account")
        self._messages = [{"role": "system", "content": self._load_system_prompt()}]
        self._events = queue.Queue()
        self._assistant = None
        self._assistant_text = ""
        self._streaming = False
        self._logout_on_exit = False
        self._t = 0
        self._sf = 0
        self._tip_set = 0
        self._tip_tick = 0
        self._on_start = on_start
        self._on_user_message = on_user_message
        self._on_assistant_message = on_assistant_message
        self._on_command = on_command
        self._on_save_command = on_save_command
        self._on_world_change = on_world_change
        self._on_exit = on_exit
        self._session_started = False
        self._last_user_text = ""
        self._last_assistant_text = ""
        self._world = self.cfg.get("world") or "cowork"
        self._model = self.cfg.get("model")

    def compose(self) -> ComposeResult:
        with Container(id="shell"):
            with Static(id="panel"):
                with Static(id="inner"):
                    yield Static(self._logo(0), id="left")
                    yield Static(self._right(), id="right")
                yield Static(self._stars(0), id="stars")
                yield Static(self._meta(), id="meta")
            yield VerticalScroll(id="output")
            with Container(id="composer"):
                yield Static("", id="status")
                yield Static(Text("✦", justify="center"), id="input-star")
                yield Input(placeholder="Ask NX anything", id="prompt")
                yield Static(Text(self._context_text(), justify="right"), id="context")

    def on_mount(self):
        self._seed_output()
        self.query_one(Input).focus()
        self._update_context()
        self.set_interval(0.02, self._drain_events)
        self.set_interval(0.055, self._tick)
        if self._on_start and not self._session_started:
            self._session_started = True
            try:
                self._on_start()
            except Exception:
                pass

    def on_unmount(self):
        if self._on_exit:
            try:
                self._on_exit()
            except Exception:
                pass

    def on_key(self, event: events.Key):
        if event.key == "ctrl+c":
            event.stop()
            self.exit()

    def _tick(self):
        self._t += 1
        self._sf = (self._sf + 1) % 60
        self._tip_tick += 1
        try:
            if self._tip_tick >= 140:
                self._tip_tick = 0
                self._tip_set = (self._tip_set + 1) % len(self.TIPS)
                self.query_one("#right", Static).update(self._right())
            self.query_one("#left", Static).update(self._logo(self._t))
            self.query_one("#stars", Static).update(self._stars(self._sf))
        except NoMatches:
            return

    def _seed_output(self):
        return

    def _append_message(self, role, text):
        block = MessageBlock(role, text)
        output = self.query_one("#output", VerticalScroll)
        output.mount(block)
        self._scroll_output_end()
        return block

    def _scroll_output_end(self):
        self.query_one("#output", VerticalScroll).scroll_end(animate=False)

    def _sync_assistant_block(self):
        if self._assistant is None:
            return
        self._assistant.set_text(self._assistant_text)
        self._scroll_output_end()

    def _set_status(self, text):
        self.query_one("#status", Static).update(text)

    def _show_activity(self):
        self._set_status(Text("✦", justify="center", style="rgb(120,98,44)"))

    def _clear_status(self):
        self._set_status("")

    def _context_text(self):
        tokens = sum(len(m.get("content", "")) for m in self._messages) // 4
        pct = min(100, int(tokens * 100 / self.CONTEXT_LIMIT))
        return f"context window {pct}%"

    def _update_context(self):
        self.query_one("#context", Static).update(Text(self._context_text(), justify="right"))

    def _logo(self, tick):
        from rich.text import Text

        version = self.cfg.get("_version", "0.3.50")
        width, height = 20, 10
        cx, cy = 9, 5
        grid = [[" "] * width for _ in range(height)]
        brightness = [[0.0] * width for _ in range(height)]
        speed = 0.025
        tail_length = 22

        def lemniscate_horizontal(theta):
            sine, cosine = math.sin(theta), math.cos(theta)
            denom = 1 + sine * sine
            return cx + 8 * cosine / denom, cy + 4 * sine * cosine / denom

        def lemniscate_vertical(theta):
            sine, cosine = math.sin(theta), math.cos(theta)
            denom = 1 + sine * sine
            return cx + 3 * sine * cosine / denom, cy + 8 * cosine / denom

        paths = [
            (lemniscate_horizontal, 0, speed),
            (lemniscate_horizontal, math.pi, speed),
            (lemniscate_vertical, math.pi / 2, speed * 0.85),
            (lemniscate_vertical, math.pi * 1.5, speed * 0.85),
        ]

        for path_fn, phase, path_speed in paths:
            head = phase + tick * path_speed
            for step in range(tail_length, 0, -1):
                x, y = path_fn(head - step * 0.09)
                xi, yi = int(round(x)), int(round(y))
                glow = ((tail_length - step) / tail_length) ** 1.3 * 0.9
                if 0 <= yi < height and 0 <= xi < width and glow > brightness[yi][xi]:
                    brightness[yi][xi] = glow
                    grid[yi][xi] = "."

        n_left, n_top, n_height, n_width = cx - 3, 1, height - 2, 6
        for row in range(n_top, n_top + n_height):
            if 0 <= row < height:
                if 0 <= n_left < width:
                    grid[row][n_left] = "▌"
                    brightness[row][n_left] = -1
                if 0 <= n_left + n_width < width:
                    grid[row][n_left + n_width] = "▐"
                    brightness[row][n_left + n_width] = -1
        for step in range(n_height):
            row = n_top + step
            col = n_left + int(n_width * step / n_height)
            if 0 <= row < height and 0 <= col < width:
                grid[row][col] = "░"
                brightness[row][col] = -2
            if 0 <= row < height and 0 <= col + 1 < width:
                grid[row][col + 1] = "░"
                brightness[row][col + 1] = -2

        for path_fn, phase, path_speed in paths:
            hx, hy = path_fn(phase + tick * path_speed)
            xi, yi = int(round(hx)), int(round(hy))
            if 0 <= yi < height and 0 <= xi < width:
                grid[yi][xi] = "✦"
                brightness[yi][xi] = 1.0

        out = Text()
        for row in range(height):
            for col in range(width):
                char = grid[row][col]
                glow = brightness[row][col]
                if char == " ":
                    out.append(" ")
                elif glow == -1:
                    out.append(char, style="rgb(18,14,6)")
                elif glow == -2:
                    out.append(char, style="rgb(28,22,8)")
                else:
                    red = int(45 + 155 * glow)
                    green = int(35 + 129 * glow)
                    blue = int(15 + 59 * glow)
                    out.append(char, style=f"rgb({red},{green},{blue})")
            out.append("\n")

        out.append("\n")
        out.append("Welcome back\n", style="rgb(120,98,44)")
        out.append(f"{self._who}\n", style="#c8a44a bold")
        out.append(f"NX v{version}", style="rgb(80,62,22)")
        return out

    def _right(self):
        from rich.text import Text

        out = Text()
        out.append("TIPS\n", style="#c8a44a bold")
        for text, tone in self.TIPS[self._tip_set]:
            style = "#c8a44a" if tone == "gold" else "rgb(176,150,100)"
            out.append(f"  {text}\n", style=style)
        out.append("\n")
        # WHAT'S LIVE — real, current numbers from the actual config, never
        # fabricated. (Old copy hardcoded "1,000+ skills / 21 operations".)
        worlds, tiers, skills = self._live_caps()
        out.append("WHAT'S LIVE\n", style="#c8a44a bold")
        out.append("  " + str(worlds), style="#c8a44a bold")
        out.append(" worlds  ·  ", style="rgb(176,150,100)")
        out.append(str(tiers), style="#c8a44a bold")
        out.append(" model tiers\n", style="rgb(176,150,100)")
        if skills > 0:
            out.append("  " + f"{skills:,}", style="#c8a44a bold")
            out.append(" skills loaded\n", style="rgb(176,150,100)")
        out.append("  ", style="rgb(176,150,100)")
        out.append("Plan First", style="#c8a44a bold")
        out.append(" — autonomous, reviewable\n", style="rgb(176,150,100)")
        out.append("  BYOK or Nexplora credits", style="rgb(176,150,100)")
        return out

    def _live_caps(self):
        """Real capability counts — worlds + tiers from the router, skills from
        the import summary. Fails safe to honest minimums; never fabricates."""
        worlds = tiers = 0
        skills = 0
        try:
            import nx_routing as _r
            worlds = len(_r.WORLD_CONFIG)
            tiers = len(_r.TIERS_BY_PROVIDER.get(_r.PRIMARY_PROVIDER, {}))
        except Exception:
            pass
        try:
            import nx_skills_import as _s
            skills = int((_s.skills_summary() or {}).get("total", 0) or 0)
        except Exception:
            pass
        return worlds, tiers, skills

    def _stars(self, frame):
        from rich.text import Text

        slots = 58
        trail = ["✦", "✧", "·", " "]
        trail_brightness = [1.0, 0.65, 0.35, 0.0]
        orbits = [" "] * slots
        brightness = [0.0] * slots
        for index in range(3):
            head = (frame + index * (slots // 3)) % slots
            for trail_index, char in enumerate(trail):
                pos = (head - trail_index) % slots
                orbits[pos] = char
                brightness[pos] = trail_brightness[trail_index]
        out = Text()
        for index in range(slots):
            char = orbits[index]
            glow = brightness[index]
            if char == " " or glow == 0:
                out.append(" ")
            else:
                red = int(5 + 195 * glow)
                green = int(5 + 159 * glow)
                blue = int(5 + 69 * glow)
                out.append(char, style=f"rgb({red},{green},{blue})")
        return out

    def _meta(self):
        from rich.text import Text

        version = self.cfg.get("_version", "0.3.50")
        out = Text()
        for label, value in (
            ("Model    ", "Nexplora model layer"),
            ("Version  ", f"NX v{version}"),
            ("World    ", self._world or "cowork"),
            ("Directory", os.getcwd()),
        ):
            out.append(f"  {label}  ", style="rgb(80,62,22)")
            out.append(f"{value}\n", style="#c8a44a")
        return out

    def _update_meta(self):
        try:
            self.query_one("#meta", Static).update(self._meta())
        except NoMatches:
            pass

    def on_input_submitted(self, event: Input.Submitted):
        text = event.value.strip()
        event.input.value = ""
        if not text:
            return
        if self._streaming:
            self._append_message("system", "Wait for NX to finish responding.")
            return
        if text.startswith("/"):
            self._handle_command(text)
            return
        self._messages.append({"role": "user", "content": text})
        self._last_user_text = text
        self._append_message("user", text)
        if self._on_user_message:
            try:
                self._on_user_message(text, self._world, self._model)
            except TypeError:
                # backward compatibility with callbacks that only accept text
                try:
                    self._on_user_message(text)
                except Exception:
                    pass
            except Exception:
                pass
        self._update_context()
        self._assistant = self._append_message("assistant", "")
        self._assistant_text = ""
        self._streaming = True
        event.input.disabled = True
        self._show_activity()
        payload = list(self._messages)
        thread = threading.Thread(target=self._stream_worker, args=(payload,), daemon=True)
        thread.start()

    def _handle_command(self, raw):
        cmd = raw.split()[0].lower()
        if cmd in ("/exit", "/quit"):
            self.exit()
            return
        if cmd == "/help":
            self._append_message("system", "Commands\n" + "\n".join(self._help_lines))
            return
        if cmd == "/clear":
            self._messages = [{"role": "system", "content": self._load_system_prompt()}]
            output = self.query_one("#output", VerticalScroll)
            output.remove_children()
            self._seed_output()
            self._update_context()
            self._clear_status()
            return
        if cmd == "/save":
            if self._on_save_command:
                result = self._on_save_command(raw[len(cmd):].strip(), self._last_assistant_text, self._world)
                path = result.get("path") if isinstance(result, dict) else None
            else:
                path = self._save_session(self._messages)
            self._append_message("system", f"saved -> {path}" if path else "save failed")
            self._clear_status()
            return
        if cmd == "/mode":
            parts = raw.split()
            if len(parts) > 1:
                try:
                    from nx_prompts import normalize_mode as _nm
                    mode = _nm(parts[1])
                except Exception:
                    mode = parts[1].upper()
                self.cfg["voice_override"] = mode
                self._append_message("system", f"Mode locked to {mode.title()}")
            else:
                self.cfg.pop("voice_override", None)
                self._append_message("system", "Mode auto-detection restored")
            self._clear_status()
            return
        if self._on_command:
            try:
                response = self._on_command(raw)
            except Exception:
                response = None
            if response is not None:
                self._append_message("system", response)
                self._clear_status()
                return
        if cmd == "/who":
            self._append_message("system", self._who)
            return
        if cmd == "/world":
            name = raw[len(cmd):].strip()
            if name:
                self._world = name
                self.cfg["world"] = name
                if self._on_world_change:
                    try:
                        self._on_world_change(name)
                    except Exception:
                        pass
                self._update_meta()
                self._append_message("system", f"world set to {name}")
            else:
                self._append_message("system", format_worlds_list(self._world))
            return
        if cmd == "/model":
            name = raw[len(cmd):].strip()
            if name:
                self._model = name
                self.cfg["model"] = name
                self._append_message("system", f"model set to {name}")
            else:
                self._append_message("system", f"model: {self._model or 'not set'}")
            return
        if cmd == "/logout":
            self._clear_config()
            self._logout_on_exit = True
            self._append_message("system", "signed out.")
            self.exit()
            return
        self._append_message("error", f"unknown: {cmd} — /help")

    def _stream_worker(self, payload):
        reply = []
        try:
            for chunk in self._stream_chat(payload, self.cfg):
                for char in chunk:
                    reply.append(char)
                    self._events.put(("delta", char))
            self._events.put(("done", "".join(reply)))
        except PermissionError:
            self._events.put(("auth", "Session expired. Run `nx login`."))
        except requests.RequestException as exc:
            self._events.put(("error", f"Gateway error: {exc}"))

    def _finish_stream(self):
        self._streaming = False
        prompt = self.query_one(Input)
        prompt.disabled = False
        prompt.focus()
        self._clear_status()

    def _drain_events(self):
        changed = False
        while True:
            try:
                kind, payload = self._events.get_nowait()
            except queue.Empty:
                break
            if kind == "delta":
                self._assistant_text += payload
                changed = True
            elif kind == "done":
                if not payload:
                    self._assistant_text = "(no response)"
                    changed = True
                else:
                    self._assistant_text = payload
                self._sync_assistant_block()
                self._messages.append({"role": "assistant", "content": payload})
                self._last_assistant_text = payload or self._assistant_text
                if self._on_assistant_message:
                    try:
                        self._on_assistant_message(payload or self._assistant_text, self._world, self._model)
                    except TypeError:
                        try:
                            self._on_assistant_message(payload or self._assistant_text)
                        except Exception:
                            pass
                    except Exception:
                        pass
                self._update_context()
                self._finish_stream()
            elif kind == "auth":
                if self._assistant_text:
                    self._sync_assistant_block()
                self._append_message("error", payload)
                self._finish_stream()
            elif kind == "error":
                if self._assistant_text:
                    self._sync_assistant_block()
                else:
                    self._assistant_text = "response interrupted"
                    self._sync_assistant_block()
                self._append_message("error", payload)
                self._finish_stream()
        if changed:
            self._sync_assistant_block()
