"""Tests for DealCloud models."""

import pytest
from dealcloud_sdk.data.dealcloud_data import BatchResult
from dealcloud_sdk.models.schema import Object, Field, ChoiceValue, User, Schema, ObjectWithFields
from dealcloud_sdk.models.data import Rows
from dealcloud_sdk.models.factory_models import (
    DealCloudConfig,
    DealCloudFactoryArgs,
    QuerySettings,
    ConcurrencyLimits,
    ResponseRetrySettings,
)


class TestBatchResult:
    """Tests for BatchResult dataclass."""

    def test_batch_result_default_values(self):
        """Test BatchResult default values."""
        result = BatchResult()
        assert result.results == []
        assert result.errors == []
        assert result.total_requested == 0
        assert result.total_succeeded == 0
        assert result.total_failed == 0

    def test_has_errors_property(self):
        """Test has_errors property."""
        result_no_errors = BatchResult(results=[1, 2, 3])
        assert result_no_errors.has_errors is False

        result_with_errors = BatchResult(errors=[{"error": "test"}])
        assert result_with_errors.has_errors is True

    def test_success_rate_property(self):
        """Test success_rate property."""
        # 100% success
        result_all = BatchResult(total_requested=10, total_succeeded=10)
        assert result_all.success_rate == 100.0

        # 50% success
        result_half = BatchResult(total_requested=10, total_succeeded=5)
        assert result_half.success_rate == 50.0

        # 0 requested (edge case)
        result_empty = BatchResult(total_requested=0)
        assert result_empty.success_rate == 100.0


class TestSchemaModels:
    """Tests for schema models."""
    
    def test_object_creation(self):
        """Test Object model creation."""
        obj = Object(
            apiName="Company",
            singularName="Company",
            pluralName="Companies",
            id=1,
            entryListId=100,
        )
        assert obj.apiName == "Company"
        assert obj.singularName == "Company"
        assert obj.pluralName == "Companies"
        assert obj.id == 1
    
    def test_object_from_api_unescapes_html(self):
        """Test Object.from_api unescapes HTML entities."""
        data = {
            "apiName": "Company",
            "singularName": "Company &amp; Partners",
            "pluralName": "Companies &lt;Test&gt;",
            "id": 1,
        }
        obj = Object.from_api(data)
        assert obj.singularName == "Company & Partners"
        assert obj.pluralName == "Companies <Test>"
    
    def test_object_from_api_without_optional_fields(self):
        """Test Object.from_api with missing optional fields."""
        data = {
            "apiName": "Company",
            "id": 1,
            # singularName and pluralName are None
        }
        obj = Object.from_api(data)
        assert obj.apiName == "Company"
        assert obj.singularName is None
        assert obj.pluralName is None
    
    def test_field_creation(self):
        """Test Field model creation."""
        field = Field(
            apiName="CompanyName",
            name="Company Name",
            fieldType=1,
            id=10,
            entryListId=100,
        )
        assert field.apiName == "CompanyName"
        assert field.name == "Company Name"
        assert field.fieldType == 1
    
    def test_field_from_api_builds_choice_map(self):
        """Test Field.from_api builds choice map for choice fields."""
        data = {
            "apiName": "Status",
            "name": "Status",
            "fieldType": 2,  # CHOICE
            "choiceValues": [
                {"name": "Active", "id": 1},
                {"name": "Inactive", "id": 2},
            ],
            "id": 10,
        }
        field = Field.from_api(data)
        assert field.choiceMap == {"Active": 1, "Inactive": 2}
    
    def test_field_from_api_without_choice_values(self):
        """Test Field.from_api without choice values."""
        data = {
            "apiName": "Name",
            "name": "Name",
            "fieldType": 1,  # TEXT
            "id": 10,
        }
        field = Field.from_api(data)
        assert field.choiceMap is None
    
    def test_field_from_api_choice_type_empty_choices(self):
        """Test Field.from_api with choice type but empty choiceValues."""
        data = {
            "apiName": "Status",
            "name": "Status",
            "fieldType": 2,  # CHOICE
            "choiceValues": [],  # Empty list
            "id": 10,
        }
        field = Field.from_api(data)
        # Empty choiceValues should not create choiceMap
        assert field.choiceMap is None
    
    def test_field_from_api_non_choice_with_choice_values(self):
        """Test Field.from_api with non-choice type but has choiceValues."""
        data = {
            "apiName": "Name",
            "name": "Name",
            "fieldType": 1,  # TEXT - not a choice type
            "choiceValues": [{"name": "Ignored", "id": 1}],
            "id": 10,
        }
        field = Field.from_api(data)
        # Non-choice fields shouldn't build choiceMap
        assert field.choiceMap is None
    
    def test_field_from_api_without_unescape_attributes(self):
        """Test Field.from_api when optional attributes are None."""
        data = {
            "apiName": "Field",
            "fieldType": 1,
            "id": 10,
            # description, name, formula are None
        }
        field = Field.from_api(data)
        assert field.apiName == "Field"
        assert field.description is None
    
    def test_user_creation(self):
        """Test User model creation."""
        user = User(
            id=1,
            name="John Doe",
            email="john.doe@gmail.co",
            entryListId=100,
        )
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john.doe@gmail.co"
    
    def test_choice_value_creation(self):
        """Test ChoiceValue model creation."""
        choice = ChoiceValue(
            id=1,
            name="Active",
            seqNumber=1,
        )
        assert choice.id == 1
        assert choice.name == "Active"


class TestDataModels:
    """Tests for data models."""
    
    def test_rows_creation(self):
        """Test Rows model creation."""
        rows = Rows(
            totalRecords=100,
            rows=[{"EntryId": 1, "Name": "Test"}],
        )
        assert rows.totalRecords == 100
        assert len(rows.rows) == 1


class TestFactoryModels:
    """Tests for factory models."""
    
    def test_query_settings_defaults(self):
        """Test QuerySettings default values."""
        settings = QuerySettings()
        assert settings.pageSize == 1000
        assert settings.cellPaginationLimit == 9000
        assert settings.deletePageSize == 5000
    
    def test_concurrency_limits_defaults(self):
        """Test ConcurrencyLimits default values."""
        limits = ConcurrencyLimits()
        assert limits.read == 2
        assert limits.delete == 2
        assert limits.create == 2
    
    def test_response_retry_settings_defaults(self):
        """Test ResponseRetrySettings default values."""
        settings = ResponseRetrySettings()
        assert settings.tooManyRequests == 5
        assert settings.internalServerError == 2
        assert settings.backoffFactor == 2.0
    
    def test_response_retry_settings_to_retry_count_by_status(self):
        """Test ResponseRetrySettings.to_retry_count_by_status."""
        settings = ResponseRetrySettings(
            tooManyRequests=10,
            internalServerError=3,
            serviceUnavailable=4,
        )
        retry_map = settings.to_retry_count_by_status()
        assert retry_map[429] == 10
        assert retry_map[500] == 3
        assert retry_map[503] == 4
    
    def test_dealcloud_config_creation(self):
        """Test DealCloudConfig creation."""
        config = DealCloudConfig(
            siteUrl="client.dealcloud.com",
            clientId="12345",
            clientSecret="secret",
        )
        assert config.siteUrl == "client.dealcloud.com"
        assert config.clientId == "12345"
        assert config.connectorTimeoutSeconds == 100  # Default
    
    def test_dealcloud_config_with_custom_settings(self):
        """Test DealCloudConfig with custom settings."""
        config = DealCloudConfig(
            siteUrl="client.dealcloud.com",
            clientId="12345",
            clientSecret="secret",
            connectorTimeoutSeconds=200,
            querySettings=QuerySettings(pageSize=500),
            concurrencyLimits=ConcurrencyLimits(read=4),
            responseRetrySettings=ResponseRetrySettings(tooManyRequests=10),
        )
        assert config.connectorTimeoutSeconds == 200
        assert config.querySettings.pageSize == 500
        assert config.concurrencyLimits.read == 4
        assert config.responseRetrySettings.tooManyRequests == 10
    
    def test_dealcloud_factory_args_to_config(self):
        """Test DealCloudFactoryArgs.to_config."""
        args = DealCloudFactoryArgs(
            site_url="client.dealcloud.com",
            client_id="12345",
            client_secret="secret",
        )
        config = args.to_config()
        assert config.siteUrl == "client.dealcloud.com"
        assert config.clientId == "12345"
        assert config.clientSecret == "secret"
    
    def test_dealcloud_config_from_json_file(self, tmp_path):
        """Test DealCloudConfig.from_json_file."""
        import json
        
        config_data = {
            "siteUrl": "test.dealcloud.com",
            "clientId": "12345",
            "clientSecret": "secret",
        }
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps(config_data))
        
        config = DealCloudConfig.from_json_file(str(config_file))
        
        assert config.siteUrl == "test.dealcloud.com"
        assert config.clientId == "12345"
    
    def test_dealcloud_config_from_yaml_file(self, tmp_path):
        """Test DealCloudConfig.from_yaml_file."""
        import yaml
        
        config_data = {
            "siteUrl": "yaml.dealcloud.com",
            "clientId": "yaml-id",
            "clientSecret": "yaml-secret",
        }
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump(config_data))
        
        config = DealCloudConfig.from_yaml_file(str(config_file))
        
        assert config.siteUrl == "yaml.dealcloud.com"
        assert config.clientId == "yaml-id"


