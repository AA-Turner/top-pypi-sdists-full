"""What capture uploads, checked against what the consent screen promises.

The promise (`app/assistant/product.md`, held by
`dashboard/src/lib/capture-disclosure.test.ts`): file contents, command output
and search results are not sent. Through tap 0.9.9 it was broken in Claude Code capture
through three deny-lists (a top-level `toolUseResult`, file-bearing attachments,
unknown content blocks) and in Codex through `_codex_extras.action`. 0.9.10
turned the filters into allow-lists.

Two checks over every transcript fixture in the repo, for all four harnesses:

  * PRIVACY PROPERTIES — structural, so they hold for any input, not only the
    strings a fixture happens to contain: no `toolUseResult`, no tool_result
    body, no tool input beyond summary/stats, a shell command within
    COMMAND_MAX_LEN, no file-bearing attachment, nothing of an unknown block
    but its type, no `_codex_extras.action`.
  * BEFORE/AFTER (Claude Code) — 0.9.10's output differs from 0.9.9's ONLY by
    removals, and none of them is something a reader reads. 0.9.9's filters
    are frozen below as data; what readers read is spelled out from the
    engine's renderer, not taken from the sanitizer under test. 0.9.11's two
    additions (`inference_id`, `usage`) are checked against the raw message
    and set aside before the comparison. 0.9.13's two changes ARE read, and
    are spelled out here too: what a command the researcher ran printed
    (`<bash-stdout>`, `<local-command-stdout>`, ...) becomes its size, and a
    loaded skill's body is dropped.

Tap 0.9.13 also holds every harness to the same rule for a researcher's own
shell command: the command ships, what it printed does not, only its size
(Claude Code's `!command` and local commands, Codex's `<user_shell_command>`,
pi's bashExecution, Kimi's shell mode).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest

from probe.tap_core import codex_sanitize, kimi_sanitize, pi_sanitize, sanitize
from probe.tap_core.sanitize import COMMAND_MAX_LEN, USAGE_KEYS

_AGENT = Path(__file__).resolve().parent.parent
_FIXTURES = _AGENT / "tests" / "fixtures"
_TAP_FIXTURES = _AGENT / "plugins" / "probe-research-tap" / "tests" / "fixtures"

#: Synthetic Claude Code session shaped like real CC 2.x lines, with a marker
#: planted in every place file content, tool output, tool input or a search
#: result appears in the raw file.
CC_SYNTHETIC = _FIXTURES / "probe_events" / "claude_code" / "raw.jsonl"
#: The other harnesses' probe-events goldens (test_probe_events_contract.py).
_GOLDEN = {h: _FIXTURES / "probe_events" / h / "raw.jsonl" for h in ("codex", "pi", "kimi_code")}
PLANTED = ("FILE-CONTENT-7f3a", "TOOL-OUTPUT-9b2c", "TOOL-INPUT-4d1e", "SEARCH-RESULT-2e8d", "iVBORw0KGgo",
           "COMMAND-OUTPUT-5a6b", "SKILL-BODY-6d2a")

_HARNESS_FIXTURES: dict[str, tuple[Any, list[Path]]] = {
    "claude_code": (
        sanitize,
        [CC_SYNTHETIC, *sorted((_FIXTURES / "daemon_adapters" / "claude_code").glob("*.jsonl"))],
    ),
    "codex": (
        codex_sanitize,
        [
            _GOLDEN["codex"],
            _TAP_FIXTURES / "rollout-sample.jsonl",
            *sorted((_FIXTURES / "daemon_adapters" / "codex").glob("*.jsonl")),
        ],
    ),
    "pi": (
        pi_sanitize,
        [
            _GOLDEN["pi"],
            *sorted((_TAP_FIXTURES / "pi").glob("*.jsonl")),
            *sorted((_FIXTURES / "daemon_adapters" / "pi").glob("*.jsonl")),
        ],
    ),
    "kimi_code": (
        kimi_sanitize,
        [
            _GOLDEN["kimi_code"],
            *sorted((_FIXTURES / "kimi_code" / "sessions").glob("*/*/agents/*/wire.jsonl")),
            *sorted((_FIXTURES / "daemon_adapters" / "kimi_code").glob("*.jsonl")),
        ],
    ),
}

_CASES = [
    pytest.param(module, path, id=f"{harness}:{path.relative_to(_AGENT)}")
    for harness, (module, paths) in _HARNESS_FIXTURES.items()
    for path in paths
]


def _raw_events(path: Path) -> list[Any]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _sanitized(module: Any, path: Path) -> list[dict]:
    out: list[dict] = []
    for raw in _raw_events(path):
        value = module.sanitize_event(raw)
        out.extend(value if isinstance(value, list) else [] if value is None else [value])
    return out


def test_every_harness_has_fixtures() -> None:
    for harness, (_module, paths) in _HARNESS_FIXTURES.items():
        assert paths and all(p.is_file() for p in paths), harness


# ---------------------------------------------------------------------------
# Privacy properties
# ---------------------------------------------------------------------------

_TOP_LEVEL = {
    "type", "subtype", "message", "content", "isCompactSummary", "timestamp",
    "uuid", "parentUuid", "logicalParentUuid", "attachment",
    "_codex_extras", "_pi_extras", "_kimi_extras",
    # probe-events/1 (tap 0.9.11): ids, four counts and one enum value.
    "inference_id", "usage", "origin",
}
_MESSAGE = {"role", "content", "model", "stop_reason"}
#: Block type -> the keys it may carry. tool_use carries a summary and counts,
#: never `input`; tool_result a size, never `content`. pi names its counts
#: `edit_stats`.
_BLOCK_KEYS = {
    "text": {"type", "text"},
    "thinking": {"type", "thinking"},
    "tool_use": {"type", "id", "name", "summary", "stats", "edit_stats"},
    "tool_result": {"type", "tool_use_id", "is_error", "result_bytes"},
    "unknown_block": {"type", "block_type"},  # pi and Kimi's marker
}
_MEDIA = {"image", "audio", "video"}
_STAT_VALUES = (int, bool, str)  # counts, replace_all, op / mode labels
_ATTACHMENTS = {"compact_file_reference": {"type", "filename", "displayPath"}}


def _check_block(block: Any, where: str) -> None:
    assert isinstance(block, dict), where
    kind = block.get("type")
    if block.get("dropped") is True:
        assert set(block) == {"type", "dropped"} and isinstance(kind, str), where
        return
    if kind in _MEDIA:
        # A type and a size, or a remote URL kept as a pointer -- never bytes.
        if "source" in block:
            assert set(block) == {"type", "source"}, where
            assert set(block["source"]) == {"type", "url"}, where
            assert block["source"]["url"].startswith(("http://", "https://")), where
        else:
            assert set(block) <= {"type", "mimeType", "bytes"}, where
            assert isinstance(block.get("bytes", 0), int), where
        return
    assert kind in _BLOCK_KEYS, f"{where}: unknown block type {kind!r} shipped"
    assert set(block) <= _BLOCK_KEYS[kind], f"{where}: {kind} carries {set(block) - _BLOCK_KEYS[kind]}"
    if kind == "tool_use":
        summary = block.get("summary", "")
        assert isinstance(summary, str) and len(summary) <= COMMAND_MAX_LEN, where
        for stats in (block.get("stats"), block.get("edit_stats")):
            if stats is not None:
                assert all(isinstance(v, _STAT_VALUES) for v in stats.values()), where
                assert all(len(v) <= 32 for v in stats.values() if isinstance(v, str)), where


@pytest.mark.parametrize("module,path", _CASES)
def test_privacy_properties_hold_for_every_sanitized_event(module: Any, path: Path) -> None:
    events = _sanitized(module, path)
    assert events, "a fixture that sanitizes to nothing proves nothing"
    for i, event in enumerate(events):
        where = f"{path.name}#{i}"
        assert isinstance(event, dict), where
        assert set(event) <= _TOP_LEVEL, f"{where}: {set(event) - _TOP_LEVEL}"
        assert "toolUseResult" not in event
        assert "action" not in event.get("_codex_extras", {}), where
        if "usage" in event:
            assert set(event["usage"]) <= set(USAGE_KEYS), where
            assert all(type(v) is int for v in event["usage"].values()), where
        assert isinstance(event.get("inference_id", ""), str), where
        assert event.get("origin", "user_shell") == "user_shell", where
        if "content" in event:
            assert isinstance(event["content"], str), where
        if event.get("type") == "attachment":
            attachment = event.get("attachment")
            assert isinstance(attachment, dict) and attachment.get("type") in _ATTACHMENTS, where
            assert set(attachment) <= _ATTACHMENTS[attachment["type"]], where
        else:
            assert "attachment" not in event, where
        message = event.get("message")
        if message is None:
            continue
        assert isinstance(message, dict) and set(message) <= _MESSAGE, f"{where}: {set(message) - _MESSAGE}"
        content = message.get("content", "")
        if isinstance(content, str):
            continue
        assert isinstance(content, list), where
        for block in content:
            _check_block(block, where)


def test_nothing_planted_in_the_synthetic_session_ships() -> None:
    """Belt to the properties' braces: the markers sit in toolUseResult, tool
    inputs, tool_result bodies, file / nested_memory / edited_text_file
    attachments, an unknown attachment, server tool and search result blocks,
    an unknown top-level key, a pasted image, a file-history-delta, a
    `!command`'s `<bash-stdout>`, a local command's `<local-command-stdout>`
    (on a user turn and on a system event) and a loaded skill's body."""
    raw = CC_SYNTHETIC.read_text()
    for marker in PLANTED:
        assert marker in raw, f"fixture no longer plants {marker}"
    shipped = json.dumps(_sanitized(sanitize, CC_SYNTHETIC))
    for marker in PLANTED:
        assert marker not in shipped, marker
    # ...while the conversation itself still ships.
    for kept in ("Train the baseline", "I will run the baseline first.", "lr lowered to 3e-4",
                 "Eval split done", "also run the eval split", "Conversation compacted",
                 # the researcher's commands, and the size of what they printed
                 "<bash-input>python eval.py --split test</bash-input>",
                 "<bash-stdout>[output not sent: 53 chars]</bash-stdout><bash-stderr></bash-stderr>",
                 "<local-command-stdout>[output not sent: 37 chars]</local-command-stdout>",
                 "<command-name>/eval-report</command-name>"):
        assert kept in shipped, kept


def test_the_full_shell_command_ships_up_to_its_cap() -> None:
    """The cap is the documented bound, not a reason to drop the command: the
    synthetic heredoc is longer than COMMAND_MAX_LEN and ships cut to it."""
    raw_command = next(
        b["input"]["command"]
        for e in _raw_events(CC_SYNTHETIC) if e.get("type") == "assistant"
        for b in e["message"]["content"] if b.get("name") == "Bash"
    )
    assert len(raw_command) > COMMAND_MAX_LEN
    summaries = [
        b["summary"]
        for e in _sanitized(sanitize, CC_SYNTHETIC) if e.get("type") == "assistant"
        for b in e["message"]["content"] if b.get("name") == "Bash"
    ]
    assert summaries == [raw_command[:COMMAND_MAX_LEN]]


# ---------------------------------------------------------------------------
# 0.9.13: what a researcher's own command printed, and a loaded skill's body
# ---------------------------------------------------------------------------

#: Harness -> (what its golden's researcher-typed commands printed, the size
#: that ships instead). Kimi's size counts its `<bash-stdout>` tags too.
_SHELL_OUTPUT = {
    "claude_code": (("COMMAND-OUTPUT-5a6b",), "[output not sent: 53 chars]"),
    "codex": (("COMMAND-OUTPUT-5a6b",), "Output:\\n[output not sent: 32 chars]\\n</result>"),
    "pi": (("M notes.md", "FAILED 1 test"), '"result_bytes": 13'),
    "kimi_code": (("a1b2c3d fix",), '"result_bytes": 39'),
}


@pytest.mark.parametrize("harness", sorted(_SHELL_OUTPUT))
def test_no_harness_ships_what_a_researchers_command_printed(harness: str) -> None:
    """The consent screen: command output is not sent. A command the researcher
    typed (`!cmd`, a local slash command, shell mode) ships; what it printed
    ships as its size."""
    path = CC_SYNTHETIC if harness == "claude_code" else _GOLDEN[harness]
    printed, size = _SHELL_OUTPUT[harness]
    shipped = json.dumps(_sanitized(_HARNESS_FIXTURES[harness][0], path))
    for text in printed:
        assert text in path.read_text(), f"the fixture no longer plants {text!r}"
        assert text not in shipped, text
    assert size in shipped


@pytest.mark.parametrize(
    "text",
    [
        "<bash-stdout>A</bash-stdout>LEAK</bash-stdout><bash-stderr>B</bash-stderr>",
        "<bash-stdout>A</bash-stdout>LEAK<bash-stderr>LEAK</bash-stdout><bash-stderr>B</bash-stderr>",
        "<bash-stdout>A <bash-stdout>LEAK</bash-stdout> LEAK</bash-stdout><bash-stderr></bash-stderr>",
        "<local-command-stdout>never closed LEAK",
        "<bash-stdout>A</bash-stdout><bash-stderr>never closed LEAK",
    ],
    ids=["fake-close", "fake-close-and-open", "nested", "unclosed", "unclosed-second"],
)
def test_output_that_prints_the_tags_themselves_still_does_not_ship(text: str) -> None:
    """A `!cat` of a transcript, or a grep of this repo, prints the tags. From
    the first open tag to the last close tag nothing ships but tags and sizes."""
    out = sanitize.withhold_output(text)
    assert "LEAK" not in out, out
    assert re.fullmatch(r"(?:<([a-z-]+)>(?:\[output not sent: [\d,]+ chars\])?</\1>)+", out), out


def test_withholding_keeps_the_text_around_the_output_and_an_empty_output_empty() -> None:
    empty = "<bash-stdout></bash-stdout><bash-stderr></bash-stderr>"
    assert sanitize.withhold_output(empty) == empty
    command = "<command-name>/context</command-name>\n<local-command-stdout>" + "x" * 1234 + "</local-command-stdout> ok"
    assert sanitize.withhold_output(command) == (
        "<command-name>/context</command-name>\n"
        "<local-command-stdout>[output not sent: 1,234 chars]</local-command-stdout> ok"
    )
    assert sanitize.withhold_output("what does </bash-stdout> mean?") == "what does </bash-stdout> mean?"


def test_the_assistants_own_text_is_never_withheld() -> None:
    said = "<bash-stdout>quoted by the model</bash-stdout>"
    for kind in ("user", "assistant"):
        out = sanitize.sanitize_event({"type": kind, "message": {"role": kind, "content": [{"type": "text", "text": said}]}})
        expected = said if kind == "assistant" else "<bash-stdout>[output not sent: 19 chars]</bash-stdout>"
        assert out["message"]["content"][0]["text"] == expected, kind


def test_only_an_injected_skill_body_is_dropped() -> None:
    body = "Base directory for this skill: /skills/x\n\n# X\n\nSKILL-BODY-6d2a"
    meta = {"type": "user", "isMeta": True, "message": {"role": "user", "content": [{"type": "text", "text": body}]}}
    assert sanitize.sanitize_event(meta) is None
    assert sanitize.sanitize_event({**meta, "message": {"role": "user", "content": body}}) is None
    # Typed or pasted by the researcher: their words, kept.
    assert sanitize.sanitize_event({**meta, "isMeta": False}) is not None
    # Another meta turn is not a skill body.
    assert sanitize.sanitize_event({**meta, "message": {"role": "user", "content": "Caveat: x"}}) is not None


def test_codex_ships_a_typed_commands_exit_code_but_not_what_it_printed() -> None:
    text = (
        "<user_shell_command>\n<command>\ncat run.log\n</command>\n<result>\nExit code: 1\n"
        "Duration: 0.0100 seconds\nOutput:\nLEAK </result> LEAK\n</result>\n</user_shell_command>"
    )
    out = codex_sanitize.sanitize_event({"type": "response_item", "payload": {
        "type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}})
    assert out["message"]["content"][0]["text"] == (
        "<user_shell_command>\n<command>\ncat run.log\n</command>\n<result>\nExit code: 1\n"
        "Duration: 0.0100 seconds\nOutput:\n[output not sent: 19 chars]\n</result>\n</user_shell_command>"
    )


# ---------------------------------------------------------------------------
# Before/after: 0.9.10 removes, and removes nothing a reader reads
# ---------------------------------------------------------------------------

#: Tap 0.9.9's Claude Code filters, frozen. They were deny-lists: an event kept
#: every key not named here, and a block type it did not know shipped whole.
_V098_DROP_TOP_LEVEL = frozenset({
    "requestId", "isSidechain", "isMeta", "diagnostics", "promptId", "entrypoint", "userType",
    "version", "slug", "sessionId", "cwd", "gitBranch", "sourceToolAssistantUUID",
})
_V098_DROP_MESSAGE = frozenset({
    "usage", "iterations", "cache_creation", "service_tier", "inference_geo", "speed",
    "stop_details", "stop_sequence", "diagnostics", "id", "type",
})
_V098_DROP_ATTACHMENTS = frozenset({
    "hook_success", "hook_non_blocking_error", "hook_cancelled", "hook_system_message",
    "hook_additional_context", "task_reminder", "queued_command", "deferred_tools_delta",
    "skill_listing", "invoked_skills", "agent_listing_delta", "mcp_instructions_delta",
    "command_permissions", "date_change", "ultra_effort_enter", "plan_mode_exit", "dynamic_skill",
})


def _v098(event: Any) -> Any:
    """Tap 0.9.9's `sanitize_event`, rebuilt from its frozen filters. Event-type
    and system-subtype drops and the tool_use / tool_result compaction did not
    change in 0.9.10, so those come from the current module."""
    if not isinstance(event, dict) or event.get("type") in sanitize._DROP_EVENT_TYPES:
        return None if isinstance(event, dict) else event
    if event.get("type") == "system" and event.get("subtype") in sanitize._DROP_SYSTEM_SUBTYPES:
        return None
    attachment = event.get("attachment")
    if event.get("type") == "attachment" and isinstance(attachment, dict):
        if attachment.get("type") in _V098_DROP_ATTACHMENTS:
            return None
    out = {k: v for k, v in event.items() if k not in _V098_DROP_TOP_LEVEL}
    message = out.get("message")
    if isinstance(message, dict):
        message = {k: v for k, v in message.items() if k not in _V098_DROP_MESSAGE}
        if isinstance(message.get("content"), list):
            blocks = []
            for block in message["content"]:
                kind = block.get("type") if isinstance(block, dict) else None
                if kind in ("tool_use", "tool_result"):
                    blocks.append(sanitize._sanitize_block(block))
                elif kind == "thinking":
                    if isinstance(block.get("thinking"), str) and block["thinking"].strip():
                        blocks.append({k: v for k, v in block.items() if k != "signature"})
                else:
                    blocks.append(block)
            message["content"] = blocks
        out["message"] = message
    return out


#: Tap 0.9.13's two changes to what a reader reads, spelled out here rather
#: than taken from the sanitizer: plain non-greedy tag pairing, exact for
#: well-formed lines (the sanitizer's fail-closed handling of output that fakes
#: a tag is tested on its own below).
_OUTPUT_PAIR = re.compile(r"<(bash-stdout|bash-stderr|local-command-stdout|local-command-stderr)>(.*?)</\1>", re.S)
_SKILL_BODY = "Base directory for this skill:"


def _withheld(text: str) -> str:
    def size(m: re.Match) -> str:
        inner = m.group(2)
        return f"<{m.group(1)}>" + (f"[output not sent: {len(inner):,} chars]" if inner else "") + f"</{m.group(1)}>"

    return _OUTPUT_PAIR.sub(size, text)


def _texts(message: Any) -> list[str]:
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, str):
        return [content]
    if isinstance(content, list):
        return [b["text"] for b in content if isinstance(b, dict) and b.get("type") == "text" and isinstance(b.get("text"), str)]
    return []


def _v0913(raw: Any, before: Any) -> Any:
    """0.9.9's output with 0.9.13's changes applied: a loaded skill's body
    (an `isMeta` user turn starting with _SKILL_BODY) is gone, and outside the
    assistant's own text, each command-output tag holds its size."""
    if not isinstance(before, dict) or before.get("type") == "assistant":
        return before
    if raw.get("type") == "user" and raw.get("isMeta") is True:
        if any(t.lstrip().startswith(_SKILL_BODY) for t in _texts(raw.get("message"))):
            return None
    out = json.loads(json.dumps(before))
    if isinstance(out.get("content"), str):
        out["content"] = _withheld(out["content"])
    message = out.get("message")
    if isinstance(message, dict):
        if isinstance(message.get("content"), str):
            message["content"] = _withheld(message["content"])
        elif isinstance(message.get("content"), list):
            for block in message["content"]:
                if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                    block["text"] = _withheld(block["text"])
    return out


def _what_readers_read(event: dict | None) -> Any:
    """Every field of an event a reader of the upload reads.

    Spelled out from prbe-knowledge `engine/shared/transcript_render.py`
    (`_render_event`, `_render_user`, `_render_assistant`, `_render_tool_use`),
    `kb/handlers/claude_code.py` (`_count_compactions`, the first event's
    `content`, the session-complete `timestamp` check) and
    `engine/shared/claude_code_extraction.py` (`isCompactSummary`,
    `compact_boundary`). The ids are the event's identity and order.
    """
    if event is None:
        return None
    message = event.get("message") if isinstance(event.get("message"), dict) else {}
    content = message.get("content")
    blocks = []
    if isinstance(content, list):
        for b in content:
            if not isinstance(b, dict):
                continue
            kind = b.get("type")
            if kind == "text":
                blocks.append(("text", b.get("text")))
            elif kind == "thinking":
                blocks.append(("thinking", b.get("thinking")))
            elif kind == "tool_use":
                blocks.append(("tool_use", b.get("id"), b.get("name"), b.get("summary"), b.get("stats")))
            elif kind == "tool_result":
                blocks.append(("tool_result", b.get("tool_use_id"), b.get("is_error"), b.get("result_bytes")))
    return (
        event.get("type"), event.get("subtype"),
        event.get("content") if isinstance(event.get("content"), str) else None,
        event.get("isCompactSummary"), event.get("timestamp"),
        event.get("uuid"), event.get("parentUuid"), event.get("logicalParentUuid"),
        content if isinstance(content, str) else tuple(blocks),
        message.get("stop_reason"), message.get("model"),
    )


def _removals_only(before: Any, after: Any, where: str) -> None:
    """`after` is `before` with things taken away, never added or changed --
    except a block 0.9.9 forwarded whole, which 0.9.10 replaces with a marker
    (an unknown type) or a placeholder (a pasted image)."""
    if isinstance(before, dict) and isinstance(after, dict):
        if before.get("type") not in _BLOCK_KEYS and after.get("dropped") is True:
            assert after == {"type": before.get("type"), "dropped": True}, where
            return
        if before.get("type") == "image" and set(after) <= {"type", "mimeType", "bytes", "source"}:
            return
        assert set(after) <= set(before), f"{where}: added {set(after) - set(before)}"
        for key in after:
            _removals_only(before[key], after[key], f"{where}.{key}")
        return
    if isinstance(before, list) and isinstance(after, list):
        kept = [b for b in before if isinstance(b, dict)]
        assert len(after) == len(kept), where
        for i, (b, a) in enumerate(zip(kept, after)):
            _removals_only(b, a, f"{where}[{i}]")
        return
    assert before == after, where


@pytest.mark.parametrize("path", _HARNESS_FIXTURES["claude_code"][1], ids=lambda p: p.name)
def test_claude_code_output_differs_from_0_9_8_only_by_removals_no_reader_reads(path: Path) -> None:
    dropped_attachments = 0
    for i, raw in enumerate(_raw_events(path)):
        before, after = _v0913(raw, _v098(raw)), sanitize.sanitize_event(raw)
        where = f"{path.name}#{i}"
        if after is None and before is not None:
            # A whole event goes only when it is an attachment off the allow-list.
            assert before.get("type") == "attachment", where
            assert before["attachment"].get("type") not in _ATTACHMENTS, where
            dropped_attachments += 1
            continue
        if before is None:
            assert after is None, where
            continue
        # The two fields 0.9.11 ADDS (probe-events/1) are lifted from the
        # message 0.9.8 already stripped; the rest must still be removals only.
        after = dict(after)
        message = raw.get("message") if isinstance(raw.get("message"), dict) else {}
        assert after.pop("inference_id", None) == (message.get("id") if raw["type"] == "assistant" else None), where
        usage = after.pop("usage", None)
        if usage is not None:
            assert raw["type"] == "assistant" and usage == {k: message["usage"][k] for k in usage}, where
        _removals_only(before, after, where)
        assert _what_readers_read(after) == _what_readers_read(before), where
    assert dropped_attachments, "every CC fixture carries an attachment 0.9.9 shipped"


# -- one hostile line costs that line, never the session ----------------------------

_HOSTILE_VALUES: list[Any] = [None, 0, -1, 1.5, True, "", "x" * 10_000, [], [1, "a"], {}, {"k": "v"},
                              {"type": "user"}, [{"type": "text"}], "\x00"]
_SANITIZERS = [sanitize.sanitize_event, codex_sanitize.sanitize_event, pi_sanitize.sanitize_event,
               kimi_sanitize.sanitize_event]


def _mutations(event: Any, path: tuple = ()) -> Any:
    """Every (path, value) replacing one field of `event`, recursively."""
    if isinstance(event, dict):
        for key, value in event.items():
            for hostile in _HOSTILE_VALUES:
                yield (*path, key), hostile
            yield from _mutations(value, (*path, key))
    elif isinstance(event, list):
        for i, value in enumerate(event[:3]):
            yield from _mutations(value, (*path, i))


def _replace(event: Any, path: tuple, value: Any) -> Any:
    out = json.loads(json.dumps(event))
    target = out
    for step in path[:-1]:
        target = target[step]
    target[path[-1]] = value
    return out


def test_the_claude_code_sanitizer_survives_a_hostile_type_on_type_and_subtype() -> None:
    for value in _HOSTILE_VALUES:
        sanitize.sanitize_event({"type": value, "message": {"content": "hi"}})
        sanitize.sanitize_event({"type": "system", "subtype": value, "content": "x"})


def test_codex_summarizes_an_empty_argument_string() -> None:
    out = codex_sanitize.sanitize_event({"type": "response_item", "payload": {
        "type": "function_call", "name": "shell", "call_id": "c1", "arguments": ""}})
    assert out is not None


def test_codex_drops_an_agents_md_turn() -> None:
    body = "# AGENTS.md instructions for /repo\n\n<INSTRUCTIONS>\nsecret house rules\n</INSTRUCTIONS>"
    out = codex_sanitize.sanitize_event({"type": "response_item", "payload": {
        "type": "message", "role": "user", "content": [{"type": "input_text", "text": body}]}})
    assert "secret house rules" not in json.dumps(out)


def test_a_line_no_sanitizer_can_handle_is_dropped_and_the_batch_still_builds(monkeypatch) -> None:
    from probe.tap_core import transcript

    def explodes(event: Any) -> Any:
        if event.get("boom"):
            raise TypeError("hostile")
        return event

    body = transcript.build_batch_body(
        device_id="d", session_id="s", batch_seq=0, cwd="/w", base_line_no=0,
        lines=[json.dumps({"type": "user", "boom": True}).encode(),
               json.dumps({"type": "user", "keep": "me"}).encode()],
        sanitize=explodes,
    )
    assert b"keep" in body and b"boom" not in body


@pytest.mark.parametrize("harness", sorted(_HARNESS_FIXTURES))
def test_no_sanitizer_raises_on_a_hostile_field(harness: str) -> None:
    """14 hostile values over every field of the first 40 events of each fixture.
    The journal contains a raise anyway (it costs that line), but a sanitizer
    that raises drops a line it could have kept."""
    module, paths = _HARNESS_FIXTURES[harness]
    failures = []
    for path in paths:
        for event in _raw_events(path)[:40]:
            for field_path, value in _mutations(event):
                try:
                    module.sanitize_event(_replace(event, field_path, value))
                except Exception as exc:  # noqa: BLE001
                    failures.append((path.name, field_path, repr(value)[:40], type(exc).__name__))
    assert failures == [], failures[:5]


def test_codex_drops_an_older_user_instructions_turn() -> None:
    body = "<user_instructions>\nsecret house rules\n</user_instructions>"
    out = codex_sanitize.sanitize_event({"type": "response_item", "payload": {
        "type": "message", "role": "user", "content": [{"type": "input_text", "text": body}]}})
    assert "secret house rules" not in json.dumps(out)


def test_nesting_check_is_iterative_and_bounded() -> None:
    from probe.tap_core.transcript import MAX_EVENT_DEPTH, nesting_exceeds

    deep: Any = 1
    for _ in range(5000):
        deep = {"k": deep}
    assert nesting_exceeds(deep)
    shallow: Any = 1
    for _ in range(MAX_EVENT_DEPTH - 1):
        shallow = [shallow]
    assert not nesting_exceeds({"a": shallow})  # depth 64: allowed


def test_a_task_notifications_event_bodies_are_withheld_and_its_notice_stays() -> None:
    text = ("<task-notification>\n<task-type>monitor</task-type>\n<summary>2 new lines</summary>\n"
            "<event>MONITOR-OUTPUT-1</event>\n<event>MONITOR-OUTPUT-2</event>\n</task-notification>")
    out = sanitize.withhold_output(text)
    assert "MONITOR-OUTPUT" not in out
    assert "<summary>2 new lines</summary>" in out and out.count("[output not sent:") == 2
    assert sanitize.withhold_output("my <event>own words</event>") == "my <event>own words</event>"
    unclosed = sanitize.withhold_output("<task-notification><event>CUT-OFF-OUTPUT")
    assert "CUT-OFF-OUTPUT" not in unclosed


def test_a_truncated_codex_shell_record_ships_nothing_after_a_fake_close() -> None:
    text = ("<user_shell_command>\n<command>cat log</command>\n<result>\nExit code: 0\nOutput:\n"
            "line one\n</result>\nLEAKED-AFTER-FAKE-CLOSE")
    out = codex_sanitize._withhold_shell_output(text)
    assert "LEAKED-AFTER-FAKE-CLOSE" not in out and "line one" not in out
