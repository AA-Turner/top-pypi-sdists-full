import pytest
from matrx_graph.contracts.audit import audit_model
from pydantic import ValidationError

from matrx_ai.tools.kinds.google import GoogleMarketingResult


def test_google_marketing_workflow_result_has_no_type_leaks():
    report = audit_model(GoogleMarketingResult)
    assert not report.leaks, report


@pytest.mark.parametrize(
    "fields",
    [
        {"bounds": {"start_date": "2026-10-01", "limit": 10, "filters": ["organic"]}},
        {"checks": [{"id": "ga4_installed", "question": "Is GA4 installed?",
                     "verdict": "pass", "evidence": "One active configuration tag."}]},
        {"checks": [{"id": "conversion_tracking", "question": "Is conversion tracking present?",
                     "verdict": "fail", "evidence": "No active conversion tag.",
                     "remedy": "Add a conversion tag."}]},
        {"containers": [{"account_id": "123", "account": "Marketing",
                         "container_id": "456", "container": "Website",
                         "public_id": "GTM-ABC", "usage_context": ["web"]}]},
        {"containers": [{"container_id": "456", "container": "Website",
                         "workspace": "Default", "active_tags": 3, "paused_tags": 1}]},
    ],
)
def test_google_marketing_contract_preserves_branch_fields(fields):
    payload = {"__kind": "google_marketing_result", "action": "tracking_health", **fields}
    result = GoogleMarketingResult.model_validate(payload)
    assert result.model_dump(mode="json", by_alias=True, exclude_unset=True) == payload


@pytest.mark.parametrize(
    "fields",
    [
        {"bounds": {"limit": object()}},
        {"checks": [{"id": "ga4_installed", "question": "Is GA4 installed?",
                     "verdict": "invented", "evidence": "No evidence."}]},
        {"containers": [{"container_id": "456", "container": "Website", "active_tags": []}]},
    ],
)
def test_google_marketing_contract_rejects_untyped_branch_values(fields):
    with pytest.raises(ValidationError):
        GoogleMarketingResult.model_validate(fields)
