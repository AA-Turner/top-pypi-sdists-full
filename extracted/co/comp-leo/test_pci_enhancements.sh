#!/bin/bash
# Test PCI-DSS Enhancements

set -e

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║          PCI-DSS Enhancement Testing                             ║"
echo "║          v0.4.0 - Standard Policy Pack                           ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

PASS=0
FAIL=0

# Test 1: Import extended module
echo "${YELLOW}Test 1: Importing extended PCI rules...${NC}"
if python3 -c "from comp_leo.payments import check_strong_cryptography, check_multi_signature_requirements; print('✅ Extended module imported')" 2>/dev/null; then
    ((PASS++))
else
    echo "${RED}❌ Failed to import extended module${NC}"
    ((FAIL++))
fi
echo ""

# Test 2: Check standard policy exists
echo "${YELLOW}Test 2: Checking standard policy pack...${NC}"
if [ -f "comp_leo/policies/pci-dss-standard.json" ]; then
    echo "✅ Standard policy pack found"
    ((PASS++))
else
    echo "${RED}❌ Standard policy pack not found${NC}"
    ((FAIL++))
fi
echo ""

# Test 3: Verify policy content
echo "${YELLOW}Test 3: Verifying standard policy content...${NC}"
if python3 -c "
import json
with open('comp_leo/policies/pci-dss-standard.json') as f:
    policy = json.load(f)
    assert len(policy['rules']) == 15, f'Expected 15 rules, got {len(policy[\"rules\"])}'
    assert policy['threshold'] == 90, f'Expected threshold 90, got {policy[\"threshold\"]}'
    print(f'✅ Policy valid: {len(policy[\"rules\"])} rules, threshold {policy[\"threshold\"]}')
" 2>/dev/null; then
    ((PASS++))
else
    echo "${RED}❌ Policy validation failed${NC}"
    ((FAIL++))
fi
echo ""

# Test 4: Test secure configuration check
echo "${YELLOW}Test 4: Testing secure configuration check...${NC}"
if python3 -c "
from comp_leo.payments import check_secure_configuration

test_code = '''
const admin: address = aleo1test123;
const test_mode: bool = true;
'''

issues = check_secure_configuration(test_code, [])
assert len(issues) >= 1, f'Expected violations, got {len(issues)}'
print(f'✅ Detected {len(issues)} configuration issues')
" 2>/dev/null; then
    ((PASS++))
else
    echo "${RED}❌ Secure configuration check failed${NC}"
    ((FAIL++))
fi
echo ""

# Test 5: Test cryptography check
echo "${YELLOW}Test 5: Testing strong cryptography check...${NC}"
if python3 -c "
from comp_leo.payments import check_strong_cryptography

test_code = '''
let hash = md5(data);
let cipher = des_encrypt(data);
'''

issues = check_strong_cryptography(test_code)
assert len(issues) >= 1, f'Expected violations, got {len(issues)}'
print(f'✅ Detected {len(issues)} weak crypto issues')
" 2>/dev/null; then
    ((PASS++))
else
    echo "${RED}❌ Cryptography check failed${NC}"
    ((FAIL++))
fi
echo ""

# Test 6: Test private key detection
echo "${YELLOW}Test 6: Testing private key detection...${NC}"
if python3 -c "
from comp_leo.payments import check_private_key_exposure

test_code = '''
const key = \"APrivateKey1abcdefghijklmnopqrstuvwxyz1234567890abcdefghijklmno\";
'''

issues = check_private_key_exposure(test_code)
assert len(issues) >= 1, f'Expected violations, got {len(issues)}'
print(f'✅ Detected {len(issues)} exposed keys')
" 2>/dev/null; then
    ((PASS++))
else
    echo "${RED}❌ Private key detection failed${NC}"
    ((FAIL++))
fi
echo ""

# Test 7: Test with bad contract using standard policy
echo "${YELLOW}Test 7: Testing bad contract with standard policy...${NC}"
if comp-leo check examples/payment_contract_bad.leo --policy pci-dss-standard 2>&1 | grep -q "Violation"; then
    echo "✅ Standard policy detects violations"
    ((PASS++))
else
    echo "${RED}❌ Standard policy check failed${NC}"
    ((FAIL++))
fi
echo ""

# Test 8: Verify standard has more rules than basic
echo "${YELLOW}Test 8: Comparing basic vs standard policies...${NC}"
if python3 -c "
import json

with open('comp_leo/policies/pci-dss-basic.json') as f:
    basic = json.load(f)

with open('comp_leo/policies/pci-dss-standard.json') as f:
    standard = json.load(f)

basic_rules = len(basic['rules'])
standard_rules = len(standard['rules'])

assert standard_rules > basic_rules, f'Standard should have more rules: {standard_rules} vs {basic_rules}'
print(f'✅ Standard has more rules: {standard_rules} vs {basic_rules}')
" 2>/dev/null; then
    ((PASS++))
else
    echo "${RED}❌ Policy comparison failed${NC}"
    ((FAIL++))
fi
echo ""

# Test 9: Test multi-sig detection
echo "${YELLOW}Test 9: Testing multi-signature detection...${NC}"
if python3 -c "
from comp_leo.payments import check_multi_signature_requirements
from comp_leo.analyzer.parser import LeoFunction

# Mock transition
class MockTransition:
    def __init__(self):
        self.name = 'pause_contract'
        self.body = 'Mapping::set(paused, true);'
        self.line_start = 1

transitions = [MockTransition()]
issues = check_multi_signature_requirements(transitions, '')

assert len(issues) >= 1, f'Expected violations, got {len(issues)}'
print(f'✅ Detected {len(issues)} multi-sig issues')
" 2>/dev/null; then
    ((PASS++))
else
    echo "${RED}❌ Multi-sig detection failed${NC}"
    ((FAIL++))
fi
echo ""

# Test 10: Test vulnerability detection
echo "${YELLOW}Test 10: Testing vulnerability detection...${NC}"
if python3 -c "
from comp_leo.payments import check_common_vulnerabilities

test_code = '''
transition risky() {
    let result = external.aleo/transfer();
    Mapping::set(balances, caller, amount);
}
'''

class MockTransition:
    def __init__(self):
        self.name = 'risky'
        self.body = test_code
        self.line_start = 1

transitions = [MockTransition()]
issues = check_common_vulnerabilities(test_code, transitions)

print(f'✅ Vulnerability detection tested ({len(issues)} issues found)')
" 2>/dev/null; then
    ((PASS++))
else
    echo "${RED}❌ Vulnerability detection failed${NC}"
    ((FAIL++))
fi
echo ""

# Results
echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║                      TEST RESULTS                                 ║"
echo "╠═══════════════════════════════════════════════════════════════════╣"
printf "║  ✅ Passed: %-3d tests                                             ║\n" $PASS
printf "║  ❌ Failed: %-3d tests                                             ║\n" $FAIL
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "${GREEN}🎉 ALL TESTS PASSED! PCI-DSS enhancements are working!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Test with real contracts"
    echo "  2. Update version to 0.4.0"
    echo "  3. Update README"
    echo "  4. Publish new version"
    exit 0
else
    echo "${RED}⚠️  Some tests failed. Please review and fix.${NC}"
    exit 1
fi
