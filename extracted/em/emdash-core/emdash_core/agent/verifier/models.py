"""Data models for the verification system."""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class VerifierConfig:
    """Configuration for a single verifier."""

    type: Literal["command", "llm"]
    name: str
    command: str | None = None      # for command type
    prompt: str | None = None       # for llm type
    timeout: int = 120              # seconds
    pass_on_exit_0: bool = True     # for command type
    enabled: bool = True            # can disable without removing

    @classmethod
    def from_dict(cls, data: dict) -> "VerifierConfig":
        """Create from dictionary."""
        return cls(
            type=data.get("type", "command"),
            name=data.get("name", "unnamed"),
            command=data.get("command"),
            prompt=data.get("prompt"),
            timeout=data.get("timeout", 120),
            pass_on_exit_0=data.get("pass_on_exit_0", True),
            enabled=data.get("enabled", True),
        )

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        result = {
            "type": self.type,
            "name": self.name,
            "enabled": self.enabled,
        }
        if self.type == "command":
            result["command"] = self.command
            result["timeout"] = self.timeout
            result["pass_on_exit_0"] = self.pass_on_exit_0
        else:
            result["prompt"] = self.prompt
        return result


@dataclass
class VerifierResult:
    """Result from running a single verifier."""

    name: str
    passed: bool
    output: str
    duration: float
    issues: list[str] = field(default_factory=list)

    @property
    def status_icon(self) -> str:
        """Get status icon for display."""
        return "[green]✓[/green]" if self.passed else "[red]✗[/red]"


@dataclass
class VerificationReport:
    """Complete report from running all verifiers."""

    results: list[VerifierResult]
    all_passed: bool
    summary: str

    @property
    def passed_count(self) -> int:
        """Count of passed verifiers."""
        return sum(1 for r in self.results if r.passed)

    @property
    def failed_count(self) -> int:
        """Count of failed verifiers."""
        return sum(1 for r in self.results if not r.passed)

    @property
    def total_duration(self) -> float:
        """Total duration of all verifiers."""
        return sum(r.duration for r in self.results)

    def get_failures(self) -> list[VerifierResult]:
        """Get list of failed results."""
        return [r for r in self.results if not r.passed]

    def get_all_issues(self) -> list[str]:
        """Get all issues from all failed verifiers."""
        issues = []
        for r in self.results:
            if not r.passed:
                issues.extend(r.issues)
        return issues
