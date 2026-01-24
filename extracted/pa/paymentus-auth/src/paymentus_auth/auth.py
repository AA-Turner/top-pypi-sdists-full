"""
Authentication module for Paymentus API
"""
from datetime import datetime
import os
import uuid
from enum import Enum, auto
from typing import Dict, List, Optional, Union, Any, Literal

import jwt
import requests
from pydantic import BaseModel, Field

from .errors import ConfigurationError, TokenError, NetworkError
from .version import LIB_VERSION

# Define pixel types as an enumeration
class PixelType(str, Enum):
    """Enumeration of allowed pixel types"""
    TOKENIZATION = "tokenization-pixel"
    LIST_WALLETS = "list-wallets-pixel"
    USER_CHECKOUT = "user-checkout-pixel"
    GUEST_CHECKOUT = "guest-checkout-pixel"
    USER_AUTOPAY = "user-autopay-pixel"
    LIST_AUTOPAY = "list-autopay-pixel"

# Pixel scope mappings (matching TypeScript implementation)
PIXEL_SCOPE_MAP = {
    PixelType.TOKENIZATION: ["xotp:profile"],
    PixelType.LIST_WALLETS: ["xotp:profile", "xotp:listProfiles", "xotp:profile:delete"],
    PixelType.USER_CHECKOUT: ["xotp:profile", "xotp:payment", "xotp:listProfiles", "xotp:listAccounts", "xotp:profile:delete"],
    PixelType.GUEST_CHECKOUT: ["xotp:payment", "xotp:listAccounts", "xotp:profile"],
    PixelType.USER_AUTOPAY: ["xotp:profile", "xotp:autopay", "xotp:listProfiles", "xotp:listAccounts", "xotp:profile:delete", "xotp:payment"],
    PixelType.LIST_AUTOPAY: ["xotp:profile", "xotp:autopay", "xotp:listProfiles", "xotp:listAccounts", "xotp:profile:delete", "xotp:payment", "xotp:autopay:delete"]
}

# Pixel claim requirements (matching TypeScript implementation)
PIXEL_CLAIM_REQUIREMENTS = {
    PixelType.TOKENIZATION: {},
    PixelType.LIST_WALLETS: {"userLogin": True},
    PixelType.USER_CHECKOUT: {"userLogin": True, "paymentsData": True, "pmTokens": False},
    PixelType.GUEST_CHECKOUT: {"paymentsData": True},
    PixelType.USER_AUTOPAY: {"userLogin": True, "paymentsData": True, "pmTokens": False},
    PixelType.LIST_AUTOPAY: {"userLogin": True, "paymentsData": True}
}


class PaymentData(BaseModel):
    """Payment data structure"""
    accountNumber: str
    convFeeState: Optional[str] = None
    convFeeCountry: Optional[str] = None


class JwtPayload(BaseModel):
    """JWT payload structure"""
    iss: str = Field(..., description="Issuer (three-letter acronym)")
    iat: int = Field(..., description="Issued at timestamp")
    requestedScope: List[str] = Field([], description="Requested scopes")
    aud: Optional[str] = Field(None, description="Audience (optional)")
    userLogin: Optional[str] = Field(None, description="User login (optional)")
    pmToken: Optional[List[str]] = Field(None, description="Payment method tokens (optional)")
    paymentsData: Optional[List[PaymentData]] = Field(None, description="Payments data (optional, serialized PaymentData objects)")


class AuthConfig(BaseModel):
    """Authentication configuration for Paymentus API"""
    base_url: str
    pre_shared_key: str
    tla: str
    scope: Optional[List[str]] = []
    pixels: Optional[List[PixelType]] = []
    user_login: Optional[str] = None
    payments_data: Optional[List[PaymentData]] = None
    pm_token: Optional[List[str]] = None
    aud: Optional[str] = None
    kid: Optional[str] = "001"
    timeout: int = 5000
    session: Optional[Dict[str, str]] = None


class TokenResponse(BaseModel):
    """Token response from API"""
    token: str
    exp: int


class Auth:
    """Authentication handler for Paymentus API"""
    def __init__(self, config: AuthConfig):
        """Initialize with auth configuration

        Args:
            config: Auth configuration object
        """
        self._validate_config(config)
        self.config = self._process_config(config)
        self.current_token = None
        self.token_expiry = None

    def _process_config(self, config: AuthConfig) -> AuthConfig:
        """Process configuration and add required scopes from pixels"""
        # Start with provided scopes
        final_scopes = config.scope or []

        # Add scopes from pixels if provided
        if config.pixels:
            pixel_scopes = []
            for pixel in config.pixels:
                if pixel in PIXEL_SCOPE_MAP:
                    pixel_scopes.extend(PIXEL_SCOPE_MAP[pixel])
            
            # Remove duplicates
            final_scopes = list(set(final_scopes + pixel_scopes))
        
         # Handle pmToken for guest-checkout-pixel
        final_pm_token = config.pm_token or []
        if config.pixels and PixelType.GUEST_CHECKOUT in config.pixels:
            # Always override pmToken with ["anonymousPMOnly"] for guest-checkout-pixel
            final_pm_token = ["anonymousPMOnly"]
            
        config.pm_token = final_pm_token
        config.scope = final_scopes
        return config

    def _validate_config(self, config: AuthConfig) -> None:
        """Validate the configuration is complete"""
        if not config.base_url or not config.base_url.strip():
            raise ConfigurationError("Invalid base_url")
        if not config.pre_shared_key or not config.pre_shared_key.strip():
            raise ConfigurationError("Invalid pre_shared_key")
        if not config.tla or not config.tla.strip():
            raise ConfigurationError("Invalid tla")
        if not config.scope and not config.pixels:
            raise ConfigurationError("At least one scope or pixel is required")
        
        # Validate pixel claim requirements
        if config.pixels:
            for pixel in config.pixels:
                requirements = PIXEL_CLAIM_REQUIREMENTS.get(pixel, {})
                if requirements.get("userLogin") and not config.user_login:
                    raise ConfigurationError(f"user_login is required for {pixel}")
                if requirements.get("paymentsData") and not config.payments_data:
                    raise ConfigurationError(f"payments_data is required for {pixel}")
                # For guest-checkout-pixel, pmToken will be automatically set to ["anonymousPMOnly"]
                # For other pixels that require pmTokens, check if pmToken is provided
                if requirements.get("pmTokens") and pixel != PixelType.GUEST_CHECKOUT and not config.pm_token:
                    raise ConfigurationError(f"pm_token is required for {pixel}")

    def _create_jwt_payload(self) -> Dict:
        """Create JWT payload for token request"""
        now = int(datetime.now().timestamp())
        payload = {
            "iss": self.config.tla,
            "iat": now,
            "requestedScope": self.config.scope or []
        }
        
        # Add optional fields if provided
        if self.config.aud:
            payload["aud"] = self.config.aud
            
        if self.config.user_login:
            payload["userLogin"] = self.config.user_login
            
        if self.config.pm_token:
            payload["pmToken"] = self.config.pm_token
            
        if self.config.payments_data:
            # Convert Pydantic models to dictionaries for JSON serialization
            payload["paymentsData"] = [payment_data.model_dump() for payment_data in self.config.payments_data]
            
        return payload

    def _sign_jwt(self, payload: Dict) -> str:
        """Sign JWT with provided key"""
        try:
            signed_jwt = jwt.encode(
                payload=payload,
                key=self.config.pre_shared_key,
                algorithm="HS256",
                headers={
                    "kid": self.config.kid or "001",
                    "alg": "HS256",
                    "typ": "JWT"
                }
            )
            return signed_jwt
        except Exception as e:
            raise TokenError(f"Failed to sign JWT: {str(e)}") from e

    async def fetch_token(self) -> str:
        """Fetch a token from the authentication server"""
        try:
            payload = self._create_jwt_payload()
            signed_jwt = self._sign_jwt(payload)
            
            # Create session ID if not provided
            session_id = self.config.session.get("id") if self.config.session else str(uuid.uuid4())
            
            headers = {
                "Content-Type": "application/json",
                "X-Ext-Session-Id": session_id,
                "X-Ext-Session-App": f"auth-sdk@{LIB_VERSION}"
            }
            
            url = f"{self.config.base_url.rstrip('/')}/api/token/{self.config.tla}"
            
            response = requests.post(
                url,
                json={"jwt": signed_jwt},
                headers=headers,
                timeout=self.config.timeout / 1000,  # Convert from ms to seconds
                # verify=False, # TODO: Remove this once development is complete
            )
                
            response.raise_for_status()
            data = response.json()
            
            if not data.get("token"):
                raise TokenError("Invalid token response")
                
            self.current_token = data["token"]
            self.token_expiry = data["exp"]
            
            return self.current_token
            
        except requests.RequestException as e:
            raise NetworkError(f"Network error: {str(e)}") from e
        except Exception as e:
            if isinstance(e, TokenError):
                raise
            raise TokenError(f"Failed to fetch token: {str(e)}") from e

    def get_current_token(self) -> Optional[str]:
        """Get the current token if available"""
        return self.current_token

    def is_token_expired(self) -> bool:
        """Check if the current token is expired"""
        if not self.token_expiry:
            return True
        return datetime.now().timestamp() >= self.token_expiry 