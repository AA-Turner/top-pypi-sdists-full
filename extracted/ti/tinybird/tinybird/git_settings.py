from enum import Enum
from typing import Dict, Optional


class GitHubSettingsStatus(Enum):
    IDLE = "idle"
    LINKED = "linked"
    SYNCED = "synced"
    SYNCING = "syncing"
    UNLINKED = "unlinked"
    CLI = "cli"


def has_legacy_git_remote(remote: Optional[Dict[str, str]]) -> bool:
    return bool(
        remote
        and (
            remote.get("provider")
            or remote.get("status")
            in {
                GitHubSettingsStatus.LINKED.value,
                GitHubSettingsStatus.SYNCING.value,
                GitHubSettingsStatus.SYNCED.value,
            }
        )
    )


def unlinked_remote() -> Dict[str, str]:
    """Return the workspace `remote` value for a workspace that is not connected to a Git provider."""
    return {
        "provider": "",
        "owner": "",
        "owner_type": "",
        "remote": "",
        "name": "",
        "access_token": "",
        "branch": "",
        "project_path": "",
        "last_commit_sha": "",
        "status": GitHubSettingsStatus.UNLINKED.value,
    }


DEFAULT_TINYENV_FILE = """
VERSION=0.0.0



##########
# OPTIONAL env vars

# Don't print CLI version warning message if there's a new available version
# TB_VERSION_WARNING=0

# Skip regression tests
# TB_SKIP_REGRESSION=0

# Use `OBFUSCATE_REGEX_PATTERN` and `OBFUSCATE_PATTERN_SEPARATOR` environment variables to define a regex pattern and a separator (in case of a single string with multiple regex) to obfuscate secrets in the CLI output.
# OBFUSCATE_REGEX_PATTERN="https://(www\\.)?[^/]+||^Follow these instructions =>"
# OBFUSCATE_PATTERN_SEPARATOR=||
##########
"""
