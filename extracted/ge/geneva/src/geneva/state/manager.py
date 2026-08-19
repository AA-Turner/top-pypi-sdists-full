# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import os
from abc import ABC, abstractmethod
from typing import Any

from lancedb.table import Table

from geneva.db import Connection

_LOG = logging.getLogger(__name__)


class BaseManager(ABC):
    """Abstract base class for Geneva table managers."""

    def __init__(
        self,
        genevadb: Connection,
        table_name: str | None = None,
        namespace: list[str] | None = None,
    ) -> None:
        """Initialize the manager with a database connection and table name.
           This will create the table if it does not exist, using the schema inferred
           from the provided model.

        Parameters
        ----------
            genevadb
                The Geneva database connection
            table_name
                The table name to use, or None to use the default
            from get_table_name()
            namespace
                Optional explicit namespace override. When None, the
            manager uses Geneva's default internal-table location.
        """
        table_name = table_name or self.get_table_name()
        self._table_name = table_name
        self.db, self._namespace, self.table = genevadb.alter_or_create_system_table(
            table_name,
            self.get_model(),
            namespace=namespace,
        )

    @abstractmethod
    def get_table_name(self) -> str:
        """Return the table name for this manager.

        Returns
        -------
            The table name
        """

    @abstractmethod
    def get_model(self) -> Any:
        """Return the model for this manager.

        Returns
        -------
            The model instance used to generate the schema
        """

    def get_table(self, checkout_latest: bool = False) -> Table:
        """Get the underlying Lance table.

        Parameters
        ----------
            checkout_latest
                Whether to checkout the latest version
            for strongly consistent reads.

        Returns
        -------
            The Lance table instance
        """
        # Re-open (which re-vends fresh credentials) when forced for
        # consistency, OR when the cached handle's vended credentials are near
        # expiry
        if (checkout_latest and _force_reopen_for_consistency()) or (
            self._vended_credentials_expiring()
        ):
            try:
                fresh = self.db.open_table(
                    self._table_name,
                    namespace_path=self._namespace,
                )
                _LOG.debug(
                    f"reopened table table_uri={fresh.uri} "
                    f"table_version={fresh.version}"
                )
                self.table = fresh
                return fresh._ltbl  # type: ignore[attr-defined]
            except Exception as e:
                _LOG.warning(
                    "BaseManager.get_table re-open failed for %s; "
                    "falling back to checkout_latest on cached handle: %s",
                    self._table_name,
                    e,
                )

        t = self.table._ltbl  # pyright: ignore[reportAttributeAccessIssue]
        if checkout_latest:
            # ensure strongly consistent reads
            t.checkout_latest()
        return t

    def _vended_credentials_expiring(self) -> bool:
        """True when the cached handle's vended S3 credentials are near expiry.

        No-op (``False``) for static credentials / tables that carry no
        ``expires_at_millis``; shared with the worker table cache so every
        long-lived handle uses the same expiry policy.
        """
        from geneva.credentials import table_handle_credentials_expiring

        return table_handle_credentials_expiring(self.table)

    def _refresh_credentials_on_error(self) -> None:
        """Re-open the system table so the next op re-vends fresh S3 creds.

        Invoked by ``@retry_lance`` when an operation fails with an
        expired-credential S3 error; re-opening goes through the namespace
        client, which vends a fresh token. Best-effort — a failed re-open leaves
        the cached handle in place for the retry's own error handling.
        """
        try:
            self.table = self.db.open_table(
                self._table_name,
                namespace_path=self._namespace,
            )
        except Exception:
            _LOG.warning(
                "BaseManager credential re-open failed for %s",
                self._table_name,
                exc_info=True,
            )


def _force_reopen_for_consistency() -> bool:
    """if true, ``get_table(checkout_latest=True)`` will re-open the
    table from the connection. If false, that will instead call
    ``checkout_latest()``.
    """
    val = os.environ.get("GENEVA_SYSTEM_TABLE_FORCE_REOPEN", "false")
    return val.strip().lower() not in ("false", "0", "no", "off", "")
