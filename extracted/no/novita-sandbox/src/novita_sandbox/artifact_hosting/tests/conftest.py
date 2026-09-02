"""Pytest configuration and fixtures for Artifact Hosting SDK tests."""

import io
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import MagicMock

import httpx
import pytest

from novita_sandbox.core.connection_config import (
    DEFAULT_NOVITA_DOMAIN,
    validate_domain,
)


# =============================================================================
# Test Report Configuration
# =============================================================================

class HTTPLogCapture:
    """Captures HTTP request/response logs for test reporting."""
    
    def __init__(self):
        self.entries: List[Dict[str, Any]] = []
    
    def add_request(self, method: str, url: str, body: Any = None, headers: Dict = None):
        """Record an HTTP request."""
        self.entries.append({
            "type": "request",
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "url": url,
            "body": body,
            "headers": headers,
        })
    
    def add_response(self, status_code: int, body: Any = None, elapsed: float = 0):
        """Record an HTTP response."""
        self.entries.append({
            "type": "response",
            "timestamp": datetime.now().isoformat(),
            "status_code": status_code,
            "body": body,
            "elapsed_seconds": elapsed,
        })
    
    def clear(self):
        """Clear all captured entries."""
        self.entries.clear()
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """Return all entries as a list of dicts."""
        return self.entries.copy()


# Global HTTP log capture instance
_http_log_capture = HTTPLogCapture()


def pytest_addoption(parser):
    """Add custom command-line options for integration tests."""
    parser.addoption(
        "--no-cleanup",
        action="store_true",
        default=False,
        help="Skip cleanup of test resources (sandbox, projects) for debugging",
    )


def pytest_configure(config):
    """Configure logging and reporting for integration tests.
    
    Sets up:
    - File logging for SDK modules with DEBUG level
    - Console logging with configurable level
    - HTML report generation
    - JSON report for machine parsing
    
    Environment Variables:
        SDK_LOG_LEVEL: Console log level (DEBUG, INFO, WARNING, ERROR). Default: INFO
                       Set to DEBUG for verbose mode.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent.parent.parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Generate timestamped filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = logs_dir / f"integration_test_{timestamp}.log"
    
    # Configure file handler for root SDK logger only
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    
    # Get console log level from environment (default: INFO, use DEBUG for verbose)
    console_level_name = os.getenv("SDK_LOG_LEVEL", "INFO").upper()
    console_level = getattr(logging, console_level_name, logging.INFO)
    
    # Configure root SDK logger (child loggers inherit settings)
    sdk_logger = logging.getLogger("novita_sandbox.artifact_hosting")
    sdk_logger.setLevel(logging.DEBUG)
    sdk_logger.propagate = False  # Prevent duplicate logs
    
    # Only add handler if not already added (for pytest-xdist workers)
    if not sdk_logger.handlers:
        sdk_logger.addHandler(file_handler)
        
        # Also add console handler for visibility
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S"
        ))
        sdk_logger.addHandler(console_handler)
    
    # Store paths in config for reporting
    config._log_file_path = log_file
    config._logs_dir = logs_dir
    config._timestamp = timestamp
    
    verbose_mode = "ON" if console_level == logging.DEBUG else "OFF"
    print(f"\n📝 Integration test logs: {log_file}")
    print(f"🔊 Verbose mode: {verbose_mode} (set SDK_LOG_LEVEL=DEBUG for verbose)\n")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach additional information to test reports for failed tests."""
    outcome = yield
    report = outcome.get_result()
    
    # Only process for call phase (actual test execution)
    if call.when == "call":
        # Add HTTP log entries to report extras (for pytest-html)
        extras = getattr(report, "extras", [])
        
        if report.failed:
            # Capture HTTP logs for failed tests
            http_logs = _http_log_capture.to_dict()
            if http_logs:
                # Format HTTP logs as HTML for the report
                html_content = _format_http_logs_html(http_logs)
                extras.append(pytest.html.extras.html(html_content))
        
        report.extras = extras
    
    # Clear HTTP logs after each test
    _http_log_capture.clear()


def _format_http_logs_html(logs: List[Dict[str, Any]]) -> str:
    """Format HTTP logs as HTML for test report."""
    if not logs:
        return ""
    
    html = ['<div class="http-logs" style="background:#1e1e1e;color:#d4d4d4;padding:10px;border-radius:4px;font-family:monospace;font-size:12px;overflow-x:auto;">']
    html.append('<h4 style="color:#569cd6;margin:0 0 10px 0;">📡 HTTP Request/Response Logs</h4>')
    
    for entry in logs:
        if entry["type"] == "request":
            html.append(f'<div style="color:#4ec9b0;margin:5px 0;">')
            html.append(f'<strong>→ {entry["method"]} {entry["url"]}</strong>')
            if entry.get("body"):
                try:
                    body_str = json.dumps(entry["body"], indent=2, ensure_ascii=False)
                    html.append(f'<pre style="color:#ce9178;margin:2px 0 0 15px;">{body_str}</pre>')
                except (TypeError, ValueError):
                    html.append(f'<pre style="color:#ce9178;margin:2px 0 0 15px;">{entry["body"]}</pre>')
            html.append('</div>')
        
        elif entry["type"] == "response":
            status_color = "#4fc414" if 200 <= entry["status_code"] < 300 else "#f14c4c"
            html.append(f'<div style="color:{status_color};margin:5px 0 10px 15px;">')
            html.append(f'<strong>← {entry["status_code"]}</strong> ({entry.get("elapsed_seconds", 0):.3f}s)')
            if entry.get("body"):
                try:
                    body_str = json.dumps(entry["body"], indent=2, ensure_ascii=False)
                    html.append(f'<pre style="color:#d4d4d4;margin:2px 0 0 0;">{body_str}</pre>')
                except (TypeError, ValueError):
                    html.append(f'<pre style="color:#d4d4d4;margin:2px 0 0 0;">{entry["body"]}</pre>')
            html.append('</div>')
    
    html.append('</div>')
    return '\n'.join(html)


def pytest_html_report_title(report):
    """Set custom title for HTML report."""
    report.title = "Artifact Hosting SDK - Integration Test Report"


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print summary with report locations at the end of test run."""
    logs_dir = getattr(config, "_logs_dir", None)
    timestamp = getattr(config, "_timestamp", None)
    
    if logs_dir and timestamp:
        terminalreporter.write_sep("=", "Test Report Files")
        terminalreporter.write_line(f"📝 Log file: {config._log_file_path}")
        
        # Check for HTML report
        html_report = logs_dir / f"test_report_{timestamp}.html"
        if html_report.exists():
            terminalreporter.write_line(f"📊 HTML report: {html_report}")
        
        # Check for JSON report
        json_report = logs_dir / f"test_report_{timestamp}.json"
        if json_report.exists():
            terminalreporter.write_line(f"📋 JSON report: {json_report}")


@pytest.fixture
def mock_http_client():
    """Create a mock httpx.Client for testing.
    
    Returns:
        MagicMock configured as an httpx.Client.
    """
    client = MagicMock(spec=httpx.Client)
    return client


@pytest.fixture
def mock_response():
    """Create a mock HTTP response factory.
    
    Returns:
        Callable that creates mock httpx.Response objects.
    """
    def _create_response(
        status_code: int = 200,
        json_data: Dict[str, Any] = None,
        text: str = "",
        headers: Dict[str, str] = None,
    ) -> httpx.Response:
        response = MagicMock(spec=httpx.Response)
        response.status_code = status_code
        response.is_success = 200 <= status_code < 300
        response.text = text
        response.headers = headers or {}
        
        if json_data is not None:
            response.json.return_value = json_data
        else:
            response.json.side_effect = Exception("No JSON data")
        
        return response
    
    return _create_response


@pytest.fixture
def sample_project_data() -> Dict[str, Any]:
    """Sample project data for testing (V2 API format with camelCase).
    
    Returns:
        Dictionary with valid project fields matching openapi_v2.yaml schema.
    """
    return {
        "projectId": "proj_xxx",
        "accountInfo": {
            "accountId": "acc_xxx",
            "teamId": "team_xxx",
            "memberId": "member_xxx",
        },
        "name": "my-app",
        "description": "A test project",
        "status": 1,  # Active status as integer
        "endpoint": {
            "defaultUrl": "https://my-app.novita.space",
            "customUrl": None,
        },
        "endpointConfig": {
            "customDomain": None,
            "requestTimeoutSeconds": 30,
        },
        "deploymentCount": 0,
        "currentDeploymentId": None,
        "createdAt": "2024-12-16T10:00:00Z",
        "updatedAt": "2024-12-16T10:00:00Z",
    }


@pytest.fixture
def sample_deployment_data() -> Dict[str, Any]:
    """Sample deployment data for testing (V2 API format with camelCase).
    
    Returns:
        Dictionary with valid deployment fields matching openapi_v2.yaml schema.
    """
    return {
        "deploymentId": "dep_xxx",
        "projectId": "proj_xxx",
        "status": 1,  # QUEUED as integer (0=UNSPECIFIED, 1=QUEUED)
        "message": "Initial deployment",
        "errorMessage": None,
        "accountInfo": {
            "accountId": "acc_xxx",
            "teamId": "team_xxx",
            "memberId": "member_xxx",
        },
        "artifactsSource": {
            "sandboxId": "sbx_xxx",
            "path": "/app/source",
        },
        "metadata": {
            "environmentVariables": {"NODE_ENV": "production"},
            "httpPort": 3000,
            "checkHealthPath": "/health",
            "replicaSpec": {
                "cpu": "1",
                "memory": "1Gi",
                "maxReplicas": 1,
                "minReplicas": 0,
            },
        },
        "createdAt": "2024-12-16T10:00:00Z",
    }


@pytest.fixture(scope="session")
def api_key():
    """Get API key from environment (session-scoped for reuse).
    
    Environment variable: NOVITA_API_KEY
    
    Returns:
        API key string.
    """
    return os.getenv("NOVITA_API_KEY", "test-key")


# Note: base_url fixture removed - SDK uses fixed URL https://artifact.novita.ai/v1


@pytest.fixture(scope="session")
def novita_domain():
    """Get Novita sandbox domain from environment (session-scoped for reuse).
    
    Environment variable: NOVITA_DOMAIN
    Default: us-phx-1.sandbox.novita.ai
    
    Returns:
        Sandbox domain string.
    """
    domain = os.getenv("NOVITA_DOMAIN", DEFAULT_NOVITA_DOMAIN)
    validate_domain(domain)
    return domain


@pytest.fixture
def sample_rollback_response() -> Dict[str, Any]:
    """Sample rollback response for testing.
    
    Returns:
        Dictionary matching RollbackResponse schema.
    """
    return {
        "projectId": "proj_xxx",
        "previousDeploymentId": "dep_old",
        "currentDeploymentId": "dep_target",
    }


@pytest.fixture
def sample_log_entry_data() -> Dict[str, Any]:
    """Sample log entry data for testing.
    
    Returns:
        Dictionary with log entry fields matching current API format.
    """
    return {
        "line": "Building image...",
    }


# =============================================================================
# Test Sandbox Configuration
# =============================================================================

# Static HTML content for test sandbox
_INDEX_HTML_CONTENT = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Static Site</title>
</head>
<body>
    <h1>Test Static Site</h1>
    <p>This is a test page for integration testing.</p>
</body>
</html>
"""

# Sandbox template for testing (configurable via SANDBOX_TEMPLATE env var)
_SANDBOX_TEMPLATE = os.getenv("SANDBOX_TEMPLATE", "base")
_SANDBOX_TIMEOUT = 600  # 10 minutes


@pytest.fixture(scope="session")
def test_sandbox(request):
    """Create a test sandbox for integration tests (session-scoped).
    
    Automatically creates a sandbox using the novita_sandbox SDK,
    sets up static files, and optionally cleans up after all tests complete.
    
    Use --no-cleanup to skip cleanup for debugging.
    
    Returns:
        Dictionary with sandbox info: {sandbox_id, app_dir, full_sandbox_id}
    """
    try:
        from novita_sandbox.core import Sandbox
    except ImportError:
        pytest.skip("novita_sandbox.core.Sandbox not available")
        return None
    
    logger = logging.getLogger("novita_sandbox.artifact_hosting.test")
    no_cleanup = request.config.getoption("--no-cleanup", default=False)
    
    # Create sandbox
    logger.info(f"Creating test sandbox with template: {_SANDBOX_TEMPLATE}")
    try:
        sandbox = Sandbox.create(_SANDBOX_TEMPLATE, timeout=_SANDBOX_TIMEOUT)
    except Exception as e:
        logger.error(f"Failed to create sandbox: {e}")
        pytest.fail(f"Failed to create sandbox: {e}")  # Fail instead of skip
    
    sandbox_id = sandbox.sandbox_id

    logger.info(f"Sandbox created: {sandbox_id}")
    
    # Create static file
    app_dir = "/app"
    index_path = f"{app_dir}/index.html"
    dockerfile_path = f"{app_dir}/Dockerfile"
    
    try:
        sandbox.files.write(index_path, _INDEX_HTML_CONTENT)
        logger.info(f"Created test file: {index_path}")
        sandbox.files.write(dockerfile_path, _dockerfile_content())
        logger.info(f"Created test file: {dockerfile_path}")
    except Exception as e:
        logger.warning(f"Failed to create test files: {e}")
    
    sandbox_info = {
        "sandbox_id": sandbox_id,
        "full_sandbox_id": sandbox_id,
        "app_dir": app_dir,
        "sandbox": sandbox,
    }
    
    yield sandbox_info
    
    # Cleanup: Kill sandbox after tests (unless --no-cleanup)
    if no_cleanup:
        logger.info(f"Skipping sandbox cleanup (--no-cleanup): {sandbox_id}")
    else:
        logger.info(f"Cleaning up sandbox: {sandbox_id}")
        try:
            sandbox.kill()
            logger.info("Sandbox killed successfully")
        except Exception as e:
            logger.warning(f"Failed to kill sandbox: {e}")


@pytest.fixture(scope="session")
def test_sandbox_id(test_sandbox):
    """Get test sandbox ID (session-scoped).
    
    Automatically creates a sandbox if needed.
    
    Returns:
        Sandbox ID string (part before "-").
    """
    if test_sandbox is None:
        return None
    return test_sandbox["sandbox_id"]


@pytest.fixture(scope="session")
def test_app_dir(test_sandbox):
    """Get application directory in the sandbox (session-scoped).
    
    Returns:
        Application directory path (default: /app).
    """
    if test_sandbox is None:
        return "/app"
    return test_sandbox["app_dir"]


@pytest.fixture(scope="session")
def test_dockerfile_content() -> str:
    """Get Dockerfile content for integration tests.
    
    Nginx static site with env.html that displays environment variables.
    The env.html is generated at container startup to capture runtime env vars.
    
    Returns:
        Dockerfile content string.
    """
    return _dockerfile_content()


def _dockerfile_content() -> str:
    return """FROM nginx:1.27-alpine
RUN rm -rf /usr/share/nginx/html/*
COPY . /var/www/html/
RUN cp -r /var/www/html/* /usr/share/nginx/html/

EXPOSE 80
CMD sh -c 'echo "<html><head><title>Environment Variables</title></head><body><h1>Environment Variables</h1><pre>NODE_ENV=$NODE_ENV\\nVERSION=$VERSION</pre></body></html>" > /usr/share/nginx/html/env.html && nginx -g "daemon off;"'
"""
