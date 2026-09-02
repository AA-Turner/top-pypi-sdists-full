"""
Exception class unit tests

Tests the inheritance relationships and functionality of client exception classes
"""

import pytest

from novita_sandbox.agent_runtime.client.exceptions import (
    AgentClientError,
    AuthenticationError,
    TemplateNotFoundError,
    SandboxCreationError,
    SessionNotFoundError,
    InvocationError,
    NetworkError,
    RateLimitError,
    QuotaExceededError,
    SandboxOperationError
)


class TestExceptionHierarchy:
    """Exception inheritance relationship tests"""
    
    @pytest.mark.unit
    def test_base_exception_inheritance(self):
        """Test base exception inheritance"""
        error = AgentClientError("Test error")
        
        assert isinstance(error, Exception)
        assert isinstance(error, AgentClientError)
        assert str(error) == "Test error"
    
    @pytest.mark.unit
    def test_all_exceptions_inherit_from_base(self):
        """Test all exceptions inherit from base exception"""
        exception_classes = [
            AuthenticationError,
            TemplateNotFoundError,
            SandboxCreationError,
            SessionNotFoundError,
            InvocationError,
            NetworkError,
            RateLimitError,
            QuotaExceededError,
            SandboxOperationError
        ]
        
        for exc_class in exception_classes:
            error = exc_class("Test error")
            assert isinstance(error, AgentClientError)
            assert isinstance(error, Exception)
    
    @pytest.mark.unit
    def test_exception_inheritance_chain(self):
        """Test exception inheritance chain"""
        error = AuthenticationError("Auth failed")
        
        # Verify inheritance chain
        assert isinstance(error, AuthenticationError)
        assert isinstance(error, AgentClientError)
        assert isinstance(error, Exception)
        
        # Verify type checking
        assert type(error) == AuthenticationError
        assert issubclass(AuthenticationError, AgentClientError)
        assert issubclass(AgentClientError, Exception)


class TestAgentClientError:
    """AgentClientError base exception tests"""
    
    @pytest.mark.unit
    def test_basic_creation(self):
        """Test basic creation"""
        message = "Test error message"
        error = AgentClientError(message)
        
        assert error.message == message
        assert error.error_code is None
        assert str(error) == message
    
    @pytest.mark.unit
    def test_creation_with_error_code(self):
        """Test creation with error code"""
        message = "Test error message"
        error_code = "TEST_ERROR"
        error = AgentClientError(message, error_code)
        
        assert error.message == message
        assert error.error_code == error_code
        assert str(error) == message
    
    @pytest.mark.unit
    def test_empty_message(self):
        """Test empty error message"""
        error = AgentClientError("")
        
        assert error.message == ""
        assert str(error) == ""
    
    @pytest.mark.unit
    def test_none_error_code(self):
        """Test None error code"""
        error = AgentClientError("Test", None)
        
        assert error.error_code is None


class TestSpecificExceptions:
    """Specific exception class tests"""
    
    @pytest.mark.unit
    def test_authentication_error(self):
        """Test authentication error"""
        error = AuthenticationError("Invalid API key", "AUTH_FAILED")
        
        assert isinstance(error, AuthenticationError)
        assert isinstance(error, AgentClientError)
        assert error.message == "Invalid API key"
        assert error.error_code == "AUTH_FAILED"
    
    @pytest.mark.unit
    def test_template_not_found_error(self):
        """Test template not found error"""
        template_id = "non-existent-template"
        error = TemplateNotFoundError(f"Template {template_id} not found", "TEMPLATE_NOT_FOUND")
        
        assert isinstance(error, TemplateNotFoundError)
        assert template_id in error.message
        assert error.error_code == "TEMPLATE_NOT_FOUND"
    
    @pytest.mark.unit
    def test_sandbox_creation_error(self):
        """Test Sandbox creation error"""
        error = SandboxCreationError("Failed to create sandbox", "CREATION_FAILED")
        
        assert isinstance(error, SandboxCreationError)
        assert "create sandbox" in error.message
        assert error.error_code == "CREATION_FAILED"
    
    @pytest.mark.unit
    def test_session_not_found_error(self):
        """Test session not found error"""
        session_id = "non-existent-session"
        error = SessionNotFoundError(f"Session {session_id} not found", "SESSION_NOT_FOUND")
        
        assert isinstance(error, SessionNotFoundError)
        assert session_id in error.message
        assert error.error_code == "SESSION_NOT_FOUND"
    
    @pytest.mark.unit
    def test_invocation_error(self):
        """Test invocation error"""
        error = InvocationError("Agent execution failed", "EXECUTION_FAILED")
        
        assert isinstance(error, InvocationError)
        assert "execution failed" in error.message.lower()
        assert error.error_code == "EXECUTION_FAILED"
    
    @pytest.mark.unit
    def test_network_error(self):
        """Test network error"""
        error = NetworkError("Connection timeout", "NETWORK_TIMEOUT")
        
        assert isinstance(error, NetworkError)
        assert "timeout" in error.message.lower()
        assert error.error_code == "NETWORK_TIMEOUT"
    
    @pytest.mark.unit
    def test_rate_limit_error(self):
        """Test rate limit error"""
        error = RateLimitError("Rate limit exceeded", "RATE_LIMIT_EXCEEDED")
        
        assert isinstance(error, RateLimitError)
        assert "rate limit" in error.message.lower()
        assert error.error_code == "RATE_LIMIT_EXCEEDED"
    
    @pytest.mark.unit
    def test_quota_exceeded_error(self):
        """Test quota exceeded error"""
        error = QuotaExceededError("Monthly quota exceeded", "QUOTA_EXCEEDED")
        
        assert isinstance(error, QuotaExceededError)
        assert "quota" in error.message.lower()
        assert error.error_code == "QUOTA_EXCEEDED"
    
    @pytest.mark.unit
    def test_sandbox_operation_error(self):
        """Test Sandbox operation error"""
        error = SandboxOperationError("Failed to pause sandbox", "OPERATION_FAILED")
        
        assert isinstance(error, SandboxOperationError)
        assert "sandbox" in error.message.lower()
        assert error.error_code == "OPERATION_FAILED"


class TestExceptionCatching:
    """Exception catching tests"""
    
    @pytest.mark.unit
    def test_catch_specific_exception(self):
        """Test catching specific exception"""
        with pytest.raises(AuthenticationError) as exc_info:
            raise AuthenticationError("Auth failed")
        
        assert exc_info.value.message == "Auth failed"
        assert isinstance(exc_info.value, AuthenticationError)
        assert isinstance(exc_info.value, AgentClientError)
    
    @pytest.mark.unit
    def test_catch_base_exception(self):
        """Test catching base exception"""
        with pytest.raises(AgentClientError) as exc_info:
            raise TemplateNotFoundError("Template not found")
        
        assert isinstance(exc_info.value, TemplateNotFoundError)
        assert isinstance(exc_info.value, AgentClientError)
    
    @pytest.mark.unit
    def test_catch_multiple_exception_types(self):
        """Test catching multiple exception types"""
        exceptions_to_test = [
            AuthenticationError("Auth error"),
            NetworkError("Network error"),
            InvocationError("Invocation error")
        ]
        
        for exc in exceptions_to_test:
            with pytest.raises(AgentClientError) as exc_info:
                raise exc
            
            assert isinstance(exc_info.value, type(exc))
            assert isinstance(exc_info.value, AgentClientError)
    
    @pytest.mark.unit
    def test_exception_distinction(self):
        """Test exception distinction"""
        auth_error = AuthenticationError("Auth failed")
        network_error = NetworkError("Network failed")
        
        # They are both AgentClientError, but different types
        assert isinstance(auth_error, AgentClientError)
        assert isinstance(network_error, AgentClientError)
        assert type(auth_error) != type(network_error)
        assert not isinstance(auth_error, NetworkError)
        assert not isinstance(network_error, AuthenticationError)


class TestExceptionProperties:
    """Exception property tests"""
    
    @pytest.mark.unit
    def test_exception_message_property(self):
        """Test exception message property"""
        message = "Detailed error message"
        error = AgentClientError(message)
        
        assert error.message == message
        assert str(error) == message
        assert repr(error)  # Ensure repr doesn't error
    
    @pytest.mark.unit
    def test_exception_error_code_property(self):
        """Test exception error code property"""
        error_code = "SPECIFIC_ERROR_CODE"
        error = AgentClientError("Error", error_code)
        
        assert error.error_code == error_code
    
    @pytest.mark.unit
    def test_exception_args_compatibility(self):
        """Test exception args compatibility"""
        message = "Test message"
        error = AgentClientError(message)
        
        # Verify args property (Python standard exception interface)
        assert error.args == (message,)
        assert len(error.args) == 1
        assert error.args[0] == message
    
    @pytest.mark.unit
    def test_exception_with_different_message_types(self):
        """Test exception with different message types"""
        # String message
        str_error = AgentClientError("String message")
        assert str_error.message == "String message"
        
        # None message (though not recommended)
        none_error = AgentClientError(None)
        assert none_error.message is None


class TestExceptionIntegration:
    """Exception integration tests"""
    
    @pytest.mark.unit
    def test_exception_in_try_except_chains(self):
        """Test exception behavior in try-except chains"""
        def raise_auth_error():
            raise AuthenticationError("Auth failed", "AUTH_ERROR")
        
        def raise_network_error():
            raise NetworkError("Network failed", "NETWORK_ERROR")
        
        # Test specific exception catching
        with pytest.raises(AuthenticationError):
            raise_auth_error()
        
        # Test base class exception catching
        with pytest.raises(AgentClientError):
            raise_network_error()
        
        # Test exception chain
        with pytest.raises(NetworkError) as exc_info:
            try:
                raise_auth_error()
            except AuthenticationError as e:
                assert e.error_code == "AUTH_ERROR"
                # Re-raise as different exception type
                raise NetworkError(f"Network issue caused by: {e.message}")
        
        # Verify chained exception information
        assert "Network issue caused by: Auth failed" in str(exc_info.value)
    
    @pytest.mark.unit
    def test_exception_information_preservation(self):
        """Test exception information preservation"""
        original_message = "Original error message"
        original_code = "ORIGINAL_CODE"
        
        # Create exception
        error = InvocationError(original_message, original_code)
        
        # Verify information preservation
        assert error.message == original_message
        assert error.error_code == original_code
        assert str(error) == original_message
        
        # Re-raise and catch
        with pytest.raises(InvocationError) as exc_info:
            raise error
        
        caught_error = exc_info.value
        assert caught_error.message == original_message
        assert caught_error.error_code == original_code
        assert caught_error is error  # Same object
