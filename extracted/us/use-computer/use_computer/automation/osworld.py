from __future__ import annotations

import asyncio
import os
import time
from pathlib import Path
from typing import Any

import httpx

PYAUTOGUI_PKGS_PREFIX = (
    "import pyautogui; import time; import platform; "
    "pyautogui.FAILSAFE = False; "
    "_osworld_shift_chars = '~!@#$%^&*()_+' + chr(123) + chr(125) + '|:\"<>?'; "
    "_osworld_linux_shift_chars = '~!@#$%^&*()_+' + chr(123) + chr(125) + '|:\">?'; "
    "pyautogui.isShiftCharacter = lambda character: character.isupper() or "
    "character in (_osworld_linux_shift_chars if platform.system() == 'Linux' else "
    "_osworld_shift_chars); "
    "{command}"
)
OSWORLD_SCREENSHOT_RETRY_TIMES = 3
OSWORLD_SCREENSHOT_RETRY_INTERVAL = 5.0
OSWORLD_SCREENSHOT_TIMEOUT = 10


class OSWorldClient:
    """Raw OSWorld HTTP surface exposed by macOS sandboxes."""

    def __init__(self, http: httpx.Client, prefix: str):
        self._http = http
        self._prefix = prefix

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        resp = self._http.request(method, self._url(path), **kwargs)
        resp.raise_for_status()
        return resp

    def screenshot(self) -> bytes:
        last_error: Exception | None = None
        for attempt in range(OSWORLD_SCREENSHOT_RETRY_TIMES):
            try:
                resp = self.request("GET", "/screenshot", timeout=OSWORLD_SCREENSHOT_TIMEOUT)
                if _is_valid_image_response(resp):
                    return resp.content
                last_error = RuntimeError(
                    "OSWorld screenshot endpoint returned a non-image payload"
                )
            except httpx.HTTPStatusError as e:
                if _is_not_found(e):
                    try:
                        resp = self._http.request(
                            "GET",
                            f"{self._prefix}/screenshot",
                            timeout=OSWORLD_SCREENSHOT_TIMEOUT,
                        )
                        resp.raise_for_status()
                        if _is_valid_image_response(resp):
                            return resp.content
                        last_error = RuntimeError(
                            "Sandbox screenshot endpoint returned a non-image payload"
                        )
                    except httpx.HTTPError as fallback_error:
                        last_error = fallback_error
                else:
                    last_error = e
            except httpx.HTTPError as e:
                last_error = e

            if attempt + 1 < OSWORLD_SCREENSHOT_RETRY_TIMES:
                time.sleep(OSWORLD_SCREENSHOT_RETRY_INTERVAL)

        if last_error is not None:
            raise last_error
        raise RuntimeError("OSWorld screenshot endpoint did not return an image")

    def accessibility(self) -> str | None:
        data = self.request("GET", "/accessibility", timeout=60).json()
        return data.get("AT")

    def terminal(self) -> str | None:
        data = self.request("GET", "/terminal", timeout=60).json()
        return data.get("output")

    def file(self, file_path: str) -> bytes:
        return self.request("POST", "/file", data={"file_path": file_path}, timeout=120).content

    def execute(
        self, command: str | list[str], *, shell: bool = False, timeout: int = 120
    ) -> dict[str, Any]:
        resp = self.request(
            "POST",
            "/execute",
            json={"command": command, "shell": shell},
            timeout=timeout,
        )
        return resp.json()

    def execute_python(self, command: str, *, timeout: int = 120) -> dict[str, Any]:
        return self.execute(
            ["python", "-c", PYAUTOGUI_PKGS_PREFIX.format(command=command)],
            shell=False,
            timeout=timeout,
        )

    def setup_upload(
        self, file_path: str, data: bytes, filename: str | None = None
    ) -> dict[str, Any]:
        files = {"file_data": (filename or os.path.basename(file_path), data)}
        resp = self.request(
            "POST",
            "/setup/upload",
            data={"file_path": file_path},
            files=files,
            timeout=600,
        )
        return _json_or_text(resp)

    def setup_execute(self, payload: dict[str, Any], *, timeout: int = 120) -> dict[str, Any]:
        return self.request("POST", "/setup/execute", json=payload, timeout=timeout).json()

    def setup_execute_with_verification(
        self, payload: dict[str, Any], *, timeout: int = 120
    ) -> dict[str, Any]:
        try:
            return self.request(
                "POST", "/setup/execute_with_verification", json=payload, timeout=timeout
            ).json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code != 404:
                raise
        return self._setup_execute_with_verification_fallback(payload, timeout=timeout)

    def setup_launch(self, command: str | list[str], *, shell: bool = False) -> dict[str, Any]:
        return _json_or_text(
            self.request("POST", "/setup/launch", json={"command": command, "shell": shell})
        )

    def setup_open_file(self, path: str) -> dict[str, Any]:
        return _json_or_text(
            self.request("POST", "/setup/open_file", json={"path": path}, timeout=1810)
        )

    def setup_activate_window(
        self, window_name: str, *, strict: bool = False, by_class: bool = False
    ) -> dict[str, Any]:
        try:
            return _json_or_text(
                self.request(
                    "POST",
                    "/setup/activate_window",
                    json={"window_name": window_name, "strict": strict, "by_class": by_class},
                )
            )
        except httpx.HTTPStatusError as e:
            if not _is_not_found(e):
                raise
            return {"status": "skipped", "reason": "missing_activate_window_endpoint"}

    def setup_close_window(
        self, window_name: str, *, strict: bool = False, by_class: bool = False
    ) -> dict[str, Any]:
        try:
            return _json_or_text(
                self.request(
                    "POST",
                    "/setup/close_window",
                    json={"window_name": window_name, "strict": strict, "by_class": by_class},
                )
            )
        except httpx.HTTPStatusError as e:
            if not _is_not_found(e):
                raise
            return {"status": "skipped", "reason": "missing_close_window_endpoint"}

    def setup_change_wallpaper(self, path: str) -> dict[str, Any]:
        return _json_or_text(self.request("POST", "/setup/change_wallpaper", json={"path": path}))

    def screen_size(self) -> dict[str, Any]:
        return self.request("POST", "/screen_size", timeout=30).json()

    def _url(self, path: str) -> str:
        return f"{self._prefix}/osworld{path if path.startswith('/') else '/' + path}"

    def _setup_execute_with_verification_fallback(
        self, payload: dict[str, Any], *, timeout: int
    ) -> dict[str, Any]:
        result = self.setup_execute(
            {
                "command": payload["command"],
                "shell": bool(payload.get("shell", False)),
            },
            timeout=timeout,
        )
        verification = payload.get("verification") or {}
        command = verification.get("command")
        if not command:
            return {**result, "verification": "skipped", "wait_time": 0}

        max_wait_time = float(payload.get("max_wait_time", 10))
        check_interval = float(payload.get("check_interval", 1.0))
        start = time.monotonic()
        deadline = start + max_wait_time
        verify_payload = {
            "command": command,
            "shell": bool(verification.get("shell", False)),
        }
        last_result: dict[str, Any] | None = None
        while True:
            last_result = self.setup_execute(verify_payload, timeout=timeout)
            if _is_success_result(last_result):
                return {
                    **result,
                    "verification": "passed",
                    "wait_time": time.monotonic() - start,
                    "verification_result": last_result,
                }
            if time.monotonic() >= deadline:
                break
            time.sleep(check_interval)
        raise RuntimeError(
            f"OSWorld setup verification failed: {_compact_result(last_result or {})}"
        )


class AsyncOSWorldClient:
    """Async raw OSWorld HTTP surface exposed by macOS sandboxes."""

    def __init__(self, http: httpx.AsyncClient, prefix: str):
        self._http = http
        self._prefix = prefix

    async def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        resp = await self._http.request(method, self._url(path), **kwargs)
        resp.raise_for_status()
        return resp

    async def screenshot(self) -> bytes:
        last_error: Exception | None = None
        for attempt in range(OSWORLD_SCREENSHOT_RETRY_TIMES):
            try:
                resp = await self.request("GET", "/screenshot", timeout=OSWORLD_SCREENSHOT_TIMEOUT)
                if _is_valid_image_response(resp):
                    return resp.content
                last_error = RuntimeError(
                    "OSWorld screenshot endpoint returned a non-image payload"
                )
            except httpx.HTTPStatusError as e:
                if _is_not_found(e):
                    try:
                        resp = await self._http.request(
                            "GET",
                            f"{self._prefix}/screenshot",
                            timeout=OSWORLD_SCREENSHOT_TIMEOUT,
                        )
                        resp.raise_for_status()
                        if _is_valid_image_response(resp):
                            return resp.content
                        last_error = RuntimeError(
                            "Sandbox screenshot endpoint returned a non-image payload"
                        )
                    except httpx.HTTPError as fallback_error:
                        last_error = fallback_error
                else:
                    last_error = e
            except httpx.HTTPError as e:
                last_error = e

            if attempt + 1 < OSWORLD_SCREENSHOT_RETRY_TIMES:
                await asyncio.sleep(OSWORLD_SCREENSHOT_RETRY_INTERVAL)

        if last_error is not None:
            raise last_error
        raise RuntimeError("OSWorld screenshot endpoint did not return an image")

    async def accessibility(self) -> str | None:
        data = (await self.request("GET", "/accessibility", timeout=60)).json()
        return data.get("AT")

    async def terminal(self) -> str | None:
        data = (await self.request("GET", "/terminal", timeout=60)).json()
        return data.get("output")

    async def file(self, file_path: str) -> bytes:
        return (
            await self.request("POST", "/file", data={"file_path": file_path}, timeout=120)
        ).content

    async def execute(
        self, command: str | list[str], *, shell: bool = False, timeout: int = 120
    ) -> dict[str, Any]:
        resp = await self.request(
            "POST",
            "/execute",
            json={"command": command, "shell": shell},
            timeout=timeout,
        )
        return resp.json()

    async def execute_python(self, command: str, *, timeout: int = 120) -> dict[str, Any]:
        return await self.execute(
            ["python", "-c", PYAUTOGUI_PKGS_PREFIX.format(command=command)],
            shell=False,
            timeout=timeout,
        )

    async def setup_upload(
        self, file_path: str, data: bytes | Path, filename: str | None = None
    ) -> dict[str, Any]:
        content = data.read_bytes() if isinstance(data, Path) else data
        files = {"file_data": (filename or os.path.basename(file_path), content)}
        resp = await self.request(
            "POST",
            "/setup/upload",
            data={"file_path": file_path},
            files=files,
            timeout=600,
        )
        return _json_or_text(resp)

    async def setup_execute(self, payload: dict[str, Any], *, timeout: int = 120) -> dict[str, Any]:
        return (await self.request("POST", "/setup/execute", json=payload, timeout=timeout)).json()

    async def setup_execute_with_verification(
        self, payload: dict[str, Any], *, timeout: int = 120
    ) -> dict[str, Any]:
        try:
            return (
                await self.request(
                    "POST", "/setup/execute_with_verification", json=payload, timeout=timeout
                )
            ).json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code != 404:
                raise
        return await self._setup_execute_with_verification_fallback(payload, timeout=timeout)

    async def setup_launch(
        self, command: str | list[str], *, shell: bool = False
    ) -> dict[str, Any]:
        return _json_or_text(
            await self.request("POST", "/setup/launch", json={"command": command, "shell": shell})
        )

    async def setup_open_file(self, path: str) -> dict[str, Any]:
        return _json_or_text(
            await self.request("POST", "/setup/open_file", json={"path": path}, timeout=1810)
        )

    async def setup_activate_window(
        self, window_name: str, *, strict: bool = False, by_class: bool = False
    ) -> dict[str, Any]:
        try:
            return _json_or_text(
                await self.request(
                    "POST",
                    "/setup/activate_window",
                    json={"window_name": window_name, "strict": strict, "by_class": by_class},
                )
            )
        except httpx.HTTPStatusError as e:
            if not _is_not_found(e):
                raise
            return {"status": "skipped", "reason": "missing_activate_window_endpoint"}

    async def setup_close_window(
        self, window_name: str, *, strict: bool = False, by_class: bool = False
    ) -> dict[str, Any]:
        try:
            return _json_or_text(
                await self.request(
                    "POST",
                    "/setup/close_window",
                    json={"window_name": window_name, "strict": strict, "by_class": by_class},
                )
            )
        except httpx.HTTPStatusError as e:
            if not _is_not_found(e):
                raise
            return {"status": "skipped", "reason": "missing_close_window_endpoint"}

    async def setup_change_wallpaper(self, path: str) -> dict[str, Any]:
        return _json_or_text(
            await self.request("POST", "/setup/change_wallpaper", json={"path": path})
        )

    async def screen_size(self) -> dict[str, Any]:
        return (await self.request("POST", "/screen_size", timeout=30)).json()

    def _url(self, path: str) -> str:
        return f"{self._prefix}/osworld{path if path.startswith('/') else '/' + path}"

    async def _setup_execute_with_verification_fallback(
        self, payload: dict[str, Any], *, timeout: int
    ) -> dict[str, Any]:
        result = await self.setup_execute(
            {
                "command": payload["command"],
                "shell": bool(payload.get("shell", False)),
            },
            timeout=timeout,
        )
        verification = payload.get("verification") or {}
        command = verification.get("command")
        if not command:
            return {**result, "verification": "skipped", "wait_time": 0}

        max_wait_time = float(payload.get("max_wait_time", 10))
        check_interval = float(payload.get("check_interval", 1.0))
        start = time.monotonic()
        deadline = start + max_wait_time
        verify_payload = {
            "command": command,
            "shell": bool(verification.get("shell", False)),
        }
        last_result: dict[str, Any] | None = None
        while True:
            last_result = await self.setup_execute(verify_payload, timeout=timeout)
            if _is_success_result(last_result):
                return {
                    **result,
                    "verification": "passed",
                    "wait_time": time.monotonic() - start,
                    "verification_result": last_result,
                }
            if time.monotonic() >= deadline:
                break
            await asyncio.sleep(check_interval)
        raise RuntimeError(
            f"OSWorld setup verification failed: {_compact_result(last_result or {})}"
        )


def _json_or_text(resp: httpx.Response) -> dict[str, Any]:
    try:
        return resp.json()
    except ValueError:
        return {"status": "success", "output": resp.text}


def _is_valid_image_response(resp: httpx.Response) -> bool:
    content = resp.content
    content_type = resp.headers.get("Content-Type", "")
    if len(content) >= 8 and content[:8] == b"\x89PNG\r\n\x1a\n":
        return True
    if len(content) >= 3 and content[:3] == b"\xff\xd8\xff":
        return True
    return (
        "image/png" in content_type or "image/jpeg" in content_type or "image/jpg" in content_type
    )


def _is_not_found(error: httpx.HTTPStatusError) -> bool:
    return error.response.status_code == 404


def _is_success_result(result: dict[str, Any]) -> bool:
    status = str(result.get("status", "")).lower()
    returncode = result.get("returncode", result.get("return_code", result.get("code")))
    if status and status not in {"success", "ok"}:
        return False
    return returncode in (None, 0, "0")


def _compact_result(result: dict[str, Any]) -> str:
    text = str(result)
    return text if len(text) <= 300 else text[:297] + "..."
