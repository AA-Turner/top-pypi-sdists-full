"""
Parse & construct GitHub repository URLs & specifiers

``ghrepo`` extracts a GitHub repository's owner & name from various GitHub URL
formats (or just from a string of the form ``OWNER/REPONAME`` or ``REPONAME``),
and the resulting object provides properties for going in reverse to determine
the possible URLs.  Also included is a function for determining the GitHub
owner & name for a local Git repository, plus a couple of other useful Git
repository inspection functions.

Visit <https://github.com/jwodder/ghrepo> for more information.
"""

from __future__ import annotations
from collections.abc import Callable
from os import PathLike
import re
import subprocess
from typing import NamedTuple, Optional, Union

__version__ = "0.7.1"
__author__ = "John Thorvald Wodder II"
__author_email__ = "ghrepo@varonathe.org"
__license__ = "MIT"
__url__ = "https://github.com/jwodder/ghrepo"

__all__ = [
    "DetachedHeadError",
    "GHRepo",
    "GH_REPO_RGX",
    "GH_USER_RGX",
    "NoSuchRemoteError",
    "NoUpstreamError",
    "get_current_branch",
    "get_local_repo",
    "is_git_repo",
]

AnyPath = Union[str, bytes, "PathLike[str]", "PathLike[bytes]"]

#: Regular expression for a valid GitHub username or organization name.  As of
#: 2017-07-23, trying to sign up to GitHub with an invalid username or create
#: an organization with an invalid name gives the message "Username may only
#: contain alphanumeric characters or single hyphens, and cannot begin or end
#: with a hyphen".  Additionally, trying to create a user named "none" (case
#: insensitive) gives the message "Username name 'none' is a reserved word."
#:
#: Unfortunately, there are a number of users who made accounts before the
#: current name restrictions were put in place, and so this regex also needs to
#: accept names that contain underscores, contain multiple consecutive hyphens,
#: begin with a hyphen, and/or end with a hyphen.
GH_USER_RGX = r"(?![Nn][Oo][Nn][Ee]($|[^-A-Za-z0-9]))[-_A-Za-z0-9]+"

#: Regular expression for a valid GitHub repository name.  Testing as of
#: 2017-05-21 indicates that repository names can be composed of alphanumeric
#: ASCII characters, hyphens, periods, and/or underscores, with the names ``.``
#: and ``..`` being reserved and names ending with ``.git`` (case insensitive)
#: forbidden.
GH_REPO_RGX = (
    r"(?:\.?[-A-Za-z0-9_][-A-Za-z0-9_.]*|\.\.[-A-Za-z0-9_.]+)(?<!\.[Gg][Ii][Tt])"
)

#: Convenience regular expression for ``<owner>/<name>``, including named
#: capturing groups
OWNER_NAME = rf"(?P<owner>{GH_USER_RGX})/(?P<name>{GH_REPO_RGX})"

OWNER_REPO_CRGX = re.compile(rf"(?:(?P<owner>{GH_USER_RGX})/)?(?P<name>{GH_REPO_RGX})")

GITHUB_URL_CREGEXEN = [
    re.compile(
        r"(?:(?i:https?)://(?:(?:[A-Za-z0-9-._~!$&'()*+,;=:]|%[0-9a-fA-F]{2})*@)?)?"
        rf"(?i:(?:www\.)?github\.com)/{OWNER_NAME}(?:\.git)?/?"
    ),
    re.compile(rf"(?i:https?://)?(?i:api\.github\.com)/repos/{OWNER_NAME}"),
    re.compile(rf"(?i:git://github\.com)/{OWNER_NAME}(?:\.git)?"),
    re.compile(rf"git@(?i:github\.com):{OWNER_NAME}(?:\.git)?"),
    re.compile(rf"(?i:ssh://)git@(?i:github\.com)/{OWNER_NAME}(?:\.git)?"),
]


class GHRepo(NamedTuple):
    """
    A pair of a GitHub repository's owner and base name.  Stringifying a
    `GHRepo` instance produces a repository "fullname" of the form
    ``{owner}/{name}``.
    """

    owner: str
    name: str

    def __str__(self) -> str:
        return f"{self.owner}/{self.name}"

    @property
    def api_url(self) -> str:
        """
        The base URL for accessing the repository via the GitHub REST API; this
        is a string of the form
        ``https://api.github.com/repos/{owner}/{name}``.
        """
        return f"https://api.github.com/repos/{self.owner}/{self.name}"

    @property
    def clone_url(self) -> str:
        """The URL for cloning the repository over HTTPS"""
        return f"https://github.com/{self.owner}/{self.name}.git"

    @property
    def git_url(self) -> str:
        """The URL for cloning the repository via the native Git protocol"""
        return f"git://github.com/{self.owner}/{self.name}.git"

    @property
    def html_url(self) -> str:
        """The URL for the repository's web interface"""
        return f"https://github.com/{self.owner}/{self.name}"

    @property
    def ssh_url(self) -> str:
        """The URL for cloning the repository over SSH"""
        return f"git@github.com:{self.owner}/{self.name}.git"

    @classmethod
    def parse(
        cls,
        spec: str,
        default_owner: Optional[str | Callable[[], str]] = None,
    ) -> GHRepo:
        """
        Parse a GitHub repository specifier.  This can be either a URL (as
        accepted by `parse_url()`) or a string in the form ``{owner}/{name}``.
        If ``default_owner`` is specified (as either a string or a
        zero-argument callable that returns a string), strings that are just a
        repository name are also accepted, and the resulting `GHRepo` instances
        will have their ``owner`` set to the given value.
        """
        m = OWNER_REPO_CRGX.fullmatch(spec)
        if m:
            owner = m["owner"]
            if owner is None:
                # <https://github.com/python/typeshed/issues/5546>
                if default_owner is None:  # type: ignore[unreachable]
                    raise ValueError(f"No owner given in {spec!r}")
                elif callable(default_owner):
                    owner = default_owner()
                else:
                    owner = default_owner
            name = m["name"]
            assert name is not None
            return cls(owner=owner, name=name)
        else:
            return cls.parse_url(spec)

    @classmethod
    def parse_url(cls, url: str) -> GHRepo:
        """
        Parse a GitHub repository URL.  The following URL formats are
        recognized:

        - ``[http[s]://[<username>[:<password>]@]][www.]github.com/<owner>/<name>\
          [.git][/]``
        - ``[http[s]://]api.github.com/repos/<owner>/<name>``
        - ``git://github.com/<owner>/<name>[.git]``
        - ``git@github.com:<owner>/<name>[.git]``
        - ``ssh://git@github.com/<owner>/<name>[.git]``

        All other formats produce a `ValueError`.
        """
        for crgx in GITHUB_URL_CREGEXEN:
            m = crgx.fullmatch(url)
            if m:
                return cls(owner=m["owner"], name=m["name"])
        else:
            raise ValueError(f"Invalid GitHub URL: {url!r}")


def get_local_repo(dirpath: Optional[AnyPath] = None, remote: str = "origin") -> GHRepo:
    """
    Determine the GitHub repository for the Git repository located at or
    containing the directory ``dirpath`` (default: the current directory) by
    parsing the URL for the specified remote.  Raises `NoSuchRemoteError` if
    the given remote does not exist.  Raises `subprocess.CalledProcessError` if
    a different Git error occurs, such as the given path not being in a Git
    repository.
    """
    try:
        url = readgit("remote", "get-url", "--", remote, dirpath=dirpath)
    except subprocess.CalledProcessError as e:
        if e.returncode == 2:
            raise NoSuchRemoteError(remote)
        else:
            raise
    return GHRepo.parse_url(url)


def get_branch_upstream(branch: str, dirpath: Optional[AnyPath] = None) -> GHRepo:
    """
    .. versionadded:: 0.5.0

    Determine the GitHub repository for the upstream remote of the given branch
    in the Git repository located at or containing the directory ``dirpath``
    (default: the current directory).

    Raises `NoUpstreamError` if the given branch does not have an upstream
    remote configured (This includes the situation in which the branch does not
    exist).  Raises `subprocess.CalledProcessError` if a different Git error
    occurs, such as the given path not being in a Git repository.
    """
    try:
        upstream = readgit(
            "config", "--get", "--", f"branch.{branch}.remote", dirpath=dirpath
        )
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            raise NoUpstreamError(branch)
        else:
            raise  # pragma: no cover
    return get_local_repo(dirpath, remote=upstream)


def get_current_branch(dirpath: Optional[AnyPath] = None) -> str:
    """
    Get the current branch for the Git repository located at or containing the
    directory ``dirpath`` (default: the current directory).  Raises
    `DetachedHeadError` if the repository is in a detached ``HEAD`` state.
    Raises `subprocess.CalledProcessError` if a different Git error occurs,
    such as the given path not being in a Git repository.
    """
    try:
        return readgit("symbolic-ref", "--short", "-q", "HEAD", dirpath=dirpath)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            raise DetachedHeadError()
        else:
            raise  # pragma: no cover


def is_git_repo(dirpath: Optional[AnyPath] = None) -> bool:
    """
    Tests whether the given directory (default: the current directory) is
    either a Git repository or contained in one
    """
    r = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=dirpath,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return bool(r.returncode == 0)


def readgit(*args: str, dirpath: Optional[AnyPath]) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=dirpath,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    ).stdout.strip()


class NoSuchRemoteError(Exception):
    """
    Raised by `get_local_repo()` when the given remote does not exist in the
    Git repository
    """

    def __init__(self, remote: str) -> None:
        #: The queried remote
        self.remote = remote

    def __str__(self) -> str:
        return f"Remote not found in Git repository: {self.remote!r}"


class DetachedHeadError(Exception):
    """
    Raised by `get_current_branch()` if the Git repository is in a detached
    ``HEAD`` state
    """

    def __str__(self) -> str:
        return "Git repository is in a detached HEAD state"


class NoUpstreamError(Exception):
    """
    Raised by `get_branch_upstream()` if the given branch does not have a
    remote configured
    """

    def __init__(self, branch: str) -> None:
        #: The branch in question
        self.branch = branch

    def __str__(self) -> str:
        return f"No upstream remote configured for Git branch: {self.branch!r}"
