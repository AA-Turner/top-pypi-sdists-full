from pathlib import Path


def test_search_performance_provider_count_has_covering_index() -> None:
    migration = (
        Path(__file__).parents[1]
        / "matrx_seo"
        / "migrations"
        / "20260822233000_search_performance_site_provider_count_index.sql"
    ).read_text()

    normalized = " ".join(migration.lower().split())
    assert "on seo.search_performance_daily (site_id, provider)" in normalized
