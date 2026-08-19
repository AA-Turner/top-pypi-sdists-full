# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Surplus tuning knobs surviving the remote (``db://``) dispatch.

The namespace request declares the knobs that existed when its schema was
generated. Everything since works locally and vanishes remotely -- the
generated model defaults to pydantic's ``extra="ignore"``, so an unknown key
is dropped at construction with no error, and the job runs misconfigured.

The server side already carries unknown scalar keys through to the driver's
``backfill()``/``refresh()`` call (sophon ENT-2133), so the only thing missing
is putting them on the wire. These tests pin that: which keys go, which are
held back, and that they survive the client's real serialization path.
"""

from __future__ import annotations

import pytest
from lance_namespace import AlterTableBackfillColumnsRequest

from geneva.utils.remote_options import (
    forwardable_remote_options,
    request_model_with_options,
)


class TestForwardableOptions:
    @staticmethod
    def _options(reserved=(), **kwargs) -> dict:  # noqa: ANN001, ANN003
        return forwardable_remote_options(kwargs, reserved=reserved)

    def test_forwards_a_knob(self) -> None:
        assert self._options(output_row_bytes=153600) == {"output_row_bytes": 153600}

    def test_forwards_scalars_of_each_kind(self) -> None:
        assert self._options(
            task_size=64, update_mode="sparse", ratio=0.5, enabled=True
        ) == {
            "task_size": 64,
            "update_mode": "sparse",
            "ratio": 0.5,
            "enabled": True,
        }

    def test_skips_keys_already_on_the_request(self) -> None:
        """Declared fields are sent explicitly; re-sending them as surplus
        would give the server two sources for one knob."""
        assert (
            forwardable_remote_options({"task_size": 64}, reserved={"task_size"}) == {}
        )

    def test_skips_none(self) -> None:
        """An unset knob is absence, not an instruction to override."""
        assert self._options(output_row_bytes=None) == {}

    def test_a_brand_new_knob_needs_no_edit_here(self) -> None:
        """The point of a denylist. A knob added to backfill() reaches the
        remote driver without anyone remembering to register it -- an
        allowlist would silently drop it, which is the bug being fixed."""
        assert self._options(some_knob_invented_tomorrow=7) == {
            "some_knob_invented_tomorrow": 7
        }

    def test_holds_back_storage_options(self) -> None:
        """Credentials must never leave the client, and storage_options is
        where they live."""
        assert self._options(storage_options={"account_key": "secret"}) == {}

    def test_holds_back_underscore_prefixed_knobs(self) -> None:
        """Not because they are private -- they are Geneva's experimental
        knobs, and real tuning. The server's validate_key requires an ASCII
        lowercase first character and answers anything else with a 400 for the
        whole request, so sending one would fail the backfill rather than lose
        the flag."""
        assert self._options(_skip_planner_filter_count=True) == {}
        assert self._options(_skip_checkpoint_index_scan=True) == {}

    @pytest.mark.parametrize("name", ["col_name", "column_name", "job_id", "udf"])
    def test_holds_back_names_the_server_reserves(self, name: str) -> None:
        """phalanx BACKFILL_RESERVED_KEYS: it 400s these rather than ignoring
        them, so a caller passing one would lose the whole job."""
        assert self._options(**{name: "x"}) == {}

    def test_holds_back_an_oversized_value(self) -> None:
        """MAX_VALUE_LEN is 1024 server-side, and over it is a 400."""
        assert self._options(note="x" * 1025) == {}
        assert self._options(note="x" * 1024) == {"note": "x" * 1024}

    def test_holds_back_driver_owned_names(self) -> None:
        assert self._options(job_id="abc", udf="x", column="blob") == {}

    def test_holds_back_non_scalars(self) -> None:
        """The server takes scalars only, and a local object means nothing
        remotely anyway."""
        assert self._options(checkpoint=object(), frags=[1, 2]) == {}

    def test_holds_back_names_the_server_would_reject(self) -> None:
        """Rejected keys 400 the whole request, so they stay local rather than
        failing a job over a knob."""
        assert self._options(**{"Upper": 1, "has-dash": 1, "x" * 65: 1}) == {}
        # Python accepts these as identifiers; phalanx's ASCII rule does not.
        assert self._options(**{"café": 1, "9lives": 1}) == {}


class TestExtrasReachTheWire:
    """Allowing extras is the half that pydantic would otherwise undo."""

    def test_generated_model_silently_drops_unknown_keys(self) -> None:
        """The bug this exists for: no error, just a missing knob."""
        request = AlterTableBackfillColumnsRequest(
            id=["t"], column="blob", output_row_bytes=153600
        )
        assert not hasattr(request, "output_row_bytes")
        assert "output_row_bytes" not in request.to_dict()

    def test_options_model_keeps_them(self) -> None:
        cls = request_model_with_options(AlterTableBackfillColumnsRequest)
        request = cls(id=["t"], column="blob", output_row_bytes=153600)
        assert request.to_dict()["output_row_bytes"] == 153600

    def test_declared_fields_still_bind_normally(self) -> None:
        cls = request_model_with_options(AlterTableBackfillColumnsRequest)
        request = cls(id=["t"], column="blob", task_size=64, output_row_bytes=1)
        assert request.task_size == 64
        assert request.to_dict()["task_size"] == 64

    def test_extras_survive_the_client_serializer(self) -> None:
        """``to_dict()`` is not the wire format -- the generated client runs
        its own serializer, and the key has to survive that too."""
        from lance_namespace_urllib3_client.api_client import ApiClient

        cls = request_model_with_options(AlterTableBackfillColumnsRequest)
        request = cls(id=["t"], column="blob", output_row_bytes=153600)
        body = ApiClient().sanitize_for_serialization(request)
        assert body["output_row_bytes"] == 153600

    def test_subclass_is_reused(self) -> None:
        """Built once per request class; a fresh type per call would defeat
        pydantic's schema cache."""
        assert request_model_with_options(
            AlterTableBackfillColumnsRequest
        ) is request_model_with_options(AlterTableBackfillColumnsRequest)


@pytest.mark.parametrize(
    "knob",
    [
        "output_row_bytes",
        "memory",
        "batch_size",
        "skip_frags",
        "task_shuffle_diversity",
        "update_mode",
    ],
)
def test_known_knobs_the_schema_does_not_declare_are_forwarded(knob: str) -> None:
    """Regression net: these are real ``backfill()`` arguments absent from the
    namespace schema today, and each was silently dropped remotely."""
    assert knob not in AlterTableBackfillColumnsRequest.model_fields
    assert forwardable_remote_options({knob: 1}, reserved=()) == {knob: 1}


class TestTransportOwnedFieldsAreReserved:
    """The bag tunes execution; it must not be able to steer the operation.

    Extras bind to a declared field when the model has one, so a name like
    ``branch`` would arrive as routing rather than tuning -- changing *where*
    the write lands through a channel meant only for *how* it runs.
    """

    @staticmethod
    def _reserved(request_cls) -> set:  # noqa: ANN001, ANN205
        return set(request_cls.model_fields)

    def test_branch_cannot_ride_the_bag(self) -> None:
        assert "branch" in AlterTableBackfillColumnsRequest.model_fields
        options = forwardable_remote_options(
            {"branch": "other"},
            reserved=self._reserved(AlterTableBackfillColumnsRequest),
        )
        assert options == {}

    def test_declared_field_never_becomes_an_extra(self) -> None:
        """Anything the schema declares travels as a declared field or not at
        all -- never as a surplus key alongside it."""
        for name in AlterTableBackfillColumnsRequest.model_fields:
            assert (
                forwardable_remote_options(
                    {name: "x"},
                    reserved=self._reserved(AlterTableBackfillColumnsRequest),
                )
                == {}
            )

    def test_routing_survives_a_real_dispatch(self, monkeypatch) -> None:  # noqa: ANN001
        """End of the chain: a caller passing ``branch`` does not move the
        write, while a real knob alongside it still travels."""
        request = TestRefreshDispatchForwardsOptions._captured_request(
            monkeypatch, branch="other", task_size=64
        )
        body = request.to_dict()
        assert body.get("branch") is None
        assert body["task_size"] == 64


class TestRefreshDispatchForwardsOptions:
    """Refresh drops surplus knobs the same way backfill did.

    ``refresh``/``refresh_async`` both take ``**kwargs`` and, on the remote
    path, handed none of it to the dispatcher -- so a knob reached Ray locally
    and evaporated over ``db://``.
    """

    @staticmethod
    def _captured_request(monkeypatch, **refresh_kwargs):  # noqa: ANN001, ANN205
        """Drive ``_refresh_async_remote`` and return the request it built."""
        from lance_namespace import RefreshMaterializedViewResponse

        from geneva.table import Table

        captured = {}

        class _Namespace:
            def refresh_materialized_view(self, request):  # noqa: ANN001, ANN202
                captured["request"] = request
                return RefreshMaterializedViewResponse(job_id="job-1")

        class _History:
            def launch(self, *a, **k) -> None:  # noqa: ANN002, ANN003
                pass

        class _Conn:
            _history = _History()

            def namespace_client(self):  # noqa: ANN202
                return _Namespace()

        table = object.__new__(Table)
        object.__setattr__(table, "_conn", _Conn())
        object.__setattr__(table, "_table_id", ["t"])
        object.__setattr__(table, "_name", "t")

        monkeypatch.setattr(
            "geneva.jobs.remote.RemoteJob", lambda **k: object(), raising=False
        )
        monkeypatch.setattr(
            "geneva.remote_v2.RemoteJobFuture", lambda job: object(), raising=False
        )
        Table._refresh_async_remote(table, **refresh_kwargs)
        return captured["request"]

    def test_surplus_knob_reaches_the_request(self, monkeypatch) -> None:  # noqa: ANN001
        request = self._captured_request(monkeypatch, batch_size=4096)
        assert request.to_dict()["batch_size"] == 4096

    def test_declared_knobs_still_bind(self, monkeypatch) -> None:  # noqa: ANN001
        request = self._captured_request(monkeypatch, concurrency=16, batch_size=4096)
        assert request.concurrency == 16

    def test_no_surplus_leaves_the_plain_model(self, monkeypatch) -> None:  # noqa: ANN001
        """No extras means no subclass -- unchanged behavior when nothing new
        is passed."""
        from lance_namespace import RefreshMaterializedViewRequest

        request = self._captured_request(monkeypatch, concurrency=8)
        assert type(request) is RefreshMaterializedViewRequest

    def test_credentials_never_ride_along(self, monkeypatch) -> None:  # noqa: ANN001
        request = self._captured_request(
            monkeypatch, storage_options={"account_key": "secret"}
        )
        assert "storage_options" not in request.to_dict()
        assert "secret" not in str(request.to_dict())


class TestRefreshEntryPointsThreadKwargs:
    """The dispatcher forwarding surplus keys is useless if its callers eat
    them first -- both entry points took ``**kwargs`` and passed none of it."""

    @staticmethod
    def _dispatch_kwargs(monkeypatch, method: str, **call_kwargs):  # noqa: ANN001, ANN205
        from geneva.table import Table

        captured = {}

        class _Job:
            def result(self, timeout=None):  # noqa: ANN001, ANN202
                return "done"

        def _fake_remote(self, **kwargs):  # noqa: ANN001, ANN003, ANN202
            captured.update(kwargs)
            return _Job()

        class _Conn:
            def use_remote_dispatch(self) -> bool:
                return True

        table = object.__new__(Table)
        object.__setattr__(table, "_conn", _Conn())
        monkeypatch.setattr(Table, "_refresh_async_remote", _fake_remote)
        monkeypatch.setattr(Table, "checkout_latest", lambda self: None)
        getattr(Table, method)(table, **call_kwargs)
        return captured

    def test_refresh_async_forwards_surplus(self, monkeypatch) -> None:  # noqa: ANN001
        captured = self._dispatch_kwargs(monkeypatch, "refresh_async", batch_size=4096)
        assert captured.get("batch_size") == 4096

    def test_refresh_forwards_surplus(self, monkeypatch) -> None:  # noqa: ANN001
        captured = self._dispatch_kwargs(monkeypatch, "refresh", batch_size=4096)
        assert captured.get("batch_size") == 4096
