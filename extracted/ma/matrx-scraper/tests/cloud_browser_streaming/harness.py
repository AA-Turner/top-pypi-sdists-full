"""Shared standalone harness for the WS-4 streaming proofs.

Generates a throwaway EC P-256 key, builds a real StreamPlane + gateway + mint
over the in-memory backends, and stands a run + handoff up so a control ticket
can be minted and claimed — with NO Browser Manager and NO ``browser.*`` schema
(S4 §10 stub contract).
"""

from __future__ import annotations

from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec

from matrx_scraper.cloud_browser.streaming.access import FixtureAccessResolver
from matrx_scraper.cloud_browser.streaming.config import StreamingConfig
from matrx_scraper.cloud_browser.streaming.control_plane import MintService
from matrx_scraper.cloud_browser.streaming.gateway import StreamGateway
from matrx_scraper.cloud_browser.streaming.plane import StreamPlane

ORIGIN = "https://aimatrx.com"


def generate_ec_pem() -> str:
    key = ec.generate_private_key(ec.SECP256R1())
    return key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")


@dataclass
class Harness:
    pem: str
    config: StreamingConfig
    access: FixtureAccessResolver
    plane: StreamPlane
    gateway: StreamGateway
    mint: MintService
    user_id: str
    profile_id: str
    run_id: str
    worker_id: str
    handoff_id: str

    def worker_channel(self):
        return self.plane.workers.channel(self.run_id)


def make_harness(
    *, multi_view_low_latency: bool = False, turn_secret: str | None = "shhh-turn-secret"
) -> Harness:
    pem = generate_ec_pem()
    config = StreamingConfig(
        stream_signing_key_pem=pem,
        allowed_origins=frozenset({ORIGIN}),
        turn_shared_secret=turn_secret,
        turn_realm="aimatrx.com",
        stun_urls=("stun:turn.aimatrx.com:3478",),
        turn_urls=("turn:turn.aimatrx.com:3478?transport=udp",),
        gateway_ws_base="wss://stream.aimatrx.com",
    )
    access = FixtureAccessResolver()
    plane = StreamPlane.build(config=config, access=access)
    gateway = StreamGateway(plane)
    mint = MintService(plane, gateway, multi_view_low_latency=multi_view_low_latency)

    user_id = "user-arman"
    profile_id = "profile-1"
    worker_id = "worker-A"
    run = plane.runs.create_run(run_id="run-1", profile_id=profile_id, worker_id=worker_id)
    # Agent currently controls; revision 1.
    handoff_id = plane.runs.open_handoff(run.run_id, ttl_seconds=1800)
    # Grant the user editor access (control tier).
    access.grant(user_id=user_id, profile_id=profile_id, level="editor")

    return Harness(
        pem=pem,
        config=config,
        access=access,
        plane=plane,
        gateway=gateway,
        mint=mint,
        user_id=user_id,
        profile_id=profile_id,
        run_id=run.run_id,
        worker_id=worker_id,
        handoff_id=handoff_id,
    )
