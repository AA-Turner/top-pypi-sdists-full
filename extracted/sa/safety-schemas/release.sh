#!/bin/bash

# Exit script on error
set -e

# Ensure the version is passed as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <new_version>"
    exit 1
fi

NEW_VERSION=$1

# Validate the version follows semantic versioning (X.Y.Z)
if [[ ! "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in format X.Y.Z (e.g., 1.0.0)"
    exit 1
fi

# Pull the latest changes from the main branch
echo "Pulling latest changes..."
git pull origin main

# Verify the latest commit
echo "Verifying the latest commit..."
git log -1

# Ask for user confirmation to proceed
read -r -p "Is this the correct commit? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ]; then
    echo "Aborting the release process."
    exit 1
fi

# Create a new tag
echo "Creating a new tag for version $NEW_VERSION..."
git tag -s -a "$NEW_VERSION" -m "Version $NEW_VERSION"

# Push the new tag to GitHub
echo "Pushing the tag to GitHub..."
git push origin "$NEW_VERSION"

# Verify the tag on GitHub
echo "Tag created. Verify it here: https://github.com/pyupio/safety_schemas/tags"

# Remove any existing dist folder to avoid conflicts
echo "Cleaning up old builds..."
rm -rf dist

# Build the package using Hatch
echo "Building the package..."
hatch build

# Publish the package to PyPI
echo "Publishing the package to PyPI..."
hatch publish -u "__token__"

# Verify the release on PyPI
echo "Verify the new release here: https://pypi.org/project/safety-schemas/"
