"""
Pydantic models for CompZ compliance data structures.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ControlEvaluation(BaseModel):
    """
    Individual control evaluation result.
    
    Attributes:
        control_id: Control identifier (e.g., "PCI-1.1.1", "CC1.1")
        framework: Framework name (e.g., "PCI-DSS", "SOC2")
        passed: Whether the control passed
        reason: Explanation of pass/fail
        severity: Optional severity level
    """
    control_id: str = Field(..., description="Control identifier")
    framework: str = Field(..., description="Compliance framework")
    passed: bool = Field(..., description="Control pass/fail status")
    reason: str = Field(..., description="Evaluation reason")
    severity: Optional[str] = Field(None, description="Severity level")
    
    class Config:
        json_schema_extra = {
            "example": {
                "control_id": "PCI-1.1.1",
                "framework": "PCI-DSS",
                "passed": True,
                "reason": "Firewall rules properly configured",
                "severity": "high"
            }
        }


class ComplianceResult(BaseModel):
    """
    Complete compliance evaluation result.
    
    This is the primary data structure that gets normalized,
    hashed, and anchored to the Zcash blockchain.
    
    Attributes:
        repo_id: Repository or system identifier
        commit_hash: Git commit hash or version identifier
        frameworks: List of evaluated frameworks
        control_evaluations: List of individual control results
        risk_score: Overall risk score (0-100)
        timestamp: ISO 8601 timestamp
        metadata: Optional additional metadata
    """
    repo_id: str = Field(..., description="Repository/system identifier")
    commit_hash: str = Field(..., description="Git commit or version")
    frameworks: List[str] = Field(..., description="Compliance frameworks")
    control_evaluations: List[ControlEvaluation] = Field(..., description="Control results")
    risk_score: float = Field(..., ge=0, le=100, description="Risk score (0-100)")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    metadata: Optional[dict] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "repo_id": "myorg/myrepo",
                "commit_hash": "abc123def456",
                "frameworks": ["PCI-DSS", "SOC2"],
                "control_evaluations": [
                    {
                        "control_id": "PCI-1.1.1",
                        "framework": "PCI-DSS",
                        "passed": True,
                        "reason": "Firewall configured"
                    }
                ],
                "risk_score": 25.5,
                "timestamp": "2024-01-01T00:00:00Z",
                "metadata": {"scan_duration": 120}
            }
        }


class AnchorResult(BaseModel):
    """
    Result of anchoring compliance data to blockchain.
    
    Attributes:
        hash: SHA-256 hash of compliance data
        txid: Zcash transaction ID
        network: Network (testnet/mainnet)
        timestamp: Anchor timestamp
        mode: Mode used (demo/self-hosted)
        block_height: Optional block height
        explorer_url: Optional explorer URL
    """
    hash: str = Field(..., description="SHA-256 hash")
    txid: str = Field(..., description="Zcash transaction ID")
    network: str = Field(..., description="Network (testnet/mainnet)")
    timestamp: str = Field(..., description="ISO 8601 timestamp")
    mode: str = Field(..., description="Mode (demo/self-hosted)")
    block_height: Optional[int] = Field(None, description="Block height")
    explorer_url: Optional[str] = Field(None, description="Block explorer URL")


class VerificationResult(BaseModel):
    """
    Result of verifying compliance data against blockchain.
    
    Attributes:
        valid: Whether verification passed
        local_hash: Hash computed from provided data
        onchain_hash: Hash retrieved from blockchain
        txid: Transaction ID verified
        reason: Explanation of result
        block_time: Optional block timestamp
        confirmations: Optional confirmation count
    """
    valid: bool = Field(..., description="Verification passed")
    local_hash: str = Field(..., description="Locally computed hash")
    onchain_hash: str = Field(..., description="On-chain hash")
    txid: str = Field(..., description="Transaction ID")
    reason: str = Field(..., description="Verification reason")
    block_time: Optional[str] = Field(None, description="Block timestamp")
    confirmations: Optional[int] = Field(None, description="Confirmation count")
