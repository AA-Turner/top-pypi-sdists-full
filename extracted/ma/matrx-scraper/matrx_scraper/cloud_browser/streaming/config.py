"""CAPS constants and injected configuration for the streaming/takeover plane.

Everything here that is a *policy* — a TTL, a cadence, a viewport size, the
first-release media rules — is a CAPS constant, per repo doctrine ("config is
not an env var"). The only things that are genuinely per-deployment VALUES —
the ES256 signing key, the coTURN shared secret, the allowed web origins, the
gateway host — arrive through :class:`StreamingConfig`, injected by the host at
startup. Nothing in this module reads ``os.environ``.

Authority: contracts/S4-stream-tickets.md §Vocabulary (lifetimes table),
§0 (issuer/audience/TTL block), §8 (TURN), PLAN.md §First-release media policy.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- Ticket / issuer identity (S4 §0) -------------------------------------
STREAM_ISSUER_NAME = "matrx-browser-stream"
STREAM_AUDIENCE = "browser_stream"

# --- Lifetimes, all CAPS (S4 §1 lifetimes table) --------------------------
TICKET_TTL_SECONDS = 60  # PLAN.md pins 60s
TICKET_MAX_TTL = 60  # a stream ticket may never be long-lived
CONTROL_LEASE_TTL_SECONDS = 60  # identical to the run lease (S4 §5.3)
CONTROL_LEASE_RENEW_INTERVAL_SECONDS = 20  # identical to the run heartbeat
STREAM_COOKIE_MAX_AGE_SECONDS = 120  # 2x lease; the cookie is a carrier not the authority
HANDOFF_RECONNECT_GRACE_SECONDS = 300  # dropped human may reconnect without re-requesting control
HANDOFF_IDLE_TIMEOUT_SECONDS = 1800  # PLAN.md's 30 minutes without input
TURN_CREDENTIAL_TTL_SECONDS = 120  # long enough for ICE gathering, useless later

# --- Ticket audit retention (S4 §3.3) -------------------------------------
TICKET_HASH_RETENTION_SECONDS = 24 * 3600  # replay forensics window, then purge

# --- Reconnect abuse backstop (S4 §7.1) -----------------------------------
RECONNECT_LOOP_LIMIT = 20
RECONNECT_LOOP_WINDOW_SECONDS = 300

# --- Cookie (S4 §4.2) -----------------------------------------------------
STREAM_COOKIE_NAME = "__Secure-mtx_stream"

# --- Scopes (S4 §3.1) -----------------------------------------------------
SCOPE_VIDEO = "stream:video"
SCOPE_AUDIO = "stream:audio"
SCOPE_INPUT = "input:xtest"


@dataclass(frozen=True)
class MediaPolicy:
    """Server-declared, first-release media rules (PLAN.md §First-release media
    policy). The client renders from what the server sends; it never carries its
    own copy, so tightening the policy is a server-only change."""

    video: bool = True
    audio: bool = False
    clipboard: bool = False
    microphone: bool = False
    camera: bool = False
    file_transfer: bool = False

    def as_dict(self) -> dict[str, bool]:
        return {
            "video": self.video,
            "audio": self.audio,
            "clipboard": self.clipboard,
            "microphone": self.microphone,
            "camera": self.camera,
            "file_transfer": self.file_transfer,
        }


# The one first-release policy for a control (takeover) stream. Audio is OFF by
# default; a deployment may enable it, but a `view` stream forces it false
# regardless (S4 §9).
CONTROL_MEDIA_POLICY = MediaPolicy(video=True, audio=False)
VIEW_MEDIA_POLICY = MediaPolicy(video=True, audio=False)

# Fixed, server-controlled viewport; resize negotiation disabled during actions
# (PLAN.md). CAPS — the worker's Xvfb display is launched to match.
VIEWPORT_WIDTH = 1280
VIEWPORT_HEIGHT = 800


class StreamTicketNotConfigured(RuntimeError):
    """Raised (→ loud 503) when a stream route is hit but no signing key was
    injected. Never a fallback to the broker key or a silent no-op."""


@dataclass
class StreamingConfig:
    """Host-injected deployment VALUES. Constructed once at startup and handed
    to the mint service, gateway, and TURN minter.

    Parameters
    ----------
    stream_signing_key_pem:
        EC P-256 (ES256) private key PEM — its OWN key, never the broker's, so
        rotating or compromising one system never touches the other
        (``BROWSER_STREAM_TOKEN_SIGNING_KEY``). Unset -> every stream route 503s.
    allowed_origins:
        Exact web origins (scheme+host+port) permitted to mint/claim. Byte-for-byte
        equality, no suffix matching, no wildcard (S4 §3.2 B3).
    turn_shared_secret:
        coTURN REST-API shared secret. Lives ONLY on the gateway and the coTURN
        host — never in a ticket, a client bundle, or the worker (S4 §8).
    turn_realm / stun_urls / turn_urls:
        coTURN advertisement. `turn_urls` are handed to the client; the shared
        secret is not.
    gateway_ws_base:
        The gateway's public wss base (e.g. ``wss://stream.aimatrx.com``). The
        ``endpoint`` field is built here and returned as *data* — the client never
        constructs it (S4 §2.1).
    turn_rest_digest:
        The HMAC digest coTURN's REST mechanism uses. Default ``sha1`` (classic
        REST). Pinned from the deployed coTURN build — see OPEN(turn-rest-hash).
    """

    stream_signing_key_pem: str | None = None
    allowed_origins: frozenset[str] = field(default_factory=frozenset)
    turn_shared_secret: str | None = None
    turn_realm: str = "aimatrx.com"
    stun_urls: tuple[str, ...] = ()
    turn_urls: tuple[str, ...] = ()
    gateway_ws_base: str = "wss://stream.aimatrx.com"
    turn_rest_digest: str = "sha1"

    def require_signing_key(self) -> str:
        if not self.stream_signing_key_pem:
            raise StreamTicketNotConfigured(
                "BROWSER_STREAM_TOKEN_SIGNING_KEY is not configured; every stream "
                "route must 503 rather than fall back to another key."
            )
        return self.stream_signing_key_pem

    def origin_allowed(self, origin: str | None) -> bool:
        return bool(origin) and origin in self.allowed_origins
