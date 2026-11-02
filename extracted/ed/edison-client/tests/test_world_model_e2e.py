"""
End-to-end tests for world model operations.

Tests cover:
1. Creating world models with both content_location types (INLINE and DATA_STORAGE)
2. Retrieving both types and verifying content filtering
3. Non-admin users cannot access underlying data storage for platform_only entries
"""

from uuid import uuid4

import pytest

from edison_client.clients.data_storage_methods import (
    DataStorageError,
)
from edison_client.clients.rest_client import (
    RestClient,
)
from edison_client.models.rest import (
    ContentLocation,
    WorldModel,
)


class TestWorldModelContentLocationInline:
    """Tests for world models with content_location=INLINE (content stored in DB)."""

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_create_and_get_inline_world_model_async(
        self, admin_client: RestClient
    ):
        """Test creating and retrieving an INLINE world model asynchronously."""
        test_name = f"E2E Test Inline World Model {uuid4()}"
        test_content = "This is the world model content stored inline in the database."
        test_metadata = {"key1": "value1", "nested": {"key2": "value2"}}

        model = WorldModel(
            content=test_content,
            content_location=ContentLocation.INLINE,
            name=test_name,
            description="An E2E test world model with inline content",
            model_metadata=test_metadata,
        )

        # Create the world model
        model_id = await admin_client.acreate_world_model(model)
        assert model_id is not None

        try:
            # Retrieve the world model
            retrieved = await admin_client.aget_world_model(world_model_id=model_id)

            assert str(retrieved.id) == str(model_id)
            assert retrieved.name == test_name
            assert retrieved.content == test_content
            assert retrieved.content_location == ContentLocation.INLINE
            assert retrieved.data_storage_id is None
            assert retrieved.model_metadata == test_metadata
            assert retrieved.enabled is True
        finally:
            # Cleanup
            await admin_client.delete_world_model(model_id)

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_create_and_get_inline_world_model_sync(
        self, admin_client: RestClient
    ):
        """Test creating and retrieving an INLINE world model synchronously."""
        test_name = f"E2E Test Inline World Model Sync {uuid4()}"
        test_content = "Sync test content for inline world model."

        model = WorldModel(
            content=test_content,
            content_location=ContentLocation.INLINE,
            name=test_name,
            description="Sync E2E test world model",
        )

        # Create the world model
        model_id = admin_client.create_world_model(model)
        assert model_id is not None

        # Retrieve the world model
        retrieved = admin_client.get_world_model(world_model_id=model_id)

        assert str(retrieved.id) == str(model_id)
        assert retrieved.name == test_name
        assert retrieved.content == test_content
        assert retrieved.content_location == ContentLocation.INLINE
        assert retrieved.data_storage_id is None

        await admin_client.delete_world_model(model_id)


class TestWorldModelContentLocationDataStorage:
    """Tests for world models with content_location=DATA_STORAGE (content stored in GCS)."""

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_create_and_get_dss_world_model_async(self, admin_client: RestClient):
        """Test creating and retrieving a DATA_STORAGE world model asynchronously."""
        test_name = f"E2E Test DSS World Model {uuid4()}"
        test_content = (
            "This is the world model content stored in GCS via Data Storage Service."
        )
        test_metadata = {"source": "e2e_test", "version": "1.0"}

        model = WorldModel(
            content=test_content,
            content_location=ContentLocation.DATA_STORAGE,
            name=test_name,
            description="An E2E test world model with DSS-backed content",
            model_metadata=test_metadata,
        )

        # Create the world model (this uploads content to GCS)
        model_id = await admin_client.acreate_world_model(model)
        assert model_id is not None

        try:
            # Retrieve the world model
            retrieved = await admin_client.aget_world_model(world_model_id=model_id)

            assert str(retrieved.id) == str(model_id)
            assert retrieved.name == test_name
            assert retrieved.content_location == ContentLocation.DATA_STORAGE
            assert retrieved.data_storage_id is not None

            # For admin users, content should be populated from DSS
            assert retrieved.content == test_content
            assert retrieved.model_metadata == test_metadata
        finally:
            # Cleanup
            await admin_client.delete_world_model(model_id)

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_create_and_get_dss_world_model_sync(self, admin_client: RestClient):
        """Test creating and retrieving a DATA_STORAGE world model synchronously."""
        test_name = f"E2E Test DSS World Model Sync {uuid4()}"
        test_content = "Sync test content stored in GCS."
        test_metadata = {"sync_test": True}

        model = WorldModel(
            content=test_content,
            content_location=ContentLocation.DATA_STORAGE,
            name=test_name,
            description="Sync E2E test DSS world model",
            model_metadata=test_metadata,
        )

        # Create the world model
        model_id = admin_client.create_world_model(model)
        assert model_id is not None

        # Retrieve the world model
        retrieved = admin_client.get_world_model(world_model_id=model_id)

        assert str(retrieved.id) == str(model_id)
        assert retrieved.name == test_name
        assert retrieved.content_location == ContentLocation.DATA_STORAGE
        assert retrieved.data_storage_id is not None
        assert retrieved.content == test_content
        assert retrieved.model_metadata == test_metadata

        await admin_client.delete_world_model(model_id)


class TestWorldModelVersioning:
    """Tests for world model versioning with both content location types."""

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_inline_world_model_versioning(self, admin_client: RestClient):
        """Test creating multiple versions of an INLINE world model."""
        test_name = f"E2E Test Versioned WM {uuid4()}"

        # Create initial version
        v1 = WorldModel(
            content="Version 1 content",
            content_location=ContentLocation.INLINE,
            name=test_name,
            description="Version 1",
        )
        v1_id = await admin_client.acreate_world_model(v1)
        v2_id = None

        try:
            # Create version 2 with prior reference
            v2 = WorldModel(
                content="Version 2 content - updated",
                content_location=ContentLocation.INLINE,
                prior=v1_id,
            )
            v2_id = await admin_client.acreate_world_model(v2)

            # Verify version 2 inherits name from prior
            retrieved_v2 = await admin_client.aget_world_model(world_model_id=v2_id)
            assert retrieved_v2.name == test_name
            assert retrieved_v2.content == "Version 2 content - updated"
            assert str(retrieved_v2.prior) == str(v1_id)
        finally:
            # Cleanup (only need to delete latest, prior remains for history)
            await admin_client.delete_world_model(v1_id)
            if v2_id is not None:
                await admin_client.delete_world_model(v2_id)

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_dss_world_model_versioning(self, admin_client: RestClient):
        """Test creating multiple versions of a DATA_STORAGE world model."""
        test_name = f"E2E Test Versioned DSS WM {uuid4()}"

        # Create initial version
        v1 = WorldModel(
            content="DSS Version 1 content",
            content_location=ContentLocation.DATA_STORAGE,
            name=test_name,
            description="DSS Version 1",
            model_metadata={"version": 1},
        )
        v1_id = await admin_client.acreate_world_model(v1)
        v2_id = None

        try:
            # Retrieve v1 to verify
            retrieved_v1 = await admin_client.aget_world_model(world_model_id=v1_id)
            assert retrieved_v1.content_location == ContentLocation.DATA_STORAGE
            assert retrieved_v1.data_storage_id is not None

            # Create version 2 with prior reference (also DSS-backed)
            v2 = WorldModel(
                content="DSS Version 2 content - updated",
                content_location=ContentLocation.DATA_STORAGE,
                prior=v1_id,
                model_metadata={"version": 2},
            )
            v2_id = await admin_client.acreate_world_model(v2)

            # Verify version 2
            retrieved_v2 = await admin_client.aget_world_model(world_model_id=v2_id)
            assert retrieved_v2.name == test_name
            assert retrieved_v2.content == "DSS Version 2 content - updated"
            assert str(retrieved_v2.prior) == str(v1_id)
            assert retrieved_v2.data_storage_id is not None
            # DSS ID should be different for each version

            assert str(retrieved_v2.data_storage_id) != str(
                retrieved_v1.data_storage_id
            )
        finally:
            await admin_client.delete_world_model(v1_id)
            if v2_id is not None:
                await admin_client.delete_world_model(v2_id)


class TestWorldModelDataStorageAccess:
    """
    Tests for data storage access control on world model underlying data.

    World models with content_location=DATA_STORAGE have their content stored
    in a data storage entry marked as platform_only=True. This means:
    - The world model API endpoint can access and return the content
    - Direct access to the underlying data storage entry requires INTERNAL auth
    - Public users should NOT be able to directly access the data storage entry
    """

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_public_user_cannot_access_dss_entry_directly(
        self, admin_client: RestClient, pub_client: RestClient
    ):
        """
        Test that a public user cannot directly access the data storage entry.

        The world model content is accessible via the world model API for authorized
        users, but the raw data storage entry should not be accessible.
        """
        test_name = f"E2E Test DSS Access Control {uuid4()}"
        test_content = "Content that should not be directly accessible via DSS API"

        model = WorldModel(
            content=test_content,
            content_location=ContentLocation.DATA_STORAGE,
            name=test_name,
            description="Test world model for DSS access control",
        )

        # Admin creates the world model
        model_id = await admin_client.acreate_world_model(model)

        try:
            # Admin retrieves the world model to get the data_storage_id
            retrieved = await admin_client.aget_world_model(world_model_id=model_id)
            assert retrieved.data_storage_id is not None
            data_storage_id = retrieved.data_storage_id

            # Public user should NOT be able to directly access the data storage entry
            # because it's marked as platform_only=True
            with pytest.raises(DataStorageError, match="not found"):
                await pub_client.afetch_data_from_storage(data_storage_id)

        finally:
            await admin_client.delete_world_model(model_id)

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_public_user_cannot_access_dss_entry_directly_sync(
        self, admin_client: RestClient, pub_client: RestClient
    ):
        test_name = f"E2E Test DSS Access Control Sync {uuid4()}"
        test_content = "Sync test content that should not be directly accessible"

        model = WorldModel(
            content=test_content,
            content_location=ContentLocation.DATA_STORAGE,
            name=test_name,
            description="Sync test world model for DSS access control",
        )

        # Admin creates the world model
        model_id = admin_client.create_world_model(model)

        # Admin retrieves the world model to get the data_storage_id
        retrieved = admin_client.get_world_model(world_model_id=model_id)
        assert retrieved.data_storage_id is not None
        data_storage_id = retrieved.data_storage_id

        # Public user should NOT be able to directly access the data storage entry
        with pytest.raises(DataStorageError, match="not found"):
            pub_client.fetch_data_from_storage(data_storage_id)

        await admin_client.delete_world_model(model_id)

    @pytest.mark.timeout(300)
    @pytest.mark.asyncio
    async def test_admin_cannot_access_dss_entry_directly(
        self, admin_client: RestClient
    ):
        test_name = f"E2E Test Admin DSS Access {uuid4()}"
        test_content = "Admin-accessible DSS content"
        test_metadata = {"admin_test": True}

        model = WorldModel(
            content=test_content,
            content_location=ContentLocation.DATA_STORAGE,
            name=test_name,
            description="Test world model for admin DSS access",
            model_metadata=test_metadata,
        )

        # Admin creates the world model
        model_id = await admin_client.acreate_world_model(model)

        try:
            # Admin retrieves the world model to get the data_storage_id
            retrieved = await admin_client.aget_world_model(world_model_id=model_id)
            assert retrieved.data_storage_id is not None
            data_storage_id = retrieved.data_storage_id

            with pytest.raises(DataStorageError, match="not found"):
                admin_client.fetch_data_from_storage(data_storage_id)

        finally:
            await admin_client.delete_world_model(model_id)
