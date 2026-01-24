#!/bin/bash
# PCI-DSS Implementation Verification Script

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     PCI-DSS Implementation Verification                       ║"
echo "║     Comp-LEO SDK v0.3.0                                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

PASS=0
FAIL=0

# Test 1: Check if PCI module can be imported
echo "🔍 Test 1: Importing PCI payment module..."
if python3 -c "from comp_leo.payments import is_payment_function; print('✅ PCI module imported')" 2>/dev/null; then
    ((PASS++))
else
    echo "❌ Failed to import PCI module"
    ((FAIL++))
fi
echo ""

# Test 2: Check if policy file exists
echo "🔍 Test 2: Checking PCI-DSS policy pack..."
if [ -f "comp_leo/policies/pci-dss-basic.json" ]; then
    echo "✅ PCI-DSS policy pack found"
    ((PASS++))
else
    echo "❌ PCI-DSS policy pack not found"
    ((FAIL++))
fi
echo ""

# Test 3: Check compliant contract (should pass)
echo "🔍 Test 3: Testing compliant contract..."
if comp-leo check examples/payment_contract_compliant.leo --policy pci-dss-basic 2>&1 | grep -q "PASSED"; then
    echo "✅ Compliant contract passed"
    ((PASS++))
else
    echo "❌ Compliant contract did not pass"
    ((FAIL++))
fi
echo ""

# Test 4: Check non-compliant contract (should fail)
echo "🔍 Test 4: Testing non-compliant contract..."
if comp-leo check examples/payment_contract_bad.leo --policy pci-dss-basic 2>&1 | grep -q "FAILED"; then
    echo "✅ Non-compliant contract failed as expected"
    ((PASS++))
else
    echo "❌ Non-compliant contract should have failed"
    ((FAIL++))
fi
echo ""

# Test 5: Check for critical violations in bad contract
echo "🔍 Test 5: Checking for critical violations..."
if comp-leo check examples/payment_contract_bad.leo --policy pci-dss-basic 2>&1 | grep -q "CRITICAL"; then
    echo "✅ Critical violations detected"
    ((PASS++))
else
    echo "❌ No critical violations detected"
    ((FAIL++))
fi
echo ""

# Test 6: Check PCI function detection
echo "🔍 Test 6: Testing PCI function detection..."
if python3 -c "from comp_leo.payments import is_payment_function; assert is_payment_function('process_payment', '') == True; print('✅ Payment function detection works')" 2>/dev/null; then
    ((PASS++))
else
    echo "❌ Payment function detection failed"
    ((FAIL++))
fi
echo ""

# Test 7: Check forbidden data detection
echo "🔍 Test 7: Testing forbidden data detection..."
if python3 -c "from comp_leo.payments import detect_forbidden_payment_data; result = detect_forbidden_payment_data('cvv'); assert result['detected'] == True; print('✅ Forbidden data detection works')" 2>/dev/null; then
    ((PASS++))
else
    echo "❌ Forbidden data detection failed"
    ((FAIL++))
fi
echo ""

# Test 8: Check documentation
echo "🔍 Test 8: Checking documentation..."
if [ -f "PCI_DSS_GUIDE.md" ] && [ -f "comp_leo/payments/README.md" ]; then
    echo "✅ Documentation complete"
    ((PASS++))
else
    echo "❌ Documentation incomplete"
    ((FAIL++))
fi
echo ""

# Results
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    VERIFICATION RESULTS                        ║"
echo "╠════════════════════════════════════════════════════════════════╣"
echo "║  ✅ Passed: $PASS tests                                           "
echo "║  ❌ Failed: $FAIL tests                                           "
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED! PCI-DSS implementation is ready!"
    echo ""
    echo "Next steps:"
    echo "  1. Build: python3 -m build"
    echo "  2. Upload: twine upload dist/*"
    echo "  3. Announce: Share on Twitter, Aleo Discord"
    exit 0
else
    echo "⚠️  Some tests failed. Please review and fix."
    exit 1
fi
