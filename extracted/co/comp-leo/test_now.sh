#!/bin/bash
# Quick test script for Comp-LEO SDK

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Comp-LEO SDK - Quick Test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.10+"; exit 1; }
echo "✅ Python OK"
echo ""

# Install dependencies
echo "📦 Installing Comp-LEO SDK..."
cd "$(dirname "$0")"
pip3 install -e . --quiet || pip3 install -e .
echo "✅ SDK installed"
echo ""

# Verify CLI works
echo "🔍 Verifying CLI installation..."
comp-leo --version || python3 -m comp_leo.cli.main --version
echo "✅ CLI working"
echo ""

# Test on sbom_registry
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Test 1: SBOM Registry Program"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

SBOM_FILE="../compliedger-aleo/programs/sbom_registry/src/main.leo"

if [ -f "$SBOM_FILE" ]; then
    comp-leo check "$SBOM_FILE" --threshold 70 || python3 -m comp_leo.cli.main check "$SBOM_FILE" --threshold 70
    echo ""
else
    echo "⚠️  SBOM Registry file not found at $SBOM_FILE"
fi

# Test on compliance_oracle
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Test 2: Compliance Oracle Program"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

ORACLE_FILE="../compliedger-aleo/programs/compliance_oracle/src/main.leo"

if [ -f "$ORACLE_FILE" ]; then
    comp-leo check "$ORACLE_FILE" --threshold 70 || python3 -m comp_leo.cli.main check "$ORACLE_FILE" --threshold 70
    echo ""
else
    echo "⚠️  Compliance Oracle file not found at $ORACLE_FILE"
fi

# Test on entire directory
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Test 3: All Programs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

PROGRAMS_DIR="../compliedger-aleo/programs"

if [ -d "$PROGRAMS_DIR" ]; then
    comp-leo check "$PROGRAMS_DIR" --threshold 70 --output test-results.json || \
        python3 -m comp_leo.cli.main check "$PROGRAMS_DIR" --threshold 70 --output test-results.json
    echo ""
    
    if [ -f "test-results.json" ]; then
        echo "✅ Results saved to test-results.json"
        echo ""
        echo "📊 Quick stats:"
        python3 -c "import json; r=json.load(open('test-results.json')); print(f'  Score: {r[\"score\"]}/100'); print(f'  Violations: {len(r[\"violations\"])}'); print(f'  Critical: {r[\"critical_count\"]}'); print(f'  High: {r[\"high_count\"]}')"
    fi
else
    echo "⚠️  Programs directory not found at $PROGRAMS_DIR"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ Testing Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "  • Review violations in the output above"
echo "  • Check test-results.json for detailed report"
echo "  • Run: comp-leo report $PROGRAMS_DIR -o report.html"
echo ""
