"""
Authentication Manager

Manages client authentication using API Key for Bearer Token authentication
"""

import os
import re
from typing import Dict, Optional

from .exceptions import AuthenticationError, AccessDeniedException


class AuthManager:
    """Authentication Manager - AWS Agentcore compatible, API Key only
    
    Supports API Key authentication only, compatible with AWS Agentcore style.
    No OAuth or other complex authentication methods.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize authentication manager
        
        Args:
            api_key: API key, if not provided it will be read from environment variable NOVITA_API_KEY
            
        Raises:
            AuthenticationError: Raised when API Key is not provided and environment variable does not exist
        """
        # Distinguish between None and empty string: use environment variable when None, use directly when empty string
        if api_key is None:
            self._api_key = os.getenv("NOVITA_API_KEY")
        else:
            self._api_key = api_key
        
        if not self._api_key:
            raise AuthenticationError(
                "API Key is required. Please provide it directly or set the NOVITA_API_KEY environment variable."
            )
        
        # Validate API Key format
        if not self._is_valid_api_key_format(self._api_key):
            raise AuthenticationError(
                "Invalid API Key format. API Key should be a non-empty string."
            )
    
    def _is_valid_api_key_format(self, api_key: str) -> bool:
        """Validate API Key format
        
        Args:
            api_key: API Key to validate
            
        Returns:
            Whether the API Key format is valid
        """
        if not api_key or not isinstance(api_key, str):
            return False
        
        # Basic validation: non-empty and reasonable length
        if len(api_key.strip()) < 8:
            return False
        
        # Additional validation rules can be added based on actual API Key format
        # For example: specific prefix, length, character set, etc.
        return True
    
    def validate_credentials(self) -> bool:
        """Validate credential validity (AWS Agentcore compatible)
        
        Returns:
            Whether credentials are valid (checks if API Key exists and format is correct)
        """
        try:
            return bool(self._api_key and self._is_valid_api_key_format(self._api_key))
        except Exception:
            return False
    
    def validate_access(self) -> None:
        """Validate access permissions (AWS Agentcore compatible)
        
        Raises:
            AccessDeniedException: When access is denied
            AuthenticationError: When authentication fails
        """
        if not self.validate_credentials():
            raise AuthenticationError("Invalid or missing API Key")
        
        # Additional access validation can be added here
        # For now, we assume API Key validation is sufficient
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers (AWS Agentcore compatible)
        
        Returns:
            Authentication header dictionary containing Bearer Token
            
        Example:
            {"Authorization": "Bearer your-api-key"}
        """
        self.validate_access()  # Use AWS-style validation
        
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "User-Agent": "novita-agentRuntime-Client/1.0"
        }
    
    @property
    def api_key(self) -> str:
        """Get current API Key"""
        if not self._api_key:
            raise AuthenticationError("API Key not available")
        return self._api_key
    
    def update_api_key(self, new_api_key: str) -> None:
        """Update API Key
        
        Args:
            new_api_key: New API Key
            
        Raises:
            AuthenticationError: Raised when new API Key format is invalid
        """
        if not self._is_valid_api_key_format(new_api_key):
            raise AuthenticationError("Invalid API Key format")
        
        self._api_key = new_api_key