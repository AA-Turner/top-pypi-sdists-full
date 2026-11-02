"""A chat is indexed ONLY as what the person typed (D327 + the typed field, 2026-10-25).

`chat.message.content` on a ``role='user'`` row is the COMPLETE PROVIDER PAYLOAD (seeded opening
turn + resolved launch variables + what the person typed); ``user_content`` is the authorship
record, read through the injected ``human_authored_text`` seam. On top of that, the conversation
resolver now:

* reads ONLY ``role='user'`` rows — the whole-transcript path that concatenated assistant replies
  as ``"<role>: <text>"`` is retired, and a NULL ``field_id`` resolves exactly like ``"typed"``;
* adds the variable values the person entered, minus values equal to the agent's declared default
  and minus lines repeated verbatim across ``template_repeat_runs`` runs of the same agent;
* resolves nothing for a conversation the ONE authorship rule says is not the person's own chat
  (coding-session mirror, sub-agent, mandate job, automation) — the rule is the host's knobs,
  injected as ``typed_chat_policy``; with none injected the resolver refuses by name.

These run the REAL ``matrx_rag.sources._resolve_cx_message`` over faked ORM models that honour
the resolver's own filters and select lists. Proven failing then passing: on the pre-change
resolver the assistant-reply, default-value, template-line, machine-chat, field-id and
missing-policy cases fail (18 of 23 on 2026-10-25, the rest are the D327 guards that
already held); with the change, all 23 pass.
"""

from __future__ import annotations

import pytest
from matrx_rag import _ext, sources
from matrx_rag.chat_authorship import TypedChatPolicy
from matrx_utils.source_guard import stable_source

OWNER = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
ORG = "cccccccc-cccc-cccc-cccc-cccccccccccc"
CONV = "11111111-1111-1111-1111-111111111111"
MSG = "22222222-2222-2222-2222-222222222222"
AGENT = "33333333-3333-3333-3333-333333333333"

SEEDED_TEMPLATE = "Let's get started. Follow the mode you were given above and interview the expert."
HER_WORDS = "We never accept a load without a weight ticket from the scale house."
GATE_NOTICE = "SYSTEM NOTICE (not from the user): required member missing."
REPLY = "Understood — I'll record the weight-ticket rule."
DEFAULT_TEXT = "Describe your business in plain words."
SHORTCUT_LINE = "Summarize this for a busy executive in five bullets."

POLICY = TypedChatPolicy(
    person_conversation_types=frozenset({"standard"}),
    person_origin_classes=frozenset({"human", "client_auto", "unknown"}),
    mirror_source_apps=frozenset({"code-plugin"}),
    machine_source_features=("mandate:", "system"),
    automation_title_markers=("Automation:", "<heartbeat>"),
    template_repeat_runs=5,
    template_scan_runs=50,
)


def _text(s: str) -> list[dict]:
    return [{"type": "text", "text": s}]


def _match(row: dict, kw: dict) -> bool:
    for key, want in kw.items():
        if key.endswith("__isnull"):
            if (row.get(key[: -len("__isnull")]) is None) != want:
                return False
        elif row.get(key) != want:
            return False
    return True


class _Q:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def order_by(self, *_a):
        return self

    def exclude(self, **kw):
        return _Q([r for r in self._rows if not _match(r, kw)])

    def limit(self, n: int):
        return _Q(self._rows[:n])

    async def values(self, *fields):
        _Model.last_selects.append(fields)
        return [{f: r.get(f) for f in fields} for r in self._rows]


class _Model:
    last_selects: list[tuple] = []

    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def filter(self, **kw):
        return _Q([r for r in self._rows if _match(r, kw)])


def _conv(**kw) -> dict:
    row = {
        "id": CONV,
        "created_by": OWNER,
        "organization_id": ORG,
        "title": "Intake rules",
        "conversation_type": "standard",
        "origin_class": "human",
        "source_app": "matrx-frontend",
        "source_feature": "chat",
        "parent_conversation_id": None,
        "exclude_from_kg": False,
        "deleted_at": None,
        "variables": {},
        "initial_agent_id": None,
    }
    row.update(kw)
    return row


def _msg(**kw) -> dict:
    row = {
        "id": MSG,
        "conversation_id": CONV,
        "role": "user",
        "content": None,
        "user_content": None,
        "is_visible_to_model": True,
    }
    row.update(kw)
    return row


@pytest.fixture
def wire(monkeypatch):
    def _wire(messages: list[dict], *, convs: list[dict] | None = None, defs: list[dict] | None = None):
        models = {
            "Conversation": _Model(convs if convs is not None else [_conv()]),
            "Message": _Model(messages),
            "Definition": _Model(defs or []),
        }
        monkeypatch.setattr(sources, "get_db_model", lambda name, schema=None: models[name])

    async def _policy():
        return POLICY

    monkeypatch.setitem(_ext._registry, "human_authored_text", None)
    monkeypatch.setitem(_ext._registry, "typed_chat_policy", _policy)
    return _wire


@pytest.mark.asyncio
async def test_seeded_template_is_never_indexed_as_her_words(wire):
    wire([_msg(content=_text(SEEDED_TEMPLATE + "\n\n" + HER_WORDS), user_content=_text(HER_WORDS))])
    resolved = await sources._resolve_cx_message(CONV, user_id=OWNER)
    assert resolved is not None
    assert resolved.text == HER_WORDS


@pytest.mark.asyncio
async def test_host_authored_user_turn_is_not_a_turn(wire):
    wire([
        _msg(id="m1", content=_text(GATE_NOTICE), user_content=[]),
        _msg(id="m2", content=_text(HER_WORDS), user_content=_text(HER_WORDS)),
    ])
    resolved = await sources._resolve_cx_message(CONV, user_id=OWNER)
    assert resolved is not None and resolved.text == HER_WORDS
    assert resolved.metadata["typed_lines"] == 1


@pytest.mark.asyncio
async def test_null_authorship_still_reads_content(wire):
    wire([_msg(content=_text(HER_WORDS), user_content=None)])
    resolved = await sources._resolve_cx_message(CONV, user_id=OWNER)
    assert resolved is not None and resolved.text == HER_WORDS


@pytest.mark.asyncio
async def test_assistant_replies_are_never_indexed(wire):
    """THE RETIRED PATH: a reply never reaches the text; a reply-only chat resolves to nothing."""
    wire([
        _msg(id="m1", content=_text(HER_WORDS), user_content=_text(HER_WORDS)),
        _msg(id="m2", role="assistant", content=_text(REPLY)),
        _msg(id="m3", role="system", content=_text(SEEDED_TEMPLATE)),
    ])
    resolved = await sources._resolve_cx_message(CONV, user_id=OWNER)
    assert resolved is not None
    assert REPLY not in resolved.text and SEEDED_TEMPLATE not in resolved.text
    assert "assistant:" not in resolved.text and "user:" not in resolved.text

    wire([_msg(role="assistant", content=_text(REPLY))])
    assert await sources._resolve_cx_message(CONV, user_id=OWNER) is None


@pytest.mark.asyncio
async def test_a_conversation_is_always_its_typed_field(wire):
    wire([_msg(content=_text(HER_WORDS), user_content=_text(HER_WORDS))])
    resolved = await sources.resolve("cx_message", CONV, None, user_id=OWNER)
    assert resolved is not None and resolved.field_id == "typed"
    resolved = await sources.resolve("cx_message", CONV, "typed", user_id=OWNER)
    assert resolved is not None and resolved.field_id == "typed"


@pytest.mark.asyncio
async def test_a_message_id_resolves_to_its_conversations_typed_text(wire):
    wire([
        _msg(content=_text(SEEDED_TEMPLATE + "\n" + HER_WORDS), user_content=_text(HER_WORDS)),
        _msg(id="m2", role="assistant", content=_text(REPLY)),
    ])
    resolved = await sources._resolve_cx_message(MSG, user_id=OWNER)
    assert resolved is not None
    assert (resolved.source_id, resolved.text) == (CONV, HER_WORDS)


@pytest.mark.asyncio
async def test_entered_variables_count_but_defaults_do_not(wire):
    wire(
        [_msg(content=_text(HER_WORDS), user_content=_text(HER_WORDS))],
        convs=[_conv(initial_agent_id=AGENT, variables={"brief": DEFAULT_TEXT, "client": "Harbor Clinic", "n": 3})],
        defs=[{"id": AGENT, "variable_definitions": [{"name": "brief", "defaultValue": DEFAULT_TEXT}]}],
    )
    resolved = await sources._resolve_cx_message(CONV, user_id=OWNER)
    assert resolved is not None
    assert "Harbor Clinic" in resolved.text and HER_WORDS in resolved.text
    assert DEFAULT_TEXT not in resolved.text
    assert resolved.metadata["dropped_default_values"] == 1


@pytest.mark.asyncio
async def test_a_line_repeated_across_runs_of_one_agent_is_a_template(wire):
    runs = [_conv(id=f"run-{i}", initial_agent_id=AGENT, variables={"ask": SHORTCUT_LINE}) for i in range(4)]
    wire(
        [_msg(content=_text(f"{SHORTCUT_LINE}\n{HER_WORDS}"), user_content=_text(f"{SHORTCUT_LINE}\n{HER_WORDS}"))],
        convs=[_conv(initial_agent_id=AGENT), *runs],
    )
    resolved = await sources._resolve_cx_message(CONV, user_id=OWNER)
    assert resolved is not None
    assert resolved.text == HER_WORDS
    assert resolved.metadata["dropped_template_lines"] == 1


@pytest.mark.parametrize(
    "conv",
    [
        _conv(source_app="code-plugin", origin_class="api"),
        _conv(source_app="code-plugin", origin_class="unknown"),
        _conv(conversation_type="subagent"),
        _conv(conversation_type="auto", origin_class="human", source_feature="mandate:seo.topic_assigner"),
        _conv(origin_class="child_agent"),
        _conv(source_feature="mandate:research.source_authority"),
        _conv(title="Automation: nightly digest"),
        _conv(parent_conversation_id="44444444-4444-4444-4444-444444444444"),
        _conv(exclude_from_kg=True),
    ],
)
@pytest.mark.asyncio
async def test_a_machine_chat_resolves_to_nothing(wire, conv):
    wire([_msg(content=_text(HER_WORDS), user_content=_text(HER_WORDS))], convs=[conv])
    assert await sources._resolve_cx_message(CONV, user_id=OWNER) is None


@pytest.mark.asyncio
async def test_without_the_hosts_policy_a_chat_is_refused_by_name(wire, monkeypatch):
    wire([_msg(content=_text(HER_WORDS), user_content=_text(HER_WORDS))])
    monkeypatch.setitem(_ext._registry, "typed_chat_policy", None)
    with pytest.raises(_ext.RagNotConfiguredError):
        await sources._resolve_cx_message(CONV, user_id=OWNER)


@pytest.mark.asyncio
async def test_someone_elses_conversation_is_absent(wire):
    wire([_msg(content=_text(HER_WORDS), user_content=_text(HER_WORDS))], convs=[_conv(created_by="someone-else")])
    assert await sources._resolve_cx_message(CONV, user_id=OWNER) is None


@pytest.mark.asyncio
async def test_jsonb_decoded_as_a_raw_string_never_embeds_json(wire):
    import json

    wire([_msg(content=json.dumps(_text(SEEDED_TEMPLATE)), user_content=json.dumps(_text(HER_WORDS)))])
    resolved = await sources._resolve_cx_message(CONV, user_id=OWNER)
    assert resolved is not None and resolved.text == HER_WORDS


@pytest.mark.asyncio
async def test_injected_host_projection_is_the_one_that_runs(wire, monkeypatch):
    seen: list[tuple] = []

    def _host_projection(role, content, user_content):
        seen.append((role, content, user_content))
        return "HOST-PROJECTED"

    wire([_msg(content=_text(SEEDED_TEMPLATE), user_content=_text(HER_WORDS))])
    monkeypatch.setitem(_ext._registry, "human_authored_text", _host_projection)
    resolved = await sources._resolve_cx_message(CONV, user_id=OWNER)
    assert resolved is not None and resolved.text == "HOST-PROJECTED"
    assert seen == [("user", _text(SEEDED_TEMPLATE), _text(HER_WORDS))]


def test_every_message_select_carries_the_authorship_column():
    """Source census: no select of a message's `content` without `user_content`."""
    import ast

    tree = ast.parse(stable_source(sources))
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "values":
            fields = {a.value for a in node.args if isinstance(a, ast.Constant)}
            if "role" in fields and "content" in fields and "user_content" not in fields:
                offenders.append(sorted(fields))
    assert offenders == []


def test_the_raw_payload_reader_is_gone():
    import ast

    tree = ast.parse(stable_source(sources))
    defined = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef)}
    assert "_extract_message_text" not in defined
    assert "_human_authored_message_text" in defined
