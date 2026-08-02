"""
nx_vpn.py — VPN rotation via ProtonVPN CLI (graceful degradation if not installed)
"""

import random
import subprocess
import threading
import time
from typing import Optional

VPN_COUNTRIES = ["US", "CA", "GB", "NL", "SE"]
ROTATE_EVERY_REQUESTS = 100
ROTATE_EVERY_SECONDS = 300


class VPNRotator:
    def __init__(self, auto_rotate: bool = True):
        self._request_count = 0
        self._last_rotation = time.time()
        self._lock = threading.Lock()
        self._auto_rotate = auto_rotate
        self._current_server = None
        self._available = self._check_available()

    def _check_available(self) -> bool:
        try:
            result = subprocess.run(
                ["which", "protonvpn-cli"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _run(self, *args) -> tuple[bool, str]:
        if not self._available:
            return False, "protonvpn-cli not installed"
        try:
            result = subprocess.run(
                ["protonvpn-cli", *args],
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.returncode == 0, result.stdout.strip()
        except Exception as e:
            return False, str(e)

    def connect(self, country: Optional[str] = None) -> bool:
        if not self._available:
            return False
        country = country or random.choice(VPN_COUNTRIES)
        ok, out = self._run("connect", "--cc", country)
        if ok:
            self._current_server = country
            self._last_rotation = time.time()
            self._request_count = 0
            print(f"VPN -> {country}")
        return ok

    def disconnect(self):
        self._run("disconnect")

    def rotate(self) -> bool:
        if not self._available:
            return False
        current = self._current_server
        options = [country for country in VPN_COUNTRIES if country != current]
        return self.connect(random.choice(options))

    def should_rotate(self) -> bool:
        return (
            self._request_count >= ROTATE_EVERY_REQUESTS or
            time.time() - self._last_rotation >= ROTATE_EVERY_SECONDS
        )

    def on_request(self):
        if not self._auto_rotate or not self._available:
            return
        with self._lock:
            self._request_count += 1
            if self.should_rotate():
                self.rotate()

    def status(self) -> dict:
        if not self._available:
            return {"available": False, "reason": "protonvpn-cli not installed"}
        _, out = self._run("status")
        return {
            "available": True,
            "output": out,
            "requests_since_rotation": self._request_count,
            "current_group": self._current_server,
        }


_rotator: Optional[VPNRotator] = None


def get_rotator() -> VPNRotator:
    global _rotator
    if _rotator is None:
        _rotator = VPNRotator(auto_rotate=True)
        if _rotator._available:
            _rotator.connect()
    return _rotator
