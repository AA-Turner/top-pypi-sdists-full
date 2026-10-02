import pytest


@pytest.mark.live
def test_live_bing_collection_waits_for_canonical_persistence() -> None:
    pytest.skip("canonical SEO persistence is intentionally not implemented yet")
