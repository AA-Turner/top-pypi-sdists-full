"""Shared SQL fragments for job + spider joins."""


def jobs_from_clause(settings) -> str:
    jobs = settings.db_jobs_table
    spiders = settings.db_spiders_table
    return f"{jobs} j INNER JOIN {spiders} s ON j.spider_id = s.id"


def jobs_select_sql(settings, keys: tuple[str, ...]) -> str:
    parts = []
    for key in keys:
        if key == "spider_name":
            parts.append("s.name AS spider_name")
        else:
            parts.append(f"j.{key}")
    return f"SELECT {', '.join(parts)} FROM {jobs_from_clause(settings)}"


def spider_name_filter_clause(settings, *, prefix="s") -> str:
    dialect = getattr(settings, "db_dialect", "postgres") or "postgres"
    col = f"{prefix}.name"
    if dialect == "postgres":
        return f"{col} ILIKE %s ESCAPE E'\\\\'"
    return f"{col} LIKE %s"
