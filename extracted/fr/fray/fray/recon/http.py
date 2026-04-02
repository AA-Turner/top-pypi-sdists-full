"""HTTP utilities for Fray Recon — URL parsing, SSL, HTTP GET, TLS audit."""

import http.client
import socket
import ssl
import urllib.parse
from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple

from fray import __version__


def _parse_url(url: str) -> Tuple[str, str, int, bool]:
    """Parse URL into (host, path, port, use_ssl)."""
    if not url.startswith("http"):
        url = f"https://{url}"
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    use_ssl = parsed.scheme == "https"
    port = parsed.port or (443 if use_ssl else 80)
    path = parsed.path or "/"
    return host, path, port, use_ssl


def _make_ssl_context(verify: bool = True) -> ssl.SSLContext:
    """Create an SSL context, optionally unverified."""
    if verify:
        return ssl.create_default_context()
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _http_get(host: str, port: int, path: str, use_ssl: bool,
              timeout: int = 8, max_redirects: int = 5,
              extra_headers: Optional[Dict[str, str]] = None) -> Tuple[int, Dict[str, str], str]:
    """Make a raw HTTP GET, follow redirects, return (status, headers_dict, body)."""
    all_headers: Dict[str, str] = {}
    for _ in range(max_redirects + 1):
        try:
            req_headers = {
                "Host": host,
                "User-Agent": f"Fray/{__version__} Recon",
                "Accept": "text/html,application/json,*/*",
                "Connection": "close",
            }
            if extra_headers:
                req_headers.update(extra_headers)

            if use_ssl:
                # Try verified first, fallback to unverified on cert errors
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

            status = resp.status
            headers = {k.lower(): v for k, v in resp.getheaders()}
            all_headers.update(headers)
            body = resp.read(200000).decode("utf-8", errors="replace")
            conn.close()

            if status in (301, 302, 303, 307, 308):
                location = headers.get("location", "")
                if location.startswith("https://") or location.startswith("http://"):
                    parsed = urllib.parse.urlparse(location)
                    host = parsed.hostname or host
                    port = parsed.port or (443 if parsed.scheme == "https" else 80)
                    use_ssl = parsed.scheme == "https"
                    path = parsed.path or "/"
                    if parsed.query:
                        path += f"?{parsed.query}"
                    continue
                elif location.startswith("/"):
                    path = location
                    continue
            return status, all_headers, body
        except Exception as e:
            return 0, all_headers, str(e)
    return status, all_headers, body


def check_http(host: str, timeout: int = 5) -> Dict[str, Any]:
    """Check if port 80 is open and whether it redirects to HTTPS."""
    result: Dict[str, Any] = {
        "port_80_open": False,
        "redirects_to_https": False,
        "http_status": 0,
    }
    try:
        sock = socket.create_connection((host, 80), timeout=timeout)
        sock.close()
        result["port_80_open"] = True
    except (socket.error, socket.timeout, OSError):
        return result

    # Check redirect
    status, headers, _ = _http_get(host, 80, "/", use_ssl=False, timeout=timeout)
    result["http_status"] = status
    if status in (301, 302, 307, 308):
        location = headers.get("location", "")
        if location.startswith("https://"):
            result["redirects_to_https"] = True
    return result


def check_tls(host: str, port: int = 443, timeout: int = 8) -> Dict[str, Any]:
    """Audit TLS configuration: version, cipher, certificate."""
    result: Dict[str, Any] = {
        "tls_version": None,
        "cipher": None,
        "cipher_bits": None,
        "cert_subject": None,
        "cert_issuer": None,
        "cert_expiry": None,
        "cert_expired": None,
        "cert_days_remaining": None,
        "supports_tls_1_0": False,
        "supports_tls_1_1": False,
        "error": None,
    }

    # Main connection — best TLS version
    # Try verified first; fallback to unverified on cert errors (common on macOS)
    ssock = None
    for verify in (True, False):
        try:
            if verify:
                ctx = ssl.create_default_context()
            else:
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            sock = socket.create_connection((host, port), timeout=timeout)
            ssock = ctx.wrap_socket(sock, server_hostname=host)
            break
        except ssl.SSLError:
            if verify:
                continue  # Retry without verification
            result["error"] = "TLS handshake failed"
        except Exception as e:
            result["error"] = str(e)
            break

    if ssock:
        try:
            result["tls_version"] = ssock.version()
            cipher_info = ssock.cipher()
            if cipher_info:
                result["cipher"] = cipher_info[0]
                result["cipher_bits"] = cipher_info[2]

            cert = ssock.getpeercert()
            if cert:
                # Subject
                subject_parts = []
                for rdn in cert.get("subject", ()):
                    for attr_type, attr_value in rdn:
                        if attr_type == "commonName":
                            subject_parts.append(attr_value)
                result["cert_subject"] = ", ".join(subject_parts) or None

                # Issuer
                issuer_parts = []
                for rdn in cert.get("issuer", ()):
                    for attr_type, attr_value in rdn:
                        if attr_type in ("organizationName", "commonName"):
                            issuer_parts.append(attr_value)
                result["cert_issuer"] = ", ".join(issuer_parts) or None

                # Expiry
                not_after = cert.get("notAfter")
                if not_after:
                    try:
                        expiry = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                        expiry = expiry.replace(tzinfo=timezone.utc)
                        result["cert_expiry"] = expiry.isoformat()
                        now = datetime.now(timezone.utc)
                        delta = expiry - now
                        result["cert_days_remaining"] = delta.days
                        result["cert_expired"] = delta.days < 0
                    except ValueError:
                        result["cert_expiry"] = not_after

            ssock.close()
        except Exception as e:
            result["error"] = str(e)

    # Probe for weak TLS versions
    for proto_name, proto_const in [("tls_1_0", ssl.PROTOCOL_TLS), ("tls_1_1", ssl.PROTOCOL_TLS)]:
        try:
            ctx_weak = ssl.SSLContext(proto_const)
            ctx_weak.check_hostname = False
            ctx_weak.verify_mode = ssl.CERT_NONE
            if proto_name == "tls_1_0":
                ctx_weak.maximum_version = ssl.TLSVersion.TLSv1
            else:
                ctx_weak.maximum_version = ssl.TLSVersion.TLSv1_1
            sock = socket.create_connection((host, port), timeout=timeout)
            ssock = ctx_weak.wrap_socket(sock, server_hostname=host)
            version = ssock.version()
            ssock.close()
            if version and "TLSv1.0" in version:
                result["supports_tls_1_0"] = True
            elif version and "TLSv1.1" in version:
                result["supports_tls_1_1"] = True
        except Exception:
            pass  # Good — weak version not supported

    return result


# ── Weak cipher / protocol lists ────────────────────────────────────────

_WEAK_CIPHERS = {
    # NULL ciphers
    "TLS_NULL_WITH_NULL_NULL", "TLS_RSA_WITH_NULL_MD5", "TLS_RSA_WITH_NULL_SHA",
    "TLS_RSA_WITH_NULL_SHA256",
    # Export-grade (FREAK)
    "TLS_RSA_EXPORT_WITH_RC4_40_MD5", "TLS_RSA_EXPORT_WITH_DES40_CBC_SHA",
    "TLS_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA",
    # RC4 (broken)
    "RC4-MD5", "RC4-SHA", "TLS_RSA_WITH_RC4_128_MD5", "TLS_RSA_WITH_RC4_128_SHA",
    "ECDHE-RSA-RC4-SHA", "ECDHE-ECDSA-RC4-SHA",
    # DES / 3DES (Sweet32)
    "DES-CBC-SHA", "DES-CBC3-SHA", "TLS_RSA_WITH_DES_CBC_SHA",
    "TLS_RSA_WITH_3DES_EDE_CBC_SHA", "ECDHE-RSA-DES-CBC3-SHA",
    # CBC with SHA-1 (BEAST-vulnerable with TLS 1.0)
    "AES128-SHA", "AES256-SHA",
}

_WEAK_CIPHER_KEYWORDS = ("rc4", "des", "null", "export", "anon", "md5")


def check_tls_grade(tls_data: Dict[str, Any]) -> Dict[str, Any]:
    """Grade TLS configuration from check_tls() output.

    Returns:
      - grade: "A+" | "A" | "B" | "C" | "D" | "F"
      - score: 0-100
      - issues: list of problems found
      - strengths: list of good practices
    """
    result: Dict[str, Any] = {
        "grade": "A+",
        "score": 100,
        "issues": [],
        "strengths": [],
    }

    if not tls_data or tls_data.get("error"):
        result["grade"] = "F"
        result["score"] = 0
        result["issues"].append(tls_data.get("error", "TLS connection failed"))
        return result

    tls_version = tls_data.get("tls_version") or ""
    cipher = tls_data.get("cipher") or ""
    cipher_bits = tls_data.get("cipher_bits") or 0
    supports_10 = tls_data.get("supports_tls_1_0", False)
    supports_11 = tls_data.get("supports_tls_1_1", False)
    cert_expired = tls_data.get("cert_expired", False)
    cert_days = tls_data.get("cert_days_remaining")

    score = 100

    # ── Protocol version ──
    if "TLSv1.3" in tls_version:
        result["strengths"].append("TLS 1.3 negotiated")
    elif "TLSv1.2" in tls_version:
        result["strengths"].append("TLS 1.2 negotiated")
        score -= 5  # Not the latest
    elif "TLSv1.1" in tls_version:
        result["issues"].append("Negotiated TLS 1.1 — deprecated since 2021 (RFC 8996)")
        score -= 30
    elif "TLSv1.0" in tls_version or "TLSv1" == tls_version:
        result["issues"].append("Negotiated TLS 1.0 — deprecated, vulnerable to BEAST/POODLE")
        score -= 40
    elif "SSLv3" in tls_version:
        result["issues"].append("SSLv3 negotiated — broken (POODLE), must disable")
        score -= 60

    # ── Weak protocol support ──
    if supports_10:
        result["issues"].append("TLS 1.0 supported — should be disabled (PCI DSS non-compliant)")
        score -= 20
    if supports_11:
        result["issues"].append("TLS 1.1 supported — should be disabled (RFC 8996)")
        score -= 15

    # ── Cipher strength ──
    cipher_upper = cipher.upper()
    cipher_lower = cipher.lower()

    if cipher in _WEAK_CIPHERS or any(kw in cipher_lower for kw in _WEAK_CIPHER_KEYWORDS):
        result["issues"].append(f"Weak cipher: {cipher}")
        score -= 30
    elif cipher_bits >= 256:
        result["strengths"].append(f"Strong cipher: {cipher} ({cipher_bits}-bit)")
    elif cipher_bits >= 128:
        result["strengths"].append(f"Adequate cipher: {cipher} ({cipher_bits}-bit)")
    elif cipher_bits > 0:
        result["issues"].append(f"Short key: {cipher} ({cipher_bits}-bit) — minimum 128-bit recommended")
        score -= 25

    # Forward secrecy (TLS 1.3 always has PFS; TLS 1.2 needs ECDHE/DHE)
    if "TLSv1.3" in tls_version:
        result["strengths"].append("Forward secrecy (TLS 1.3 — always PFS)")
    elif "ECDHE" in cipher_upper or "DHE" in cipher_upper:
        result["strengths"].append("Forward secrecy (ECDHE/DHE)")
    elif cipher:
        result["issues"].append(f"No forward secrecy — cipher {cipher} uses static key exchange")
        score -= 15

    # AEAD cipher (GCM/CCM/ChaCha20)
    if "GCM" in cipher_upper or "CHACHA20" in cipher_upper or "CCM" in cipher_upper:
        result["strengths"].append("AEAD cipher mode (GCM/ChaCha20)")
    elif "CBC" in cipher_upper:
        result["issues"].append("CBC cipher mode — vulnerable to padding oracle attacks with TLS < 1.3")
        score -= 10

    # ── Certificate ──
    if cert_expired:
        result["issues"].append("Certificate EXPIRED")
        score -= 40
    elif cert_days is not None:
        if cert_days < 7:
            result["issues"].append(f"Certificate expires in {cert_days} days — URGENT renewal needed")
            score -= 20
        elif cert_days < 30:
            result["issues"].append(f"Certificate expires in {cert_days} days — renew soon")
            score -= 10
        elif cert_days > 365:
            result["issues"].append(f"Certificate validity > 1 year ({cert_days} days) — max 398 days recommended")
            score -= 5

    # ── Final grade ──
    score = max(0, min(100, score))
    result["score"] = score

    if score >= 95:
        result["grade"] = "A+"
    elif score >= 85:
        result["grade"] = "A"
    elif score >= 70:
        result["grade"] = "B"
    elif score >= 50:
        result["grade"] = "C"
    elif score >= 30:
        result["grade"] = "D"
    else:
        result["grade"] = "F"

    return result


# ── Additional HTTP utilities (moved from _monolith.py) ─────────────────

def _follow_redirect(host: str, path: str, timeout: int = 10,
                     max_hops: int = 3) -> Tuple[int, bytes]:
    """Follow HTTPS redirects, return (status, body_bytes)."""
    for _ in range(max_hops + 1):
        try:
            ctx = _make_ssl_context(verify=True)
        except Exception:
            ctx = _make_ssl_context(verify=False)
        try:
            conn = http.client.HTTPSConnection(host, context=ctx, timeout=timeout)
            conn.request("GET", path, headers={"User-Agent": f"Fray/{__version__}"})
            resp = conn.getresponse()
            status = resp.status
            body = resp.read()
            hdrs = {k.lower(): v for k, v in resp.getheaders()}
            conn.close()
            if status in (301, 302, 303, 307, 308):
                loc = hdrs.get("location", "")
                if loc.startswith("https://"):
                    parsed = urllib.parse.urlparse(loc)
                    host = parsed.hostname or host
                    path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
                    continue
            return status, body
        except Exception:
            return 0, b""
    return 0, b""


def _post_json(url: str, body: str, timeout: int = 6,
               verify_ssl: bool = True,
               headers: Optional[Dict[str, str]] = None) -> tuple:
    """HTTP POST with JSON body — stdlib only, SSL fallback."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    req_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    if headers:
        req_headers.update(headers)

    encoded = body.encode("utf-8")

    if parsed.scheme == "https":
        port = port or 443
        for do_verify in ([True, False] if verify_ssl else [False]):
            try:
                ctx = ssl.create_default_context()
                if not do_verify:
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                conn = http.client.HTTPSConnection(host, port, timeout=timeout, context=ctx)
                conn.request("POST", path, body=encoded, headers=req_headers)
                resp = conn.getresponse()
                resp_body = resp.read(500_000).decode("utf-8", errors="replace")
                conn.close()
                return resp.status, resp_body
            except ssl.SSLError:
                continue
            except Exception:
                return 0, ""
        return 0, ""
    else:
        port = port or 80
        conn = http.client.HTTPConnection(host, port, timeout=timeout)
        try:
            conn.request("POST", path, body=encoded, headers=req_headers)
            resp = conn.getresponse()
            resp_body = resp.read(500_000).decode("utf-8", errors="replace")
            return resp.status, resp_body
        except Exception:
            return 0, ""
        finally:
            conn.close()


def fetch_headers(url: str, timeout: int = 8) -> Dict[str, str]:
    """Fetch HTTP response headers from a URL. Returns lowercase header dict."""
    status, _, headers = _fetch_url(url, timeout=timeout)
    return headers if status > 0 else {}


def _fetch_url(url: str, timeout: int = 12, verify_ssl: bool = True,
               headers: Optional[Dict[str, str]] = None) -> tuple:
    """Simple HTTP GET — independent of scanner's _fetch (no global backoff state)."""
    parsed = urllib.parse.urlparse(url)
    host = parsed.hostname or ""
    port = parsed.port
    path = parsed.path or "/"
    if parsed.query:
        path += "?" + parsed.query

    if parsed.scheme == "https":
        port = port or 443
        ctx = ssl.create_default_context()
        if not verify_ssl:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        conn = http.client.HTTPSConnection(host, port, timeout=timeout, context=ctx)
    else:
        port = port or 80
        conn = http.client.HTTPConnection(host, port, timeout=timeout)

    req_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "*/*",
    }
    if headers:
        req_headers.update(headers)

    try:
        conn.request("GET", path, headers=req_headers)
        resp = conn.getresponse()
        body = resp.read(1_000_000).decode("utf-8", errors="replace")
        resp_headers = {k.lower(): v for k, v in resp.getheaders()}
        return resp.status, body, resp_headers
    except Exception:
        return 0, "", {}
    finally:
        conn.close()
