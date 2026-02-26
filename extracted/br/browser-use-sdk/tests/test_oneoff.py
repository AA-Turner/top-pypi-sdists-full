"""
One-time prod API tests -- broader coverage beyond the smoke tests.

Run: uv run python -m pytest tests/test_oneoff.py -v -s

Uses .env.prod (or .env fallback) for BROWSER_USE_API_KEY.
Hits the default production endpoint.
"""
from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import BaseModel

# ── Load env ────────────────────────────────────────────────────────────────

_root = Path(__file__).resolve().parent.parent.parent
_prod_env = _root / ".env.prod"
_fallback_env = _root / ".env"
_env_path = _prod_env if _prod_env.exists() else _fallback_env

_env: dict[str, str] = {}
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        eq = line.index("=")
        _env[line[:eq].strip()] = line[eq + 1 :].strip()

API_KEY = _env.get("BROWSER_USE_API_KEY", "")

pytestmark = [
    pytest.mark.prod,
    pytest.mark.skipif(not API_KEY, reason="No API key"),
]


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def v2():
    from browser_use_sdk import BrowserUse

    with BrowserUse(api_key=API_KEY) as c:
        yield c


@pytest.fixture(scope="module")
def v3():
    from browser_use_sdk.v3 import BrowserUse

    with BrowserUse(api_key=API_KEY) as c:
        yield c


# ── V2 Billing ──────────────────────────────────────────────────────────────

class TestBillingShape:
    def test_account_has_all_fields(self, v2):
        account = v2.billing.account()
        assert hasattr(account, "total_credits_balance_usd")
        assert hasattr(account, "rate_limit")
        assert hasattr(account, "project_id")
        assert isinstance(account.rate_limit, int)
        assert account.rate_limit > 0
        assert isinstance(account.total_credits_balance_usd, (int, float))
        print(f"  credits: ${account.total_credits_balance_usd}, rate limit: {account.rate_limit}")


# ── V2 Pagination ───────────────────────────────────────────────────────────

class TestPagination:
    def test_tasks_list_pagination(self, v2):
        listing = v2.tasks.list(page_size=3)
        assert hasattr(listing, "items")
        assert isinstance(listing.items, list)
        assert hasattr(listing, "total_items")
        assert isinstance(listing.total_items, int)
        assert hasattr(listing, "page_number")
        assert hasattr(listing, "page_size")
        assert listing.page_size <= 3
        print(f"  total tasks: {listing.total_items}, page items: {len(listing.items)}")

    def test_sessions_list_pagination(self, v2):
        listing = v2.sessions.list(page_size=3)
        assert hasattr(listing, "items")
        assert isinstance(listing.items, list)
        assert isinstance(listing.total_items, int)
        print(f"  total sessions: {listing.total_items}")


# ── V2 Profile Lifecycle ────────────────────────────────────────────────────

class TestProfileLifecycle:
    def test_full_crud_with_field_validation(self, v2):
        # Create
        profile = v2.profiles.create(name="OneOff Py Test")
        assert profile.id is not None
        pid = str(profile.id)

        try:
            # Get
            got = v2.profiles.get(pid)
            assert str(got.id) == pid

            # Update
            updated = v2.profiles.update(pid, name="OneOff Py Updated")
            assert str(updated.id) == pid

            # List — verify our profile shows up
            listing = v2.profiles.list(page_size=50)
            assert isinstance(listing.items, list)
            ids = [str(p.id) for p in listing.items]
            assert pid in ids, "Created profile should appear in list"
        finally:
            v2.profiles.delete(pid)


# ── V2 Session Lifecycle ────────────────────────────────────────────────────

class TestSessionLifecycle:
    def test_create_get_stop_delete(self, v2):
        session = v2.sessions.create()
        assert session.id is not None
        sid = str(session.id)

        try:
            got = v2.sessions.get(sid)
            assert str(got.id) == sid
            assert hasattr(got, "status")
        finally:
            try:
                v2.sessions.stop(sid)
            except Exception:
                pass
            try:
                v2.sessions.delete(sid)
            except Exception:
                pass


# ── V2 Task Lifecycle ───────────────────────────────────────────────────────

class TestTaskLifecycle:
    def test_create_status_stop(self, v2):
        task = v2.tasks.create("Go to example.com")
        assert task.id is not None
        tid = str(task.id)

        try:
            # Status
            status = v2.tasks.status(tid)
            assert str(status.id) == tid
            assert hasattr(status, "status")

            # Stop
            stopped = v2.tasks.stop(tid)
            assert str(stopped.id) == tid
        except Exception:
            try:
                v2.tasks.stop(tid)
            except Exception:
                pass


# ── V2 Run ──────────────────────────────────────────────────────────────────

class TestRunOutput:
    def test_run_returns_task_result_with_all_fields(self, v2):
        from browser_use_sdk import TaskResult

        result = v2.run("What is 2 + 2? Return just the number.")
        assert isinstance(result, TaskResult)
        assert isinstance(result.output, str)
        assert len(result.output) > 0
        assert result.id is not None
        assert result.status is not None
        assert hasattr(result, "steps")
        assert len(result.steps) >= 1
        print(f"  output: \"{result.output}\", steps: {len(result.steps)}")


class CapitalInfo(BaseModel):
    capital: str
    population: str


class TestStructuredOutput:
    def test_run_with_pydantic_schema(self, v2):
        from browser_use_sdk import TaskResult

        result = v2.run(
            "What is the capital of France and its approximate population? Return as JSON.",
            schema=CapitalInfo,
        )
        assert isinstance(result, TaskResult)
        assert isinstance(result.output, CapitalInfo)
        assert isinstance(result.output.capital, str)
        assert isinstance(result.output.population, str)
        assert "paris" in result.output.capital.lower()
        print(f"  capital: {result.output.capital}, population: {result.output.population}")


# ── V2 Streaming ────────────────────────────────────────────────────────────

class TestStreaming:
    def test_stream_yields_steps_with_all_fields(self, v2):
        from browser_use_sdk import TaskResult

        stream = v2.stream("Go to example.com and return the page title")
        step_count = 0
        for step in stream:
            assert hasattr(step, "number")
            assert isinstance(step.number, int)
            assert hasattr(step, "next_goal")
            assert isinstance(step.next_goal, str)
            assert hasattr(step, "url")
            assert isinstance(step.url, str)
            assert hasattr(step, "actions")
            assert isinstance(step.actions, list)
            step_count += 1
            if step_count > 30:
                break
        assert step_count >= 1, "Should yield at least 1 step"
        assert stream.result is not None
        assert isinstance(stream.result, TaskResult)
        assert isinstance(stream.result.output, str)
        print(f"  steps: {step_count}, output: \"{stream.result.output}\"")


# ── V2 Resource Lists ──────────────────────────────────────────────────────

class TestResourceLists:
    def test_browsers_list(self, v2):
        listing = v2.browsers.list(page_size=5)
        assert hasattr(listing, "items")
        assert isinstance(listing.items, list)
        assert isinstance(listing.total_items, int)

    def test_skills_list(self, v2):
        listing = v2.skills.list(page_size=5)
        assert hasattr(listing, "items")
        assert isinstance(listing.items, list)

    def test_marketplace_list(self, v2):
        listing = v2.marketplace.list(page_size=5)
        assert listing is not None


# ── V2 Error Handling ───────────────────────────────────────────────────────

class TestErrors:
    def test_404_on_invalid_task(self, v2):
        from browser_use_sdk._core.errors import BrowserUseError

        with pytest.raises(BrowserUseError) as exc_info:
            v2.tasks.get("00000000-0000-0000-0000-000000000000")
        err = exc_info.value
        assert err.status_code == 404
        assert len(err.message) > 0
        assert err.detail is not None

    def test_404_on_invalid_session(self, v2):
        from browser_use_sdk._core.errors import BrowserUseError

        with pytest.raises(BrowserUseError) as exc_info:
            v2.sessions.get("00000000-0000-0000-0000-000000000000")
        assert exc_info.value.status_code == 404

    def test_404_on_invalid_profile(self, v2):
        from browser_use_sdk._core.errors import BrowserUseError

        with pytest.raises(BrowserUseError) as exc_info:
            v2.profiles.get("00000000-0000-0000-0000-000000000000")
        assert exc_info.value.status_code == 404

    def test_auth_error_on_invalid_key(self):
        from browser_use_sdk import BrowserUse
        from browser_use_sdk._core.errors import BrowserUseError

        bad = BrowserUse(api_key="bu_invalid_key")
        with pytest.raises(BrowserUseError) as exc_info:
            bad.billing.account()
        assert exc_info.value.status_code in (401, 403, 404)


# ── V3 Tests ────────────────────────────────────────────────────────────────

class TestV3Sessions:
    def test_list_sessions(self, v3):
        listing = v3.sessions.list(page_size=5)
        assert hasattr(listing, "sessions")
        assert isinstance(listing.sessions, list)
        print(f"  sessions count: {len(listing.sessions)}")

    def test_run_returns_output(self, v3):
        result = v3.run("What is 3 + 5? Return just the number.")
        assert isinstance(result.output, str)
        assert len(result.output) > 0
        assert result.id is not None
        print(f"  output: \"{result.output}\"")


class ColorInfo(BaseModel):
    color: str
    hex: str


class TestV3StructuredOutput:
    def test_run_with_schema(self, v3):
        result = v3.run(
            "What is the hex color code for red? Return as JSON with color name and hex code.",
            schema=ColorInfo,
        )
        assert isinstance(result.output, ColorInfo)
        assert isinstance(result.output.color, str)
        assert isinstance(result.output.hex, str)
        print(f"  color: {result.output.color}, hex: {result.output.hex}")
