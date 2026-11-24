"""Every run is told, by the platform, WHERE it is running and WHAT its tools reach.

The trigger (2026-11-17): an agent running INSIDE the Chrome extension refused the extension's own
browser tools because a saved memory said "Always use cloud_browser, never the Chrome extension
tools" (written for agents outside the extension). Nothing in its prompt said which environment it
was in, so the memory won. Its stored prompt also disagreed with its live tools (chrome_batch "stops
on first error" while ``stop_on_error`` defaults to false; find_text_on_page "returns refs" while it
returns CSS selectors; context_patch named while the run did not hold it).

The guard: the send boundary stages ONE system-generated ENVIRONMENT block on every chat send
(``matrx_ai/config/run_environment.py``), built from the real client/runtime signals and the
run's live tool set; a contradicting memory never removes it; a prompt naming a tool the run does
not hold is caught.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from matrx_utils.source_guard import stable_source

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.config import run_environment as env_mod
from matrx_ai.config.context_trim import TrimPolicy
from matrx_ai.config.run_environment import (
    ENVIRONMENT_SLOT,
    PRECEDENCE_RULE,
    RunEnvironment,
    detect_environment,
    environment_facts,
    tools_named_but_absent,
)
from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send, reset_loop_state
from matrx_ai.instructions.core import SystemInstruction

# What the live registry says (tool.definition / tool.binding rows, 2026-11-17), as a fake.
_EXT = "chrome-extension"
_TAB = {"tab_id": {"type": "string"}}


def _row(binding: str, category: str, description: str = "", parameters: dict[str, Any] | None = None, **extra: Any) -> dict[str, Any]:
    return {"binding": binding, "category": category, "description": description, "parameters": parameters or {}, **extra}


_TOOLS: dict[str, dict[str, Any]] = {
    "chrome_batch": _row(
        _EXT,
        "core",
        "Run up to 20 read-tier extension tools sequentially in one round trip. "
        "Returns {count, results: [{name, ok, output | error}]} in order.",
        {"calls": {"type": "array"}, "stop_on_error": {"type": "boolean", "default": False}},
    ),
    "find_text_on_page": _row(
        _EXT,
        "reading",
        "Ctrl+F over a tab's text nodes. Returns {count, matches: [{text, context, selector, tag}]}; "
        "selector = enclosing element.",
        {**_TAB, "query": {"type": "string"}, "regex": {"type": "boolean", "default": False}},
    ),
    "read_page": _row(_EXT, "reading", "Read the page.", _TAB),
    "find": _row(_EXT, "reading", "Find elements.", _TAB),
    "computer": _row(_EXT, "interaction", "Mouse and keys.", _TAB),
    "navigate": _row(_EXT, "interaction", "Go to a URL.", _TAB),
    "extract_table": _row(_EXT, "reading", "Tables to JSON.", _TAB),
    "update_plan": _row(_EXT, "human", "Propose a plan.", {"steps": {"type": "array"}}, also_bound=["matrx-user"]),
    "request_user_takeover": _row(_EXT, "human", "Ask the person to act in the page.", {**_TAB, "reason": {"type": "string"}}),
    "cdp_session": _row(_EXT, "devtools", "Attach the debugger.", _TAB, admin_only=True),
    "chrome_cookies": _row(
        _EXT, "chrome", "Read cookies.", {}, gating=[{"gate": "has_optional_permission", "args": {"permission": "cookies"}}]
    ),
    "desktop_run_command": _row(_EXT, "desktop", "Run a command on the desktop app.", {}),
    "load_chrome_tools": _row("matrx-ai-core", "core"),
    "cloud_browser": _row("aidream", "browser"),
    "context_patch": _row("matrx-ai-core", "context"),
    "fs_read": _row("matrx-ai-core", "fs"),
    "shell_execute": _row("matrx-ai-core", "fs"),
    "web": _row("aidream", "web"),
    "bundle:list_browser": _row("matrx-ai-core", "tooling"),
    "load_desktop_tools": _row("matrx-ai-core", "core"),
    "local_file": _row("matrx-local", "desktop", "Read and write files."),
    "local_mac_apps": _row("matrx-local", "desktop", "Mac apps."),
    "local_windows_ps": _row("matrx-local", "desktop", "Windows shell."),
}


class _FakeRegistry:
    def _tool(self, name: str):
        row = _TOOLS.get(name)
        if row is None:
            return None
        return SimpleNamespace(
            name=name,
            category=row["category"],
            description=row["description"],
            parameters=row["parameters"],
            admin_only=row.get("admin_only", False),
            gating=row.get("gating", []),
            tier="read",
        )

    def get(self, name: str):
        return self._tool(name)

    def list_tools(self, category: str | None = None):
        tools = [self._tool(n) for n in sorted(_TOOLS)]
        return [t for t in tools if category is None or t.category == category]

    def bindings_for_tool(self, name: str) -> set[str]:
        row = _TOOLS.get(name)
        return {row["binding"], *row.get("also_bound", [])} if row else set()

    def list_tool_names(self) -> list[str]:
        return sorted(_TOOLS)


EXTENSION_PROMPT = (
    "You are the Matrx Browser Agent.\n"
    "- `chrome_batch` stops on first error.\n"
    "- `find_text_on_page` returns matches with refs.\n"
    "Apply EVERY change to the working_document with `context_patch`.\n"
)
MEMORY = "<person_context source=\"platform\">Always use cloud_browser, never the Chrome extension tools.</person_context>"


@pytest.fixture(autouse=True)
def _registry(monkeypatch):
    import matrx_connect

    monkeypatch.setattr(env_mod, "_registry", lambda: _FakeRegistry())
    monkeypatch.setattr(matrx_connect, "admin_tool_authorized", lambda: True)
    reset_loop_state()
    env_mod.clear_memo()
    yield
    reset_loop_state()
    env_mod.clear_memo()


def _ctx(**metadata: Any) -> SimpleNamespace:
    """A carried context. The host resolves the live client executors at the edge; an extension request has the extension."""
    surface = str(metadata.get("declared_ui_surface", ""))
    if surface.startswith("chrome-extension") or "client_capabilities_payloads" in metadata:
        metadata.setdefault("active_tool_executors", ["chrome-extension"])
    return SimpleNamespace(request_id=f"req-{id(metadata)}", metadata=dict(metadata))


def _config(tools: list[str], system: str = "You are an agent.") -> UnifiedConfig:
    config = UnifiedConfig(
        model="claude-sonnet-4-6",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="Open my inbox")])]),
    )
    config.system_instruction = SystemInstruction.from_value(system)
    config.tools = list(tools)
    return config


async def _send(config: UnifiedConfig, ctx: Any, monkeypatch) -> str:
    monkeypatch.setattr(env_mod, "_carried_context", lambda: ctx)
    await prepare_for_send(config, stage=STAGE_LOOP, policy=TrimPolicy())
    return config.messages.turn_context_blocks().get(ENVIRONMENT_SLOT, "")


# ── 1. detection: the real client/runtime signals decide, nothing hand-written ──────────────────


@pytest.mark.parametrize(
    ("metadata", "expected"),
    [
        ({"declared_ui_surface": "chrome-extension/assistant"}, RunEnvironment.CHROME_EXTENSION),
        ({"client_capabilities_payloads": {"browser-dom": {"auth": {}}}}, RunEnvironment.CHROME_EXTENSION),
        ({"declared_ui_surface": "matrx-user/chat"}, RunEnvironment.CLOUD),
        ({}, RunEnvironment.CLOUD),
        ({"active_sandbox": {"target_kind": "sandbox", "root_path": "/home/agent"}}, RunEnvironment.SANDBOX),
        ({"active_sandbox": {"target_kind": "local_machine", "root_path": "/Users/x"}}, RunEnvironment.LOCAL_MACHINE),
        ({"declared_ui_surface": "matrx-desktop/chat"}, RunEnvironment.LOCAL_MACHINE),
    ],
)
def test_the_environment_comes_from_the_runs_real_signals(metadata, expected) -> None:
    assert detect_environment(environment_facts(_ctx(**metadata))) is expected


# ── 2. every chat send carries the block; the extension run gets the extension block ────────────


async def test_an_extension_run_gets_the_extension_block(monkeypatch) -> None:
    config = _config(["chrome_batch", "find_text_on_page", "read_page", "find", "computer", "navigate", "load_chrome_tools", "cloud_browser"])
    block = await _send(config, _ctx(declared_ui_surface="chrome-extension/assistant"), monkeypatch)
    assert "ENVIRONMENT: CHROME EXTENSION" in block
    assert PRECEDENCE_RULE in block
    assert "tab_id" in block and "real cookies" in block
    # The tool section is generated from the registry, so it says what the tools really do.
    assert "chrome_batch: stop_on_error defaults to false" in block
    assert "selector" in block and "find_text_on_page" in block
    # Preloaded tools are said to be loaded; only the rest are offered through load_chrome_tools.
    loaded_line = next(line for line in block.splitlines() if line.startswith("Already loaded"))
    assert "read_page" in loaded_line and "navigate" in loaded_line
    load_line = next(line for line in block.splitlines() if "load_chrome_tools(" in line)
    assert "extract_table" in block.split(load_line, 1)[1] or "extract_table" in load_line
    assert "read_page" not in block.split(load_line, 1)[1].split("\n\n", 1)[0]


async def test_a_memory_that_contradicts_the_block_never_removes_it(monkeypatch) -> None:
    from matrx_ai.config import person_context

    async def _memory(*_a: Any, **_k: Any) -> tuple[str, str]:  # the person's saved memory, staged by its own step
        return MEMORY, "delivered"

    monkeypatch.setattr(person_context, "render_person_context", _memory)
    config = _config(["chrome_batch", "read_page", "cloud_browser"])
    block = await _send(config, _ctx(declared_ui_surface="chrome-extension/assistant"), monkeypatch)
    blocks = config.messages.turn_context_blocks()
    assert "ENVIRONMENT: CHROME EXTENSION" in block
    assert "never the Chrome extension tools" in blocks["person_context"]  # the memory is not touched (lane B)
    # The block renders AFTER the memory, so the later, authoritative words are the platform's.
    order = list(blocks)
    assert order.index(ENVIRONMENT_SLOT) > order.index("person_context")


@pytest.mark.parametrize(
    ("metadata", "tools", "headline", "must", "must_not"),
    [
        ({"declared_ui_surface": "matrx-user/chat"}, ["cloud_browser", "web"], "ENVIRONMENT: CLOUD", "cloud_browser", "tab_id"),
        (
            {"active_sandbox": {"target_kind": "sandbox", "root_path": "/home/agent"}},
            ["fs_read", "shell_execute", "web"],
            "ENVIRONMENT: SANDBOX",
            "/home/agent",
            "real cookies",
        ),
        (
            {"active_sandbox": {"target_kind": "local_machine", "root_path": "/Users/x/work"}},
            ["fs_read", "shell_execute"],
            "ENVIRONMENT: LOCAL MACHINE",
            "clear go-ahead",
            "tab_id",
        ),
    ],
)
async def test_every_environment_gets_its_own_block(monkeypatch, metadata, tools, headline, must, must_not) -> None:
    block = await _send(_config(tools), _ctx(**metadata), monkeypatch)
    assert headline in block and must in block and must_not not in block
    assert PRECEDENCE_RULE in block
    assert "Chrome extension tools: not available here" in block


async def test_the_block_is_byte_identical_when_nothing_changed(monkeypatch) -> None:
    config = _config(["chrome_batch", "read_page", "load_chrome_tools"])
    ctx = _ctx(declared_ui_surface="chrome-extension/assistant")
    first = await _send(config, ctx, monkeypatch)
    second = await _send(config, ctx, monkeypatch)
    assert first and first == second


async def test_a_mid_run_load_moves_the_tool_from_loadable_to_loaded(monkeypatch) -> None:
    config = _config(["chrome_batch", "read_page", "load_chrome_tools"])
    ctx = _ctx(declared_ui_surface="chrome-extension/assistant")
    first = await _send(config, ctx, monkeypatch)
    assert "- reading: " in first and "extract_table" in first.split("More browser tools load")[1]
    config.tools = [*config.tools, "extract_table"]  # load_chrome_tools added a category mid-run
    second = await _send(config, ctx, monkeypatch)
    assert second != first
    assert "extract_table" in second.split("Already loaded")[1].split("\n")[0]
    assert "extract_table" not in second.split("More browser tools load")[1].split("What these tools do")[0]
    assert await _send(config, ctx, monkeypatch) == second  # and stable again


# ── 3. a prompt naming a tool absent from the run's tool set is caught ───────────────────────────


def test_a_prompt_naming_an_absent_tool_fails_the_check() -> None:
    held = frozenset({"chrome_batch", "find_text_on_page", "read_page"})
    assert tools_named_but_absent(EXTENSION_PROMPT, held, _FakeRegistry()) == ("context_patch",)
    assert tools_named_but_absent("Use `read_page` then `chrome_batch`.", held, _FakeRegistry()) == ()


async def test_the_block_names_the_absent_tools_the_prompt_mentions(monkeypatch) -> None:
    config = _config(["chrome_batch", "find_text_on_page", "read_page"], system=EXTENSION_PROMPT)
    block = await _send(config, _ctx(declared_ui_surface="chrome-extension/assistant"), monkeypatch)
    assert "not available in this run: context_patch" in block
    assert "Ignore" not in block


async def test_a_helper_without_extension_tools_is_never_told_to_use_them(monkeypatch) -> None:
    # A sub-agent inherits its parent's surface (``_child_agent_metadata``) but not always its tools.
    block = await _send(_config(["cloud_browser", "web"]), _ctx(declared_ui_surface="chrome-extension/assistant"), monkeypatch)
    assert "helper inside a run the person started from their Chrome extension" in block
    assert "running inside the person's own Chrome" not in block
    assert "you cannot drive their Chrome" in block and "Preferred browsing path: cloud_browser" in block


# ── 4. the detector sees a registered tool named in plain prose (the incident memory) ────────────

INCIDENT_MEMORY = "Always use cloud_browser, never the Chrome extension tools."


def test_a_bare_tool_name_in_plain_prose_is_caught() -> None:
    reg = _FakeRegistry()
    # A run without cloud_browser: the memory names a tool this run does not have.
    assert tools_named_but_absent(INCIDENT_MEMORY, {"read_page", "chrome_batch"}, reg) == ("cloud_browser",)
    # A run that holds it (preloaded or loaded mid-run) is never flagged.
    assert tools_named_but_absent(INCIDENT_MEMORY, {"read_page", "cloud_browser"}, reg) == ()
    # Whole words only: a longer identifier that merely contains a tool name is not that tool.
    assert tools_named_but_absent("see my_cloud_browser_notes", {"read_page"}, reg) == ()


def test_ordinary_english_words_are_flagged_only_when_marked_as_tools() -> None:
    reg = _FakeRegistry()
    held = {"chrome_batch"}
    prose = "Find the invoice, navigate to the web portal, and use the computer to check it."
    assert tools_named_but_absent(prose, held, reg) == ()
    assert tools_named_but_absent("Call `navigate` then find(query).", held, reg) == ("navigate", "find")  # in order of first mention


# ══ FIX ROUND 1 (2026-11-17): the block states only what is TRUE FOR THIS RUN ═══════════════════

_BD_MEMBER = {"is_admin": False, "desktop_bridge": "none", "optional_permissions_granted": []}
_EXT_HELD = ["chrome_batch", "read_page", "find", "navigate", "update_plan", "request_user_takeover", "load_chrome_tools"]


def _ext_ctx(state: dict[str, Any] | None = None, **more: Any) -> SimpleNamespace:
    payload = {"client_capabilities_payloads": {"browser-dom": dict(_BD_MEMBER if state is None else state)}}
    return _ctx(declared_ui_surface="chrome-extension/assistant", **payload, **more)


# 1. a tool is named as a path only if the run holds it or can load it ────────────────────────────


async def test_no_path_names_a_tool_the_run_does_not_hold(monkeypatch) -> None:
    ext = await _send(_config(_EXT_HELD), _ext_ctx(), monkeypatch)  # no cloud_browser in this run
    assert "cloud_browser" not in ext
    cloud = await _send(_config(["web"]), _ctx(declared_ui_surface="matrx-user/chat"), monkeypatch)
    assert "cloud_browser" not in cloud and "web reads public pages only" in cloud
    nothing = await _send(_config(["fs_read"]), _ctx(declared_ui_surface="matrx-user/chat"), monkeypatch)
    assert "holds no browsing tool" in nothing and "Preferred browsing path" not in nothing


async def test_the_fallback_is_named_only_when_the_run_holds_it(monkeypatch) -> None:
    with_cb = await _send(_config([*_EXT_HELD, "cloud_browser"]), _ext_ctx(), monkeypatch)
    assert "Use cloud_browser only if they fail" in with_cb
    assert "- Cloud browser (cloud_browser)" in with_cb


# 2. a tool the run can load is never "not in this run"; no wholesale "ignore" ────────────────────

LOADABLE_PROMPT = "Use `chrome_batch`. For devtools load `devtools`: `cdp_session`. Use `extract_table`, `context_patch`, `cloud_browser`."


async def test_loadable_tools_are_never_called_absent_and_nothing_says_ignore(monkeypatch) -> None:
    admin = {**_BD_MEMBER, "is_admin": True, "optional_permissions_granted": ["cookies"], "desktop_bridge": "connected"}
    block = await _send(_config(_EXT_HELD, system=LOADABLE_PROMPT), _ext_ctx(admin), monkeypatch)
    absent_line = next(line for line in block.splitlines() if line.startswith("Your instructions name tools"))
    assert "context_patch" in absent_line and "cloud_browser" in absent_line  # neither held nor loadable
    assert "extract_table" not in absent_line and "cdp_session" not in absent_line  # loadable for this run
    assert "Ignore" not in block and "ignore" not in block.lower().split("conflicts with it")[0]


# 3. only categories this run could really load, by the loader's own gates ───────────────────────


async def test_the_load_list_follows_the_requests_real_gates(monkeypatch) -> None:
    member = await _send(_config(_EXT_HELD), _ext_ctx(), monkeypatch)
    for gated in ("cdp_session", "chrome_cookies", "desktop_run_command"):
        assert gated not in member  # not admin / permission not granted / no desktop bridge
    assert "extract_table" in member
    admin = {"is_admin": True, "desktop_bridge": "connected", "optional_permissions_granted": ["cookies"]}
    env_mod.clear_memo()
    granted = await _send(_config(_EXT_HELD), _ext_ctx(admin), monkeypatch)
    for open_now in ("cdp_session", "chrome_cookies", "desktop_run_command"):
        assert open_now in granted


def test_the_block_and_the_loader_share_one_gate_implementation() -> None:
    from matrx_ai.tools.implementations import browser_discovery as bd

    state = {"is_admin": False, "desktop_bridge": "none", "optional_permissions_granted": []}
    listed = {n for names in bd.loadable_chrome_tools(state, registry=_FakeRegistry()).values() for n in names}
    metadata, routing = bd._registry_routing_for_category("devtools", _FakeRegistry())
    gates = bd.chrome_gates(state)
    passed, skipped = bd._filter_tools(
        routing, is_admin=gates.is_admin, granted=gates.granted, desktop_status=gates.desktop_status, metadata_source=metadata
    )
    assert "cdp_session" in skipped["skipped_admin_only"] and "cdp_session" not in listed and not passed


async def test_a_run_without_a_live_extension_is_offered_nothing_to_load(monkeypatch) -> None:
    ctx = _ctx(declared_ui_surface="chrome-extension/assistant", active_tool_executors=[])  # loader would refuse
    block = await _send(_config(_EXT_HELD), ctx, monkeypatch)
    assert "load_chrome_tools(category" not in block


# 4. every family line is derived from what is bound; combinations are truthful ─────────────────

_FILES = ["fs_read", "shell_execute"]


async def test_extension_plus_local_machine_never_says_not_the_persons_computer(monkeypatch) -> None:
    ctx = _ext_ctx(active_sandbox={"target_kind": "local_machine", "root_path": "/Users/x/work"})
    block = await _send(_config([*_EXT_HELD, *_FILES]), ctx, monkeypatch)
    assert "ENVIRONMENT: CHROME EXTENSION" in block
    assert "- Files and commands (fs_read, shell_execute): the person's real computer." in block
    assert "never the person's own computer" not in block
    assert "Workspace root: /Users/x/work" in block and "clear go-ahead" in block


async def test_extension_plus_sandbox_says_the_sandbox(monkeypatch) -> None:
    ctx = _ext_ctx(active_sandbox={"target_kind": "sandbox", "root_path": "/home/agent"})
    block = await _send(_config([*_EXT_HELD, *_FILES]), ctx, monkeypatch)
    assert "- Files and commands (fs_read, shell_execute): the sandbox's own file system and shell." in block
    assert "real computer" not in block and "clear go-ahead" not in block


async def test_local_machine_plus_sandbox_data_never_claims_both(monkeypatch) -> None:
    # one target is bound per run; the target decides what the files line says
    local = await _send(_config(_FILES), _ctx(active_sandbox={"target_kind": "local_machine", "root_path": "/Users/x"}), monkeypatch)
    env_mod.clear_memo()
    sandbox = await _send(_config(_FILES), _ctx(active_sandbox={"target_kind": "sandbox", "root_path": "/home/agent"}), monkeypatch)
    assert "the person's real computer" in local and "sandbox" not in local.split("What your tools reach here:")[1].split("Preferred")[0]
    assert "the sandbox's own file system" in sandbox and "real computer" not in sandbox


async def test_files_tools_with_no_bound_target_do_not_claim_a_place(monkeypatch) -> None:
    block = await _send(_config(_FILES), _ctx(declared_ui_surface="matrx-user/chat"), monkeypatch)
    assert "- Files and commands (fs_read, shell_execute): the workspace attached to this run." in block
    assert "real computer" not in block and "never the person" not in block


async def test_a_scheduled_server_run_for_a_person_with_an_extension_is_cloud(monkeypatch) -> None:
    # no browser-dom payload, no surface, no live extension executor: the person owning one changes nothing
    block = await _send(_config(["web", "cloud_browser"]), _ctx(), monkeypatch)
    assert "ENVIRONMENT: CLOUD" in block and "Chrome extension tools: not available here" in block
    assert "tab_id" not in block


async def test_extension_tools_held_without_a_connected_extension_are_said_unrunnable(monkeypatch) -> None:
    block = await _send(_config(["chrome_batch", "read_page", "update_plan", "web"]), _ctx(), monkeypatch)
    assert "(chrome_batch, read_page): in this run's tool set, but no Chrome extension is connected" in block
    assert "update_plan" not in block.split("What your tools reach here:")[1].split("Browsing")[0]  # also runs in the app


async def test_a_tool_that_also_runs_in_the_app_is_never_called_unrunnable(monkeypatch) -> None:
    block = await _send(_config(["update_plan", "web"]), _ctx(), monkeypatch)
    assert "cannot run" not in block and "Chrome extension tools: not available here" in block


# 7. only tools that really take a tab_id say so, derived from their argument schema ─────────────


async def test_tab_id_is_claimed_only_for_tools_whose_schema_has_it(monkeypatch) -> None:
    block = await _send(_config(_EXT_HELD), _ext_ctx(), monkeypatch)
    line = next(line for line in block.splitlines() if line.strip().startswith("Tools that take a tab_id"))
    assert "read_page" in line and "request_user_takeover" in line
    assert "update_plan" not in line and "chrome_batch" not in line
    assert "Each takes a tab_id" not in block


# 5. the slot order is declared, never the alphabet ────────────────────────────────────────────


def test_the_environment_block_renders_last_by_declaration() -> None:
    from matrx_ai.config.message_config import TURN_CONTEXT_LAST_SLOTS, turn_context_slot_order

    assert TURN_CONTEXT_LAST_SLOTS == (ENVIRONMENT_SLOT,)
    assert turn_context_slot_order(["zzz_late", ENVIRONMENT_SLOT, "person_context", "aaa"])[-1] == ENVIRONMENT_SLOT


def test_the_rendered_turn_context_puts_the_environment_after_every_other_slot() -> None:
    config = _config([])
    ml = config.messages
    ml.attach_turn_context("MEMORY-TEXT", slot="person_context")
    ml.attach_turn_context("LATE-SLOT-TEXT", slot="zz_sorts_after_run_environment")
    ml.attach_turn_context("ENVIRONMENT-TEXT", slot=ENVIRONMENT_SLOT)
    rendered = ml.render_turn_context() or ""
    assert rendered.index("MEMORY-TEXT") < rendered.index("LATE-SLOT-TEXT") < rendered.index("ENVIRONMENT-TEXT")


# memories naming a loadable tool are not flagged absent ───────────────────────────────────────


async def test_reachable_names_include_what_the_run_can_load(monkeypatch) -> None:
    config = _config(_EXT_HELD)
    monkeypatch.setattr(env_mod, "_carried_context", lambda: _ext_ctx())
    reachable = await env_mod.reachable_tool_names(config)
    assert "extract_table" in reachable and "cdp_session" not in reachable and "cloud_browser" not in reachable


# ── round 2: bundle loaders, helper headline, identity switch, mid-run bundle load ──────────────

_BROWSER_BUNDLE = ("cloud_browser", "request_user_takeover")


def _bundles(monkeypatch, members: dict[str, tuple[str, ...]] | None = None) -> None:
    table = members if members is not None else {"bundle:list_browser": _BROWSER_BUNDLE}

    async def fake(lister: str) -> tuple[str, ...]:
        return table[lister]

    monkeypatch.setattr(env_mod, "_bundle_members", fake)


async def test_a_run_that_can_load_cloud_browser_through_a_bundle_is_never_told_it_has_none(monkeypatch) -> None:
    _bundles(monkeypatch)
    config = _config(["web", "bundle:list_browser"], system="Use `cloud_browser` for logins.")
    block = await _send(config, _ctx(), monkeypatch)
    assert "this run holds no interactive browser" not in block
    assert "Cloud browser (cloud_browser): not loaded yet; load it by calling bundle__list_browser" in block
    assert "bundle__list_browser: cloud_browser, request_user_takeover" in block
    assert "Preferred browsing path: cloud_browser (load it first with bundle__list_browser)" in block
    assert "not available in this run" not in block  # cloud_browser is loadable, never "absent"


async def test_an_extension_chat_holding_the_browser_loader_says_cloud_browser_is_loadable(monkeypatch) -> None:
    """The extension surface rows carry the browser bundle (2026-11-18): the run holds its lister, so the
    block names cloud_browser as loadable instead of leaving the agent to conclude it does not exist."""
    _bundles(monkeypatch)
    config = _config(["chrome_batch", "read_page", "find", "navigate", "load_chrome_tools", "bundle:list_browser"])
    block = await _send(config, _ctx(declared_ui_surface="chrome-extension/assistant"), monkeypatch)
    assert "ENVIRONMENT: CHROME EXTENSION" in block
    assert "bundle__list_browser: cloud_browser" in block
    assert "not available in this run" not in block


async def test_an_extension_chat_without_the_loader_is_told_cloud_browser_is_absent(monkeypatch) -> None:
    """The defect before 2026-11-18: no lister held, so cloud_browser is unreachable and the block says what is true."""
    _bundles(monkeypatch)
    config = _config(["chrome_batch", "read_page", "find", "navigate", "load_chrome_tools"])
    block = await _send(config, _ctx(declared_ui_surface="chrome-extension/assistant"), monkeypatch)
    assert "bundle__list_browser" not in block


async def test_loading_the_bundle_mid_run_moves_cloud_browser_to_held(monkeypatch) -> None:
    _bundles(monkeypatch)
    config = _config(["web", "bundle:list_browser"])
    before = await _send(config, _ctx(), monkeypatch)
    config.tools = [*config.tools, "cloud_browser", "request_user_takeover"]
    after = await _send(config, _ctx(), monkeypatch)
    assert "not loaded yet" in before and "not loaded yet" not in after
    assert "- Cloud browser (cloud_browser): a separate browser" in after
    assert "bundle__list_browser: " not in after  # everything it adds is held


async def test_a_bundle_whose_members_cannot_be_read_says_so(monkeypatch) -> None:
    async def boom(lister: str) -> tuple[str, ...]:
        raise RuntimeError("db down")

    monkeypatch.setattr(env_mod, "_bundle_members", boom)
    block = await _send(_config(["web", "bundle:list_browser"]), _ctx(), monkeypatch)
    assert "could not be read just now" in block and "bundle__list_browser" in block


async def test_the_bundle_and_the_loader_share_one_resolution() -> None:

    from matrx_ai.tools.implementations import bundle_lister

    src = stable_source(env_mod._bundle_members)
    assert "bundle_member_names" in src and hasattr(bundle_lister, "bundle_member_names")


async def test_a_helper_of_an_extension_run_is_told_where_the_parent_runs(monkeypatch) -> None:
    block = await _send(_config(["web", "fs_read"]), _ctx(declared_ui_surface="chrome-extension/assistant"), monkeypatch)
    assert "started from their Chrome extension" in block and "hold no tool that reaches their Chrome" in block
    assert "Chrome extension tools: not in this run's tool set; you cannot drive their Chrome." in block


async def test_the_environment_block_does_not_hang_on_the_identity_switch(monkeypatch) -> None:
    config = _config(["web", "cloud_browser"])
    config.system_instruction.include_identity = False
    block = await _send(config, _ctx(), monkeypatch)
    assert "ENVIRONMENT: CLOUD" in block and "cloud_browser" in block


async def test_a_run_with_no_tools_and_no_loaders_gets_no_block(monkeypatch) -> None:
    assert await _send(_config([]), _ctx(), monkeypatch) == ""


async def test_the_desktop_loader_names_what_it_can_load(monkeypatch) -> None:
    from matrx_ai.tools.implementations import desktop_discovery as dd

    monkeypatch.setattr(dd, "_is_matrx_local_tool", lambda t: t.name.startswith("local_"))
    monkeypatch.setattr(dd, "_category_names_cache", None)
    monkeypatch.setattr(dd, "_hard_excluded_tool_names", lambda: frozenset())
    monkeypatch.setattr("matrx_ai.tools.registry.ToolRegistry.get_instance", classmethod(lambda cls: _FakeRegistry()))
    ctx = _ctx(client_capabilities_payloads={"desktop-native": {"platform": "darwin"}})
    block = await _send(_config(["load_desktop_tools", "web"]), ctx, monkeypatch)
    assert 'load_desktop_tools(category="<name>")' in block
    assert "- desktop: local_file, local_mac_apps" in block and "local_windows_ps" not in block


# ── closing round: order of the absent list, tab wording, a golden for a tool-holding run ───────


class _NamesRegistry:
    def __init__(self, names: list[str]) -> None:
        self._names = names

    def list_tool_names(self) -> list[str]:
        return self._names


def test_absent_names_lead_with_the_ones_the_instructions_tell_the_agent_to_call() -> None:
    cdp = [f"cdp_tool_{i:02d}" for i in range(15)]
    registry = _NamesRegistry([*cdp, "context", "context_patch", "desktop_run_command"])
    prompt = (
        "### devtools\n" + ", ".join(f"`{n}`" for n in cdp) + ".\n"
        "Use `context` to read keys, and apply EVERY change with `context_patch`.\n"
        "### other\n`desktop_run_command` needs the desktop app.\n"
    )
    names = tools_named_but_absent(prompt, frozenset(), registry)
    assert names[:2] == ("context", "context_patch")  # told to call: first, in order of mention
    assert names[2:] == (*cdp, "desktop_run_command")  # merely listed: after, in order of mention


async def test_a_long_absent_list_says_how_many_it_left_out(monkeypatch) -> None:
    extra = [f"cdp_tool_{i:02d}" for i in range(30)]
    for n in extra:
        _TOOLS[n] = _row("aidream", "devtools")
    try:
        prompt = ", ".join(f"`{n}`" for n in extra) + ". Use `context_patch` to edit the document."
        block = await _send(_config(["web"], system=prompt), _ctx(), monkeypatch)
    finally:
        for n in extra:
            _TOOLS.pop(n, None)
    line = next(line for line in block.splitlines() if "not available in this run" in line)
    assert line.index("context_patch") < line.index("cdp_tool_00")  # the one it was told to call leads
    assert "more not listed)" in line


async def test_update_plan_and_user_are_not_described_as_acting_on_a_tab(monkeypatch) -> None:
    block = await _send(_config(_EXT_HELD), _ext_ctx(), monkeypatch)
    tab_line = next(line for line in block.splitlines() if line.startswith("- Chrome extension tools that act on a tab"))
    assert "update_plan" not in tab_line and "chrome_batch" not in tab_line and "read_page" in tab_line
    other = next(line for line in block.splitlines() if line.startswith("- Other extension tools"))
    assert "update_plan" in other and "take no tab_id" in other


async def test_the_block_for_a_run_holding_extension_tools_matches_its_golden(monkeypatch) -> None:
    import os
    from pathlib import Path

    golden = Path(__file__).with_name("prompt_blocks") / "golden" / "environment_extension_run.txt"
    block = await _send(_config(_EXT_HELD, system=EXTENSION_PROMPT), _ext_ctx(), monkeypatch)
    if os.environ.get("PROMPT_BLOCKS_REGEN_GOLDEN") == "1":
        golden.write_text(block + "\n")
        return
    assert block + "\n" == golden.read_text(), "the ENVIRONMENT block's wording moved for a tool-holding run (regen with PROMPT_BLOCKS_REGEN_GOLDEN=1 if intended)"


# ── how to work the page: generated from the held tools, never hand-written per agent ─────────


@pytest.mark.asyncio
async def test_an_extension_run_is_told_how_to_work_the_page(monkeypatch) -> None:
    block = await _send(
        _config(["navigate", "computer", "read_page", "find", "chrome_batch"]),
        _ctx(declared_ui_surface="chrome-extension/assistant"),
        monkeypatch,
    )
    assert "How to work the page:" in block
    assert "picture" in block and "act from it" in block
    assert "read_page" in block.split("How to work the page:")[1]
    assert "chrome_batch" in block.split("How to work the page:")[1]
    assert "Do not re-read a page you were just shown" in block


@pytest.mark.asyncio
async def test_page_guidance_never_names_a_tool_the_run_does_not_hold(monkeypatch) -> None:
    block = await _send(
        _config(["navigate", "read_page"]),
        _ctx(declared_ui_surface="chrome-extension/assistant"),
        monkeypatch,
    )
    guidance = block.split("How to work the page:")[1]
    assert "chrome_batch" not in guidance and "find" not in guidance.replace("findings", "")
