"""Comp-LEO API Service - FastAPI backend for compliance checks."""

from typing import Optional
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Depends, Header, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import time

from comp_leo import __version__
from comp_leo.analyzer.checker import ComplianceChecker
from comp_leo.core.models import CheckResult


# ============================================================================
# APP CONFIGURATION
# ============================================================================

app = FastAPI(
    title="Comp-LEO API",
    description="Compliance & Security API for Leo Smart Contracts",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key security
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


# ============================================================================
# MODELS
# ============================================================================

class CheckRequest(BaseModel):
    """Request body for compliance check."""
    source: str = Field(..., description="Leo source code to analyze")
    policy_pack: str = Field("aleo-baseline", description="Policy pack to use")
    threshold: int = Field(75, ge=0, le=100, description="Minimum passing score")
    fail_on_critical: bool = Field(True, description="Fail if critical violations found")


class CheckResponse(BaseModel):
    """Response from compliance check."""
    success: bool
    result: CheckResult
    usage: dict = Field(..., description="API usage info")


class UsageInfo(BaseModel):
    """API usage information."""
    checks_remaining: int
    checks_used: int
    checks_limit: int
    tier: str
    reset_at: Optional[datetime] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime


# ============================================================================
# MOCK AUTH & RATE LIMITING (Replace with Redis/DB in production)
# ============================================================================

API_KEYS = {
    "free_user_key": {
        "tier": "freemium",
        "limit": 100,
        "used": 0,
        "reset_at": datetime.utcnow() + timedelta(days=30)
    },
    "pro_user_key": {
        "tier": "pro",
        "limit": 1000,
        "used": 0,
        "reset_at": datetime.utcnow() + timedelta(days=30)
    },
    "enterprise_key": {
        "tier": "enterprise",
        "limit": 999999,  # Unlimited
        "used": 0,
        "reset_at": datetime.utcnow() + timedelta(days=30)
    }
}


def verify_api_key(api_key: Optional[str] = Depends(api_key_header)) -> dict:
    """Verify API key and return user info."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required. Get one at https://compiledger.com/api-keys"
        )
    
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    user_info = API_KEYS[api_key]
    
    # Check rate limit
    if user_info["used"] >= user_info["limit"]:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded. Limit: {user_info['limit']} checks/month. "
                   f"Upgrade at https://compiledger.com/pricing"
        )
    
    return user_info


def increment_usage(api_key: str):
    """Increment API usage counter."""
    if api_key in API_KEYS:
        API_KEYS[api_key]["used"] += 1


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["System"])
def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version=__version__,
        timestamp=datetime.utcnow()
    )


@app.get("/usage", response_model=UsageInfo, tags=["Account"])
def get_usage(user_info: dict = Depends(verify_api_key)):
    """Get API usage information for authenticated user."""
    return UsageInfo(
        checks_remaining=user_info["limit"] - user_info["used"],
        checks_used=user_info["used"],
        checks_limit=user_info["limit"],
        tier=user_info["tier"],
        reset_at=user_info["reset_at"]
    )


@app.post("/v1/check", response_model=CheckResponse, tags=["Compliance"])
def check_code(
    request: CheckRequest,
    api_key: str = Depends(api_key_header),
    user_info: dict = Depends(verify_api_key)
):
    """
    Run compliance checks on Leo source code.
    
    **Authentication:** Requires API key in `X-API-Key` header.
    
    **Rate Limits:**
    - Freemium: 100 checks/month
    - Pro: 1,000 checks/month
    - Enterprise: Unlimited
    
    **Example:**
    ```python
    import requests
    
    response = requests.post(
        "https://api.compiledger.com/v1/check",
        headers={"X-API-Key": "your_key"},
        json={
            "source": "program example.aleo { ... }",
            "policy_pack": "nist-800-53",
            "threshold": 80
        }
    )
    ```
    """
    
    start_time = time.time()
    
    try:
        # Initialize checker
        checker = ComplianceChecker(policy_pack=request.policy_pack)
        
        # Write source to temp file
        import tempfile
        from pathlib import Path
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.leo', delete=False) as f:
            f.write(request.source)
            temp_path = f.name
        
        try:
            # Run check
            result = checker.check_file(temp_path, threshold=request.threshold)
        finally:
            # Clean up temp file
            Path(temp_path).unlink(missing_ok=True)
        
        # Increment usage
        increment_usage(api_key)
        
        # Build response
        return CheckResponse(
            success=result.passed,
            result=result,
            usage={
                "checks_used": user_info["used"] + 1,
                "checks_remaining": user_info["limit"] - user_info["used"] - 1,
                "tier": user_info["tier"],
                "duration_ms": (time.time() - start_time) * 1000
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@app.get("/v1/policies", tags=["Compliance"])
def list_policies():
    """List available policy packs."""
    # In production, load from database
    return {
        "policies": [
            {
                "id": "aleo-baseline",
                "name": "Aleo Baseline Security",
                "description": "Core security and best practices for Leo",
                "frameworks": ["Aleo"],
                "rules_count": 10
            },
            {
                "id": "nist-800-53",
                "name": "NIST 800-53",
                "description": "Federal security controls",
                "frameworks": ["NIST"],
                "rules_count": 120
            },
            {
                "id": "iso-27001",
                "name": "ISO/IEC 27001",
                "description": "Information security management",
                "frameworks": ["ISO"],
                "rules_count": 114
            },
            {
                "id": "pci-dss",
                "name": "PCI-DSS",
                "description": "Payment card security",
                "frameworks": ["PCI"],
                "rules_count": 85
            }
        ]
    }


@app.get("/", tags=["System"])
def root():
    """API root endpoint."""
    return {
        "name": "Comp-LEO API",
        "version": __version__,
        "docs": "/docs",
        "get_api_key": "https://compiledger.com/api-keys",
        "pricing": "https://compiledger.com/pricing"
    }


# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print(f"🚀 Comp-LEO API v{__version__} starting...")
    print("📝 Docs: http://localhost:8000/docs")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
