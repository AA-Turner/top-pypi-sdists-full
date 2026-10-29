"""FORCING GUARD — no provider call reaches the wire without the per-call spend cap check.

The break this names: a provider dispatch path (a new client, a new seam caller, a batch lane, a
direct SDK send) that sends while ``admit_call_spend_cap`` was never asked, so a workflow step's
``max_call_cost_usd`` stops meaning anything on that path.

Three layers, each able to fail alone:

1. STRUCTURE of the seam (AST over the real source): ``admit_guardrails`` asks the cap first and
   unconditionally; ``UnifiedAIClient._dispatch_with_billing_net`` calls ``admit_guardrails`` before
   its dispatch loop, with the only earlier exits being the nested-pool pass-through and capture
   mode; ``_dispatch_admitted`` is reachable from nowhere else; every ``<client>.execute(...)`` in
   the unified client and STT lives inside a callable handed to the seam; the set of seam callers is
   pinned; every class with ``async def execute`` is a client the unified client builds.
2. CENSUS of vendor sends: any module that calls a vendor SDK's generation/embedding/rerank method
   must either define an ``execute`` client (reached only through the seam) or be named below with
   its reason. A new direct sender turns this red until it is classified.
3. BEHAVIOUR: with a cap of $0.000001 open, every provider family's REAL client class, every
   seam-direct caller (embeddings, rerank, extraction) and the batch lane's live send are refused
   with the ``call_spend_cap`` stop, and the faked network (``httpx.AsyncClient.send`` plus
   the vendor client objects) is never touched. Without the cap the same call DOES reach the wire,
   so the tripwire is not vacuous.

Falsifiability: the structural checks are pure functions of source text. The ``test_*_catches_*``
tests feed them the real source with the gate removed (in memory, never a tracked file) and require
a violation. Gut check run by hand: gate removed from a scratch copy of ``unified_client.py`` /
``batch_live.py`` makes the matching test red (recorded in the commit message).
"""

from __future__ import annotations

import ast
import asyncio
from pathlib import Path
from typing import Any

import httpx
import pytest

from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.providers import guardrail_gate as gg
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile

PKG = Path(__file__).resolve().parents[1]
MATRX_AI = PKG / "matrx_ai"
UNIFIED = MATRX_AI / "providers" / "unified_client.py"
GATE = MATRX_AI / "providers" / "guardrail_gate.py"
BATCH_LIVE = MATRX_AI / "providers" / "batch_live.py"
STT = MATRX_AI / "processing" / "audio" / "stt.py"

SEAM = "_dispatch_with_billing_net"
IMPOSSIBLE_CAP_USD = 0.000001


# --------------------------------------------------------------------------- #
# AST helpers                                                                  #
# --------------------------------------------------------------------------- #


def _find_func(tree: ast.AST, name: str) -> ast.AST | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == name:
            return node
    return None


def _call_name(call: ast.Call) -> str:
    f = call.func
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute):
        return f.attr
    return ""


def _parents(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    return {child: parent for parent in ast.walk(tree) for child in ast.iter_child_nodes(parent)}


def _is_docstring_or_decl(stmt: ast.stmt) -> bool:
    if isinstance(stmt, ast.Global | ast.Import | ast.ImportFrom):
        return True
    return isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant)


# --------------------------------------------------------------------------- #
# Layer 1 checks (pure functions of source text: violations, [] = healthy)      #
# --------------------------------------------------------------------------- #


def check_admit_guardrails_asks_the_cap_first(gate_src: str) -> list[str]:
    fn = _find_func(ast.parse(gate_src), "admit_guardrails")
    if fn is None:
        return ["admit_guardrails is missing from guardrail_gate.py"]
    for stmt in fn.body:  # type: ignore[attr-defined]
        if _is_docstring_or_decl(stmt):
            continue
        if (
            isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Call)
            and _call_name(stmt.value) == "admit_call_spend_cap"
        ):
            return []
        return [
            f"guardrail_gate.admit_guardrails line {stmt.lineno}: something other than the "
            "unconditional admit_call_spend_cap(...) statement comes first"
        ]
    return ["guardrail_gate.admit_guardrails never calls admit_call_spend_cap"]


def check_the_seam_asks_the_gate_before_dispatch(unified_src: str) -> list[str]:
    tree = ast.parse(unified_src)
    fn = _find_func(tree, SEAM)
    if fn is None:
        return [f"{SEAM} is missing from unified_client.py"]
    parents = _parents(fn)
    gate_calls = [
        n for n in ast.walk(fn) if isinstance(n, ast.Call) and _call_name(n) == "admit_guardrails"
    ]
    if len(gate_calls) != 1:
        return [f"{SEAM} must call admit_guardrails exactly once, found {len(gate_calls)}"]
    gate = gate_calls[0]
    problems: list[str] = []

    # The gate is a plain statement directly in the body of the try that guards the spend gates.
    stmt = parents[gate]
    try_node = parents.get(stmt)
    if not (isinstance(stmt, ast.Expr) and isinstance(try_node, ast.Try) and stmt in try_node.body):
        return [
            f"{SEAM}: admit_guardrails is nested under a condition/loop instead of the gate try body"
        ]
    handlers = {ast.unparse(h.type) if h.type else "": h for h in try_node.handlers}
    if set(handlers) != {"_SkipSpendGates", "BaseException"}:
        problems.append(
            f"{SEAM}: gate try handlers are {sorted(handlers)}, expected _SkipSpendGates + BaseException"
        )
    else:
        if not any(isinstance(n, ast.Raise) for n in ast.walk(handlers["BaseException"])):
            problems.append(
                f"{SEAM}: the BaseException handler around the gates swallows a refusal"
            )
        if not all(isinstance(s, ast.Pass) for s in handlers["_SkipSpendGates"].body):
            problems.append(f"{SEAM}: the _SkipSpendGates handler does more than pass")

    # Only capture mode may skip the gate from inside the try.
    for raise_node in (n for n in ast.walk(try_node) if isinstance(n, ast.Raise)):
        exc = raise_node.exc
        if exc is not None and "_SkipSpendGates" in ast.unparse(exc):
            guard = parents[raise_node]
            while guard is not try_node and not isinstance(guard, ast.If):
                guard = parents[guard]
            if not (isinstance(guard, ast.If) and "is_capturing" in ast.unparse(guard.test)):
                problems.append(
                    f"{SEAM} line {raise_node.lineno}: _SkipSpendGates raised outside capture mode"
                )

    # Anything that returns/leaves before the gate must be the nested-pool pass-through.
    for node in ast.walk(fn):
        if isinstance(node, ast.Return) and node.lineno < gate.lineno:
            guard = parents[node]
            while guard is not fn and not isinstance(guard, ast.If):
                guard = parents[guard]
            if not (isinstance(guard, ast.If) and "active_pools" in ast.unparse(guard.test)):
                problems.append(
                    f"{SEAM} line {node.lineno}: returns before the gate outside the nested-pool pass-through"
                )

    # The dispatch (admitted attempt loop) comes strictly after the gate.
    admitted = [
        n for n in ast.walk(fn) if isinstance(n, ast.Call) and _call_name(n) == "_dispatch_admitted"
    ]
    if not admitted:
        problems.append(f"{SEAM} never dispatches through _dispatch_admitted")
    for call in admitted:
        if call.lineno <= gate.lineno:
            problems.append(f"{SEAM} line {call.lineno}: dispatches before the gate")
    if any(
        isinstance(n, ast.Call) and _call_name(n) == "dispatch" and n.lineno > gate.lineno
        for n in ast.walk(fn)
    ):
        problems.append(
            f"{SEAM}: calls dispatch() directly after the gate, bypassing the attempt loop"
        )
    return problems


def _seam_call_nodes(tree: ast.AST) -> list[ast.Call]:
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call) and _call_name(n) == SEAM]


def check_every_execute_is_inside_the_seam(src: str, receivers: set[str]) -> list[str]:
    """Each ``<receiver>.execute(...)`` is inside a lambda/function handed to the seam."""
    tree = ast.parse(src)
    parents = _parents(tree)
    problems: list[str] = []
    seam_arg_lambdas: set[ast.AST] = set()
    seam_arg_names: set[tuple[ast.AST | None, str]] = set()
    for seam in _seam_call_nodes(tree):
        first = seam.args[0] if seam.args else None
        if isinstance(first, ast.Lambda):
            seam_arg_lambdas.add(first)
        elif isinstance(first, ast.Name):
            scope: ast.AST | None = parents.get(seam)
            while scope is not None and not isinstance(
                scope, ast.FunctionDef | ast.AsyncFunctionDef
            ):
                scope = parents.get(scope)
            seam_arg_names.add((scope, first.id))
    for call in ast.walk(tree):
        if not (
            isinstance(call, ast.Call)
            and isinstance(call.func, ast.Attribute)
            and call.func.attr == "execute"
            and isinstance(call.func.value, ast.Name)
            and call.func.value.id in receivers
        ):
            continue
        node: ast.AST | None = call
        covered = False
        while node is not None:
            if node in seam_arg_lambdas:
                covered = True
                break
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                outer: ast.AST | None = parents.get(node)
                while outer is not None and not isinstance(
                    outer, ast.FunctionDef | ast.AsyncFunctionDef
                ):
                    outer = parents.get(outer)
                if (outer, node.name) in seam_arg_names:
                    covered = True
                    break
            node = parents.get(node)
        if not covered:
            problems.append(
                f"line {call.lineno}: {call.func.value.id}.execute(...) is outside any callable "
                f"passed to {SEAM}, so it can send without the spend cap"
            )
    return problems


def _repo_py_files(*roots: Path) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        for path in root.rglob("*.py"):
            parts = path.parts
            if any(
                p in parts
                for p in ("__pycache__", ".venv", "node_modules", "site-packages", "tests")
            ):
                continue
            if path.name.startswith("test_"):
                continue
            out.append(path)
    return out


def _count_calls(files: list[Path], name: str) -> dict[str, int]:
    found: dict[str, int] = {}
    for path in files:
        text = path.read_text()
        if name not in text:
            continue
        n = sum(
            1
            for node in ast.walk(ast.parse(text))
            if isinstance(node, ast.Call) and _call_name(node) == name
        )
        if n:
            found[str(path.relative_to(PKG.parents[1]))] = n
    return found


# Every caller of the seam, as of this guard. Each one is gated BY the seam; the pin exists so a new
# caller is a reviewed decision (does it pass its config so the cap can price it?).
EXPECTED_SEAM_CALLERS = {
    "packages/matrx-ai/matrx_ai/providers/unified_client.py": 4,
    "packages/matrx-ai/matrx_ai/processing/audio/stt.py": 1,
    "packages/matrx-ai/matrx_ai/decisions/runner.py": 1,
    "packages/matrx-ai/matrx_ai/providers/cohere/rerank.py": 1,
    "packages/matrx-ai/matrx_ai/providers/fastino/fastino_api.py": 1,
    "packages/matrx-ai/matrx_ai/providers/google/specialized.py": 1,
}


# --------------------------------------------------------------------------- #
# Layer 1 tests                                                                #
# --------------------------------------------------------------------------- #


def test_the_cap_is_the_first_thing_the_guardrail_gate_asks() -> None:
    assert check_admit_guardrails_asks_the_cap_first(GATE.read_text()) == []


def test_the_seam_asks_the_gate_before_any_dispatch() -> None:
    assert check_the_seam_asks_the_gate_before_dispatch(UNIFIED.read_text()) == []


def test_dispatch_admitted_is_reachable_only_from_the_seam() -> None:
    users = []
    for path in _repo_py_files(MATRX_AI, PKG.parents[1] / "aidream"):
        text = path.read_text()
        if "_dispatch_admitted" not in text:
            continue
        tree = ast.parse(text)
        parents = _parents(tree)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and _call_name(node) == "_dispatch_admitted":
                scope: ast.AST | None = node
                while scope is not None and not isinstance(
                    scope, ast.FunctionDef | ast.AsyncFunctionDef
                ):
                    scope = parents.get(scope)
                users.append((path.name, getattr(scope, "name", "<module>")))
    assert users == [("unified_client.py", SEAM)], users


def test_every_client_execute_in_the_unified_client_and_stt_is_inside_the_seam() -> None:
    receivers = {"instance", "provider_client", "research_client", "client"}
    assert check_every_execute_is_inside_the_seam(UNIFIED.read_text(), receivers) == []
    assert check_every_execute_is_inside_the_seam(STT.read_text(), receivers) == []


def test_the_seam_callers_are_exactly_the_reviewed_set() -> None:
    found = _count_calls(_repo_py_files(MATRX_AI, PKG.parents[1] / "aidream"), SEAM)
    assert found == EXPECTED_SEAM_CALLERS, (
        "A new caller of UnifiedAIClient._dispatch_with_billing_net appeared (or one vanished). It is "
        "gated by the seam, but pass the exact config so the per-call cap can price it (a call with "
        "no config is refused under a cap), then add it to EXPECTED_SEAM_CALLERS."
    )


def test_every_class_with_an_execute_is_a_client_the_unified_client_builds() -> None:
    import matrx_ai.providers as providers

    reachable: set[str] = set()
    for factory in UnifiedAIClient._PROVIDER_FACTORIES.values():
        reachable.update(cls.__name__ for cls in getattr(providers, factory).__mro__)
    reachable.add("UnifiedAIClient")
    orphans = []
    for path in _repo_py_files(MATRX_AI / "providers"):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.ClassDef) and any(
                isinstance(b, ast.AsyncFunctionDef) and b.name == "execute" for b in node.body
            ):
                if node.name not in reachable:
                    orphans.append(f"{path.relative_to(MATRX_AI)}::{node.name}")
    assert orphans == [], (
        f"{orphans} define execute() but UnifiedAIClient._PROVIDER_FACTORIES never builds them, so "
        "they are a provider entry that does not pass the seam. Register the client or route it."
    )


# --------------------------------------------------------------------------- #
# Layer 2 — census of direct vendor sends                                       #
# --------------------------------------------------------------------------- #

_SEND_SUFFIXES = [
    ("responses", "create"),
    ("responses", "stream"),
    ("completions", "create"),
    ("messages", "create"),
    ("messages", "stream"),
    ("embeddings", "create"),
    ("generate_content",),
    ("generate_content_stream",),
    ("embed_content",),
    ("generate_videos",),
    ("generate_images",),
    ("rerank",),
    ("transcriptions", "create"),
    ("speech", "create"),
    ("images", "generate"),
    ("images", "edit"),
    ("text_to_speech",),
]

#: Modules that send to a vendor SDK but define no ``execute`` client, each with why it is safe.
DIRECT_SENDERS_WITHOUT_AN_EXECUTE_CLIENT: dict[str, str] = {
    "providers/batch_live.py": "the batch lane's live send; asks admit_call_spend_cap itself "
    "(test_the_batch_live_send_is_refused_under_a_cap).",
    "providers/cohere/rerank.py": "dispatches through the seam (EXPECTED_SEAM_CALLERS); config-less, so refused under a cap.",
    "providers/google/specialized.py": "embeddings dispatch through the seam (EXPECTED_SEAM_CALLERS).",
    "providers/google/google_image_api.py": "subclass of BaseMediaGeneration; reached only via its execute().",
    "providers/google/google_video_api.py": "subclass of BaseMediaGeneration; reached only via its execute().",
    "providers/together/together_image_api.py": "subclass of BaseMediaGeneration; reached only via its execute().",
    "providers/google/sample_podcast_direct.py": "standalone sample script, imported by nothing in the repo "
    "(UNFINISHED, not deletable); it cannot run inside a workflow step's cap scope.",
}


def _chain(node: ast.AST) -> tuple[str, ...]:
    out: list[str] = []
    while isinstance(node, ast.Attribute):
        out.append(node.attr)
        node = node.value
    return tuple(reversed(out))


def _direct_sender_modules() -> dict[str, bool]:
    """``{path-under-matrx_ai: defines_an_execute_class}`` for every module calling a vendor send."""
    found: dict[str, bool] = {}
    for path in _repo_py_files(MATRX_AI):
        rel = str(path.relative_to(MATRX_AI))
        if rel.startswith("tools/"):
            continue
        tree = ast.parse(path.read_text())
        sends = False
        has_execute = False
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and any(
                isinstance(b, ast.AsyncFunctionDef) and b.name == "execute" for b in node.body
            ):
                has_execute = True
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                chain = _chain(node.func)
                if any(chain[-len(s) :] == s for s in _SEND_SUFFIXES):
                    sends = True
        if sends:
            found[rel] = has_execute
    return found


def test_no_module_sends_to_a_vendor_outside_a_gated_client_or_a_named_exception() -> None:
    ungated = sorted(
        rel for rel, has_execute in _direct_sender_modules().items() if not has_execute
    )
    unclassified = [rel for rel in ungated if rel not in DIRECT_SENDERS_WITHOUT_AN_EXECUTE_CLIENT]
    assert unclassified == [], (
        f"{unclassified} call a vendor SDK send method but define no execute() client and are not "
        "named in DIRECT_SENDERS_WITHOUT_AN_EXECUTE_CLIENT. Route the send through a provider client "
        "dispatched by UnifiedAIClient, or ask admit_call_spend_cap yourself and name it here."
    )
    stale = sorted(set(DIRECT_SENDERS_WITHOUT_AN_EXECUTE_CLIENT) - set(ungated))
    assert stale == [], f"{stale} no longer send directly; drop them from the exception list"


# --------------------------------------------------------------------------- #
# Layer 3 — behaviour                                                          #
# --------------------------------------------------------------------------- #


@pytest.fixture
def wire(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """The faked network: any real HTTP send is recorded and aborted."""
    sends: list[str] = []

    async def tripwire(self: Any, request: Any, *args: Any, **kwargs: Any) -> Any:
        sends.append(str(getattr(request, "url", request)))
        raise RuntimeError("THE WIRE WAS REACHED")

    monkeypatch.setattr(httpx.AsyncClient, "send", tripwire)
    for key in (
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "GOOGLE_API_KEY",
        "GEMINI_API_KEY",
        "GROQ_API_KEY",
        "CEREBRAS_API_KEY",
        "XAI_API_KEY",
        "TOGETHER_API_KEY",
        "ELEVENLABS_API_KEY",
        "ELEVEN_LABS_API_KEY",
        "REPLICATE_API_TOKEN",
        "MOONSHOT_API_KEY",
        "HF_TOKEN",
        "COHERE_API_KEY",
    ):
        monkeypatch.setenv(key, "test-key-not-real")
    return sends


def _assert_refused_by_the_cap(excinfo: pytest.ExceptionInfo[BaseException]) -> None:
    stop = excinfo.value
    assert isinstance(stop, gg.GuardrailStopError), f"refused by something else: {stop!r}"
    assert stop.kind == gg.CALL_SPEND_CAP, f"refused by {stop.kind}, not the per-call cap"
    assert stop.is_caller_refusal


@pytest.mark.parametrize("client_attr", sorted(UnifiedAIClient._PROVIDER_FACTORIES))
def test_a_capped_call_through_every_provider_client_is_refused_before_any_send(
    client_attr: str, wire: list[str]
) -> None:
    client = UnifiedAIClient._build_provider_client(
        client_attr, UnifiedAIClient._PROVIDER_FACTORIES[client_attr]
    )
    profile = make_profile(
        model_name=f"model-{client_attr}", wire_format=client_attr, vendor=client_attr.split("_")[0]
    )
    config = UnifiedConfig(model=profile.model_name, messages=[], max_output_tokens=1000)

    async def capped_call() -> Any:
        with gg.call_spend_cap_scope(IMPOSSIBLE_CAP_USD, subject="Step guard"):
            return await UnifiedAIClient._dispatch_with_billing_net(
                lambda: client.execute(config, profile, False),
                profile=profile,
                provider_client=client,
                config=config,
            )

    with pytest.raises(BaseException) as excinfo:
        asyncio.run(capped_call())
    _assert_refused_by_the_cap(excinfo)
    assert wire == [], f"{client_attr} reached the wire under a cap: {wire}"


def test_the_tripwire_is_not_vacuous_without_a_cap(wire: list[str]) -> None:
    """Same call, no cap: it must get past the gate and attempt the wire (or fail in the client)."""
    client = UnifiedAIClient._build_provider_client("openai_chat", "OpenAIChat")
    profile = make_profile(model_name="model-openai", wire_format="openai_chat", vendor="openai")
    config = UnifiedConfig(model=profile.model_name, messages=[], max_output_tokens=1000)

    async def uncapped_call() -> Any:
        return await UnifiedAIClient._dispatch_with_billing_net(
            lambda: client.execute(config, profile, False),
            profile=profile,
            provider_client=client,
            config=config,
        )

    try:
        asyncio.run(uncapped_call())
    except BaseException as exc:  # noqa: BLE001 — any outcome but the cap's refusal proves the gate let it by
        assert not isinstance(exc, gg.GuardrailStopError), f"refused with no cap open: {exc!r}"


def test_a_capped_embedding_is_refused_before_any_send(
    wire: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    import matrx_ai.providers.google.specialized as specialized
    from matrx_ai.providers.google import GoogleEmbeddingRuntime

    touched: list[str] = []

    class _Models:
        async def embed_content(self, **_kw: Any) -> Any:
            touched.append("embed_content")
            raise RuntimeError("THE WIRE WAS REACHED")

    class _Client:
        class aio:  # noqa: N801 — mirrors the SDK attribute
            models = _Models()

    monkeypatch.setattr(specialized, "get_google_client", lambda: _Client())
    runtime = GoogleEmbeddingRuntime(
        make_profile(
            model_name="gemini-embedding-2",
            provider_model_id="gemini-embedding-2",
            wire_format="google_embeddings",
            vendor="google",
        )
    )

    async def capped() -> Any:
        with gg.call_spend_cap_scope(IMPOSSIBLE_CAP_USD, subject="Step guard"):
            return await runtime.embed(["Unit 4B reports a slow drain in the kitchen sink."])

    with pytest.raises(BaseException) as excinfo:
        asyncio.run(capped())
    _assert_refused_by_the_cap(excinfo)
    assert touched == [] and wire == []


def test_a_capped_rerank_is_refused_before_any_send(
    wire: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_ai.providers.cohere.rerank import CohereReranker

    touched: list[str] = []

    class _Cohere:
        async def rerank(self, **_kw: Any) -> Any:
            touched.append("rerank")
            raise RuntimeError("THE WIRE WAS REACHED")

    reranker = CohereReranker()
    monkeypatch.setattr(type(reranker), "client", _Cohere(), raising=False)

    async def capped() -> Any:
        with gg.call_spend_cap_scope(IMPOSSIBLE_CAP_USD, subject="Step guard"):
            return await reranker.rerank(
                model="rerank-v3.5", query="slow drain", documents=["a", "b"]
            )

    with pytest.raises(BaseException) as excinfo:
        asyncio.run(capped())
    _assert_refused_by_the_cap(excinfo)
    assert touched == [] and wire == []


def test_a_capped_extraction_is_refused_before_any_send(wire: list[str]) -> None:
    from matrx_ai.providers.fastino.fastino_api import FastinoExtraction

    async def capped() -> Any:
        with gg.call_spend_cap_scope(IMPOSSIBLE_CAP_USD, subject="Step guard"):
            return await FastinoExtraction().extract("Unit 4B has a slow drain.", ["issue"])

    with pytest.raises(BaseException) as excinfo:
        asyncio.run(capped())
    _assert_refused_by_the_cap(excinfo)
    assert wire == []


class _TripClient:
    """A vendor client whose every call (any depth) records itself and raises."""

    def __init__(self, hits: list[str], path: str = "") -> None:
        self._hits, self._path = hits, path

    def __getattr__(self, name: str) -> Any:
        return _TripClient(self._hits, f"{self._path}.{name}")

    async def __call__(self, *_a: Any, **_k: Any) -> Any:
        self._hits.append(self._path)
        raise RuntimeError("THE WIRE WAS REACHED")


@pytest.mark.parametrize(
    ("provider", "endpoint"),
    [
        ("openai", "/v1/responses"),
        ("openai", "/v1/chat/completions"),
        ("openai", "/v1/embeddings"),
        ("anthropic", "messages"),
        ("gemini", "generate_content"),
    ],
)
def test_the_batch_live_send_is_refused_under_a_cap(provider: str, endpoint: str) -> None:
    from matrx_ai.providers.batch_live import send_live

    hits: list[str] = []

    async def capped() -> Any:
        with gg.call_spend_cap_scope(IMPOSSIBLE_CAP_USD, subject="Step guard"):
            return await send_live(
                provider, endpoint, {"model": "m", "input": "x"}, client=_TripClient(hits)
            )  # type: ignore[arg-type]

    with pytest.raises(BaseException) as excinfo:
        asyncio.run(capped())
    _assert_refused_by_the_cap(excinfo)
    assert hits == []

    # No cap open: the same send reaches the vendor client (the tripwire is not vacuous).
    with pytest.raises(RuntimeError, match="THE WIRE WAS REACHED"):
        asyncio.run(
            send_live(provider, endpoint, {"model": "m", "input": "x"}, client=_TripClient(hits))
        )  # type: ignore[arg-type]
    assert hits, "the uncapped send never reached the vendor client"


# --------------------------------------------------------------------------- #
# Falsifiability — the checks can fail                                         #
# --------------------------------------------------------------------------- #


def test_the_guard_catches_a_seam_with_the_gate_removed() -> None:
    src = UNIFIED.read_text()
    line = "            admit_guardrails(profile, config)\n"
    assert src.count(line) == 1
    assert check_the_seam_asks_the_gate_before_dispatch(src.replace(line, "            pass\n"))


def test_the_guard_catches_a_gate_made_conditional() -> None:
    src = UNIFIED.read_text()
    line = "            admit_guardrails(profile, config)\n"
    mutated = src.replace(
        line,
        "            if config is not None:\n                admit_guardrails(profile, config)\n",
    )
    assert check_the_seam_asks_the_gate_before_dispatch(mutated)


def test_the_guard_catches_a_gate_that_forgets_the_cap() -> None:
    src = GATE.read_text()
    line = "    admit_call_spend_cap(profile, config)\n"
    assert src.count(line) == 1
    assert check_admit_guardrails_asks_the_cap_first(src.replace(line, ""))
    assert check_admit_guardrails_asks_the_cap_first(
        src.replace(
            line, "    if config is not None:\n        admit_call_spend_cap(profile, config)\n"
        )
    )


def test_the_guard_catches_an_execute_outside_the_seam() -> None:
    src = UNIFIED.read_text()
    needle = "lambda: provider_client.execute(wire_config, profile, debug),"
    assert src.count(needle) == 1
    mutated = src.replace(needle, "provider_client.execute(wire_config, profile, debug),")
    assert check_every_execute_is_inside_the_seam(mutated, {"provider_client"})
    assert check_every_execute_is_inside_the_seam(
        "async def go(client):\n    return await client.execute(1)\n", {"client"}
    )


def test_the_guard_catches_a_new_direct_vendor_sender() -> None:
    assert BATCH_LIVE.read_text().count("admit_call_spend_cap") >= 1
    stripped = BATCH_LIVE.read_text().replace("admit_call_spend_cap(None, None)", "pass")
    assert "admit_call_spend_cap(None, None)" not in stripped
    # The behavioural twin: the same module with the gate line gone sends under a cap.
    namespace: dict[str, Any] = {"__name__": "scratch_batch_live"}
    exec(compile(stripped, "scratch_batch_live.py", "exec"), namespace)  # noqa: S102 — in-memory scratch copy
    hits: list[str] = []

    async def capped() -> Any:
        with gg.call_spend_cap_scope(IMPOSSIBLE_CAP_USD, subject="Step guard"):
            return await namespace["send_live"](
                "anthropic", "messages", {"model": "m"}, client=_TripClient(hits)
            )

    with pytest.raises(RuntimeError, match="THE WIRE WAS REACHED"):
        asyncio.run(capped())
    assert hits, "the gate-less scratch copy should have reached the wire"


def test_the_census_sees_the_batch_lane() -> None:
    senders = _direct_sender_modules()
    assert senders.get("providers/batch_live.py") is False
    assert senders.get("providers/anthropic/anthropic_api.py") is True
