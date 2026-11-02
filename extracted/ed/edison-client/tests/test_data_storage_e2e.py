import asyncio
import json
from pathlib import Path
from uuid import uuid4

import pytest
from pydantic import HttpUrl

from edison_client.clients.data_storage_methods import (
    DataStorageError,
    DataStorageNotFoundError,
)
from edison_client.clients.rest_client import RestClient
from edison_client.models.data_storage_methods import (
    DataContentType,
    DataStorageLocationPayload,
    DataStorageType,
    PermittedAccessors,
    RawFetchResponse,
    ShareStatus,
)
from edison_client.models.rest import (
    FilterLogic,
    SearchCriterion,
    SearchOperator,
)


@pytest.mark.timeout(300)
def test_store_raw_content_sync(admin_client: RestClient):
    test_content = "This is random content for the sync test"
    # Store the text content
    response = admin_client.store_text_content(
        name=f"E2E test entry text: {uuid4()}",
        content=test_content,
        description="Here is some description",
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = admin_client.fetch_data_from_storage(response.data_storage.id)

    assert isinstance(fetch_response, RawFetchResponse)
    assert fetch_response.content == test_content
    assert fetch_response.entry_id == response.data_storage.id
    assert fetch_response.entry_name == response.data_storage.name

    admin_client.delete_data_storage_entry(response.data_storage.id)

    with pytest.raises(DataStorageError, match="Data storage entry not found"):
        admin_client.fetch_data_from_storage(response.data_storage.id)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_store_raw_content_async(admin_client: RestClient):
    test_content = "This is random content for the async test"
    response = await admin_client.astore_text_content(
        name=f"E2E test entry text: {uuid4()}",
        content=test_content,
        description="Here is some description",
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = await admin_client.afetch_data_from_storage(
        response.data_storage.id
    )

    assert isinstance(fetch_response, RawFetchResponse)
    assert fetch_response.content == test_content
    assert fetch_response.entry_id == response.data_storage.id
    assert fetch_response.entry_name == response.data_storage.name

    await admin_client.adelete_data_storage_entry(response.data_storage.id)

    with pytest.raises(DataStorageError, match="Data storage entry not found"):
        await admin_client.afetch_data_from_storage(response.data_storage.id)


@pytest.mark.timeout(300)
def test_store_file_content_sync(admin_client: RestClient):
    file_path = Path("packages/edison-client/tests/test_data/test_file.txt")
    response = admin_client.store_file_content(
        name=f"E2E test entry file: {uuid4()}",
        file_path=file_path,
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = admin_client.fetch_data_from_storage(response.data_storage.id)

    assert fetch_response is not None
    assert isinstance(fetch_response, RawFetchResponse)
    assert fetch_response.filename == file_path
    assert (
        fetch_response.content
        == "Here is some random text that shall immortalize Eddie's brain in code.\n"
    )

    admin_client.delete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
def test_store_file_content_with_path_override_sync(admin_client: RestClient):
    file_path = Path("packages/edison-client/tests/test_data/test_file.txt")
    file_path_override = Path("test_file_override.txt")
    response = admin_client.store_file_content(
        name=f"E2E test entry file: {uuid4()}",
        file_path=file_path,
        file_path_override=file_path_override,
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = admin_client.fetch_data_from_storage(response.data_storage.id)

    assert fetch_response is not None
    assert isinstance(fetch_response, RawFetchResponse)
    assert fetch_response.filename == file_path_override
    assert (
        fetch_response.content
        == "Here is some random text that shall immortalize Eddie's brain in code.\n"
    )

    admin_client.delete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
def test_store_dir_content_sync(admin_client: RestClient):
    response = admin_client.store_file_content(
        name=f"E2E test entry dir: {uuid4()}",
        file_path=Path("packages/edison-client/tests/test_data"),
        as_collection=True,
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = admin_client.fetch_data_from_storage(response.data_storage.id)

    assert isinstance(fetch_response, Path)
    assert fetch_response.exists()

    admin_client.delete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_store_file_content_async(admin_client: RestClient):
    file_path = Path("packages/edison-client/tests/test_data/test_file.txt")
    response = await admin_client.astore_file_content(
        name=f"E2E test entry file: {uuid4()}",
        file_path=file_path,
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = await admin_client.afetch_data_from_storage(
        response.data_storage.id
    )

    assert fetch_response is not None
    assert isinstance(fetch_response, RawFetchResponse)
    assert fetch_response.filename == file_path
    assert (
        fetch_response.content
        == "Here is some random text that shall immortalize Eddie's brain in code.\n"
    )

    await admin_client.adelete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_store_file_content_with_path_override_async(admin_client: RestClient):
    file_path = Path("packages/edison-client/tests/test_data/test_file.txt")
    file_path_override = Path("test_file_override.txt")
    response = await admin_client.astore_file_content(
        name=f"E2E test entry file: {uuid4()}",
        file_path=file_path,
        file_path_override=file_path_override,
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = await admin_client.afetch_data_from_storage(
        response.data_storage.id
    )

    assert fetch_response is not None
    assert isinstance(fetch_response, RawFetchResponse)
    assert fetch_response.filename == file_path_override
    assert (
        fetch_response.content
        == "Here is some random text that shall immortalize Eddie's brain in code.\n"
    )

    await admin_client.adelete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_store_dir_content_async(admin_client: RestClient):
    response = await admin_client.astore_file_content(
        name=f"E2E test entry dir: {uuid4()}",
        file_path=Path("packages/edison-client/tests/test_data"),
        as_collection=True,
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = await admin_client.afetch_data_from_storage(
        response.data_storage.id
    )

    assert isinstance(fetch_response, Path)
    assert fetch_response.exists()

    await admin_client.adelete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_store_dir_with_manifest_async(admin_client: RestClient):
    response = await admin_client.astore_file_content(
        name=f"E2E test dir: {uuid4()}",
        file_path=Path("packages/edison-client/tests/test_data"),
        manifest_filename="packages/edison-client/tests/test_data/test_manifest.yaml",
        as_collection=True,
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = await admin_client.afetch_data_from_storage(
        response.data_storage.id
    )

    assert isinstance(fetch_response, Path)
    assert fetch_response.exists()

    await admin_client.adelete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
def test_register_existing_content_gcs_sync_rejected(admin_client: RestClient):
    with pytest.raises(
        DataStorageError,
        match="Registering existing GCS locations is not supported",
    ):
        admin_client.register_existing_data_source(
            name=f"E2E test entry gcs: {uuid4()}",
            description="This is data that already exists",
            existing_location=DataStorageLocationPayload(
                storage_type=DataStorageType.GCS,
                content_type=DataContentType.FILE,
                metadata={"bucket_name": "fh-pubmed-data"},
                location="oa_package/00/00/PMC10054724.tar.gz",
            ),
        )


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_register_existing_content_gcs_async_rejected(
    admin_client: RestClient,
):
    with pytest.raises(
        DataStorageError,
        match="Registering existing GCS locations is not supported",
    ):
        await admin_client.aregister_existing_data_source(
            name=f"E2E test entry gcs: {uuid4()}",
            description="This is data that already exists",
            existing_location=DataStorageLocationPayload(
                storage_type=DataStorageType.GCS,
                content_type=DataContentType.FILE,
                metadata={"bucket_name": "fh-pubmed-data"},
                location="oa_package/00/00/PMC10054724.tar.gz",
            ),
        )


@pytest.mark.timeout(300)
def test_register_existing_content_postgres_sync(admin_client: RestClient):
    test_trajectory_id = "39510f66-c2ee-41c7-94de-64eb142c3f2a"

    response = admin_client.register_existing_data_source(
        name=f"E2E test entry postgres row: {uuid4()}",
        description="This is data that already exists",
        existing_location=DataStorageLocationPayload(
            storage_type=DataStorageType.PG_TABLE,
            content_type=DataContentType.TEXT,
            metadata={
                "table_name": "trajectories",
                "row_id": test_trajectory_id,
            },
        ),
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = admin_client.fetch_data_from_storage(response.data_storage.id)

    assert isinstance(fetch_response, RawFetchResponse)
    assert json.loads(fetch_response.content).get("id") == test_trajectory_id

    admin_client.delete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_register_existing_content_postgres_async(admin_client: RestClient):
    test_trajectory_id = "39510f66-c2ee-41c7-94de-64eb142c3f2a"

    response = await admin_client.aregister_existing_data_source(
        name=f"E2E test entry postgres row: {uuid4()}",
        description="This is data that already exists",
        existing_location=DataStorageLocationPayload(
            storage_type=DataStorageType.PG_TABLE,
            content_type=DataContentType.TEXT,
            metadata={
                "table_name": "trajectories",
                "row_id": test_trajectory_id,
            },
        ),
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    fetch_response = await admin_client.afetch_data_from_storage(
        response.data_storage.id
    )

    assert isinstance(fetch_response, RawFetchResponse)
    assert json.loads(fetch_response.content).get("id") == test_trajectory_id

    await admin_client.adelete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
def test_register_existing_content_bigquery_sync(admin_client: RestClient):
    response = admin_client.register_existing_data_source(
        name=f"E2E test entry bigquery table: {uuid4()}",
        description="This is data that already exists",
        existing_location=DataStorageLocationPayload(
            storage_type=DataStorageType.BIGQUERY,
            content_type=DataContentType.TEXT,
            metadata={
                "project_id": "bigquery-public-data",
                "dataset_id": "samples",
                "table_id": "shakespeare",
            },
        ),
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    admin_client.delete_data_storage_entry(response.data_storage.id)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_register_existing_content_bigquery_async(admin_client: RestClient):
    response = await admin_client.aregister_existing_data_source(
        name=f"E2E test entry bigquery table: {uuid4()}",
        description="This is data that already exists",
        existing_location=DataStorageLocationPayload(
            storage_type=DataStorageType.BIGQUERY,
            content_type=DataContentType.TEXT,
            metadata={
                "project_id": "bigquery-public-data",
                "dataset_id": "samples",
                "table_id": "shakespeare",
            },
        ),
    )

    assert response is not None
    assert response.data_storage.id is not None
    assert len(response.storage_locations) > 0

    await admin_client.adelete_data_storage_entry(response.data_storage.id)


class TestDataset:
    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_dataset_async(self, admin_client: RestClient):
        dataset_name_id = uuid4()
        create_response = await admin_client.acreate_dataset(
            name=f"E2E test dataset: {dataset_name_id}",
            description="This is a test dataset",
        )

        assert create_response is not None
        assert create_response.id is not None
        assert create_response.name == f"E2E test dataset: {dataset_name_id}"
        assert create_response.description == "This is a test dataset"

        get_response = await admin_client.aget_dataset(dataset_id=create_response.id)

        assert get_response is not None
        assert get_response.dataset.id == create_response.id
        assert get_response.data_storage_entries == []

        await admin_client.adelete_dataset(dataset_id=create_response.id)

        with pytest.raises(DataStorageNotFoundError, match="Dataset not found"):
            await admin_client.aget_dataset(dataset_id=create_response.id)

    @pytest.mark.timeout(300)
    def test_dataset_sync(self, admin_client: RestClient):
        dataset_name_id = uuid4()
        create_response = admin_client.create_dataset(
            name=f"E2E test dataset: {dataset_name_id}",
            description="This is a test dataset",
        )

        assert create_response is not None
        assert create_response.id is not None
        assert create_response.name == f"E2E test dataset: {dataset_name_id}"

        get_response = admin_client.get_dataset(dataset_id=create_response.id)

        assert get_response is not None
        assert get_response.dataset.id == create_response.id
        assert get_response.data_storage_entries == []

        admin_client.delete_dataset(dataset_id=create_response.id)

        with pytest.raises(DataStorageNotFoundError, match="Dataset not found"):
            admin_client.get_dataset(dataset_id=create_response.id)


@pytest.mark.timeout(300)
@pytest.mark.asyncio
async def test_astore_link_success(admin_client: RestClient):
    """Test successful asynchronous link storage."""
    result = await admin_client.astore_link(
        name="Test API Link",
        url=HttpUrl("https://xyz.api.futurehouse.org"),
        description="Test link to xyz.api.futurehouse.org",
        instructions="this is a test api which you can call without authentication",
        api_key="test_key_123",
    )

    assert result.data_storage.id is not None
    assert result.data_storage.name == "Test API Link"
    assert result.data_storage.description == "Test link to xyz.api.futurehouse.org"
    assert result.data_storage.content == "https://xyz.api.futurehouse.org/"
    assert len(result.storage_locations) > 0
    assert result.storage_locations[0].storage_config.storage_type == "link"
    assert (
        result.storage_locations[0].storage_config.location
        == "https://xyz.api.futurehouse.org/"
    )

    await admin_client.adelete_data_storage_entry(result.data_storage.id)


class TestDataStorageSearch:
    @pytest.mark.timeout(300)
    def test_data_storage_search_sync(self, admin_client: RestClient):
        test_query = "test"

        test_criteria = SearchCriterion(
            field="name", operator=SearchOperator.CONTAINS, value=test_query
        )

        results = admin_client.search_data_storage(criteria=[test_criteria], limit=5)

        assert results is not None
        assert len(results) == 5
        assert test_query.lower() in results[0]["name"].lower()

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_data_storage_search_async(self, admin_client: RestClient):
        test_query = "test"

        name_test_criteria = SearchCriterion(
            field="name", operator=SearchOperator.CONTAINS, value=test_query
        )

        results = await admin_client.asearch_data_storage(
            criteria=[name_test_criteria], limit=5
        )

        assert results is not None
        assert len(results) == 5
        assert test_query.lower() in results[0]["name"].lower()

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_complex_data_storage_search_async(self, admin_client: RestClient):
        test_query = "test"

        name_test_criteria = SearchCriterion(
            field="name", operator=SearchOperator.CONTAINS, value=test_query
        )

        user_id_test_criteria = SearchCriterion(
            field="user_id",
            operator=SearchOperator.EQUALS,
            value="a5E0sDbOYEWLBoy9qzOQ8yfKiKw1",
        )

        dataset_id_test_criteria = SearchCriterion(
            field="dataset_id",
            operator=SearchOperator.EQUALS,
            value="328375e2-591e-4cc9-b17b-cccf040c343a",
        )

        description_test_criteria = SearchCriterion(
            field="description",
            operator=SearchOperator.CONTAINS,
            value="xyz.api.futurehouse.org",
        )

        or_results = await admin_client.asearch_data_storage(
            criteria=[
                name_test_criteria,
                user_id_test_criteria,
                dataset_id_test_criteria,
                description_test_criteria,
            ],
            filter_logic=FilterLogic.OR,
        )

        and_results = await admin_client.asearch_data_storage(
            criteria=[
                name_test_criteria,
                user_id_test_criteria,
                dataset_id_test_criteria,
                description_test_criteria,
            ],
            filter_logic=FilterLogic.AND,
        )

        assert or_results is not None
        assert len(or_results) > 0

        assert and_results is not None
        assert len(and_results) > 0
        assert test_query.lower() in and_results[0]["name"].lower()

        assert len(or_results) > len(and_results)

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_fulltext_or_returns_results_for_non_cooccurring_terms(
        self, admin_client: RestClient
    ):
        """FULLTEXT criteria with OR should return results for non-co-occurring terms.

        Seeds two docs with unique hex tokens so:
        - Each returns results individually
        - Don't co-occur in any document (AND returns 0)
        - With the fix: OR returns the union (> 0)
        - With the bug: OR incorrectly returns 0 (treated as AND)
        """
        token_a, token_b = uuid4().hex, uuid4().hex
        entry_a = await admin_client.astore_text_content(
            name=f"or-{token_a}", content=token_a
        )
        entry_b = await admin_client.astore_text_content(
            name=f"or-{token_b}", content=token_b
        )
        await asyncio.sleep(5)  # wait for ES refresh
        try:
            criteria = [
                SearchCriterion(
                    field="content", operator=SearchOperator.FULLTEXT, value=token_a
                ),
                SearchCriterion(
                    field="content", operator=SearchOperator.FULLTEXT, value=token_b
                ),
            ]

            or_results = await admin_client.asearch_data_storage(
                criteria=criteria,
                filter_logic=FilterLogic.OR,
                limit=50,
            )

            and_results = await admin_client.asearch_data_storage(
                criteria=criteria,
                filter_logic=FilterLogic.AND,
                limit=50,
            )

            # AND should return 0 (terms don't co-occur)
            assert len(and_results) == 0, (
                f"Expected AND to return 0 for non-co-occurring terms, got {len(and_results)}"
            )
            # OR should return results (union of both term matches)
            assert len(or_results) > 0, (
                "FULLTEXT OR should return results when individual terms match documents. "
                "Got 0 results - this indicates the bug where OR is treated as AND."
            )
        finally:
            await admin_client.adelete_data_storage_entry(entry_a.data_storage.id)
            await admin_client.adelete_data_storage_entry(entry_b.data_storage.id)

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_fulltext_or_results_sorted_by_score(self, admin_client: RestClient):
        """FULLTEXT OR results must be sorted by score descending.

        Uses non-co-occurring terms to verify OR behavior:
        - With the fix: OR returns union of results, sorted by score
        - With the bug: OR treats as AND, returns 0 results (test fails)
        """
        results = await admin_client.asearch_data_storage(
            criteria=[
                SearchCriterion(
                    field="content",
                    operator=SearchOperator.FULLTEXT,
                    value="tirzepatide",
                ),
                SearchCriterion(
                    field="content", operator=SearchOperator.FULLTEXT, value="retina"
                ),
            ],
            filter_logic=FilterLogic.OR,
            limit=50,
        )

        assert len(results) >= 2, (
            "FULLTEXT OR should return results for non-co-occurring terms. "
            "Got < 2 results - this indicates the bug where OR is treated as AND."
        )

        scores = [r.get("score", 0) for r in results]
        for i in range(len(scores) - 1):
            assert scores[i] >= scores[i + 1], (
                f"Results not sorted by score descending: "
                f"position {i} ({scores[i]}) < position {i + 1} ({scores[i + 1]})"
            )


class TestEntryPermissions:
    @pytest.mark.timeout(300)
    def test_data_update_entry_permissions_sync(
        self, admin_client: RestClient, pub_client: RestClient
    ):
        test_content = "This is random content for the sync test"

        # Store the text content
        create_entry_response = admin_client.store_text_content(
            name=f"E2E test entry text: {uuid4()}",
            content=test_content,
            description="Here is some description",
        )

        assert create_entry_response.data_storage.share_status == ShareStatus.PRIVATE

        with pytest.raises(DataStorageError, match="Data storage entry not found"):
            pub_client.fetch_data_from_storage(create_entry_response.data_storage.id)

        update_entry_response = admin_client.update_entry_permissions(
            data_storage_id=create_entry_response.data_storage.id,
            share_status=ShareStatus.PUBLIC,
            permitted_accessors=PermittedAccessors(
                users=[],
                organizations=[],
            ),
        )

        assert update_entry_response.data_storage.share_status == ShareStatus.PUBLIC

        fetch_entry_response = admin_client.fetch_data_from_storage(
            create_entry_response.data_storage.id
        )

        assert isinstance(fetch_entry_response, RawFetchResponse)
        assert fetch_entry_response.content == test_content
        assert fetch_entry_response.entry_id == create_entry_response.data_storage.id
        assert (
            fetch_entry_response.entry_name == create_entry_response.data_storage.name
        )

        admin_client.delete_data_storage_entry(create_entry_response.data_storage.id)

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_data_update_entry_permissions_async(
        self, admin_client: RestClient, pub_client: RestClient
    ):
        test_content = "This is random content for the async test"

        # Store the text content
        create_entry_response = await admin_client.astore_text_content(
            name=f"E2E test entry text: {uuid4()}",
            content=test_content,
            description="Here is some description",
        )

        assert create_entry_response.data_storage.share_status == ShareStatus.PRIVATE

        with pytest.raises(DataStorageError, match="Data storage entry not found"):
            await pub_client.afetch_data_from_storage(
                create_entry_response.data_storage.id
            )

        update_entry_response = await admin_client.aupdate_entry_permissions(
            data_storage_id=create_entry_response.data_storage.id,
            share_status=ShareStatus.PUBLIC,
            permitted_accessors=PermittedAccessors(
                users=[],
                organizations=[],
            ),
        )

        fetch_entry_response = await pub_client.afetch_data_from_storage(
            create_entry_response.data_storage.id
        )

        assert isinstance(fetch_entry_response, RawFetchResponse)
        assert fetch_entry_response.content == test_content
        assert fetch_entry_response.entry_id == create_entry_response.data_storage.id
        assert (
            fetch_entry_response.entry_name == create_entry_response.data_storage.name
        )

        assert update_entry_response.data_storage.share_status == ShareStatus.PUBLIC

        await admin_client.adelete_data_storage_entry(
            create_entry_response.data_storage.id
        )
