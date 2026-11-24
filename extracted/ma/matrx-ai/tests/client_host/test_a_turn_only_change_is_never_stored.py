"""A CHANGE FOR ONE TURN IS NEVER STORED WITH THE CHAT (CGU-10 IMG7 #2, 2026-11-11).

The class (IMG6 #1): a setting meant for ONE call or ONE turn lands on the canonical
``UnifiedConfig``, which the turn's persist stores (``to_storage_dict`` → the conversation's
config), so every later turn inherits it. IMG7 found two more members on the executor's own paths:

* an overload reroute to a fallback model set ``offering_id = None`` on the canonical config —
  one provider overload erased the person's own model pin from the chat (attack A1);
* the iteration-ceiling wrap-up and the loop-guard pause set ``config.tools = []`` — the stored
  ``tools`` went empty (attack A2).

Both now run THIS turn only: the reroute through ``begin_model_this_turn_only`` (the row keeps the
model and pin it had), the tool strip through ``tools_off_this_turn_only``. What each test is FOR:

* revert the reroute to bare writes (drop ``begin_model_this_turn_only``) → the stored pin is gone;
* revert the ceiling strip to ``config.tools = []`` → the stored ``tools`` is empty;
* drop the resolver's ``end_tools_off_this_turn_only`` → the next turn starts tool-less.

The provider is the in-repo mock (no network).
"""

from __future__ import annotations

import uuid
from typing import Any

import pytest
from matrx_utils.source_guard import stable_source

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_execute_with_store import (  # noqa: E402
    _MOCK_MODEL,
    InMemoryStore,
    StaticCatalog,
)
from test_the_iteration_ceiling_ends_with_an_answer import (  # noqa: E402
    TOOL,
    _config,
    _set_context,
    _tool_hungry_model,
    probe_tool,  # noqa: F401 — fixture
)

PINNED = "pinned-offering-of-the-person"
FALLBACK = "mock-fallback-model"


def _configure() -> None:
    fallback = dict(_MOCK_MODEL, id=str(uuid.uuid4()), name=FALLBACK)
    configure_ext(
        conversation_store=InMemoryStore(),
        model_catalog=StaticCatalog([_MOCK_MODEL, fallback]),
        api_key_resolver=lambda name: "not-a-real-key",
    )


def _stored(config: Any) -> dict[str, Any]:
    return config.to_storage_dict()


@pytest.mark.asyncio
async def test_the_ceiling_wrap_up_never_stores_an_empty_tool_list(probe_tool, monkeypatch) -> None:  # noqa: F811
    from matrx_ai.orchestrator.executor import execute_ai_request

    offered = _tool_hungry_model(monkeypatch, ignores_empty_tool_list=False)
    _configure()
    _set_context(sub_agent=False)

    completed = await execute_ai_request(_config(), max_iterations=2)

    assert offered[-1] == [], "the wrap-up turn was offered tools (the strip itself must still happen)"
    stored = _stored(completed.request.config)
    assert stored["config"].get("tools") == [TOOL], (
        f"the ceiling's tool-less turn was stored with the chat: {stored['config'].get('tools')!r}"
    )


def test_the_next_turn_gets_its_tools_back() -> None:
    config = _config()
    config.tools_off_this_turn_only()
    config.tools_off_this_turn_only()  # idempotent: the first snapshot is kept
    assert config.tools == [] and config.custom_tools == []
    assert _stored(config)["config"]["tools"] == [TOOL]
    assert config.end_tools_off_this_turn_only() is True
    assert config.tools == [TOOL]
    assert config.end_tools_off_this_turn_only() is False


def test_the_resolver_ends_a_turn_only_tool_strip() -> None:
    """The next turn (process cache) starts from the chat's own tools: the resolver's turn exit
    restores them before anything else reads the config."""

    from matrx_ai.agents import resolver

    source = stable_source(resolver)
    assert "config.end_tools_off_this_turn_only()" in source


@pytest.mark.asyncio
async def test_an_overload_reroute_keeps_the_persons_model_pin(monkeypatch) -> None:
    from matrx_ai.orchestrator import executor as executor_mod
    from matrx_ai.orchestrator import overload_reroute
    from matrx_ai.orchestrator.overload_reroute import OverloadPolicy, RerouteDecision, RerouteNote
    from matrx_ai.providers.errors import RetryableError
    from matrx_ai.providers.mock.mock_api import MockChat

    _configure()
    _set_context(sub_agent=False)

    sent_models: list[str] = []
    original_raw_spec = MockChat._raw_spec

    def _raw_spec(unified_config: Any) -> dict[str, Any]:
        raw = dict(original_raw_spec(unified_config) or {})
        sent_models.append(str(unified_config.model))
        raw["tool_calls"] = []
        if len(sent_models) == 1:
            raw["fail"] = True
            raw["error_message"] = "overloaded_error: the provider is overloaded"
        return raw

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))
    monkeypatch.setattr(
        executor_mod,
        "classify_provider_error",
        lambda _provider, exc: RetryableError(
            error_type="provider_overloaded", message=str(exc), status_code=529, is_retryable=True
        ),
    )

    async def _policy(*_a: Any, **_k: Any) -> OverloadPolicy:
        return OverloadPolicy(retry_max_attempts=0, fallback_ref=FALLBACK)

    async def _no_ladder(*_a: Any, **_k: Any) -> None:
        return None

    def _decide(**kw: Any) -> RerouteDecision:
        if kw["current_model"] == FALLBACK:
            return RerouteDecision(action="give_up", reason="already on the fallback")
        return RerouteDecision(
            action="reroute",
            to_model=FALLBACK,
            reason="overloaded",
            note=RerouteNote(
                from_model=kw["current_model"],
                to_model=FALLBACK,
                attempts_on_model=kw["attempts_on_model"],
                error_type="overloaded",
                reason="overloaded",
            ),
        )

    monkeypatch.setattr(overload_reroute, "load_overload_policy", _policy)
    monkeypatch.setattr(overload_reroute, "load_offering_ladder", _no_ladder)
    monkeypatch.setattr(overload_reroute, "decide_overload_action", _decide)

    # The client-host catalog has no offering rows, so a class pin cannot route there: the stand-in
    # resolves the person's pin as the model's own route (what a server catalog does with a real one).
    from matrx_ai.catalog import resolve as catalog_resolve

    real_resolve = catalog_resolve.resolve_call_profile

    async def _resolve(model_ref: str, endpoint_hint: str | None = None, **kw: Any) -> Any:
        kw["offering_id"] = None
        return await real_resolve(model_ref, endpoint_hint, **kw)

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _resolve)

    config = _config()
    config.tools = []
    config.adopt_model_for_conversation(config.model, offering_id=PINNED)  # the person's own pin
    completed = await execute_ai_request_quiet(config)

    assert sent_models[:2] == ["mock-model", FALLBACK], f"the reroute did not happen: {sent_models}"
    stored = _stored(completed.request.config)
    assert stored["model"] == "mock-model", f"the fallback was stored as the chat's model: {stored['model']!r}"
    assert stored["config"].get("offering_id") == PINNED, (
        f"one overload erased the person's model pin: {stored['config'].get('offering_id')!r}"
    )
    # The next turn starts from the person's own model again.
    completed.request.config.end_model_this_turn_only()
    assert completed.request.config.model == "mock-model"
    assert completed.request.config.offering_id == PINNED


@pytest.mark.asyncio
async def test_a_sibling_offering_reroute_runs_this_turn_only(monkeypatch) -> None:
    """CGU-10 IMG8 #4 (plant P2 was green across 1,461 tests): the same-model sibling-offering reroute
    sets ``runtime_offering_id`` and swaps ``model`` for the canonical id. Through the real loop, the
    stored chat keeps the person's model name and the next turn starts with no sibling pin. Red when
    ``begin_model_this_turn_only()`` is removed from that branch."""
    from matrx_ai.orchestrator import executor as executor_mod
    from matrx_ai.orchestrator import overload_reroute
    from matrx_ai.orchestrator.overload_reroute import (
        OfferingLadder,
        OverloadPolicy,
        RerouteDecision,
        RerouteNote,
    )
    from matrx_ai.providers.errors import RetryableError
    from matrx_ai.providers.mock.mock_api import MockChat

    _configure()
    _set_context(sub_agent=False)
    sent: list[tuple[str, Any]] = []
    original_raw_spec = MockChat._raw_spec

    def _raw_spec(unified_config: Any) -> dict[str, Any]:
        raw = dict(original_raw_spec(unified_config) or {})
        sent.append((str(unified_config.model), getattr(unified_config, "runtime_offering_id", None)))
        raw["tool_calls"] = []
        if len(sent) == 1:
            raw["fail"] = True
            raw["error_message"] = "overloaded_error: the provider is overloaded"
        return raw

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))
    monkeypatch.setattr(
        executor_mod,
        "classify_provider_error",
        lambda _provider, exc: RetryableError(
            error_type="provider_overloaded", message=str(exc), status_code=529, is_retryable=True
        ),
    )

    async def _policy(*_a: Any, **_k: Any) -> OverloadPolicy:
        return OverloadPolicy(retry_max_attempts=0, fallback_ref=None)

    async def _ladder(*_a: Any, **_k: Any) -> OfferingLadder:
        return OfferingLadder(
            canonical_model_id=_MOCK_MODEL["id"], current_offering_id=PINNED, sibling_offering_ids=["sibling"]
        )

    def _decide(**kw: Any) -> RerouteDecision:
        if kw.get("current_offering_id") == "sibling" or len(sent) > 1:
            return RerouteDecision(action="give_up", reason="already on the sibling")
        return RerouteDecision(
            action="reroute_offering",
            to_offering_id="sibling",
            reason="overloaded",
            note=RerouteNote(
                scope="offering",
                from_model=kw["current_model"],
                to_model=kw["current_model"],
                from_offering_id=PINNED,
                to_offering_id="sibling",
                attempts_on_model=kw["attempts_on_model"],
                error_type="overloaded",
                reason="overloaded",
            ),
        )

    monkeypatch.setattr(overload_reroute, "load_overload_policy", _policy)
    monkeypatch.setattr(overload_reroute, "load_offering_ladder", _ladder)
    monkeypatch.setattr(overload_reroute, "decide_overload_action", _decide)
    from matrx_ai.catalog import resolve as catalog_resolve

    real_resolve = catalog_resolve.resolve_call_profile

    async def _resolve(model_ref: str, endpoint_hint: str | None = None, **kw: Any) -> Any:
        kw["offering_id"] = None
        return await real_resolve(model_ref, endpoint_hint, **kw)

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _resolve)

    config = _config()
    config.tools = []
    config.adopt_model_for_conversation(config.model, offering_id=PINNED)  # the person's own pin
    completed = await execute_ai_request_quiet(config)

    assert len(sent) >= 2 and sent[1][1] == "sibling", f"the sibling reroute did not happen: {sent}"
    stored = _stored(completed.request.config)
    assert stored["model"] == "mock-model", f"the sibling's canonical id was stored as the model: {stored['model']!r}"
    assert stored["config"].get("offering_id") == PINNED
    completed.request.config.end_model_this_turn_only()
    assert completed.request.config.runtime_offering_id is None, "the sibling pin carries into the next turn"
    assert completed.request.config.model == "mock-model"


def test_a_failed_forced_member_send_stores_the_chats_own_tools() -> None:
    """CGU-10 IMG8 #3: the required-member gate narrows the belt to the missing members' tools with
    ``tool_choice='required'`` and restored them only after the provider answered — a failed or
    cancelled forced send stored the narrowed list. The narrowing is turn-only now."""
    config = _config()
    config.tool_choice = "auto"
    config.tools_narrowed_this_turn_only(["member_tool"], [], tool_choice="required")
    assert config.tools == ["member_tool"] and config.tool_choice == "required"
    stored = _stored(config)["config"]
    assert stored["tools"] == [TOOL], f"the narrowed belt was stored: {stored['tools']!r}"
    assert stored.get("tool_choice") == "auto"
    assert config.end_tools_off_this_turn_only() is True
    assert config.tools == [TOOL] and config.tool_choice == "auto"


def test_the_required_member_gate_narrows_through_the_turn_only_helper() -> None:

    from matrx_ai.orchestrator import executor

    source = stable_source(executor)
    assert "tools_narrowed_this_turn_only(\n                        list(_rm_report.forceable_names)" in source


# ── THE CLASS, first line (static, cheap): only the helpers write the route; belts narrow turn-only ──
#: Functions outside the orchestrator that are handed the STORED ``request.config`` mid-turn (their
#: belt writes are scanned too). Every orchestrator module is scanned whole.
_STORED_CONFIG_FUNCTIONS = {
    "matrx_ai.providers.free_tier_models": ("swap_for_free_tier",),
    "matrx_ai.providers.baa_gate": ("swap_for_baa",),
    "matrx_ai.orchestrator.loop_guard": ("disable_failing_tool",),
    "matrx_ai.providers.small_model_tools": ("strip_small_model_optional_tools",),
}
#: The only package functions that may write a config's route outside the helpers, and why.
ROUTE_WRITE_WAIVERS = {
    "matrx_ai.providers.device.route_guard.refuse_device_move": (
        "puts a device-served run's model back after a host step moved it, then refuses the run"
    ),
    "matrx_ai.providers.unified_client._build_provider_wire_config": (
        "writes the provider's model id on the per-call WIRE copy, never the stored config"
    ),
}


def test_no_package_path_writes_a_route_outside_the_helpers() -> None:
    """Every module of the package (the helpers' own module aside): a model, class pin or device is
    written only through ``model_this_turn_only`` / ``swap_model_this_turn_only`` (a stand-in) or
    ``apply_overrides`` / ``adopt_model_for_conversation`` (a chosen model). Scope-aware by
    construction: an earlier snapshot elsewhere in the function no longer excuses a bare write."""
    from pathlib import Path

    import matrx_ai
    from matrx_ai.testing.route_write_guard import scan_tree, stale_waivers

    root = Path(matrx_ai.__file__).parent
    found = scan_tree(
        root, "matrx_ai", allowed=ROUTE_WRITE_WAIVERS, skip_modules=["matrx_ai.config.unified_config"]
    )
    assert not found, "a route is written outside the turn-only helpers:\n" + "\n".join(found)
    assert not stale_waivers(root, "matrx_ai", ROUTE_WRITE_WAIVERS), "a waiver no longer writes: delete it"


def test_no_mid_turn_path_narrows_the_stored_belt_bare() -> None:
    import importlib
    import pkgutil

    import matrx_ai.orchestrator as orchestrator
    from matrx_ai.testing.route_write_guard import scan_source

    found: list[str] = []
    for info in pkgutil.iter_modules(orchestrator.__path__, "matrx_ai.orchestrator."):
        if info.ispkg:
            continue
        module = importlib.import_module(info.name)
        found += scan_source(stable_source(module), info.name, belt=True, allowed=ROUTE_WRITE_WAIVERS)
    for name, functions in _STORED_CONFIG_FUNCTIONS.items():
        module = importlib.import_module(name)
        found += scan_source(stable_source(module), name, functions=functions, belt=True)
    assert not found, "a turn-only change can be stored with the chat:\n" + "\n".join(found)


#: AND-V IMG9's sixteen shapes, plus the P5 shape (a snapshot earlier in the SAME function, then a
#: bare write) and a decoy function named ``begin``. Every one must be caught.
_CHECKER_SHAPES = {
    "bare model": "def f(r):\n    r.config.model = 'm'\n",
    "P5 earlier snapshot": (
        "def f(r, a, b):\n    if a:\n        r.config.begin_model_this_turn_only()\n"
        "        r.config.runtime_offering_id = 's'\n    if b:\n        r.config.model = 'fallback'\n"
        "        r.config.offering_id = None\n"
    ),
    "begin decoy": "def f(r):\n    begin()\n    r.config.model = 'm'\n",
    "alias": "def f(r):\n    cfg = r.config\n    cfg.model = 'm'\n",
    "alias of alias": "def f(r):\n    a = r.config\n    b = a\n    b.offering_id = None\n",
    "tuple target": "def f(r):\n    r.config.model, x = 'm', 1\n",
    "dict update": "def f(r):\n    r.config.__dict__.update({'model': 'm'})\n",
    "dict setitem": "def f(r):\n    r.config.__dict__.__setitem__('model', 'm')\n",
    "replace": "from dataclasses import replace\ndef f(r):\n    r.config = replace(r.config, model='m')\n",
    "model_copy": "def f(r):\n    r.config = r.config.model_copy(update={'model': 'm'})\n",
    "branch snapshot": (
        "def f(r, a):\n    if a:\n        r.config.begin_model_this_turn_only()\n    else:\n        pass\n"
        "    r.config.model = 'm'\n"
    ),
    "setattr const": "def f(config):\n    setattr(config, 'offering_id', None)\n",
    "setattr loop": "def f(config):\n    for p in ('offering_id', 'runtime_offering_id'):\n        setattr(config, p, None)\n",
    "lambda setattr": "def f(r):\n    g = lambda: setattr(r.config, 'model', 'm')\n    g()\n",
    "getattr setter": "def f(r):\n    s = getattr(r.config, '__setattr__')\n    s('model', 'm')\n",
    "dunder setattr": "def f(r):\n    r.config.__setattr__('model', 'm')\n",
    "partial setattr": "import functools\ndef f(r):\n    s = functools.partial(setattr, r.config)\n    s('model', 'm')\n",
    "request helper": "def swap(request_config):\n    request_config.model = 'm'\n",
    # CGU-10 AND-IMG11: a config bound to ANY name, by type or by flow.
    "typed param": "def f(uc: UnifiedConfig):\n    uc.model = 'm'\n",
    "typed optional param": "def f(uc: 'UnifiedConfig | None'):\n    uc.offering_id = None\n",
    "qualified type": "def f(uc: unified_config.UnifiedConfig):\n    uc.model = 'm'\n",
    "annotated local": "def f(r):\n    uc: UnifiedConfig = load()\n    uc.model = 'm'\n",
    "constructed": "def f(r):\n    uc = UnifiedConfig(model='a')\n    uc.model = 'b'\n",
    "factory": "async def f(d):\n    uc = UnifiedConfig.from_dict(d)\n    uc.served_via = 'x'\n",
    "deep copy": "import copy\ndef f(r):\n    uc = copy.deepcopy(r.config)\n    uc.model = 'm'\n",
    "model_copy then write": "def f(r):\n    uc = r.config.model_copy()\n    setattr(uc, 'model', 'm')\n",
    "walrus": "def f(r):\n    if (uc := r.config):\n        uc.model = 'm'\n",
    "kw-only typed": "def f(*, uc: UnifiedConfig):\n    uc.runtime_offering_id = 'x'\n",
    # CGU-10 AND-IMG12 #4: the cheap shapes the IMG11 checker wrote that the scan missed.
    "private cfg attribute": "def f(self):\n    self._cfg.model = 'm'\n",
    "tuple unpack alias": "def f(config):\n    uc, n = config, 1\n    uc.model = 'm'\n",
    "for over configs": "def f(configs):\n    for uc in configs:\n        uc.model = 'm'\n",
    "with as": "def f(r):\n    with r.config as uc:\n        uc.offering_id = None\n",
    "subscript of configs": "def f(configs):\n    configs[0].model = 'm'\n",
    "object setattr": "def f(uc: UnifiedConfig):\n    object.__setattr__(uc, 'model', 'm')\n",
    "vars subscript": "def f(config):\n    vars(config)['model'] = 'm'\n",
    "dict subscript": "def f(config):\n    config.__dict__['model'] = 'm'\n",
    "vars update": "def f(config):\n    vars(config).update(model='m')\n",
}
_CHECKER_BELT_SHAPES = {
    "bare list": "def f(r):\n    r.config.tools = []\n",
    "narrowed list": "def f(r, x):\n    r.config.tools = list(x)\n",
    "append": "def f(r):\n    r.config.tools.append('t')\n",
    "remove": "def f(r):\n    r.config.tools.remove('t')\n",
    "clear": "def f(r):\n    r.config.custom_tools.clear()\n",
    "slice": "def f(r):\n    r.config.tools[:] = []\n",
    "alias append": "def f(r):\n    cfg = r.config\n    cfg.tools.extend([])\n",
    "computed setattr": "def f(config, n):\n    setattr(config, n, [])\n",
}


@pytest.mark.parametrize("shape", sorted(_CHECKER_SHAPES))
def test_the_static_guard_sees_every_route_write_shape(shape: str) -> None:
    from matrx_ai.testing.route_write_guard import scan_source

    assert scan_source(_CHECKER_SHAPES[shape], "planted"), f"the guard missed: {shape}"


@pytest.mark.parametrize("shape", sorted(_CHECKER_BELT_SHAPES))
def test_the_static_guard_sees_every_belt_write_shape(shape: str) -> None:
    from matrx_ai.testing.route_write_guard import scan_source

    assert scan_source(_CHECKER_BELT_SHAPES[shape], "planted", belt=True), f"the guard missed: {shape}"


def test_the_static_guard_passes_the_helpers_and_a_child() -> None:
    from matrx_ai.testing.route_write_guard import scan_source

    assert not scan_source("def f(r):\n    r.config.model_this_turn_only('m')\n", "ok")
    assert not scan_source("def f(r):\n    r.config.tools_narrowed_this_turn_only([], [])\n", "ok", belt=True)
    assert not scan_source("def f(child):\n    child.model = 'm'\n", "ok")
    assert not scan_source("def f(child: ChildCall):\n    child.model = 'm'\n", "ok")
    assert not scan_source("def f(r):\n    uc = make_child()\n    uc.model = 'm'\n", "ok")
    assert not scan_source("def f(uc: UnifiedConfig):\n    uc.temperature = 1\n", "ok")
    assert not scan_source("def f(config):\n    config.temperature = 1\n", "ok")


# ── THE CLASS, real layer (behavioural): what the row stores never moves outside the sanctioned doors ──
def _route_moves() -> dict[str, Any]:
    """Every write shape the static guard looks for, done for real on a live config."""
    import dataclasses

    def bare(c: Any) -> Any:
        c.model = "stand-in"
        c.offering_id = None
        return c

    def alias(c: Any) -> Any:
        cfg = c
        cfg.model = "stand-in"
        return c

    def via_setattr(c: Any) -> Any:
        for name, value in (("model", "stand-in"), ("offering_id", None)):
            setattr(c, name, value)
        return c

    def via_dict(c: Any) -> Any:
        c.__dict__.update({"model": "stand-in"})
        return c

    def via_replace(c: Any) -> Any:
        return dataclasses.replace(c, model="stand-in", offering_id=None)  # noqa: dataclass-replace-ok

    def after_an_unrelated_snapshot(c: Any) -> Any:
        c.begin_model_this_turn_only()  # someone else's snapshot, then closed
        c.end_model_this_turn_only()
        c.model = "stand-in"
        return c

    return {
        "bare": bare,
        "alias": alias,
        "setattr": via_setattr,
        "__dict__": via_dict,
        "replace": via_replace,
        "unrelated snapshot": after_an_unrelated_snapshot,
    }


@pytest.mark.parametrize("shape", sorted(_route_moves()))
def test_the_row_never_stores_a_route_moved_outside_the_doors(shape: str, capsys) -> None:
    """CGU-10 IMG9 #2: a behavioural guarantee — whatever the write shape, the stored row keeps the
    person's model and pin, and the move is announced (stderr + ``stored_route_unsanctioned_write``)."""
    config = _config()
    config.adopt_model_for_conversation("mock-model", offering_id=PINNED)
    moved = _route_moves()[shape](config)
    assert moved.model == "stand-in", "the plant did not move the live model"
    stored = _stored(moved)
    assert stored["model"] == "mock-model", f"{shape}: the stand-in was stored: {stored['model']!r}"
    assert stored["config"].get("offering_id") == PINNED, f"{shape}: the person's pin was dropped"
    assert "outside the sanctioned doors" in capsys.readouterr().err, f"{shape}: the move was silent"


def test_the_sanctioned_doors_are_stored_and_silent(capsys) -> None:
    from matrx_ai.config.llm_params import LLMParams

    config = _config()
    config.adopt_model_for_conversation("mock-model", offering_id=PINNED)
    config.model_this_turn_only("stand-in", swap_reason="free_tier")  # a stand-in: runs, never stored
    assert config.model == "stand-in" and config.offering_id is None
    assert _stored(config)["model"] == "mock-model"
    assert _stored(config)["config"].get("offering_id") == PINNED
    # The person picks another model mid-turn while the stand-in runs: that IS the chat's model now.
    config.apply_overrides(LLMParams(model="persons-new-pick"))
    assert _stored(config)["model"] == "persons-new-pick"
    assert config.end_model_this_turn_only() is True
    assert config.model == "persons-new-pick"
    # "This message only" over a stand-in: the chat keeps its own.
    config.model_this_turn_only("stand-in", swap_reason="free_tier")
    config.begin_model_this_turn_only()
    config.apply_overrides(LLMParams(model="just-this-message"))
    assert _stored(config)["model"] == "persons-new-pick"
    assert "outside the sanctioned doors" not in capsys.readouterr().err


async def execute_ai_request_quiet(config: Any) -> Any:
    from matrx_ai.orchestrator.executor import execute_ai_request

    return await execute_ai_request(config, max_iterations=2)


def test_no_executor_path_strips_tools_on_the_stored_config() -> None:
    """The class, not the instance: the ceiling wrap-up, the drain's wrap-up re-strip and the
    loop-guard pause all go through ``tools_off_this_turn_only``. A bare ``config.tools = []`` (or
    a bare reroute's ``offering_id = None`` with no snapshot before it) is the stored-config defect."""
    import re

    from matrx_ai.orchestrator import executor

    source = stable_source(executor)
    assert not re.search(r"\.config\.tools\s*=\s*\[\]", source), "a bare tool strip writes the stored chat"
    for match in re.finditer(r"\.config\.offering_id\s*=\s*None", source):
        before = source[max(0, match.start() - 1500) : match.start()]
        assert "begin_model_this_turn_only()" in before, "a reroute clears the pin with no turn-only snapshot"
    assert source.count("tools_off_this_turn_only()") >= 3


# ── Every swap / strip / reroute path, through the REAL executor: the stored chat is unchanged ──────
def _scripted_model(monkeypatch, script: list[list[dict[str, Any]]]) -> list[tuple[str, list[str], Any]]:
    """The mock answers call N with ``script[N]`` tool calls (text when empty / past the end). Returns
    ``(model, tools offered, tool_choice)`` for every provider call."""
    from matrx_ai.providers.mock.mock_api import MockChat

    seen: list[tuple[str, list[str], Any]] = []
    original_raw_spec = MockChat._raw_spec
    monkeypatch.setattr(MockChat, "_history_has_tool_result", staticmethod(lambda unified_config: False))

    def _raw_spec(unified_config: Any) -> dict[str, Any]:
        raw = dict(original_raw_spec(unified_config) or {})
        seen.append(
            (str(unified_config.model), [str(t) for t in (unified_config.tools or [])], unified_config.tool_choice)
        )
        n = len(seen) - 1
        raw["tool_calls"] = list(script[n]) if n < len(script) else []
        return raw

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))
    return seen


def _persons_config() -> Any:
    config = _config()
    config.adopt_model_for_conversation("mock-model", offering_id=PINNED)
    return config


def _assert_the_row_is_the_persons(completed: Any, *, tools: list[str]) -> None:
    stored = _stored(completed.request.config)
    assert stored["model"] == "mock-model", f"the stand-in was stored as the chat's model: {stored['model']!r}"
    assert stored["config"].get("offering_id") == PINNED, (
        f"the person's pin was not stored: {stored['config'].get('offering_id')!r}"
    )
    assert stored["config"].get("tools") == tools, f"a turn-only belt was stored: {stored['config'].get('tools')!r}"


@pytest.fixture
def _pin_resolves_as_the_models_own_route(monkeypatch):
    from matrx_ai.catalog import resolve as catalog_resolve

    real_resolve = catalog_resolve.resolve_call_profile

    async def _resolve(model_ref: str, endpoint_hint: str | None = None, **kw: Any) -> Any:
        kw["offering_id"] = None
        return await real_resolve(model_ref, endpoint_hint, **kw)

    monkeypatch.setattr(catalog_resolve, "resolve_call_profile", _resolve)


@pytest.mark.asyncio
async def test_a_free_tier_stand_in_runs_and_the_row_keeps_the_persons_model(
    monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route  # noqa: F811
) -> None:
    from matrx_ai.providers import free_tier_models as ftm

    _configure()
    _set_context(sub_agent=False)
    seen = _scripted_model(monkeypatch, [])
    monkeypatch.setattr(ftm, "_resolver", lambda ctx: ftm.FreeTierPolicy(tier="guest", max_cost_rating=2))

    async def _target(original: str, policy: Any, **_kw: Any) -> Any:
        return (FALLBACK, "") if original == "mock-model" else None

    async def _quiet(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(ftm, "free_tier_target", _target)
    monkeypatch.setattr(ftm, "tell_model_swapped", _quiet)
    monkeypatch.setattr(ftm, "admit_free_tier_model", _quiet)

    completed = await execute_ai_request_quiet(_persons_config())

    assert seen and seen[0][0] == FALLBACK, f"the stand-in did not answer: {seen}"
    _assert_the_row_is_the_persons(completed, tools=[TOOL])


@pytest.mark.asyncio
async def test_a_hipaa_stand_in_runs_and_the_row_keeps_the_persons_model(
    monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route  # noqa: F811
) -> None:
    from types import SimpleNamespace

    from matrx_ai.providers import baa_gate

    _configure()
    _set_context(sub_agent=False)
    seen = _scripted_model(monkeypatch, [])
    policy = SimpleNamespace(covers=lambda vendor, interaction: False, chat_standin_model=FALLBACK)

    async def _policy(*_a: Any, **_k: Any) -> Any:
        return policy

    async def _quiet(*_a: Any, **_k: Any) -> Any:
        return []

    monkeypatch.setattr(baa_gate, "baa_policy", _policy)
    monkeypatch.setattr(baa_gate, "baa_interaction", lambda profile: "chat")
    for name in ("_refuse_above_free_tier", "_tell_once", "admit_baa", "apply_baa_features", "_label"):
        monkeypatch.setattr(baa_gate, name, _quiet)

    completed = await execute_ai_request_quiet(_persons_config())

    assert seen and seen[0][0] == FALLBACK, f"the stand-in did not answer: {seen}"
    _assert_the_row_is_the_persons(completed, tools=[TOOL])


@pytest.mark.asyncio
async def test_a_small_model_strip_runs_this_turn_only(
    monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route  # noqa: F811
) -> None:
    """CGU-10 IMG9 #7: the small-model strip narrowed the stored belt, and with no authored list it
    stored the pre-strip belt (the automatic lister included) as authored."""
    from matrx_ai.providers import small_model_tools as smt
    from matrx_ai.providers import tool_adaptation

    _configure()
    _set_context(sub_agent=False)
    from matrx_connect.context.app_context import get_app_context

    get_app_context().metadata[tool_adaptation.SMALL_MODEL_OPTIONAL_TOOLS_KEY] = ["surface_lister"]
    monkeypatch.setattr(smt, "is_small_model", lambda rating: True)
    monkeypatch.setattr(smt, "automatic_tool_names", lambda config: {"surface_lister"})
    seen = _scripted_model(monkeypatch, [])
    config = _persons_config()
    config.tools = [TOOL, "surface_lister"]
    config.authored_tools = [TOOL]

    completed = await execute_ai_request_quiet(config)

    assert seen and "surface_lister" not in seen[0][1], f"the lister was offered to a small model: {seen}"
    _assert_the_row_is_the_persons(completed, tools=[TOOL, "surface_lister"])
    assert _stored(completed.request.config)["config"]["authored_tools"] == [TOOL], (
        "the automatic lister was made authored (permanent)"
    )


def test_the_small_model_strip_never_writes_authored_tools_on_a_bare_config(monkeypatch) -> None:
    from types import SimpleNamespace

    from matrx_ai.providers import small_model_tools as smt

    monkeypatch.setattr(smt, "_optional_tool_names", lambda: {"surface_lister"})
    monkeypatch.setattr(smt, "is_small_model", lambda rating: True)
    monkeypatch.setattr(smt, "automatic_tool_names", lambda config: {"surface_lister"})
    config = SimpleNamespace(tools=["a", "surface_lister"], custom_tools=[], authored_tools=None)
    assert smt.strip_small_model_optional_tools(config, SimpleNamespace(model_cost_rating=1)) is not None
    assert config.tools == ["a"]
    assert config.authored_tools is None, "the pre-strip belt (lister included) was written as authored"


@pytest.mark.asyncio
async def test_after_a_forced_member_turn_the_next_turn_gets_the_full_belt(
    monkeypatch, probe_tool, _pin_resolves_as_the_models_own_route  # noqa: F811
) -> None:
    """AND-V IMG9 P8: with the gate's own snapshot, the restore must close it. Skipped, the next
    provider turn of the same chat turn ran on the narrowed belt (``tool_choice='required'``)."""
    from matrx_ai.orchestrator import executor as executor_mod

    _configure()
    _set_context(sub_agent=False)
    member_call = {"name": TOOL, "arguments": {"path": "member"}}
    seen = _scripted_model(monkeypatch, [[], [member_call], []])
    from matrx_ai.orchestrator.required_members import RequiredMember, RequiredMemberReport

    member = RequiredMember(agent_id="member-agent", role_title="The Member", projected_name="member_tool")
    report = RequiredMemberReport(required=[member], missing=[member], unenforceable=[])
    calls = {"n": 0}

    def _gate(current_request: Any, state: Any) -> tuple[str, Any, bool]:
        calls["n"] += 1
        return ("force", report, False) if calls["n"] == 1 else ("proceed", None, False)

    monkeypatch.setattr(executor_mod, "_required_member_gate", _gate)
    config = _persons_config()
    config.tool_choice = "auto"

    from matrx_ai.orchestrator.executor import execute_ai_request

    completed = await execute_ai_request(config, max_iterations=4)

    assert len(seen) >= 3, f"the forced turn and the one after it did not both run: {seen}"
    assert seen[1][1] == ["member_tool"] and seen[1][2] == "required", f"the forced turn was not narrowed: {seen[1]}"
    assert seen[2][1] == [TOOL], f"the turn after the forced one ran on the narrowed belt: {seen[2]}"
    assert seen[2][2] != "required", f"the turn after the forced one is still forced: {seen[2]}"
    assert completed.request.config.tools_turn_only_restore is None, "the gate's snapshot was left open"
    _assert_the_row_is_the_persons(completed, tools=[TOOL])
