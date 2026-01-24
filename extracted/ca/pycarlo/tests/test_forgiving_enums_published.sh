#!/usr/bin/env bash
set -e

VENV_DIR="test-forgiving-enums-venv"

# Function to get the latest stable version >= 0.12.0 from PyPI
get_latest_version() {
    echo "🔍 Querying PyPI for latest pycarlo version >= 0.12.0..." >&2

    # Get all versions from PyPI JSON API
    versions=$(curl -s https://pypi.org/pypi/pycarlo/json | \
        python3 -c "
import sys, json, re
data = json.load(sys.stdin)
versions = data['releases'].keys()

# Filter for versions >= 0.12.0 and exclude pre-releases
stable_versions = []
for v in versions:
    # Parse version (e.g., '0.12.0' or '0.12.1')
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', v)
    if match:
        major, minor, patch = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if (major, minor, patch) >= (0, 12, 0):
            stable_versions.append(((major, minor, patch), v))

# Sort by version tuple and get the latest
if stable_versions:
    stable_versions.sort(reverse=True)
    print(stable_versions[0][1])
else:
    # Fallback to beta if no stable version exists
    print('0.12.0b1')
")

    echo "$versions"
}

# Function to test a specific version
test_version() {
    local version=$1
    local expected_outcome=$2  # "RAISE_ERROR" or "NO_ERROR"

    echo ""
    if [ "$expected_outcome" = "RAISE_ERROR" ]; then
        echo -e "\033[0;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
        echo -e "\033[0;31m🔴 TESTING v$version (Should Raise ValueError)\033[0m"
        echo -e "\033[0;31m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
    else
        echo -e "\033[0;32m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
        echo -e "\033[0;32m🟢 TESTING v$version (Should Not Raise ValueError)\033[0m"
        echo -e "\033[0;32m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m"
    fi

    # Clean up existing venv if it exists
    if [ -d "$VENV_DIR" ]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf "$VENV_DIR"
    fi

    # Create a fresh virtual environment
    echo "📦 Creating fresh virtual environment..."
    python3 -m venv "$VENV_DIR"

    # Activate the virtual environment
    # shellcheck disable=SC1091
    . "$VENV_DIR/bin/activate"

    # Upgrade pip to latest version (suppress notices)
    pip install -q --upgrade pip

    # Install the specified version
    echo "⬇️  Installing pycarlo==$version..."
    pip install -q "pycarlo==$version"

    # Run the test
    echo ""
    echo "🧪 Running test..."
    echo ""

    # Capture exit code to show final result
    if ./utils/env.sh python tests/verify_forgiving_enums_published.py "$version"; then
        test_exit_code=0
    else
        test_exit_code=$?
    fi

    # Clean up
    echo ""
    echo "🗑️  Cleaning up virtual environment..."
    deactivate
    rm -rf "$VENV_DIR"

    # Show final result banner
    echo ""
    if [ $test_exit_code -eq 0 ]; then
        if [ "$expected_outcome" = "RAISE_ERROR" ]; then
            echo -e "\033[0;31m✅ Raised ValueError as Expected (v$version)\033[0m"
        else
            echo -e "\033[0;32m✅ Did Not Raise ValueError (v$version)\033[0m"
        fi
    else
        echo -e "\033[0;31m❌ TEST FAILED UNEXPECTEDLY (v$version)\033[0m"
        return $test_exit_code
    fi
}

# Main script
if [ $# -eq 1 ]; then
    # Single version specified - test just that version
    # Assume it should raise error if it's 0.11.x
    if [[ "$1" =~ ^0\.11\. ]]; then
        test_version "$1" "RAISE_ERROR"
    else
        test_version "$1" "NO_ERROR"
    fi
else
    # No version specified - test both old (0.11.27) and new (latest >= 0.12.0)
    echo ""
    echo "========================================================================"
    echo "FORGIVING ENUMS FEATURE TEST"
    echo "Testing backward compatibility for unknown enum values"
    echo "========================================================================"

    OLD_VERSION="0.11.27"
    NEW_VERSION=$(get_latest_version)

    echo ""
    echo "📋 Test Plan:"
    echo "   1. Test v$OLD_VERSION (without fix) → Should raise ValueError"
    echo "   2. Test v$NEW_VERSION (with fix)    → Should not raise ValueError"
    echo ""

    # Test old version (should raise ValueError)
    test_version "$OLD_VERSION" "RAISE_ERROR"

    echo ""

    # Test new version (should not raise ValueError)
    test_version "$NEW_VERSION" "NO_ERROR"

    echo ""
    echo -e "\033[0;32m========================================================================"
    echo -e "✅ ALL TESTS COMPLETED SUCCESSFULLY"
    echo -e "The forgiving enums feature is working correctly!"
    echo -e "========================================================================\033[0m"
    echo ""
fi
