"""Version information for dealcloud-sdk.

This file is automatically updated during the CI build process.
Do not edit manually - changes will be overwritten.
"""

# Package name (should not change)
PACKAGE_NAME = "dealcloud-sdk"

# Version is injected at build time by CI pipeline
# Format: MAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH+PRERELEASE
__version__ = "1.0.18"

# SDK version string for X-Dealcloud-Sdk-Version header
# Format: {package_name}.{version}
SDK_VERSION = f"{PACKAGE_NAME}.{__version__}"

