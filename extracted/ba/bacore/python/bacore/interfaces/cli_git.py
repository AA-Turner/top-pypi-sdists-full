"""Git interface."""
import subprocess as sup
from pathlib import Path


def git_update_remote(repo: Path, remote: str, commit_msg: str, branch: str = "main", rebase: bool = False) -> None:
    """Push latest changes in repository to remote.

    Use case for this function is only simple automations.

    Parameters:
        repo: Path to the repository
        remote: Remote repository
        commit_msg: The commit message for the commit.
        branch: Branch to commit. Defaults to "master".
        rebase: If rebasing should be done when pulling. Default is False.
    """
    sup.run(["git", "-C", repo, "add", "-A"])
    sup.run(["git", "-C", repo, "commit", "-m", commit_msg])
    if rebase:
        sup.run(["git", "-C", repo, "pull", "--rebase"])
    sup.run(["git", "-C", repo, "push", remote, branch])
