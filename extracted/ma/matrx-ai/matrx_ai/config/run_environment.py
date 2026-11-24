"""THE ENVIRONMENT BLOCK — every run is told where it is running and what its tools reach.

Why (2026-11-17): an agent running INSIDE the Chrome extension refused the extension's own browser
tools because a saved memory said "Always use cloud_browser, never the Chrome extension tools" —
written for agents outside the extension. Nothing in its prompt said which environment it was in, so
the memory won. The same agent's stored prompt also disagreed with its live tools (a batch default,
a return shape, tools it did not hold, tools "to load" that were already loaded).

What it is
----------
ONE system-generated block, never hand-written per agent, so it cannot drift:

* the ENVIRONMENT, read from the run's real signals (``detect_environment``): the client surface
  the request declared, the ``browser-dom`` capability payload the extension sends, the compute
  target bound to the run (``active_sandbox.target_kind``), and this process's runtime role;
* what each tool family can and cannot reach THERE, from the run's live tool set and the tool
  registry's bindings (``chrome-extension`` executor = the person's own Chrome);
* the preferred browsing path;
* for the extension: which browser tools are already loaded, which load by category, and the
  facts the tool definitions themselves state (boolean defaults, the "Returns ..." clause);
* any tool the agent's own instructions name that this run neither holds nor can load;
* the precedence rule (``PRECEDENCE_RULE``).

Placement: the per-turn context channel, slot ``run_environment``, staged by the send boundary
alone (``send_boundary._stage_run_environment``) on every send of a run that holds at least one tool
(a run with no tools has nothing to be wrong about; the block is NOT identity and does not hang on
``include_identity``), AFTER the person's saved memories so its words come later. It sits after every
cache breakpoint, so it is re-rendered whenever the held or loadable tool set changes (memo keyed on
that set) and is byte-identical when nothing changed: a mid-run load moves a tool from "can load" to
"already loaded" on the very next send.

"Can load" means through ANY loader the run holds: the Chrome category loader, the desktop category
loader and every bundle lister (``bundle:list_<name>``), each resolved by the loader's OWN logic
(``browser_discovery.loadable_chrome_tools``, ``desktop_discovery.loadable_desktop_tools``,
``bundle_lister.bundle_member_names``). A tool reachable that way is described with the exact call that
loads it and is never listed as unavailable. Everything is derived from what THIS run holds, so a helper
inside an extension-started run that cannot drive Chrome is told exactly that.

matrx-ai never imports aidream: every signal is read off the carried ``AppContext.metadata`` by
the keys declared here (the host writes ``DECLARED_UI_SURFACE_KEY``).
"""

from __future__ import annotations

import re
from collections import OrderedDict
from collections.abc import Awaitable, Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from matrx_ai.config.wire_names import to_wire_name

#: The turn-context slot the block rides in.
ENVIRONMENT_SLOT = "run_environment"
ENVIRONMENT_OPEN = '<environment source="platform">'
ENVIRONMENT_CLOSE = "</environment>"

#: ``AppContext.metadata`` key holding the request's ``client.surface`` (written by the host's
#: tool merge; aidream ``tool_merge.DECLARED_UI_SURFACE_KEY`` re-exports this constant).
DECLARED_UI_SURFACE_KEY = "declared_ui_surface"

PRECEDENCE_RULE = (
    "The ENVIRONMENT block is ground truth about where you are running and what tools you have. "
    "If a memory, note or past message conflicts with it (for example, it names a tool you don't "
    "have or says to avoid tools that this environment is built for), follow the ENVIRONMENT block "
    "and read the memory as if it were written for a different environment."
)

_CHROME_EXECUTOR = "chrome-extension"
_LOCAL_EXECUTOR = "matrx-local"
_EXTENSION_SURFACE_PREFIXES = ("chrome-extension", "matrx-extend")
_LOCAL_SURFACE_PREFIXES = ("matrx-desktop", "matrx-local")
_CLOUD_BROWSER_TOOLS = frozenset({"cloud_browser"})
_WEB_TOOLS = frozenset({"web", "research_web"})
_FILES_AND_COMMANDS_PREFIXES = ("fs_", "shell_", "code_", "sandbox_", "desktop_", "python_", "execute_")
_MAX_FACT_LINES = 30


class RunEnvironment(StrEnum):
    CHROME_EXTENSION = "CHROME EXTENSION"
    CLOUD = "CLOUD"
    SANDBOX = "SANDBOX"
    LOCAL_MACHINE = "LOCAL MACHINE"


@dataclass(frozen=True)
class EnvironmentFacts:
    """The run's real signals (never a hand-written label)."""

    surface: str = ""
    browser_dom: bool = False
    target_kind: str = ""
    root_path: str = ""
    process_role: str = ""
    #: The ``browser-dom`` capability payload (the request's real gates: is_admin, granted
    #: permissions, desktop bridge). Empty when the run carries none.
    browser_state: dict[str, Any] = field(default_factory=dict)
    #: True iff the request's live client executors include the extension (what ``load_chrome_tools`` checks).
    extension_live: bool = False
    #: The ``desktop-native`` capability payload (platform), what ``load_desktop_tools`` reads.
    desktop_state: dict[str, Any] = field(default_factory=dict)


# ── signals ──────────────────────────────────────────────────────────────────────────────────


def _process_role() -> str:
    """``sandbox`` / ``desktop`` from the process's DECLARED role (never crashes: ``declared_role``)."""
    try:
        from matrx_utils.runtime_env import MatrxRole, declared_role

        role = declared_role()
    except Exception:  # noqa: BLE001 — an undeclared role is a cloud process
        return ""
    if role is MatrxRole.SANDBOX:
        return "sandbox"
    if role is MatrxRole.DESKTOP:
        return "desktop"
    return ""


def environment_facts(ctx: Any) -> EnvironmentFacts:
    """Read the signals off the carried context (``None`` → a bare cloud run)."""
    metadata = getattr(ctx, "metadata", None)
    metadata = metadata if isinstance(metadata, dict) else {}
    surface = str(metadata.get(DECLARED_UI_SURFACE_KEY) or "")
    payloads = metadata.get("client_capabilities_payloads")
    state: dict[str, Any] = {}
    if isinstance(payloads, dict) and isinstance(payloads.get("browser-dom"), dict):
        state = payloads["browser-dom"]
    elif isinstance(metadata.get("browser-dom"), dict):
        state = metadata["browser-dom"]
    desktop_state: dict[str, Any] = {}
    if isinstance(payloads, dict) and isinstance(payloads.get("desktop-native"), dict):
        desktop_state = payloads["desktop-native"]
    elif isinstance(metadata.get("desktop-native"), dict):
        desktop_state = metadata["desktop-native"]
    active = metadata.get("active_sandbox")
    target_kind = root_path = ""
    if isinstance(active, dict):
        target_kind = str(active.get("target_kind") or "sandbox")
        root_path = str(active.get("root_path") or "")
    return EnvironmentFacts(
        surface=surface,
        browser_dom=bool(state),
        target_kind=target_kind,
        root_path=root_path,
        process_role=_process_role(),
        browser_state=dict(state),
        extension_live=_extension_executor_live(ctx),
        desktop_state=dict(desktop_state),
    )


def _extension_executor_live(ctx: Any) -> bool:
    """The same question ``load_chrome_tools`` asks first: is the extension among the live client executors?"""
    try:
        from matrx_ai.tools.merge import active_tool_executors

        return any(k == _CHROME_EXECUTOR or k.startswith(f"{_CHROME_EXECUTOR}.") for k in active_tool_executors(ctx))
    except Exception:  # noqa: BLE001 — unknown means not live
        return False


def detect_environment(facts: EnvironmentFacts) -> RunEnvironment:
    """The extension first (it is where the person is), then the bound computer, then a sandbox."""
    surface = facts.surface.lower()
    if facts.browser_dom or surface.startswith(_EXTENSION_SURFACE_PREFIXES):
        return RunEnvironment.CHROME_EXTENSION
    if facts.target_kind == "local_machine" or surface.startswith(_LOCAL_SURFACE_PREFIXES) or facts.process_role == "desktop":
        return RunEnvironment.LOCAL_MACHINE
    if facts.target_kind == "sandbox" or facts.process_role == "sandbox":
        return RunEnvironment.SANDBOX
    return RunEnvironment.CLOUD


# ── the live tool set, through the registry ──────────────────────────────────────────────────


def _registry() -> Any:
    from matrx_ai.tools.registry import ToolRegistry

    return ToolRegistry.get_instance()


def _bound_to(registry: Any, name: str, executor: str) -> bool:
    try:
        bindings = registry.bindings_for_tool(name) or set()
    except Exception:  # noqa: BLE001 — an unknown tool is simply not bound
        return False
    return any(b == executor or str(b).startswith(f"{executor}.") for b in bindings)


@dataclass(frozen=True)
class ToolFamilies:
    extension: tuple[str, ...]
    cloud_browser: tuple[str, ...]
    files_and_commands: tuple[str, ...]
    local: tuple[str, ...]
    web: tuple[str, ...]
    #: Extension tools whose own argument schema carries ``tab_id`` (derived, never assumed).
    tab_tools: tuple[str, ...] = ()
    #: Extension tools that run ONLY in the extension (no other executor is bound), so no extension
    #: connected means they cannot run. A tool also bound to another executor (update_plan runs in the app too) is not here.
    extension_only: tuple[str, ...] = ()


def _only_extension(registry: Any, name: str) -> bool:
    try:
        bindings = registry.bindings_for_tool(name) or set()
    except Exception:  # noqa: BLE001
        return False
    return bool(bindings) and all(b == _CHROME_EXECUTOR or str(b).startswith(f"{_CHROME_EXECUTOR}.") for b in bindings)


def tool_families(held: Iterable[str], registry: Any) -> ToolFamilies:
    names = sorted(set(held))
    extension = tuple(n for n in names if _bound_to(registry, n, _CHROME_EXECUTOR))
    local = tuple(n for n in names if _bound_to(registry, n, _LOCAL_EXECUTOR))
    taken = set(extension) | set(local)
    return ToolFamilies(
        extension=extension,
        cloud_browser=tuple(n for n in names if n in _CLOUD_BROWSER_TOOLS),
        files_and_commands=tuple(n for n in names if n not in taken and n.startswith(_FILES_AND_COMMANDS_PREFIXES)),
        local=local,
        web=tuple(n for n in names if n in _WEB_TOOLS),
        tab_tools=tuple(n for n in extension if _takes_tab_id(registry, n)),
        extension_only=tuple(n for n in extension if _only_extension(registry, n)),
    )


def _takes_tab_id(registry: Any, name: str) -> bool:
    """Only a tool whose own argument schema has ``tab_id`` takes one."""
    tool = registry.get(name)
    params = getattr(tool, "parameters", None)
    return isinstance(params, dict) and "tab_id" in params


def _loadable_extension_tools(facts: EnvironmentFacts, held: frozenset[str], registry: Any) -> dict[str, list[str]]:
    """Extension tools this run could REALLY load now: its loader is held, the extension is live, and
    ``browser_discovery.loadable_chrome_tools`` (the loader's own routing and gates) passes them."""
    if "load_chrome_tools" not in held or not facts.extension_live:
        return {}
    try:
        from matrx_ai.tools.implementations.browser_discovery import loadable_chrome_tools

        return loadable_chrome_tools(facts.browser_state, held=held, registry=registry)
    except Exception:  # noqa: BLE001 — an unreadable registry offers nothing rather than something false
        return {}


def _loadable_desktop_tools(facts: EnvironmentFacts, held: frozenset[str]) -> dict[str, list[str]]:
    """Desktop tools ``load_desktop_tools`` could load: its own candidates and filter."""
    if "load_desktop_tools" not in held:
        return {}
    try:
        from matrx_ai.tools.implementations.desktop_discovery import loadable_desktop_tools

        return loadable_desktop_tools(facts.desktop_state, held=held)
    except Exception:  # noqa: BLE001 — an unreadable registry offers nothing rather than something false
        return {}


LISTER_PREFIX = "bundle:list_"


def held_bundle_listers(held: Iterable[str]) -> tuple[str, ...]:
    """The bundle listers (``bundle:list_<name>``) a run holds, sorted."""
    return tuple(sorted(n for n in held if n.startswith(LISTER_PREFIX)))


@dataclass(frozen=True)
class Loaders:
    """Everything this run could load through a loader it holds (never a tool it already holds)."""

    chrome: dict[str, list[str]] = field(default_factory=dict)
    desktop: dict[str, list[str]] = field(default_factory=dict)
    #: lister -> member tools not yet held (listers whose members are all held are left out).
    bundles: dict[str, tuple[str, ...]] = field(default_factory=dict)
    #: listers whose members could not be read just now (said so in the block, never guessed).
    unreadable: tuple[str, ...] = ()

    def names(self) -> frozenset[str]:
        out: set[str] = set()
        for group in (*self.chrome.values(), *self.desktop.values(), *self.bundles.values()):
            out.update(group)
        return frozenset(out)

    def lister_of(self, tool: str) -> str | None:
        return next((lister for lister, names in self.bundles.items() if tool in names), None)

    def key(self) -> tuple[Any, ...]:
        return (
            tuple((c, tuple(n)) for c, n in sorted(self.chrome.items())),
            tuple((c, tuple(n)) for c, n in sorted(self.desktop.items())),
            tuple(sorted(self.bundles.items())),
            self.unreadable,
        )


def loaders_for(
    facts: EnvironmentFacts,
    held: frozenset[str],
    registry: Any,
    bundle_members: Mapping[str, Sequence[str] | None] | None = None,
) -> Loaders:
    """ONE answer to "what can this run load?": category loaders and bundle listers alike.

    ``bundle_members`` is ``{lister: members}`` from ``resolve_bundle_members`` (``None`` = unreadable)."""
    bundles: dict[str, tuple[str, ...]] = {}
    unreadable: list[str] = []
    for lister, members in sorted((bundle_members or {}).items()):
        if lister not in held:
            continue
        if members is None:
            unreadable.append(lister)
            continue
        rest = tuple(sorted(n for n in set(members) if n not in held))
        if rest:
            bundles[lister] = rest
    return Loaders(
        chrome=_loadable_extension_tools(facts, held, registry),
        desktop=_loadable_desktop_tools(facts, held),
        bundles=bundles,
        unreadable=tuple(unreadable),
    )


_BUNDLE_TTL_SECONDS = 120.0  # protocol-constant: memory bound on an in-process memo of a run bundle read (expires on its own), not an admin behavior
_BUNDLE_MEMO: dict[str, tuple[float, tuple[str, ...] | None]] = {}


async def _bundle_members(lister: str) -> tuple[str, ...]:
    """The lister's own member resolution (``bundle_lister.bundle_member_names``)."""
    from matrx_ai.tools.implementations.bundle_lister import bundle_member_names

    return tuple(await bundle_member_names(lister))


async def resolve_bundle_members(held: Iterable[str]) -> dict[str, tuple[str, ...] | None]:
    """``{lister: members}`` for every bundle lister the run holds (short TTL memo: membership rarely
    changes and every send asks). A lister that cannot be read maps to ``None`` and is announced."""
    import time

    from matrx_utils import vcprint

    out: dict[str, tuple[str, ...] | None] = {}
    now = time.monotonic()
    for lister in held_bundle_listers(held):
        cached = _BUNDLE_MEMO.get(lister)
        if cached is not None and now - cached[0] < _BUNDLE_TTL_SECONDS:
            out[lister] = cached[1]
            continue
        try:
            members: tuple[str, ...] | None = await _bundle_members(lister)
        except Exception as exc:  # noqa: BLE001 — the block says so; the send goes on
            members = None
            vcprint(
                f"[run_environment] could not read the members of {lister}: {type(exc).__name__}: {exc} "
                "— the ENVIRONMENT block says its tools are unreadable right now.",
                color="yellow",
            )
        if members is not None:  # a failure is never memoised
            _BUNDLE_MEMO[lister] = (now, members)
        out[lister] = members
    return out


def _loadable_names(loadable: Mapping[str, Sequence[str]]) -> frozenset[str]:
    return frozenset(n for names in loadable.values() for n in names)


_RETURNS = re.compile(r"(Returns?\b[^.]*(?:\.[^\sA-Z][^.]*)*\.?(?:\s*[a-z_]+ = [^.]*\.?)?)")


def _tool_facts(names: Iterable[str], registry: Any) -> list[str]:
    """What each held tool's OWN definition states: boolean defaults and its "Returns ..." clause."""
    lines: list[str] = []
    for name in names:
        tool = registry.get(name)
        if tool is None:
            continue
        parts: list[str] = []
        params = getattr(tool, "parameters", None) or {}
        if isinstance(params, dict):
            for key, spec in sorted(params.items()):
                if isinstance(spec, dict) and spec.get("type") == "boolean" and "default" in spec:
                    parts.append(f"{key} defaults to {str(bool(spec['default'])).lower()}")
        match = _RETURNS.search(str(getattr(tool, "description", "") or ""))
        if match:
            parts.append(match.group(1).strip())
        if parts:
            lines.append(f"- {name}: " + "; ".join(parts))
        if len(lines) >= _MAX_FACT_LINES:
            break
    return lines


#: A word made of identifier characters, with nothing word-like or dotted glued to either side.
_WORD = re.compile(r"(?<![\w.:-])([A-Za-z][\w.:-]*\w|[A-Za-z])(?![\w])")
#: A name written AS a tool: in code marks (`name`) or in call form name(...).
_MARKED = re.compile(r"`([A-Za-z][\w.:-]*)`|\b([A-Za-z][\w.:-]*)\(")


def _identifier_shaped(name: str) -> bool:
    """A registered name that cannot be an ordinary English word: it carries ``_``, a digit, ``.`` or ``:``."""
    return any(ch in name for ch in "_.:") or any(ch.isdigit() for ch in name)


def tools_named_but_absent(text: str, held: Iterable[str], registry: Any) -> tuple[str, ...]:
    """Registered tool names ``text`` mentions that the run does not hold (unique; the ones the text tells the agent to call first, then the rest, each in order of first mention).

    Matched against the registry's REAL names, whole word only. An identifier-shaped name
    (``cloud_browser``, ``mcp.notion.search``) counts even in plain prose. A name that is also an
    ordinary English word (``find``, ``navigate``, ``computer``, ``web``) counts only when written as a
    tool — in code marks or call form — so everyday prose never trips it. ``held`` is every tool the
    run holds, preloaded or loaded mid-run (``tool_briefings.tool_names_of``). Shared by the
    ENVIRONMENT block and the person-memory renderer; it never edits the text."""
    if not text:
        return ()
    held_set = set(held)
    try:
        known = set(registry.list_tool_names())
    except Exception:  # noqa: BLE001
        return ()
    first: dict[str, int] = {}
    for m in _MARKED.finditer(text):
        name = m.group(1) or m.group(2)
        if name in known and name not in held_set:
            first.setdefault(name, m.start())
    for m in _WORD.finditer(text):
        name = m.group(1)
        if name in known and name not in held_set and _identifier_shaped(name):
            first.setdefault(name, m.start())

    def told_to_call(name: str) -> bool:
        """True when ANY mention of the tool is an instruction to use it, not just a listing."""
        for m in re.finditer(rf"(?<![\w.:-]){re.escape(name)}(?![\w])", text):
            line_start = text.rfind("\n", 0, m.start()) + 1
            before = text[max(line_start, m.start() - 80) : m.start()]
            if _INSTRUCTION_VERB.search(before) or text[m.end() : m.end() + 1] == "(":
                return True
        return False

    # Names the instructions tell the agent to CALL lead; each group is in order of first mention.
    return tuple(sorted(first, key=lambda n: (not told_to_call(n), first[n])))


#: A word that turns a mention into an instruction ("use `x`", "apply every change with `x`").
_INSTRUCTION_VERB = re.compile(r"\b(use|using|call|calls|apply|edit|run|invoke|via|with|read|write|ask)\b", re.IGNORECASE)


# ── the block ────────────────────────────────────────────────────────────────────────────────


def _join(names: Iterable[str]) -> str:
    return ", ".join(names)


_HEADLINES: dict[RunEnvironment, str] = {
    RunEnvironment.CHROME_EXTENSION: (
        "You are running inside the person's own Chrome browser, through the AI Matrx Chrome "
        "extension. The extension's browser tools act in their real Chrome, with their real cookies "
        "and logins."
    ),
    RunEnvironment.CLOUD: (
        "You are running on AI Matrx servers. There is no Chrome extension in this run and no reach "
        "into the person's own browser or computer."
    ),
    RunEnvironment.SANDBOX: (
        "You are running in an isolated sandbox (a cloud VM or container). Its file system is your "
        "workspace and code-execution tools run there. Its network may be limited, and it cannot "
        "reach the person's own browser or computer."
    ),
    RunEnvironment.LOCAL_MACHINE: (
        "You are working with the person's own computer through the AI Matrx desktop app. Local file "
        "and command tools act on that real machine."
    ),
}

def _local_bound(env: RunEnvironment, facts: EnvironmentFacts) -> bool:
    return env is RunEnvironment.LOCAL_MACHINE or facts.target_kind == "local_machine"


def _workspace_phrase(env: RunEnvironment, facts: EnvironmentFacts) -> str:
    """What the files-and-commands tools act on, from what is BOUND to this run."""
    if _local_bound(env, facts):
        return "the person's real computer"
    if env is RunEnvironment.SANDBOX or facts.target_kind == "sandbox":
        return "the sandbox's own file system and shell"
    return "the workspace attached to this run"


_LOCAL_SAFETY = (
    "Safety on this computer: read before you change anything; stay inside the folder you were "
    "given; never delete, overwrite or move the person's files, or run a destructive or "
    "system-changing command, without their clear go-ahead in this conversation."
)

#: How many unavailable names the block lists before saying how many more it left out (a knob: raise it here).
_MAX_ABSENT = 20


_HELPER_HEADLINE = (
    "You are a helper inside a run the person started from their Chrome extension. The run that started "
    "you works in their Chrome, but you run on AI Matrx servers and hold no tool that reaches their Chrome, "
    "their tabs, cookies or logins."
)

_MAX_LISTED_LOADERS = 15
_MAX_LISTED_MEMBERS = 8


def _browsing_path(fam: ToolFamilies, *, extension_reachable: bool, cloud_browser_loader: str = "") -> str:
    """The browsing sentence, built only from tools this run holds or can load."""
    cloud = bool(fam.cloud_browser) or bool(cloud_browser_loader)
    cloud_name = "cloud_browser" + (f" (load it first with {to_wire_name(cloud_browser_loader)})" if cloud_browser_loader else "")
    if extension_reachable:
        text = "Preferred browsing path: the extension's browser tools"
        if any(fam.tab_tools):
            text += " (pass a tab_id to those that take one)"
        if cloud:
            text += (
                f". Use {cloud_name} only if they fail, or when the work must continue unattended "
                "after the person closes Chrome"
            )
        return text + "."
    if cloud and fam.web:
        return (
            f"Preferred browsing path: {cloud_name} for interactive pages, web for public pages; "
            "neither carries the person's logins."
        )
    if cloud:
        return f"Preferred browsing path: {cloud_name} (a browser on our servers, without the person's logins)."
    if fam.web:
        return "Browsing: web reads public pages only; this run holds no interactive browser."
    return "Browsing: this run holds no browsing tool."


def _bundle_lines(loaders: Loaders) -> list[str]:
    """The bundle-lister section: each lister, the exact call, and what it adds."""
    lines: list[str] = []
    if loaders.bundles:
        lines.append("More tools load by calling a bundle loader (it adds that bundle's tools to this run):")
        for lister, names in list(loaders.bundles.items())[:_MAX_LISTED_LOADERS]:
            shown = list(names[:_MAX_LISTED_MEMBERS])
            more = f" (and {len(names) - _MAX_LISTED_MEMBERS} more)" if len(names) > _MAX_LISTED_MEMBERS else ""
            lines.append(f"- {to_wire_name(lister)}: {_join(shown)}{more}")
        if len(loaders.bundles) > _MAX_LISTED_LOADERS:
            lines.append(f"- (and {len(loaders.bundles) - _MAX_LISTED_LOADERS} more loaders)")
    if loaders.unreadable:
        lines.append(
            "Bundle loaders whose tools could not be read just now (call one to see what it adds): "
            + _join(to_wire_name(n) for n in loaders.unreadable)
        )
    return lines


_PAGE_READERS = ("get_page_text", "read_page", "find", "find_text_on_page")


def _page_guidance(extension: tuple[str, ...]) -> list[str]:
    """How to work a page with the extension, derived from the held extension tools only: act from
    the automatic picture, read text/elements for exact values, batch a known sequence, never
    re-read what was just shown. A few short lines; no line names a tool the run does not hold."""
    readers = [n for n in _PAGE_READERS if n in extension]
    lines = [
        "How to work the page:",
        "- After you navigate or act, the result usually includes a picture of the tab: act from it "
        "when it shows what you need.",
    ]
    if readers:
        lines.append(
            f"- Read the text or element list ({_join(readers)}) when you need exact text, values or refs."
        )
    if "chrome_batch" in extension:
        lines.append("- Put a known sequence of steps in one chrome_batch call.")
    lines.append("- Do not re-read a page you were just shown.")
    return lines


def compose_environment_block(
    env: RunEnvironment,
    held: Iterable[str],
    registry: Any,
    *,
    facts: EnvironmentFacts | None = None,
    prompt_text: str = "",
    bundle_members: Mapping[str, Sequence[str] | None] | None = None,
) -> str:
    """THE ONE RENDERER (pure over its inputs). Every line is derived from what is held by and
    loadable in THIS run; nothing is said about a tool or place the run does not have."""
    held_set = frozenset(held)
    facts = facts or EnvironmentFacts()
    fam = tool_families(held_set, registry)
    loaders = loaders_for(facts, held_set, registry, bundle_members)
    loadable = loaders.chrome if env is RunEnvironment.CHROME_EXTENSION else {}
    loader_live = "load_chrome_tools" in held_set and facts.extension_live
    # An extension-started run whose OWN tool set cannot drive Chrome (a helper) is told so.
    helper = env is RunEnvironment.CHROME_EXTENSION and not (fam.extension or loader_live)
    cloud_lister = "" if fam.cloud_browser else (loaders.lister_of("cloud_browser") or "")
    headline = _HELPER_HEADLINE if helper else _HEADLINES[env]
    lines: list[str] = [f"ENVIRONMENT: {env.value}", headline, "", "What your tools reach here:"]

    if env is RunEnvironment.CHROME_EXTENSION:
        if fam.extension:
            tab = tuple(n for n in fam.extension if n in fam.tab_tools)
            other = tuple(n for n in fam.extension if n not in fam.tab_tools)
            if tab:
                lines.append(
                    f"- Chrome extension tools that act on a tab ({_join(tab)}): the person's real open tabs, "
                    "with their cookies and logins. This is your primary browser here."
                )
                lines.append(f"  Tools that take a tab_id: {_join(tab)}.")
            if other:
                lines.append(
                    f"- Other extension tools ({_join(other)}): run in the extension but take no tab_id, so they "
                    "do not act on a page themselves (they talk to the person, plan, or batch other calls)."
                )
        elif loader_live:
            lines.append("- Chrome extension tools: none loaded yet; load them with load_chrome_tools.")
        else:
            lines.append("- Chrome extension tools: not in this run's tool set; you cannot drive their Chrome.")
    elif fam.extension_only:
        lines.append(
            f"- Chrome extension tools ({_join(fam.extension_only)}): in this run's tool set, but no Chrome "
            "extension is connected to this run, so they cannot run."
        )
    else:
        lines.append("- Chrome extension tools: not available here.")
    if fam.cloud_browser:
        lines.append(
            f"- Cloud browser ({_join(fam.cloud_browser)}): a separate browser on our servers. It does "
            "not have the person's cookies or logins."
        )
    elif cloud_lister:
        lines.append(
            f"- Cloud browser (cloud_browser): not loaded yet; load it by calling {to_wire_name(cloud_lister)}. "
            "It is a separate browser on our servers and does not have the person's cookies or logins."
        )
    if fam.web:
        lines.append(f"- Web reading ({_join(fam.web)}): public pages fetched from our servers, no logins.")
    if fam.files_and_commands:
        lines.append(f"- Files and commands ({_join(fam.files_and_commands)}): {_workspace_phrase(env, facts)}.")
    if fam.local:
        lines.append(f"- Local machine tools ({_join(fam.local)}): the person's real computer.")
    local_bound = _local_bound(env, facts)
    if local_bound and not (fam.files_and_commands or fam.local):
        lines.append("- Local file and command tools: not in this run (the computer is not connected); say so instead of guessing.")
    if facts.root_path and (fam.files_and_commands or fam.local):
        lines.append(f"Workspace root: {facts.root_path}")

    extension_reachable = env is RunEnvironment.CHROME_EXTENSION and (bool(fam.extension) or loader_live)
    lines += ["", _browsing_path(fam, extension_reachable=extension_reachable, cloud_browser_loader=cloud_lister)]
    if local_bound:
        lines.append(_LOCAL_SAFETY)

    if env is RunEnvironment.CHROME_EXTENSION and fam.extension:
        lines += ["", f"Already loaded (call directly): {_join(fam.extension)}"]
        lines += ["", *_page_guidance(fam.extension), *([""] if loadable else [])]
    if loadable:
        lines += ["", 'More browser tools load by category with load_chrome_tools(category="<name>"):'] if not fam.extension else [
            'More browser tools load by category with load_chrome_tools(category="<name>"):'
        ]
        lines += [f"- {cat}: {_join(names)}" for cat, names in loadable.items()]
    if loaders.desktop:
        lines += ["", 'More desktop tools load by category with load_desktop_tools(category="<name>"):']
        lines += [f"- {cat}: {_join(names)}" for cat, names in loaders.desktop.items()]
    bundle_lines = _bundle_lines(loaders)
    if bundle_lines:
        lines += ["", *bundle_lines]
    if env is RunEnvironment.CHROME_EXTENSION:
        facts_lines = _tool_facts(fam.extension, registry)
        if facts_lines:
            lines += ["", "What these tools do (from their own definitions):", *facts_lines]

    absent = tools_named_but_absent(prompt_text, held_set | loaders.names(), registry)
    if absent:
        shown = list(absent[:_MAX_ABSENT])
        more = f" (and {len(absent) - _MAX_ABSENT} more not listed)" if len(absent) > _MAX_ABSENT else ""
        lines += [
            "",
            f"Your instructions name tools that are not available in this run: {_join(shown)}{more}. "
            "Do not call them; use the tools above for the same job.",
        ]

    lines += ["", PRECEDENCE_RULE]
    return f"{ENVIRONMENT_OPEN}\n" + "\n".join(lines) + f"\n{ENVIRONMENT_CLOSE}"


# ── staging (called only by the send boundary) ───────────────────────────────────────────────

_MAX_MEMO = 512
_MEMO: OrderedDict[tuple[Any, ...], str] = OrderedDict()


def clear_memo() -> None:
    _MEMO.clear()
    _BUNDLE_MEMO.clear()


#: THE AUTHOR'S SWITCH (law 6, PB-07 N1 2026-11-18): ``async (ctx) -> (on, decided_by)``. The host binds it
#: (aidream: the platform-notes knob ``agents.context.system_notes_disabled``, key ``run_environment``, set in
#: the agent builder under Advanced > Platform notes). Unbound (standalone) = on, decided by the platform.
EnvironmentSwitch = Callable[[Any], Awaitable[tuple[bool, str]]]
_SWITCH: EnvironmentSwitch | None = None


def set_environment_switch(switch: EnvironmentSwitch | None) -> None:
    """Install the host's ``ctx -> (on, decided_by)`` switch for the ENVIRONMENT block (``None`` = always on)."""
    global _SWITCH
    _SWITCH = switch


async def environment_switch(ctx: Any) -> tuple[bool, str]:
    """Is the ENVIRONMENT block on for this run, and which rung decided? A switch failure raises to the caller."""
    if _SWITCH is None:
        return True, "platform"
    return await _SWITCH(ctx)


def _carried_context() -> Any:
    try:
        from matrx_ai.context.app_context import try_get_app_context

        return try_get_app_context()
    except Exception:  # noqa: BLE001 — no carried context is a legal standalone call
        return None


async def reachable_tool_names(config: Any) -> frozenset[str]:
    """Every tool the run holds PLUS every one it could really load through any loader it holds.

    What "not available in this run" is measured against: a tool in this set is never called absent."""
    from matrx_ai.config.tool_briefings import tool_names_of

    held = tool_names_of(config)
    facts = environment_facts(_carried_context())
    members = await resolve_bundle_members(held)
    env = detect_environment(facts)
    loaders = loaders_for(facts, held, _registry(), members)
    chrome = _loadable_names(loaders.chrome) if env is RunEnvironment.CHROME_EXTENSION else frozenset()
    return held | chrome | _loadable_names(loaders.desktop) | _loadable_names(loaders.bundles)


async def render_for_run(config: Any) -> tuple[str, RunEnvironment, tuple[str, ...]]:
    """``(block, environment, absent tool names)`` for this run, or ``("", ..)`` when the run holds no tool.

    Re-rendered whenever the held or loadable set changes (memo keyed on it), identical bytes otherwise."""
    from matrx_ai.config.tool_briefings import tool_names_of

    ctx = _carried_context()
    request = str(getattr(ctx, "request_id", "") or "")
    facts = environment_facts(ctx)
    env = detect_environment(facts)
    held = tool_names_of(config)
    if not held:
        return "", env, ()
    si = getattr(config, "system_instruction", None)
    prompt_text = str(si) if si is not None else ""
    registry = _registry()
    members = await resolve_bundle_members(held)
    loaders = loaders_for(facts, held, registry, members)
    reachable = held | loaders.names()
    if env is not RunEnvironment.CHROME_EXTENSION:
        reachable = held | _loadable_names(loaders.desktop) | _loadable_names(loaders.bundles)
    absent = tools_named_but_absent(prompt_text, reachable, registry)
    key = (request, env, tuple(sorted(held)), loaders.key(), hash(prompt_text), facts.root_path, facts.target_kind, facts.surface)
    if request and key in _MEMO:
        return _MEMO[key], env, absent
    block = compose_environment_block(env, held, registry, facts=facts, prompt_text=prompt_text, bundle_members=members)
    if request:
        _MEMO[key] = block
        while len(_MEMO) > _MAX_MEMO:
            _MEMO.popitem(last=False)
    return block, env, absent


__all__ = [
    "DECLARED_UI_SURFACE_KEY",
    "EnvironmentSwitch",
    "environment_switch",
    "set_environment_switch",
    "ENVIRONMENT_CLOSE",
    "ENVIRONMENT_OPEN",
    "ENVIRONMENT_SLOT",
    "PRECEDENCE_RULE",
    "EnvironmentFacts",
    "Loaders",
    "RunEnvironment",
    "clear_memo",
    "compose_environment_block",
    "detect_environment",
    "environment_facts",
    "held_bundle_listers",
    "loaders_for",
    "reachable_tool_names",
    "resolve_bundle_members",
    "render_for_run",
    "tool_families",
    "tools_named_but_absent",
]
