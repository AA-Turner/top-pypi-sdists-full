"""Connect-routing tests: every provider must land on its CORRECT connect path.
Founder directive (2026-07-21): NEVER lazy-byok an OAuth-native provider — fix the MCP or route to backend OAuth.
Genuine api-key connectors get the new inline CLI key-paste; OAuth-native ones sit in _OAUTH_PENDING (coming soon)
until their Nexplora OAuth app lands; gitlab/workable are live MCP again."""
import sys, os, re, importlib
_HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(_HERE))  # nx/cli
m = importlib.import_module("nx_mcp_oauth")
nx = importlib.import_module("nx_cli")  # must import cleanly (no NameError in the new helper/sets)

fails = []
def check(name, cond):
    print(("PASS" if cond else "FAIL"), name)
    if not cond: fails.append(name)

# ── the inline byok key-paste helper exists (replaces the "add it in the web app" punt) ──
check("_connect_byok_key is callable", callable(getattr(nx, "_connect_byok_key", None)))
check("_BYOK_KEY_SOURCE has key hints", isinstance(getattr(nx, "_BYOK_KEY_SOURCE", None), dict) and len(nx._BYOK_KEY_SOURCE) >= 15)
check("split has a key-source hint", "split" in nx._BYOK_KEY_SOURCE)

# ── GitLab cloud MCP exists but is NOT the default NX connect path ──
# Victor's real account finishes OAuth, then GitLab's MCP initialize returns
# HTTP 404. GitLab documents that as MCP server access/prereqs disabled, so NX
# must route /integrations gitlab to the working REST/PAT connector instead of
# saving a remote-MCP connection that cannot initialize.
check("gitlab URL kept in REMOTE_MCP for explicit re-probe", "gitlab" in m.REMOTE_MCP)
check("gitlab marked MCP_BROKEN so normal connect skips remote MCP", "gitlab" in m.MCP_BROKEN)
check("gitlab is NOT remote MCP for default /integrations routing", not m.is_remote_mcp("gitlab"))
check("gitlab NOT in MCP_COMING_SOON", "gitlab" not in m.MCP_COMING_SOON)
check("gitlab has a terminal REST token hint", "gitlab" in nx._BYOK_KEY_SOURCE)
check("gitlab has backend REST-token fallback", "gitlab" in getattr(nx, "_REST_TOKEN_FALLBACK", frozenset()))

# Workable remains a live MCP one-click DCR path.
check("workable in REMOTE_MCP", "workable" in m.REMOTE_MCP)
check("workable NOT in MCP_BROKEN", "workable" not in m.MCP_BROKEN)
check("workable NOT in MCP_COMING_SOON", "workable" not in m.MCP_COMING_SOON)

# ── OAuth-native (incl. the MCP-broken ones) route to OAuth, NEVER byok — and SELF-HEAL on provision ──
_src = open(nx.__file__).read()
_NXOAUTH = set(re.findall(r'\(\s*"([a-z0-9_]+)"',
              (lambda s: s[s.index('_NX_OAUTH = {'):].split("\n                        }")[0])(_src)))
for s in ("okta", "intercom", "datadog", "auth0", "lever",
          "mailchimp", "typeform", "hootsuite", "buffer", "digitalocean",
          "salesforce"):
    check(f"{s} in _NX_OAUTH (routes to backend OAuth)", s in _NXOAUTH)
    # NOT early-parked → the pick ATTEMPTS OAuth and self-heals the moment the app is provisioned
    check(f"{s} NOT in MCP_COMING_SOON (self-healing, not early-parked)", s not in m.MCP_COMING_SOON)

# ── PAT/token-native connectors (no global OAuth app — user provides own token) ──
for s in ("opsgenie", "databricks", "servicenow"):
    check(f"{s} in _BYOK_KEY_SOURCE (PAT/token path, not OAuth)", s in nx._BYOK_KEY_SOURCE)
    check(f"{s} NOT in _NX_OAUTH (never lazy-OAuth a PAT-native provider)", s not in _NXOAUTH)
# the byok branch is STRUCTURALLY guarded so an _NX_OAUTH provider can never fall to key-paste
check("byok branch guarded by `not in _nxoauth_by_slug`", 'chosen not in _nxoauth_by_slug' in _src)
# only genuine app-provisioned-but-rejected connectors stay in the early gate
check("MCP_COMING_SOON is now just the early-reject case (zoho_desk)", m.MCP_COMING_SOON == frozenset({"zoho_desk"}))

# ── genuine api-key connectors fall to inline key-paste (NOT coming-soon, NOT _NX_OAUTH) ──
for s in ("split", "clerk", "greenhouse", "height", "segment"):
    check(f"{s} NOT in MCP_COMING_SOON (falls to inline key-paste)", s not in m.MCP_COMING_SOON)
    check(f"{s} NOT in _NX_OAUTH", s not in _NXOAUTH)

# ── entitlement-gated MCPs stay honest api-key (real path), NOT forced OAuth ──
for s in ("mixpanel", "newrelic"):
    check(f"{s} stays MCP_BROKEN", s in m.MCP_BROKEN)
    check(f"{s} NOT in _NX_OAUTH", s not in _NXOAUTH)

# ── OAuth-capable connectors that were pinned to token: OAuth-first WITH a token fallback (never a dead end) ──
def _tokpath(s): return s in getattr(m, "_MCP_TOKEN", set()) or s in getattr(m, "_FORCE_TOKEN", set())
for s in ("xero", "docusign", "hubspot", "freshdesk", "rippling", "front", "smartsheet", "bitbucket"):
    check(f"{s} in _NX_OAUTH (backend OAuth first)", s in _NXOAUTH)
    check(f"{s} keeps a token fallback (works until the app is provisioned)", _tokpath(s))
check("_has_token_path helper exists", callable(getattr(nx, "_has_token_path", None)))
check("token-fallback branch wired in the connect dispatch", "_has_token_path(chosen)" in _src)
# github keeps its own device-flow path, NOT moved into _NX_OAUTH
check("github NOT in _NX_OAUTH (device-flow preserved)", "github" not in _NXOAUTH)

# ── the working DCR set is untouched ──
for s in ("notion", "pipedrive", "sentry", "zendesk", "vanta", "launchdarkly"):
    check(f"{s} still one-click DCR (in REMOTE_MCP, not broken)", s in m.REMOTE_MCP and s not in m.MCP_BROKEN)

# ── zoom unchanged: backed by an OAuth app, not moved into pending ──
check("zoom NOT in _OAUTH_PENDING (has its app)", "zoom" not in m.MCP_COMING_SOON)

print("\nRESULT:", "ALL PASS" if not fails else ("FAILURES: " + ", ".join(fails)))

# Discover-compatible wrapper — same shape as tests/test_integration_write_honesty.py.
# The checks above run AT IMPORT. A bare module-level sys.exit() raises SystemExit during
# pytest's import of this module, which pytest reports as an INTERNALERROR and which aborts
# collection for the WHOLE directory — so this file passing was silently costing us every
# other test in the suite. `python test_connect_routing.py` behaves exactly as before.
import unittest  # noqa: E402


class ConnectRoutingChecks(unittest.TestCase):
    def test_all_connect_routing_checks_pass(self):
        self.assertEqual(fails, [], f"failing checks: {fails}")


if __name__ == "__main__":
    sys.exit(1 if fails else 0)
