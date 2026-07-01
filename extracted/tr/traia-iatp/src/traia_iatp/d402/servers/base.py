"""Base classes and utilities for d402 server middleware.

This module provides shared functionality used across different server framework
implementations.
"""

import logging
from typing import Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class PaymentMode(Enum):
    """Payment mode for a request."""
    FREE_WITH_API_KEY = "free_with_api_key"  # Client has valid API key
    PAID_WITH_SERVER_KEY = "paid_with_server_key"  # Client paid, server uses internal key
    NO_PAYMENT = "no_payment"  # No payment required


class BasePaymentConfig:
    """Base configuration for payment-enabled servers.
    
    This class provides common configuration used across all server frameworks.
    """
    
    def __init__(
        self,
        server_address: str,
        requires_auth: bool = False,
        internal_api_key: Optional[str] = None,
        testing_mode: bool = False,
        facilitator_url: Optional[str] = None,
        facilitator_api_key: Optional[str] = None,
        server_name: Optional[str] = None
    ):
        """Initialize payment configuration.
        
        Args:
            server_address: Address where payments should be sent
            requires_auth: Whether server accepts API keys for free access
            internal_api_key: Server's internal API key (used when client pays)
            testing_mode: If True, skip facilitator verification
            facilitator_url: URL of the payment facilitator
            facilitator_api_key: API key for facilitator authentication
            server_name: Name/ID of this server for tracking
        """
        self.server_address = server_address
        self.requires_auth = requires_auth
        self.internal_api_key = internal_api_key
        self.testing_mode = testing_mode
        self.facilitator_url = facilitator_url
        self.facilitator_api_key = facilitator_api_key
        self.server_name = server_name
        
        self.validate()
    
    def validate(self):
        """Validate configuration."""
        if not self.server_address:
            raise ValueError("server_address is required")
        
        if not self.testing_mode and not self.facilitator_url:
            raise ValueError("facilitator_url required when testing_mode is False")


def extract_api_key_from_headers(headers: Dict[str, str]) -> Optional[str]:
    """Extract API key from request headers.
    
    Supports Authorization header (with or without Bearer prefix) and X-API-KEY header.
    
    Args:
        headers: Request headers (dict or Headers object)
        
    Returns:
        API key string if found, None otherwise
    """
    # Authorization header - strip "Bearer " prefix if present
    auth = headers.get("authorization") or headers.get("Authorization", "")
    if auth:
        if auth.lower().startswith("bearer "):
            return auth[7:].strip()
        else:
            return auth.strip()
    
    # X-API-KEY header
    api_key = headers.get("x-api-key") or headers.get("X-API-KEY", "")
    if api_key:
        return api_key.strip()
    
    return None


def log_payment_verification_start(tool_name: str, has_auth: bool, payment_header_present: bool):
    """Log start of payment verification process.
    
    Args:
        tool_name: Name of the tool/endpoint being called
        has_auth: Whether client has API key
        payment_header_present: Whether payment header is present
    """
    if has_auth:
        logger.info(f"✅ {tool_name}: Client authenticated with API key (Mode 1: Free)")
    elif payment_header_present:
        logger.info(f"💰 {tool_name}: Payment header RECEIVED - validating...")
    else:
        logger.info(f"💰 {tool_name}: Payment required (Mode 2) - HTTP 402")


def log_payment_validation_success(
    tool_name: str,
    payment_amount: int,
    required_amount: int,
    from_address: str,
    to_address: str
):
    """Log successful payment validation.
    
    Args:
        tool_name: Name of the tool/endpoint
        payment_amount: Amount paid
        required_amount: Amount required
        from_address: Payer address
        to_address: Payee address
    """
    logger.info(f"✅ {tool_name}: Payment VERIFIED successfully (Mode 2: Paid)")
    logger.info(f"   Payment amount: {payment_amount} wei (required: {required_amount} wei)")
    logger.info(f"   From (wallet): {from_address}")
    logger.info(f"   To (provider): {to_address}")


__all__ = [
    "PaymentMode",
    "BasePaymentConfig",
    "extract_api_key_from_headers",
    "log_payment_verification_start",
    "log_payment_validation_success",
]

