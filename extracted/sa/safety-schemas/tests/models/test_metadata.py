import dataclasses
from datetime import timedelta

from safety_schemas.models import (
    AuthenticationType,
    MetadataModel,
    ReportSchemaVersion,
    ScanType,
    Stage,
    TelemetryModel,
)


def _build_metadata() -> MetadataModel:
    """A MetadataModel with every required field set, letting timestamp default."""
    return MetadataModel(
        scan_type=ScanType.scan,
        stage=Stage.development,
        scan_locations=[],
        authenticated=True,
        authentication_type=AuthenticationType.API_KEY,
        telemetry=TelemetryModel(
            safety_options={},
            safety_version="1.0.0",
            safety_source="cli",
        ),
        schema_version=ReportSchemaVersion.v3_0,
    )


class TestMetadataTimestamp:
    def test_default_timestamp_is_timezone_aware_utc(self):
        # A naive timestamp is silently misread as UTC on ingest, skewing the
        # stored scan time by the client's UTC offset. The default must be aware
        # and UTC so the serialized instant is unambiguous.
        timestamp = _build_metadata().timestamp

        assert timestamp.tzinfo is not None, "timestamp must be timezone-aware"
        assert timestamp.utcoffset() == timedelta(0), "timestamp must be UTC"

    def test_default_timestamp_uses_default_factory(self):
        # A bare `datetime.now()` default is evaluated once at import, so every
        # instance would share one frozen value. A default_factory is re-run per
        # instance, capturing the real construction time.
        timestamp_field = {f.name: f for f in dataclasses.fields(MetadataModel)}[
            "timestamp"
        ]

        assert timestamp_field.default_factory is not dataclasses.MISSING
        assert timestamp_field.default is dataclasses.MISSING
