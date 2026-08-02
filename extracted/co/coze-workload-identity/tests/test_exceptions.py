"""Tests for custom exceptions."""

import unittest

from coze_workload_identity.exceptions import (
    WorkloadIdentityError,
    ConfigurationError,
    TokenExchangeError,
    TokenRetrievalError
)


class TestExceptions(unittest.TestCase):
    """Test cases for custom exceptions."""

    def test_workload_identity_error(self):
        """Test base WorkloadIdentityError."""
        error = WorkloadIdentityError("Test error")
        self.assertEqual(str(error), "Test error")
        self.assertIsInstance(error, Exception)

    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError("Missing config")
        self.assertEqual(str(error), "Missing config")
        self.assertIsInstance(error, WorkloadIdentityError)

    def test_token_exchange_error(self):
        """Test TokenExchangeError."""
        error = TokenExchangeError("Exchange failed")
        self.assertEqual(str(error), "Exchange failed")
        self.assertIsInstance(error, WorkloadIdentityError)

    def test_token_retrieval_error(self):
        """Test TokenRetrievalError."""
        error = TokenRetrievalError("Retrieval failed")
        self.assertEqual(str(error), "Retrieval failed")
        self.assertIsInstance(error, WorkloadIdentityError)


if __name__ == '__main__':
    unittest.main()