"""S6 §8 — the committed fixture corpus, consumed by WS-6 (here) and WS-8
(frontend panel). One corpus, two consumers: a fixture only one side has is how
the two sides drift.

Three tests are part of WS-6's Definition of Done:
  1. shape conformance — every fixture is well-formed for its declared shape;
  2. leak denylist — no fixture carries a ticket/token/cookie/secret/etc. key
     (S6 §6, the whole-table structural guard);
  3. legacy anchors — the transient-session and evicted-session fixtures match
     today's documented byte-shape so a compatibility break fails the build.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from matrx_ai.browser_handoff.outcomes import Status

FIX = Path(__file__).parent / "fixtures" / "browser_s6"

# S6 §6 name-denylist. Deliberately a NAME denylist and incomplete on its own —
# it is the second layer behind the structural reasons in the contract, never
# the only one.
_DENY = re.compile(
    r"ticket|token|claim|cookie|password|secret|totp|credential|"
    r"worker_url|worker_host|container_id|fencing|storage_uri|file_uri",
    re.IGNORECASE,
)

# base64 image blobs must never reach the model (S6 §1.3 / §6).
_BASE64_KEYS = {"screenshot_base64", "base64_data", "image_base64"}

_ALL = sorted(p.name for p in FIX.glob("*.json"))


def _load(name: str) -> dict:
    return json.loads((FIX / name).read_text())


def _walk_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _walk_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_keys(v)


def test_corpus_has_the_expected_files():
    assert len(_ALL) == 19, _ALL


@pytest.mark.parametrize("name", _ALL)
def test_shape_conformance(name):
    obj = _load(name)
    assert isinstance(obj, dict)
    if name.startswith("error_"):
        assert "error_type" in obj and "message" in obj
        assert obj.get("is_retryable") in (True, False)
    elif name.startswith("screenshot_"):
        assert obj.get("kind") == "image_ref"
        assert "media_ref" in obj
    elif name.startswith("resume_page_inventory"):
        assert set(["pages", "pages_total", "pages_shown", "pages_truncated"]) <= set(obj)
        for row in obj["pages"]:
            assert set(row) == {"page_id", "url", "title", "active"}
    elif "status" in obj:
        assert obj["status"] in ("ok", "human_required", "reopened_for_handoff")
        # every value of the Status literal is exhaustive (S6 §5.6)
        assert obj["status"] in Status.__args__


@pytest.mark.parametrize("name", _ALL)
def test_leak_denylist(name):
    obj = _load(name)
    for key in _walk_keys(obj):
        assert not _DENY.search(key), f"{name}: forbidden key {key!r} (S6 §6)"
        assert key not in _BASE64_KEYS, f"{name}: base64 blob key {key!r} reached the model"


def test_human_required_carries_success_true():
    for name in ("human_required_mfa.json", "human_required_captcha.json",
                 "human_required_credential_missing.json"):
        obj = _load(name)
        assert obj["success"] is True  # else the executor flips it to a failure
        assert obj["continuation_required"] is True


def test_reopened_volatile_state_preserved_is_false():
    obj = _load("reopened_for_handoff.json")
    assert obj["volatile_state_preserved"] is False
    assert obj["session_id"] != obj["previous_run_id"]


def test_truncated_inventory_keeps_active_page():
    obj = _load("resume_page_inventory_truncated.json")
    assert obj["pages_total"] == 40 and obj["pages_shown"] == 25
    assert obj["pages_truncated"] is True
    assert any(row["active"] for row in obj["pages"])


def test_legacy_transient_anchor_has_no_profile_keys():
    # The backwards-compatibility anchor: a legacy transient success emits NO
    # run_id/profile_id keys (S6 §4.1 #3).
    obj = _load("navigate_ok_transient_legacy.json")
    assert "run_id" not in obj and "profile_id" not in obj
    assert "status" not in obj  # legacy transient shape predates the status key
    assert len(obj["session_id"]) == 12  # 12-hex transient handle


def test_legacy_not_found_anchor_message_is_unchanged():
    # The regression anchor: the evicted-session error is byte-identical to
    # today's behavior (S6 §4.2 row 2 / §8).
    obj = _load("error_not_found_legacy.json")
    assert obj["error_type"] == "not_found"
    assert obj["is_retryable"] is False
    assert obj["suggested_action"] == "Call cloud_browser_navigate again to start a new session."


def test_screenshot_carries_no_base64_anywhere():
    for name in ("screenshot_ok_media_ref.json", "screenshot_media_ref_error.json"):
        raw = (FIX / name).read_text().lower()
        assert "base64" not in raw
