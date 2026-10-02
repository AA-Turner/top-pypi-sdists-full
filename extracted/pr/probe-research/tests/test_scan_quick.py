"""The researcher-side quick check (`scan_quick`): the full scanner's rules and
filters, read only next to each rule's keywords, with no decoding layer."""

from __future__ import annotations

import json
import random

import pytest

from probe.tap_core import secrets

_GHP = "ghp_KKF0RDt0Xaetn6QMfStFUWSus4jowQUux6hu"
# One plainly written credential per rule the quick check covers.
_PLAIN = {
    "aws-access-key-id": "AKIAWRRMRPMP6MCDARQ7",
    "anthropic-api-key": "sk-ant-api03-vQJX9fE3ozdn8iZZyHYHXrYdQ7p5a3E5xCYpTAM3kAkXujq63ZHiOVNrHIdjKXlan062j0ifwrNTHg4E",
    "probe-token": "probe_pat_" + "a" * 16 + "0123456789abcdef",
    "probe-ingest-token": "ros_ing_d62e61df59a9c29e2b243ce3e0cf793e",
    "openai-api-key": "sk-proj-l6dWDbLE6ZcugmlwnLpMTEMGoCl5rzl6W7tOJ80JE2qF4z69",
    "openai-api-key-classic": "sk-abcdefghij0123456789T3BlbkFJabcdefghij0123456789",
    "github-token": _GHP,
    "github-fine-grained-pat": "github_pat_TCKM658R6rCHZtDuoz97U5_Hpfx1xbxRzLyYmVKxZyIj1LKllfWD42sZboHdIkKs9bP1Z",
    "huggingface-token": "hf_AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGh",
    "slack-token": "xoxb-510216337857-6555277819065-2aZy1f4D9IObHxTaZhA7A6jp",
    "slack-webhook": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
    "gcp-api-key": "AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY",
    "stripe-live-key": "sk_live_VkOyRkunyBHsr4dEtUhtPjX6",
    "gitlab-pat": "glpat-xY3zAbCdEfGhIjKlMnOp",
    "npm-token": "npm_AbCdEfGhIjKlMnOpQrStUvWxYz0123456789",
    "wandb-key": "wandb login 0123456789abcdef0123456789abcdef01234567",
    "private-key-block": "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAu1SU1LfVLPHCozMxH2Mo4lgOEePz\n-----END RSA PRIVATE KEY-----",
    "jwt": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
    "bearer-token": "Authorization: Bearer abcDEF123456.ghiJKL7890mno",
    "basic-auth": "authorization=Basic dXNlcjpwYXNzd29yZDEyMw",
    "credential-uri": "postgres://trainer:vt8rKEUOvC0yfgjN@db.internal:5432/runs",
}
_ANCHORED = [
    'password = "bAtLWMRYlGyzWo"',
    'secret_key = "x8Kd93mZq1Lr7Vt4Np2Wy6Hc0Bg5Jf"',
    "AWS_SECRET_ACCESS_KEY=denCJjluEV99TARR+rjp5B42HXtVtPLx2Vm7Pkk3",
]


def _filler(size: int, seed: int = 0) -> str:
    """ML-shaped text dense in the words the anchored rules key on."""
    r = random.Random(seed)
    rows = []
    while sum(map(len, rows)) < size:
        rows.append(json.dumps({
            "run": f"{r.getrandbits(128):032x}", "prompt_tokens": r.randint(1, 900),
            "pad_token": "<pad>", "eos_token": "</s>", "loss": r.random(),
            "text": "the model token key pass secret batch",
        }))
    return "\n".join(rows)


def _rules(findings) -> set[str]:
    return {finding.rule for finding in findings}


def test_every_rule_has_a_keyword():
    """A rule without keywords would have no windows and be read nowhere."""
    assert all(rule.keywords for rule in secrets._RULES)


@pytest.mark.parametrize("rule", sorted(_PLAIN))
def test_each_plain_credential_is_found_in_a_long_text(rule):
    text = _filler(20_000) + "\n" + _PLAIN[rule] + "\n" + _filler(20_000, seed=1)
    assert rule in _rules(secrets.scan_quick(text))


@pytest.mark.parametrize("value", _ANCHORED)
def test_key_name_values_are_found(value):
    text = _filler(10_000) + "\n" + value + "\n" + _filler(10_000, seed=2)
    assert "anchored-secret" in _rules(secrets.scan_quick(text))


def test_quick_agrees_with_the_full_scan_on_plain_credentials():
    text = _filler(8_000) + "\n" + "\n".join([*_PLAIN.values(), *_ANCHORED]) + "\n" + _filler(8_000, seed=3)
    assert _rules(secrets.scan_quick(text)) == _rules(secrets.scan(text))


def test_clean_ml_text_finds_nothing():
    assert secrets.scan_quick(_filler(200_000)) == []


def test_a_keyword_at_a_window_edge_is_not_misread():
    """A token cut by the end of its window must not match as a shorter one."""
    text = _filler(10_000) + " " + _GHP + "extra" + " " + _filler(1_000, seed=4)
    assert "github-token" not in _rules(secrets.scan_quick(text))
    assert "github-token" not in _rules(secrets.scan(text))


def test_offsets_survive_unicode_that_lowercases_longer():
    # `İ`.lower() is two characters; keyword offsets must still line up.
    text = ("İ" * 5_000) + " " + _GHP + " " + ("x" * 5_000)
    findings = secrets.scan_quick(text)
    assert [text[f.start:f.end] for f in findings if f.rule == "github-token"] == [_GHP]


def test_escaped_credentials_are_left_to_the_server():
    """The quick check has no decoding layer; the server's full scan does."""
    escaped = _GHP.replace("K", "%4B")
    text = _filler(6_000) + " token-in-url " + escaped + " " + _filler(6_000, seed=5)
    assert "github-token" not in _rules(secrets.scan_quick(text))
    assert "github-token" in _rules(secrets.scan(text))


def test_redact_quick_replaces_what_it_finds():
    text = _filler(5_000) + f"\nGITHUB_TOKEN={_GHP}\n"
    cleaned, rules = secrets.redact_quick(text)
    assert _GHP not in cleaned and "github-token" in rules
    assert secrets.redact_quick(cleaned)[1] == [], "redacted output is a fixed point"


@pytest.mark.parametrize("key", ["privateKey", "accessKey", "PRIVATEKEY"])
def test_a_key_name_without_a_separator_is_read(key):
    """`_ANCHORED` accepts `private[_ -]?key`; its keywords must cover the
    unseparated spelling too, or no window ever opens there."""
    text = _filler(8_000) + f'\n"{key}": "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"\n'
    text += _filler(8_000, seed=6)
    assert "anchored-secret" in _rules(secrets.scan(text))
    assert "anchored-secret" in _rules(secrets.scan_quick(text))


def test_a_credential_longer_than_its_window_is_read_whole():
    """Keyword windows reach `_QUICK_TAIL` past a keyword; a match cut there is
    matched again against the whole text, not dropped as a truncation."""
    token = "A1b2" * 250  # a 1,000-character opaque bearer token
    text = _filler(8_000) + f"\nAuthorization: Bearer {token}\n" + _filler(8_000, seed=7)
    quick = [(f.rule, f.start, f.end) for f in secrets.scan_quick(text) if f.rule == "bearer-token"]
    assert quick and quick == [(f.rule, f.start, f.end) for f in secrets.scan(text) if f.rule == "bearer-token"]


def test_a_password_on_a_long_line_is_read():
    line = "step=1 " * 110 + "password=correct-horse-battery-staple-9 " + "loss=0.1 " * 5
    text = _filler(6_000) + "\n" + line + "\n" + _filler(6_000, seed=8)
    assert _rules(secrets.scan_quick(text)) == _rules(secrets.scan(text, _decode=False))
    assert "anchored-secret" in _rules(secrets.scan_quick(text))
