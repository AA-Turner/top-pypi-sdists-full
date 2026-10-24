from __future__ import annotations

from dataclasses import asdict, fields

from matrx_scraper.coverage import Coverage, CoverageValue


def test_coverage_to_dict_matches_the_typed_dataclass_wire_field_for_field() -> None:
    coverage = Coverage(
        service="structured",
        label="Structured data",
        speed="batch",
        typical_seconds=None,
        unit="record",
        points_per_unit=12,
        returns="records",
        source_key="maps",
        source_label="Maps",
        platform=None,
    )

    actual: CoverageValue = coverage.to_dict()
    assert actual == asdict(coverage)
    assert list(actual) == [field.name for field in fields(Coverage)]
