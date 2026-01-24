#!/bin/bash
# Complete Publishing Script for Comp-LEO SDK v0.3.0

set -e  # Exit on error

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║          Comp-LEO SDK v0.3.0 Publishing Script                   ║"
echo "║          PCI-DSS Payment Compliance Release                       ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Verification
echo "${YELLOW}Step 1: Running verification tests...${NC}"
if ./verify_pci.sh; then
    echo "${GREEN}✅ All verification tests passed${NC}"
else
    echo "${RED}❌ Verification failed. Please fix errors before publishing.${NC}"
    exit 1
fi
echo ""

# Step 2: Clean previous builds
echo "${YELLOW}Step 2: Cleaning previous builds...${NC}"
rm -rf build/ dist/ *.egg-info
echo "${GREEN}✅ Cleaned build directories${NC}"
echo ""

# Step 3: Build package
echo "${YELLOW}Step 3: Building package...${NC}"
python3 -m build
if [ $? -eq 0 ]; then
    echo "${GREEN}✅ Package built successfully${NC}"
    ls -lh dist/
else
    echo "${RED}❌ Build failed${NC}"
    exit 1
fi
echo ""

# Step 4: Check distribution
echo "${YELLOW}Step 4: Checking distribution files...${NC}"
twine check dist/*
if [ $? -eq 0 ]; then
    echo "${GREEN}✅ Distribution files are valid${NC}"
else
    echo "${RED}❌ Distribution check failed${NC}"
    exit 1
fi
echo ""

# Step 5: Test local installation (optional)
echo "${YELLOW}Step 5: Would you like to test local installation? (y/n)${NC}"
read -r test_local

if [ "$test_local" = "y" ]; then
    echo "Creating test environment..."
    python3 -m venv test_env
    source test_env/bin/activate
    
    echo "Installing from wheel..."
    pip install dist/comp_leo-0.3.0-py3-none-any.whl
    
    echo "Testing version..."
    comp-leo --version
    
    echo "Testing PCI check..."
    comp-leo check examples/payment_contract_bad.leo --policy pci-dss-basic | head -30
    
    echo "Cleaning up test environment..."
    deactivate
    rm -rf test_env
    
    echo "${GREEN}✅ Local installation test passed${NC}"
fi
echo ""

# Step 6: Upload confirmation
echo "${YELLOW}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo "${YELLOW}║  Ready to upload to PyPI!                                    ║${NC}"
echo "${YELLOW}║                                                               ║${NC}"
echo "${YELLOW}║  This will publish:                                           ║${NC}"
echo "${YELLOW}║  • comp-leo v0.3.0                                           ║${NC}"
echo "${YELLOW}║  • New Feature: PCI-DSS Compliance                            ║${NC}"
echo "${YELLOW}║  • 7 payment security checks                                  ║${NC}"
echo "${YELLOW}║                                                               ║${NC}"
echo "${YELLOW}║  Once uploaded, this CANNOT be undone!                        ║${NC}"
echo "${YELLOW}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Do you want to upload to PyPI now? (yes/no)"
read -r confirm

if [ "$confirm" != "yes" ]; then
    echo "${YELLOW}⚠️  Upload cancelled. Run this script again when ready.${NC}"
    echo ""
    echo "To upload manually:"
    echo "  twine upload dist/*"
    exit 0
fi

# Step 7: Upload to PyPI
echo "${YELLOW}Step 7: Uploading to PyPI...${NC}"
echo "You will be prompted for your PyPI credentials:"
echo "  Username: __token__"
echo "  Password: <your-pypi-token>"
echo ""

twine upload dist/*

if [ $? -eq 0 ]; then
    echo ""
    echo "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo "${GREEN}║          🎉 SUCCESS! Package published to PyPI! 🎉            ║${NC}"
    echo "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Wait 2-5 minutes for PyPI to process"
    echo "  2. Visit: https://pypi.org/project/comp-leo/"
    echo "  3. Test installation: pip install comp-leo==0.3.0 --no-cache-dir"
    echo "  4. Announce on:"
    echo "     • Twitter/X"
    echo "     • Aleo Discord"
    echo "     • GitHub Releases"
    echo ""
    echo "Installation command for users:"
    echo "  ${GREEN}pip install --upgrade comp-leo${NC}"
    echo ""
    echo "Test PCI-DSS feature:"
    echo "  ${GREEN}comp-leo check payment.leo --policy pci-dss-basic${NC}"
    echo ""
else
    echo "${RED}❌ Upload failed. Please check errors above.${NC}"
    exit 1
fi
