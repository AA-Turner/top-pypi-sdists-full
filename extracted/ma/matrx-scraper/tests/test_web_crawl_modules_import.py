"""Every web_crawl module imports: a syntax or indentation slip in one breaks anything that imports it."""

import importlib
import pkgutil

import matrx_scraper.web_crawl as web_crawl


def test_every_web_crawl_module_imports():
    failures = []
    for info in pkgutil.walk_packages(web_crawl.__path__, web_crawl.__name__ + "."):
        try:
            importlib.import_module(info.name)
        except Exception as exc:  # noqa: BLE001 - the point is to name every module that fails
            failures.append(f"{info.name}: {type(exc).__name__}: {exc}")
    assert not failures, "\n".join(failures)


def test_gsc_sync_imports_and_names_its_credential_door():
    from matrx_scraper.web_crawl import gsc_sync

    assert hasattr(gsc_sync, "GoogleConnectionCredential")
