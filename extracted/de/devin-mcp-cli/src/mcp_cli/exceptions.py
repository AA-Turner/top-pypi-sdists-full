"""Exceptions for MCP CLI."""


class ToolExecutionError(Exception):
    """
    Exception raised when a tool returns an error in the result.
    """
    pass


# OAuth-specific exceptions
class MCPOAuthError(Exception):
    """Base exception for MCP OAuth errors."""
    pass


class NotOAuthCompliantError(MCPOAuthError):
    """Raised when server doesn't support OAuth."""
    pass


class OAuthDiscoveryError(MCPOAuthError):
    """Raised when OAuth discovery fails."""
    pass


class OAuthClientRegistrationError(MCPOAuthError):
    """Raised when client registration fails."""
    pass


class OAuthAuthorizationError(MCPOAuthError):
    """Raised during authorization phase."""
    pass


class OAuthTokenExchangeError(MCPOAuthError):
    """Raised when token exchange fails."""
    pass


def extract_exception_details(exception: Exception | BaseExceptionGroup[Exception]) -> str:
    """
    Extract detailed error information from an exception, including unwrapping ExceptionGroup.
    
    Args:
        exception: The exception to extract details from
        
    Returns:
        A detailed error message string
    """
    # Handle ExceptionGroup by extracting underlying exceptions
    if isinstance(exception, ExceptionGroup):
        error_details = []
        for i, exc in enumerate(exception.exceptions):
            exc_type = type(exc).__name__
            exc_msg = str(exc)
            error_details.append(f"  [{i+1}] {exc_type}: {exc_msg}")
        
        base_msg = f"{type(exception).__name__} with {len(exception.exceptions)} exception(s):"
        return base_msg + "\n" + "\n".join(error_details)
    
    # Handle regular exceptions
    return f"{type(exception).__name__}: {str(exception)}"