from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import tarfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from aiohttp import web

from .page_source import IGNORED_DIRS, SOURCE_EXTENSIONS, component_entry, component_root, is_within

BUNDLE_HEADERS = {
    "Content-Type": "text/javascript; charset=utf-8",
    "Cache-Control": "no-cache",
}

ESBUILD_VERSION = "0.25.12"


@dataclass(frozen=True)
class BundleResult:
    path: Path
    cache_key: str
    cached: bool


def package_root(package: str) -> str:
    """Return the import-map/root name for an npm package spec."""
    package = package.strip()
    if not package:
        return package
    if package.startswith("@"):
        parts = package.split("/")
        if len(parts) >= 2:
            return f"{parts[0]}/{parts[1].split('@', 1)[0]}"
        return package
    return package.split("@", 1)[0]


def external_args(packages: list[str]) -> list[str]:
    roots = [
        "react",
        "react-dom",
        "react-dom/client",
        "react/jsx-runtime",
        "@capsule/page",
    ]
    roots.extend(package_root(pkg) for pkg in packages)
    seen = list(dict.fromkeys(root for root in roots if root))
    args: list[str] = []
    for root in seen:
        args.append(f"--external:{root}")
        args.append(f"--external:{root}/*")
    return args


def source_files(component_path: str) -> list[Path]:
    root = component_root(component_path)
    entry = component_entry(component_path)
    if not entry.is_file() or not is_within(entry, root):
        return []

    files = [entry]
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in IGNORED_DIRS]
        base = Path(dirpath)
        for filename in filenames:
            path = (base / filename).resolve()
            if path == entry or path.suffix not in SOURCE_EXTENSIONS:
                continue
            files.append(path)
    return sorted(files)


def bundle_cache_key(component_path: str, packages: list[str]) -> str:
    h = hashlib.sha256()
    h.update(json.dumps(sorted(package_root(pkg) for pkg in packages), sort_keys=True).encode())
    for path in source_files(component_path):
        rel = path.relative_to(component_root(component_path)).as_posix()
        h.update(rel.encode())
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()[:24]


def cache_dir() -> Path:
    path = Path.cwd() / ".capsule" / "cache" / "page-bundles"
    path.mkdir(parents=True, exist_ok=True)
    return path


def esbuild_package_name() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    arch = "arm64" if machine in {"arm64", "aarch64"} else "x64"
    if system == "darwin":
        return f"@esbuild/darwin-{arch}"
    if system == "linux":
        return f"@esbuild/linux-{arch}"
    raise RuntimeError(f"unsupported esbuild platform: {system}-{machine}")


def cached_esbuild_binary() -> Path:
    package = esbuild_package_name()
    bin_path = Path.cwd() / ".capsule" / "cache" / "bin" / "esbuild"
    if bin_path.exists():
        return bin_path

    bin_path.parent.mkdir(parents=True, exist_ok=True)
    meta_url = f"https://registry.npmjs.org/{package.replace('/', '%2f')}/{ESBUILD_VERSION}"
    with urllib.request.urlopen(meta_url, timeout=20) as resp:
        meta = json.loads(resp.read().decode())
    tarball_url = meta["dist"]["tarball"]
    tar_path = bin_path.with_suffix(".tgz")
    urllib.request.urlretrieve(tarball_url, tar_path)

    with tarfile.open(tar_path) as tar:
        member = next((m for m in tar.getmembers() if m.name.endswith("/bin/esbuild")), None)
        if member is None:
            raise RuntimeError("esbuild tarball did not contain bin/esbuild")
        extracted = tar.extractfile(member)
        if extracted is None:
            raise RuntimeError("failed to extract esbuild binary")
        bin_path.write_bytes(extracted.read())
    tar_path.unlink(missing_ok=True)
    bin_path.chmod(0o755)
    return bin_path


def esbuild_binary() -> str:
    found = shutil.which("esbuild")
    if found:
        return found
    return str(cached_esbuild_binary())


def build_page_bundle(component_path: str, packages: list[str]) -> BundleResult:
    entry = component_entry(component_path)
    if not entry.is_file():
        raise FileNotFoundError(component_path)

    key = bundle_cache_key(component_path, packages)
    out_path = cache_dir() / f"{key}.js"
    if out_path.exists():
        return BundleResult(path=out_path, cache_key=key, cached=True)

    cmd = [
        esbuild_binary(),
        str(entry),
        "--bundle",
        "--format=esm",
        "--platform=browser",
        "--jsx=automatic",
        "--log-level=warning",
        f"--outfile={out_path}",
        *external_args(packages),
    ]
    proc = subprocess.run(cmd, cwd=Path.cwd(), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "esbuild failed").strip())
    return BundleResult(path=out_path, cache_key=key, cached=False)


def page_bundle_handler(component_path: str, packages: list[str] | None = None):
    async def handler(_request: web.Request) -> web.StreamResponse:
        try:
            result = build_page_bundle(component_path, packages or [])
        except Exception as exc:
            return web.json_response({"error": "bundle_failed", "message": str(exc)}, status=503)

        headers = {
            **BUNDLE_HEADERS,
            "ETag": result.cache_key,
            "X-Capsule-Bundle-Cache": "hit" if result.cached else "miss",
        }
        return web.FileResponse(result.path, headers=headers)

    return handler
