# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Exercise the hierarchical checkpoint store against real Azure storage.

Regression coverage for GEN-645: the driver-side identity sidecar write and
read (``ensure_identity_sidecar`` -> ``_write_identity_if_missing`` ->
``session.upload_file``; ``_read_identity`` -> ``session.download_file``) and
the cleanup delete path (``delete_prefix`` -> ``_purge_one`` ->
``session.delete_file``) must succeed on Azure Blob storage without requiring
hierarchical-namespace (HNS) support.

PyArrow's ``AzureFileSystem`` probes the ``dfs.core.windows.net`` endpoint
on directory-semantic operations and stream opens. On flat (non-HNS) accounts,
or when that endpoint is unreachable, the probe used to abort the backfill even
though the blob write would have succeeded; checkpoint I/O — sidecar
read/write, bf-dir enumeration (``list_with_delimiter``), and deletes
(``delete_file``) — therefore routes through the blob-only object_store session
instead (GEN-645/GEN-658/GEN-661).

The *deterministic* regression guard for GEN-645 is the unit suite in
``src/tests/test_checkpoint.py``:

* ``test_v2_identity_sidecar_uses_object_store_not_pyarrow_fs``
* ``test_v2_iter_bf_identities_enumerates_blob_only_no_pyarrow_fs``
* ``test_v2_list_bf_dir_leaves_scope_not_doubled_in_namespace_mode``

They sabotage ``filesystem_from_uri`` so any PyArrow fs use raises, fail on
the pre-fix code, and run on every PR with no cloud. This live test is
complementary: it exercises real blob I/O end to end but can only *reproduce*
the original failure when the target account's ``dfs`` endpoint is actually
unreachable. On a shared dev account with a reachable ``dfs`` the probe simply
succeeds and even the pre-fix code passes — so a green run here is a smoke test,
not the regression guard. Point it at a flat / dfs-blocked account
(``GENEVA_AZURE_CKP_URI``) to make it reproduce the failure.

Runs only when the integ suite targets Azure (``--csp azure``). Point it at
a specifically **flat / non-HNS** account (or one whose ``dfs`` endpoint is
blocked) to faithfully reproduce the original failure — set
``GENEVA_AZURE_CKP_URI`` to override the default integ bucket. Authentication
follows ``filesystem_from_uri``: ``AZURE_STORAGE_ACCOUNT_NAME`` plus either
``AZURE_STORAGE_ACCOUNT_KEY`` or ``DefaultAzureCredential``.
"""

from __future__ import annotations

import logging
import os
import uuid

import pyarrow as pa
import pytest

from geneva.checkpoint import HierarchicalLanceCheckpointStore
from geneva.checkpoint_utils import hash_string

_LOG = logging.getLogger(__name__)


def _identity_prefix(seed: str) -> str:
    """A flat-key checkpoint prefix whose hashed segments let the
    hierarchical resolver recover the table- and identity-hash components.
    """
    return (
        f"udf-hns{seed}_ver-1_col-c"
        f"_where-{hash_string(f'where-{seed}')}"
        f"_uri-{hash_string(f'uri-{seed}')}"
        f"_srcfiles-{hash_string(f'srcfiles-{seed}')}"
    )


def _azure_storage_options() -> dict[str, str] | None:
    """Resolve Azure credentials from the environment, if present.

    ``None`` falls back to ``DefaultAzureCredential`` inside
    ``filesystem_from_uri``.
    """
    account_name = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
    opts: dict[str, str] = {}
    if account_name:
        opts["account_name"] = account_name
    if account_key:
        opts["account_key"] = account_key
    return opts or None


@pytest.mark.timeout(300)
def test_hierarchical_checkpoint_store_no_hns_required_on_azure(
    geneva_test_bucket: str,
    slug: str | None,
    csp: str,
) -> None:
    """Sidecar write, membership, scoped list, and cleanup all succeed on
    Azure Blob storage without HNS.
    """
    if csp != "azure":
        pytest.skip("Azure-only: exercises the AzureFileSystem HNS code path.")

    run_id = uuid.uuid4().hex[:8]
    isolation = f"{slug}-{run_id}" if slug else run_id
    # Override to target a specifically flat/non-HNS account to reproduce the
    # original GEN-645 failure mode; otherwise use the integ bucket.
    root = os.environ.get(
        "GENEVA_AZURE_CKP_URI", f"{geneva_test_bucket}/ckp-hns-{isolation}"
    )
    storage_options = _azure_storage_options()
    _LOG.info("azure HNS checkpoint test: root=%s", root)

    store = HierarchicalLanceCheckpointStore(root, storage_options=storage_options)
    identity = _identity_prefix(run_id)
    frag_key = f"{identity}_frag-0"
    range_key = f"{identity}_frag-0_range-0-100"
    batch = pa.RecordBatch.from_pydict({"x": [1]})

    try:
        # 1. Driver-side identity sidecar write: this is the exact call that
        #    aborted on a flat/unreachable-dfs account (create_dir + write).
        store.ensure_identity_sidecar(identity)

        # 2. Fragment + range checkpoint writes round-trip.
        store[frag_key] = batch
        store[range_key] = batch
        assert frag_key in store, "fragment checkpoint should be present"
        assert range_key in store, "range checkpoint should be present"

        # 3. Scoped listing returns exactly the keys for this identity.
        listed = sorted(store.list_keys(prefix=identity))
        assert listed == sorted([frag_key, range_key]), (
            f"scoped list_keys returned {listed!r}"
        )
    finally:
        # 4. Cleanup exercises the delete path (_purge_one ->
        #    session.delete_file), which is blob-only — no HNS probe.
        #    Best-effort teardown.
        try:
            store.delete_prefix(identity)
        except OSError:
            _LOG.warning("azure checkpoint cleanup failed for %s", root, exc_info=True)


@pytest.mark.timeout(60)
def test_azure_dfs_endpoint_blocked_when_asserted(csp: str) -> None:
    """Validity gate for the dfs-blocked FNS job (``make test-azure-fns-hns``).

    When ``GENEVA_AZURE_ASSERT_DFS_BLOCKED=1`` is set (the job blackholes the
    account's ``dfs.core.windows.net`` via ``docker --add-host``), confirm the
    dfs endpoint is actually unreachable while blob stays reachable. This makes
    a green run of the sidecar test above attributable to the fix rather than
    to dfs being silently reachable (the failure only reproduces when dfs is
    unreachable). Skipped everywhere else, including the normal ``--csp azure``
    integ job where dfs is reachable.
    """
    if os.environ.get("GENEVA_AZURE_ASSERT_DFS_BLOCKED") != "1":
        pytest.skip("only runs in the dfs-blocked FNS job")
    if csp != "azure":
        pytest.skip("Azure-only.")

    import socket

    account = os.environ["AZURE_STORAGE_ACCOUNT_NAME"]

    def _reachable(host: str) -> bool:
        sock = socket.socket()
        sock.settimeout(5)
        try:
            return sock.connect_ex((host, 443)) == 0
        finally:
            sock.close()

    assert not _reachable(f"{account}.dfs.core.windows.net"), (
        "dfs endpoint must be blackholed (docker --add-host) for this job to be "
        "a valid HNS-not-required test"
    )
    assert _reachable(f"{account}.blob.core.windows.net"), (
        "blob endpoint must stay reachable"
    )
