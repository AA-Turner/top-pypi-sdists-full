"""Smoke tests verifying generated protobuf stubs are importable and functional.

These tests run AFTER code generation (scripts/generate_python.py). They catch:
  - import path fixing regressions (wrong relative imports after flattening)
  - enum value drift between proto source and generated stubs
  - serialization regressions in the protobuf runtime
  - missing gRPC service stub attributes
"""


def test_asset_pb2_importable():
    from rs_data.v1 import asset_pb2

    assert asset_pb2 is not None


def test_issue_pb2_importable():
    from rs_data.v1 import issue_pb2

    assert issue_pb2 is not None


def test_vuln_pb2_importable():
    from rs_data.v1 import vuln_pb2

    assert vuln_pb2 is not None


def test_top_level_api_importable():
    from rs_data import AssetBase, IssueBase, VulnBase

    assert AssetBase is not None
    assert IssueBase is not None
    assert VulnBase is not None


def test_asset_base_field_assignment():
    from rs_data import AssetBase

    asset = AssetBase()
    asset.name = "web-server-01"
    asset.ip_address = "10.0.0.1"
    asset.asset_type = "Server"
    assert asset.name == "web-server-01"
    assert asset.ip_address == "10.0.0.1"


def test_asset_upsert_has_base_and_source():
    from rs_data import AssetBase, AssetUpsert

    upsert = AssetUpsert()
    assert hasattr(upsert, "base")
    assert isinstance(upsert.base, AssetBase)
    assert hasattr(upsert, "source")


def test_issue_severity_enum_values():
    from rs_data import IssueSeverity

    assert IssueSeverity.Value("ISSUE_SEVERITY_UNSPECIFIED") == 0
    assert IssueSeverity.Value("ISSUE_SEVERITY_LOW") == 1
    assert IssueSeverity.Value("ISSUE_SEVERITY_MODERATE") == 2
    assert IssueSeverity.Value("ISSUE_SEVERITY_HIGH") == 3
    assert IssueSeverity.Value("ISSUE_SEVERITY_CRITICAL") == 4


def test_issue_status_enum_values():
    from rs_data import IssueStatus

    assert IssueStatus.Value("ISSUE_STATUS_UNSPECIFIED") == 0
    assert IssueStatus.Value("ISSUE_STATUS_OPEN") == 1
    assert IssueStatus.Value("ISSUE_STATUS_CLOSED") == 2


def test_vuln_severity_enum_values():
    from rs_data import VulnerabilitySeverity

    assert VulnerabilitySeverity.Value("VULNERABILITY_SEVERITY_UNSPECIFIED") == 0
    assert VulnerabilitySeverity.Value("VULNERABILITY_SEVERITY_INFORMATIONAL") == 1
    assert VulnerabilitySeverity.Value("VULNERABILITY_SEVERITY_CRITICAL") == 5


def test_vuln_status_enum_values():
    from rs_data import VulnerabilityStatus

    assert VulnerabilityStatus.Value("VULNERABILITY_STATUS_UNSPECIFIED") == 0
    assert VulnerabilityStatus.Value("VULNERABILITY_STATUS_OPEN") == 1
    assert VulnerabilityStatus.Value("VULNERABILITY_STATUS_MITIGATED") == 9


def test_asset_base_serialization_roundtrip():
    from rs_data import AssetBase

    original = AssetBase()
    original.name = "db-server"
    original.ip_address = "192.168.1.100"
    original.asset_type = "Database Server"
    serialized = original.SerializeToString()
    restored = AssetBase()
    restored.ParseFromString(serialized)
    assert restored.name == "db-server"
    assert restored.ip_address == "192.168.1.100"
    assert restored.asset_type == "Database Server"


def test_issue_base_serialization_roundtrip():
    from rs_data import IssueBase, IssueSeverity, IssueStatus

    original = IssueBase()
    original.title = "Weak cipher suite"
    original.severity = IssueSeverity.Value("ISSUE_SEVERITY_HIGH")
    original.status = IssueStatus.Value("ISSUE_STATUS_OPEN")
    original.source = "Qualys"
    serialized = original.SerializeToString()
    restored = IssueBase()
    restored.ParseFromString(serialized)
    assert restored.title == "Weak cipher suite"
    assert restored.severity == 3  # ISSUE_SEVERITY_HIGH
    assert restored.source == "Qualys"


def test_grpc_asset_stub_has_expected_methods():
    from rs_data.v1 import asset_service_pb2_grpc

    assert hasattr(asset_service_pb2_grpc, "AssetIngestionServiceStub")


def test_grpc_issue_stub_has_expected_methods():
    from rs_data.v1 import issue_service_pb2_grpc

    assert hasattr(issue_service_pb2_grpc, "IssueIngestionServiceStub")


def test_grpc_vuln_stub_has_expected_methods():
    from rs_data.v1 import vuln_service_pb2_grpc

    assert hasattr(vuln_service_pb2_grpc, "VulnIngestionServiceStub")
