"""Example: Utility agent with d402 payment support."""

import os
import asyncio
from fastapi import FastAPI, Request
import uvicorn

from traia_iatp.d402 import (
    D402Config,
    D402ServicePrice,
    require_iatp_payment,
    add_d402_info_to_agent_card
)

# Initialize FastAPI app
app = FastAPI(title="Paid Sentiment Analysis Agent")

# Configure d402 payments
d402_config = D402Config(
    enabled=True,
    # This would be the deployed utility agent contract address
    pay_to_address=os.getenv("UTILITY_AGENT_CONTRACT_ADDRESS", "0x1234567890123456789012345678901234567890"),
    
    # Default pricing: $0.01 per request
    default_price=D402ServicePrice(
        usd_amount="0.01",
        network="base-mainnet",
        asset_address="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC on Base
        max_timeout_seconds=300
    ),
    
    # Custom pricing per skill
    skill_prices={
        "sentiment_analysis": D402ServicePrice(
            usd_amount="0.01",
            network="base-mainnet",
            asset_address="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            max_timeout_seconds=300
        ),
        "entity_extraction": D402ServicePrice(
            usd_amount="0.02",
            network="base-mainnet",
            asset_address="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
            max_timeout_seconds=300
        )
    },
    
    # Facilitator configuration
    facilitator_url=os.getenv("FACILITATOR_URL", "https://api.traia.io/d402/facilitator"),
    facilitator_api_key=os.getenv("TRAIA_RELAYER_API_KEY"),
    
    # Service description for payment UI
    service_description="AI-powered financial sentiment analysis using FinBERT models",
    
    # Protect all paths by default
    protected_paths=["*"]
)


# Add d402 middleware
@app.middleware("http")
async def payment_middleware(request: Request, call_next):
    """Middleware that requires payment for all requests."""
    middleware = require_iatp_payment(d402_config)
    return await middleware(request, call_next)


# Agent card endpoint (standard A2A protocol)
@app.get("/.well-known/agent.json")
async def agent_card():
    """Return agent card with d402 payment information."""
    card = {
        "name": "sentiment_analysis_agent",
        "description": "AI-powered financial sentiment analysis",
        "version": "1.0.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
            "stateTransitionHistory": False
        },
        "skills": [
            {
                "id": "sentiment_analysis",
                "name": "Sentiment Analysis",
                "description": "Analyze sentiment of financial text",
                "examples": [
                    "Analyze: 'Tech stocks rally on strong earnings'",
                    "What is the sentiment of: 'Markets tumble amid recession fears'"
                ]
            }
        ]
    }
    
    # Add d402 payment information
    card = await add_d402_info_to_agent_card(card, d402_config)
    return card


# Protected endpoint - requires payment
@app.post("/analyze")
async def analyze_sentiment(request: Request):
    """Analyze sentiment of text. Requires payment."""
    data = await request.json()
    text = data.get("text", "")
    
    # Simulate sentiment analysis
    # In real implementation, this would call a model
    result = {
        "text": text,
        "sentiment": "positive",
        "confidence": 0.87,
        "scores": {
            "positive": 0.87,
            "neutral": 0.08,
            "negative": 0.05
        }
    }
    
    return result


# Another protected endpoint
@app.post("/extract-entities")
async def extract_entities(request: Request):
    """Extract entities from text. Requires payment (higher price)."""
    data = await request.json()
    text = data.get("text", "")
    
    # Simulate entity extraction
    result = {
        "text": text,
        "entities": [
            {"text": "Apple", "type": "ORGANIZATION", "confidence": 0.95},
            {"text": "Tim Cook", "type": "PERSON", "confidence": 0.92}
        ]
    }
    
    return result


# Health check endpoint (not protected)
@app.get("/health")
async def health():
    """Health check endpoint - no payment required."""
    # This endpoint bypasses payment because we can add specific path exclusions
    return {"status": "healthy"}


def main():
    """Run the server."""
    print("Starting Paid Sentiment Analysis Agent")
    print(f"D402 Enabled: {d402_config.enabled}")
    print(f"Pay-to Address: {d402_config.pay_to_address}")
    print(f"Default Price: ${d402_config.default_price.usd_amount} USD")
    print(f"Facilitator: {d402_config.facilitator_url}")
    print()
    print("Protected endpoints:")
    print("  POST /analyze - $0.01 per request")
    print("  POST /extract-entities - $0.02 per request")
    print()
    print("Free endpoints:")
    print("  GET /health")
    print("  GET /.well-known/agent.json")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()

