from dataclasses import dataclass
from pathlib import Path

@dataclass
class TestResult:
    request: dict
    raw_response: str
    artifact_path: Path | None
    logs: str
    exit_code: int

def run_test(channel: str, request: dict, model: str) -> TestResult:
    if channel == "cli":
        from .cli import execute
    elif channel == "sms":
        from .sms import execute
    elif channel == "web":
        from .web import execute
    else:
        raise ValueError(f"Unknown channel: {channel}")
        
    return execute(request, model)
