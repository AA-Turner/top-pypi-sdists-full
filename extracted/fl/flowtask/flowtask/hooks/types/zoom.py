import hashlib
import hmac
import json
import re
import time
from ipaddress import ip_address, ip_network

from aiohttp import web

from .web import WebHook

_CRC_TOKEN_MAX_LEN = 256
_CRC_REJECT_PREFIXES = ("v0:", "v0=")
# Permissive: covers base64 standard + base64url + the few separators Zoom
# tokens have historically used. Notably excludes ":" which is the only
# character a forged signing-message input would need.
_CRC_TOKEN_RE = re.compile(r"^[A-Za-z0-9._\-=+/]+$")


class ZoomWebHook(WebHook):
    """Zoom event-subscription webhook receiver.

    Handles CRC handshake and HMAC-SHA256 signature verification for
    Zoom Phone event subscriptions. Pattern mirrors jira.py:172-189.
    """

    methods: list = ["GET", "POST"]
    default_status: int = 200

    def __init__(
        self,
        *args,
        secret_token: str | None = None,
        replay_window_seconds: int | None = None,
        allowed_cidrs: str | list[str] | None = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        if secret_token is None:
            from flowtask.conf import ZOOM_WEBHOOK_SECRET_TOKEN
            secret_token = ZOOM_WEBHOOK_SECRET_TOKEN
        self._secret_token: str = secret_token or ""
        if replay_window_seconds is None:
            from flowtask.conf import ZOOM_WEBHOOK_REPLAY_WINDOW_SECONDS
            replay_window_seconds = ZOOM_WEBHOOK_REPLAY_WINDOW_SECONDS
        self._replay_window: int = int(replay_window_seconds)
        if allowed_cidrs is None:
            from flowtask.conf import ZOOM_ALLOWED_CIDRS
            allowed_cidrs = ZOOM_ALLOWED_CIDRS
        self._allowed_networks = self._parse_cidrs(allowed_cidrs)
        if not self._secret_token:
            self._logger.warning(
                "ZoomWebHook %s: empty secret token; all events will be rejected with 401.",
                self.trigger_id,
            )

    @staticmethod
    def _parse_cidrs(value) -> list:
        if not value:
            return []
        if isinstance(value, str):
            items = [s.strip() for s in value.split(",") if s.strip()]
        else:
            items = list(value)
        return [ip_network(item, strict=False) for item in items]

    def _verify_signature(self, ts: str, raw: bytes, sig: str) -> bool:
        """Return True only if sig is a valid HMAC-SHA256 v0 signature."""
        if not (self._secret_token and ts and sig):
            return False
        msg = b"v0:" + ts.encode("utf-8") + b":" + raw
        expected = "v0=" + hmac.new(
            self._secret_token.encode("utf-8"), msg, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, sig)

    def _validate_crc_token(self, plain: str) -> str | None:
        """Return None if acceptable, else a short reason string for the 400 body."""
        if not plain:
            return "empty plainToken"
        if len(plain) > _CRC_TOKEN_MAX_LEN:
            return "plainToken too long"
        for prefix in _CRC_REJECT_PREFIXES:
            if plain.startswith(prefix):
                return "plainToken has reserved prefix"
        if not _CRC_TOKEN_RE.fullmatch(plain):
            return "plainToken contains disallowed characters"
        return None

    def _crc_response(self, plain_token: str) -> dict:
        """Return the CRC handshake payload expected by Zoom."""
        encrypted = hmac.new(
            self._secret_token.encode("utf-8"),
            plain_token.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return {"plainToken": plain_token, "encryptedToken": encrypted}

    async def _pre_post(self, request: web.Request) -> "web.Response | None":
        """Enforce the IP allowlist when configured.

        Returns 403 if the client IP does not fall within any of the
        configured CIDRs. Empty allowlist → returns None (no-op, FEAT-013
        behavior preserved).

        Trust order: X-Forwarded-For first hop, then ``request.remote``.

        Subclass contract: subclasses MUST call ``await super()._pre_post(request)``
        first and short-circuit on a non-None return.
        """
        if not self._allowed_networks:
            return None
        xff = request.headers.get("X-Forwarded-For")
        raw_ip = xff.split(",", 1)[0].strip() if xff else request.remote
        if not raw_ip:
            self._logger.warning(
                "ZoomWebHook %s: rejected request with no source IP", self.trigger_id
            )
            return web.Response(status=403, text="untrusted source")
        try:
            client_ip = ip_address(raw_ip)
        except ValueError:
            self._logger.warning(
                "ZoomWebHook %s: rejected unparseable source IP %r",
                self.trigger_id,
                raw_ip[:64],
            )
            return web.Response(status=403, text="untrusted source")
        for net in self._allowed_networks:
            if client_ip in net:
                return None
        self._logger.warning(
            "ZoomWebHook %s: rejected source IP %s (not in allowlist)",
            self.trigger_id,
            client_ip,
        )
        return web.Response(status=403, text="untrusted source")

    async def get(self, request: web.Request) -> web.Response:
        return web.Response(status=200, text="ok")

    async def post(self, request: web.Request) -> web.Response:
        blocked = await self._pre_post(request)
        if blocked is not None:
            return blocked

        raw = await request.read()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            self._logger.warning(
                "ZoomWebHook %s: invalid JSON body", self.trigger_id
            )
            return web.Response(status=400, text="invalid json")

        event = data.get("event", "")

        # CRC handshake — no signature required during endpoint validation
        if event == "endpoint.url_validation":
            if not self._secret_token:
                self._logger.error(
                    "ZoomWebHook %s: CRC arrived but secret is empty", self.trigger_id
                )
                return web.Response(status=500, text="secret not configured")
            plain = (data.get("payload") or {}).get("plainToken", "")
            reason = self._validate_crc_token(plain)
            if reason is not None:
                self._logger.warning(
                    "ZoomWebHook %s: rejected CRC token (%s)", self.trigger_id, reason,
                )
                return web.Response(status=400, text=reason)
            return web.json_response(
                self._crc_response(plain), status=self.default_status
            )

        # Signature verification for real events
        sig = request.headers.get("x-zm-signature", "")
        ts = request.headers.get("x-zm-request-timestamp", "")
        if not self._verify_signature(ts, raw, sig):
            self._logger.warning(
                "ZoomWebHook %s: signature mismatch", self.trigger_id
            )
            return web.Response(status=401, text="invalid signature")

        # Replay window protection
        try:
            req_ts = int(ts)
            if abs(time.time() - req_ts) > self._replay_window:
                self._logger.warning(
                    "ZoomWebHook %s: stale request (ts=%s, window=%ss)",
                    self.trigger_id,
                    ts,
                    self._replay_window,
                )
                return web.Response(status=401, text="stale request")
        except (TypeError, ValueError):
            return web.Response(status=401, text="invalid timestamp")

        await self.run_actions(
            payload=data, raw_body=raw, headers=dict(request.headers)
        )
        return web.Response(status=self.default_status, text="ok")
