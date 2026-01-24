"""
Example: General-purpose API server with D402 payment support.

This example shows how to use the @require_payment decorator for a 
custom FastAPI server with multiple endpoints at different prices.

This is the same pattern as MCP servers, just generalized for any endpoint!
"""

import os
from fastapi import FastAPI, Request
import uvicorn

from traia_iatp.d402.servers import (
    D402PaymentMiddleware,
    require_payment,
    extract_payment_configs
)
from traia_iatp.d402 import D402PriceBuilder

# Initialize FastAPI app
app = FastAPI(title="Paid Analysis API")

# Get configuration from environment
SERVER_ADDRESS = os.getenv("SERVER_ADDRESS", "0x1234567890123456789012345678901234567890")
NETWORK = os.getenv("NETWORK", "sepolia")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS", "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238")
TOKEN_DECIMALS = int(os.getenv("TOKEN_DECIMALS", "6"))
TOKEN_SYMBOL = os.getenv("TOKEN_SYMBOL", "USDC")

# Create price builder - works with ANY token!
# Just pass your token configuration from environment
price_builder = D402PriceBuilder(
    token_address=TOKEN_ADDRESS,
    token_decimals=TOKEN_DECIMALS,
    network=NETWORK,
    token_symbol=TOKEN_SYMBOL
)

# ============================================================================
# API ENDPOINTS - Different prices for different operations
# ============================================================================

@app.post("/quick-check")
@require_payment(
    price=price_builder.create_price(0.001),  # $0.001 - uses builder!
    endpoint_path="/quick-check",
    description="Quick health check of data"
)
async def quick_check(request: Request, data: dict):
    """Cheap, fast check - only $0.001"""
    return {"status": "ok", "data_quality": "good"}


@app.post("/analyze")
@require_payment(
    price=price_builder.create_price(0.01),  # $0.01 - uses builder!
    endpoint_path="/analyze",
    description="Standard analysis"
)
async def analyze(request: Request, data: dict):
    """Standard analysis - $0.01"""
    return {"analysis": "detailed results", "confidence": 0.95}


@app.post("/deep-analysis")
@require_payment(
    price=price_builder.create_price(0.05),  # $0.05 - uses builder!
    endpoint_path="/deep-analysis",
    description="Comprehensive deep analysis with ML models"
)
async def deep_analysis(request: Request, data: dict):
    """Expensive operation - $0.05"""
    return {
        "analysis": "very detailed results",
        "confidence": 0.99,
        "model": "advanced-ml-v2"
    }


@app.get("/health")
async def health():
    """Health check - FREE (no decorator, no payment required)"""
    return {"status": "healthy"}


# ============================================================================
# D402 MIDDLEWARE SETUP
# ============================================================================

def create_app_with_middleware():
    """Add D402 middleware to the app."""
    
    # Extract payment configs from @require_payment decorators
    # This is the SAME approach as MCP servers, just generalized!
    payment_configs = extract_payment_configs(app, SERVER_ADDRESS)
    
    print("=" * 80)
    print("D402 Payment Configuration:")
    print(f"  Server Address: {SERVER_ADDRESS}")
    print(f"  Protected endpoints: {len(payment_configs)}")
    for path, config in payment_configs.items():
        price_usd = config['price_float']
        print(f"    {path}: ${price_usd} USD")
    print("=" * 80)
    
    # Add D402 middleware
    facilitator_url = os.getenv("D402_FACILITATOR_URL", "http://localhost:7070")
    testing_mode = os.getenv("D402_TESTING_MODE", "true").lower() == "true"
    
    app.add_middleware(
        D402PaymentMiddleware,
        server_address=SERVER_ADDRESS,
        tool_payment_configs=payment_configs,  # Same interface as MCP!
        requires_auth=False,  # Payment only (no API keys)
        testing_mode=testing_mode,
        facilitator_url=facilitator_url,
        server_name="example-analysis-api"
    )
    
    print("✅ D402 middleware added")
    print(f"   Testing mode: {testing_mode}")
    print(f"   Facilitator: {facilitator_url}")
    print("=" * 80)
    
    return app


if __name__ == "__main__":
    # Create app with middleware
    app_with_d402 = create_app_with_middleware()
    
    # Run server
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        app_with_d402,
        host="0.0.0.0",
        port=port
    )

