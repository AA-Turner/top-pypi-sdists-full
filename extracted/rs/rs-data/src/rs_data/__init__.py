"""rs_data — RegScale gRPC contract library.

Generated from Protocol Buffer definitions in proto/.

Quick start
-----------
.. code-block:: python

    import grpc
    from rs_data import AssetBase, AssetUpsert
    from rs_data.v1 import asset_service_pb2_grpc

    channel = grpc.secure_channel("ingest.regscale.internal:443", grpc.ssl_channel_credentials())
    stub = asset_service_pb2_grpc.AssetIngestionServiceStub(channel)

    asset = AssetBase(name="my-server", ip_address="10.0.0.1", asset_type="Server")
    request = AssetUpsert(base=asset, source="my-scanner")

All generated service stubs are accessed via rs_data.v1:
    from rs_data.v1 import asset_service_pb2_grpc, issue_service_pb2_grpc, vuln_service_pb2_grpc
"""
# These imports succeed only after code generation has been run.
# In CI, generation always precedes packaging. Locally, run:
#   python scripts/generate_python.py
from rs_data.v1.asset_pb2 import (
    AssetBase,
    AssetResponse,
    AssetUpsert,
    BatchCreateOrUpdateAssetsRequest,
    BatchCreateOrUpdateAssetsResponse,
    BatchCreateOrUpdateOptions,
)
from rs_data.v1.issue_pb2 import (
    BatchUpsertIssuesOptions,
    BatchUpsertIssuesRequest,
    BatchUpsertIssuesResponse,
    IssueBase,
    IssueResponse,
    IssueSeverity,
    IssueStatus,
    IssueUpsert,
)
from rs_data.v1.vuln_pb2 import (
    BatchUpsertVulnsOptions,
    BatchUpsertVulnsRequest,
    BatchUpsertVulnsResponse,
    VulnBase,
    VulnResponse,
    VulnerabilitySeverity,
    VulnerabilityStatus,
    VulnUpsert,
)

__all__ = [
    # Assets
    "AssetBase",
    "AssetUpsert",
    "AssetResponse",
    "BatchCreateOrUpdateAssetsRequest",
    "BatchCreateOrUpdateAssetsResponse",
    "BatchCreateOrUpdateOptions",
    # Issues
    "IssueBase",
    "IssueUpsert",
    "IssueResponse",
    "IssueSeverity",
    "IssueStatus",
    "BatchUpsertIssuesRequest",
    "BatchUpsertIssuesResponse",
    "BatchUpsertIssuesOptions",
    # Vulns
    "VulnBase",
    "VulnUpsert",
    "VulnResponse",
    "VulnerabilitySeverity",
    "VulnerabilityStatus",
    "BatchUpsertVulnsRequest",
    "BatchUpsertVulnsResponse",
    "BatchUpsertVulnsOptions",
]
