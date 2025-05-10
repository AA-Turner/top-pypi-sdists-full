import asyncio
import logging
import os
from time import time

import dask.config
from dask.utils import parse_timedelta
from distributed.diagnostics.plugin import SchedulerPlugin, WorkerPlugin


class DaskSchedulerWriteFiles(SchedulerPlugin):
    name = "scheduler-write-files"

    def __init__(self, files, symlink_dirs=None):
        self._files_to_write = {**(files or {})}
        self._symlink_dirs = {**(symlink_dirs or {})}

    async def start(self, *args, **kwargs):
        logger = logging.getLogger("distributed.scheduler")
        files = self._files_to_write
        for path, content in files.items():
            abs_path = os.path.expanduser(path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w") as f:
                f.write(content)
                logger.info(f"{self.name} wrote to {abs_path}")

        for source_dir, target_dir in self._symlink_dirs.items():
            target_dir = os.path.abspath(os.path.expanduser(target_dir))
            if not os.path.exists(target_dir):
                try:
                    os.symlink(source_dir, target_dir)
                except Exception:
                    logger.exception(f"Error creating symlink from {source_dir} to {target_dir}")
        if self._symlink_dirs == {"/mount": "./mount"}:
            timeout = parse_timedelta(dask.config.get("coiled.mount-bucket.timeout", "30 s"))
            await wait_for_bucket_mounting(timeout=timeout, logger=logger)


class DaskWorkerWriteFiles(WorkerPlugin):
    name = "worker-write-files"

    def __init__(self, files, symlink_dirs=None):
        self._files_to_write = {**(files or {})}
        self._symlink_dirs = {**(symlink_dirs or {})}

    async def setup(self, *args, **kwargs):
        logger = logging.getLogger("distributed.worker")
        files = self._files_to_write
        for path, content in files.items():
            abs_path = os.path.expanduser(path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w") as f:
                f.write(content)
                logger.info(f"{self.name} wrote to {abs_path}")

        for source_dir, target_dir in self._symlink_dirs.items():
            target_dir = os.path.abspath(os.path.expanduser(target_dir))
            if not os.path.exists(target_dir):
                try:
                    os.symlink(source_dir, target_dir)
                except Exception:
                    logger.exception(f"Error creating symlink from {source_dir} to {target_dir}")
        if self._symlink_dirs == {"/mount": "./mount"}:
            timeout = parse_timedelta(dask.config.get("coiled.mount-bucket.timeout", "30 s"))
            await wait_for_bucket_mounting(timeout=timeout, logger=logger)


async def wait_for_bucket_mounting(timeout: int, logger: logging.Logger):
    deadline = time() + timeout
    mount_todo_dir = "/mount/.requests/todo"

    def bucket_mounts_are_pending():
        return os.path.exists(mount_todo_dir) and os.listdir(mount_todo_dir)

    while time() < deadline and bucket_mounts_are_pending():
        await asyncio.sleep(1)
    if bucket_mounts_are_pending():
        logger.error(f"Timed out waiting for buckets to be mounted after {timeout} seconds.")
