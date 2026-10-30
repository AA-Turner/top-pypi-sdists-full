"""The shared scanner's accelerator hook: same answers, read in fewer places.

The server plugs a Hyperscan index into `scan`/`scrub_changes`
(`app/security/fast_scan.py`); nothing on a researcher's machine does. These
tests drive the SAME windowed code with a pure-Python accelerator that keeps
the `Windows` contract exactly (a window around every match Python finds), and
with a noisy one that adds random extra windows, and require the gate's answer
to equal the unaccelerated one. Hyperscan-specific tests live server-side
(`tests/unit/test_fast_scan.py`).
"""

from __future__ import annotations

import base64
import json
import math
import random
import re
import tracemalloc
import urllib.parse

import pytest

from probe.sdk import redaction
from probe.sdk import secret_gate as gate
from probe.tap_core import secrets

_GHP = "ghp_KKF0RDt0Xaetn6QMfStFUWSus4jowQUux6hu"
_PLANTED = [
    "AWS_ACCESS_KEY_ID=AKIAWRRMRPMP6MCDARQ7\nAWS_SECRET_ACCESS_KEY=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",
    f'github_token = "{_GHP}"',
    "PROBE_TOKEN=ros_ing_d62e61df59a9c29e2b243ce3e0cf793e",
    'password = "bAtLWMRYlGyzWo"',
    # After a separator `_BASE64`'s lookbehind accepts (not `=`), so it decodes.
    "cfg: " + base64.b64encode(f"token={_GHP}".encode()).decode(),
    urllib.parse.quote(f"token={_GHP}"),
    "gh\x1b[31mp_" + _GHP[4:],
    "https://alice@example.org/x",
    "GET https://h/x?token=S3cr3tV4lu3xx&a=1",
    json.dumps({"credentials": {"user": "u"}}),
    json.dumps({"hub_token": None}),
    "authorization=Basic dXNlcjpwYXNz",
    "sk-12345678abcd",
    '{"token": "\\u0120the"}',
    "60 cookies * $0.10/cookie = $<<60*0.1=6>>6.",
    '"pad_token": "<pad>", "prompt_tokens": 12',
    "p\x00w\x00d\x00:\x00 \x00x",
]
#: Dense in hint words and changed by nothing: the key-name tier's negative
#: control (an accelerated `scrub_changes` that always said "changed" passed
#: every test before these).
_CLEAN_HINTED = [
    json.dumps({"pad_token": "<pad>", "prompt_tokens": 12, "sig_len": 3}),
    "the cookie jar holds 60 cookies",
    json.dumps({"config": {"aws_region": "us-east-1", "tokenizer": "gpt2"}}),
    json.dumps({"token": None, "max_tokens": 256, "passes": 2}),
    '{"eos_token": "</s>", "bos_token": "<s>"}',
]


def _document(seed: int, size: int, as_json: bool, pool: list[str] = _PLANTED) -> str:
    r = random.Random(seed)
    parts: list[str] = []
    while sum(map(len, parts)) < size:
        roll = r.random()
        if roll < 0.08:
            parts.append(r.choice(pool))
        elif roll < 0.4:
            parts.append(json.dumps({"run": f"{r.getrandbits(128):032x}", "loss": r.random(),
                                     "path": f"/home/r/ckpts/{r.getrandbits(32):08x}.pt"}))
        elif roll < 0.6:
            parts.append(base64.b64encode(r.randbytes(r.randint(8, 300))).decode())
        elif roll < 0.75:
            parts.append(r.randbytes(40).decode("utf-8", "replace"))
        else:
            parts.append(" ".join(f"{r.random():.4f}" for _ in range(10)))
    if as_json:
        return json.dumps([{"line": p} for p in parts])
    return "\n".join(parts)


def _reference(noise: float = 0.0):
    """An accelerator that keeps the `Windows` contract by asking Python itself:
    a window from each match's start to one past its end, optionally mixed with
    random extra windows (a superset must not change any answer)."""

    def accel(text: str):
        cache: dict[re.Pattern[str], list[tuple[int, int]]] = {}
        r = random.Random(len(text))

        def windows(pattern: re.Pattern[str]):
            if pattern not in cache:
                spans = [(m.start(), min(len(text), m.end() + 1)) for m in pattern.finditer(text)]
                for _ in range(int(noise * 20)):
                    lo = r.randrange(len(text))
                    spans.append((lo, min(len(text), lo + r.randint(1, 500))))
                merged: list[tuple[int, int]] = []
                for lo, hi in sorted(spans):
                    if merged and lo <= merged[-1][1]:
                        merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
                    else:
                        merged.append((lo, hi))
                cache[pattern] = merged
            return cache[pattern]

        return windows

    return accel


_DOCUMENTS = [
    _document(seed, size, as_json, pool)
    for seed in range(12)
    for size in (5_000, 70_000)
    for as_json in (False, True)
    for pool in (_PLANTED, _CLEAN_HINTED)
]


@pytest.mark.parametrize("noise", [0.0, 1.0])
@pytest.mark.heavy
def test_accelerated_gate_equals_the_exact_gate(noise):
    accel = _reference(noise)
    flagged = clean = encoded = 0
    for text in _DOCUMENTS:
        exact = gate._findings(text)
        flagged += bool(exact[1])
        clean += exact == ((), ())
        encoded += "encoded-secret" in exact[0]
        fast = gate._findings(text, accel)
        assert (set(fast[0]), set(fast[1])) == (set(exact[0]), set(exact[1])), text[:120]
    assert flagged, "the key-name tier must be exercised, not skipped by a scanner hit"
    assert clean >= 10, "a clean verdict must be exercised too"
    assert encoded, "a credential only decoding reveals must be exercised"


def test_a_window_cut_mid_token_is_not_a_shorter_token():
    """A stretch that ends inside a longer run must not read its prefix as a
    token: the start is matched again against the whole text."""
    text = ("0.1 " * 1_500) + _GHP + "extra" + (" 0.2" * 1_500)
    at = text.index(_GHP)
    cut = lambda _text: (lambda _pattern: [(at, at + len(_GHP))])  # noqa: E731
    assert not any(f.rule == "github-token" for f in secrets.scan(text))
    assert not any(f.rule == "github-token" for f in secrets.scan(text, _accel=cut))


def test_a_window_cut_mid_credential_reads_it_whole():
    """The other side of the same rule: a real match longer than its stretch
    (a 1,000-character bearer token read through a 100-character window) is
    found whole, not dropped as a truncation."""
    text = ("0.1 " * 1_500) + "Authorization: Bearer " + "A1b2" * 250 + (" 0.2" * 1_500)
    at = text.index("Authorization")
    cut = lambda _text: (lambda _pattern: [(at, at + 100)])  # noqa: E731
    exact = [(f.rule, f.start, f.end) for f in secrets.scan(text) if f.rule == "bearer-token"]
    assert exact
    assert [(f.rule, f.start, f.end) for f in secrets.scan(text, _accel=cut) if f.rule == "bearer-token"] == exact


def _spellings(key: str) -> set[str]:
    """Spellings a `_KEYED_VALUE` key can have (letters, digits, `_.-`)."""
    parts = key.split("_")
    return {
        "_".join(parts), "___".join(parts), "..".join(parts), "-".join(parts), "_.-".join(parts),
        parts[0] + "".join(p.title() for p in parts[1:]), "_".join(parts).upper(),
        f"hub_{key}", f"x_{key}_v2",
    }


def test_the_key_hints_cover_every_sensitive_spelling():
    """`scrub_changes` reads keyed values only where `_SENSITIVE_KEY_HINT` fires,
    and a JSON walk only strings `scrub_hint` fires on. Both are hand-kept
    supersets of `is_sensitive_key`; this is what keeps them one."""
    hint = redaction.scrub_hint()
    keys = [*redaction._SENSITIVE_KEYS, "vendor_api_key", "x_amz_signature", "my_sig", "hub_token",
            "db_password_hash", "client_secret", "aws_credentials"]
    for key in keys:
        for spelling in _spellings(key):
            if not redaction.is_sensitive_key(spelling):
                continue
            for pair in (f"{spelling}=x", f'"{spelling}": "x"', f"{spelling} : x"):
                assert redaction._KEYED_VALUE.search(pair).group("key") == spelling
                assert redaction._SENSITIVE_KEY_HINT.search(pair), pair
            assert hint.search(spelling), spelling


def test_every_anchor_spelling_carries_a_keyword():
    """`_ANCHORED` runs only where one of `_ANCHOR_KEYWORDS` occurs (the plain
    prefilter and the quick check's windows alike). `privateKey` once had none."""
    for word in secrets._ANCHOR_WORDS:
        for separator in ("", "_", " ", "-"):
            spelling = word.replace("[_ -]?", separator)
            assert any(k in spelling.lower() for k in secrets._ANCHOR_KEYWORDS), spelling


def test_scrub_changes_without_an_accelerator_is_the_comparison():
    for text in _DOCUMENTS[:8] + _PLANTED:
        assert redaction.scrub_changes(text) == (redaction.scrub_string(text) != text)


def test_an_accelerator_that_cannot_index_changes_nothing():
    for text in _DOCUMENTS[:6]:
        assert gate._findings(text, lambda _text: None) == gate._findings(text)


def test_windowed_scan_decodes_one_layer_only():
    """`_scan_windowed` used to decode again, so `_decode=False` on a text over
    64K characters still decoded it: an ANSI-split token was found or missed
    depending on the length of the text around it."""
    hidden = "gh\x1b[31mp_" + _GHP[4:]
    text = ("0.1234 " * 12_000) + hidden + (" 0.5678" * 1_000)
    assert len(text) > secrets.MAX_SCAN_CHARS
    assert not any(f.rule == "github-token" for f in secrets.scan(text, _decode=False))
    assert any(f.rule == "github-token" for f in secrets.scan(text))


def test_unquote_matches_urllib():
    r = random.Random(1)
    alphabet = "%%%0123456789abcdefABCDEFgz éÿ�\x00-_"
    for _ in range(20_000):
        value = "".join(r.choice(alphabet) for _ in range(r.randint(0, 24)))
        assert redaction._unquote(value) == urllib.parse.unquote(value)
    blob = r.randbytes(200_000).decode("utf-8", "replace")
    assert redaction._unquote(blob) == urllib.parse.unquote(blob)


def test_entropy_helpers_keep_their_answers():
    r = random.Random(2)
    for _ in range(2_000):
        value = "".join(r.choice("abcAB12+/=") for _ in range(r.randint(1, 60)))
        counts: dict[str, int] = {}
        for char in value:
            counts[char] = counts.get(char, 0) + 1
        expected = 0.0
        for count in counts.values():
            p = count / len(value)
            expected -= p * math.log2(p)
        assert secrets.shannon_entropy(value) == expected
        assert secrets.low_diversity(value) == (len(counts) < 6)


def test_readable_keeps_its_answer():
    for text in ["plain\ttext\r\n", "bell\x07", "", "émoji ✓", "\x00", "tab\tonly"]:
        assert gate._readable(text) == all(c.isprintable() or c in "\t\r\n" for c in text)


def test_a_sensitive_pair_nested_in_a_plain_value_is_read():
    """`_KEYED_VALUE` consumes `config='api_key=abc'` whole, so the nested pair
    is only seen through the recursion `_keyed` runs on a plain key's value."""
    pad = "0.1234 loss step " * 400
    text = pad + " config='api_key=abc' " + pad
    assert gate._findings(text) == ((), (gate.FIELD_NAME_RULE,))
    assert gate._findings(text, _reference()) == gate._findings(text)


# --- Issue 3611: memory follows the text, never the number of escapes --------


def test_unquote_matches_urllib_across_long_runs():
    """A run past `_PERCENT_RUN`'s 4096 escapes arrives as several matches,
    decoded through one incremental decoder: a multi-byte character, or an
    invalid sequence, across that seam decodes as in one piece."""
    r = random.Random(3)
    for text in ("日本語" * 3_000, "é" * 5_000 + "x", "\U0001f600" * 2_000):
        quoted = urllib.parse.quote(text)
        assert redaction._unquote(quoted) == urllib.parse.unquote(quoted) == text
    for _ in range(5):
        raw = r.randbytes(r.randint(4_000, 20_000))
        blob = "".join(f"%{b:02X}" for b in raw) + "x" + "%e6%97" * 3_000
        assert redaction._unquote(blob) == urllib.parse.unquote(blob)


def test_decode_escapes_matches_the_substitution():
    def substituted(value: str) -> str:
        return redaction._UNICODE_ESCAPE.sub(lambda m: chr(int(m.group(1), 16)), redaction._unquote(value))

    r = random.Random(4)
    pieces = ["\\u4e00", "\\u00e9", "\\uD83D", "\\u", "x", "%41", "%e4%b8", "%80", "\\\\", "u12", " "]
    for _ in range(5_000):
        value = "".join(r.choice(pieces) for _ in range(r.randint(0, 30)))
        assert redaction._decode_escapes(value) == substituted(value)
    long = "\\u4e00x" * 20_000 + "%e6%97%a5" * 9_000
    assert redaction._decode_escapes(long) == substituted(long)


def test_neighbourhoods_merge_as_merge_does():
    r = random.Random(5)
    for _ in range(500):
        text = "".join(r.choice("ab%41 ") for _ in range(r.randint(0, 400)))
        reach = r.randint(0, 30)
        matches = list(re.finditer(r"%41", text))
        expected = redaction._merge(
            [(max(0, m.start() - reach), min(len(text), m.end() + reach)) for m in matches]
        )
        assert list(redaction._neighbourhoods(iter(matches), len(text), reach)) == expected


def test_only_escape_dense_text_skips_the_accelerator():
    accel = object()
    limit = "x" * 6_400 + "%41" * 104  # 104 escapes in 6,712 characters: the limit
    assert redaction.scan_accelerator(limit, accel) is accel
    assert redaction.scan_accelerator(limit + "%41", accel) is None
    # Ordinary escaped text keeps the accelerator (one escape per 119
    # characters: 0.41 s accelerated against 1.43 s windowed, per 4 MiB).
    assert redaction.scan_accelerator(("x" * 116 + "%41") * 1_000, accel) is accel
    assert redaction.scan_accelerator(json.dumps("日本語" * 2_000), accel) is None
    assert redaction.scan_accelerator("x" * 10_000, None) is None


def test_a_document_too_big_to_parse_is_read_as_text(monkeypatch):
    """A `MemoryError` from parsing a JSON document (the multipart verifier's
    memory cap) sends the key-name tier to its text passes, not to a refusal
    that drops every finding the inspection already made."""
    document = json.dumps([{"api_key": 12345}] + [{}] * 3_000)
    assert redaction.scrub_changes(document, accel=_reference()) is True

    def boom(*_args, **_kwargs):
        raise MemoryError

    monkeypatch.setattr(redaction, "json", type("json", (), {"loads": staticmethod(boom)}))
    assert redaction.scrub_changes(document, accel=_reference()) is True
    assert gate._findings(document, _reference()) == ((), (gate.FIELD_NAME_RULE,))


@pytest.mark.parametrize(
    "text",
    [
        json.dumps(["日本語のテキスト" * 2_000, f"token={_GHP}", "テキスト" * 2_000]),
        "%41" * 20_000 + " " + urllib.parse.quote(f"token={_GHP}") + " " + "%41" * 20_000,
        # Double-encoded: the key-name tier's own scan of the decoded view.
        urllib.parse.quote(urllib.parse.quote(f"token={_GHP}") * 5_000),
        "%41" * 30_000 + " config='api_key=abc' ",
    ],
)
def test_escape_dense_text_gets_the_exact_answer(text):
    assert redaction.scan_accelerator(text, _reference()) is None
    fast = gate._findings(text, _reference())
    assert (set(fast[0]), set(fast[1])) == tuple(map(set, gate._findings(text)))
    assert fast != ((), ())


@pytest.mark.parametrize(
    ("text", "decoded", "bound_mib"),
    [("%41" * 300_000, 300_000, 6), ("\\u4e00" * 1_200_000, 1_200_000, 24)],
)
def test_the_key_name_tier_decodes_escapes_in_bounded_memory(text, decoded, bound_mib):
    """`(?:%XX)+` kept regex backtracking state per escape (39 MiB for these
    300K `%41`), and `\\uXXXX` past U+00FF a new string each until the end of
    the substitution (81-100 MiB for these 1.2M). Now ~1 MiB and 5-10 MiB: on
    Python 3.10/3.11 `io.StringIO` holds up to 100K pieces (~8 MB) before it
    joins them, a constant, not a cost per escape."""
    tracemalloc.start()
    try:
        out = redaction._decode_escapes(text)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert len(out) == decoded
    assert peak < bound_mib * 2**20, f"{peak / 2**20:.1f} MiB"


def test_an_opaque_blob_is_read_in_overlapping_windows(monkeypatch):
    """Bytes no decode reads as text are read through their ASCII-preserving
    view a window at a time (`_OPAQUE_WINDOW`, shrunk here): a credential across
    a seam is read whole, and the answer is the whole view's."""
    monkeypatch.setattr(gate, "_OPAQUE_WINDOW", 200_000)
    r = random.Random(6)
    data = bytearray(r.randbytes(600_000))
    for offset, snippet in {199_990: f"token={_GHP}", 450_000: 'password = "bAtLWMRYlGyzWo"'}.items():
        data[offset:offset + len(snippet) + 2] = f" {snippet} ".encode()
    data = bytes(data)
    seen: list[int] = []
    findings = gate._findings
    monkeypatch.setattr(gate, "_findings", lambda text, accel=None: seen.append(len(text)) or findings(text, accel))
    result = gate.inspect_bytes(data, scan_policy=gate.ScanPolicy())
    assert max(seen) <= 200_000, "the view was never built whole"
    whole = findings(data.decode("utf-8", errors="replace"))
    assert {"github-token", "anchored-secret"} <= set(result.rules)
    assert set(result.rules) == set(whole[0]) | set(whole[1])
