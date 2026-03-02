"""Integration tests for Chronos callbacks and OpenTelemetry tracing.

Tests artifact uploads and OTel tracing to Chronos.

Run with:
    pytest tests/integration/test_chronos_callback.py -v -s
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

import pytest


def _cleanup_docker_dir(path: str) -> None:
    """Clean up directory that may contain root-owned files from Docker."""
    try:
        shutil.rmtree(path)
    except PermissionError:
        subprocess.run(["sudo", "rm", "-rf", path], check=False)


class MockChronosHandler(BaseHTTPRequestHandler):
    """HTTP handler that captures Chronos callbacks."""

    # Class-level storage for received requests
    received_requests: list[dict] = []

    def log_message(self, format, *args):
        """Suppress HTTP server logs."""
        pass

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = {"raw": body.decode()}

        # Store the request
        MockChronosHandler.received_requests.append(
            {
                "path": self.path,
                "data": data,
            }
        )

        # Send success response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        # Return appropriate response based on endpoint
        # The logging module uses /event for events and /logs-upload for artifacts
        if self.path == "/event":
            response = {"success": True, "event_id": data.get("event_id", "generated-id")}
        elif self.path == "/logs-upload":
            response = {"success": True, "logs_url": "s3://test-bucket/logs.zip"}
        else:
            response = {"success": True}

        self.wfile.write(json.dumps(response).encode())


@pytest.fixture
def mock_callback_url():
    """Start a mock Chronos HTTP server."""
    # Clear any previous requests
    MockChronosHandler.received_requests = []

    # Find a free port
    server = HTTPServer(("127.0.0.1", 0), MockChronosHandler)
    port = server.server_address[1]

    # Run server in background thread
    thread = Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    yield f"http://127.0.0.1:{port}"

    # Shutdown
    server.shutdown()


@pytest.fixture
def temp_workspace():
    """Create a temporary workspace directory."""
    tmpdir = tempfile.mkdtemp()
    test_file = os.path.join(tmpdir, "test.py")
    with open(test_file, "w") as f:
        f.write("# Test file\nprint('hello')\n")
    yield tmpdir
    _cleanup_docker_dir(tmpdir)


@pytest.fixture
def temp_logs_dir():
    """Create a temporary logs directory."""
    tmpdir = tempfile.mkdtemp()
    yield tmpdir
    _cleanup_docker_dir(tmpdir)


@pytest.fixture
def openhands_image():
    """OpenHands ECR image."""
    return "383806609161.dkr.ecr.us-west-1.amazonaws.com/agents/plato/openhands:1.0.7"


@pytest.fixture
def openhands_config():
    """OpenHands agent config."""
    return {"model_name": "gemini/gemini-3-flash-preview"}


@pytest.fixture
def secrets():
    """Secrets from environment."""
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        return {"gemini_api_key": gemini_key}

    anthropic_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if anthropic_key:
        return {"anthropic_api_key": anthropic_key}

    pytest.skip("GEMINI_API_KEY or ANTHROPIC_API_KEY not set")
    return {}


class TestOTelTracing:
    """Test OpenTelemetry tracing integration.

    Note: The old custom logging system (init_logging, span, etc.) has been replaced
    with OpenTelemetry. These tests are placeholders for future OTel integration tests.
    """

    def test_otel_tracer_available(self):
        """Test that OTel tracer is available."""
        from plato.agents import get_tracer

        tracer = get_tracer("test")
        assert tracer is not None


class TestLoggingUtils:
    """Tests for logging utility functions."""

    def test_zip_directory(self):
        """Test zip_directory creates valid zip."""
        import io
        import zipfile

        from plato.agents.artifacts import zip_directory

        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some files
            with open(os.path.join(tmpdir, "test.log"), "w") as f:
                f.write("test log content")
            os.makedirs(os.path.join(tmpdir, "subdir"))
            with open(os.path.join(tmpdir, "subdir", "nested.log"), "w") as f:
                f.write("nested content")

            # Zip it
            zip_bytes = zip_directory(tmpdir)

            # Verify it's a valid zip
            zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
            names = zf.namelist()
            assert "test.log" in names
            assert "subdir/nested.log" in names or "subdir\\nested.log" in names
