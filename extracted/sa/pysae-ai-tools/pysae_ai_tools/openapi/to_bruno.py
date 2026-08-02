#!/usr/bin/env python3
"""Convert an OpenAPI spec to a Bruno collection ("collection as code").

Reuses the OpenAPI -> Postman conversion pipeline (openapi2postmanv2 + the
post-processing in ``to_postman``: base-URL variable, collection-level auth from
the spec security schemes, path-parameter variables) and serialises the
resulting in-memory Postman collection to a Bruno collection directory, in one of
two on-disk formats:

- ``yaml`` — OpenCollection YAML (Bruno 3.1+ default): ``opencollection.yml`` +
  per-request ``<Name>.yml`` + ``folder.yml`` + ``environments/<Name>.yml``.
- ``bru`` — legacy Bruno DSL: ``bruno.json`` + ``collection.bru`` +
  ``<Request>.bru`` + ``environments/<Name>.bru``.

Bruno stores collections on disk, so there is no API import step: point Bruno at
the generated directory (Open Collection). Both formats stay fully supported by
Bruno 3.x.
"""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Any

import typer
import yaml

from .bruno_app import (
    SYSTEM_BROWSER_CALLBACK_URL,
    active_workspace_path,
    bruno_config_dir,
    register_collection_in_workspace,
    set_system_browser,
)
from .to_postman import (
    _find_oidc_url,
    _prefixed,
    apply_collection_auth,
    collect_path_params,
    convert,
    ensure_cli,
    extract_spec_metadata,
    patch_path_variables,
    replace_base_url,
    resolve_oauth2_env_vars,
    resolve_spec,
    strip_request_auth,
    to_env_var_name,
)

INDENT = "  "

# Bruno's built-in browser intercepts the OAuth2 redirect internally (it never
# navigates to the callback), so a localhost URL works without any listener and
# avoids reusing Postman's hosted callback. It must still be in the IdP's allowed
# callback URLs (the pysae-ai-tools Auth0 app already allows localhost:8765-8767).
BRUNO_CALLBACK_URL = "http://localhost:8765/callback"

_SECRET_SUFFIXES = ("_API_KEY", "_CLIENT_SECRET", "_PASSWORD", "_BEARER_TOKEN")


def _is_secret_var(name: str) -> bool:
    """A variable whose value must live in Bruno's secret store, not the .bru file."""
    upper = name.upper()
    return upper.endswith(_SECRET_SUFFIXES)


# ---------------------------------------------------------------------------
# .bru block rendering
# ---------------------------------------------------------------------------

_KEY_NEEDS_QUOTING = re.compile(r'[:"{}\s]')


def _key_str(key: str) -> str:
    """Quote a dictionary key when it contains a reserved character."""
    if _KEY_NEEDS_QUOTING.search(key):
        return '"' + key.replace('"', '\\"') + '"'
    return key


def _indent(text: str) -> str:
    """Indent every line of ``text`` by one level (blank lines stay blank)."""
    return "\n".join(INDENT + line if line else line for line in text.split("\n"))


def _dict_block(name: str, pairs: list[tuple[str, str, bool]]) -> str:
    """Render a dictionary block (``name { key: value }``). Each pair is (key, value, disabled)."""
    lines = [f"{name} {{"]
    for key, value, disabled in pairs:
        prefix = "~" if disabled else ""
        lines.append(f"{INDENT}{prefix}{_key_str(key)}: {value}")
    lines.append("}")
    return "\n".join(lines)


def _text_block(name: str, body: str) -> str:
    """Render a text block (``name { <raw multi-line content> }``)."""
    inner = _indent(body)
    return f"{name} {{\n{inner}\n}}"


def _secret_list_block(names: list[str]) -> str:
    """Render the ``vars:secret [ ... ]`` list block (names only, no values)."""
    if not names:
        return ""
    entries = ",\n".join(f"{INDENT}{n}" for n in names)
    return f"vars:secret [\n{entries}\n]"


# ---------------------------------------------------------------------------
# Filesystem-safe names
# ---------------------------------------------------------------------------

_FS_UNSAFE = re.compile(r'[/\\:*?"<>|]+')


def _safe_name(name: str, used: set[str]) -> str:
    """Sanitise an item name into a unique filesystem base name within a directory."""
    base = _FS_UNSAFE.sub("-", name).strip() or "request"
    candidate = base
    n = 2
    while candidate.lower() in used:
        candidate = f"{base} ({n})"
        n += 1
    used.add(candidate.lower())
    return candidate


# ---------------------------------------------------------------------------
# Postman auth object -> Bruno auth blocks
# ---------------------------------------------------------------------------


def _oauth2_pairs(oauth2: dict[str, str]) -> list[str]:
    """Render the auth:oauth2 body lines for an authorization-code + PKCE flow.

    ``grant_type`` is fixed to ``authorization_code``: Bruno's .bru parser only
    accepts password/authorization_code/implicit/client_credentials and silently
    drops the whole oauth2 block on anything else — the Postman value carries the
    PKCE marker (``authorization_code_with_pkce``), which is conveyed separately
    by the ``pkce: true`` line below.
    """
    return [
        f"{INDENT}grant_type: authorization_code",
        f"{INDENT}callback_url: {oauth2.get('redirect_uri', '')}",
        f"{INDENT}authorization_url: {oauth2.get('authUrl', '')}",
        f"{INDENT}access_token_url: {oauth2.get('accessTokenUrl', '')}",
        f"{INDENT}client_id: {oauth2.get('clientId', '')}",
        f"{INDENT}client_secret: {oauth2.get('clientSecret', '')}",
        f"{INDENT}scope: {oauth2.get('scope', '')}",
        f"{INDENT}pkce: true",
        f"{INDENT}credentials_placement: body",
        f"{INDENT}token_source: access_token",
        f"{INDENT}token_placement: header",
        f"{INDENT}token_header_prefix: Bearer",
        f"{INDENT}auto_fetch_token: false",
        f"{INDENT}auto_refresh_token: false",
    ]


def _postman_auth_to_bruno(auth: dict[str, Any] | None) -> tuple[str, str]:
    """Map a Postman collection auth object to (mode, detail_block). Empty block for none/inherit."""
    if not auth:
        return "none", ""
    auth_type = auth.get("type", "none")

    if auth_type == "oauth2":
        oauth2 = {entry["key"]: entry.get("value", "") for entry in auth.get("oauth2", [])}
        body = "\n".join(_oauth2_pairs(oauth2))
        return "oauth2", f"auth:oauth2 {{\n{body}\n}}"

    if auth_type == "bearer":
        bearer = {entry["key"]: entry.get("value", "") for entry in auth.get("bearer", [])}
        return "bearer", _dict_block("auth:bearer", [("token", bearer.get("token", ""), False)])

    if auth_type == "apikey":
        apikey = {entry["key"]: entry.get("value", "") for entry in auth.get("apikey", [])}
        placement = "queryparams" if apikey.get("in") == "query" else "header"
        pairs = [
            ("key", apikey.get("key", ""), False),
            ("value", apikey.get("value", ""), False),
            ("placement", placement, False),
        ]
        return "apikey", _dict_block("auth:apikey", pairs)

    if auth_type == "basic":
        basic = {entry["key"]: entry.get("value", "") for entry in auth.get("basic", [])}
        pairs = [
            ("username", basic.get("username", ""), False),
            ("password", basic.get("password", ""), False),
        ]
        return "basic", _dict_block("auth:basic", pairs)

    return "none", ""


# ---------------------------------------------------------------------------
# Cascading-auth pre-request script (Bruno-native: bru / req)
# ---------------------------------------------------------------------------

_BRU_CASCADE_SCRIPT = """\
// Auth cascade — the first configured credential wins:
//   1. {prefix}AUTH_API_KEY               -> Authorization: {api_key_scheme} <key>
//   2. {prefix}AUTH_EMAIL + _PASSWORD     -> POST {login_endpoint}, then Bearer <token>
//   3. otherwise                          -> the collection's OAuth2 (Auth0) auth
const P = "{prefix_val}";
const g = (k) => bru.getEnvVar(P ? P + "_" + k : k);
const setVar = (k, v) => bru.setEnvVar(P ? P + "_" + k : k, v, {{ persist: true }});

// 1) API key
const apiKey = g("AUTH_API_KEY");
if (apiKey) {{
  req.setHeader("Authorization", "{api_key_scheme} " + apiKey);
  return;
}}

// 2) email / password -> session token via the login endpoint
const email = g("AUTH_EMAIL");
const password = g("AUTH_PASSWORD");
if (email && password) {{
  const token = g("AUTH_BEARER_TOKEN");
  const expiresAt = parseInt(g("AUTH_EXPIRES_AT") || "0");
  // Reuse a cached session token while it is still valid (1h safety margin).
  if (token && expiresAt && Date.now() < expiresAt - 3600000) {{
    req.setHeader("Authorization", "Bearer " + token);
    return;
  }}
  const res = await bru.sendRequest({{
    url: g("BASE_URL") + "{login_endpoint}",
    method: "POST",
    headers: {{ "Content-Type": "application/x-www-form-urlencoded" }},
    data: "email=" + encodeURIComponent(email) + "&password=" + encodeURIComponent(password),
  }});
  const body = res.data;
  const sessionId = body.{token_field};
  const expiresDays = body.expires_days || 1;
  setVar("AUTH_BEARER_TOKEN", sessionId);
  setVar("AUTH_EXPIRES_AT", (Date.now() + expiresDays * 86400000).toString());
  req.setHeader("Authorization", "Bearer " + sessionId);
  return;
}}

// 3) no API key, no credentials -> fall through to the collection OAuth2 (Auth0) auth
"""


def build_bruno_cascade_script(
    prefix: str, login_endpoint: str, token_field: str = "session_id", api_key_scheme: str = "Api-Key"
) -> str:
    """Build the Bruno-native cascading-auth pre-request script."""
    label_prefix = f"{prefix}_" if prefix else ""
    return _BRU_CASCADE_SCRIPT.format(
        prefix=label_prefix,
        prefix_val=prefix,
        login_endpoint=login_endpoint,
        token_field=token_field,
        api_key_scheme=api_key_scheme,
    ).rstrip("\n")


# ---------------------------------------------------------------------------
# Request item -> .bru
# ---------------------------------------------------------------------------


def _substitute_collection_vars(url: str, collection_vars: dict[str, str]) -> str:
    """Resolve one level of Postman collection variables (e.g. {{baseUrl}} -> {{PYSAE_BASE_URL}})."""
    for key, value in collection_vars.items():
        url = url.replace("{{" + key + "}}", value)
    return url


def _request_url(req: dict[str, Any], collection_vars: dict[str, str]) -> str:
    """Extract the request URL string from a Postman request, resolving collection vars."""
    url = req.get("url", {})
    if isinstance(url, str):
        raw = url
    else:
        raw = url.get("raw", "")
        if not raw:
            host = url.get("host", [])
            host_str = ".".join(host) if isinstance(host, list) else str(host)
            path = url.get("path", [])
            path_str = "/".join(str(p) for p in path) if isinstance(path, list) else str(path)
            raw = f"{host_str}/{path_str}" if path_str else host_str
    return _substitute_collection_vars(raw, collection_vars)


def _body_blocks(body: dict[str, Any]) -> tuple[str, str]:
    """Return (body_mode_token, body_block) for a Postman request body."""
    mode = body.get("mode")
    if mode == "raw":
        raw = body.get("raw", "")
        language = body.get("options", {}).get("raw", {}).get("language", "")
        if language == "json" or (raw.strip().startswith(("{", "["))):
            return "json", _text_block("body:json", raw)
        return "text", _text_block("body:text", raw)
    if mode == "urlencoded":
        pairs = [(p.get("key", ""), p.get("value", ""), bool(p.get("disabled"))) for p in body.get("urlencoded", [])]
        return "form-urlencoded", _dict_block("body:form-urlencoded", pairs)
    return "none", ""


def serialize_request(item: dict[str, Any], seq: int, collection_vars: dict[str, str]) -> str:
    """Serialise a Postman request item to a .bru file body."""
    req = item.get("request", {})
    method = str(req.get("method", "GET")).lower()
    url = _request_url(req, collection_vars)

    query_pairs: list[tuple[str, str, bool]] = []
    url_obj = req.get("url", {})
    if isinstance(url_obj, dict):
        query_pairs = [
            (q.get("key", ""), q.get("value", ""), bool(q.get("disabled"))) for q in url_obj.get("query", [])
        ]
    if query_pairs:
        url = url.split("?", 1)[0]

    path_pairs: list[tuple[str, str, bool]] = []
    if isinstance(url_obj, dict):
        path_pairs = [
            (v.get("key", ""), v.get("value", ""), False) for v in url_obj.get("variable", []) if v.get("key")
        ]

    body_mode, body_block = _body_blocks(req.get("body", {}))

    blocks: list[str] = []
    blocks.append(_text_block("meta", f"name: {item.get('name', 'Request')}\ntype: http\nseq: {seq}"))

    verb_lines = [f"{INDENT}url: {url}", f"{INDENT}body: {body_mode}", f"{INDENT}auth: inherit"]
    blocks.append(f"{method} {{\n" + "\n".join(verb_lines) + "\n}")

    if path_pairs:
        blocks.append(_dict_block("params:path", path_pairs))
    if query_pairs:
        blocks.append(_dict_block("params:query", query_pairs))

    header_pairs = [
        (h.get("key", ""), h.get("value", ""), bool(h.get("disabled"))) for h in req.get("header", []) if h.get("key")
    ]
    if header_pairs:
        blocks.append(_dict_block("headers", header_pairs))

    if body_block:
        blocks.append(body_block)

    return "\n\n".join(blocks) + "\n"


def serialize_tree(items: list[dict[str, Any]], dir_path: Path, collection_vars: dict[str, str]) -> int:
    """Recursively write folders (dirs + folder.bru) and requests (.bru). Returns request count."""
    dir_path.mkdir(parents=True, exist_ok=True)
    used: set[str] = set()
    count = 0
    for seq, item in enumerate(items, start=1):
        name = item.get("name", "item")
        if "item" in item:
            folder_dir = dir_path / _safe_name(name, used)
            folder_dir.mkdir(parents=True, exist_ok=True)
            meta = _text_block("meta", f"name: {name}\nseq: {seq}")
            (folder_dir / "folder.bru").write_text(meta + "\n", encoding="utf-8")
            count += serialize_tree(item["item"], folder_dir, collection_vars)
        elif "request" in item:
            filename = _safe_name(name, used) + ".bru"
            (dir_path / filename).write_text(serialize_request(item, seq, collection_vars), encoding="utf-8")
            count += 1
    return count


# ---------------------------------------------------------------------------
# Collection manifest, collection.bru, environments
# ---------------------------------------------------------------------------


def write_bruno_json(out_dir: Path, name: str) -> None:
    """Write the bruno.json collection manifest."""
    manifest = {"version": "1", "name": name, "type": "collection", "ignore": ["node_modules", ".git"]}
    (out_dir / "bruno.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_collection_bru(out_dir: Path, auth: dict[str, Any] | None, cascade_script: str | None) -> None:
    """Write collection.bru with collection-level auth and the optional cascade pre-request script."""
    mode, detail = _postman_auth_to_bruno(auth)
    blocks = [_text_block("meta", "type: collection"), _dict_block("auth", [("mode", mode, False)])]
    if detail:
        blocks.append(detail)
    if cascade_script:
        blocks.append(_text_block("script:pre-request", cascade_script))
    (out_dir / "collection.bru").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")


def write_environment(env_dir: Path, env_name: str, values: list[tuple[str, str, bool]]) -> Path:
    """Write an environments/<Name>.bru file. Each value is (key, value, is_secret)."""
    env_dir.mkdir(parents=True, exist_ok=True)
    plain = [(k, v, False) for k, v, secret in values if not secret]
    secrets = [k for k, _v, secret in values if secret]
    blocks = [_dict_block("vars", plain)]
    secret_block = _secret_list_block(secrets)
    if secret_block:
        blocks.append(secret_block)
    path = env_dir / f"{env_name}.bru"
    path.write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    return path


def _environment_values(
    base_url: str | None,
    base_url_var: str,
    auth_vars: dict[str, str],
    param_vars: dict[str, str],
    defaults: dict[str, str],
) -> list[tuple[str, str, bool]]:
    """Build the (key, value, is_secret) list for one environment."""
    values: list[tuple[str, str, bool]] = []
    if base_url:
        values.append((base_url_var, base_url, False))
    for var_name, auth_default in sorted(auth_vars.items()):
        val = defaults.get(var_name, auth_default)
        values.append((var_name, val, _is_secret_var(var_name)))
    for _param, env_var in sorted(param_vars.items(), key=lambda x: x[1]):
        values.append((env_var, defaults.get(env_var, ""), False))
    return values


# ---------------------------------------------------------------------------
# OpenCollection YAML serialisation (Bruno 3.1+ default format)
# ---------------------------------------------------------------------------


class _YamlDumper(yaml.SafeDumper):
    """Dumper that renders multi-line strings as literal block scalars (``|-``)."""


def _represent_str(dumper: yaml.SafeDumper, data: str) -> yaml.ScalarNode:
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_YamlDumper.add_representer(str, _represent_str)


def _yaml_dump(obj: dict[str, Any]) -> str:
    """Serialise a mapping to OpenCollection-style YAML (key order preserved)."""
    return yaml.dump(obj, Dumper=_YamlDumper, sort_keys=False, default_flow_style=False, allow_unicode=True, width=4096)


def _auth_to_yaml(auth: dict[str, Any] | None) -> dict[str, Any] | None:
    """Map a Postman collection auth object to an OpenCollection ``auth`` mapping."""
    if not auth:
        return None
    auth_type = auth.get("type", "none")

    if auth_type == "oauth2":
        o = {entry["key"]: entry.get("value", "") for entry in auth.get("oauth2", [])}
        placement = "basic_auth_header" if o.get("client_authentication") == "header" else "body"
        node: dict[str, Any] = {
            "type": "oauth2",
            "flow": "authorization_code",
            "authorizationUrl": o.get("authUrl", ""),
            "accessTokenUrl": o.get("accessTokenUrl", ""),
            "callbackUrl": o.get("redirect_uri", ""),
            "credentials": {
                "clientId": o.get("clientId", ""),
                "clientSecret": o.get("clientSecret", ""),
                "placement": placement,
            },
            "scope": o.get("scope", ""),
            "pkce": {},
            "tokenConfig": {"placement": {"header": "Bearer"}, "source": "access_token"},
            "settings": {"autoFetchToken": False, "autoRefreshToken": False},
        }
        return node

    if auth_type == "bearer":
        b = {entry["key"]: entry.get("value", "") for entry in auth.get("bearer", [])}
        return {"type": "bearer", "token": b.get("token", "")}

    if auth_type == "apikey":
        a = {entry["key"]: entry.get("value", "") for entry in auth.get("apikey", [])}
        return {
            "type": "apikey",
            "key": a.get("key", ""),
            "value": a.get("value", ""),
            "placement": "query" if a.get("in") == "query" else "header",
        }

    if auth_type == "basic":
        c = {entry["key"]: entry.get("value", "") for entry in auth.get("basic", [])}
        return {"type": "basic", "username": c.get("username", ""), "password": c.get("password", "")}

    return None


def _body_to_yaml(body: dict[str, Any]) -> dict[str, Any] | None:
    """Map a Postman request body to an OpenCollection ``body`` mapping."""
    mode = body.get("mode")
    if mode == "raw":
        raw = body.get("raw", "")
        language = body.get("options", {}).get("raw", {}).get("language", "")
        body_type = "json" if language == "json" or raw.strip().startswith(("{", "[")) else "text"
        return {"type": body_type, "data": raw.rstrip("\n")}
    if mode == "urlencoded":
        data: list[dict[str, Any]] = []
        for p in body.get("urlencoded", []):
            entry: dict[str, Any] = {"name": p.get("key", ""), "value": p.get("value", "")}
            if p.get("disabled"):
                entry["disabled"] = True
            data.append(entry)
        return {"type": "form-urlencoded", "data": data}
    return None


def serialize_request_yaml(item: dict[str, Any], seq: int, collection_vars: dict[str, str]) -> str:
    """Serialise a Postman request item to an OpenCollection ``<Name>.yml`` document."""
    req = item.get("request", {})
    method = str(req.get("method", "GET")).upper()
    url_obj = req.get("url", {})

    http: dict[str, Any] = {"method": method, "url": _request_url(req, collection_vars)}

    params: list[dict[str, Any]] = []
    if isinstance(url_obj, dict):
        for q in url_obj.get("query", []):
            entry: dict[str, Any] = {"name": q.get("key", ""), "value": q.get("value", ""), "type": "query"}
            if q.get("disabled"):
                entry["disabled"] = True
            params.append(entry)
        for v in url_obj.get("variable", []):
            if v.get("key"):
                params.append({"name": v["key"], "value": v.get("value", ""), "type": "path"})
    if params:
        http["params"] = params

    headers = [
        {"name": h.get("key", ""), "value": h.get("value", ""), **({"disabled": True} if h.get("disabled") else {})}
        for h in req.get("header", [])
        if h.get("key")
    ]
    if headers:
        http["headers"] = headers

    body = _body_to_yaml(req.get("body", {}))
    if body:
        http["body"] = body

    http["auth"] = "inherit"

    doc = {
        "info": {"name": item.get("name", "Request"), "type": "http", "seq": seq},
        "http": http,
        "settings": {"encodeUrl": True, "timeout": 0, "followRedirects": True, "maxRedirects": 5},
    }
    return _yaml_dump(doc)


def serialize_tree_yaml(items: list[dict[str, Any]], dir_path: Path, collection_vars: dict[str, str]) -> int:
    """Recursively write folders (dirs + folder.yml) and requests (.yml). Returns request count."""
    dir_path.mkdir(parents=True, exist_ok=True)
    used: set[str] = set()
    count = 0
    for seq, item in enumerate(items, start=1):
        name = item.get("name", "item")
        if "item" in item:
            folder_dir = dir_path / _safe_name(name, used)
            folder_dir.mkdir(parents=True, exist_ok=True)
            folder_doc = {"info": {"name": name, "type": "folder", "seq": seq}}
            (folder_dir / "folder.yml").write_text(_yaml_dump(folder_doc), encoding="utf-8")
            count += serialize_tree_yaml(item["item"], folder_dir, collection_vars)
        elif "request" in item:
            filename = _safe_name(name, used) + ".yml"
            (dir_path / filename).write_text(serialize_request_yaml(item, seq, collection_vars), encoding="utf-8")
            count += 1
    return count


def write_opencollection_yml(out_dir: Path, name: str, auth: dict[str, Any] | None, cascade_script: str | None) -> None:
    """Write the opencollection.yml manifest with collection-level auth and pre-request script."""
    manifest: dict[str, Any] = {"opencollection": "1.0.0", "info": {"name": name}}
    request: dict[str, Any] = {}
    auth_node = _auth_to_yaml(auth)
    if auth_node:
        request["auth"] = auth_node
    if cascade_script:
        request["scripts"] = [{"type": "before-request", "code": cascade_script}]
    if request:
        manifest["request"] = request
    manifest["bundled"] = False
    manifest["extensions"] = {"bruno": {"ignore": ["node_modules", ".git"]}}
    (out_dir / "opencollection.yml").write_text(_yaml_dump(manifest), encoding="utf-8")


def write_environment_yaml(env_dir: Path, env_name: str, values: list[tuple[str, str, bool]]) -> Path:
    """Write an environments/<Name>.yml file. Secrets are name-only (no value on disk)."""
    env_dir.mkdir(parents=True, exist_ok=True)
    variables: list[dict[str, Any]] = []
    for key, value, secret in values:
        variables.append({"name": key, "secret": True} if secret else {"name": key, "value": value})
    path = env_dir / f"{env_name}.yml"
    path.write_text(_yaml_dump({"name": env_name, "variables": variables}), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Conversion orchestration
# ---------------------------------------------------------------------------


@dataclass
class BrunoConversionRequest:
    """Options driving an OpenAPI -> Bruno conversion (mirrors the CLI options)."""

    spec: str
    output: str | None = None
    output_format: str = "yaml"
    name: str | None = None
    env_name: str | None = None
    min_occurrences: int = 2
    env_prefix: str = ""
    auth_type: str = "auto"
    oidc_url: str | None = None
    login_endpoint: str | None = None
    login_token_field: str = "session_id"
    api_key_scheme: str = "Api-Key"
    extra_base_url: list[str] | None = None
    env_default: list[str] | None = None
    env_var: list[str] | None = None
    system_browser: bool = True
    register: bool = True
    workspace: str | None = None


def convert_openapi_to_bruno(req: BrunoConversionRequest) -> dict[str, Any]:
    """Convert an OpenAPI spec to a Bruno collection directory. Returns the result dict.

    Reuses the ``to_postman`` post-processing pipeline as an in-memory intermediate
    representation, then serialises to the chosen on-disk Bruno format. Progress is
    logged to stderr; the CLI command only parses options and delegates here.
    """
    extra_base_url_list = req.extra_base_url or []
    env_default_list = req.env_default or []
    env_var_list = req.env_var or []
    fmt = req.output_format.lower()
    if fmt not in ("yaml", "bru"):
        print(f"ERROR: --format must be 'yaml' or 'bru', got '{req.output_format}'", file=sys.stderr)
        raise typer.Exit(code=2)

    spec_path = resolve_spec(req.spec)
    spec_name = Path(spec_path).stem.replace(".openapi", "").replace(".swagger", "")

    out_dir = Path(req.output or spec_name)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Convert via openapi2postmanv2 into a temp Postman collection, then serialise to Bruno.
    postman_json = out_dir / ".openapi.postman_collection.json"
    cli_path = ensure_cli()
    convert(cli_path, spec_path, str(postman_json))

    metadata = extract_spec_metadata(spec_path)
    base_url = metadata.base_url

    raw = postman_json.read_text(encoding="utf-8")
    prefix = req.env_prefix.upper().rstrip("_") if req.env_prefix else ""
    base_url_var = f"{prefix}_BASE_URL" if prefix else "BASE_URL"
    if base_url:
        raw = replace_base_url(raw, base_url, base_url_var)
        print(f"  Base URL '{base_url}' -> {{{{{base_url_var}}}}}", file=sys.stderr)

    collection = json.loads(raw)
    collection_vars = {v.get("key", ""): v.get("value", "") for v in collection.get("variable", []) if v.get("key")}

    resolved_auth_type, auth_vars = apply_collection_auth(collection, metadata.auth_schemes, prefix, req.auth_type)
    if auth_vars:
        stripped = strip_request_auth(collection.get("item", []))
        if stripped:
            print(f"  Stripped per-request auth from {stripped} requests (inherit collection auth)", file=sys.stderr)

    cascade_script: str | None = None
    if req.login_endpoint:
        cascade_script = build_bruno_cascade_script(
            prefix, req.login_endpoint, req.login_token_field, req.api_key_scheme
        )
        for key in ("AUTH_API_KEY", "AUTH_EMAIL", "AUTH_PASSWORD", "AUTH_BEARER_TOKEN", "AUTH_EXPIRES_AT"):
            auth_vars[_prefixed(prefix, key)] = ""
        print(f"  Auth cascade: API key > {req.login_endpoint} login > OAuth2", file=sys.stderr)

    param_counts = collect_path_params(collection.get("item", []))
    frequent_params = {p: to_env_var_name(p, prefix) for p, c in param_counts.items() if c >= req.min_occurrences}
    if frequent_params:
        replaced = patch_path_variables(collection.get("item", []), frequent_params)
        print(f"  Replaced {replaced} path parameter values with env vars", file=sys.stderr)

    collection_name = req.name or collection.get("info", {}).get("name", spec_name)

    # Write the Bruno collection files in the chosen on-disk format.
    if fmt == "yaml":
        write_opencollection_yml(out_dir, collection_name, collection.get("auth"), cascade_script)
        request_count = serialize_tree_yaml(collection.get("item", []), out_dir, collection_vars)
    else:
        write_bruno_json(out_dir, collection_name)
        write_collection_bru(out_dir, collection.get("auth"), cascade_script)
        request_count = serialize_tree(collection.get("item", []), out_dir, collection_vars)

    env_defaults: dict[str, str] = {}
    for default in env_default_list:
        if "=" not in default:
            print(f"WARNING: ignoring --env-default '{default}' (expected VAR=VALUE)", file=sys.stderr)
            continue
        var, val = default.split("=", 1)
        env_defaults[var] = val

    # Per-environment overrides ("ENV:VAR=VALUE"), e.g. a prod tenant's OAuth2 client.
    env_overrides: dict[str, dict[str, str]] = {}
    for override in env_var_list:
        if ":" not in override or "=" not in override.split(":", 1)[1]:
            print(f"WARNING: ignoring --env-var '{override}' (expected ENV:VAR=VALUE)", file=sys.stderr)
            continue
        env_label, assignment = override.split(":", 1)
        var, val = assignment.split("=", 1)
        env_overrides.setdefault(env_label, {})[var] = val

    is_oauth2 = resolved_auth_type == "oauth2"
    callback_var = _prefixed(prefix, "AUTH_CALLBACK_URL")
    spec_oidc_url = _find_oidc_url(metadata.auth_schemes) if is_oauth2 else ""
    primary_oidc_url = req.oidc_url or spec_oidc_url
    primary_auth_defaults = resolve_oauth2_env_vars(prefix, primary_oidc_url) if is_oauth2 else dict(auth_vars)
    # With --system-browser the IdP redirects to Bruno's bruno:// deep link; otherwise
    # Bruno's built-in browser intercepts the localhost redirect (no local server).
    callback_default = SYSTEM_BROWSER_CALLBACK_URL if req.system_browser else BRUNO_CALLBACK_URL
    if is_oauth2:
        primary_auth_defaults[callback_var] = callback_default
    resolved_env_name = req.env_name or collection_name
    primary_defaults = {**primary_auth_defaults, **env_defaults, **env_overrides.get(resolved_env_name, {})}

    env_dir = out_dir / "environments"
    env_paths: list[str] = []

    def _write_env(env_label: str, env_values: list[tuple[str, str, bool]]) -> Path:
        if fmt == "yaml":
            return write_environment_yaml(env_dir, env_label, env_values)
        return write_environment(env_dir, env_label, env_values)

    primary_values = _environment_values(base_url, base_url_var, auth_vars, frequent_params, primary_defaults)
    env_paths.append(str(_write_env(resolved_env_name, primary_values)))

    for extra in extra_base_url_list:
        if "=" not in extra:
            print(f"WARNING: ignoring --extra-base-url '{extra}' (expected NAME=URL)", file=sys.stderr)
            continue
        extra_name, extra_rest = extra.split("=", 1)
        extra_oidc_url = ""
        if ",oidc=" in extra_rest:
            extra_url, extra_oidc_url = extra_rest.rsplit(",oidc=", 1)
        else:
            extra_url = extra_rest
        if is_oauth2 and extra_oidc_url:
            extra_auth_defaults = resolve_oauth2_env_vars(prefix, extra_oidc_url)
            extra_auth_defaults[callback_var] = callback_default
        elif is_oauth2:
            extra_auth_defaults = primary_auth_defaults
        else:
            extra_auth_defaults = dict(auth_vars)
        extra_defaults = {**extra_auth_defaults, **env_defaults, **env_overrides.get(extra_name, {})}
        extra_values = _environment_values(extra_url, base_url_var, auth_vars, frequent_params, extra_defaults)
        env_paths.append(str(_write_env(extra_name, extra_values)))

    postman_json.unlink(missing_ok=True)

    registered_workspace: str | None = None
    system_browser_set = False
    config_dir = bruno_config_dir()
    if config_dir is None:
        if req.register or req.workspace:
            print("  Bruno not found — skipping app integration (files still written)", file=sys.stderr)
    else:
        system_browser_set = set_system_browser(config_dir, req.system_browser)
        if system_browser_set:
            print(
                f"  Bruno preference: OAuth2 via system browser {'enabled' if req.system_browser else 'disabled'}",
                file=sys.stderr,
            )
        if req.register:
            ws = Path(req.workspace) if req.workspace else active_workspace_path(config_dir)
            if ws is None:
                print("  No active Bruno workspace found — skipping registration", file=sys.stderr)
            else:
                try:
                    added = register_collection_in_workspace(ws, collection_name, out_dir)
                except FileNotFoundError as exc:
                    print(f"  {exc}", file=sys.stderr)
                else:
                    registered_workspace = str(ws)
                    print(f"  {'Registered' if added else 'Already in'} Bruno workspace: {ws}", file=sys.stderr)

    folder_count = sum(1 for item in collection.get("item", []) if "item" in item)
    print(f"\nCollection: {collection_name}", file=sys.stderr)
    print(f"Folders:    {folder_count}", file=sys.stderr)
    print(f"Requests:   {request_count}", file=sys.stderr)
    print(f"Output:     {out_dir}/", file=sys.stderr)
    for ep in env_paths:
        print(f"Environment: {ep}", file=sys.stderr)

    return {
        "collection_dir": str(out_dir),
        "environments": env_paths,
        "stats": {"name": collection_name, "folders": folder_count, "requests": request_count},
        "registered_workspace": registered_workspace,
        "system_browser": system_browser_set,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

cli = typer.Typer()


@cli.command()
def main(
    spec: Annotated[str, typer.Argument(help="OpenAPI spec file path or URL")],
    output: Annotated[str | None, typer.Option("--output", "-o", help="Output Bruno collection directory")] = None,
    output_format: Annotated[
        str,
        typer.Option("--format", help="On-disk format: yaml (OpenCollection, Bruno 3.1+ default) or bru (legacy DSL)"),
    ] = "yaml",
    name: Annotated[
        str | None, typer.Option("--name", help="Collection name (default: derived from spec title)")
    ] = None,
    env_name: Annotated[str | None, typer.Option("--env-name", help="Name for the primary Bruno environment")] = None,
    min_occurrences: Annotated[
        int,
        typer.Option("--min-occurrences", help="Minimum occurrences for a path param to become an env var"),
    ] = 2,
    env_prefix: Annotated[
        str, typer.Option("--env-prefix", help="Prefix for environment variable names (e.g. 'PYSAE')")
    ] = "",
    auth_type: Annotated[
        str,
        typer.Option("--auth-type", help="Collection auth: auto, oauth2, bearer, apikey, basic, none"),
    ] = "auto",
    oidc_url: Annotated[
        str | None, typer.Option("--oidc-url", help="Override the OIDC discovery URL for the primary environment")
    ] = None,
    login_endpoint: Annotated[
        str | None, typer.Option("--login-endpoint", help="Add auto-login cascade script (e.g. '/api/v4/login')")
    ] = None,
    login_token_field: Annotated[
        str, typer.Option("--login-token-field", help="JSON field in the login response holding the token")
    ] = "session_id",
    api_key_scheme: Annotated[
        str, typer.Option("--api-key-scheme", help="Authorization scheme prefix for the API-key cascade level")
    ] = "Api-Key",
    extra_base_url: Annotated[
        list[str] | None,
        typer.Option("--extra-base-url", metavar="NAME=URL", help="Generate additional environments"),
    ] = None,
    env_default: Annotated[
        list[str] | None,
        typer.Option("--env-default", metavar="VAR=VALUE", help="Set default values for environment variables"),
    ] = None,
    env_var: Annotated[
        list[str] | None,
        typer.Option(
            "--env-var",
            metavar="ENV:VAR=VALUE",
            help="Set a variable for one environment only (e.g. a prod tenant's OAuth2 client); repeatable",
        ),
    ] = None,
    system_browser: Annotated[
        bool,
        typer.Option(
            "--system-browser/--no-system-browser",
            help="OAuth2 via the system browser (default): bruno:// deep-link callback + useSystemBrowser pref. "
            "--no-system-browser uses the built-in browser with a localhost callback.",
        ),
    ] = True,
    register: Annotated[
        bool,
        typer.Option(
            "--register/--no-register",
            help="Register the collection in Bruno's active workspace so it shows up in the sidebar (default). "
            "--no-register only writes the files.",
        ),
    ] = True,
    workspace: Annotated[
        str | None,
        typer.Option("--workspace", help="Workspace directory to register into (default: Bruno's active workspace)"),
    ] = None,
) -> None:
    """Convert an OpenAPI spec to a Bruno collection (directory of .bru files)."""
    result = convert_openapi_to_bruno(
        BrunoConversionRequest(
            spec=spec,
            output=output,
            output_format=output_format,
            name=name,
            env_name=env_name,
            min_occurrences=min_occurrences,
            env_prefix=env_prefix,
            auth_type=auth_type,
            oidc_url=oidc_url,
            login_endpoint=login_endpoint,
            login_token_field=login_token_field,
            api_key_scheme=api_key_scheme,
            extra_base_url=extra_base_url,
            env_default=env_default,
            env_var=env_var,
            system_browser=system_browser,
            register=register,
            workspace=workspace,
        )
    )
    print(json.dumps(result))


if __name__ == "__main__":
    cli()
