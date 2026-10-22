"""Install log-capture hooks before Scrapy configures logging (startup logs)."""

from __future__ import annotations

_installed = False


def uses_ingest_pipeline(settings) -> bool:
    try:
        from scrapy.utils.conf import build_component_list

        raw = settings.getdict("ITEM_PIPELINES")
        return bool(raw) and any(
            "scrapy_ingest" in str(p).lower() for p in build_component_list(raw)
        )
    except Exception:
        return False


def ensure_early_log_buffer(settings) -> None:
    from scrapy.settings import Settings

    from .extensions.log_handler import install_early

    if isinstance(settings, dict) or settings is None:
        settings = Settings(settings)
    if uses_ingest_pipeline(settings):
        install_early()


def _mark_wrapped(fn, orig):
    fn._ingest_wrapped = True  # type: ignore[attr-defined]
    fn.__wrapped__ = orig  # type: ignore[attr-defined]
    return fn


def _patch_scrapy() -> None:
    import scrapy.crawler as crawler_mod
    import scrapy.cmdline as cmdline
    import scrapy.utils.project as project_mod
    from scrapy.settings import Settings
    from scrapy.utils import log as scrapy_log

    if not getattr(scrapy_log.configure_logging, "_ingest_wrapped", False):
        orig = scrapy_log.configure_logging
        while getattr(orig, "_ingest_wrapped", False):
            orig = orig.__wrapped__  # type: ignore[attr-defined]

        def configure_logging(settings=None, install_root_handler=None):
            ensure_early_log_buffer(
                settings if settings is not None else project_mod.get_project_settings()
            )
            return orig(settings, install_root_handler)

        scrapy_log.configure_logging = _mark_wrapped(configure_logging, orig)
        crawler_mod.configure_logging = scrapy_log.configure_logging

    if not getattr(Settings.setmodule, "_ingest_wrapped", False):
        orig_sm = Settings.setmodule

        def setmodule(self, module, priority="project"):
            orig_sm(self, module, priority)
            if priority == "project":
                ensure_early_log_buffer(self)

        Settings.setmodule = _mark_wrapped(setmodule, orig_sm)

    if not getattr(project_mod.get_project_settings, "_ingest_wrapped", False):
        orig_gps = project_mod.get_project_settings

        def get_project_settings():
            settings = orig_gps()
            ensure_early_log_buffer(settings)
            return settings

        project_mod.get_project_settings = _mark_wrapped(get_project_settings, orig_gps)

    if getattr(cmdline.execute, "_ingest_wrapped", False):
        return

    orig_ex = cmdline.execute

    def execute(argv=None, settings=None):
        if settings is None:
            from scrapy.utils.project import init_env

            init_env()
            ensure_early_log_buffer(project_mod.get_project_settings())
        else:
            ensure_early_log_buffer(settings)
        return orig_ex(argv, settings)

    cmdline.execute = _mark_wrapped(execute, orig_ex)


def install() -> None:
    global _installed
    if _installed:
        return
    try:
        import scrapy.cmdline  # noqa: F401
    except ImportError:
        return
    _patch_scrapy()
    _installed = True
