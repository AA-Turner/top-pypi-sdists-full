"""Explicit local target for contract suites that synthesize multiple identities."""

from __future__ import annotations

import os
import re

from psycopg.conninfo import conninfo_to_dict, make_conninfo


class UnsafeContractDatabase(ValueError):
    """No contract connection is allowed until an isolated target is selected."""


def contract_database_dsn() -> str:
    """Never inherit platform credentials or libpq routing defaults."""
    raw = os.environ.get("MATRX_SEO_CONTRACT_TEST_DSN", "").strip()
    if not raw:
        raise UnsafeContractDatabase(
            "Set MATRX_SEO_CONTRACT_TEST_DSN to a local isolated contract database; "
            "platform credentials are never used for synthetic identities."
        )
    if os.environ.get("PGSERVICE"):
        raise UnsafeContractDatabase("Clear inherited PGSERVICE before contract tests")
    try:
        params = {
            key: str(value) for key, value in conninfo_to_dict(raw).items() if value is not None
        }
    except Exception:
        raise UnsafeContractDatabase("Invalid contract database connection string") from None
    allowed = {"host", "port", "dbname", "user", "password", "sslmode", "connect_timeout"}
    if set(params) - allowed:
        raise UnsafeContractDatabase("Contract target contains unsupported routing options")
    if params.get("host") not in {"127.0.0.1", "::1"}:
        raise UnsafeContractDatabase("Contract database must use a literal loopback address")
    if not re.fullmatch(r"matrx_seo_contract_[a-z0-9_]+", params.get("dbname", "")):
        raise UnsafeContractDatabase("Contract database must be named matrx_seo_contract_<run>")
    try:
        port = int(params.get("port", ""))
    except ValueError:
        raise UnsafeContractDatabase(
            "Contract database needs an explicit unprivileged port"
        ) from None
    if not 1024 <= port <= 65535 or not params.get("user") or not params.get("password"):
        raise UnsafeContractDatabase("Contract database needs a port, user and password")
    # Explicit values outrank PG* defaults. No service, hostaddr or multiple-host route.
    params.update(hostaddr=params["host"], sslmode="disable", connect_timeout="5")
    return make_conninfo(**params)
