"""Arguments of the Matrx 2 desktop tools (ops of ``@ai-matrx/desktop-protocol``).

Each field mirrors the op's params schema; the tool's ``tool.definition.parameters`` row is this
model, held equal by the drift gate and by test_desktop_tools.py.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field

from matrx_ai.tools.declared import ToolArgs

#: A list of names (aliased so a model with a field named ``list`` can still say it).
NameList = list[str]


class DesktopTranscribeArgs(ToolArgs):
    path: str = Field(
        description="The audio or video file on the user's computer (absolute, or relative to its home folder)."
    )
    model: Literal["tiny", "base", "small", "large-v3-turbo"] | None = Field(
        default=None,
        description="Whisper size: tiny is fastest, large-v3-turbo most accurate. Omit for the computer's default.",
    )
    language: str | None = Field(
        default=None,
        description="Spoken language as an ISO 639-1 code such as en or es. Omit to detect it.",
    )
    task: Literal["transcribe", "translate"] = Field(
        default="transcribe",
        description="transcribe keeps the spoken language; translate writes English.",
    )


class DesktopProcessArgs(ToolArgs):
    action: Literal["list", "ports", "kill"] = Field(
        description="list: running processes; ports: listening ports and the process on each; kill: stop one by pid.",
    )
    name: str | None = Field(
        default=None,
        description="list: only processes whose name or command line contains this text.",
    )
    sort: Literal["cpu", "memory", "pid", "name"] = Field(
        default="cpu", description="list: order, busiest first for cpu and memory."
    )
    limit: int = Field(default=25, ge=1, le=200, description="list: at most this many processes.")
    port: int | None = Field(default=None, ge=1, le=65535, description="ports: only this port.")
    pid: int | None = Field(
        default=None, ge=1, description="kill: the process id, from list or ports."
    )
    force: bool = Field(
        default=False,
        description="kill: end it at once instead of asking it to quit (it cannot save its work).",
    )


class DesktopClipboardArgs(ToolArgs):
    action: Literal["read", "write"] = Field(
        description="read: the clipboard's text; write: replace the clipboard's text."
    )
    text: str | None = Field(default=None, description="write: the text to put on the clipboard.")


class ShellJobArgs(ToolArgs):
    action: Literal["start", "output", "stop", "list"] = Field(
        description=(
            "start: run a command in the background (a dev server, a long build) and get its job_id; "
            "output: read what it printed since `offset`; stop: end it; list: every job."
        ),
    )
    command: str | None = Field(default=None, description="start: the shell command.")
    cwd: str | None = Field(
        default=None,
        description="start: the folder it runs in (absolute, or relative to the home folder).",
    )
    env: dict[str, str] | None = Field(
        default=None, description="start: extra environment variables, name to value."
    )
    job_id: str | None = Field(
        default=None, description="output, stop: the job (from start or list)."
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="output: read from this byte (next_offset of the last read; 0 = from the start).",
    )
    wait_seconds: int = Field(
        default=0,
        ge=0,
        le=25,
        description="output: wait up to this long for new output or the exit when none is waiting.",
    )
    max_bytes: int | None = Field(
        default=None,
        ge=1024,
        le=1048576,
        description="output: at most this many bytes per read (65536 by default).",
    )
    force: bool = Field(
        default=False, description="stop: end it at once instead of asking it to quit."
    )


class DesktopAppsArgs(ToolArgs):
    action: Literal["list", "open"] = Field(
        description="list: the apps Matrx 2 knows and whether each is installed; open: open one or bring it forward.",
    )
    app_key: str | None = Field(default=None, description="open: the app (its app_key from list).")
    profile_id: str | None = Field(
        default=None,
        description="open: one of the app's saved profiles (from list); the default profile when omitted.",
    )


class DesktopSystemArgs(ToolArgs):
    action: Literal["info", "open_url", "open_path", "notify"] = Field(
        description=(
            "info: the computer (OS, user, folders, CPU, memory, battery); open_url: open a link in the "
            "default browser or mail app; open_path: open a file or folder with its default app; notify: "
            "show a notification."
        ),
    )
    url: str | None = Field(default=None, description="open_url: an http, https or mailto link.")
    path: str | None = Field(
        default=None,
        description="open_path: the file or folder (absolute, or relative to the home folder).",
    )
    reveal: bool = Field(
        default=False, description="open_path: show it in Finder or Explorer instead of opening it."
    )
    title: str | None = Field(default=None, description="notify: the notification's title.")
    body: str = Field(default="", description="notify: the notification's text.")


class DesktopScreenArgs(ToolArgs):
    action: Literal["list", "capture"] = Field(
        description="list: the displays; capture: a picture of one display (you see the image).",
    )
    display_id: int | None = Field(
        default=None,
        ge=0,
        description="capture: the display (from list); the main display when omitted.",
    )
    format: Literal["jpeg", "png"] = Field(
        default="jpeg", description="capture: jpeg is smaller; png is exact."
    )
    max_width: int = Field(
        default=1600,
        ge=160,
        le=7680,
        description="capture: scale the picture down to at most this many pixels wide.",
    )


class DesktopWindowArgs(ToolArgs):
    action: Literal["list", "focus", "move", "minimize"] = Field(
        description="list: open windows; focus: bring one to the front; move: move or resize one; minimize: minimize, maximize or restore one.",
    )
    title: str | None = Field(
        default=None, description="list: only windows whose title contains this text."
    )
    app: str | None = Field(
        default=None, description="list: only windows of apps whose name contains this text."
    )
    mode: Literal["minimize", "maximize", "restore"] | None = Field(
        default=None,
        description="minimize: minimize (the default), maximize (fill its display) or restore (bring it back).",
    )
    id: int | None = Field(
        default=None, ge=0, description="focus, move, minimize: the window (its id from list)."
    )
    x: int | None = Field(default=None, description="move: new left edge, in screen points.")
    y: int | None = Field(default=None, description="move: new top edge, in screen points.")
    width: int | None = Field(
        default=None, ge=50, le=16384, description="move: new width, in points."
    )
    height: int | None = Field(
        default=None, ge=50, le=16384, description="move: new height, in points."
    )
    limit: int = Field(default=50, ge=1, le=500, description="list: at most this many windows.")


InputKeyName = Literal[
    "cmd", "ctrl", "alt", "shift", "meta",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9", "f10", "f11", "f12",
    "enter", "tab", "escape", "space", "backspace", "delete",
    "up", "down", "left", "right", "home", "end", "pageup", "pagedown",
    "minus", "equal", "comma", "period", "slash", "semicolon", "quote", "bracketleft", "bracketright", "backslash", "grave",
]  # fmt: skip


class DesktopInputArgs(ToolArgs):
    action: Literal["type_text", "hotkey", "mouse_move", "mouse_click"] = Field(
        description=(
            "type_text: type text into whatever has focus; hotkey: press keys together (cmd is Command on a "
            "Mac, Ctrl elsewhere); mouse_move: move the pointer; mouse_click: click (at x, y when given)."
        ),
    )
    text: str | None = Field(default=None, description="type_text: the text to type.")
    keys: list[InputKeyName] | None = Field(
        default=None,
        description='hotkey: the keys pressed together, modifiers first, such as ["cmd", "shift", "t"].',
    )
    x: int | None = Field(
        default=None,
        description="mouse_move, mouse_click: screen x in points (from desktop_screen or desktop_window).",
    )
    y: int | None = Field(default=None, description="mouse_move, mouse_click: screen y in points.")
    button: Literal["left", "right", "middle"] = Field(
        default="left", description="mouse_click: which button."
    )
    double: bool = Field(default=False, description="mouse_click: a double click.")


class DesktopPowerArgs(ToolArgs):
    action: Literal["status", "prevent_sleep"] = Field(
        description="status: battery, charging, and whether Matrx 2 is keeping it awake; prevent_sleep: keep it awake for a while.",
    )
    seconds: int | None = Field(
        default=None,
        ge=0,
        le=86400,
        description="prevent_sleep: how long to keep it awake; 0 lets it sleep again now.",
    )
    reason: str = Field(
        default="Matrx 2 is working",
        description="prevent_sleep: shown where the OS lists what keeps it awake.",
    )


class DesktopResourcesArgs(ToolArgs):
    action: Literal["snapshot"] = Field(
        default="snapshot",
        description="snapshot: CPU use, memory, swap and disk space now (the busiest processes are desktop_process list).",
    )


class FsWatchArgs(ToolArgs):
    action: Literal["start", "events", "stop"] = Field(
        description="start: watch a folder; events: what changed since the last read; stop: end the watch.",
    )
    path: str | None = Field(
        default=None, description="start: the folder (absolute, or relative to the home folder)."
    )
    recursive: bool = Field(default=True, description="start: include every subfolder.")
    ignore: list[str] | None = Field(
        default=None,
        description='start: globs not to report, such as [".git/**", "node_modules/**"].',
    )
    watch_id: str | None = Field(default=None, description="events, stop: the watch (from start).")
    wait_seconds: int = Field(
        default=0,
        ge=0,
        le=25,
        description="events: wait up to this long for a change when none is waiting.",
    )


class DesktopAudioArgs(ToolArgs):
    action: Literal["devices", "record", "play"] = Field(
        description="devices: microphones and outputs; record: record a clip to a WAV file; play: play an audio file aloud.",
    )
    seconds: float | None = Field(
        default=None, ge=0.5, le=600, description="record: how long to record, in seconds."
    )
    device_id: str | None = Field(
        default=None,
        description="record: the microphone; play: the speaker or output (its id from devices). The default one when omitted.",
    )
    path: str | None = Field(
        default=None,
        description="record: where to save the WAV (a temp file when omitted); play: the file to play. Absolute, or relative to the home folder.",
    )
    channels: int | None = Field(
        default=None, ge=1, le=2, description="record: 1 (mono, the default) or 2 (stereo)."
    )
    sample_rate: int | None = Field(
        default=None,
        ge=8000,
        le=192000,
        description="record: samples per second, 16000 by default (the rate transcription reads).",
    )


class DesktopGitArgs(ToolArgs):
    action: Literal[
        "status", "diff", "log", "add", "commit", "push", "pull", "branch", "stash", "clone"
    ] = Field(
        description=(
            "status: branch, tracking and changed files; diff: unstaged (or staged) changes; "
            "log: recent commits; add: stage paths; commit: commit what is staged; push / pull: "
            "with a remote; branch: list, create, delete or switch; stash: push, pop, list or drop; "
            "clone: copy a repository into a new folder."
        ),
    )
    cwd: str | None = Field(
        default=None,
        description="Every action but clone: the repository folder (absolute, or relative to the home folder).",
    )
    path: str | None = Field(default=None, description="diff: only this file or folder.")
    staged: bool = Field(default=False, description="diff: show staged changes instead.")
    limit: int = Field(default=20, ge=1, le=500, description="log: how many commits.")
    paths: list[str] | None = Field(
        default=None, description='add: the paths to stage, such as ["."].'
    )
    message: str | None = Field(
        default=None, description="commit: the message; stash push: an optional label."
    )
    amend: bool = Field(default=False, description="commit: amend the last commit.")
    author: str | None = Field(
        default=None,
        max_length=512,
        description="commit: the author as \"Name <email>\"; the computer's own git identity when omitted.",
    )
    remote: str = Field(default="origin", description="push, pull: the remote.")
    branch: str | None = Field(
        default=None,
        description="push, pull: the branch (default: the current one's upstream); clone: the branch to check out.",
    )
    force_with_lease: bool = Field(
        default=False, description="push: force, only if the remote is as last seen."
    )
    rebase: bool = Field(default=False, description="pull: rebase instead of merge.")
    branch_action: Literal["list", "create", "delete", "switch"] = Field(
        default="list", description="branch: what to do."
    )
    stash_action: Literal["push", "pop", "list", "drop"] = Field(
        default="push", description="stash: what to do."
    )
    name: str | None = Field(
        default=None, description="branch create, delete, switch: the branch name."
    )
    url: str | None = Field(
        default=None, description="clone: the repository URL (or a local path)."
    )
    dest: str | None = Field(
        default=None,
        description="clone: the new folder (absolute, or relative to the home folder); its parent must exist.",
    )
    depth: int | None = Field(
        default=None, ge=1, description="clone: only this many recent commits."
    )


class DesktopWebArgs(ToolArgs):
    action: Literal["fetch", "scrape", "browser_fetch", "search", "research"] = Field(
        description=(
            "fetch: one HTTP request from the user's computer (their IP), the raw answer; scrape: read "
            "pages as clean text through the platform scraper, from the user's computer; browser_fetch: "
            "render one page in a real browser on the user's computer (JavaScript pages); search: web "
            "search through AI Matrx's own search provider; research: search, then read every result "
            "on the user's computer and return the pages' text together."
        ),
    )
    url: str | None = Field(default=None, description="fetch, browser_fetch: the http(s) URL.")
    urls: list[str] | None = Field(default=None, description="scrape: up to 20 http(s) URLs.")
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"] = Field(
        default="GET", description="fetch: the HTTP method."
    )
    headers: dict[str, str] | None = Field(
        default=None, description="fetch: extra request headers."
    )
    body: str | None = Field(default=None, description="fetch: the request body.")
    timeout_s: int = Field(default=30, ge=1, le=300, description="fetch: seconds to wait.")
    get_links: bool = Field(default=False, description="scrape: also return each page's links.")
    follow_redirects: bool | None = Field(
        default=None, description="fetch: follow redirects (true by default)."
    )
    engine: Literal["auto", "browser", "server"] | None = Field(
        default=None,
        description="scrape: auto (the default), browser (render each page in the computer's browser first) or server.",
    )
    wait_timeout_ms: int | None = Field(
        default=None,
        ge=100,
        le=120000,
        description="browser_fetch: how long to wait for wait_for, in milliseconds (30000 by default).",
    )
    use_cache: bool = Field(
        default=True, description="scrape: reuse a page read in the last 30 minutes."
    )
    wait_for: str | None = Field(
        default=None,
        description="browser_fetch: a CSS selector to wait for before reading the page.",
    )
    extract_text: bool = Field(
        default=True,
        description="browser_fetch: true for readable text, false for the rendered HTML.",
    )
    queries: list[str] | None = Field(
        default=None, description="search, research: 1 to 5 search queries."
    )
    count: int = Field(
        default=5,
        ge=1,
        le=20,
        description="search: results per query; research: pages read per query.",
    )
    freshness: Literal["pd", "pw", "pm", "py"] | None = Field(
        default=None,
        description="search, research: only results from the past day, week, month or year.",
    )


class DesktopBrowserArgs(ToolArgs):
    action: Literal[
        "sessions", "tabs", "read", "screenshot", "navigate", "click", "type", "close", "call"
    ] = Field(
        description=(
            "sessions: the browsers connected to Matrx 2 on the user's computer; tabs: their open "
            "tabs; read: the active tab's text; screenshot: a picture of the active tab; navigate: "
            "open a URL in the active tab; click: click an element; type: type into an element; "
            "close: close tabs; call: run any other AI Matrx extension tool by name. navigate, "
            "click, type and close ask the user to confirm in the browser first."
        ),
    )
    url: str | None = Field(default=None, description="navigate: the http(s) URL.")
    selector: str | None = Field(
        default=None, description="click, type: the element's CSS selector."
    )
    ref: str | None = Field(
        default=None, description="click, type: an element ref from read (instead of a selector)."
    )
    text: str | None = Field(default=None, description="type: the text to type.")
    tab_ids: list[int] | None = Field(default=None, description="close: the tabs (ids from tabs).")
    max_chars: int = Field(
        default=8000, ge=100, le=50000, description="read: at most this many characters."
    )
    tool: str | None = Field(
        default=None, description="call: the extension tool's name, such as find_text_on_page."
    )
    tool_args: dict[str, Any] | None = Field(
        default=None, description="call: that tool's arguments."
    )
    browser: str | None = Field(
        default=None,
        description="Which browser (client_instance from sessions). Omit for the one used last.",
    )
    timeout_s: int = Field(
        default=120,
        ge=5,
        le=600,
        description="Seconds to wait, including the user's confirmation in the browser.",
    )


# ── Matrx Local's remaining tools (desktop-protocol 1.37): one op per action ───────────────────
# Times are ISO 8601 (the implementation turns them into the ops' epoch milliseconds).


class DesktopNetArgs(ToolArgs):
    action: Literal["info", "wifi", "bluetooth", "devices", "mdns", "scan", "download"] = Field(
        description=(
            "info: interfaces, addresses, gateway and DNS; wifi: the current Wi-Fi network and the ones "
            "in range; bluetooth: paired and connected devices; devices: devices seen on the local network; "
            "mdns: Bonjour services (or the service types when service_type is omitted); scan: which TCP "
            "ports answer on a host on the local network; download: save a URL onto the computer."
        ),
    )
    service_type: str | None = Field(
        default=None, description="mdns: a service type such as _http._tcp."
    )
    host: str | None = Field(default=None, description="scan: the host name or address.")
    ports: list[int] | None = Field(
        default=None, description="scan: the TCP ports to try (up to 1024)."
    )
    allow_public: bool | None = Field(
        default=None,
        description="scan: true to scan a host on the public internet (only one you are allowed to scan).",
    )
    timeout_ms: int | None = Field(
        default=None, ge=50, le=10000, description="scan: milliseconds to wait on each port (800 by default)."
    )
    url: str | None = Field(default=None, description="download: the http(s) URL.")
    path: str | None = Field(
        default=None,
        description="download: where to save it on the computer (a folder keeps the URL's file name).",
    )
    overwrite: bool | None = Field(
        default=None, description="download: replace a file already there."
    )
    max_bytes: int | None = Field(
        default=None,
        ge=1,
        le=10737418240,
        description="download: refuse a file larger than this many bytes (2 GB by default).",
    )
    timeout_s: int | None = Field(
        default=None, ge=1, le=3600, description="mdns, download: seconds to wait."
    )


class DesktopAutomationArgs(ToolArgs):
    language: Literal["applescript", "jxa", "powershell"] = Field(
        description="applescript or jxa (JavaScript for Automation) on a Mac; powershell on Windows."
    )
    script: str = Field(description="The script. Its output is returned as stdout.")
    timeout_s: int = Field(default=60, ge=1, le=600, description="Seconds before it is stopped.")


class DesktopMailArgs(ToolArgs):
    action: Literal["accounts", "list", "send"] = Field(
        description="accounts: the Mail app's accounts; list: messages in a mailbox, newest first; send: send an email (or leave it open as a draft)."
    )
    account: str | None = Field(default=None, description="list: one account's name; omit for all.")
    mailbox: str | None = Field(default=None, description="list: the mailbox, INBOX by default.")
    unread_only: bool | None = Field(default=None, description="list: only unread messages.")
    limit: int | None = Field(default=None, ge=1, le=200, description="list: at most this many.")
    to: list[str] | None = Field(default=None, description="send: recipient addresses.")
    cc: list[str] | None = Field(default=None, description="send: copied addresses.")
    bcc: list[str] | None = Field(default=None, description="send: blind-copied addresses.")
    subject: str | None = Field(default=None, description="send: the subject.")
    body: str | None = Field(default=None, description="send: the plain-text body.")
    sender: str | None = Field(
        default=None, description="send: the sending address; omit for Mail's default."
    )
    send: bool | None = Field(
        default=None,
        description="send: false leaves it open in Mail as a draft for the user to send.",
    )


class DesktopOutlookArgs(ToolArgs):
    action: Literal["status", "draft", "list", "read"] = Field(
        description="status: which Outlook is on the computer, its accounts, and whether it can be driven; draft: save a new email in Outlook's Drafts (never sends; the user sends it); list: recent messages in a folder, newest first; read: one message in full."
    )
    to: list[str] | None = Field(default=None, description="draft: recipient addresses.")
    cc: list[str] | None = Field(default=None, description="draft: copied addresses.")
    bcc: list[str] | None = Field(default=None, description="draft: blind-copied addresses.")
    subject: str | None = Field(default=None, description="draft: the subject.")
    body: str | None = Field(default=None, description="draft: the body.")
    body_format: Literal["text", "html"] | None = Field(
        default=None, description="draft: text (default) or html."
    )
    attachments: list[str] | None = Field(
        default=None, description="draft: absolute paths of files on the user's computer to attach."
    )
    account: str | None = Field(
        default=None,
        description="draft, list: the account's email address (from status); omit for Outlook's default.",
    )
    display: bool | None = Field(
        default=None, description="draft: also open the draft in a window for the user."
    )
    folder: Literal["inbox", "sent", "drafts"] | None = Field(
        default=None, description="list: the folder, inbox by default."
    )
    unread_only: bool | None = Field(default=None, description="list: only unread messages.")
    limit: int | None = Field(default=None, ge=1, le=200, description="list: at most this many.")
    id: str | None = Field(default=None, description="read: the message's id (from list or draft).")


class DesktopMessagesArgs(ToolArgs):
    action: Literal["chats", "list", "send"] = Field(
        description="chats: recent Messages chats; list: messages, newest first (one chat or all); send: send an iMessage or SMS."
    )
    chat_id: str | None = Field(default=None, description="list: one chat's chat_id (from chats).")
    contact: str | None = Field(
        default=None,
        description="list: only messages with this phone, email or name in the chat (partial matches).",
    )
    unread_only: bool | None = Field(default=None, description="list: only messages not yet read.")
    limit: int | None = Field(
        default=None, ge=1, le=500, description="chats, list: at most this many."
    )
    to: str | None = Field(default=None, description="send: the phone number or email to message.")
    text: str | None = Field(default=None, description="send: the message.")
    service: Literal["iMessage", "SMS"] | None = Field(
        default=None,
        description="send: force iMessage or SMS; omit to use iMessage, or SMS when they have none.",
    )


class DesktopContactsArgs(ToolArgs):
    action: Literal["search", "get"] = Field(
        description="search: find contacts; get: one contact's card."
    )
    query: str | None = Field(
        default=None,
        description="search: a name, organization, email or phone number; omit to list the first contacts.",
    )
    limit: int | None = Field(default=None, ge=1, le=200, description="search: at most this many.")
    id: str | None = Field(default=None, description="get: the contact's id (from search).")


class DesktopCalendarArgs(ToolArgs):
    action: Literal["events", "create_event", "reminders", "create_reminder"] = Field(
        description="events: calendar events in a time range; create_event: add an event; reminders: open (or all) reminders; create_reminder: add a reminder."
    )
    start: str | None = Field(
        default=None, description="events: range start; create_event: event start (ISO 8601)."
    )
    end: str | None = Field(
        default=None, description="events: range end; create_event: event end (ISO 8601)."
    )
    calendar: str | None = Field(
        default=None, description="events, create_event: one calendar's name."
    )
    calendars: NameList | None = Field(
        default=None, description="events: several calendars by name (with calendar, both count)."
    )
    title: str | None = Field(default=None, description="create_event, create_reminder: the title.")
    all_day: bool | None = Field(default=None, description="create_event: an all-day event.")
    location: str | None = Field(default=None, description="create_event: where.")
    notes: str | None = Field(default=None, description="create_event, create_reminder: notes.")
    list: str | None = Field(
        default=None, description="reminders, create_reminder: one Reminders list's name."
    )
    lists: NameList | None = Field(
        default=None, description="reminders: several Reminders lists by name (with list, both count)."
    )
    due: str | None = Field(default=None, description="create_reminder: when it is due (ISO 8601).")
    include_completed: bool | None = Field(
        default=None, description="reminders: also completed ones."
    )
    limit: int | None = Field(
        default=None, ge=1, le=500, description="events, reminders: at most this many."
    )


class DesktopPhotosArgs(ToolArgs):
    action: Literal["search", "get"] = Field(
        description="search: photos, newest first; get: one photo, optionally exported so other tools can read the file."
    )
    query: str | None = Field(default=None, description="search: text in the file name or title.")
    start: str | None = Field(default=None, description="search: taken on or after (ISO 8601).")
    end: str | None = Field(default=None, description="search: taken on or before (ISO 8601).")
    favorites_only: bool | None = Field(default=None, description="search: only favorites.")
    media_type: Literal["image", "video", "all"] | None = Field(
        default=None, description="search: only photos (image) or videos; all by default."
    )
    limit: int | None = Field(default=None, ge=1, le=200, description="search: at most this many.")
    id: str | None = Field(default=None, description="get: the photo's id (from search).")
    export: bool | None = Field(
        default=None,
        description="get: copy the original to a file on the computer and return its path.",
    )
    thumbnail_size: int | None = Field(
        default=None,
        ge=64,
        le=2048,
        description="get: also return a thumbnail this many pixels on its longest side, which you see as an image.",
    )


class DesktopLocationArgs(ToolArgs):
    timeout_s: int = Field(default=15, ge=1, le=60, description="Seconds to wait for a fix.")


class DesktopWindowsAdminArgs(ToolArgs):
    action: Literal[
        "registry_read", "registry_write", "services", "service_control", "event_log", "features"
    ] = Field(
        description=(
            "registry_read: a key's values and subkeys; registry_write: set or delete a value; services: "
            "Windows services; service_control: start, stop, restart, pause or resume one; event_log: recent events; "
            "features: optional Windows features."
        ),
    )
    key: str | None = Field(
        default=None,
        description="registry_read, registry_write: the key, such as HKCU\\Software\\Example.",
    )
    name: str | None = Field(
        default=None,
        description="registry_read, registry_write: the value's name; service_control: the service's name.",
    )
    type: (
        Literal[
            "REG_SZ",
            "REG_EXPAND_SZ",
            "REG_MULTI_SZ",
            "REG_DWORD",
            "REG_QWORD",
            "REG_BINARY",
            "REG_NONE",
        ]
        | None
    ) = Field(default=None, description="registry_write: the value's type, REG_SZ by default.")
    data: str | None = Field(default=None, description="registry_write: the value's data.")
    delete: bool | None = Field(
        default=None, description="registry_write: delete the value instead."
    )
    service_action: Literal["start", "stop", "restart", "pause", "resume"] | None = Field(
        default=None, description="service_control: what to do."
    )
    filter: str | None = Field(default=None, description="services, features: text in the name.")
    status: Literal["running", "stopped", "paused"] | None = Field(
        default=None, description="services: only services in this state."
    )
    installed_only: bool | None = Field(
        default=None, description="features: only features that are on."
    )
    source: str | None = Field(
        default=None, description="event_log: only events whose source name contains this."
    )
    log: str | None = Field(
        default=None, description="event_log: System, Application, Security… (System by default)."
    )
    levels: list[Literal["critical", "error", "warning", "information", "verbose"]] | None = Field(
        default=None, description="event_log: only these levels."
    )
    since: str | None = Field(default=None, description="event_log: only events after (ISO 8601).")
    limit: int | None = Field(
        default=None, ge=1, le=1000, description="services, event_log: at most this many."
    )


class DesktopScheduleArgs(ToolArgs):
    action: Literal["create", "list", "cancel"] = Field(
        description="create: run a desktop tool action on one of the user's computers on a schedule (every N seconds, a cron, or once at a time); it is saved in AI Matrx and runs on that computer whenever Matrx 2 is open there. list: the scheduled tasks with their latest runs; cancel: stop one."
    )
    name: str | None = Field(default=None, description="create: a name for the task.")
    tool: str | None = Field(
        default=None,
        description="create: the desktop tool to run, such as desktop_net or desktop_notes (not desktop_schedule); or coding_sessions_drive to start a Claude Code or Codex session on that computer each run (tool_args: folder, prompt, provider claude|codex, optional account_profile_id).",
    )
    tool_args: dict[str, Any] | None = Field(
        default=None, description="create: that tool's arguments, exactly as you would call it."
    )
    device_id: str | None = Field(
        default=None,
        description="create/list: the computer (its device id) that runs the task. Default: the computer connected to this conversation.",
    )
    interval_s: int | None = Field(
        default=None, ge=10, le=2_592_000, description="create: seconds between runs (one of interval_s, cron, at)."
    )
    cron: str | None = Field(
        default=None, description="create: a cron expression such as '0 9 * * 1-5' (one of interval_s, cron, at)."
    )
    timezone: str | None = Field(
        default=None, description="create with cron: the IANA timezone the cron reads in, such as America/Los_Angeles (UTC by default)."
    )
    at: str | None = Field(
        default=None, description="create: run once at this ISO-8601 time (one of interval_s, cron, at)."
    )
    max_runs: int | None = Field(
        default=None, ge=1, le=100_000, description="create: stop after this many runs."
    )
    run_now: bool | None = Field(default=None, description="create: also run once right away.")
    include_finished: bool | None = Field(
        default=None, description="list: also finished and canceled tasks."
    )
    id: str | None = Field(default=None, description="cancel: the task's id (from create or list).")


class DesktopNotesArgs(ToolArgs):
    action: Literal["folders", "list", "read", "write", "search"] = Field(
        description="The user's local notes (Markdown files in Documents/Matrx/Notes). folders: the folders and their note counts; list: notes, newest first; read: one note; write: create or replace a note; search: notes containing text."
    )
    folder: str | None = Field(
        default=None,
        description="list: one folder; write: the folder (General by default), such as Work/Clients.",
    )
    path: str | None = Field(
        default=None, description="read: the note's path from list, such as Work/Plan.md."
    )
    label: str | None = Field(default=None, description="write: the note's name, without .md.")
    content: str | None = Field(default=None, description="write: the note's Markdown.")
    if_hash: str | None = Field(
        default=None, description="write: only if the note is still this version (read's hash)."
    )
    query: str | None = Field(default=None, description="search: the text to find.")
    limit: int | None = Field(
        default=None, ge=1, le=2000, description="list, search: at most this many."
    )


class DesktopDocumentsArgs(ToolArgs):
    action: Literal["pdf_text", "ocr", "image_resize", "office_generate"] = Field(
        description="pdf_text: a PDF's text by page; ocr: the text in an image; image_resize: make an image smaller or convert it; office_generate: write a Word (.docx) or Excel (.xlsx) file. All on the user's computer."
    )
    path: str | None = Field(
        default=None,
        description="pdf_text, ocr, image_resize: the file on the computer; office_generate: where to write it.",
    )
    first_page: int | None = Field(
        default=None, ge=1, description="pdf_text: first page (1-based)."
    )
    last_page: int | None = Field(default=None, ge=1, description="pdf_text: last page.")
    max_chars: int | None = Field(
        default=None, ge=1, le=1_048_576, description="pdf_text: at most this much text."
    )
    languages: list[str] | None = Field(
        default=None, description="ocr: language hints such as en-US."
    )
    fast: bool | None = Field(default=None, description="ocr: faster, less accurate.")
    out_path: str | None = Field(
        default=None, description="image_resize: where to write the result."
    )
    max_size: int | None = Field(
        default=None, ge=1, le=32_768, description="image_resize: the longest side in pixels."
    )
    format: Literal["png", "jpeg", "tiff", "heic", "bmp", "gif"] | None = Field(
        default=None, description="image_resize: the output format."
    )
    overwrite: bool | None = Field(
        default=None, description="image_resize, office_generate: replace a file already there."
    )
    kind: Literal["docx", "xlsx"] | None = Field(
        default=None, description="office_generate: Word or Excel."
    )
    title: str | None = Field(default=None, description="office_generate: the document's title.")
    paragraphs: list[dict[str, Any]] | None = Field(
        default=None,
        description="office_generate docx: paragraphs in order, each {style: title|heading1|heading2|heading3|body|bullet|numbered|quote|code, text}.",
    )
    sheets: list[dict[str, Any]] | None = Field(
        default=None,
        description="office_generate xlsx: sheets in order, each {name, rows: [[cell, …], …], header: true}.",
    )


class DesktopEntitiesArgs(ToolArgs):
    action: Literal["names", "private_data"] = Field(
        description="names: people, places and organizations in a text (on a Mac); private_data: emails, phone numbers, card numbers, SSNs, IBANs, IP addresses, URLs and API keys, found and optionally redacted. Nothing leaves the user's computer."
    )
    text: str = Field(description="The text to read.")
    labels: list[Literal["person", "place", "organization"]] | None = Field(
        default=None, description="names: only these kinds."
    )
    kinds: (
        list[
            Literal[
                "email", "phone", "credit_card", "us_ssn", "iban", "ip_address", "url", "api_key"
            ]
        ]
        | None
    ) = Field(default=None, description="private_data: only these kinds.")
    redact: bool | None = Field(
        default=None,
        description="private_data: also return the text with each finding replaced by its kind.",
    )
