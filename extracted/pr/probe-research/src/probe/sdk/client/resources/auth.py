"""AuthResource (client.auth, typed reads) and AuthMixin, Client's methods: sign-in, tokens, run
tokens, client installations and credential grants
(twins: app/accounts/auth, app/capture/clients/installations)."""

from __future__ import annotations
from ....generated.models import ClientInstallationsOut, TokenOut
from ..resource import Resource
import os
import sys
import time
import warnings


class AuthMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    # -- identity / auth ----------------------------------------------------
    def ensure_authenticated(self, *, interactive: bool | None = None) -> bool:
        """Make sure a user token exists, minting one via the browser device flow
        when a human can approve it.

        The interactive path runs only when stdin+stderr are TTYs and
        ``PROBE_AUTO_LOGIN`` is not ``0`` (or when ``interactive=True`` forces it).
        On success the token is persisted to the same config file the wizard's
        sign-in writes, so the browser round-trip happens once per machine. Returns
        True when a token is available; False leaves the transport to raise its normal
        ``AuthError`` on first use (the crisp headless/CI behavior)."""
        if self.settings.token:
            return True
        if interactive is None:
            interactive = (
                os.environ.get("PROBE_AUTO_LOGIN", "1") != "0"
                and sys.stdin.isatty()
                and sys.stderr.isatty()
            )
        if not interactive:
            return False
        from ...settings.settings import save_context
        from ...settings.device import DeviceLoginError, device_login

        print(
            f"no Probe token found — opening {self.settings.base_url} for browser approval…",
            file=sys.stderr,
        )

        def _show(prompt) -> None:
            print(f"  visit: {prompt.verification_uri_complete}", file=sys.stderr)
            print(f"  code:  {prompt.user_code}", file=sys.stderr)

        try:
            token = device_login(self.settings.base_url, on_prompt=_show)
        except DeviceLoginError as exc:
            warnings.warn(f"automatic device login failed: {exc}", stacklevel=2)
            return False
        save_context({"base_url": self.settings.base_url, "token": token})
        # Settings is shared with the transport; mutating it authenticates both.
        self.settings.token = token
        print("logged in — token saved for future runs", file=sys.stderr)
        return True

    def me(self) -> dict:
        # /v1/me (not the session-only /auth/me): resolves through the unified
        # door, so a `probe_pat` or OAuth token identifies its own tenant/role.
        return self.transport.get("/v1/me")

    def complete_desktop_onboarding(self) -> dict:
        """Acknowledge a finished native install for this credential's user/team.

        The server accepts only install → complete (or an already complete
        retry), preserving the browser's flow. No target identity is sent.
        """
        from ...delivery.transport.deadlines import deadline_scope

        with deadline_scope(time.monotonic() + 12):
            return self.transport.post("/v1/desktop/onboarding/complete", idempotent=True)

    def logout(self) -> dict:
        """Release the calling token from THIS machine.

        Device-aware on a current backend: the transport sends `X-Probe-Device`,
        so the server unbinds the credential from this machine and revokes it
        only when no other live device still holds it. That is what stops
        reauthorizing one laptop from signing another one out when both were
        using the same shared PAT.

        Returns `{revoked, detached, still_used_by}` so the caller can report
        what actually happened. An older backend answers 204 with no body, which
        arrives as `{}` -- callers must treat a missing `revoked` key as "this
        server could not tell me", never as "nothing happened".
        """
        return self.transport.delete("/v1/tokens/current") or {}

    # -- tokens -------------------------------------------------------------
    def list_tokens(self) -> list[dict]:
        """My live (unrevoked) tokens. Secrets are never returned — only
        ``token_prefix``, which is what a human matches against."""
        return self.transport.get("/v1/tokens")

    def create_token(
        self,
        name: str,
        *,
        scopes: list[str] | None = None,
        open_browser: bool = True,
        on_prompt=None,
    ) -> dict:
        """Mint a named token through the browser device flow.

        NOT ``POST /v1/tokens``: that route is session-only by design, so it 403s
        for a token-authenticated CLI. The device flow reaches the same minter with
        a human approving in the browser, which is what the invariant "a leaked
        token must not be able to mint more tokens" is protecting.

        Returns ``TokenCreated``; ``["token"]`` is the plaintext secret and this is
        the only time it exists. Callers must show it once and never persist it.
        """
        from ...settings.device import device_authorize

        # A named token is for another machine or a job: it must not take this
        # machine's device slot, or minting it signs this machine out.
        return device_authorize(
            self.settings.base_url,
            scopes=scopes,
            token_name=name,
            bind_device=False,
            open_browser=open_browser,
            on_prompt=on_prompt,
        )

    def revoke_token(self, token_id: str) -> None:
        """Revoke a token by id. Your own: any writer. A teammate's: needs a
        browser session AND owner/admin, so it 403s from the CLI (by design)."""
        self.transport.delete(f"/v1/tokens/{token_id}")

    # -- per-run tokens (a remote job's credential, one run only) ------------
    def mint_run_token(self, run_id: str, *, ttl_seconds: int | None = None) -> dict:
        """``POST /v1/runs/{id}/tokens`` -- a ``probe_run_`` token that records this
        run and nothing else, for a job on another machine. ``ttl_seconds`` is its
        life (the server's default when None); minting again never shortens an
        earlier token's. Returns ``{token, run_id, expires_at, ttl_seconds, gen}``."""
        body = {} if ttl_seconds is None else {"ttl_seconds": int(ttl_seconds)}
        return self.transport.post(f"/v1/runs/{run_id}/tokens", json_body=body)

    def extend_run_tokens(self, run_id: str, *, ttl_seconds: int) -> dict:
        """``POST /v1/runs/{id}/tokens/extend`` -- every token of this run now
        expires ``ttl_seconds`` from now. The running job keeps its token."""
        return self.transport.post(
            f"/v1/runs/{run_id}/tokens/extend", json_body={"ttl_seconds": int(ttl_seconds)}
        )

    def revoke_run_tokens(self, run_id: str) -> dict:
        """``POST /v1/runs/{id}/tokens/revoke`` -- every token minted for this run
        so far stops at its next request."""
        return self.transport.post(f"/v1/runs/{run_id}/tokens/revoke", json_body={})

    def run_token_state(self, run_id: str) -> dict:
        """``GET /v1/runs/{id}/tokens`` -- when this run's tokens expire. Never a token."""
        return self.transport.get(f"/v1/runs/{run_id}/tokens")

    # -- client installations ----------------------------------------------
    def register_client_capabilities(
        self,
        *,
        schema_version: int = 2,
        auto_update: str,
        tracking: str,
        capture: str,
        transcript_state: str | None = None,
        transcript_off_by: str | None = None,
        transcript_off_at: str | None = None,
    ) -> dict:
        """Replace the complete allowlisted snapshot for this token's install.

        The token identifies the installation; no token or installation id is
        accepted in the body. The schema deliberately carries only coarse
        tri-states, never paths, commands, environment variables, or secrets.

        v2 replaced v1's `mcp`/`skills` pair with a single `tracking` -- they
        were always written from one boolean -- and added `capture`, which v1
        could not report at all. The server still accepts v1 from clients in the
        field and reads their capture as `unknown`. v3 adds why transcripts are
        not uploading (control/080); its fields go only with `schema_version=3`.
        """
        body = {
            "schema_version": schema_version,
            "auto_update": auto_update,
            "tracking": tracking,
            "capture": capture,
        }
        if schema_version >= 3:
            body.update(
                transcript_state=transcript_state,
                transcript_off_by=transcript_off_by,
                transcript_off_at=transcript_off_at,
            )
        return self.transport.put("/v1/client-installations/current/capabilities", body)

    def name_client_installation(self, *, hostname: str) -> dict:
        """Name this token's installation after the machine it runs on.

        Sends the BARE hostname, not a label: the machine's name is a fact the
        client observes, and how it is rendered is the server's convention. Two
        callers composing their own label is how one laptop comes to appear
        under two spellings.

        The server replaces only names it generated itself, so a device someone
        named deliberately is left alone; `renamed` in the response says which
        happened. A backend that predates this route 404s, which the caller
        treats as "nothing to do".
        """
        return self.transport.put(
            "/v1/client-installations/current/name",
            {"hostname": hostname},
        )

    def create_credential_attachment_grant(self, installation_id: str) -> dict:
        """Mint a short-lived installation join grant with the linked API PAT."""
        return self.transport.post(
            f"/v1/client-installations/{installation_id}/credential-attachment-grants"
        )

    def attach_current_credential(self, installation_id: str, *, grant: str) -> dict:
        """Consume an API-minted join grant using this read-only MCP PAT."""
        return self.transport.put(
            f"/v1/client-installations/{installation_id}/credentials/current",
            {"grant": grant},
        )

    def mint_companion_credential(self) -> dict:
        """The Probe daemon's key for THIS installation, minted with its own
        `api` credential (no browser). Answers one approval-exchange grant
        entry: `{"grant": "companion", "token", "token_id"}`."""
        return self.transport.post("/v1/client-installations/current/companion-credential")

    def mint_capture_credential(self, source: str) -> dict:
        """One coding agent's capture key for THIS installation, minted with its
        own `api` credential (no browser). Answers one approval-exchange grant
        entry: `{"grant": "capture", "token", "device_id", "capture_source"}`."""
        return self.transport.post(
            "/v1/client-installations/current/capture-credential", {"source": source}
        )

    def list_client_installations(self) -> dict:
        """Unified view of installs, API/MCP credentials, and capture devices."""
        return self.transport.get("/v1/client-installations")

    def retire_client_installations(self, ids: list[str]) -> dict:
        """Retire these machines (`POST /v1/client-installations/retire`): their
        rows leave the dashboard, their capture keys and the credentials bound
        to them only are revoked. Explicit ids only; needs a token with the
        `delete` scope. 404 when none of them is live (already retired)."""
        return self.transport.post("/v1/client-installations/retire", {"ids": list(ids)})


class AuthResource(Resource):
    """`client.auth`: typed token and client-installation reads (`/v1/me` declares no model)."""

    __slots__ = ()

    def list_tokens(self) -> list[TokenOut]:
        """`Client.list_tokens` as `TokenOut`s."""
        return self._to_models(TokenOut, self._client.list_tokens())

    def list_installations(self) -> ClientInstallationsOut:
        """`Client.list_client_installations` as a `ClientInstallationsOut`."""
        return self._to_model(ClientInstallationsOut, self._client.list_client_installations())
