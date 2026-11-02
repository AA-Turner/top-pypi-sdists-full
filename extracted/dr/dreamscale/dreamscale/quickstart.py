"""Setup flows for CLI login and SO-101 hardware quickstart."""

from __future__ import annotations

import asyncio
import getpass
import time
import webbrowser
from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import Any

import httpx

from dreamscale import errors
from dreamscale.config import (
    API_KEY_ENV,
    Config,
    config_path,
    dreamscale_home,
    load_config,
    save_config,
    saved_api_key,
)
from dreamscale.constants import API_KEY_PREFIXES, DEFAULT_CONTROL_PLANE_URL
from dreamscale.control import ControlPlaneClient
from dreamscale.hardware.cameras import RigCameraProber, save_preview
from dreamscale.hardware.ports import list_candidate_ports
from dreamscale.hardware.rig_file import rig_file_path

DEFAULT_FRONTEND_URL = "https://app.dreamscalelabs.com"
LOGIN_START_ATTEMPTS = 3
LOGIN_START_BACKOFF_S = (0.5, 1.0)
LOGIN_POLL_CONSECUTIVE_FAILURE_LIMIT = 3


@dataclass(frozen=True)
class BrowserAuthStart:
    user_code: str
    verification_url: str
    device_token: str
    expires_in: int
    interval: int


class BrowserAuthClient:
    def __init__(
        self,
        base_url: str = DEFAULT_FRONTEND_URL,
        *,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=httpx.Timeout(10.0, connect=5.0),
            transport=transport,
        )

    def start(self) -> BrowserAuthStart:
        response = self._client.post("/api/cli-auth/start")
        response.raise_for_status()
        payload = response.json()
        return BrowserAuthStart(
            user_code=str(payload["userCode"]),
            verification_url=str(payload["verificationUrl"]),
            device_token=str(payload["deviceToken"]),
            expires_in=int(payload.get("expiresIn", 600)),
            interval=max(1, int(payload.get("interval", 2))),
        )

    def poll(self, device_token: str, previous_api_key: str | None = None) -> dict[str, Any]:
        body = {"deviceToken": device_token}
        if previous_api_key:
            # The login revokes the CLI key it replaces: one key per machine.
            body["previousApiKey"] = previous_api_key
        response = self._client.post("/api/cli-auth/poll", json=body)
        response.raise_for_status()
        return dict(response.json())

    def logout(self, api_key: str) -> str:
        """Revoke a CLI login's key: "revoked", "not_cli_login" (a key the user made,
        left working) or "invalid" (already revoked or unknown)."""
        response = self._client.post(
            "/api/cli-auth/logout", headers={"Authorization": f"Bearer {api_key}"}
        )
        response.raise_for_status()
        return str(response.json()["status"])

    def whoami(self, api_key: str) -> dict[str, Any] | None:
        """Who the key signs in as, or None when it no longer works."""
        response = self._client.get(
            "/api/cli-auth/whoami", headers={"Authorization": f"Bearer {api_key}"}
        )
        if response.status_code == 401:
            return None
        response.raise_for_status()
        return dict(response.json())

    def close(self) -> None:
        self._client.close()


def _retryable_browser_auth_error(exc: httpx.HTTPError) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        return status in {408, 429} or status >= 500
    return isinstance(exc, httpx.TransportError)


def _browser_auth_error_detail(phase: str, exc: httpx.HTTPError) -> str:
    action = {
        "start": "starting browser login",
        "poll": "waiting for browser approval",
        "logout": "signing out",
        "whoami": "looking up your account",
    }[phase]
    request_id: str | None = None
    if isinstance(exc, httpx.HTTPStatusError):
        headers = exc.response.headers
        request_id = headers.get("x-dreamscale-request-id") or headers.get(
            "x-dropbear-request-id"
        )
        detail = f"the login service returned HTTP {exc.response.status_code} while {action}"
    else:
        detail = f"the login service could not be reached while {action} ({type(exc).__name__})"
    if request_id:
        detail += f"; request id {request_id}"
    return detail


def _browser_auth_protocol_error(phase: str) -> errors.DreamscaleError:
    return errors.catalog(
        "cli_login_protocol_failed",
        detail=f"the login service returned malformed data during {phase}",
    )


def run_login(
    *,
    print_fn: Callable[[str], None] = print,
    key_input_fn: Callable[[str], str] = getpass.getpass,
    client_factory: Callable[..., Any] = ControlPlaneClient,
    auth_client_factory: Callable[..., Any] = BrowserAuthClient,
    open_browser: Callable[[str], bool] = webbrowser.open,
    sleep_fn: Callable[[float], None] = time.sleep,
    monotonic_fn: Callable[[], float] = time.monotonic,
    api_key: str | None = None,
    prompt_for_api_key: bool = False,
) -> Config:
    """Log in by browser device flow or by explicitly supplied API key."""
    if api_key is not None or prompt_for_api_key:
        key = api_key.strip() if api_key is not None else key_input_fn("API key: ").strip()
        return _save_verified_login_key(
            key,
            print_fn=print_fn,
            client_factory=client_factory,
        )

    previous_api_key = saved_api_key()
    auth_client = auth_client_factory()
    try:
        for attempt in range(LOGIN_START_ATTEMPTS):
            try:
                started = auth_client.start()
                break
            except httpx.HTTPError as exc:
                if _retryable_browser_auth_error(exc) and attempt < LOGIN_START_ATTEMPTS - 1:
                    sleep_fn(LOGIN_START_BACKOFF_S[attempt])
                    continue
                raise errors.catalog(
                    "cli_login_start_failed",
                    detail=_browser_auth_error_detail("start", exc),
                ) from exc
            except (KeyError, TypeError, ValueError) as exc:
                raise _browser_auth_protocol_error("login start") from exc
        else:  # pragma: no cover - loop either succeeds or raises
            raise errors.catalog("cli_login_start_failed")
        print_fn("Sign in to Dreamscale:")
        print_fn(f"  {started.verification_url}")
        print_fn(f"Code: {started.user_code}")
        try:
            opened = open_browser(started.verification_url)
        except Exception:
            opened = False
        if opened:
            print_fn("✓ opened your browser")
        else:
            print_fn("Open the URL above in your browser to continue.")
        print_fn("Waiting for approval...")

        deadline = monotonic_fn() + min(started.expires_in, 600)
        interval = max(1, started.interval)
        consecutive_poll_failures = 0
        while monotonic_fn() < deadline:
            sleep_fn(interval)
            try:
                payload = auth_client.poll(started.device_token, previous_api_key)
            except httpx.HTTPError as exc:
                consecutive_poll_failures += 1
                if (
                    _retryable_browser_auth_error(exc)
                    and consecutive_poll_failures <= LOGIN_POLL_CONSECUTIVE_FAILURE_LIMIT
                ):
                    continue
                raise errors.catalog(
                    "cli_login_poll_failed",
                    detail=_browser_auth_error_detail("poll", exc),
                ) from exc
            except (KeyError, TypeError, ValueError) as exc:
                raise _browser_auth_protocol_error("approval polling") from exc
            consecutive_poll_failures = 0
            if not isinstance(payload, dict):
                raise _browser_auth_protocol_error("approval polling")
            status = payload.get("status")
            if status == "pending":
                continue
            if status == "approved":
                key = str(payload.get("apiKey") or "")
                return _save_verified_login_key(
                    key,
                    print_fn=print_fn,
                    client_factory=client_factory,
                )
            if status == "expired":
                raise errors.catalog("cli_login_expired")
            raise _browser_auth_protocol_error("approval polling")
        raise errors.catalog("cli_login_expired")
    finally:
        auth_client.close()


def _save_verified_login_key(
    key: str,
    *,
    print_fn: Callable[[str], None],
    client_factory: Callable[..., Any],
) -> Config:
    key = _validate_api_key(key)
    existing = load_config()
    _run(_verify_key(client_factory, DEFAULT_CONTROL_PLANE_URL, key))
    print_fn("✓ key verified")
    config = Config(
        api_key=key,
        control_plane_url=DEFAULT_CONTROL_PLANE_URL,
        preferred_region=existing.preferred_region or "nearest",
        robot_port=existing.robot_port,
        calibration_path=existing.calibration_path,
        camera_index=existing.camera_index,
        wrist_camera_index=existing.wrist_camera_index,
        home_position=existing.home_position,
        integrations=existing.integrations,
    )
    saved_path = save_config(config, save_api_key=True)
    print_fn(f"✓ saved login to {saved_path}")
    _print_nearest_region(print_fn=print_fn, client_factory=client_factory, key=key)
    if existing.api_key_source == API_KEY_ENV and existing.api_key != key:
        print_fn(
            f"Note: {API_KEY_ENV} is set in this shell and takes precedence over this login; "
            f"unset it to use the login."
        )
    print_fn("Tip: run `dreamscale --install-completion` to enable tab completion.")
    return config


def _print_nearest_region(
    *,
    print_fn: Callable[[str], None],
    client_factory: Callable[..., Any],
    key: str,
) -> None:
    """Says which region is nearest this machine, from the region record's probes (a second or
    two) and the control plane. Only says: a deployment's ``auto`` measures when it's created,
    and ``preferred_region`` is a fixed region to whatever reads it, which models served from one
    region refuse. Nothing measured says nothing, and this never fails a login."""
    from dreamscale.region_choice import nearest_region

    def call(method: str, **kwargs: Any) -> Any:
        return _run(_client_call(client_factory, DEFAULT_CONTROL_PLANE_URL, key, method, **kwargs))

    try:
        live = {
            region["id"]: region
            for region in (call("list_regions") or {}).get("regions") or ()
            if region.get("live")
        }
        found = nearest_region(
            [
                {"region": id_, "url": region["probe_url"]}
                for id_, region in live.items()
                if region.get("probe_url")
            ],
            ask=lambda measurements: call("resolve_region", measurements=measurements),
            allowed=live,
        )
    except Exception:
        return
    if found is None:
        return
    measured = f" ({found.median_ms:.0f} ms)" if found.median_ms is not None else ""
    print_fn(f"Nearest region: {live[found.region].get('label') or found.region}{measured}")


def run_logout(
    *,
    print_fn: Callable[[str], None] = print,
    auth_client_factory: Callable[..., Any] = BrowserAuthClient,
) -> None:
    """`dreamscale auth logout`: revoke this machine's login key and forget it."""
    key = saved_api_key()
    if key is None:
        print_fn("No login is saved on this machine.")
    else:
        auth_client = auth_client_factory()
        try:
            # Revoked before it is forgotten: a CLI key appears on no page to revoke later.
            status = auth_client.logout(key)
        except httpx.HTTPError as exc:
            raise errors.catalog(
                "cli_logout_failed", detail=_browser_auth_error_detail("logout", exc)
            ) from exc
        except (KeyError, TypeError, ValueError) as exc:
            raise _browser_auth_protocol_error("logout") from exc
        finally:
            auth_client.close()
        save_config(replace(load_config(), api_key=None))
        if status == "not_cli_login":
            print_fn(
                f"✓ signed out; the saved API key still works — revoke it at "
                f"{DEFAULT_FRONTEND_URL}/dashboard/keys if you no longer need it"
            )
        else:
            print_fn("✓ signed out")
    if load_config().api_key_source == API_KEY_ENV:
        print_fn(f"Note: {API_KEY_ENV} is set in this shell; unset it to stop using that key.")


def run_whoami(
    *,
    print_fn: Callable[[str], None] = print,
    auth_client_factory: Callable[..., Any] = BrowserAuthClient,
) -> None:
    """`dreamscale auth whoami`: who this machine's key signs in as."""
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")
    auth_client = auth_client_factory()
    try:
        identity = auth_client.whoami(config.api_key)
    except httpx.HTTPError as exc:
        raise errors.catalog(
            "cli_whoami_failed", detail=_browser_auth_error_detail("whoami", exc)
        ) from exc
    finally:
        auth_client.close()
    if identity is None:
        raise errors.catalog("invalid_api_key", key_source=config.api_key_source)
    try:
        email, name = str(identity["email"]), str(identity.get("name") or "")
        organization = identity.get("organization")
        print_fn(f"{email} ({name})" if name and name != email else email)
        if organization:
            slug = organization.get("slug")
            print_fn(f"Organization: {organization['name']}" + (f" ({slug})" if slug else ""))
    except (AttributeError, KeyError, TypeError) as exc:
        raise _browser_auth_protocol_error("whoami") from exc
    print_fn(
        f"Key: from {API_KEY_ENV}"
        if config.api_key_source == API_KEY_ENV
        else f"Key: saved by `{errors.COMMAND_LOGIN}`"
    )


def run_quickstart(*, input_fn: Callable[[str], str] = input,
                   print_fn: Callable[[str], None] = print,
                   prober: Any = None,
                   comports: Callable | None = None,
                   client_factory: Callable[..., Any] = ControlPlaneClient,
                   open_viewer: Callable | None = None,
                   ensure_extras: Callable[..., None] | None = None) -> None:
    existing = load_config()
    if not existing.api_key:
        raise errors.catalog("not_configured")
    # After the login check, so a signed-out user is not sent through a large download.
    if ensure_extras is None:
        from dreamscale.extras import ensure_extras
    ensure_extras(["so101"], label="SO-101", setup_command=errors.COMMAND_QUICKSTART,
                  print_fn=print_fn)
    if open_viewer is None:
        from dreamscale.doctor import _open_viewer as open_viewer
    from dreamscale.hardware.so101_config import load_config as load_rig
    from dreamscale.hardware.so101_config import save_config as save_rig

    rig = load_rig()
    prober = prober if prober is not None else RigCameraProber(rig.cameras)

    print_fn(
        "dreamscale robots so101 setup — choose the arm's port and its two cameras."
    )

    key = existing.api_key
    _run(_verify_key(client_factory, existing.control_plane_url, key))
    print_fn("✓ key verified")

    # ── input 1/3: robot port (autodetect → confirm) ───────────────────
    port = _choose_robot_port(
        existing.robot_port,
        input_fn=input_fn,
        print_fn=print_fn,
        comports=comports,
    )
    print_fn(f"✓ robot port: {port}")

    # ── inputs 2/3 and 3/3: cameras (preview → confirm) ────────────────
    saved = {role: rig.camera(role) for role in rig.roles}
    side_camera = _choose_camera(
        "side", saved.get("side"), step="2/3", prober=prober, input_fn=input_fn,
        print_fn=print_fn, open_viewer=open_viewer,
    )
    print_fn(f"✓ side camera: {side_camera.id}")
    wrist_camera = _choose_camera(
        "wrist", saved.get("wrist"), step="3/3", prober=prober, input_fn=input_fn,
        print_fn=print_fn, open_viewer=open_viewer, exclude={side_camera.physical_id},
    )
    print_fn(f"✓ wrist camera: {wrist_camera.id}")

    rig.cameras = [side_camera, wrist_camera]
    rig.roles = {"side": side_camera.id, "wrist": wrist_camera.id}
    rig.port, rig.calibration_path = port, existing.calibration_path
    rig.home_pose = (
        tuple(float(v) for v in existing.home_position)
        if existing.home_position is not None else None
    )
    save_rig(rig)
    # The rig file now exists, so the account save leaves the robot keys to it.
    save_config(Config(api_key=key, control_plane_url=existing.control_plane_url,
                       preferred_region=existing.preferred_region,
                       robot_port=port, calibration_path=existing.calibration_path,
                       home_position=existing.home_position,
                       integrations=existing.integrations))
    if rig.migrated:
        print_fn("✓ moved SO-101 settings from config.toml into the rig file")
    print_fn(f"✓ saved to {config_path()} and {rig_file_path('so101')}")


def _validate_api_key(key: str) -> str:
    if not key.startswith(API_KEY_PREFIXES):
        raise errors.catalog("invalid_api_key")
    return key


def _candidate_ports(comports: Callable | None) -> list[Any]:
    return list_candidate_ports() if comports is None else list_candidate_ports(comports=comports)


def _detect_robot_port(*, input_fn, print_fn, comports: Callable | None) -> str:
    candidates = _candidate_ports(comports)
    if len(candidates) == 1:
        answer = input_fn(
            f"1/3 Found your robot at {candidates[0].device} — press Enter to "
            "confirm (or type another port): "
        ).strip()
        return answer or candidates[0].device
    if candidates:
        for i, candidate in enumerate(candidates):
            print_fn(f"  [{i}] {candidate.device}  {candidate.description}")
        answer = input_fn("1/3 Which one is the robot? [0]: ").strip()
        return candidates[int(answer or "0")].device
    port = input_fn(
        "1/3 No USB-serial device found — plug the arm in and type its port "
        "(e.g. /dev/ttyACM0): "
    ).strip()
    if not port:
        raise errors.catalog("robot_port_not_found", port="(none found)")
    return port


def _choose_robot_port(existing: str | None, *, input_fn, print_fn,
                       comports: Callable | None) -> str:
    if existing:
        answer = input_fn(
            f"1/3 Robot port [{existing}] — press Enter to keep, type 'auto' "
            "to detect, or type a new port: "
        ).strip()
        if not answer:
            return existing
        if answer.lower() != "auto":
            return answer
    return _detect_robot_port(input_fn=input_fn, print_fn=print_fn, comports=comports)


def _preview_camera(spec, *, prober, open_viewer) -> bool:
    frame = prober.capture_preview(spec)
    if frame is None:
        return False
    preview = save_preview(frame, dreamscale_home() / "camera_preview.jpg")
    open_viewer(preview)
    return True


def _pick_camera_with_preview(*, role: str, step: str, prober, input_fn,
                              open_viewer, exclude: set[str] | None = None):
    exclude = exclude or set()
    available = [s for s in prober.list_cameras() if s.physical_id not in exclude]
    if not available:
        raise errors.catalog("camera_missing", index=0)
    for spec in available:
        frame = prober.capture_preview(spec)
        if frame is None:
            continue
        preview = save_preview(frame, dreamscale_home() / "camera_preview.jpg")
        open_viewer(preview)
        answer = input_fn(
            f"{step} Preview from {spec.backend} camera {spec.id} saved to {preview} — "
            f"use it as the {role} camera? [Y/n] "
        ).strip().lower()
        if answer != "n":
            return spec
    raise errors.catalog("camera_missing", index=0)


def _choose_camera(role: str, existing, *, step: str, prober, input_fn, print_fn,
                   open_viewer, exclude: set[str] | None = None):
    """A camera for role, by stable identity: keep the saved one, or pick by preview."""
    exclude = exclude or set()
    connected = {s.physical_id: s for s in prober.list_cameras()}
    if existing is not None:
        answer = input_fn(
            f"{step} {role.capitalize()} camera [{existing.id}] — press Enter to keep, "
            "or type 'preview' to choose visually: "
        ).strip()
        if not answer:
            current = connected.get(existing.physical_id)
            if current is not None and current.physical_id not in exclude:
                return current
            print_fn(f"{role.capitalize()} camera {existing.id} isn't available; "
                     "choose another.")
        else:
            print_fn(f"Opening {role} camera previews. Press Enter to accept a good view.")
    return _pick_camera_with_preview(
        role=role, step=step, prober=prober, input_fn=input_fn, open_viewer=open_viewer,
        exclude=exclude,
    )


def _run(coro):
    return asyncio.run(coro)


async def _client_call(client_factory, base_url: str, key: str, method: str, **kwargs) -> Any:
    client = client_factory(base_url, key)
    try:
        return await getattr(client, method)(**kwargs)
    finally:
        await client.close()


async def _verify_key(client_factory, base_url: str, key: str) -> None:
    client = client_factory(base_url, key)
    try:
        await client.status()
    finally:
        await client.close()
