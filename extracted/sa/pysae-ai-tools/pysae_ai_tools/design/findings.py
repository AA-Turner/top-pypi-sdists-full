from dataclasses import dataclass


@dataclass(frozen=True)
class Finding:
    rule: str
    line: int
    snippet: str
    message: str
    suggestion: str


@dataclass(frozen=True)
class Report:
    file: str
    verdict: str
    findings: list[Finding]
