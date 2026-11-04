"""RunWritersMixin, Client's methods: a run's heartbeats and writer leases: beat, release, list,
report a writer gone (twin: app/runs)."""

from __future__ import annotations

from ....delivery.transport.deadlines import disable_retries


class RunWritersMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def heartbeat_run(
        self,
        run_id: str,
        role: str = "owner",
        *,
        attached: bool = False,
        write_epoch: int | None = None,
        delivery: dict | None = None,
    ) -> dict:
        """``POST /v1/runs/{id}/heartbeat``: report that this run is still alive.
        ``delivery``: this run's backlog, as the body's ``delivery`` (R13); a server that predates
        it ignores the body.

        Liveness cannot be inferred from `status`: it is a plain column, so a run
        whose process dies without a final PATCH stays 'running' forever and any
        "what is active" count decays into noise. Call this periodically while a
        run executes; the server's reaper marks an OWNER that stops beating as
        'crashed', and a run that goes silent without ever having had an owner
        beat as 'untracked'.

        ``role`` keeps the ownership rule honest. ``owner`` (the default)
        asserts "the run's process is alive" and may only be sent by a process
        whose lifetime IS the run's lifetime -- beat for the run's whole life or
        not at all. ``observer`` asserts only "something is still watching"
        (the miles exporter sidecar): it keeps the run out of the reaper's scan
        while attached, but its silence resolves to 'untracked', never
        'crashed', because a watcher dying proves nothing about the work.

        SDK handles beat automatically: ``create_run`` starts a background
        thread (see :meth:`Run.start_heartbeat`) unless called with
        ``heartbeat=False``. Call this method directly only for runs managed
        outside the SDK — e.g. a workflow driver renewing the lease on a run it
        opened with ``probe run start``.

        Only a 'running' run is stamped; a late beat racing a normal completion
        is a no-op rather than an error.
        """
        if role not in ("owner", "observer"):
            # The beat loop swallows exceptions; a typo'd role would 422
            # silently forever. Fail at the call site instead.
            raise ValueError(f"heartbeat role must be 'owner' or 'observer', got {role!r}")
        # Fencing (0185): the epoch rides as a query param (this route has no
        # body); a pre-0185 server drops it, a 0185+ one 409s a superseded
        # writer so the zombie learns it lost.
        params: dict = {}
        if role != "owner":
            params["role"] = role
        # 0205. `attached` says this beat comes from INSIDE the work, not from a
        # launcher holding the run open around it. Only these stamp attached_at,
        # which is how "the job never plugged in" stays expressible under a
        # wrapped run where both processes beat as owners. Omitted when false so
        # a pre-0205 server sees exactly the request it saw before.
        if attached:
            params["attached"] = "true"
        if write_epoch is not None:
            params["write_epoch"] = write_epoch
        body = {"delivery": delivery} if delivery else None
        # Sent once (I14): the next beat is its retry; retried inline, an outage cost 4 per beat.
        with disable_retries():
            if params:
                return self.transport.request(
                    "POST",
                    f"/v1/runs/{run_id}/heartbeat",
                    params=params,
                    json_body=body,
                    idempotent=True,
                ).json()
            return self.transport.post(f"/v1/runs/{run_id}/heartbeat", body, idempotent=True)

    def beat_writer(self, run_id: str, session_id: str, body: dict) -> dict:
        """``POST /v1/runs/{id}/writers/{session}/beat`` (SDK reliability 2.8):
        one lease beat. The first registers the lease. Returns
        ``{run_status, write_epoch, liveness_protocol}``; a 409 means a newer
        attempt took the run over. Sent once (I14): the next beat is its retry."""
        with disable_retries():
            return self.transport.post(
                f"/v1/runs/{run_id}/writers/{session_id}/beat", body, idempotent=True
            ) or {}

    def release_writer(self, run_id: str, session_id: str, body: dict) -> dict:
        """``POST /v1/runs/{id}/writers/{session}/release`` (2.8): this writer
        is done with ``exit_status``; the server closes the run once its leases
        say the work ended. Idempotent per session. Returns ``{run_status,
        closed, liveness_protocol}``."""
        return self.transport.post(
            f"/v1/runs/{run_id}/writers/{session_id}/release", body, idempotent=True
        ) or {}

    def list_writers(self, run_id: str) -> list[dict]:
        """``GET /v1/runs/{id}/writers`` (2.8): the run's writer leases, newest
        epoch first, each with its derived ``state`` (beating, draining,
        released, gone, expired) and whether it is on the ``current`` epoch."""
        return self.transport.get(f"/v1/runs/{run_id}/writers") or []

    def report_writer_gone(self, run_id: str, body: dict) -> dict:
        """``POST /v1/runs/{id}/writer-gone`` (SDK reliability 2.2): tell the
        server this run's writer process is gone, so a sole-writer run ends
        `crashed` in seconds rather than after the reaper's 900 s. Sent by the
        output helper's reporter and the node agent, never by the writer
        itself; only after ``supports_feature("run_writer_gone")``. Returns
        ``{run_id, applied, status, reason}``."""
        resp = self.transport.request("POST", f"/v1/runs/{run_id}/writer-gone", json_body=body)
        return resp.json() if resp.content else {}
