from agentic_devtools.ai_providers.tier_selector import NoSelection


def test_no_selection_defaults_status_to_reason() -> None:
    assert NoSelection("no_eligible_model").status == "no_eligible_model"
    assert NoSelection("no_eligible_model", status="custom").status == "custom"
