"""Read a Docker image's declared ENV, WORKDIR, ENTRYPOINT and CMD from its
registry config blob.

Why this exists: ``docker run <image>`` inherits everything the image declares in
its config -- PATH, LANG, VIRTUAL_ENV, CONDA_PREFIX, JAVA_HOME, and whatever the
language ecosystem stores there. A sandbox started from a template built with
``from_image`` does not, because nothing ever read the image's config:
``from_image`` records the reference and the platform pulls the image
server-side. So an image that "works in Docker" can land in a sandbox where the
preinstalled toolchain is not on PATH at all, with no error that points at the
cause.

Anonymous registry v2 pulls, falling back to Docker Hub for bare names. Results
are cached per process. Every failure is reported as data rather than raised --
a template without the restored config still builds, and one unreachable
registry must not abort a batch conversion.

Kept behaviourally identical to the JS SDK's ``template/imageConfig.ts``.
"""

import base64
import json
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import httpx

#: The host :func:`parse_image_ref` normalises every Docker Hub spelling to, and
#: the prefix it gives a bare name.
HUB_HOST = "registry-1.docker.io"
HUB_OFFICIAL = "library/"

MANIFEST_TYPES = ", ".join(
    [
        "application/vnd.docker.distribution.manifest.v2+json",
        "application/vnd.oci.image.manifest.v1+json",
        "application/vnd.docker.distribution.manifest.list.v2+json",
        "application/vnd.oci.image.index.v1+json",
    ]
)

#: ENV vars describing the *build* machine, or that would fight the sandbox's own
#: runtime setup. Carrying these over can actively break a sandbox, so they never
#: do -- even when the image declares them.
SKIP_ENV = frozenset(
    ["HOSTNAME", "HOME", "PWD", "OLDPWD", "SHLVL", "_", "TERM"]
)

#: Registry failures worth another attempt. 429 is the one that matters: Docker
#: Hub's anonymous pull limit is per-IP, so converting a hundred images hits it
#: routinely -- and the consequence is not a failed conversion but a template
#: built with no restored ENV, which is the one thing this exists to prevent.
RETRY_STATUS = frozenset([429, 500, 502, 503, 504])
READ_ATTEMPTS = 3

#: Backoff base, in seconds. Overridable only so a unit test can assert the retry
#: behaviour without spending the real three seconds waiting for it.
_backoff_base_s = 1.0


def set_retry_backoff_for_tests(seconds: float):
    """Set the backoff base; returns a callable restoring the previous value."""
    global _backoff_base_s
    previous = _backoff_base_s
    _backoff_base_s = seconds

    def restore():
        global _backoff_base_s
        _backoff_base_s = previous

    return restore


_APT_EVIDENCE = re.compile(r"debian\.sh|debuerreotype|apt-get|apt install|dpkg", re.I)

_BASE_FAMILIES = [
    (
        re.compile(r"alpine-minirootfs|etc/alpine-release|apk add|apk --no-cache", re.I),
        "Alpine (musl)",
    ),
    (re.compile(r"^BusyBox ", re.I | re.M), "BusyBox"),
    (
        re.compile(r"microdnf|dnf install|yum install|rpm -i", re.I),
        "RPM-based (Fedora/RHEL/Rocky)",
    ),
    (re.compile(r"pacman -S", re.I), "Arch"),
    (re.compile(r"zypper|KIWI ", re.I), "SUSE"),
]


def unsupported_base(blob: Dict[str, Any]) -> Optional[str]:
    """Whether the platform can provision a sandbox from this image's base OS.

    Measured, one template per image::

        debian:12, ubuntu:22.04, python:3.11-slim, redis:7   ready
        alpine:3.20, nginx:alpine, node:20-alpine            provisioning exit 1
        busybox:1.36, fedora:40, rockylinux:9                provisioning exit 1

    So the line is not "Debian": Ubuntu builds. It is apt and glibc -- the
    platform installs systemd during provisioning, which needs both.

    The check is deliberately one-directional. ``ubuntu:22.04`` builds and its
    config blob carries *no* signal at all (one ``ADD``, no labels, no
    distro-specific ENV), while ``rockylinux:9``'s blob is shaped identically and
    does not build. Absence of evidence therefore cannot mean "unsupported"
    without rejecting images that work, so this reports only what it can
    positively identify and says nothing about the rest. The build is the backstop
    for those.

    apt evidence wins over everything: an image assembled from an Alpine stage but
    based on Debian has both, and the apt one is what provisioning needs.

    Kept behaviourally identical to the JS SDK's ``unsupportedBase``.

    :returns: the unsupported family, or ``None`` when the image looks fine or
        cannot be classified.
    """
    history = "\n".join(
        (entry or {}).get("created_by") or "" for entry in blob.get("history") or []
    )
    config = blob.get("config") or {}
    labels = " ".join((config.get("Labels") or {}).keys())
    env = " ".join(config.get("Env") or [])

    # A bare mention of "debian" is not evidence: busybox:1.36 reports
    # "BusyBox 1.36.1 (glibc), Debian 13" and cannot be provisioned.
    if _APT_EVIDENCE.search(history):
        return None

    for pattern, family in _BASE_FAMILIES:
        if pattern.search(history):
            return family

    # Signals outside the history: openSUSE stamps its own label namespace, and
    # Fedora sets DISTTAG in ENV. Neither image builds here.
    if re.search(r"org\.opensuse\.", labels):
        return "SUSE"
    if re.search(r"DISTTAG=f\d+container", env):
        return "RPM-based (Fedora/RHEL/Rocky)"

    return None


@dataclass
class ImageConfig:
    """What the image declares, plus why the read failed when it did."""

    env: Dict[str, str] = field(default_factory=dict)
    workdir: Optional[str] = None
    entrypoint: List[str] = field(default_factory=list)
    cmd: List[str] = field(default_factory=list)
    #: Set when the config could not be read at all.
    error: Optional[str] = None
    #: Set when the image's base OS cannot be provisioned -- see
    #: :func:`unsupported_base`. Kept apart from ``unusable``: the reference is
    #: fine and the image exists, it is the base the platform cannot boot.
    unsupported_base: Optional[str] = None
    #: Set when the image was read fine and still cannot be used here -- no
    #: linux/amd64 variant, or the reference names nothing. Distinct from
    #: ``error`` because a retry cannot change it and the build would fail for
    #: the same reason after minutes of pulling.
    unusable: Optional[str] = None

    def copy(self) -> "ImageConfig":
        """A caller-owned copy, so one caller's edit cannot reach the next."""
        return ImageConfig(
            env=dict(self.env),
            workdir=self.workdir,
            entrypoint=list(self.entrypoint),
            cmd=list(self.cmd),
            error=self.error,
            unsupported_base=self.unsupported_base,
            unusable=self.unusable,
        )


_CACHE: Dict[str, ImageConfig] = {}


def parse_image_ref(image: str) -> Tuple[str, str, str]:
    """Split an image reference into ``(host, repository, reference)``.

    ::

        'nginx'                    -> registry-1.docker.io, library/nginx, latest
        'org/app:1.2'              -> registry-1.docker.io, org/app, 1.2
        'ghcr.io/org/app:dev'      -> ghcr.io, org/app, dev
        'reg:5000/app@sha256:ab...' -> reg:5000, app, sha256:ab...
    """
    ref = image[len("docker.io/") :] if image.startswith("docker.io/") else image

    host = HUB_HOST
    slash = ref.find("/")
    if slash != -1:
        head = ref[:slash]
        # A first segment is a registry host only if it looks like one: it
        # contains a dot or a port, or is literally localhost. Otherwise it is a
        # Hub org.
        if "." in head or ":" in head or head == "localhost":
            host = head
            ref = ref[slash + 1 :]

    at = ref.find("@")
    if at != -1:
        # Digest pins take precedence: '@' can only introduce a digest.
        repository, reference = ref[:at], ref[at + 1 :]
    else:
        colon = ref.rfind(":")
        # A ':' inside the final path segment is a tag; one before a '/' is a port.
        if colon != -1 and "/" not in ref[colon + 1 :]:
            repository, reference = ref[:colon], ref[colon + 1 :]
        else:
            repository, reference = ref, "latest"

    if host == HUB_HOST and "/" not in repository:
        repository = f"{HUB_OFFICIAL}{repository}"

    return host, repository, reference


class _RegistryHttpError(Exception):
    """An HTTP status carried alongside the failure, so callers can act on it."""

    def __init__(self, status: int, retry_after: Optional[str], message: str):
        super().__init__(message)
        self.status = status
        self.retry_after = retry_after
        self.message = message

    def __str__(self) -> str:
        return self.message


class _UnusableImageError(Exception):
    """The image was read successfully and cannot be used here."""


def _retry_delay_s(error: Optional[BaseException], fallback_s: float) -> float:
    """Seconds to wait, from the response's Retry-After when it is usable."""
    raw = error.retry_after if isinstance(error, _RegistryHttpError) else None
    try:
        seconds = float(raw) if raw is not None else None
    except ValueError:
        # Retry-After may be an HTTP-date rather than seconds; not worth parsing.
        seconds = None
    if seconds is None:
        return fallback_s
    return min(seconds * _backoff_base_s, 10.0)


def _discard_connections(client: httpx.Client) -> None:
    """Drop this client's pooled connections, keeping the client usable.

    A retry over a reset connection is not a retry: httpx keeps the pool alive and
    hands the same dead connection back. Measured against Docker Hub's blob CDN,
    one reset made all three attempts fail with `[Errno 54] Connection reset by
    peer` about 50ms apart, and the read returned a config with no environment.
    The JS SDK has no such failure mode -- `fetch` connects per call -- so the same
    image read fine there and degraded here.

    Best-effort by design: reaching into `_transport._pool` is not part of httpx's
    public API, so a version that renames it must not turn a retryable read into an
    exception. The retry still happens either way; it is only less likely to land
    on the same dead connection.
    """
    try:
        client._transport._pool.close()  # type: ignore[attr-defined]
    except Exception:  # noqa: BLE001
        pass


def _registry_get(
    client: httpx.Client,
    url: str,
    headers: Dict[str, str],
    attempts: int = READ_ATTEMPTS,
) -> Any:
    """GET with a short retry on the statuses a registry uses for "later".

    Deliberately not a general retry: 401/403/404 are answers, not hiccups, and
    retrying them spends a batch run's time to reach the same conclusion.
    """
    last: Optional[BaseException] = None

    for attempt in range(attempts):
        if attempt > 0:
            time.sleep(_retry_delay_s(last, 2 ** (attempt - 1) * _backoff_base_s))

        try:
            response = client.get(url, headers=headers)

            if response.status_code >= 400:
                error = _RegistryHttpError(
                    response.status_code,
                    response.headers.get("retry-after"),
                    f"HTTP {response.status_code} {response.reason_phrase}",
                )
                if response.status_code not in RETRY_STATUS:
                    raise error
                last = error
                continue

            return response.json()
        except _RegistryHttpError:
            raise
        except Exception as error:  # noqa: BLE001
            # Network-level flakiness has no status to inspect; same treatment --
            # except that the connection has to be discarded first. Measured
            # against Docker Hub's blob CDN: one reset made all three attempts
            # fail with `[Errno 54] Connection reset by peer` about 50ms apart,
            # because httpx keeps the pool alive and handed the same dead
            # connection back each time. The JS SDK does not have this failure
            # mode -- `fetch` connects per call -- so the same read succeeded
            # there and returned an image config with no environment here.
            last = error
            # Drop the pooled connections before retrying. `client.close()` would
            # make the client permanently unusable, so only the pool goes.
            _discard_connections(client)

    raise last if last is not None else RuntimeError(f"{url}: no attempt was made")


def _auth_headers(
    client: httpx.Client,
    host: str,
    repository: str,
    username: Optional[str],
    password: Optional[str],
) -> Dict[str, str]:
    """Best-effort registry token.

    Public Docker Hub and GHCR both hand out anonymous pull tokens; private
    registries take the basic auth through unchanged.
    """
    headers: Dict[str, str] = {"Accept": MANIFEST_TYPES}

    if username and password:
        basic = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode(
            "ascii"
        )
        headers["Authorization"] = f"Basic {basic}"

    services = {
        "registry-1.docker.io": ("auth.docker.io", "registry.docker.io"),
        "ghcr.io": ("ghcr.io", "ghcr.io"),
    }
    service = services.get(host)
    if service is None:
        return headers

    auth_host, service_name = service
    url = (
        f"https://{auth_host}/token?service={service_name}"
        f"&scope=repository:{repository}:pull"
    )

    try:
        token_headers = (
            {"Authorization": headers["Authorization"]}
            if "Authorization" in headers
            else {}
        )
        # One attempt: a failure here falls back to anonymous or basic auth, and
        # the read below has its own retries. Retrying both turned one offline
        # registry into six requests and six seconds of backoff.
        body = _registry_get(client, url, token_headers, attempts=1)
        token = body.get("token") if isinstance(body, dict) else None
        if token:
            headers["Authorization"] = f"Bearer {token}"
    except Exception:  # noqa: BLE001
        # Anonymous or basic auth may already suffice; the read below decides.
        pass

    return headers


def _platform_name(entry: Dict[str, Any]) -> str:
    p = entry.get("platform") or {}
    base = f"{p.get('os', '?')}/{p.get('architecture', '?')}"
    variant = p.get("variant")
    return f"{base}/{variant}" if variant else base


def _pick_amd64(index: Dict[str, Any], image: str) -> str:
    """The linux/amd64 digest from a multi-arch index.

    Raises naming the platforms the image *does* offer. No amd64 variant means
    the build will fail too, so this is worth catching before a build is spent.
    """
    manifests = index.get("manifests") or []
    for entry in manifests:
        p = entry.get("platform") or {}
        if p.get("architecture") == "amd64" and p.get("os") == "linux":
            return entry["digest"]

    # 'unknown/unknown' entries are attestation manifests, not usable images;
    # listing them would suggest a platform that could be selected.
    offered = sorted(
        {
            _platform_name(e)
            for e in manifests
            if (e.get("platform") or {}).get("os") != "unknown"
        }
    )

    raise _UnusableImageError(
        f"{image} has no linux/amd64 variant"
        + (f" (offers {', '.join(offered)})" if offered else "")
        + "; sandboxes are amd64, so this image cannot be used"
    )


def _describe_failure(
    error: BaseException,
    image: str,
    host: str,
    repository: str,
    authenticated: bool,
) -> ImageConfig:
    """Turn a registry failure into the config's ``error`` / ``unusable`` fields.

    The two Docker Hub cases below are measured, and the codes are the opposite
    way round from the obvious guess::

        library/redis                       200
        library/REDIS, library/nGiNx        404   (case-folds onto a real repo)
        library/nginx:no-such-tag           404   (repo exists, tag does not)
        library/nginxx, library/nginx-typo  401   (no such repo at all)

    So 404 means "the repository resolved, the thing you named did not", and a
    plain typo -- much the commoner mistake -- answers 401.
    """
    if isinstance(error, _UnusableImageError):
        return ImageConfig(error=str(error), unusable=str(error))

    if isinstance(error, _RegistryHttpError):
        if error.status == 404:
            reason = (
                f"no such image: the registry has no '{image}' (HTTP 404). "
                "Check spelling and case -- repository names are case-sensitive"
            )
            return ImageConfig(error=reason, unusable=reason)

        # 401 is normally ambiguous: an absent repository and a private one answer
        # byte-identically. Docker Hub's official `library/` namespace is the
        # exception -- it has no private repositories, so nothing there can 401
        # for a reason other than not existing.
        #
        # Unless credentials were supplied. Then the rejected credential is itself
        # a reason for a 401, and the ambiguity is back: measured, ``redis:7`` with
        # a wrong password and ``rediss:7`` with a right one answer identically. So
        # neither cause can be named alone -- blaming the spelling of a correct
        # name, or the credentials behind a correct one, each sends the reader to
        # the wrong place -- and this is not marked ``unusable``: a corrected
        # password makes the very same reference work, which is the one thing
        # ``unusable`` promises it will not.
        if (
            error.status == 401
            and host == HUB_HOST
            and repository.startswith(HUB_OFFICIAL)
        ):
            if authenticated:
                return ImageConfig(
                    error=(
                        f"cannot read '{image}' (HTTP 401): either the credentials "
                        "were rejected or there is no such image. Both answer alike "
                        "here, so check the spelling and the case of the name, then "
                        "the credentials"
                    )
                )
            reason = (
                f"no such image: Docker Hub has no official image '{image}' "
                "(HTTP 401). The `library/` namespace has no private "
                "repositories, so this is a typo rather than a permissions problem"
            )
            return ImageConfig(error=reason, unusable=reason)

        return ImageConfig(error=f"RegistryHttpError: {error.message}")

    return ImageConfig(error=str(error))


def _open_client(timeout_s: float) -> httpx.Client:
    """An httpx client that reads the registry even when the proxy cannot be used.

    httpx honours ``ALL_PROXY``/``HTTPS_PROXY`` from the environment, and refuses
    to construct at all for a ``socks5://`` proxy unless the optional ``socksio``
    package is installed. Measured on a machine with ``all_proxy=socks5://...``:
    every read failed with "Using SOCKS proxy, but the 'socksio' package is not
    installed", while the JS SDK on the same machine read the same images fine --
    Node's fetch ignores those variables. Same SDK, same image, different answer.

    So a proxy that cannot be constructed is treated as no proxy rather than as a
    failed read. Adding ``httpx[socks]`` as a dependency would be the other fix,
    but a direct connection is what the JS SDK already does, and this keeps the
    two in agreement without growing the install.
    """
    try:
        return httpx.Client(timeout=timeout_s, follow_redirects=True)
    except (ImportError, ValueError):
        # trust_env=False drops the environment's proxy settings entirely.
        return httpx.Client(timeout=timeout_s, follow_redirects=True, trust_env=False)


def fetch_image_config(
    image: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout_s: float = 30.0,
) -> ImageConfig:
    """Read what an image declares.

    Every field is present even on failure, so a caller never has to distinguish
    "no config" from "read failed" structurally -- ``error`` says which it was.
    Nothing is raised: restoring an image's config is best-effort, and a batch
    conversion must not stop because one registry was unreachable.
    """
    # Keyed on the credentials too. An anonymous and an authenticated read of the
    # same private repository are different questions with different answers, so
    # caching only the reference would hand a caller who supplied credentials the
    # anonymous 401 from an earlier call.
    key = json.dumps([image, username, password])
    cached = _CACHE.get(key)
    if cached is not None:
        return cached.copy()

    host, repository, reference = parse_image_ref(image)

    try:
        with _open_client(timeout_s) as client:
            auth = _auth_headers(client, host, repository, username, password)
            base = f"https://{host}/v2/{repository}"

            manifest = _registry_get(client, f"{base}/manifests/{reference}", auth)

            if isinstance(manifest, dict) and manifest.get("manifests"):
                # Multi-arch index: resolve to the linux/amd64 manifest.
                digest = _pick_amd64(manifest, image)
                manifest = _registry_get(client, f"{base}/manifests/{digest}", auth)

            config_digest = (manifest or {}).get("config", {}).get("digest")
            if not config_digest:
                raise RuntimeError(f"{image}: manifest names no config blob")

            blob = _registry_get(client, f"{base}/blobs/{config_digest}", auth)

        declared = (blob or {}).get("config") or {}
        env: Dict[str, str] = {}
        for entry in declared.get("Env") or []:
            eq = entry.find("=")
            if eq == -1:
                continue
            name = entry[:eq]
            if name not in SKIP_ENV:
                env[name] = entry[eq + 1 :]

        result = ImageConfig(
            env=env,
            workdir=declared.get("WorkingDir") or None,
            entrypoint=list(declared.get("Entrypoint") or []),
            cmd=list(declared.get("Cmd") or []),
            unsupported_base=unsupported_base(blob or {}),
        )
    except Exception as error:  # noqa: BLE001
        result = _describe_failure(
            error, image, host, repository, username is not None
        )

    _CACHE[key] = result
    return result.copy()


def effective_start_cmd(entrypoint: List[str], cmd: List[str]) -> Optional[str]:
    """Docker's effective command: ENTRYPOINT followed by CMD, joined with spaces.

    This matches what the SDK's own Dockerfile parser does with the array form,
    so ``docker-entrypoint.sh redis-server`` is reproduced exactly. The naive
    join loses shell quoting for an argument that itself contains spaces
    (``['sh','-c','echo a b']`` becomes ``sh -c echo a b``), which is the
    parser's limitation too; matching it keeps the two build paths in agreement
    rather than inventing a third behaviour.

    Returns None when the image declares neither, so the sandbox is left as a
    bare shell rather than handed an empty command.
    """
    parts = list(entrypoint) + list(cmd)
    return " ".join(_shell_quote_arg(part) for part in parts) if parts else None


def _shell_quote_arg(value: str) -> str:
    """Quote an exec-form argument for the shell string used by the build API."""
    if re.fullmatch(r"[A-Za-z0-9_./:@%+=,-]+", value):
        return value
    return "'" + value.replace("'", "'\\''") + "'"


def clear_image_config_cache() -> None:
    """Drop the process-wide read cache. Exposed for tests."""
    _CACHE.clear()
