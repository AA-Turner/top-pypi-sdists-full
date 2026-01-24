import logging
import os
import shutil
import tarfile
import tempfile
from pathlib import Path

from git import GitError
from git.cmd import Git
from git.repo import Repo

from .constants import DEFAULT_DOWNLOAD_BUFFER_SIZE
from .delete_files import delete_out_of_scope_files
from .download_file import download_file

LOGGER = logging.getLogger(__name__)


def _is_member_safe(
    member: tarfile.TarInfo,
) -> bool:
    return not (
        member.issym() or member.islnk() or Path(member.name).is_absolute() or "../" in member.name
    )


def _safe_extract_tar(tar_handler: tarfile.TarFile, file_path: Path) -> bool:
    for member in tar_handler.getmembers():
        if not _is_member_safe(member):
            LOGGER.error("Unsafe path detected: %s", member.name)
            continue
        try:
            tar_handler.extract(member, path=file_path, numeric_owner=True)
        except tarfile.ExtractError:
            LOGGER.exception("Error extracting %s", member.name)

    return True


def remove_symlinks_in_directory(directory: str) -> None:
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)  # noqa: PTH118
            if Path(file_path).is_symlink():
                Path(file_path).unlink(missing_ok=True)


async def reset_repo(repo_path: str) -> bool:
    try:
        Path.cwd()
    except OSError:
        LOGGER.exception("Failed to get the working directory: %s", repo_path)
        os.chdir(repo_path)

    try:
        Git().execute(
            [
                "git",
                "config",
                "--global",
                "--add",
                "safe.directory",
                "*",
            ],
        )
    except GitError:
        LOGGER.exception("Failed to add safe directory %s", repo_path)

    try:
        repo = Repo(repo_path)
        repo.git.reset("--hard", "HEAD")
    except GitError:
        LOGGER.exception("Expand repositories has failed for repository %s", repo_path)

        return False

    if repo.working_dir:
        remove_symlinks_in_directory(str(repo.working_dir))

    return True


async def download_repo_from_s3(
    download_url: str,
    destination_path: Path,
    git_ignore: list[str] | None = None,
    *,
    download_buffer_size: int = DEFAULT_DOWNLOAD_BUFFER_SIZE,
) -> bool:
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="fluidattacks_", ignore_cleanup_errors=True) as tmpdir:
        tmp_path = Path(tmpdir)
        file_path = tmp_path / "repo.tar.gz"
        result = await download_file(
            url=download_url,
            destination_path=str(file_path.absolute()),
            download_buffer_size=download_buffer_size,
        )
        if not result:
            LOGGER.error("Failed to download repository from %s", download_url)
            return False

        try:
            with tarfile.open(file_path, "r:gz") as tar_handler:
                _safe_extract_tar(tar_handler, tmp_path)

            extracted_dirs = [d for d in tmp_path.iterdir() if d.is_dir()]
            if not extracted_dirs:
                LOGGER.error("No directory found in the extracted archive: %s", destination_path)
                return False

            if len(extracted_dirs) > 1:
                LOGGER.warning(
                    "Multiple directories found in archive, using first one: %s",
                    destination_path,
                )
            extracted_dir = extracted_dirs[0]

            if destination_path.exists():
                shutil.rmtree(destination_path)

            shutil.move(extracted_dir, destination_path)

        except OSError:
            LOGGER.exception(
                "Error downloading repository", extra={"extra": {"path": destination_path}}
            )
            return False

    if not await reset_repo(str(destination_path.absolute())):
        shutil.rmtree(destination_path, ignore_errors=True)
        return False

    delete_out_of_scope_files(git_ignore or [], str(destination_path.absolute()))

    return True
