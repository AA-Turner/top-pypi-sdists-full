"""Standalone binding for the canonical Supabase ``web`` schema."""

from __future__ import annotations

WEB_DB_NAME = "matrx_web"

_models_registered = False


def _register_models() -> None:
    global _models_registered
    if _models_registered:
        return
    from matrx_scraper.db import models_web  # noqa: F401

    _models_registered = True


def bind_web_to_host(db_config_name: str) -> None:
    """Hosted entry — bind canonical web models to an existing host pool."""

    from matrx_orm import is_database_registered, register_database_alias

    if not is_database_registered(WEB_DB_NAME):
        register_database_alias(WEB_DB_NAME, db_config_name)
    _register_models()


def bootstrap_web_db() -> str:
    """Bind ``matrx_web`` to the ONE database (Matrx Main), then register models.

    Goes through the same ONE resolver (``matrx_orm.register_platform_db``)
    as ``scraper.*`` — one resolver, so the two schemas can never point at
    different databases.
    """

    from matrx_orm import register_platform_db

    register_platform_db(WEB_DB_NAME, package="matrx-scraper", additional_schemas=["web"])
    _register_models()
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
