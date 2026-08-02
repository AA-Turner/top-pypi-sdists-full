#!/usr/bin/env python3
"""Convert an OpenAPI spec to a Postman collection with environment variable post-processing.

Usage:
    pysae-ai-tools openapi_to_postman.convert <spec> [options]

Examples:
    pysae-ai-tools openapi_to_postman.convert openapi.yaml
    pysae-ai-tools openapi_to_postman.convert https://api.pysae.com/api/docs/v4/internal/openapi.json
    pysae-ai-tools openapi_to_postman.convert spec.json --output my-collection.json --env-name "My API"
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any

import httpx
import typer

from ..common.winpath import spawnable

# ---------------------------------------------------------------------------
# Postman API key resolution
# ---------------------------------------------------------------------------

POSTMAN_API_URL = "https://api.getpostman.com"

# Spec downloads and Postman API calls have no upload/download progress to gate
# on, so a single generous timeout keeps a hung endpoint from blocking forever.
HTTP_TIMEOUT = 30.0


def resolve_postman_api_key() -> str | None:
    """Resolve Postman API key from env var or Claude MCP config (~/.claude.json)."""
    key = os.environ.get("POSTMAN_API_KEY")
    if key:
        return key
    claude_json = Path.home() / ".claude.json"
    if claude_json.exists():
        try:
            cfg = json.loads(claude_json.read_text(encoding="utf-8"))
            raw_key = cfg.get("mcpServers", {}).get("postman", {}).get("env", {}).get("POSTMAN_API_KEY")
            if isinstance(raw_key, str) and raw_key:
                return raw_key
        except (json.JSONDecodeError, KeyError):
            pass
    return None


# ---------------------------------------------------------------------------
# Step 1: Ensure CLI is installed
# ---------------------------------------------------------------------------


def ensure_cli() -> str:
    """Check that openapi2postmanv2 is installed, install if missing. Returns the path."""
    path = shutil.which("openapi2postmanv2")
    if path:
        return path
    print("Installing openapi-to-postmanv2...", file=sys.stderr)
    # ``npm`` is a ``.cmd`` shim on Windows — see ``spawnable``.
    subprocess.run([spawnable("npm"), "i", "-g", "openapi-to-postmanv2"], check=True)
    path = shutil.which("openapi2postmanv2")
    if not path:
        print("ERROR: openapi2postmanv2 not found after install", file=sys.stderr)
        sys.exit(1)
    return path


# ---------------------------------------------------------------------------
# Step 2: Fetch spec if URL
# ---------------------------------------------------------------------------


def resolve_spec(spec: str) -> str:
    """If spec is a URL, download to a temp file. Returns local file path."""
    if spec.startswith("http://") or spec.startswith("https://"):
        print(f"Downloading spec from {spec}...", file=sys.stderr)
        resp = httpx.get(spec, timeout=HTTP_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
        tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        tmp.write(resp.content)
        tmp.close()
        return tmp.name
    if not os.path.exists(spec):
        print(f"ERROR: spec file not found: {spec}", file=sys.stderr)
        sys.exit(1)
    return spec


# ---------------------------------------------------------------------------
# Step 3: Convert
# ---------------------------------------------------------------------------


def convert(cli_path: str, spec_path: str, output_path: str) -> None:
    """Run openapi2postmanv2 CLI."""
    cmd = [
        cli_path,
        "-s",
        spec_path,
        "-o",
        output_path,
        "-p",
        "-O",
        "folderStrategy=Paths,requestNameSource=Fallback,schemaFaker=true,enableOptionalParameters=false",
    ]
    print(f"Converting: {' '.join(cmd)}", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: conversion failed\n{result.stderr}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(output_path):
        print("ERROR: output file not created", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Step 4: Parse spec metadata (base URL + security schemes)
# ---------------------------------------------------------------------------


@dataclass
class AuthScheme:
    """A detected authentication scheme from the OpenAPI spec."""

    name: str
    type: str  # "bearer", "apikey-header", "apikey-query", "apikey-cookie", "basic", "openidconnect"
    header_or_param_name: str  # e.g. "Authorization", "X-Api-Key", "session_id"
    description: str


@dataclass
class SpecMetadata:
    """Metadata extracted from an OpenAPI spec."""

    base_url: str | None
    auth_schemes: list[AuthScheme]


def _parse_spec(spec_path: str) -> dict[str, Any] | None:
    """Parse an OpenAPI spec file (JSON or YAML)."""
    try:
        with open(spec_path) as f:
            content = f.read()
        try:
            parsed: dict[str, Any] = json.loads(content)
            return parsed
        except json.JSONDecodeError:
            try:
                import yaml

                result: dict[str, Any] = yaml.safe_load(content)
                return result
            except ImportError:
                return None
    except Exception:
        return None


def _extract_base_url(spec: dict[str, Any]) -> str | None:
    """Extract the first server URL from a parsed spec."""
    servers = spec.get("servers", [])
    if servers:
        return str(servers[0].get("url", ""))
    host = spec.get("host", "")
    if host:
        scheme = (spec.get("schemes") or ["https"])[0]
        base_path = spec.get("basePath", "")
        return f"{scheme}://{host}{base_path}"
    return None


def _extract_auth_schemes(spec: dict[str, Any]) -> list[AuthScheme]:
    """Extract security schemes from a parsed OpenAPI spec."""
    schemes: list[AuthScheme] = []
    security_schemes = spec.get("components", {}).get("securitySchemes", {})
    # Swagger 2.0 fallback
    if not security_schemes:
        security_schemes = spec.get("securityDefinitions", {})

    for name, defn in security_schemes.items():
        scheme_type = defn.get("type", "")
        description = defn.get("description", "")

        if scheme_type == "http":
            http_scheme = defn.get("scheme", "").lower()
            if http_scheme == "bearer":
                schemes.append(AuthScheme(name, "bearer", "Authorization", description))
            elif http_scheme == "basic":
                schemes.append(AuthScheme(name, "basic", "Authorization", description))

        elif scheme_type == "apiKey":
            location = defn.get("in", "header")
            param_name = defn.get("name", name)
            if location == "header":
                schemes.append(AuthScheme(name, "apikey-header", param_name, description))
            elif location == "query":
                schemes.append(AuthScheme(name, "apikey-query", param_name, description))
            elif location == "cookie":
                schemes.append(AuthScheme(name, "apikey-cookie", param_name, description))

        elif scheme_type == "openIdConnect":
            oidc_url = defn.get("openIdConnectUrl", "")
            schemes.append(AuthScheme(name, "openidconnect", oidc_url, description))

        elif scheme_type == "oauth2":
            # Extract token URL from flows if available
            flows = defn.get("flows", {})
            token_url = ""
            for flow in flows.values():
                if isinstance(flow, dict) and "tokenUrl" in flow:
                    token_url = flow["tokenUrl"]
                    break
            schemes.append(AuthScheme(name, "oauth2", token_url, description))

    return schemes


def _fetch_oidc_config(oidc_url: str) -> dict[str, Any] | None:
    """Fetch OpenID Connect discovery document."""
    try:
        print(f"  Fetching OIDC config from {oidc_url}...", file=sys.stderr)
        resp = httpx.get(oidc_url, timeout=10.0, follow_redirects=True)
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result
    except Exception as e:
        print(f"  WARNING: failed to fetch OIDC config: {e}", file=sys.stderr)
        return None


def extract_spec_metadata(spec_path: str) -> SpecMetadata:
    """Extract base URL and auth schemes from an OpenAPI spec."""
    spec = _parse_spec(spec_path)
    if not spec:
        return SpecMetadata(base_url=None, auth_schemes=[])
    return SpecMetadata(base_url=_extract_base_url(spec), auth_schemes=_extract_auth_schemes(spec))


# ---------------------------------------------------------------------------
# Step 4b: Apply auth to Postman collection
# ---------------------------------------------------------------------------


def _prefixed(prefix: str, name: str) -> str:
    """Build a prefixed variable name."""
    return f"{prefix}_{name}" if prefix else name


def _oauth2_var_names(prefix: str) -> dict[str, str]:
    """Return the standard OAuth2 environment variable names."""
    return {
        "auth_url": _prefixed(prefix, "AUTH_URL"),
        "token_url": _prefixed(prefix, "AUTH_TOKEN_URL"),
        "client_id": _prefixed(prefix, "AUTH_CLIENT_ID"),
        "client_secret": _prefixed(prefix, "AUTH_CLIENT_SECRET"),
        "scope": _prefixed(prefix, "AUTH_SCOPE"),
        "callback_url": _prefixed(prefix, "AUTH_CALLBACK_URL"),
    }


def _build_oauth2_auth(prefix: str) -> tuple[dict[str, Any], list[str]]:
    """Build Postman OAuth2 auth object. Returns (auth_obj, list_of_var_names)."""
    names = _oauth2_var_names(prefix)

    # PKCE + client_authentication=body: the Auth0 app is a public (native) client
    # with no secret. Auth0 rejects the token exchange ("access_denied /
    # Unauthorized") for a plain authorization_code grant — it requires PKCE.
    auth_obj: dict[str, Any] = {
        "type": "oauth2",
        "oauth2": [
            {"key": "grant_type", "value": "authorization_code_with_pkce", "type": "string"},
            {"key": "authUrl", "value": "{{" + names["auth_url"] + "}}", "type": "string"},
            {"key": "accessTokenUrl", "value": "{{" + names["token_url"] + "}}", "type": "string"},
            {"key": "clientId", "value": "{{" + names["client_id"] + "}}", "type": "string"},
            {"key": "clientSecret", "value": "{{" + names["client_secret"] + "}}", "type": "string"},
            {"key": "scope", "value": "{{" + names["scope"] + "}}", "type": "string"},
            {"key": "redirect_uri", "value": "{{" + names["callback_url"] + "}}", "type": "string"},
            {"key": "challengeAlgorithm", "value": "S256", "type": "string"},
            {"key": "client_authentication", "value": "body", "type": "string"},
            {"key": "addTokenTo", "value": "header", "type": "string"},
            {"key": "tokenName", "value": "access_token", "type": "string"},
            {"key": "useBrowser", "value": False, "type": "boolean"},
        ],
    }

    return auth_obj, list(names.values())


def resolve_oauth2_env_vars(prefix: str, oidc_url: str) -> dict[str, str]:
    """Resolve OAuth2 environment variable defaults by fetching the OIDC discovery doc."""
    names = _oauth2_var_names(prefix)

    auth_url_default = ""
    token_url_default = ""
    scope_default = "openid profile"
    if oidc_url:
        oidc = _fetch_oidc_config(oidc_url)
        if oidc:
            auth_url_default = oidc.get("authorization_endpoint", "")
            token_url_default = oidc.get("token_endpoint", "")
            scopes = oidc.get("scopes_supported", [])
            if scopes:
                scope_default = " ".join(s for s in scopes if s in ("openid", "profile", "email", "offline_access"))

    return {
        names["auth_url"]: auth_url_default,
        names["token_url"]: token_url_default,
        names["client_id"]: "",
        names["client_secret"]: "",
        names["scope"]: scope_default,
        names["callback_url"]: "https://oauth.pstmn.io/v1/callback",
    }


def _build_bearer_auth(prefix: str) -> tuple[dict[str, Any], dict[str, str]]:
    """Build Postman Bearer auth. Returns (auth_obj, {var: ""})."""
    var = _prefixed(prefix, "AUTH_BEARER_TOKEN")
    auth_obj: dict[str, Any] = {
        "type": "bearer",
        "bearer": [{"key": "token", "value": "{{" + var + "}}", "type": "string"}],
    }
    return auth_obj, {var: ""}


def _build_apikey_auth(prefix: str, scheme: AuthScheme) -> tuple[dict[str, Any], dict[str, str]]:
    """Build Postman API Key auth. Returns (auth_obj, {var: ""})."""
    slug = scheme.name.upper().replace("-", "_").replace(" ", "_")
    var = _prefixed(prefix, f"AUTH_{slug}_KEY")
    location = "header" if scheme.type == "apikey-header" else "query"
    auth_obj: dict[str, Any] = {
        "type": "apikey",
        "apikey": [
            {"key": "key", "value": scheme.header_or_param_name, "type": "string"},
            {"key": "value", "value": "{{" + var + "}}", "type": "string"},
            {"key": "in", "value": location, "type": "string"},
        ],
    }
    return auth_obj, {var: ""}


def _build_basic_auth(prefix: str) -> tuple[dict[str, Any], dict[str, str]]:
    """Build Postman Basic auth. Returns (auth_obj, {var: ""})."""
    user_var = _prefixed(prefix, "AUTH_USERNAME")
    pwd_var = _prefixed(prefix, "AUTH_PASSWORD")
    auth_obj: dict[str, Any] = {
        "type": "basic",
        "basic": [
            {"key": "username", "value": "{{" + user_var + "}}", "type": "string"},
            {"key": "password", "value": "{{" + pwd_var + "}}", "type": "string"},
        ],
    }
    return auth_obj, {user_var: "", pwd_var: ""}


def _find_oidc_url(schemes: list[AuthScheme]) -> str:
    """Find the first OIDC discovery URL from auth schemes."""
    for s in schemes:
        if s.type == "openidconnect" and s.header_or_param_name:
            return s.header_or_param_name
    return ""


def apply_collection_auth(
    collection: dict[str, Any],
    schemes: list[AuthScheme],
    prefix: str,
    auth_type: str,
) -> tuple[str, dict[str, str]]:
    """Apply auth to a Postman collection and return {env_var: ""} (keys only, no defaults).

    For OAuth2, defaults are resolved per-environment via resolve_oauth2_env_vars().
    auth_type: "auto", "oauth2", "bearer", "apikey", "basic", "none".
    "auto" picks from spec schemes: bearer > apikey > oauth2.
    """
    if auth_type == "none":
        return "none", {}

    apikey_scheme: AuthScheme | None = None
    has_bearer = False
    has_oauth2 = False
    for s in schemes:
        if s.type.startswith("apikey") and not apikey_scheme:
            apikey_scheme = s
        if s.type == "bearer":
            has_bearer = True
        if s.type in ("openidconnect", "oauth2"):
            has_oauth2 = True

    # Resolve "auto": bearer > apikey > oauth2
    if auth_type == "auto":
        if has_bearer:
            auth_type = "bearer"
        elif apikey_scheme:
            auth_type = "apikey"
        elif has_oauth2:
            auth_type = "oauth2"
        else:
            print("  Auth: no supported scheme found in spec, skipping", file=sys.stderr)
            return "none", {}

    auth_obj: dict[str, Any]
    auth_vars: dict[str, str]

    if auth_type == "oauth2":
        auth_obj, var_names = _build_oauth2_auth(prefix)
        auth_vars = dict.fromkeys(var_names, "")
        label = "OAuth2 (authorization_code)"
    elif auth_type == "bearer":
        auth_obj, auth_vars = _build_bearer_auth(prefix)
        label = "Bearer Token"
    elif auth_type == "apikey":
        if not apikey_scheme:
            apikey_scheme = AuthScheme("Api-Key", "apikey-header", "x-api-key", "")
        auth_obj, auth_vars = _build_apikey_auth(prefix, apikey_scheme)
        label = f"API Key ({apikey_scheme.header_or_param_name})"
    elif auth_type == "basic":
        auth_obj, auth_vars = _build_basic_auth(prefix)
        label = "Basic Auth"
    else:
        print(f"  WARNING: unknown auth type '{auth_type}', skipping auth", file=sys.stderr)
        return "none", {}

    collection["auth"] = auth_obj
    var_list = ", ".join(f"{{{{{v}}}}}" for v in auth_vars)
    print(f"  Auth: {label} -> {var_list}", file=sys.stderr)
    return auth_type, auth_vars


# ---------------------------------------------------------------------------
# Step 4c: Strip per-request auth so requests inherit from collection
# ---------------------------------------------------------------------------


def strip_request_auth(items: list[dict[str, Any]]) -> int:
    """Remove per-request auth from all requests so they inherit collection-level auth.

    Returns the number of requests stripped.
    """
    count = 0
    for item in items:
        if "item" in item:
            count += strip_request_auth(item["item"])
        req = item.get("request")
        if req and "auth" in req:
            del req["auth"]
            count += 1
    return count


# ---------------------------------------------------------------------------
# Step 4d: Cascading auth pre-request script (API key > login > OAuth2)
# ---------------------------------------------------------------------------

_AUTH_CASCADE_SCRIPT = """\
// Auth cascade — the first configured credential wins:
//   1. {prefix}_AUTH_API_KEY               -> Authorization: {api_key_scheme} <key>
//   2. {prefix}_AUTH_EMAIL + _PASSWORD     -> POST {login_endpoint}, then Bearer <token>
//   3. otherwise                           -> the collection's OAuth2 (Auth0) auth
const P = "{prefix}";
const g = (k) => pm.environment.get(P ? P + "_" + k : k);
const setVar = (k, v) => pm.environment.set(P ? P + "_" + k : k, v);

// 1) API key
const apiKey = g("AUTH_API_KEY");
if (apiKey) {{
    pm.request.auth = {{ type: "noauth" }};
    pm.request.headers.upsert({{ key: "Authorization", value: "{api_key_scheme} " + apiKey }});
    return;
}}

// 2) email / password -> session token via the login endpoint
const email = g("AUTH_EMAIL");
const password = g("AUTH_PASSWORD");
if (email && password) {{
    pm.request.auth = {{ type: "noauth" }};
    const token = g("AUTH_BEARER_TOKEN");
    const expiresAt = parseInt(g("AUTH_EXPIRES_AT") || "0");
    // Reuse a cached session token while it is still valid (1h safety margin).
    if (token && expiresAt && Date.now() < expiresAt - 3600000) {{
        pm.request.headers.upsert({{ key: "Authorization", value: "Bearer " + token }});
        return;
    }}
    pm.sendRequest({{
        url: g("BASE_URL") + "{login_endpoint}",
        method: "POST",
        header: {{ "Content-Type": "application/x-www-form-urlencoded" }},
        body: {{ mode: "urlencoded", urlencoded: [
            {{ key: "email", value: email }},
            {{ key: "password", value: password }}
        ] }}
    }}, (err, res) => {{
        if (err || res.code !== 200) {{
            console.error("Login failed:", err || res.text());
            return;
        }}
        const body = res.json();
        const sessionId = body.{token_field};
        const expiresDays = body.expires_days || 1;
        setVar("AUTH_BEARER_TOKEN", sessionId);
        setVar("AUTH_EXPIRES_AT", (Date.now() + expiresDays * 86400000).toString());
        pm.request.headers.upsert({{ key: "Authorization", value: "Bearer " + sessionId }});
    }});
    return;
}}

// 3) no API key, no credentials -> fall through to the collection OAuth2 (Auth0) auth
"""


def build_auth_cascade_script(
    prefix: str, login_endpoint: str, token_field: str = "session_id", api_key_scheme: str = "Api-Key"
) -> list[str]:
    """Build the cascading-auth pre-request script lines."""
    script = _AUTH_CASCADE_SCRIPT.format(
        prefix=prefix, login_endpoint=login_endpoint, token_field=token_field, api_key_scheme=api_key_scheme
    )
    return script.splitlines()


def apply_auth_cascade(
    collection: dict[str, Any],
    prefix: str,
    login_endpoint: str,
    token_field: str = "session_id",
    api_key_scheme: str = "Api-Key",
) -> dict[str, str]:
    """Add the cascading-auth pre-request script to the collection.

    At request time the first configured credential wins: ``AUTH_API_KEY``
    (sent as ``Authorization: {api_key_scheme} <key>``), else ``AUTH_EMAIL``
    + ``AUTH_PASSWORD`` (login at ``login_endpoint`` → Bearer token), else the
    request falls through to the collection's OAuth2 (Auth0) auth. The first two
    neutralise the collection auth for that request (``pm.request.auth =
    noauth``). Returns the extra env vars to surface.
    """
    script_lines = build_auth_cascade_script(prefix, login_endpoint, token_field, api_key_scheme)
    # Preserve existing events, replace or add prerequest
    events: list[dict[str, Any]] = collection.get("event", [])
    events = [e for e in events if e.get("listen") != "prerequest"]
    events.append({"listen": "prerequest", "script": {"type": "text/javascript", "exec": script_lines}})
    collection["event"] = events
    print(f"  Auth cascade: API key > {login_endpoint} login > OAuth2", file=sys.stderr)

    return {
        _prefixed(prefix, "AUTH_API_KEY"): "",
        _prefixed(prefix, "AUTH_EMAIL"): "",
        _prefixed(prefix, "AUTH_PASSWORD"): "",
        _prefixed(prefix, "AUTH_BEARER_TOKEN"): "",
        _prefixed(prefix, "AUTH_EXPIRES_AT"): "",
    }


# ---------------------------------------------------------------------------
# Step 5: Analyze path parameters in collection
# ---------------------------------------------------------------------------


def collect_path_params(items: list[dict[str, Any]]) -> Counter[str]:
    """Count occurrences of each path parameter across all requests."""
    counts: Counter[str] = Counter()
    for item in items:
        if "item" in item:
            counts.update(collect_path_params(item["item"]))
        req = item.get("request", {})
        url = req.get("url", {})
        for var in url.get("variable", []):
            key = var.get("key", "")
            if key:
                counts[key] += 1
    return counts


def to_env_var_name(param_name: str, prefix: str = "") -> str:
    """Convert a path parameter name to an environment variable name."""
    upper = param_name.upper()
    if prefix:
        return f"{prefix}_{upper}"
    return upper


# ---------------------------------------------------------------------------
# Step 6: Post-process -- replace base URL and path parameters
# ---------------------------------------------------------------------------


def replace_base_url(raw: str, base_url: str, var_name: str = "BASE_URL") -> str:
    """Replace hardcoded base URL with {{var_name}} variable."""
    if not base_url:
        return raw
    # Escape for regex, replace the base URL
    escaped = re.escape(base_url.rstrip("/"))
    raw = re.sub(escaped, "{{" + var_name + "}}", raw)
    return raw


def patch_path_variables(items: list[dict[str, Any]], param_vars: dict[str, str]) -> int:
    """Replace path parameter values with Postman env vars. Returns count of replacements."""
    count = 0
    for item in items:
        if "item" in item:
            count += patch_path_variables(item["item"], param_vars)
        req = item.get("request", {})
        url = req.get("url", {})
        for var in url.get("variable", []):
            env_key = param_vars.get(var.get("key", ""))
            if env_key:
                var["value"] = "{{" + env_key + "}}"
                count += 1
    return count


# ---------------------------------------------------------------------------
# Step 7: Generate Postman environment
# ---------------------------------------------------------------------------


def generate_environment(
    output_dir: str,
    env_name: str,
    base_url: str | None,
    param_vars: dict[str, str],
    base_url_var: str = "BASE_URL",
    auth_vars: dict[str, str] | None = None,
    defaults: dict[str, str] | None = None,
) -> str:
    """Generate a Postman environment file."""
    defs = defaults or {}
    values: list[dict[str, Any]] = []
    if base_url:
        values.append({"key": base_url_var, "value": base_url, "enabled": True})
    # Auth variables -- use auth_vars defaults, overridden by user defaults; secrets are masked
    secret_vars = {"SECRET", "TOKEN", "PASSWORD", "KEY"}
    for var_name, auth_default in sorted((auth_vars or {}).items()):
        val = defs.get(var_name, auth_default)
        is_secret = any(s in var_name.upper() for s in secret_vars)
        entry: dict[str, Any] = {"key": var_name, "value": val, "enabled": True}
        if is_secret:
            entry["type"] = "secret"
        values.append(entry)
    for _param, env_var in sorted(param_vars.items(), key=lambda x: x[1]):
        values.append({"key": env_var, "value": defs.get(env_var, ""), "enabled": True})

    env = {
        "id": f"{env_name.lower().replace(' ', '-')}-env",
        "name": env_name,
        "values": values,
        "_postman_variable_scope": "environment",
    }
    slug = env_name.lower().replace(" ", "-")
    env_path = os.path.join(output_dir, f"{slug}.postman_environment.json")
    with open(env_path, "w") as f:
        json.dump(env, f, indent=2)
    return env_path


# ---------------------------------------------------------------------------
# Step 8: Validate
# ---------------------------------------------------------------------------


def count_requests(items: list[dict[str, Any]]) -> int:
    """Count total requests in a Postman collection."""
    n = 0
    for item in items:
        if "request" in item:
            n += 1
        if "item" in item:
            n += count_requests(item["item"])
    return n


def validate(output_path: str) -> dict[str, Any]:
    """Validate and return stats about the generated collection."""
    with open(output_path) as f:
        c = json.load(f)
    info = c.get("info", {})
    items = c.get("item", [])
    return {
        "name": info.get("name", "N/A"),
        "folders": len(items),
        "requests": count_requests(items),
    }


# ---------------------------------------------------------------------------
# Step 9: Import to Postman via API
# ---------------------------------------------------------------------------


def postman_api_request(method: str, path: str, api_key: str, data: Any = None) -> dict[str, Any]:
    """Make a request to the Postman API."""
    url = f"{POSTMAN_API_URL}{path}"
    headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
    body = json.dumps(data).encode() if data else None
    try:
        resp = httpx.request(method, url, content=body, headers=headers, timeout=HTTP_TIMEOUT, follow_redirects=True)
        resp.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"ERROR: Postman API {method} {path} -> {e.response.status_code}: {e.response.text}", file=sys.stderr)
        raise
    result: dict[str, Any] = resp.json()
    return result


def postman_get_workspaces(api_key: str) -> list[dict[str, Any]]:
    """List all Postman workspaces."""
    resp = postman_api_request("GET", "/workspaces", api_key)
    workspaces: list[dict[str, Any]] = resp.get("workspaces", [])
    return workspaces


def postman_find_collection_by_name(api_key: str, workspace_id: str, name: str) -> dict[str, Any] | None:
    """Find a collection by name in a workspace. Returns {id, uid, name} or None."""
    resp = postman_api_request("GET", f"/collections?workspace={workspace_id}", api_key)
    for col in resp.get("collections", []):
        if col.get("name") == name:
            return {"id": col["id"], "uid": col["uid"], "name": col["name"]}
    return None


def postman_find_environment_by_name(api_key: str, workspace_id: str, name: str) -> dict[str, Any] | None:
    """Find an environment by name in a workspace. Returns {id, uid, name} or None."""
    resp = postman_api_request("GET", f"/environments?workspace={workspace_id}", api_key)
    for env in resp.get("environments", []):
        if env.get("name") == name:
            return {"id": env["id"], "uid": env["uid"], "name": env["name"]}
    return None


def postman_get_environment_values(api_key: str, env_id: str) -> list[dict[str, Any]]:
    """Fetch current values of an existing environment."""
    resp = postman_api_request("GET", f"/environments/{env_id}", api_key)
    values: list[dict[str, Any]] = resp.get("environment", {}).get("values", [])
    return values


def _prepare_collection(collection_path: str) -> dict[str, Any]:
    """Load a collection file and prepare it for the Postman API."""
    with open(collection_path) as f:
        collection: dict[str, Any] = json.load(f)
    info = collection.get("info", {})
    info["schema"] = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
    info.pop("_postman_id", None)
    collection["info"] = info
    return collection


def postman_upsert_collection(api_key: str, workspace_id: str, collection_path: str) -> dict[str, Any]:
    """Create or update a collection in a workspace (matched by name)."""
    collection = _prepare_collection(collection_path)
    col_name = collection.get("info", {}).get("name", "")

    existing = postman_find_collection_by_name(api_key, workspace_id, col_name)
    if existing:
        col_id = existing["id"]
        print(f"  Updating existing collection '{col_name}' ({col_id})...", file=sys.stderr)
        resp = postman_api_request("PUT", f"/collections/{col_id}", api_key, {"collection": collection})
        info = resp.get("collection", {})
        return {"id": info.get("id", col_id), "uid": info.get("uid"), "name": col_name, "action": "updated"}

    print(f"  Creating new collection '{col_name}'...", file=sys.stderr)
    resp = postman_api_request("POST", f"/collections?workspace={workspace_id}", api_key, {"collection": collection})
    info = resp.get("collection", {})
    return {"id": info.get("id"), "uid": info.get("uid"), "name": info.get("name"), "action": "created"}


def _merge_env_values(
    existing_values: list[dict[str, Any]],
    new_values: list[dict[str, Any]],
    append_only: bool = False,
) -> list[dict[str, Any]]:
    """Merge environment values: keep non-empty existing values, add new keys.

    If append_only is False (default), variables not in new_values are removed.
    If append_only is True, existing variables are always kept (only new ones are added).
    """
    existing_by_key = {v["key"]: v for v in existing_values}
    new_keys = {v["key"] for v in new_values}
    merged: list[dict[str, Any]] = []

    if append_only:
        # Start with all existing values (preserve everything)
        merged = list(existing_values)
        # Add new keys that don't exist yet
        added = []
        for new_val in new_values:
            if new_val["key"] not in existing_by_key:
                merged.append(new_val)
                added.append(new_val["key"])
        if added:
            print(f"    Added new variables: {', '.join(sorted(added))}", file=sys.stderr)
    else:
        # Replace mode: use new_values as base, preserve non-empty existing values
        for new_val in new_values:
            key = new_val["key"]
            old = existing_by_key.get(key)
            if old and old.get("value"):
                merged.append({**new_val, "value": old["value"]})
            else:
                merged.append(new_val)
        dropped = set(existing_by_key) - new_keys
        if dropped:
            print(f"    Removed obsolete variables: {', '.join(sorted(dropped))}", file=sys.stderr)

    return merged


def postman_upsert_environment(
    api_key: str, workspace_id: str, env_path: str, append_only: bool = False
) -> dict[str, Any]:
    """Create or update an environment in a workspace (matched by name), preserving non-empty values."""
    with open(env_path) as f:
        env: dict[str, Any] = json.load(f)
    env_name = env.get("name", "Environment")
    new_values: list[dict[str, Any]] = env.get("values", [])

    existing = postman_find_environment_by_name(api_key, workspace_id, env_name)
    if existing:
        env_id = existing["id"]
        print(f"  Updating existing environment '{env_name}' ({env_id})...", file=sys.stderr)
        # Fetch current values and merge
        current_values = postman_get_environment_values(api_key, env_id)
        merged = _merge_env_values(current_values, new_values, append_only=append_only)
        preserved = sum(1 for m, n in zip(merged, new_values, strict=False) if m.get("value") != n.get("value"))
        if preserved:
            print(f"    Preserved {preserved} user-defined value(s)", file=sys.stderr)
        resp = postman_api_request(
            "PUT", f"/environments/{env_id}", api_key, {"environment": {"name": env_name, "values": merged}}
        )
        info = resp.get("environment", {})
        return {"id": info.get("id", env_id), "uid": info.get("uid"), "name": env_name, "action": "updated"}

    print(f"  Creating new environment '{env_name}'...", file=sys.stderr)
    resp = postman_api_request(
        "POST",
        f"/environments?workspace={workspace_id}",
        api_key,
        {"environment": {"name": env_name, "values": new_values}},
    )
    info = resp.get("environment", {})
    return {"id": info.get("id"), "uid": info.get("uid"), "name": info.get("name"), "action": "created"}


def import_to_postman(
    api_key: str,
    workspace_id: str | None,
    collection_path: str,
    env_paths: list[str],
    append_env: bool = False,
) -> dict[str, Any]:
    """Upsert collection and environments into Postman. Returns summary."""
    # Resolve workspace
    if not workspace_id:
        workspaces = postman_get_workspaces(api_key)
        if not workspaces:
            print("ERROR: no Postman workspaces found", file=sys.stderr)
            sys.exit(1)
        personal = [w for w in workspaces if w.get("type") == "personal"]
        ws = personal[0] if personal else workspaces[0]
        workspace_id = ws["id"]
        print(f"  Using workspace: {ws.get('name', workspace_id)}", file=sys.stderr)

    result: dict[str, Any] = {"workspace_id": workspace_id, "collection": None, "environments": []}

    # Upsert collection
    col_info = postman_upsert_collection(api_key, workspace_id, collection_path)
    result["collection"] = col_info
    print(f"  Collection {col_info['action']}: {col_info['name']} ({col_info.get('uid')})", file=sys.stderr)

    # Upsert environments
    for env_path in env_paths:
        env_info = postman_upsert_environment(api_key, workspace_id, env_path, append_only=append_env)
        result["environments"].append(env_info)
        print(f"  Environment {env_info['action']}: {env_info['name']} ({env_info.get('uid')})", file=sys.stderr)

    return result


# ---------------------------------------------------------------------------
# Conversion orchestration
# ---------------------------------------------------------------------------


@dataclass
class PostmanConversionRequest:
    """Options driving an OpenAPI -> Postman conversion (mirrors the CLI options)."""

    spec: str
    output: str | None = None
    env_name: str | None = None
    min_occurrences: int = 2
    import_postman: bool = False
    append_env: bool = False
    workspace: str | None = None
    extra_env: list[str] | None = None
    env_prefix: str = ""
    auth_type: str = "auto"
    oidc_url: str | None = None
    login_endpoint: str | None = None
    login_token_field: str = "session_id"
    api_key_scheme: str = "Api-Key"
    extra_base_url: list[str] | None = None
    env_default: list[str] | None = None


def convert_openapi_to_postman(req: PostmanConversionRequest) -> dict[str, Any]:
    """Convert an OpenAPI spec to a Postman collection (+ environments), optionally importing it.

    Returns the machine-readable result dict. Progress is logged to stderr; the CLI
    command only parses options and delegates here.
    """
    extra_env_list = req.extra_env or []
    extra_base_url_list = req.extra_base_url or []
    env_default_list = req.env_default or []

    # Resolve spec
    spec_path = resolve_spec(req.spec)
    spec_name = Path(spec_path).stem.replace(".openapi", "").replace(".swagger", "")

    # Output path
    output_path = req.output or f"{spec_name}.postman_collection.json"
    output_dir = os.path.dirname(os.path.abspath(output_path)) or "."

    # Ensure CLI
    cli_path = ensure_cli()

    # Convert
    convert(cli_path, spec_path, output_path)

    # Extract spec metadata (base URL + auth schemes)
    metadata = extract_spec_metadata(spec_path)
    base_url = metadata.base_url

    # Load collection
    with open(output_path) as f:
        raw = f.read()

    # Environment variable prefix
    prefix = req.env_prefix.upper().rstrip("_") if req.env_prefix else ""

    # Replace base URL
    base_url_var = f"{prefix}_BASE_URL" if prefix else "BASE_URL"
    if base_url:
        raw = replace_base_url(raw, base_url, base_url_var)
        print(f"  Base URL '{base_url}' -> {{{{{base_url_var}}}}}", file=sys.stderr)

    collection = json.loads(raw)

    # Apply collection-level auth from spec security schemes
    resolved_auth_type, auth_vars = apply_collection_auth(collection, metadata.auth_schemes, prefix, req.auth_type)

    # Strip per-request auth so all requests inherit from collection
    if auth_vars:
        stripped = strip_request_auth(collection.get("item", []))
        if stripped:
            print(f"  Stripped per-request auth from {stripped} requests (inherit collection auth)", file=sys.stderr)

    # Add auto-login pre-request script if requested
    login_vars: dict[str, str] = {}
    if req.login_endpoint:
        login_vars = apply_auth_cascade(
            collection, prefix, req.login_endpoint, req.login_token_field, req.api_key_scheme
        )
        auth_vars = {**auth_vars, **login_vars}

    # Analyze path parameters
    param_counts = collect_path_params(collection.get("item", []))
    # Keep params with >= min_occurrences
    frequent_params = {p: to_env_var_name(p, prefix) for p, c in param_counts.items() if c >= req.min_occurrences}

    if frequent_params:
        print(f"  Path parameters with >= {req.min_occurrences} occurrences:", file=sys.stderr)
        for param, env_var in sorted(frequent_params.items(), key=lambda x: -param_counts[x[0]]):
            print(f"    {param} ({param_counts[param]}x) -> {{{{{env_var}}}}}", file=sys.stderr)

        replaced = patch_path_variables(collection.get("item", []), frequent_params)
        print(f"  Replaced {replaced} path parameter values", file=sys.stderr)

    with open(output_path, "w") as f:
        json.dump(collection, f, indent=2)

    # Derive environment name
    resolved_env_name = req.env_name or collection.get("info", {}).get("name", spec_name)

    # Parse default values for environment variables
    env_defaults: dict[str, str] = {}
    for default in env_default_list:
        if "=" not in default:
            print(f"WARNING: ignoring --env-default '{default}' (expected VAR=VALUE)", file=sys.stderr)
            continue
        var, val = default.split("=", 1)
        env_defaults[var] = val

    # Resolve OAuth2 defaults per environment (each env may have its own OIDC URL)
    is_oauth2 = resolved_auth_type == "oauth2"
    spec_oidc_url = _find_oidc_url(metadata.auth_schemes) if is_oauth2 else ""
    primary_oidc_url = req.oidc_url or spec_oidc_url

    # Primary environment: resolve auth defaults from its OIDC
    primary_auth_defaults = resolve_oauth2_env_vars(prefix, primary_oidc_url) if is_oauth2 else auth_vars
    primary_defaults = {**primary_auth_defaults, **env_defaults}

    # All environment variables (base URL + auth + path params)
    all_env_vars = {base_url_var: base_url or "", **auth_vars, **dict.fromkeys(frequent_params.values(), "")}

    # Generate primary environment
    env_path = generate_environment(
        output_dir, resolved_env_name, base_url, frequent_params, base_url_var, auth_vars, primary_defaults
    )
    print(f"  Environment: {env_path}", file=sys.stderr)
    env_paths = [env_path]

    # Generate extra environments from --extra-base-url
    # Format: "Name=URL" or "Name=URL,oidc=OIDC_URL"
    for extra in extra_base_url_list:
        if "=" not in extra:
            print(f"WARNING: ignoring --extra-base-url '{extra}' (expected NAME=URL)", file=sys.stderr)
            continue
        extra_name, extra_rest = extra.split("=", 1)
        # Parse optional ,oidc= suffix
        extra_oidc_url = ""
        if ",oidc=" in extra_rest:
            extra_url, extra_oidc_url = extra_rest.rsplit(",oidc=", 1)
        else:
            extra_url = extra_rest
        # Resolve auth defaults for this environment
        if is_oauth2 and extra_oidc_url:
            extra_auth_defaults = resolve_oauth2_env_vars(prefix, extra_oidc_url)
        elif is_oauth2:
            # No OIDC specified: inherit from primary
            extra_auth_defaults = primary_auth_defaults
        else:
            extra_auth_defaults = auth_vars
        extra_defaults = {**extra_auth_defaults, **env_defaults}
        extra_env_path = generate_environment(
            output_dir, extra_name, extra_url, frequent_params, base_url_var, auth_vars, extra_defaults
        )
        env_paths.append(extra_env_path)
        print(f"  Environment: {extra_env_path}", file=sys.stderr)

    # Add any manually specified extra env files
    env_paths.extend(extra_env_list)

    # Validate
    stats = validate(output_path)
    print(f"\nCollection: {stats['name']}", file=sys.stderr)
    print(f"Folders:    {stats['folders']}", file=sys.stderr)
    print(f"Requests:   {stats['requests']}", file=sys.stderr)
    print(f"Output:     {output_path}", file=sys.stderr)
    for ep in env_paths:
        print(f"Environment: {ep}", file=sys.stderr)

    # Machine-readable output
    result: dict[str, Any] = {
        "collection": output_path,
        "environments": env_paths,
        "stats": stats,
        "env_vars": all_env_vars,
    }

    # Import to Postman if requested
    if req.import_postman:
        api_key = resolve_postman_api_key()
        if not api_key:
            print(
                "ERROR: Postman API key not found."
                " Set POSTMAN_API_KEY env var or configure the Postman MCP in ~/.claude.json",
                file=sys.stderr,
            )
            sys.exit(1)
        import_result = import_to_postman(api_key, req.workspace, output_path, env_paths, append_env=req.append_env)
        result["postman_import"] = import_result

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

cli = typer.Typer()


@cli.command()
def main(
    spec: Annotated[str, typer.Argument(help="OpenAPI spec file path or URL")],
    output: Annotated[str | None, typer.Option("--output", "-o", help="Output collection file path")] = None,
    env_name: Annotated[
        str | None,
        typer.Option("--env-name", help="Name for the Postman environment (default: derived from spec title)"),
    ] = None,
    min_occurrences: Annotated[
        int,
        typer.Option(
            "--min-occurrences",
            help="Minimum occurrences for a path param to become an env var (default: 2)",
        ),
    ] = 2,
    import_postman: Annotated[
        bool,
        typer.Option("--import-postman", help="Import collection and environments into Postman via the API"),
    ] = False,
    append_env: Annotated[
        bool,
        typer.Option(
            "--append-env",
            help="Append-only environment upsert: add new variables but never remove existing ones",
        ),
    ] = False,
    workspace: Annotated[
        str | None,
        typer.Option("--workspace", help="Postman workspace ID to import into (default: first personal workspace)"),
    ] = None,
    extra_env: Annotated[
        list[str] | None,
        typer.Option("--extra-env", help="Additional environment files to import (can be repeated)"),
    ] = None,
    env_prefix: Annotated[
        str,
        typer.Option(
            "--env-prefix",
            help="Prefix for environment variable names (e.g. 'PYSAE' -> PYSAE_GROUP_ID)",
        ),
    ] = "",
    auth_type: Annotated[
        str,
        typer.Option(
            "--auth-type",
            help="Collection-level authentication type: auto, oauth2, bearer, apikey, basic, none (default: auto)",
        ),
    ] = "auto",
    oidc_url: Annotated[
        str | None,
        typer.Option(
            "--oidc-url",
            help="Override the OIDC discovery URL for the primary environment (default: from spec)",
        ),
    ] = None,
    login_endpoint: Annotated[
        str | None,
        typer.Option("--login-endpoint", help="Add auto-login pre-request script (e.g. '/api/v4/login')"),
    ] = None,
    login_token_field: Annotated[
        str,
        typer.Option(
            "--login-token-field",
            help="JSON field name in the login response containing the token (default: session_id)",
        ),
    ] = "session_id",
    api_key_scheme: Annotated[
        str,
        typer.Option(
            "--api-key-scheme",
            help="Authorization scheme prefix for the AUTH_API_KEY cascade level (default: 'Api-Key').",
        ),
    ] = "Api-Key",
    extra_base_url: Annotated[
        list[str] | None,
        typer.Option(
            "--extra-base-url",
            metavar="NAME=URL",
            help="Generate additional environments with different base URLs (e.g. 'Dev=https://dev.api.example.com')",
        ),
    ] = None,
    env_default: Annotated[
        list[str] | None,
        typer.Option(
            "--env-default",
            metavar="VAR=VALUE",
            help="Set default values for environment variables (e.g. 'PYSAE_GROUP_ID=pysae')",
        ),
    ] = None,
) -> None:
    """Convert an OpenAPI spec to a Postman collection (with env variables)."""
    result = convert_openapi_to_postman(
        PostmanConversionRequest(
            spec=spec,
            output=output,
            env_name=env_name,
            min_occurrences=min_occurrences,
            import_postman=import_postman,
            append_env=append_env,
            workspace=workspace,
            extra_env=extra_env,
            env_prefix=env_prefix,
            auth_type=auth_type,
            oidc_url=oidc_url,
            login_endpoint=login_endpoint,
            login_token_field=login_token_field,
            api_key_scheme=api_key_scheme,
            extra_base_url=extra_base_url,
            env_default=env_default,
        )
    )
    print(json.dumps(result))


if __name__ == "__main__":
    cli()
