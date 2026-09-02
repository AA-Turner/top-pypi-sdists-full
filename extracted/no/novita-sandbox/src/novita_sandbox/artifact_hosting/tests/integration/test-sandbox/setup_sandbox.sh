#!/bin/bash
# Create test sandbox and return sandbox information
#
# Usage:
#   ./setup_sandbox.sh                       # Create sandbox
#   ./setup_sandbox.sh --output result.json  # Output to file
#   ./setup_sandbox.sh --timeout 1800        # Specify timeout
#
# Output format (JSON):
#   {
#     "sandbox_id": "xxx",
#     "app_dir": "/app",
#     "files": ["/app/index.html"],
#     "dockerfile": "..."
#   }
#
# Note: Sandbox will not be automatically cleaned up, please run after testing:
#   python3 cleanup_sandbox.py <sandbox_id>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ensure Python environment has dependencies installed
if ! python3 -c "import novita_sandbox" 2>/dev/null; then
    echo "Installing novita-sandbox dependencies..." >&2
    pip3 install -q -r "$SCRIPT_DIR/requirements.txt"
fi

# Run Python script
python3 "$SCRIPT_DIR/sandbox_test.py" "$@"
