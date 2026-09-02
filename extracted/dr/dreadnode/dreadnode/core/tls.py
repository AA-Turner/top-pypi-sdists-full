"""Native host trust for Dreadnode-owned platform connections."""

import functools
import os
import ssl
import tempfile
import typing as t
from contextlib import suppress
from pathlib import Path

import requests
import truststore
from loguru import logger
from requests.adapters import HTTPAdapter

if t.TYPE_CHECKING:
    from requests.adapters import _HostParams, _PoolKwargs

TLS_TRUST_DOCS_URL = "https://docs.dreadnode.io/self-hosting/client-tls-trust/"

# The operator CA arrives in numbered PEM chunks rather than a mounted file
# because the sandbox providers do not share a volume mechanism: OpenSandbox
# `Volume` supports only host/pvc/ossfs backends, and E2B has no cluster volumes
# at all. A single combined bundle can exceed Linux MAX_ARG_STRLEN, so the API
# bounds each value and this process rejoins them before writing a file.
CA_BUNDLE_CHUNK_COUNT_ENV = "DREADNODE_CA_BUNDLE_CHUNKS"
CA_BUNDLE_CHUNK_PREFIX = "DREADNODE_CA_BUNDLE_PEM_"
CA_BUNDLE_FILE_ENV = "DREADNODE_CA_BUNDLE_FILE"
CA_BUNDLE_DIR_ENV = "DREADNODE_CA_BUNDLE_DIR"

# Written as the first line of every bundle we generate. Lets us recognise our
# own output and rebuild from the system trust store rather than appending to a
# previous run's file, which would grow without bound across restarts.
_GENERATED_MARKER = "# dreadnode-generated trust bundle (system + operator CA)"

# Every path-valued trust variable the runtime image actually honours. The image
# ships Python, curl, git, Node 22, Bun, the Claude Code CLI, uv and a set of Go
# binaries, and they do not share a trust mechanism:
#   SSL_CERT_FILE ................ Python/truststore, Go binaries, openssl
#   REQUESTS_CA_BUNDLE ........... requests, pip
#   CURL_CA_BUNDLE ............... curl
#   GIT_SSL_CAINFO ............... git
#   NODE_EXTRA_CA_CERTS .......... Node, Bun, Claude Code CLI, agent-browser
#   AWS_CA_BUNDLE ................ botocore, s3fs, mount-s3
#   GRPC_DEFAULT_SSL_ROOTS_FILE_PATH ... the OTLP span exporter
TRUST_FILE_ENV_VARS: tuple[str, ...] = (
    "SSL_CERT_FILE",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "GIT_SSL_CAINFO",
    "NODE_EXTRA_CA_CERTS",
    "AWS_CA_BUNDLE",
    "GRPC_DEFAULT_SSL_ROOTS_FILE_PATH",
)

# uv ignores every variable above and uses its own vendored roots unless told to
# read the platform trust store, so a capability install would still fail behind
# a TLS-intercepting proxy with all seven set correctly.
TRUST_FLAG_ENV_VARS: dict[str, str] = {"UV_NATIVE_TLS": "1"}

# Distribution trust bundles, in the order truststore itself probes them. Used
# only when OpenSSL's compiled-in path is missing.
_SYSTEM_BUNDLE_CANDIDATES: tuple[str, ...] = (
    "/etc/ssl/certs/ca-certificates.crt",  # Debian, Ubuntu
    "/etc/ssl/cert.pem",  # Alpine, Arch, RHEL 9+, BSD
    "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",  # Fedora 43+, RHEL 11+
    "/etc/pki/tls/cert.pem",  # RHEL <= 9, CentOS <= 9
    "/etc/ssl/ca-bundle.pem",  # SUSE
)

BUNDLE_FILE_NAME = "dreadnode-ca-bundle.pem"


def create_platform_ssl_context() -> ssl.SSLContext:
    """Create a verified TLS context backed by the host OS trust store."""
    ensure_trust_installed()
    return truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


@functools.lru_cache(maxsize=1)
def cached_platform_ssl_context() -> ssl.SSLContext:
    """A process-wide native-trust context, for callers that build many clients.

    Runtime connections construct a client per runtime and open a socket per
    session, so re-reading the OS trust store each time is pure overhead.
    """
    return create_platform_ssl_context()


class NativeTrustAdapter(HTTPAdapter):
    """Use an explicit SSL context while preserving Requests pool semantics."""

    def __init__(self, ssl_context: ssl.SSLContext) -> None:
        self.ssl_context = ssl_context
        super().__init__()

    def build_connection_pool_key_attributes(
        self,
        request: requests.PreparedRequest,
        verify: bool | str,
        cert: str | tuple[str, str] | None = None,
    ) -> "tuple[_HostParams, _PoolKwargs]":
        host_params, pool_kwargs = super().build_connection_pool_key_attributes(
            request,
            verify,
            cert,
        )
        if request.url and request.url.lower().startswith("https://") and verify is not False:
            pool_kwargs.pop("ca_certs", None)
            pool_kwargs.pop("ca_cert_dir", None)
            pool_kwargs["ssl_context"] = self.ssl_context
            pool_kwargs["cert_reqs"] = "CERT_REQUIRED"
        return host_params, pool_kwargs


def create_platform_http_session(
    ssl_context: ssl.SSLContext | None = None,
) -> requests.Session:
    """Create a Requests session using native trust for HTTPS destinations."""
    session = requests.Session()
    session.mount("https://", NativeTrustAdapter(ssl_context or create_platform_ssl_context()))
    return session


def format_tls_error(error: BaseException | str, error_type: str | None = None) -> str | None:
    """Return an actionable message when an error chain contains a TLS verification failure."""
    parts = [error_type or "", str(error)]
    if isinstance(error, BaseException):
        seen: set[int] = set()
        current: BaseException | None = error
        while current is not None and id(current) not in seen:
            seen.add(id(current))
            parts.extend((current.__class__.__name__, str(current)))
            current = current.__cause__ or current.__context__

    lowered = " ".join(parts).lower()
    if not any(
        marker in lowered
        for marker in (
            "certificate_verify_failed",
            "certificate verify failed",
            "sslcertverificationerror",
            "hostname mismatch",
            "certificate name does not match input",
            "certificate has expired",
            "certificate is not yet valid",
        )
    ):
        return None

    if any(
        marker in lowered
        for marker in (
            "hostname mismatch",
            "certificate name does not match input",
            "doesn't match",
            "not valid for",
            "ip address mismatch",
        )
    ):
        reason = "hostname mismatch"
        action = "Fix the server certificate SAN configuration."
    elif any(marker in lowered for marker in ("expired", "not yet valid", "not valid yet")):
        reason = "certificate validity or system clock"
        action = "Renew the certificate or correct the client clock."
    elif any(
        marker in lowered
        for marker in (
            "unable to get local issuer",
            "unable to verify the first certificate",
            "self-signed certificate",
            "unknown ca",
            "unknown issuer",
        )
    ):
        reason = "unknown issuer or incomplete chain"
        action = "Install or repair the organization CA chain in the OS trust store."
    else:
        reason = "certificate verification failed"
        action = "Check the server certificate and the host OS trust store."

    return f"TLS certificate verification failed: {reason}. {action} See {TLS_TRUST_DOCS_URL}"


def _read_operator_ca() -> str | None:
    """Return the operator-supplied CA chain as PEM text, or None if unset.

    ``DREADNODE_CA_BUNDLE_FILE`` points at an already-mounted file and wins over
    the numbered ``DREADNODE_CA_BUNDLE_PEM_*`` transport, since a real file is
    the more specific instruction.
    """
    file_path = os.environ.get(CA_BUNDLE_FILE_ENV, "").strip()
    if file_path:
        try:
            text = Path(file_path).read_text(encoding="utf-8")
        except OSError as exc:
            logger.warning("Operator CA file {} is unreadable: {}", file_path, exc)
        else:
            if text.strip():
                return text
            logger.warning("Operator CA file {} is empty, ignoring", file_path)

    raw_count = os.environ.get(CA_BUNDLE_CHUNK_COUNT_ENV, "").strip()
    if not raw_count:
        return None
    try:
        count = int(raw_count)
    except ValueError:
        logger.warning("Ignoring invalid {}={!r}", CA_BUNDLE_CHUNK_COUNT_ENV, raw_count)
        return None
    if count < 1:
        logger.warning("Ignoring non-positive {}={}", CA_BUNDLE_CHUNK_COUNT_ENV, count)
        return None

    chunks: list[str] = []
    for index in range(count):
        name = f"{CA_BUNDLE_CHUNK_PREFIX}{index}"
        chunk = os.environ.get(name)
        if chunk is None:
            logger.warning(
                "Ignoring incomplete operator CA bundle: {} declares {} chunks but {} is missing",
                CA_BUNDLE_CHUNK_COUNT_ENV,
                count,
                name,
            )
            return None
        chunks.append(chunk)

    inline = "".join(chunks)
    return inline if inline.strip() else None


def _read_system_bundle() -> str:
    """Return the distribution trust bundle as PEM text.

    Deliberately reads OpenSSL's *compiled-in* path rather than the effective
    one. ``ssl.get_default_verify_paths().cafile`` already reflects
    ``SSL_CERT_FILE``, so on a second call it would point at the file this
    module wrote and we would concatenate our own output into itself.
    """
    candidates: list[str] = []
    compiled_in = ssl.get_default_verify_paths().openssl_cafile
    if compiled_in:
        candidates.append(compiled_in)
    candidates.extend(_SYSTEM_BUNDLE_CANDIDATES)

    for candidate in candidates:
        try:
            text = Path(candidate).read_text(encoding="utf-8")
        except OSError:
            continue
        if _GENERATED_MARKER in text:
            continue
        if text.strip():
            return text

    logger.warning(
        "No system trust bundle found; the operator CA will be the only trusted root "
        "and public TLS from this sandbox will fail. Checked: {}",
        ", ".join(candidates),
    )
    return ""


def _resolve_bundle_dir() -> Path | None:
    """Pick a writable directory for the generated bundle.

    Ordered so an operator can pin a location under a read-only root filesystem,
    where a writable path is usually an explicitly mounted volume rather than
    anywhere this function could guess.

    Deliberately short. Callers outside this process have to name the resulting
    file — the sandbox container sets ``SSL_CERT_FILE`` and friends to it from
    the pod environment — so every extra candidate is a way for the path they
    were given and the path we write to disagree.
    """
    candidates: list[Path] = []
    override = os.environ.get(CA_BUNDLE_DIR_ENV, "").strip()
    if override:
        candidates.append(Path(override))
    candidates.append(Path(tempfile.gettempdir()))
    candidates.append(Path.home() / ".dreadnode")

    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".dreadnode-trust-probe"
            probe.write_text("", encoding="utf-8")
            probe.unlink()
        except OSError:
            continue
        return candidate

    logger.error(
        "No writable directory for the trust bundle. Tried: {}. Set {} to a writable path.",
        ", ".join(str(c) for c in candidates),
        CA_BUNDLE_DIR_ENV,
    )
    return None


def install_trust_bundle() -> Path | None:
    """Materialize system + operator CA trust and export it to this process tree.

    Returns the generated bundle path, or None when no operator CA is configured
    (the overwhelmingly common case, where the stock trust store is correct and
    this is a no-op).

    Must run before the first outbound TLS call. ``SSL_CERT_FILE`` *replaces* the
    trust store rather than adding to it, so exporting the operator CA on its own
    would leave the sandbox unable to verify any public host — the concatenation
    below is what keeps both working, and its absence fails silently.

    Mutates ``os.environ`` so subprocesses the runtime spawns (MCP servers,
    workers, capability install scripts, agent shell commands) inherit the same
    trust without every call site having to know about it.
    """
    operator_ca = _read_operator_ca()
    if operator_ca is None:
        return None

    bundle_dir = _resolve_bundle_dir()
    if bundle_dir is None:
        return None

    system_bundle = _read_system_bundle()
    parts = [_GENERATED_MARKER, ""]
    if system_bundle:
        parts.append(system_bundle.strip())
    parts.append(operator_ca.strip())
    contents = "\n".join(parts) + "\n"

    bundle_path = bundle_dir / BUNDLE_FILE_NAME
    try:
        bundle_path.write_text(contents, encoding="utf-8")
    except OSError as exc:
        logger.error("Failed writing trust bundle to {}: {}", bundle_path, exc)
        return None

    # Best-effort, and separate from the write above. The sandbox image seeds
    # this path so the container's trust variables never dangle, which leaves a
    # file we can write but do not own — and `chmod` on a file you do not own
    # fails. That seed is already world-readable, so there is nothing to fix.
    with suppress(OSError):
        bundle_path.chmod(0o644)

    export_trust_env(bundle_path)

    # Anything built before the env changed still holds the old roots.
    cached_platform_ssl_context.cache_clear()

    logger.info(
        "Installed operator CA trust | path={} | system_roots={} | vars={}",
        bundle_path,
        "present" if system_bundle else "MISSING",
        len(TRUST_FILE_ENV_VARS) + len(TRUST_FLAG_ENV_VARS),
    )
    return bundle_path


def export_trust_env(bundle_path: Path) -> None:
    """Point every trust variable the image honours at *bundle_path*.

    Set unconditionally rather than with ``setdefault``. An operator who has
    already exported one of these has almost certainly set it to the bare
    corporate CA, which is the silent-breakage case this function exists to
    prevent; the generated bundle is a strict superset of that.
    """
    resolved = str(bundle_path)
    for name in TRUST_FILE_ENV_VARS:
        os.environ[name] = resolved
    for name, value in TRUST_FLAG_ENV_VARS.items():
        os.environ[name] = value


@functools.lru_cache(maxsize=1)
def ensure_trust_installed() -> Path | None:
    """Install operator CA trust once per process, before the first TLS call.

    ``run_server()`` is not the only way into the SDK — the CLI, and an agent
    running its own ``import dreadnode`` script inside a sandbox, both reach the
    platform without going near it. Hanging this off context creation covers all
    of them, at the cost of a factory that writes a file and mutates
    ``os.environ`` the first time it is called. That side effect is real but
    narrow: ``install_trust_bundle()`` returns immediately unless an operator CA
    is actually configured, so on a public deployment this does nothing at all.

    Memoized rather than deferring to ``install_trust_bundle()`` directly, since
    clients are built per connection and rewriting the bundle for each one is
    pure overhead.
    """
    return install_trust_bundle()
