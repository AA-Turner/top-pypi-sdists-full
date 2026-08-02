# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Injectable committer for lance commits.

geneva's durable writes all call ``lance.LanceDataset.commit``. Routing them through a
``Committer`` read at call time lets a test swap one in. Production uses
``LanceCommitter`` (a pass-through to lance); tests install a fault-injecting one via
``set_committer`` / ``using_committer``. The fault implementations live in the external
``geneva_faults`` test library, not here.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any, Protocol

import lance

if TYPE_CHECKING:
    from collections.abc import Iterator


class Committer(Protocol):
    """Commits a lance operation/transaction; mirrors ``lance.LanceDataset.commit``.
    The keywords are the union geneva's commit sites use; each passes its own subset."""

    def commit(
        self,
        dataset_or_uri: Any,
        operation: Any,
        *,
        read_version: int | None = None,
        storage_options: dict[str, str] | None = None,
        namespace_client: Any = None,
        table_id: list[str] | None = None,
    ) -> lance.LanceDataset: ...


class LanceCommitter:
    """Production committer: forwards the supplied keywords (skipping ``None``) to
    ``lance.LanceDataset.commit``, so each call matches what the site issued before."""

    def commit(
        self,
        dataset_or_uri: Any,
        operation: Any,
        *,
        read_version: int | None = None,
        storage_options: dict[str, str] | None = None,
        namespace_client: Any = None,
        table_id: list[str] | None = None,
    ) -> lance.LanceDataset:
        kw: dict[str, Any] = {}
        if read_version is not None:
            kw["read_version"] = read_version
        if storage_options is not None:
            kw["storage_options"] = storage_options
        if namespace_client is not None:
            kw["namespace_client"] = namespace_client
        if table_id is not None:
            kw["table_id"] = table_id
        # write-guard-ok: this is the routed production default committer
        return lance.LanceDataset.commit(dataset_or_uri, operation, **kw)


# Process-global committer. Default is the real one; tests swap it.
_COMMITTER: Committer = LanceCommitter()


def get_committer() -> Committer:
    """The committer every durable mutation must go through."""
    return _COMMITTER


def set_committer(committer: Committer) -> None:
    """Install ``committer`` process-wide (test-only); pass a ``LanceCommitter`` to
    reset to production behavior."""
    global _COMMITTER
    _COMMITTER = committer


@contextlib.contextmanager
def using_committer(committer: Committer) -> Iterator[Committer]:
    """Install ``committer`` for the duration of the block, restoring the prior one."""
    prev = _COMMITTER
    set_committer(committer)
    try:
        yield committer
    finally:
        set_committer(prev)
