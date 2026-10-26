"""The CLI starts without the generated wire models.

Building the ~770 pydantic models in `probe._generated.models` took ~0.5 s of
every `probe` command -- the wizard, the plugin hooks, the status line -- that
never sends one. The CLI imports the option enums from `_generated.enums`
(`scripts/gen_models.py:split_enums`) and the SDK client when a command builds
one (`main._client_class`).
"""

from __future__ import annotations

import subprocess
import sys

HEAVY = ("probe._generated.models", "probe.models", "probe.sdk.client")


def test_the_cli_starts_without_the_wire_models():
    code = (
        # What the wizard loads before its menu, too: the speed of its first
        # screens rests on these.
        "import sys, probe._entry, probe.cli.main, probe.cli.setup, probe.cli.capabilities, "
        "probe.cli.doctor, probe.cli.actions, probe.cli.tui; "
        f"print(sorted(m for m in {HEAVY!r} if m in sys.modules))"
    )
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert done.stdout.strip() == "[]"


def test_the_client_seam_is_still_the_sdk_client():
    import probe.cli
    from probe.sdk.client import Client

    assert probe.cli.Client is Client


def test_every_generated_enum_is_still_a_model_export():
    from probe._compat import StrEnum
    from probe._generated import enums, models

    names = [n for n, v in vars(enums).items() if isinstance(v, type) and issubclass(v, StrEnum) and v is not StrEnum]
    assert names
    assert all(getattr(models, n) is getattr(enums, n) for n in names)


def test_the_read_token_check_answers_without_a_client(monkeypatch):
    """`_verify_read`, the wizard's `/v1/me` for the read token, through the SDK
    transport alone: the same answers as `_verify` (ok with the identity, a 401
    refused), against a real server."""
    import json
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    import importlib

    main = importlib.import_module("probe.cli.main")  # `probe.cli.main` the package attribute is a function
    answer = {"status": 200}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802 - http.server's name
            body = json.dumps({"email": "r@example.test"}).encode()
            self.send_response(answer["status"])
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        assert main._verify_read("probe_pat_read", base_url) == ("ok", {"email": "r@example.test"})
        answer["status"] = 401
        assert main._verify_read("probe_pat_read", base_url) == ("rejected", None)
    finally:
        server.shutdown()
        server.server_close()
