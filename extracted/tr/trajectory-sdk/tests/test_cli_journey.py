from __future__ import annotations

import json
import os
import subprocess
import sys
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


class FixtureAPI(BaseHTTPRequestHandler):
  key = "fixture-cli-secret"
  requests: list[tuple[str, str, str | None, str | None]] = []
  revoked = False

  def log_message(self, format: str, *args: object) -> None:
    pass

  def do_GET(self) -> None:
    self.handle_api()

  def do_POST(self) -> None:
    self.handle_api()

  def handle_api(self) -> None:
    cls = type(self)
    cls.requests.append(
      (self.command, self.path, self.headers.get("X-API-Key"), self.headers.get("Idempotency-Key"))
    )
    size = int(self.headers.get("Content-Length", "0"))
    body = json.loads(self.rfile.read(size)) if size else {}
    if self.path == "/api/v1/device/auth/sessions":
      self.reply(
        201,
        {
          "device_code": "fixture-device-code",
          "user_code": "BCDF-GHJK",
          "verification_url": "https://platform.example.com/device/authorize?code=BCDF-GHJK",
          "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=10)).isoformat(),
          "poll_interval_seconds": 1,
        },
      )
    elif self.path == "/api/v1/device/auth/token":
      self.reply(
        200,
        {
          "status": "approved",
          "api_key": cls.key,
          "api_key_prefix": "fixture",
          "organization": {"id": "org_test", "key": "example", "name": "Example"},
          "user_email": "member@example.com",
        },
      )
    elif self.headers.get("X-API-Key") != cls.key or cls.revoked:
      self.reply(401, {"detail": "Authentication required"})
    elif self.path == "/api/v1/organizations/current":
      self.reply(200, {"organization_id": "org_test", "organization_key": "example"})
    elif self.path == "/api/v1/eval":
      self.reply(
        200,
        {
          "eval_run_id": "eval_test",
          "agent_id": "agent_test",
          "bench_id": body["bench_id"],
          "display_name": None,
          "base_model_slug": body["base_model_slug"],
          "options": body.get("options", {}),
          "status": "pending",
          "created_at": "2026-01-01T00:00:00Z",
          "updated_at": "2026-01-01T00:00:00Z",
        },
      )
    elif self.path == "/api/v1/device/auth/logout":
      cls.revoked = True
      self.reply(200, {"revoked": True})
    else:
      self.reply(404, {"detail": "Unhandled fixture endpoint"})

  def reply(self, status: int, body: object) -> None:
    encoded = json.dumps(body).encode()
    self.send_response(status)
    self.send_header("Content-Type", "application/json")
    self.send_header("Content-Length", str(len(encoded)))
    self.end_headers()
    self.wfile.write(encoded)


def test_login_sdk_eval_reconnect_and_logout_across_processes(tmp_path: Path) -> None:
  class Handler(FixtureAPI):
    requests = []
    revoked = False

  server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
  worker = threading.Thread(target=server.serve_forever, daemon=True)
  worker.start()
  environment = dict(os.environ)
  for name in ("TRAJECTORY_API_KEY", "TRAJECTORY_BASE_URL", "TRAJECTORY_PROFILE"):
    environment.pop(name, None)
  environment["TRAJECTORY_CONFIG_HOME"] = str(tmp_path / "credentials")
  environment["NO_PROXY"] = "127.0.0.1,localhost"
  origin = f"http://127.0.0.1:{server.server_port}"

  def command(*args: str) -> dict[str, object]:
    result = subprocess.run(
      [sys.executable, "-m", "trajectory.lib.cli.main", *args, "--json"],
      cwd=tmp_path,
      env=environment,
      capture_output=True,
      text=True,
      timeout=15,
      check=False,
    )
    assert Handler.key not in result.stdout + result.stderr
    assert result.returncode == 0, result.stdout + result.stderr
    return json.loads(result.stdout)

  try:
    command("login", "--base-url", origin, "--no-browser", "--timeout", "5")
    identity = command("whoami")
    assert "example" in json.dumps(identity)
    sdk = subprocess.run(
      [
        sys.executable,
        "-c",
        "from trajectory import Client; c = Client(); print(c.organizations.retrieve_current()['organization_key']); c.close()",
      ],
      cwd=tmp_path,
      env=environment,
      capture_output=True,
      text=True,
      timeout=15,
      check=False,
    )
    assert sdk.returncode == 0, sdk.stderr
    assert sdk.stdout.strip() == "example"
    config = tmp_path / "eval.json"
    config.write_text(
      json.dumps(
        {
          "bench_id": "bench_test",
          "base_model_slug": "openai/gpt-5-mini",
          "options": {"val_num_tasks": 1},
        }
      )
    )
    first = command("evals", "create", "--config", str(config), "--request-id", "eval-request-test")
    replay = command(
      "evals", "create", "--config", str(config), "--request-id", "eval-request-test"
    )
    assert first == replay
    calls = [r for r in Handler.requests if r[1] == "/api/v1/eval"]
    assert len(calls) == 1
    assert calls[0][3] == "eval-request-test"
    command("logout")
    assert Handler.revoked
    assert all(
      r[2] is None
      for r in Handler.requests
      if r[1] in {"/api/v1/device/auth/sessions", "/api/v1/device/auth/token"}
    )
  finally:
    server.shutdown()
    server.server_close()
    worker.join(timeout=5)
