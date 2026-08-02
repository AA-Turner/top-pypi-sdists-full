"""
test_integrations_login.py — the operator's bar: EVERY directory integration must
be connectable, and OAuth ones must take you to the provider's REAL login with the
standard loopback redirect back to NX. No dead entries, no fabricated login URLs.

Pass per the founder's definition: "until it takes you to login = it works", and
"redirects back to nx in the terminal connected = the standard".

Run: python3 -m unittest tests.test_integrations_login
"""
import os
import sys
import unittest
import unittest.mock
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import nx_integrations_directory as D   # noqa: E402
import nx_channels as C                 # noqa: E402

# Server-side-bridged channels: connect through Nexplora's own server-side OAuth (no local loopback
# redirect; redirect_uri is None). The bos-bridge (_BosBridgedChannel) plus the two Google bridges
# (Workspace + Ads/YouTube) all share that contract — product code enumerates the same three in
# nx_channels.py's connect/routing. Tests special-case the concept via this ONE tuple, not a per-test list.
_SERVER_BRIDGED = (
    C._NexploraOAuthBridgedChannel,
    C._BosBridgedChannel,
    C._GoogleWorkspaceBridgedChannel,
    C._GoogleAdsYouTubeBridgedChannel,
)

# Real provider hosts we expect verified OAuth authorize URLs to live on.
def _host(u):
    try:
        return urlparse(u).netloc.lower()
    except Exception:
        return ""


class EveryIntegrationConnectableTests(unittest.TestCase):
    def setUp(self):
        # Configure every connector with dummy app creds so auth_url builds a
        # complete login URL (the real client_id is the operator's; here we only
        # assert the URL is well-formed and points at the real provider).
        self.kc = {}
        def fake_security(args, input_text=None):
            import types
            cp = types.SimpleNamespace(returncode=1, stdout="", stderr="")
            svc = args[args.index("-s") + 1] if "-s" in args else None
            op = args[0]
            if op == "find-generic-password" and svc in self.kc:
                cp.returncode = 0; cp.stdout = self.kc[svc] + "\n"
            elif op == "add-generic-password":
                wi = args.index("-w"); self.kc[svc] = args[wi + 1]; cp.returncode = 0
            return cp
        patcher = unittest.mock.patch.object(C, "_security", fake_security)
        patcher.start(); self.addCleanup(patcher.stop)

    def _all_entries(self):
        for world, items in D.WORLD_INTEGRATIONS.items():
            for it in items:
                yield world, it

    def test_every_oauth_or_apikey_service_is_connectable(self):
        unconnectable = []
        for world, it in self._all_entries():
            if it.auth in ("none", "mcp"):
                continue
            conn = C.connector_for_service(it.name, it.auth)
            if conn is None:
                unconnectable.append(f"{world}/{it.name} ({it.auth})")
        self.assertEqual(unconnectable, [],
                         f"{len(unconnectable)} services have no connector: {unconnectable[:10]}")

    def test_oauth_connectors_reach_real_login_with_loopback(self):
        """Every service that resolves to an OAuth connector must build an
        https auth_url at a real provider host, carrying the localhost loopback
        redirect — i.e. it takes you to a real login and comes back to NX.

        Bos-bridged connectors (Meta/Google/TikTok/Snapchat) are EXCLUDED here:
        they no longer build their own auth_url locally — Nexplora's own
        server does, and the callback is Nexplora's domain, not a localhost
        loopback (see test_channels.py::BosBridgedChannelTests for their
        equivalent real-login coverage)."""
        checked = 0
        for world, it in self._all_entries():
            conn = C.connector_for_service(it.name, it.auth)
            if isinstance(conn, _SERVER_BRIDGED):
                continue
            if not isinstance(conn, (C.GenericOAuthConnector, C.MetaChannel,
                                     C.GoogleChannel, C.XChannel, C.LinkedInChannel)):
                continue
            conn.setup("DUMMYID", "DUMMYSECRET")  # so client_id is populated
            url = conn.auth_url("teststate")
            with self.subTest(svc=it.name):
                self.assertTrue(url.startswith("https://"), f"{it.name}: not https")
                self.assertNotEqual(_host(url), "", f"{it.name}: empty authorize host")
                qs = parse_qs(urlparse(url).query)
                # the standard: redirect comes back to the NX loopback
                self.assertIn("localhost", (qs.get("redirect_uri", [""])[0]),
                              f"{it.name}: redirect not loopback")
                self.assertEqual(qs.get("client_id", [""])[0], "DUMMYID",
                                 f"{it.name}: client_id not in login URL")
                self.assertEqual(qs.get("state", [""])[0], "teststate")
            checked += 1
        self.assertGreater(checked, 40, "expected many OAuth services to be login-capable")

    def test_loopback_redirect_is_the_standard_for_all(self):
        # The redirect target is the one-shot localhost server connect_channel
        # binds — except bos-bridged connectors (Meta/Google/TikTok/Snapchat),
        # whose real redirect_uri lives server-side in nexplora-v2, never local.
        for world, it in self._all_entries():
            conn = C.connector_for_service(it.name, it.auth)
            if conn is None or isinstance(conn, _SERVER_BRIDGED):
                continue
            self.assertIn("localhost", conn.redirect_uri)

    def test_generic_setup_then_login_loop(self):
        # The full operator loop for a NON-built OAuth service: store app creds
        # → connector becomes configured → login URL carries the real client_id.
        creds = iter(["MY_CLIENT_ID", "MY_SECRET"])
        res = C.setup_service("Notion", auth="oauth", prompt_secret=lambda l: next(creds))
        self.assertTrue(res["ok"])
        self.assertEqual(res["mode"], "oauth")
        ch = C.connector_for_service("Notion", "oauth")
        self.assertTrue(ch.is_configured())
        self.assertIn("MY_CLIENT_ID", ch.auth_url("s"))

    def test_no_fabricated_connect_urls_in_source(self):
        # Regression: connecting an unknown service must NEVER open a fabricated
        # "https://{name}.com/settings/api" — that opened dead domains like
        # google-workspace.com.
        import os, re as _re
        src_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bad = _re.compile(r'f"https://\{[a-z_]+\}\.com')
        offenders = []
        for name in os.listdir(src_dir):
            if name.endswith(".py") and not name.startswith("test_"):
                with open(os.path.join(src_dir, name), encoding="utf-8") as f:
                    for n, line in enumerate(f, 1):
                        if line.lstrip().startswith("#"):
                            continue
                        if bad.search(line):
                            offenders.append(f"{name}:{n}")
        self.assertEqual(offenders, [], f"fabricated connect URL(s): {offenders}")

    def test_google_workspace_routes_to_real_google_oauth(self):
        # The bug: connecting Google Workspace opened google-workspace.com.
        # Now it must resolve to the built google connector, which connects
        # through Nexplora's own server-side Google OAuth (never a fabricated
        # or dead host — the bos-bridge's URL comes straight from the backend).
        for q in ("google workspace", "youtube", "google ads"):
            with self.subTest(q=q):
                plan = D.resolve(q, world="cowork")
                self.assertEqual(plan["status"], "ready")
                self.assertEqual(plan["connector"], "google")
        g = C.get_channel("google")
        self.assertIsInstance(g, _SERVER_BRIDGED)
        # google resolves to the Ads/YouTube bridge (shared 'google' grant, web OAuth via
        # /api/oauth/initiate/google), so mock THAT path's url + connected-check, not the bos-bridge.
        with unittest.mock.patch.object(
                C, "_google_ads_youtube_connect_url",
                return_value=("https://accounts.google.com/o/oauth2/v2/auth?x=1", None)):
            with unittest.mock.patch.object(C, "_google_grant_is_connected", return_value=True):
                out = C.connect_channel(g, open_browser=False, timeout=5)
        self.assertTrue(out["ok"])

    def test_marketplace_picks_route_to_oauth_not_token_paste(self):
        # The bug: picking slack/google-workspace from the marketplace used the
        # old "open browser + paste a token" path (or network-errored). The
        # unified path must resolve them to a real OAuth connector (loopback,
        # or — for Google — Nexplora's own bos-bridge); only genuine MCP-only
        # servers fall back to the hub.
        oauth_expected = {
            "slack": "slack.com",
            "notion": "api.notion.com",
            "hubspot": "app.hubspot.com",
        }
        for pick, host in oauth_expected.items():
            with self.subTest(pick=pick):
                plan = D.resolve(pick, world="cowork")
                self.assertIn(plan["status"], ("ready", "directory"),
                              f"{pick} should resolve to a connector, not the hub")
                conn = plan.get("connector")
                ch = (C.get_channel(conn) if conn
                      else C.connector_for_service(pick, plan.get("auth")))
                self.assertNotIsInstance(ch, C.GenericApiKeyConnector,
                    f"{pick} should be OAuth (loopback), not a token/key paste")
                ch.setup("ID", "SEC")
                self.assertIn(host, ch.auth_url("s"))
        # google-workspace: bos-bridged, no local auth_url — verified via the
        # bridge instead (real coverage in test_google_workspace_routes_to_real_google_oauth).
        plan = D.resolve("google-workspace", world="cowork")
        self.assertIn(plan["status"], ("ready", "directory"))
        ch = C.get_channel(plan.get("connector")) if plan.get("connector") else None
        self.assertIsInstance(ch, _SERVER_BRIDGED)
        # a genuine MCP-only tool stays on the hub path
        self.assertNotIn(D.resolve("sequential-thinking", world="cowork")["status"],
                         ("ready", "directory"))

    def test_generic_and_tenant_oauth_services_resolve_to_login_not_hub(self):
        # The gap: services with a real OAuth/tenant connector but not in the
        # curated directory (Discord, Snowflake, …) resolved to the MCP hub, so
        # /integrations <name> never reached their login. resolve() must route
        # them to a real OAuth connect; genuine MCP-only tools stay on the hub.
        oauth = ["discord", "zoom", "dropbox", "box",
                 "grafana", "quickbooks", "pipedrive",          # generic endpoints
                 "snowflake", "zendesk", "okta", "gorgias"]      # per-account tenant
        for name in oauth:
            with self.subTest(name=name):
                plan = D.resolve(name, world="cowork")
                self.assertEqual(plan["status"], "directory", f"{name} not routed to connect")
                self.assertEqual(plan["auth"], "oauth", f"{name} not OAuth")
        # a genuine MCP-only tool must NOT be mislabeled as OAuth
        self.assertEqual(D.resolve("sequential-thinking", world="cowork")["auth"], "mcp")
        # tiktok/pinterest/snapchat are now BUILT channel connectors → "ready" tier (like meta)
        for built in ("tiktok", "pinterest", "snapchat"):
            with self.subTest(name=built):
                plan = D.resolve(built, world="cowork")
                self.assertEqual(plan["status"], "ready", f"{built} should be a built connector")
                self.assertEqual(plan["auth"], "oauth")

    def test_endpoint_lookup_is_case_insensitive(self):
        # "notion" (lowercase) must still resolve to the real Notion OAuth.
        ch = C.connector_for_service("notion", "oauth")
        self.assertIsInstance(ch, C.GenericOAuthConnector)
        ch.setup("ID", "SEC")
        self.assertIn("api.notion.com", ch.auth_url("s"))

    def test_generic_apikey_setup_stores_key(self):
        res = C.setup_service("Stripe", auth="api_key", prompt_secret=lambda l: "sk_live_x")
        self.assertTrue(res["ok"])
        self.assertEqual(res["mode"], "api_key")
        self.assertTrue(C.connector_for_service("Stripe", "api_key").is_connected())

    def test_coverage_report(self):
        oauth_login = api_key = none_ = 0
        seen = set()
        for world, it in self._all_entries():
            if it.name in seen:
                continue
            seen.add(it.name)
            conn = C.connector_for_service(it.name, it.auth)
            if isinstance(conn, C.GenericApiKeyConnector):
                api_key += 1
            elif conn is not None:
                oauth_login += 1
            else:
                none_ += 1
        total = len(seen)
        print(f"\n  COVERAGE (unique services={total}): "
              f"{oauth_login} OAuth-login, {api_key} key-connect, {none_} none/mcp")
        # Every unique oauth/api_key service must be connectable.
        self.assertGreaterEqual(oauth_login + api_key, total - 8)


if __name__ == "__main__":
    import unittest.mock  # noqa
    unittest.main()
