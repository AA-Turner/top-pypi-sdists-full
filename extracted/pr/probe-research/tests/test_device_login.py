"""Device-authorization login (RFC 8628) against a mock Probe Research device API."""

from __future__ import annotations

import base64
import hashlib
import json

import httpx
import pytest

from probe.sdk import device
from probe.sdk.device import DeviceLoginError, DevicePrompt, device_login

_START = {
    "device_code": "dev-abc",
    "user_code": "WXYZ-1234",
    "verification_uri": "https://dash.test/authorize",
    "verification_uri_complete": "https://dash.test/authorize?code=WXYZ-1234",
    "expires_in": 600,
    "interval": 2,
}


def _client(handler) -> httpx.Client:
    return httpx.Client(base_url="https://api.test", transport=httpx.MockTransport(handler))


def _pending(desc: str = "waiting for browser approval") -> httpx.Response:
    return httpx.Response(
        400, json={"detail": {"error": "authorization_pending", "error_description": desc}}
    )


def test_device_login_polls_then_returns_token() -> None:
    polls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/device/code":
            return httpx.Response(201, json=_START)
        if request.url.path == "/auth/device/token":
            polls["n"] += 1
            if polls["n"] == 1:
                return _pending()
            return httpx.Response(200, json={"token": "ros_pat_deadbeef"})
        return httpx.Response(404)

    prompts: list[DevicePrompt] = []
    slept: list[float] = []
    token = device_login(
        "https://api.test",
        client=_client(handler),
        open_browser=False,
        on_prompt=prompts.append,
        sleep=slept.append,
    )

    assert token == "ros_pat_deadbeef"
    assert polls["n"] == 2
    assert prompts and prompts[0].user_code == "WXYZ-1234"
    assert slept == [2]  # one interval wait between the pending poll and success


def test_device_login_backs_off_on_slow_down() -> None:
    polls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/device/code":
            return httpx.Response(201, json=_START)
        polls["n"] += 1
        if polls["n"] == 1:
            return httpx.Response(
                429, json={"detail": {"error": "slow_down", "error_description": "too fast"}}
            )
        return httpx.Response(200, json={"token": "ros_pat_ok"})

    slept: list[float] = []

    token = device_login(
        "https://api.test", client=_client(handler), open_browser=False, sleep=slept.append
    )

    assert token == "ros_pat_ok"
    assert slept == [7]  # interval 2 + 5 back-off


def test_device_login_raises_on_denied() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/device/code":
            return httpx.Response(201, json=_START)
        return httpx.Response(
            400,
            json={
                "detail": {
                    "error": "access_denied",
                    "error_description": "the user denied this request",
                }
            },
        )

    with pytest.raises(DeviceLoginError, match="denied"):
        device_login(
            "https://api.test", client=_client(handler), open_browser=False, sleep=lambda _s: None
        )


def test_device_login_raises_when_start_fails() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            429, json={"detail": {"error": "slow_down", "error_description": "too many requests"}}
        )

    with pytest.raises(DeviceLoginError, match="too many requests"):
        device_login(
            "https://api.test", client=_client(handler), open_browser=False, sleep=lambda _s: None
        )


@pytest.mark.parametrize("start_status", [200, 201])
def test_website_code_uses_pkce_exchange_without_opening_a_browser(monkeypatch, start_status) -> None:
    requests: list[tuple[str, dict]] = []
    minted = {"token": "probe_pat_one", "grants": [{"grant": "api", "token": "probe_pat_one"}]}

    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content)
        requests.append((request.url.path, body))
        if request.url.path == "/auth/device/install-token":
            return httpx.Response(start_status, json=_START)
        assert request.url.path == "/auth/device/token"
        return httpx.Response(200, json=minted)

    def no_browser(*args):
        pytest.fail("a website code must not require a second browser approval")

    monkeypatch.setattr(device.webbrowser, "open", no_browser)
    result = device.device_authorize(
        "https://api.test",
        install_code="ABCD234567",
        grants=["api", "mcp", "capture"],
        capture_sources=["claude_code", "codex"],
        token_name="my laptop",
        device_instance_id="local-device",
        client_context={"flow": "install"},
        client=_client(handler),
        on_prompt=no_browser,
    )

    assert result == minted
    assert len(requests) == 2
    start, exchange = requests[0][1], requests[1][1]
    assert start["code"] == "ABCD234567"
    assert start["grants"] == ["api", "mcp", "capture"]
    assert start["capture_sources"] == ["claude_code", "codex"]
    assert start["token_name"] == "my laptop"
    assert start["device_instance_id"] == "local-device"
    assert "code" not in exchange
    assert (
        start["code_challenge"]
        == base64.urlsafe_b64encode(hashlib.sha256(exchange["code_verifier"].encode()).digest())
        .rstrip(b"=")
        .decode()
    )


@pytest.mark.parametrize("at_start", [True, False])
def test_onboarding_requirement_is_terminal_and_keeps_the_website_url(at_start) -> None:
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request.url.path)
        if not at_start and request.url.path == "/auth/device/code":
            return httpx.Response(201, json=_START)
        return httpx.Response(
            400,
            json={
                "detail": {
                    "error": "onboarding_required",
                    "error_description": "Complete onboarding on the website first.",
                    "onboarding_url": "https://dash.test/onboarding",
                }
            },
        )

    with pytest.raises(device.OnboardingRequired) as caught:
        device_login(
            "https://api.test",
            client=_client(handler),
            open_browser=False,
            sleep=lambda _: pytest.fail("terminal onboarding state must stop polling"),
        )
    assert caught.value.onboarding_url == "https://dash.test/onboarding"
    assert len(requests) == (1 if at_start else 2)


@pytest.mark.parametrize("code", ["ABC", "abcdefghij", "ABCD-23456", "ABCD234567X"])
def test_invalid_website_code_never_reaches_the_server(code) -> None:
    with pytest.raises(DeviceLoginError, match="exactly 10"):
        device.device_authorize(
            "https://api.test",
            install_code=code,
            client=_client(lambda _: pytest.fail("invalid code should not make a request")),
        )


def test_expired_website_code_does_not_fall_back_to_browser_login() -> None:
    requests = []

    def handler(request: httpx.Request) -> httpx.Response:
        requests.append(request.url.path)
        return httpx.Response(
            400,
            json={
                "detail": {
                    "error": "expired_token",
                    "error_description": "This code expired. Get a new install command on the website.",
                }
            },
        )

    with pytest.raises(DeviceLoginError, match="expired"):
        device.device_authorize(
            "https://api.test", install_code="ABCD234567", client=_client(handler)
        )
    assert requests == ["/auth/device/install-token"]


# ---------------------------------------------------------------------------
# The machine's NAME, as opposed to its identity.
#
# The name is display metadata and is meant to change -- but it should change
# when the machine is renamed, not when it joins a network. A captive campus
# WiFi handed a MacBook the DHCP name `visitor-10-59-125-182`, and that string
# is what got written into the dashboard as the machine's name.
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _uncached_hostname():
    """`hostname()` is process-cached, so a test that does not clear it either
    asserts against another test's answer or poisons the next one."""
    device.hostname.cache_clear()
    yield
    device.hostname.cache_clear()


def test_the_configured_name_beats_the_one_the_network_assigned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(device, "_configured_hostnames", lambda: ["Richards-MacBook-Pro"])
    monkeypatch.setattr(device.socket, "gethostname", lambda: "visitor-10-59-125-182")
    assert device.hostname() == "Richards-MacBook-Pro"


def test_the_transient_name_is_still_the_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """A platform offering no configured name must be exactly as well off as before."""
    monkeypatch.setattr(device, "_configured_hostnames", lambda: [])
    monkeypatch.setattr(device.socket, "gethostname", lambda: "prbe-devbox.internal")
    assert device.hostname() == "prbe-devbox"


@pytest.mark.parametrize("configured", [[""], ["   "], ["Not set"], ["not set"]])
def test_an_unset_configured_name_is_not_used(
    configured: list[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """`scutil --get LocalHostName` prints `Not set` rather than failing."""
    monkeypatch.setattr(device, "_configured_hostnames", lambda: configured)
    monkeypatch.setattr(device.socket, "gethostname", lambda: "fallback-host")
    assert device.hostname() == "fallback-host"


def test_a_hostname_file_that_is_not_utf8_falls_back_instead_of_crashing(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """`read_text` raises UnicodeDecodeError -- a ValueError, not an OSError --
    and letting it escape would crash every CLI invocation on that host."""
    bad = tmp_path / "hostname"
    bad.write_bytes(b"\xff\xfe not utf 8")
    monkeypatch.setattr(device.sys, "platform", "linux")
    monkeypatch.setattr(device, "Path", lambda _p: bad)
    assert device._configured_hostnames() == []


def test_a_missing_scutil_does_not_raise(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(device.sys, "platform", "darwin")

    def _boom(*_args, **_kwargs):
        raise FileNotFoundError("no scutil here")

    monkeypatch.setattr(device.subprocess, "run", _boom)
    assert device._configured_hostnames() == []
