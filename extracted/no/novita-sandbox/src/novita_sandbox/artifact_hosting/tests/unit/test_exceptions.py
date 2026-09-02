"""Unit tests for exception classes."""

import pytest

from novita_sandbox.artifact_hosting.exceptions import (
    DeploymentError,
    DeploymentNotFoundError,
    ProjectNotFoundError,
    QuotaExceededError,
    RollbackError,
)


class TestDeploymentError:
    """Tests for DeploymentError base class."""
    
    def test_deployment_error_with_message(self):
        """Test that DeploymentError can be created with message."""
        error = DeploymentError("Something went wrong")
        assert str(error) == "Something went wrong"
        assert error.code is None
    
    def test_deployment_error_with_code(self):
        """Test that DeploymentError can be created with code."""
        error = DeploymentError("Something went wrong", code="ERROR_CODE")
        assert str(error) == "Something went wrong"
        assert error.code == "ERROR_CODE"
    
    def test_deployment_error_is_exception(self):
        """Test that DeploymentError is an Exception."""
        error = DeploymentError("Error")
        assert isinstance(error, Exception)


class TestProjectNotFoundError:
    """Tests for ProjectNotFoundError."""
    
    def test_project_not_found_error(self):
        """Test that ProjectNotFoundError can be created."""
        error = ProjectNotFoundError("Project not found")
        assert str(error) == "Project not found"
        assert isinstance(error, DeploymentError)
        assert isinstance(error, Exception)


class TestDeploymentNotFoundError:
    """Tests for DeploymentNotFoundError."""
    
    def test_deployment_not_found_error(self):
        """Test that DeploymentNotFoundError can be created."""
        error = DeploymentNotFoundError("Deployment not found")
        assert str(error) == "Deployment not found"
        assert isinstance(error, DeploymentError)
        assert isinstance(error, Exception)


class TestRollbackError:
    """Tests for RollbackError."""
    
    def test_rollback_error(self):
        """Test that RollbackError can be created."""
        error = RollbackError("Rollback failed")
        assert str(error) == "Rollback failed"
        assert isinstance(error, DeploymentError)
        assert isinstance(error, Exception)


class TestQuotaExceededError:
    """Tests for QuotaExceededError."""
    
    def test_quota_exceeded_error(self):
        """Test that QuotaExceededError can be created."""
        error = QuotaExceededError("Quota exceeded")
        assert str(error) == "Quota exceeded"
        assert isinstance(error, DeploymentError)
        assert isinstance(error, Exception)


class TestExceptionHierarchy:
    """Tests for exception hierarchy."""
    
    def test_all_exceptions_inherit_from_deployment_error(self):
        """Test that all specific exceptions inherit from DeploymentError."""
        exceptions = [
            ProjectNotFoundError("test"),
            DeploymentNotFoundError("test"),
            RollbackError("test"),
            QuotaExceededError("test"),
        ]
        
        for exc in exceptions:
            assert isinstance(exc, DeploymentError)
            assert isinstance(exc, Exception)
    
    def test_catch_all_deployment_errors(self):
        """Test that catching DeploymentError catches all specific errors."""
        exceptions = [
            ProjectNotFoundError("test"),
            DeploymentNotFoundError("test"),
            RollbackError("test"),
            QuotaExceededError("test"),
        ]
        
        for exc in exceptions:
            try:
                raise exc
            except DeploymentError:
                # Should catch all specific exceptions
                pass
            except Exception:
                pytest.fail(f"Exception {type(exc)} should be caught by DeploymentError")
