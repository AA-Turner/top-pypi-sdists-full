"""The real SEO app must consult current session authority before route work."""

import time

import httpx
import jwt
import pytest
from fastapi.testclient import TestClient

SECRET = "synthetic-seo-session-admission-secret"
SUBJECT = "00000000-0000-4000-8000-000000000001"
SESSION = "00000000-0000-4000-8000-000000000002"
AUTHORITY = "https://authority.example/auth/session/status"


def bearer():
    expiry = int(time.time()) + 3600
    token = jwt.encode(
        {"sub": SUBJECT, "session_id": SESSION, "aud": "authenticated", "exp": expiry},
        SECRET,
        algorithm="HS256",
    )
    return token, expiry


def configure(monkeypatch):
    monkeypatch.setenv("SUPABASE_JWT_SECRET", SECRET)
    monkeypatch.delenv("SUPABASE_MATRIX_URL", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.setenv("MATRX_SESSION_AUTHORITY_URL", AUTHORITY)


def test_actual_seo_me_refuses_ended_and_unavailable_before_db(monkeypatch):
    from matrx_seo.standalone.app import create_app

    configure(monkeypatch)
    token, expiry = bearer()
    state = "active"
    queries = []
    requests = []

    async def membership(*args, **kwargs):
        queries.append(args)
        return []

    monkeypatch.setattr("matrx_orm.call_function", membership)

    def authority(request):
        requests.append(request)
        assert str(request.url) == AUTHORITY
        assert request.headers["authorization"] == f"Bearer {token}"
        if state == "ended":
            return httpx.Response(401)
        if state == "unavailable":
            return httpx.Response(503)
        return httpx.Response(
            200, json={"user_id": SUBJECT, "session_id": SESSION, "expires_at": expiry}
        )

    client_class = httpx.AsyncClient
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kw: client_class(**kw, transport=httpx.MockTransport(authority)),
    )
    client = TestClient(create_app())
    headers = {"Authorization": f"Bearer {token}"}
    active = client.get("/me", headers=headers)
    assert active.status_code == 200
    assert active.json()["user_id"] == SUBJECT
    state = "ended"
    assert client.get("/me", headers=headers).status_code == 401
    state = "unavailable"
    response = client.get("/me", headers=headers)
    assert response.status_code == 503
    assert response.headers["retry-after"] == "1"
    assert len(queries) == 1
    assert len(requests) == 3
    assert client.get("/health").status_code == 200
    assert client.get("/me", headers={"X-API-Key": "synthetic"}).status_code == 401


def test_missing_authority_cannot_silently_fall_back_to_crypto_only(monkeypatch):
    from matrx_seo.standalone.app import create_app

    configure(monkeypatch)
    monkeypatch.delenv("MATRX_SESSION_AUTHORITY_URL")
    token, _ = bearer()
    client = TestClient(create_app())
    assert client.get("/health").status_code == 200
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 503
    assert response.json()["code"] == "session_authority_unavailable"
    ready = client.get("/health/ready")
    assert ready.status_code == 503
    assert ready.json()["session_authority_configured"] is False
    assert "session_authority_configured" in ready.json()["failed_components"]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "status,body",
    [
        (401, {"code": "invalid_session"}),
        (401, {"code": "cdn_challenge"}),
        (302, {}),
        (503, {}),
        (200, {}),
    ],
)
async def test_candidate_probe_requires_exact_endpoint_contract(monkeypatch, status, body):
    from matrx_seo.standalone.check_session_authority import check_authority

    calls = []

    def authority(request):
        calls.append(request)
        assert str(request.url) == AUTHORITY
        assert "authorization" not in request.headers
        return httpx.Response(status, json=body, headers={"Location": "https://other.example/"})

    client_class = httpx.AsyncClient
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kw: client_class(**kw, transport=httpx.MockTransport(authority)),
    )
    if status == 401 and body == {"code": "invalid_session"}:
        await check_authority(AUTHORITY)
    else:
        with pytest.raises(RuntimeError):
            await check_authority(AUTHORITY)
    assert len(calls) == 1


def test_both_deploy_paths_probe_candidate_before_removal_and_inject_authority():
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[3]
    manual = (root / "packages/matrx-seo/deploy.sh").read_text()
    workflow = (root / ".github/workflows/publish-package.yml").read_text()
    local = (root / "packages/matrx-seo/scripts/run_local.sh").read_text()
    manual_url = re.search(r'^SESSION_AUTHORITY_URL="([^"]+)"$', manual, re.M)[1]
    workflow_url = re.search(r"^      SESSION_AUTHORITY_URL: (.+)$", workflow, re.M)[1]
    assert manual_url == workflow_url
    assert manual_url in local
    for script in (manual, workflow):
        assert script.index("docker run --rm -i --entrypoint python") < script.index(
            "docker rm -f matrx-seo"
        )
        for run in re.findall(r"docker run -d --name matrx-seo[^\n]*", script.replace("\\\n", " ")):
            assert "MATRX_SESSION_AUTHORITY_URL=" in run
    assert workflow.count('-e "MATRX_SESSION_AUTHORITY_URL=$SESSION_AUTHORITY_URL"') == 3
    assert manual.count("-e 'MATRX_SESSION_AUTHORITY_URL=${SESSION_AUTHORITY_URL}'") == 2


@pytest.mark.parametrize("kind", ["api-key", "service-role"])
def test_independent_credential_cannot_become_login_session(monkeypatch, kind):
    from matrx_seo.standalone.app import create_app

    configure(monkeypatch)
    token = (
        "mx_synthetic"
        if kind == "api-key"
        else jwt.encode(
            {
                "sub": SUBJECT,
                "aud": "authenticated",
                "role": "service_role",
                "exp": int(time.time()) + 3600,
            },
            SECRET,
            algorithm="HS256",
        )
    )
    calls = []

    def authority(request):
        calls.append(request)
        return httpx.Response(401)

    client_class = httpx.AsyncClient
    monkeypatch.setattr(
        httpx,
        "AsyncClient",
        lambda **kw: client_class(**kw, transport=httpx.MockTransport(authority)),
    )
    client = TestClient(create_app())
    assert client.get("/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401
    assert len(calls) == (1 if kind == "service-role" else 0)


@pytest.mark.asyncio
@pytest.mark.parametrize("kind", ["malformed", "oversize", "timeout"])
async def test_candidate_probe_bounds_body_and_time(monkeypatch, kind):
    import asyncio

    from matrx_seo.standalone.check_session_authority import check_authority

    class Stream(httpx.AsyncByteStream):
        closed = False

        async def __aiter__(self):
            if kind == "timeout":
                await asyncio.sleep(10)
            yield b"x" * (4097 if kind == "oversize" else 10)

        async def aclose(self):
            self.closed = True

    stream = Stream()
    client_class = httpx.AsyncClient

    def factory(**kw):
        assert kw["follow_redirects"] is False
        assert kw["trust_env"] is False
        return client_class(
            **kw, transport=httpx.MockTransport(lambda request: httpx.Response(401, stream=stream))
        )

    monkeypatch.setattr(httpx, "AsyncClient", factory)
    with pytest.raises((RuntimeError, ValueError, TimeoutError)):
        await check_authority(AUTHORITY, timeout_seconds=0.01)
    assert stream.closed


def test_manual_failed_candidate_probe_never_removes_existing_container(tmp_path, monkeypatch):
    import os
    import subprocess
    from pathlib import Path

    root = Path(__file__).resolve().parents[3]
    log = tmp_path / "calls"
    monkeypatch.setenv("CALL_LOG", str(log))
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ['PATH']}")
    for name in ("curl", "scp"):
        stub = tmp_path / name
        stub.write_text("#!/bin/sh\nexit 0\n")
        stub.chmod(0o755)
    ssh = tmp_path / "ssh"
    ssh.write_text("""#!/bin/sh
printf '%s\\n' "$*" >> "$CALL_LOG"
case "$*" in
  *MATRX_SESSION_AUTHORITY_URL*) exit 17 ;;
  *importlib.metadata*) printf '0.0.0\\n' ;;
esac
exit 0
""")
    ssh.chmod(0o755)
    result = subprocess.run(
        ["bash", str(root / "packages/matrx-seo/deploy.sh"), "0.0.0"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 17, result.stdout + result.stderr
    calls = log.read_text()
    assert "docker run --rm -i --entrypoint python" in calls
    assert (
        "MATRX_SESSION_AUTHORITY_URL=https://server.app.matrxserver.com/auth/session/status"
        in calls
    )
    assert "docker rm" not in calls
    assert "docker run -d" not in calls


def test_source_probe_allows_rollback_wheel_without_new_seo_cli(tmp_path, monkeypatch):
    import os
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[3]
    log = tmp_path / "calls"
    monkeypatch.setenv("CALL_LOG", str(log))
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ['PATH']}")
    for name in ("curl", "scp"):
        stub = tmp_path / name
        stub.write_text("#!/bin/sh\nexit 0\n")
        stub.chmod(0o755)
    ssh = tmp_path / "ssh"
    ssh.write_text(
        f"#!{sys.executable}\n"
        + """import os, sys
from pathlib import Path
command = " ".join(sys.argv[1:])
with Path(os.environ["CALL_LOG"]).open("a") as log:
    log.write(command + "\\n")
if "docker run --rm -i --entrypoint python" in command:
    import httpx
    # The older wheel lacks the new SEO CLI; shared resolver is installed.
    sys.modules["matrx_seo.standalone.check_session_authority"] = None
    os.environ["MATRX_SESSION_AUTHORITY_URL"] = "https://authority.example/status"
    original = httpx.AsyncClient
    httpx.AsyncClient = lambda **kw: original(**kw, transport=httpx.MockTransport(
        lambda request: httpx.Response(401, json={"code": "invalid_session"})))
    source = sys.stdin.read()
    assert "RemoteSessionResolver" in source
    exec(compile(source, "candidate-stdin", "exec"), {"__name__": "__main__"})
elif "docker rm -f matrx-seo" in command:
    # Record reaching cutover, then stop the simulation before health checks.
    sys.exit(23)
elif "importlib.metadata" in command:
    print("0.0.0")
"""
    )
    ssh.chmod(0o755)
    result = subprocess.run(
        ["bash", str(root / "packages/matrx-seo/deploy.sh"), "0.0.0"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    assert result.returncode == 23, result.stdout + result.stderr
    calls = log.read_text()
    assert "docker rm -f matrx-seo" in calls
    assert "Session authority contract available" in result.stdout
