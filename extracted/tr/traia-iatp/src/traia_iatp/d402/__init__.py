"""D402 payment integration for IATP protocol.

This module provides d402 (HTTP 402 Payment Required) payment capabilities
for the Inter-Agent Transfer Protocol (IATP). It enables utility agents to
accept payments and client agents to send payments for API access.

Components:
- middleware: FastAPI middleware for accepting d402 payments
- client: d402 client integration for sending payments
- facilitator: Custom facilitator that interfaces with IATPSettlementLayer
- models: Payment configuration models
"""

from .models import (
    D402Config,
    D402PaymentInfo,
    D402ServicePrice,
    PaymentScheme,
)
from .servers import require_payment, D402PaymentMiddleware
from .asgi_wrapper import D402ASGIWrapper
from .client import D402IATPClient
from .facilitator import IATPSettlementFacilitator
from .mcp_middleware import (
    EndpointPaymentInfo,
    get_active_api_key,
    require_payment_for_tool,
    settle_payment
)
from .clients.httpx import d402_payment_hooks, d402HttpxClient
from .clients.base import decode_x_payment_response
from .price_builder import D402PriceBuilder

__all__ = [
    "D402Config",
    "D402PaymentInfo",
    "D402ServicePrice",
    "PaymentScheme",
    "require_payment",
    "D402PaymentMiddleware",
    "D402ASGIWrapper",
    "D402IATPClient",
    "IATPSettlementFacilitator",
    "EndpointPaymentInfo",
    "get_active_api_key",
    "require_payment_for_tool",
    "settle_payment",
    "d402_payment_hooks",
    "d402HttpxClient",
    "decode_x_payment_response",
    # Price builder helper
    "D402PriceBuilder",
]

