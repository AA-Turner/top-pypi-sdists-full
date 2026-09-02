"""The startup banner must not print the database password.

It did. On a deployed service stdout is the platform's log stream, so every
restart wrote the credential somewhere retained and broadly readable. These
pin the fix, because the failure is invisible in normal use -- the banner
looks fine unless you read it closely enough to notice what is between the
`//` and the `@`.
"""

import pytest

from src.banner import _safe_database_target

SECRET = "hunter2SUPERSECRET"


@pytest.fixture(autouse=True)
def _clear(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)


class TestTheCredentialNeverAppears:
    def test_password_is_absent(self, monkeypatch):
        monkeypatch.setenv(
            "DATABASE_URL",
            f"postgresql://someuser:{SECRET}@db.example.com:6543/postgres",
        )
        assert SECRET not in _safe_database_target()

    def test_username_is_absent_too(self, monkeypatch):
        """The user half is not a secret, but it names the tenant on Supabase's
        pooler (`postgres.<project-ref>`), so it is not something to log either."""
        monkeypatch.setenv(
            "DATABASE_URL",
            f"postgresql://postgres.abcproject:{SECRET}@aws.pooler.supabase.com:5432/postgres",
        )
        out = _safe_database_target()
        assert SECRET not in out
        assert "abcproject" not in out

    def test_a_password_containing_url_characters_still_does_not_leak(
        self, monkeypatch
    ):
        """A `@` or `/` in the password is exactly where naive splitting breaks."""
        nasty = "p@ss/word:with@symbols"
        monkeypatch.setenv(
            "DATABASE_URL",
            f"postgresql://u:{nasty}@host.example.com:5432/db",
        )
        out = _safe_database_target()
        assert "symbols" not in out
        assert "p@ss" not in out


class TestItStillSaysSomethingUseful:
    def test_host_port_and_database_survive(self, monkeypatch):
        monkeypatch.setenv(
            "DATABASE_URL", f"postgresql://u:{SECRET}@db.example.com:6543/postgres"
        )
        out = _safe_database_target()
        assert "db.example.com:6543" in out
        assert out.endswith("/postgres")

    def test_sqlite_is_passed_through(self, monkeypatch):
        """No host, no credential -- and the path is the useful part."""
        monkeypatch.setenv("DATABASE_URL", "sqlite:///./innoday.db")
        assert _safe_database_target() == "sqlite:///./innoday.db"

    def test_unset_falls_back_to_the_sqlite_default(self):
        assert _safe_database_target() == "sqlite:///./innoday.db"
