# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# a zip packager for local workspace

import contextlib
import hashlib
import logging
import queue
import re
import site
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import TYPE_CHECKING

import attrs
import emoji

from geneva.config import ConfigBase

if TYPE_CHECKING:
    from multiprocess.queues import Queue

from geneva.tqdm import tqdm

_LOG = logging.getLogger(__name__)


@attrs.define
class _ZipperConfig(ConfigBase):
    output_path: Path | None = attrs.field(
        validator=attrs.validators.optional(attrs.validators.instance_of(Path)),
        converter=attrs.converters.optional(Path),
        default=None,
    )

    @classmethod
    def name(cls) -> str:
        return "zipper"


_DEFAULT_IGNORES = [
    r"\.pyc",
    r".*__pycache__.*",
    r"\.venv",
    r"\.git",
    r"\.ruff_cache",
    r"\.vscode",
    r"\.github",
    r"\.lance",
    r"\.ipynb",
    r"\.geneva",
]

# archive files can be valid items on the python sys path.
_ARCHIVE_EXTS = {".zip", ".egg", ".whl"}


@attrs.define
class _ProgressQueue:
    queue: "Queue" = attrs.field()

    def update(self, value: int) -> None:
        self.queue.put(value)

    def get(self, *args, **kwargs) -> int:
        return self.queue.get(*args, **kwargs)


def _candidate_sys_roots() -> set[Path]:
    roots: set[Path] = set()
    for raw in sys.path:
        # '' means CWD
        base = Path.cwd() if raw == "" else Path(raw)
        try:
            base = base.resolve().absolute()
        except Exception:
            _LOG.warning(f"Strange path entry {raw}, ignoring")
            continue  # ignore broken/strange entries

        if base.is_dir():
            roots.add(base)
        elif base.is_file() and base.suffix.lower() in _ARCHIVE_EXTS:
            # allow dirs under the parent of an archive on sys.path
            roots.add(base.parent.resolve().absolute())
        # else: ignore non-existent paths, zipimport hooks, etc.
    return roots


@attrs.define
class WorkspaceZipper:
    path: Path = attrs.field(
        converter=attrs.converters.pipe(
            Path,
            Path.resolve,
            Path.absolute,
        )
    )

    output_dir: Path = attrs.field(
        converter=attrs.converters.optional(Path), default=None
    )

    def __attrs_post_init__(self) -> None:
        # Validate path
        if not self.path.is_dir():
            raise ValueError(f"path {self.path} must be a directory")

        # make sure the path is the current working directory, or
        # is part of sys.path
        if self.path == Path.cwd().resolve().absolute():
            pass
        else:
            roots = _candidate_sys_roots()
            valid_root = False
            for root in roots:
                if self.path == root or self.path.is_relative_to(root):
                    valid_root = True
                    break
            if not valid_root:
                raise ValueError(f"path {self.path} must be cwd or part of sys.path")

        # Set default output_dir
        if self.output_dir is None:
            config = _ZipperConfig.get()
            if config.output_path is not None:
                self.output_dir = config.output_path
            else:
                self.output_dir = self.path / ".geneva"

        # when output_dir is inside the scanned workspace, ignore the zips we
        # produce there, otherwise they change the next scan's checksum/content
        output_dir = self.output_dir.resolve().absolute()
        if output_dir.is_relative_to(self.path):
            rel = output_dir.as_posix().removeprefix(self.path.as_posix()).lstrip("/")
            prefix = re.escape(rel + "/") if rel else ""
            self.ignore_regexs.append(
                re.compile(rf"{prefix}[0-9a-f]{{64}}(\.part\d+)?\.zip$")
            )

    ignore_regexs: list[re.Pattern] = attrs.field(
        factory=lambda: [re.compile(r) for r in _DEFAULT_IGNORES],
        converter=lambda x: [re.compile(r) for r in x],
    )
    """
    a list of regex patterns to ignore when zipping the workspace

    only ignores based on the relative path of the file
    """

    shard_size: int = attrs.field(
        default=128 * 1024**2,
    )
    """
    the size of each shard in bytes
    """

    def checksum(self) -> tuple[str, int, list[tuple[str, int]]]:
        """
        create a checksum for the files in the workspace based on name and mtime.

        return the path of the zip file and a content hash of the zip file
        """

        with tqdm(self.path.rglob("*")) as pbar:
            total_size = 0
            pbar.set_description(
                emoji.emojize(
                    f":magnifying_glass_tilted_left: scanning workspace: {self.path}"
                )
            )

            hasher = hashlib.sha256()

            files = []
            for child in pbar:
                child: Path = child
                if child.is_dir():
                    continue  # skip directories
                if not child.is_file():
                    _LOG.warning(f"{child} is not a file or valid symlink, skipping")
                    continue

                # Path.relative_to() is too slow
                # here is the benchmark:
                # removeprefix is 10x faster than relative_to
                #
                # In [49]: %timeit for p in cwd.rglob("*"): p.as_posix().removeprefix(cwd.as_posix() + "/") # noqa: E501
                # 134 ms ± 663 μs per loop (mean ± std. dev. of 7 runs, 10 loops each)
                #
                # In [50]: %timeit for p in cwd.rglob("*"): p.relative_to(cwd)
                # 1.32 s ± 22.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
                arcname = child.as_posix().removeprefix(self.path.as_posix() + "/")
                if any(r.match(arcname) for r in self.ignore_regexs):
                    continue
                try:
                    stat = child.stat()
                    total_size += stat.st_size

                    files.append((arcname, stat.st_size))
                    hasher.update(arcname.encode("utf-8"))
                    hasher.update(
                        stat.st_mtime_ns.to_bytes(length=8, byteorder="little")
                    )
                except FileNotFoundError:
                    # maybe there was a race condition on the file?
                    _LOG.warning(f"File {child} not found, skipping")
                    continue
            checksum = hasher.hexdigest()
            pbar.set_description(
                emoji.emojize(
                    f":white_check_mark: scanned workspace: checksum={checksum}"
                )
            )
            return checksum, total_size, files

    def zip(
        self, create_zips=True, excludes: list[Path] | None = None
    ) -> tuple[list[Path], str]:
        """
        create a zip file for the workspace

        return the path of the zip file and a content hash of the zip file
        """
        if excludes is None:
            excludes = []
        if create_zips:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        checksum, total_size, files = self.checksum()

        with tqdm(
            total=total_size, unit="B", unit_scale=True, unit_divisor=1024, smoothing=0
        ) as pbar:
            if create_zips:
                pbar.set_description(
                    emoji.emojize(f":card_file_box: zipping workspace: {self.path}")
                )
            else:
                pbar.set_description(
                    emoji.emojize(
                        f":card_file_box: zipping workspace: {self.path} (dry run)"
                    )
                )

            # just a single zip if the size is small
            if total_size <= self.shard_size:
                zip_path = self.output_dir / f"{checksum}.zip"
                if zip_path in excludes:
                    _LOG.info("Zip exists, skipping: %s", zip_path)
                    return [], ""

                if create_zips:
                    _LOG.info(
                        f"Zipping {self.path} to {zip_path} with {len(files)} files"
                    )
                    self._write_zip(zip_path, files, pbar)
                    zip_path.chmod(0o777)
                    zip_path.parent.chmod(0o777)
                return [zip_path], checksum

            # workspace is large, shard it into multiple zip files
            def _chunk_by_size():  # noqa: ANN202
                running_size = 0
                current_chunk = []
                for arcname, size in files:
                    current_chunk.append((arcname, size))
                    running_size += size
                    if running_size >= self.shard_size:
                        yield current_chunk
                        current_chunk = []
                        running_size = 0
                if current_chunk:
                    yield current_chunk

            import multiprocess

            ctx = multiprocess.context.SpawnContext()
            with (
                ctx.Pool() as pool,
                ctx.Manager() as manager,
            ):
                progress_queue = _ProgressQueue(manager.Queue())  # type: ignore[attr-defined]

                chunks = [
                    (
                        self.output_dir / f"{checksum}.part{idx:02d}.zip",
                        file_and_sizes,
                        progress_queue,
                    )
                    for idx, file_and_sizes in enumerate(_chunk_by_size())
                ]

                if create_zips:
                    _LOG.info(f"{len(chunks)} chunks to zip")
                    filtered_chunks = [
                        (zip_name, fands, pq)
                        for zip_name, fands, pq in chunks
                        if zip_name not in excludes
                    ]
                    _LOG.info(f"{len(filtered_chunks)} filtered chunks to zip:")
                    if len(filtered_chunks) == 0:
                        # all filtered out, return empty list.
                        return [], ""

                    join_handle = pool.starmap_async(
                        self._write_zip,
                        filtered_chunks,
                    )

                    while pbar.n < total_size:
                        # join handle is ready before we expect it to
                        # this means there was an error in the worker
                        # get the future to raise the error
                        if join_handle.ready():
                            join_handle.get()

                        with contextlib.suppress(queue.Empty):
                            pbar.update(progress_queue.get(block=False))

                    join_handle.get()

            return [chunk[0] for chunk in chunks], checksum

    def _write_zip(
        self,
        zip_path: Path,
        file_and_sizes: list[tuple[str, int]],
        pbar,
    ) -> None:
        if zip_path.exists():
            _LOG.info("Zip exists, skipping: %s", zip_path)
            # Update progress bar even when skipping to avoid hanging
            total_size = sum(size for _, size in file_and_sizes)
            pbar.update(total_size)
            return

        _LOG.info(f"Zipping workspace {self.path} to {zip_path}")

        # use compression level 1 to speed up the process
        # the output size is not too different from level 6
        with zipfile.ZipFile(
            zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1
        ) as z:
            for arcname, size in file_and_sizes:
                z.write(self.path / arcname, arcname)
                pbar.update(size)


@attrs.define
class _UnzipperConfig(ConfigBase):
    output_dir: Path | None = attrs.field(
        converter=attrs.converters.optional(Path),
        default=None,
    )

    @classmethod
    def name(cls) -> str:
        return "unzipper"


# Kept separate from the zipper to avoid config mess
@attrs.define
class WorkspaceUnzipper:
    output_dir: Path = attrs.field(
        converter=attrs.converters.pipe(
            attrs.converters.default_if_none(
                _UnzipperConfig.get().output_dir,
            ),
            attrs.converters.default_if_none(
                factory=tempfile.mkdtemp,
            ),
            Path,
            Path.resolve,
            Path.absolute,
        ),
        default=None,
    )

    def unzip(self, zip_path: Path) -> None:
        """
        extract the zip file to the workspace
        """
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(self.output_dir)
        _LOG.info("extracted workspace to %s", self.output_dir)

        site.addsitedir(self.output_dir.as_posix())
        _LOG.info("added %s to sys.path", self.output_dir)
