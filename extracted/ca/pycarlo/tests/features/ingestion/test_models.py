from datetime import datetime
from typing import Any
from unittest import TestCase

from pycarlo.features.ingestion.models import (
    AssetField,
    AssetFreshness,
    AssetMetadata,
    AssetVolume,
    ColumnLineageField,
    ColumnLineageSourceField,
    LineageAssetRef,
    LineageEvent,
    LineageEventType,
    QueryLogEntry,
    RelationalAsset,
    Tag,
    build_lineage_payload,
    build_metadata_payload,
    build_query_log_payload,
)


class TestTag(TestCase):
    def test_to_dict_key_value(self):
        tag = Tag(key="env", value="prod")
        assert tag.to_dict() == {"key": "env", "value": "prod"}

    def test_to_dict_key_only(self):
        tag = Tag(key="pii")
        assert tag.to_dict() == {"key": "pii"}

    def test_to_dict_key_with_none_value(self):
        tag = Tag(key="sensitive", value=None)
        assert tag.to_dict() == {"key": "sensitive"}


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


def _dt(iso: str) -> datetime:
    """Parse ISO8601 string to datetime for tests."""
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))


class TestQueryLogEntry(TestCase):
    def test_to_dict_minimal(self):
        entry = QueryLogEntry(
            start_time=_dt("2026-03-02T10:00:00Z"),
            end_time=_dt("2026-03-02T10:00:05Z"),
            query_text="SELECT * FROM orders",
        )
        result = entry.to_dict()
        assert result == {
            "start_time": "2026-03-02T10:00:00Z",
            "end_time": "2026-03-02T10:00:05Z",
            "query_text": "SELECT * FROM orders",
        }

    def test_to_dict_full(self):
        entry = QueryLogEntry(
            start_time=_dt("2026-03-02T10:00:00Z"),
            end_time=_dt("2026-03-02T10:00:05Z"),
            query_text="SELECT * FROM orders",
            query_id="q-123",
            user="analyst@example.com",
            error_code=None,
            error_text=None,
            returned_rows=1000,
            extra={"warehouse": "COMPUTE_WH"},
        )
        result = entry.to_dict()
        assert result["query_id"] == "q-123"
        assert result["user"] == "analyst@example.com"
        assert result["returned_rows"] == 1000
        assert result["extra"] == {"warehouse": "COMPUTE_WH"}
        assert "error_code" not in result
        assert "error_text" not in result

    def test_to_dict_with_error(self):
        entry = QueryLogEntry(
            start_time=_dt("2026-03-02T10:00:00Z"),
            end_time=_dt("2026-03-02T10:00:01Z"),
            query_text="SELECT * FROM invalid",
            error_code=100132,
            error_text="Object does not exist",
        )
        result = entry.to_dict()
        assert result["error_code"] == 100132
        assert result["error_text"] == "Object does not exist"

    def test_from_dict_round_trip(self):
        """Datetime fields deserialize from ISO8601 strings."""
        d = {
            "start_time": "2026-03-02T10:00:00Z",
            "end_time": "2026-03-02T10:00:05Z",
            "query_text": "SELECT 1",
        }
        entry = QueryLogEntry.from_dict(d)
        assert entry.start_time == _dt("2026-03-02T10:00:00Z")
        assert entry.end_time == _dt("2026-03-02T10:00:05Z")
        assert entry.query_text == "SELECT 1"


class TestBuildQueryLogPayload(TestCase):
    def test_payload_structure(self):
        entry = QueryLogEntry(
            start_time=_dt("2026-03-02T10:00:00Z"),
            end_time=_dt("2026-03-02T10:00:05Z"),
            query_text="SELECT 1",
        )
        payload = build_query_log_payload(
            resource_uuid="res-123",
            log_type="snowflake",
            events=[entry],
        )
        assert payload["event_type"] == "QUERY_LOG"
        assert payload["resource"] == {
            "uuid": "res-123",
            "log_type": "snowflake",
        }
        assert len(payload["events"]) == 1
        assert payload["events"][0]["start_time"] == "2026-03-02T10:00:00Z"
        assert payload["events"][0]["query_text"] == "SELECT 1"

    def test_multiple_events(self):
        events = [
            QueryLogEntry(
                start_time=_dt("2026-03-02T10:00:00Z"),
                end_time=_dt("2026-03-02T10:00:01Z"),
                query_text=f"SELECT {i}",
            )
            for i in range(3)
        ]
        payload = build_query_log_payload(
            resource_uuid="res-456",
            log_type="bigquery",
            events=events,
        )
        assert len(payload["events"]) == 3
        for i, event in enumerate(payload["events"]):
            assert event["query_text"] == f"SELECT {i}"


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


# ---------------------------------------------------------------
# Lineage models
# ---------------------------------------------------------------


class TestLineageAssetRef(TestCase):
    def test_to_dict_required_only(self):
        ref = LineageAssetRef(type="TABLE", name="t", database="db", schema="s")
        result = ref.to_dict()
        assert result["type"] == "TABLE"
        assert result["name"] == "t"
        assert result["database"] == "db"
        assert result["schema"] == "s"

    def test_to_dict_omits_none_asset_id(self):
        ref = LineageAssetRef(type="TABLE", name="t", database="db", schema="s")
        assert "asset_id" not in ref.to_dict()

    def test_to_dict_includes_asset_id_when_set(self):
        ref = LineageAssetRef(type="TABLE", name="t", database="db", schema="s", asset_id="src1")
        assert ref.to_dict()["asset_id"] == "src1"


class TestColumnLineageSourceField(TestCase):
    def test_to_dict(self):
        f = ColumnLineageSourceField(asset_id="src1", field_name="amount")
        assert f.to_dict() == {"asset_id": "src1", "field_name": "amount"}


class TestColumnLineageField(TestCase):
    def test_to_dict(self):
        f = ColumnLineageField(
            name="total",
            source_fields=[
                ColumnLineageSourceField(asset_id="src1", field_name="amount"),
                ColumnLineageSourceField(asset_id="src2", field_name="price"),
            ],
        )
        result: dict[str, Any] = f.to_dict()
        assert result["name"] == "total"
        assert len(result["source_fields"]) == 2
        assert result["source_fields"][0] == {"asset_id": "src1", "field_name": "amount"}


class TestLineageEvent(TestCase):
    def test_to_dict_table_level(self):
        event = LineageEvent(
            destination=LineageAssetRef(
                type="TABLE", database="analytics", schema="pub", name="out"
            ),
            sources=[
                LineageAssetRef(type="TABLE", database="raw", schema="pub", name="in1"),
            ],
        )
        result: dict[str, Any] = event.to_dict()
        assert result["destination"]["name"] == "out"
        assert len(result["sources"]) == 1
        assert result["sources"][0]["name"] == "in1"

    def test_to_dict_omits_empty_fields(self):
        event = LineageEvent(
            destination=LineageAssetRef(type="TABLE", database="db", schema="s", name="t"),
            sources=[LineageAssetRef(type="TABLE", database="db", schema="s", name="s")],
        )
        assert "fields" not in event.to_dict()

    def test_to_dict_includes_fields_when_set(self):
        event = LineageEvent(
            destination=LineageAssetRef(type="TABLE", database="db", schema="s", name="t"),
            sources=[
                LineageAssetRef(
                    type="TABLE", database="db", schema="s", name="src", asset_id="src1"
                ),
            ],
            fields=[
                ColumnLineageField(
                    name="total",
                    source_fields=[
                        ColumnLineageSourceField(asset_id="src1", field_name="amount"),
                    ],
                ),
            ],
        )
        result: dict[str, Any] = event.to_dict()
        assert len(result["fields"]) == 1
        assert result["fields"][0]["name"] == "total"
        assert result["sources"][0]["asset_id"] == "src1"


class TestBuildLineagePayload(TestCase):
    def _make_table_event(self) -> LineageEvent:
        return LineageEvent(
            destination=LineageAssetRef(
                type="TABLE", database="analytics", schema="pub", name="out"
            ),
            sources=[
                LineageAssetRef(type="TABLE", database="raw", schema="pub", name="orders"),
                LineageAssetRef(type="TABLE", database="raw", schema="pub", name="customers"),
            ],
        )

    def _make_column_event(self) -> LineageEvent:
        return LineageEvent(
            destination=LineageAssetRef(type="TABLE", database="db", schema="s", name="dst"),
            sources=[
                LineageAssetRef(
                    type="TABLE", database="db", schema="s", name="src", asset_id="src1"
                ),
            ],
            fields=[
                ColumnLineageField(
                    name="total",
                    source_fields=[
                        ColumnLineageSourceField(asset_id="src1", field_name="amount"),
                    ],
                ),
            ],
        )

    def test_payload_structure_table_lineage(self):
        payload = build_lineage_payload(
            resource_uuid="res-123",
            resource_type="snowflake",
            events=[self._make_table_event()],
        )
        assert payload["event_type"] == "LINEAGE"
        assert payload["resource"] == {
            "uuid": "res-123",
            "resource_type": "snowflake",
        }
        assert len(payload["events"]) == 1
        assert payload["events"][0]["destination"]["name"] == "out"
        assert len(payload["events"][0]["sources"]) == 2

    def test_auto_detects_column_lineage(self):
        payload = build_lineage_payload(
            resource_uuid="res-123",
            resource_type="snowflake",
            events=[self._make_column_event()],
        )
        assert payload["event_type"] == "COLUMN_LINEAGE"
        assert "fields" in payload["events"][0]

    def test_auto_detects_column_lineage_with_mixed_events(self):
        payload = build_lineage_payload(
            resource_uuid="res-123",
            resource_type="snowflake",
            events=[self._make_table_event(), self._make_column_event()],
        )
        assert payload["event_type"] == "COLUMN_LINEAGE"

    def test_explicit_event_type_enum_overrides_auto_detection(self):
        payload = build_lineage_payload(
            resource_uuid="res-123",
            resource_type="snowflake",
            events=[self._make_column_event()],
            event_type=LineageEventType.LINEAGE,
        )
        assert payload["event_type"] == "LINEAGE"

    def test_explicit_event_type_string_overrides_auto_detection(self):
        payload = build_lineage_payload(
            resource_uuid="res-123",
            resource_type="snowflake",
            events=[self._make_column_event()],
            event_type="LINEAGE",
        )
        assert payload["event_type"] == "LINEAGE"

    def test_lineage_event_type_enum_values(self):
        assert LineageEventType.LINEAGE.value == "LINEAGE"
        assert LineageEventType.COLUMN_LINEAGE.value == "COLUMN_LINEAGE"

    def test_multiple_events(self):
        events = [self._make_table_event() for _ in range(3)]
        payload = build_lineage_payload(
            resource_uuid="res-456",
            resource_type="bigquery",
            events=events,
        )
        assert len(payload["events"]) == 3
