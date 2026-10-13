"""Pasted images: the researcher's own pastes upload beside the batch, never in it.

The contract is prbe-knowledge #646 (engine: `accepts.media`, the media door,
fragment version 2) and research-os #2647 (the gateway's
`POST /ingest/v1/sessions/{source}/{session_id}/media`). Plan:
`~/plans/daemon-upload-5gb/PLAN.md` D7, D9, D16, D21, D24, D25.

  * Only an image the researcher pasted into their own prompt (each harness's
    `pasted_images`), never one a tool showed the agent (D7, D24).
  * Only when the server says `accepts.media`, the machine has not turned it
    off (`pasted_images`), the type is jpeg/png/gif/webp and the bytes agree
    (D9), and the journal's spool has room. Otherwise the placeholder is
    exactly what it was.
  * The bytes never enter an event, fragment or batch: the placeholder gains
    `sha256`, a version-2 fragment an image part, and the bytes wait in the
    journal's `media` table until `deliver` has uploaded them.
  * A line over MAX_SOURCE_LINE is skipped with an `oversize_line` event (D16).

`MediaDoor` answers as the gateway and the engine's store do, with the same
method signatures as the real `Wire` (checked below), so a fake that drifts
from production fails here first.
"""

from __future__ import annotations

import base64
import hashlib
import inspect
import json
import sqlite3
import uuid
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from probe.tap_core import atif_fragment, codex_sanitize, kimi_sanitize, pi_sanitize, sanitize
from probe.tap_core import session_journal as sj
from probe.tap_core.session_journal import DeliveryPending, Journal, SessionDeleted
from test_transcript_protocol3 import CUSTOMER, CWD, DoorWire, _write

_AGENT = Path(__file__).resolve().parent.parent
SCHEMA = Draft202012Validator(
    json.loads((_AGENT / "src" / "probe" / "tap_core" / "probe-events-1.schema.json").read_text())
)

PNG = b"\x89PNG\r\n\x1a\n" + hashlib.sha256(b"synthetic png").digest() * 40
JPEG = b"\xff\xd8\xff\xe0" + hashlib.sha256(b"synthetic jpeg").digest() * 40
GIF = b"GIF89a" + hashlib.sha256(b"synthetic gif").digest() * 8
WEBP = b"RIFF\x24\x00\x00\x00WEBPVP8 " + hashlib.sha256(b"synthetic webp").digest() * 8
VIEWED = b"\x89PNG\r\n\x1a\n" + hashlib.sha256(b"a screenshot the agent took").digest() * 40


def b64(data: bytes) -> str:
    return base64.b64encode(data).decode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# -- one pasted and one agent-viewed image per harness, in the shapes each writes ------


def cc_pasted(data: bytes = PNG, media: str = "image/png", text: str = "why is the loss flat here?") -> dict:
    """Claude Code: a paste is a top-level `image` block in the user's message."""
    return {
        "type": "user", "uuid": str(uuid.uuid4()), "parentUuid": None, "isSidechain": False,
        "timestamp": "2026-10-12T09:00:00.000Z", "cwd": CWD, "sessionId": "s",
        "message": {"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64(data)}},
            {"type": "text", "text": text},
        ]},
    }


def cc_viewed() -> dict:
    """Claude Code 2.1.283: a `Read` of a PNG (keys as a real line, data invented)."""
    return {
        "type": "user", "uuid": str(uuid.uuid4()), "isSidechain": False,
        "timestamp": "2026-10-12T09:00:05.000Z", "cwd": CWD, "sessionId": "s",
        "message": {"role": "user", "content": [{
            "tool_use_id": "toolu_synthetic", "type": "tool_result",
            "content": [{"type": "image", "source": {"type": "base64", "data": b64(VIEWED), "media_type": "image/png"}}],
        }]},
        "toolUseResult": {"type": "image", "file": {"base64": b64(VIEWED), "type": "image/png"}},
    }


def codex_pasted(*images: tuple[bytes, str]) -> dict:
    """Codex 0.160: the attachment manifest, then one `input_image` per file."""
    images = images or ((PNG, "image/png"),)
    manifest = "\n# Files mentioned by the user:\n\n" + "".join(
        f"## Screenshot {i}.png: /home/researcher/.codex/attachments/{i}/Screenshot {i}.png\n"
        "Image attachment: true\n\n"
        for i in range(len(images))
    ) + "## My request:\nthe legend overlaps the plot\n"
    return {
        "timestamp": "2026-10-12T09:00:00.000Z", "type": "response_item",
        "payload": {"type": "message", "role": "user", "content": [
            {"type": "input_text", "text": manifest},
            *({"type": "input_image", "image_url": f"data:{media};base64,{b64(data)}", "detail": "high"}
              for data, media in images),
        ]},
    }


def codex_viewed() -> dict:
    """Codex 0.160: `view_image` returns the image in its function output."""
    return {
        "timestamp": "2026-10-12T09:00:05.000Z", "type": "response_item",
        "payload": {"type": "function_call_output", "call_id": "call_synthetic", "output": [
            {"type": "input_text", "text": "Script completed\nOutput:\n"},
            {"type": "input_image", "image_url": f"data:image/png;base64,{b64(VIEWED)}", "detail": "high"},
        ]},
    }


def codex_viewed_legacy() -> dict:
    """Codex before #12553 (2026-02): `view_image` injected a user message of
    its own holding only the image. No manifest, so never read as a paste."""
    return {
        "timestamp": "2026-10-12T09:00:05.000Z", "type": "response_item",
        "payload": {"type": "message", "role": "user", "content": [
            {"type": "input_image", "image_url": f"data:image/png;base64,{b64(VIEWED)}"},
        ]},
    }


def kimi_pasted(data: bytes = PNG, media: str = "image/png") -> dict:
    return {
        "type": "context.append_message", "time": 1791800000000,
        "message": {"role": "user", "id": "m-1", "origin": {"kind": "user"}, "content": [
            {"type": "text", "text": "what does this chart say?"},
            {"type": "image_url", "imageUrl": {"url": f"data:{media};base64,{b64(data)}"}},
        ]},
    }


def kimi_viewed() -> dict:
    return {
        "type": "context.append_loop_event", "time": 1791800005000,
        "event": {"type": "tool.result", "toolCallId": "t-1", "turnId": 1, "step": 2, "result": {"output": [
            {"type": "image_url", "imageUrl": {"url": f"data:image/png;base64,{b64(VIEWED)}"}},
        ]}},
    }


def pi_pasted(data: bytes = PNG, media: str = "image/png") -> dict:
    return {
        "type": "message", "id": "e-1", "parentId": None, "timestamp": "2026-10-12T09:00:00.000Z",
        "message": {"role": "user", "content": [
            {"type": "text", "text": "compare these runs"},
            {"type": "image", "data": b64(data), "mimeType": media},
        ], "timestamp": 1791800000000},
    }


def pi_viewed() -> dict:
    return {
        "type": "message", "id": "e-2", "parentId": "e-1", "timestamp": "2026-10-12T09:00:05.000Z",
        "message": {"role": "toolResult", "toolCallId": "c-1", "toolName": "read", "content": [
            {"type": "image", "data": b64(VIEWED), "mimeType": "image/png"},
        ], "isError": False, "timestamp": 1791800005000},
    }


HARNESS = {
    "claude_code": (sanitize, cc_pasted, cc_viewed),
    "codex": (codex_sanitize, codex_pasted, codex_viewed),
    "kimi_code": (kimi_sanitize, kimi_pasted, kimi_viewed),
    "pi": (pi_sanitize, pi_pasted, pi_viewed),
}


def _text_line(harness: str, text: str) -> dict:
    """An ordinary prompt in each harness's shape (the turn after the image)."""
    if harness == "claude_code":
        return {"type": "user", "uuid": str(uuid.uuid4()), "timestamp": "2026-10-12T09:01:00.000Z",
                "message": {"role": "user", "content": text}}
    if harness == "codex":
        return {"timestamp": "2026-10-12T09:01:00.000Z", "type": "response_item",
                "payload": {"type": "message", "role": "user", "content": [{"type": "input_text", "text": text}]}}
    if harness == "kimi_code":
        return {"type": "context.append_message", "time": 1791800060000,
                "message": {"role": "user", "origin": {"kind": "user"}, "content": [{"type": "text", "text": text}]}}
    return {"type": "message", "id": "e-9", "timestamp": "2026-10-12T09:01:00.000Z",
            "message": {"role": "user", "content": [{"type": "text", "text": text}]}}


# -- the fake door, with the real Wire's shape ---------------------------------------------


class MediaDoor(DoorWire):
    """DoorWire (the engine's batch door behind the gateway) plus the gateway's
    media door and the store a presigned PUT reaches.

    The store refuses what R2/MinIO refuse: a body whose length, type or
    SHA-256 differs from the signed headers (400). `log` keeps the order of
    every call, so 'uploaded before the batch' is checked, not assumed."""

    last_request_retryable = False

    def __init__(self, source="claude_code", *, media=True, versions=(1, 2), **kw):
        kw.setdefault("offers", True)
        super().__init__(source, versions=versions, **kw)
        self.media_on = media
        self.stored: dict[tuple[str, str], bytes] = {}
        self.media_calls: list[tuple[str, str, int, str]] = []
        self.puts: list[tuple[str, dict, bytes]] = []
        self.log: list[str] = []
        #: Force the media door's answer: (status, body).
        self.answer: tuple[int, dict] | None = None
        #: Force the store's answer to a PUT.
        self.put_status: int | None = None

    def receipts(self, sid, *, after=-1, limit=None):
        result = super().receipts(sid, after=after, limit=limit)
        if self.media_on and isinstance(result.get("accepts"), dict):
            result["accepts"]["media"] = True
        return result

    def post(self, encoded: bytes):
        self.log.append("post")
        return super().post(encoded)

    def media(self, session_id: str, sha256: str, size_bytes: int, media_type: str) -> tuple[int, dict]:
        self.log.append("media")
        self.media_calls.append((session_id, sha256, size_bytes, media_type))
        if self.answer is not None:
            return self.answer
        if (session_id, sha256) in self.stored:
            return 200, {"status": "have"}
        return 200, {
            "status": "upload", "method": "PUT",
            "url": f"https://storage.invalid/raw/{self.source}/{CUSTOMER}/media-staging/{session_id}/{sha256}",
            "headers": {
                "Content-Length": str(size_bytes),
                "Content-Type": media_type,
                "x-amz-checksum-sha256": base64.b64encode(bytes.fromhex(sha256)).decode(),
            },
            "expires_at": "2026-10-12T09:15:00Z",
        }

    def put(self, url: str, data: bytes, headers: dict[str, str]) -> int:
        self.log.append("put")
        self.puts.append((url, dict(headers), data))
        if self.put_status is not None:
            return self.put_status
        if (
            headers.get("Content-Length") != str(len(data))
            or headers.get("x-amz-checksum-sha256") != base64.b64encode(hashlib.sha256(data).digest()).decode()
        ):
            return 400
        session_id, sha256 = url.rsplit("/", 2)[-2:]
        self.stored[(session_id, sha256)] = data
        return 200


_REAL_RESOLVE = sj._resolve_host

#: What the stub resolver answers (tests never depend on real DNS). The fake
#: door's storage host is a public address, as a real bucket endpoint is.
ADDRESSES = {
    "storage.invalid": ["93.184.216.34"],
    "bucket.example": ["93.184.216.34", "2606:2800:220:1::1"],
    "internal.example": ["10.0.0.5", "fd00::5"],
    "half-internal.example": ["10.0.0.5", "93.184.216.34"],
    "metadata.example": ["169.254.169.254"],
}


@pytest.fixture(autouse=True)
def _stub_resolver(monkeypatch):
    def resolve(host):
        if host not in ADDRESSES:
            raise sj.Unresolved("synthetic: not in the stub")
        return ADDRESSES[host]

    monkeypatch.setattr(sj, "_resolve_host", resolve)


def test_the_fake_door_has_the_real_wires_signatures():
    for name in ("media", "put"):
        real = inspect.signature(getattr(sj.Wire, name))
        fake = inspect.signature(getattr(MediaDoor, name))
        assert list(fake.parameters) == list(real.parameters), name


# -- helpers -------------------------------------------------------------------------------


def _session(tmp_path: Path, lines: list[dict]) -> tuple[str, Path]:
    sid = str(uuid.uuid4())
    path = tmp_path / f"{sid}.jsonl"
    path.write_bytes(b"")
    _write(path, lines)
    return sid, path


def _journal(tmp_path: Path, wire, name="state") -> Journal:
    return Journal(wire.base_url, CUSTOMER, wire.source, directory=tmp_path / name)


def _start(journal, wire, sid, path):
    return journal.ensure(sid, path, wire.receipts(sid), historical=False, cwd=CWD)


def _drain(journal, wire, sid, **stage) -> list[bytes]:
    stage.setdefault("pasted_images", True)
    sent = []
    while (body := journal.stage(sid, cwd=CWD, **stage)) is not None:
        journal.deliver(sid, wire)
        sent.append(body)
    return sent


def _spool(journal) -> list[tuple]:
    with sqlite3.connect(journal.db_path) as conn:
        return conn.execute("SELECT session_id, sha256, media_type, size FROM media").fetchall()


def _placeholders(body: dict) -> list[dict]:
    return [
        block
        for item in body.get("events") or ()
        for block in (item["raw"].get("message") or {}).get("content") or ()
        if isinstance(block, dict) and block.get("type") == "image"
    ]


def _image_parts(body: dict) -> list[dict]:
    return [p for f in body.get("fragments") or () for p in f.get("parts") or () if p.get("type") == "image"]


# -- per harness: the paste uploads, the agent's view does not (D7, D24) ---------------------


@pytest.mark.parametrize("harness", sorted(HARNESS))
def test_each_harness_reads_the_pasted_image_and_never_the_viewed_one(harness):
    module, pasted, viewed = HARNESS[harness]
    (image,) = module.pasted_images(pasted())
    assert image.media_type == "image/png" and base64.b64decode(image.data) == PNG
    sanitized = module.sanitize_event(pasted())
    (placeholder,) = sj._image_placeholders(sanitized if isinstance(sanitized, list) else [sanitized])
    assert placeholder["bytes"] == image.encoded and placeholder["mimeType"] == image.media_type
    assert module.pasted_images(viewed()) == []


@pytest.mark.parametrize("harness", sorted(HARNESS))
def test_a_pasted_image_uploads_and_the_batch_names_it_by_digest(tmp_path, harness):
    _module, pasted, viewed = HARNESS[harness]
    wire = MediaDoor(harness, events=True)
    sid, path = _session(tmp_path, [pasted(), viewed(), _text_line(harness, "and after the image")])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    (encoded,) = _drain(journal, wire, sid)
    body = json.loads(encoded)
    assert body["protocol_version"] == 3 and body["fragment_version"] == 2
    named = [b for b in _placeholders(body) if "sha256" in b]
    assert [b["sha256"] for b in named] == [digest(PNG)]
    assert all("sha256" not in b for b in _placeholders(body) if b is not named[0])
    (part,) = _image_parts(body)
    (event,) = [
        e["raw"] for e in body["events"]
        if isinstance(content := (e["raw"].get("message") or {}).get("content"), list) and named[0] in content
    ]
    seq = event["message"]["content"].index(named[0])
    assert part == {"type": "image", "seq": seq, "media_type": "image/png", "sha256": digest(PNG)}
    # The bytes never travel in the batch, in any encoding.
    assert b64(PNG)[:64].encode() not in encoded and b64(VIEWED)[:64].encode() not in encoded
    # One image, one upload, before the batch; the agent's view never asked.
    assert wire.media_calls == [(sid, digest(PNG), len(PNG), "image/png")]
    assert wire.stored == {(sid, digest(PNG)): PNG}
    assert wire.log == ["media", "put", "post"]
    assert "Authorization" not in wire.puts[0][1]
    assert _spool(journal) == []  # uploaded, so nothing waits
    assert sanitize_text_turn_follows(body, "and after the image")
    for item in body["events"]:
        assert not list(SCHEMA.iter_errors(item["raw"])), item["raw"]
    journal.close()


def sanitize_text_turn_follows(body: dict, text: str) -> bool:
    return text in json.dumps(body["events"][-1])


def test_codex_keeps_the_placeholder_where_a_paste_cannot_be_told_from_a_view(tmp_path):
    """A user message holding an image without Codex's attachment manifest is
    what `view_image` wrote before #12553: never uploaded, from the line alone."""
    assert codex_sanitize.pasted_images(codex_viewed_legacy()) == []
    wire = MediaDoor("codex", events=True)
    sid, path = _session(tmp_path, [codex_viewed_legacy()])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    (encoded,) = _drain(journal, wire, sid)
    (block,) = _placeholders(json.loads(encoded))
    assert block == {"type": "image", "mimeType": "image/png", "bytes": len(f"data:image/png;base64,{b64(VIEWED)}")}
    assert wire.media_calls == [] and _image_parts(json.loads(encoded)) == []
    journal.close()


def test_claude_code_never_reads_a_turn_it_wrote_in_the_users_place():
    for marker in ({"isMeta": True}, {"isCompactSummary": True}, {"isSidechain": True}, {"toolUseResult": {}}):
        assert sanitize.pasted_images(cc_pasted() | marker) == []


def test_kimi_reads_only_the_researchers_prompt():
    injected = kimi_pasted()
    injected["message"]["origin"] = {"kind": "injection"}
    assert kimi_sanitize.pasted_images(injected) == []
    blobbed = kimi_pasted()
    blobbed["message"]["content"][1]["imageUrl"]["url"] = "blobref:agents/main/blobs/1"
    assert kimi_sanitize.pasted_images(blobbed) == []


def test_pi_never_reads_an_extensions_message():
    custom = {"type": "custom_message", "customType": "x", "content": pi_pasted()["message"]["content"]}
    assert pi_sanitize.pasted_images(custom) == []


def test_codex_reads_every_attached_image_in_order():
    images = codex_sanitize.pasted_images(codex_pasted((PNG, "image/png"), (JPEG, "image/jpeg")))
    assert [(i.media_type, base64.b64decode(i.data)) for i in images] == [("image/png", PNG), ("image/jpeg", JPEG)]


# -- the gates: anything short of all of them is the placeholder, exactly as before ------------


def _before(harness: str, line: dict) -> list[dict]:
    module = HARNESS[harness][0]
    out = module.sanitize_event(line)
    return out if isinstance(out, list) else [out]


@pytest.mark.parametrize(
    "door,stage",
    [
        pytest.param({"media": True}, {"pasted_images": False}, id="toggle-off"),
        pytest.param({"media": False}, {"pasted_images": True}, id="accepts-media-absent"),
        pytest.param({"media": True, "versions": (1,)}, {"pasted_images": True}, id="door-takes-v1-only"),
    ],
)
def test_without_every_gate_the_placeholder_is_exactly_what_it_was(tmp_path, door, stage):
    wire = MediaDoor("claude_code", events=True, **door)
    line = cc_pasted()
    sid, path = _session(tmp_path, [line])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    (encoded,) = _drain(journal, wire, sid, **stage)
    body = json.loads(encoded)
    before = [{"line_no": 0, "raw": raw} for raw in _before("claude_code", line)]
    assert body["events"] == sj._scrub_content({"events": before})["events"]
    assert body["events"][0]["raw"]["message"]["content"][0] == {
        "type": "image", "mimeType": "image/png", "bytes": len(b64(PNG)),
    }
    assert _image_parts(body) == [] and wire.media_calls == [] and _spool(journal) == []
    assert body["fragment_version"] == max(door.get("versions", (1, 2)))
    journal.close()


def test_protocol_2_carries_the_digest_on_its_events(tmp_path):
    """Protocol 2 sends events only: the media block names the image."""
    wire = MediaDoor("pi", offers=False)
    sid, path = _session(tmp_path, [pi_pasted()])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    (encoded,) = _drain(journal, wire, sid)
    body = json.loads(encoded)
    assert body["protocol_version"] == 2 and "fragments" not in body
    assert [b.get("sha256") for b in _placeholders(body)] == [digest(PNG)]
    assert wire.stored == {(sid, digest(PNG)): PNG}
    journal.close()


@pytest.mark.parametrize(
    "data,media",
    [
        pytest.param(JPEG, "image/png", id="png-declared-jpeg-bytes"),
        pytest.param(b"<svg xmlns='http://www.w3.org/2000/svg'/>", "image/svg+xml", id="svg"),
        pytest.param(b"%PDF-1.7 synthetic", "image/png", id="pdf-bytes"),
    ],
)
def test_a_type_the_engine_does_not_store_or_bytes_that_disagree_keep_the_placeholder(tmp_path, data, media):
    wire = MediaDoor("claude_code", events=True)
    sid, path = _session(tmp_path, [cc_pasted(data, media)])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    (encoded,) = _drain(journal, wire, sid)
    assert [b.get("sha256") for b in _placeholders(json.loads(encoded))] == [None]
    assert wire.media_calls == [] and _spool(journal) == []
    journal.close()


@pytest.mark.parametrize("data,media", [(JPEG, "image/jpeg"), (GIF, "image/gif"), (WEBP, "image/webp")])
def test_every_type_the_engine_stores_uploads(tmp_path, data, media):
    wire = MediaDoor("kimi_code", events=True)
    sid, path = _session(tmp_path, [kimi_pasted(data, media)])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    assert wire.stored == {(sid, digest(data)): data}
    journal.close()


def test_base64_that_does_not_decode_keeps_the_placeholder(tmp_path):
    line = cc_pasted()
    line["message"]["content"][0]["source"]["data"] = "iVBORw0K!!not base64"
    wire = MediaDoor("claude_code", events=True)
    sid, path = _session(tmp_path, [line])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    assert wire.media_calls == []
    journal.close()


def test_images_and_placeholders_that_do_not_pair_up_attach_nothing(tmp_path, monkeypatch):
    """Two images read from the line for one placeholder: no digest may land
    on another image's placeholder, so none lands at all."""
    real = sanitize.pasted_images
    monkeypatch.setattr(sanitize, "pasted_images", lambda line: real(line) * 2)
    wire = MediaDoor("claude_code", events=True)
    sid, path = _session(tmp_path, [cc_pasted()])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    assert wire.media_calls == []
    journal.close()


def test_the_spool_cap_keeps_the_placeholder_for_what_does_not_fit(tmp_path, monkeypatch):
    monkeypatch.setattr(sj, "MEDIA_SPOOL_CAP_BYTES", len(PNG) + len(JPEG) // 2)
    wire = MediaDoor("codex", events=True)
    sid, path = _session(tmp_path, [codex_pasted((PNG, "image/png"), (PNG, "image/png"), (JPEG, "image/jpeg"))])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    encoded = journal.stage(sid, cwd=CWD, pasted_images=True)
    # The same image twice costs once; the third does not fit.
    assert [b.get("sha256") for b in _placeholders(json.loads(encoded))] == [digest(PNG), digest(PNG), None]
    assert _spool(journal) == [(sid, digest(PNG), "image/png", len(PNG))]
    journal.deliver(sid, wire)
    assert wire.media_calls == [(sid, digest(PNG), len(PNG), "image/png")]
    journal.close()


def test_the_spool_holds_the_bytes_and_only_until_they_are_uploaded(tmp_path):
    wire = MediaDoor("claude_code", events=True)
    sid, path = _session(tmp_path, [cc_pasted()])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    journal.stage(sid, cwd=CWD, pasted_images=True)
    with sqlite3.connect(journal.db_path) as conn:
        ((stored,),) = conn.execute("SELECT bytes FROM media").fetchall()
    assert stored == PNG
    journal.deliver(sid, wire)
    assert _spool(journal) == [] and journal.pending(sid) is None
    journal.close()


# -- fragment versions (D21) ----------------------------------------------------------------


@pytest.mark.parametrize(
    "versions,expected",
    [([1], 1), ([1, 2], 2), ([2], 2), ([2, 1], 2), ([3], None), ([1, 3], 1), (["2", True, 2.0], None), ([], None)],
)
def test_the_fragment_version_is_the_highest_both_sides_build(versions, expected):
    remote = {"accepts": {"protocols": [2, 3], "fragment_versions": versions}}
    assert sj.fragment_version_for(remote) == expected
    assert sj.negotiate(remote) == ((3, False) if expected else (2, False))


def test_a_builder_from_before_version_2_builds_only_its_own(monkeypatch):
    class OldBuilder:
        FRAGMENT_VERSION = 1

    monkeypatch.setattr(sj, "_fragment_module", lambda: OldBuilder)
    assert sj.fragment_version_for({"accepts": {"fragment_versions": [1, 2]}}) == 1
    assert sj.fragment_version_for({"accepts": {"fragment_versions": [2]}}) is None


def test_a_state_from_before_versions_builds_version_1(tmp_path):
    """A stream a tap before this one started stores no version: it keeps
    building version 1 until a receipts answer says otherwise."""
    assert sj._stream_fragment_version({}, atif_fragment) == 1
    assert sj._stream_fragment_version({"fragment_version": 9}, atif_fragment) == 1
    wire = MediaDoor("claude_code", versions=(1, 2))
    sid, path = _session(tmp_path, [cc_pasted()])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    journal.update(sid, fragment_version=None, media=None)  # as an older tap left it
    (encoded,) = _drain(journal, wire, sid)
    body = json.loads(encoded)
    assert body["fragment_version"] == 1 and {f["v"] for f in body["fragments"]} == {1}
    assert wire.media_calls == []  # version 1 carries no image, so none is uploaded
    journal.close()


def test_a_stream_follows_the_server_to_version_2_and_back(tmp_path):
    wire = MediaDoor("claude_code", versions=(1,))
    sid, path = _session(tmp_path, [cc_pasted()])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    wire.versions = [1, 2]
    _write(path, [cc_pasted(JPEG, "image/jpeg")])
    _start(journal, wire, sid, path)  # a later daemon start reads the receipts again
    _drain(journal, wire, sid)
    wire.versions = [1]
    _write(path, [_text_line("claude_code", "rolled back")])
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    assert [b["fragment_version"] for b in wire.bodies(sid)] == [1, 2, 1]
    assert [b["protocol_version"] for b in wire.bodies(sid)] == [3, 3, 3]
    assert list(wire.stored) == [(sid, digest(JPEG))]
    journal.close()


def test_version_2_without_images_is_version_1_plus_its_version_number():
    """The engine's rule the tap relies on: v2 minus image parts IS v1."""
    event = {"line_no": 0, "raw": sanitize.sanitize_event(cc_pasted())}
    v1, v2 = atif_fragment.fragment(event, 1), atif_fragment.fragment(event, 2)
    assert v2 == v1 | {"v": 2}  # no sha256 on the placeholder: no image part
    event["raw"]["message"]["content"][0]["sha256"] = digest(PNG)
    with_image = atif_fragment.fragment(event, 2)
    assert [p for p in with_image["parts"] if p["type"] == "image"] == [
        {"type": "image", "seq": 0, "media_type": "image/png", "sha256": digest(PNG)}
    ]
    assert atif_fragment.fragment(event, 1) == v1


# -- the upload state machine ----------------------------------------------------------------


def _staged(tmp_path, wire, lines=None):
    sid, path = _session(tmp_path, lines or [cc_pasted()])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    body = journal.stage(sid, cwd=CWD, pasted_images=True)
    return journal, sid, body


def test_have_uploads_nothing_and_the_batch_goes(tmp_path):
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    wire.answer = (200, {"status": "have"})
    assert journal.deliver(sid, wire)
    assert wire.puts == [] and wire.log == ["media", "post"] and _spool(journal) == []
    journal.close()


@pytest.mark.parametrize("status", [403, 404, 409, 413, 415, 422, 429])
def test_a_final_refusal_drops_the_image_and_the_batch_goes(tmp_path, status):
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    wire.answer = (status, {"detail": {"reason": "media_budget"}})
    assert journal.deliver(sid, wire)
    assert wire.puts == [] and wire.accepted[(sid, 0)] == body  # still names the image
    assert _image_parts(json.loads(body)) and _spool(journal) == []
    journal.close()


def test_storage_refusing_the_bytes_is_final_for_the_image(tmp_path):
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    wire.put_status = 400  # e.g. XAmzContentChecksumMismatch
    assert journal.deliver(sid, wire)
    assert wire.log == ["media", "put", "post"] and _spool(journal) == []
    journal.close()


def test_the_put_carries_exactly_the_signed_headers_and_is_refused_otherwise(tmp_path):
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    journal.deliver(sid, wire)
    (url, headers, data) = wire.puts[0]
    assert data == PNG and headers == {
        "Content-Length": str(len(PNG)),
        "Content-Type": "image/png",
        "x-amz-checksum-sha256": base64.b64encode(hashlib.sha256(PNG).digest()).decode(),
    }
    journal.close()


@pytest.mark.parametrize(
    "answer",
    [
        {"status": "upload", "method": "PUT", "url": "file:///etc/passwd", "headers": {}},
        {"status": "upload", "method": "PUT", "url": "https://x.invalid/a", "headers": {"Authorization": "Bearer x"}},
        {"status": "upload", "method": "PUT", "url": "https://x.invalid/a", "headers": {"Content-Length": "1"}},
        {"status": "upload", "method": "POST", "url": "https://x.invalid/a", "headers": {}},
        {"status": "something new"},
    ],
    ids=["not-http", "credential-header", "wrong-length", "not-put", "unknown-status"],
)
def test_an_answer_this_client_will_not_follow_is_final_for_the_image(tmp_path, answer):
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    wire.answer = (200, answer)
    assert journal.deliver(sid, wire)
    assert wire.puts == [] and _spool(journal) == []
    journal.close()


def test_410_from_the_media_door_is_the_sessions_deletion(tmp_path):
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    wire.answer = (410, {"detail": {"reason": "session_deleted", "session_id": sid, "source": "claude_code"}})
    with pytest.raises(SessionDeleted):
        journal.deliver(sid, wire)
    assert "post" not in wire.log and journal.pending(sid) is None and _spool(journal) == []
    assert journal.is_deleted(sid)
    journal.close()


@pytest.mark.parametrize("failure", ["door-503", "door-no-answer", "put-503", "put-no-answer"])
def test_a_failure_that_may_pass_holds_the_batch_and_resends_the_same_bytes(tmp_path, failure):
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    if failure.startswith("door"):
        wire.answer = (503 if failure == "door-503" else 0, {"detail": {"reason": "media_unavailable"}})
    else:
        wire.put_status = 503 if failure == "put-503" else 0
    wire.last_request_retryable = failure.endswith("no-answer")
    with pytest.raises(DeliveryPending) as waiting:
        journal.deliver(sid, wire)
    assert waiting.value.retryable
    assert "post" not in wire.log and journal.pending(sid) == body
    assert _spool(journal) == [(sid, digest(PNG), "image/png", len(PNG))]
    # Next pass: the same pending bytes, the image uploads, then they go.
    wire.answer = wire.put_status = None
    assert journal.stage(sid, cwd=CWD, pasted_images=True) == body
    assert journal.deliver(sid, wire)
    assert wire.accepted[(sid, 0)] == body and wire.stored == {(sid, digest(PNG)): PNG}
    assert _spool(journal) == []
    journal.close()


def test_an_image_that_never_uploads_is_given_up_and_capture_goes_on(tmp_path, monkeypatch):
    clock = [1_000_000.0]
    monkeypatch.setattr(sj.time, "time", lambda: clock[0])
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    wire.answer = (503, {"detail": {"reason": "media_unavailable"}})
    for _ in range(sj.MEDIA_RETRY_MIN_ATTEMPTS + 2):  # many failures, but quickly
        with pytest.raises(DeliveryPending):
            journal.deliver(sid, wire)
        clock[0] += 60
    clock[0] += sj.MEDIA_RETRY_WINDOW_SECONDS
    assert journal.deliver(sid, wire)  # given up: the batch goes, the image is not available
    assert wire.accepted[(sid, 0)] == body and _spool(journal) == []
    journal.close()


def test_a_retired_batch_takes_its_images_with_it(tmp_path):
    """A refused protocol-3 batch 0 restarts on protocol 2: its spool rows go
    with it, and the new batch spools its own."""
    wire = MediaDoor("claude_code")
    wire.refuse_batch0 = sj.PROTOCOL3_REFUSALS[0]
    journal, sid, body = _staged(tmp_path, wire)
    with pytest.raises(sj.ProtocolRestarted):
        journal.deliver(sid, wire)
    assert _spool(journal) == []
    again = json.loads(journal.stage(sid, cwd=CWD, pasted_images=True))
    assert again["protocol_version"] == 2 and [b["sha256"] for b in _placeholders(again)] == [digest(PNG)]
    assert len(_spool(journal)) == 1
    journal.close()


def test_rows_an_older_tap_left_are_swept(tmp_path):
    """A tap before this one delivers a batch without knowing `media`: its
    rows are dropped by the next stage, never uploaded for a gone batch."""
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    # What an older tap's acknowledgement does: cursors forward, pending gone,
    # and `media` (a table it does not know) untouched.
    payload = json.loads(body)
    journal.update(sid, last_seq=0, protocol_version=3, **{
        k: payload[k] for k in ("source_byte_end", "source_line_end", "event_end", "prefix_sha256")
    })
    with sqlite3.connect(journal.db_path) as conn:
        conn.execute("DELETE FROM pending")
    assert len(_spool(journal)) == 1
    _write(Path(journal.get(sid)["path"]), [_text_line("claude_code", "next")])
    journal.stage(sid, cwd=CWD, pasted_images=True)
    assert _spool(journal) == []
    journal.close()


# -- D16: a line too long to read is skipped, and capture goes on ------------------------------


def test_an_oversize_line_is_skipped_and_said(tmp_path, monkeypatch):
    monkeypatch.setattr(sj, "MAX_SOURCE_LINE", 4096)
    wire = MediaDoor("claude_code", events=True)
    big = json.dumps({"type": "user", "message": {"role": "user", "content": "x" * 10_000}}).encode() + b"\n"
    sid, path = _session(tmp_path, [_text_line("claude_code", "before")])
    with path.open("ab") as handle:
        handle.write(big)
    _write(path, [_text_line("claude_code", "after")])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    events = [e["raw"] for b in wire.bodies(sid) for e in b["events"]]
    assert [e.get("subtype") for e in events] == [None, "oversize_line", None]
    assert events[1] == sj.oversize_line_event(len(big))
    assert f"{len(big):,} bytes" in events[1]["content"]
    assert "after" in json.dumps(events[2])
    assert journal.get(sid)["source_byte_end"] == path.stat().st_size
    assert journal.get(sid)["source_line_end"] == 3
    assert not list(SCHEMA.iter_errors(events[1]))
    fragment = wire.bodies(sid)[-1]["fragments"][1]
    assert fragment["kind"] == "system" and fragment["line"]["line_no"] == 1
    journal.close()


def test_an_oversize_line_still_being_written_waits(tmp_path, monkeypatch):
    monkeypatch.setattr(sj, "MAX_SOURCE_LINE", 4096)
    wire = MediaDoor("claude_code")
    sid, path = _session(tmp_path, [_text_line("claude_code", "before")])
    with path.open("ab") as handle:
        handle.write(b'{"type": "user", "message": {"content": "' + b"x" * 10_000)  # no newline yet
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    assert len(wire.bodies(sid)) == 1
    with path.open("ab") as handle:
        handle.write(b'"}}\n')
    _write(path, [_text_line("claude_code", "after")])
    _drain(journal, wire, sid)
    assert journal.get(sid)["source_byte_end"] == path.stat().st_size
    journal.close()


def test_a_70_mib_line_no_longer_stalls_the_session(tmp_path):
    """THE REGRESSION (D16): one transcript line over 64 MiB raised
    DeliveryPending and kept the cursor, so every later turn of that session
    was never captured."""
    wire = MediaDoor("claude_code", events=True)
    sid, path = _session(tmp_path, [_text_line("claude_code", "before the paste")])
    head = b'{"type": "user", "message": {"role": "user", "content": "'
    with path.open("ab") as handle:
        handle.write(head)
        chunk = b"A" * (1024 * 1024)
        for _ in range(70):
            handle.write(chunk)
        handle.write(b'"}}\n')
    big = len(head) + 70 * 1024 * 1024 + 4
    _write(path, [_text_line("claude_code", "the next turn")])
    journal = _journal(tmp_path, wire)
    _start(journal, wire, sid, path)
    _drain(journal, wire, sid)
    events = [e["raw"] for b in wire.bodies(sid) for e in b["events"]]
    assert [e.get("subtype") for e in events] == [None, "oversize_line", None]
    assert f"{big:,} bytes" in events[1]["content"]
    assert "the next turn" in json.dumps(events[2])
    assert journal.get(sid)["source_byte_end"] == path.stat().st_size
    journal.close()


# -- D25: what the wizard's Settings row writes is what the tap reads --------------------------


@pytest.mark.parametrize("on", [True, False])
def test_the_tap_reads_what_the_wizard_writes(tmp_path, monkeypatch, on):
    import ast
    import subprocess
    import sys

    from probe.sdk import session_marker

    tap_config = _AGENT / "plugins" / "probe-research-tap" / "tap" / "config.py"
    (key,) = [
        node.value.value
        for node in ast.parse(tap_config.read_text()).body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "PASTED_IMAGES_KEY" for t in node.targets)
    ]
    assert key == session_marker.PASTED_IMAGES_KEY
    config = tmp_path / "config.json"
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(config))
    session_marker.write_pasted_images(not on)
    session_marker.write_pasted_images(on)  # the switch back must undo it, not stack
    assert session_marker.pasted_images_on() is on
    read = subprocess.run(
        [sys.executable, "-c", "from tap import config; print(config.pasted_images_on())"],
        cwd=tap_config.parent.parent, capture_output=True, text=True, timeout=60,
        env={"PROBE_CONFIG_PATH": str(config), "PATH": "/usr/bin:/bin", "HOME": str(tmp_path)},
    )
    assert read.returncode == 0, read.stderr
    assert read.stdout.strip() == str(on)


# -- where the image's bytes may be PUT (SSRF guard) ------------------------------------------

PUBLIC_HTTPS = "https://api.research.prbe.ai"
SIGNED = "?X-Amz-Signature=synthetic-signature&X-Amz-Credential=synthetic"


def _answer(url: str, data: bytes = PNG) -> dict:
    return {
        "status": "upload", "method": "PUT", "url": url,
        "headers": {"Content-Length": str(len(data)), "Content-Type": "image/png"},
    }


@pytest.mark.parametrize(
    "url,base",
    [
        pytest.param("http://169.254.169.254/latest/meta-data/", "http://synthetic.invalid", id="link-local-metadata"),
        pytest.param("http://127.0.0.1:8080/upload", "http://synthetic.invalid", id="loopback"),
        pytest.param("https://10.1.2.3/bucket/key", PUBLIC_HTTPS, id="private-literal"),
        pytest.param("https://192.168.1.10/bucket/key", PUBLIC_HTTPS, id="private-192-168"),
        pytest.param("https://[::1]/bucket/key", PUBLIC_HTTPS, id="ipv6-loopback"),
        pytest.param("https://[::ffff:127.0.0.1]/bucket/key", PUBLIC_HTTPS, id="ipv4-mapped-loopback"),
        pytest.param("https://[fe80::1]/bucket/key", PUBLIC_HTTPS, id="ipv6-link-local"),
        pytest.param("https://0.0.0.0/bucket/key", PUBLIC_HTTPS, id="unspecified"),
        pytest.param("https://224.0.0.1/bucket/key", PUBLIC_HTTPS, id="multicast"),
        pytest.param("https://localhost/bucket/key", PUBLIC_HTTPS, id="localhost-name"),
        pytest.param("https://minio.localhost/bucket/key", PUBLIC_HTTPS, id="dot-localhost"),
        pytest.param("https://internal.example/bucket/key", PUBLIC_HTTPS, id="name-resolving-only-private"),
        pytest.param("https://metadata.example/latest", PUBLIC_HTTPS, id="name-resolving-to-metadata"),
        pytest.param("http://storage.invalid/bucket/key", PUBLIC_HTTPS, id="http-under-https"),
        pytest.param("ftp://storage.invalid/bucket/key", PUBLIC_HTTPS, id="not-http"),
        pytest.param("https://user:pw@storage.invalid/bucket/key", PUBLIC_HTTPS, id="credentials-in-url"),
        pytest.param("http://[broken", PUBLIC_HTTPS, id="malformed-bracket"),
        pytest.param("https://storage.invalid:99999/key", PUBLIC_HTTPS, id="port-out-of-range"),
        pytest.param("https://storage.invalid:abc/key", PUBLIC_HTTPS, id="port-not-a-number"),
        pytest.param("https:///no-host", PUBLIC_HTTPS, id="no-host"),
        pytest.param("http://127.0.0.1:9000/bucket/key", "http://[broken", id="malformed-base"),
    ],
)
def test_a_put_target_that_could_reach_the_researchers_network_is_refused(url, base):
    assert sj._put_target(_answer(url + SIGNED), PNG, base) is None


@pytest.mark.parametrize(
    "url,base",
    [
        pytest.param("https://storage.invalid/bucket/key", PUBLIC_HTTPS, id="https-public-host"),
        pytest.param("https://bucket.example/key", PUBLIC_HTTPS, id="every-address-public"),
        pytest.param("https://half-internal.example/key", PUBLIC_HTTPS, id="not-every-address-private"),
        pytest.param("http://storage.invalid/key", "http://synthetic.invalid", id="http-under-http"),
        pytest.param("http://localhost:9000/bucket/key", "http://localhost:8000", id="localhost-beside-localhost"),
        pytest.param("http://127.0.0.1:9000/bucket/key", "http://127.0.0.1:8000", id="loopback-beside-loopback"),
        pytest.param("http://10.0.0.7:9000/bucket/key", "http://internal.example", id="private-beside-private-gateway"),
    ],
)
def test_a_put_target_where_storage_can_be_is_followed(url, base):
    assert sj._put_target(_answer(url + SIGNED), PNG, base) == (
        url + SIGNED, {"Content-Length": str(len(PNG)), "Content-Type": "image/png"}
    )


@pytest.mark.parametrize(
    "url", ["http://169.254.169.254/latest/meta-data/iam", "http://[broken", "https://storage.invalid:99999/k"]
)
def test_a_refused_put_target_is_final_for_the_image_and_the_batch_goes(tmp_path, caplog, url):
    """Refused, never retried and never a stall: the spool row goes, the batch
    goes (still naming the image, which the engine shows as not available),
    and the log never carries the signed query."""
    import logging

    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    wire.answer = (200, _answer(url + SIGNED))
    with caplog.at_level(logging.WARNING):
        assert journal.deliver(sid, wire)
    assert wire.puts == [] and _spool(journal) == [] and wire.accepted[(sid, 0)] == body
    assert "upload answer refused" in caplog.text
    assert "X-Amz-Signature" not in caplog.text and "synthetic-signature" not in caplog.text
    journal.close()


def test_a_put_host_that_does_not_resolve_waits_and_is_never_put(tmp_path):
    """Resolution failing is a network failure, not a verdict on the URL: no
    PUT is made, the batch waits (bounded by the give-up), and the next
    attempt asks the door again."""
    wire = MediaDoor("claude_code")
    journal, sid, body = _staged(tmp_path, wire)
    wire.answer = (200, _answer("https://nowhere.invalid/bucket/key" + SIGNED))
    with pytest.raises(DeliveryPending) as waiting:
        journal.deliver(sid, wire)
    assert waiting.value.retryable and wire.puts == [] and "post" not in wire.log
    assert len(_spool(journal)) == 1
    wire.answer = None
    assert journal.deliver(sid, wire) and wire.stored == {(sid, digest(PNG)): PNG}
    journal.close()


def test_the_real_resolver_reads_every_address_and_fails_closed():
    assert all(sj._local_address(a) for a in _REAL_RESOLVE("localhost"))
    with pytest.raises(sj.Unresolved):
        _REAL_RESOLVE("no-such-host.invalid")
