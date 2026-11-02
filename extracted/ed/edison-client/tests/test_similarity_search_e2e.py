"""E2E tests for similarity search with embeddings."""

import os
import time
from uuid import uuid4

import pytest

from edison_client.clients.rest_client import RestClient
from edison_client.models.app import Stage

ADMIN_API_KEY = os.environ.get("PLAYWRIGHT_ADMIN_API_KEY", "")


@pytest.fixture(name="admin_client")
def fixture_admin_client():
    """Create a RestClient for testing; using an admin user key with full access."""
    client = RestClient(
        stage=Stage.LOCAL,
        api_key=ADMIN_API_KEY,
    )
    try:
        yield client
    finally:
        client.close()


# TODO: [PLA-1165] Change to Stage.DEV before unskipping the test
@pytest.mark.skip(reason="Requires similarity search endpoint deployed to dev")
@pytest.mark.timeout(300)
def test_upload_with_embedding_and_similarity_search(admin_client: RestClient):
    """Test uploading content with embedding and searching by similarity."""
    test_embedding = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6] * 512  # 3072-dim vector

    response = admin_client.store_text_content(
        name=f"E2E similarity test: {uuid4()}",
        content="Test content for similarity search",
        description="Test entry with embedding",
        embedding=test_embedding,
    )

    entry_id = response.data_storage.id

    # give it a sec to index
    time.sleep(5)

    try:
        results = admin_client.similarity_search_data_storage(
            embedding=test_embedding,
            size=10,
            min_score=0.5,
        )

        assert results, f"No results returned. Entry ID: {entry_id}"

        # Results are flat dicts with id at top level and embedding_similarity
        result_ids = [str(r["id"]) for r in results]
        assert str(entry_id) in result_ids, (
            f"Entry {entry_id} not found in results: {result_ids}"
        )

        our_result = next(r for r in results if str(r["id"]) == str(entry_id))
        assert our_result["embedding_similarity"] >= 0.95, (
            f"Expected high score, got {our_result['embedding_similarity']}"
        )

    finally:
        admin_client.delete_data_storage_entry(entry_id)
