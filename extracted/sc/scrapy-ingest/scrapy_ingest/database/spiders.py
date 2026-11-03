"""Register crawlers in ``ingest_spiders`` and return stable ids."""

from __future__ import annotations

from ..utils.time import get_current_datetime


def spider_class_path(spider) -> str:
    cls = spider.__class__
    return f"{cls.__module__}.{cls.__name__}"


def ensure_spider(db, settings, spider) -> int:
    """Insert or refresh spider metadata; return ``ingest_spiders.id``."""
    table = settings.db_spiders_table
    name = (getattr(spider, "name", None) or "spider").strip()[:255]
    path = spider_class_path(spider)[:512]
    now = get_current_datetime(settings)

    if row := db.execute(f"SELECT id FROM {table} WHERE name = %s", (name,)):
        sid = int(row[0])
        db.execute(
            f"UPDATE {table} SET class_path = %s, updated_at = %s WHERE id = %s",
            (path, now, sid),
        )
        return sid

    sid = int(db.execute(f"SELECT COALESCE(MAX(id), 0) FROM {table}")[0]) + 1
    try:
        db.execute(
            f"INSERT INTO {table} (id, name, class_path, created_at, updated_at) "
            f"VALUES (%s, %s, %s, %s, %s)",
            (sid, name, path, now, now),
        )
    except Exception:
        pass
    return int(db.execute(f"SELECT id FROM {table} WHERE name = %s", (name,))[0])
