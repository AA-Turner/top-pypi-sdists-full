from argparse import Namespace
from typing import Any

from connector.cli import build_loggable_args, redact_json_obj
from connector.oai.integration import DescriptionData, Integration
from pydantic import BaseModel, Field


class TestCli:
    def test_redact_json_obj_success_redact_secrets(self) -> None:
        """Test that redact_json_obj properly redacts sensitive fields in various data structures."""
        # Test data similar to the example provided
        json_obj: dict[str, Any] = {
            "user": "admin",
            "password": "secret",
            "credentials": {"username": "admin", "password": "secret"},
            "list_of_strings": ["something", "something2"],
            "list_of_dicts": [{"username": "admin", "password": "secret"}],
            "boolean": True,
            "number": 1,
            "mixed_list": ["something", {"username": "admin"}, True, 1, 1.0, None, "", [], {}],
            "nested_dict": {
                "level1": {
                    "level2": {
                        "password": "deep_secret",
                        "token": "deep_token",
                        "normal_field": "visible",
                    }
                }
            },
            "list_with_nested_dicts": [
                {"api_key": "secret_key", "name": "visible"},
                {"token": "another_secret", "description": "visible"},
            ],
            "case_insensitive": {
                "PASSWORD": "should_be_redacted",
                "API_KEY": "should_be_redacted",
                "normal_field": "should_remain",
            },
        }

        # Call the function to redact secrets
        redact_json_obj(json_obj, [])

        # Verify that sensitive fields are redacted
        assert json_obj["password"] == "REDACTED"
        assert json_obj["credentials"]["password"] == "REDACTED"
        assert json_obj["list_of_dicts"][0]["password"] == "REDACTED"
        assert json_obj["nested_dict"]["level1"]["level2"]["password"] == "REDACTED"
        assert json_obj["nested_dict"]["level1"]["level2"]["token"] == "REDACTED"
        assert json_obj["list_with_nested_dicts"][0]["api_key"] == "REDACTED"
        assert json_obj["list_with_nested_dicts"][1]["token"] == "REDACTED"
        assert json_obj["case_insensitive"]["PASSWORD"] == "REDACTED"
        assert json_obj["case_insensitive"]["API_KEY"] == "REDACTED"

        # Verify that non-sensitive fields remain unchanged
        assert json_obj["user"] == "admin"
        assert json_obj["credentials"]["username"] == "admin"
        assert json_obj["list_of_strings"] == ["something", "something2"]
        assert json_obj["boolean"] is True
        assert json_obj["number"] == 1
        assert json_obj["mixed_list"] == [
            "something",
            {"username": "admin"},
            True,
            1,
            1.0,
            None,
            "",
            [],
            {},
        ]
        assert json_obj["nested_dict"]["level1"]["level2"]["normal_field"] == "visible"
        assert json_obj["list_with_nested_dicts"][0]["name"] == "visible"
        assert json_obj["list_with_nested_dicts"][1]["description"] == "visible"
        assert json_obj["case_insensitive"]["normal_field"] == "should_remain"

    def test_redact_json_obj_with_custom_secret_fields(self) -> None:
        """Test that custom secret fields and edge cases are properly handled."""
        json_obj: dict[str, Any] = {
            "custom_secret": "should_be_redacted",
            "normal_field": "should_remain",
            "nested": {"custom_secret": "should_be_redacted", "normal_field": "should_remain"},
            "password": 123,  # Non-string password should not be redacted
            "token": True,  # Boolean token should not be redacted
            "api_key": None,  # None value should not be redacted
            "secret": {"nested": "value"},  # Dict value should not be redacted
            "string_password": "secret",  # String password should be redacted
            "empty_dict": {},
            "empty_list": [],
            "list_with_empty_dict": [{}],
            "dict_with_empty_list": {"empty": []},
        }

        custom_secret_fields = ["custom_secret", "string_password"]
        redact_json_obj(json_obj, custom_secret_fields)

        # Verify custom secret fields are redacted
        assert json_obj["custom_secret"] == "REDACTED"
        assert json_obj["nested"]["custom_secret"] == "REDACTED"
        assert json_obj["string_password"] == "REDACTED"

        # Verify normal fields remain unchanged
        assert json_obj["normal_field"] == "should_remain"
        assert json_obj["nested"]["normal_field"] == "should_remain"

        # Non-string values should remain unchanged
        assert json_obj["password"] == 123
        assert json_obj["token"] is True
        assert json_obj["api_key"] is None
        assert json_obj["secret"] == {"nested": "value"}

        # Empty structures should remain unchanged
        assert json_obj["empty_dict"] == {}
        assert json_obj["empty_list"] == []
        assert json_obj["list_with_empty_dict"] == [{}]
        assert json_obj["dict_with_empty_list"] == {"empty": []}

    def test_redact_json_obj_modifies_in_place(self) -> None:
        """Test that the function modifies the object in place and doesn't return anything."""
        original_obj: dict[str, Any] = {"password": "secret", "normal": "value"}
        obj_copy = original_obj.copy()

        # Call the function
        redact_json_obj(obj_copy, [])

        # Original object should be modified
        assert obj_copy["password"] == "REDACTED"
        assert obj_copy["normal"] == "value"

        # Original object should remain unchanged
        assert original_obj["password"] == "secret"
        assert original_obj["normal"] == "value"

    def test_build_loggable_args_without_json(self) -> None:
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
