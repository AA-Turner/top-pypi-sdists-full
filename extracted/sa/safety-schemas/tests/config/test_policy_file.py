from dataclasses import astuple
import datetime
from glob import glob
from pathlib import Path
from pydantic import ValidationError

import pytest
from safety_schemas.models import ConfigModel, SecurityUpdates, IgnoreCodes, InstallationAction, PackageEcosystem
from safety_schemas.config.schemas.v3_0.main import (
    DeniedPackageCriteria,
    parse_duration_to_seconds,
)

def get_nested_attr(obj, attr_name):
    attrs = attr_name.split('.')
    for attr in attrs:
        obj = getattr(obj, attr)
    return obj


class TestPolicyFile:

    def setUp(self) -> None:
        return super().setUp()
    
    def _assert_default(self, config: ConfigModel):
        expected = {
            "telemetry_enabled": True,
            "scan.max_depth": 6,
            "scan.ignore": [],
            "scan.include_files": {},
            "scan.system_targets": []
        }

        for key, expected in expected.items():
            assert get_nested_attr(config, key) == expected, f"{key} does not match expected value '{expected}'"

    def _assert_full(self, config: ConfigModel):
        expected = {
            "depedendency_vulnerability.enabled": True,
            "depedendency_vulnerability.python_ignore.unpinned_specifications": True,
            "depedendency_vulnerability.python_ignore.environment_results": True,
            "depedendency_vulnerability.security_updates.auto_security_updates_limit": [SecurityUpdates.UpdateLevel.PATCH]
        }

        for key, expected in expected.items():
            assert get_nested_attr(config, key) == expected, f"{key} does not match expected value '{expected}'"

        EXPECTED_IDS = {
            "59901": {
                "reason": "We are not impacted by this vulnerability", 
                "expires": datetime.date(2024, 3, 15)},
            "62044": {
                "reason": "No upstream python images provide updated pip yet", 
                "expires": datetime.date(2024, 6, 1)}
        }

        for vuln_id, ignoredDetail in config.depedendency_vulnerability.ignore_vulnerabilities.items():            
            assert ignoredDetail.reason == EXPECTED_IDS[vuln_id]["reason"], f"reason does not match expected value '{EXPECTED_IDS[vuln_id]['reason']}'"
            assert ignoredDetail.expires == EXPECTED_IDS[vuln_id]["expires"], f"expires does not match expected value '{EXPECTED_IDS[vuln_id]['expires']}'"
            assert ignoredDetail.code == IgnoreCodes.manual

    def _assert_gateway(self, config: ConfigModel):
        expected = {
           "installation.default_action": InstallationAction.allow,
           "installation.audit_logging.enabled": True,
        }

        for key, expected in expected.items():
            assert get_nested_attr(config, key) == expected, f"{key} does not match expected value '{expected}'"

    def _assert_gateway_npmjs(self, config: ConfigModel):
        self._assert_gateway(config)

        expected_packages_def = {
            "installation.allow.packages": (PackageEcosystem.npmjs, ["react@19", "@angular/core@18"]),
            "installation.deny.packages.block.packages": (PackageEcosystem.npmjs, ["react"]),
            "installation.deny.packages.warn.packages": (PackageEcosystem.npmjs, ["react"]),
        }

        for key, package_def in expected_packages_def.items():
            assert astuple(get_nested_attr(config, key)[0]) == package_def, f"{key} does not match expected value '{package_def}'"

    @pytest.mark.parametrize("assert_type, policy_file_path", [(Path(file_path).stem.split('-')[0], Path(file_path)) for file_path in glob('tests/config/data/v30/*.yml')])
    def test_policy_file_parsing(self, assert_type: str, policy_file_path: Path):
        FAIL_VALIDATION = ["typo"]

        if assert_type in FAIL_VALIDATION:
            with pytest.raises(ValidationError):
                config = ConfigModel.parse_policy_file(raw_report=policy_file_path)
        else:
            config = ConfigModel.parse_policy_file(raw_report=policy_file_path)

            assert_method = getattr(self, f"_assert_{assert_type}")
            assert_method(config)


class TestDurationParsing:
    """Tests for the duration parsing helper function."""

    @pytest.mark.parametrize("duration,expected_seconds", [
        ("1 day", 86400),
        ("2 years", 63072000),
    ])
    def test_valid_duration_formats(self, duration, expected_seconds):
        """Test that valid duration formats are parsed correctly."""
        assert parse_duration_to_seconds(duration) == expected_seconds


class TestAgeConstraintValidation:
    """Tests for the version_age_below <= age_below validation."""

    def test_valid_constraint_version_less_than_age(self):
        """Test that version_age_below < age_below is valid."""
        criteria = DeniedPackageCriteria(
            age_below="3 months",
            version_age_below="1 month"
        )
        assert criteria.age_below == "3 months"
        assert criteria.version_age_below == "1 month"

    def test_valid_constraint_version_equals_age(self):
        """Test that version_age_below == age_below is valid."""
        criteria = DeniedPackageCriteria(
            age_below="1 month",
            version_age_below="1 month"
        )
        assert criteria.age_below == "1 month"
        assert criteria.version_age_below == "1 month"

    def test_invalid_constraint_version_greater_than_age(self):
        """Test that version_age_below > age_below raises ValidationError."""
        with pytest.raises(ValidationError):
            DeniedPackageCriteria(
                age_below="1 month",
                version_age_below="3 months"
            )

    def test_only_age_below_specified(self):
        """Test that only age_below can be specified without version_age_below."""
        criteria = DeniedPackageCriteria(age_below="3 months")
        assert criteria.age_below == "3 months"
        assert criteria.version_age_below is None

    def test_only_version_age_below_specified(self):
        """Test that only version_age_below can be specified without age_below."""
        criteria = DeniedPackageCriteria(version_age_below="1 month")
        assert criteria.version_age_below == "1 month"
        assert criteria.age_below is None

