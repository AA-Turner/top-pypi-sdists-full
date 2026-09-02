from __future__ import annotations

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import pytest
from fastapi.testclient import TestClient
from matrx_connect import ScopedTokenIssuer

from matrx_scraper.cloud_browser.worker.auth import Es256WorkerTokenVerifier
from matrx_scraper.cloud_browser.worker.errors import WorkerProtocolError
from matrx_scraper.cloud_browser.worker.http_app import create_worker_app
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker


def _issuer() -> ScopedTokenIssuer:
    key = ec.generate_private_key(ec.SECP256R1())
    pem = key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption(),
    ).decode()
    return ScopedTokenIssuer(issuer="browser-manager", private_key_pem=pem)


def _mint(
    issuer: ScopedTokenIssuer, *, worker_id: str, op: str = "heartbeat", ttl: int = 60
) -> str:
    token, _ = issuer.mint(
        user_id="run:00000000-0000-0000-0000-000000000001",
        audience=f"worker:{worker_id}",
        tier_policy="none",
        ttl_seconds=ttl,
        extra_claims={
            "run_id": "00000000-0000-0000-0000-000000000001",
            "profile_id": "00000000-0000-0000-0000-000000000002",
            "mtx_op": op,
        },
    )
    return token


def test_public_key_verifier_accepts_once_and_rejects_replay() -> None:
    issuer = _issuer()
    verifier = Es256WorkerTokenVerifier("browser-manager", issuer.public_key_pem)
    token = _mint(issuer, worker_id="worker-a")

    credential = verifier.verify(token, worker_id="worker-a", op="heartbeat")
    assert credential.profile_id == "00000000-0000-0000-0000-000000000002"
    with pytest.raises(WorkerProtocolError, match="credential_replayed"):
        verifier.verify(token, worker_id="worker-a", op="heartbeat")


def test_public_key_verifier_rejects_wrong_worker_and_operation() -> None:
    issuer = _issuer()
    verifier = Es256WorkerTokenVerifier("browser-manager", issuer.public_key_pem)
    token = _mint(issuer, worker_id="worker-a")

    with pytest.raises(WorkerProtocolError, match="audience_mismatch"):
        verifier.verify(token, worker_id="worker-b", op="heartbeat")
    with pytest.raises(WorkerProtocolError, match="unauthorized_worker_call"):
        verifier.verify(token, worker_id="worker-a", op="shutdown")


def test_http_app_exposes_health_and_all_worker_operations() -> None:
    worker = BrowserWorker(worker_id="worker-a")
    client = TestClient(create_worker_app(worker))
    assert client.get("/health").json() == {"status": "starting", "worker_id": "worker-a"}
    paths = {route.path for route in client.app.routes}
    assert {
        "/bootstrap",
        "/heartbeat",
        "/command",
        "/observe",
        "/capture",
        "/controller-transition",
        "/checkpoint",
        "/shutdown",
    } <= paths
