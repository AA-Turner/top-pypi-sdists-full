"""Standalone binding for the canonical Supabase ``web`` schema."""

from __future__ import annotations

WEB_DB_NAME = "matrx_web"

_models_registered = False


def _register_models() -> None:
    global _models_registered
    if _models_registered:
        return
    from matrx_scraper.db import models_web  # noqa: F401

    # `platform.acquisition_block` rides the same config: the Block Ledger is written by
    # whichever process hits the wall, and this package runs in more than one of them.
    from matrx_scraper.blocks import model as _block_model  # noqa: F401

    _models_registered = True


def _wire_block_ledger() -> None:
    """Give THIS process a Block Ledger the moment it has a database to write one to.

    🚨 Board row H7: for weeks the sink was configured in exactly one place —
    `aidream/package_integration.py` — so the hosted scraper service, whose image does not
    contain aidream at all, threw away every finding it produced and said nothing. Hanging the
    wiring off the binding functions is what makes that unrepeatable: a new entrypoint,
    worker or CLI cannot have a database without also having a ledger. Deferential by design
    (see `matrx_scraper.blocks.sink.configure_block_ledger`) — a host that already wired its
    own sink keeps it. Never fatal: a ledger that can break a boot is worse than no ledger.
    """
    try:
        from matrx_scraper.blocks.sink import configure_block_ledger

        configure_block_ledger()
    except Exception as exc:  # noqa: BLE001 — announced, never fatal
        import logging

        logging.getLogger("matrx_scraper.blocks").warning(
            "block ledger could not be wired (%s). Acquisition failures in this process "
            "will be logged instead of landing in platform.acquisition_block.",
            exc,
        )


def bind_web_to_host(db_config_name: str) -> None:
    """Hosted entry — bind canonical web models to an existing host pool."""

    from matrx_orm import is_database_registered, register_database_alias

    if not is_database_registered(WEB_DB_NAME):
        register_database_alias(WEB_DB_NAME, db_config_name)
    _register_models()
    _wire_block_ledger()


def bootstrap_web_db() -> str:
    """Bind ``matrx_web`` to the ONE database (Matrx Main), then register models.

    Goes through the same ONE resolver (``matrx_orm.register_platform_db``)
    as ``scraper.*`` — one resolver, so the two schemas can never point at
    different databases.
    """

    from matrx_orm import register_platform_db

    register_platform_db(
        WEB_DB_NAME,
        package="matrx-scraper",
        # `platform` is here for the Block Ledger's one table, written by every process this
        # package runs in (`matrx_scraper.blocks`), not only by aidream's monolith.
        additional_schemas=["web", "platform"],
    )
    _register_models()
    _wire_block_ledger()
    return WEB_DB_NAME


def is_web_db_registered() -> bool:
    from matrx_orm import is_database_registered

    return is_database_registered(WEB_DB_NAME)


__all__ = [
    "WEB_DB_NAME",
    "bind_web_to_host",
    "bootstrap_web_db",
    "is_web_db_registered",
]
