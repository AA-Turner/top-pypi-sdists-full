"""MetadataMixin, Run's methods: describe the run -- tags, foreign-key links, metric expectations,
ambient unit/context labels."""

from __future__ import annotations
from typing import Any

from ...foundation.safe_warn import safe_warn as _diagnostics
from .context.context import FailureContext, UnitContext


class MetadataMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    # -- below-run coordinates ----------------------------------------------
    def unit(
        self,
        *,
        coords: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
    ) -> UnitContext:
        """Ambient coordinate context for everything logged inside the block::

            with run.unit(coords={"rank": 0}, labels={"sample": 3}):
                run.log({"loss": 0.42}, step=12)   # dimensions/labels merged in
                with run.unit(labels={"uid": "p1"}):
                    ...                            # nested: child = parent ∪ child

        ``coords`` are the bounded grouping axes (SERIES identity: rank/split/...,
        never a per-sample id and never the step axis — an ambient coord is applied
        to EVERY point in the block, so a per-sample one shreds the block into
        one-point series, see :meth:`log`); ``labels`` are unbounded per-sample
        drill-down ids (POINT identity only). Nested units merge with
        the child winning per key; a key may not end up in both maps
        (``ValueError``, mirroring the server's 422). The context is contextvar-
        scoped: thread- and asyncio-task-local, restored on exit, and folded into
        payloads at call time so spooled writes replay with the coordinate that
        was ambient when the value was produced."""
        return UnitContext(coords=coords, labels=labels, run_id=self.id)

    def context(self, **ids: Any) -> FailureContext:
        """Name what the block is processing, for crash reports ONLY::

            for epoch in range(epochs):
                for i, batch in enumerate(loader):
                    with run.context(batch_id=i, epoch=epoch):
                        train_step(batch)   # its run.log() calls are unchanged

        If the block raises, the run's crash report -- and the crash email --
        names the batch, sample or epoch it died on. Unlike :meth:`unit`,
        nothing is stamped onto what is logged inside: no dimensions, no
        labels, so every curve plots exactly as it would without the block.

        Keys: ``batch_id``, ``sample_id`` (also ``sample``/``example_id``/
        ``row_id``), ``task_id``, ``prompt_id``, ``epoch``, ``step``,
        ``split``, ``phase``, ``dataset``, ``model``. Values are ints or
        strings; any other value, and any other key, is dropped. Nested blocks
        merge with the inner one winning per key, and exit restores the outer
        state (thread- and asyncio-task-local). No I/O, never raises: cheap
        enough to enter once per batch."""
        return FailureContext(self.id, ids)

    # -- tags ----------------------------------------------------------------
    @property
    def tags(self) -> list[str]:
        return list(self._data.get("tags") or [])

    def set_tags(self, tags: list[str], *, strict: bool | None = None):
        """REPLACE the run's whole tag list ([] clears). The server normalizes
        to lowercase-kebab and 422s past the caps (CONTRACT.md "tags").
        Granular add/remove is the CLI ``probe run tag`` verb's
        read-modify-write job, not a server op.

        A pre-0066 backend would silently drop the field and 200 the old row;
        the response is verified so that no-op cannot masquerade as success.
        A spooled fail-open write returns None (unverifiable until flush).

        sync=True: that verification is the whole point of the method, and it
        only runs on a returned row -- under async this write journals, `data`
        is None, and the guard silently never fires for the SDK callers it was
        written for. `run.tags` would also keep reporting the pre-write list.
        One tag write per run is not loop traffic, so the round trip is free
        in the only sense that matters here."""
        data = self._client.write(
            "PATCH", f"/v1/runs/{self.id}", {"tags": list(tags)}, strict=strict, sync=True
        )
        if data:
            self._client._verify_tags_written(list(tags), data, "PATCH /v1/runs/{id}")
            self._data = data
        return data

    # -- foreign keys (shadow-SoT handles) ----------------------------------
    def link(self, *, strict: bool | None = None, **foreign_keys: Any):
        """Attach foreign keys (wandb_run_id, mlflow_run_id, s3_prefix, ...) to the
        real ``runs.foreign_keys`` column (fold #8). The server merges per-key
        new-wins via RunPatch, so a late-discovered id attaches without clobbering
        earlier keys and no read-modify-write round-trip is needed."""
        data = self._client.write(
            "PATCH", f"/v1/runs/{self.id}", {"foreign_keys": foreign_keys}, strict=strict
        )
        if data:
            self._data = data
        return data

    # -- declared metric ranges (0263) ----------------------------------------
    def expect(self, ranges: dict[str, Any], *, strict: bool | None = None):
        """Declare where metrics should stay; Probe emails you when one leaves.

        ::

            run.expect({
                "val/acc": (0.5, 1.0),      # email if it goes below 0.5 or above 1
                "train/loss": (None, 20),   # None = no limit on that side
            })

        OPTIONAL AND ADDITIVE. Call it once after the run opens -- before the
        training loop is the natural place -- or at any time later: every value
        already logged for the key is judged too. Calling it again adds or
        changes ranges (an unchanged range keeps its alert state, so a relaunch
        does not re-send an email); ``{"key": None}`` removes one. A range covers
        every series of that key (all ranks and coordinates).

        IT NEVER BREAKS THE SCRIPT: a malformed entry is dropped with a warning,
        and delivery is fail-open like :meth:`log` unless ``strict=True``.
        Returns the server's run row, or None when nothing was sent."""
        from .context import expectations as _expectations

        wire, problems = _expectations.normalize(ranges)
        if strict and problems:
            # The CLI asked: a range it cannot record is an error, not a warning.
            raise ValueError("; ".join(problems))
        try:
            # `_diagnostics.warn`, never `warnings.warn`: under `-W error` a plain
            # warning RAISES, and an optional add-on must not end a training run.
            for problem in problems:
                _diagnostics.warn(f"probe.expect: dropped {problem}", stacklevel=2)
            if not wire:
                return None
            data = self._client.write(
                "PATCH",
                f"/v1/runs/{self.id}",
                {"metric_expectations": wire},
                strict=strict,
            )
        except Exception as exc:  # noqa: BLE001 -- an optional add-on cannot break the run
            if strict:
                raise
            _diagnostics.warn(f"probe.expect: not recorded ({exc})", stacklevel=2)
            return None
        if data:
            self._data = data
        return data
