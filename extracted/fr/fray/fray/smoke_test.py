"""
Fray QA Smoke Test — Internal quality assurance against test targets.

Two target zones:
  1. qa        — Intentionally vulnerable sites (Juice Shop, Acunetix, etc.)
                 We verify we detect XSS, SQLi, CVEs, broken auth, etc. correctly.
  2. llm_zone  — Live AI/LLM company endpoints used to calibrate LLM endpoint
                 detection accuracy. We verify our AI path detection, model
                 endpoint fingerprinting, and API security checks fire correctly.

Usage:
    fray smoke                     # Run all QA targets (quick mode)
    fray smoke --quick             # Detect + recon only
    fray smoke --full              # Detect + recon + payload test
    fray smoke --llm               # Run LLM zone targets only
    fray smoke --all               # Run both zones
    fray smoke --json              # JSON output for CI

QA Targets (intentionally vulnerable):
    1. Acunetix PHP        (testphp.vulnweb.com)
    2. Acunetix ASP.NET    (testaspnet.vulnweb.com)
    3. Acunetix Classic ASP (testasp.vulnweb.com)
    4. OWASP Juice Shop    (juice-shop.herokuapp.com)
    5. Zero Bank           (zero.webappsecurity.com)
    6. Gin & Juice Shop    (ginandjuice.shop) — PortSwigger
    7. DVWA                (www.dvwa.co.uk)
    8. Google Firing Range (public-firing-range.appspot.com)
    9. Altoro Mutual       (demo.testfire.net) — HCL/IBM
   10. Hackable Vercel     (hackable-vulnerable-website.vercel.app)

LLM Zone Targets (live AI companies — recon only, no payload testing):
   11. OpenAI              (api.openai.com)
   12. Anthropic           (api.anthropic.com)
   13. Hugging Face        (huggingface.co)
   14. Replicate           (replicate.com)
   15. Cohere              (api.cohere.ai)
   16. Mistral             (api.mistral.ai)
   17. Together AI         (api.together.xyz)
   18. Perplexity          (api.perplexity.ai)
"""

import json
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from fray import __version__

# ── Smoke Test Target ────────────────────────────────────────────────────────

@dataclass
class SmokeTarget:
    """A smoke test target with expected detection assertions."""
    url: str
    name: str
    zone: str           # "qa" or "llm_zone"
    expected_waf: str   # Expected WAF vendor (or "none")
    description: str
    tags: List[str] = field(default_factory=list)
    # What Fray MUST detect to pass QA
    must_detect: List[str] = field(default_factory=list)
    # Minimum risk score expected (0 = no requirement)
    min_risk_score: int = 0


# ── QA Targets — Intentionally Vulnerable ───────────────────────────────────

QA_TARGETS = [
    SmokeTarget(
        url="http://testphp.vulnweb.com",
        name="Acunetix PHP",
        zone="qa",
        expected_waf="none",
        description="Acunetix intentionally vulnerable PHP app (XSS, SQLi, LFI)",
        tags=["php", "xss", "sqli", "lfi"],
        must_detect=["xss", "sqli"],
        min_risk_score=50,
    ),
    SmokeTarget(
        url="http://testaspnet.vulnweb.com",
        name="Acunetix ASP.NET",
        zone="qa",
        expected_waf="none",
        description="Acunetix intentionally vulnerable ASP.NET app",
        tags=["aspnet", "xss", "sqli"],
        must_detect=["xss", "sqli"],
        min_risk_score=50,
    ),
    SmokeTarget(
        url="http://testasp.vulnweb.com",
        name="Acunetix Classic ASP",
        zone="qa",
        expected_waf="none",
        description="Acunetix intentionally vulnerable classic ASP app",
        tags=["asp", "xss", "sqli"],
        must_detect=["xss", "sqli"],
        min_risk_score=50,
    ),
    SmokeTarget(
        url="https://juice-shop.herokuapp.com",
        name="OWASP Juice Shop",
        zone="qa",
        expected_waf="none",
        description="OWASP Juice Shop — modern JS app with 100+ vulns",
        tags=["owasp", "nodejs", "xss", "sqli", "auth", "jwt"],
        must_detect=["xss", "sqli", "broken_auth", "jwt"],
        min_risk_score=70,
    ),
    SmokeTarget(
        url="http://zero.webappsecurity.com",
        name="Zero Bank",
        zone="qa",
        expected_waf="none",
        description="Micro Focus vulnerable banking app (auth, injection)",
        tags=["banking", "auth", "sqli"],
        must_detect=["sqli", "broken_auth"],
        min_risk_score=50,
    ),
    SmokeTarget(
        url="https://ginandjuice.shop",
        name="Gin & Juice Shop",
        zone="qa",
        expected_waf="none",
        description="PortSwigger (Burp) public vulnerable target",
        tags=["portswigger", "xss", "sqli", "ssrf", "supply_chain"],
        must_detect=["xss", "sqli", "supply_chain"],
        min_risk_score=60,
    ),
    SmokeTarget(
        url="http://www.dvwa.co.uk",
        name="DVWA",
        zone="qa",
        expected_waf="none",
        description="Damn Vulnerable Web Application — classic training target",
        tags=["dvwa", "xss", "sqli", "cmdi"],
        must_detect=["xss", "sqli", "cmdi"],
        min_risk_score=60,
    ),
    SmokeTarget(
        url="https://public-firing-range.appspot.com",
        name="Google Firing Range",
        zone="qa",
        expected_waf="none",
        description="Google's test bed for web vulnerability scanners",
        tags=["google", "xss", "dom"],
        must_detect=["xss"],
        min_risk_score=40,
    ),
    SmokeTarget(
        url="http://demo.testfire.net",
        name="Altoro Mutual",
        zone="qa",
        expected_waf="none",
        description="HCL/IBM AppScan demo vulnerable banking site",
        tags=["ibm", "banking", "sqli", "xss"],
        must_detect=["sqli", "xss"],
        min_risk_score=60,
    ),
    SmokeTarget(
        url="https://hackable-vulnerable-website.vercel.app",
        name="Hackable Vercel",
        zone="qa",
        expected_waf="none",
        description="Community-maintained vulnerable app on Vercel",
        tags=["vercel", "xss", "modern"],
        must_detect=["xss"],
        min_risk_score=40,
    ),
]

# ── Real Domain Zone — production sites for tech stack detection accuracy ────
# Purpose: verify Fray correctly detects CDN, WAF, DNS provider, and tech stack
# on real production targets. Recon ONLY — no payload injection ever.
# These are large public companies — we check fingerprinting accuracy only.
# Expected detections sourced from confirmed research (DNS lookup, header analysis).

# ── Local Zone — locally-running vulnerable apps for CVE/detection verification ──
# Used with `fray smoke --local`. Apps run on localhost at known ports.
# Each entry documents which GitHub repo to clone and how to start it.
# These never hit the internet — pure localhost testing.
#
# Setup (one-time):
#   git clone https://github.com/lirantal/vulnerable-nextjs-14-CVE-2025-29927
#   cd vulnerable-nextjs-14-CVE-2025-29927 && npm install && npm run dev
#   # Opens on localhost:3000
#
# Then: fray smoke --local

LOCAL_TARGETS = [
    # ── Next.js CVE-2025-29927 (middleware auth bypass) ─────────────────
    SmokeTarget(
        url="http://localhost:3000",
        name="CVE-2025-29927 (Next.js 14.2.24)",
        zone="local",
        expected_waf="none",
        description=(
            "lirantal/vulnerable-nextjs-14-CVE-2025-29927 — "
            "Next.js 14.2.24 intentionally vulnerable to middleware bypass. "
            "Setup: git clone https://github.com/lirantal/vulnerable-nextjs-14-CVE-2025-29927 "
            "&& cd vulnerable-nextjs-14-CVE-2025-29927 && npm install && npm run dev"
        ),
        tags=["nextjs", "cve-2025-29927", "middleware_bypass", "local"],
        must_detect=["middleware_bypass", "CVE-2025-29927"],
        min_risk_score=50,
    ),
    SmokeTarget(
        url="http://localhost:3001",
        name="CVE-2025-29927 (Next.js 15.2.2 / azu)",
        zone="local",
        expected_waf="none",
        description=(
            "azu/nextjs-cve-2025-29927-poc — "
            "Next.js 15.2.2 TypeScript variant. "
            "Setup: git clone https://github.com/azu/nextjs-cve-2025-29927-poc "
            "&& cd nextjs-cve-2025-29927-poc && npm install && npm run dev -- --port 3001"
        ),
        tags=["nextjs", "cve-2025-29927", "middleware_bypass", "local", "typescript"],
        must_detect=["middleware_bypass", "CVE-2025-29927"],
        min_risk_score=50,
    ),
    # ── OWASP Juice Shop (Docker) ────────────────────────────────────────
    SmokeTarget(
        url="http://localhost:3002",
        name="OWASP Juice Shop (local Docker)",
        zone="local",
        expected_waf="none",
        description=(
            "OWASP Juice Shop — local Docker instance. "
            "Setup: docker run -p 3002:3000 bkimminich/juice-shop"
        ),
        tags=["owasp", "nodejs", "xss", "sqli", "auth", "jwt", "local"],
        must_detect=["xss", "sqli", "broken_auth"],
        min_risk_score=70,
    ),
    # ── DVWA (Docker) ───────────────────────────────────────────────────
    SmokeTarget(
        url="http://localhost:3003",
        name="DVWA (local Docker)",
        zone="local",
        expected_waf="none",
        description=(
            "Damn Vulnerable Web Application — local Docker. "
            "Setup: docker run --rm -p 3003:80 vulnerables/web-dvwa"
        ),
        tags=["dvwa", "php", "xss", "sqli", "cmdi", "local"],
        must_detect=["xss", "sqli"],
        min_risk_score=60,
    ),
    # ── Log4Shell (Docker) ───────────────────────────────────────────────
    SmokeTarget(
        url="http://localhost:3004",
        name="Log4Shell CVE-2021-44228 (local Docker)",
        zone="local",
        expected_waf="none",
        description=(
            "christophetd/log4shell-vulnerable-app — CVE-2021-44228 test target. "
            "Setup: docker run -p 3004:8080 ghcr.io/christophetd/log4shell-vulnerable-app"
        ),
        tags=["java", "log4shell", "cve-2021-44228", "local"],
        must_detect=["log4shell"],
        min_risk_score=80,
    ),
    # ── crAPI — OWASP API Top 10 ─────────────────────────────────────────
    SmokeTarget(
        url="http://localhost:3005",
        name="crAPI (OWASP API Top 10, local Docker)",
        zone="local",
        expected_waf="none",
        description=(
            "OWASP/crAPI — Completely Ridiculous API. "
            "Setup: git clone https://github.com/OWASP/crAPI "
            "&& cd crAPI && docker-compose -f deploy/docker/docker-compose.yml up -d "
            "(exposes API on :8888, mail on :8025; map :8888 to :3005)"
        ),
        tags=["api", "owasp", "bola", "broken_auth", "mass_assignment", "local"],
        must_detect=["api_security", "bola"],
        min_risk_score=60,
    ),
]


REAL_DOMAIN_TARGETS = [
    SmokeTarget(
        url="https://www.sony.com",
        name="Sony",
        zone="real_domain",
        expected_waf="akamai",
        description="Sony global — Akamai CDN/WAF, CSC Global enterprise DNS",
        tags=["akamai", "enterprise", "cscdns"],
        must_detect=["akamai"],
        min_risk_score=0,
        # Notes: returns 403 (Akamai bot protection) but reference ID in body
        # confirms Akamai. No payload testing ever on this target.
    ),
    SmokeTarget(
        url="https://www.jal.co.jp",
        name="JAL (Japan Airlines)",
        zone="real_domain",
        expected_waf="none",
        description="Japan Airlines — IIJ D-53 DNS. Times out from non-JP IPs (geo-block).",
        tags=["iij", "japan", "geo-block"],
        must_detect=[],  # cf-team was client ZT injection, not server WAF
        min_risk_score=0,
        # Notes: www.jal.co.jp times out from outside Japan.
        # jal.co.jp apex redirects. IIJ D-53 DNS correctly detected.
        # cf-team header was confirmed client-injected by WARP ZT client.
    ),
    SmokeTarget(
        url="https://grab.com",
        name="Grab",
        zone="real_domain",
        expected_waf="none",
        description="Grab super-app — AWS Route 53, CloudFront CDN, nginx origin",
        tags=["aws", "cloudfront", "nginx"],
        must_detect=["cloudfront", "aws"],
        min_risk_score=0,
    ),
    SmokeTarget(
        url="https://www.bbc.com",
        name="BBC",
        zone="real_domain",
        expected_waf="none",
        description="BBC — Self-hosted DNS (dns0.bbc.co.uk), Fastly CDN + Varnish. "
                    "First-visit shows a service worker consent page with no CDN headers.",
        tags=["fastly", "varnish", "self-hosted-dns"],
        must_detect=[],  # Fastly/Varnish only visible via Via header after consent
        min_risk_score=0,
        # Notes: cf-biso-version was confirmed client-injected by WARP ZT client.
        # BBC uses Fastly + Varnish but headers only appear after cookie consent.
        # Self-hosted DNS: dns0.bbc.co.uk / dns0.bbc.com
    ),
]

# ── LLM Zone — AI company endpoints for detection accuracy calibration ───────
# Purpose: verify LLM endpoint fingerprinting, API security checks, supply
# chain detection fire correctly on real AI infrastructure.
# Rules: recon ONLY — no payload injection on these targets ever.

LLM_TARGETS = [
    SmokeTarget(
        url="https://api.openai.com",
        name="OpenAI API",
        zone="llm_zone",
        expected_waf="none",
        description="OpenAI LLM API — verify /v1/models, /v1/chat/completions detection",
        tags=["openai", "llm", "api"],
        must_detect=["llm_endpoint", "api_security"],
    ),
    SmokeTarget(
        url="https://api.anthropic.com",
        name="Anthropic API",
        zone="llm_zone",
        expected_waf="none",
        description="Anthropic Claude API — verify /v1/messages detection",
        tags=["anthropic", "llm", "api"],
        must_detect=["llm_endpoint", "api_security"],
    ),
    SmokeTarget(
        url="https://huggingface.co",
        name="Hugging Face",
        zone="llm_zone",
        expected_waf="none",
        description="HF model hub — verify AI endpoint, supply chain, CDN detection",
        tags=["huggingface", "llm", "model_hub", "supply_chain"],
        must_detect=["llm_endpoint", "supply_chain"],
    ),
    SmokeTarget(
        url="https://replicate.com",
        name="Replicate",
        zone="llm_zone",
        expected_waf="none",
        description="Replicate model inference API — verify LLM + API detection",
        tags=["replicate", "llm", "api"],
        must_detect=["llm_endpoint"],
    ),
    SmokeTarget(
        url="https://api.cohere.ai",
        name="Cohere API",
        zone="llm_zone",
        expected_waf="none",
        description="Cohere LLM API — verify /v1/generate, /v1/embed detection",
        tags=["cohere", "llm", "api"],
        must_detect=["llm_endpoint", "api_security"],
    ),
    SmokeTarget(
        url="https://api.mistral.ai",
        name="Mistral API",
        zone="llm_zone",
        expected_waf="none",
        description="Mistral LLM API — verify /v1/chat/completions detection",
        tags=["mistral", "llm", "api"],
        must_detect=["llm_endpoint", "api_security"],
    ),
    SmokeTarget(
        url="https://api.together.xyz",
        name="Together AI",
        zone="llm_zone",
        expected_waf="none",
        description="Together AI inference API — LLM endpoint + API auth detection",
        tags=["together", "llm", "api"],
        must_detect=["llm_endpoint"],
    ),
    SmokeTarget(
        url="https://api.perplexity.ai",
        name="Perplexity AI",
        zone="llm_zone",
        expected_waf="none",
        description="Perplexity AI search + LLM API",
        tags=["perplexity", "llm", "api"],
        must_detect=["llm_endpoint"],
    ),
]


def get_targets(zone: str = "qa") -> List[SmokeTarget]:
    """Get targets by zone.

    Zones:
        qa          — 10 intentionally vulnerable apps (XSS, SQLi, broken auth)
        llm_zone    — 8 AI company endpoints (LLM detection calibration)
        real_domain — 4 real production domains (tech stack detection accuracy)
        local       — 6 locally-running vulnerable apps (CVE/detection accuracy)
                      Requires apps running on localhost:3000-3005 (see SmokeTarget descriptions)
        all         — all remote zones (qa + llm_zone + real_domain), NOT local
    """
    if zone == "all":
        return QA_TARGETS + LLM_TARGETS + REAL_DOMAIN_TARGETS
    elif zone == "llm_zone":
        return LLM_TARGETS
    elif zone == "real_domain":
        return REAL_DOMAIN_TARGETS
    elif zone == "local":
        return LOCAL_TARGETS
    return QA_TARGETS


# ── Detection Assertion Checker ───────────────────────────────────────────────

def _check_assertions(target: SmokeTarget, recon_result: Dict) -> Dict:
    """Check which must_detect assertions are satisfied by recon results."""
    findings = recon_result.get("findings", [])
    attack_vectors = recon_result.get("attack_vectors", [])
    technologies = recon_result.get("technologies", [])
    ai_endpoints = recon_result.get("ai_endpoints", {})
    supply_chain = recon_result.get("supply_chain", {})

    all_text = " ".join([
        str(f.get("finding", "")) for f in findings
    ] + [
        str(v.get("title", "") + " " + v.get("description", "")) for v in attack_vectors
    ]).lower()

    passed: List[str] = []
    failed: List[str] = []

    for assertion in target.must_detect:
        ok = False
        if assertion == "xss":
            ok = any(kw in all_text for kw in ["xss", "cross-site scripting", "script injection"])
        elif assertion == "sqli":
            ok = any(kw in all_text for kw in ["sql", "injection", "sqli", "database"])
        elif assertion == "cmdi":
            ok = any(kw in all_text for kw in ["command injection", "cmdi", "rce", "shell"])
        elif assertion == "broken_auth":
            ok = any(kw in all_text for kw in ["auth", "login", "session", "jwt", "token", "credential"])
        elif assertion == "jwt":
            ok = any(kw in all_text for kw in ["jwt", "json web token", "bearer"])
        elif assertion == "supply_chain":
            ok = (bool(supply_chain.get("third_party_scripts")) or
                  any(kw in all_text for kw in ["supply chain", "third-party", "cdn", "sri", "integrity"]))
        elif assertion == "llm_endpoint":
            ok = (bool(ai_endpoints.get("detected")) or
                  any(kw in all_text for kw in [
                      "openai", "anthropic", "llm", "gpt", "claude", "completions",
                      "embeddings", "inference", "hugging", "replicate", "cohere",
                      "mistral", "together", "perplexity",
                  ]) or
                  any(t.get("name", "").lower() in [
                      "openai", "anthropic", "huggingface", "cohere", "mistral",
                      "replicate", "together", "perplexity",
                  ] for t in technologies))
        elif assertion == "api_security":
            ok = any(kw in all_text for kw in [
                "api", "rate limit", "auth", "bearer", "key", "cors",
                "401", "403", "unauthorized", "forbidden", "x-api-key",
                "authentication required", "requires authentication",
            ])
        # ── Real domain tech stack assertions ─────────────────────────────
        elif assertion == "akamai":
            ok = any(kw in all_text for kw in [
                "akamai", "edgesuite", "edgekey", "akamaitech",
                "ghost.akamai", "akamai reference",
            ]) or any(t.get("name","").lower() == "akamai" for t in technologies)
        elif assertion == "cloudflare":
            # Only server-side signals — NOT cf-team/cf-biso (client ZT injection)
            ok = any(kw in all_text for kw in [
                "cloudflare", "cf-ray", "cf-cache-status",
                "cloudflare-static", "__cf_chl",
            ]) or any("cloudflare" in t.get("name","").lower() for t in technologies)
        elif assertion == "cloudfront":
            ok = any(kw in all_text for kw in [
                "cloudfront", "amazon_cloudfront", "x-amz-cf",
            ]) or any("cloudfront" in t.get("name","").lower() for t in technologies)
        elif assertion == "aws":
            ok = any(kw in all_text for kw in [
                "cloudfront", "aws", "amazon", "amazonaws",
                "x-amz", "awsalb", "amazon_cloudfront",
            ]) or any("aws" in t.get("name","").lower() or
                      "amazon" in t.get("name","").lower()
                      for t in technologies)
        elif assertion == "fastly":
            ok = any(kw in all_text for kw in [
                "fastly", "x-fastly", "fastly-restarts",
            ]) or any("fastly" in t.get("name","").lower() for t in technologies)
        elif assertion == "varnish":
            ok = any(kw in all_text for kw in [
                "varnish", "x-varnish", "via.*varnish",
            ]) or any("varnish" in t.get("name","").lower() for t in technologies)
        # ── Local CVE assertions ───────────────────────────────────────────
        elif assertion in ("middleware_bypass", "CVE-2025-29927"):
            ok = any(kw in all_text for kw in [
                "middleware", "x-middleware-subrequest", "cve-2025-29927",
                "auth bypass", "middleware bypass", "protected route",
            ]) or any("next" in t.get("name","").lower() for t in technologies)
        elif assertion == "log4shell":
            ok = any(kw in all_text for kw in [
                "log4shell", "jndi", "cve-2021-44228", "log4j",
                "jndi injection", "remote code execution",
            ])
        elif assertion == "bola":
            ok = any(kw in all_text for kw in [
                "bola", "idor", "broken object", "unauthorized access",
                "object level", "api1",
            ])

        (passed if ok else failed).append(assertion)

    return {"passed": passed, "failed": failed, "all_pass": len(failed) == 0}


# ── Smoke Test Runner ────────────────────────────────────────────────────────

@dataclass
class SmokeResult:
    """Result of a smoke test run on one target."""
    target: str
    name: str
    zone: str
    status: str = "pending"
    waf_detected: str = ""
    waf_match: bool = False
    recon_ok: bool = False
    test_ok: bool = False
    findings_count: int = 0
    risk_score: int = 0
    risk_score_ok: bool = True
    assertions_passed: List[str] = field(default_factory=list)
    assertions_failed: List[str] = field(default_factory=list)
    duration_s: float = 0.0
    error: str = ""
    details: Dict = field(default_factory=dict)


def _run_detect(target: SmokeTarget, timeout: int = 15) -> Dict:
    try:
        from fray.detector import WAFDetector
        detector = WAFDetector()
        result = detector.detect_waf(target.url, timeout=timeout, verify_ssl=False)
        return {
            "waf": result.get("waf_vendor", ""),
            "confidence": result.get("confidence", 0),
            "status_code": result.get("status_code", 0),
        }
    except Exception as e:
        return {"error": str(e)}


def _run_recon(target: SmokeTarget, timeout: int = 20) -> Dict:
    try:
        from fray.recon.pipeline import run_recon
        return run_recon(target.url, timeout=timeout, quiet=True)
    except Exception as e:
        return {"error": str(e)}


def _run_test(target: SmokeTarget, category: str = "xss",
              max_payloads: int = 5, timeout: int = 10) -> Dict:
    """Payload testing — qa zone only, never on llm_zone."""
    if target.zone != "qa":
        return {"skipped": True}
    try:
        import json as _json
        from pathlib import Path as _Path
        from fray import DATA_DIR
        from fray.tester import WAFTester
        payload_file = DATA_DIR / "payloads" / f"{category}.json"
        if not payload_file.exists():
            return {"skipped": True, "reason": f"no payloads for category {category}"}
        payloads = _json.loads(payload_file.read_text())[:max_payloads]
        tester = WAFTester(target.url, timeout=timeout, delay=0.3, verify_ssl=False)
        result = tester.test_payloads(payloads)
        total   = len(result) if isinstance(result, list) else result.get("total", 0)
        blocked = sum(1 for r in result if isinstance(r, dict) and r.get("blocked")) if isinstance(result, list) else result.get("blocked", 0)
        passed  = total - blocked
        return {"total": total, "blocked": blocked, "passed": passed, "errors": 0}
    except Exception as e:
        return {"error": str(e)}


def run_smoke_test(
    zone: str = "qa",
    mode: str = "quick",
    verbose: bool = True,
    json_output: bool = False,
) -> List[SmokeResult]:
    """Run smoke tests for the given zone and mode."""
    targets = get_targets(zone)
    results: List[SmokeResult] = []

    try:
        from fray.ui import S  # type: ignore[assignment]
    except Exception:
        class S:  # type: ignore[no-redef]
            bold = bright_cyan = bright_magenta = success = warning = error = dim = white = reset = ""

    if verbose and not json_output:
        zone_label = {
            "qa": "QA Vulnerable Sites",
            "llm_zone": "LLM Zone",
            "real_domain": "Real Domain (Tech Detection)",
            "local": "Local Lab (localhost:3000-3005)",
            "all": "All Remote Zones",
        }.get(zone, zone)
        print(f"\n  {S.bold}{S.white}Fray Smoke Test — {zone_label}{S.reset}  "
              f"{S.dim}v{__version__} · {len(targets)} targets · {mode} mode{S.reset}")
        print(f"  {S.dim}{'━' * 60}{S.reset}\n")

    for target in targets:
        sr = SmokeResult(target=target.url, name=target.name, zone=target.zone)
        t0 = time.time()

        if verbose and not json_output:
            _zone_col = {
                "qa":          getattr(S, "bright_cyan", S.success),
                "llm_zone":    getattr(S, "warning", S.dim),
                "real_domain": getattr(S, "accent2", S.success),
                "local":       getattr(S, "brand",   S.success),
            }.get(target.zone, S.dim)
            zone_badge = f"{_zone_col}{target.zone.upper()[:5]}{S.reset}"
            print(f"  [{zone_badge}] {S.bold}{target.name}{S.reset} ({target.url})")
            if target.must_detect:
                print(f"    {S.dim}Must detect: {', '.join(target.must_detect)}{S.reset}")

        # Phase 1 — WAF detection
        det = _run_detect(target)
        if "error" not in det:
            sr.waf_detected = det.get("waf", "")
            expected = target.expected_waf.lower()
            detected = sr.waf_detected.lower()
            sr.waf_match = (detected in ("", "none") if expected == "none"
                            else expected in detected or detected in expected)
            if verbose and not json_output and S:
                match_icon = f"{S.success}✓{S.reset}" if sr.waf_match else f"{S.warning}~{S.reset}"
                print(f"    WAF: {sr.waf_detected or 'none'} {match_icon}")
        else:
            sr.error = det["error"]

        # Phase 2 — Recon
        if not sr.error:
            rec = _run_recon(target)
            if "error" not in rec:
                sr.recon_ok = True
                sr.findings_count = len(rec.get("findings", []))
                sr.risk_score = rec.get("risk_score", 0)
                sr.details["recon"] = {
                    "technologies": len(rec.get("technologies", [])),
                    "subdomains": len(rec.get("subdomains", [])),
                    "risk_score": sr.risk_score,
                    "findings": sr.findings_count,
                    "attack_vectors": len(rec.get("attack_vectors", [])),
                    "ai_endpoints_detected": bool(rec.get("ai_endpoints", {}).get("detected")),
                    "supply_chain_scripts": len(rec.get("supply_chain", {}).get("third_party_scripts", [])),
                }
                if target.must_detect:
                    ar = _check_assertions(target, rec)
                    sr.assertions_passed = ar["passed"]
                    sr.assertions_failed = ar["failed"]
                if target.min_risk_score > 0:
                    sr.risk_score_ok = sr.risk_score >= target.min_risk_score

                if verbose and not json_output and S:
                    score_color = S.success if sr.risk_score_ok else S.error
                    print(f"    Recon: {sr.details['recon']['technologies']} techs, "
                          f"risk={score_color}{sr.risk_score}{S.reset}/100, "
                          f"{sr.details['recon']['attack_vectors']} vectors {S.success}✓{S.reset}")
                    for a in sr.assertions_passed:
                        print(f"      {S.success}✓{S.reset} {a}")
                    for a in sr.assertions_failed:
                        print(f"      {S.error}✗{S.reset} {a}  {S.dim}(not detected){S.reset}")
                    if not sr.risk_score_ok:
                        print(f"      {S.warning}⚠{S.reset} risk {sr.risk_score} < min {target.min_risk_score}")
            else:
                sr.error = rec.get("error", "recon failed")

        # Phase 3 — Payload test (full mode, qa only)
        if mode == "full" and not sr.error and target.zone == "qa":
            tst = _run_test(target, category="xss", max_payloads=5)
            if "error" not in tst and "skipped" not in tst:
                sr.test_ok = True
                sr.details["test"] = tst
                if verbose and not json_output and S:
                    print(f"    Test: {tst.get('total',0)} payloads, "
                          f"{tst.get('passed',0)} passed, "
                          f"{tst.get('blocked',0)} blocked {S.success}✓{S.reset}")

        sr.duration_s = round(time.time() - t0, 1)
        sr.status = ("error" if sr.error
                     else "fail" if (sr.assertions_failed or not sr.risk_score_ok)
                     else "pass")

        if verbose and not json_output and S:
            color = {"pass": S.success, "fail": S.warning, "error": S.error}.get(sr.status, S.dim)
            label = {"pass": "PASS", "fail": "FAIL", "error": "ERR"}.get(sr.status, sr.status.upper())
            print(f"    {color}{label}{S.reset} ({sr.duration_s}s)\n")

        results.append(sr)

    # ── Summary ──────────────────────────────────────────────────────────────
    passed  = sum(1 for r in results if r.status == "pass")
    failed  = sum(1 for r in results if r.status == "fail")
    errored = sum(1 for r in results if r.status == "error")
    waf_matches = sum(1 for r in results if r.waf_match)
    total_time = sum(r.duration_s for r in results)
    all_gaps = [f"{r.name}: {a}" for r in results for a in r.assertions_failed]

    if verbose and not json_output and S:
        print(f"  {S.dim}{'━' * 60}{S.reset}")
        print(f"  {S.bold}Results:{S.reset} "
              f"{S.success}{passed} passed{S.reset}  "
              f"{S.warning}{failed} failed{S.reset}  "
              f"{S.error}{errored} errors{S.reset}  "
              f"({total_time:.0f}s)")
        if all_gaps:
            print(f"\n  {S.bold}{S.warning}Detection gaps (fix these):{S.reset}")
            for gap in all_gaps:
                print(f"    {S.error}✗{S.reset} {gap}")
        print()

    if json_output:
        print(json.dumps({
            "version": __version__,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "zone": zone,
            "mode": mode,
            "targets": len(results),
            "passed": passed,
            "failed": failed,
            "errored": errored,
            "waf_accuracy": f"{waf_matches}/{len(results)}",
            "detection_gaps": all_gaps,
            "total_time_s": round(total_time, 1),
            "results": [asdict(r) for r in results],
        }, indent=2, default=str))

    # ── #298 Persist smoke history ────────────────────────────────────────────
    _persist_smoke_history(zone, mode, results, passed, failed, errored, all_gaps, total_time)

    return results


def _persist_smoke_history(
    zone: str, mode: str, results: List["SmokeResult"],
    passed: int, failed: int, errored: int,
    gaps: List[str], total_time: float,
) -> None:
    """#298 — Append this run to ~/.fray/smoke_history.json.

    Keeps the last 100 runs per zone. Used to track detection accuracy
    over time and surface regressions (e.g. Juice Shop XSS used to pass
    but now fails after a code change).
    """
    history_path = Path.home() / ".fray" / "smoke_history.json"
    try:
        history_path.parent.mkdir(parents=True, exist_ok=True)
        history: dict = {}
        if history_path.exists():
            try:
                history = json.loads(history_path.read_text())
            except Exception:
                history = {}

        run_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "zone": zone,
            "mode": mode,
            "passed": passed,
            "failed": failed,
            "errored": errored,
            "total_time_s": round(total_time, 1),
            "detection_gaps": gaps,
            "per_target": [
                {
                    "name": r.name,
                    "zone": r.zone,
                    "status": r.status,
                    "risk_score": r.risk_score,
                    "assertions_passed": r.assertions_passed,
                    "assertions_failed": r.assertions_failed,
                    "duration_s": r.duration_s,
                }
                for r in results
            ],
        }

        zone_key = zone
        if zone_key not in history:
            history[zone_key] = []
        history[zone_key].append(run_record)
        # Keep last 100 runs per zone
        history[zone_key] = history[zone_key][-100:]

        history_path.write_text(json.dumps(history, indent=2, default=str))
    except Exception:
        pass  # Never fail a smoke run because history write fails


# ── CLI entry point ──────────────────────────────────────────────────────────

def cmd_smoke(args):
    """CLI handler for 'fray smoke'."""
    mode       = "full" if getattr(args, "full", False) else "quick"
    llm        = getattr(args, "llm", False)
    all_z      = getattr(args, "all", False)
    real       = getattr(args, "real", False)
    local      = getattr(args, "local", False)
    json_out   = getattr(args, "json", False)
    zone       = ("all"         if all_z
                  else "llm_zone"    if llm
                  else "real_domain" if real
                  else "local"       if local
                  else "qa")

    results = run_smoke_test(zone=zone, mode=mode, verbose=True, json_output=json_out)
    return 1 if any(r.status != "pass" for r in results) else 0
