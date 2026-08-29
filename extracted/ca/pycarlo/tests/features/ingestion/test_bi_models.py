from unittest import TestCase

import pytest

from pycarlo.features.ingestion.bi import (
    BI_RELATIONSHIP_TYPE_VALUES,
    AssetRef,
    BiAsset,
    BiAssetRef,
    BiOwner,
    build_bi_metadata_payload,
)
from pycarlo.features.ingestion.models import Tag


def _asset(source_id: str = "dash-1", name: str = "Revenue") -> BiAsset:
    return BiAsset(asset_source_id=source_id, name=name, asset_type="dashboard")


class TestRelationshipTypeValues(TestCase):
    def test_values(self):
        assert BI_RELATIONSHIP_TYPE_VALUES == frozenset(
            {"DERIVES_FROM", "CONTAINED_IN", "REFERENCES"}
        )


class TestBiOwner(TestCase):
    def test_empty_owner_serializes_to_empty_dict(self):
        assert BiOwner().to_dict() == {}

    def test_excludes_none_fields(self):
        assert BiOwner(email="a@b.com").to_dict() == {"email": "a@b.com"}

    def test_full(self):
        result = BiOwner(email="a@b.com", name="A B", source_id="u1").to_dict()
        assert result == {"email": "a@b.com", "name": "A B", "source_id": "u1"}


class TestBiAssetRef(TestCase):
    def test_minimal_excludes_none(self):
        assert BiAssetRef(asset_source_id="m1").to_dict() == {"asset_source_id": "m1"}

    def test_full(self):
        result = BiAssetRef(
            asset_source_id="m1",
            relationship_type="DERIVES_FROM",
        ).to_dict()
        assert result == {
            "asset_source_id": "m1",
            "relationship_type": "DERIVES_FROM",
        }

    def test_rejects_unknown_relationship_type(self):
        with pytest.raises(ValueError, match="relationship_type"):
            BiAssetRef(asset_source_id="m1", relationship_type="BOGUS")

    def test_allows_none_relationship_type(self):
        assert "relationship_type" not in BiAssetRef(asset_source_id="m1").to_dict()


class TestBiAsset(TestCase):
    def test_minimal_only_required_fields(self):
        assert _asset().to_dict() == {
            "asset_source_id": "dash-1",
            "name": "Revenue",
            "asset_type": "dashboard",
        }

    def test_empty_collections_and_none_excluded(self):
        result = _asset().to_dict()
        for absent in (
            "description",
            "asset_url",
            "folder",
            "owner",
            "created_time",
            "view_count",
            "is_certified",
            "upstream_assets",
            "downstream_assets",
            "inputs",
            "properties",
            "attributes",
        ):
            assert absent not in result

    def test_full_asset_nests_children(self):
        asset = BiAsset(
            asset_source_id="dash-1",
            name="Revenue",
            asset_type="dashboard",
            description="Quarterly revenue",
            asset_url="https://bi.example.com/dash-1",
            folder="Finance",
            owner=BiOwner(email="a@b.com"),
            created_time="2026-01-01T00:00:00Z",
            last_modified_time="2026-02-01T00:00:00Z",
            last_viewed_time="2026-03-01T00:00:00Z",
            view_count=42,
            is_certified=True,
            certification_note="Approved",
            is_archived=False,
            upstream_assets=[
                BiAssetRef(asset_source_id="model-1", relationship_type="DERIVES_FROM")
            ],
            downstream_assets=[BiAssetRef(asset_source_id="dash-2")],
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", mcon="MCON++abc")],
            properties=[Tag(key="team", value="finance"), Tag(key="pii")],
            attributes={"vendor": "looker"},
        )
        result = asset.to_dict()
        assert result["view_count"] == 42
        assert result["is_certified"] is True
        assert result["is_archived"] is False
        assert result["owner"] == {"email": "a@b.com"}
        assert result["upstream_assets"] == [
            {"asset_source_id": "model-1", "relationship_type": "DERIVES_FROM"}
        ]
        assert result["downstream_assets"] == [{"asset_source_id": "dash-2"}]
        assert result["properties"] == [{"key": "team", "value": "finance"}, {"key": "pii"}]
        assert result["attributes"] == {"vendor": "looker"}

    def test_inputs_reuse_shared_asset_ref_uppercase_role(self):
        # A BI asset always reads from its warehouse-table inputs, so role=INPUT;
        # role is UPPERCASE on the wire (the normalizer lowercases it).
        asset = BiAsset(
            asset_source_id="dash-1",
            name="Revenue",
            asset_type="dashboard",
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", fully_qualified_name="db.schema.t")],
        )
        result = asset.to_dict()
        assert result["inputs"] == [
            {"asset_type": "TABLE", "role": "INPUT", "fully_qualified_name": "db.schema.t"}
        ]

    def test_wire_field_names_match_contract(self):
        # Pin the full set of serialized wire keys so a renamed/typo'd field is
        # caught (mirrors the ETL suite's key-set guard).
        asset = BiAsset(
            asset_source_id="a",
            name="n",
            asset_type="dashboard",
            description="d",
            asset_url="u",
            folder="f",
            owner=BiOwner(email="e@x.com"),
            created_time="2026-01-01T00:00:00Z",
            last_modified_time="2026-01-01T00:00:00Z",
            last_viewed_time="2026-01-01T00:00:00Z",
            view_count=1,
            is_certified=True,
            certification_note="c",
            is_archived=False,
            upstream_assets=[BiAssetRef(asset_source_id="u1")],
            downstream_assets=[BiAssetRef(asset_source_id="d1")],
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", mcon="MCON++x")],
            properties=[Tag(key="k", value="v")],
            attributes={"x": 1},
        )
        assert set(asset.to_dict().keys()) == {
            "asset_source_id",
            "name",
            "asset_type",
            "description",
            "asset_url",
            "folder",
            "owner",
            "created_time",
            "last_modified_time",
            "last_viewed_time",
            "view_count",
            "is_certified",
            "certification_note",
            "is_archived",
            "upstream_assets",
            "downstream_assets",
            "inputs",
            "properties",
            "attributes",
        }

    def test_from_dict_round_trip(self):
        original = BiAsset(
            asset_source_id="dash-1",
            name="Revenue",
            asset_type="dashboard",
            owner=BiOwner(email="a@b.com"),
            upstream_assets=[BiAssetRef(asset_source_id="m1", relationship_type="DERIVES_FROM")],
            inputs=[AssetRef(asset_type="TABLE", role="INPUT", mcon="MCON++x")],
            properties=[Tag(key="team", value="finance")],
            attributes={"vendor": "looker"},
        )
        assert BiAsset.from_dict(original.to_dict()) == original


class TestBuildBiMetadataPayload(TestCase):
    def test_envelope_shape_flat_events(self):
        payload = build_bi_metadata_payload(
            resource_uuid="res-1",
            resource_type="custom-bi-connector",
            events=[_asset()],
        )
        assert payload["event_type"] == "BI_METADATA"
        assert payload["resource"] == {"uuid": "res-1", "resource_type": "custom-bi-connector"}
        assert len(payload["events"]) == 1
        # Flat events — no per-event ``bi_asset`` wrapper (unlike ETL).
        assert "bi_asset" not in payload["events"][0]
        assert payload["events"][0]["asset_source_id"] == "dash-1"

    def test_accepts_batch_of_100(self):
        events = [_asset(source_id=f"a{i}") for i in range(100)]
        payload = build_bi_metadata_payload("r", "t", events)
        assert len(payload["events"]) == 100

    def test_rejects_empty_batch(self):
        with pytest.raises(ValueError, match="between 1 and 100"):
            build_bi_metadata_payload("r", "t", [])

    def test_rejects_batch_over_100(self):
        events = [_asset(source_id=f"a{i}") for i in range(101)]
        with pytest.raises(ValueError, match="between 1 and 100"):
            build_bi_metadata_payload("r", "t", events)
