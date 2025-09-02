import asyncio
import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from subprocess import (  # nosec
    SubprocessError,
)

from git.exc import GitError
from git.repo import Repo

from .classes import (
    CommitInfo,
    InvalidParameter,
    RebaseResult,
)
from .clone import (
    call_codecommit_clone,
    https_clone,
    ssh_clone,
)
from .download_repo import (
    download_repo_from_s3,
    remove_symlinks_in_directory,
    reset_repo,
)
from .https_utils import (
    https_ls_remote,
)
from .remote import (
    ls_remote,
)
from .ssh_utils import (
    ssh_ls_remote,
)

LOGGER = logging.getLogger(__name__)

__all__ = [
    # Classes
    "CommitInfo",
    "InvalidParameter",
    "RebaseResult",
    # Helpers
    "clone",
    "disable_quotepath",
    "download_repo_from_s3",
    "get_head_commit",
    "get_last_commit_info_new",
    "get_line_author",
    "get_modified_filenames",
    "https_clone",
    "https_ls_remote",
    "is_commit_in_branch",
    "ls_remote",
    "rebase",
    "remove_symlinks_in_directory",
    "reset_repo",
    "ssh_clone",
    "ssh_ls_remote",
]


async def disable_quotepath(git_path: str) -> None:
    await asyncio.create_subprocess_exec(
        "git",
        f"--git-dir={git_path}",
        "config",
        "core.quotepath",
        "off",
    )


async def get_last_commit_info_new(
    repo_path: str,
    filename: str,
) -> CommitInfo | None:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "log",
        "--max-count",
        "1",
        "--format=%H%n%ce%n%cI",
        "--",
        filename,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        cwd=repo_path,
    )
    stdout, stderr = await proc.communicate()
    git_log = stdout.decode().splitlines()

    if stderr or proc.returncode != 0 or not git_log:
        return None

    return CommitInfo(
        hash=git_log[0],
        author=git_log[1],
        modified_date=datetime.fromisoformat(git_log[2]),
    )


async def get_line_author(
    repo_path: str,
    filename: str,
    line: int,
    rev: str = "HEAD",
) -> CommitInfo | None:
    try:
        proc = await asyncio.create_subprocess_exec(
            "git",
            "blame",
            "-L",
            f"{line!s},+1",
            "-l",
            "-p",
            "-M",
            "-C",
            "-C",
            rev,
            "--",
            filename,
            stderr=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            cwd=repo_path,
        )
        stdout, stderr = await proc.communicate()
        cmd_output = stdout.decode("utf-8", "ignore")
    except (
        OSError,
        SubprocessError,
        UnicodeDecodeError,
    ) as exc:
        LOGGER.exception(
            exc,
            extra={
                "extra": {
                    "repo_path": repo_path,
                    "filename": filename,
                    "line": str(line),
                },
            },
        )

        return None

    if stderr or proc.returncode != 0 or not cmd_output:
        return None

    commit_hash = cmd_output.splitlines()[0].split(" ")[0]
    mail_search = re.search(r"author-mail <(.*?)>", cmd_output)
    author_email = mail_search.group(1) if mail_search else ""
    time_search = re.search(r"committer-time (\d*)", cmd_output)
    committer_time = time_search.group(1) if time_search else "0"
    commit_date = datetime.fromtimestamp(float(committer_time), UTC)

    return CommitInfo(
        hash=commit_hash,
        author=author_email,
        modified_date=commit_date,
    )


async def get_modified_filenames(repo_path: str, commit_sha: str) -> list[str]:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "diff",
        "--name-only",
        f"{commit_sha}..HEAD",
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        cwd=repo_path,
    )
    stdout, stderr = await proc.communicate()
    if stderr or proc.returncode != 0:
        return []

    return stdout.decode().splitlines()


async def is_commit_in_branch(
    repo_path: str,
    branch: str,
    commit_sha: str,
) -> bool:
    proc = await asyncio.create_subprocess_exec(
        "git",
        "branch",
        "--contains",
        f"{commit_sha}",
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        cwd=repo_path,
    )
    stdout, stderr = await proc.communicate()
    if stderr or proc.returncode != 0:
        return False

    return branch in stdout.decode()


def rebase(
    repo: Repo,
    *,
    path: str,
    line: int,
    rev_a: str,
    rev_b: str,
    ignore_errors: bool = True,
) -> RebaseResult | None:
    try:
        result: list[str] = repo.git.blame(
            f"{rev_a}..{rev_b}",
            "--",
            path,
            L=f"{line},+1",
            l=True,
            p=True,
            show_number=True,
            reverse=True,
            show_name=True,
            M=True,
            C=True,
        ).splitlines()
    except GitError as exc:
        if ignore_errors:
            LOGGER.exception(exc)
            return None

        raise

    new_rev = result[0].split(" ")[0]
    new_line = int(result[0].split(" ")[1])
    new_path = next(
        (row.split(" ", maxsplit=1)[1] for row in result if row.startswith("filename ")),
        path,
    )
    try:
        new_path = (
            new_path.encode("latin-1").decode("unicode-escape").encode("latin-1").decode("utf-8")
        ).strip('"')
    except (UnicodeDecodeError, UnicodeEncodeError) as exc:
        if ignore_errors:
            LOGGER.exception(
                exc,
                extra={
                    "extra": {
                        "path": path,
                        "new_path": new_path,
                    },
                },
            )
            return None

        raise

    return RebaseResult(path=new_path, line=new_line, rev=new_rev)


def get_head_commit(path_to_repo: Path, branch: str) -> str | None:
    try:
        return (
            Repo(path_to_repo.resolve(), search_parent_directories=True).heads[branch].object.hexsha
        )
    except GitError:
        return None


async def clone(
    repo_url: str,
    repo_branch: str,
    *,
    temp_dir: str,
    credential_key: str | None = None,
    user: str | None = None,
    password: str | None = None,
    token: str | None = None,
    provider: str | None = None,
    is_pat: bool = False,
    arn: str | None = None,
    org_external_id: str | None = None,
    follow_redirects: bool = False,
    mirror: bool = False,
) -> tuple[str | None, str | None]:
    if credential_key:
        return await ssh_clone(
            branch=repo_branch,
            credential_key=credential_key,
            repo_url=repo_url,
            temp_dir=temp_dir,
            mirror=mirror,
        )
    if user is not None and password is not None:
        return await https_clone(
            branch=repo_branch,
            password=password,
            repo_url=repo_url,
            temp_dir=temp_dir,
            token=None,
            user=user,
            follow_redirects=follow_redirects,
            mirror=mirror,
        )
    if token is not None:
        return await https_clone(
            branch=repo_branch,
            password=None,
            repo_url=repo_url,
            temp_dir=temp_dir,
            token=token,
            user=None,
            provider=provider,
            is_pat=is_pat,
            follow_redirects=follow_redirects,
            mirror=mirror,
        )
    if arn is not None and org_external_id is not None:
        return await call_codecommit_clone(
            branch=repo_branch,
            repo_url=repo_url,
            temp_dir=temp_dir,
            arn=arn,
            org_external_id=org_external_id,
            follow_redirects=follow_redirects,
            mirror=mirror,
        )

    if repo_url.startswith("http"):
        # it can be a public repository
        return await https_clone(
            branch=repo_branch,
            repo_url=repo_url,
            temp_dir=temp_dir,
            follow_redirects=follow_redirects,
            mirror=mirror,
        )

    raise InvalidParameter
