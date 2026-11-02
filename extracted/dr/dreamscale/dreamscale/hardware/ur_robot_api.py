"""PolyScope X's Robot API: load and play the External Control program from this computer.

PolyScope X 10.11+ serves a REST API at http://<robot>/universal-robots/robot-api. Program
load and play are accepted only while the pendant is in Remote control mode, so in Local mode
the operator still presses Play. Older software has no API; callers fall back to the pendant.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

BASE_PATH = "/universal-robots/robot-api"
TIMEOUT_S = 5.0


class RobotAPIError(RuntimeError):
    """The Robot API refused a request or could not be reached."""


class RobotAPI:
    def __init__(self, host: str, *, opener=urllib.request.urlopen, timeout_s: float = TIMEOUT_S):
        self.base = f"http://{host}{BASE_PATH}"
        self._open, self.timeout_s = opener, timeout_s

    def _call(self, method: str, path: str, body: dict | None = None) -> dict:
        data = None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(
            self.base + path, data=data, method=method,
            headers={"Content-Type": "application/json"} if data is not None else {},
        )
        try:
            with self._open(request, timeout=self.timeout_s) as response:
                return json.loads(response.read() or b"{}")
        except urllib.error.HTTPError as exc:
            try:
                body = json.loads(exc.read() or b"{}")
                message = body.get("message") or body.get("detail") or exc.reason
                if isinstance(body.get("details"), str) and body["details"]:
                    message = f"{message}: {body['details']}"
            except ValueError:
                message = exc.reason
            raise RobotAPIError(f"{message} (HTTP {exc.code})") from exc
        except (OSError, ValueError) as exc:
            raise RobotAPIError(str(exc)) from exc

    def remote_control(self) -> bool:
        """True when the pendant is in Remote control mode; False without the API."""
        try:
            return self._call("GET", "/system/v1/controlmode").get("mode") == "REMOTE"
        except RobotAPIError:
            return False

    def loaded_program(self) -> str | None:
        return self._call("GET", "/program/v1/loaded").get("name")

    def load(self, name: str) -> None:
        self._call("PUT", "/program/v1/loaded", {"name": name})

    def program_state(self) -> str:
        """STOPPED, PLAYING or PAUSED."""
        return str(self._call("GET", "/program/v1/state").get("state"))

    def play(self) -> None:
        self._call("PUT", "/program/v1/state", {"action": "play"})

    def stop(self) -> None:
        self._call("PUT", "/program/v1/state", {"action": "stop"})
