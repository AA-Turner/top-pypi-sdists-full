"""Frozen wire-level constants for the agent RPC protocol.

Everything here is part of the compatibility contract between a world-side
client and the agent daemon. Evolution rules (see docs/agent-rpc-design.md):
additive-only within /v1 — never rename or remove routes, headers, capability
names, or model fields. Breaking changes get a /v2 prefix served alongside /v1.
"""

from __future__ import annotations

PROTOCOL_VERSION = 1

# Fixed port on the session WireGuard mesh. Mesh traffic is session-private and
# already encrypted by WireGuard; auth is the bearer token, not TLS (v1).
DEFAULT_PORT = 7373

API_PREFIX = "/v1"

# --- Headers -----------------------------------------------------------------

HEADER_REQUEST_ID = "X-Plato-Request-Id"
# Absolute deadline budget in seconds for this request, enforced server-side
# (execs are cancelled, long-polls bounded). Float, as a decimal string.
HEADER_DEADLINE = "X-Plato-Deadline"
# Client-generated key for mutating ops that may be resent after a transport
# error. The daemon caches completed results per key so retry-once is
# exactly-once (unlike the git_ops stdio protocol's blind resend).
HEADER_IDEMPOTENCY_KEY = "X-Plato-Idempotency-Key"
HEADER_FILE_SHA256 = "X-Plato-File-Sha256"
HEADER_FILE_SIZE = "X-Plato-File-Size"
# Additive response header: set when the daemon answered a resend from its
# idempotency machinery instead of executing ("cache" = completed-result
# replay, "inflight" = joined the still-running first attempt). The client
# logs it — the only centralized evidence the exactly-once path exercised.
HEADER_DEDUPED = "X-Plato-Deduped"

# --- Capability names --------------------------------------------------------
# The handshake advertises these; the client gates every feature on the
# capability string, never on version comparisons. New ops ⇒ new names.

CAP_EXEC_RUN = "exec.run"
CAP_EXEC_SIGNAL = "exec.signal"
CAP_ENV_SETUP = "env.setup"
CAP_FILES_PUSH = "files.push"
CAP_FILES_PULL = "files.pull"
CAP_AGENT_JOB_START = "agent_job.start"
CAP_AGENT_JOB_WAIT = "agent_job.wait"
CAP_AGENT_JOB_SIGNAL = "agent_job.signal"
CAP_POOL_RESET = "pool.reset"
CAP_POOL_RECLAIM = "pool.reclaim"
CAP_HEALTH_REPORT = "health.report"
CAP_GIT = "git"

ALL_CAPABILITIES: tuple[str, ...] = (
    CAP_EXEC_RUN,
    CAP_EXEC_SIGNAL,
    CAP_ENV_SETUP,
    CAP_FILES_PUSH,
    CAP_FILES_PULL,
    CAP_AGENT_JOB_START,
    CAP_AGENT_JOB_WAIT,
    CAP_AGENT_JOB_SIGNAL,
    CAP_POOL_RESET,
    CAP_POOL_RECLAIM,
    CAP_HEALTH_REPORT,
    CAP_GIT,
)

# Flag groups the PLATO_AGENT_RPC_CAPS env var accepts (comma-separated), each
# expanding to the capability prefixes it governs.
FLAG_GROUPS: dict[str, tuple[str, ...]] = {
    "health": ("health.",),
    "env": ("env.",),
    "exec": ("exec.",),
    "files": ("files.",),
    "pool": ("pool.",),
    "git": ("git",),
    "job": ("agent_job.",),
}
FLAGS_ENV_VAR = "PLATO_AGENT_RPC_CAPS"

# --- Size limits -------------------------------------------------------------

# Ceiling for any request body (files push is the big consumer).
MAX_BODY_BYTES = 256 * 1024 * 1024
# Per-stream spool cap; the spool is truncated with a marker record beyond this.
SPOOL_CAP_BYTES = 512 * 1024 * 1024
# Default per-stream output cap for unary exec (head+tail truncation).
DEFAULT_EXEC_OUTPUT_BYTES = 1024 * 1024

# --- Daemon filesystem layout ------------------------------------------------

STATE_DIR = "/var/lib/plato-agent"
TOKEN_FILE = f"{STATE_DIR}/token"
PID_FILE = f"{STATE_DIR}/daemon.pid"
LOG_FILE = f"{STATE_DIR}/daemon.log"
JOBS_DIR = f"{STATE_DIR}/jobs"

# Exit code the bootstrap SSH command uses to signal "daemon entry point not
# installed" (stale baked SDK) — distinct from transport failures.
BOOTSTRAP_NO_DAEMON_RC = 42
