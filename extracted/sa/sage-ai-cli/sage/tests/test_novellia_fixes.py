"""Regression tests for the Novellia incident bugs.

Three bug classes the Novellia run exposed:
  1. FILE: writes accept prose-as-code (the package.json with "are"/"to"/"met")
  2. Tool parser accepts nested commands like `READ: SEARCH: *.py`
  3. Model resolver routes to llama_cpp:X without checking ollama fallback

These tests pin the fixes so they don't regress.
"""

from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest


# ════════════════════════════════════════════════════════════════════════
# Fix #1: content_validator
# ════════════════════════════════════════════════════════════════════════

def test_validator_accepts_real_code():
    from sage.core.content_validator import validate_content
    js = """
const express = require('express');
const app = express();
app.get('/pets', (req, res) => res.json([{id: 1, name: 'Rex'}]));
app.listen(3000);
""".strip()
    assert validate_content("src/server.js", js).ok


def test_validator_rejects_protocol_leak_in_js():
    """The exact symptom from the Novellia run."""
    from sage.core.content_validator import validate_content
    bad = """
FILE: src/api/records.js

// Remove this line to fix the syntax error
FILE: src/components/PetList.js (modify existing file)
CREATE: src/components/PetList.test.js

## TASK: Technology Stack
Plan ID: plan_20260510_000034
Goal: Use whatever stack you're comfortable with
""".strip()
    result = validate_content("src/api/pets.js", bad)
    assert not result.ok
    assert result.signal in ("protocol_leak", "prompt_echo")


def test_validator_rejects_planning_steps_in_js():
    from sage.core.content_validator import validate_content
    bad = """
## STEP 1: Explore the Codebase
READ: SEARCH: *.py

## STEP 4.2: Implement Pet List Component
FILE: src/components/PetList.js
""".strip()
    result = validate_content("src/api/pets.js", bad)
    assert not result.ok
    assert result.signal == "protocol_leak"


def test_validator_rejects_english_words_as_npm_packages():
    """The literal package.json from the Novellia run."""
    from sage.core.content_validator import validate_content
    poison = json.dumps({
        "dependencies": {
            "are": "^0.0.1",
            "ensure": "^0.4.6",
            "met": "^0.0.3",
            "to": "^0.2.9",
            "dependencies": "^0.0.1",
        }
    })
    result = validate_content("package.json", poison)
    assert not result.ok
    assert result.signal == "json_poison"
    assert "are" in result.reason or "to" in result.reason or "met" in result.reason


def test_validator_accepts_real_package_json():
    from sage.core.content_validator import validate_content
    good = json.dumps({
        "name": "novellia-pets",
        "version": "1.0.0",
        "dependencies": {
            "express": "^4.18.0",
            "react": "^18.2.0",
            "mongoose": "^7.5.0",
        },
        "devDependencies": {
            "vitest": "^1.0.0",
        },
    })
    assert validate_content("package.json", good).ok


def test_validator_rejects_invalid_version_strings():
    from sage.core.content_validator import validate_content
    bad = json.dumps({
        "dependencies": {
            "express": "not a version",
            "lodash": "the latest one please",
            "react": "^18.0.0",
        }
    })
    result = validate_content("package.json", bad)
    assert not result.ok
    assert result.signal == "json_poison"


def test_validator_rejects_invalid_json():
    from sage.core.content_validator import validate_content
    result = validate_content("config.json", "this is not { json")
    assert not result.ok
    assert result.signal == "json_invalid"


def test_validator_rejects_prose_mass_in_python():
    from sage.core.content_validator import validate_content
    prose = """
# This is a documentation file
# describing the architecture
- First, we need to set up the database
- Then, we configure the API
- Finally, we wire up the UI
## Architecture
- The system uses MongoDB
- The frontend is React
""".strip()
    result = validate_content("src/main.py", prose)
    assert not result.ok
    assert result.signal == "prose_mass"


def test_validator_allows_doc_comment_at_top():
    from sage.core.content_validator import validate_content
    real_code = '''
"""Module docstring describing what this does."""
import os

def hello():
    return os.environ.get("USER", "world")

if __name__ == "__main__":
    print(hello())
'''.strip()
    assert validate_content("src/main.py", real_code).ok


def test_validator_rejects_prompt_echo_pattern():
    from sage.core.content_validator import validate_content
    echoed = """
some text

## TASK: Build a thing
Plan ID: plan_20260510_000123
## NEXT STEPS
1. Do something
""".strip()
    result = validate_content("src/anything.ts", echoed)
    assert not result.ok
    assert result.signal in ("protocol_leak", "prompt_echo")


def test_validator_empty_content_is_ok():
    from sage.core.content_validator import validate_content
    assert validate_content("src/x.py", "").ok
    assert validate_content("src/x.py", "   \n  \n").ok


# ── FileWriteTool integration ────────────────────────────────────────

def test_filewrite_tool_blocks_validator_failure(tmp_path):
    from sage.core.tools import FileWriteTool, ToolContext, ToolStatus
    ctx = ToolContext(cwd=tmp_path)
    tool = FileWriteTool(ctx)
    poison = json.dumps({"dependencies": {"are": "^0.0.1", "ensure": "^0.4.6"}})
    result = tool.write("package.json", poison, backup=False)
    assert result.status == ToolStatus.ERROR
    assert "REJECTED" in (result.error or "")
    # File must NOT have been written
    assert not (tmp_path / "package.json").exists()


def test_filewrite_tool_writes_real_code(tmp_path):
    from sage.core.tools import FileWriteTool, ToolContext, ToolStatus
    ctx = ToolContext(cwd=tmp_path)
    tool = FileWriteTool(ctx)
    real = """
const express = require('express');
const app = express();
app.listen(3000);
""".strip()
    result = tool.write("server.js", real, backup=False)
    assert result.status == ToolStatus.SUCCESS, result.error
    assert (tmp_path / "server.js").read_text() == real


# ════════════════════════════════════════════════════════════════════════
# Fix #2: tool parser nested-command guard
# ════════════════════════════════════════════════════════════════════════

def test_parser_rejects_nested_commands():
    """`READ: SEARCH: *.py` is the model emitting two commands on one line."""
    from sage.core.tools import parse_tool_command
    assert parse_tool_command("READ: SEARCH: *.py") is None
    assert parse_tool_command("RUN: BASH: ls -la") is None
    assert parse_tool_command("SEARCH: READ: src/foo.py") is None


def test_parser_accepts_normal_commands():
    from sage.core.tools import parse_tool_command
    a = parse_tool_command("READ: src/server.js")
    assert a is not None
    b = parse_tool_command("SEARCH: pattern_here")
    assert b is not None
    c = parse_tool_command("RUN: npm test")
    assert c is not None


def test_parser_rejects_file_block_with_nested_command_path():
    from sage.core.tools import parse_tool_command
    out = parse_tool_command("FILE: READ: src/foo.py\n```js\ncode\n```")
    assert out is None


def test_parser_accepts_normal_file_block():
    from sage.core.tools import parse_tool_command
    out = parse_tool_command("FILE: src/foo.js\nconsole.log('hi');")
    assert out is not None
    assert out.arguments["path"] == "src/foo.js"


# ════════════════════════════════════════════════════════════════════════
# Fix #3: model resolver smart re-route (unit-tested via the validator
# logic; full _prepare_model_for_use needs the catalog, which loads from
# GCS at import time and is heavy to mock — we verify the pieces).
# ════════════════════════════════════════════════════════════════════════

def test_resolver_existing_branch_unchanged_for_explicit_ollama():
    """Sanity: explicit `ollama:X` always resolves to itself."""
    from sage.main import _resolve_model_prefix
    from sage.config import SageConfig
    cfg = SageConfig()
    out = _resolve_model_prefix("ollama:llama3.2", cfg)
    assert out == "ollama:llama3.2"


def test_resolver_existing_branch_unchanged_for_explicit_llama_cpp():
    from sage.main import _resolve_model_prefix
    from sage.config import SageConfig
    cfg = SageConfig()
    out = _resolve_model_prefix("llama_cpp:custom", cfg)
    assert out == "llama_cpp:custom"
