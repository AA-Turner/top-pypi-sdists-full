"""
nx_terminal.py v5
Gold top bar. True black. Bright white text. Professional.
Zero background ANSI codes.
"""
import sys, os, re, shutil, threading, time

try:
    from nx_routing import WORLD_CONFIG
except Exception:
    WORLD_CONFIG = None

GOLD   = "\033[38;2;200;164;74m"
GOLDD  = "\033[38;2;196;162;88m"
GOLDK  = "\033[38;2;60;46;8m"
WHITE  = "\033[38;2;224;221;212m"
WHITD  = "\033[38;2;186;183;172m"
DIM    = "\033[38;2;172;166;148m"
DIMR   = "\033[38;2;146;140;122m"
DIMMR  = "\033[38;2;132;126;110m"
GREEN  = "\033[38;2;80;200;100m"
RED    = "\033[38;2;220;80;70m"
RESET  = "\033[0m"
BOLD   = "\033[1m"
CLEAR  = "\033[2J\033[H"

def clear_screen():
    sys.stdout.write(CLEAR)
    sys.stdout.flush()

def _w():
    return min(shutil.get_terminal_size().columns, 96)

def _s(t):
    return re.sub(r'\033\[[0-9;]*m','',t)

def _p(t, n):
    return t + ' ' * max(0, n - len(_s(t)))

def _mask_email(email: str) -> str:
    """Mask an email for on-screen display so screen-shares / demos don't
    leak the operator's address. `vnstraders777@gmail.com` → `v…@gmail.com`.
    Non-email strings (like a phone or empty) pass through unchanged."""
    if not email or "@" not in email:
        return email or ""
    local, _, domain = email.partition("@")
    if not local:
        return email
    if len(local) <= 1:
        return f"{local}…@{domain}"
    return f"{local[0]}…@{domain}"


def _track(s: str) -> str:
    """Letter-spaced caps for eyebrow labels — the small tracked tag that reads
    'considered' rather than 'default'. 'Start' -> 'S T A R T'."""
    return " ".join(s.upper())


def print_welcome(email, version, world="cowork", connected=None, agents=None):
    w = _w()
    sys.stdout.write("\033[2J\033[H")
    masked = _mask_email(email)
    # Real counts — worlds + model tiers from the actual router config.
    _worlds = _tiers = 0
    try:
        import nx_routing as _r
        _worlds = len(_r.WORLD_CONFIG)
        _tiers = len(_r.TIERS_BY_PROVIDER.get(_r.PRIMARY_PROVIDER, {}))
    except Exception:
        pass

    pad = "  "
    inner = max(36, w - 4)          # framed content width
    narrow = w < 76                 # split-pane / small terminal → single column
    GCHIP = "\033[48;2;200;164;74m\033[38;2;14;11;5m"  # gold chip: dark ink on gold

    # LIVE footprint — the operator's live account state, COUNTS ONLY (never the lists):
    # connected integrations + agents on the account. Each part shows only when its count
    # resolved (agents is a bounded server lookup the caller may skip on a slow network).
    _dot = f"   {DIMMR}·{RESET}   "
    _fp_bits = []
    if connected is not None:
        _fp_bits.append(f"{WHITE}{connected}{RESET}{DIM} connected{RESET}")
    if agents is not None:
        _fp_bits.append(f"{WHITE}{agents}{RESET}{DIM} agent{'' if agents == 1 else 's'}{RESET}")
    footprint = _dot.join(_fp_bits)                                   # colored, "" if none

    print()
    # ── Brand lockup: the gold NX chip + NEXPLORA wordmark on ONE clean prominent line
    # across the top. No world / version / "AI Operating System" clutter — just NX · Nexplora
    # (letter-spaced when there's room so it has presence without being over-sized).
    wordmark = "NEXPLORA" if narrow else _track("Nexplora")
    print(f"{pad}{GCHIP} NX {RESET}   {WHITE}{wordmark}{RESET}")
    print()
    print(f"{pad}{GOLDK}{'─' * inner}{RESET}")
    print()

    if narrow:
        # Single-column, stacked — fits ~48 cols, never overflows.
        print(f"{pad}{GOLDD}START{RESET}")
        print(f"{pad}{WHITE}Type your task to start{RESET}")
        print(f"{pad}{DIM}/help  /mode  /model  /council{RESET}")
        print(f"{pad}{DIM}/integrations  /skills  $brain  $council{RESET}")
        print()
        print(f"{pad}{GOLDD}LIVE{RESET}")
        print(f"{pad}{WHITE}{masked}{RESET}")
        if footprint:
            print(f"{pad}{footprint}")
    else:
        colw = (inner - 4) // 2
        rows = [
            (f"{GOLDD}{_track('Start')}{RESET}",                       f"{GOLDD}{_track('Live')}{RESET}"),
            (f"{WHITE}Type your task to start{RESET}",                 f"{WHITE}{masked}{RESET}"),
            (f"{DIM}/help   /mode   /model   /council{RESET}",        footprint),
            (f"{GOLDD}$brain{RESET}{DIM}   save{RESET}    {GOLDD}$council{RESET}{DIM}   debate{RESET}", ""),
            (f"{DIM}/integrations   /skills{RESET}",                   ""),
        ]
        for i, (l, r) in enumerate(rows):
            print(f"{pad}{_p(l, colw)}  {r}")
            if i == 0:
                print()
    print()
    print(f"{pad}{GOLDK}{'─' * inner}{RESET}")
    print()

    # ── Quiet status line — the account now lives in the LIVE block, so keep this minimal ──
    if narrow:
        print(f"{pad}{GREEN}●{RESET} {DIM}ready{RESET}")
    else:
        sep = f"   {DIMMR}·{RESET}   "
        print(
            f"{pad}{GREEN}●{RESET}  {DIM}ready{RESET}"
            f"{sep}{DIM}Nexplora model layer{RESET}"
        )
    print()


def print_user_message(text: str):
    DIM   = "\033[38;2;146;140;122m"
    RESET = "\033[0m"
    print(f"\n  {DIM}{text}{RESET}\n")


# ── Streaming response: tag-aware, indented word-wrap ────────────────────────
# The model interleaves prose with internal tool calls (<nx:read_file/>,
# <nx:run_command/>, ```nx-run blocks, ```file: edits). These arrive token by
# token, so a per-chunk regex can NOT strip them — the opener lands in one
# chunk and the closer in the next, and the match never fires across the
# boundary (that's why raw tags used to leak on screen). This streamer BUFFERS
# across chunks: prose is wrapped + shown live; a tool region is held until it
# completes, then rendered as ONE clean action line ("✦ Read README.md"),
# never the raw syntax.
_current_stream = None

_TAG_OPENERS = ("<nx:read_file", "<nx:run_command", "<nx:write_file", "<nx:mcp", "```nx-run", "```file:",
                "<bash>", "<sh>", "<shell>", "<zsh>", "<console>",
                # bare markdown fences the model uses to RUN commands (Kimi/DeepSeek/Qwen do this
                # constantly). The executor already runs these — streaming must recognize them too,
                # or the raw ```bash block leaks to the screen while the command silently runs.
                "```bash", "```sh", "```shell", "```zsh", "```console", "```shell-session")
_WS = (" ", "\n", "\t")


def _summarize_cmd(cmd: str, limit: int = 72) -> str:
    one = re.sub(r"\s+", " ", (cmd or "").strip())
    return one if len(one) <= limit else one[: limit - 1].rstrip() + "…"


def _basename(p: str) -> str:
    p = (p or "").strip().strip('"').strip("'")
    return p.rsplit("/", 1)[-1] if "/" in p else p


class _NxStream:
    __slots__ = ("buf", "started", "block_started", "col", "width", "indent", "prefix_len")

    def __init__(self):
        self.buf = ""
        self.started = False
        self.block_started = False  # has the current prose block emitted its ✦?
        self.col = 0                # 0 = at line start (prefix/indent not yet written)
        self.width = max(40, _w() - 2)
        self.indent = "     "
        self.prefix_len = 5

    def start(self):
        # Prefix is written lazily (on first prose / action), so a tool-call-only
        # turn never shows a dangling "✦" with nothing after it.
        self.started = True

    def write(self, text: str, final: bool = False):
        self.started = True
        self.buf += text
        self._drain(final)

    # ── tag scanning ─────────────────────────────────────────────────────────
    def _earliest_opener(self):
        best, kind = None, None
        for m in _TAG_OPENERS:
            i = self.buf.find(m)
            # A ```lang fence opener (except ```file: whose ':' already anchors it) must end
            # at a word boundary, so "```bash" matches ```bash but NOT ```bashrc / ```shellcheck
            # / ```zshrc — those are OTHER languages the executor won't run; suppressing them
            # would make documented code vanish. Skip past any non-boundary match.
            while i != -1 and m.startswith("```") and not m.endswith(":"):
                nxt = self.buf[i + len(m): i + len(m) + 1]
                if nxt and (nxt.isalnum() or nxt in "-_"):
                    i = self.buf.find(m, i + 1)  # this was ```bashrc etc — keep looking
                    continue
                break
            if i != -1 and (best is None or i < best):
                best, kind = i, m
        return best, kind

    def _region_end(self, kind):
        b = self.buf
        if kind.startswith("<nx:"):
            sc = b.find("/>")
            bc = b.find("</nx:")
            if sc != -1 and (bc == -1 or sc < bc):
                return sc + 2
            if bc != -1:
                gt = b.find(">", bc)
                return gt + 1 if gt != -1 else None
            return None
        if kind in ("<bash>", "<sh>", "<shell>", "<zsh>", "<console>"):
            # a plain <bash>…</bash> the model invents — closes at its matching tag
            close = "</" + kind[1:]                     # "<bash>" → "</bash>"
            bc = b.find(close)
            if bc == -1:
                return None
            end = bc + len(close)
            if end < len(b) and b[end] == "\n":
                end += 1
            return end
        # fenced ```nx-run / ```file: — closes at the next ``` after the first line
        nl = b.find("\n")
        if nl == -1:
            return None
        close = b.find("```", nl)
        if close == -1:
            return None
        end = close + 3
        if end < len(b) and b[end] == "\n":
            end += 1
        return end

    def _safe_cut(self):
        # Emit up to the last whitespace; hold the trailing partial token so we
        # never split a word mid-wrap or emit a half-arrived tool marker.
        for i in range(len(self.buf) - 1, -1, -1):
            if self.buf[i] in _WS:
                return i + 1
        return 0

    def _drain(self, final=False):
        while self.buf:
            idx, kind = self._earliest_opener()
            if idx is None:
                cut = len(self.buf) if final else self._safe_cut()
                if cut <= 0:
                    return
                self._emit_prose(self.buf[:cut])
                self.buf = self.buf[cut:]
                return
            if idx > 0:
                self._emit_prose(self.buf[:idx])
                self.buf = self.buf[idx:]
                continue
            end = self._region_end(kind)
            if end is None:
                if final:
                    self.buf = ""  # incomplete tool region at EOF — drop, never raw
                return
            region, self.buf = self.buf[:end], self.buf[end:]
            self._emit_action(kind, region)

    # ── emission ───────────────────────────────────────────────────────────────
    def _line_start(self):
        if self.col == 0:
            if not self.block_started:
                sys.stdout.write(f"  {GOLD}✦{RESET}  ")
                self.block_started = True
            else:
                sys.stdout.write(self.indent)
            self.col = self.prefix_len

    def _emit_prose(self, text):
        # Secondary net for any tag form the openers don't model (<invoke>, etc.).
        text = _strip_user_visible_tool_tags(text)
        if not text:
            return
        # Prose discipline: NX defaults to prose, so strip stray markdown emphasis
        # that renders as literal junk in a terminal — "**bold**" -> "bold",
        # leading "## Header" -> "Header". (Numbered lists + single * for math
        # are left intact; "__" is left alone so code like __init__ survives.)
        text = text.replace("**", "")
        text = re.sub(r"(?m)^\s{0,3}#{1,6}\s+", "", text)
        parts = text.split("\n")
        for i, line in enumerate(parts):
            if line:
                self._write_words(line)
            if i < len(parts) - 1:
                sys.stdout.write("\n")
                self.col = 0
        sys.stdout.flush()

    def _suppress_region(self):
        # Consume a tool region without printing anything (runs + package installs are
        # rendered by the EXECUTOR as a Ran/└ block). The region was already sliced out of
        # the buffer in _drain, so nothing leaks; we only normalize line/block state here.
        if self.col > 0:
            sys.stdout.write("\n")
        self.col = 0
        self.block_started = False  # next prose opens a fresh ✦ block
        sys.stdout.flush()

    def _emit_action(self, kind, region):
        if kind in ("<nx:run_command", "```nx-run", "<bash>", "<sh>", "<shell>", "<zsh>", "<console>",
                    "```bash", "```sh", "```shell", "```zsh", "```console", "```shell-session"):
            # A run is rendered by the EXECUTOR as a "Ran <cmd>" / "└ <output>" block —
            # the command AND its real result together, after it actually runs. Streaming
            # only CONSUMES the region here (the slice in _drain already happened, so no
            # raw tag can leak); it prints nothing, so the command never appears twice and
            # a ```bash example that never runs is never mislabelled "Ran".
            self._suppress_region()
            return
        if kind == "<nx:mcp":
            srv = re.search(r'server\s*=\s*["\']([^"\']+)["\']', region)
            if not srv:
                # a malformed <nx:mcp> with no server= — NEVER render the bare "Using
                # integration" line (that was the photo-2 leak). The executor prints the
                # real ↪ result line for the call; suppress the streaming action here.
                self._suppress_region()
                return
            label, detail = "Using", srv.group(1).replace("-", " ").title()
        elif kind == "<nx:read_file":
            m = re.search(r'path\s*=\s*["\']([^"\']+)["\']', region)
            label, detail = "Read", _basename(m.group(1) if m else "")
        elif kind in ("<nx:write_file", "```file:"):
            if kind == "```file:":
                m = re.match(r"```file:\s*([^\n]+)", region)
                detail = _basename(m.group(1).strip() if m else "")
            else:
                m = re.search(r'path\s*=\s*["\']([^"\']+)["\']', region)
                detail = _basename(m.group(1) if m else "")
            label = "Edited"
        elif kind in ("<bash>", "<sh>", "<shell>", "<zsh>", "<console>"):
            # plain <bash>…</bash> the model invents → the same clean "Ran <cmd>" line
            inner = region[len(kind):]
            inner = re.sub(r"</(?:bash|sh|shell|zsh|console)\s*>\s*$", "", inner, flags=re.I)
            label, detail = "Ran ", _summarize_cmd(inner)
        else:  # <nx:run_command or ```nx-run
            if kind == "```nx-run":
                body = region.split("\n", 1)[1] if "\n" in region else ""
                body = body.rsplit("```", 1)[0]
                detail = _summarize_cmd(body)
            else:
                m = re.search(r'cmd\s*=\s*"([^"]*)"', region) or re.search(r"cmd\s*=\s*'([^']*)'", region)
                detail = _summarize_cmd(m.group(1) if m else "")
            label = "Ran "
        if self.col > 0:
            sys.stdout.write("\n")
            self.col = 0
        # tree/codex style — a clean past-tense action line, no per-action ✦ (the executor's
        # ⌐ line shows the result right under it). Reads/edits/runs all read the same.
        sys.stdout.write(f"  {GOLDD}{label.strip()}{RESET}  {WHITE}{detail}{RESET}\n")
        self.block_started = False  # next prose opens a fresh ✦ block
        self.col = 0
        sys.stdout.flush()

    def _write_words(self, line: str):
        for token in re.finditer(r"\S+|\s+", line):
            text = token.group(0)
            if text.isspace():
                if self.col <= self.prefix_len:  # drop leading ws at a line start
                    continue
                if self.col + len(text) > self.width:
                    sys.stdout.write("\n")
                    self.col = 0
                    continue
                sys.stdout.write(text)
                self.col += len(text)
                continue
            visible = len(_s(text))
            if self.col > self.prefix_len and self.col + visible > self.width:
                sys.stdout.write("\n")
                self.col = 0
            self._line_start()
            sys.stdout.write(text)
            self.col += visible
        sys.stdout.flush()

    def finish(self):
        self._drain(final=True)
        if self.started and self.col > 0:
            sys.stdout.write("\n")
        self.col = 0
        self.started = False
        sys.stdout.flush()


def print_nx_start():
    global _current_stream
    _current_stream = _NxStream()
    _current_stream.start()


_TOOL_TAG_RE = None


def _strip_user_visible_tool_tags(chunk: str) -> str:
    """Strip internal tool-tag syntax from chunks before showing the user.

    The agentic executor still parses the assistant turn for `<nx:...>` tags
    after streaming completes; this only affects what the user *sees*.
    """
    global _TOOL_TAG_RE
    if _TOOL_TAG_RE is None:
        import re as _re
        # Hide tool tags from the user. The agentic loop parses them after
        # streaming completes; this only affects what's shown on screen.
        _TOOL_TAG_RE = _re.compile(
            r"```(?:nx-run|bash|sh|shell|zsh|console|shell-session)\s*\n.*?\n```|"
            r"<nx:run_command\b[^>]*?(?:/>|>.*?</nx:run_command>)|"
            r"<nx:run\b[^>]*?/?>|"
            r"<nx:read_file\s+[^>]*?/>|"
            r"<nx:write_file\s+[^>]*?/>|"
            r"<nx:mcp\s+[^>]*?/>|"
            r"<nx:health\s*/>|"
            # Internal markers / malformed tool-call ECHOES — the model drifts the
            # call syntax endlessly ([MCP …], [nx:mcp …], [nx:run: …], «nx:mcp tool="…"…»,
            # «ran …»), so strip GENERICALLY: any «…» (guillemets are NX-internal, never
            # legit prose), and any [ … ] / < … > wrapper that mentions mcp/health/cmd/run.
            r"«[^»\n]{0,400}»|"
            r"\[\s*(?:nx:)?(?:mcp|health|cmd)\b[^\]\n]{0,400}\]|"
            r"\[\s*nx:run\b[^\]\n]{0,400}\]|"
            r"<\s*nx:mcp\b[^>\n]{0,400}>|"
            r"<invoke[\s>][^<]*?</invoke>|"
            r"<tool_call>.*?</tool_call>",
            _re.DOTALL | _re.IGNORECASE,
        )
    return _TOOL_TAG_RE.sub("", chunk)


def print_nx_chunk(chunk):
    # Pass the RAW chunk — the stream buffers across chunk boundaries and renders
    # tool calls as clean action lines itself. (Pre-stripping here was the bug:
    # the regex needs a complete tag, but tags arrive split across chunks.)
    global _current_stream
    if _current_stream is None:
        _current_stream = _NxStream()
    _current_stream.write(chunk)


def print_nx_end():
    global _current_stream
    if _current_stream is not None:
        _current_stream.finish()
        _current_stream = None


class _ThinkingStopper:
    def __init__(self, stop, done):
        self._stop = stop
        self._done = done

    def set(self):
        self._stop.set()
        self._done.wait(timeout=2)


class esc_watch:
    """Context manager active ONLY during model streaming: watch stdin for a lone ESC and,
    on esc, raise KeyboardInterrupt in the MAIN thread (via _thread.interrupt_main) so ESC
    aborts the turn through the SAME path Ctrl-C uses. Uses cbreak (NOT raw) so Ctrl-C keeps
    signalling. Fully fail-safe: if the tty can't be driven the watcher is a silent no-op
    (Ctrl-C still works), and the terminal mode is ALWAYS restored on exit — the `with`
    guarantees __exit__ runs even as the KeyboardInterrupt we raise unwinds through it, so
    the terminal can never be left in cbreak."""

    def __init__(self):
        self._fd = None
        self._saved = None
        self._stop = threading.Event()
        self._thread = None

    def __enter__(self):
        try:
            import termios, tty
            if not (sys.stdin.isatty() and sys.stdout.isatty()):
                return self
            self._fd = sys.stdin.fileno()
            self._saved = termios.tcgetattr(self._fd)
            tty.setcbreak(self._fd)   # ICANON+ECHO off → esc byte readable; ISIG on → Ctrl-C still signals
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        except Exception:
            self._restore()           # any setup failure → no watcher, tty restored
        return self

    def _run(self):
        import os as _os, select, _thread
        try:
            while not self._stop.is_set():
                try:
                    r, _, _ = select.select([sys.stdin], [], [], 0.15)
                except Exception:
                    return
                if not r:
                    continue
                try:
                    ch = _os.read(self._fd, 1)
                except Exception:
                    return
                if ch == b"\x1b":
                    # A lone ESC = stop. An escape SEQUENCE (arrow keys send \x1b[A, etc.)
                    # has more bytes waiting — drain and ignore those so arrows don't abort.
                    try:
                        r2, _, _ = select.select([sys.stdin], [], [], 0.03)
                    except Exception:
                        r2 = None
                    if r2:
                        try:
                            _os.read(self._fd, 16)
                        except Exception:
                            pass
                        continue
                    self._stop.set()
                    _thread.interrupt_main()
                    return
                # any other byte during streaming is discarded (the operator shouldn't be typing)
        except Exception:
            pass

    def _restore(self):
        try:
            import termios
            if self._fd is not None and self._saved is not None:
                termios.tcsetattr(self._fd, termios.TCSADRAIN, self._saved)
        except Exception:
            pass

    def __exit__(self, *exc):
        self._stop.set()
        try:
            if self._thread is not None:
                self._thread.join(timeout=0.3)
        except Exception:
            pass
        self._restore()
        return False


def print_nx_thinking():
    """
    A LIVE in-flight indicator so a slow model call never looks frozen: a moving
    glyph, a rotating word, and an elapsed-seconds counter — "✦ thinking… (12s ·
    esc to interrupt)" — updated in place. Returns a stopper; call .set() when the
    first response token arrives.
    """
    import os as _os
    import shutil as _shutil
    stop = threading.Event()
    done = threading.Event()
    start = time.time()

    GOLD     = "\033[38;2;200;164;74m"
    GOLD_MID = "\033[38;2;176;150;100m"
    DIM      = "\033[38;2;172;166;148m"
    RESET    = "\033[0m"
    GLYPHS   = [(GOLD, "✦"), (GOLD_MID, "✧")]        # a gentle breath
    PHRASES  = ["thinking", "working", "still on it", "reasoning", "cooking"]

    try:
        is_tty = sys.stdout.isatty()
    except Exception:
        is_tty = False
    # Redraw in place ONLY on a terminal KNOWN to honor `\r` overwrite — the standard
    # xterm-family TERMs, which includes Codespaces / VS Code (TERM=xterm-256color; the
    # welcome panel already redraws there via \r\033[K). Any other/unknown/dumb TERM might
    # NOT honor \r (an in-place loop would then STACK a fresh line every tick — the flood
    # the old static line guarded against), so it gets a throttled append heartbeat that
    # prints at most every 15s: motion everywhere, a flood nowhere.
    _term = _os.environ.get("TERM", "")
    _rcap = any(_term.startswith(p) for p in (
        "xterm", "screen", "tmux", "vt1", "vt2", "rxvt", "linux", "ansi",
        "alacritty", "kitty", "wezterm", "foot", "st-", "eterm", "putty"))
    animated = is_tty and _rcap

    def _termw():
        # Actual panel width. A narrow Codespace/VS Code panel is the case that bit us:
        # a line WIDER than the panel wraps to a 2nd physical row, and \r\033[2K can only
        # clear the row the cursor is on — the wrapped remainder survives and every frame
        # stacks a fresh line (the "7 duplicates" flood). Keeping the line inside the width
        # is what makes the in-place redraw actually redraw in one place.
        try:
            w = _shutil.get_terminal_size((80, 24)).columns
            return w if isinstance(w, int) and w > 0 else 80
        except Exception:
            return 80

    if animated:
        def run():
            i = 0
            try:
                while not stop.wait(1.0 if i else 0.0):     # first frame now, then 1/sec (calm)
                    el = int(time.time() - start)
                    gc, gl = GLYPHS[i % 2]
                    ph = PHRASES[(el // 4) % len(PHRASES)]
                    w = _termw()
                    core = f"{ph}… {el}s"                    # short: fits even a ~24-col panel
                    hint = " · esc or ⌃C to stop"
                    # "  ✦  " is 5 visible cols; a dingbat glyph can measure 2, so budget 6.
                    body = core + hint if (6 + len(core) + len(hint)) <= w - 1 else core
                    cap = max(1, w - 1 - 6)
                    if len(body) > cap:                      # hard guard: never reach the width
                        body = body[:cap]
                    prefix = "\n" if i == 0 else "\r\033[2K"
                    sys.stdout.write(f"{prefix}  {gc}{gl}{RESET}  {DIM}{body}{RESET}")
                    sys.stdout.flush()
                    i += 1
                sys.stdout.write("\r\033[2K")
                sys.stdout.flush()
            except Exception:
                pass
            finally:
                done.set()                                  # never leave .set() hanging
    else:
        def run():
            try:
                sys.stdout.write(f"\n  {GOLD}✦{RESET}  {DIM}working… (esc to interrupt){RESET}\n")
                sys.stdout.flush()
                last = 0
                while not stop.wait(1.0):
                    el = int(time.time() - start)
                    if el - last >= 15:                     # a beat every 15s, never a flood
                        last = el
                        sys.stdout.write(f"  {DIM}… still working ({el}s){RESET}\n")
                        sys.stdout.flush()
            except Exception:
                pass
            finally:
                done.set()

    threading.Thread(target=run, daemon=True).start()
    return _ThinkingStopper(stop, done)


def print_world_change(world):
    w = _w()
    print(f"\n  {GOLDD}· worlds → {GOLD}{world}{RESET}\n")


def _available_worlds():
    worlds = sorted(WORLD_CONFIG.keys()) if WORLD_CONFIG else ["cowork"]
    return worlds


def format_worlds_list(active_world):
    worlds = _available_worlds()
    lines = [f"\n  {GOLDD}Available worlds:{RESET}"]
    for world in worlds:
        marker = f"{GOLD}✦{RESET}" if world == active_world else f"{DIMMR}·{RESET}"
        lines.append(f"    {marker}  {WHITE}{world}{RESET}")
    lines.append("")
    return "\n".join(lines)


def print_worlds_list(active_world):
    print(format_worlds_list(active_world))


def print_mode_change(mode):
    print(f"\n  {GOLDD}· mode → {GOLD}{mode}{RESET}\n")


def print_connect_success(service, tools):
    print(f"\n  {GREEN}✦{RESET}  {WHITE}{service}{RESET}  {DIM}connected  ·  {tools} tools{RESET}\n")


def print_error(msg):
    print(f"\n  {RED}·{RESET}  {DIM}{msg}{RESET}\n")


def print_save_confirm(path):
    print(f"\n  {GREEN}✦ saved → {path}{RESET}\n")


def print_footer():
    w = _w()
    print(f"{GOLDK}{'─' * w}{RESET}")
    # Live status bar — real worlds/tiers/skills, no fabricated "42 skills /
    # 46 integrations". Skills shown only when actually loaded.
    _worlds = _tiers = _skills = 0
    try:
        import nx_routing as _r
        _worlds = len(_r.WORLD_CONFIG)
        _tiers = len(_r.TIERS_BY_PROVIDER.get(_r.PRIMARY_PROVIDER, {}))
    except Exception:
        pass
    try:
        import nx_skills_import as _sk
        _skills = int((_sk.skills_summary() or {}).get("total", 0) or 0)
    except Exception:
        pass
    items = [
        f"{DIMMR}✦ {RESET}{DIMR}{_worlds} worlds{RESET}",
        f"{DIMMR}◇ {RESET}{DIMR}{_tiers} model tiers{RESET}",
    ]
    if _skills > 0:
        items.append(f"{DIMMR}$ {RESET}{DIMR}{_skills} skills{RESET}")
    right = f"{DIMMR}NX  ·  Nexplora AI Operating System{RESET}"
    row = "  " + "    ".join(items)
    gap = max(1, w - len(_s(row)) - len(_s(right)) - 1)
    print(f"{row}{' ' * gap}{right}\n")


def print_status_bar(world: str):
    """Print once at bottom. Never inside message loop."""
    DIM   = "\033[38;2;150;144;128m"
    GOLD  = "\033[38;2;200;164;74m"
    RESET = "\033[0m"
    try:
        cols = os.get_terminal_size().columns
    except Exception:
        cols = 80
    w = min(cols, 96)
    left  = f"  {GOLD}{world}{RESET}"
    right = f"{DIM}NX{RESET}  "
    gap   = max(1, w - len(_s(left)) - len(_s(right)))
    print(f"{left}{' ' * gap}{right}")


def print_confirm_prompt(text):
    try: return input(f"  {GOLDD}{text}{RESET} ").strip().lower()
    except: return "n"


def print_secure_prompt(label):
    import getpass
    try: return getpass.getpass(f"  {GOLDD}{label}{RESET} ")
    except: return ""


def get_input(world, voice="auto"):
    try: return input(f"  {GOLD}{world}{RESET}  {GOLDD}›{RESET}  ").strip()
    except: return "/exit"


# ── Backwards-compatible names used by nx_cli.py and existing tests ───────────
NX_SYMBOL = f"{GOLD}✦{RESET}"
SEPARATOR = f"{GOLDK}{'─' * _w()}{RESET}"

def stream_nx_response(text, voice="PARTNER"):
    """Stream a complete NX response with a gold prefix (legacy helper)."""
    sys.stdout.write(f"  {NX_SYMBOL}  {WHITE}")
    words = text.split(" ")
    for i, word in enumerate(words):
        sys.stdout.write(word)
        if i < len(words) - 1:
            sys.stdout.write(" ")
            time.sleep(0.008)
    sys.stdout.write(f"{RESET}\n\n")
    sys.stdout.flush()


def print_key_status(slots):
    print(f"\n  {GOLD}key pool{RESET}")
    for s in slots:
        locked = f"{RED}locked{RESET}" if s["locked"] else f"{GREEN}active{RESET}"
        print(f"  {DIM}key {s['slot']}  {s['requests_this_minute']} req/min  {locked}{RESET}")
    print()


def print_vpn_status(status):
    if not status.get("available"):
        reason = status.get("reason") or "vpn not configured"
        print(f"\n  {DIM}{reason}{RESET}\n")
    else:
        print(f"\n  {GOLD}vpn{RESET}  {DIM}{status.get('output', '')}{RESET}\n")


def print_separator():
    print(f"\n  {SEPARATOR}\n")


start_nx_response = print_nx_start
stream_nx_chunk = print_nx_chunk
end_nx_response = print_nx_end
