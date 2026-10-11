"""Tests for DealCloudUserManagement class."""

import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch

from intapp_rest_client.exceptions import HttpError

from dealcloud_sdk.usermanagement.dealcloud_usermanagement import DealCloudUserManagement


class TestDealCloudUserManagementInit:
    """Tests for initialization."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_init_sets_usermgmt_url(self, mock_client_class):
        """Test that init sets user management URL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        assert "management/user" in um._usermgmt_url and "v1" in um._usermgmt_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_usermanagement_url_property(self, mock_client_class):
        """usermanagement_url exposes the same base URL as _usermgmt_url."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.usermanagement_url == um._usermgmt_url
        assert "management/user" in um.usermanagement_url


class TestUserCRUD:
    """Tests for user CRUD operations."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_basic(self, mock_client_class):
        """Test create_user basic."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"id": 1, "email": "john@gmail.co"}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.create_user("john@gmail.co", "John", "Doe")
        
        assert result["id"] == 1
        mock_client.post.assert_called_once()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_with_groups_ids(self, mock_client_class):
        """Test create_user with groups as list of IDs (sent as-is)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"id": 1}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        um.create_user("john@gmail.co", "John", "Doe", groups=[10, 20])
        
        payload = mock_client.post.call_args[1]["json"]
        assert payload["groups"] == [10, 20]
        mock_client.get.assert_not_called()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_with_groups_names_resolves_to_ids(self, mock_client_class):
        """Test create_user with groups as list of names resolves via resolve_group_names_to_ids."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 10, "name": "Admins"},
            {"id": 20, "name": "API"},
        ]
        mock_client.post.return_value = {"id": 1}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        um.create_user("john@gmail.co", "John", "Doe", groups=["Admins", "API"])
        
        payload = mock_client.post.call_args[1]["json"]
        assert payload["groups"] == [10, 20]
        mock_client.get.assert_called_once()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_with_password_and_2fa(self, mock_client_class):
        """Test create_user with password and two_factor_enabled (API params)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"id": 1}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        um.create_user(
            "john@gmail.co", "John", "Doe",
            password="secret123",
            two_factor_enabled=True,
        )
        
        payload = mock_client.post.call_args[1]["json"]
        assert payload["password"] == "secret123"
        assert payload["twoFactorEnabled"] is True
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_with_federation_id(self, mock_client_class):
        """Test create_user with federation_id (SSO)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"id": 1}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        um.create_user(
            "sso@gmail.co", "SSO", "User",
            federation_id="sso@gmail.co",
        )
        
        payload = mock_client.post.call_args[1]["json"]
        assert payload["federationId"] == "sso@gmail.co"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_with_ip_restrictions_enabled(self, mock_client_class):
        """Test create_user with ip_restrictions_enabled."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"id": 1}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        um.create_user("john@gmail.co", "John", "Doe", ip_restrictions_enabled=True)
        
        payload = mock_client.post.call_args[1]["json"]
        assert payload["ipRestrictionsEnabled"] is True
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_inactive(self, mock_client_class):
        """Test create_user with is_active=False."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"id": 1, "isActive": False}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        um.create_user("john@gmail.co", "John", "Doe", is_active=False)
        
        payload = mock_client.post.call_args[1]["json"]
        assert payload["isActive"] is False
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user(self, mock_client_class):
        """Test get_user (uses get_users_by_ids: POST with body [id])."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"id": 1, "email": "john@gmail.co"}]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_user(1)
        
        assert result["id"] == 1
        mock_client.post.assert_called_once()
        assert mock_client.post.call_args[1]["json"] == [1]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_users(self, mock_client_class):
        """create_users calls create_user for each dict and returns all results."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.side_effect = [
            {"id": 1, "email": "a@gmail.co"},
            {"id": 2, "email": "b@gmail.co", "isActive": False},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        results = um.create_users([
            {"email": "a@gmail.co", "first_name": "A", "last_name": "One"},
            {
                "email": "b@gmail.co",
                "first_name": "B",
                "last_name": "Two",
                "password": "x",
                "is_active": False,
            },
        ])

        assert len(results) == 2
        assert results[0]["id"] == 1
        assert results[1]["id"] == 2
        assert mock_client.post.call_count == 2
        second_payload = mock_client.post.call_args_list[1][1]["json"]
        assert second_payload["password"] == "x"
        assert second_payload["isActive"] is False

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_by_ids(self, mock_client_class):
        """Test get_users_by_ids (POST /management/user with body [ids])."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"id": 1}, {"id": 2}]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_users_by_ids([1, 2])
        
        assert len(result) == 2
        mock_client.post.assert_called_once()
        assert mock_client.post.call_args[1]["json"] == [1, 2]
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_requires_filter(self, mock_client_class):
        """Test get_users with no filter raises ValueError."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(ValueError, match="Provide either modified_since, emails or user_group_ids"):
            um.get_users()
        
        with pytest.raises(ValueError, match="Provide either modified_since, emails or user_group_ids"):
            um.get_users(emails=[])
        
        with pytest.raises(ValueError, match="Provide either modified_since, emails or user_group_ids"):
            um.get_users(user_group_ids=[])

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_user_ids_with_filter_raises(self, mock_client_class):
        """Cannot combine user_ids (POST) with GET filters."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="Use either user_ids"):
            um.get_users(user_ids=[1], emails="a@x.com")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_only_one_filter_allowed(self, mock_client_class):
        """Test get_users with two filters raises ValueError."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        with pytest.raises(ValueError, match="only one filter is allowed"):
            um.get_users(emails="a@x.com", user_group_ids=1)
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_with_user_group_ids_filter(self, mock_client_class):
        """Test get_users with user_group_ids only (GET params)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1}, {"id": 2}]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_users(
            user_group_ids=5,
            page_number=2,
            page_size=100,
        )
        
        assert len(result) == 2
        call_url = mock_client.get.call_args[0][0]
        assert "userGroupID=5" in call_url
        assert "pageNumber=2" in call_url
        assert "pageSize=100" in call_url
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_with_modified_since_filter(self, mock_client_class):
        """Test get_users with modified_since only (GET params)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1}]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_users(modified_since=datetime(2024, 1, 1))
        
        assert len(result) == 1
        call_url = mock_client.get.call_args[0][0]
        assert "modifiedSince=" in call_url
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_with_emails_single(self, mock_client_class):
        """Test get_users with single email (emails=str)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1, "email": "a@x.com"}]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_users(emails="a@x.com")
        
        assert len(result) == 1
        assert result[0]["email"] == "a@x.com"
        call_url = mock_client.get.call_args[0][0]
        assert "email=" in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_modified_since_string(self, mock_client_class):
        """modified_since may be an ISO string (not only datetime)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.get_users(modified_since="2024-06-01T00:00:00")

        call_url = mock_client.get.call_args[0][0]
        assert "modifiedSince=" in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_all_users_paginates_until_empty(self, mock_client_class):
        """get_all_users loops get_users until an empty batch."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"id": 1}, {"id": 2}],
            [{"id": 3}],
            [],
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        users = um.get_all_users(page_size=1000)

        assert len(users) == 3
        assert mock_client.get.call_count == 3

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_with_emails_list(self, mock_client_class):
        """Test get_users with list of emails (multiple GETs, combined)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [[{"id": 1, "email": "a@x.com"}], [{"id": 2, "email": "b@x.com"}]]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_users(emails=["a@x.com", "b@x.com"])
        
        assert len(result) == 2
        assert mock_client.get.call_count == 2
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_with_user_group_ids_list(self, mock_client_class):
        """Test get_users with list of user_group_ids (multiple GETs, combined)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [[{"id": 1}], [{"id": 2}]]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_users(user_group_ids=[5, 10])
        
        assert len(result) == 2
        assert mock_client.get.call_count == 2

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_emails_list_deduplicates_by_id(self, mock_client_class):
        """When multiple emails resolve to the same user id, combined list deduplicates."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"id": 1, "email": "a@x.com"}],
            [{"id": 1, "email": "alias@x.com"}],
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_users(emails=["a@x.com", "alias@x.com"])

        assert len(result) == 1
        assert result[0]["id"] == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_user_group_ids_list_deduplicates_by_id(self, mock_client_class):
        """When multiple group filters return the same user, combined list deduplicates."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"id": 1, "email": "u@gmail.co"}],
            [{"id": 1, "email": "u@gmail.co"}],
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_users(user_group_ids=[5, 10])

        assert len(result) == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_resolve_group_names_to_ids(self, mock_client_class):
        """Test resolve_group_names_to_ids maps names to IDs via get_user_groups."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 10, "name": "Admins"},
            {"id": 20, "name": "API"},
        ]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        ids = um.resolve_group_names_to_ids("Admins")
        assert ids == [10]
        
        ids = um.resolve_group_names_to_ids(["Admins", "API"])
        assert ids == [10, 20]
        
        with pytest.raises(ValueError, match="Unknown user group name"):
            um.resolve_group_names_to_ids("Nonexistent")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_resolve_group_names_skips_groups_with_no_name(self, mock_client_class):
        """Groups with name=None are ignored when building name->id map."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"id": 99, "name": None},
            {"id": 10, "name": "Admins"},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.resolve_group_names_to_ids("Admins") == [10]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_users_with_group_name_resolves_then_fetches(self, mock_client_class):
        """Test get_users(user_group_ids='Admins') resolves name to ID then GETs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"id": 10, "name": "Admins"}],  # get_user_groups
            [{"id": 1}, {"id": 2}],           # get_users(user_group_ids=10)
        ]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_users(user_group_ids="Admins")
        
        assert len(result) == 2
        assert mock_client.get.call_count == 2
        call_url = mock_client.get.call_args[0][0]
        assert "userGroupID=10" in call_url
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_by_email_found(self, mock_client_class):
        """Test get_user_by_email when found (via get_users with emails filter)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1, "email": "john@gmail.co"}]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_user_by_email("john@gmail.co")
        
        assert result["id"] == 1
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_by_email_not_found(self, mock_client_class):
        """Test get_user_by_email when not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_user_by_email("unknown@gmail.co")
        
        assert result is None
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user(self, mock_client_class):
        """Test update_user fetches user when email/lastName missing, then PUTs with payload (camelCase)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"id": 1, "firstName": "Old", "lastName": "Doe", "email": "e@x.com"}]
        mock_client.put.return_value = {"id": 1, "firstName": "Johnny"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.update_user(1, first_name="Johnny")

        assert result["firstName"] == "Johnny"
        mock_client.put.assert_called_once()
        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 1
        assert payload["firstName"] == "Johnny"
        assert payload["lastName"] == "Doe"
        assert payload["email"] == "e@x.com"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_with_email(self, mock_client_class):
        """Test update_user with email; fetches user for missing firstName/lastName, then PUTs (camelCase)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"id": 1, "firstName": "Old", "lastName": "Doe", "email": "old@gmail.co"}]
        mock_client.put.return_value = {"id": 1, "email": "new@gmail.co"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.update_user(1, email="new@gmail.co")

        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 1
        assert payload["email"] == "new@gmail.co"
        assert payload["firstName"] == "Old"
        assert payload["lastName"] == "Doe"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_with_last_name(self, mock_client_class):
        """Test update_user with last_name; fetches user for missing firstName/email, then PUTs (camelCase)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"id": 1, "firstName": "Old", "lastName": "Doe", "email": "e@x.com"}]
        mock_client.put.return_value = {"id": 1, "lastName": "Smith"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.update_user(1, last_name="Smith")

        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 1
        assert payload["lastName"] == "Smith"
        assert payload["firstName"] == "Old"
        assert payload["email"] == "e@x.com"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_with_groups(self, mock_client_class):
        """Test update_user with groups; fetches user for missing email/firstName/lastName, then PUTs (camelCase)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [{"id": 1, "firstName": "Old", "lastName": "Doe", "email": "e@x.com"}]
        mock_client.put.return_value = {"id": 1, "groups": [10, 20]}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.update_user(1, groups=[10, 20])

        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 1
        assert payload["groups"] == [10, 20]
        assert payload["firstName"] == "Old"
        assert payload["lastName"] == "Doe"
        assert payload["email"] == "e@x.com"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_groups_with_names_resolves(self, mock_client_class):
        """update_user with groups as names resolves via resolve_group_names_to_ids."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 10, "name": "Admins"}]
        mock_client.post.return_value = [{"id": 1, "firstName": "F", "lastName": "L", "email": "e@x.com"}]
        mock_client.put.return_value = {"id": 1}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.update_user(1, groups=["Admins"])

        payload = mock_client.put.call_args[1]["json"]
        assert payload["groups"] == [10]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_not_found_raises_value_error(self, mock_client_class):
        """Test update_user raises ValueError when API returns 400 'does not exist'."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.side_effect = HttpError(
            400,
            "User with given id does not exist.",
            response_body="User with given id does not exist.",
        )
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="User with given id does not exist"):
            um.update_user(999, first_name="X")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_http_error_other_400_re_raises(self, mock_client_class):
        """PUT returns 400 without 'does not exist' — HttpError propagates."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.side_effect = HttpError(
            400,
            "Bad request",
            response_body="Some other validation error",
        )
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(HttpError):
            um.update_user(1, first_name="X", email="e@x.com", last_name="L")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_http_error_not_found_returns_none(self, mock_client_class):
        """get_user swallows HttpError 404 / 'does not exist' and returns None."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = HttpError(
            404,
            "Not found",
            response_body="User does not exist",
        )
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.get_user("missing@gmail.co") is None

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_http_error_re_raises(self, mock_client_class):
        """get_user re-raises HttpError that is not a not-found case."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = HttpError(500, "Server error")
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(HttpError, match="Server error"):
            um.get_user("x@gmail.co")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_by_id_http_error_not_found_returns_none(self, mock_client_class):
        """get_user(int) swallows HttpError when status is 404."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.side_effect = HttpError(404, "Not found")
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.get_user(99999) is None

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_users(self, mock_client_class):
        """Test update_users calls update_user per item and returns list of results."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.side_effect = [
            {"id": 1, "firstName": "Alice"},
            {"id": 2, "email": "bob@gmail.co"},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        results = um.update_users([
            {"id": 1, "firstName": "Alice"},
            {"id": 2, "email": "bob@gmail.co"},
        ])

        assert len(results) == 2
        assert results[0]["firstName"] == "Alice"
        assert results[1]["email"] == "bob@gmail.co"
        assert mock_client.put.call_count == 2
        # update_user fills required API fields (email, firstName, lastName) when omitted
        p0 = mock_client.put.call_args_list[0][1]["json"]
        assert p0["id"] == 1 and p0["firstName"] == "Alice"
        p1 = mock_client.put.call_args_list[1][1]["json"]
        assert p1["id"] == 2 and p1["email"] == "bob@gmail.co"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_users_accepts_id_key(self, mock_client_class):
        """Test update_users accepts swagger-shaped spec with 'id' and camelCase fields."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.side_effect = [{"id": 10, "isActive": False}]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        results = um.update_users([{"id": 10, "isActive": False}])

        assert len(results) == 1
        assert results[0]["id"] == 10
        mock_client.put.assert_called_once()
        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 10
        assert payload["isActive"] is False

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_users_missing_id_raises(self, mock_client_class):
        """Test update_users raises ValueError when a spec has no 'id' (swagger)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="Each update spec must have 'id'"):
            um.update_users([{"firstName": "NoId"}])

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_users_passes_optional_fields(self, mock_client_class):
        """Test update_users passes all optional fields through to update_user."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = {"id": 1}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.update_users([{
            "id": 1,
            "email": "e@x.com",
            "firstName": "F",
            "lastName": "L",
            "password": "p",
            "federationId": "fed",
            "groups": [5],
            "twoFactorEnabled": True,
            "ipRestrictionsEnabled": True,
            "isActive": False,
        }])

        mock_client.put.assert_called_once()
        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 1
        assert payload["email"] == "e@x.com"
        assert payload["firstName"] == "F"
        assert payload["lastName"] == "L"
        assert payload["password"] == "p"
        assert payload["federationId"] == "fed"
        assert payload["groups"] == [5]
        assert payload["twoFactorEnabled"] is True
        assert payload["ipRestrictionsEnabled"] is True
        assert payload["isActive"] is False
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user(self, mock_client_class):
        """Test delete_user."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.delete_user(1)
        
        assert result is True
        mock_client.delete.assert_called_once()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_deactivate_user(self, mock_client_class):
        """Test deactivate_user fetches user via get_user then PUTs with firstName, lastName, email, isActive=False."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [
            {"id": 1, "firstName": "John", "lastName": "Doe", "email": "john@gmail.co"},
        ]
        mock_client.put.return_value = {"id": 1, "isActive": False}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.deactivate_user(1)

        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 1
        assert payload["firstName"] == "John"
        assert payload["lastName"] == "Doe"
        assert payload["email"] == "john@gmail.co"
        assert payload["isActive"] is False

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_deactivate_user_by_email(self, mock_client_class):
        """Test deactivate_user accepts email; get_user uses GET with emails filter."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 2, "firstName": "Jane", "lastName": "Smith", "email": "jane@gmail.co"}]
        mock_client.put.return_value = {"id": 2, "isActive": False}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.deactivate_user("jane@gmail.co")

        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 2
        assert payload["firstName"] == "Jane"
        assert payload["isActive"] is False

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_deactivate_user_not_found_raises(self, mock_client_class):
        """Test deactivate_user raises ValueError when user is not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="User not found"):
            um.deactivate_user(999)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_activate_user(self, mock_client_class):
        """Test activate_user fetches user via get_user then PUTs with firstName, lastName, email, isActive=True."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = [
            {"id": 1, "firstName": "Jane", "lastName": "Smith", "email": "jane@gmail.co"},
        ]
        mock_client.put.return_value = {"id": 1, "isActive": True}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.activate_user(1)

        payload = mock_client.put.call_args[1]["json"]
        assert payload["id"] == 1
        assert payload["firstName"] == "Jane"
        assert payload["lastName"] == "Smith"
        assert payload["email"] == "jane@gmail.co"
        assert payload["isActive"] is True

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_activate_user_not_found_raises(self, mock_client_class):
        """Test activate_user raises ValueError when user is not found."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = []
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="User not found"):
            um.activate_user(999)


class TestUserGroups:
    """Tests for user group operations."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_all_user_groups(self, mock_client_class):
        """Test get_all_user_groups (list all with default pagination)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 1, "name": "Admins"}]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_all_user_groups()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "Admins"
        mock_client.get.assert_called_once()
        call_url = mock_client.get.call_args[0][0]
        assert "pageNumber=1" in call_url
        assert "pageSize=1000" in call_url
        assert call_url.endswith("/group?pageNumber=1&pageSize=1000") or "/group?" in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_all_user_groups_pagination_params(self, mock_client_class):
        """Test get_all_user_groups with explicit page_number and page_size."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.get_all_user_groups(page_number=2, page_size=50)

        mock_client.get.assert_called_once()
        call_url = mock_client.get.call_args[0][0]
        assert "pageNumber=2" in call_url
        assert "pageSize=50" in call_url
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_group(self, mock_client_class):
        """Test get_user_groups with single ID returns one group dict."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"id": 1, "name": "Admins", "memberIds": [1, 2]}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_user_groups(1)

        assert result["name"] == "Admins"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_group_by_name(self, mock_client_class):
        """Test get_user_groups with string name resolves via resolve_group_names_to_ids."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"id": 10, "name": "Admins"}, {"id": 20, "name": "API"}],
            {"id": 10, "name": "Admins", "memberIds": [1, 2]},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_user_groups("Admins")

        assert isinstance(result, dict)
        assert result["name"] == "Admins"
        assert result["id"] == 10
        assert mock_client.get.call_count == 2
        assert mock_client.get.call_args_list[1][0][0].endswith("/group/10")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_group_list(self, mock_client_class):
        """Test get_user_groups with list of IDs returns list of group dicts."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            {"id": 1, "name": "G1"},
            {"id": 2, "name": "G2"},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_user_groups([1, 2])

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["name"] == "G1"
        assert result[1]["name"] == "G2"
        assert mock_client.get.call_count == 2

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_groups_mixed_ids_and_names(self, mock_client_class):
        """get_user_groups with [int, str] resolves names and fetches each group."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            [{"id": 10, "name": "Admins"}],
            {"id": 1, "name": "First"},
            {"id": 10, "name": "Admins"},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_user_groups([1, "Admins"])

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 10

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_group(self, mock_client_class):
        """Test update_user_group."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = {"id": 1, "name": "Updated"}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.update_user_group(1, name="Updated")
        
        assert result["name"] == "Updated"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_group_with_description(self, mock_client_class):
        """Test update_user_group with description."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = {"id": 1, "description": "New description"}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        um.update_user_group(1, description="New description")
        
        payload = mock_client.put.call_args[1]["json"]
        assert payload["description"] == "New description"
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_group(self, mock_client_class):
        """Test delete_user_group."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.delete_user_group(1)

        assert result is True
        mock_client.delete.assert_called_once()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_group_by_name(self, mock_client_class):
        """Test delete_user_group with string name resolves via resolve_group_names_to_ids."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 10, "name": "Admins"}]
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.delete_user_group("Admins")

        assert result is True
        mock_client.delete.assert_called_once()
        assert mock_client.delete.call_args[0][0].endswith("/group/10")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_group_list(self, mock_client_class):
        """Test delete_user_group with list of IDs deletes each."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.delete_user_group([1, 2])

        assert result is True
        assert mock_client.delete.call_count == 2
        urls = [c[0][0] for c in mock_client.delete.call_args_list]
        assert any("/group/1" in u for u in urls)
        assert any("/group/2" in u for u in urls)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_group_mixed_ids_and_names(self, mock_client_class):
        """delete_user_group([int, str]) resolves names and deletes each id."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 10, "name": "Admins"}]
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.delete_user_group([2, "Admins"]) is True
        assert mock_client.delete.call_count == 2
        urls = [c[0][0] for c in mock_client.delete.call_args_list]
        assert any("/group/2" in u for u in urls)
        assert any("/group/10" in u for u in urls)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_user_to_group(self, mock_client_class):
        """Test add_user_to_group."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"id": 1, "memberIds": [1]}
        mock_client.put.return_value = {"id": 1, "memberIds": [1, 2]}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.add_user_to_group(2, 1)
        
        # Should have added user 2 to the list
        payload = mock_client.put.call_args[1]["json"]
        assert 2 in payload["memberIds"]
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_user_to_group_already_member(self, mock_client_class):
        """Test add_user_to_group when already member."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"id": 1, "memberIds": [1, 2]}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.add_user_to_group(2, 1)
        
        # Should not call put if already member
        mock_client.put.assert_not_called()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_remove_user_from_group(self, mock_client_class):
        """Test remove_user_from_group."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"id": 1, "memberIds": [1, 2]}
        mock_client.put.return_value = {"id": 1, "memberIds": [1]}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.remove_user_from_group(2, 1)
        
        payload = mock_client.put.call_args[1]["json"]
        assert 2 not in payload["memberIds"]
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_remove_user_from_group_not_member(self, mock_client_class):
        """Test remove_user_from_group when user is not in group."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {"id": 1, "memberIds": [1, 3]}  # User 2 not in list
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.remove_user_from_group(2, 1)  # Try to remove user 2 who's not there
        
        # Should not call put if user not in group
        mock_client.put.assert_not_called()
        # Should return current group
        assert result["id"] == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_users_to_groups(self, mock_client_class):
        """Test add_users_to_groups sends PUT /user/group with array of userIds/groupIds."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.add_users_to_groups([
            {"userIds": [1, 2], "groupIds": [10]},
            {"userIds": [3], "groupIds": [10, 20]},
        ])

        mock_client.put.assert_called_once()
        assert "/group" in mock_client.put.call_args[0][0]
        payload = mock_client.put.call_args[1]["json"]
        assert payload == [
            {"userIds": [1, 2], "groupIds": [10]},
            {"userIds": [3], "groupIds": [10, 20]},
        ]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_users_to_groups_snake_case_and_group_names(self, mock_client_class):
        """add_users_to_groups accepts user_ids/group_ids and resolves string group names."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 10, "name": "Admins"}]
        mock_client.put.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.add_users_to_groups([
            {"user_ids": [1], "group_ids": ["Admins"]},
        ])

        payload = mock_client.put.call_args[1]["json"]
        assert payload == [{"userIds": [1], "groupIds": [10]}]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_users_to_groups_empty_payload_returns_none(self, mock_client_class):
        """When all assignments are skipped, PUT is not called and None is returned."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.add_users_to_groups([{"userIds": [], "groupIds": [1]}]) is None
        assert um.add_users_to_groups([{"userIds": [1], "groupIds": []}]) is None
        mock_client.put.assert_not_called()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_remove_users_from_groups(self, mock_client_class):
        """Test remove_users_from_groups sends DELETE /user/group with array of userIds/groupIds."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.remove_users_from_groups([{"userIds": [1, 2], "groupIds": [10]}])

        mock_client.delete.assert_called_once()
        assert "/group" in mock_client.delete.call_args[0][0]
        payload = mock_client.delete.call_args[1]["json"]
        assert payload == [{"userIds": [1, 2], "groupIds": [10]}]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_remove_users_from_groups_snake_case_and_names(self, mock_client_class):
        """remove_users_from_groups accepts snake_case keys and resolves group names."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 10, "name": "Admins"}]
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.remove_users_from_groups([{"user_ids": [5], "group_ids": ["Admins"]}])

        payload = mock_client.delete.call_args[1]["json"]
        assert payload == [{"userIds": [5], "groupIds": [10]}]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_remove_users_from_groups_empty_payload_returns_none(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.remove_users_from_groups([{}]) is None
        mock_client.delete.assert_not_called()


class TestUserLicenses:
    """Tests for user license operations (get_user_licenses, update_user_license)."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_licenses_single_id(self, mock_client_class):
        """Test get_user_licenses with single user ID returns one license dict."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = {
            "userId": 42,
            "licenseType": "Standard",
            "isBillable": True,
            "description": "Full access",
        }
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_user_licenses(42)

        assert isinstance(result, dict)
        assert result["userId"] == 42
        assert result["isBillable"] is True
        mock_client.get.assert_called_once()
        assert "/management/userLicense/42" in mock_client.get.call_args[0][0]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_licenses_list_of_ids(self, mock_client_class):
        """Test get_user_licenses with list of user IDs returns list of license dicts."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.side_effect = [
            {"userId": 1, "licenseType": "Standard", "isBillable": True},
            {"userId": 2, "licenseType": "Limited", "isBillable": True},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_user_licenses([1, 2])

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["userId"] == 1
        assert result[1]["userId"] == 2
        assert mock_client.get.call_count == 2
        urls = [c[0][0] for c in mock_client.get.call_args_list]
        assert any("/userLicense/1" in u for u in urls)
        assert any("/userLicense/2" in u for u in urls)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_licenses_paginated_defaults(self, mock_client_class):
        """Test get_user_licenses with user_ids=None uses pagination (default page/size)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"userId": 1, "isBillable": True}]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.get_user_licenses()

        assert isinstance(result, list)
        assert len(result) == 1
        mock_client.get.assert_called_once()
        call_url = mock_client.get.call_args[0][0]
        assert "/management/userLicenses" in call_url
        assert "pageNumber=1" in call_url
        assert "pageSize=10" in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_licenses_paginated_with_filter(self, mock_client_class):
        """Test get_user_licenses with user_ids=None and is_billable, page params."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.get_user_licenses(is_billable=True, page_number=2, page_size=50)

        call_url = mock_client.get.call_args[0][0]
        assert "/management/userLicenses" in call_url
        assert "isBillable=true" in call_url
        assert "pageNumber=2" in call_url
        assert "pageSize=50" in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_license(self, mock_client_class):
        """Test update_user_license sends PUT with userId, licenseType, optional description."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.update_user_license(10, license_type=2, description="Limited")

        mock_client.put.assert_called_once()
        call_url = mock_client.put.call_args[0][0]
        assert "/management/userLicense" in call_url
        payload = mock_client.put.call_args[1]["json"]
        assert payload["userId"] == 10
        assert payload["licenseType"] == 2
        assert payload["description"] == "Limited"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_update_user_licenses(self, mock_client_class):
        """Test update_user_licenses calls update_user_license for each item in list."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.put.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        updates = [
            {"userId": 1, "licenseType": 2},
            {"userId": 2, "licenseType": 3, "description": "Free"},
        ]
        result = um.update_user_licenses(updates)

        assert len(result) == 2
        assert mock_client.put.call_count == 2
        payloads = [c[1]["json"] for c in mock_client.put.call_args_list]
        assert payloads[0]["userId"] == 1 and payloads[0]["licenseType"] == 2
        assert payloads[1]["userId"] == 2 and payloads[1]["licenseType"] == 3
        assert payloads[1]["description"] == "Free"


class TestUserProxy:
    """Tests for user proxy operations."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_proxy(self, mock_client_class):
        """Test create_user_proxy (proxy_user_id, principal_user_ids) per API docs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.create_user_proxy(proxy_user_id=2, principal_user_ids=1)

        payload = mock_client.post.call_args[1]["json"]
        assert payload["proxyUserId"] == 2
        assert payload["users"] == [1]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_create_user_proxy_multiple_principals(self, mock_client_class):
        """Test create_user_proxy with multiple principal user IDs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.create_user_proxy(proxy_user_id=2, principal_user_ids=[1, 3])

        payload = mock_client.post.call_args[1]["json"]
        assert payload["proxyUserId"] == 2
        assert payload["users"] == [1, 3]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_proxy(self, mock_client_class):
        """Test get_user_proxy (GET .../proxy; optional user_id filters client-side)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"userId": 1, "proxyUserId": 2}]
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_user_proxy(1)

        assert len(result) == 1
        assert result[0]["userId"] == 1

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_proxy_search_by_name(self, mock_client_class):
        """Test get_user_proxy passes searchByName query param when provided."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.get_user_proxy(proxy_query="user@domain.com", search_by_name=False)

        call_url = mock_client.get.call_args[0][0]
        assert "searchByName=false" in call_url
        assert "proxyQuery=user%40domain.com" in call_url or "proxyQuery=" in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_proxy_includes_user_query(self, mock_client_class):
        """user_query is appended to the proxy GET URL."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = []
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.get_user_proxy(user_query="principal@corp.com")

        call_url = mock_client.get.call_args[0][0]
        assert "userQuery=" in call_url

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_proxy(self, mock_client_class):
        """Test delete_user_proxy."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.delete_user_proxy(1, 2)
        
        assert result is True

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_proxies_from_current(self, mock_client_class):
        """Test delete_user_proxies_from_current gets proxy list then deletes each assignment."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        # API returns list of { proxyUser: {id}, users: [{id}, ...] } or flat { userId, proxyUserId }
        mock_client.get.return_value = [
            {"proxyUser": {"id": 20}, "users": [{"id": 10}, {"id": 11}]},
            {"userId": 12, "proxyUserId": 21},
        ]
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        results = um.delete_user_proxies_from_current()

        assert results == [True, True, True]  # (10,20), (11,20), (12,21)
        assert mock_client.get.call_count == 1
        assert mock_client.delete.call_count == 3
        delete_urls = [c[0][0] for c in mock_client.delete.call_args_list]
        assert any("/proxy/10/20" in u for u in delete_urls)
        assert any("/proxy/11/20" in u for u in delete_urls)
        assert any("/proxy/12/21" in u for u in delete_urls)

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_proxies_skips_assignment_without_proxy_id(self, mock_client_class):
        """Rows without proxy user id are skipped (no delete)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"users": [{"id": 1}]}]  # no proxyUserId / proxyUser
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.delete_user_proxies_from_current() == []
        mock_client.delete.assert_not_called()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_proxies_skips_nested_user_without_id(self, mock_client_class):
        """Users array entries without id/Id do not produce delete pairs."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"proxyUserId": 20, "users": [{"id": 10}, {}]},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.delete_user_proxies_from_current() == [True]
        mock_client.delete.assert_called_once()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_proxies_filters_by_proxy_user_id(self, mock_client_class):
        """Only pairs matching proxy_user_id are deleted."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [
            {"userId": 1, "proxyUserId": 10},
            {"userId": 2, "proxyUserId": 99},
        ]
        mock_client.delete.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        results = um.delete_user_proxies_from_current(proxy_user_id=10)

        assert results == [True]
        mock_client.delete.assert_called_once()
        assert "/proxy/1/10" in mock_client.delete.call_args[0][0]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_delete_user_proxies_flat_row_without_principal_skipped(self, mock_client_class):
        """Flat shape with no users[] and no userId does not add a pair."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"proxyUserId": 7}]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        assert um.delete_user_proxies_from_current() == []
        mock_client.delete.assert_not_called()


class TestUserInvitations:
    """Tests for user invitation operations."""

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_invite_user(self, mock_client_class):
        """Test invite_user (single email, one POST)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"invited": True}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.invite_user("a@gmail.co")

        assert result == {"invited": True}
        mock_client.post.assert_called_once()
        payload = mock_client.post.call_args[1]["json"]
        assert payload["email"] == "a@gmail.co"

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_invite_user_with_duration_and_groups(self, mock_client_class):
        """Test invite_user with duration and groups (IDs)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.invite_user("a@gmail.co", duration=5, groups=[1, 2])

        payload = mock_client.post.call_args[1]["json"]
        assert payload["email"] == "a@gmail.co"
        assert payload["duration"] == 5
        assert payload["groups"] == [1, 2]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_invite_user_auto_create_and_mapped_contact(self, mock_client_class):
        """invite_user sends autoCreateOrLinkContact and mappedContactId when set."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.invite_user(
            "inv@gmail.co",
            auto_create_or_link_contact=True,
            mapped_contact_id=555,
        )

        payload = mock_client.post.call_args[1]["json"]
        assert payload["autoCreateOrLinkContact"] is True
        assert payload["mappedContactId"] == 555

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_invite_user_with_group_names_resolves(self, mock_client_class):
        """Test invite_user with groups as names resolves via resolve_group_names_to_ids."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 10, "name": "Admins"}, {"id": 20, "name": "API"}]
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.invite_user("a@gmail.co", groups=["Admins", "API"])

        payload = mock_client.post.call_args[1]["json"]
        assert payload["groups"] == [10, 20]
        mock_client.get.assert_called_once()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_existing_user(self, mock_client_class):
        """Test add_existing_user (shadow-add) POSTs to /addExisting with same params as invite."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"added": True}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.add_existing_user("shadow@gmail.co", duration=10, groups=[1, 2])

        assert result == {"added": True}
        mock_client.post.assert_called_once()
        call_url = mock_client.post.call_args[0][0]
        assert "addExisting" in call_url
        payload = mock_client.post.call_args[1]["json"]
        assert payload["email"] == "shadow@gmail.co"
        assert payload["duration"] == 10
        assert payload["groups"] == [1, 2]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_existing_user_with_is_active(self, mock_client_class):
        """Test add_existing_user sends isActive when is_active is provided (Swagger AddExistingUserRequestVm)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.add_existing_user("u@gmail.co", is_active=False)
        payload = mock_client.post.call_args[1]["json"]
        assert payload["isActive"] is False

        um.add_existing_user("v@gmail.co", is_active=True)
        payload = mock_client.post.call_args[1]["json"]
        assert payload["isActive"] is True

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_existing_users(self, mock_client_class):
        """Test add_existing_users (list of specs) calls add_existing_user per item."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        results = um.add_existing_users([
            {"email": "a@gmail.co"},
            {"email": "b@gmail.co", "duration": 5},
        ])

        assert len(results) == 2
        assert mock_client.post.call_count == 2
        assert "addExisting" in mock_client.post.call_args_list[0][0][0]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_existing_user_group_names_and_contact_options(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.get.return_value = [{"id": 10, "name": "Admins"}]
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.add_existing_user(
            "u@gmail.co",
            groups=["Admins"],
            auto_create_or_link_contact=True,
            mapped_contact_id=99,
        )

        payload = mock_client.post.call_args[1]["json"]
        assert payload["groups"] == [10]
        assert payload["autoCreateOrLinkContact"] is True
        assert payload["mappedContactId"] == 99

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_invite_users(self, mock_client_class):
        """Test invite_users (list of invite specs; calls invite_user per item)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"invited": True}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        result = um.invite_users([
            {"email": "a@gmail.co"},
            {"email": "b@gmail.co"},
        ])

        assert len(result) == 2
        assert mock_client.post.call_count == 2
        assert result[0] == result[1] == {"invited": True}

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_invite_users_with_duration_and_groups(self, mock_client_class):
        """Test invite_users passes per-spec options to invite_user."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.invite_users([{"email": "a@gmail.co", "duration": 5, "groups": [1, 2]}])

        payload = mock_client.post.call_args[1]["json"]
        assert payload["email"] == "a@gmail.co"
        assert payload["duration"] == 5
        assert payload["groups"] == [1, 2]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_invite_users_missing_email_raises(self, mock_client_class):
        """Test invite_users raises ValueError when a spec has no email."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="Each invite spec must have 'email'"):
            um.invite_users([{"duration": 5}])

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_add_existing_users_missing_email_raises(self, mock_client_class):
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="Each add-existing spec must have 'email'"):
            um.add_existing_users([{"duration": 5}])


class TestUserActivity:
    """Tests for user activity operations."""
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_activity(self, mock_client_class):
        """Test get_user_activity (POST .../activity with body; returns { totalRecords, rows })."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {
            "totalRecords": 1,
            "rows": [{"action": "login", "timestamp": "2024-01-15T10:00:00Z"}],
        }
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        result = um.get_user_activity(user_ids=[1])
        
        assert "rows" in result
        assert len(result["rows"]) == 1
        mock_client.post.assert_called_once()
    
    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_activity_with_dates(self, mock_client_class):
        """Test get_user_activity with date filters (POST body: dateFrom, dateTo)."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"totalRecords": 0, "rows": []}
        mock_client_class.return_value = mock_client
        
        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )
        
        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)
        um.get_user_activity(
            user_ids=[1], date_from=start, date_to=end, page_number=1, page_size=500
        )
        
        call_args = mock_client.post.call_args
        payload = call_args[1]["json"]
        assert "dateFrom" in payload
        assert "dateTo" in payload
        assert payload["userIds"] == [1]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_activity_accepts_string_names(self, mock_client_class):
        """Test get_user_activity accepts exact string names for activity, source, export_data_type."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"totalRecords": 0, "rows": []}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        um.get_user_activity(
            activity="Export Data",
            source="Web UI",
            export_data_type="Template Report",
        )

        payload = mock_client.post.call_args[1]["json"]
        assert payload["activity"] == 8
        assert payload["source"] == 1
        assert payload["exportDataType"] == 4

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_user_activity_unknown_activity_name_raises(self, mock_client_class):
        """Test get_user_activity raises ValueError for unknown activity name."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        with pytest.raises(ValueError, match="Unknown activity type name"):
            um.get_user_activity(activity="Not An Activity")

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_all_user_activity_date_range_required(self, mock_client_class):
        """Test get_all_user_activity raises if date_to is not greater than date_from."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        start = datetime(2024, 1, 15)
        end = datetime(2024, 1, 10)
        with pytest.raises(ValueError, match="date_to must be greater than date_from"):
            um.get_all_user_activity(date_from=start, date_to=end)

        with pytest.raises(ValueError, match="date_to must be greater than date_from"):
            um.get_all_user_activity(date_from=start, date_to=start)

        mock_client.post.assert_not_called()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_all_user_activity_paginates(self, mock_client_class):
        """Test get_all_user_activity fetches all pages and returns combined rows."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.side_effect = [
            {"totalRecords": 3, "rows": [{"id": 1}, {"id": 2}]},
            {"totalRecords": 3, "rows": [{"id": 3}]},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)
        result = um.get_all_user_activity(date_from=start, date_to=end, page_size=2)

        assert result["totalRecords"] == 3
        assert len(result["rows"]) == 3
        assert [r["id"] for r in result["rows"]] == [1, 2, 3]
        assert mock_client.post.call_count == 2
        # First call page 1, second call page 2
        assert "pageNumber=1" in mock_client.post.call_args_list[0][0][0]
        assert "pageNumber=2" in mock_client.post.call_args_list[1][0][0]

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_all_user_activity_single_page(self, mock_client_class):
        """Test get_all_user_activity with one page returns same shape."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.return_value = {"totalRecords": 1, "rows": [{"id": 1}]}
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)
        result = um.get_all_user_activity(date_from=start, date_to=end)

        assert result["totalRecords"] == 1
        assert result["rows"] == [{"id": 1}]
        mock_client.post.assert_called_once()

    @patch('dealcloud_sdk.base.dealcloud_base.RestClient')
    def test_get_all_user_activity_partial_page_without_total_records(self, mock_client_class):
        """Stops when a page returns fewer rows than page_size if totalRecords is absent."""
        mock_client = MagicMock()
        mock_client._get_auth_headers_sync.return_value = {"Authorization": "Bearer token"}
        mock_client.post.side_effect = [
            {"rows": [{"id": 1}, {"id": 2}]},
            {"rows": [{"id": 3}]},
        ]
        mock_client_class.return_value = mock_client

        um = DealCloudUserManagement(
            site_url="test.dealcloud.com",
            client_id="123",
            client_secret="secret",
        )

        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)
        result = um.get_all_user_activity(date_from=start, date_to=end, page_size=2)

        assert len(result["rows"]) == 3
        assert mock_client.post.call_count == 2


class TestUserActivityConstants:
    """Tests for user activity translation tables and helpers."""

    def test_get_activity_types_returns_dict(self):
        """Test get_activity_types() returns full activity type mapping."""
        from dealcloud_sdk.constants.user_activity import (
            ACTIVITY_TYPES,
            get_activity_types,
            get_activity_type_name,
            get_activity_type_id,
        )

        assert get_activity_types() == ACTIVITY_TYPES
        assert get_activity_type_name(1) == "Login Successful"
        assert get_activity_type_name(8) == "Export Data"
        assert get_activity_type_name(999) == "999"
        assert get_activity_type_id("Export Data") == 8
        with pytest.raises(ValueError, match="Unknown activity type name"):
            get_activity_type_id("Not Real")

    def test_get_source_types_returns_dict(self):
        """Test get_source_types() and get_source_type_name()."""
        from dealcloud_sdk.constants.user_activity import (
            SOURCE_TYPES,
            get_source_types,
            get_source_type_name,
        )

        assert get_source_types() == SOURCE_TYPES
        assert get_source_type_name(1) == "Web UI"
        assert get_source_type_name(11) == "Teams"

    def test_get_export_data_types_returns_dict(self):
        """Test get_export_data_types() and get_export_data_type_name()."""
        from dealcloud_sdk.constants.user_activity import (
            EXPORT_DATA_TYPES,
            get_export_data_types,
            get_export_data_type_name,
        )

        assert get_export_data_types() == EXPORT_DATA_TYPES
        assert get_export_data_type_name(0) == "Export Data"
        assert get_export_data_type_name(4) == "Template Report"

    def test_usermanagement_static_helpers(self):
        """Test DealCloudUserManagement static helpers delegate to constants."""
        from dealcloud_sdk.usermanagement.dealcloud_usermanagement import DealCloudUserManagement

        assert DealCloudUserManagement.get_activity_types() is not None
        assert DealCloudUserManagement.get_activity_type_name(1) == "Login Successful"
        assert DealCloudUserManagement.get_source_types() is not None
        assert DealCloudUserManagement.get_source_type_name(1) == "Web UI"
        assert DealCloudUserManagement.get_export_data_types() is not None
        assert DealCloudUserManagement.get_export_data_type_name(0) == "Export Data"


# Roles: DealCloud User Management API does not expose get_roles/get_role endpoints.
# See https://api.docs.dealcloud.com/docs/management for documented endpoints.

