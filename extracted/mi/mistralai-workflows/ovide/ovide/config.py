from pathlib import Path

VALID_BUMPS = ("major", "minor", "patch")
VALID_KINDS = ("Added", "Changed", "Deprecated", "Removed", "Fixed", "Security")

BUMP_PRIORITY = {bump: i for i, bump in enumerate(VALID_BUMPS)}

CHANGELOG_DIR = Path("changelog.d")
CHANGELOG_FILE = Path("CHANGELOG.md")
