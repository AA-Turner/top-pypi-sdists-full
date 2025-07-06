"""Autonomous issue creator for mesh agents."""

from __future__ import annotations

import json as _json
from typing import Dict, Optional

try:  # optional dependency
    import requests  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback used in CI
    import urllib.request

    class _Resp:
        def __init__(self, text: str, status: int = 200) -> None:
            self.text = text
            self.status_code = status

        def json(self) -> Dict:
            return _json.loads(self.text)

        def raise_for_status(self) -> None:
            if self.status_code >= 400:
                raise RuntimeError(f"status {self.status_code}")

    class requests:
        @staticmethod
        def post(url: str, json: Dict, headers: Optional[Dict[str, str]] = None) -> _Resp:
            data = _json.dumps(json or {}).encode()
            req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST")
            with urllib.request.urlopen(req) as resp:
                text = resp.read().decode()
            return _Resp(text, resp.getcode())


def create_issue(repo: str, title: str, body: str, token: str) -> int:
    """Open an issue on ``repo`` and return the issue number."""
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"title": title, "body": body}
    resp = requests.post(url, json=payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return int(data.get("number", 0))


def sandbox_diagnostics(log: str) -> None:
    """Placeholder diagnostics when auth fails."""
    print("🐒 Mad monkey diagnostics engaged")
    print(log)


def handle_http_error(repo: str, err: Exception, log: str, token: Optional[str] = None) -> None:
    """Create a GitHub issue for auth errors and trigger diagnostics."""
    msg = str(err)
    if "403" in msg or "404" in msg:
        if token:
            body = f"Error: {msg}\n\nLogs:\n```\n{log}\n```\nCheck PAT permissions."
            try:
                create_issue(repo, "Auth failure detected", body, token)
            except Exception as ex:  # pragma: no cover - network faults
                sandbox_diagnostics(f"Issue creation failed: {ex}\n{log}")
        else:
            sandbox_diagnostics(log)

