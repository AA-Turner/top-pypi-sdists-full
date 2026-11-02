"""Pure-Python build-context tarball for remote (daemonless) image builds.

Packs a build context directory into a .tar.gz that kaniko reads from S3
(`--context=s3://…`). No Docker required — mirrors the pure-Python
`package_chart` in `helm_chart.py`.

Honors a `.dockerignore` at the context root (a practical subset: comment
lines, blank lines, and `fnmatch`-style globs; negation with `!` is supported;
`**` is treated as `*`). `.git` is always excluded.
"""

from __future__ import annotations

import fnmatch
import logging
import os
import tarfile
import tempfile

logger = logging.getLogger(__name__)

# Bound the context size so an accidental huge dir (node_modules, data files)
# fails fast locally instead of after a slow upload.
DEFAULT_MAX_BYTES = 512 * 1024 * 1024  # 512 MiB


class BuildContextError(Exception):
    """Raised when the build context can't be packaged."""


def _load_dockerignore(context_dir: str) -> list[str]:
    path = os.path.join(context_dir, ".dockerignore")
    if not os.path.isfile(path):
        return []
    patterns: list[str] = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            patterns.append(line)
    return patterns


def _is_ignored(relpath: str, patterns: list[str]) -> bool:
    """Evaluate .dockerignore patterns in order; last match wins. A leading
    '!' re-includes. Directory prefixes match everything under them."""
    ignored = False
    # Always drop VCS metadata.
    if relpath == ".git" or relpath.startswith(".git/"):
        return True
    for pat in patterns:
        negate = pat.startswith("!")
        p = pat[1:] if negate else pat
        p = p.lstrip("/").replace("**", "*")
        # match the path itself or any parent-dir glob
        if fnmatch.fnmatch(relpath, p) or fnmatch.fnmatch(relpath, p.rstrip("/") + "/*"):
            ignored = not negate
    return ignored


def build_context_tarball(
    context_dir: str,
    dockerfile: str | None = None,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> str:
    """Package `context_dir` into a gzipped tar and return the temp file path.

    Args:
        context_dir: Directory to pack (the Docker build context root).
        dockerfile: Optional path to the Dockerfile; if it lives outside
            `context_dir` it is added into the tar as `Dockerfile` so a remote
            builder with `--dockerfile=Dockerfile` finds it.
        max_bytes: Fail if the packed context would exceed this many bytes.

    Returns:
        Path to a temporary `.tar.gz`. The caller owns it and should delete it.
    """
    if not os.path.isdir(context_dir):
        raise BuildContextError(f"Build context is not a directory: {context_dir}")

    patterns = _load_dockerignore(context_dir)
    total = 0
    fd, tgz_path = tempfile.mkstemp(suffix=".tar.gz", prefix="cube-ctx-")
    os.close(fd)

    try:
        with tarfile.open(tgz_path, "w:gz") as tar:
            for root, dirs, files in os.walk(context_dir):
                # prune ignored dirs in-place so we don't descend into them
                rel_root = os.path.relpath(root, context_dir)
                keep = []
                for d in dirs:
                    rel = d if rel_root == "." else os.path.join(rel_root, d)
                    if not _is_ignored(rel.replace(os.sep, "/"), patterns):
                        keep.append(d)
                dirs[:] = keep

                for name in files:
                    abspath = os.path.join(root, name)
                    rel = name if rel_root == "." else os.path.join(rel_root, name)
                    rel = rel.replace(os.sep, "/")
                    if _is_ignored(rel, patterns):
                        continue
                    if os.path.islink(abspath) or not os.path.isfile(abspath):
                        continue
                    total += os.path.getsize(abspath)
                    if total > max_bytes:
                        raise BuildContextError(
                            f"Build context exceeds {max_bytes} bytes "
                            f"(hit at {rel}); add a .dockerignore to trim it."
                        )
                    tar.add(abspath, arcname=rel)

            # Ensure the Dockerfile is present as `Dockerfile` when it lives
            # outside the context (e.g. an explicit Dockerfile.prod one level up).
            if dockerfile:
                df_abs = os.path.abspath(dockerfile)
                if os.path.commonpath([df_abs, os.path.abspath(context_dir)]) != os.path.abspath(context_dir):
                    if not os.path.isfile(df_abs):
                        raise BuildContextError(f"Dockerfile not found: {dockerfile}")
                    tar.add(df_abs, arcname="Dockerfile")
    except Exception:
        try:
            os.remove(tgz_path)
        except OSError:
            pass
        raise

    logger.info("Packed build context %s (%d bytes) -> %s", context_dir, total, tgz_path)
    return tgz_path
