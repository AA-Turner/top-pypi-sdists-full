"""Compile caches a run can write, wherever its image says to keep them."""

import os
import sys
from pathlib import Path


class CompileCaches:
    """Point a compile cache the image names at the run's scratch when the run cannot write where it names.

    An image that keeps compiled kernels on a volume names the volume's path in its environment, and every function
    using the image inherits it, including those that do not mount the volume. Triton, which cannot build its driver
    without a writable cache, then reports that it has no GPU, and libraries built on it fall back to the CPU.
    """

    VARIABLES = ("TRITON_CACHE_DIR", "TORCHINDUCTOR_CACHE_DIR", "VLLM_CACHE_ROOT")

    @classmethod
    def ensure(cls, scratch: Path) -> None:
        """Before authored code imports anything that compiles, give each named cache a directory it can write."""
        for name in cls.VARIABLES:
            named = os.environ.get(name)
            if named and not cls.writable(Path(named)):
                cls._redirect(name, named, scratch / "compile-caches" / name.lower())

    @staticmethod
    def writable(path: Path) -> bool:
        """Whether the directory exists, or can be made, and accepts new files."""
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError:
            return False
        return os.access(path, os.W_OK)

    @staticmethod
    def _redirect(name: str, named: str, fallback: Path) -> None:
        """Use the run's own scratch and say so, since what compiles there is not kept for later runs."""
        fallback.mkdir(parents=True, exist_ok=True)
        os.environ[name] = str(fallback)
        print(
            f"{name}={named} cannot be written in this run, so its compiled kernels go to {fallback} and are not "
            "kept; mount the cache volume at that path on this function to keep them.",
            file=sys.stderr,
            flush=True,
        )
