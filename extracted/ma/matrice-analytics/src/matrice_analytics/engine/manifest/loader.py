"""The app-config loader: **resolve → fetch → unpack → validate → cache**.

Contract: ``09-tobe-engine-architecture.md`` §5.

    load_app("https://apps.matrice.ai/ppe_compliance@2.0.zip")
    load_app("/opt/matrice/apps/ppe_compliance")
    load_app("ppe_compliance")            # against MATRICE_APPS_ROOT / MATRICE_APPS_URL

Three properties this module exists to guarantee:

**Failure is loud and early.** A malformed manifest stops startup. It never degrades to an app that
runs and silently emits nothing — which is exactly what today's engine does when config or geometry
is missing, and why "the dashboard is empty" is diagnosed as a camera problem for a week.

**An app folder is untrusted input.** Zips arrive over HTTP. Every entry is checked for path
traversal, absolute paths and symlinks before anything is written, and the total unpacked size and
entry count are bounded.

**A local path always re-reads.** Editing ``app.yaml`` and re-running must show the edit, so local
folders never touch the cache. Remote zips are cached content-addressed, keyed by URL.

Standard library only (``urllib``, ``zipfile``, ``hashlib``, ``importlib``) plus PyYAML and
Pydantic, both of which the engine already requires.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import logging
import os
import random
import re
import shutil
import stat
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Literal

from pydantic import BaseModel, ValidationError

from .models import AppManifest, CustomConfig

logger = logging.getLogger(__name__)

__all__ = [
    "AppFetchError",
    "AppLoadError",
    "AppRef",
    "AppResolveError",
    "AppUnpackError",
    "CustomCodeError",
    "CustomImpl",
    "LoadedApp",
    "ManifestValidationError",
    "cache_root",
    "canonical_cache_url",
    "load_app",
    "load_app_bundle",
    "load_manifest_file",
    "redact_url",
    "remote_code_allowed",
    "resolve_ref",
]

#: The only required file in an app folder (``09`` §5). A pure-config app is exactly this one file.
MANIFEST_FILENAME = "app.yaml"

DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_RETRIES = 3

#: Bounds on untrusted archives. A zip bomb is 40KB on the wire and 4GB on disk; these caps turn
#: that into a clear error instead of a full disk on an edge box.
MAX_DOWNLOAD_BYTES = 64 * 1024 * 1024
MAX_UNPACKED_BYTES = 256 * 1024 * 1024
MAX_ZIP_ENTRIES = 4096

#: HTTP statuses worth retrying. Anything else (404, 403, 400) is a configuration mistake that a
#: retry only delays.
_RETRYABLE_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})

_ENV_APPS_ROOT = "MATRICE_APPS_ROOT"
_ENV_APPS_URL = "MATRICE_APPS_URL"
_ENV_APPS_CACHE = "MATRICE_APPS_CACHE"
_ENV_TRUSTED_HOSTS = "MATRICE_APPS_TRUSTED_HOSTS"
_ENV_ALLOW_REMOTE_CODE = "MATRICE_APPS_ALLOW_REMOTE_CODE"

_BARE_ID_RE = re.compile(r"^(?P<id>[a-z][a-z0-9_]*)(?:@(?P<version>[0-9][0-9A-Za-z.\-+]*))?$")
_VERSIONED_SEGMENT_RE = re.compile(r"(@[0-9]|/v[0-9]+(\.[0-9]+)*[./])")

#: A zip named for a git commit — ``…/application-usecases/<folder>/<sha>.zip``, the shape
#: be-application uploads. A commit SHA pins content absolutely, so such an object can never
#: change and is always safe to serve from the cache. Short SHAs are accepted because
#: be-application's own validator does (``^[0-9a-f]{7,40}$``).
_SHA_STEM_RE = re.compile(r"^[0-9a-f]{7,40}$")


# ---------------------------------------------------------------------------
# Errors — one per stage, so a caller can tell "you typed the name wrong" from
# "the manifest is invalid" from "someone shipped a malicious zip".
# ---------------------------------------------------------------------------


class AppLoadError(Exception):
    """Base class for every failure in resolve → fetch → unpack → validate → cache."""


class AppResolveError(AppLoadError):
    """The reference could not be turned into a folder or a URL."""


class AppFetchError(AppLoadError):
    """The app folder or zip could not be read/downloaded."""


class AppUnpackError(AppLoadError):
    """The archive was rejected — traversal, symlink, or size/entry bounds."""


class ManifestValidationError(AppLoadError):
    """``app.yaml`` is not a valid manifest. Raised at load time, deliberately fatal."""


class CustomCodeError(AppLoadError):
    """``logic.py`` is missing, does not contain the named symbol, or has no ``Config``."""


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class AppRef:
    """A parsed app reference — the output of the *resolve* stage."""

    raw: str
    kind: Literal["path", "url"]
    #: Filesystem path (``kind == "path"``) or absolute URL (``kind == "url"``).
    location: str
    app_id: str | None = None
    version: str | None = None
    #: How the reference was resolved, for the log line that follows a "why did it load *that*".
    via: str = "literal"


@dataclass(frozen=True)
class CustomImpl:
    """A resolved ``custom.impl`` reference, checked at load time."""

    stage: str
    module_path: Path
    symbol: str
    obj: type[Any]
    config_model: type[BaseModel]
    #: The stage's ``config:`` block, already validated against ``obj.Config``.
    config: BaseModel


@dataclass(frozen=True)
class LoadedApp:
    """Everything the runtime needs about one app folder."""

    manifest: AppManifest
    root: Path
    ref: AppRef
    #: sha256 of ``app.yaml`` — the identity a cache or a "did this change?" check should use.
    digest: str
    custom: dict[str, CustomImpl] = field(default_factory=dict)
    samples: tuple[Path, ...] = ()
    expected: tuple[Path, ...] = ()
    #: ``True`` when the folder came from the cache rather than a fresh download.
    from_cache: bool = False

    @property
    def app_id(self) -> str:
        return self.manifest.app.id


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


def load_app(
    ref: str | os.PathLike[str],
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    retries: int = DEFAULT_RETRIES,
    refresh: bool = False,
    cache_dir: str | os.PathLike[str] | None = None,
    allow_remote_code: bool | None = None,
) -> AppManifest:
    """Load and validate an app manifest. Raises :class:`AppLoadError` on any failure.

    This is the narrow entry point named in ``09`` §5. Use :func:`load_app_bundle` when you also
    need the folder, the resolved custom code, or the sample/golden files.
    """
    return load_app_bundle(
        ref,
        timeout=timeout,
        retries=retries,
        refresh=refresh,
        cache_dir=cache_dir,
        allow_remote_code=allow_remote_code,
    ).manifest


def load_manifest_file(path: str | os.PathLike[str]) -> AppManifest:
    """Parse and validate a single ``app.yaml``, with no folder, cache or custom-code handling.

    For tooling that only needs the schema verdict — ``matrice-analytics validate``, editors, the
    test generator. Use :func:`load_app` to actually run an app: only the full loader checks that
    ``logic.py`` imports and that declared fixtures exist.
    """
    manifest_path = Path(path).expanduser()
    if not manifest_path.is_file():
        raise AppFetchError(f"No manifest at {manifest_path}.")
    return _validate_manifest(manifest_path.read_bytes(), manifest_path)


def load_app_bundle(
    ref: str | os.PathLike[str],
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    retries: int = DEFAULT_RETRIES,
    refresh: bool = False,
    cache_dir: str | os.PathLike[str] | None = None,
    allow_remote_code: bool | None = None,
) -> LoadedApp:
    """The full loader. See the module docstring for the stages.

    ``allow_remote_code`` vouches for the *provenance* of ``ref``: pass ``True`` when the reference
    came from somewhere authenticated (the platform's own usecase-download API) so that a remote
    app's ``logic.py`` may be executed. Left ``None``, a remote app carrying custom code is checked
    against the trusted-host set — see :func:`remote_code_allowed`.
    """
    parsed = resolve_ref(ref)
    logger.debug(
        "app ref %r resolved to %s %s (via %s)",
        _redact(str(ref)),
        parsed.kind,
        _redact(parsed.location),
        parsed.via,
    )

    if parsed.kind == "path":
        root = _read_folder(parsed)
        from_cache = False
    else:
        root, from_cache = _fetch_and_unpack(
            parsed, timeout=timeout, retries=retries, refresh=refresh, cache_dir=cache_dir
        )

    manifest_path = root / MANIFEST_FILENAME
    raw_bytes = manifest_path.read_bytes()
    manifest = _validate_manifest(raw_bytes, manifest_path)

    _warn_on_identity_mismatch(manifest, root, parsed)

    custom = _load_custom_code(manifest, root, parsed, allow_remote_code=allow_remote_code)
    samples = _list_optional_dir(root / "samples")
    expected = _list_optional_dir(root / "expected")
    _check_declared_test_files(manifest, root)

    unimplemented = manifest.unimplemented_primitives()
    if unimplemented:
        # Not an error: the schema deliberately validates apps the runtime cannot run yet (08 §2).
        # The runtime refuses at session start; the loader only says so out loud.
        logger.warning(
            "app %s declares primitive(s) the runtime has not implemented yet: %s. The manifest is "
            "valid; running it will fail until they land.",
            manifest.app.id,
            ", ".join(unimplemented),
        )

    logger.info(
        "loaded app %s v%s from %s (%d pipeline stage(s), %d metric(s)%s)",
        manifest.app.id,
        manifest.app.version,
        root,
        len(manifest.pipeline),
        len(manifest.metrics),
        ", from cache" if from_cache else "",
    )

    return LoadedApp(
        manifest=manifest,
        root=root,
        ref=parsed,
        digest=hashlib.sha256(raw_bytes).hexdigest(),
        custom=custom,
        samples=samples,
        expected=expected,
        from_cache=from_cache,
    )


# ---------------------------------------------------------------------------
# Stage 1 — resolve
# ---------------------------------------------------------------------------


def resolve_ref(ref: str | os.PathLike[str]) -> AppRef:
    """Turn a reference into a path or a URL.

    Accepted, in the order they are tried:

    1. ``http(s)://…`` — a zip of the app folder
    2. anything that looks like a path (absolute, contains a separator, or exists)
    3. a bare ``app_id`` or ``app_id@version``, resolved against ``MATRICE_APPS_ROOT`` (a folder)
       or ``MATRICE_APPS_URL`` (a zip base URL)

    Both the path and the URL form exist so that offline and local development never touch the
    network (``09`` §5).
    """
    raw = os.fspath(ref).strip()
    if not raw:
        raise AppResolveError(
            "No app reference given. Pass an app folder path, a URL to a zip of one, or a bare "
            f"app id resolved against ${_ENV_APPS_ROOT} / ${_ENV_APPS_URL}."
        )

    scheme = urllib.parse.urlsplit(raw).scheme.lower()
    if scheme in {"http", "https"}:
        return AppRef(raw=raw, kind="url", location=raw, **_ids_from_url(raw))
    if scheme == "file":
        raise AppResolveError(
            f"file:// URLs are not supported ({raw!r}). Pass the plain filesystem path instead — "
            f"local folders are read directly and never cached, so edits take effect immediately."
        )
    if scheme and len(scheme) > 1:  # a Windows drive letter is a 1-char "scheme"
        raise AppResolveError(
            f"Unsupported URL scheme {scheme!r} in {raw!r}. Only http:// and https:// zips and "
            f"local folder paths are supported."
        )

    looks_like_path = (
        Path(raw).is_absolute() or raw.startswith((".", "~")) or "/" in raw or "\\" in raw or Path(raw).exists()
    )
    if looks_like_path:
        expanded = Path(raw).expanduser()
        return AppRef(raw=raw, kind="path", location=str(expanded), app_id=expanded.name)

    match = _BARE_ID_RE.match(raw)
    if not match:
        raise AppResolveError(
            f"{raw!r} is neither a path, a URL, nor a valid app id. An app id matches "
            f"^[a-z][a-z0-9_]*$ and may carry a version, e.g. 'ppe_compliance@2.0'."
        )
    return _resolve_bare_id(raw, match.group("id"), match.group("version"))


def _resolve_bare_id(raw: str, app_id: str, version: str | None) -> AppRef:
    """Resolve ``app_id[@version]`` against the environment.

    ``MATRICE_APPS_ROOT`` wins over ``MATRICE_APPS_URL`` deliberately: a developer who has set both
    is working locally, and the local copy is the one they are editing.
    """
    root_env = os.environ.get(_ENV_APPS_ROOT, "").strip()
    if root_env:
        base = Path(root_env).expanduser()
        candidates: list[Path] = []
        if version:
            candidates += [base / f"{app_id}@{version}", base / app_id / f"v{version}", base / app_id / version]
        else:
            candidates.append(base / app_id)
        for candidate in candidates:
            if (candidate / MANIFEST_FILENAME).is_file():
                return AppRef(
                    raw=raw,
                    kind="path",
                    location=str(candidate),
                    app_id=app_id,
                    version=version,
                    via=_ENV_APPS_ROOT,
                )
        tried = ", ".join(str(c) for c in candidates)
        if not os.environ.get(_ENV_APPS_URL, "").strip():
            raise AppResolveError(
                f"App {raw!r} was not found under ${_ENV_APPS_ROOT}={root_env}. Looked for "
                f"{MANIFEST_FILENAME} in: {tried}."
            )
        logger.warning("app %r not found under $%s; falling back to $%s", raw, _ENV_APPS_ROOT, _ENV_APPS_URL)

    url_env = os.environ.get(_ENV_APPS_URL, "").strip()
    if url_env:
        return AppRef(
            raw=raw,
            kind="url",
            location=_apps_url_for(url_env, app_id, version),
            app_id=app_id,
            version=version,
            via=_ENV_APPS_URL,
        )

    raise AppResolveError(
        f"Cannot resolve the bare app id {raw!r}: neither ${_ENV_APPS_ROOT} nor ${_ENV_APPS_URL} "
        f"is set. Set ${_ENV_APPS_ROOT} to the folder holding app directories, or "
        f"${_ENV_APPS_URL} to the base URL serving app zips, or pass a full path/URL instead."
    )


def _apps_url_for(base: str, app_id: str, version: str | None) -> str:
    """Build the zip URL for a bare id.

    ``MATRICE_APPS_URL`` may be a template containing ``{id}`` and ``{version}``; otherwise the
    conventional ``<base>/<id>@<version>.zip`` is used.
    """
    if "{id}" in base or "{version}" in base:
        return base.format(id=app_id, version=version or "latest")
    stem = f"{app_id}@{version}" if version else app_id
    return f"{base.rstrip('/')}/{stem}.zip"


def _ids_from_url(url: str) -> dict[str, str | None]:
    """Best-effort ``app_id`` / ``version`` from a zip URL, used only for cache keys and logs."""
    name = PurePosixPath(urllib.parse.urlsplit(url).path).name
    if name.endswith(".zip"):
        name = name[: -len(".zip")]
    if _SHA_STEM_RE.match(name):
        # …/application-usecases/<folderKey>/<commitSha>.zip. The SHA is the version: it pins the
        # bytes absolutely, which is exactly what the immutable-cache shortcut wants to know.
        #
        # ``app_id`` stays None on purpose. be-application's folderKey is the *last* segment of
        # githubPath (internal/utils/github.go:37-42), which for applications/<Cat>/<App>/<vX.Y>/
        # is the version folder, not an app id — feeding it to _warn_on_identity_mismatch would
        # warn on every single load.
        return {"app_id": None, "version": name}
    app_id, _, version = name.partition("@")
    return {"app_id": app_id or None, "version": version or None}


def canonical_cache_url(url: str) -> str:
    """The cache identity of a URL: scheme + host + path. No query, no fragment.

    A presigned S3 URL carries ``X-Amz-Signature``/``-Date``/``-Credential``, all of which change
    every time the URL is minted. Keying the cache on the whole URL therefore produces a fresh
    entry directory and a full re-download on every single container start, forever. The signature
    identifies the *requester*; only the path identifies the *object*.

    The residual risk — a URL whose query selects the content — is covered by the
    ``content-<sha256-of-bytes>`` directory: a fresh fetch always lands in the right place. Only
    the immutable shortcut could serve the wrong bytes, and that needs an immutability marker in
    the path, which such a URL does not have.
    """
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, "", ""))


def redact_url(url: str) -> str:
    """A URL safe to log. A presigned query string is a bearer credential, not metadata.

    Public because anything that reports *which* reference failed has the same problem: a bundle
    candidate named in an error message travels straight into a log.
    """
    parts = urllib.parse.urlsplit(url)
    if not parts.query:
        return url
    return canonical_cache_url(url) + "?<redacted>"


#: Internal alias kept for the call sites in this module.
_redact = redact_url


# ---------------------------------------------------------------------------
# Stage 2/3 — fetch and unpack
# ---------------------------------------------------------------------------


def _read_folder(ref: AppRef) -> Path:
    """A local folder is read in place, every time. No cache, so edits are instant."""
    root = Path(ref.location).expanduser()
    if not root.exists():
        raise AppFetchError(f"App folder {root} does not exist.")
    if root.is_file():
        if root.suffix.lower() == ".zip":
            raise AppFetchError(
                f"{root} is a zip file. Unzip it and pass the folder, or serve it over http(s) — "
                f"the loader only unpacks archives it fetched itself."
            )
        if root.name in {MANIFEST_FILENAME, "app.yml"}:
            raise AppFetchError(f"Pass the app *folder*, not the manifest file: use {root.parent} instead of {root}.")
        raise AppFetchError(f"App reference {root} is a file, not an app folder.")

    manifest = root / MANIFEST_FILENAME
    if not manifest.is_file():
        alternative = root / "app.yml"
        if alternative.is_file():
            raise AppFetchError(
                f"{root} contains 'app.yml' but the manifest must be named '{MANIFEST_FILENAME}' "
                f"(one spelling, so tooling can find it). Rename it."
            )
        contents = ", ".join(sorted(p.name for p in list(root.iterdir())[:12])) or "(empty)"
        raise AppFetchError(
            f"No {MANIFEST_FILENAME} in {root}. An app folder must contain the manifest at its "
            f"top level. Found: {contents}."
        )
    return root


def cache_root(cache_dir: str | os.PathLike[str] | None = None) -> Path:
    """Where unpacked remote apps live. ``$MATRICE_APPS_CACHE`` overrides the default."""
    if cache_dir is not None:
        return Path(cache_dir).expanduser()
    env = os.environ.get(_ENV_APPS_CACHE, "").strip()
    if env:
        return Path(env).expanduser()
    base = os.environ.get("XDG_CACHE_HOME", "").strip()
    return (Path(base) if base else Path.home() / ".cache") / "matrice" / "apps"


def _fetch_and_unpack(
    ref: AppRef,
    *,
    timeout: float,
    retries: int,
    refresh: bool,
    cache_dir: str | os.PathLike[str] | None,
) -> tuple[Path, bool]:
    """Download the zip and unpack it into the content-addressed cache.

    The cache is keyed by the URL's scheme, host and path — never its query string, see
    :func:`canonical_cache_url`. The unpacked directory is named by the sha256 of the archive
    bytes, so two URLs serving identical content share one directory and a changed artefact can
    never be served from a stale one.

    A URL that names a version (``…@2.0.zip``, ``…/v1.6/…``, ``…/<commitSha>.zip``) is treated as
    immutable and answered from the cache without a network call. A version-less URL is re-fetched
    every load — that is the difference between "pinned" and "latest", and guessing wrong the other
    way means an edge box runs last month's app forever.
    """
    cache_url = canonical_cache_url(ref.location)
    entry = cache_root(cache_dir) / hashlib.sha256(cache_url.encode("utf-8")).hexdigest()[:16]
    pointer = entry / "current.json"
    immutable = bool(_VERSIONED_SEGMENT_RE.search(cache_url)) or bool(ref.version)

    if not refresh and immutable and pointer.is_file():
        try:
            cached = json.loads(pointer.read_text(encoding="utf-8"))
            cached_dir = entry / str(cached["content"])
            if (cached_dir / MANIFEST_FILENAME).is_file():
                logger.debug("app cache hit for %s -> %s", cache_url, cached_dir)
                return cached_dir, True
        except (OSError, ValueError, KeyError) as exc:  # pragma: no cover - corrupt cache entry
            logger.warning("ignoring unreadable app cache entry %s: %s", pointer, exc)

    payload = _http_get(ref.location, timeout=timeout, retries=retries)
    digest = hashlib.sha256(payload).hexdigest()
    content_dir = entry / f"content-{digest[:16]}"

    if not (content_dir / MANIFEST_FILENAME).is_file():
        entry.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".unpack-", dir=entry))
        try:
            _unpack_zip(payload, staging, source=_redact(ref.location))
            unpacked_root = _locate_manifest_root(staging, source=_redact(ref.location))
            if content_dir.exists():  # pragma: no cover - concurrent loader won the race
                shutil.rmtree(content_dir, ignore_errors=True)
            unpacked_root.replace(content_dir)
        finally:
            shutil.rmtree(staging, ignore_errors=True)

    _write_pointer(pointer, url=cache_url, content=content_dir.name, digest=digest)
    return content_dir, False


def _write_pointer(pointer: Path, *, url: str, content: str, digest: str) -> None:
    """Atomically record which content directory this URL currently maps to.

    ``url`` is the canonical (query-stripped) form: a presigned signature is a credential and has
    no business sitting on disk in a cache file.
    """
    payload = json.dumps(
        {"url": url, "query_stripped": True, "content": content, "sha256": digest, "fetched_at": time.time()},
        indent=2,
    )
    pointer.parent.mkdir(parents=True, exist_ok=True)
    tmp = pointer.with_suffix(".json.tmp")
    tmp.write_text(payload, encoding="utf-8")
    tmp.replace(pointer)


def _http_get(url: str, *, timeout: float, retries: int) -> bytes:
    """GET with a bounded body, a bounded number of retries, and a log line per attempt.

    Only transient statuses are retried; a 404 is a typo in the app id and retrying it three times
    only makes startup slower to fail.
    """
    if urllib.parse.urlsplit(url).scheme.lower() not in {"http", "https"}:  # pragma: no cover
        raise AppFetchError(f"Refusing to fetch non-HTTP URL {_redact(url)!r}.")

    safe_url = _redact(url)
    attempts = max(1, retries)
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        started = time.monotonic()
        try:
            request = urllib.request.Request(  # noqa: S310 - scheme checked above
                url, headers={"User-Agent": "matrice-analytics-engine/1", "Accept": "application/zip"}
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
                payload = response.read(MAX_DOWNLOAD_BYTES + 1)
            if len(payload) > MAX_DOWNLOAD_BYTES:
                raise AppFetchError(
                    f"App archive at {safe_url} exceeds the {MAX_DOWNLOAD_BYTES // (1024 * 1024)}MiB "
                    f"download limit. An app folder is a manifest and a few fixtures; something "
                    f"much larger is almost certainly a model file, or a githubPath pointing at a "
                    f"repository root rather than one app folder."
                )
            logger.info(
                "fetched app archive %s (%d bytes) in %.2fs on attempt %d/%d",
                safe_url,
                len(payload),
                time.monotonic() - started,
                attempt,
                attempts,
            )
            return payload
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in _RETRYABLE_STATUS:
                raise AppFetchError(
                    f"Fetching {safe_url} failed with HTTP {exc.code} {exc.reason}. {_http_hint(url, exc.code)}".strip()
                ) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc

        if attempt < attempts:
            backoff = min(8.0, 0.5 * (2 ** (attempt - 1))) * (1.0 + random.random() * 0.1)  # noqa: S311
            logger.warning(
                "fetching %s failed on attempt %d/%d (%s); retrying in %.1fs",
                safe_url,
                attempt,
                attempts,
                last_error,
                backoff,
            )
            time.sleep(backoff)

    raise AppFetchError(
        f"Fetching {safe_url} failed after {attempts} attempt(s): {last_error}. The app cannot "
        f"start without its manifest; check the URL, the network and ${_ENV_APPS_URL}."
    ) from last_error


def _http_hint(url: str, code: int) -> str:
    """What to actually do about a non-retryable HTTP status."""
    if code == 404:
        return "Check the app id and version in the URL."
    if code == 403 and "X-Amz-Signature" in urllib.parse.urlsplit(url).query:
        return (
            "This is a presigned URL, and 403 on one almost always means it expired — "
            "be-application mints them for 5 hours. A presigned URL has to be minted at load "
            "time, not baked into a deployment config that outlives it. Supply "
            "application_id + application_version so the container can mint its own, or point "
            f"${_ENV_APPS_ROOT} at a synced app folder."
        )
    return ""


def _unpack_zip(payload: bytes, dest: Path, *, source: str) -> None:
    """Extract an untrusted archive, rejecting anything that could write outside ``dest``.

    ``ZipFile.extractall`` is not used: it sanitises absolute paths but historically has been the
    vehicle for Zip-Slip, and it gives no control over symlinks or total size. Every entry is
    checked here, before a single byte is written.
    """
    dest.mkdir(parents=True, exist_ok=True)
    dest_real = Path(os.path.realpath(dest))

    try:
        archive = zipfile.ZipFile(io.BytesIO(payload))
    except zipfile.BadZipFile as exc:
        raise AppUnpackError(
            f"The file fetched from {source} is not a valid zip archive ({exc}). The URL should "
            f"point at a zip of the app folder."
        ) from exc

    with archive:
        infos = archive.infolist()
        if len(infos) > MAX_ZIP_ENTRIES:
            raise AppUnpackError(
                f"App archive from {source} contains {len(infos)} entries, over the "
                f"{MAX_ZIP_ENTRIES} limit. An app folder is a manifest plus a few fixtures — an "
                f"archive this large usually means githubPath pointed at a repository root "
                f"instead of one app folder."
            )
        total = sum(info.file_size for info in infos)
        if total > MAX_UNPACKED_BYTES:
            raise AppUnpackError(
                f"App archive from {source} unpacks to {total} bytes, over the "
                f"{MAX_UNPACKED_BYTES // (1024 * 1024)}MiB limit."
            )

        for info in infos:
            name = info.filename
            _reject_unsafe_entry(name, info, source=source)

            target = dest / name
            target_real = Path(os.path.realpath(target))
            if dest_real != target_real and dest_real not in target_real.parents:
                # Belt and braces: the string checks above should already have caught this, but a
                # crafted name plus a symlinked cache directory is exactly the case they miss.
                raise AppUnpackError(
                    f"Refusing to unpack {name!r} from {source}: it resolves to {target_real}, "
                    f"outside the extraction directory {dest_real}. This archive is attempting "
                    f"path traversal."
                )

            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                with archive.open(info) as src, open(target, "wb") as out:
                    shutil.copyfileobj(src, out, length=64 * 1024)
            except (zipfile.BadZipFile, EOFError) as exc:
                # A truncated download passes the central-directory check and only fails here.
                # Without this it escapes as a bare BadZipFile traceback at container startup
                # instead of an AppLoadError anyone can act on (F8).
                raise AppUnpackError(
                    f"Entry {name!r} in the archive from {source} could not be read ({exc}). The "
                    f"download is most likely truncated or corrupt; retrying the load re-fetches it."
                ) from exc


def _reject_unsafe_entry(name: str, info: zipfile.ZipInfo, *, source: str) -> None:
    """Reject absolute paths, drive letters, ``..`` segments and symlinks."""
    normalised = name.replace("\\", "/")
    parts = PurePosixPath(normalised).parts

    if normalised.startswith("/") or re.match(r"^[A-Za-z]:", normalised):
        raise AppUnpackError(
            f"Refusing to unpack {name!r} from {source}: the entry is an absolute path. Archive "
            f"entries must be relative to the app folder."
        )
    if ".." in parts:
        raise AppUnpackError(
            f"Refusing to unpack {name!r} from {source}: the entry contains a '..' segment and "
            f"would write outside the extraction directory (path traversal / Zip-Slip)."
        )
    if stat.S_ISLNK(info.external_attr >> 16):
        raise AppUnpackError(
            f"Refusing to unpack {name!r} from {source}: symlinks in app archives are not "
            f"supported, because a symlink can point anywhere on the host filesystem."
        )


def _locate_manifest_root(unpacked: Path, *, source: str) -> Path:
    """Find ``app.yaml`` at the archive root, or inside a single wrapping folder.

    ``zip -r ppe_compliance.zip ppe_compliance/`` produces the wrapped form and is what people
    actually type, so both layouts are accepted — but only when there is exactly one candidate.
    """
    if (unpacked / MANIFEST_FILENAME).is_file():
        return unpacked

    children = [child for child in unpacked.iterdir() if not child.name.startswith(".")]
    directories = [child for child in children if child.is_dir()]
    if len(directories) == 1 and (directories[0] / MANIFEST_FILENAME).is_file():
        return directories[0]

    found = ", ".join(sorted(child.name for child in children[:12])) or "(empty archive)"
    raise AppUnpackError(
        f"No {MANIFEST_FILENAME} found in the archive from {source}. It must be at the archive "
        f"root, or inside a single top-level folder. Top level contains: {found}."
    )


# ---------------------------------------------------------------------------
# Stage 4 — validate
# ---------------------------------------------------------------------------


_LOADER: Any = None


def _yaml_loader() -> Any:
    """A ``SafeLoader`` that rejects duplicate mapping keys.

    PyYAML silently keeps the *last* duplicate. A manifest with two ``metrics:`` blocks would
    therefore load with half its metrics missing and no warning anywhere — precisely the class of
    silent loss this engine exists to remove.
    """
    global _LOADER
    if _LOADER is not None:
        return _LOADER
    yaml = _require_yaml()

    class _StrictLoader(yaml.SafeLoader):
        pass

    def _no_duplicate_keys(loader: Any, node: Any, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise yaml.constructor.ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"duplicate key {key!r} — YAML keeps only the last one, so the earlier block "
                    f"would be silently discarded",
                    key_node.start_mark,
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    _StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicate_keys)
    _LOADER = _StrictLoader
    return _LOADER


def _require_yaml() -> Any:
    try:
        import yaml  # noqa: PLC0415
    except ImportError as exc:  # pragma: no cover - PyYAML ships with the engine
        raise AppLoadError(
            "PyYAML is required to read app manifests but is not installed. Install it with 'pip install pyyaml'."
        ) from exc
    return yaml


def _validate_manifest(raw: bytes, path: Path) -> AppManifest:
    """Parse and validate ``app.yaml``. Any problem is fatal, by design (``09`` §5)."""
    yaml = _require_yaml()
    try:
        data = yaml.load(raw.decode("utf-8"), Loader=_yaml_loader())  # noqa: S506 - strict SafeLoader subclass  # nosec B506 - same reason, for the standalone bandit run
    except UnicodeDecodeError as exc:
        raise ManifestValidationError(f"{path} is not valid UTF-8: {exc}.") from exc
    except yaml.YAMLError as exc:
        raise ManifestValidationError(f"{path} is not valid YAML.\n\n{exc}") from exc

    if data is None:
        raise ManifestValidationError(
            f"{path} is empty. A manifest needs at least schema_version, app, model and pipeline — "
            f"see ml-applications/guidelines/examples/01-people-counting/app.yaml for the smallest one."
        )
    if not isinstance(data, dict):
        raise ManifestValidationError(
            f"{path} must contain a YAML mapping at the top level; got {type(data).__name__}."
        )

    try:
        return AppManifest.model_validate(data)
    except ValidationError as exc:
        raise ManifestValidationError(_format_validation_error(exc, path)) from exc


def _format_validation_error(exc: ValidationError, path: Path) -> str:
    """Render Pydantic's error list as something an ML engineer can act on.

    Pydantic's default repr leads with the model class name and the error type; what the reader
    needs is the YAML field path and the sentence explaining the fix.
    """
    errors = exc.errors()
    lines = [f"{path} is not a valid app manifest ({len(errors)} problem{'s' if len(errors) != 1 else ''}):", ""]
    for error in errors:
        location = _format_location(error.get("loc", ()))
        message = str(error.get("msg", "")).removeprefix("Value error, ").removeprefix("Assertion failed, ")
        lines.append(f"  {location}")
        lines.append(f"      {message}")
        if error.get("type") == "extra_forbidden":
            lines.append(
                "      (unknown fields are rejected rather than ignored — an ignored field looks "
                "like it works and does nothing)"
            )
        lines.append("")
    lines.append("Field reference: ml-applications/guidelines/FIELD_REFERENCE.md")
    return "\n".join(lines)


def _format_location(loc: tuple[Any, ...]) -> str:
    """``('pipeline', 2, 'unique_count', 'categories')`` → ``pipeline[2].categories``."""
    parts: list[str] = []
    for item in loc:
        if isinstance(item, int):
            if parts:
                parts[-1] = f"{parts[-1]}[{item}]"
            else:  # pragma: no cover - a root-level index is not reachable today
                parts.append(f"[{item}]")
        elif isinstance(item, str) and item.startswith("function-"):
            continue  # pydantic's internal wrapper-validator marker
        else:
            parts.append(str(item))
    return ".".join(parts) if parts else "(manifest root)"


def _warn_on_identity_mismatch(manifest: AppManifest, root: Path, ref: AppRef) -> None:
    """The app folder is usually ``…/<App_Name>/v<version>/``; a mismatch is worth saying.

    Not an error: the folder layout belongs to the apps repo, not to this schema, and a checkout at
    a different path must still load. But ``app.version: "1.0"`` inside ``v1.6/`` means one of the
    two is wrong, and it is cheap to notice here rather than after the wrong version deploys.
    """
    folder = root.name
    if folder.startswith("v") and folder[1:] and folder[1:] != manifest.app.version:
        logger.warning(
            "app %s declares version %r but lives in folder %r — the version folder and app.version are meant to match",
            manifest.app.id,
            manifest.app.version,
            folder,
        )
    if ref.app_id and ref.app_id not in {manifest.app.id, folder} and ref.kind == "url":
        logger.warning("app reference %r resolved to an app declaring id %r", ref.raw, manifest.app.id)


def _list_optional_dir(path: Path) -> tuple[Path, ...]:
    """``samples/`` and ``expected/`` are optional; a missing one is not an error."""
    if not path.is_dir():
        return ()
    return tuple(sorted(p for p in path.rglob("*") if p.is_file()))


def _check_declared_test_files(manifest: AppManifest, root: Path) -> None:
    """A fixture or golden file named in ``tests:`` but absent would silently skip a check."""
    missing = [name for name in manifest.tests.fixtures if not (root / name).is_file()]
    if manifest.tests.golden and not (root / manifest.tests.golden).is_file():
        missing.append(manifest.tests.golden)
    if missing:
        raise ManifestValidationError(
            f"{root / MANIFEST_FILENAME}: tests reference file(s) that do not exist in the app "
            f"folder: {', '.join(missing)}. A missing fixture makes the generated suite skip the "
            f"check it was written for. Add the file, or remove the reference."
        )


# ---------------------------------------------------------------------------
# Custom code (08 §9, 09 §6)
# ---------------------------------------------------------------------------


def remote_code_allowed(url: str, *, env: dict[str, str] | None = None) -> bool:
    """May we ``exec_module()`` Python out of a zip fetched from this host?

    Deliberately a *host* check and not a content check: nothing about the bytes can tell us who
    produced them. ``$MATRICE_APPS_URL``'s own host is trusted implicitly — an operator who
    configured it has already chosen where apps come from.
    """
    environ = os.environ if env is None else env
    if environ.get(_ENV_ALLOW_REMOTE_CODE, "").strip() in {"1", "true", "yes"}:
        return True

    host = urllib.parse.urlsplit(url).hostname or ""
    host = host.lower()
    if not host:  # pragma: no cover - resolve_ref rejects hostless URLs long before here
        return False

    allowed: list[str] = [
        item.strip().lower() for item in environ.get(_ENV_TRUSTED_HOSTS, "").split(",") if item.strip()
    ]
    apps_url = environ.get(_ENV_APPS_URL, "").strip()
    if apps_url:
        configured = urllib.parse.urlsplit(apps_url).hostname
        if configured:
            allowed.append(configured.lower())

    return any(host == item or (item.startswith(".") and host.endswith(item)) for item in allowed)


def _load_custom_code(
    manifest: AppManifest,
    root: Path,
    ref: AppRef | None = None,
    *,
    allow_remote_code: bool | None = None,
) -> dict[str, CustomImpl]:
    """Resolve every ``custom.impl`` and validate its ``config:`` block.

    This *imports* the app's Python at load time, which is the point: the alternative is finding
    out that ``logic.py`` has a typo three hours into a deployment.

    For a **local folder** that import is unconditional — the folder is as trusted as the process
    reading it. For an app fetched over **HTTP** it is not: every zip entry is checked for
    traversal, absolute paths and symlinks before a byte is written, and executing the Python
    inside would make that hardening pointless (finding F9). So a remote app carrying custom code
    must come from a reference whose provenance we can vouch for — one the SDK minted itself from
    the authenticated platform API, or a host an operator named. A remote app with *no* custom
    stages is never gated; there is nothing to execute.
    """
    stages = manifest.custom_stages()
    if (
        stages
        and ref is not None
        and ref.kind == "url"
        and not allow_remote_code
        and not remote_code_allowed(ref.location)
    ):
        names = ", ".join(sorted(stage.stage_name for stage in stages))
        raise CustomCodeError(
            f"App {manifest.app.id!r} fetched from {_redact(ref.location)} declares custom "
            f"stage(s) {names}, whose Python this loader would execute in-process. The host is "
            f"not vouched for: the reference did not come from the platform API, and the host is "
            f"not in ${_ENV_TRUSTED_HOSTS}. Point ${_ENV_APPS_ROOT} at a synced copy of the app, "
            f"name the host in ${_ENV_TRUSTED_HOSTS}, or set ${_ENV_ALLOW_REMOTE_CODE}=1 to "
            f"accept the risk for every remote app in this process."
        )

    impls: dict[str, CustomImpl] = {}
    for stage in stages:
        impls[stage.stage_name] = _resolve_custom_impl(stage, manifest, root)
    return impls


def _resolve_custom_impl(stage: CustomConfig, manifest: AppManifest, root: Path) -> CustomImpl:
    module_ref, _, symbol = stage.impl.partition(":")
    module_path = (root / module_ref.lstrip("./")).resolve()
    root_real = root.resolve()
    if root_real != module_path and root_real not in module_path.parents:
        raise CustomCodeError(
            f"custom.impl {stage.impl!r} resolves to {module_path}, outside the app folder "
            f"{root_real}. Custom code must live in the app folder so the app ships as one zip."
        )
    if not module_path.is_file():
        available = ", ".join(sorted(p.name for p in root.glob("*.py"))) or "(no .py files)"
        raise CustomCodeError(
            f"custom.impl {stage.impl!r} points at {module_path.name}, which does not exist in the "
            f"app folder. Python files present: {available}."
        )

    module_name = f"matrice_app.{manifest.app.id}.{module_path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - only for exotic loaders
        raise CustomCodeError(f"Could not import {module_path} as a Python module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        sys.modules.pop(module_name, None)
        raise CustomCodeError(
            f"Importing {module_path} failed: {type(exc).__name__}: {exc}. The app cannot start "
            f"until its custom code imports cleanly."
        ) from exc

    obj = getattr(module, symbol, None)
    if obj is None:
        public = ", ".join(
            sorted(name for name, value in vars(module).items() if isinstance(value, type) and not name.startswith("_"))
        )
        raise CustomCodeError(
            f"custom.impl {stage.impl!r}: {module_path.name} has no symbol named {symbol!r}. "
            f"Classes defined there: {public or '(none)'}."
        )
    if not isinstance(obj, type):
        raise CustomCodeError(
            f"custom.impl {stage.impl!r}: {symbol!r} is a {type(obj).__name__}, not a class. The "
            f"reference must name the class implementing the CustomPrimitive protocol."
        )

    config_model = getattr(obj, "Config", None)
    if config_model is None:
        raise CustomCodeError(
            f"custom.impl {stage.impl!r}: class {symbol} has no 'Config' attribute. Every custom "
            f"primitive declares 'Config = <a pydantic BaseModel>' so that the 'config:' block in "
            f"app.yaml is validated at load time instead of failing as a KeyError mid-stream."
        )
    if not (isinstance(config_model, type) and issubclass(config_model, BaseModel)):
        raise CustomCodeError(
            f"custom.impl {stage.impl!r}: {symbol}.Config must be a pydantic BaseModel subclass; got {config_model!r}."
        )
    if not callable(getattr(obj, "process", None)):
        raise CustomCodeError(
            f"custom.impl {stage.impl!r}: class {symbol} has no 'process' method. A custom "
            f"primitive implements 'process(self, ctx: FrameContext) -> PrimitiveOutput'."
        )

    try:
        config = config_model.model_validate(stage.config)
    except ValidationError as exc:
        raise CustomCodeError(
            f"The 'config:' block of the '{stage.stage_name}' stage does not match "
            f"{symbol}.Config:\n\n{_format_validation_error(exc, root / MANIFEST_FILENAME)}"
        ) from exc

    logger.debug("resolved custom stage %s -> %s:%s", stage.stage_name, module_path, symbol)
    return CustomImpl(
        stage=stage.stage_name,
        module_path=module_path,
        symbol=symbol,
        obj=obj,
        config_model=config_model,
        config=config,
    )
