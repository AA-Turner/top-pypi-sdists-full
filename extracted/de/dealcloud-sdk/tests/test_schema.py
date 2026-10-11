"""Tests for DealCloudSchema class."""

import time
import pytest
from unittest.mock import MagicMock, patch

from dealcloud_sdk.schema.dealcloud_schema import DealCloudSchema, _merge_field_lists
from dealcloud_sdk.utils.process_response_errors import DealCloudValidationError
from dealcloud_sdk.utils.schema_cache import SchemaCache, get_schema_cache
from dealcloud_sdk.constants import field_types
from dealcloud_sdk.models.schema import (
    User,
    Object,
    Field,
    FieldUnit,
    Mapping,
    MappingsType,
    Schema,
    Timezone,
    ObjectWithFields,
    ChoiceValue,
)


class TestDealCloudSchemaGetUsers:
    """Tests for get_users method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_basic(self, mock_client_class):
        """Test get_users returns User objects."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "John Doe", "email": "john@gmail.co", "entryListId": 100},
            {"id": 2, "name": "Jane Smith", "email": "jane@gmail.co", "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        users = schema.get_users()
        
        assert len(users) == 2
        assert isinstance(users[0], User)
        assert users[0].name == "John Doe"
        assert users[1].email == "jane@gmail.co"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_active_only(self, mock_client_class):
        """Test get_users with active_only filter."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "Active User", "email": "active@gmail.co", "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        users = schema.get_users(active_only=True)
        
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/users?activeOnly=true"
        )
        assert len(users) == 1
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_empty(self, mock_client_class):
        """Test get_users with empty result."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        users = schema.get_users()
        
        assert len(users) == 0


class TestDealCloudSchemaGetCurrencies:
    """Tests for get_currencies method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_currencies(self, mock_client_class):
        """Test get_currencies returns currency codes."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = ["USD", "EUR", "GBP"]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        currencies = schema.get_currencies()
        
        assert currencies == ["USD", "EUR", "GBP"]
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/currencies"
        )


class TestDealCloudSchemaGetObjects:
    """Tests for get_objects method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_objects(self, mock_client_class):
        """Test get_objects returns Object instances."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100},
            {"apiName": "Contact", "singularName": "Contact", "pluralName": "Contacts", "id": 2, "entryListId": 200},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        objects = schema.get_objects()
        
        assert len(objects) == 2
        assert isinstance(objects[0], Object)
        assert objects[0].apiName == "Company"
        assert objects[1].pluralName == "Contacts"


class TestDealCloudSchemaGetAttachmentObjectId:
    """Tests for get_attachment_object_id helper."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_single_candidate_returns_api_name(self, mock_client_class):
        """When exactly one object has entryListType==7, return its apiName."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Company", "id": 1, "entryListId": 100},
            {"apiName": "Attachment", "singularName": "Attachment", "pluralName": "Attachments", "entryListType": 7, "id": 35013, "entryListId": -5},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = schema.get_attachment_object_id()
        assert result == "Attachment"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_no_candidate_raises(self, mock_client_class):
        """When no object has entryListType==7, raise ValueError."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Company", "id": 1, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="No object with entryListType==7"):
            schema.get_attachment_object_id()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_multiple_candidates_disambiguate_by_fields(self, mock_client_class):
        """When multiple have entryListType==7, pick the one with Title, FileType, Size."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.get_objects = lambda: [
            Object(apiName="OtherDoc", id=1, entryListType=7, entryListId=1),
            Object(apiName="Attachment", id=35013, entryListType=7, entryListId=-5),
        ]
        # Stub get_fields so OtherDoc has no required fields, Attachment has Title/FileType/Size
        def get_fields_stub(object_id=None, field_id=None, **kwargs):
            if object_id == "OtherDoc":
                return [Field(apiName="Name", id=10), Field(apiName="Document", id=11)]
            if object_id == "Attachment":
                return [
                    Field(apiName="Title", id=20),
                    Field(apiName="FileType", id=21),
                    Field(apiName="Size", id=22),
                    Field(apiName="Document", id=23),
                ]
            return []
        schema.get_fields = get_fields_stub

        result = schema.get_attachment_object_id()
        assert result == "Attachment"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_single_candidate_without_api_name_or_id_raises(self, mock_client_class):
        """When the only attachment candidate has no apiName and no id, raise."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.get_objects = lambda: [
            Object(apiName=None, id=None, entryListType=7, entryListId=1),
        ]

        with pytest.raises(ValueError, match="neither apiName nor id"):
            schema.get_attachment_object_id()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_multiple_candidates_fallback_first_when_no_required_fields(self, mock_client_class):
        """When no candidate has Title/FileType/Size, return first candidate's id."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.get_objects = lambda: [
            Object(apiName="FirstAttach", id=100, entryListType=7, entryListId=1),
            Object(apiName="SecondAttach", id=200, entryListType=7, entryListId=2),
        ]

        def get_fields_stub(object_id=None, field_id=None, **kwargs):
            return [Field(apiName="OnlyOther", id=1)]

        schema.get_fields = get_fields_stub

        assert schema.get_attachment_object_id() == "FirstAttach"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_multiple_candidates_skips_candidate_with_no_object_id(self, mock_client_class):
        """Candidates with neither apiName nor id are skipped in the disambiguation loop."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.get_objects = lambda: [
            Object(apiName=None, id=None, entryListType=7, entryListId=1),
            Object(apiName="RealAttach", id=50, entryListType=7, entryListId=2),
        ]

        def get_fields_stub(object_id=None, field_id=None, **kwargs):
            if object_id in (50, "RealAttach"):
                return [
                    Field(apiName="Title", id=1),
                    Field(apiName="FileType", id=2),
                    Field(apiName="Size", id=3),
                ]
            return []

        schema.get_fields = get_fields_stub

        assert schema.get_attachment_object_id() == "RealAttach"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_fallback_first_candidate_invalid_raises(self, mock_client_class):
        """If disambiguation fails and first candidate has no apiName/id, raise."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.get_objects = lambda: [
            Object(apiName=None, id=None, entryListType=7, entryListId=1),
            Object(apiName="Other", id=99, entryListType=7, entryListId=2),
        ]

        def get_fields_stub(object_id=None, field_id=None, **kwargs):
            return [Field(apiName="Misc", id=1)]

        schema.get_fields = get_fields_stub

        with pytest.raises(ValueError, match="neither apiName nor id"):
            schema.get_attachment_object_id()


class TestDealCloudSchemaGetFields:
    """Tests for get_fields method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_all_fields(self, mock_client_class):
        """Test get_fields returns all fields."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
            {"apiName": "Status", "name": "Status", "fieldType": 2, "id": 11, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        fields = schema.get_fields()
        
        assert len(fields) == 2
        assert isinstance(fields[0], Field)
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/allfields"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_by_object_id(self, mock_client_class):
        """Test get_fields filtered by object_id."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        fields = schema.get_fields(object_id="Company")
        
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/entryTypes/Company/fields"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_by_object_id_int(self, mock_client_class):
        """Test get_fields filtered by numeric object_id."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        fields = schema.get_fields(object_id=100)
        
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/entryTypes/100/fields"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_by_field_id(self, mock_client_class):
        """Test get_fields filtered by field_id."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        # Single field returns dict, not list
        mock_client.get.return_value = {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        fields = schema.get_fields(field_id=10)
        
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/fields/10"
        )
        assert len(fields) == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_field_id_none_response_raises_validation_error(self, mock_client_class):
        """GET fields/{id} returning no JSON body yields DealCloudValidationError."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = None
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(DealCloudValidationError) as exc_info:
            schema.get_fields(field_id=999_999_999)
        assert "no field data" in exc_info.value.message.lower()
        assert exc_info.value.status_code == 404

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_field_id_null_list_response_raises_validation_error(self, mock_client_class):
        """GET fields/{id} returning [null] (JSON) yields DealCloudValidationError."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [None]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(DealCloudValidationError) as exc_info:
            schema.get_fields(field_id=999_999_999)
        assert "no field data" in exc_info.value.message.lower()
        assert exc_info.value.status_code == 404

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_object_id_none_response_raises_validation_error(self, mock_client_class):
        """GET entryTypes/.../fields returning no JSON body yields DealCloudValidationError."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = None
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(DealCloudValidationError) as exc_info:
            schema.get_fields(object_id="Company")
        assert "no field data" in exc_info.value.message.lower()
        assert exc_info.value.status_code == 404
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_both_params_raises(self, mock_client_class):
        """Test get_fields raises when both object_id and field_id provided."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError) as exc_info:
            schema.get_fields(object_id="Company", field_id=10)
        
        assert "Cannot specify both" in str(exc_info.value)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_uses_instance_cache_on_second_call(self, mock_client_class):
        """Second get_fields(object_id=...) with same id does not call HTTP again."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        f1 = schema.get_fields(object_id="Company")
        f2 = schema.get_fields(object_id="Company")

        assert f1 == f2
        assert mock_client.get.call_count == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_entry_filters_build_query(self, mock_client_class):
        """editable / entry_form append schema query params; names match swagger."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        schema.get_fields(object_id="Company", editable=True, entry_form=False)

        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/entryTypes/Company/fields"
            "?editable=true&entryForm=false"
        )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_entry_filters_skip_cache(self, mock_client_class):
        """Filtered object field requests do not use cache (each call hits HTTP)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        schema.get_fields(object_id="Company", editable=True)
        schema.get_fields(object_id="Company", editable=True)

        assert mock_client.get.call_count == 2

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_entry_filters_do_not_fill_object_cache(self, mock_client_class):
        """After a filtered fetch, unfiltered get_fields still performs GET."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        schema.get_fields(object_id="Company", editable=True)
        schema.get_fields(object_id="Company")

        assert mock_client.get.call_count == 2
        base = "https://test.dealcloud.com/api/rest/v4/schema/entryTypes/Company/fields"
        assert mock_client.get.call_args_list[0][0][0].startswith(f"{base}?")
        assert mock_client.get.call_args_list[1][0][0] == base

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_entry_filters_require_object_id(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(AttributeError, match="only valid with object_id"):
            schema.get_fields(editable=True)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_entry_filters_conflict_with_field_id(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(AttributeError, match="editable or entry_form together with field_id"):
            schema.get_fields(field_id=10, editable=True)

    def test_merge_field_lists_unions_by_id(self):
        a = Field(apiName="A", id=1)
        b = Field(apiName="B", id=2)
        c = Field(apiName="B2", id=2)
        merged = _merge_field_lists([a], [b, c])
        assert len(merged) == 2
        assert merged[0] is a
        assert merged[1] is b


class TestDealCloudSchemaClearCaches:
    """Tests for clear_fields_cache and clear_schema_cache."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_clear_fields_cache_single_object(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.get_fields(object_id="Company")
        schema.clear_fields_cache("Company")
        schema.get_fields(object_id="Company")

        assert mock_client.get.call_count == 2

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_clear_schema_cache_clears_fields_cache(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.get_fields(object_id="Z")
        schema.clear_schema_cache()
        schema.get_fields(object_id="Z")

        assert mock_client.get.call_count == 2


class TestDealCloudSchemaGetFieldsByIds:
    """Tests for get_fields_by_ids method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_by_ids_multiple(self, mock_client_class):
        """Test get_fields_by_ids with multiple field IDs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
            {"apiName": "Status", "name": "Status", "fieldType": 2, "id": 11, "entryListId": 100},
            {"apiName": "Owner", "name": "Owner", "fieldType": 3, "id": 12, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        fields = schema.get_fields_by_ids([10, 11, 12])
        
        assert len(fields) == 3
        assert isinstance(fields[0], Field)
        assert fields[0].apiName == "Name"
        assert fields[2].apiName == "Owner"
        # Verify URL contains all fieldIds
        call_url = mock_client.get.call_args[0][0]
        assert "fieldIds=10" in call_url
        assert "fieldIds=11" in call_url
        assert "fieldIds=12" in call_url
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_by_ids_single(self, mock_client_class):
        """Test get_fields_by_ids with a single ID returns list."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        # API may return single object or list for single ID
        mock_client.get.return_value = {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100}
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        fields = schema.get_fields_by_ids([10])
        
        assert len(fields) == 1
        assert isinstance(fields[0], Field)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_fields_by_ids_empty_list(self, mock_client_class):
        """Test get_fields_by_ids with empty list returns empty."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        fields = schema.get_fields_by_ids([])
        
        assert len(fields) == 0
        # Should not make an API call for empty list
        mock_client.get.assert_not_called()


class TestDealCloudSchemaGetField:
    """Tests for get_field method (single field by ID or API name)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_by_id(self, mock_client_class):
        """Test get_field calls GET schema/fields/{fieldId} and returns Field."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "id": 12345,
            "name": "Company Name",
            "apiName": "CompanyName",
            "fieldType": 1,
        }
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        field = schema.get_field(12345)

        assert isinstance(field, Field)
        assert field.id == 12345
        assert field.name == "Company Name"
        assert field.apiName == "CompanyName"
        mock_client.get.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/schema/fields/12345"
        )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_none_response_raises_validation_error(self, mock_client_class):
        """GET fields/{id} returning no JSON body yields DealCloudValidationError."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = None
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(DealCloudValidationError) as exc_info:
            schema.get_field(12345)
        assert "no field data" in exc_info.value.message.lower()
        assert exc_info.value.status_code == 404

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_string_null_response_raises_validation_error(self, mock_client_class):
        """GET fields/{id} returning literal string 'null' yields DealCloudValidationError."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = "null"
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(DealCloudValidationError) as exc_info:
            schema.get_field(12345)
        assert "no field data" in exc_info.value.message.lower()
        assert exc_info.value.status_code == 404

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_by_api_name(self, mock_client_class):
        """Test get_field with string (API name) calls same endpoint."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"id": 99, "name": "Status", "apiName": "Status"}
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        field = schema.get_field("Status")

        assert field.apiName == "Status"
        mock_client.get.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/schema/fields/Status"
        )


class TestDealCloudSchemaGetFieldTypes:
    """Tests for get_field_types method."""
    
    @patch('dealcloud_sdk.schema.dealcloud_schema.get_schema_cache')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_types_no_cache(self, mock_client_class, mock_get_cache):
        """Test get_field_types fetches from API when cache miss."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "Text"},
            {"id": 2, "name": "Number"},
            {"id": 3, "name": "Date"},
        ]
        mock_client_class.return_value = mock_client
        
        mock_cache = MagicMock()
        mock_cache.get.return_value = None  # Cache miss
        mock_get_cache.return_value = mock_cache
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field_types = schema.get_field_types()
        
        assert len(field_types) == 3
        assert field_types[0]["id"] == 1
        assert field_types[0]["name"] == "Text"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/fieldtypes"
        )
        # Should cache the result
        mock_cache.set.assert_called_once_with("test.dealcloud.com", "field_types", field_types)
    
    @patch('dealcloud_sdk.schema.dealcloud_schema.get_schema_cache')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_types_cache_hit(self, mock_client_class, mock_get_cache):
        """Test get_field_types returns cached data without API call."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        cached_data = [
            {"id": 1, "name": "Text"},
            {"id": 2, "name": "Number"},
        ]
        mock_cache = MagicMock()
        mock_cache.get.return_value = cached_data  # Cache hit
        mock_get_cache.return_value = mock_cache
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field_types = schema.get_field_types()
        
        assert field_types == cached_data
        # Should NOT call API when cache hit
        mock_client.get.assert_not_called()
    
    @patch('dealcloud_sdk.schema.dealcloud_schema.get_schema_cache')
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_types_bypass_cache(self, mock_client_class, mock_get_cache):
        """Test get_field_types with use_cache=False bypasses cache."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "Text"},
        ]
        mock_client_class.return_value = mock_client
        
        cached_data = [{"id": 99, "name": "OldCached"}]
        mock_cache = MagicMock()
        mock_cache.get.return_value = cached_data
        mock_get_cache.return_value = mock_cache
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field_types = schema.get_field_types(use_cache=False)
        
        # Should call API even with cache available
        mock_client.get.assert_called_once()
        assert field_types[0]["name"] == "Text"  # Fresh data, not cached


class TestDealCloudSchemaGetSystemFieldTypes:
    """Tests for get_system_field_types method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_system_field_types_fetches_from_api(self, mock_client_class):
        """Test get_system_field_types fetches from API on first call."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "EntryId"},
            {"id": 2, "name": "CreatedDate"},
            {"id": 3, "name": "ModifiedDate"},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        system_types = schema.get_system_field_types()
        
        assert len(system_types) == 3
        assert system_types[0]["id"] == 1
        assert system_types[0]["name"] == "EntryId"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/systemfieldtypes"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_system_field_types_uses_instance_cache(self, mock_client_class):
        """Test get_system_field_types uses instance variable cache."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "EntryId"},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # First call - should hit API
        result1 = schema.get_system_field_types()
        # Second call - should use cache
        result2 = schema.get_system_field_types()
        
        # API should only be called once
        assert mock_client.get.call_count == 1
        assert result1 == result2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_system_field_types_bypass_cache(self, mock_client_class):
        """Test get_system_field_types with use_cache=False."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "EntryId"},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Pre-populate cache
        schema._system_field_types_cache = [{"id": 99, "name": "OldCached"}]
        
        # Call with use_cache=False
        result = schema.get_system_field_types(use_cache=False)
        
        # Should call API despite cache
        mock_client.get.assert_called_once()
        assert result[0]["name"] == "EntryId"  # Fresh data


class TestDealCloudSchemaGetSystemEntryTypes:
    """Tests for get_system_entry_types method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_system_entry_types_fetches_from_api(self, mock_client_class):
        """Test get_system_entry_types fetches from API on first call."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "User"},
            {"id": 2, "name": "Currency"},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        entry_types = schema.get_system_entry_types()
        
        assert len(entry_types) == 2
        assert entry_types[0]["name"] == "User"
        assert entry_types[1]["name"] == "Currency"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/systementrytypes"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_system_entry_types_uses_instance_cache(self, mock_client_class):
        """Test get_system_entry_types uses instance variable cache."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1, "name": "User"}]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # First call - should hit API
        result1 = schema.get_system_entry_types()
        # Second call - should use cache
        result2 = schema.get_system_entry_types()
        
        # API should only be called once
        assert mock_client.get.call_count == 1
        assert result1 == result2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_system_entry_types_bypass_cache(self, mock_client_class):
        """Test get_system_entry_types with use_cache=False."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1, "name": "User"}]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Pre-populate cache
        schema._system_entry_types_cache = [{"id": 99, "name": "OldCached"}]
        
        # Call with use_cache=False
        result = schema.get_system_entry_types(use_cache=False)
        
        # Should call API despite cache
        mock_client.get.assert_called_once()
        assert result[0]["name"] == "User"  # Fresh data


class TestDealCloudSchemaGetFilterOperations:
    """Tests for get_filter_operations method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_filter_operations(self, mock_client_class):
        """Test get_filter_operations fetches from API."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "Equals"},
            {"id": 2, "name": "NotEquals"},
            {"id": 3, "name": "Contains"},
            {"id": 4, "name": "GreaterThan"},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        operations = schema.get_filter_operations()
        
        assert len(operations) == 4
        assert operations[0]["name"] == "Equals"
        assert operations[2]["name"] == "Contains"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/filteroperations"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_filter_operations_no_cache(self, mock_client_class):
        """Test get_filter_operations always calls API (no caching)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1, "name": "Equals"}]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        # Call multiple times
        schema.get_filter_operations()
        schema.get_filter_operations()
        schema.get_filter_operations()
        
        # Should call API each time (no caching)
        assert mock_client.get.call_count == 3


class TestDealCloudSchemaGetSchema:
    """Tests for get_schema method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_schema_api_keys(self, mock_client_class):
        """Test get_schema with API name keys."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        # First call: get_objects
        objects_response = [
            {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100},
        ]
        # Second call: get_fields
        fields_response = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 1},
            {"apiName": "Status", "name": "Status", "fieldType": 2, "id": 11, "entryListId": 1},
        ]
        
        mock_client.get.side_effect = [objects_response, fields_response]
        mock_client_class.return_value = mock_client
        
        schema_obj = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        schema = schema_obj.get_schema(key_type="api")
        
        assert isinstance(schema, Schema)
        assert "Company" in schema.objects
        assert "Name" in schema.objects["Company"].fields
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_schema_display_keys(self, mock_client_class):
        """Test get_schema with display name keys."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        objects_response = [
            {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100, "name": "Company"},
        ]
        fields_response = [
            {"apiName": "CompanyName", "name": "Company Name", "fieldType": 1, "id": 10, "entryListId": 1},
        ]
        
        mock_client.get.side_effect = [objects_response, fields_response]
        mock_client_class.return_value = mock_client
        
        schema_obj = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        schema = schema_obj.get_schema(key_type="display")
        
        # With display key_type, uses field.name as key
        assert "Company Name" in schema.objects["Company"].fields
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_schema_id_keys(self, mock_client_class):
        """Test get_schema with ID keys."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        objects_response = [
            {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100},
        ]
        fields_response = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 1},
        ]
        
        mock_client.get.side_effect = [objects_response, fields_response]
        mock_client_class.return_value = mock_client
        
        schema_obj = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        schema = schema_obj.get_schema(key_type="id")
        
        # With id key_type, uses str(id) as keys
        assert "1" in schema.objects
        assert "10" in schema.objects["1"].fields
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_schema_invalid_key_type_raises(self, mock_client_class):
        """Test get_schema raises for invalid key_type."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        # Need at least one object to trigger the validation
        objects_response = [
            {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100},
        ]
        fields_response = [
            {"apiName": "Name", "name": "Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client.get.side_effect = [objects_response, fields_response]
        mock_client_class.return_value = mock_client
        
        schema_obj = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(AttributeError) as exc_info:
            schema_obj.get_schema(key_type="invalid")
        
        assert "key_type must be one of" in str(exc_info.value)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_schema_filters_fields_by_entry_list_id(self, mock_client_class):
        """Test get_schema filters fields by object's entryListId."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        objects_response = [
            {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100},
            {"apiName": "Contact", "singularName": "Contact", "pluralName": "Contacts", "id": 2, "entryListId": 200},
        ]
        # Fields for both objects
        fields_response = [
            {"apiName": "CompanyName", "name": "Company Name", "fieldType": 1, "id": 10, "entryListId": 1},
            {"apiName": "ContactName", "name": "Contact Name", "fieldType": 1, "id": 20, "entryListId": 2},
        ]
        
        mock_client.get.side_effect = [objects_response, fields_response]
        mock_client_class.return_value = mock_client
        
        schema_obj = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        schema = schema_obj.get_schema(key_type="api")
        
        # Each object should only have its own fields
        assert "CompanyName" in schema.objects["Company"].fields
        assert "ContactName" not in schema.objects["Company"].fields
        assert "ContactName" in schema.objects["Contact"].fields


class TestDealCloudSchemaFieldLookups:
    """Tests for field lookup methods."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_by_name_found(self, mock_client_class):
        """Test get_field_by_name when field exists."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Full Name", "fieldType": 1, "id": 10, "entryListId": 100},
            {"apiName": "Email", "name": "Email Address", "fieldType": 1, "id": 11, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field = schema.get_field_by_name("Company", "Full Name")
        
        assert field is not None
        assert field.apiName == "Name"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_by_name_not_found(self, mock_client_class):
        """Test get_field_by_name when field doesn't exist."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Full Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field = schema.get_field_by_name("Company", "Nonexistent")
        
        assert field is None
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_by_api_name_found(self, mock_client_class):
        """Test get_field_by_api_name when field exists."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "Name", "name": "Full Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field = schema.get_field_by_api_name("Company", "Name")
        
        assert field is not None
        assert field.name == "Full Name"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_by_api_name_not_found(self, mock_client_class):
        """Test get_field_by_api_name when field doesn't exist."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field = schema.get_field_by_api_name("Company", "Nonexistent")
        
        assert field is None

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_by_api_name_finds_second_field(self, mock_client_class):
        """Loop reaches a match after scanning non-matching fields."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "A", "name": "First", "fieldType": 1, "id": 1, "entryListId": 100},
            {"apiName": "B", "name": "Second", "fieldType": 1, "id": 2, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        field = schema.get_field_by_api_name("Company", "B")
        assert field is not None
        assert field.apiName == "B"


class TestDealCloudSchemaFieldMaps:
    """Tests for field map methods."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_map(self, mock_client_class):
        """Test get_field_map returns proper structure."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        objects_response = [
            {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100},
        ]
        fields_response = [
            {
                "apiName": "Name", "name": "Company Name", "fieldType": 1, "id": 10, "entryListId": 1,
                "isRequired": True, "isCalculated": False, "isMultiSelect": False, "isMoney": False,
                "choiceValues": [{"name": "Choice1", "id": 101}],
                "entryLists": [200, 300],
            },
        ]
        
        mock_client.get.side_effect = [objects_response, fields_response]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field_map = schema.get_field_map()
        
        assert "Company" in field_map
        assert "Name" in field_map["Company"]
        assert field_map["Company"]["Name"]["id"] == 10
        assert field_map["Company"]["Name"]["isRequired"] is True
        assert "Choice1" in field_map["Company"]["Name"]["choices"]
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_map_filtered_objects(self, mock_client_class):
        """Test get_field_map with specific objects."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        
        objects_response = [
            {"apiName": "Company", "singularName": "Company", "pluralName": "Companies", "id": 1, "entryListId": 100},
            {"apiName": "Contact", "singularName": "Contact", "pluralName": "Contacts", "id": 2, "entryListId": 200},
        ]
        fields_response = [
            {"apiName": "CompanyName", "name": "Company Name", "fieldType": 1, "id": 10, "entryListId": 1},
            {"apiName": "ContactName", "name": "Contact Name", "fieldType": 1, "id": 20, "entryListId": 2},
        ]
        
        mock_client.get.side_effect = [objects_response, fields_response]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        field_map = schema.get_field_map(object_names=["Company"])
        
        assert "Company" in field_map
        assert "Contact" not in field_map
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_name_to_api_map(self, mock_client_class):
        """Test get_name_to_api_map returns correct mapping."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "FullName", "name": "Full Name", "fieldType": 1, "id": 10, "entryListId": 100},
            {"apiName": "EmailAddr", "name": "Email Address", "fieldType": 1, "id": 11, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        name_map = schema.get_name_to_api_map("Company")
        
        assert name_map["Full Name"] == "FullName"
        assert name_map["Email Address"] == "EmailAddr"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_api_to_name_map(self, mock_client_class):
        """Test get_api_to_name_map returns correct mapping."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"apiName": "FullName", "name": "Full Name", "fieldType": 1, "id": 10, "entryListId": 100},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        api_map = schema.get_api_to_name_map("Company")
        
        assert api_map["FullName"] == "Full Name"


class TestDealCloudSchemaGetEntryType:
    """Tests for get_entry_type method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_entry_type_by_id(self, mock_client_class):
        """Test get_entry_type returns an Object by numeric ID."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "apiName": "Company", "singularName": "Company",
            "pluralName": "Companies", "id": 1, "entryListId": 100,
            "entryListType": 0, "entryListSubType": 0,
        }
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        obj = schema.get_entry_type(1)
        
        assert isinstance(obj, Object)
        assert obj.apiName == "Company"
        assert obj.id == 1
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/entryTypes/1"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_entry_type_by_api_name(self, mock_client_class):
        """Test get_entry_type returns an Object by API name."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "apiName": "Contact", "singularName": "Contact",
            "pluralName": "Contacts", "id": 2, "entryListId": 200,
        }
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        obj = schema.get_entry_type("Contact")
        
        assert isinstance(obj, Object)
        assert obj.apiName == "Contact"
        assert obj.pluralName == "Contacts"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/entryTypes/Contact"
        )


class TestDealCloudSchemaGetMappingsTypes:
    """Tests for get_mappings_types method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_mappings_types(self, mock_client_class):
        """Test get_mappings_types returns MappingsType objects."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "External System", "entryListId": 100},
            {"id": 2, "name": "Data Source", "entryListId": 200},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        types = schema.get_mappings_types()
        
        assert len(types) == 2
        assert isinstance(types[0], MappingsType)
        assert types[0].id == 1
        assert types[0].name == "External System"
        assert types[1].id == 2
        assert types[1].name == "Data Source"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/mappingstypes"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_mappings_types_empty(self, mock_client_class):
        """Test get_mappings_types with empty result."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        types = schema.get_mappings_types()
        
        assert len(types) == 0


class TestDealCloudSchemaGetMappings:
    """Tests for get_mappings method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_mappings(self, mock_client_class):
        """Test get_mappings returns Mapping objects for a type ID."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 10, "name": "Company Mapping", "entryListId": 100},
            {"id": 11, "name": "Contact Mapping", "entryListId": 200},
            {"id": 12, "name": "Deal Mapping", "entryListId": 300},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        mappings = schema.get_mappings(mappings_type_id=1)
        
        assert len(mappings) == 3
        assert isinstance(mappings[0], Mapping)
        assert mappings[0].id == 10
        assert mappings[0].name == "Company Mapping"
        assert mappings[2].name == "Deal Mapping"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/mappings/1"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_mappings_empty(self, mock_client_class):
        """Test get_mappings with empty result."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        mappings = schema.get_mappings(mappings_type_id=99)
        
        assert len(mappings) == 0
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/mappings/99"
        )


class TestDealCloudSchemaGetContract:
    """Tests for get_contract method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_contract(self, mock_client_class):
        """Test get_contract returns contract content."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = '{"version": "1.0", "fields": ["Name", "Status"]}'
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        contract_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        contract = schema.get_contract(contract_id)
        
        assert isinstance(contract, str)
        assert "version" in contract
        mock_client.get.assert_called_with(
            f"https://test.dealcloud.com/api/rest/v4/schema/contracts/{contract_id}"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_contract_different_id(self, mock_client_class):
        """Test get_contract with different UUID."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = "contract-data"
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        contract_id = "ffffffff-ffff-ffff-ffff-ffffffffffff"
        contract = schema.get_contract(contract_id)
        
        assert contract == "contract-data"
        mock_client.get.assert_called_with(
            f"https://test.dealcloud.com/api/rest/v4/schema/contracts/{contract_id}"
        )


class TestDealCloudSchemaAppendChoiceValues:
    """Tests for append_choice_values method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_append_choice_values_by_id(self, mock_client_class):
        """Test append_choice_values with numeric field ID."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [
            {"id": 201, "name": "New Option A"},
            {"id": 202, "name": "New Option B"},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        new_choices = [{"name": "New Option A"}, {"name": "New Option B"}]
        result = schema.append_choice_values(field_id=12345, choice_values=new_choices)
        
        assert len(result) == 2
        assert result[0]["name"] == "New Option A"
        mock_client.post.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/choiceFieldValues/12345",
            json=["New Option A", "New Option B"],
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_append_choice_values_by_api_name(self, mock_client_class):
        """Test append_choice_values with field API name."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"id": 301, "name": "Option X"}]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        new_choices = [{"name": "Option X"}]
        result = schema.append_choice_values(field_id="StatusField", choice_values=new_choices)
        
        assert len(result) == 1
        mock_client.post.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/choiceFieldValues/StatusField",
            json=["Option X"],
        )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_append_choice_values_list_of_strings(self, mock_client_class):
        """Test append_choice_values with list of strings sends array of strings."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]
        mock_client_class.return_value = mock_client

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = schema.append_choice_values(field_id=12345, choice_values=["A", "B"])

        assert len(result) == 2
        mock_client.post.assert_called_once_with(
            "https://test.dealcloud.com/api/rest/v4/schema/choiceFieldValues/12345",
            json=["A", "B"],
        )

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_append_choice_values_empty(self, mock_client_class):
        """Test append_choice_values with empty list."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = schema.append_choice_values(field_id=12345, choice_values=[])

        assert result == []
        mock_client.post.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/choiceFieldValues/12345",
            json=[],
        )


class TestDealCloudSchemaGetFieldUnits:
    """Tests for get_field_units method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_units(self, mock_client_class):
        """Test get_field_units returns FieldUnit objects."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 1, "name": "Percentage"},
            {"id": 2, "name": "Multiplier"},
            {"id": 3, "name": "Basis Points"},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        units = schema.get_field_units()
        
        assert len(units) == 3
        assert isinstance(units[0], FieldUnit)
        assert units[0].id == 1
        assert units[0].name == "Percentage"
        assert units[2].name == "Basis Points"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/fieldunits"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_field_units_empty(self, mock_client_class):
        """Test get_field_units with empty result."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        units = schema.get_field_units()
        
        assert len(units) == 0


class TestDealCloudSchemaGetTimezones:
    """Tests for get_timezones method."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_timezones(self, mock_client_class):
        """Test get_timezones returns Timezone objects."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": "UTC", "name": "UTC", "displayName": "UTC (Coordinated Universal Time)"},
            {"id": "America/New_York", "name": "Eastern", "displayName": "(UTC-05:00) Eastern Time"},
            {"id": "Europe/London", "name": "GMT", "displayName": "(UTC+00:00) London"},
        ]
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        timezones = schema.get_timezones()
        
        assert len(timezones) == 3
        assert isinstance(timezones[0], Timezone)
        assert timezones[0].id == "UTC"
        assert timezones[1].name == "Eastern"
        assert timezones[2].displayName == "(UTC+00:00) London"
        mock_client.get.assert_called_with(
            "https://test.dealcloud.com/api/rest/v4/schema/timezones"
        )
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_timezones_empty(self, mock_client_class):
        """Test get_timezones with empty result."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client
        
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        timezones = schema.get_timezones()
        
        assert len(timezones) == 0


class TestSchemaCache:
    """Tests for SchemaCache."""

    def setup_method(self):
        """Clear cache before each test."""
        cache = get_schema_cache()
        cache.clear_all()

    def test_singleton_instance(self):
        """SchemaCache uses singleton pattern."""
        cache1 = SchemaCache.get_instance()
        cache2 = SchemaCache.get_instance()
        assert cache1 is cache2

    def test_set_and_get(self):
        """Test basic set and get operations."""
        cache = get_schema_cache()

        test_schema = {"objects": {"Company": {}}}
        cache.set("site.dealcloud.com", "schema", test_schema)

        retrieved = cache.get("site.dealcloud.com", "schema")
        assert retrieved == test_schema

    def test_has_checks_existence(self):
        """Test has() method."""
        cache = get_schema_cache()

        assert cache.has("site.dealcloud.com", "schema") is False

        cache.set("site.dealcloud.com", "schema", {})
        assert cache.has("site.dealcloud.com", "schema") is True

    def test_cache_key_normalization(self):
        """Test site URL normalization for cache keys."""
        cache = get_schema_cache()

        # Set with one format
        cache.set("https://SITE.DealCloud.Com/", "schema", {"test": True})

        # Get with different formats - should all work
        assert cache.has("site.dealcloud.com", "schema") is True
        assert cache.has("https://site.dealcloud.com", "schema") is True
        assert cache.has("http://Site.DealCloud.Com/", "schema") is True

    def test_ttl_expiry(self):
        """Test cache entry expiration."""
        cache = SchemaCache(default_ttl=0.1)  # Very short TTL

        cache.set("site.dealcloud.com", "schema", {"test": True})
        assert cache.has("site.dealcloud.com", "schema") is True

        time.sleep(0.15)

        assert cache.has("site.dealcloud.com", "schema") is False
        assert cache.get("site.dealcloud.com", "schema") is None

    def test_custom_ttl_per_check(self):
        """Test custom TTL when checking cache."""
        cache = SchemaCache(default_ttl=300)

        cache.set("site.dealcloud.com", "schema", {"test": True})

        # Should be valid with default TTL
        assert cache.has("site.dealcloud.com", "schema") is True

        # Should be expired with very short TTL
        time.sleep(0.05)
        assert cache.has("site.dealcloud.com", "schema", ttl=0.01) is False

    def test_clear_specific_type(self):
        """Test clearing specific cache type for a site."""
        cache = get_schema_cache()

        cache.set("site.dealcloud.com", "schema", {"schema": True})
        cache.set("site.dealcloud.com", "user_map", {"users": []})

        cache.clear("site.dealcloud.com", "schema")

        assert cache.has("site.dealcloud.com", "schema") is False
        assert cache.has("site.dealcloud.com", "user_map") is True

    def test_clear_all_for_site(self):
        """Test clearing all cache for a site."""
        cache = get_schema_cache()

        cache.set("site.dealcloud.com", "schema", {"schema": True})
        cache.set("site.dealcloud.com", "user_map", {"users": []})

        cache.clear("site.dealcloud.com")

        assert cache.has("site.dealcloud.com", "schema") is False
        assert cache.has("site.dealcloud.com", "user_map") is False

    def test_clear_all(self):
        """Test clearing all caches."""
        cache = get_schema_cache()

        cache.set("site1.dealcloud.com", "schema", {})
        cache.set("site2.dealcloud.com", "schema", {})

        cache.clear_all()

        assert cache.has("site1.dealcloud.com", "schema") is False
        assert cache.has("site2.dealcloud.com", "schema") is False

    def test_get_stats(self):
        """Test cache statistics."""
        cache = get_schema_cache()
        cache.clear_all()

        cache.set("site1.dealcloud.com", "schema", {})
        cache.set("site1.dealcloud.com", "user_map", {})
        cache.set("site2.dealcloud.com", "schema", {})

        stats = cache.get_stats()
        assert stats["sites_cached"] == 2
        assert stats["total_entries"] == 3
        assert "site1.dealcloud.com" in stats["sites"]

    def test_thread_safety(self):
        """Test thread safety of cache operations."""
        import threading

        cache = get_schema_cache()
        cache.clear_all()

        errors = []

        def writer():
            try:
                for i in range(100):
                    cache.set(f"site{i}.dealcloud.com", "schema", {"iteration": i})
            except Exception as e:
                errors.append(e)

        def reader():
            try:
                for i in range(100):
                    cache.get(f"site{i}.dealcloud.com", "schema")
            except Exception as e:
                errors.append(e)

        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=reader),
            threading.Thread(target=writer),
            threading.Thread(target=reader),
        ]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0, f"Thread errors: {errors}"

    def test_get_nonexistent_site(self):
        """Test get returns None for nonexistent site."""
        cache = get_schema_cache()
        cache.clear_all()

        result = cache.get("nonexistent.dealcloud.com", "schema")
        assert result is None

    def test_get_nonexistent_cache_type(self):
        """Test get returns None for nonexistent cache type."""
        cache = get_schema_cache()
        cache.clear_all()

        cache.set("site.dealcloud.com", "schema", {"data": True})
        result = cache.get("site.dealcloud.com", "nonexistent_type")
        assert result is None

    def test_has_nonexistent_site(self):
        """Test has returns False for nonexistent site."""
        cache = get_schema_cache()
        cache.clear_all()

        assert cache.has("nonexistent.dealcloud.com", "schema") is False

    def test_has_nonexistent_cache_type(self):
        """Test has returns False for nonexistent cache type."""
        cache = get_schema_cache()
        cache.clear_all()

        cache.set("site.dealcloud.com", "schema", {"data": True})
        assert cache.has("site.dealcloud.com", "nonexistent_type") is False

    def test_clear_nonexistent_site(self):
        """Test clearing nonexistent site doesn't raise."""
        cache = get_schema_cache()
        cache.clear_all()

        # Should not raise
        cache.clear("nonexistent.dealcloud.com")

    def test_get_expired_entry_custom_ttl(self):
        """Test get returns None for expired entry with custom TTL."""
        cache = SchemaCache(default_ttl=300)  # Long default TTL

        cache.set("site.dealcloud.com", "schema", {"data": True})

        time.sleep(0.05)

        # Should return None with very short custom TTL
        result = cache.get("site.dealcloud.com", "schema", ttl=0.01)
        assert result is None

    def test_cache_entry_is_expired(self):
        """Test CacheEntry.is_expired method."""
        from dealcloud_sdk.utils.schema_cache import CacheEntry

        entry = CacheEntry(data={"test": True})

        # Should not be expired immediately
        assert entry.is_expired(300) is False

        time.sleep(0.05)

        # Should be expired with very short TTL
        assert entry.is_expired(0.01) is True


class TestExportSchemaToExcel:
    """Unit tests for export_schema_to_excel (mocked get_schema / export_to_excel)."""

    @patch("dealcloud_sdk.utils.excel_utils.export_to_excel")
    @patch.object(DealCloudSchema, "get_schema")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_schema_to_excel_builds_sheets(
        self, mock_client_class, mock_get_schema, mock_export, tmp_path
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        parent = Object(
            id=10,
            apiName="Parent",
            singularName="Parent",
            pluralName="Parents",
            entryListType=1,
            entryListSubType=2,
        )
        child = Object(
            id=20,
            apiName="Child",
            singularName="Child",
            pluralName="Children",
            entryListType=1,
            entryListSubType=2,
        )
        text_f = Field(
            id=1,
            apiName="Name",
            name="Name",
            fieldType=field_types.TEXT,
            isRequired=True,
            isMultiSelect=False,
            isCalculated=False,
            isMoney=False,
            isKey=False,
            isAttachment=False,
        )
        choice_f = Field(
            id=2,
            apiName="Stage",
            name="Stage",
            fieldType=field_types.CHOICE,
            choiceValues=[ChoiceValue(name="Open"), ChoiceValue(name="Won")],
        )
        ref_f = Field(
            id=3,
            apiName="ParentRef",
            name="Parent",
            fieldType=field_types.REFERENCE,
            entryLists=[10],
            isMultiSelect=False,
            isAttachment=False,
        )
        orphan_ref = Field(
            id=4,
            apiName="Orphan",
            name="Orphan",
            fieldType=field_types.REFERENCE,
            entryLists=[999],
            isMultiSelect=False,
            isAttachment=False,
        )
        owf_parent = ObjectWithFields(object=parent, fields={"Name": text_f})
        owf_child = ObjectWithFields(
            object=child,
            fields={
                "Name": text_f,
                "Stage": choice_f,
                "ParentRef": ref_f,
                "Orphan": orphan_ref,
            },
        )
        mock_get_schema.return_value = Schema(
            objects={"Parent": owf_parent, "Child": owf_child}
        )
        out_path = tmp_path / "schema.xlsx"
        mock_export.return_value = out_path

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        result = schema.export_schema_to_excel(out_path, objects=["Parent", "Child"])

        assert result == out_path
        mock_get_schema.assert_called_once_with(key_type="api")
        mock_export.assert_called_once()
        sheets_arg = mock_export.call_args[0][0]
        assert "Summary" in sheets_arg
        assert "Relationships" in sheets_arg
        assert "Parent" in sheets_arg
        assert "Child" in sheets_arg

    @patch.object(DealCloudSchema, "get_schema")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_schema_to_excel_no_matching_objects_raises(
        self, mock_client_class, mock_get_schema, tmp_path
    ):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        o = Object(id=1, apiName="Only", singularName="O", pluralName="Os")
        mock_get_schema.return_value = Schema(
            objects={"Only": ObjectWithFields(object=o, fields={})}
        )
        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        with pytest.raises(ValueError, match="No objects found"):
            schema.export_schema_to_excel(
                tmp_path / "x.xlsx", objects=["MissingObject"]
            )

    @patch("dealcloud_sdk.utils.excel_utils.export_to_excel")
    @patch.object(DealCloudSchema, "get_schema")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_schema_to_excel_all_objects_no_summary_no_relationships(
        self, mock_client_class, mock_get_schema, mock_export, tmp_path
    ):
        """objects=None exports all; optional sheets can be omitted."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        o = Object(
            id=1,
            apiName="Solo",
            singularName="S",
            pluralName="Ss",
            entryListType=0,
            entryListSubType=0,
        )
        mock_get_schema.return_value = Schema(
            objects={"Solo": ObjectWithFields(object=o, fields={})}
        )
        mock_export.return_value = tmp_path / "out.xlsx"

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.export_schema_to_excel(
            tmp_path / "out.xlsx",
            objects=None,
            include_summary=False,
            include_relationships=False,
        )

        sheets = mock_export.call_args[0][0]
        assert "Summary" not in sheets
        assert "Relationships" not in sheets
        assert "Solo" in sheets

    @patch("dealcloud_sdk.utils.excel_utils.export_to_excel")
    @patch.object(DealCloudSchema, "get_schema")
    @patch("dealcloud_sdk.base.dealcloud_base.RestClient")
    def test_export_schema_to_excel_no_relationships_when_no_reference_fields(
        self, mock_client_class, mock_get_schema, mock_export, tmp_path
    ):
        """Relationships sheet omitted when there are no reference fields."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        o = Object(
            id=1,
            apiName="Obj",
            singularName="O",
            pluralName="Os",
            entryListType=0,
            entryListSubType=0,
        )
        text_f = Field(
            id=1,
            apiName="Name",
            name="Name",
            fieldType=field_types.TEXT,
            isRequired=False,
            isMultiSelect=False,
            isCalculated=False,
            isMoney=False,
            isKey=False,
            isAttachment=False,
        )
        mock_get_schema.return_value = Schema(
            objects={"Obj": ObjectWithFields(object=o, fields={"Name": text_f})}
        )
        mock_export.return_value = tmp_path / "out.xlsx"

        schema = DealCloudSchema(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        schema.export_schema_to_excel(tmp_path / "out.xlsx", objects=["Obj"])

        sheets = mock_export.call_args[0][0]
        assert "Relationships" not in sheets


class TestSchemaUtilities:
    """Tests for schema utility methods."""

    @patch('dealcloud_sdk.schema.dealcloud_schema.DealCloudSchema.get_users')
    def test_get_user_map_returns_dict(self, mock_get_users):
        """get_user_map returns email->id mapping."""
        # Create mock users
        mock_user1 = MagicMock()
        mock_user1.email = "John@gmail.co"
        mock_user1.id = 1

        mock_user2 = MagicMock()
        mock_user2.email = "jane@gmail.co"
        mock_user2.id = 2

        mock_get_users.return_value = [mock_user1, mock_user2]

        # Create schema instance with mocked get_users (call real get_user_map with mock self)
        schema = MagicMock(spec=DealCloudSchema)
        schema.get_users = mock_get_users

        # Call real get_user_map with mock as self so it uses mocked get_users
        result = DealCloudSchema.get_user_map(schema)

        # Verify lowercase keys
        assert "john@gmail.co" in result
        assert "jane@gmail.co" in result
        assert result["john@gmail.co"] == 1
        assert result["jane@gmail.co"] == 2

