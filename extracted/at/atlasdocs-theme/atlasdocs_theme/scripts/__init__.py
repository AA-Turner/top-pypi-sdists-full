from __future__ import annotations


def __getattr__(name: str):
    if name == "create_directory_pages":
        from .prepare_directory_pages import create_directory_pages
        return create_directory_pages
    if name == "create_migration_status":
        from .prepare_migration_pages import create_migration_status
        return create_migration_status
    if name in ("LocalGitHistoryProvider", "get_gravatar_url", "calculate_update_stats"):
        import importlib
        mod = importlib.import_module(".fetch_git_history", __name__)
        return getattr(mod, name)
    if name in ("extract_twiki_web_and_page", "convert_twiki_revision_to_commit", "append_twiki_history"):
        import importlib
        mod = importlib.import_module(".fetch_twiki_history", __name__)
        return getattr(mod, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "create_directory_pages",
    "create_migration_status",
    "LocalGitHistoryProvider",
    "get_gravatar_url",
    "calculate_update_stats",
    "extract_twiki_web_and_page",
    "convert_twiki_revision_to_commit",
    "append_twiki_history",
]
