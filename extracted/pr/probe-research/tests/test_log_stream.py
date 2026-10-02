"""The live console log (plan item (h)): what the shipper sends, and when.

`probe.sdk.logstream` reads the helper's spool (`logcapture.LiveSpool`) and
POSTs complete, redacted lines to `/v1/runs/{id}/log-chunks`. These drive it
against the in-memory API (`FakeApp`, through the real `Transport`), with the
spool written by the real `LiveSpool` -- and end to end through `run.execute`,
where the real helper process writes the spool.
"""

from __future__ import annotations

import inspect
import os
import sys

import pytest

from probe.sdk import logstream, outputs
from probe.sdk.logcapture import LiveSpool, list_segments, live_dir
from probe.sdk.logstream import (
    MAX_CHUNK_RAW_BYTES,
    MAX_PARTIAL_LINE_BYTES,
    MAX_PEM_HOLD_BYTES,
    MAX_TOKEN_RUN_BYTES,
    LogStreamer,
    Mode,
    collapse_redraws,
    plan_cut,
    render,
    shippable,
)
from probe.sdk.transport import Transport
from tests.conftest import open_run

TOKEN = "ghp_A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
PEM_BODY = [
    "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC7VJTUt9Us8cKj",
    "MzEfYyjiWA4R4/M2bS1GB4t7NXp98C3SC6dVMvDuictGeurT8jNbvJZHtCSuYEvu",
    "NMoSfm76oqFvAp8Gy0iz5sxjZmSnXyCdPEovGhLa0VzMaQ8s+CLOyS56YyCFGeJZ",
]
PEM = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(PEM_BODY) + "\n-----END PRIVATE KEY-----\n"


@pytest.fixture(autouse=True)
def _streaming_env(monkeypatch):
    for name in ("RANK", "SLURM_PROCID", "OMPI_COMM_WORLD_RANK", "PMI_RANK", "WORLD_SIZE", "SLURM_NTASKS"):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.delenv(logstream.MODE_ENV, raising=False)
    monkeypatch.delenv(logstream.INTERVAL_ENV, raising=False)


@pytest.fixture
def streaming(app):
    app.supports_run_log_stream = True
    return app


def _spool(tmp_path) -> tuple[str, LiveSpool]:
    log_path = str(tmp_path / "run.log")
    os.makedirs(live_dir(log_path))
    return log_path, LiveSpool(live_dir(log_path))


def _streamer(client, run, log_path, **kw) -> LogStreamer:
    return LogStreamer(client, run.id, log_path, "run", interval=0.05, **kw)


def _texts(app, run) -> str:
    chunks = app.log_chunks.get(run.id, {})
    return "".join(c["text"] for (_s, _o), c in sorted(chunks.items(), key=lambda kv: kv[0][1]))


def _chunk_requests(app) -> list:
    return [r for r in app.requests if r.url.path.endswith("/log-chunks")]


# -- pure: what may ship --------------------------------------------------------------
def test_only_complete_lines_ship_and_a_short_partial_waits():
    assert shippable(b"loss 1.0\nloss 0.9\nloss 0.", final=False) == len(b"loss 1.0\nloss 0.9\n")
    assert shippable(b"half a line", final=False) == 0
    # The stream ended: its last line ships without a newline.
    assert shippable(b"half a line", final=True) == len(b"half a line")


def test_a_partial_line_too_long_to_hold_is_cut_at_a_redraw_or_space():
    bar = b"\r".join(b"%3d%%" % i for i in range(100)) * 700
    assert len(bar) > MAX_PARTIAL_LINE_BYTES
    cut = shippable(bar, final=False)
    assert 0 < cut <= len(bar) and bar[cut - 1 : cut] == b"\r"
    words = b"word " * 20_000
    assert words[shippable(words, final=False) - 1 : shippable(words, final=False)] == b" "


def test_an_unterminated_private_key_is_held_back_until_its_end_arrives():
    head = b"step 1\n" + PEM.encode().split(b"-----END")[0]
    assert shippable(head, final=False) == len(b"step 1\n")
    assert shippable(head + b"-----END PRIVATE KEY-----\n", final=False) == len(head) + len(
        b"-----END PRIVATE KEY-----\n"
    )
    # A "block" past the hold is not a key being printed; it ships, and the
    # renderer withholds it (below).
    huge = b"-----BEGIN PRIVATE KEY-----\n" + b"A" * (MAX_PEM_HOLD_BYTES + 10) + b"\n"
    assert shippable(huge, final=False) == len(huge)


def test_redraws_collapse_to_the_frame_the_terminal_showed():
    assert collapse_redraws("epoch 1  10%\repoch 1  55%\repoch 1 100%\nnext\n") == "epoch 1 100%\nnext\n"
    assert collapse_redraws("a\r\nb\n") == "a\nb\n"


def test_a_text_that_ends_inside_a_redraw_keeps_its_carriage_return():
    """A chunk cut at a redraw: the next chunk's first frame must REPLACE this
    one where the chunks are joined (the server collapses redraws on the
    joined text), not be appended to it on the same line."""
    assert collapse_redraws("done\n 10%|#\r 20%|##\r") == "done\n 20%|##\r"
    assert collapse_redraws(" 20%|##\r 30%|###\n") == " 30%|###\n"
    joined = collapse_redraws("done\n 20%|##\r") + collapse_redraws(" 30%|###\n")
    assert collapse_redraws(joined) == "done\n 30%|###\n"
    # Negative control: a redraw INSIDE a line that ended keeps no \r.
    assert collapse_redraws(" 10%\r 20%\nnext") == " 20%\nnext"


def test_a_key_block_that_never_ends_is_withheld_through_its_end_line():
    raw = b"before\n-----BEGIN PRIVATE KEY-----\n" + PEM_BODY[0].encode() + b"\n"
    text, in_pem = render(raw, False)
    assert text == "before\n[probe: a private key block was withheld from the live log]\n" and in_pem
    text, in_pem = render(PEM_BODY[1].encode() + b"\n", True)
    assert (text, in_pem) == ("", True)
    text, in_pem = render(b"-----END PRIVATE KEY-----\nafter\n", True)
    assert (text, in_pem) == ("after\n", False)


# -- a line too long to hold: where it is cut ------------------------------------------
#: Real-shaped tokens for three rules of the gate (`tap_core.secrets._RULES`).
#: The Hugging Face rule is letters only (`hf_[A-Za-z]{34}`).
STRADDLE_TOKENS = {
    "ghp_": "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8",
    "hf_": "hf_" + "AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGh",
    "sk-proj-": "sk-proj-" + "Ab3dEf6hIj9lMn2pQr5tUv8xYz1bCd4fGh7jKl0nOp3rSt6vWx9zAb2dEf5h",
}


def _minified(token: str, *, cut: int, into: int) -> bytes:
    """One line of `json.dumps(..., separators=(",", ":"))` -- no space, tab
    or \\r anywhere -- longer than a chunk, with ``token`` placed so a cut
    at byte ``cut`` falls ``into`` characters inside it (the review's repro,
    `probe_sdk_split2.py`)."""
    item = '{"layer":12,"lr":0.0003},'
    head = '{"hist":[' + item * ((cut - into - 40) // len(item))
    pad = cut - into - len(head) - len('"pad":"') - len('","ref":"')
    head = head + '"pad":"' + "p" * pad + '","ref":"'
    assert len(head) == cut - into
    return (head + token + '","tail":[' + item * 2000 + "]}\n").encode()


def _fragments(token: str) -> list[str]:
    """Pieces of ``token`` long enough to mean something on their own."""
    body = token.split("_", 1)[-1] if "_" in token[:4] else token[len("sk-proj-") :]
    return [body[:8], body[-8:], body[10:18]]


@pytest.mark.parametrize("prefix", sorted(STRADDLE_TOKENS))
@pytest.mark.parametrize("into", [1, 4, 8, 12, 20])
def test_a_token_straddling_a_forced_cut_is_never_stored_in_halves(client, streaming, tmp_path, prefix, into):
    """MED-1 (#2046 review): a line past a chunk with no space, tab or \\r was
    cut at a fixed byte, so a token across the cut went out as two halves the
    gate could not recognise -- and the server's read joins chunks back
    together. The cut now never falls inside a run of token-shaped bytes."""
    token = STRADDLE_TOKENS[prefix]
    if into >= len(token):
        pytest.skip("cut past the token")
    run = open_run(client, experiment=f"live-straddle-{prefix.strip('_-')}-{into}")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(_minified(token, cut=MAX_CHUNK_RAW_BYTES, into=into))
    streamer.ship()
    spool.close()
    streamer.ship(final=True, deadline=__import__("time").monotonic() + 5)
    texts = [p["text"] for p in streaming.log_chunk_posts]
    assert len(texts) >= 2  # the line WAS cut
    joined = "".join(texts)
    assert token not in joined and not any(token in t for t in texts)
    assert not any(piece in joined for piece in _fragments(token))
    assert "<redacted" in joined and joined.endswith("]}\n")


@pytest.mark.parametrize("prefix", sorted(STRADDLE_TOKENS))
def test_a_wake_up_in_the_middle_of_a_long_partial_line_holds_the_token_back(client, streaming, tmp_path, prefix):
    """The same cut at the END of what was read: a partial line past
    ``MAX_PARTIAL_LINE_BYTES`` is shipped while the program is still printing
    a token. The bytes after it are unknown, so the run is held back."""
    token = STRADDLE_TOKENS[prefix]
    run = open_run(client, experiment=f"live-partial-{prefix.strip('_-')}")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    line = _minified(token, cut=80 * 1024, into=6)
    spool.write(line[: 80 * 1024])  # the wake-up lands 6 characters into the token
    streamer.ship()
    spool.write(line[80 * 1024 :])
    streamer.ship()
    texts = [p["text"] for p in streaming.log_chunk_posts]
    assert len(texts) == 2
    assert token not in "".join(texts) and not any(piece in "".join(texts) for piece in _fragments(token))


def test_the_final_pass_cuts_a_long_unterminated_tail_the_same_way(client, streaming, tmp_path):
    """The stream ended with a line longer than a chunk and no newline: the
    last pass cut it at the size limit, byte-exact, the same straddle."""
    token = STRADDLE_TOKENS["ghp_"]
    run = open_run(client, experiment="live-final-straddle")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(_minified(token, cut=MAX_CHUNK_RAW_BYTES, into=10)[:-1])  # no newline at the end
    spool.close()
    streamer.stop(budget=5.0)
    joined = "".join(p["text"] for p in streaming.log_chunk_posts)
    assert len(streaming.log_chunk_posts) >= 2
    assert token not in joined and "<redacted" in joined and joined.endswith("]}")


def test_a_cut_never_falls_inside_a_token_shaped_run():
    run = b"A1b2" * 1000  # 4 KiB of token-shaped bytes
    line = b'{"k":"' * 43_500 + run + b'"}' * 40_000 + b"\n"
    head = len(b'{"k":"' * 43_500)
    cut = plan_cut(line, final=False)
    # The limit lands inside the run: the whole run waits for the next chunk.
    assert head < MAX_CHUNK_RAW_BYTES < head + len(run)
    assert cut.size == head and not cut.at_line_end and cut.withhold_from is None
    # Negative control: a line with a space before the limit is still cut there.
    spaced = b"x" * 1000 + b" " + line[1001:]
    assert plan_cut(spaced, final=False).size == 1001


def test_a_token_run_too_long_to_hold_is_withheld_across_the_cut(client, streaming, tmp_path):
    """A run longer than ``MAX_TOKEN_RUN_BYTES`` (an inline base64 blob) cannot
    be held back whole: it is withheld, once, on both sides of the cut."""
    token = STRADDLE_TOKENS["ghp_"]
    run = open_run(client, experiment="live-long-run")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    blob = ("Zm9v" * ((MAX_TOKEN_RUN_BYTES * 3) // 4)).encode()
    start = MAX_CHUNK_RAW_BYTES - len(blob) // 2
    lead = b'{"x":"' * (start // 6)
    lead += b"q" * (start - len(lead) - 1) + b'"'
    body = blob[: len(blob) // 2 - 30] + token.encode() + blob[len(blob) // 2 - 30 :]
    spool.write(lead + body + b'","after":"visible"}\n')
    streamer.ship()
    spool.close()
    streamer.ship(final=True, deadline=__import__("time").monotonic() + 5)
    texts = [p["text"] for p in streaming.log_chunk_posts]
    joined = "".join(texts)
    assert token not in joined and not any(piece in joined for piece in _fragments(token))
    assert joined.count("long unbroken run of output was withheld") == 1
    assert joined.endswith('","after":"visible"}\n') and joined.startswith('{"x":"')


def test_a_key_name_and_its_value_split_by_a_forced_cut_are_still_redacted(client, streaming, tmp_path):
    """Cut at the last space before the limit: `password = ` ends one chunk and
    the value starts the next, which alone carries nothing the gate knows as
    a key. The next chunk is redacted WITH the text before the cut."""
    secret = "Xk9mQ2vL7pR4tZ8w"
    tail = "password = "
    head = ("w " * (MAX_CHUNK_RAW_BYTES // 2))[: MAX_CHUNK_RAW_BYTES - len(tail) - 1]
    line = head + " " + tail + secret + "; epoch 3 done " + "z" * 100 + "\n"
    assert line.rfind(" ", 0, MAX_CHUNK_RAW_BYTES) == len(head) + len(tail)  # the cut lands there
    run = open_run(client, experiment="live-seam")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(line.encode())
    streamer.ship()
    spool.close()
    streamer.ship(final=True, deadline=__import__("time").monotonic() + 5)
    texts = [p["text"] for p in streaming.log_chunk_posts]
    assert len(texts) == 2 and texts[0].endswith(tail)
    assert secret not in "".join(texts)
    assert texts[1].startswith("<redacted") and texts[1].endswith("; epoch 3 done " + "z" * 100 + "\n")


def test_the_chunk_after_a_cut_is_not_redacted_with_stale_context():
    """Redacting with context returns only this chunk's part: nothing of the
    context comes back when nothing crosses the cut."""
    assert logstream.redact("step 2 done\n", "loss 0.1 epoch ") == "step 2 done\n"
    assert logstream.redact(f"{TOKEN} done\n", "x ") .startswith("<redacted")


# -- the shipper against the API -------------------------------------------------------
def test_complete_lines_ship_and_the_rest_waits_for_its_newline(client, streaming, tmp_path):
    run = open_run(client, experiment="live-lines")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(b"epoch 1 loss 2.3\nepoch 2 lo")
    assert streamer.ship() == 1
    spool.write(b"ss 1.9\n")
    assert streamer.ship() == 1
    posts = streaming.log_chunk_posts
    assert [(p["raw_offset"], p["raw_len"], p["text"]) for p in posts] == [
        (0, 17, "epoch 1 loss 2.3\n"),
        (17, 17, "epoch 2 loss 1.9\n"),
    ]
    assert posts[0]["stream"] == "run"


def test_a_token_split_across_reads_is_redacted_and_never_sent_in_halves(client, streaming, tmp_path):
    run = open_run(client, experiment="live-token")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(f"step 7\nexport GITHUB_TOKEN={TOKEN[:15]}".encode())
    streamer.ship()
    spool.write(f"{TOKEN[15:]}\nstep 8\n".encode())
    streamer.ship()
    sent = "".join(p["text"] for p in streaming.log_chunk_posts)
    assert TOKEN not in sent and TOKEN[4:15] not in sent and TOKEN[15:] not in sent
    assert "step 7\n" in sent and "step 8\n" in sent and "<redacted" in sent


def test_the_shipper_redacts_before_the_transport_sees_the_text(client, streaming, tmp_path, monkeypatch):
    """The chunk is cleaned by the final log's own function (`redact_log_text`),
    not left to the transport's generic scrub -- which does not look inside an
    encoded blob (base64 of gzip) the gate can see a token in."""
    import base64
    import gzip

    handed: list[dict] = []
    real = client.transport.request

    def spy(method, path, **kw):
        if path.endswith("/log-chunks"):
            handed.append(dict(kw["json_body"]))
        return real(method, path, **kw)

    monkeypatch.setattr(client.transport, "request", spy)
    run = open_run(client, experiment="live-redact")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    blob = base64.b64encode(gzip.compress(f"GITHUB_TOKEN={TOKEN}".encode(), mtime=0)).decode()
    spool.write(f"token {TOKEN}\nblob {blob}\nstep 9\n".encode())
    assert streamer.ship() == 1
    (body,) = handed
    assert TOKEN not in body["text"] and blob not in body["text"]
    assert "step 9\n" in body["text"] and "<redacted" in body["text"]


def test_a_pem_block_split_across_reads_is_redacted(client, streaming, tmp_path):
    run = open_run(client, experiment="live-pem")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    half = len(PEM) // 2
    spool.write(b"loading key\n" + PEM[:half].encode())
    streamer.ship()
    spool.write(PEM[half:].encode() + b"done\n")
    streamer.ship()
    sent = "".join(p["text"] for p in streaming.log_chunk_posts)
    assert "loading key\n" in sent and "done\n" in sent
    assert not any(line in sent for line in PEM_BODY)


def test_a_failed_post_is_replayed_with_the_identical_body(client, streaming, tmp_path):
    run = open_run(client, experiment="live-replay")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(b"first\n")
    streaming.log_chunk_failures = 1
    streamer.client.transport.max_retries = 0  # one attempt per pass: the pass is what retries
    assert streamer.ship() == 0
    spool.write(b"second\n")  # arrives while the first is unsent: must not change its body
    streamer._next_try = 0.0  # the backoff has passed
    assert streamer.ship() == 2
    first, replay, second = streaming.log_chunk_posts
    assert first == replay == {"stream": "run", "raw_offset": 0, "raw_len": 6, "text": "first\n"}
    assert second["raw_offset"] == 6 and second["text"] == "second\n"


def test_a_replay_the_server_already_has_moves_the_cursor_where_it_says(client, streaming, tmp_path):
    run = open_run(client, experiment="live-rebase")
    log_path, spool = _spool(tmp_path)
    spool.write(b"a\nb\nc\n")
    # A previous process sent "a\nb\n" and died before recording it.
    streaming.log_chunks[run.id] = {("run", 0): {"stream": "run", "raw_offset": 0, "raw_len": 4, "text": "a\nb\n"}}
    streamer = _streamer(client, run, log_path)
    streamer.ship()
    assert _texts(streaming, run) == "a\nb\nc\n"
    assert streamer.cursor == 6


def test_a_budget_drop_reaches_the_server_as_a_jump_in_offsets(client, streaming, tmp_path):
    run = open_run(client, experiment="live-gap")
    log_path = str(tmp_path / "run.log")
    os.makedirs(live_dir(log_path))
    spool = LiveSpool(live_dir(log_path), segment_bytes=8, budget_bytes=24)
    streamer = _streamer(client, run, log_path)
    spool.write(b"".join(b"line %02d\n" % i for i in range(10)))  # 80 bytes, 10 segments
    assert spool.dropped > 0
    # Right after a gap too little follows to rule out a key block cut in
    # half by it (see the next test): held until more arrives, or the end.
    assert streamer.ship() == 0
    spool.close()
    streamer.ship(final=True)
    offsets = sorted(p["raw_offset"] for p in streaming.log_chunk_posts)
    assert offsets[0] == spool.dropped and offsets[0] > 0  # the gap the server marks
    assert _texts(streaming, run).endswith("line 09\n")


def test_a_gap_that_took_a_keys_begin_line_withholds_the_rest_of_the_key(client, streaming, tmp_path):
    """The spool dropped the segment with `-----BEGIN`: what follows the gap
    is bare key material the gate cannot recognise without it."""
    run = open_run(client, experiment="live-gap-key")
    log_path = str(tmp_path / "run.log")
    os.makedirs(live_dir(log_path))
    spool = LiveSpool(live_dir(log_path), segment_bytes=64, budget_bytes=256)
    streamer = _streamer(client, run, log_path)
    spool.write(b"x" * 63 + b"\n" + PEM.encode() + b"after the key\n")
    assert spool.dropped > 64  # the BEGIN line is gone
    spool.close()
    streamer.ship(final=True)
    sent = "".join(p["text"] for p in streaming.log_chunk_posts)
    assert not any(line[:20] in sent for line in PEM_BODY)
    assert "resumed inside a private key block" in sent and sent.endswith("after the key\n")


def test_one_wake_up_ships_a_bounded_amount_and_a_backlog_skips_to_the_newest(client, streaming, tmp_path):
    """The shipper runs in the TRAINING process: redaction there is CPU the
    job pays. One pass takes PASS_RAW_BYTES; a backlog past MAX_BACKLOG_BYTES
    jumps to the newest output, which is what a live view is for."""
    run = open_run(client, experiment="live-budget")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    line = b"y" * 1023 + b"\n"
    spool.write(line * 512)  # 512 KiB: under the backlog cap
    streamer.ship()
    first = sum(p["raw_len"] for p in streaming.log_chunk_posts)
    assert first == logstream.PASS_RAW_BYTES
    spool.write(line * 2048)  # 2 MiB more: past it
    streamer.ship()
    newest = max(p["raw_offset"] + p["raw_len"] for p in streaming.log_chunk_posts)
    skipped_to = min(p["raw_offset"] for p in streaming.log_chunk_posts[1:])
    assert skipped_to > first  # a jump: the server marks it as a gap
    assert newest == spool.offset  # the pass reached the newest line
    assert newest - skipped_to <= logstream.PASS_RAW_BYTES


def test_one_wake_up_never_ships_past_its_budget(client, streaming, tmp_path):
    """MED-3 (#2046 review): the loop checked the budget only BETWEEN chunks,
    so a pass that had shipped just under it took one more whole chunk --
    up to twice the CPU the docstring promises. No chunk takes it past."""
    run = open_run(client, experiment="live-budget-cap")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    line = b"y" * 999 + b"\n"  # 1000 bytes: 262 lines fall just short of 256 KiB
    spool.write(line * 700)
    streamer.ship()
    first = sum(p["raw_len"] for p in streaming.log_chunk_posts)
    assert 0 < first <= logstream.PASS_RAW_BYTES
    assert first > logstream.PASS_RAW_BYTES - len(line)  # and it used the budget
    streamer.ship()  # the next pass carries on where this one stopped
    assert min(p["raw_offset"] for p in streaming.log_chunk_posts[1:]) == first


def test_sent_segments_are_deleted_and_the_cursor_survives_the_process(client, streaming, tmp_path):
    run = open_run(client, experiment="live-cursor")
    log_path = str(tmp_path / "run.log")
    os.makedirs(live_dir(log_path))
    spool = LiveSpool(live_dir(log_path), segment_bytes=10, budget_bytes=1000)
    streamer = _streamer(client, run, log_path)
    spool.write(b"0123456789abcdefghij\n")  # three segments
    streamer.ship()
    remaining = [start for start, _path, _size in list_segments(live_dir(log_path))]
    assert remaining == [20]  # the open one stays; the two sent before it are gone
    assert LogStreamer(client, run.id, log_path, "run").cursor == 21


def test_a_stale_attempt_stops_and_a_gone_run_stops(client, streaming, tmp_path, monkeypatch):
    run = open_run(client, experiment="live-stop")
    log_path, spool = _spool(tmp_path)
    spool.write(b"x\n")
    streamer = _streamer(client, run, log_path, epoch=lambda: 1)
    from probe.sdk import errors

    # The exceptions the real transport raises for these answers (`error_for`).
    def stale(*a, **k):
        raise errors.error_for(409, {"message": "stale", "code": "stale_write_epoch", "write_epoch": 2})

    monkeypatch.setattr(client.transport, "request", stale)
    assert streamer.ship() == 0 and streamer._disabled
    other = _streamer(client, run, log_path)

    def gone(*a, **k):
        raise errors.error_for(410, "in_trash")

    monkeypatch.setattr(client.transport, "request", gone)
    assert other.ship() == 0 and other._disabled
    # The server keeps a bounded number of streams per attempt (#2012).
    third = _streamer(client, run, log_path)

    def full(*a, **k):
        raise errors.error_for(409, {"message": "too many", "code": "too_many_streams", "max_streams": 64})

    monkeypatch.setattr(client.transport, "request", full)
    assert third.ship() == 0 and third._disabled


def test_a_429_waits_at_least_its_retry_after(client, streaming, tmp_path):
    """The server's per-run rate limit answers 429 with `retry_after`: the
    next try is no sooner than that, not the 2 s the backoff starts at."""
    run = open_run(client, experiment="live-429")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(b"hello\n")
    streamer.client.transport.max_retries = 0
    streaming.log_chunk_throttled, streaming.log_chunk_retry_after = 1, 40
    import time as _time

    assert streamer.ship() == 0
    assert streamer._next_try - _time.monotonic() > 35
    assert streamer.ship() == 0 and len(streaming.log_chunk_posts) == 1  # not before it
    streamer._next_try = 0.0
    assert streamer.ship() == 1
    # Negative control: a plain 503 backs off from the start of the ladder.
    spool.write(b"again\n")
    streaming.log_chunk_failures = 1
    assert streamer.ship() == 0
    assert streamer._next_try - _time.monotonic() < 3


def test_one_post_is_bounded_even_when_the_transport_would_wait_out_retry_after(
    client, streaming, tmp_path, monkeypatch
):
    """#2046 re-review: the transport waits out a Retry-After of up to 10 s
    inside one request, up to 3 retries -- ~40 s of one POST, outside any
    shipper deadline. The whole POST is bounded now; the shipper waits the
    rest out on its own clock."""
    import time as _time

    monkeypatch.setattr(logstream, "POST_TIMEOUT_SECONDS", 1.0)
    run = open_run(client, experiment="live-429-bound")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(b"hello\n")
    streaming.log_chunk_throttled, streaming.log_chunk_retry_after = 10, 3  # under the inline max
    started = _time.monotonic()
    assert streamer.ship() == 0
    assert _time.monotonic() - started < 2.0  # old: 3 inline waits of 3 s
    assert streamer._next_try - _time.monotonic() > 2.0  # and still no sooner than asked


def test_a_recovery_drain_keeps_to_its_budget_under_a_throttling_server(client, streaming, tmp_path):
    import time as _time

    run = open_run(client, experiment="live-429-drain")
    log_path, spool = _spool(tmp_path)
    spool.write(b"the crash\n")
    spool.close()
    streaming.log_chunk_throttled, streaming.log_chunk_retry_after = 10, 3
    started = _time.monotonic()
    assert logstream.drain_spool(client, run.id, log_path, "probe/run.log", budget=1.0) == 0
    assert _time.monotonic() - started < 2.5  # old: ~9 s of inline Retry-After waits
    assert not os.path.exists(live_dir(log_path))


def test_the_final_pass_sends_the_last_line_and_removes_the_spool(client, streaming, tmp_path):
    run = open_run(client, experiment="live-final")
    log_path, spool = _spool(tmp_path)
    streamer = _streamer(client, run, log_path)
    spool.write(b"Traceback (most recent call last):\nRuntimeError: CUDA error: out of memory")
    spool.close()  # the helper ended the stream
    streamer.stop(budget=5.0)
    assert _texts(streaming, run).endswith("RuntimeError: CUDA error: out of memory")
    assert not os.path.exists(live_dir(log_path))


def test_a_killed_attempts_spool_is_never_taken_by_the_next_attempt(client, streaming, tmp_path):
    """MED-2 (#2046 review): attempt 1 is SIGKILLed after its log was queued
    (the local copy discarded) but before its stream stopped. The spool --
    its cursor, its unsent tail -- stays. Attempt 2 used to reserve the same
    log name, reuse the spool (makedirs exist_ok + O_APPEND), ship attempt
    1's tail as its own and start past its own first bytes."""
    run = open_run(client, experiment="live-stale")
    first = outputs.reserve_log_path(run.id)
    assert logstream.prepare(client, first) is True
    spool = LiveSpool(live_dir(first), segment_bytes=64)
    spool.write(b"".join(b"attempt-1 line %02d\n" % i for i in range(12)))
    _streamer(client, run, first).ship()
    spool.write(b"attempt-1 unsent tail\n")
    spool.close()
    os.unlink(first)  # `_discard_local_log` ran; then SIGKILL
    assert os.path.isdir(live_dir(first))
    # Attempt 2 on the same host.
    second = outputs.reserve_log_path(run.id)
    assert second != first and second.endswith(f"{run.id}.2.log")
    assert logstream.prepare(client, second) is True
    fresh = LiveSpool(live_dir(second))
    fresh.write(b"attempt-2 hello\n")
    fresh.close()
    streaming.log_chunk_posts.clear()
    streamer = _streamer(client, run, second)
    assert streamer.cursor == 0
    streamer.stop(budget=5.0)
    assert [p["text"] for p in streaming.log_chunk_posts] == ["attempt-2 hello\n"]
    # The dead attempt's spool is left for its recovery, untouched.
    assert sorted(os.listdir(live_dir(first)))[0] == "cursor"


def test_a_spool_that_already_exists_is_never_reused():
    """`prepare` never adopts a directory it did not create."""
    import tempfile

    with tempfile.TemporaryDirectory() as folder:
        log_path = os.path.join(folder, "run.log")
        os.makedirs(live_dir(log_path))
        with open(os.path.join(live_dir(log_path), "cursor"), "w") as fh:
            fh.write("216")

        class _Server:
            def supports_feature(self, name):
                return True

        assert logstream.prepare(_Server(), log_path) is False
        assert os.listdir(live_dir(log_path)) == ["cursor"]
        # Negative control: a fresh path is created and taken.
        assert logstream.prepare(_Server(), os.path.join(folder, "other.log")) is True


def test_a_recovery_resumes_a_dead_processes_spool_from_its_cursor(client, streaming, tmp_path):
    run = open_run(client, experiment="live-recover")
    log_path, spool = _spool(tmp_path)
    spool.write(b"sent before the crash\n")
    _streamer(client, run, log_path).ship()
    spool.write(b"Segmentation fault (core dumped)\n")
    spool.close()
    assert logstream.drain_spool(client, run.id, log_path, "probe/run.log", budget=5.0) == 1
    posts = streaming.log_chunk_posts
    assert [p["raw_offset"] for p in posts] == [0, 22]
    assert posts[1]["text"] == "Segmentation fault (core dumped)\n"
    assert not os.path.exists(live_dir(log_path))


def test_a_recovery_sends_as_the_dead_attempt_and_stops_once_the_run_moved_on(client, streaming, tmp_path):
    """The recovery's chunks carry the epoch the dead process recorded. Once
    a newer attempt took the run over, the server refuses them (409) and
    nothing of the dead attempt lands in the new attempt's log. Before, they
    carried none, and the server filed them under the current attempt."""
    run = open_run(client, experiment="live-recover-epoch")
    log_path, spool = _spool(tmp_path)
    spool.write(b"attempt 1 died here\n")
    spool.close()
    streaming.runs[run.id]["write_epoch"] = 2  # attempt 2 reopened the run
    assert logstream.drain_spool(client, run.id, log_path, "probe/run.log", budget=5.0, write_epoch=1) == 0
    assert [p.get("write_epoch") for p in streaming.log_chunk_posts] == [1]
    assert streaming.log_chunks.get(run.id, {}) == {}
    assert not os.path.exists(live_dir(log_path))
    # Negative control: the run's own attempt is stored.
    log_path, spool = _spool(tmp_path / "again")
    spool.write(b"attempt 2 died here\n")
    spool.close()
    assert logstream.drain_spool(client, run.id, log_path, "probe/run.log", budget=5.0, write_epoch=2) == 1
    assert _texts(streaming, run) == "attempt 2 died here\n"


# -- who streams -----------------------------------------------------------------------
def test_rank_three_is_silent_by_default_and_all_streams_it(client, streaming, tmp_path, monkeypatch):
    monkeypatch.setenv("WORLD_SIZE", "4")
    monkeypatch.setenv("RANK", "3")
    log_path = str(tmp_path / "run.log")
    assert logstream.mode() is Mode.RANK0
    assert logstream.prepare(client, log_path) is False
    assert not os.path.exists(live_dir(log_path))
    assert not any(r.url.path == "/v1/server/features" for r in streaming.requests)
    monkeypatch.setenv(logstream.MODE_ENV, "all")
    assert logstream.prepare(client, log_path) is True
    monkeypatch.setenv(logstream.MODE_ENV, "0")
    monkeypatch.setenv("RANK", "0")
    assert logstream.wanted_here() is False


def test_an_old_server_gets_no_spool_and_no_requests(client, app, tmp_path):
    assert app.supports_run_log_stream is False
    log_path = str(tmp_path / "run.log")
    assert logstream.prepare(client, log_path) is False
    assert not os.path.exists(live_dir(log_path))
    assert _chunk_requests(app) == []


def test_the_stream_is_named_after_the_log():
    assert logstream.stream_for("probe/run.log") == "run"
    assert logstream.stream_for("probe/run.rank3.log") == "run.rank3"
    assert logstream.stream_for("probe/run.4242.log") == "run.4242"


def test_every_rank_streams_under_its_own_name_in_all_mode(monkeypatch):
    """`mpirun` sets OMPI_COMM_WORLD_RANK, not RANK/WORLD_SIZE: every host's
    log is `probe/run.log`, and in `all` mode every host streamed as `run`,
    each covering the others' offsets. The rank is in the name now."""
    monkeypatch.setenv("OMPI_COMM_WORLD_RANK", "3")
    monkeypatch.setenv(logstream.MODE_ENV, "all")
    assert logstream.stream_for("probe/run.log") == "run.rank3"
    assert logstream.stream_for("probe/run.4242.log") == "run.rank3"
    assert logstream.stream_for("probe/run.rank3.log") == "run.rank3"
    # Negative controls: the default mode (rank 0 only) and no rank at all.
    monkeypatch.setenv(logstream.MODE_ENV, "rank0")
    assert logstream.stream_for("probe/run.log") == "run"
    monkeypatch.setenv(logstream.MODE_ENV, "all")
    monkeypatch.delenv("OMPI_COMM_WORLD_RANK")
    assert logstream.stream_for("probe/run.log") == "run"


def test_the_interval_has_a_floor(monkeypatch):
    monkeypatch.setenv(logstream.INTERVAL_ENV, "0.01")
    assert logstream.interval_seconds() == logstream.MIN_INTERVAL_SECONDS
    monkeypatch.setenv(logstream.INTERVAL_ENV, "30")
    assert logstream.interval_seconds() == 30.0
    monkeypatch.setenv(logstream.INTERVAL_ENV, "0")
    assert logstream.interval_seconds() == logstream.DEFAULT_INTERVAL_SECONDS


def test_the_feature_answer_is_kept_for_the_process_failures_and_timeouts_too():
    """Opening a run asked the server every time, and a server that failed
    (or took the whole 2 s) cost every `probe.init()` in the process again."""
    import threading
    import time as _time

    class _Failing:
        calls = 0
        settings = type("S", (), {"base_url": "http://failing"})()

        def supports_feature(self, name):
            _Failing.calls += 1
            raise RuntimeError("down")

    assert logstream.server_accepts(_Failing()) is False
    assert logstream.server_accepts(_Failing()) is False
    assert _Failing.calls == 1

    release = threading.Event()

    class _Slow:
        calls = 0
        settings = type("S", (), {"base_url": "http://slow"})()

        def supports_feature(self, name):
            _Slow.calls += 1
            release.wait(5)
            return True

    started = _time.monotonic()
    assert logstream.server_accepts(_Slow(), timeout=0.2) is False
    again = _time.monotonic()
    assert logstream.server_accepts(_Slow(), timeout=0.2) is False  # no second wait
    assert _time.monotonic() - again < 0.1 and again - started >= 0.2
    release.set()
    deadline = _time.monotonic() + 5
    while logstream.server_accepts(_Slow()) is False and _time.monotonic() < deadline:
        _time.sleep(0.01)
    assert logstream.server_accepts(_Slow()) is True and _Slow.calls == 1  # the late answer, kept


def test_the_shipper_calls_the_transport_with_its_real_signature():
    """The shipper's one network call, checked against production's."""
    params = inspect.signature(Transport.request).parameters
    assert {"json_body", "idempotent", "timeout"} <= set(params)
    source = inspect.getsource(LogStreamer._send)
    assert "self.client.transport.request(" in source


# -- end to end: probe exec's helper writes the spool, the launcher ships it -----------
@pytest.fixture
def work(monkeypatch, tmp_path):
    folder = tmp_path / "work"
    folder.mkdir()
    monkeypatch.chdir(folder)
    monkeypatch.setattr(outputs, "_shared_warned", set())
    monkeypatch.setenv(logstream.INTERVAL_ENV, "1")
    return folder


def _exec(run, work, body: str):
    script = work / "job.py"
    script.write_text(body)
    return run.execute([sys.executable, str(script)], cwd=str(work), capture_outputs=True)


def test_the_close_gives_the_stream_a_slice_not_the_whole_deadline(monkeypatch):
    """The last-lines flush ran before the outputs sweep and could take all
    that was left of a short `PROBE_FINISH_TIMEOUT_SEC`."""
    import time as _time

    budgets: list[float] = []

    class _Streamer:
        def stop(self, budget):
            budgets.append(budget)

    capture = outputs.OutputCapture.__new__(outputs.OutputCapture)
    capture._live, capture._log_path = False, None
    capture._streamer = _Streamer()
    capture._stop_stream(_time.monotonic() + 8.0)
    capture._streamer = _Streamer()
    capture._stop_stream(_time.monotonic() + 600.0)
    assert 1.9 < budgets[0] <= 8.0 * logstream.FINAL_FLUSH_SHARE
    assert budgets[1] == logstream.FINAL_FLUSH_SECONDS


def test_execute_streams_the_childs_output_and_still_uploads_the_final_log(client, streaming, work):
    run = open_run(client, experiment="live-exec", capture_outputs=False)
    with pytest.warns(UserWarning, match="replaced credentials in probe/run.log"):
        result = _exec(
            run,
            work,
            "import time\n"
            "for i in range(5):\n"
            "    print(f'epoch {i} loss {1.0 / (i + 1):.3f}', flush=True)\n"
            "    time.sleep(0.1)\n"
            f"print('token {TOKEN}', flush=True)\n"
            "print('no newline at the end', end='', flush=True)\n",
        )
    assert result.returncode == 0
    text = _texts(streaming, run)
    assert "epoch 0 loss 1.000\n" in text and "epoch 4 loss 0.200\n" in text
    assert text.endswith("no newline at the end")
    assert TOKEN not in text and "<redacted" in text
    # The launcher's chunks name the attempt it opened (the server refuses
    # them once a newer one takes the run over).
    assert run.write_epoch and {p.get("write_epoch") for p in streaming.log_chunk_posts} == {run.write_epoch}
    # The final artifact is unchanged by the live stream.
    names = [a["name"] for a in streaming.artifacts.get(run.id, [])]
    assert "probe/run.log" in names
    # The spool is gone once the close sent the last lines.
    assert not any(p.endswith(".live") for p in os.listdir(outputs._private_dir("logs")))


def test_execute_against_an_old_server_streams_nothing(client, app, work):
    run = open_run(client, experiment="live-old", capture_outputs=False)
    assert _exec(run, work, "print('hello', flush=True)\n").returncode == 0
    assert _chunk_requests(app) == []
    assert not any(p.endswith(".live") for p in os.listdir(outputs._private_dir("logs")))
    assert "probe/run.log" in [a["name"] for a in app.artifacts.get(run.id, [])]


def test_execute_as_rank_three_streams_nothing(client, streaming, work, monkeypatch):
    monkeypatch.setenv("WORLD_SIZE", "4")
    monkeypatch.setenv("RANK", "3")
    run = open_run(client, experiment="live-rank3", capture_outputs=False)
    assert _exec(run, work, "print('rank three', flush=True)\n").returncode == 0
    assert _chunk_requests(streaming) == []


def test_in_process_capture_asks_for_the_stream_before_the_helper_starts(client, streaming, work, monkeypatch):
    """The helper turns live mode on only if the spool exists AS IT STARTS."""
    seen: list[bool] = []

    class _Tee:
        def __init__(self, log_path, **kw):
            self.log_path = log_path
            self.helper_pid = None

        def start(self):
            seen.append(os.path.isdir(live_dir(self.log_path)))

        def stop(self):
            return None

    monkeypatch.setattr("probe.sdk.logcapture.InProcessTee", _Tee)
    monkeypatch.setattr(outputs, "in_process_log_supported", lambda: True)
    monkeypatch.delenv("PROBE_CAPTURE_LOG", raising=False)
    # No helper here ever writes `eof`: keep the close's wait for it short.
    monkeypatch.setenv("PROBE_CAPTURE_BUDGET_SEC", "1")
    run = open_run(client, experiment="live-inproc", capture_outputs=True)
    capture = run._capture
    assert seen == [True]
    assert capture._streamer is not None
    # What a recovery needs to send the rest as this attempt's.
    import json as _json

    record = _json.loads(capture._entry.read_text())
    assert record["log_stream"] == "run" and record["write_epoch"] == run.write_epoch == 1
    run.finish()
    assert not os.path.isdir(live_dir(capture._log_path))
