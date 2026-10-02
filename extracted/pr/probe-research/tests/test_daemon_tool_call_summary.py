"""A tool call that runs no command is still visible to the daemon (lineage plan L8).

A WebFetch URL, a Read path, an MCP call's arguments were stored (redacted) but
never rendered or indexed: `Event.command()` reads only `command`/`cmd`/`input`,
the chat shows `command or text`, and search indexes text and command. So the
daemon could not see which paper page an agent read, nor cite that event. Now
`Store.add` gives such a call a one-line summary of its key arguments as its
text -- for every harness, since all three adapters pass through it -- and
never as its command, which the working-folder check reads.
"""

from __future__ import annotations

import json
from pathlib import Path

from probe.daemon import adapters, bite
from probe.daemon.events import Kind
from probe.daemon.store import Store, call_summary

FAKE_KEY = "sk-ant-api03-" + "A" * 93 + "AA"


def _parse(source: str, lines: list[dict]) -> list:
    adapter = adapters.for_source(source)
    if source == "claude_code":
        adapter.session_files(Path("/x/s1.jsonl"))
    out, off = [], 0
    for obj in lines:
        raw = json.dumps(obj).encode()
        off += len(raw) + 1
        out.extend(adapter.parse_bytes(raw, stream="main", offset=off))
    return out


CLAUDE = [{"type": "assistant", "message": {"content": [
    {"type": "tool_use", "id": "t1", "name": "WebFetch",
     "input": {"url": "https://arxiv.org/abs/2401.00001", "prompt": "what loss does it use?"}},
    {"type": "tool_use", "id": "t2", "name": "Read", "input": {"file_path": "/w/configs/best.yaml", "limit": 40}},
    {"type": "tool_use", "id": "t3", "name": "Edit",
     "input": {"file_path": "/w/train.py", "old_string": "lr=1e-3", "new_string": "lr=3e-4"}},
    {"type": "tool_use", "id": "t4", "name": "Bash", "input": {"command": "python train.py"}}]}}]
CODEX = [{"type": "response_item", "payload": {"type": "function_call", "name": "mcp__probe__find_papers",
                                               "arguments": json.dumps({"query": "label smoothing calibration"}),
                                               "call_id": "c1"}}]
PI = [{"type": "message", "message": {"role": "assistant", "content": [
    {"type": "toolCall", "id": "p1", "name": "read", "arguments": {"path": "/w/results/eval.json"}}]}}]


def _stored(tmp_path, source, lines) -> Store:
    store = Store(tmp_path / f"{source}.sqlite", clock=lambda: 1000.0)
    store.add(_parse(source, lines))
    return store


def _calls(store: Store):
    return [e for e in store.events_between(1) if e.kind == Kind.TOOL_CALL]


def test_every_harness_stores_the_arguments_of_a_call_with_no_command(tmp_path):
    fetch, read, edit, shell = _calls(_stored(tmp_path, "claude_code", CLAUDE))
    assert fetch.text == "url=https://arxiv.org/abs/2401.00001 · prompt=what loss does it use?"
    assert read.text == "file_path=/w/configs/best.yaml · limit=40"
    assert edit.text == "file_path=/w/train.py"  # the edit's content is not an address
    assert shell.text == "" and shell.command == "python train.py"  # a command stays the command
    for call in (fetch, read, edit):
        assert call.command is None, "never a command: the working folders are read from commands"
    [papers] = _calls(_stored(tmp_path, "codex", CODEX))
    assert papers.text == "query=label smoothing calibration" and papers.command is None
    [pi_read] = _calls(_stored(tmp_path, "pi", PI))
    assert pi_read.text == "path=/w/results/eval.json" and pi_read.command is None


def test_the_summary_renders_is_searchable_and_heads_its_output(tmp_path):
    from probe.daemon import approvals as appr
    from probe.daemon import tools

    store = _stored(tmp_path, "claude_code", CLAUDE + [{"type": "user", "message": {"content": [
        {"type": "tool_result", "tool_use_id": "t1", "content": "It uses focal loss."}]}}])
    fetch = _calls(store)[0]
    assert bite.render(fetch) == (f"[agent ran WebFetch · {fetch.event_id}] "
                                  "url=https://arxiv.org/abs/2401.00001 · prompt=what loss does it use?")
    assert [e.event_id for e in store.search("arxiv 2401")] == [fetch.event_id]
    deps = tools.Deps(store=store, board=appr.Board(tmp_path / "appr"), session_id="s", cwd=tmp_path,
                      workdirs=[tmp_path], home=tmp_path, write_dirs=[], probe_env={}, bypass=False,
                      mode_known=True, bite_id=1, replay=object())
    found = tools.session(deps, "search", query="arxiv")
    assert fetch.event_id in found and "url=https://arxiv.org" in found
    output = next(e for e in store.events_between(1) if e.kind == Kind.TOOL_OUTPUT)
    opened = tools.session(deps, "open", event_id=output.event_id)
    assert "output of: WebFetch url=https://arxiv.org/abs/2401.00001" in opened and "focal loss" in opened


def test_the_summary_is_scrubbed_one_line_and_bounded():
    line = call_summary({"url": "https://h.test/x", "query": "a\nb\tc", "prompt": "p" * 500,
                         "headers": {"a": "b"}, "run_in_background": True, "pattern": ""})
    assert "\n" not in line and "query=a b c" in line
    assert "prompt=" + "p" * 199 + "…" in line and "headers" not in line and "run_in_background" not in line
    assert len(call_summary({f"k{i}": "v" * 200 for i in range(10)})) <= 600
    assert call_summary({"content": "the whole file"}) == ""


def test_a_credential_in_an_argument_never_reaches_the_summary(tmp_path):
    store = _stored(tmp_path, "claude_code", [{"type": "assistant", "message": {"content": [
        {"type": "tool_use", "id": "t9", "name": "WebFetch",
         "input": {"url": f"https://api.test/v1?key={FAKE_KEY}"}}]}}])
    [call] = _calls(store)
    assert call.text.startswith("url=https://api.test/v1") and FAKE_KEY not in call.text
    assert store.search(FAKE_KEY[:20]) == []
