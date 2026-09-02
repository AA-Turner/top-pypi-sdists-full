"""
Test script for error handling and retry logic.

This script tests the error classification and retry behavior without
making actual API calls.
"""

from matrx_ai.providers.errors import (
    classify_google_error,
    classify_openai_error,
    classify_anthropic_error,
    classify_provider_error,
)


def test_google_503_high_demand():
    """Test Google 503 high demand error classification.

    A bare Exception carrying the code in its message (no SDK type / status
    attribute) lands in the string fallback, which classifies any 5xx /
    'unavailable' as a retryable server_error.
    """
    error = Exception(
        "503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}"
    )

    result = classify_google_error(error)

    assert result.error_type == "server_error"
    assert result.status_code == 503
    assert result.is_retryable == True
    assert result.retry_after == 5.0
    print("✓ Google 503 high demand: PASS")


def test_google_429_rate_limit():
    """Test Google 429 rate limit error classification."""
    error = Exception("429 RESOURCE_EXHAUSTED: Rate limit exceeded")
    
    result = classify_google_error(error)
    
    assert result.error_type == "rate_limit"
    assert result.status_code == 429
    assert result.is_retryable == True
    assert result.retry_after == 10.0
    print("✓ Google 429 rate limit: PASS")


def test_google_500_server_error():
    """Test Google 500 server error classification."""
    error = Exception("500 INTERNAL: Internal server error")
    
    result = classify_google_error(error)

    assert result.error_type == "server_error"
    assert result.status_code == 500
    assert result.is_retryable == True
    assert result.retry_after == 5.0
    print("✓ Google 500 server error: PASS")


def test_google_network_error():
    """Test network/timeout error classification.

    'Connection timeout' contains 'timeout', so the fallback classifies it as a
    retryable provider_timeout (the timeout check precedes the connection one).
    """
    error = Exception("Connection timeout: Failed to connect to API")

    result = classify_google_error(error)

    assert result.error_type == "provider_timeout"
    assert result.is_retryable == True
    assert result.retry_after == 10.0
    print("✓ Google network/timeout error: PASS")


def test_google_connection_error():
    """A pure connection failure (no 'timeout') classifies as connection_error."""
    error = Exception("Connection refused: network unreachable")

    result = classify_google_error(error)

    assert result.error_type == "connection_error"
    assert result.is_retryable == True
    assert result.retry_after == 3.0
    print("✓ Google connection error: PASS")


def test_google_non_retryable():
    """Test non-retryable (bad request) error classification."""
    error = Exception("400 INVALID_ARGUMENT: Invalid request")

    result = classify_google_error(error)

    assert result.error_type == "invalid_request"
    assert result.is_retryable == False
    print("✓ Google non-retryable error: PASS")


def test_openai_rate_limit():
    """Test OpenAI rate limit error classification."""
    error = Exception("429 Rate limit exceeded")
    
    result = classify_openai_error(error)
    
    assert result.error_type == "rate_limit"
    assert result.is_retryable == True
    print("✓ OpenAI rate limit: PASS")


def test_openai_server_error():
    """Test OpenAI server error classification."""
    error = Exception("503 Service temporarily unavailable")
    
    result = classify_openai_error(error)
    
    assert result.error_type == "server_error"
    assert result.is_retryable == True
    print("✓ OpenAI server error: PASS")


def test_anthropic_overloaded():
    """Test Anthropic overloaded error classification."""
    error = Exception("529 Overloaded: The API is currently overloaded")
    
    result = classify_anthropic_error(error)

    assert result.error_type == "provider_overloaded"
    assert result.status_code == 529
    assert result.is_retryable == True
    print("✓ Anthropic overloaded: PASS")


def test_backoff_calculation():
    """Test exponential backoff calculation."""
    from matrx_ai.providers.errors import RetryableError
    
    error = RetryableError(
        error_type="test",
        message="test",
        is_retryable=True
    )
    
    # Test exponential backoff: 1s, 2s, 4s, 8s, 16s, 30s (capped)
    assert error.get_backoff_delay(0) == 1
    assert error.get_backoff_delay(1) == 2
    assert error.get_backoff_delay(2) == 4
    assert error.get_backoff_delay(3) == 8
    assert error.get_backoff_delay(4) == 16
    assert error.get_backoff_delay(5) == 30  # Capped at 30s
    assert error.get_backoff_delay(10) == 30  # Still capped
    
    print("✓ Backoff calculation: PASS")


def test_custom_retry_after():
    """Test custom retry_after override."""
    from matrx_ai.providers.errors import RetryableError
    
    error = RetryableError(
        error_type="test",
        message="test",
        retry_after=15.0,
        is_retryable=True
    )
    
    # Should always return custom retry_after
    assert error.get_backoff_delay(0) == 15.0
    assert error.get_backoff_delay(5) == 15.0
    
    print("✓ Custom retry_after: PASS")


def test_provider_classification():
    """Test generic provider classification."""
    error = Exception("503 Service Unavailable")
    
    # Test with unknown provider
    result = classify_provider_error("unknown", error)
    assert result.is_retryable == True
    assert result.error_type == "server_error"
    
    # Test with Google provider - 503 alone is classified as server_error
    # (rate_limit_high_demand requires "high demand" in message)
    error_generic = Exception("500 Internal error")
    result = classify_provider_error("google", error_generic)
    assert result.error_type == "server_error"
    
    print("✓ Provider classification: PASS")


def run_all_tests():
    """Run all error handling tests."""
    print("\n" + "="*60)
    print("Testing Error Handling System")
    print("="*60 + "\n")
    
    try:
        test_google_503_high_demand()
        test_google_429_rate_limit()
        test_google_500_server_error()
        test_google_network_error()
        test_google_connection_error()
        test_google_non_retryable()
        test_openai_rate_limit()
        test_openai_server_error()
        test_anthropic_overloaded()
        test_backoff_calculation()
        test_custom_retry_after()
        test_provider_classification()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60 + "\n")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}\n")
        raise


if __name__ == "__main__":
    run_all_tests()
