import asyncio
import os
import pytest
from unittest.mock import AsyncMock, patch
from flowtask.tests import BaseTestCase, PandasTestCase
from flowtask.exceptions import ComponentError


@pytest.fixture(autouse=True, scope="session")
def component():
    component = "OdooInjector"
    yield component


pytestmark = pytest.mark.asyncio


# ---------------------------------------------------------------------------
# Unit tests — all auth paths (no live Odoo connection required)
# ---------------------------------------------------------------------------

class TestOdooInjectorAuthAPIKeyOnly(BaseTestCase):
    """APIKEY-only credentials → api-key header used."""

    arguments: dict = {
        "credentials": {
            "APIKEY": "test_api_key",
            "HOST": "http://localhost",
            "PORT": "8069",
            "INJECTOR_URL": "/web/dataset/call_kw",
        },
        "model": "res.users",
        "data": [{"name": "Test User", "login": "test@test.com"}],
    }
    expected_result = True

    async def test_auth_header(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            await self.component.start()
            assert self.component.headers == {"api-key": "test_api_key"}

    async def test_start(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            result = await self.component.start()
            assert result is True

    async def test_run(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            await self.component.start()
            result = await self.component.run()
            assert result is True


class TestOdooInjectorAuthBearerOnly(BaseTestCase):
    """BEARER_TOKEN-only credentials → Authorization Bearer header used."""

    arguments: dict = {
        "credentials": {
            "BEARER_TOKEN": "test_bearer_token",
            "HOST": "http://localhost",
            "PORT": "8069",
            "INJECTOR_URL": "/web/dataset/call_kw",
        },
        "model": "res.users",
        "data": [{"name": "Test User", "login": "test@test.com"}],
    }
    expected_result = True

    async def test_auth_header(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            await self.component.start()
            assert self.component.headers == {"Authorization": "Bearer test_bearer_token"}

    async def test_start(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            result = await self.component.start()
            assert result is True

    async def test_run(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            await self.component.start()
            result = await self.component.run()
            assert result is True


class TestOdooInjectorAuthBothPresent(BaseTestCase):
    """Both APIKEY and BEARER_TOKEN present → APIKEY wins."""

    arguments: dict = {
        "credentials": {
            "APIKEY": "test_api_key",
            "BEARER_TOKEN": "test_bearer_token",
            "HOST": "http://localhost",
            "PORT": "8069",
            "INJECTOR_URL": "/web/dataset/call_kw",
        },
        "model": "res.users",
        "data": [{"name": "Test User", "login": "test@test.com"}],
    }
    expected_result = True

    async def test_auth_header_apikey_wins(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            await self.component.start()
            assert self.component.headers == {"api-key": "test_api_key"}
            assert "Authorization" not in self.component.headers

    async def test_start(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            result = await self.component.start()
            assert result is True

    async def test_run(self):
        with patch.object(
            self.component,
            "session",
            new=AsyncMock(return_value=({"ids": [1]}, None)),
        ):
            await self.component.start()
            result = await self.component.run()
            assert result is True


class TestOdooInjectorAuthNeitherPresent(BaseTestCase):
    """Neither APIKEY nor BEARER_TOKEN → ComponentError raised in start()."""

    arguments: dict = {
        "credentials": {
            "HOST": "http://localhost",
            "PORT": "8069",
            "INJECTOR_URL": "/web/dataset/call_kw",
        },
        "model": "res.users",
        "data": [{"name": "Test User", "login": "test@test.com"}],
    }
    expected_result = True

    async def test_raises_component_error(self):
        with pytest.raises(ComponentError, match="Either APIKEY or BEARER_TOKEN"):
            await self.component.start()

    async def test_start(self):
        # Override: this test class expects start() to raise ComponentError
        with pytest.raises(ComponentError, match="Either APIKEY or BEARER_TOKEN"):
            await self.component.start()

    async def test_run(self):
        # Override: skip run — start() never completes for this case
        with pytest.raises(ComponentError):
            await self.component.start()

    async def test_initialize(self, component):
        assert self.name == component

    async def test_close(self):
        # Nothing to close since start() raises before any network activity
        result = await self.component.close()
        assert result is True


# ---------------------------------------------------------------------------
# Integration tests — Assurant Odoo v18+ (skipped if env vars absent)
# ---------------------------------------------------------------------------

_ASSURANT_VARS = (
    "ODOO_ASSURANT_BEARER_TOKEN",
    "ODOO_ASSURANT_HOST",
    "ODOO_ASSURANT_PORT",
    "ODOO_INJECTOR_URL",
)
_assurant_missing = [v for v in _ASSURANT_VARS if not os.environ.get(v)]
_skip_assurant = pytest.mark.skipif(
    bool(_assurant_missing),
    reason=f"Assurant env vars not set: {', '.join(_assurant_missing)}",
)


@_skip_assurant
class TestOdooInjectCreateRecordsWithBearerToken(BaseTestCase):
    """E2E injection against Assurant using Bearer Token (list[dict] input path)."""

    arguments: dict = {
        "credentials": {
            "BEARER_TOKEN": "ODOO_ASSURANT_BEARER_TOKEN",
            "HOST": "ODOO_ASSURANT_HOST",
            "PORT": "ODOO_ASSURANT_PORT",
            "INJECTOR_URL": "ODOO_INJECTOR_URL",
        },
        "model": "res.users",
        "data": [
            {
                "name": "Test User Bearer Token",
                "login": "test_user_bearer@test.com",
                "groups_id/id": "base.group_user",
            },
            {
                "name": "Test User Bearer Token 2",
                "login": "test_user_bearer2@test.com",
                "groups_id/id": "base.group_user",
            },
        ],
    }

    expected_result = True


@_skip_assurant
class TestOdooInjectCreateRecordsFromPreviousDFWithBearerToken(PandasTestCase):
    """E2E injection against Assurant using Bearer Token (DataFrame via pipeline)."""

    file_test = "odoo_users.csv"
    renamed_cols = None

    arguments: dict = {
        "credentials": {
            "BEARER_TOKEN": "ODOO_ASSURANT_BEARER_TOKEN",
            "HOST": "ODOO_ASSURANT_HOST",
            "PORT": "ODOO_ASSURANT_PORT",
            "INJECTOR_URL": "ODOO_INJECTOR_URL",
        },
        "model": "res.users",
        # data comes from the previous step (CSV loaded by PandasTestCase)
    }

    expected_result = True


# ---------------------------------------------------------------------------
# Original APIKEY integration tests — preserved for future restoration
# ---------------------------------------------------------------------------

# TODO: re-enable when Odoo v16 test environment is available.
# class TestOdooInjectCreateRecords(BaseTestCase): ...
# class TestOdooInjectCreateRecordsFromPreviousDF(PandasTestCase): ...


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
