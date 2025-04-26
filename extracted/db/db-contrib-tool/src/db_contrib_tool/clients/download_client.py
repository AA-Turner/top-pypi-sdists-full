"""A client to download artifacts."""

import contextlib
import ctypes
import errno
import os
import shutil
import tarfile
import zipfile
from typing import Optional

import requests
import structlog

from db_contrib_tool.utils.filesystem import build_bin_path, mkdtemp_in_build_dir

LOGGER = structlog.getLogger(__name__)


class DownloadError(Exception):
    """Errors resulting from download failures."""

    pass


class DownloadClient:
    """A client to download artifacts."""

    @staticmethod
    def download_from_url(url: str) -> str:
        """
        Download a file from the given URL.

        :param url: URL of file to download.
        :return: Path to downloaded file on local filesystem.
        """
        if not url:
            raise DownloadError("Download URL not found")

        LOGGER.info("Downloading", url=url)
        filename = os.path.join(mkdtemp_in_build_dir(), url.split("/")[-1].split("?")[0])

        with requests.get(url, stream=True) as reader:
            if reader.status_code == 200:
                with open(filename, "wb") as file_handle:
                    shutil.copyfileobj(reader.raw, file_handle)
            else:
                LOGGER.warning("Download failed", status_code=reader.status_code)
                raise DownloadError(reader.text)

        return filename

    @staticmethod
    def extract_archive(archive_file: str, install_dir: str) -> str:
        """
        Extract the given archive files content into the specified directory.

        :param archive_file: Path to file to extract.
        :param install_dir: Path of directory to extract into.
        :return: Path to directory file were extracted into.
        """
        LOGGER.info("Extracting archive data.", archive=archive_file, install_dir=install_dir)
        temp_dir = mkdtemp_in_build_dir()
        archive_name = os.path.basename(archive_file)
        _, file_suffix = os.path.splitext(archive_name)

        if file_suffix == ".zip":
            # Support .zip downloads, used for Windows binaries.
            with zipfile.ZipFile(archive_file) as zip_handle:
                zip_handle.extractall(temp_dir)
        elif file_suffix == ".tgz":
            # Support .tgz downloads, used for Linux binaries.
            with contextlib.closing(tarfile.open(archive_file, "r:gz")) as tar_handle:
                tar_handle.extractall(path=temp_dir)
        else:
            raise DownloadError(f"Unsupported file extension {file_suffix}")

        try:
            os.makedirs(install_dir)
        except FileExistsError:
            pass

        _rsync_move_dir(temp_dir, install_dir)
        shutil.rmtree(temp_dir)

        LOGGER.info("Extract archive completed.", installed_dir=install_dir)

        return install_dir

    @staticmethod
    def symlink_version(suffix: str, installed_dir: str, link_dir: Optional[str] = None) -> str:
        """
        Symlink the binaries in the 'installed_dir' to the 'link_dir'.

        If `link_dir` is None, link to the physical executable's directory (`bin_dir`).

        :param suffix: Bin name suffix.
        :param installed_dir: Path to install dir.
        :param link_dir: Path to dir where links should be created.
        :return: Path to dir where links were created.
        """
        bin_dir = build_bin_path(installed_dir)
        if bin_dir is None or not os.path.isdir(bin_dir):
            bin_dir = installed_dir

        if link_dir is None:
            link_dir = bin_dir
        else:
            mkdir_p(link_dir)

        for executable in os.listdir(bin_dir):
            if executable.endswith(".dll"):
                LOGGER.debug("Skipping linking DLL", file=executable)
                continue

            executable_name, executable_extension = os.path.splitext(executable)
            if suffix:
                link_name = f"{executable_name}-{suffix}{executable_extension}"
            else:
                link_name = executable

            executable = os.path.join(bin_dir, executable)
            executable_link = os.path.join(link_dir, link_name)

            create_symlink(executable, executable_link)

        LOGGER.info("Symlinks for all executables are created in the directory.", link_dir=link_dir)
        return link_dir


def _rsync_move_dir(source_dir: str, dest_dir: str) -> None:
    """
    Move dir.

    Move the contents of `source_dir` into `dest_dir` as a subdir while merging with
    all existing dirs.

    This is similar to the behavior of `rsync` but different to `mv`.

    :param source_dir: Source directory.
    :param dest_dir: Destination directory.
    """
    for cur_src_dir, _, files in os.walk(source_dir):
        cur_dest_dir = cur_src_dir.replace(source_dir, dest_dir, 1)
        if not os.path.exists(cur_dest_dir):
            os.makedirs(cur_dest_dir)
        for cur_file in files:
            src_file = os.path.join(cur_src_dir, cur_file)
            dst_file = os.path.join(cur_dest_dir, cur_file)
            if os.path.exists(dst_file):
                # in case of the src and dst are the same file
                if os.path.samefile(src_file, dst_file):
                    continue
                os.remove(dst_file)
            shutil.move(src_file, cur_dest_dir)


def mkdir_p(path: str) -> None:
    """
    Python equivalent of `mkdir -p`.

    :param path: Path to directory.
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def create_symlink(executable: str, executable_link: str) -> None:
    """
    Symlink executable to executable_link.

    :param executable: Path to executable.
    :param executable_link: Path to executable link.
    """
    try:
        if os.name == "nt":
            symlink_ms(executable, executable_link)
        else:
            os.symlink(executable, executable_link)
        LOGGER.debug("Symlink created.", executable=executable, executable_link=executable_link)

    except OSError as exc:
        if exc.errno == errno.EEXIST:
            LOGGER.warning("Symlink already exists.", exc=exc)
            if os.name != "nt":
                LOGGER.warning(
                    "Removing old symlink & trying again", executable_link=executable_link
                )
                os.remove(executable_link)
                os.symlink(executable, executable_link)
                LOGGER.debug(
                    "Symlink created.", executable=executable, executable_link=executable_link
                )
            pass
        else:
            raise


def symlink_ms(source: str, symlink_name: str) -> None:
    """
    Provide symlink for Windows.

    :param source: Path to file.
    :param symlink_name: Path to file link.
    """
    csl = ctypes.windll.kernel32.CreateSymbolicLinkW  # type: ignore
    csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
    csl.restype = ctypes.c_ubyte
    flags = 1 if os.path.isdir(source) else 0
    if csl(symlink_name, source.replace("/", "\\"), flags) == 0:
        raise ctypes.WinError()  # type: ignore
