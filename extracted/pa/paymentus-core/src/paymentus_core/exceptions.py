"""
Exceptions for Paymentus API
"""
from typing import Any, Dict, Optional


class BaseError(Exception):
    """Base exception for Paymentus API errors"""
    def __init__(
        self, 
        message: str, 
        code: Optional[str] = None, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
        
    def __str__(self) -> str:
        if self.code:
            return f"{self.code}: {self.message}"
        return self.message


class NetworkError(BaseError):
    """Network-related error"""
    pass


class APIError(BaseError):
    """API error"""
    pass


class RateLimitError(APIError):
    """Rate limit exceeded error"""
    pass


class ServerError(APIError):
    """Server error (5xx)"""
    pass