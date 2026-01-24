"""Core data models for Comp-LEO SDK."""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class Severity(str, Enum):
    """Severity levels for compliance violations."""
    CRITICAL = "critical"  # Immediate fix required, blocks deployment
    HIGH = "high"          # Security/compliance risk, should fix before deploy
    MEDIUM = "medium"      # Best practice violation, fix recommended
    LOW = "low"            # Minor issue, informational
    INFO = "info"          # Guidance, no action required


class ViolationType(str, Enum):
    """Categories of compliance violations."""
    SECURITY = "security"
    ACCESS_CONTROL = "access_control"
    DATA_PRIVACY = "data_privacy"
    INPUT_VALIDATION = "input_validation"
    LOGGING_AUDIT = "logging_audit"
    CRYPTO_COMPLIANCE = "crypto_compliance"
    STATE_MANAGEMENT = "state_management"
    BEST_PRACTICE = "best_practice"


class ControlMapping(BaseModel):
    """Maps violation to compliance framework controls."""
    framework: str = Field(..., description="Framework name (e.g., NIST-800-53, ISO-27001)")
    control_id: str = Field(..., description="Control identifier (e.g., AC-3, A.9.2.1)")
    control_name: str = Field(..., description="Human-readable control name")
    description: Optional[str] = Field(None, description="Control description")


class Remediation(BaseModel):
    """Suggested fix for a violation."""
    description: str = Field(..., description="What to fix")
    code_example: Optional[str] = Field(None, description="Example fix code")
    automated: bool = Field(False, description="Can be auto-fixed")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score for auto-fix")


class Violation(BaseModel):
    """A single compliance or security violation."""
    rule_id: str = Field(..., description="Unique rule identifier")
    rule_name: str = Field(..., description="Human-readable rule name")
    severity: Severity
    violation_type: ViolationType
    message: str = Field(..., description="Violation description")
    
    # Location information
    file_path: str
    line_number: int
    column: Optional[int] = None
    code_snippet: Optional[str] = Field(None, description="Relevant code excerpt")
    
    # Compliance mappings
    controls: List[ControlMapping] = Field(default_factory=list)
    
    # Remediation
    remediation: Optional[Remediation] = None
    
    # Evidence
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Additional context")


class CheckResult(BaseModel):
    """Results from a compliance check run."""
    passed: bool = Field(..., description="Overall pass/fail status")
    score: int = Field(..., ge=0, le=100, description="Compliance score (0-100)")
    threshold: int = Field(75, ge=0, le=100, description="Minimum passing score")
    
    violations: List[Violation] = Field(default_factory=list)
    
    # Statistics
    total_checks: int = Field(0, description="Total checks performed")
    passed_checks: int = Field(0, description="Checks that passed")
    failed_checks: int = Field(0, description="Checks that failed")
    
    # Breakdown by severity
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    info_count: int = 0
    
    # Metadata
    policy_pack: str = Field("default", description="Policy pack used")
    scan_duration_ms: Optional[float] = None
    scanned_files: List[str] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    def __init__(self, **data):
        super().__init__(**data)
        # Auto-compute severity counts
        self._compute_severity_counts()
    
    def _compute_severity_counts(self):
        """Compute violation counts by severity."""
        for v in self.violations:
            if v.severity == Severity.CRITICAL:
                self.critical_count += 1
            elif v.severity == Severity.HIGH:
                self.high_count += 1
            elif v.severity == Severity.MEDIUM:
                self.medium_count += 1
            elif v.severity == Severity.LOW:
                self.low_count += 1
            elif v.severity == Severity.INFO:
                self.info_count += 1
        
        self.failed_checks = len(self.violations)
        self.passed_checks = self.total_checks - self.failed_checks


class PolicyPack(BaseModel):
    """Compliance policy pack definition."""
    id: str = Field(..., description="Policy pack identifier")
    name: str = Field(..., description="Display name")
    description: str
    version: str = Field("1.0.0")
    
    frameworks: List[str] = Field(default_factory=list, description="Associated frameworks")
    enabled_rules: List[str] = Field(default_factory=list, description="Rule IDs to enforce")
    
    # Scoring
    fail_threshold: int = Field(75, ge=0, le=100, description="Minimum score to pass")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AuditReport(BaseModel):
    """Comprehensive audit report for compliance evidence."""
    report_id: str = Field(..., description="Unique report identifier")
    project_name: str
    policy_pack: str
    
    results: CheckResult
    
    # Evidence artifacts
    code_hash: Optional[str] = Field(None, description="Hash of scanned code")
    policy_version: str = Field("1.0.0")
    sdk_version: str = Field("0.1.0")
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    generated_by: Optional[str] = Field(None, description="User or system that ran check")
    
    # Exceptions register
    accepted_risks: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Violations marked as accepted risk"
    )
