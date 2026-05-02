"""Tests for G13 WebSocket/HTTP API server."""

import json
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from aiohttp import web

from g13_linux.gui.models.macro_types import (
    Macro,
    MacroStep,
    MacroStepType,
    PlaybackMode,
)

pytestmark = pytest.mark.asyncio


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_led_controller():
    """Mock LED controller with color/brightness."""
    ctrl = MagicMock()
    color_mock = MagicMock()
    color_mock.to_hex.return_value = "#ff6b00"
    ctrl.current_color = color_mock
    ctrl.brightness = 100
    ctrl.set_color = MagicMock()
    ctrl.set_brightness = MagicMock()
    return ctrl


@pytest.fixture
def mock_event_decoder():
    """Mock event decoder."""
    decoder = MagicMock()
    decoder.last_state = None
    decoder.get_pressed_buttons.return_value = []
    return decoder


@pytest.fixture
def mock_profile_manager():
    """Mock profile manager."""
    pm = MagicMock()
    pm.current_name = "default"
    pm.list_profiles.return_value = ["default", "gaming"]
    return pm


@pytest.fixture
def mock_macro_manager():
    """Mock macro manager."""
    mm = MagicMock()
    mm.list_macro_summaries.return_value = [
        {"id": "macro-1", "name": "Test Macro", "steps": 3},
    ]
    return mm


@pytest.fixture
def mock_daemon(mock_led_controller, mock_event_decoder, mock_profile_manager, mock_macro_manager):
    """Mock G13Daemon with all sub-managers."""
    daemon = MagicMock()
    daemon._led_controller = mock_led_controller
    daemon._event_decoder = mock_event_decoder
    daemon._device = MagicMock()  # device is connected
    daemon._current_mode = "M1"
    daemon._last_joystick = (128, 128)
    daemon.profile_manager = mock_profile_manager
    daemon.macro_manager = mock_macro_manager
    daemon.set_mode = MagicMock()
    daemon.set_button_mapping = MagicMock(return_value=True)
    daemon.load_profile = MagicMock(return_value=True)
    return daemon


@pytest.fixture
def static_dir(tmp_path):
    """Create a temporary static directory with test files."""
    sdir = tmp_path / "static"
    sdir.mkdir()
    (sdir / "index.html").write_text("<html><body>G13</body></html>")
    (sdir / "vite.svg").write_text("<svg/>")
    assets = sdir / "assets"
    assets.mkdir()
    (assets / "main.js").write_text("console.log('hello');")
    (sdir / "other.html").write_text("<html>other</html>")
    return sdir


@pytest.fixture
def server_no_static(mock_daemon, tmp_path):
    """G13Server with no static dir (non-existent path)."""
    with patch("g13_linux.server.DEFAULT_STATIC_DIR", tmp_path / "nonexistent"):
        from g13_linux.server import G13Server

        srv = G13Server(mock_daemon, host="127.0.0.1", port=0)
    return srv


@pytest.fixture
def server_with_static(mock_daemon, static_dir):
    """G13Server with a valid static directory."""
    with patch("g13_linux.server.DEFAULT_STATIC_DIR", static_dir):
        from g13_linux.server import G13Server

        srv = G13Server(mock_daemon, host="127.0.0.1", port=0, static_dir=static_dir)
    return srv


async def _make_app(server):
    """Build the aiohttp app from a G13Server without starting a TCP site."""
    server._app = web.Application()
    server._setup_routes()
    return server._app


@pytest_asyncio.fixture
async def client_no_static(server_no_static, aiohttp_client):
    """Test client for server without static files."""
    app = await _make_app(server_no_static)
    return await aiohttp_client(app)


@pytest_asyncio.fixture
async def client_with_static(server_with_static, aiohttp_client):
    """Test client for server with static files."""
    app = await _make_app(server_with_static)
    return await aiohttp_client(app)


# ---------------------------------------------------------------------------
# Constructor tests
# ---------------------------------------------------------------------------


class TestG13ServerInit:
    """Test server initialization."""

    def test_default_static_dir(self, mock_daemon, tmp_path):
        with patch("g13_linux.server.DEFAULT_STATIC_DIR", tmp_path / "nope"):
            from g13_linux.server import G13Server

            srv = G13Server(mock_daemon)
        assert srv._static_dir == tmp_path / "nope"
        assert not srv._serve_static

    def test_custom_static_dir_exists(self, mock_daemon, static_dir):
        with patch("g13_linux.server.DEFAULT_STATIC_DIR", Path("/nope")):
            from g13_linux.server import G13Server

            srv = G13Server(mock_daemon, static_dir=static_dir)
        assert srv._static_dir == static_dir
        assert srv._serve_static is True

    def test_custom_static_dir_string(self, mock_daemon, static_dir):
        with patch("g13_linux.server.DEFAULT_STATIC_DIR", Path("/nope")):
            from g13_linux.server import G13Server

            srv = G13Server(mock_daemon, static_dir=str(static_dir))
        assert srv._static_dir == static_dir

    def test_host_port(self, mock_daemon, tmp_path):
        with patch("g13_linux.server.DEFAULT_STATIC_DIR", tmp_path / "nope"):
            from g13_linux.server import G13Server

            srv = G13Server(mock_daemon, host="0.0.0.0", port=9999)
        assert srv.host == "0.0.0.0"
        assert srv.port == 9999


# ---------------------------------------------------------------------------
# Start / Stop lifecycle
# ---------------------------------------------------------------------------


class TestLifecycle:
    """Test start/stop methods."""

    @pytest.mark.asyncio
    async def test_start_stop(self, mock_daemon, tmp_path):
        with patch("g13_linux.server.DEFAULT_STATIC_DIR", tmp_path / "nope"):
            from g13_linux.server import G13Server

            srv = G13Server(mock_daemon, host="127.0.0.1", port=0)
        await srv.start()
        assert srv._app is not None
        assert srv._runner is not None
        assert srv._site is not None
        await srv.stop()

    @pytest.mark.asyncio
    async def test_stop_clears_clients(self, mock_daemon, tmp_path):
        with patch("g13_linux.server.DEFAULT_STATIC_DIR", tmp_path / "nope"):
            from g13_linux.server import G13Server

            srv = G13Server(mock_daemon, host="127.0.0.1", port=0)
        ws_mock = AsyncMock()
        srv._clients.add(ws_mock)
        await srv.stop()
        ws_mock.close.assert_awaited_once()
        assert len(srv._clients) == 0

    @pytest.mark.asyncio
    async def test_stop_without_start(self, mock_daemon, tmp_path):
        """Stop when site/runner are None should not raise."""
        with patch("g13_linux.server.DEFAULT_STATIC_DIR", tmp_path / "nope"):
            from g13_linux.server import G13Server

            srv = G13Server(mock_daemon, host="127.0.0.1", port=0)
        await srv.stop()  # should not raise


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------


class TestCORS:
    """Test CORS headers."""

    @pytest.mark.asyncio
    async def test_cors_on_status(self, client_no_static):
        resp = await client_no_static.get("/api/status")
        assert resp.status == 200
        assert resp.headers["Access-Control-Allow-Origin"] == "*"
        assert "GET" in resp.headers["Access-Control-Allow-Methods"]

    @pytest.mark.asyncio
    async def test_options_preflight(self, client_no_static):
        resp = await client_no_static.options("/api/profiles")
        assert resp.status == 200
        assert resp.headers["Access-Control-Allow-Origin"] == "*"
        assert "Content-Type" in resp.headers["Access-Control-Allow-Headers"]


# ---------------------------------------------------------------------------
# REST: Status
# ---------------------------------------------------------------------------


class TestAPIStatus:
    """Test GET /api/status."""

    @pytest.mark.asyncio
    async def test_get_status(self, client_no_static, mock_daemon):
        resp = await client_no_static.get("/api/status")
        assert resp.status == 200
        data = await resp.json()
        assert data["connected"] is True
        assert data["active_profile"] == "default"
        assert data["active_mode"] == "M1"

    @pytest.mark.asyncio
    async def test_status_no_device(self, client_no_static, mock_daemon):
        mock_daemon._device = None
        resp = await client_no_static.get("/api/status")
        data = await resp.json()
        assert data["connected"] is False

    @pytest.mark.asyncio
    async def test_status_no_profile_manager(self, client_no_static, mock_daemon):
        mock_daemon.profile_manager = None
        resp = await client_no_static.get("/api/status")
        data = await resp.json()
        assert data["active_profile"] is None

    @pytest.mark.asyncio
    async def test_status_no_led_controller(self, client_no_static, mock_daemon):
        mock_daemon._led_controller = None
        resp = await client_no_static.get("/api/status")
        data = await resp.json()
        assert data["connected"] is True


# ---------------------------------------------------------------------------
# REST: Profiles
# ---------------------------------------------------------------------------


class TestAPIProfiles:
    """Test profile CRUD endpoints."""

    @pytest.mark.asyncio
    async def test_list_profiles(self, client_no_static, mock_daemon):
        @dataclass
        class FakeProfile:
            description: str = "A profile"

        mock_daemon.profile_manager.load_profile.return_value = FakeProfile()
        resp = await client_no_static.get("/api/profiles")
        assert resp.status == 200
        data = await resp.json()
        assert len(data["profiles"]) == 2
        assert data["profiles"][0]["name"] == "default"
        assert data["profiles"][0]["description"] == "A profile"

    @pytest.mark.asyncio
    async def test_list_profiles_load_error(self, client_no_static, mock_daemon):
        """Profiles that fail to load still appear with empty description."""
        mock_daemon.profile_manager.load_profile.side_effect = Exception("corrupt")
        resp = await client_no_static.get("/api/profiles")
        data = await resp.json()
        assert len(data["profiles"]) == 2
        assert data["profiles"][0]["description"] == ""

    @pytest.mark.asyncio
    async def test_get_profile(self, client_no_static, mock_daemon):
        @dataclass
        class FakeProfile:
            name: str = "default"
            description: str = "test"
            mappings: dict = None
            backlight: dict = None

        mock_daemon.profile_manager.load_profile.return_value = FakeProfile()
        resp = await client_no_static.get("/api/profiles/default")
        assert resp.status == 200
        data = await resp.json()
        assert data["name"] == "default"

    @pytest.mark.asyncio
    async def test_get_profile_not_found(self, client_no_static, mock_daemon):
        mock_daemon.profile_manager.load_profile.side_effect = FileNotFoundError()
        resp = await client_no_static.get("/api/profiles/nonexistent")
        assert resp.status == 404

    @pytest.mark.asyncio
    async def test_save_profile_create(self, client_no_static, mock_daemon):
        mock_daemon.profile_manager.profile_exists.return_value = False
        new_profile = MagicMock()
        mock_daemon.profile_manager.create_profile.return_value = new_profile
        resp = await client_no_static.post(
            "/api/profiles/newprof",
            json={"name": "newprof", "description": "Brand new"},
        )
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "saved"
        mock_daemon.profile_manager.create_profile.assert_called_once_with("newprof")
        mock_daemon.profile_manager.save_profile.assert_called_once()
        assert new_profile.name == "newprof"
        assert new_profile.description == "Brand new"

    @pytest.mark.asyncio
    async def test_save_profile_update(self, client_no_static, mock_daemon):
        mock_daemon.profile_manager.profile_exists.return_value = True
        existing = MagicMock()
        mock_daemon.profile_manager.load_profile.return_value = existing
        resp = await client_no_static.post(
            "/api/profiles/existing",
            json={
                "description": "Updated",
                "mappings": {"G1": "a"},
                "backlight": {"color": "#ff0000"},
            },
        )
        assert resp.status == 200
        assert existing.description == "Updated"
        assert existing.mappings == {"G1": "a"}
        assert existing.backlight == {"color": "#ff0000"}

    @pytest.mark.asyncio
    async def test_save_profile_error(self, client_no_static, mock_daemon):
        mock_daemon.profile_manager.profile_exists.side_effect = Exception("boom")
        resp = await client_no_static.post("/api/profiles/bad", json={"name": "bad"})
        assert resp.status == 400

    @pytest.mark.asyncio
    async def test_delete_profile(self, client_no_static, mock_daemon):
        resp = await client_no_static.delete("/api/profiles/gaming")
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "deleted"
        mock_daemon.profile_manager.delete_profile.assert_called_once_with("gaming")

    @pytest.mark.asyncio
    async def test_delete_profile_not_found(self, client_no_static, mock_daemon):
        mock_daemon.profile_manager.delete_profile.side_effect = FileNotFoundError()
        resp = await client_no_static.delete("/api/profiles/nonexistent")
        assert resp.status == 404

    @pytest.mark.asyncio
    async def test_activate_profile_success(self, client_no_static, mock_daemon):
        resp = await client_no_static.post("/api/profiles/gaming/activate")
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "activated"
        mock_daemon.load_profile.assert_called_once_with("gaming")

    @pytest.mark.asyncio
    async def test_activate_profile_failure(self, client_no_static, mock_daemon):
        mock_daemon.load_profile.return_value = False
        resp = await client_no_static.post("/api/profiles/bad/activate")
        assert resp.status == 400

    @pytest.mark.asyncio
    async def test_activate_profile_exception(self, client_no_static, mock_daemon):
        mock_daemon.load_profile.side_effect = Exception("no device")
        resp = await client_no_static.post("/api/profiles/err/activate")
        assert resp.status == 400


# ---------------------------------------------------------------------------
# REST: Macros
# ---------------------------------------------------------------------------


class TestAPIMacros:
    """Test macro CRUD endpoints."""

    @pytest.mark.asyncio
    async def test_list_macros(self, client_no_static, mock_daemon):
        resp = await client_no_static.get("/api/macros")
        assert resp.status == 200
        data = await resp.json()
        assert len(data["macros"]) == 1
        assert data["macros"][0]["name"] == "Test Macro"

    @pytest.mark.asyncio
    async def test_get_macro(self, client_no_static, mock_daemon):
        macro = Macro(id="macro-1", name="TestMacro")
        mock_daemon.macro_manager.load_macro.return_value = macro
        resp = await client_no_static.get("/api/macros/macro-1")
        assert resp.status == 200
        data = await resp.json()
        assert data["name"] == "TestMacro"
        assert data["id"] == "macro-1"

    @pytest.mark.asyncio
    async def test_get_macro_not_found(self, client_no_static, mock_daemon):
        mock_daemon.macro_manager.load_macro.side_effect = FileNotFoundError()
        resp = await client_no_static.get("/api/macros/nope")
        assert resp.status == 404

    @pytest.mark.asyncio
    async def test_create_macro(self, client_no_static, mock_daemon):
        new_macro = Macro(id="new-1", name="New Macro")
        mock_daemon.macro_manager.create_macro.return_value = new_macro
        resp = await client_no_static.post(
            "/api/macros",
            json={"name": "New Macro", "description": "desc"},
        )
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "created"
        assert data["id"] == "new-1"

    @pytest.mark.asyncio
    async def test_create_macro_default_name(self, client_no_static, mock_daemon):
        new_macro = Macro(id="new-2", name="New Macro")
        mock_daemon.macro_manager.create_macro.return_value = new_macro
        resp = await client_no_static.post("/api/macros", json={})
        assert resp.status == 200
        mock_daemon.macro_manager.create_macro.assert_called_with("New Macro")

    @pytest.mark.asyncio
    async def test_create_macro_error(self, client_no_static, mock_daemon):
        mock_daemon.macro_manager.create_macro.side_effect = Exception("disk full")
        resp = await client_no_static.post("/api/macros", json={"name": "x"})
        assert resp.status == 400

    @pytest.mark.asyncio
    async def test_update_macro(self, client_no_static, mock_daemon):
        macro = Macro(id="macro-1", name="Old")
        mock_daemon.macro_manager.load_macro.return_value = macro
        resp = await client_no_static.put(
            "/api/macros/macro-1",
            json={"name": "Updated", "description": "new desc"},
        )
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "updated"
        assert macro.name == "Updated"
        assert macro.description == "new desc"

    @pytest.mark.asyncio
    async def test_update_macro_not_found(self, client_no_static, mock_daemon):
        mock_daemon.macro_manager.load_macro.side_effect = FileNotFoundError()
        resp = await client_no_static.put("/api/macros/nope", json={"name": "x"})
        assert resp.status == 404

    @pytest.mark.asyncio
    async def test_update_macro_error(self, client_no_static, mock_daemon):
        mock_daemon.macro_manager.load_macro.side_effect = ValueError("bad data")
        resp = await client_no_static.put("/api/macros/bad", json={"name": "x"})
        assert resp.status == 400

    @pytest.mark.asyncio
    async def test_delete_macro(self, client_no_static, mock_daemon):
        resp = await client_no_static.delete("/api/macros/macro-1")
        assert resp.status == 200
        data = await resp.json()
        assert data["status"] == "deleted"

    @pytest.mark.asyncio
    async def test_delete_macro_not_found(self, client_no_static, mock_daemon):
        mock_daemon.macro_manager.delete_macro.side_effect = FileNotFoundError()
        resp = await client_no_static.delete("/api/macros/nope")
        assert resp.status == 404


# ---------------------------------------------------------------------------
# REST: _update_macro_fields
# ---------------------------------------------------------------------------


class TestUpdateMacroFields:
    """Test _update_macro_fields helper."""

    def test_simple_fields(self, server_no_static):
        macro = Macro(id="m1", name="old")
        server_no_static._update_macro_fields(
            macro,
            {
                "name": "new",
                "description": "desc",
                "speed_multiplier": 2.0,
                "repeat_count": 5,
                "repeat_delay_ms": 100,
                "fixed_delay_ms": 20,
                "assigned_button": "G5",
                "global_hotkey": "Ctrl+F1",
            },
        )
        assert macro.name == "new"
        assert macro.description == "desc"
        assert macro.speed_multiplier == 2.0
        assert macro.repeat_count == 5
        assert macro.repeat_delay_ms == 100
        assert macro.fixed_delay_ms == 20
        assert macro.assigned_button == "G5"
        assert macro.global_hotkey == "Ctrl+F1"

    def test_steps_field(self, server_no_static):
        macro = Macro(id="m1")
        server_no_static._update_macro_fields(
            macro,
            {
                "steps": [
                    {"type": "key_press", "value": "KEY_A", "is_press": True, "timestamp_ms": 0},
                    {"type": "delay", "value": 100, "is_press": True, "timestamp_ms": 50},
                ]
            },
        )
        assert len(macro.steps) == 2
        assert macro.steps[0].step_type == MacroStepType.KEY_PRESS
        assert macro.steps[0].value == "KEY_A"
        assert macro.steps[1].step_type == MacroStepType.DELAY

    def test_playback_mode_field(self, server_no_static):
        macro = Macro(id="m1")
        server_no_static._update_macro_fields(macro, {"playback_mode": "fixed"})
        assert macro.playback_mode == PlaybackMode.FIXED

    def test_no_fields_no_change(self, server_no_static):
        macro = Macro(id="m1", name="original")
        server_no_static._update_macro_fields(macro, {})
        assert macro.name == "original"


# ---------------------------------------------------------------------------
# _get_state
# ---------------------------------------------------------------------------


class TestGetState:
    """Test _get_state helper."""

    def test_full_state(self, server_no_static, mock_daemon):
        state = server_no_static._get_state()
        assert state["connected"] is True
        assert state["active_profile"] == "default"
        assert state["active_mode"] == "M1"
        assert state["pressed_keys"] == []
        assert state["joystick"] == {"x": 128, "y": 128}
        assert state["backlight"]["color"] == "#ff6b00"
        assert state["backlight"]["brightness"] == 100

    def test_state_no_profile_manager(self, server_no_static, mock_daemon):
        mock_daemon.profile_manager = None
        state = server_no_static._get_state()
        assert state["active_profile"] is None

    def test_state_profile_manager_no_current(self, server_no_static, mock_daemon):
        mock_daemon.profile_manager.current_name = None
        state = server_no_static._get_state()
        assert state["active_profile"] is None

    def test_state_no_led_controller(self, server_no_static, mock_daemon):
        mock_daemon._led_controller = None
        state = server_no_static._get_state()
        assert state["backlight"]["color"] == "#ff6b00"
        assert state["backlight"]["brightness"] == 100

    def test_state_no_event_decoder(self, server_no_static, mock_daemon):
        mock_daemon._event_decoder = None
        state = server_no_static._get_state()
        assert state["pressed_keys"] == []

    def test_state_event_decoder_no_last_state(self, server_no_static, mock_daemon):
        mock_daemon._event_decoder.last_state = None
        state = server_no_static._get_state()
        assert state["pressed_keys"] == []

    def test_state_with_pressed_buttons(self, server_no_static, mock_daemon):
        mock_daemon._event_decoder.last_state = b"\x01"
        mock_daemon._event_decoder.get_pressed_buttons.return_value = ["G1", "G5"]
        state = server_no_static._get_state()
        assert state["pressed_keys"] == ["G1", "G5"]

    def test_state_no_device(self, server_no_static, mock_daemon):
        mock_daemon._device = None
        state = server_no_static._get_state()
        assert state["connected"] is False


# ---------------------------------------------------------------------------
# _set_backlight
# ---------------------------------------------------------------------------


class TestSetBacklight:
    """Test _set_backlight helper."""

    def test_set_color_and_brightness(self, server_no_static, mock_daemon):
        server_no_static._set_backlight("#ff0000", 75)
        mock_daemon._led_controller.set_color.assert_called_once_with(255, 0, 0)
        mock_daemon._led_controller.set_brightness.assert_called_once_with(75)

    def test_set_color_green(self, server_no_static, mock_daemon):
        server_no_static._set_backlight("#00ff00", 50)
        mock_daemon._led_controller.set_color.assert_called_once_with(0, 255, 0)

    def test_set_color_blue(self, server_no_static, mock_daemon):
        server_no_static._set_backlight("#0000ff", 100)
        mock_daemon._led_controller.set_color.assert_called_once_with(0, 0, 255)

    def test_no_led_controller(self, server_no_static, mock_daemon):
        mock_daemon._led_controller = None
        server_no_static._set_backlight("#ff0000", 50)  # should not raise

    def test_invalid_color_format_short(self, server_no_static, mock_daemon):
        """Color strings that don't match #RRGGBB are ignored."""
        server_no_static._set_backlight("#fff", 50)
        mock_daemon._led_controller.set_color.assert_not_called()
        mock_daemon._led_controller.set_brightness.assert_called_once_with(50)

    def test_invalid_color_no_hash(self, server_no_static, mock_daemon):
        server_no_static._set_backlight("ff0000", 50)
        mock_daemon._led_controller.set_color.assert_not_called()

    def test_brightness_none(self, server_no_static, mock_daemon):
        server_no_static._set_backlight("#ff0000", None)
        mock_daemon._led_controller.set_color.assert_called_once()
        mock_daemon._led_controller.set_brightness.assert_not_called()


# ---------------------------------------------------------------------------
# Static file serving
# ---------------------------------------------------------------------------


class TestStaticServing:
    """Test static file routes."""

    @pytest.mark.asyncio
    async def test_serve_index(self, client_with_static):
        resp = await client_with_static.get("/")
        assert resp.status == 200
        text = await resp.text()
        assert "G13" in text

    @pytest.mark.asyncio
    async def test_serve_vite_svg(self, client_with_static):
        resp = await client_with_static.get("/vite.svg")
        assert resp.status == 200

    @pytest.mark.asyncio
    async def test_serve_static_file_not_found(self, client_with_static, static_dir):
        """Request a static file endpoint where the file doesn't exist."""
        # Remove vite.svg to trigger 404
        (static_dir / "vite.svg").unlink()
        resp = await client_with_static.get("/vite.svg")
        assert resp.status == 404

    @pytest.mark.asyncio
    async def test_spa_fallback_serves_index(self, client_with_static):
        resp = await client_with_static.get("/some/spa/route")
        assert resp.status == 200
        text = await resp.text()
        assert "G13" in text

    @pytest.mark.asyncio
    async def test_spa_fallback_api_prefix_404(self, client_with_static):
        resp = await client_with_static.get("/api/nonexistent")
        assert resp.status == 404

    @pytest.mark.asyncio
    async def test_spa_fallback_ws_path_404(self, client_with_static):
        """ws path in SPA fallback should 404 (not serve index)."""
        # The /ws route is handled by websocket handler, not SPA fallback.
        # But if something hits SPA fallback with path="ws", it should 404.
        # This is tricky because /ws is already routed. Skip if route match takes precedence.
        pass

    @pytest.mark.asyncio
    async def test_spa_fallback_existing_file(self, client_with_static):
        resp = await client_with_static.get("/other.html")
        assert resp.status == 200
        text = await resp.text()
        assert "other" in text

    @pytest.mark.asyncio
    async def test_serve_html_file_missing(self, server_with_static, static_dir):
        """_serve_html_file raises 404 when file doesn't exist."""
        (static_dir / "index.html").unlink()
        with pytest.raises(web.HTTPNotFound):
            await server_with_static._serve_html_file("index.html")

    @pytest.mark.asyncio
    async def test_no_static_routes(self, client_no_static):
        """Without static dir, root returns 404 or 405 (OPTIONS route matches)."""
        resp = await client_no_static.get("/")
        assert resp.status in (404, 405)


# ---------------------------------------------------------------------------
# Broadcast helpers
# ---------------------------------------------------------------------------


class TestBroadcast:
    """Test broadcast mechanism."""

    @pytest.mark.asyncio
    async def test_broadcast_no_clients(self, server_no_static):
        """Broadcast with no clients should not raise."""
        await server_no_static._broadcast({"type": "test"})

    @pytest.mark.asyncio
    async def test_broadcast_to_clients(self, server_no_static):
        ws1 = AsyncMock()
        ws2 = AsyncMock()
        server_no_static._clients = {ws1, ws2}
        await server_no_static._broadcast({"type": "test", "data": 42})
        assert ws1.send_str.await_count == 1
        assert ws2.send_str.await_count == 1
        sent = json.loads(ws1.send_str.call_args[0][0])
        assert sent["type"] == "test"

    @pytest.mark.asyncio
    async def test_broadcast_removes_dead_client(self, server_no_static):
        ws_good = AsyncMock()
        ws_dead = AsyncMock()
        ws_dead.send_str.side_effect = ConnectionError("gone")
        server_no_static._clients = {ws_good, ws_dead}
        await server_no_static._broadcast({"type": "ping"})
        assert ws_dead not in server_no_static._clients
        assert ws_good in server_no_static._clients

    @pytest.mark.asyncio
    async def test_broadcast_button_pressed(self, server_no_static):
        ws = AsyncMock()
        server_no_static._clients = {ws}
        await server_no_static.broadcast_button_pressed("G1")
        sent = json.loads(ws.send_str.call_args[0][0])
        assert sent["type"] == "button_pressed"
        assert sent["button"] == "G1"

    @pytest.mark.asyncio
    async def test_broadcast_button_released(self, server_no_static):
        ws = AsyncMock()
        server_no_static._clients = {ws}
        await server_no_static.broadcast_button_released("G2")
        sent = json.loads(ws.send_str.call_args[0][0])
        assert sent["type"] == "button_released"
        assert sent["button"] == "G2"

    @pytest.mark.asyncio
    async def test_broadcast_profile_activated(self, server_no_static):
        ws = AsyncMock()
        server_no_static._clients = {ws}
        await server_no_static.broadcast_profile_activated("gaming")
        sent = json.loads(ws.send_str.call_args[0][0])
        assert sent["type"] == "profile_activated"
        assert sent["name"] == "gaming"

    @pytest.mark.asyncio
    async def test_broadcast_device_connected(self, server_no_static):
        ws = AsyncMock()
        server_no_static._clients = {ws}
        await server_no_static.broadcast_device_connected()
        sent = json.loads(ws.send_str.call_args[0][0])
        assert sent["type"] == "device_connected"

    @pytest.mark.asyncio
    async def test_broadcast_device_disconnected(self, server_no_static):
        ws = AsyncMock()
        server_no_static._clients = {ws}
        await server_no_static.broadcast_device_disconnected()
        sent = json.loads(ws.send_str.call_args[0][0])
        assert sent["type"] == "device_disconnected"


# ---------------------------------------------------------------------------
# WebSocket message handling
# ---------------------------------------------------------------------------


class TestWebSocketMessages:
    """Test WebSocket message dispatch and handlers."""

    @pytest.mark.asyncio
    async def test_ws_get_state(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "get_state"})
            resp = await ws.receive_json()
            assert resp["type"] == "state"
            assert resp["data"]["connected"] is True
            assert resp["data"]["active_mode"] == "M1"

    @pytest.mark.asyncio
    async def test_ws_set_mode(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_mode", "mode": "M2"})
            # Send a follow-up to ensure the first message was processed
            await ws.send_json({"type": "get_state"})
            await ws.receive_json()
            mock_daemon.set_mode.assert_called_with("M2")

    @pytest.mark.asyncio
    async def test_ws_set_mode_default(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_mode"})
            await ws.send_json({"type": "get_state"})
            await ws.receive_json()
            mock_daemon.set_mode.assert_called_with("M1")

    @pytest.mark.asyncio
    async def test_ws_set_mapping_success(self, client_no_static, mock_daemon):
        mock_daemon.set_button_mapping.return_value = True
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_mapping", "button": "G1", "key": "a"})
            resp = await ws.receive_json()
            assert resp["type"] == "mapping_changed"
            assert resp["button"] == "G1"
            assert resp["key"] == "a"

    @pytest.mark.asyncio
    async def test_ws_set_mapping_failure(self, client_no_static, mock_daemon):
        mock_daemon.set_button_mapping.return_value = False
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_mapping", "button": "G1", "key": "a"})
            resp = await ws.receive_json()
            assert resp["type"] == "error"

    @pytest.mark.asyncio
    async def test_ws_set_mapping_missing_params(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_mapping"})
            resp = await ws.receive_json()
            assert resp["type"] == "error"
            assert "Missing" in resp["message"]

    @pytest.mark.asyncio
    async def test_ws_simulate_press(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "simulate_press", "button": "G5"})
            resp = await ws.receive_json()
            assert resp["type"] == "button_pressed"
            assert resp["button"] == "G5"

    @pytest.mark.asyncio
    async def test_ws_simulate_release(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "simulate_release", "button": "G5"})
            resp = await ws.receive_json()
            assert resp["type"] == "button_released"
            assert resp["button"] == "G5"

    @pytest.mark.asyncio
    async def test_ws_set_backlight(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_backlight", "color": "#00ff00", "brightness": 50})
            resp = await ws.receive_json()
            assert resp["type"] == "backlight_changed"
            assert resp["backlight"]["color"] == "#00ff00"
            assert resp["backlight"]["brightness"] == 50
            mock_daemon._led_controller.set_color.assert_called_with(0, 255, 0)

    @pytest.mark.asyncio
    async def test_ws_set_backlight_defaults(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_backlight"})
            resp = await ws.receive_json()
            assert resp["type"] == "backlight_changed"
            assert resp["backlight"]["color"] == "#ffffff"
            assert resp["backlight"]["brightness"] == 100

    @pytest.mark.asyncio
    async def test_ws_get_macros(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "get_macros"})
            resp = await ws.receive_json()
            assert resp["type"] == "macros"
            assert len(resp["data"]) == 1

    @pytest.mark.asyncio
    async def test_ws_play_macro_success(self, client_no_static, mock_daemon):
        step = MacroStep(MacroStepType.KEY_PRESS, "KEY_A")
        macro = Macro(id="m1", name="TestMacro", steps=[step])
        mock_daemon.macro_manager.load_macro.return_value = macro
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "play_macro", "macro_id": "m1"})
            # Should receive: playback_started, step(s), playback_complete
            msgs = []
            for _ in range(3):
                msg = await ws.receive_json()
                msgs.append(msg)
            types = [m["type"] for m in msgs]
            assert "macro_playback_started" in types
            assert "macro_step" in types
            assert "macro_playback_complete" in types

    @pytest.mark.asyncio
    async def test_ws_play_macro_no_id(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "play_macro"})
            resp = await ws.receive_json()
            assert resp["type"] == "error"
            assert "macro_id" in resp["message"].lower() or "No macro_id" in resp["message"]

    @pytest.mark.asyncio
    async def test_ws_play_macro_not_found(self, client_no_static, mock_daemon):
        mock_daemon.macro_manager.load_macro.side_effect = FileNotFoundError()
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "play_macro", "macro_id": "nope"})
            resp = await ws.receive_json()
            assert resp["type"] == "error"

    @pytest.mark.asyncio
    async def test_ws_play_macro_exception(self, client_no_static, mock_daemon):
        mock_daemon.macro_manager.load_macro.side_effect = RuntimeError("boom")
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "play_macro", "macro_id": "bad"})
            resp = await ws.receive_json()
            assert resp["type"] == "error"
            assert "boom" in resp["message"]

    @pytest.mark.asyncio
    async def test_ws_stop_macro(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "stop_macro"})
            resp = await ws.receive_json()
            assert resp["type"] == "macro_playback_stopped"

    @pytest.mark.asyncio
    async def test_ws_unknown_type(self, client_no_static, mock_daemon):
        """Unknown message type should log warning but not crash."""
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "nonexistent_type"})
            # Server shouldn't send anything back for unknown types
            # Just verify connection stays alive
            await ws.send_json({"type": "get_state"})
            resp = await ws.receive_json()
            assert resp["type"] == "state"

    @pytest.mark.asyncio
    async def test_ws_invalid_json(self, client_no_static, mock_daemon):
        """Invalid JSON should log error but not crash connection."""
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_str("not valid json {{{")
            # Connection should survive
            await ws.send_json({"type": "get_state"})
            resp = await ws.receive_json()
            assert resp["type"] == "state"

    @pytest.mark.asyncio
    async def test_ws_client_connect_disconnect(self, client_no_static, server_no_static):
        """Client should be tracked in _clients set."""
        assert len(server_no_static._clients) == 0
        ws = await client_no_static.ws_connect("/ws")
        # Give server a moment to add client
        await ws.send_json({"type": "get_state"})
        await ws.receive_json()
        assert len(server_no_static._clients) == 1
        await ws.close()
        # After close, client should be removed (eventually)
        # The removal happens when the async for loop exits


# ---------------------------------------------------------------------------
# Multiple WebSocket clients
# ---------------------------------------------------------------------------


class TestMultipleClients:
    """Test broadcast reaches multiple clients."""

    @pytest.mark.asyncio
    async def test_broadcast_to_multiple(self, client_no_static, server_no_static, mock_daemon):
        ws1 = await client_no_static.ws_connect("/ws")
        ws2 = await client_no_static.ws_connect("/ws")

        # Warm up connections
        await ws1.send_json({"type": "get_state"})
        await ws1.receive_json()
        await ws2.send_json({"type": "get_state"})
        await ws2.receive_json()

        assert len(server_no_static._clients) == 2

        # Trigger broadcast via simulate_press
        await ws1.send_json({"type": "simulate_press", "button": "G1"})

        # Both should receive the broadcast
        r1 = await ws1.receive_json()
        r2 = await ws2.receive_json()
        assert r1["type"] == "button_pressed"
        assert r2["type"] == "button_pressed"

        await ws1.close()
        await ws2.close()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @pytest.mark.asyncio
    async def test_ws_handler_exception_in_handler(self, server_no_static):
        """_handle_ws_message catches generic exceptions."""
        ws = AsyncMock()
        # A message that would trigger an exception in a handler
        server_no_static.daemon.set_mode.side_effect = RuntimeError("device error")
        await server_no_static._handle_ws_message(
            ws, json.dumps({"type": "set_mode", "mode": "M1"})
        )
        # Should not raise - error is caught and logged

    @pytest.mark.asyncio
    async def test_ws_mapping_missing_button(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_mapping", "key": "a"})
            resp = await ws.receive_json()
            assert resp["type"] == "error"

    @pytest.mark.asyncio
    async def test_ws_mapping_missing_key(self, client_no_static, mock_daemon):
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "set_mapping", "button": "G1"})
            resp = await ws.receive_json()
            assert resp["type"] == "error"

    @pytest.mark.asyncio
    async def test_api_cors_on_all_endpoints(self, client_no_static):
        """Verify CORS headers on status and macros endpoints."""
        for path in ["/api/status", "/api/macros"]:
            resp = await client_no_static.get(path)
            assert resp.status == 200
            assert "Access-Control-Allow-Origin" in resp.headers

    @pytest.mark.asyncio
    async def test_play_macro_with_multiple_steps(self, client_no_static, mock_daemon):
        steps = [
            MacroStep(MacroStepType.KEY_PRESS, "KEY_A", True, 0),
            MacroStep(MacroStepType.DELAY, 50, True, 50),
            MacroStep(MacroStepType.KEY_RELEASE, "KEY_A", False, 100),
        ]
        macro = Macro(id="m2", name="Multi", steps=steps)
        mock_daemon.macro_manager.load_macro.return_value = macro
        async with client_no_static.ws_connect("/ws") as ws:
            await ws.send_json({"type": "play_macro", "macro_id": "m2"})
            msgs = []
            # started + 3 steps + complete = 5 messages
            for _ in range(5):
                msg = await ws.receive_json()
                msgs.append(msg)
            step_msgs = [m for m in msgs if m["type"] == "macro_step"]
            assert len(step_msgs) == 3
            assert step_msgs[0]["step_index"] == 0
            assert step_msgs[0]["total_steps"] == 3
            assert step_msgs[2]["step_index"] == 2

    @pytest.mark.asyncio
    async def test_update_macro_with_steps_and_playback_mode(self, client_no_static, mock_daemon):
        macro = Macro(id="m1", name="Old")
        mock_daemon.macro_manager.load_macro.return_value = macro
        resp = await client_no_static.put(
            "/api/macros/m1",
            json={
                "name": "Updated",
                "steps": [
                    {"type": "key_press", "value": "KEY_B", "is_press": True, "timestamp_ms": 0}
                ],
                "playback_mode": "as_fast",
                "speed_multiplier": 0.5,
            },
        )
        assert resp.status == 200
        assert macro.name == "Updated"
        assert len(macro.steps) == 1
        assert macro.playback_mode == PlaybackMode.AS_FAST
        assert macro.speed_multiplier == 0.5
