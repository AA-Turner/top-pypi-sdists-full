from __future__ import annotations

from pathlib import Path


def test_canonical_crawler_runtime_has_no_legacy_artifact_lane() -> None:
    package = Path(__file__).parents[1] / "matrx_scraper"
    # `persistence/` was deliberately deleted with the legacy crawler
    # (2026-08-09) — it held the legacy crawl artifact adapters this guard
    # existed to fence off. Dropped from the list rather than skipped-if-
    # missing: a blanket skip would silently stop watching any target someone
    # deletes, which is the opposite of what a boundary guard is for.
    targets = [
        package / "web_crawl",
        package / "crawler.py",
        package / "browser_pool.py",
        package / "db" / "models_web.py",
        package / "server" / "app.py",
    ]
    missing = [str(t.relative_to(package)) for t in targets if not t.exists()]
    assert not missing, (
        f"this guard is watching paths that no longer exist: {missing}. "
        "Update the list deliberately — do not let it silently stop watching."
    )
    forbidden = (
        "body_ref",
        "markdown_ref",
        "storage_bucket",
        "storage_path",
        "supabase://",
        "supabase.storage",
        ".storage.from_(",
        ".storage.from(",
    )
    violations: list[str] = []
    for target in targets:
        files = target.rglob("*.py") if target.is_dir() else [target]
        for path in files:
            text = path.read_text()
            for token in forbidden:
                if token in text:
                    violations.append(f"{path.relative_to(package)}: {token}")
    assert violations == []


def test_screenshot_capture_has_one_runtime_implementation() -> None:
    package = Path(__file__).parents[1] / "matrx_scraper"
    sources = {path.relative_to(package): path.read_text() for path in package.rglob("*.py")}
    fetch_impls = [
        str(path) for path, source in sources.items() if "async def fetch_with_capture(" in source
    ]
    capture_impls = [
        str(path) for path, source in sources.items() if "async def capture_screenshots(" in source
    ]
    assert fetch_impls == ["browser_pool.py"]
    assert capture_impls == ["browser_pool.py"]
    # fetch_with_capture must delegate — never re-embed the capture loop.
    browser_pool = sources[Path("browser_pool.py")]
    assert "await capture_screenshots(" in browser_pool
    assert "kinds=same_profile_kinds" in browser_pool
    assert "failure_sink=screenshot_failures" in browser_pool
