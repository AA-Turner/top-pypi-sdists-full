from argparse import Namespace

import pytest
from connector.cli import build_loggable_args, redact_json_obj
from connector.oai.integration import DescriptionData, Integration
from pydantic import BaseModel, Field


class TestCli:
    @pytest.mark.parametrize(
        "json_obj, secret_fields, expected",
        [
            ({"a": "b"}, [], {"a": "b"}),
            ({"a": "b", "password": "c"}, [], {"a": "b", "password": "REDACTED"}),
            (
                {"a": "b", "extra_secret": "c"},
                ["extra_secret"],
                {"a": "b", "extra_secret": "REDACTED"},
            ),
            (
                {"a": "b", "nested": {"password": "secret", "other": "value"}},
                [],
                {"a": "b", "nested": {"password": "REDACTED", "other": "value"}},
            ),
            (
                {"a": "b", "list": [{"token": "secret"}, {"api_key": "key"}]},
                [],
                {"a": "b", "list": [{"token": "REDACTED"}, {"api_key": "REDACTED"}]},
            ),
        ],
    )
    def test_redact_json_obj(self, json_obj, secret_fields, expected) -> None:
        redact_json_obj(json_obj, secret_fields)
        assert json_obj == expected

    def test_build_loggable_args_without_json(self):
        # Create a mock Integration with no secret fields
        class MockSettings(BaseModel):
            normal_field: str = Field(json_schema_extra={})

        mock_integration = Integration(
            settings_model=MockSettings,
            app_id="test-app",
            version="1.0.0",
            exception_handlers=[],
            description_data=DescriptionData(
                user_friendly_name="Test Integration",
                description="Test integration for unit tests",
                categories=[],
            ),
        )

        args = Namespace(command="test", use_proxy=False, result_file_path=None)

        result = build_loggable_args(args, mock_integration)
        assert result == {"command": "test", "use_proxy": False, "result_file_path": None}

    def test_build_loggable_args_with_json_and_secrets(self) -> None:
        # Create a mock Integration with secret fields
        class MockSettings(BaseModel):
            api_key: str = Field(json_schema_extra={"x-secret": True})
            normal_field: str = Field(json_schema_extra={})

        mock_integration = Integration(
            settings_model=MockSettings,
            app_id="test-app",
            version="1.0.0",
            exception_handlers=[],
            description_data=DescriptionData(
                user_friendly_name="Test Integration",
                description="Test integration for unit tests",
                categories=[],
            ),
        )

        args = Namespace(
            command="test",
            json='{"auth": {"api_key": "secret123"}, "settings": {"normal_field": "value"}}',
            use_proxy=False,
        )

        result = build_loggable_args(args, mock_integration)
        assert result["command"] == "test"
        assert result["use_proxy"] is False
        assert result["json"]["auth"]["api_key"] == "REDACTED"
        assert result["json"]["settings"]["normal_field"] == "value"

    def test_build_loggable_args_with_nested_json(self) -> None:
        # Create a mock Integration with secret fields
        class MockSettings(BaseModel):
            password: str = Field(json_schema_extra={"x-secret": True})

        mock_integration = Integration(
            settings_model=MockSettings,
            app_id="test-app",
            version="1.0.0",
            exception_handlers=[],
            description_data=DescriptionData(
                user_friendly_name="Test Integration",
                description="Test integration for unit tests",
                categories=[],
            ),
        )

        args = Namespace(
            command="test",
            json='{"nested": {"auth": {"password": "secret123"}}, "other": "value"}',
            use_proxy=False,
        )

        result = build_loggable_args(args, mock_integration)
        assert result["command"] == "test"
        assert result["use_proxy"] is False
        assert result["json"]["nested"]["auth"]["password"] == "REDACTED"
        assert result["json"]["other"] == "value"
