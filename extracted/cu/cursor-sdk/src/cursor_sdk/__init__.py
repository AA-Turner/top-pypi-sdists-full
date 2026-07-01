"""cursor-sdk source distribution stub.

The real package ships as platform-specific wheels that bundle the
cursor-sdk-bridge binary. Source installs cannot embed that binary
(there is no build-from-source path), so this stub raises at import to
prevent silently broken environments. See https://docs.cursor.com/sdk
for install instructions.
"""

raise ImportError(
    "cursor-sdk requires a binary wheel; pip resolved the source "
    "distribution instead. Re-run with --only-binary=cursor-sdk "
    "(or remove --no-binary :all:) and ensure your platform has a "
    "matching wheel on PyPI. Supported platforms: macOS arm64/x64, "
    "Linux arm64/x64, Windows x64."
)
