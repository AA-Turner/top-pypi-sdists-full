import pytest
from statsig_python_core import Statsig, StatsigOptions, StatsigUser
from mock_scrapi import MockScrapi
from utils import get_test_data_resource
from pytest_httpserver import HTTPServer


@pytest.fixture
def statsig_setup(httpserver: HTTPServer):
    mock_scrapi = MockScrapi(httpserver)
    dcs_content = get_test_data_resource("eval_proj_dcs.json")
    mock_scrapi.stub(
        "/v2/download_config_specs", response=dcs_content, method="GET"
    )
    mock_scrapi.stub("/v1/log_event", response='{"success": true}', method="POST")

    options = StatsigOptions()
    options.specs_url = mock_scrapi.url_for_endpoint("/v2/download_config_specs")
    options.log_event_url = mock_scrapi.url_for_endpoint("/v1/log_event")
    options.output_log_level = "none"

    statsig = Statsig("secret-key", options)
    statsig.initialize().wait()

    yield statsig, mock_scrapi

    statsig.shutdown().wait()


def test_logged_complex_user_fields(statsig_setup):
    statsig, mock_scrapi = statsig_setup
    user = StatsigUser(
        user_id="dloomb",
        custom={
            "is_employee": True,
            "custom_field": "custom_value",
            "number_field": 42,
            "score": 95.5,
            "array_field": ["value1", 23, True],
            "object_field": {
                "key": "value",
                "nested": {"key": "nested_value"},
                "number_field": 123,
                "array_field": ["item1", "item2"],
            },
            "emoji_string": "🚀",
            "emoji_array": ["🚀", "🚀"],
            "emoji_object": {"key": "🚀"},
            "non_english_string": "大",
            "unpaired_surrogate": "\ud800",
        },
        private_attributes={"do_not_log": True},
        custom_ids={"workID": "a_work_id"},
    )

    statsig.check_gate(user, "test_public")
    statsig.flush_events().wait()
    events = mock_scrapi.get_logged_events()

    assert len(events) == 1
    event = events[0]

    assert event["eventName"] == "statsig::gate_exposure"

    assert "user" in event
    user_data = event["user"]
    assert user_data["userID"] == "dloomb"

    custom = user_data["custom"]
    assert custom["is_employee"] is True
    assert custom["custom_field"] == "custom_value"
    assert user_data["customIDs"] == {"workID": "a_work_id"}
    assert custom["score"] == 95.5
    assert custom["number_field"] == 42
    assert custom["array_field"] == ["value1", 23, True]
    assert custom["object_field"]["key"] == "value"
    assert custom["object_field"]["nested"]["key"] == "nested_value"
    assert custom["object_field"]["number_field"] == 123
    assert custom["object_field"]["array_field"] == ["item1", "item2"]

    assert custom["emoji_string"] == "🚀"
    assert custom["emoji_array"] == ["🚀", "🚀"]
    assert custom["emoji_object"]["key"] == "🚀"
    assert custom["non_english_string"] == "大"
    assert custom.get("unpaired_surrogate") is None

    assert user_data.get("privateAttributes") is None


def test_accessed_unicode_user_fields():
    user = StatsigUser(
        user_id="user",
        custom={
            "emoji_string": "🚀",
            "emoji_array": ["🚀", "🚀"],
            "emoji_object": {"key": "🚀"},
            "non_english_string": "大",
            "unpaired_surrogate": "\ud800",
        },
    )
    assert user.custom["emoji_string"] == "🚀"
    assert user.custom["emoji_array"] == ["🚀", "🚀"]
    assert user.custom["emoji_object"]["key"] == "🚀"
    assert user.custom["non_english_string"] == "大"
    assert user.custom.get("unpaired_surrogate") is None


def test_exposures_snapshot_user_email_and_deduplicate_repeated_gate(statsig_setup):
    statsig, mock_scrapi = statsig_setup
    user = StatsigUser("test_user_123", email="before@example.com", country="US")
    statsig.check_gate(user, "test_public")
    user.email = "after@example.com"
    statsig.check_gate(user, "test_public")
    statsig.check_gate(user, "test_email")
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    assert len(events) == 2
    users_by_gate = {}
    for event in events:
        assert event["eventName"] == "statsig::gate_exposure"
        assert event["user"]["userID"] == "test_user_123"
        assert event["user"]["country"] == "US"
        users_by_gate[event["metadata"]["gate"]] = event["user"]["email"]
    assert users_by_gate == {
        "test_public": "before@example.com",
        "test_email": "after@example.com",
    }


def test_exposure_with_empty_user_id(statsig_setup):
    """Test that exposures work correctly with empty user ID."""
    statsig, mock_scrapi = statsig_setup
    user = StatsigUser()  # Empty user ID

    statsig.check_gate(user, "test_public")
    statsig.flush_events().wait()

    events = mock_scrapi.get_logged_events()
    gate_exposures = [e for e in events if e["eventName"] == "statsig::gate_exposure"]

    assert len(gate_exposures) == 1
    event = gate_exposures[0]

    # User ID should be empty string or not present
    user_data = event.get("user", {})
    user_id = user_data.get("userID", "")
    assert user_id == "" or user_id is None
