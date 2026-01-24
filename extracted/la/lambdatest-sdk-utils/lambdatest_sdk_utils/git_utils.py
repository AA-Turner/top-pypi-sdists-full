import os
import json
import subprocess
from typing import Optional, Dict


class GitInfo:
    def __init__(self, branch: str = "", commit_id: str = "", commit_message: str = "", 
                 commit_author: str = "", github_url: str = "", baseline_branch: str = ""):
        self.branch = branch
        self.commit_id = commit_id
        self.commit_message = commit_message
        self.commit_author = commit_author
        self.github_url = github_url
        self.baseline_branch = baseline_branch

    def to_dict(self):
        return {
            "branch": self.branch,
            "commitId": self.commit_id,
            "commitMessage": self.commit_message,
            "commitAuthor": self.commit_author,
            "githubURL": self.github_url,
            "baselineBranch": self.baseline_branch
        }


def get_git_info(env_vars: Optional[Dict[str, str]] = None) -> Optional[GitInfo]:
    """
    Extract git information from file or git commands.
    
    Args:
        env_vars: Dictionary of environment variables
        
    Returns:
        GitInfo object or None if extraction fails
    """
    if env_vars is None:
        env_vars = dict(os.environ)
    
    git_info_filepath = env_vars.get("SMARTUI_GIT_INFO_FILEPATH")
    if git_info_filepath:
        return _read_git_info_from_file(git_info_filepath, env_vars)
    else:
        return _fetch_git_info_from_commands(env_vars)


def _read_git_info_from_file(filepath: str, env_vars: Dict[str, str]) -> Optional[GitInfo]:
    """Read git information from a JSON file."""
    try:
        with open(filepath, 'r') as f:
            git_info = json.load(f)
        
        return GitInfo(
            branch=env_vars.get("CURRENT_BRANCH", git_info.get("branch", "")),
            commit_id=_shorten_commit_id(git_info.get("commit_id", "")),
            commit_message=git_info.get("commit_body", ""),
            commit_author=git_info.get("commit_author", ""),
            github_url=_get_github_url(env_vars, git_info.get("commit_id", "")),
            baseline_branch=env_vars.get("BASELINE_BRANCH", "")
        )
    except Exception as e:
        return None


def _fetch_git_info_from_commands(env_vars: Dict[str, str]) -> GitInfo:
    """Fetch git information using git commands."""
    try:
        # Get commit info
        commit_command = 'git log -1 --pretty=format:"%h|%H|%s|%an"'
        commit_output = _execute_command(commit_command)
        
        if not commit_output:
            return GitInfo()
        
        # Get branch name
        branch_command = 'git rev-parse --abbrev-ref HEAD'
        branch_output = _execute_command(branch_command)
        branch = env_vars.get("CURRENT_BRANCH", branch_output.strip() if branch_output else "")
        
        # Parse commit output
        parts = commit_output.strip().split('|')
        if len(parts) >= 4:
            commit_id_short = parts[0]
            commit_id_full = parts[1]
            commit_message = parts[2]
            commit_author = parts[3]
        else:
            commit_id_short = ""
            commit_id_full = ""
            commit_message = ""
            commit_author = ""
        
        return GitInfo(
            branch=branch,
            commit_id=commit_id_short,
            commit_message=commit_message,
            commit_author=commit_author,
            github_url=_get_github_url(env_vars, commit_id_full),
            baseline_branch=env_vars.get("BASELINE_BRANCH", "")
        )
    except Exception:
        return GitInfo()


def _execute_command(command: str) -> str:
    """Execute a shell command and return the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception:
        return ""


def _shorten_commit_id(commit_id: str) -> str:
    """Shorten commit ID to 6 characters."""
    if commit_id and len(commit_id) >= 6:
        return commit_id[:6]
    return commit_id


def _get_github_url(env_vars: Dict[str, str], commit_id: str) -> str:
    """Generate GitHub URL if in GitHub Actions."""
    if env_vars.get("GITHUB_ACTIONS"):
        repo = os.environ.get("GITHUB_REPOSITORY", "")
        if repo and commit_id:
            return f"https://api.github.com/repos/{repo}/statuses/{commit_id}"
    return ""

