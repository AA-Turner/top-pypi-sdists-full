#!/usr/bin/env bash
# Test script for verifying plugin installation scenarios
# Tests that extend_path() correctly merges namespace packages for editable installs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SDK_DIR="$(dirname "$SCRIPT_DIR")"
TMP_DIR="/tmp/test_plugin_installs_$$"

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

cleanup() {
    rm -rf "$TMP_DIR"
}
trap cleanup EXIT

# test_import <import_path> <expected: pass|fail>
test_import() {
    local import_path="$1"
    local expected="${2:-pass}"

    # Use .venv/bin/python directly to avoid uv run auto-syncing dev deps
    if .venv/bin/python -c "import $import_path" 2>/dev/null; then
        if [ "$expected" = "pass" ]; then
            echo -e "  ${GREEN}✓${NC} import $import_path"
        else
            echo -e "  ${RED}✗${NC} import $import_path (should have failed!)"
        fi
    else
        if [ "$expected" = "fail" ]; then
            echo -e "  ${GREEN}✓${NC} import $import_path (correctly unavailable)"
        else
            echo -e "  ${RED}✗${NC} import $import_path (FAILED!)"
        fi
    fi
}

echo "Testing plugin installation scenarios"
echo "SDK Directory: $SDK_DIR"
echo ""

# ===========================================
# SCENARIO 1: From workflow_sdk with --extra
# ===========================================

echo "=========================================="
echo "SCENARIO 1: From workflow_sdk with --extra"
echo "=========================================="

cd "$SDK_DIR"
rm -rf .venv

echo ""
echo "$ uv sync --extra mistralai"
uv sync --extra mistralai 2>/dev/null
test_import "mistralai.workflows.core" pass
test_import "mistralai.workflows.plugins.mistralai" pass

rm -rf .venv

echo ""
echo "$ uv sync --extra mistralai"
uv sync --extra mistralai 2>/dev/null
test_import "mistralai.workflows.core" pass
test_import "mistralai.workflows.plugins.mistralai" pass

rm -rf .venv

echo ""
echo "$ uv sync --extra mistralai"
uv sync --extra mistralai 2>/dev/null
test_import "mistralai.workflows.core" pass
test_import "mistralai.workflows.plugins.mistralai" pass

# ===========================================
# SCENARIO 2: From plugin directory (with dev deps)
# ===========================================

echo ""
echo "=========================================="
echo "SCENARIO 2: From plugin directory"
echo "=========================================="

cd "$SDK_DIR/plugins/mistralai"
rm -rf .venv

echo ""
echo "$ cd plugins/mistralai && uv sync"
uv sync 2>/dev/null
test_import "mistralai.workflows.core" pass
test_import "mistralai.workflows.plugins.mistralai" pass

# ===========================================
# SCENARIO 3: New project with editable install
# ===========================================

echo ""
echo "=========================================="
echo "SCENARIO 3: New project with editable install"
echo "=========================================="

mkdir -p "$TMP_DIR"
cd "$TMP_DIR"

echo ""
echo "$ uv init myproject && cd myproject"
uv init myproject 2>/dev/null
cd myproject

echo ""
echo "$ uv add --editable \$SDK_DIR"
uv add --editable "$SDK_DIR" 2>/dev/null
test_import "mistralai.workflows.core" pass
test_import "mistralai.workflows.plugins.mistralai" fail

echo ""
echo "$ uv add --editable \$SDK_DIR/plugins/mistralai"
uv add --editable "$SDK_DIR/plugins/mistralai" 2>/dev/null
test_import "mistralai.workflows.core" pass
test_import "mistralai.workflows.plugins.mistralai" pass

# ===========================================
# SCENARIO 4: Wildcard imports
# ===========================================

echo ""
echo "=========================================="
echo "SCENARIO 4: Wildcard imports"
echo "=========================================="

cd "$SDK_DIR"
rm -rf .venv
uv sync --extra mistralai 2>/dev/null

echo ""
echo "$ from mistralai.workflows import *"
if .venv/bin/python -c "from mistralai.workflows import *; assert 'workflow' in dir()" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} wildcard import works"
else
    echo -e "  ${RED}✗${NC} wildcard import FAILED"
fi

echo ""
echo "$ from mistralai.workflows.plugins.mistralai import *"
if .venv/bin/python -c "from mistralai.workflows.plugins.mistralai import *; assert 'get_mistral_client' in dir()" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} wildcard import works"
else
    echo -e "  ${RED}✗${NC} wildcard import FAILED"
fi

# ===========================================
# Restore original state
# ===========================================

echo ""
echo "=========================================="
echo "Done! All tests completed."
echo "=========================================="
