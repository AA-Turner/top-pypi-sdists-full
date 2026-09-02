"""StubControlPlane — the in-process Browser Manager stand-in (WS-2 independence).

It is the whole reason the worker is testable with zero Browser Manager, zero DB,
and zero streaming: it owns the fencing token, the fencing revision, the sequence
counter, the activation key, and the token authority, and it drives the worker
through the eight S2 operations exactly as the real manager would — minting a
scoped bearer per call, incrementing the sequence for sequenced ops, and rotating
the fence only through ``controller_transition``.

It deliberately does NOT reimplement any worker behaviour. It is the client half of
S2; the worker is the server half. The shared conformance suite runs the worker
under this stub (and, symmetrically on WS-5's side, runs a ``FakeWorker`` under the
real control plane).
"""

from __future__ import annotations

import uuid
from datetime import UTC, datetime, timedelta

from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.auth import InMemoryTokenAuthority
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker


def _now() -> datetime:
    return datetime.now(UTC)


class StubControlPlane:
    def __init__(
        self,
        worker: BrowserWorker,
        *,
        run_id: str | None = None,
        profile_id: str | None = None,
        authority: InMemoryTokenAuthority | None = None,
    ) -> None:
        self.worker = worker
        self.run_id = run_id or f"run_{uuid.uuid4().hex[:10]}"
        self.profile_id = profile_id or f"prof_{uuid.uuid4().hex[:10]}"
        self.authority = authority
        self.fencing_token = f"ft_{uuid.uuid4().hex}"
        self.fencing_revision = 1
        self.sequence_base = 100
        self._sequence = self.sequence_base
        self.activation_key = uuid.uuid4().hex
        self.events: list[M.WorkerEvent] = []

    # ── envelope + auth helpers ─────────────────────────────────────────────

    def _bearer(self, op: str) -> str | None:
        if self.authority is None:
            return None
        return self.authority.mint(
            worker_id=self.worker.worker_id, run_id=self.run_id, profile_id=self.profile_id, op=op
        )

    def _env(
        self, *, sequenced: bool, sequence: int | None = None, idem: str | None = None
    ) -> dict:
        seq = None
        idempotency = None
        if sequenced:
            seq = sequence if sequence is not None else self._next_sequence()
            idempotency = idem or uuid.uuid4().hex
        return {
            "run_id": self.run_id,
            "profile_id": self.profile_id,
            "fencing_token": self.fencing_token,
            "fencing_revision": self.fencing_revision,
            "sequence": seq,
            "idempotency_key": idempotency,
            "issued_at": _now(),
        }

    def _next_sequence(self) -> int:
        self._sequence += 1
        return self._sequence

    # ── the eight operations ────────────────────────────────────────────────

    async def bootstrap(
        self,
        *,
        user_data_dir: str,
        run_mode: str = "automation_only",
        display: M.DisplayConfig | None = None,
        allow_eval_js: bool = False,
        reopened_for_handoff: bool = False,
    ) -> M.BootstrapResponse:
        policy = M.LaunchPolicy(
            run_mode=run_mode,
            allow_eval_js=allow_eval_js,
            reopened_for_handoff=reopened_for_handoff,
        )
        req = M.BootstrapRequest(
            **self._env(sequenced=False),
            mount=M.ProfileMount(
                user_data_dir=user_data_dir, source="active_volume", profile_format_version=1
            ),
            policy=policy,
            activation_key=self.activation_key,
            initial_fencing_token=self.fencing_token,
            sequence_base=self.sequence_base + 1,
            callback_url="stub://events",
            callback_token="cbt_" + uuid.uuid4().hex,
            display=display,
        )
        response = await self.worker.bootstrap(req, bearer=self._bearer("bootstrap"))
        if response.ok and response.accepted:
            await self.heartbeat()
        return response

    async def heartbeat(
        self, *, access_still_valid: bool = True, lease_seconds: int = 60
    ) -> M.HeartbeatResponse:
        req = M.HeartbeatRequest(
            **self._env(sequenced=False),
            lease_expires_at=_now() + timedelta(seconds=lease_seconds),
            access_still_valid=access_still_valid,
        )
        return await self.worker.heartbeat(req, bearer=self._bearer("heartbeat"))

    async def command(
        self,
        command: object,
        *,
        origin: str = "agent",
        page_id: str | None = None,
        sequence: int | None = None,
        idem: str | None = None,
    ) -> M.CommandResponse:
        req = M.CommandRequest(
            **self._env(sequenced=True, sequence=sequence, idem=idem),
            origin=origin,  # type: ignore[arg-type]
            page_id=page_id,
            command=command,  # type: ignore[arg-type]
        )
        return await self.worker.command(req, bearer=self._bearer("command"))

    async def observe(self, *, include: list[str] | None = None) -> M.ObserveResponse:
        req = M.ObserveRequest(
            **self._env(sequenced=False),
            include=include or ["pages", "dialogs", "downloads", "human_episode"],  # type: ignore[arg-type]
        )
        return await self.worker.observe(req, bearer=self._bearer("observe"))

    async def capture(
        self,
        *,
        kind: str = "screenshot",
        reason: str = "operator",
        page_id: str | None = None,
        return_base64: bool = True,
    ) -> M.CaptureResponse:
        req = M.CaptureRequest(
            **self._env(sequenced=True),
            kind=kind,  # type: ignore[arg-type]
            reason=reason,  # type: ignore[arg-type]
            page_id=page_id,
            return_base64=return_base64,
            redaction_policy_version="v1",
        )
        return await self.worker.capture(req, bearer=self._bearer("capture"))

    async def controller_transition(
        self,
        *,
        to_state: str,
        reason: str = "control_requested",
        handoff_id: str | None = None,
        controller_ref: str | None = None,
        enable_human_input: bool = False,
        bump_revision: int = 1,
        new_fencing_token: str | None = None,
    ) -> M.ControllerTransitionResponse:
        new_rev = self.fencing_revision + bump_revision
        new_token = new_fencing_token or f"ft_{uuid.uuid4().hex}"
        req = M.ControllerTransitionRequest(
            **self._env(sequenced=True),
            to_state=to_state,  # type: ignore[arg-type]
            reason=reason,
            new_fencing_token=new_token,
            new_fencing_revision=new_rev,
            controller_ref=controller_ref,
            handoff_id=handoff_id,
            enable_human_input=enable_human_input,
        )
        resp = await self.worker.controller_transition(
            req, bearer=self._bearer("controller_transition")
        )
        # On success the manager adopts the new fence it just issued.
        if resp.ok and not resp.replayed:
            self.fencing_token = new_token
            self.fencing_revision = new_rev
        return resp

    async def checkpoint(
        self,
        *,
        checkpoint_id: str | None = None,
        mode: str = "close_and_archive",
        reason: str = "stop",
    ) -> M.CheckpointResponse:
        import base64
        import os

        req = M.CheckpointRequest(
            **self._env(sequenced=True),
            checkpoint_id=checkpoint_id or uuid.uuid4().hex,
            mode=mode,  # type: ignore[arg-type]
            reason=reason,  # type: ignore[arg-type]
            dek_plaintext_b64=base64.b64encode(os.urandom(32)).decode("ascii"),
            dek_wrapped_b64=base64.b64encode(b"wrapped-by-kms").decode("ascii"),
            key_version="k1",
            nonce_b64=base64.b64encode(os.urandom(12)).decode("ascii"),
            archive_format_version=1,
            upload_target=M.PresignedUpload(
                method="PUT", url="stub://put", expires_at=_now() + timedelta(minutes=5)
            ),
        )
        return await self.worker.checkpoint(req, bearer=self._bearer("checkpoint"))

    async def shutdown(self, *, reason: str = "normal_stop") -> M.ShutdownResponse:
        req = M.ShutdownRequest(**self._env(sequenced=True), reason=reason)  # type: ignore[arg-type]
        return await self.worker.shutdown(req, bearer=self._bearer("shutdown"))

    # ── a raw envelope escape hatch for adversarial conformance cases ───────

    def raw_command_request(self, command: object, **overrides: object) -> M.CommandRequest:
        env = self._env(sequenced=True)
        env.update(overrides)  # type: ignore[arg-type]
        return M.CommandRequest(origin="agent", command=command, **env)  # type: ignore[arg-type]
