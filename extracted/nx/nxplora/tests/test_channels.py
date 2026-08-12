"""
test_channels.py — maddog suite for the Channels OAuth framework + Meta connector.

Intent: try to make it fake a success, leak a secret, or claim "connected" when
it isn't. Every path must fail closed and honest. The real Keychain + Meta API
are mocked so the suite is hermetic.

Run: python3 -m unittest tests.test_channels
"""
import json
import os
import sys
import time
import types
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_channels  # noqa: E402
import nx_channel_tools  # noqa: E402


class FakeKeychain:
    """In-memory stand-in for the macOS `security` subprocess."""
    def __init__(self):
        self.store = {}

    def __call__(self, args, input_text=None):
        cp = types.SimpleNamespace(returncode=1, stdout="", stderr="")
        if not args:
            return cp
        op = args[0]
        # parse -s <service> and -w <value?>
        svc = None
        val = None
        if "-s" in args:
            svc = args[args.index("-s") + 1]
        if op == "find-generic-password":
            if svc in self.store:
                cp.returncode = 0
                cp.stdout = self.store[svc] + "\n"
        elif op == "add-generic-password":
            # -w <value> present for writes
            if "-w" in args:
                wi = args.index("-w")
                val = args[wi + 1] if wi + 1 < len(args) else ""
            self.store[svc] = val
            cp.returncode = 0
        elif op == "delete-generic-password":
            if svc in self.store:
                del self.store[svc]
                cp.returncode = 0
        return cp


def fake_response(status=200, payload=None, text=""):
    r = mock.Mock()
    r.status_code = status
    r.json = mock.Mock(return_value=(payload if payload is not None else {}))
    r.text = text or json.dumps(payload or {})
    return r


class ChannelsBaseTests(unittest.TestCase):
    """Base ChannelConnector behavior for remaining per-operator OAuth apps."""

    def setUp(self):
        self.kc = FakeKeychain()
        self._patch = mock.patch.object(nx_channels, "_security", self.kc)
        self._patch.start()
        self.addCleanup(self._patch.stop)
        self.li = nx_channels.GenericOAuthConnector(
            "Test OAuth",
            "https://example.com/oauth/authorize",
            "https://example.com/oauth/token",
            scopes=["read"],
        )

    # ── fail-closed when NOT configured ──────────────────────────────────────
    def test_unconfigured_status_is_honest(self):
        s = self.li.status()
        self.assertFalse(s["configured"])
        self.assertFalse(s["connected"])

    def test_unconfigured_preflight_blocks_with_setup_hint(self):
        pf = self.li.preflight("publish")
        self.assertFalse(pf["ok"])
        self.assertEqual(pf["detail"], "not_configured")
        self.assertIn("setup", pf["hint"])

    def test_unconfigured_publish_refuses_never_fakes(self):
        with mock.patch.object(nx_channels, "_oauth_vault_connection", return_value=None):
            out = nx_channels.XChannel().publish_text("hello")
        self.assertFalse(out["ok"])
        self.assertEqual(out["detail"], "not_connected")

    def test_unconfigured_exchange_raises(self):
        with self.assertRaises(nx_channels.ChannelError):
            self.li.exchange_code("abc")

    # ── configured but NOT connected ─────────────────────────────────────────
    def test_configured_not_connected(self):
        self.assertTrue(self.li.setup("APPID123", "APPSECRET456"))
        self.assertTrue(self.li.is_configured())
        self.assertFalse(self.li.is_connected())
        pf = self.li.preflight("publish")
        self.assertEqual(pf["detail"], "not_connected")
        self.assertIn("connect", pf["hint"])

    def test_auth_url_carries_redirect_state(self):
        self.li.setup("APPID123", "APPSECRET456")
        url = self.li.auth_url(state="xyz")
        self.assertIn("client_id=APPID123", url)
        self.assertIn("state=xyz", url)
        # redirect is loopback only
        self.assertIn("localhost", url)

    # ── credentials + tokens live ONLY in the (mock) Keychain ────────────────
    def test_secrets_only_in_keychain_not_returned_by_status(self):
        self.li.setup("APPID123", "APPSECRET456")
        s = self.li.status()
        self.assertNotIn("APPSECRET456", json.dumps(s))
        # but they ARE in the keychain store
        self.assertIn("APPSECRET456", self.kc.store.values())

    def test_keychain_name_validation_blocks_injection(self):
        self.assertFalse(nx_channels._safe_kc_name("evil; rm -rf /"))
        self.assertFalse(nx_channels._safe_kc_name("a name with spaces"))
        self.assertTrue(nx_channels._safe_kc_name("nx-channel-test-oauth-token"))
        # kc_get with a bad name returns None without calling security
        self.assertIsNone(nx_channels.kc_get("bad name; whoami"))

    # ── token expiry honesty ─────────────────────────────────────────────────
    def test_expired_token_is_not_connected(self):
        self.li.setup("APPID123", "APPSECRET456")
        self.li._save_token({"access_token": "T", "expires_at": time.time() - 10})
        self.assertFalse(self.li.is_connected())
        self.li._save_token({"access_token": "T", "expires_at": time.time() + 9999})
        self.assertTrue(self.li.is_connected())


class BosTokenResolutionTests(unittest.TestCase):
    """Regression: _bos_token() must find a signed-in session regardless of
    HOW the operator signed in. Caught live 2026-06-28 — a real signed-in
    operator got "not_signed_in" on /publish connect google because the
    function only checked nx_token, never the plain `token` field a pasted
    API key (or an unrefreshed OAuth session) uses.

    nx_cli is mocked directly (not the real ~/.nx/config.json) so these tests
    never depend on whatever session state happens to exist on the machine
    running them."""

    def _fake_nx_cli(self, cfg):
        fake = types.SimpleNamespace(
            load_config=lambda: dict(cfg),
            refresh_token_if_needed=lambda c: c,
        )
        return mock.patch.dict(sys.modules, {"nx_cli": fake})

    def test_falls_back_to_plain_token_field(self):
        # The pasted-API-key sign-in path only ever sets `token`, never nx_token.
        with self._fake_nx_cli({"token": "PASTED_KEY"}):
            self.assertEqual(nx_channels._bos_token(), "PASTED_KEY")

    def test_prefers_gateway_session_token_over_nx_token(self):
        # business-os (api.nexplora.ai) validates the gateway SESSION JWT (cfg["token"]) via
        # supabase.auth.getUser; the tiyon-bridge nx_token is a DIFFERENT project's JWT that
        # getUser rejects (401). So _bos_token() prefers `token`, with nx_token only a fallback.
        with self._fake_nx_cli({"token": "SESSION_JWT", "nx_token": "TIYON_BRIDGE_JWT"}):
            self.assertEqual(nx_channels._bos_token(), "SESSION_JWT")
        # nx_token is used only when no session token is present.
        with self._fake_nx_cli({"nx_token": "TIYON_BRIDGE_JWT"}):
            self.assertEqual(nx_channels._bos_token(), "TIYON_BRIDGE_JWT")

    def test_empty_config_falls_back_to_raw_file_then_honest_empty(self):
        with self._fake_nx_cli({}):
            with mock.patch.object(nx_channels, "_bos_cfg", return_value={}):
                self.assertEqual(nx_channels._bos_token(), "")
                self.assertEqual(nx_channels._bos_get("/api/business-os/connections"),
                                  {"ok": False, "error": "not_signed_in"})

    def test_nx_cli_import_failure_falls_back_to_raw_config_file(self):
        # If the nx_cli path can't be used for any reason, the raw ~/.nx/config.json
        # read (_bos_cfg) is still a valid fallback — never silently empty when a
        # token genuinely exists on disk.
        with mock.patch.dict(sys.modules, {"nx_cli": None}):
            with mock.patch.object(nx_channels, "_bos_cfg",
                                   return_value={"token": "RAW_FILE_TOKEN"}):
                self.assertEqual(nx_channels._bos_token(), "RAW_FILE_TOKEN")


class BosBridgedChannelTests(unittest.TestCase):
    """Meta + TikTok + Google + Snapchat connect through Nexplora's own shared
    app (server-side OAuth in nexplora-v2), not a local per-operator app.
    These tests mock the HTTP bridge functions directly — no real network, no
    real Keychain need (there's nothing local to store for these anymore)."""

    def setUp(self):
        self.meta = nx_channels.MetaChannel()
        self.tiktok = nx_channels.TikTokChannel()
        self.google = nx_channels.GoogleChannel()
        self.snapchat = nx_channels.SnapchatChannel()

    def test_bos_platform_mapping(self):
        # TikTok/Snapchat connect through the business-os bridge (bos_platform).
        # Meta moved to the canonical cross-surface OAuth vault.
        # Google moved OFF the bos-platform bridge to the shared 'google' web-OAuth grant
        # (_GoogleAdsYouTubeBridgedChannel), so it no longer carries a bos_platform.
        self.assertEqual(self.tiktok.bos_platform, "tiktok")
        self.assertEqual(self.snapchat.bos_platform, "snapchat")
        self.assertFalse(hasattr(self.meta, "bos_platform"))
        self.assertFalse(hasattr(self.google, "bos_platform"))

    def test_always_configured_nothing_to_set_up_locally(self):
        # Nexplora's own app already exists server-side — no local setup step.
        self.assertTrue(self.meta.is_configured())
        self.assertTrue(self.tiktok.is_configured())
        self.assertTrue(self.google.is_configured())
        self.assertTrue(self.snapchat.is_configured())

    def test_is_connected_reflects_the_real_bridge_not_local_state(self):
        with mock.patch.object(nx_channels, "_oauth_vault_is_connected", return_value=False):
            self.assertFalse(self.meta.is_connected())
        with mock.patch.object(nx_channels, "_oauth_vault_is_connected", return_value=True):
            self.assertTrue(self.meta.is_connected())

    def test_meta_preflight_uses_the_deployed_server_execution_proxy(self):
        with mock.patch.object(
                nx_channels,
                "_oauth_vault_connection",
                return_value={"providerSlug": "meta", "status": "connected"}):
            pf = self.meta.preflight("publish")
        self.assertTrue(pf["ok"])

    def test_preflight_refuses_when_not_connected(self):
        with mock.patch.object(nx_channels, "_bos_is_connected", return_value=False):
            pf = self.tiktok.preflight("publish")
        self.assertFalse(pf["ok"])
        self.assertEqual(pf["detail"], "not_connected")
        self.assertIn("connect", pf["hint"])

    def test_connect_opens_real_nexplora_url_not_localhost(self):
        with mock.patch.object(nx_channels, "_oauth_vault_connect_url",
                               return_value=("https://api.nexplora.ai/api/oauth/initiate/meta?x=1", None)):
            with mock.patch.object(nx_channels, "_oauth_vault_is_connected", return_value=True):
                with mock.patch("webbrowser.open") as wb:
                    out = nx_channels.connect_channel(self.meta, open_browser=True, timeout=5)
        self.assertTrue(out["ok"])
        opened_url = wb.call_args[0][0]
        self.assertIn("api.nexplora.ai", opened_url)
        self.assertNotIn("localhost", opened_url)

    def test_connect_not_signed_in_fails_fast_no_hang(self):
        with mock.patch.object(nx_channels, "_bos_connect_url", return_value=(None, "not_signed_in")):
            out = nx_channels.connect_channel(self.tiktok, open_browser=False, timeout=5)
        self.assertFalse(out["ok"])
        self.assertEqual(out["detail"], "not_signed_in")

    def test_connect_timeout_is_honest_not_faked(self):
        with mock.patch.object(nx_channels, "_bos_connect_url", return_value=("https://api.nexplora.ai/x", None)):
            with mock.patch.object(nx_channels, "_bos_is_connected", return_value=False):
                out = nx_channels.connect_channel(self.tiktok, open_browser=False, timeout=0.05)
        self.assertFalse(out["ok"])
        self.assertEqual(out["detail"], "authorization_not_completed")

    def test_disconnect_calls_the_bridge_not_local_keychain(self):
        with mock.patch.object(nx_channels, "_oauth_vault_disconnect", return_value={"ok": True}) as d:
            ok = self.meta.disconnect()
        self.assertTrue(ok)
        d.assert_called_once_with("meta")

    def test_meta_x_and_linkedin_use_one_nexplora_vault_bridge(self):
        x = nx_channels.get_channel("x")
        li = nx_channels.get_channel("linkedin")
        self.assertNotIsInstance(x, nx_channels._BosBridgedChannel)
        self.assertNotIsInstance(li, nx_channels._BosBridgedChannel)
        self.assertIsInstance(self.meta, nx_channels._NexploraOAuthBridgedChannel)
        self.assertIsInstance(x, nx_channels._NexploraOAuthBridgedChannel)
        self.assertIsInstance(li, nx_channels._NexploraOAuthBridgedChannel)

    def test_web_connection_is_immediately_visible_to_cli_status(self):
        rows = [{"providerSlug": "meta", "status": "connected"}]
        with mock.patch.object(nx_channels, "_oauth_vault_connections", return_value=rows):
            self.assertTrue(nx_channels.MetaChannel().is_connected())
        rows = [{"providerSlug": "x", "status": "connected"}]
        with mock.patch.object(nx_channels, "_oauth_vault_connections", return_value=rows):
            self.assertTrue(nx_channels.XChannel().is_connected())
            self.assertFalse(nx_channels.LinkedInChannel().is_connected())

    def test_cli_connect_starts_the_same_integrations_endpoint_as_web(self):
        with mock.patch.object(
                nx_channels,
                "_bos_post",
                return_value={
                    "ok": True,
                    "kind": "redirect",
                    "redirectUrl": "https://api.nexplora.ai/api/oauth/initiate/linkedin",
                }) as post:
            url, error = nx_channels._oauth_vault_connect_url("linkedin")
        self.assertIsNone(error)
        self.assertIn("/api/oauth/initiate/linkedin", url)
        post.assert_called_once_with(
            "/api/integrations/connect",
            {"providerSlug": "linkedin"},
        )

    def test_generic_setup_service_never_prompts_or_writes_a_second_social_vault(self):
        prompts = []
        with mock.patch.object(nx_channels, "_security") as security:
            result = nx_channels.setup_service(
                "x",
                auth="oauth",
                prompt_secret=lambda label: prompts.append(label) or "must-not-be-used",
            )
        self.assertTrue(result["ok"])
        self.assertEqual(result["mode"], "shared_oauth")
        self.assertEqual(result["provider"], "x")
        self.assertEqual(result["hint"], "/publish connect x")
        self.assertEqual(prompts, [])
        security.assert_not_called()

    def test_shared_vault_tools_never_fall_back_to_a_local_token(self):
        with mock.patch.object(
                nx_channels.XChannel,
                "is_connected",
                return_value=True):
            with mock.patch.object(nx_channel_tools, "_call_local") as local:
                result = nx_channel_tools.call("x", "x_get_me", {})
        self.assertFalse(result["ok"])
        self.assertEqual(result["detail"], "server_execution_not_available")
        local.assert_not_called()


class CommandDispatchTests(unittest.TestCase):
    def setUp(self):
        self.kc = FakeKeychain()
        mock.patch.object(nx_channels, "_security", self.kc).start()
        self.addCleanup(mock.patch.stopall)

    def test_status_lists_meta_as_nexplora_managed(self):
        out = nx_channels.handle_command(["status"])
        self.assertIn("Meta", out)
        self.assertIn("configured", out)

    def test_setup_on_unified_social_channel_never_creates_a_second_keychain_vault(self):
        out = nx_channels.handle_command(["setup", "linkedin"])
        self.assertIn("nothing to register", out)
        self.assertEqual(self.kc.store, {})

    def test_setup_on_bos_bridged_channel_explains_nothing_to_register(self):
        out = nx_channels.handle_command(["setup", "meta"])
        self.assertIn("nothing to register", out)
        self.assertIn("/publish connect meta", out)

    def test_disconnect_only_claims_removal_after_shared_vault_confirms_it(self):
        with mock.patch.object(nx_channels.XChannel, "disconnect", return_value=False):
            out = nx_channels.handle_command(["disconnect", "x"])
        self.assertIn("could not be disconnected", out)
        self.assertIn("Nothing was reported as removed", out)
        self.assertNotIn("token removed", out)

    def test_unknown_channel_is_honest(self):
        # tiktok/pinterest are now built-in channels — use a name that truly isn't one.
        out = nx_channels.handle_command(["connect", "myspace"])
        self.assertIn("Unknown channel", out)

    def test_connect_refuses_when_not_configured(self):
        with mock.patch.object(
                nx_channels,
                "_oauth_vault_connect_url",
                return_value=(None, "not_signed_in")):
            out = nx_channels.handle_command(["connect", "linkedin"])
        self.assertIn("Run /login first", out)


class NewConnectorTests(unittest.TestCase):
    def setUp(self):
        self.kc = FakeKeychain()
        mock.patch.object(nx_channels, "_security", self.kc).start()
        self.addCleanup(mock.patch.stopall)

    def test_all_connectors_registered(self):
        for n in ("meta", "google", "x", "linkedin"):
            with self.subTest(n=n):
                self.assertIsNotNone(nx_channels.get_channel(n))

    def test_connectors_fail_closed_unconfigured(self):
        # X is intentionally pre-configured via Nexplora's shared PUBLIC client_id
        # (one-click, PKCE no-secret), so it is NOT unconfigured-by-default. Google
        # is bos-bridged (always "configured" — Nexplora's own app — see
        # BosBridgedChannelTests) — test the per-operator-app connector that
        # genuinely fails closed without creds.
        for n in ("x", "linkedin"):
            with self.subTest(n=n):
                ch = nx_channels.get_channel(n)
                self.assertTrue(ch.is_configured())
                self.assertFalse(ch.is_connected())

    def test_x_connect_is_server_managed_not_a_local_pkce_token(self):
        x = nx_channels.get_channel("x")
        self.assertIsInstance(x, nx_channels._NexploraOAuthBridgedChannel)
        self.assertIsNone(x.redirect_uri)

    def _x_connected(self):
        return mock.patch.object(
            nx_channels,
            "_oauth_vault_connection",
            return_value={"providerSlug": "x", "status": "connected"})

    def test_x_publish_goes_through_the_server_and_returns_the_post_id(self):
        # This used to assert the OPPOSITE — that publishing refused with
        # server_execution_not_available. That refusal was honest while the grant
        # carried read scopes only and nothing server-side mapped a name onto the
        # tweet_create tool. Both are fixed, so refusing is now the wrong answer.
        x = nx_channels.get_channel("x")
        with self._x_connected():
            with mock.patch.object(
                    nx_channels, "_social_dispatch",
                    return_value={"ok": True, "result": {"tweet": {"id": "1799"}}}) as disp:
                out = x.publish_text("hello world")
        self.assertTrue(out["ok"])
        self.assertEqual(out["id"], "1799")
        self.assertIn("1799", out["url"])
        # The token must never come near this machine: the CLI holds no X token by
        # design, so the send has to go through the server with the operator's grant.
        disp.assert_called_once_with("x_post", {"text": "hello world"})

    def test_x_publish_reports_a_server_failure_rather_than_claiming_success(self):
        x = nx_channels.get_channel("x")
        with self._x_connected():
            with mock.patch.object(
                    nx_channels, "_social_dispatch",
                    return_value={"ok": False, "error": "byok_required_but_missing"}):
                out = x.publish_text("hello world")
        self.assertFalse(out["ok"])

    def test_x_publish_refuses_to_claim_success_without_a_post_id(self):
        # A 200 with no id is not a send we can vouch for. Reporting ok here would
        # be this CLI's version of the false green just removed from the web.
        x = nx_channels.get_channel("x")
        with self._x_connected():
            with mock.patch.object(
                    nx_channels, "_social_dispatch",
                    return_value={"ok": True, "result": {}}):
                out = x.publish_text("hello world")
        self.assertFalse(out["ok"])
        self.assertEqual(out["detail"], "unconfirmed")

    def test_x_publish_still_fails_closed_when_not_connected(self):
        x = nx_channels.get_channel("x")
        with mock.patch.object(nx_channels, "_oauth_vault_connection", return_value=None):
            with mock.patch.object(nx_channels, "_social_dispatch") as disp:
                out = x.publish_text("hello world")
        self.assertFalse(out["ok"])
        self.assertEqual(out["detail"], "not_connected")
        # Preflight must run BEFORE the network call, or an unconnected operator
        # gets a server round-trip and a worse error than the one we already had.
        disp.assert_not_called()

    def test_x_publish_refuses_empty_text_without_calling_the_server(self):
        x = nx_channels.get_channel("x")
        with self._x_connected():
            with mock.patch.object(nx_channels, "_social_dispatch") as disp:
                out = x.publish_text("   ")
        self.assertFalse(out["ok"])
        self.assertEqual(out["detail"], "empty_message")
        disp.assert_not_called()

    def test_linkedin_publish_fails_closed_without_provider_approval_and_proxy(self):
        li = nx_channels.get_channel("linkedin")
        self.assertFalse(li.can_publish)
        with mock.patch.object(
                nx_channels,
                "_oauth_vault_connection",
                return_value={"providerSlug": "linkedin", "status": "connected"}):
            out = li.publish_text("Launch day.")
        self.assertFalse(out["ok"])
        self.assertEqual(out["detail"], "server_execution_not_available")

    def test_publish_capable_channels_flagged_honestly(self):
        # The flag is a CLAIM to the operator, so it moves only when the route does.
        # X moved to True when publish_text started reaching social.x.tweet_create
        # through /api/worlds/social/dispatch.
        self.assertTrue(nx_channels.get_channel("meta").can_publish)
        self.assertTrue(nx_channels.get_channel("x").can_publish)
        # LinkedIn stays False for a reason that is not ours: posting needs
        # w_organization_social via the Community Management API programme, and the
        # write tool also needs an author URN a channel has no field for.
        self.assertFalse(nx_channels.get_channel("linkedin").can_publish)
        self.assertFalse(nx_channels.get_channel("google").can_publish)
        self.assertFalse(nx_channels.get_channel("snapchat").can_publish)

    def test_x_scopes_include_write_so_the_listed_grant_matches_the_real_one(self):
        # An operator reads this list. It said read-only long after connects began
        # requesting tweet.write, which is a wrong claim even though a bridged
        # channel's real scope set is composed server-side.
        self.assertIn("tweet.write", nx_channels.get_channel("x").scopes)
        self.assertIn("offline.access", nx_channels.get_channel("x").scopes)


class OAuthEndpointSanityTests(unittest.TestCase):
    def test_no_placeholder_or_dead_endpoints_loaded(self):
        # Real-audit guard: no shipped OAuth endpoint may be a placeholder
        # (<YOUR_OKTA_DOMAIN>, {subdomain}.zendesk.com) or a confirmed-dead host —
        # those would open a dead browser tab (the google-workspace.com class).
        import re as _re
        import urllib.parse as _up
        bad = []
        for name, spec in nx_channels.OAUTH_ENDPOINTS.items():
            a = spec.get("authorize", "")
            t = spec.get("token", "")
            if _re.search(r"[<{]|YOUR_", a + t):
                bad.append(f"{name}: placeholder")
            elif _up.urlparse(a).netloc.lower() in nx_channels._EP_DEAD_HOSTS:
                bad.append(f"{name}: dead host")
            elif not a.startswith("https://"):
                bad.append(f"{name}: non-https authorize")
        self.assertEqual(bad, [], f"unusable OAuth endpoint(s) shipped: {bad}")


class TenantOAuthTests(unittest.TestCase):
    """Per-account providers (Zendesk/Okta/Gorgias/Snowflake): the operator's
    subdomain/domain is substituted into a real login URL — never a placeholder."""

    def setUp(self):
        self.kc = FakeKeychain()
        self._patch = mock.patch.object(nx_channels, "_security", self.kc)
        self._patch.start()
        self.addCleanup(self._patch.stop)

    def test_each_tenant_service_resolves_to_tenant_connector(self):
        for name in ("Zendesk", "Okta", "Gorgias", "Snowflake", "zendesk", "snowflake"):
            with self.subTest(name=name):
                ch = nx_channels.connector_for_service(name, "oauth")
                self.assertIsInstance(ch, nx_channels.TenantOAuthConnector)

    def test_substitution_produces_real_host_no_placeholder(self):
        expect = {
            "Zendesk": ("acme", "acme.zendesk.com"),
            "Gorgias": ("support", "support.gorgias.com"),
            "Okta": ("acme.okta.com", "acme.okta.com"),
            "Snowflake": ("ab123.us-east-2.aws", "ab123.us-east-2.aws.snowflakecomputing.com"),
        }
        from urllib.parse import urlparse
        for name, (tenant, host) in expect.items():
            with self.subTest(name=name):
                ch = nx_channels.connector_for_service(name, "oauth")
                ch.set_tenant(tenant)
                ch.setup("CID", "SEC")
                url = ch.auth_url("st")
                self.assertNotIn("{tenant}", url, f"{name}: placeholder leaked into login URL")
                self.assertEqual(urlparse(url).netloc, host)
                self.assertEqual(urlparse(ch._token).netloc, host)

    def test_pasting_full_host_or_url_is_normalized(self):
        ch = nx_channels.connector_for_service("Zendesk", "oauth")
        ch.set_tenant("https://acme.zendesk.com/agent")  # operator pastes the whole thing
        ch.setup("CID", "SEC")
        from urllib.parse import urlparse
        self.assertEqual(urlparse(ch.auth_url("s")).netloc, "acme.zendesk.com")

    def test_not_configured_until_tenant_AND_creds(self):
        ch = nx_channels.connector_for_service("Okta", "oauth")
        self.assertFalse(ch.is_configured())
        ch.setup("CID", "SEC")
        self.assertFalse(ch.is_configured(), "creds without tenant must NOT be configured")
        ch.set_tenant("acme.okta.com")
        self.assertTrue(ch.is_configured())

    def test_setup_service_prompts_tenant_then_creds(self):
        answers = iter(["acme", "CID", "SEC"])  # tenant (visible), then 2 secrets
        res = nx_channels.setup_service(
            "Zendesk", auth="oauth",
            prompt_secret=lambda l: next(answers),
            prompt_value=lambda l: next(answers))
        self.assertTrue(res["ok"])
        self.assertEqual(res["tenant"], "acme")
        ch = nx_channels.connector_for_service("Zendesk", "oauth")
        self.assertIn("acme.zendesk.com", ch.auth_url("s"))

    def test_tenant_services_absent_from_static_table(self):
        # They must NOT also live in OAUTH_ENDPOINTS (that would shadow the
        # tenant connector with a placeholder entry).
        for name in ("Okta", "Zendesk", "Gorgias", "Snowflake"):
            self.assertNotIn(name, nx_channels.OAUTH_ENDPOINTS,
                             f"{name} should be tenant-only, not in the static table")


class NoSecretsInSourceTests(unittest.TestCase):
    def test_source_has_no_hardcoded_secrets_or_tokens(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "nx_channels.py")
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        # No Meta user-token prefix, no obvious app-secret assignment literals.
        self.assertNotIn("EAA", src, "looks like a hardcoded Meta access token")
        import re as _re
        self.assertIsNone(_re.search(r'app_secret\s*=\s*["\'][A-Za-z0-9]{16,}["\']', src),
                          "hardcoded app secret literal")
        self.assertIsNone(_re.search(r'access_token\s*=\s*["\'][A-Za-z0-9]{16,}["\']', src),
                          "hardcoded access token literal")


if __name__ == "__main__":
    unittest.main()
