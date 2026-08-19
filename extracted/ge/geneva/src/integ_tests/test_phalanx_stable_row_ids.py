# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""
Measure stable-row-id behavior of rest-namespace (phalanx) table creates.

These tests measure — against a live phalanx server — whether the per-call
``new_table_enable_stable_row_ids`` storage option survives the full create
path (geneva ``Connection.create_table`` → lancedb namespace connection →
client-side Lance write with vended credentials), and pin the remaining known
gap:

- ENT-2106: enterprise MV creates dispatch to phalanx's
  ``create_materialized_view``, which writes the MV table with default write
  params, bypassing the client-side option entirely.

Conventions shared by all tests:

- ``exist_ok`` is never passed: the rest namespace rejects geneva's
  exist_ok→mode fold (GEN-840).
- The option value is the string ``"true"``: storage options are string maps
  and boolean values are not portable across layers (GEN-869).
- Schemas are blob-free: blob columns force stable row IDs on in the lancedb
  create path, which would mask what these tests measure.

Requires a running phalanx (GENEVA_HOST_OVERRIDE / GENEVA_API_KEY); see
``make test-phalanx``.
"""

import logging
import os
import uuid

import lance
import pyarrow as pa
import pytest

from geneva import connect
from geneva.db import Connection, dataset_uses_stable_row_ids, has_stable_row_ids

_LOG = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.phalanx,
    pytest.mark.skipif(
        not os.getenv("GENEVA_HOST_OVERRIDE"),
        reason="requires a running phalanx (set GENEVA_HOST_OVERRIDE / GENEVA_API_KEY)",
    ),
]

_SRID_OPTION = {"new_table_enable_stable_row_ids": "true"}


class _KnownGapError(AssertionError):
    """The pinned known-gap condition was observed, and only that condition.

    Distinct from a plain ``AssertionError`` so the strict xfail below can be
    narrowed with ``raises=_KnownGapError``: an assertion raised anywhere else in
    the test body -- inside ``create_table``, ``open_table``,
    ``create_materialized_view`` or ``to_lance`` -- surfaces as a hard failure
    instead of a masked, meaningless XFAIL.
    """


@pytest.fixture(scope="module")
def phalanx_conn(session_db_uri: str, host_override: str, api_key: str) -> Connection:
    conn = connect(
        uri=session_db_uri,
        api_key=api_key,
        host_override=host_override,
    )
    # These tests measure the rest-namespace create path specifically; any
    # other impl means the environment is not exercising phalanx.
    assert conn.namespace_client_impl == "rest", (
        f"expected a rest namespace connection, got {conn.namespace_client_impl!r}"
    )
    return conn


def _sample_data(offset: int = 0, num_rows: int = 20) -> pa.Table:
    """Small blob-free table; blob columns would force stable row IDs on."""
    return pa.table(
        {
            "id": list(range(offset, offset + num_rows)),
            "text": [f"item_{i}" for i in range(offset, offset + num_rows)],
        }
    )


def _drop_quietly(conn: Connection, name: str) -> None:
    """Best-effort table drop; cleanup must not mask the test outcome."""
    try:
        conn.drop_table(name)
    except Exception:
        _LOG.warning("Failed to drop table %s during cleanup", name)


def _row_id_mapping(ds: lance.LanceDataset) -> dict[int, int]:
    """Map each ``id`` value to its Lance row id."""
    data = ds.to_table(columns=["id"], with_row_id=True)
    ids = data.column("id").to_pylist()
    row_ids = data.column("_rowid").to_pylist()
    return dict(zip(ids, row_ids, strict=True))


def _assert_ids_preserved(
    baseline: dict[int, int], current: dict[int, int], step: str
) -> None:
    """Every row in ``baseline`` keeps its row id in ``current``.

    Compares only the baseline ids, so rows added after the baseline was taken
    are ignored; a baseline id that vanished fails too, since the restriction
    then has fewer entries than the baseline.
    """
    kept = {k: v for k, v in current.items() if k in baseline}
    assert kept == baseline, f"id→_rowid mapping changed across {step}"


def test_create_table_with_stable_row_ids_via_rest_namespace(
    phalanx_conn: Connection,
) -> None:
    """Per-call SRID option on a rest-namespace create yields a SRID dataset.

    The option must survive every layer: geneva forwards it to the lancedb
    namespace connection, whose Rust client applies it to the client-side
    Lance write before vended credentials replace the storage options. Both
    detection paths geneva relies on must agree: the dataset manifest flag
    and per-fragment row_id_meta.
    """
    name = f"srid_{uuid.uuid4().hex[:8]}"
    try:
        tbl = phalanx_conn.create_table(
            name,
            _sample_data(),
            storage_options=dict(_SRID_OPTION),
        )
        ds = tbl.to_lance()
        assert dataset_uses_stable_row_ids(ds), (
            "manifest flag not set: new_table_enable_stable_row_ids was "
            "dropped between geneva and the Lance write"
        )
        assert has_stable_row_ids(list(ds.get_fragments())), (
            "no fragment carries row_id_meta despite the manifest flag"
        )
    finally:
        _drop_quietly(phalanx_conn, name)


def test_create_table_without_option_has_no_stable_row_ids(
    phalanx_conn: Connection,
) -> None:
    """Negative control: without the option the dataset lacks stable row IDs.

    Proves the positive test measures the per-call option rather than a
    server or connection default. A failure here means a default flipped
    somewhere in the stack and the positive test is vacuous.
    """
    name = f"srid_off_{uuid.uuid4().hex[:8]}"
    try:
        tbl = phalanx_conn.create_table(name, _sample_data())
        ds = tbl.to_lance()
        assert not dataset_uses_stable_row_ids(ds), (
            "stable row IDs enabled without requesting them: a default "
            "changed server-side or in lancedb"
        )
        assert not has_stable_row_ids(list(ds.get_fragments()))
    finally:
        _drop_quietly(phalanx_conn, name)


def test_supports_stable_row_ids_on_create_reports_rest_supported(
    phalanx_conn: Connection,
) -> None:
    """The capability gate must match measured reality for rest namespaces.

    The create path honors the option (see
    test_create_table_with_stable_row_ids_via_rest_namespace), so Geneva must
    report that tables it creates internally can request stable row IDs on rest
    connections.
    """
    assert phalanx_conn._supports_stable_row_ids_on_create() is True


@pytest.mark.xfail(
    strict=True,
    raises=_KnownGapError,
    reason="ENT-2106: phalanx create_materialized_view writes the MV table "
    "with WriteParams::default(), so enterprise MV tables never get stable "
    "row IDs",
)
def test_materialized_view_table_gets_stable_row_ids(
    phalanx_conn: Connection,
) -> None:
    """An MV over a stable-row-id source should itself get stable row IDs.

    On remote (db://) connections MV creation dispatches to phalanx's
    ``create_materialized_view`` endpoint, which writes the MV table
    server-side with default write params — the client-side stable-row-id
    request never reaches that write. Strict xfail: a phalanx-side fix turns
    this into a loud XPASS and the marker must be removed.
    """
    src_name = f"srid_mv_src_{uuid.uuid4().hex[:8]}"
    mv_name = f"srid_mv_{uuid.uuid4().hex[:8]}"
    try:
        phalanx_conn.create_table(
            src_name,
            _sample_data(),
            storage_options=dict(_SRID_OPTION),
        )
        src = phalanx_conn.open_table(src_name)
        mv = phalanx_conn.create_materialized_view(mv_name, src.search())
        # The MV table starts empty (with_no_data=True), so only the
        # manifest flag is checked — there are no fragments yet.
        if not dataset_uses_stable_row_ids(mv.to_lance()):
            raise _KnownGapError("MV table created without stable row IDs")
    finally:
        _drop_quietly(phalanx_conn, mv_name)
        _drop_quietly(phalanx_conn, src_name)


def test_row_ids_stable_across_append_and_compaction(
    phalanx_conn: Connection,
) -> None:
    """Row IDs assigned at creation survive appends and compaction.

    The baseline is the mapping at create time, so each append is checked too:
    an append that remapped pre-existing rows fails here rather than being
    folded into a post-append baseline. Compaction rewrites fragments; with
    stable row IDs the id→_rowid mapping must be unchanged afterwards.
    Compaction runs client-side through the namespace connection; a server that
    rejects client-side compaction on managed tables fails loudly here rather
    than skipping, so the gap stays visible.
    """
    name = f"srid_compact_{uuid.uuid4().hex[:8]}"
    try:
        tbl = phalanx_conn.create_table(
            name,
            _sample_data(),
            storage_options=dict(_SRID_OPTION),
        )
        mapping_at_create = _row_id_mapping(tbl.to_lance())
        assert mapping_at_create, "create produced no rows to track"

        # Managed versioning applies weak read consistency; re-checkout after
        # each write so the mapping below is read from the version that
        # includes it, and not vacuously from a pre-append snapshot.
        tbl.add(_sample_data(offset=100))
        tbl.checkout_latest()
        after_first = _row_id_mapping(tbl.to_lance())
        assert 100 in after_first, "first append not visible in the read version"
        _assert_ids_preserved(mapping_at_create, after_first, "the first append")

        tbl.add(_sample_data(offset=200))
        tbl.checkout_latest()
        ds = tbl.to_lance()
        mapping_before = _row_id_mapping(ds)
        assert 200 in mapping_before, "second append not visible in the read version"
        _assert_ids_preserved(mapping_at_create, mapping_before, "the second append")

        fragments_before = len(ds.get_fragments())
        assert fragments_before >= 2, "appends did not create extra fragments"

        try:
            tbl.compact_files()
        except Exception as exc:
            pytest.fail(
                "client-side compact_files rejected on a rest-namespace "
                f"table; row-id durability cannot be measured: {exc}"
            )

        tbl.checkout_latest()
        ds = tbl.to_lance()
        assert len(ds.get_fragments()) < fragments_before, (
            "compaction was a no-op; the row-id stability assertion below "
            "would be vacuous"
        )
        assert _row_id_mapping(ds) == mapping_before, (
            "id→_rowid mapping changed across compaction"
        )
        assert has_stable_row_ids(list(ds.get_fragments()))
    finally:
        _drop_quietly(phalanx_conn, name)
