"""
AuthManager unit tests

Tests the functionality of the API Key authentication manager
"""

import os
import pytest
from unittest.mock import patch

from novita_sandbox.agent_runtime.client.auth import AuthManager
from novita_sandbox.agent_runtime.client.exceptions import AuthenticationError


class TestAuthManager:
    """AuthManager test class"""
    
    @pytest.mark.unit
    def test_init_with_api_key(self, test_api_key: str):
        """Test initialization with API Key"""
        auth = AuthManager(api_key=test_api_key)
        assert auth.api_key == test_api_key
        assert auth.validate_credentials() is True
    
    @pytest.mark.unit
    def test_init_with_env_var(self, test_api_key: str):
        """Test reading API Key from environment variable"""
        with patch.dict(os.environ, {"NOVITA_API_KEY": test_api_key}):
            auth = AuthManager()
            assert auth.api_key == test_api_key
            assert auth.validate_credentials() is True
    
    @pytest.mark.unit
    def test_init_without_api_key(self):
        """Test exception raised when no API Key is provided"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(AuthenticationError) as exc_info:
                AuthManager()
            
            assert "API Key is required" in str(exc_info.value)
    
    @pytest.mark.unit
    def test_init_with_empty_api_key(self):
        """Test exception raised with empty API Key"""
        with pytest.raises(AuthenticationError):
            AuthManager(api_key="")
    
    @pytest.mark.unit
    def test_init_with_short_api_key(self):
        """Test exception raised with too short API Key"""
        with pytest.raises(AuthenticationError):
            AuthManager(api_key="short")
    
    @pytest.mark.unit
    def test_validate_credentials_valid(self, auth_manager: AuthManager):
        """Test valid credentials validation"""
        assert auth_manager.validate_credentials() is True
    
    @pytest.mark.unit
    def test_validate_credentials_invalid(self):
        """Test invalid credentials validation"""
        auth = AuthManager.__new__(AuthManager)  # Bypass __init__
        auth._api_key = None
        assert auth.validate_credentials() is False
    
    @pytest.mark.unit
    def test_get_auth_headers_valid(self, auth_manager: AuthManager, test_api_key: str):
        """Test getting authentication headers"""
        headers = auth_manager.get_auth_headers()
        
        assert isinstance(headers, dict)
        assert "Authorization" in headers
        assert "Content-Type" in headers
        assert headers["Authorization"] == f"Bearer {test_api_key}"
        assert headers["Content-Type"] == "application/json"
    
    @pytest.mark.unit
    def test_get_auth_headers_invalid(self):
        """Test exception raised when getting auth headers with invalid credentials"""
        auth = AuthManager.__new__(AuthManager)  # Bypass __init__
        auth._api_key = None
        
        with pytest.raises(AuthenticationError) as exc_info:
            auth.get_auth_headers()
        
        assert "Invalid or missing API Key" in str(exc_info.value)
    
    @pytest.mark.unit
    def test_api_key_property(self, auth_manager: AuthManager, test_api_key: str):
        """Test API Key property access"""
        assert auth_manager.api_key == test_api_key
    
    @pytest.mark.unit
    def test_api_key_property_unavailable(self):
        """Test exception raised when API Key property is unavailable"""
        auth = AuthManager.__new__(AuthManager)  # Bypass __init__
        auth._api_key = None
        
        with pytest.raises(AuthenticationError) as exc_info:
            _ = auth.api_key
        
        assert "API Key not available" in str(exc_info.value)
    
    @pytest.mark.unit
    def test_update_api_key_valid(self, auth_manager: AuthManager):
        """Test updating valid API Key"""
        new_key = "new-test-api-key-87654321"
        auth_manager.update_api_key(new_key)
        
        assert auth_manager.api_key == new_key
        assert auth_manager.validate_credentials() is True
        
        headers = auth_manager.get_auth_headers()
        assert headers["Authorization"] == f"Bearer {new_key}"
    
    @pytest.mark.unit
    def test_update_api_key_invalid(self, auth_manager: AuthManager):
        """Test updating invalid API Key"""
        with pytest.raises(AuthenticationError) as exc_info:
            auth_manager.update_api_key("short")
        
        assert "Invalid API Key format" in str(exc_info.value)
        
        # Original API Key should remain unchanged
        assert auth_manager.validate_credentials() is True
    
    @pytest.mark.unit
    def test_update_api_key_empty(self, auth_manager: AuthManager):
        """Test updating empty API Key"""
        with pytest.raises(AuthenticationError):
            auth_manager.update_api_key("")
    
    @pytest.mark.unit
    def test_api_key_format_validation(self):
        """Test API Key format validation logic"""
        auth = AuthManager.__new__(AuthManager)  # Bypass __init__
        
        # Valid formats
        assert auth._is_valid_api_key_format("valid-api-key-12345678") is True
        assert auth._is_valid_api_key_format("sk-1234567890abcdef") is True
        assert auth._is_valid_api_key_format("a" * 20) is True
        
        # Invalid formats
        assert auth._is_valid_api_key_format("") is False
        assert auth._is_valid_api_key_format("short") is False
        assert auth._is_valid_api_key_format("   ") is False
        assert auth._is_valid_api_key_format(None) is False
        assert auth._is_valid_api_key_format(123) is False
    
    @pytest.mark.unit
    def test_environment_variable_priority(self, test_api_key: str):
        """Test environment variable priority"""
        env_key = "env-api-key-from-environment"
        
        with patch.dict(os.environ, {"NOVITA_API_KEY": env_key}):
            # Directly provided API Key should take priority over environment variable
            auth = AuthManager(api_key=test_api_key)
            assert auth.api_key == test_api_key
            
            # Should use environment variable when no API Key is provided
            auth_env = AuthManager()
            assert auth_env.api_key == env_key
    
    @pytest.mark.unit
    def test_multiple_auth_headers_calls(self, auth_manager: AuthManager):
        """Test consistency of multiple auth header retrieval calls"""
        headers1 = auth_manager.get_auth_headers()
        headers2 = auth_manager.get_auth_headers()
        
        assert headers1 == headers2
        assert headers1["Authorization"] == headers2["Authorization"]
    
    @pytest.mark.unit
    def test_auth_manager_immutable_headers(self, auth_manager: AuthManager):
        """Test immutability of auth headers"""
        headers = auth_manager.get_auth_headers()
        original_auth = headers["Authorization"]
        
        # Modifying returned dictionary should not affect subsequent calls
        headers["Authorization"] = "modified"
        
        new_headers = auth_manager.get_auth_headers()
        assert new_headers["Authorization"] == original_auth
    
    @pytest.mark.unit
    def test_credentials_validation_edge_cases(self):
        """Test edge cases in credentials validation"""
        auth = AuthManager.__new__(AuthManager)  # Bypass __init__
        
        # Exception scenario
        auth._api_key = "valid-key-12345678"
        
        # Mock _is_valid_api_key_format to raise exception
        with patch.object(auth, '_is_valid_api_key_format', side_effect=Exception("Test error")):
            assert auth.validate_credentials() is False


class TestAuthManagerIntegration:
    """AuthManager integration tests"""
    
    @pytest.mark.unit
    def test_auth_manager_lifecycle(self):
        """Test complete lifecycle of authentication manager"""
        # 1. Create
        initial_key = "initial-api-key-12345678"
        auth = AuthManager(api_key=initial_key)
        
        # 2. Verify initial state
        assert auth.validate_credentials() is True
        assert auth.api_key == initial_key
        
        # 3. Get auth headers
        headers = auth.get_auth_headers()
        assert headers["Authorization"] == f"Bearer {initial_key}"
        
        # 4. Update API Key
        new_key = "updated-api-key-87654321"
        auth.update_api_key(new_key)
        
        # 5. Verify updated state
        assert auth.api_key == new_key
        new_headers = auth.get_auth_headers()
        assert new_headers["Authorization"] == f"Bearer {new_key}"
        
        # 6. Verify old auth headers are unaffected
        assert headers["Authorization"] == f"Bearer {initial_key}"
    
    @pytest.mark.unit
    def test_concurrent_access_simulation(self, auth_manager: AuthManager):
        """Simulate concurrent access to auth manager"""
        import threading
        import time
        
        results = []
        
        def access_auth():
            """Simulate accessing auth manager"""
            time.sleep(0.01)  # Simulate some processing time
            try:
                headers = auth_manager.get_auth_headers()
                results.append(headers["Authorization"])
            except Exception as e:
                results.append(f"Error: {e}")
        
        # Create multiple threads to access simultaneously
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=access_auth)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify all results are identical and correct
        assert len(results) == 10
        expected_auth = f"Bearer {auth_manager.api_key}"
        assert all(result == expected_auth for result in results)
