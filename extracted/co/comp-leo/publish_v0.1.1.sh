#!/bin/bash
# Quick publish script for v0.1.1

set -e

echo "🚀 Publishing Comp-LEO SDK v0.1.1"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Clean previous builds
echo "1️⃣  Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info comp_leo.egg-info 2>/dev/null || true

# Build
echo "2️⃣  Building package..."
python3 -m build

# Check
echo "3️⃣  Checking package..."
twine check dist/*

# Show what will be uploaded
echo ""
echo "📦 Package contents:"
ls -lh dist/

echo ""
read -p "Upload to PyPI? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "4️⃣  Uploading to PyPI..."
    twine upload dist/*
    
    echo ""
    echo "✅ Published! View at: https://pypi.org/project/comp-leo/0.1.1/"
    echo ""
    echo "Test installation:"
    echo "  pip install --upgrade comp-leo"
    echo "  comp-leo --version"
else
    echo "❌ Upload cancelled"
fi
