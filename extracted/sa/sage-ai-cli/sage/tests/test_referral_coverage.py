"""Full-branch tests for backend.referral.

Uses tmp_path to redirect SAGE_REFERRAL_LOG so we don't touch the user's
real /tmp/sage-referrals.jsonl.
"""

from __future__ import annotations

import importlib
import json
import os
from pathlib import Path

import pytest


@pytest.fixture
def referral_module(tmp_path, monkeypatch):
    """Reload backend.referral with a tmp log path so each test is isolated."""
    log_path = tmp_path / "referrals.jsonl"
    monkeypatch.setenv("SAGE_REFERRAL_LOG", str(log_path))
    import backend.referral as r
    importlib.reload(r)
    yield r, log_path
    importlib.reload(r)  # reset for the next test


class TestRecordReferral:

    def test_records_basic_signal(self, referral_module):
        r, log_path = referral_module
        r.record_referral(new_user_uid="u-new", referrer_code="u-ref")
        assert log_path.exists()
        entry = json.loads(log_path.read_text().strip())
        assert entry["referred"] == "u-new"
        assert entry["referrer"] == "u-ref"
        assert "ts" in entry

    def test_ignores_empty_ids(self, referral_module):
        r, log_path = referral_module
        r.record_referral(new_user_uid="", referrer_code="u-ref")
        r.record_referral(new_user_uid="u-new", referrer_code="")
        assert not log_path.exists()

    def test_blocks_self_referral(self, referral_module):
        r, log_path = referral_module
        r.record_referral(new_user_uid="u-1", referrer_code="u-1")
        assert not log_path.exists()


class TestGetReferrerFor:

    def test_finds_existing_referral(self, referral_module):
        r, _ = referral_module
        r.record_referral(new_user_uid="u-new", referrer_code="u-ref")
        assert r.get_referrer_for("u-new") == "u-ref"

    def test_returns_none_when_no_log(self, referral_module):
        r, _ = referral_module
        # No referral recorded yet
        assert r.get_referrer_for("u-new") is None

    def test_returns_none_for_unknown_user(self, referral_module):
        r, _ = referral_module
        r.record_referral(new_user_uid="u-new", referrer_code="u-ref")
        assert r.get_referrer_for("u-other") is None

    def test_handles_empty_uid(self, referral_module):
        r, _ = referral_module
        assert r.get_referrer_for("") is None

    def test_skips_malformed_lines(self, referral_module, tmp_path):
        r, log_path = referral_module
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(
            "not-json\n"
            '{"ts":"t","referrer":"u-ref","referred":"u-new"}\n'
        )
        # Malformed lines must not crash the lookup
        assert r.get_referrer_for("u-new") == "u-ref"


class TestGenerateReferralLink:

    def test_default_base(self):
        from backend.referral import generate_referral_link
        assert generate_referral_link("u-1") == "https://sageworksai.com/?ref=u-1"

    def test_custom_base(self):
        from backend.referral import generate_referral_link
        assert generate_referral_link("u-1", base_url="https://staging.test") == \
               "https://staging.test/?ref=u-1"


class TestListReferralsBy:

    def test_returns_all_for_referrer(self, referral_module):
        r, _ = referral_module
        r.record_referral(new_user_uid="u-a", referrer_code="u-ref")
        r.record_referral(new_user_uid="u-b", referrer_code="u-ref")
        r.record_referral(new_user_uid="u-c", referrer_code="someone-else")
        results = r.list_referrals_by("u-ref")
        assert len(results) == 2
        assert {e["referred"] for e in results} == {"u-a", "u-b"}

    def test_empty_when_log_missing(self, referral_module):
        r, _ = referral_module
        assert r.list_referrals_by("u-ref") == []

    def test_empty_referrer_returns_empty(self, referral_module):
        r, _ = referral_module
        assert r.list_referrals_by("") == []
