"""Frozen-binary coverage for the AI Watch credential exchange TLS path."""

from __future__ import annotations

import os
import socket
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.frozen_binary


def test_frozen_credential_exchange_uses_os_trust_store(
    frozen_aiwatch: Path,
    tmp_path: Path,
) -> None:
    try:
        with socket.create_connection(("runlayer.com", 443), timeout=5):
            pass
    except OSError as exc:
        pytest.skip(f"runlayer.com is unreachable: {type(exc).__name__}")

    home = tmp_path / "home"
    credential = home / ".runlayer" / "aiwatch" / "llm-routing-credential"
    credential.parent.mkdir(parents=True)
    credential.write_text("rlk_frozen_test_dummy\n", encoding="utf-8")
    credential.chmod(0o600)

    env = dict(os.environ)
    env["HOME"] = str(home)
    env["RUNLAYER_HOST"] = "https://runlayer.com"
    env.pop("SSL_CERT_FILE", None)

    result = subprocess.run(
        [str(frozen_aiwatch), "credential", "claude"],
        capture_output=True,
        text=True,
        env=env,
        timeout=30,
        check=False,
    )

    assert result.returncode == 1
    assert "HTTP" in result.stderr
    assert "TLS certificate verification failed" not in result.stderr
