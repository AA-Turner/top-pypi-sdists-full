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

Anonymous registry v2 pulls, following the ``WWW-Authenticate`` challenge the
registry answers with: only Docker Hub and GHCR have their token service written
down here, as a shortcut that saves the first 401. Every other registry -- Aliyun
ACR, Quay, public ECR, GitLab, Kubernetes' own registry, a self-hosted Harbor --
is read by following its own header, because no two of them name the same realm,
service or scope. Credentials are presented to that token service, which is the
only party that can tell a wrong password from a missing one.

Results are cached per process. Every failure is reported as data rather than
raised -- a template without the restored config still builds, and one unreachable
registry must not abort a batch conversion.

Kept behaviourally identical to the JS SDK's ``template/imageConfig.ts``.
"""

import base64
import json
import os
import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import httpx

#: The host :func:`parse_image_ref` normalises every Docker Hub spelling to, and
#: the prefix it gives a bare name.
HUB_HOST = "registry-1.docker.io"
HUB_OFFICIAL = "library/"

#: What a ``no_proxy`` entry httpx can read looks like: ``host[:port]``, optionally
#: dotted for a domain suffix. Bracketed IPv6 is deliberately not matched; see
#: :func:`_sanitize_no_proxy`.
_NO_PROXY_ENTRY = re.compile(
    r"\.?[A-Za-z0-9_](?:[A-Za-z0-9._-]*[A-Za-z0-9_])?(?::\d+)?"
)

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

#: Sent as ``client_id`` when a Bearer challenge is exchanged for a token. The
#: distribution spec makes it optional, and the registries that log it are the
#: ones that also accept an anonymous token for public repositories.
TOKEN_CLIENT_ID = "novita-sandbox"

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
        colon = repository.rfind(":")
        if colon > repository.rfind("/"):
            repository = repository[:colon]
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


def _basic_header(username: str, password: str) -> str:
    """The ``Basic`` header value for a username/password pair.

    Used in two places, and they are not the same place: the credentials belong to
    the registry's *token service*, which is what a Bearer challenge points at --
    not to the registry's own manifest endpoint, which answers a Basic request with
    the same 401 whether the password was right or wrong.
    """
    raw = f"{username}:{password}".encode("utf-8")
    return f"Basic {base64.b64encode(raw).decode('ascii')}"


def parse_challenges(header: Optional[str]) -> List[Tuple[str, Dict[str, str]]]:
    """Split a ``WWW-Authenticate`` header into ``(scheme, params)`` pairs.

    Measured, one registry per line. The parameters are not interchangeable and no
    two registries spell them the same way, which is why the read follows this
    header instead of keeping a table of registries::

        registry-1.docker.io  Bearer realm="https://auth.docker.io/token",service="registry.docker.io"
        quay.io               Bearer realm="https://quay.io/v2/auth",service="quay.io"
        public.ecr.aws        Bearer realm="https://public.ecr.aws/token/",service="public.ecr.aws",scope="aws"
        registry.gitlab.com   Bearer realm="https://gitlab.com/jwt/auth",service="container_registry"
        registry.k8s.io       Bearer realm="https://registry.k8s.io/token",service="registry.k8s.io"
        demo.goharbor.io      Bearer realm="https://demo.goharbor.io/service/token",service="harbor-registry"
        Harbor, with creds    Basic realm="harbor"

    Quote-aware, because a value may contain commas (``service="a,b"`` is legal) and
    one header may carry several challenges -- ``Bearer ...., Basic ....`` -- which a
    naive ``split(",")`` turns into nonsense parameters.

    Malformed input yields whatever was parsed so far rather than raising: this only
    ever runs while explaining a 401, and a registry's error header is not the place
    to discover a parser's opinion.
    """
    text = header or ""
    challenges: List[Tuple[str, Dict[str, str]]] = []
    index, length = 0, len(text)

    def skip_separators() -> None:
        nonlocal index
        while index < length and text[index] in " \t,":
            index += 1

    def read_token() -> str:
        nonlocal index
        start = index
        while index < length and (text[index].isalnum() or text[index] in "-_.:"):
            index += 1
        return text[start:index]

    while True:
        skip_separators()
        scheme = read_token()
        if not scheme:
            break

        params: Dict[str, str] = {}
        while True:
            skip_separators()
            if index >= length:
                break

            key_start = index
            key = read_token()
            if not key:
                break

            while index < length and text[index] in " \t":
                index += 1
            if index >= length or text[index] != "=":
                # A bare token means the next challenge starts here, not a parameter.
                index = key_start
                break

            index += 1
            while index < length and text[index] in " \t":
                index += 1

            if index < length and text[index] == '"':
                index += 1
                chars: List[str] = []
                while index < length:
                    if text[index] == "\\" and index + 1 < length:
                        chars.append(text[index + 1])
                        index += 2
                        continue
                    if text[index] == '"':
                        index += 1
                        break
                    chars.append(text[index])
                    index += 1
                params[key.lower()] = "".join(chars)
            else:
                value_start = index
                while index < length and text[index] != ",":
                    index += 1
                params[key.lower()] = text[value_start:index].strip()

        challenges.append((scheme, params))

    return challenges


class _RegistryHttpError(Exception):
    """An HTTP status carried alongside the failure, so callers can act on it."""

    def __init__(
        self,
        status: int,
        retry_after: Optional[str],
        message: str,
        challenge: Optional[str] = None,
    ):
        super().__init__(message)
        self.status = status
        self.retry_after = retry_after
        self.message = message
        #: The ``WWW-Authenticate`` value that came with a 401. This is how a
        #: registry says where its token service is; without it a 401 is final.
        self.challenge = challenge

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
                    response.headers.get("www-authenticate"),
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


class _RegistrySession:
    """Reads from one registry, following a 401 challenge rather than guessing.

    Every registry that is not Docker Hub or GHCR answers the first unauthenticated
    manifest request with ``401`` plus a ``WWW-Authenticate`` header naming its own
    token service, and the token that service hands back is what makes the
    repository readable -- anonymously for a public one, with credentials for a
    private one.

    Measured on Aliyun ACR, skipping that step reads as
    ``RegistryHttpError: HTTP 401 Unauthorized``, after which the template is built
    without the image's ENV, WORKDIR and start command -- and built quietly, since a
    failed read is deliberately not fatal.
    """

    def __init__(
        self,
        client: httpx.Client,
        repository: str,
        username: Optional[str],
        password: Optional[str],
        headers: Dict[str, str],
    ):
        self._client = client
        self._repository = repository
        self._username = username
        self._password = password
        self._headers = headers
        self._token: Optional[str] = None

    def get(self, url: str) -> Any:
        """GET ``url``, resolving one Bearer challenge if the registry asks for it."""
        headers = dict(self._headers)
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        try:
            return _registry_get(self._client, url, headers, attempts=READ_ATTEMPTS)
        except _RegistryHttpError as error:
            if error.status != 401:
                raise

            token = self._token_from(error.challenge)
            if token is None:
                # Nothing left to try, so the 401 stands and _describe_failure gets
                # to explain it with its status, host and credential state.
                raise

            self._token = token
            headers["Authorization"] = f"Bearer {token}"
            return _registry_get(self._client, url, headers, attempts=READ_ATTEMPTS)

    def _token_from(self, challenge: Optional[str]) -> Optional[str]:
        for scheme, params in parse_challenges(challenge):
            if scheme.lower() == "bearer":
                return self._bearer(params)
            # A Basic challenge is answered by whatever credentials are already in
            # self._headers. Reaching here with a 401 back means they were either
            # absent or rejected, and neither is something a retry can fix.
        return None

    def _bearer(self, params: Dict[str, str]) -> Optional[str]:
        realm = params.get("realm")
        if not realm or not realm.startswith(("http://", "https://")):
            return None

        query = {"client_id": TOKEN_CLIENT_ID}
        if params.get("service"):
            query["service"] = params["service"]
        # The challenge's own scope when it names one -- public ECR sends "aws" --
        # and the repository's pull scope otherwise. Asking for a broader scope than
        # the challenge offered is how a token request turns into a 403.
        query["scope"] = params.get("scope") or f"repository:{self._repository}:pull"

        headers: Dict[str, str] = {}
        if self._username and self._password:
            # Credentials go to the token service, which is the only party that can
            # tell a wrong password from a missing one.
            headers["Authorization"] = _basic_header(self._username, self._password)

        body = _registry_get(
            self._client, str(httpx.URL(realm, params=query)), headers, attempts=1
        )
        if not isinstance(body, dict):
            return None

        token = body.get("token") or body.get("access_token")
        return token if isinstance(token, str) and token else None


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

        if error.status == 401:
            # Everything else that answers 401 owns a token service this read could
            # not get a token from: the repository is private, or not public, or the
            # credentials were rejected. Spelled out rather than left as "HTTP 401",
            # which sends the reader looking for a network problem. Not `unusable`:
            # credentials that work make the very same reference succeed.
            if authenticated:
                reason = (
                    f"cannot read '{image}' (HTTP 401): the registry rejected the "
                    "credentials. Check the username, the password, and the "
                    "repository's read permission"
                )
            else:
                reason = (
                    f"cannot read '{image}' (HTTP 401): the registry wants pull "
                    "credentials for it. Pass the registry username and password, or "
                    "check that the reference names an existing public image"
                )
            return ImageConfig(error=reason)

        return ImageConfig(error=f"RegistryHttpError: {error.message}")

    return ImageConfig(error=str(error))


def _open_client(
    timeout_s: float,
    ca_bundle: Optional[str] = None,
    insecure: bool = False,
) -> httpx.Client:
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

    ``httpx.InvalidURL`` is in that same list, and is the one that cost a real
    diagnosis: a ``NO_PROXY`` entry written as ``[::1]`` makes httpx's own proxy
    parsing raise before a single request is sent, so the read failed with
    "Invalid port: ':1]'" -- an error naming neither the registry nor the proxy --
    and the image's ENV was dropped on a machine whose network was fine.

    Dropping ``trust_env`` to recover from that is not good enough on its own:
    measured, the direct connection then failed with ``[Errno 54] Connection reset
    by peer`` for Docker Hub, because the proxy the environment named was the only
    way out. So the unparsable entry is removed and *everything else is kept* --
    the proxy still applies, and only the entry httpx cannot read is dropped.

    ``ca_bundle`` and ``insecure`` exist for self-hosted registries, which are
    routinely behind a private CA or a self-signed certificate. Without them the
    read fails TLS verification and the failure is invisible in the sandbox, which
    is the same outcome as the 401 this module was fixed for. ``ca_bundle`` wins
    when both are given: naming the CA is the more precise statement.
    """
    verify: Any = ca_bundle if ca_bundle else not insecure

    def build(**extra: Any) -> httpx.Client:
        return httpx.Client(
            timeout=timeout_s, follow_redirects=True, verify=verify, **extra
        )

    try:
        return build()
    except httpx.InvalidURL:
        # A no_proxy entry httpx cannot parse. Repaired rather than dropped:
        # measured, dropping the whole environment sends the read direct, and
        # Docker Hub then answers "[Errno 54] Connection reset by peer" because the
        # proxy it named was the only way out.
        saved = _repair_no_proxy()
        try:
            if saved is None:
                return build(trust_env=False)
            return build()
        except (ImportError, ValueError, httpx.InvalidURL):
            return build(trust_env=False)
        finally:
            if saved:
                os.environ.update(saved)
    except (ImportError, ValueError):
        # A proxy that cannot be constructed at all -- a socks5:// URL with no
        # socksio installed. A direct connection is what the JS SDK does anyway.
        return build(trust_env=False)


def _sanitize_no_proxy(value: str) -> str:
    """Drop the ``no_proxy`` entries httpx cannot parse, keeping the rest.

    The value is written by the user's shell or VPN client, not by us, and the
    bracketed IPv6 loopback (``[::1]``) is a spelling httpx rejects while most
    tools accept it -- measured, one such entry is enough to make ``httpx.Client``
    raise before any request exists. Entries that do not look like ``host[:port]``
    are the ones dropped; matching is deliberately conservative, since keeping a
    malformed entry is what fails and dropping a good one only widens what the
    proxy has to carry.
    """
    kept = [
        entry.strip()
        for entry in value.split(",")
        if _NO_PROXY_ENTRY.fullmatch(entry.strip())
    ]
    return ",".join(kept)


def _repair_no_proxy() -> Optional[Dict[str, str]]:
    """Rewrite this process's ``no_proxy`` for one client construction.

    Returns the values to restore, or None when there was nothing to repair. The
    mutation is process-wide and is put back by the caller in a ``finally`` -- httpx
    reads the variable while the client is being constructed and never again.
    """
    saved: Dict[str, str] = {}
    for name in ("NO_PROXY", "no_proxy"):
        raw = os.environ.get(name)
        if raw is None:
            continue
        cleaned = _sanitize_no_proxy(raw)
        if cleaned != raw:
            saved[name] = raw
            os.environ[name] = cleaned

    return saved or None


def fetch_image_config(
    image: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout_s: float = 30.0,
    ca_bundle: Optional[str] = None,
    insecure: bool = False,
) -> ImageConfig:
    """Read what an image declares.

    Every field is present even on failure, so a caller never has to distinguish
    "no config" from "read failed" structurally -- ``error`` says which it was.
    Nothing is raised: restoring an image's config is best-effort, and a batch
    conversion must not stop because one registry was unreachable.

    ``ca_bundle`` and ``insecure`` are for self-hosted registries behind a private
    CA; see :func:`_open_client`.
    """
    # Keyed on the credentials too. An anonymous and an authenticated read of the
    # same private repository are different questions with different answers, so
    # caching only the reference would hand a caller who supplied credentials the
    # anonymous 401 from an earlier call. The TLS options belong in the key for the
    # same reason: a read that failed verification is a different answer from one
    # that succeeded.
    key = json.dumps([image, username, password, ca_bundle, insecure])
    cacheable = "@" in image
    cached = _CACHE.get(key) if cacheable else None
    if cached is not None:
        return cached.copy()

    host, repository, reference = parse_image_ref(image)

    try:
        with _open_client(timeout_s, ca_bundle=ca_bundle, insecure=insecure) as client:
            auth = _auth_headers(client, host, repository, username, password)
            session = _RegistrySession(client, repository, username, password, auth)
            base = f"https://{host}/v2/{repository}"

            manifest = session.get(f"{base}/manifests/{reference}")

            if isinstance(manifest, dict) and manifest.get("manifests"):
                # Multi-arch index: resolve to the linux/amd64 manifest. The token
                # the challenge produced is scoped to the repository, so it covers
                # this second read and the blob below without another round trip.
                digest = _pick_amd64(manifest, image)
                manifest = session.get(f"{base}/manifests/{digest}")

            config_digest = (manifest or {}).get("config", {}).get("digest")
            if not config_digest:
                raise RuntimeError(f"{image}: manifest names no config blob")

            blob = session.get(f"{base}/blobs/{config_digest}")

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
            error,
            image,
            host,
            repository,
            # Both, because that is what the request actually carried: a lone
            # username is not a credential the registry could have rejected.
            bool(username and password),
        )

    if cacheable and not result.error:
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
