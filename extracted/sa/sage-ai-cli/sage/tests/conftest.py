"""Shared pytest fixtures for sage/tests.

Provides a real local background completions server fixture to allow completely
pure functional integration testing of SAGE's capabilities and routing.
"""

from __future__ import annotations

import json
import os
import sys
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import contextlib
import tempfile
import shutil
import typer.testing

# Monkeypatch isolated_filesystem for typer.testing.CliRunner in newer Typer versions
@contextlib.contextmanager
def _isolated_filesystem(self, temp_dir=None):
    cwd = os.getcwd()
    t_dir = tempfile.mkdtemp(dir=temp_dir)
    os.chdir(t_dir)
    try:
        yield t_dir
    finally:
        os.chdir(cwd)
        try:
            shutil.rmtree(t_dir)
        except OSError:
            pass

typer.testing.CliRunner.isolated_filesystem = _isolated_filesystem

import pytest

# This file lives at <project_root>/sage/tests/conftest.py
_HERE = Path(__file__).resolve().parent          # .../sage/tests
_SAGE_MODULE = _HERE.parent                       # .../sage
_PROJECT_ROOT = _SAGE_MODULE.parent               # .../ai-platform



@pytest.fixture
def sage_project_root() -> Path:
    """The ai-platform/ directory — contains pyproject.toml, sage/, backend/."""
    return _PROJECT_ROOT


@pytest.fixture
def sage_module_root() -> Path:
    """The sage/ module directory — contains main.py, __init__.py, tests/."""
    return _SAGE_MODULE


@pytest.fixture
def sage_tests_dir() -> Path:
    """The sage/tests/ directory."""
    return _HERE


@pytest.fixture(autouse=True)
def reset_sage_global_state():
    """Reset global state variables in sage.main between every test to prevent cross-test leakage."""
    import sage.main as sage_main
    sage_main._global_agent = None
    sage_main._current_cwd = None
    sage_main._current_classification = None
    from sage.core.autonomous_helpers import set_force_implementation_mode
    set_force_implementation_mode(False)
    yield
    sage_main._global_agent = None
    sage_main._current_cwd = None
    sage_main._current_classification = None
    from sage.core.autonomous_helpers import set_force_implementation_mode
    set_force_implementation_mode(False)



import subprocess
import socket
import time
import requests

def _load_env_dict(path):
    env_dict = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip()
        if v.startswith(('"', "'")):
            quote = v[0]
            end_idx = v.find(quote, 1)
            if end_idx != -1:
                v = v[1:end_idx]
            else:
                v = v[1:]
        else:
            v = v.split("#", 1)[0].strip()
        env_dict[k] = v
    return env_dict

# Load env variables into the parent test process environment
if (_PROJECT_ROOT / ".env").exists():
    for k, v in _load_env_dict(_PROJECT_ROOT / ".env").items():
        if k not in os.environ:
            os.environ[k] = v

@pytest.fixture(scope="session", autouse=True)
def real_backend_server():
    """Start the actual FastAPI backend locally for functional integration testing."""
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    
    os.environ["SAGE_API_BASE"] = f"http://127.0.0.1:{port}"
    os.environ["SAGE_TESTING"] = "1"
    os.environ["SAGE_ENABLE_SMS_POLLER"] = "1"
    os.environ["SAGE_DEFAULT_MODEL"] = "cloud:qwen3-coder"
    
    # Start uvicorn
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.app:app", "--port", str(port), "--host", "127.0.0.1"],
        cwd=str(_PROJECT_ROOT),
        env=os.environ,
        stdout=open("backend_test.log", "w"),
        stderr=subprocess.STDOUT
    )
    
    # Wait for ready
    for _ in range(30):
        try:
            if requests.get(f"http://127.0.0.1:{port}/health").status_code == 200:
                break
        except Exception:
            time.sleep(0.5)
            
    yield proc
    try:
        proc.terminate()
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()

