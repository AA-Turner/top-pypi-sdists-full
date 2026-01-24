"""D402 payment models for IATP protocol."""

from enum import Enum
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class PaymentScheme(str, Enum):
    """Payment schemes supported by d402."""
    EXACT = "exact"  # EIP-3009 exact payment


class D402ServicePrice(BaseModel):
    """Pricing configuration for an IATP service.
    
    Supports any ERC20 token payment with full token details.
    """
    
    # Token details
    token_address: str = Field(..., description="Token contract address (e.g., USDC, TRAIA, DAI)")
    token_symbol: str = Field(..., description="Token symbol for display")
    token_decimals: int = Field(..., description="Token decimals (6 for USDC, 18 for most)")
    
    # Price (stored in multiple formats for convenience)
    price_wei: str = Field(..., description="Price in wei/atomic units")
    price_float: float = Field(..., description="Price in token units (human-readable)")
    
    # Network configuration
    network: str = Field(..., description="Network (sepolia, base-sepolia, etc.)")
    chain_id: int = Field(..., description="Chain ID")
    
    # Optional USD equivalent (for display only)
    usd_amount: Optional[float] = Field(None, description="Approximate USD value")
    
    # Maximum timeout for payment completion
    max_timeout_seconds: int = Field(default=300, description="Max time to complete payment")


class D402Config(BaseModel):
    """Configuration for d402 payment integration in IATP.
    
    Supports per-path pricing with different tokens.
    """
    
    # Enable/disable d402 payments
    enabled: bool = Field(default=False, description="Enable d402 payments")
    
    # Payment address (utility agent contract address)
    pay_to_address: str = Field(..., description="Ethereum address to receive payments")
    
    # Pricing configuration
    # Can be per-path (e.g., {"/analyze": D402ServicePrice(...), "/extract": D402ServicePrice(...)})
    # or default for all paths
    path_prices: Dict[str, D402ServicePrice] = Field(
        default_factory=dict,
        description="Price configuration per path"
    )
    
    # Default price (used if path not in path_prices)
    default_price: Optional[D402ServicePrice] = Field(None, description="Default price for all paths")
    
    # Legacy: Pricing per service/skill (deprecated, use path_prices)
    skill_prices: Dict[str, D402ServicePrice] = Field(
        default_factory=dict, 
        description="Custom prices per skill ID (deprecated)"
    )
    
    # Facilitator configuration
    facilitator_url: str = Field(
        default="https://api.traia.io/d402/facilitator",
        description="URL of the d402 facilitator service"
    )
    
    # Custom facilitator authentication (if needed)
    facilitator_api_key: Optional[str] = Field(None, description="API key for facilitator")
    
    # Paths to gate with payments (* for all)
    protected_paths: list[str] = Field(
        default_factory=lambda: ["*"],
        description="Paths that require payment"
    )
    
    # Service description for payment prompt
    service_description: str = Field(..., description="Description shown in payment UI")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class D402PaymentInfo(BaseModel):
    """Payment information for agent card discovery."""
    
    enabled: bool = Field(..., description="Whether d402 is enabled")
    payment_schemes: list[PaymentScheme] = Field(
        default_factory=lambda: [PaymentScheme.EXACT],
        description="Supported payment schemes"
    )
    networks: list[str] = Field(..., description="Supported blockchain networks")
    default_price: D402ServicePrice = Field(..., description="Default pricing")
    facilitator_url: str = Field(..., description="Facilitator service URL")
    
    class Config:
        use_enum_values = True


class IATPSettlementRequest(BaseModel):
    """Request to settle a payment through IATP settlement layer."""
    
    consumer: str = Field(..., description="Consumer address (client agent)")
    provider: str = Field(..., description="Provider address (utility agent)")
    amount: str = Field(..., description="Amount in atomic units")
    timestamp: int = Field(..., description="Request timestamp")
    service_description: str = Field(..., description="Description of service")
    consumer_signature: str = Field(..., description="Consumer's EIP-712 signature")
    provider_signature: str = Field(..., description="Provider's attestation signature")

