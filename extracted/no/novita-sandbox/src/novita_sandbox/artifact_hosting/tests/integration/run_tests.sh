#!/bin/bash
# Integration Test Runner with Detailed Reports
# 
# Usage:
#   ./run_tests.sh                 # Run all integration tests
#   ./run_tests.sh -v              # Verbose mode (show all SDK logs)
#   ./run_tests.sh --no-cleanup    # Skip resource cleanup (for debugging)
#   ./run_tests.sh -k "cancel"     # Run specific tests
#
# Environment Variables (set in .env or export):
#   NOVITA_API_KEY           - API key for authentication
#   SANDBOX_TEMPLATE         - Sandbox template name (default: base)
#
# Note: API URL is fixed at https://artifact.novita.ai/v1 (not configurable)
#
# Note: Sandbox is automatically created and cleaned up by the test suite.
#       Use --no-cleanup to keep resources for debugging.

set -e

# Navigate to sdk-python directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SDK_DIR="$(cd "$SCRIPT_DIR/../../../../.." && pwd)"
cd "$SDK_DIR"

# Load environment variables from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Generate timestamp for reports
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOGS_DIR="$(cd "$SDK_DIR/.." && pwd)/logs"
mkdir -p "$LOGS_DIR"

# Default SDK log level
SDK_LOG_LEVEL="${SDK_LOG_LEVEL:-INFO}"
NO_CLEANUP=""

# Parse arguments
PYTEST_ARGS=""
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            SDK_LOG_LEVEL="DEBUG"
            shift
            ;;
        --no-cleanup)
            NO_CLEANUP="--no-cleanup"
            shift
            ;;
        *)
            PYTEST_ARGS="$PYTEST_ARGS $1"
            shift
            ;;
    esac
done

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           Artifact Hosting SDK - Integration Tests               ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Configuration:"
echo "   API URL: https://artifact.novita.ai/v1 (fixed)"
echo "   Log Level: $SDK_LOG_LEVEL"
echo "   Cleanup: ${NO_CLEANUP:-enabled}"
echo ""

# Run tests with reports
export SDK_LOG_LEVEL
poetry run pytest \
    src/novita_sandbox/artifact_hosting/tests/integration/test_deploy_flow.py \
    -v \
    --tb=long \
    --capture=tee-sys \
    -p no:xdist \
    --html="$LOGS_DIR/test_report_${TIMESTAMP}.html" \
    --self-contained-html \
    --json-report \
    --json-report-file="$LOGS_DIR/test_report_${TIMESTAMP}.json" \
    --json-report-indent=2 \
    $NO_CLEANUP \
    $PYTEST_ARGS

# Print report locations
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                         Test Reports                             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📝 Log file:    $LOGS_DIR/integration_test_${TIMESTAMP}.log"
echo "📊 HTML report: $LOGS_DIR/test_report_${TIMESTAMP}.html"
echo "📋 JSON report: $LOGS_DIR/test_report_${TIMESTAMP}.json"
echo ""
echo "Open HTML report: open \"$LOGS_DIR/test_report_${TIMESTAMP}.html\""

# Parse and display failure report
if [ -f "$LOGS_DIR/test_report_${TIMESTAMP}.json" ]; then
    echo ""
    python "$SCRIPT_DIR/parse_report.py" "$LOGS_DIR/test_report_${TIMESTAMP}.json"
fi
