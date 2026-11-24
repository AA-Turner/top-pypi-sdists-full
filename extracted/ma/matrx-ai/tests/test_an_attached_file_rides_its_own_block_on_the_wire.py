"""THE FILE RULE on the wire (``config/attached_files.py``, send-boundary step ``attached_files``).

A staged attached file rides in its OWN block, opened by its ``<attachment/>`` label, at the start
of the person turn whose stored metadata names it — on the wire copy only (defect 50), the same
bytes on every send (so it is read from the prompt cache). Placement is total (REVIEW-C103): a
host-written turn is a home (#1), a home the history window cut is replaced by the OLDEST turn still
on the wire — the same message every send — never the newest person turn, which moved the file every
turn (#3); nothing is ever placed before a tool result (#5); a list with no turn that can carry it
gets the file in its own turn at the start. Host: AI Dream ``conversation_context/file_blocks.py``.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

from matrx_ai.config.attached_files import CONTEXT_FILE_BLOCKS_KEY, FILE_BLOCK_HOMES_KEY
from matrx_ai.config.enums import Role
from matrx_ai.config.media_config import DocumentContent
from matrx_ai.config.message_config import MessageList, UnifiedMessage
from matrx_ai.config.send_boundary import STAGE_LOOP, SendPrep, _build_wire, _place_attached_files
from matrx_ai.config.unified_config import UnifiedConfig
from matrx_ai.config.unified_content import TextContent

KEY = "resource_file_1c1c6c1e-3f0a-4a77-9d55-8a1f1b2c3d4e"
FILE_ID = "1c1c6c1e-3f0a-4a77-9d55-8a1f1b2c3d4e"
CSV = "arrival,trailer\n7,TR-40917"


def _config(*, home: bool = True, native: bool = False) -> UnifiedConfig:
    first = UnifiedMessage(role=Role.USER, content=[TextContent(text="Here is the manifest.")])
    if home:
        first.metadata[FILE_BLOCK_HOMES_KEY] = [KEY]
    entry = {"key": KEY, "file_id": FILE_ID, "file_name": "inbound-oct16.csv"}
    entry.update({"native": True, "mime_type": "application/pdf"} if native else {"text": CSV})
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=[
        first,
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Noted.")]),
        UnifiedMessage(role=Role.USER, content=[TextContent(text="Which trailer?")]),
    ]))
    config.metadata[CONTEXT_FILE_BLOCKS_KEY] = [entry]
    return config


def _send(config: UnifiedConfig) -> list:
    prep = SendPrep(stage=STAGE_LOOP)
    _build_wire(prep, config)
    _place_attached_files(prep, config)
    return list(prep.wire_config.messages)


def test_the_file_rides_its_home_turn_in_its_own_labelled_block_on_the_wire_only() -> None:
    config = _config()
    wire = _send(config)
    block = wire[0].content[0]
    assert block.text == f'<attachment kind="document" name="inbound-oct16.csv" id="{FILE_ID}" converted_to="text"/>\n{CSV}'
    assert wire[0].content[1].text == "Here is the manifest."
    assert all("TR-40917" not in getattr(c, "text", "") for m in wire[1:] for c in m.content)
    assert [c.text for c in config.messages.to_list()[0].content] == ["Here is the manifest."], "stored turn changed"


def test_every_send_carries_the_same_bytes() -> None:
    config = _config()
    assert [c.text for c in _send(config)[0].content] == [c.text for c in _send(config)[0].content]


def test_a_file_whose_home_turn_is_gone_rides_the_oldest_turn_on_the_wire_every_send() -> None:
    """REVIEW-C103 #3: the window cut its home. It rides the OLDEST turn still sent, so a later turn
    leaves it where it was (cached), instead of moving to each new person turn (1.25x per turn)."""
    config = _config(home=False)
    first = _send(config)
    assert CSV in first[0].content[0].text and first[0].content[-1].text == "Here is the manifest."
    assert all(CSV not in getattr(c, "text", "") for c in first[-1].content)
    config.messages.append(UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="TR-40917.")]))
    config.messages.append(UnifiedMessage(role=Role.USER, content=[TextContent(text="And the pallets?")]))
    later = _send(config)
    assert [getattr(c, "text", None) for c in later[0].content] == [getattr(c, "text", None) for c in first[0].content]
    assert all(CSV not in getattr(c, "text", "") for m in later[1:] for c in m.content)


def _host_only(*, stamped: bool) -> UnifiedConfig:
    from matrx_ai.config.message_config import host_authored_user_turn

    turn = host_authored_user_turn("Run the receiving check.", reason="workflow")
    if stamped:
        turn.metadata[FILE_BLOCK_HOMES_KEY] = [KEY]
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=[turn]))
    config.metadata[CONTEXT_FILE_BLOCKS_KEY] = [{"key": KEY, "file_id": FILE_ID, "file_name": "inbound-oct16.csv", "text": CSV}]
    return config


def test_a_run_with_only_a_host_written_turn_receives_its_file() -> None:
    """REVIEW-C103 #1 (CRITICAL): run_mandate(host_turn=), ai.agent.start and inbox wakes have only
    host-written user turns. The value list says the text is in the message, so it must be."""
    for stamped in (True, False):
        wire = _send(_host_only(stamped=stamped))
        assert len(wire) == 1 and wire[0].content[0].text.endswith(CSV), stamped
        assert wire[0].content[-1].text == "Run the receiving check."


def test_nothing_is_ever_placed_before_a_tool_result() -> None:
    """REVIEW-C103 #5: Anthropic refuses text before a tool_result in a user turn."""
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent

    config = _config(home=False)
    config.messages.append(UnifiedMessage(role=Role.ASSISTANT, content=[ToolCallContent(id="t1", name="x", arguments={})]))
    config.messages.append(UnifiedMessage(role=Role.USER, content=[ToolResultContent(tool_use_id="t1", name="x", content="ok")]))
    wire = _send(config)
    assert [type(c).__name__ for c in wire[-1].content] == ["ToolResultContent"]
    assert CSV in wire[0].content[0].text


def test_a_list_with_no_turn_to_carry_it_gets_the_file_in_its_own_first_turn() -> None:
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent

    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=[
        UnifiedMessage(role=Role.ASSISTANT, content=[ToolCallContent(id="t1", name="x", arguments={})]),
        UnifiedMessage(role=Role.USER, content=[ToolResultContent(tool_use_id="t1", name="x", content="ok")]),
    ]))
    config.metadata[CONTEXT_FILE_BLOCKS_KEY] = [{"key": KEY, "file_id": FILE_ID, "file_name": "a.csv", "text": CSV}]
    wire = _send(config)
    assert len(wire) == 3 and str(getattr(wire[0].role, "value", wire[0].role)) == "user"
    assert wire[0].content[0].text.endswith(CSV)
    assert [type(c).__name__ for c in wire[2].content] == ["ToolResultContent"]


def test_a_small_scanned_pdf_rides_as_the_pdf_itself() -> None:
    wire = _send(_config(native=True))
    part = wire[0].content[0]
    assert isinstance(part, DocumentContent) and part.file_id == FILE_ID


def _few_shot(text: str, role: Role) -> UnifiedMessage:
    """An authored template message as the fill stamps it (``cache_marks.stamp_template_messages``)."""
    from matrx_ai.config.cache_marks import TEMPLATE_METADATA_KEY, TEMPLATE_STABLE

    message = UnifiedMessage(role=role, content=[TextContent(text=text)])
    message.metadata[TEMPLATE_METADATA_KEY] = TEMPLATE_STABLE
    return message


def _with_examples(rest: list[UnifiedMessage]) -> UnifiedConfig:
    config = UnifiedConfig(model="claude-haiku-5-5", messages=MessageList(_messages=[
        _few_shot("EXAMPLE: which trailer carried lot 12?", Role.USER),
        _few_shot("EXAMPLE: TR-1.", Role.ASSISTANT),
        *rest,
    ]))
    config.metadata[CONTEXT_FILE_BLOCKS_KEY] = [{"key": KEY, "file_id": FILE_ID, "file_name": "inbound-oct16.csv", "text": CSV}]
    return config


def _carries_file(message: UnifiedMessage) -> bool:
    return any(CSV in getattr(c, "text", "") for c in message.content)


def test_a_cut_file_never_lands_on_an_authored_few_shot_example() -> None:
    """REVIEW-C110 minor 3: the window cut the file's own turn and the agent's authored few-shot
    exchange is kept at the head. The file goes on the oldest kept REAL turn, never the example
    (the model would read the person's file as part of the example)."""
    config = _with_examples([
        UnifiedMessage(role=Role.USER, content=[TextContent(text="Which trailer?")]),
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="TR-40917.")]),
        UnifiedMessage(role=Role.USER, content=[TextContent(text="And the pallets?")]),
    ])
    wire = _send(config)
    assert not _carries_file(wire[0]) and not _carries_file(wire[1]), "the file rode the few-shot example"
    assert _carries_file(wire[2]) and wire[2].content[-1].text == "Which trailer?"
    assert sum(_carries_file(m) for m in wire) == 1


def test_with_only_examples_and_a_tool_loop_the_file_takes_its_own_turn_after_them() -> None:
    from matrx_ai.config.tools_config import ToolCallContent, ToolResultContent

    config = _with_examples([
        UnifiedMessage(role=Role.ASSISTANT, content=[ToolCallContent(id="t1", name="x", arguments={})]),
        UnifiedMessage(role=Role.USER, content=[ToolResultContent(tool_use_id="t1", name="x", content="ok")]),
    ])
    wire = _send(config)
    assert [_carries_file(m) for m in wire] == [False, False, True, False, False]
    assert [c.text for c in wire[0].content] == ["EXAMPLE: which trailer carried lot 12?"]


def test_a_new_file_is_never_homed_on_a_few_shot_example() -> None:
    from matrx_ai.config.attached_files import newest_file_home

    examples = [_few_shot("EXAMPLE: q", Role.USER), _few_shot("EXAMPLE: a", Role.ASSISTANT)]
    assert newest_file_home(examples) is None
    real = UnifiedMessage(role=Role.USER, content=[TextContent(text="Here is the manifest.")])
    assert newest_file_home([*examples, real]) is real


def test_prepare_for_send_runs_the_attached_files_step() -> None:
    """The step is the only thing that puts a staged file on the wire; the host has already told the
    model the text is in the message. A whole-file push from a stale base deleted it once (C116,
    75bf1775392): every attached file was announced and never sent. Read off the real source."""

    from matrx_ai.config import send_boundary

    source = stable_source(send_boundary.prepare_for_send)
    assert '_run_step(prep, "attached_files", lambda: _place_attached_files(prep, config))' in source
    wire_clone = source.index('"wire_config"')
    step = source.index('"attached_files"')
    assert wire_clone < step, "the file step runs on the wire clone, never the stored history"


def test_every_send_boundary_step_runs_once_and_every_helper_is_defined_once() -> None:
    """A merge of two restores put the file step in twice (2026-11-10, 8cc99750c6d over 3c3ee682a0d): every attached
    file rode the wire twice on every send, and the line-exists guard above stayed green. The class: no step name may
    run twice in ``prepare_for_send`` and no module-level function may be defined twice (the second silently wins)."""
    import ast
    import re
    from collections import Counter

    from matrx_ai.config import send_boundary

    steps = Counter(re.findall(r'_run_step\(\s*prep,\s*"([^"]+)"', stable_source(send_boundary.prepare_for_send)))
    assert steps["attached_files"] == 1
    assert not [name for name, n in steps.items() if n > 1], f"steps run more than once: {steps}"
    tree = ast.parse(stable_source(send_boundary))
    defs = Counter(node.name for node in tree.body if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef))
    assert not [name for name, n in defs.items() if n > 1], f"functions defined twice: {defs}"


# --------------------------------------------------------------------------------------------- #
# THE HELD COPY (surface-declarations G8b, commit 1): a second kind of HOMED block. A host-staged  #
# ``{"kind": "held_copy", "key", "text", "home", "hash"}`` rides its home turn like a file: after #
# the turn's files, before the per-turn platform block, byte-identical on every later send, and   #
# cached by the rolling mark on the send that delivers it. Placement, the order before the        #
# platform block and the typed layout key on ``HOMED_BLOCK_MARK``, never on ``file_id``.          #
# --------------------------------------------------------------------------------------------- #

from matrx_ai.config.attached_files import HELD_COPY_KIND, HOMED_BLOCK_MARK  # noqa: E402

HELD_TEXT = "[" + ", ".join(f'{{"id": {n}, "front": "Q{n}", "back": "A{n}"}}' for n in range(1, 101)) + "]"
HELD_ENTRY = {"kind": HELD_COPY_KIND, "key": "cards", "text": HELD_TEXT, "home": "row-0", "hash": "h1", "as_of": "turn 1"}
PAGE = '<live_date>It is now {}.</live_date>'
TEMPLATE = "TEMPLATE: You help the person study their flashcard deck. " * 30


def _anthropic(config: UnifiedConfig, *, iteration: int = 1) -> dict:
    from matrx_ai.config.send_boundary import order_for_wire
    from matrx_ai.providers.anthropic.translator import AnthropicTranslator
    from matrx_ai.testing.profile_factory import make_profile

    profile = make_profile(model_name="claude-x", wire_format="anthropic_chat")
    prep = SendPrep(stage=STAGE_LOOP)
    _build_wire(prep, config)
    _place_attached_files(prep, config)
    prep = order_for_wire(config, profile, prep=prep, iteration=iteration)
    return AnthropicTranslator().build_request(prep.wire_config or config, profile)


def _held_config(messages: list[UnifiedMessage], day: str, *, files: bool = False, held: bool = True) -> UnifiedConfig:
    config = UnifiedConfig(model="claude-x", messages=MessageList(_messages=messages))
    config.system_instruction = "You are a careful study partner. " * 60
    config.messages.attach_turn_context(PAGE.format(day), slot="live_date")
    entries = [{"key": KEY, "file_id": FILE_ID, "file_name": "inbound-oct16.csv", "text": CSV}] if files else []
    if held:
        entries.append(dict(HELD_ENTRY))
    config.metadata[CONTEXT_FILE_BLOCKS_KEY] = entries
    return config


def _user(text: str, at: int) -> UnifiedMessage:
    message = UnifiedMessage(role=Role.USER, content=[TextContent(text=text)])
    message.id = f"row-{at}"
    return message


def _blocks(request: dict) -> list:
    """Every message block in wire order as ``(role, block)``, cache marks removed — the unit
    Anthropic's prefix cache matches on."""
    out = []
    for m in request["messages"]:
        for b in m["content"]:
            out.append((str(m["role"]), {k: v for k, v in b.items() if k != "cache_control"}))
    return out


def _cached_prefix(request: dict) -> list:
    """The blocks through the request's LAST cache mark (the rolling mark)."""
    flat = [b for m in request["messages"] for b in m["content"]]
    end = max((i for i, b in enumerate(flat) if "cache_control" in b), default=-1)
    return _blocks(request)[: end + 1]


def _has(blocks: list, needle: str) -> bool:
    return any(needle in str(b.get("text", "")) for _role, b in blocks)


def test_a_held_copy_rides_before_the_platform_block_and_the_rolling_mark_caches_it() -> None:
    """(a) The delivery turn: ``[file] [held copy] [platform block] [her words]``, the rolling mark on
    the held copy — it is written to the cache on the very send that delivers it."""
    with_file = _held_config([_user("Quiz me on the deck.", 0)], "Monday", files=True)
    for config, lead in ((with_file, 2), (_held_config([_user("Quiz me on the deck.", 0)], "Monday"), 1)):
        content = _anthropic(config)["messages"][-1]["content"]
        texts = [b["text"] for b in content]
        assert texts[lead - 1].startswith('<held_copy key="cards" as_of="turn 1"/>\n['), texts
        assert texts[lead].startswith('<turn_context source="platform"'), "the held copy must lead the platform block"
        assert texts[-1] == "Quiz me on the deck."
        if lead == 2:
            assert texts[0].startswith("<attachment "), "files come first, then held copies"
        marked = [i for i, b in enumerate(content) if "cache_control" in b]
        assert marked == [lead - 1], f"the rolling mark must sit on the held copy, found {marked}"


def test_the_held_copy_is_byte_identical_on_the_next_turn_and_read_from_cache() -> None:
    """(b) Turn N+1's request is turn N's cached prefix (through the held copy) plus new turns."""
    first = _anthropic(_held_config([_user("Quiz me on the deck.", 0)], "Monday"))
    cached = _cached_prefix(first)
    assert _has(cached, HELD_TEXT) and cached[-1][1]["text"].endswith(HELD_TEXT)
    nxt = _anthropic(_held_config([
        _user("Quiz me on the deck.", 0),
        UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Card 1: Q1?")]),
        _user("A1. What is on the back of card 57?", 2),
    ], "Tuesday"))
    later = _blocks(nxt)
    assert later[: len(cached)] == cached, "the next turn diverged inside the cached held copy"
    assert sum(str(b.get("text", "")).count('"back": "A57"') for _r, b in later) == 1, "one copy per request"


def test_the_shared_prefix_tools_system_and_template_turn_never_carry_a_held_copy() -> None:
    """(c) Amendment 9: tools, system AND the authored template turn are byte-identical with and
    without a later turn's held copy, so two conversations of one agent still share them."""
    from matrx_ai.config.cache_marks import TEMPLATE_METADATA_KEY, TEMPLATE_STABLE

    def history() -> list[UnifiedMessage]:
        template = _user(TEMPLATE, 0)
        template.metadata[TEMPLATE_METADATA_KEY] = TEMPLATE_STABLE
        return [
            template,
            UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Ready.")]),
            _user("Quiz me on the deck.", 2),
        ]

    held_entry = dict(HELD_ENTRY, home="row-2")
    plain = _held_config(history(), "Monday", held=False)
    held = _held_config(history(), "Monday", held=False)
    held.metadata[CONTEXT_FILE_BLOCKS_KEY] = [held_entry]
    a, b = _anthropic(plain), _anthropic(held)
    assert a["system"] == b["system"] and a.get("tools") == b.get("tools")
    assert a["messages"][0] == b["messages"][0], "the authored template turn changed"
    flat = _blocks(b)
    assert flat[0] == _blocks(a)[0] and not _has(flat[:2], HELD_TEXT) and _has(flat, HELD_TEXT)


def test_held_copy_recognition_is_the_generic_mark_not_a_file_id() -> None:
    """(d) The forcing seam: with the mark's recognition broken, the platform block jumps ahead of
    the held copy and the delivery turn's rolling mark no longer caches it (shown red once,
    2026-11-12: ``texts[0]`` became the platform block)."""
    from matrx_ai.config import attached_files

    config = _held_config([_user("Quiz me on the deck.", 0)], "Monday")
    placed = attached_files.place_attached_files(list(config.messages), config.metadata[CONTEXT_FILE_BLOCKS_KEY])
    block = placed[0].content[0]
    assert attached_files.is_homed_block(block) and not attached_files.is_file_block(block)
    assert block.metadata == {HOMED_BLOCK_MARK: "cards"}


def test_a_window_cut_held_copy_is_never_orphaned_and_a_stamped_home_counts() -> None:
    """Amendment 9: a held copy whose home the window cut never moves to the oldest kept turn (the
    authored template turn every conversation of the agent shares). It is left off this send and
    reported; a file keeps the orphan rule. Red before 2026-11-12 (the copy rode ``cut[0]``)."""
    from matrx_ai.config.attached_files import HELD_COPY_HOMES_KEY, place_attached_files

    old, new = _user("one", 0), _user("two", 2)
    msgs = [old, UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="ok")]), new]
    off: list = []
    cut = place_attached_files(msgs, [dict(HELD_ENTRY, home="row-gone")], off_wire=off)
    assert cut is None or all(HELD_TEXT not in getattr(c, "text", "") for m in cut for c in m.content)
    assert off == [{"kind": HELD_COPY_KIND, "key": "cards", "why": "cut"}]
    new.metadata[HELD_COPY_HOMES_KEY] = ["cards"]
    stamped = place_attached_files(msgs, [dict(HELD_ENTRY, home=None)])
    assert HELD_TEXT in stamped[2].content[0].text and len(stamped[0].content) == 1


NOTE = {"after": 'key="cards"', "text": "Unchanged since turn 1.", "off_wire": "Not in this request; read it with the tool."}


def _template_history() -> list[UnifiedMessage]:
    from matrx_ai.config.cache_marks import TEMPLATE_METADATA_KEY, TEMPLATE_STABLE

    template = _user(TEMPLATE, 0)
    template.metadata[TEMPLATE_METADATA_KEY] = TEMPLATE_STABLE
    return [template, UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Ready.")]),
            _user("Here is the deck.", 2), UnifiedMessage(role=Role.ASSISTANT, content=[TextContent(text="Got it.")]),
            _user("What is on card 57?", 4)]


def _settled(config: UnifiedConfig, *, cut: set[int] = frozenset(), stub: bool = False, monkeypatch=None) -> SendPrep:
    """The boundary's order on the wire: window (``cut`` = message indexes the window removed),
    placement, the per-turn block (``order_for_wire``), the fit (``stub``: every earlier text is
    stubbed), then the off-wire settle."""
    import asyncio

    from matrx_ai.config import input_fit
    from matrx_ai.config.send_boundary import _settle_homed_off_wire, order_for_wire
    from matrx_ai.testing.profile_factory import make_profile

    if cut:  # what ``_apply_history_window`` does to the canonical list on the resolve stage
        kept = [m for i, m in enumerate(config.messages.to_list()) if i not in cut]
        config.messages.clear()
        config.messages.extend(kept)
    prep = SendPrep(stage=STAGE_LOOP)
    _build_wire(prep, config)
    _place_attached_files(prep, config)
    prep = order_for_wire(config, make_profile(model_name="claude-x", wire_format="anthropic_chat"), prep=prep, iteration=1)
    if stub:
        async def _over(_config):
            return [{"estimated_tokens": 1}]

        monkeypatch.setattr(input_fit, "_limits", _over)
        monkeypatch.setattr(input_fit, "_over", lambda limits: limits)
        monkeypatch.setattr(input_fit, "_enforced", lambda over: over)
        stats = asyncio.run(input_fit._stub_history_to_fit(prep.wire_config, list(prep.wire_config.messages)))
        prep.fit = {"passes": [dict(stats, on="wire")]}
    _settle_homed_off_wire(prep, config)
    return prep


def _platform_text(prep: SendPrep) -> str:
    texts = [getattr(c, "text", "") for m in prep.wire_config.messages for c in m.content]
    return [t for t in texts if t.startswith('<turn_context source="platform"')][-1]


def test_a_cut_home_leaves_the_template_turn_alone_and_the_note_stops_claiming_the_copy() -> None:
    from matrx_ai.config.attached_files import HOMED_OFF_WIRE_KEY

    def config_for() -> UnifiedConfig:
        config = _held_config(_template_history(), "Monday", held=False)
        config.messages.attach_turn_context('<object key="cards">Unchanged since turn 1.</object>', slot="manifest")
        config.metadata[CONTEXT_FILE_BLOCKS_KEY] = [dict(HELD_ENTRY, home="row-2", note=NOTE)]
        return config

    plain = config_for()
    whole = _settled(plain)
    template_bytes = [c.text for c in whole.wire_config.messages[0].content]
    assert "Unchanged since turn 1." in _platform_text(whole) and whole.homed_off_wire is None
    config = config_for()
    prep = _settled(config, cut={2, 3})
    assert [c.text for c in prep.wire_config.messages[0].content] == template_bytes, "the template turn changed"
    assert all(HELD_TEXT not in getattr(c, "text", "") for m in prep.wire_config.messages for c in m.content)
    text = _platform_text(prep)
    assert NOTE["off_wire"] in text and NOTE["text"] not in text, "the turn still claims a copy that is not sent"
    assert prep.homed_off_wire == [{"kind": HELD_COPY_KIND, "key": "cards", "why": "cut", "note_rewritten": True}]
    assert config.messages.to_list()[-1].metadata[HOMED_OFF_WIRE_KEY] == [{"kind": HELD_COPY_KIND, "key": "cards", "why": "cut"}]
    assert "Unchanged since turn 1." in (config.messages.render_turn_context() or ""), "the frozen block was rewritten"


def test_a_stubbed_home_is_reported_unclaimed_and_stamped_and_a_file_keeps_its_bytes(monkeypatch) -> None:
    from matrx_ai.config.attached_files import HOMED_OFF_WIRE_KEY
    from matrx_ai.config.input_fit import STUB_TEXT

    config = _held_config(_template_history(), "Monday", held=False)
    config.messages.attach_turn_context('<object key="cards">Unchanged since turn 1.</object>', slot="manifest")
    file_entry = {"key": KEY, "file_id": FILE_ID, "file_name": "inbound-oct16.csv", "text": CSV * 10}
    config.metadata[CONTEXT_FILE_BLOCKS_KEY] = [file_entry, dict(HELD_ENTRY, home="row-2", note=NOTE)]
    config.messages.to_list()[2].metadata[FILE_BLOCK_HOMES_KEY] = [KEY]
    prep = _settled(config, stub=True, monkeypatch=monkeypatch)
    home = [c.text for c in prep.wire_config.messages[2].content]
    assert home[0] == STUB_TEXT and home[1] == STUB_TEXT, "the file and the held copy are stubbed as before"
    stubbed = prep.fit["passes"][0]["homed_blocks_stubbed"]
    assert {"kind": "file", "key": KEY} in stubbed and {"kind": HELD_COPY_KIND, "key": "cards"} in stubbed
    assert NOTE["off_wire"] in _platform_text(prep) and NOTE["text"] not in _platform_text(prep)
    stamp = config.messages.to_list()[-1].metadata[HOMED_OFF_WIRE_KEY]
    assert stamp == [{"kind": HELD_COPY_KIND, "key": "cards", "why": "stubbed"}], "files are never stamped"


def test_prepare_for_send_settles_off_wire_homes_after_the_fit() -> None:
    from matrx_ai.config import send_boundary

    source = stable_source(send_boundary.prepare_for_send)
    assert source.index('"homed_off_wire"') > source.index("await _fit_wire(")


def test_the_fit_step_never_removes_a_homed_block() -> None:
    """``_fit_wire``'s removal pass takes only replayed platform turns; a homed block stays (the
    over-limit refusal decides), exactly as for files."""
    from matrx_ai.config.send_boundary import _drop_replayed_turn_context

    config = _held_config([_user("Quiz me on the deck.", 0)], "Monday", files=True)
    prep = SendPrep(stage=STAGE_LOOP)
    _build_wire(prep, config)
    _place_attached_files(prep, config)
    assert _drop_replayed_turn_context(prep.wire_config) == 0
    texts = [getattr(c, "text", "") for c in prep.wire_config.messages[0].content]
    assert texts[0].endswith(CSV) and texts[1].endswith(HELD_TEXT)
