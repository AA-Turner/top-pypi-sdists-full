from typing import Any
from unittest import TestCase

from pycarlo.features.ingestion.models import (
    AssetField,
    AssetFreshness,
    AssetMetadata,
    AssetVolume,
    RelationalAsset,
    Tag,
    build_metadata_payload,
)


class TestTag(TestCase):
    def test_to_dict(self):
        tag = Tag(key="env", value="prod")
        assert tag.to_dict() == {"key": "env", "value": "prod"}


class TestAssetField(TestCase):
    def test_to_dict_required_only(self):
        f = AssetField(name="id", type="INTEGER")
        assert f.to_dict() == {"name": "id", "type": "INTEGER"}

    def test_to_dict_with_description(self):
        f = AssetField(name="id", type="INTEGER", description="Primary key")
        assert f.to_dict() == {
            "name": "id",
            "type": "INTEGER",
            "description": "Primary key",
        }

    def test_to_dict_omits_none_description(self):
        f = AssetField(name="col", type="TEXT")
        assert "description" not in f.to_dict()


class TestAssetMetadata(TestCase):
    def test_to_dict_required_only(self):
        m = AssetMetadata(name="orders", database="analytics", schema="public")
        assert m.to_dict() == {
            "name": "orders",
            "database": "analytics",
            "schema": "public",
        }

    def test_to_dict_all_fields(self):
        m = AssetMetadata(
            name="orders",
            database="analytics",
            schema="public",
            description="Order records",
            view_query="SELECT * FROM raw.orders",
            created_on="2026-01-01T00:00:00Z",
        )
        result = m.to_dict()
        assert result["description"] == "Order records"
        assert result["view_query"] == "SELECT * FROM raw.orders"
        assert result["created_on"] == "2026-01-01T00:00:00Z"

    def test_to_dict_omits_none_optional_fields(self):
        m = AssetMetadata(name="t", database="db", schema="s")
        result = m.to_dict()
        assert "description" not in result
        assert "view_query" not in result
        assert "created_on" not in result


class TestAssetVolume(TestCase):
    def test_to_dict_with_values(self):
        v = AssetVolume(row_count=100, byte_count=2048)
        assert v.to_dict() == {"row_count": 100, "byte_count": 2048}

    def test_to_dict_partial(self):
        v = AssetVolume(row_count=50)
        assert v.to_dict() == {"row_count": 50}

    def test_to_dict_empty(self):
        v = AssetVolume()
        assert v.to_dict() == {}


class TestAssetFreshness(TestCase):
    def test_to_dict_with_value(self):
        f = AssetFreshness(last_update_time="2026-03-02T10:00:00Z")
        assert f.to_dict() == {"last_update_time": "2026-03-02T10:00:00Z"}

    def test_to_dict_empty(self):
        f = AssetFreshness()
        assert f.to_dict() == {}


class TestRelationalAsset(TestCase):
    def test_to_dict_minimal(self):
        asset = RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(name="t", database="db", schema="s"),
        )
        result = asset.to_dict()
        assert result == {
            "type": "TABLE",
            "metadata": {"name": "t", "database": "db", "schema": "s"},
        }

    def test_to_dict_omits_empty_tags_and_fields(self):
        asset = RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(name="t", database="db", schema="s"),
        )
        result = asset.to_dict()
        assert "tags" not in result
        assert "fields" not in result
        assert "volume" not in result
        assert "freshness" not in result

    def test_to_dict_full(self):
        asset = RelationalAsset(
            type="VIEW",
            metadata=AssetMetadata(
                name="v_orders",
                database="analytics",
                schema="public",
                description="Aggregated orders",
                view_query="SELECT * FROM orders",
            ),
            tags=[Tag(key="team", value="data")],
            fields=[
                AssetField(name="id", type="INTEGER"),
                AssetField(name="name", type="VARCHAR", description="Customer name"),
            ],
            volume=AssetVolume(row_count=500, byte_count=4096),
            freshness=AssetFreshness(last_update_time="2026-03-01T08:30:00Z"),
        )
        result: dict[str, Any] = asset.to_dict()

        assert result["type"] == "VIEW"
        assert result["metadata"]["name"] == "v_orders"
        assert result["metadata"]["view_query"] == "SELECT * FROM orders"
        assert result["tags"] == [{"key": "team", "value": "data"}]
        assert len(result["fields"]) == 2
        assert result["fields"][1]["description"] == "Customer name"
        assert result["volume"] == {"row_count": 500, "byte_count": 4096}
        assert result["freshness"] == {"last_update_time": "2026-03-01T08:30:00Z"}


class TestBuildMetadataPayload(TestCase):
    def test_payload_structure(self):
        asset = RelationalAsset(
            type="TABLE",
            metadata=AssetMetadata(name="orders", database="analytics", schema="public"),
            volume=AssetVolume(row_count=1000),
        )
        payload = build_metadata_payload(
            resource_uuid="res-123",
            resource_type="snowflake",
            events=[asset],
        )

        assert payload["event_type"] == "METADATA"
        assert payload["resource"] == {
            "uuid": "res-123",
            "resource_type": "snowflake",
        }
        assert len(payload["events"]) == 1
        event = payload["events"][0]
        assert "relational_asset" in event
        assert event["relational_asset"]["type"] == "TABLE"
        assert event["relational_asset"]["volume"] == {"row_count": 1000}

    def test_multiple_events(self):
        events = [
            RelationalAsset(
                type="TABLE",
                metadata=AssetMetadata(name=f"table_{i}", database="db", schema="s"),
            )
            for i in range(3)
        ]
        payload = build_metadata_payload(
            resource_uuid="res-456",
            resource_type="bigquery",
            events=events,
        )
        assert len(payload["events"]) == 3
        for i, event in enumerate(payload["events"]):
            assert event["relational_asset"]["metadata"]["name"] == f"table_{i}"
