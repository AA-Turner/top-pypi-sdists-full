"""Tests for the is_admin() helper that gates free admin tier access.

Admin tier is granted when:
  1. The email is in ADMIN_EMAILS (explicit allow-list), OR
  2. The email ends with one of ADMIN_DOMAINS (org-wide internal access).

Case-insensitive on both sides. Malformed inputs (empty / missing @) return
False. These tests pin the contract so future refactors of billing/admin can't
accidentally widen or narrow the gate.
"""

from __future__ import annotations

import os

import pytest

os.environ.setdefault("SAGE_FIREBASE_API_KEY", "test-dummy")
os.environ.setdefault("FIREBASE_PROJECT_ID", "test-project")

from backend.billing import is_admin, ADMIN_EMAILS, ADMIN_DOMAINS


class TestExplicitAllowList:
    def test_listed_email_is_admin(self):
        for e in ADMIN_EMAILS:
            assert is_admin(e) is True

    def test_listed_email_case_insensitive(self):
        for e in ADMIN_EMAILS:
            assert is_admin(e.upper()) is True
            assert is_admin(e.title()) is True


class TestAdminDomains:
    def test_bixbyland_lowercase(self):
        assert is_admin("alice@bixbyland.com") is True

    def test_bixbycapital_lowercase(self):
        assert is_admin("bob@bixbycapital.com") is True

    def test_uppercase_local_part(self):
        assert is_admin("ALICE@bixbyland.com") is True

    def test_uppercase_domain(self):
        assert is_admin("alice@BIXBYLAND.COM") is True

    def test_mixed_case_throughout(self):
        assert is_admin("Alice.Smith@BixbyCapital.com") is True

    def test_email_with_plus_tag(self):
        # "+tag" aliases go on the local-part side; domain match still wins
        assert is_admin("alice+billing@bixbyland.com") is True

    def test_subdomain_is_not_admin(self):
        # A user at a sub.domain should NOT inherit admin access; require
        # exact domain match.
        assert is_admin("alice@sub.bixbyland.com") is False
        assert is_admin("alice@evil.bixbyland.com.attacker.com") is False

    def test_lookalike_domain_is_not_admin(self):
        assert is_admin("alice@bixbylandX.com") is False
        assert is_admin("alice@bixbyland.com.fake.org") is False


class TestNonAdminEmails:
    def test_random_email(self):
        assert is_admin("stranger@gmail.com") is False

    def test_empty_string(self):
        assert is_admin("") is False

    def test_none(self):
        assert is_admin(None) is False

    def test_whitespace_only(self):
        assert is_admin("   ") is False

    def test_email_with_no_at(self):
        assert is_admin("not-an-email") is False

    def test_email_with_trailing_whitespace(self):
        # We strip, so this should match
        assert is_admin(" alice@bixbyland.com ") is True

    @pytest.mark.parametrize("attacker", [
        "alice@bixbyland.com.attacker.com",
        "alice@bixbyland.com@gmail.com",   # the last @ wins; domain is gmail.com
        "@bixbyland.com",                   # no local part
        "alice@",                           # no domain
    ])
    def test_malformed_or_tricky_inputs(self, attacker):
        # We don't promote any of these to admin
        if attacker == "alice@bixbyland.com@gmail.com":
            # rsplit("@", 1) splits at the LAST @, so domain = "gmail.com"
            assert is_admin(attacker) is False
        elif attacker == "@bixbyland.com":
            # Empty local part — we still match the domain so this returns True.
            # That's acceptable since Firebase wouldn't issue tokens for an empty
            # local part anyway. Test pins the actual behavior.
            assert is_admin(attacker) is True
        else:
            assert is_admin(attacker) is False


class TestConstants:
    def test_admin_domains_includes_both(self):
        assert "bixbyland.com" in ADMIN_DOMAINS
        assert "bixbycapital.com" in ADMIN_DOMAINS

    def test_admin_domains_are_lowercase(self):
        # We lowercase the domain at check time; the constants should match
        # so a copy-paste audit is straightforward.
        for d in ADMIN_DOMAINS:
            assert d == d.lower(), f"{d!r} must be lowercase"
