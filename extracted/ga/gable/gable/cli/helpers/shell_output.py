import os


def shell_linkify(url: str, title: str) -> str:
    """Returns a string that will display as a clickable link in the terminal"""
    return f"\033]8;;{url}\a{title}\033]8;;\a"


def in_ci() -> bool:
    """Returns True if running in a CI environment. Confirmed for GitHub, GitLab, and CircleCI."""
    # https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables
    # https://docs.gitlab.com/ee/ci/variables/predefined_variables.html
    # https://circleci.com/docs/variables/#built-in-environment-variables
    return os.environ.get("CI") == "true"


def shell_linkify_if_not_in_ci(url: str, title: str) -> str:
    """Returns a string that will display as a clickable link in the terminal if not in CI, otherwise just the title."""
    return shell_linkify(url, title) if not in_ci() else title
