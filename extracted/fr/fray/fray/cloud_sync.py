"""
Fray Cloud Sync — Hybrid GitHub + Cloudflare R2/D1 payload database sync.

Architecture:
    GitHub repo = source of truth (PRs, reviews, releases)
    Cloudflare R2 = CDN for fast payload bundle downloads (S3-compatible)
    Cloudflare D1 = shared learned patterns / test results (optional opt-in)
    GitHub Releases = fallback when R2 is not configured

Usage:
    fray update                        # Pull latest payload DB
    fray update --source github        # Force GitHub source
    fray update --source r2            # Force R2 source
    fray sync --push                   # Push local DB to cloud (maintainer)
    fray sync --pull                   # Pull latest from cloud
    fray sync --share-patterns         # Opt-in: share learned patterns to D1

Config (~/.fray/cloud.json):
    {
      "r2_endpoint": "https://YOUR_ACCOUNT.r2.cloudflarestorage.com",
      "r2_bucket": "fray-payloads",
      "r2_access_key": "...",
      "r2_secret_key": "...",
      "d1_api_url": "https://api.cloudflare.com/client/v4/accounts/ACCT/d1/database/DB_ID",
      "d1_api_token": "...",
      "github_repo": "dalisecurity/fray",
      "share_patterns": false
    }
"""

import hashlib
import io
import json
import os
import ssl
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def _r2_ssl_context():
    """SSL context for R2 — handles macOS Python cert issues.

    R2's S3-compatible endpoint triggers 'key usage extension' errors on some
    macOS Python builds.  Requests are already authenticated via AWS Sig V4
    HMAC, so we try verified first, then fall back to unverified TLS.
    """
    for _attempt in ("verified", "unverified"):
        try:
            if _attempt == "verified":
                ctx = ssl.create_default_context()
                # Quick probe to check if the context works
                import socket as _sock
                with ctx.wrap_socket(_sock.socket(), server_hostname="r2.cloudflarestorage.com") as _s:
                    _s.settimeout(3)
                    _s.connect(("r2.cloudflarestorage.com", 443))
                return ctx
            else:
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                return ctx
        except Exception:
            continue
    # Last resort
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

from fray import __version__, PAYLOADS_DIR

# ── Config ────────────────────────────────────────────────────────────────────

_FRAY_DIR = Path.home() / ".fray"
_CONFIG_PATH = _FRAY_DIR / "cloud.json"
_DEFAULT_GITHUB_REPO = "dalisecurity/fray"
_BUNDLE_NAME = "fray-payloads.tar.gz"
_MANIFEST_NAME = "manifest.json"


@dataclass
class CloudConfig:
    """Cloud sync configuration."""
    # R2 (S3-compatible)
    r2_endpoint: str = ""
    r2_bucket: str = "fray-payloads"
    r2_access_key: str = ""
    r2_secret_key: str = ""
    # D1
    d1_api_url: str = ""
    d1_api_token: str = ""
    # GitHub
    github_repo: str = _DEFAULT_GITHUB_REPO
    github_token: str = ""
    # Preferences
    share_patterns: bool = False
    preferred_source: str = "auto"  # auto, r2, github


def load_config() -> CloudConfig:
    """Load cloud config from ~/.fray/cloud.json and env vars."""
    cfg = CloudConfig()

    # File config
    if _CONFIG_PATH.exists():
        try:
            data = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
            for key in vars(cfg):
                if key in data:
                    setattr(cfg, key, data[key])
        except (json.JSONDecodeError, OSError):
            pass

    # Env overrides (higher priority)
    env_map = {
        "FRAY_R2_ENDPOINT": "r2_endpoint",
        "FRAY_R2_BUCKET": "r2_bucket",
        "FRAY_R2_ACCESS_KEY": "r2_access_key",
        "FRAY_R2_SECRET_KEY": "r2_secret_key",
        "FRAY_D1_API_URL": "d1_api_url",
        "FRAY_D1_API_TOKEN": "d1_api_token",
        "FRAY_GITHUB_REPO": "github_repo",
        "GITHUB_TOKEN": "github_token",
        "FRAY_SHARE_PATTERNS": "share_patterns",
    }
    for env_key, attr in env_map.items():
        val = os.environ.get(env_key)
        if val:
            if attr == "share_patterns":
                setattr(cfg, attr, val.lower() in ("1", "true", "yes"))
            else:
                setattr(cfg, attr, val)

    return cfg


def save_config(cfg: CloudConfig) -> None:
    """Save config to ~/.fray/cloud.json."""
    _FRAY_DIR.mkdir(parents=True, exist_ok=True)
    data = {k: v for k, v in vars(cfg).items() if v and k != "github_token"}
    _CONFIG_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ── ANSI colors ──────────────────────────────────────────────────────────────

class _C:
    B = "\033[1m"
    G = "\033[32m"
    R = "\033[31m"
    Y = "\033[33m"
    BL = "\033[94m"
    CY = "\033[36m"
    DIM = "\033[2m"
    E = "\033[0m"


# ── HTTP helpers ─────────────────────────────────────────────────────────────

def _http_get(url: str, headers: Optional[Dict] = None,
              timeout: int = 30) -> Optional[bytes]:
    """HTTP GET returning raw bytes."""
    import ssl
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", f"Fray/{__version__} CloudSync")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    for ctx in (None, ssl.create_default_context()):
        try:
            if ctx is None:
                resp = urllib.request.urlopen(req, timeout=timeout)
            else:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
            return resp.read()
        except ssl.SSLError:
            continue
        except (urllib.error.URLError, urllib.error.HTTPError, OSError):
            if ctx is None:
                continue
            return None
        except Exception:
            return None
    return None


def _http_get_json(url: str, headers: Optional[Dict] = None,
                   timeout: int = 30) -> Optional[Dict]:
    data = _http_get(url, headers, timeout)
    if data:
        try:
            return json.loads(data.decode("utf-8", errors="replace"))
        except json.JSONDecodeError:
            pass
    return None


# ── Payload bundle builder ───────────────────────────────────────────────────

def build_payload_bundle() -> Tuple[bytes, Dict]:
    """Build a tar.gz bundle of all payloads + manifest."""
    payloads_root = Path(__file__).parent.parent / "payloads"
    if not payloads_root.exists():
        payloads_root = PAYLOADS_DIR

    manifest = {
        "version": __version__,
        "created": datetime.now(timezone.utc).isoformat(),
        "categories": {},
        "total_payloads": 0,
        "total_files": 0,
    }

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for json_file in sorted(payloads_root.rglob("*.json")):
            rel = json_file.relative_to(payloads_root)
            cat = rel.parts[0] if len(rel.parts) > 1 else "root"

            content = json_file.read_bytes()
            try:
                data = json.loads(content)
                count = data.get("count", len(data.get("payloads", [])))
            except json.JSONDecodeError:
                count = 0

            manifest["categories"][cat] = (
                manifest["categories"].get(cat, 0) + count
            )
            manifest["total_payloads"] += count
            manifest["total_files"] += 1

            info = tarfile.TarInfo(name=str(rel))
            info.size = len(content)
            info.mtime = int(json_file.stat().st_mtime)
            tar.addfile(info, io.BytesIO(content))

        # Add manifest
        manifest_bytes = json.dumps(manifest, indent=2).encode("utf-8")
        info = tarfile.TarInfo(name=_MANIFEST_NAME)
        info.size = len(manifest_bytes)
        info.mtime = int(time.time())
        tar.addfile(info, io.BytesIO(manifest_bytes))

    bundle = buf.getvalue()
    manifest["bundle_size"] = len(bundle)
    manifest["bundle_sha256"] = hashlib.sha256(bundle).hexdigest()
    return bundle, manifest


def extract_payload_bundle(bundle_bytes: bytes, target_dir: Path) -> Dict:
    """Extract a payload bundle to target directory. Returns manifest."""
    target_dir.mkdir(parents=True, exist_ok=True)
    manifest = {}

    with tarfile.open(fileobj=io.BytesIO(bundle_bytes), mode="r:gz") as tar:
        # Security: prevent path traversal
        for member in tar.getmembers():
            if member.name.startswith("/") or ".." in member.name:
                continue
            if member.name == _MANIFEST_NAME:
                f = tar.extractfile(member)
                if f:
                    manifest = json.loads(f.read().decode("utf-8"))
                continue
            # Extract payload file
            dest = target_dir / member.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            f = tar.extractfile(member)
            if f:
                dest.write_bytes(f.read())

    return manifest


# ══════════════════════════════════════════════════════════════════════════════
#  GITHUB BACKEND
# ══════════════════════════════════════════════════════════════════════════════

def github_get_latest_release(cfg: CloudConfig) -> Optional[Dict]:
    """Get latest GitHub release info."""
    url = f"https://api.github.com/repos/{cfg.github_repo}/releases/latest"
    headers = {"Accept": "application/vnd.github+json"}
    if cfg.github_token:
        headers["Authorization"] = f"token {cfg.github_token}"
    return _http_get_json(url, headers)


def github_download_bundle(cfg: CloudConfig, verbose: bool = True) -> Optional[Tuple[bytes, Dict]]:
    """Download payload bundle from latest GitHub release."""
    release = github_get_latest_release(cfg)
    if not release:
        if verbose:
            print(f"    {_C.R}No GitHub release found{_C.E}")
        return None

    tag = release.get("tag_name", "unknown")
    assets = release.get("assets", [])

    # Find the payload bundle asset
    bundle_asset = None
    manifest_asset = None
    for a in assets:
        name = a.get("name", "")
        if name == _BUNDLE_NAME:
            bundle_asset = a
        elif name == _MANIFEST_NAME:
            manifest_asset = a

    if not bundle_asset:
        if verbose:
            print(f"    {_C.R}Release {tag} has no payload bundle{_C.E}")
        return None

    if verbose:
        size_mb = bundle_asset.get("size", 0) / 1024 / 1024
        print(f"    {_C.DIM}Downloading {tag} ({size_mb:.1f} MB)...{_C.E}")

    headers = {"Accept": "application/octet-stream"}
    if cfg.github_token:
        headers["Authorization"] = f"token {cfg.github_token}"

    bundle = _http_get(bundle_asset["browser_download_url"], headers, timeout=120)
    if not bundle:
        if verbose:
            print(f"    {_C.R}Failed to download bundle{_C.E}")
        return None

    # Get manifest
    manifest = {}
    if manifest_asset:
        m_data = _http_get(manifest_asset["browser_download_url"],
                           {"Accept": "application/octet-stream"}, timeout=30)
        if m_data:
            try:
                manifest = json.loads(m_data.decode("utf-8"))
            except json.JSONDecodeError:
                pass

    manifest["release_tag"] = tag
    manifest["source"] = "github"
    return bundle, manifest


def github_upload_bundle(cfg: CloudConfig, bundle: bytes, manifest: Dict,
                         tag: str = "", verbose: bool = True) -> bool:
    """Create a GitHub release with the payload bundle (maintainer only)."""
    if not cfg.github_token:
        if verbose:
            print(f"    {_C.R}GITHUB_TOKEN required for upload{_C.E}")
        return False

    if not tag:
        tag = f"payloads-{datetime.now(timezone.utc).strftime('%Y%m%d')}"

    # Create release
    url = f"https://api.github.com/repos/{cfg.github_repo}/releases"
    release_data = json.dumps({
        "tag_name": tag,
        "name": f"Payload Database {tag}",
        "body": (f"Auto-published payload database bundle.\n\n"
                 f"- **Payloads:** {manifest.get('total_payloads', '?')}\n"
                 f"- **Categories:** {len(manifest.get('categories', {}))}\n"
                 f"- **Files:** {manifest.get('total_files', '?')}\n"
                 f"- **SHA256:** `{manifest.get('bundle_sha256', '?')}`"),
        "draft": False,
        "prerelease": False,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=release_data, method="POST")
    req.add_header("Authorization", f"token {cfg.github_token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib.request.urlopen(req, timeout=30)
        release = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        if verbose:
            print(f"    {_C.R}Failed to create release: {e}{_C.E}")
        return False

    upload_url = release.get("upload_url", "").split("{")[0]
    if not upload_url:
        return False

    # Upload bundle
    for name, content, content_type in [
        (_BUNDLE_NAME, bundle, "application/gzip"),
        (_MANIFEST_NAME, json.dumps(manifest, indent=2).encode("utf-8"), "application/json"),
    ]:
        asset_url = f"{upload_url}?name={name}"
        req = urllib.request.Request(asset_url, data=content, method="POST")
        req.add_header("Authorization", f"token {cfg.github_token}")
        req.add_header("Content-Type", content_type)
        try:
            urllib.request.urlopen(req, timeout=120)
            if verbose:
                print(f"    {_C.G}Uploaded {name}{_C.E}")
        except Exception as e:
            if verbose:
                print(f"    {_C.R}Failed to upload {name}: {e}{_C.E}")
            return False

    return True


# ══════════════════════════════════════════════════════════════════════════════
#  CLOUDFLARE R2 BACKEND (S3-compatible)
# ══════════════════════════════════════════════════════════════════════════════

def _r2_sign_request(cfg: CloudConfig, method: str, path: str,
                     content_hash: str = "") -> Dict[str, str]:
    """Generate AWS Signature V4 headers for R2 (simplified)."""
    import hmac
    now = datetime.now(timezone.utc)
    date_stamp = now.strftime("%Y%m%d")
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    region = "auto"
    service = "s3"

    if not content_hash:
        content_hash = hashlib.sha256(b"").hexdigest()

    # Parse endpoint for host
    endpoint = cfg.r2_endpoint.rstrip("/")
    host = endpoint.replace("https://", "").replace("http://", "")

    canonical_uri = f"/{cfg.r2_bucket}/{path}"
    canonical_querystring = ""
    canonical_headers = (
        f"host:{host}\n"
        f"x-amz-content-sha256:{content_hash}\n"
        f"x-amz-date:{amz_date}\n"
    )
    signed_headers = "host;x-amz-content-sha256;x-amz-date"

    canonical_request = (
        f"{method}\n{canonical_uri}\n{canonical_querystring}\n"
        f"{canonical_headers}\n{signed_headers}\n{content_hash}"
    )

    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = (
        f"AWS4-HMAC-SHA256\n{amz_date}\n{credential_scope}\n"
        f"{hashlib.sha256(canonical_request.encode()).hexdigest()}"
    )

    def _sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    signing_key = _sign(
        _sign(
            _sign(
                _sign(f"AWS4{cfg.r2_secret_key}".encode("utf-8"),
                      date_stamp),
                region),
            service),
        "aws4_request")

    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    authorization = (
        f"AWS4-HMAC-SHA256 Credential={cfg.r2_access_key}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    return {
        "Authorization": authorization,
        "x-amz-content-sha256": content_hash,
        "x-amz-date": amz_date,
        "Host": host,
    }


def r2_available(cfg: CloudConfig) -> bool:
    return bool(cfg.r2_endpoint and cfg.r2_bucket and cfg.r2_access_key and cfg.r2_secret_key)


def describe_r2_missing(cfg: CloudConfig) -> str:
    missing = []
    if not cfg.r2_endpoint:
        missing.append("FRAY_R2_ENDPOINT")
    if not cfg.r2_bucket:
        missing.append("FRAY_R2_BUCKET")
    if not cfg.r2_access_key:
        missing.append("FRAY_R2_ACCESS_KEY")
    if not cfg.r2_secret_key:
        missing.append("FRAY_R2_SECRET_KEY")
    if not missing:
        return ""
    return ", ".join(missing)


def r2_download_bundle(cfg: CloudConfig, verbose: bool = True) -> Optional[Tuple[bytes, Dict]]:
    """Download payload bundle from Cloudflare R2."""
    if not r2_available(cfg):
        return None

    endpoint = cfg.r2_endpoint.rstrip("/")

    # Get manifest first
    if verbose:
        print(f"    {_C.DIM}Checking R2 for latest bundle...{_C.E}")

    manifest_url = f"{endpoint}/{cfg.r2_bucket}/{_MANIFEST_NAME}"
    headers = _r2_sign_request(cfg, "GET", _MANIFEST_NAME)
    manifest_data = _http_get(manifest_url, headers, timeout=15)
    if not manifest_data:
        if verbose:
            print(f"    {_C.Y}R2: no manifest found{_C.E}")
        return None

    try:
        manifest = json.loads(manifest_data.decode("utf-8"))
    except json.JSONDecodeError:
        return None

    # Download bundle
    if verbose:
        size = manifest.get("bundle_size", 0) / 1024 / 1024
        print(f"    {_C.DIM}Downloading bundle ({size:.1f} MB)...{_C.E}")

    bundle_url = f"{endpoint}/{cfg.r2_bucket}/{_BUNDLE_NAME}"
    headers = _r2_sign_request(cfg, "GET", _BUNDLE_NAME)
    bundle = _http_get(bundle_url, headers, timeout=120)
    if not bundle:
        if verbose:
            print(f"    {_C.R}Failed to download from R2{_C.E}")
        return None

    # Verify hash
    actual_hash = hashlib.sha256(bundle).hexdigest()
    expected_hash = manifest.get("bundle_sha256", "")
    if expected_hash and actual_hash != expected_hash:
        if verbose:
            print(f"    {_C.R}Hash mismatch! Expected {expected_hash[:16]}... got {actual_hash[:16]}...{_C.E}")
        return None

    manifest["source"] = "r2"
    return bundle, manifest


def r2_upload_bundle(cfg: CloudConfig, bundle: bytes, manifest: Dict,
                     verbose: bool = True) -> bool:
    """Upload payload bundle to Cloudflare R2."""
    if not r2_available(cfg):
        if verbose:
            print(f"    {_C.R}R2 not configured{_C.E}")
        return False

    endpoint = cfg.r2_endpoint.rstrip("/")

    for name, content, ctype in [
        (_BUNDLE_NAME, bundle, "application/gzip"),
        (_MANIFEST_NAME, json.dumps(manifest, indent=2).encode("utf-8"), "application/json"),
    ]:
        content_hash = hashlib.sha256(content).hexdigest()
        headers = _r2_sign_request(cfg, "PUT", name, content_hash)
        headers["Content-Type"] = ctype

        url = f"{endpoint}/{cfg.r2_bucket}/{name}"
        req = urllib.request.Request(url, data=content, method="PUT")
        for k, v in headers.items():
            req.add_header(k, v)

        try:
            urllib.request.urlopen(req, timeout=120)
            if verbose:
                print(f"    {_C.G}Uploaded {name} to R2{_C.E}")
        except Exception as e:
            if verbose:
                print(f"    {_C.R}R2 upload failed for {name}: {e}{_C.E}")
            return False

    return True


# ══════════════════════════════════════════════════════════════════════════════
#  SHARE DOMAIN — Upload sanitized recon snapshot to R2
# ══════════════════════════════════════════════════════════════════════════════

# Fields stripped before sharing — never expose these publicly
_SENSITIVE_KEYS = {
    "origin_ips", "origin_ip", "direct_ips", "bypass_ips",
    "secrets", "secrets_found", "leaked_credentials",
    "admin_panels", "panels_found", "found",
    "cookies", "session_tokens",
    "api_keys", "tokens",
    "source_maps", "source_map_files",
    "jwt_tokens", "jwt_analysis",
    "cloud_buckets",
}

_SHARE_PREFIX = "shares/"
_SHARE_VIEWER_BASE = "https://dalisec.io/share"


def share_viewer_url(share_id: str) -> str:
    """Return the public viewer URL for a share ID."""
    base = _SHARE_VIEWER_BASE.rstrip('/')
    return f"{base}/?id={share_id}"


def sanitize_for_sharing(data: Dict) -> Dict:
    """Deep-strip sensitive fields from recon data before public sharing."""
    if not isinstance(data, dict):
        return data

    cleaned = {}
    for key, val in data.items():
        if key in _SENSITIVE_KEYS:
            continue
        if isinstance(val, dict):
            cleaned[key] = sanitize_for_sharing(val)
        elif isinstance(val, list):
            cleaned[key] = [
                sanitize_for_sharing(item) if isinstance(item, dict) else item
                for item in val
            ]
        else:
            cleaned[key] = val
    return cleaned


def share_domain(domain: str, expires_days: int = 30,
                 verbose: bool = True) -> Optional[str]:
    """Upload a sanitized domain snapshot to R2 and return the share URL.

    Returns the public share URL on success, None on failure.
    """
    cfg = load_config()
    if not r2_available(cfg):
        if verbose:
            print(f"  R2 not configured. Run: fray sync --configure")
        return None

    # Load domain data
    recon_file = _FRAY_DIR / "recon" / f"{domain}_latest.json"
    if not recon_file.exists():
        if verbose:
            print(f"  No recon data for {domain}")
        return None

    try:
        raw = json.loads(recon_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        if verbose:
            print(f"  Failed to read recon data: {e}")
        return None

    # Sanitize
    sanitized = sanitize_for_sharing(raw)

    # Generate share ID: 8-char hex from domain + timestamp
    share_id = hashlib.sha256(
        f"{domain}:{datetime.now(timezone.utc).isoformat()}".encode()
    ).hexdigest()[:12]

    # Add share metadata
    sanitized["_share"] = {
        "id": share_id,
        "domain": domain,
        "shared_at": datetime.now(timezone.utc).isoformat(),
        "expires_at": (
            datetime.now(timezone.utc) + timedelta(days=expires_days)
        ).isoformat(),
        "version": "1",
        "stripped_fields": sorted(_SENSITIVE_KEYS),
    }

    # Upload to R2
    content = json.dumps(sanitized, indent=2, default=str).encode("utf-8")
    content_hash = hashlib.sha256(content).hexdigest()
    r2_path = f"{_SHARE_PREFIX}{share_id}.json"

    endpoint = cfg.r2_endpoint.rstrip("/")
    headers = _r2_sign_request(cfg, "PUT", r2_path, content_hash)
    headers["Content-Type"] = "application/json"
    headers["Cache-Control"] = f"public, max-age={expires_days * 86400}"

    url = f"{endpoint}/{cfg.r2_bucket}/{r2_path}"
    req = urllib.request.Request(url, data=content, method="PUT")
    for k, v in headers.items():
        req.add_header(k, v)

    try:
        urllib.request.urlopen(req, timeout=30, context=_r2_ssl_context())
    except Exception as e:
        if verbose:
            print(f"  R2 upload failed: {e}")
        return None

    # Save share record locally
    shares_file = _FRAY_DIR / "shares.json"
    shares = {}
    if shares_file.exists():
        try:
            shares = json.loads(shares_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    share_url = share_viewer_url(share_id)
    shares[share_id] = {
        "domain": domain,
        "shared_at": sanitized["_share"]["shared_at"],
        "expires_at": sanitized["_share"]["expires_at"],
        "r2_path": r2_path,
        "url": share_url,
    }
    shares_file.write_text(json.dumps(shares, indent=2), encoding="utf-8")

    if verbose:
        print(f"  Shared: {share_url}")
        print(f"  Expires: {expires_days} days")
        print(f"  Stripped: origin IPs, secrets, admin panels, cookies, JWTs, buckets")

    return share_url


def extend_share(share_id: str, days: int,
                 verbose: bool = True) -> Optional[str]:
    """Extend an existing share's expiry and re-upload sanitized snapshot."""
    cfg = load_config()
    if not r2_available(cfg):
        if verbose:
            print("  R2 not configured. Run: fray sync --configure")
        return None

    shares_file = _FRAY_DIR / "shares.json"
    if not shares_file.exists():
        if verbose:
            print("  No shares.json found")
        return None

    try:
        shares = json.loads(shares_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        shares = {}

    info = shares.get(share_id)
    if not info:
        if verbose:
            print(f"  Share not found: {share_id}")
        return None

    domain = info.get("domain")
    if not domain:
        if verbose:
            print(f"  Share {share_id} missing domain metadata")
        return None

    recon_file = _FRAY_DIR / "recon" / f"{domain}_latest.json"
    if not recon_file.exists():
        if verbose:
            print(f"  No recon snapshot found for {domain}")
        return None

    try:
        raw = json.loads(recon_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        if verbose:
            print(f"  Failed to read recon data: {exc}")
        return None

    sanitized = sanitize_for_sharing(raw)
    new_expiry = datetime.now(timezone.utc) + timedelta(days=days)
    sanitized.setdefault("_share", {})
    sanitized["_share"].update({
        "id": share_id,
        "domain": domain,
        "shared_at": info.get("shared_at", datetime.now(timezone.utc).isoformat()),
        "expires_at": new_expiry.isoformat(),
        "version": info.get("version", sanitized["_share"].get("version", "1")),
        "stripped_fields": sanitized["_share"].get("stripped_fields", sorted(_SENSITIVE_KEYS)),
    })

    content = json.dumps(sanitized, indent=2, default=str).encode("utf-8")
    content_hash = hashlib.sha256(content).hexdigest()
    r2_path = f"{_SHARE_PREFIX}{share_id}.json"

    endpoint = cfg.r2_endpoint.rstrip("/")
    headers = _r2_sign_request(cfg, "PUT", r2_path, content_hash)
    headers["Content-Type"] = "application/json"
    headers["Cache-Control"] = f"public, max-age={days * 86400}"

    url = f"{endpoint}/{cfg.r2_bucket}/{r2_path}"
    req = urllib.request.Request(url, data=content, method="PUT")
    for k, v in headers.items():
        req.add_header(k, v)

    try:
        urllib.request.urlopen(req, timeout=30, context=_r2_ssl_context())
    except Exception as exc:
        if verbose:
            print(f"  R2 upload failed: {exc}")
        return None

    shares[share_id] = {
        "domain": domain,
        "shared_at": sanitized["_share"].get("shared_at"),
        "expires_at": sanitized["_share"].get("expires_at"),
        "r2_path": r2_path,
    }
    shares_file.write_text(json.dumps(shares, indent=2), encoding="utf-8")

    if verbose:
        print(f"  Extended share {share_id} — new expiry {sanitized['_share']['expires_at']}")

    return share_viewer_url(share_id)


def unshare_domain(share_id: str, verbose: bool = True) -> bool:
    """Delete a shared snapshot from R2."""
    cfg = load_config()
    if not r2_available(cfg):
        if verbose:
            print(f"  R2 not configured")
        return False

    r2_path = f"{_SHARE_PREFIX}{share_id}.json"
    endpoint = cfg.r2_endpoint.rstrip("/")
    headers = _r2_sign_request(cfg, "DELETE", r2_path)

    url = f"{endpoint}/{cfg.r2_bucket}/{r2_path}"
    req = urllib.request.Request(url, method="DELETE")
    for k, v in headers.items():
        req.add_header(k, v)

    try:
        urllib.request.urlopen(req, timeout=30)
    except Exception as e:
        if verbose:
            print(f"  R2 delete failed: {e}")
        return False

    # Remove from local record
    shares_file = _FRAY_DIR / "shares.json"
    if shares_file.exists():
        try:
            shares = json.loads(shares_file.read_text(encoding="utf-8"))
            shares.pop(share_id, None)
            shares_file.write_text(json.dumps(shares, indent=2), encoding="utf-8")
        except (json.JSONDecodeError, OSError):
            pass

    if verbose:
        print(f"  Unshared: {share_id}")
    return True


def list_shares() -> Dict:
    """List all active shares from local record."""
    shares_file = _FRAY_DIR / "shares.json"
    if not shares_file.exists():
        return {}
    try:
        return json.loads(shares_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


# ══════════════════════════════════════════════════════════════════════════════
#  CLOUDFLARE D1 — SHARED LEARNED PATTERNS (opt-in)
# ══════════════════════════════════════════════════════════════════════════════

def d1_available(cfg: CloudConfig) -> bool:
    return bool(cfg.d1_api_url and cfg.d1_api_token)


def d1_query(cfg: CloudConfig, sql: str, params: list = None) -> Optional[Dict]:
    """Execute a D1 SQL query via REST API."""
    if not d1_available(cfg):
        return None

    url = f"{cfg.d1_api_url}/query"
    body = json.dumps({"sql": sql, "params": params or []}).encode("utf-8")

    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {cfg.d1_api_token}")
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def d1_init_schema(cfg: CloudConfig) -> bool:
    """Initialize D1 tables if they don't exist."""
    schemas = [
        """CREATE TABLE IF NOT EXISTS waf_profiles (
            vendor TEXT PRIMARY KEY,
            blocked_tags TEXT,
            blocked_events TEXT,
            blocked_keywords TEXT,
            strictness TEXT,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS test_results (
            payload_hash TEXT,
            target_domain TEXT,
            category TEXT,
            cve TEXT,
            blocked INTEGER,
            status_code INTEGER,
            tested_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (payload_hash, target_domain)
        )""",
        """CREATE TABLE IF NOT EXISTS bypass_payloads (
            payload_hash TEXT PRIMARY KEY,
            payload TEXT,
            category TEXT,
            waf_vendor TEXT,
            technique TEXT,
            discovered_at TEXT DEFAULT CURRENT_TIMESTAMP,
            reporter TEXT DEFAULT 'anonymous'
        )""",
    ]
    for sql in schemas:
        result = d1_query(cfg, sql)
        if result is None:
            return False
    return True


def d1_share_test_results(cfg: CloudConfig, results: List[Dict],
                          target_domain: str) -> int:
    """Share test results to D1 (opt-in)."""
    if not cfg.share_patterns or not d1_available(cfg):
        return 0

    count = 0
    for r in results:
        # Compute hash from raw payload string if not already present
        payload_str = r.get("payload", "")
        ph = r.get("payload_hash") or (
            hashlib.sha256(payload_str.encode("utf-8", errors="replace")).hexdigest()[:16]
            if payload_str else ""
        )
        if not ph:
            continue  # Skip rows with no identifiable payload

        sql = """INSERT OR REPLACE INTO test_results
                 (payload_hash, target_domain, category, cve, blocked, status_code, bypass_confidence, tested_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        params = [
            ph,
            target_domain,
            r.get("category", ""),
            r.get("cve", ""),
            1 if r.get("blocked") else 0,
            r.get("status_code", r.get("status", 0)),
            int(r.get("bypass_confidence", 0)),
            datetime.now(timezone.utc).isoformat(),
        ]
        if d1_query(cfg, sql, params) is not None:
            count += 1
    return count


def d1_share_bypass(cfg: CloudConfig, payload: str, category: str,
                    waf_vendor: str, technique: str = "") -> bool:
    """Share a confirmed bypass to D1 (opt-in)."""
    if not cfg.share_patterns or not d1_available(cfg):
        return False

    payload_hash = hashlib.sha256(payload.encode()).hexdigest()[:16]
    sql = """INSERT OR REPLACE INTO bypass_payloads
             (payload_hash, payload, category, waf_vendor, technique, discovered_at)
             VALUES (?, ?, ?, ?, ?, ?)"""
    params = [payload_hash, payload[:500], category, waf_vendor, technique,
              datetime.now(timezone.utc).isoformat()]
    return d1_query(cfg, sql, params) is not None


def d1_leaderboard(cfg: CloudConfig, limit: int = 20,
                   verbose: bool = True) -> Dict:
    """#45 — Community leaderboard from D1 data.

    Queries bypass_payloads and test_results tables to build a leaderboard
    showing top contributors, WAF bypass rates, and most-bypassed WAFs.

    Returns dict with 'contributors', 'waf_stats', 'category_stats', 'total_bypasses'.
    """
    result = {
        "contributors": [],
        "waf_stats": [],
        "category_stats": [],
        "total_bypasses": 0,
        "total_tests": 0,
        "available": False,
    }

    if not d1_available(cfg):
        return result

    result["available"] = True

    # Top contributors by bypass count
    sql_contributors = """
        SELECT reporter, COUNT(*) as bypass_count,
               COUNT(DISTINCT waf_vendor) as wafs_bypassed,
               COUNT(DISTINCT category) as categories
        FROM bypass_payloads
        GROUP BY reporter
        ORDER BY bypass_count DESC
        LIMIT ?
    """
    resp = d1_query(cfg, sql_contributors, [limit])
    if resp and "result" in resp:
        rows = resp["result"]
        if isinstance(rows, list) and rows:
            result["contributors"] = rows[0].get("results", [])

    # WAF bypass stats
    sql_waf = """
        SELECT waf_vendor, COUNT(*) as bypass_count,
               COUNT(DISTINCT category) as categories,
               MAX(discovered_at) as latest
        FROM bypass_payloads
        WHERE waf_vendor != ''
        GROUP BY waf_vendor
        ORDER BY bypass_count DESC
        LIMIT ?
    """
    resp = d1_query(cfg, sql_waf, [limit])
    if resp and "result" in resp:
        rows = resp["result"]
        if isinstance(rows, list) and rows:
            result["waf_stats"] = rows[0].get("results", [])

    # Category stats
    sql_cat = """
        SELECT category, COUNT(*) as bypass_count,
               COUNT(DISTINCT waf_vendor) as wafs
        FROM bypass_payloads
        GROUP BY category
        ORDER BY bypass_count DESC
        LIMIT ?
    """
    resp = d1_query(cfg, sql_cat, [limit])
    if resp and "result" in resp:
        rows = resp["result"]
        if isinstance(rows, list) and rows:
            result["category_stats"] = rows[0].get("results", [])

    # Overall stats
    sql_total = "SELECT COUNT(*) as total FROM bypass_payloads"
    resp = d1_query(cfg, sql_total)
    if resp and "result" in resp:
        rows = resp["result"]
        if isinstance(rows, list) and rows:
            r = rows[0].get("results", [])
            if r:
                result["total_bypasses"] = r[0].get("total", 0)

    sql_tests = "SELECT COUNT(*) as total FROM test_results"
    resp = d1_query(cfg, sql_tests)
    if resp and "result" in resp:
        rows = resp["result"]
        if isinstance(rows, list) and rows:
            r = rows[0].get("results", [])
            if r:
                result["total_tests"] = r[0].get("total", 0)

    # Print formatted table
    if verbose:
        _C = type("C", (), {"B": "\033[1m", "G": "\033[32m", "Y": "\033[33m",
                             "BL": "\033[34m", "CY": "\033[36m", "DIM": "\033[2m",
                             "E": "\033[0m"})

        print(f"\n  {_C.B}Community Leaderboard{_C.E}")
        print(f"  {_C.DIM}Total bypasses: {result['total_bypasses']}  |  "
              f"Total tests: {result['total_tests']}{_C.E}\n")

        # Contributors table
        if result["contributors"]:
            print(f"  {_C.BL}Top Contributors{_C.E}")
            print(f"  {'Rank':<6}{'Contributor':<25}{'Bypasses':<12}{'WAFs':<10}{'Categories':<12}")
            print(f"  {'─'*65}")
            for i, c in enumerate(result["contributors"], 1):
                name = c.get("reporter", "anonymous")
                bypasses = c.get("bypass_count", 0)
                wafs = c.get("wafs_bypassed", 0)
                cats = c.get("categories", 0)
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f" {i}"
                print(f"  {medal:<6}{name:<25}{bypasses:<12}{wafs:<10}{cats:<12}")
            print()

        # WAF bypass stats table
        if result["waf_stats"]:
            print(f"  {_C.BL}Most Bypassed WAFs{_C.E}")
            print(f"  {'WAF':<25}{'Bypasses':<12}{'Categories':<12}{'Latest':<20}")
            print(f"  {'─'*65}")
            for w in result["waf_stats"]:
                vendor = w.get("waf_vendor", "unknown")
                bypasses = w.get("bypass_count", 0)
                cats = w.get("categories", 0)
                latest = (w.get("latest", "")[:10]) or "?"
                print(f"  {vendor:<25}{bypasses:<12}{cats:<12}{latest:<20}")
            print()

        # Category stats
        if result["category_stats"]:
            print(f"  {_C.BL}Bypass Categories{_C.E}")
            print(f"  {'Category':<20}{'Bypasses':<12}{'WAFs':<10}")
            print(f"  {'─'*42}")
            for c in result["category_stats"]:
                cat = c.get("category", "?")
                bypasses = c.get("bypass_count", 0)
                wafs = c.get("wafs", 0)
                print(f"  {cat:<20}{bypasses:<12}{wafs:<10}")
            print()

        if not result["contributors"] and not result["waf_stats"]:
            print(f"  {_C.DIM}No community data yet. Share your findings:{_C.E}")
            print(f"  {_C.DIM}  fray sync --configure  (enable pattern sharing){_C.E}")

    return result


def d1_get_community_bypasses(cfg: CloudConfig, waf_vendor: str = "",
                              category: str = "", limit: int = 50) -> List[Dict]:
    """Fetch community-shared bypass payloads from D1."""
    if not d1_available(cfg):
        return []

    conditions = []
    params = []
    if waf_vendor:
        conditions.append("waf_vendor = ?")
        params.append(waf_vendor)
    if category:
        conditions.append("category = ?")
        params.append(category)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"SELECT * FROM bypass_payloads {where} ORDER BY discovered_at DESC LIMIT ?"
    params.append(limit)

    result = d1_query(cfg, sql, params)
    if result and "result" in result:
        rows = result["result"]
        if isinstance(rows, list) and rows:
            return rows[0].get("results", [])
    return []


# ══════════════════════════════════════════════════════════════════════════════
#  HIGH-LEVEL COMMANDS
# ══════════════════════════════════════════════════════════════════════════════

def update_payloads(*, source: str = "auto",
                    verbose: bool = True) -> Optional[Dict]:
    """
    Pull latest payload database (fray update).

    Priority: R2 → GitHub Releases → GitHub repo raw files
    """
    cfg = load_config()

    if verbose:
        print(f"\n  {_C.B}Fray Payload Database Update{_C.E}")
        print(f"  {_C.DIM}Current version: {__version__}{_C.E}")

    result = None

    # Try R2 first (fastest)
    if source in ("auto", "r2") and r2_available(cfg):
        if verbose:
            print(f"\n  {_C.BL}[Cloudflare R2]{_C.E}")
        result = r2_download_bundle(cfg, verbose)

    # Fallback to GitHub releases
    if not result and source in ("auto", "github"):
        if verbose:
            print(f"\n  {_C.BL}[GitHub Releases]{_C.E}")
        result = github_download_bundle(cfg, verbose)

    if not result:
        if verbose:
            print(f"\n  {_C.R}No payload bundle available.{_C.E}")
            print(f"  {_C.DIM}Payloads are up to date from the installed package.{_C.E}")
        return None

    bundle, manifest = result

    # Extract to payloads directory
    payloads_root = Path(__file__).parent.parent / "payloads"
    if not payloads_root.exists():
        payloads_root = PAYLOADS_DIR

    if verbose:
        src = manifest.get("source", "unknown")
        total = manifest.get("total_payloads", "?")
        cats = len(manifest.get("categories", {}))
        print(f"\n  {_C.BL}Extracting...{_C.E}")
        print(f"    Source:     {src}")
        print(f"    Payloads:   {total}")
        print(f"    Categories: {cats}")

    extracted_manifest = extract_payload_bundle(bundle, payloads_root)

    # Save update metadata
    update_info = {
        "last_update": datetime.now(timezone.utc).isoformat(),
        "source": manifest.get("source", "unknown"),
        "version": manifest.get("version", ""),
        "total_payloads": manifest.get("total_payloads", 0),
        "bundle_sha256": manifest.get("bundle_sha256", ""),
    }
    _FRAY_DIR.mkdir(parents=True, exist_ok=True)
    (_FRAY_DIR / "last_update.json").write_text(
        json.dumps(update_info, indent=2), encoding="utf-8")

    if verbose:
        print(f"\n  {_C.G}Update complete!{_C.E}")
        print(f"    {_C.DIM}Payloads extracted to {payloads_root}{_C.E}")

    return manifest


def publish_payloads(*, to_r2: bool = True, to_github: bool = True,
                     tag: str = "", verbose: bool = True) -> Dict:
    """
    Publish payload database to cloud (maintainer command).

    fray sync --push
    """
    cfg = load_config()

    if verbose:
        print(f"\n  {_C.B}Publishing Payload Database{_C.E}")

    # Build bundle
    if verbose:
        print(f"\n  {_C.BL}Building bundle...{_C.E}")
    bundle, manifest = build_payload_bundle()

    if verbose:
        size_mb = len(bundle) / 1024 / 1024
        print(f"    Size:       {size_mb:.1f} MB")
        print(f"    Payloads:   {manifest['total_payloads']}")
        print(f"    Categories: {len(manifest['categories'])}")
        print(f"    SHA256:     {manifest['bundle_sha256'][:16]}...")

    results = {"bundle_size": len(bundle), "manifest": manifest}

    # Upload to R2
    if to_r2 and r2_available(cfg):
        if verbose:
            print(f"\n  {_C.BL}[Cloudflare R2]{_C.E}")
        results["r2"] = r2_upload_bundle(cfg, bundle, manifest, verbose)
    elif to_r2:
        if verbose:
            print(f"\n  {_C.Y}R2 not configured — skipping{_C.E}")
        results["r2"] = False

    # Upload to GitHub
    if to_github and cfg.github_token:
        if verbose:
            print(f"\n  {_C.BL}[GitHub Release]{_C.E}")
        results["github"] = github_upload_bundle(cfg, bundle, manifest, tag, verbose)
    elif to_github:
        if verbose:
            print(f"\n  {_C.Y}GITHUB_TOKEN not set — skipping{_C.E}")
        results["github"] = False

    if verbose:
        print(f"\n  {_C.B}Publish Summary{_C.E}")
        if results.get("r2"):
            print(f"    R2:     {_C.G}uploaded{_C.E}")
        if results.get("github"):
            print(f"    GitHub: {_C.G}released{_C.E}")

    return results


def run_sync(*, push: bool = False, pull: bool = False,
             share_patterns: bool = False, source: str = "auto",
             tag: str = "", verbose: bool = True) -> Dict:
    """Main sync entry point for fray sync command."""
    if push:
        return publish_payloads(tag=tag, verbose=verbose)
    elif pull or not push:
        manifest = update_payloads(source=source, verbose=verbose)
        return {"manifest": manifest} if manifest else {}
