"""v11 Recon Report HTML builder — called by SecurityReportGenerator._build_recon_html_v11()."""
import html as _html
import ipaddress as _ipaddr
import re as _re_mod
from typing import Dict, Any, List, Optional
from fray._report_css import CSS, SEV_COLORS, LOGO_SVG, risk_color, risk_grade, gauge_svg, donut_svg
from fray.share_status import share_status as _share_status

_esc = _html.escape


# ── Tech name normalization ────────────────────────────────────────────────

# Maps raw fingerprint keys → human-readable display names
_TECH_DISPLAY_NAMES = {
    # AWS services
    'aws_s3': 'AWS S3', 'aws_ec2': 'AWS EC2', 'aws_elb': 'AWS ELB',
    'aws_cloudfront': 'AWS CloudFront', 'aws_rds': 'AWS RDS',
    'aws_lambda': 'AWS Lambda', 'aws_route53': 'AWS Route 53',
    'aws_waf': 'AWS WAF', 'amazonses': 'Amazon SES',
    # Azure
    'azure_blob': 'Azure Blob', 'azure_cdn': 'Azure CDN',
    'azure_front_door': 'Azure Front Door', 'azure_waf': 'Azure WAF',
    'azure_functions': 'Azure Functions',
    # GCP
    'gcs': 'Google Cloud Storage', 'gcp_cdn': 'Google Cloud CDN',
    'google_cloud_armor': 'Google Cloud Armor',
    # CDN / WAF
    'cloudflare_waf': 'Cloudflare WAF', 'cloudflare_cdn': 'Cloudflare CDN',
    'akamai_kona': 'Akamai Kona WAF', 'akamai_cdn': 'Akamai CDN',
    'fastly_waf': 'Fastly WAF', 'fastly_cdn': 'Fastly CDN',
    # Servers
    'nginx': 'Nginx', 'apache': 'Apache', 'iis': 'Microsoft IIS',
    'tomcat': 'Apache Tomcat', 'jetty': 'Jetty',
    'litespeed': 'LiteSpeed', 'caddy': 'Caddy',
    # Languages / runtimes
    'nodejs': 'Node.js', 'php': 'PHP', 'python': 'Python',
    'ruby': 'Ruby', 'java': 'Java', 'golang': 'Go',
    'dotnet': '.NET', 'aspnet': 'ASP.NET',
    # Databases
    'mysql': 'MySQL', 'postgresql': 'PostgreSQL', 'mongodb': 'MongoDB',
    'redis': 'Redis', 'elasticsearch': 'Elasticsearch',
    'oracle': 'Oracle DB', 'oracledb': 'Oracle DB', 'oracle_database': 'Oracle DB',
    'mariadb': 'MariaDB', 'sqlite': 'SQLite', 'cassandra': 'Cassandra',
    'dynamodb': 'AWS DynamoDB', 'firestore': 'Google Firestore',
    # Storage / Object Storage
    'wasabi': 'Wasabi Hot Cloud Storage', 'wasabi_s3': 'Wasabi Hot Cloud Storage',
    'oracle_oci': 'Oracle Cloud Object Storage', 'oraclecloud': 'Oracle Cloud',
    'sakura_cloud': 'Sakura Cloud', 'sakuracloud': 'Sakura Internet',
    'sakura_object_storage': 'Sakura Object Storage',
    'linode_objects': 'Linode Object Storage', 'linodeobjects': 'Linode Object Storage',
    'vultr_objects': 'Vultr Object Storage',
    'minio': 'MinIO',
    'tencent_cos': 'Tencent Cloud COS', 'myqcloud': 'Tencent Cloud COS',
    'huawei_obs': 'Huawei OBS', 'obs': 'Huawei OBS',
    # CMS
    'wordpress': 'WordPress', 'drupal': 'Drupal', 'joomla': 'Joomla',
    'shopify': 'Shopify', 'magento': 'Magento',
}


def _normalize_tech_name(name: str) -> str:
    """Convert raw fingerprint key (e.g. 'aws_s3') to human-readable label."""
    if not name:
        return name
    # Direct lookup
    lower = name.lower().replace('-', '_')
    if lower in _TECH_DISPLAY_NAMES:
        return _TECH_DISPLAY_NAMES[lower]
    # Already human-readable (contains spaces or proper casing)
    if ' ' in name or (name != name.lower() and '_' not in name):
        return name
    # Underscores → spaces + title case as fallback
    return name.replace('_', ' ').replace('-', ' ').title()


# ── Finding Deduplication + Contextual Severity ──────────────────────────

_CATEGORY_BASE_SCORES = {
    "rce": 45, "command_injection": 45, "cmdi": 40,
    "sqli": 35, "sql_injection": 35,
    "ssrf": 30, "ssti": 35, "xxe": 30,
    "path_traversal": 25, "lfi": 25,
    "xss": 20, "dom_xss": 22,
    "cors": 18, "csrf": 15,
    "idor": 20, "open_redirect": 12,
    "info_disclosure": 8, "header_missing": 5,
}


def contextual_severity(finding: Dict, recon_data: Optional[Dict] = None) -> tuple:
    """Calculate contextual severity based on finding + recon context.

    Returns (severity_label: str, score: int).
    """
    score = 0
    category = finding.get("category", finding.get("type", "")).lower().replace(" ", "_")
    score += _CATEGORY_BASE_SCORES.get(category, 10)

    if not finding.get("authenticated", True):
        score += 20
    if finding.get("waf_mode") == "monitoring":
        score += 10
    if finding.get("injection_context") in ("header", "cookie"):
        score += 5

    if recon_data:
        headers = recon_data.get("headers", {})
        if headers.get("missing", {}):
            csp_missing = "Content-Security-Policy" in headers.get("missing", {})
            if csp_missing:
                score += 8
        cors = recon_data.get("cors", {})
        if cors.get("misconfigured"):
            score += 10

    if score >= 70:
        return ("CRITICAL", score)
    elif score >= 50:
        return ("HIGH", score)
    elif score >= 30:
        return ("MEDIUM", score)
    return ("LOW", score)


def deduplicate_findings(findings: List[Dict],
                         recon_data: Optional[Dict] = None) -> List[Dict]:
    """Deduplicate findings: same endpoint + category = 1 finding with variants.

    Args:
        findings: List of finding dicts.
        recon_data: Optional recon result for contextual severity.

    Returns:
        Deduplicated list sorted by severity (highest first).
    """
    from collections import defaultdict

    groups: Dict[tuple, List[Dict]] = defaultdict(list)
    for f in findings:
        url = f.get("url", f.get("target", ""))
        # Normalize: strip query params for grouping
        base_url = url.split("?")[0] if url else ""
        cat = f.get("category", f.get("type", "unknown")).lower()
        ctx = f.get("injection_context", "url_param")
        key = (base_url, cat, ctx)
        groups[key].append(f)

    deduped = []
    for (url, cat, ctx), group in groups.items():
        # Pick the highest-severity example as lead
        lead = dict(group[0])
        sev_label, sev_score = contextual_severity(lead, recon_data)
        lead["severity"] = sev_label
        lead["severity_score"] = sev_score
        lead["variant_count"] = len(group)
        if len(group) > 1:
            lead["all_payloads"] = [g.get("payload", "") for g in group if g.get("payload")]
        deduped.append(lead)

    deduped.sort(key=lambda x: x.get("severity_score", 0), reverse=True)
    return deduped


def _targets_chips(items, limit=5):
    """Render a list of target URLs as code chips, with overflow."""
    chips = ''
    for t in items[:limit]:
        url = t if isinstance(t, str) else t.get('target', t.get('url', str(t)))
        chips += f'<code style="background:var(--surface2);padding:2px 8px;border-radius:4px;font-size:0.85em;">{_esc(str(url))}</code> '
    if len(items) > limit:
        chips += f'<span class="muted">+ {len(items) - limit} more</span>'
    return chips


def _method_upgrade_tip(mode: str, target: str) -> str:
    """Return a tip suggesting deeper scan profiles when applicable."""
    if mode in ('deep', 'bounty', 'stealth'):
        return ''
    tips = {
        'default':  ('deep', 'Deep scan includes historical URL crawling, JavaScript analysis, parameter discovery, and extended admin panel enumeration — recommended for thorough assessments.'),
        'standard': ('deep', 'Deep scan includes historical URL crawling, JavaScript analysis, parameter discovery, and extended admin panel enumeration — recommended for thorough assessments.'),
        'quick':    ('standard', 'Standard scan adds admin panel enumeration, rate-limit testing, and WAF gap analysis. For maximum coverage, use <code>--profile bounty</code>.'),
        'fast':     ('standard', 'Standard scan adds admin panel enumeration, rate-limit testing, and WAF gap analysis. For maximum coverage, use <code>--profile bounty</code>.'),
        'api':      ('bounty', 'Bounty profile adds full subdomain probing, admin panel enumeration, and extended attack surface analysis.'),
    }
    rec = tips.get(mode)
    if not rec:
        return ''
    profile, desc = rec
    cmd = f'fray recon {_esc(target)} --profile {profile}'
    return (f'<div style="margin-top:14px;background:var(--surface2);border-radius:10px;padding:14px 18px;'
            f'border-left:3px solid var(--accent);">'
            f'<p style="font-size:0.88em;margin-bottom:6px;"><strong style="color:var(--accent2);">'
            f'Want deeper results?</strong> {desc}</p>'
            f'<code style="background:var(--surface);padding:6px 12px;border-radius:6px;font-size:0.88em;">'
            f'{cmd}</code></div>')


def build(rd: Dict[str, Any], share_url: Optional[str] = None) -> str:
    host = rd.get('host', 'Unknown')
    target = rd.get('target', f'https://{host}')
    ts = rd.get('timestamp', '')
    # Always show UTC suffix so users know the timezone
    ts_short = (ts[:16].replace('T', ' ') + ' UTC') if ts else '—'
    scan_mode = rd.get('mode', 'default')
    _PROFILE_LABELS = {
        'default': 'Standard', 'standard': 'Standard', 'quick': 'Quick',
        'deep': 'Deep', 'stealth': 'Stealth', 'api': 'API-Focused',
        'bounty': 'Bounty (Max Coverage)', 'fast': 'Fast',
    }
    _profile_label = _PROFILE_LABELS.get(scan_mode, scan_mode.title())

    atk = rd.get('attack_surface', {})
    risk_score = atk.get('risk_score', 0)
    risk_level = atk.get('risk_level', '?')
    findings = atk.get('findings', [])
    n_findings = len(findings)
    n_crit = sum(1 for f in findings if f.get('severity') == 'critical')
    n_high = sum(1 for f in findings if f.get('severity') == 'high')
    n_med = sum(1 for f in findings if f.get('severity') == 'medium')
    n_low = sum(1 for f in findings if f.get('severity') == 'low')

    gap = rd.get('gap_analysis', {}) or {}
    _waf_single = gap.get('waf_vendor') or atk.get('waf_vendor') or '—'
    _cdn_single = rd.get('dns', {}).get('cdn_detected') or atk.get('cdn') or '—'
    tls_data = rd.get('tls', {}) or {}
    tls_ver = tls_data.get('tls_version', '—')
    cert_days = tls_data.get('cert_days_remaining', '—')
    cert_issuer = tls_data.get('cert_issuer') or tls_data.get('issuer', '—')

    hdrs = rd.get('headers', {}) or {}
    hdr_score = hdrs.get('score', 0)
    hdr_value_issues = hdrs.get('value_issues', [])
    present_hdrs = hdrs.get('present', {})
    if not isinstance(present_hdrs, dict):
        present_hdrs = {h: {} for h in present_hdrs} if isinstance(present_hdrs, list) else {}
    missing_hdrs = hdrs.get('missing', {})
    if not isinstance(missing_hdrs, dict):
        missing_hdrs = {h: {} for h in missing_hdrs} if isinstance(missing_hdrs, list) else {}

    # WAF mode (blocking/monitoring/no_waf) from differential analysis
    _diff_data = rd.get('differential', {}) or {}
    _waf_mode = _diff_data.get('waf_mode', '')

    # CORS data
    _cors_data = rd.get('cors', {}) or {}
    _cors_issues = _cors_data.get('issues', [])
    _cors_misconfigured = _cors_data.get('misconfigured', False)

    # TLS cert org from detector
    _tls_cert = rd.get('tls_cert', {}) or {}
    _tls_cert_issuer = _tls_cert.get('issuer_org', '')
    _tls_cert_waf_hint = _tls_cert.get('waf_hint', '')

    subs_data = rd.get('subdomains', {}) or {}
    sub_list = subs_data.get('subdomains', []) if isinstance(subs_data, dict) else []
    n_subs = len(sub_list) if isinstance(sub_list, list) else 0
    sub_sources = subs_data.get('sources', {}) if isinstance(subs_data, dict) else {}

    attack_vectors = atk.get('attack_vectors', [])
    attack_targets = atk.get('attack_targets', [])
    n_attack_targets = len(attack_targets)

    csp_data = rd.get('csp', {}) or {}
    csp_present = csp_data.get('present', False) if isinstance(csp_data, dict) else False
    csp_score = csp_data.get('score', 0) if isinstance(csp_data, dict) else 0
    csp_bypasses = csp_data.get('bypass_techniques', []) if isinstance(csp_data, dict) else []

    admin_data = rd.get('admin_panels', {}) or {}
    admin_panels = (admin_data.get('panels_found', []) or admin_data.get('found', []) or
                    admin_data.get('panels', [])) if isinstance(admin_data, dict) else []
    n_admin = len(admin_panels)
    # Show paths probed count (136 paths in default wordlist) — not just found
    from fray.recon.checks import _ADMIN_PATHS as _admin_wordlist
    n_admin_checked = len(_admin_wordlist)

    cloud_dist = rd.get('cloud_distribution', {}) or {}
    per_sub = cloud_dist.get('per_subdomain', [])
    waf_bypass_subs = cloud_dist.get('waf_bypass_subdomains', [])

    # Build WAF/CDN display labels — prefer multi-vendor summary when applicable
    _waf_dist = cloud_dist.get('waf_distribution', {})
    _cdn_dist = cloud_dist.get('cdn_distribution', {})
    if _waf_dist and len(_waf_dist) > 1:
        waf_vendor = 'Multi-WAF: ' + ', '.join(sorted(_waf_dist.keys()))
    elif _waf_dist and len(_waf_dist) == 1:
        waf_vendor = next(iter(_waf_dist.keys()))
    else:
        waf_vendor = _waf_single
    if _cdn_dist and len(_cdn_dist) > 1:
        cdn_vendor = 'Multi-CDN: ' + ', '.join(sorted(_cdn_dist.keys()))
    elif _cdn_dist and len(_cdn_dist) == 1:
        cdn_vendor = next(iter(_cdn_dist.keys()))
    else:
        cdn_vendor = _cdn_single

    probes = rd.get('subdomain_probes', {}) or {}
    probe_results = probes.get('results', []) if isinstance(probes, dict) else []
    n_probes = probes.get('total', 0) if isinstance(probes, dict) else 0
    n_responsive = probes.get('responsive', 0) if isinstance(probes, dict) else 0

    dns = rd.get('dns', {}) or {}
    fp = rd.get('fingerprint', {}) or {}
    techs = fp.get('technologies', {})
    fl = rd.get('frontend_libs', {}) or {}
    fl_vulns = fl.get('vulnerabilities', []) if isinstance(fl, dict) else []
    n_vuln_libs = fl.get('vulnerable_libs', 0) if isinstance(fl, dict) else 0

    origin_ips_data = rd.get('origin_ips', {}) or {}
    origin_list = origin_ips_data.get('candidates', []) if isinstance(origin_ips_data, dict) else []

    rec_cats = rd.get('recommended_categories', [])
    gap_findings = gap.get('findings', []) if isinstance(gap, dict) else []
    rate_limit = rd.get('rate_limits', rd.get('rate_limit', {})) or {}
    remediation = atk.get('remediation', [])
    staging_envs = atk.get('staging_envs', [])
    checks = rd.get('security_checks', {}) or {}

    # VPN endpoints
    vpn_data = rd.get('vpn_endpoints', {}) or {}
    vpn_list = vpn_data.get('vpn_endpoints', []) if isinstance(vpn_data, dict) else []
    vpn_cve_findings = vpn_data.get('cve_findings', []) if isinstance(vpn_data, dict) else []
    n_vpn = len(vpn_list)

    # API security
    api_sec = rd.get('api_security', {}) or {}
    api_specs = api_sec.get('specs', api_sec.get('exposed_specs', api_sec.get('specs_found', []))) if isinstance(api_sec, dict) else []
    api_endpoints = api_sec.get('endpoints', api_sec.get('api_endpoints', [])) if isinstance(api_sec, dict) else []
    api_gw = api_sec.get('api_gateway', api_sec.get('gateway_info', {})) if isinstance(api_sec, dict) else {}
    api_rate = api_sec.get('rate_limiting', api_sec.get('rate_limit_info', {})) if isinstance(api_sec, dict) else {}
    api_auth = api_sec.get('authentication', api_sec.get('auth_info', {})) if isinstance(api_sec, dict) else {}
    api_schema = api_sec.get('schema_validation', {}) if isinstance(api_sec, dict) else {}
    api_security_vendors = api_sec.get('security_vendors', {}) if isinstance(api_sec, dict) else {}
    api_posture = api_sec.get('security_posture', 'unknown') if isinstance(api_sec, dict) else 'unknown'
    api_controls = api_sec.get('security_controls', []) if isinstance(api_sec, dict) else []
    api_oidc = api_sec.get('oidc', {}) if isinstance(api_sec, dict) else {}
    n_api_specs = api_sec.get('total_specs', len(api_specs) if isinstance(api_specs, list) else 0)

    # Cloud buckets
    bucket_data = rd.get('cloud_buckets', {}) or {}
    bucket_list = bucket_data.get('buckets', []) if isinstance(bucket_data, dict) else []
    n_buckets = bucket_data.get('total_found', len(bucket_list)) if isinstance(bucket_data, dict) else 0
    n_public_buckets = bucket_data.get('total_public', 0) if isinstance(bucket_data, dict) else 0

    # Per-subdomain security
    sub_sec = rd.get('subdomain_security', {}) or {}

    # Emoji map for attack vectors
    _VEC_EMOJI = {
        'WAF Bypass': '\U0001f6e1\ufe0f', 'Unprotected Subdomain': '\U0001f310',
        'Account Takeover': '\U0001f511', 'API Vulnerability': '\U0001f50c',
        'LLM / AI Prompt Injection': '\U0001f916', 'Payment / Financial Abuse': '\U0001f4b3',
        'Staging / Dev Environment': '\U0001f9ea', 'DDoS / L7 Denial of Service': '\u26a1',
        'Web Cache Poisoning': '\U0001f4be', 'DDoS \u2014 Direct Origin': '\u26a1',
    }

    # VPN vendor display
    vpn_vendors = [v.get('label', '') for v in vpn_list] if vpn_list else []
    if vpn_vendors:
        vpn_display = ', '.join(v.split('(')[0].strip() for v in vpn_vendors[:2])
        if len(vpn_vendors) > 2:
            vpn_display += f' +{len(vpn_vendors) - 2}'
    else:
        vpn_display = ''
    vpn_has_cves = bool(vpn_data.get('verified_cves') or vpn_data.get('potential_cves'))

    # API gateway display
    _GW_VENDOR_LABELS = {
        'x-amzn-requestid':              'AWS API Gateway',
        'x-kong-proxy-latency':          'Kong',
        'x-kong-upstream-latency':       'Kong',
        'x-envoy-upstream-service-time': 'Envoy / Istio',
        'x-goog-api-client':             'Google Cloud API Gateway',
        'cf-apim':                       'Cloudflare API Shield',
        'x-request-id':                  'API Gateway (generic)',
        'traceparent':                   'OpenTelemetry (distributed tracing)',
    }
    api_gw_display = ''
    if isinstance(api_gw, dict) and api_gw.get('detected'):
        gw_names = []
        for k, info in api_gw.items():
            if k == 'detected' or not isinstance(info, dict):
                continue
            vendor = info.get('vendor') or _GW_VENDOR_LABELS.get(k.lower()) or k
            # Skip raw header key names that aren't human-readable (contain dashes, no spaces)
            if vendor and (' ' in vendor or not vendor.startswith('x-')):
                gw_names.append(vendor)
        # Deduplicate while preserving order
        seen_gw = set()
        unique_gw = [n for n in gw_names if not (n in seen_gw or seen_gw.add(n))]
        api_gw_display = ', '.join(unique_gw[:2]) if unique_gw else 'Detected'

    rc = risk_color(risk_score)
    hdr_color = 'var(--red)' if hdr_score < 30 else 'var(--yellow)' if hdr_score < 60 else 'var(--green)'

    # ── Pieces ──
    parts = []
    _COPY_CSS = '''
.cmd-wrap{position:relative;display:flex;align-items:center;width:100%;overflow:hidden;}
.cmd-wrap code{padding-right:3em!important;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;min-width:0;}
.copy-btn{position:absolute;right:4px;top:50%;transform:translateY(-50%);flex-shrink:0;
  background:rgba(99,102,241,0.15);border:1px solid rgba(99,102,241,0.3);
  color:var(--accent2,var(--accent2));border-radius:4px;cursor:pointer;font-size:0.72em;
  padding:2px 6px;white-space:nowrap;transition:all 0.15s;line-height:1.4;
  font-family:inherit;z-index:1;}
.copy-btn:hover{background:var(--accent,var(--accent));color:#fff;border-color:var(--accent,var(--accent));}
.copy-btn.copied{background:var(--green);color:#fff;border-color:var(--green);}
'''
    _COPY_JS = '''
<script>
function _fray_copy(btn){
  var code=btn.closest('.cmd-wrap').querySelector('code');
  if(!code)return;
  var txt=code.textContent||code.innerText||'';
  navigator.clipboard.writeText(txt.trim()).then(function(){
    btn.textContent='✓ copied';btn.classList.add('copied');
    setTimeout(function(){btn.textContent='copy';btn.classList.remove('copied');},1800);
  }).catch(function(){
    // Fallback for older browsers
    var ta=document.createElement('textarea');
    ta.value=txt.trim();ta.style.position='fixed';ta.style.opacity='0';
    document.body.appendChild(ta);ta.select();
    try{document.execCommand('copy');btn.textContent='✓ copied';btn.classList.add('copied');
      setTimeout(function(){btn.textContent='copy';btn.classList.remove('copied');},1800);}
    catch(e){}finally{document.body.removeChild(ta);}
  });
}
// Wrap all fray command <code> blocks with copy button on load
document.addEventListener('DOMContentLoaded',function(){
  document.querySelectorAll('code').forEach(function(c){
    var txt=(c.textContent||'').trim();
    if(!txt.startsWith('fray '))return;
    if(c.closest('.cmd-wrap'))return;  // already wrapped
    var wrap=document.createElement('span');
    wrap.className='cmd-wrap';
    c.parentNode.insertBefore(wrap,c);
    wrap.appendChild(c);
    var btn=document.createElement('button');
    btn.className='copy-btn';btn.textContent='copy';
    btn.setAttribute('onclick','_fray_copy(this)');
    wrap.appendChild(btn);
  });
});
</script>
'''
    parts.append(f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
                 f'<meta name="viewport" content="width=device-width,initial-scale=1.0">'
                 f'<title>Attack Surface Intelligence — {_esc(host)} — Fray</title>'
                 f'<style>{CSS}{_COPY_CSS}</style></head><body><div class="wrap">')
    parts.append(_COPY_JS)

    # Header
    share_chip = ''
    _share_meta = rd.get('_share', {}) if isinstance(rd.get('_share'), dict) else {}
    if share_url:
        esc_share = _esc(share_url)
        expires_at = _share_meta.get('expires_at') or ''
        status = _share_status(expires_at) if expires_at else {"label": "expiry unknown", "state": "neutral"}
        pill_color = {
            'expired': 'rgba(244,63,94,0.15)',
            'warn': 'rgba(234,179,8,0.15)',
            'ok': 'rgba(34,197,94,0.15)',
        }.get(status['state'], 'rgba(255,255,255,0.1)')
        pill_border = {
            'expired': 'rgba(244,63,94,0.5)',
            'warn': 'rgba(234,179,8,0.5)',
            'ok': 'rgba(34,197,94,0.4)',
        }.get(status['state'], 'rgba(255,255,255,0.2)')
        share_chip = (
            '<div style="display:flex;flex-direction:column;gap:8px;align-items:flex-end">'
            '  <a href="{url}" target="_blank" '
            '     style="display:inline-flex;align-items:center;gap:6px;'
            '     padding:10px 14px;border-radius:10px;background:var(--surface2);'
            '     border:1px solid var(--border);font-size:0.85em;font-weight:600;'
            '     color:var(--accent2);text-decoration:none;">🔗 Public Snapshot</a>'
            '  <span style="font-size:0.75em;padding:4px 10px;border-radius:999px;'
            '     border:1px solid {border};background:{bg};color:#fff;letter-spacing:0.05em;">'
            '    {label}'
            '  </span>'
            '</div>'
        ).format(url=esc_share, bg=pill_color, border=pill_border, label=_esc(status['label']))

    parts.append(f'''
<div class="hdr">
  <div>
    {LOGO_SVG}
    <div style="margin-top:14px;font-size:0.7em;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.5);">Attack Surface Intelligence</div>
    <h1 style="margin-top:4px;font-size:2.4em;font-weight:800;letter-spacing:-1px;">{_esc(host)}</h1>
    <div class="sub" style="margin-top:6px;">{_esc(ts_short)} — Profile: {_esc(_profile_label)}</div>
  </div>
  <div style="display:flex;align-items:center;gap:24px;flex-wrap:wrap;">
    <div class="rbadge">{gauge_svg(risk_score)}</div>
    {share_chip}
  </div>
</div>''')

    # Dashboard
    donut = donut_svg([n_crit, n_high, n_med, n_low],
                      ['var(--red)', 'var(--orange)', 'var(--yellow)', 'var(--green)'], n_findings)
    legend = ''
    for cnt, col, nm in zip([n_crit, n_high, n_med, n_low],
                            ['var(--red)', 'var(--orange)', 'var(--yellow)', 'var(--green)'],
                            ['Critical', 'High', 'Medium', 'Low']):
        if cnt > 0:
            legend += f'<div style="display:flex;align-items:center;gap:6px;font-size:0.85em;"><span style="width:10px;height:10px;border-radius:50%;background:{col};display:inline-block;"></span><strong>{nm}:</strong> {cnt}</div>'

    parts.append(f'''
<div style="display:flex;gap:20px;flex-wrap:wrap;margin-bottom:24px;align-items:stretch;">
  <div style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:24px;display:flex;align-items:center;gap:20px;flex:0 0 auto;">
    {donut}
    <div style="display:flex;flex-direction:column;gap:6px;">{legend}</div>
  </div>
  <div style="flex:1;min-width:300px;display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:12px;">
    <div class="mc"><div class="l">WAF{' <span style="font-size:0.6em;padding:2px 6px;border-radius:4px;background:' + ('var(--red)' if _waf_mode == 'monitoring' else 'var(--green)' if _waf_mode == 'blocking' else 'var(--surface2)') + ';color:white;vertical-align:middle;margin-left:4px;">' + _esc(_waf_mode or 'unknown') + '</span>' if _waf_mode else ''}</div><div class="v" style="font-size:0.85em;word-break:break-word;">{_esc(str(waf_vendor))[:120]}</div></div>
    <div class="mc"><div class="l">CDN</div><div class="v" style="font-size:0.85em;word-break:break-word;">{_esc(str(cdn_vendor))[:120]}</div></div>
    <div class="mc"><div class="l">TLS</div><div class="v">{_esc(str(tls_ver))}</div></div>
    <div class="mc"><div class="l">Headers Score</div><div class="v" style="color:{hdr_color};">{hdr_score}/100</div></div>
    <div class="mc"><div class="l">Subdomains</div><div class="v">{n_subs}</div></div>
    <div class="mc"><div class="l">Attack Targets</div><div class="v" style="color:var(--orange);">{n_attack_targets}</div></div>
    <div class="mc"><div class="l">Attack Vectors</div><div class="v" style="color:var(--red);">{len(attack_vectors)}</div></div>
    <div class="mc"><div class="l">Admin Panels</div><div class="v">{n_admin}</div></div>
    {f'<div class="mc"><div class="l">VPN Vendor</div><div class="v" style="font-size:0.85em;color:{"var(--red)" if vpn_has_cves else "var(--orange)"};"><a href="#vpn" style="color:inherit;text-decoration:none;">{_esc(vpn_display)}</a></div></div>' if vpn_display else ''}
    {f'<div class="mc"><div class="l">API Gateway</div><div class="v" style="font-size:0.85em;color:var(--cyan);"><a href="#apisec" style="color:inherit;text-decoration:none;">{_esc(api_gw_display)}</a></div></div>' if api_gw_display else ''}
    {f'<div class="mc"><div class="l">Public Buckets</div><div class="v" style="color:var(--red);"><a href="#buckets" style="color:inherit;text-decoration:none;">{n_public_buckets}</a></div></div>' if n_public_buckets else ''}
  </div>
</div>''')

    # TOC
    parts.append('''
<nav style="background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:20px 24px;margin-bottom:24px;">
  <div style="font-size:0.75em;font-weight:700;color:var(--muted);letter-spacing:1px;margin-bottom:12px;">REPORT NAVIGATION</div>
  <div style="display:flex;flex-wrap:wrap;gap:20px;">
    <div><div style="font-size:0.72em;font-weight:600;color:var(--accent2);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Overview</div>
      <div style="display:flex;flex-wrap:wrap;gap:5px;"><a href="#exec" class="toc-link">Summary</a><a href="#methodology" class="toc-link">Methodology</a><a href="#findings" class="toc-link">Findings</a><a href="#remediation" class="toc-link">Remediation</a></div></div>
    <div><div style="font-size:0.72em;font-weight:600;color:var(--red);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Threats</div>
      <div style="display:flex;flex-wrap:wrap;gap:5px;"><a href="#vectors" class="toc-link">Attack Vectors</a><a href="#priorities" class="toc-link">Priorities</a><a href="#cves" class="toc-link">CVEs</a><a href="#checks" class="toc-link">Security Checks</a></div></div>
    <div><div style="font-size:0.72em;font-weight:600;color:var(--cyan);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Infrastructure</div>
      <div style="display:flex;flex-wrap:wrap;gap:5px;"><a href="#headers" class="toc-link">Headers</a><a href="#csp" class="toc-link">CSP</a><a href="#tech" class="toc-link">Tech</a><a href="#dns" class="toc-link">DNS</a><a href="#waf-cdn" class="toc-link">WAF/CDN</a><a href="#gap" class="toc-link">Gap Analysis</a><a href="#rl" class="toc-link">Rate Limits</a><a href="#vpn" class="toc-link">VPN</a><a href="#apisec" class="toc-link">API Security</a><a href="#buckets" class="toc-link">Cloud Buckets</a></div></div>
    <div><div style="font-size:0.72em;font-weight:600;color:var(--orange);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px;">Targets</div>
      <div style="display:flex;flex-wrap:wrap;gap:5px;"><a href="#subs" class="toc-link">Subdomains</a><a href="#probes" class="toc-link">Probes</a><a href="#origin" class="toc-link">Origin IPs</a><a href="#admin" class="toc-link">Admin Panels</a><a href="#hvt" class="toc-link">HVT</a><a href="#tests" class="toc-link">Tests</a><a href="#cats" class="toc-link">Categories</a></div></div>
  </div>
</nav>''')

    # Executive Summary
    sp = []
    sp.append(f'Fray performed automated reconnaissance of <strong>{_esc(host)}</strong> '
              f'and assessed the external attack surface at <strong style="color:{rc};">'
              f'{_esc(risk_level)} risk ({risk_score}/100)</strong>, corresponding to a '
              f'security grade of <strong style="color:{rc};">{risk_grade(risk_score)}</strong>. '
              f'A total of <strong>{n_findings}</strong> finding(s) were identified'
              + (f' across <strong>{n_attack_targets}</strong> prioritised attack targets.' if n_attack_targets else '.'))
    if waf_vendor and waf_vendor != '—':
        sp.append(f'The target infrastructure is protected by <strong>{_esc(str(waf_vendor))}</strong> WAF'
                  + (f', served via <strong>{_esc(str(cdn_vendor))}</strong> CDN' if cdn_vendor and cdn_vendor != '—' else '')
                  + f', TLS {_esc(str(tls_ver))}.')
    else:
        sp.append('<span style="color:var(--red);font-weight:700;">No WAF was detected — the application is directly exposed.</span>')

    n_waf_bypass = len(waf_bypass_subs)
    n_unprotected = sum(1 for s in per_sub if not s.get('waf') and not s.get('cdn'))
    n_staging = len(staging_envs) if isinstance(staging_envs, list) else 0
    vb = []
    if n_waf_bypass:
        vb.append(f'<li><strong style="color:var(--red);">{n_waf_bypass} subdomain(s) bypass WAF</strong> — attackers can reach origin servers directly</li>')
    if n_unprotected:
        vb.append(f'<li><strong style="color:var(--orange);">{n_unprotected} subdomain(s) have no CDN/WAF</strong> — exposed without edge protection</li>')
    if n_staging:
        vb.append(f'<li><strong style="color:var(--yellow);">{n_staging} staging/dev environment(s)</strong> — often have weaker security controls</li>')
    if origin_list:
        vb.append(f'<li><strong>{len(origin_list)} origin IP candidate(s)</strong> discovered</li>')
    if n_admin:
        vb.append(f'<li>{n_admin} admin panel(s) discovered</li>')
    for vec in attack_vectors[:6]:
        vn = vec.get('type', '')
        if vn not in ('waf_bypass', 'unprotected', 'staging_dev', ''):
            vs = vec.get('severity', 'medium')
            vc = SEV_COLORS.get(vs, 'var(--muted)')
            vb.append(f'<li><strong style="color:{vc};">{_esc(vn)}</strong> — {_esc(vec.get("description", "")[:80])}</li>')
    vuln_html = f'<div style="margin-bottom:16px;font-size:0.95em;line-height:1.6;"><strong>Key vulnerabilities:</strong><ul style="margin:8px 0 0 20px;line-height:2;">{"".join(vb)}</ul></div>' if vb else ''

    rb = []
    if hdr_score < 50:
        rb.append(f'<li><strong>Security headers weak</strong> ({hdr_score}/100) — {len(missing_hdrs)} essential header(s) missing</li>')
    for r in remediation[:6]:
        t = r.get('action', str(r)) if isinstance(r, dict) else str(r)
        rb.append(f'<li>{_esc(t)}</li>')
    if n_waf_bypass:
        rb.append(f'<li>Route {n_waf_bypass} WAF-bypass subdomain(s) through CDN</li>')
    remed_html = f'<div style="margin-bottom:16px;font-size:0.95em;line-height:1.6;"><strong>Recommended improvements:</strong><ol style="margin:8px 0 0 20px;line-height:2;">{"".join(rb)}</ol></div>' if rb else ''

    # Auto WAF rules from bypass findings
    _waf_rules_html = ''
    _bypass_findings = [f for f in findings if f.get('type') in ('waf_bypass', 'bypass') or not f.get('blocked', True)]
    if _bypass_findings:
        try:
            from fray.waf_rules import generate_rules, rules_to_html
            _waf_v = str(waf_vendor) if waf_vendor and waf_vendor != '—' else 'generic'
            _rules_data = generate_rules(_bypass_findings, waf_vendor=_waf_v)
            if _rules_data.get('count', 0) > 0:
                _waf_rules_html = rules_to_html(_rules_data)
        except Exception:
            pass

    # ── Risk grade explanation + how to improve ─────────────────────────────
    supply_chain_data = rd.get('supply_chain', {}) or {}
    supply_chain_risk = supply_chain_data.get('risk_level', '') if isinstance(supply_chain_data, dict) else ''
    _grade_val = risk_grade(risk_score)
    _grade_scale = {
        'A': ('Minimal', 'var(--green)',
              'Attack surface is well-hardened with few exposures. Focus on monitoring and maintaining current posture.'),
        'B': ('Low',  'var(--green)',
              'Minor gaps exist. Address the listed findings to reach grade A.'),
        'C': ('Moderate', 'var(--yellow)',
              'Notable gaps in security posture. Prioritise fixing high-severity findings to improve to grade B.'),
        'D': ('High', 'var(--orange)',
              'Significant exposures present. Resolve critical and high-severity findings first — this will lower the score by 20–30 points.'),
        'F': ('Critical', 'var(--red)',
              'Severe attack surface exposure. Immediate remediation required. Focus on critical findings first.'),
    }
    _grade_label, _grade_color, _grade_advice = _grade_scale.get(_grade_val, ('?', rc, ''))

    # Build the "how to improve" specific to this scan
    _improve_steps = []
    if supply_chain_risk in ('critical', 'high'):
        _improve_steps.append('Add SRI integrity hashes to all third-party scripts on payment pages <em>(–10 to –15 pts)</em>')
    _secret_findings_count = len(rd.get('secrets', {}).get('findings', [])) if isinstance(rd.get('secrets'), dict) else 0
    if _secret_findings_count > 0:
        _improve_steps.append(f'Rotate {_secret_findings_count} exposed credential(s) and move to secrets manager <em>(–10 to –20 pts)</em>')
    if n_unprotected > 0:
        _improve_steps.append(f'Route {n_unprotected} unprotected subdomain(s) behind CDN/WAF <em>(–10 pts)</em>')
    if hdr_score < 50:
        _improve_steps.append(f'Add missing security headers (CSP, HSTS, X-Frame-Options) — current score {hdr_score}/100 <em>(–5 to –10 pts)</em>')
    if not _improve_steps:
        _improve_steps.append('Review and address high-severity findings in order of priority')

    _improve_html = '<ul style="margin:6px 0 0 20px;line-height:2;font-size:0.9em;">' + \
        ''.join(f'<li>{s}</li>' for s in _improve_steps) + '</ul>'

    _grade_box = f'''<div style="background:var(--surface2);border-radius:10px;padding:14px 18px;margin:12px 0;border-left:4px solid {_grade_color};">
  <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
    <span style="font-size:2em;font-weight:800;color:{_grade_color};line-height:1;">{_grade_val}</span>
    <div>
      <div style="font-weight:700;color:{_grade_color};">Security Grade {_grade_val} — {_grade_label} Risk</div>
      <div style="font-size:0.85em;color:var(--text2);">{_grade_advice}</div>
    </div>
  </div>
  <div style="font-size:0.88em;color:var(--text2);"><strong>To improve this score:</strong>{_improve_html}</div>
</div>'''

    if risk_score >= 65: risk_msg = '<span style="color:var(--red);font-weight:700;">The attack surface has critical exposures requiring immediate action.</span>'
    elif risk_score >= 45: risk_msg = '<span style="color:var(--orange);font-weight:700;">The attack surface has significant exposures that should be addressed promptly. Grade D means real risk — not just theoretical.</span>'
    elif risk_score >= 25: risk_msg = '<span style="color:var(--yellow);font-weight:700;">The attack surface has moderate exposures worth addressing.</span>'
    else: risk_msg = '<span style="color:var(--green);font-weight:700;">The attack surface is relatively well-secured.</span>'

    parts.append(f'''
<div class="sec" id="exec">
  <h2>Executive Summary</h2>
  <p style="font-size:1.02em;line-height:1.8;margin-bottom:16px;">{"<br>".join(sp)}</p>
  {_grade_box}
  {vuln_html}{remed_html}{_waf_rules_html}
  <p style="font-size:1em;line-height:1.8;margin-top:8px;">{risk_msg}</p>
</div>''')

    # Methodology
    techs_list = ['DNS enumeration (A, AAAA, MX, NS, TXT, CNAME, SOA)',
                  'Passive subdomain discovery (Certificate Transparency)',
                  'Active subdomain brute-force (common prefixes)',
                  'HTTP fingerprinting (headers, response body, scripts)',
                  'Technology detection (Wappalyzer 7,500+ signatures)',
                  'TLS/SSL analysis (version, cipher suites, certificate)',
                  'Security header assessment (HSTS, CSP, etc.)',
                  'WAF detection & bypass analysis',
                  'Origin IP discovery', 'Admin panel enumeration',
                  'Per-subdomain WAF/CDN/cache fingerprinting',
                  'Attack surface prioritization (MITRE-mapped)',
                  'Rate limit & DDoS resilience testing',
                  'Frontend library CVE scanning']
    tl = ''.join(f'<li style="font-size:0.9em;">{_esc(t)}</li>' for t in techs_list)
    src_parts = ', '.join(f'{k}: {v}' for k, v in sub_sources.items()) if sub_sources else ''
    parts.append(f'''
<div class="sec" id="methodology">
  <h2>Methodology &amp; Scope</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:16px;">
    <div><table>
      <tr><td class="kv-key">Target</td><td class="mono">{_esc(target)}</td></tr>
      <tr><td class="kv-key">Scan Date</td><td>{_esc(ts_short)}</td></tr>
      <tr><td class="kv-key">Profile</td><td>{_esc(_profile_label)}</td></tr>
    </table></div>
    <div><table>
      <tr><td class="kv-key">Subdomains Found</td><td>{n_subs}</td></tr>
      <tr><td class="kv-key">Probes Sent</td><td>{n_probes}</td></tr>
      <tr><td class="kv-key">Admin Panels Found</td><td>{n_admin} of {n_admin_checked} paths probed</td></tr>
    </table></div>
  </div>
  <details><summary>Techniques Applied ({len(techs_list)})</summary><ol style="padding-left:20px;line-height:2.2;">{tl}</ol></details>
  {f'<p class="muted" style="margin-top:8px;font-size:0.85em;">Sources: {_esc(src_parts)}</p>' if src_parts else ''}
  <p class="muted" style="margin-top:12px;font-size:0.85em;">This assessment is non-intrusive reconnaissance only — no exploitation was performed.</p>
{_method_upgrade_tip(scan_mode, target)}
</div>''')

    # Findings — sorted critical → high → medium → low
    _f_sev_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    findings_sorted = sorted(findings, key=lambda f: _f_sev_rank.get(f.get("severity", "info"), 4))
    fi = ''
    for f in findings_sorted:
        sev = f.get('severity', 'low')
        col = SEV_COLORS.get(sev, 'var(--muted)')
        fi += f'<div class="finding" style="border-left:4px solid {col};"><span class="sev-badge" style="background:{col}20;color:{col};">{sev.upper()}</span> {_esc(f.get("finding", ""))}</div>'
    parts.append(f'''
<div class="sec" id="findings">
  <h2>Key Findings <span class="count">({n_findings})</span></h2>
  {fi if fi else '<p class="muted">No findings detected.</p>'}
</div>''')

    # Attack Vectors
    if attack_vectors:
        vi = ''
        for vec in attack_vectors:
            vs = vec.get('severity', 'medium')
            vc = SEV_COLORS.get(vs, 'var(--muted)')
            vn_raw = vec.get('type', 'Unknown')
            vn = _esc(vn_raw)
            vct = vec.get('count', 0)
            vp = vec.get('priority', 0)
            vd = _esc(vec.get('description', ''))
            vim = _esc(vec.get('impact', ''))
            vm = vec.get('mitre', '')
            vt = vec.get('targets', [])
            emoji = _VEC_EMOJI.get(vn_raw, '')
            emoji_html = f'<span style="font-size:1.4em;">{emoji}</span>' if emoji else ''
            detail = vec.get('detail', '')
            # Render detail as structured lines — bullet points, full URLs, no truncation
            detail_html = ''
            if detail:
                lines = [l.strip() for l in detail.split('\n') if l.strip()]
                if lines:
                    lines_html = ''
                    _url_re = __import__('re').compile(r'(https?://[^\s<>"]+)')
                    for line in lines:
                        if line.startswith('•') or line.startswith('-'):
                            clean = _esc(line.lstrip('•- '))
                            # If line contains a URL, make it a clickable link
                            url_m = _url_re.search(clean)
                            if url_m:
                                url = url_m.group(1)
                                clean = clean.replace(url, f'<a href="{url}" style="color:var(--accent2);word-break:break-all;" target="_blank">{url}</a>')
                            lines_html += f'<li style="font-size:0.85em;color:var(--text2);margin-bottom:3px;">{clean}</li>'
                        else:
                            lines_html += f'<p style="font-size:0.85em;color:var(--text2);margin-bottom:4px;font-weight:600;">{_esc(line)}</p>'
                    detail_html = (
                        f'<details style="margin-top:8px;" open>'
                        f'<summary style="font-size:0.82em;cursor:pointer;">Detail</summary>'
                        f'<div style="margin-top:6px;padding:10px 14px;background:var(--surface);'
                        f'border-radius:6px;border:1px solid var(--border);">'
                        f'<ul style="list-style:disc;padding-left:16px;margin:0;">{lines_html}</ul>'
                        f'</div></details>'
                    ) if '<li' in lines_html else (
                        f'<details style="margin-top:8px;" open>'
                        f'<summary style="font-size:0.82em;cursor:pointer;">Detail</summary>'
                        f'<div style="margin-top:6px;padding:10px 14px;background:var(--surface);'
                        f'border-radius:6px;border:1px solid var(--border);">{lines_html}</div></details>'
                    )

            vi += f'''<div style="background:var(--surface2);border-radius:12px;padding:20px 24px;margin-bottom:16px;border-left:4px solid {vc};">
   <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
     {emoji_html}
     <div style="flex:1;"><div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;">
       <strong style="font-size:1.1em;">{vn}</strong>
       <span class="sev-badge" style="background:{vc}20;color:{vc};">{vs.upper()}</span>
       <span class="muted" style="font-size:0.82em;">P{vp} · {vct} target(s)</span>
     </div></div>
   </div>
   {f'<p style="margin-bottom:8px;font-size:0.92em;">{vd}</p>' if vd else ''}
   {f'<p style="margin-bottom:8px;font-size:0.92em;"><strong style="color:var(--orange);">Impact:</strong> {vim}</p>' if vim else ''}
   {f'<p style="margin-bottom:8px;font-size:0.82em;"><span class="muted">MITRE:</span> <code style="background:var(--surface);padding:2px 8px;border-radius:4px;">{_esc(vm)}</code></p>' if vm else ''}
   {f'<div style="margin-top:10px;"><span class="muted" style="font-size:0.82em;">Affected:</span><br><div style="margin-top:4px;display:flex;flex-wrap:wrap;gap:4px;">{_targets_chips(vt)}</div></div>' if vt else ''}
   {detail_html}
 </div>'''
        parts.append(f'''
<div class="sec" id="vectors">
  <h2>Attack Vectors <span class="count">({len(attack_vectors)} types across {n_attack_targets} targets)</span></h2>
  {vi}
</div>''')

    # Attack Priorities
    if attack_targets:
        _TYPE_COLORS = {
            'WAF Bypass': 'var(--red)', 'Unprotected Subdomain': 'var(--orange)',
            'Account Takeover': 'var(--red)', 'API Vulnerability': 'var(--orange)',
            'SSRF': 'var(--red)', 'File Upload': 'var(--orange)',
            'Payment': 'var(--red)', 'Cloud Storage': '#a855f7',
            'LLM/AI': '#a855f7', 'DDoS': 'var(--yellow)',
            'Cache Poisoning': 'var(--yellow)', 'JWT': 'var(--orange)',
            'Rate Limit': 'var(--yellow)', 'WebSocket': '#3b82f6',
            'Robots Paths': 'var(--muted)', 'Open Redirect': 'var(--orange)',
            'Critical Endpoint Exposure': 'var(--red)', 'Staging / Dev Environment': 'var(--yellow)',
            'DDoS / L7 Denial of Service': 'var(--yellow)', 'DDoS — Direct Origin': 'var(--yellow)',
            'Web Cache Poisoning': 'var(--orange)', 'Payment / Financial Abuse': 'var(--red)',
            'LLM / AI Prompt Injection': '#a855f7',
        }
        # Sort: CRITICAL (priority ≥ 90) first, then HIGH, then by priority descending
        _sev_priority = lambda t: (
            0 if t.get('priority', 0) >= 90 else
            1 if t.get('priority', 0) >= 70 else
            2 if t.get('priority', 0) >= 50 else 3,
            -t.get('priority', 0)
        )
        attack_targets_sorted = sorted(attack_targets, key=_sev_priority)
        at_rows = ''
        _at_limit = 20
        for i, t in enumerate(attack_targets_sorted[:_at_limit], 1):
           tp = t.get('priority', 0)
           tt = t.get('type', '')
           tgt = t.get('target', '')
           pc = 'var(--red)' if tp >= 90 else 'var(--orange)' if tp >= 70 else 'var(--yellow)' if tp >= 50 else 'var(--muted)'
           tc = _TYPE_COLORS.get(tt, '#3b82f6')
           at_rows += f'<tr><td class="num">{i}</td><td style="color:{pc};font-weight:700;">{tp}</td><td><span class="type-badge" style="background:{tc}20;color:{tc};">{_esc(tt)}</span></td><td class="mono" style="font-size:0.85em;">{_esc(tgt)}</td></tr>'
        overflow_note = f'<p class="muted" style="margin-top:8px;font-size:0.85em;">Showing top {_at_limit} of {n_attack_targets} targets by priority. See <a href="#vectors" style="color:var(--accent);">Attack Vectors</a> above for full details.</p>' if n_attack_targets > _at_limit else ''
        parts.append(f'''
<div class="sec" id="priorities">
  <h2>Attack Priorities <span class="count">(Top {min(_at_limit, n_attack_targets)} of {n_attack_targets})</span></h2>
  <table><tr><th>#</th><th>Priority</th><th>Type</th><th>Target</th></tr>{at_rows}</table>
  {overflow_note}
</div>''')

    # CVEs — both frontend libs and server-side technologies
    cve_items = ''
    # Sort: critical first, then high, medium, low
    _sev_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
    sorted_vulns = sorted(fl_vulns, key=lambda v: _sev_order.get(v.get('severity', 'info'), 5))
    for v in sorted_vulns[:30]:
        sev = v.get('severity', 'info')
        sc = SEV_COLORS.get(sev, 'var(--muted)')
        src = v.get('source', 'frontend')
        src_badge = f'<span class="type-badge" style="background:var(--muted)20;color:var(--muted);font-size:0.75em;">{_esc(src)}</span>' if src == 'server_header' else ''
        cve_items += f'<tr><td><span style="color:{sc};font-weight:700;">{_esc(v.get("id",""))}</span></td><td class="mono">{_esc(v.get("library",""))} {src_badge}</td><td><span style="color:{sc};">{_esc(sev)}</span></td><td class="muted" style="font-size:0.85em;">{_esc(v.get("description", v.get("summary",""))[:120])}</td></tr>'
    # Show detected libs table
    detected_libs = fl.get('libraries', []) if isinstance(fl, dict) else []
    libs_html = ''
    if detected_libs:
        lib_rows = ''
        for l in detected_libs[:20]:
            cves = l.get('cves', [])
            status = f'<span style="color:var(--red);font-weight:600;">{len(cves)} CVE(s)</span>' if cves else '<span style="color:var(--green);">No known CVEs</span>'
            lib_rows += f'<tr><td class="mono">{_esc(l.get("name",""))}</td><td>{_esc(l.get("version",""))}</td><td>{_esc(l.get("source",""))}</td><td>{status}</td></tr>'
        libs_html = f'<details style="margin-top:12px;"><summary style="cursor:pointer;font-size:0.85em;color:var(--accent);">Detected libraries & technologies ({len(detected_libs)})</summary><table style="margin-top:8px;"><tr><th>Technology</th><th>Version</th><th>Source</th><th>Status</th></tr>{lib_rows}</table></details>'
    elif not cve_items:
        libs_html = f'''<div style="margin-top:8px;background:var(--surface2);border-radius:10px;padding:14px 18px;border-left:3px solid var(--muted);">
   <p style="font-size:0.85em;line-height:1.7;">Scans 35+ frontend libraries (jQuery, Bootstrap, Angular, Vue, React, Lodash, D3, etc.) and server technologies (Apache, Nginx, IIS, Tomcat, PHP, OpenSSL) for known CVEs.
   Run <code>fray recon {_esc(host)} --deep</code> for deeper subdomain-level version detection.</p>
 </div>'''

    # Also include VPN CVEs already found (in VPN section) here for completeness
    vpn_cve_table = ''
    if vpn_cve_findings:
        vpn_cve_rows = ''
        for c in sorted(vpn_cve_findings, key=lambda x: -(x.get('cvss') or 0)):
            cid   = c.get('cve_id', '')
            cvss  = c.get('cvss', '')
            desc  = c.get('description', '')[:100]
            prod  = c.get('product', '')
            sc    = 'var(--red)' if (cvss and float(str(cvss)) >= 9) else 'var(--orange)' if (cvss and float(str(cvss)) >= 7) else 'var(--yellow)'
            verif = '✓ Verified' if c.get('verified') else '~ Potential'
            verif_col = 'var(--green)' if c.get('verified') else 'var(--muted)'
            vpn_cve_rows += (
                f'<tr><td><a href="#vpn" style="color:{sc};font-weight:700;">{_esc(cid)}</a></td>'
                f'<td class="muted">{_esc(prod)}</td>'
                f'<td style="color:{sc};">{cvss}</td>'
                f'<td class="muted" style="font-size:0.85em;">{_esc(desc)}</td>'
                f'<td style="color:{verif_col};font-size:0.82em;">{verif}</td>'
                f'</tr>'
            )
        vpn_cve_table = (
            f'<div style="margin-bottom:16px;">'
            f'<h3 style="font-size:0.95em;margin-bottom:8px;color:var(--red);">'
            f'VPN / Remote Access CVEs ({len(vpn_cve_findings)} found)</h3>'
            f'<p style="font-size:0.82em;color:var(--text2);margin-bottom:8px;">'
            f'These CVEs were detected in the <a href="#vpn" style="color:var(--accent);">VPN section</a>. '
            f'See that section for full details and exploitation notes.</p>'
            f'<table><tr><th>CVE</th><th>Product</th><th>CVSS</th><th>Description</th><th>Status</th></tr>'
            f'{vpn_cve_rows}</table></div>'
        )

    total_cves = len(fl_vulns) + len(vpn_cve_findings)
    total_components = n_vuln_libs + (1 if vpn_cve_findings else 0)
    cve_table = (
        f'<table><tr><th>CVE</th><th>Technology</th><th>Severity</th><th>Description</th></tr>'
        f'{cve_items}</table>'
    ) if cve_items else ''
    parts.append(f'''
 <div class="sec" id="cves">
   <h2>Known Vulnerabilities <span class="count">({total_cves} CVEs, {total_components} vulnerable component(s))</span></h2>
   {vpn_cve_table}{cve_table}{libs_html}
 </div>''')

    # Security Checks
    if checks:
        ck_html = ''
        all_pass = True
        for ck_name, ck_val in checks.items():
           if isinstance(ck_val, dict) and ck_val.get('findings'):
            all_pass = False
            for cf in ck_val['findings']:
                ck_html += f'<div class="finding" style="border-left:4px solid var(--orange);"><span class="sev-badge" style="background:var(--orange)20;color:var(--orange);">WARN</span> {_esc(str(cf))}</div>'
        if all_pass:
            ck_html = '<p style="color:var(--green);">All additional checks passed — no CORS, subdomain takeover, exposed files, or cookie issues detected.</p>'
        parts.append(f'<div class="sec" id="checks"><h2>Additional Security Checks</h2>{ck_html}</div>')

    # CSP Analysis
    csp_html_sec = ''
    if csp_present:
        csp_html_sec = f'<p style="margin-bottom:8px;"><strong>Score:</strong> {csp_score}/100</p>'
        if csp_bypasses:
            for bp in csp_bypasses[:5]:
                csp_html_sec += f'<div class="finding" style="border-left:4px solid var(--orange);"><span class="sev-badge" style="background:var(--orange)20;color:var(--orange);">BYPASS</span> {_esc(str(bp))}</div>'
    else:
        csp_html_sec = ('<div class="finding" style="border-left:4px solid var(--red);">'
            '<span class="sev-badge" style="background:var(--red)20;color:var(--red);">CRITICAL</span> '
            'No Content-Security-Policy header — all inline scripts execute freely</div>')
        csp_html_sec += '''<div style="margin-top:14px;background:var(--surface2);border-radius:10px;padding:14px 18px;border-left:3px solid var(--red);">
  <p style="font-size:0.9em;font-weight:600;color:var(--red);margin-bottom:8px;">Risks without CSP:</p>
  <ul style="padding-left:18px;font-size:0.85em;line-height:1.9;color:var(--text);">
    <li><strong>Reflected &amp; Stored XSS</strong> — attacker-injected scripts execute in user browsers, stealing sessions and credentials</li>
    <li><strong>Data exfiltration</strong> — malicious inline scripts can send form data, cookies, and tokens to attacker servers</li>
    <li><strong>Clickjacking via iframes</strong> — page can be embedded in attacker-controlled frames without restriction</li>
    <li><strong>Cryptojacking</strong> — injected scripts can run cryptocurrency miners in visitor browsers</li>
    <li><strong>Magecart / skimming</strong> — third-party scripts can be injected to capture payment card data</li>
  </ul>
</div>'''
    parts.append(f'''
<div class="sec" id="csp">
  <h2>CSP Analysis <span class="count">({csp_score}/100)</span></h2>
  {csp_html_sec}
</div>''')

    # Security Headers
    pt = ''.join(f'<span class="tag tag-ok">{_esc(h)}</span>' for h in present_hdrs)
    mt = ''
    for h, info in missing_hdrs.items():
        sev = info.get('severity', 'low') if isinstance(info, dict) else 'low'
        mt += f'<span class="tag tag-miss">{_esc(h)} <small>({_esc(sev)})</small></span> '
    _HDR_RISKS = {
        'HSTS': 'SSL stripping attacks — attacker downgrades HTTPS to HTTP and intercepts traffic',
        'CSP': 'XSS and code injection — no restrictions on inline scripts or loaded resources',
        'X-Frame-Options': 'Clickjacking — page can be embedded in malicious iframes to trick user clicks',
        'X-Content-Type-Options': 'MIME-type sniffing — browsers may execute uploaded files as scripts',
        'X-XSS-Protection': 'Legacy XSS filter disabled — reflected XSS in older browsers',
        'Referrer-Policy': 'URL leakage — sensitive query parameters exposed to third-party sites',
        'Permissions-Policy': 'Unrestricted browser APIs — camera, microphone, geolocation accessible to any script',
        'COOP': 'Cross-origin attacks — Spectre-class side-channel leaks via shared browsing context',
        'CORP': 'Cross-origin resource theft — sensitive resources loadable by attacker pages',
    }
    hdr_risk_html = ''
    if hdr_score < 30 and missing_hdrs:
        risk_items = ''
        for h in list(missing_hdrs.keys())[:6]:
            risk = _HDR_RISKS.get(h, '')
            if risk:
                risk_items += f'<li><strong>{_esc(h)}</strong> — {_esc(risk)}</li>'
        if risk_items:
            hdr_risk_html = f'''<div style="margin-top:14px;background:var(--surface2);border-radius:10px;padding:14px 18px;border-left:3px solid var(--red);">
  <p style="font-size:0.9em;font-weight:600;color:var(--red);margin-bottom:8px;">Risks from missing headers:</p>
  <ul style="padding-left:18px;font-size:0.85em;line-height:1.9;color:var(--text);">{risk_items}</ul>
</div>'''
    # Header value quality badges
    _hdr_quality_html = ''
    if hdr_value_issues:
        _qi = ''
        _QUALITY_COLORS = {'STRONG': 'var(--green)', 'MODERATE': 'var(--yellow)', 'WEAK': 'var(--orange)', 'MISCONFIGURED': 'var(--red)'}
        for _vi in hdr_value_issues[:8]:
            _h = _esc(_vi.get('header', ''))
            _q = _vi.get('quality', 'WEAK')
            _qc = _QUALITY_COLORS.get(_q, 'var(--muted)')
            _iss = _esc(_vi.get('issue', ''))
            _qi += f'<tr><td><strong>{_h}</strong></td><td><span style="color:{_qc};font-weight:600;">{_q}</span></td><td class="muted" style="font-size:0.85em;">{_iss}</td></tr>'
        _hdr_quality_html = f'''<div style="margin-top:14px;">
  <p style="font-size:0.9em;font-weight:600;margin-bottom:8px;">Header Value Analysis:</p>
  <table><tr><th>Header</th><th>Quality</th><th>Issue</th></tr>{_qi}</table>
</div>'''

    # CORS section
    _cors_html = ''
    if _cors_issues:
        _ci = ''
        for _c in _cors_issues[:6]:
            _ct = _esc(_c.get('test', ''))
            _cs = _c.get('severity', 'medium')
            _csc = SEV_COLORS.get(_cs, 'var(--muted)')
            _cr = _esc(_c.get('risk', ''))
            _ci += f'<tr><td>{_ct}</td><td><span class="sev-badge" style="background:{_csc}20;color:{_csc};">{_cs.upper()}</span></td><td class="muted" style="font-size:0.85em;">{_cr}</td></tr>'
        _cors_html = f'''<div style="margin-top:14px;border-top:1px solid var(--border);padding-top:14px;">
  <p style="font-size:0.9em;font-weight:600;color:var(--orange);margin-bottom:8px;">CORS Misconfiguration ({len(_cors_issues)} issue{"s" if len(_cors_issues) != 1 else ""}):</p>
  <table><tr><th>Test</th><th>Severity</th><th>Risk</th></tr>{_ci}</table>
</div>'''

    parts.append(f'''
<div class="sec" id="headers">
  <h2>Security Headers <span class="count">({hdr_score}/100)</span></h2>
  <p style="margin-bottom:10px;"><strong>Present:</strong> {pt or '<span class="muted">None</span>'}</p>
  <p><strong>Missing:</strong> {mt or '<span style="color:var(--green);">None — all present</span>'}</p>
  {hdr_risk_html}
  {_hdr_quality_html}
  {_cors_html}
</div>''')

    # Technologies
    _CAT_COLORS = {
        'WAF': 'var(--green)', 'CDN': 'var(--blue)', 'Cloud': 'var(--purple)',
        'Web Server': 'var(--cyan)', 'Application Server': 'var(--orange)',
        'Framework': 'var(--yellow)', 'CMS': 'var(--yellow)',
        'Hosting Panel': 'var(--muted)', 'Container': 'var(--cyan)',
        'CI/CD': 'var(--orange)', 'DevOps': 'var(--purple)',
        'Database': 'var(--red)', 'Search Engine': 'var(--blue)',
        'API': 'var(--accent2)', 'Container Orchestration': 'var(--cyan)',
        'Load Balancer': 'var(--cyan)', 'Proxy': 'var(--cyan)',
        'Storage': 'var(--blue)', 'Cache': 'var(--blue)',
        'JavaScript Framework': 'var(--yellow)', 'JavaScript Library': 'var(--yellow)',
        'CSS Framework': 'var(--yellow)', 'UI Library': 'var(--yellow)',
        'Runtime': 'var(--green)', 'Language': 'var(--green)',
         'Analytics': 'var(--purple)', 'Marketing': 'var(--purple)',
        'Captcha': 'var(--orange)', 'Security': 'var(--green)',
        'Email Security': '#3b82f6',   # blue — email security gateways (Proofpoint, Abnormal, etc.)
        'Email': '#3b82f6',
        'Telco': 'var(--muted)',
        'E-commerce': 'var(--orange)', 'Payment': 'var(--orange)',
        'CRM': 'var(--blue)', 'Support': 'var(--blue)',
        'ITSM': 'var(--blue)', 'Identity': 'var(--green)',
        'SaaS': 'var(--purple)', 'PaaS': 'var(--purple)',
        'Hosting': 'var(--muted)', 'BaaS': 'var(--purple)',
        'Monitoring': 'var(--orange)', 'SIEM': 'var(--red)',
        'Telco': 'var(--blue)', 'Communication': 'var(--blue)',
        'Editor': 'var(--yellow)', 'Visualization': 'var(--purple)',
        'Media': 'var(--cyan)', 'Maps': 'var(--green)',
        'A/B Testing': 'var(--purple)', 'Feature Flags': 'var(--purple)',
        'Message Queue': 'var(--orange)', 'Directory': 'var(--muted)',
        'Collaboration': 'var(--blue)', 'Wiki': 'var(--blue)',
        'Project Management': 'var(--blue)', 'Code Quality': 'var(--orange)',
        'API Gateway': 'var(--cyan)', 'Icon Library': 'var(--yellow)',
        'AI / LLM': '#a855f7', 'AI / ML': '#a855f7',
        'AI Chatbot': '#a855f7', 'Chatbot': '#a855f7',
        'AI Framework': '#a855f7', 'AI Gateway': '#a855f7',
        'AI Search': '#a855f7', 'AI Support': '#a855f7',
        'Vector DB': '#a855f7',
    }
    # Group technologies by category
    _CAT_ORDER = [
        # Security & Infrastructure
        'WAF', 'CDN', 'CDN/WAF', 'Cloud', 'Cloud/CDN',
        'Web Server', 'Load Balancer', 'Proxy', 'API Gateway', 'Storage', 'Cache',
        'Application Server', 'Framework', 'Runtime', 'Language',
        # Frontend
        'JavaScript Framework', 'JavaScript Library', 'CSS Framework', 'UI Library', 'Icon Library',
        'Visualization', 'Editor', 'Media', 'Maps',
        # CMS & E-commerce
        'CMS', 'E-commerce',
        # SaaS & Business
        'CRM', 'Support', 'ITSM', 'Payment', 'Identity',
        'Marketing', 'Analytics', 'A/B Testing', 'Feature Flags',
        'Captcha', 'Security', 'Email Security', 'Email',
        # Communication & Collaboration
        'Communication', 'Collaboration', 'Wiki', 'Project Management',
        # Data & Search
        'Database', 'Search Engine', 'Message Queue',
        # Platform & Hosting
        'SaaS', 'PaaS', 'BaaS', 'Hosting', 'Telco',
        # DevOps & Monitoring
        'Container', 'Container Orchestration', 'CI/CD', 'DevOps', 'Code Quality',
        'Monitoring', 'SIEM', 'Directory',
        # AI / LLM / Chatbot
        'AI / LLM', 'AI / ML', 'AI Chatbot', 'Chatbot', 'AI Framework',
        'AI Gateway', 'AI Search', 'AI Support', 'Vector DB',
        # API & Infra
        'API', 'TLS', 'Cipher Suite', 'Certificate Authority', 'Infrastructure',
    ]
    cat_groups = {}  # category -> [(name, info), ...]
    for name, ver in techs.items():
        if isinstance(ver, dict):
            cat = ver.get('category', 'Other')
        else:
            cat = 'Other'
        cat_groups.setdefault(cat, []).append(name)
    tech_html = ''
    for cat in _CAT_ORDER + [c for c in cat_groups if c not in _CAT_ORDER]:
        if cat not in cat_groups:
            continue
        names = sorted(cat_groups[cat])
        cat_col = _CAT_COLORS.get(cat, 'var(--muted)')
        # Also check partial matches for combined categories like CDN/WAF
        if cat_col == 'var(--muted)':
            for base_cat in cat.split('/'):
                if base_cat.strip() in _CAT_COLORS:
                    cat_col = _CAT_COLORS[base_cat.strip()]
                    break
        chips = ' '.join(
            f'<span style="display:inline-block;background:var(--surface);padding:5px 12px;'
            f'border-radius:6px;font-size:0.88em;border:1px solid var(--border);margin:3px 2px;">'
            f'{_esc(_normalize_tech_name(n))}</span>'
            for n in names)
        tech_html += (f'<div style="margin-bottom:10px;">'
                      f'<span class="type-badge" style="background:{cat_col}20;color:{cat_col};'
                      f'font-size:0.82em;min-width:100px;text-align:center;">{_esc(cat)}</span>'
                      f' {chips}</div>')
    parts.append(f'''
<div class="sec" id="tech">
  <h2>Technologies <span class="count">({len(techs)})</span></h2>
  {tech_html if tech_html else '<p class="muted">No technologies detected.</p>'}
</div>''')

    # DNS — show NS, MX, CNAME chain, email provider, SPF, DMARC
    def _is_ip(s):
        try:
            _ipaddr.ip_address(s)
            return True
        except (ValueError, TypeError):
            return False
    raw_a = dns.get('a', [])
    # Build CNAME chain
    cname_list = dns.get('cname', [])
    if isinstance(cname_list, str):
        cname_list = [cname_list] if cname_list else []
    chain_hosts = [r for r in raw_a if not _is_ip(r)]
    full_chain = []
    if cname_list:
        full_chain.extend(cname_list)
    for h in chain_hosts:
        if h not in full_chain:
            full_chain.append(h)
    a_ips = [r for r in raw_a if _is_ip(r)]
    if a_ips:
        full_chain.append(a_ips[0])
    # Build CNAME display with ASN/ISP info for IP addresses
    # Look up ASN from known IP ranges (offline, no API call needed)
    def _ip_to_asn_hint(ip: str) -> str:
        """Return ASN/org hint for known IP ranges without external API call."""
        _KNOWN_RANGES = [
            # NTT Docomo / NTT Communications (Japan)
            ("122.17.", "AS2527 NTT Docomo (Japan)"),
            ("122.16.", "AS2527 NTT Docomo (Japan)"),
            ("122.18.", "AS2527 NTT Docomo (Japan)"),
            ("61.213.", "AS4694 IIJ (Japan)"),
            ("61.214.", "AS4694 IIJ (Japan)"),
            # AWS CloudFront
            ("52.", "AWS"), ("54.", "AWS"), ("3.", "AWS"), ("18.", "AWS"),
            ("13.", "AWS"), ("15.197.", "AWS"),
            # GCP
            ("34.", "Google Cloud"), ("35.", "Google Cloud"),
            # Cloudflare
            ("104.16.", "Cloudflare"), ("104.17.", "Cloudflare"),
            ("104.18.", "Cloudflare"), ("104.19.", "Cloudflare"),
            ("104.20.", "Cloudflare"), ("104.21.", "Cloudflare"),
            ("172.64.", "Cloudflare"), ("172.65.", "Cloudflare"),
            ("172.66.", "Cloudflare"), ("172.67.", "Cloudflare"),
            # Fastly
            ("151.101.", "Fastly"), ("199.27.", "Fastly"),
            # Akamai
            ("23.", "Akamai"), ("63.217.", "Akamai"),
            ("104.64.", "Akamai"), ("104.65.", "Akamai"),
        ]
        for prefix, org in _KNOWN_RANGES:
            if ip.startswith(prefix):
                return org
        return ""

    chain_parts = []
    for h in full_chain:
        if _is_ip(h):
            asn = _ip_to_asn_hint(h)
            if asn:
                chain_parts.append(
                    f'<span class="mono">{_esc(h)}</span>'
                    f'<span class="muted" style="font-size:0.82em;"> ({_esc(asn)})</span>'
                )
            else:
                chain_parts.append(f'<span class="mono">{_esc(h)}</span>')
        else:
            chain_parts.append(f'<span class="mono">{_esc(h)}</span>')
    cname_display = ' &rarr; '.join(chain_parts) if chain_parts else '—'

    # NS records
    ns_recs = dns.get('ns', [])
    ns_display = ', '.join(ns_recs) if ns_recs else '—'

    # MX records + email provider
    mx_recs = dns.get('mx', [])
    email_providers = dns.get('email_providers', [])
    if mx_recs:
        mx_chips = ' '.join(f'<code style="background:var(--surface);padding:3px 8px;border-radius:4px;font-size:0.85em;border:1px solid var(--border);">{_esc(m)}</code>' for m in mx_recs[:5])
        provider_badge = ''
        if email_providers:
            provider_badge = ' ' + ' '.join(f'<span class="type-badge" style="background:var(--blue)20;color:var(--blue);font-size:0.8em;">{_esc(p)}</span>' for p in email_providers)
        mx_display = f'{mx_chips}{provider_badge}'
    else:
        mx_display = '<span class="muted">No MX records</span>'

    spf = dns.get('spf', '')
    dmarc = dns.get('dmarc', '')

    # RDAP domain registration data
    rdap = rd.get('rdap', {}) or {}
    rdap_registered  = rdap.get('registered', '') if isinstance(rdap, dict) else ''
    rdap_expires     = rdap.get('expires', '') if isinstance(rdap, dict) else ''
    rdap_registrar   = rdap.get('registrar', '') if isinstance(rdap, dict) else ''
    rdap_age_days    = rdap.get('domain_age_days') if isinstance(rdap, dict) else None
    rdap_is_new      = rdap.get('is_new_domain', False) if isinstance(rdap, dict) else False
    rdap_status      = rdap.get('status', []) if isinstance(rdap, dict) else []
    rdap_ns_check    = rdap.get('nameservers', []) if isinstance(rdap, dict) else []

    # Age display
    if rdap_age_days is not None:
        if rdap_age_days < 365:
            _age_str = f'<span style="color:var(--red);font-weight:600;">{rdap_age_days} days ⚠ New domain</span>'
        elif rdap_age_days < 365 * 3:
            _age_str = f'{rdap_age_days // 365}y {rdap_age_days % 365}d'
        else:
            _age_str = f'{rdap_age_days // 365} years'
    else:
        _age_str = '—'

    # RDAP HTML rows
    _rdap_rows = ''
    if rdap_registered:
        _rdap_rows += f'<tr><td class="kv-key">Registered</td><td>{_esc(rdap_registered)}</td></tr>'
    if rdap_expires:
        _rdap_rows += f'<tr><td class="kv-key">Expires</td><td>{_esc(rdap_expires)}</td></tr>'
    if rdap_age_days is not None:
        _rdap_rows += f'<tr><td class="kv-key">Domain Age</td><td>{_age_str}</td></tr>'
    if rdap_registrar:
        _rdap_rows += f'<tr><td class="kv-key">Registrar</td><td>{_esc(rdap_registrar)}</td></tr>'
    if rdap_status:
        _status_pills = ' '.join(
            f'<span style="background:var(--surface2);padding:2px 8px;border-radius:4px;font-size:0.8em;">{_esc(s)}</span>'
            for s in rdap_status[:3]
        )
        _rdap_rows += f'<tr><td class="kv-key">Domain Status</td><td>{_status_pills}</td></tr>'

    # DNSSEC
    dnssec = rd.get('dnssec', {}) or {}
    dnssec_enabled = dnssec.get('enabled', False) if isinstance(dnssec, dict) else False
    dnssec_validated = dnssec.get('validated', False) if isinstance(dnssec, dict) else False
    if dnssec_enabled and dnssec_validated:
        dnssec_display = '<span style="color:var(--green);font-weight:600;">&#x2713; Enabled &amp; Validated</span>'
    elif dnssec_enabled:
        dnssec_display = '<span style="color:var(--yellow);font-weight:600;">&#x26a0; Enabled but not validated</span>'
    else:
        dnssec_display = '<span style="color:var(--red);">&#x2717; Not enabled</span>'
    dnssec_detail = ''
    if dnssec.get('has_dnskey'):
        dnssec_detail += ' <span class="muted" style="font-size:0.82em;">DNSKEY</span>'
    if dnssec.get('has_rrsig'):
        dnssec_detail += ' <span class="muted" style="font-size:0.82em;">RRSIG</span>'
    if dnssec.get('nsec_type'):
        dnssec_detail += f' <span class="muted" style="font-size:0.82em;">{_esc(str(dnssec["nsec_type"]))}</span>'

    # OSINT email harvest
    email_harvest = rd.get('email_harvest', {}) or {}
    harvest_emails_list = email_harvest.get('emails', []) if isinstance(email_harvest, dict) else []
    role_addresses = email_harvest.get('role_addresses', []) if isinstance(email_harvest, dict) else []
    email_patterns = email_harvest.get('patterns', []) if isinstance(email_harvest, dict) else []
    # Classify email sources for clearer labelling:
    # - real_harvested: found in public sources (Hunter, breach DBs, Google)
    # - role_generated: common role addresses generated from the domain pattern
    real_harvested = [e for e in harvest_emails_list
                      if isinstance(e, dict) and e.get('source') not in ('generated', 'pattern', None, '')
                      or (isinstance(e, str) and '@' in e)]
    role_generated = role_addresses  # always pattern-generated
    is_generated = not bool(email_harvest.get('hunter_key_used')) and not real_harvested

    email_html = ''
    if harvest_emails_list or role_addresses:
        email_chips = ''
        for e in harvest_emails_list[:10]:
            addr = e.get('email', str(e)) if isinstance(e, dict) else str(e)
            src = e.get('source', '') if isinstance(e, dict) else ''
            is_gen = src in ('generated', 'pattern') or not src
            chip_col = 'var(--muted)' if is_gen else 'var(--border)'
            email_chips += (
                f'<code style="background:var(--surface);padding:3px 8px;border-radius:4px;'
                f'font-size:0.85em;border:1px solid {chip_col};color:{"var(--muted)" if is_gen else "inherit"};">'
                f'{_esc(addr)}</code> '
            )
        for r in role_addresses[:5]:
            addr = r.get('address', str(r)) if isinstance(r, dict) else str(r)
            email_chips += (
                f'<code style="background:var(--surface);padding:3px 8px;border-radius:4px;'
                f'font-size:0.85em;border:1px solid var(--muted);color:var(--muted);">'
                f'{_esc(addr)}</code> '
            )
        n_emails = len(harvest_emails_list) + len(role_addresses)
        pattern_note = ''
        if email_patterns:
            pat = email_patterns[0].get('pattern', '') if isinstance(email_patterns[0], dict) else str(email_patterns[0])
            if pat:
                pattern_note = f' <span class="muted" style="font-size:0.82em;">Pattern: <code>{_esc(pat)}</code></span>'

        # Label: clarify generated vs harvested
        if is_generated:
            label_hint = ' <span class="muted" style="font-size:0.78em;">(generated from domain pattern — not confirmed)</span>'
        else:
            label_hint = f' <span style="color:var(--green);font-size:0.78em;">({len(real_harvested)} confirmed)</span>'

        email_html = (
            f'<tr><td class="kv-key">Emails (OSINT)</td>'
            f'<td>{email_chips}{pattern_note}{label_hint}</td></tr>'
        )
    elif not harvest_emails_list:
        email_html = '<tr><td class="kv-key">Emails (OSINT)</td><td class="muted">No emails discovered (set HUNTER_API_KEY for confirmed results)</td></tr>'

    spf_cell = '&#x2713; ' + _esc(spf[:100]) if spf else '&#x2717; <span style="color:var(--red);">Missing</span>'
    dmarc_cell = '&#x2713; ' + _esc(dmarc[:100]) if dmarc else '&#x2717; <span style="color:var(--red);">Missing</span>'

    parts.append(f'''
<div class="sec" id="dns">
  <h2>DNS &amp; Email</h2>
  <table>
    <tr><td class="kv-key">NS</td><td class="mono" style="word-break:break-all;">{_esc(ns_display)}</td></tr>
    <tr><td class="kv-key">MX</td><td style="word-break:break-all;">{mx_display}</td></tr>
    <tr><td class="kv-key">CNAME Chain</td><td style="word-break:break-all;">{cname_display}<br><span class="muted" style="font-size:0.82em;">Chain above is for {_esc(host)} → resolve to final IP</span></td></tr>
    {_rdap_rows}
    <tr><td class="kv-key">DNSSEC</td><td>{dnssec_display}{dnssec_detail}</td></tr>
    <tr><td class="kv-key">SPF</td><td>{spf_cell}</td></tr>
    <tr><td class="kv-key">DMARC</td><td>{dmarc_cell}</td></tr>
    {email_html}
  </table>
</div>''')

    # Per-Subdomain WAF/CDN (the main new section)
    if per_sub:
        waf_dist = cloud_dist.get('waf_distribution', {})
        cdn_dist_d = cloud_dist.get('cdn_distribution', {})
        badges = ''
        for name, info in waf_dist.items():
            badges += f'<span class="tag" style="background:rgba(34,197,94,0.15);color:var(--green);">WAF: {_esc(name)} ({info["pct"]}%)</span> '
        for name, info in cdn_dist_d.items():
            badges += f'<span class="tag" style="background:rgba(59,130,246,0.15);color:var(--blue);">CDN: {_esc(name)} ({info["pct"]}%)</span> '
        if cloud_dist.get('multi_waf'):
            badges += '<span class="tag" style="background:rgba(234,179,8,0.15);color:var(--yellow);">Multi-WAF</span> '
        if cloud_dist.get('multi_cdn'):
            badges += '<span class="tag" style="background:rgba(234,179,8,0.15);color:var(--yellow);">Multi-CDN</span> '

        show_limit = 200
        def _sub_sort_key(s):
            has_waf = 1 if s.get('waf') else 0
            has_cdn = 1 if s.get('cdn') else 0
            return (-has_waf, -has_cdn, s.get('subdomain', ''))
        # Only show subdomains with WAF or CDN (unprotected are in Subdomains section)
        protected_subs = [s for s in per_sub if s.get('waf') or s.get('cdn')]
        per_sub_sorted = sorted(protected_subs, key=_sub_sort_key)
        n_unprotected = len(per_sub) - len(protected_subs)
        sr = ''
        for i, s in enumerate(per_sub_sorted[:show_limit]):
            wv = s.get('waf') or '—'
            cv = s.get('cdn') or '—'
            sv = _esc((s.get('server') or '-')[:20])
            ws = 'color:var(--green);font-weight:600;' if s.get('waf') else 'color:var(--red);'
            cs = 'color:var(--blue);font-weight:600;' if s.get('cdn') else 'color:var(--muted);'
            sr += f'<tr><td class="mono">{_esc(s["subdomain"])}</td><td style="{ws}">{_esc(wv)}</td><td style="{cs}">{_esc(cv)}</td><td class="muted">{sv}</td></tr>'

        overflow = f'<p class="muted" style="margin-top:8px;">Showing first {show_limit} of {len(per_sub)} subdomains.</p>' if len(per_sub) > show_limit else ''

        unprotected_note = f'<p class="muted" style="margin-top:8px;font-size:0.85em;">{n_unprotected} subdomain(s) without WAF/CDN protection — see <a href="#subs" style="color:var(--accent);">Subdomains</a> section for details.</p>' if n_unprotected else ''
        parts.append(f'''
<div class="sec" id="waf-cdn">
  <h2>Per-Subdomain WAF / CDN Analysis <span class="count">({len(protected_subs)} protected of {len(per_sub)} probed)</span></h2>
  <div style="margin-bottom:14px;">{badges}</div>
  <details open><summary>Show protected subdomains ({len(protected_subs)})</summary>
  <table><tr><th>Subdomain</th><th>WAF</th><th>CDN</th><th>Server</th></tr>{sr}</table>
  {overflow}{unprotected_note}</details>
</div>''')

    # WAF Gap Analysis
    if gap_findings:
        gf = ''
        for g in gap_findings:
            gs = g.get('severity', 'medium') if isinstance(g, dict) else 'medium'
            gc = SEV_COLORS.get(gs, 'var(--muted)')
            gn = _esc(g.get('technique', '')) if isinstance(g, dict) else ''
            gd = _esc(g.get('description', str(g))) if isinstance(g, dict) else _esc(str(g))
            gf += f'<div class="finding" style="border-left:4px solid {gc};"><span class="sev-badge" style="background:{gc}20;color:{gc};">{gs.upper()}</span> <strong>{gn}</strong> — {gd}</div>'
        parts.append(f'<div class="sec" id="gap"><h2>WAF Gap Analysis</h2>{gf}</div>')

    # Rate Limits
    rl_type = rate_limit.get('detection_type', rate_limit.get('type', 'none')) if isinstance(rate_limit, dict) else 'none'
    rl_thresh = rate_limit.get('threshold_rps', rate_limit.get('threshold')) if isinstance(rate_limit, dict) else None
    rl_headers = rate_limit.get('rate_limit_headers', {}) if isinstance(rate_limit, dict) else {}
    rl_crit = rd.get('rate_limits_critical', {}) or {}
    rl_crit_paths = rl_crit.get('rate_limited_paths', []) if isinstance(rl_crit, dict) else []
    rl_crit_summary = rl_crit.get('summary', '') if isinstance(rl_crit, dict) else ''

    # Infer rate limiting from WAF/CDN when detection returned 'none'
    waf_dist_data = cloud_dist.get('waf_distribution', {})
    cdn_dist_data = cloud_dist.get('cdn_distribution', {})
    rl_inferred = ''
    if rl_type == 'none' and (waf_dist_data or cdn_dist_data):
        waf_names = ', '.join(waf_dist_data.keys())
        cdn_names = ', '.join(cdn_dist_data.keys())
        providers = [p for p in [waf_names, cdn_names] if p]
        rl_inferred = (f'<div style="margin-top:12px;background:var(--surface2);border-radius:10px;padding:14px 18px;border-left:3px solid var(--orange);">'
            f'<p style="font-size:0.9em;font-weight:600;color:var(--orange);margin-bottom:8px;">Inferred Rate Limiting</p>'
            f'<p style="font-size:0.85em;line-height:1.7;">'
            f'WAF/CDN providers detected: <strong>{", ".join(providers)}</strong>. '
            f'These services typically enforce rate limiting at the edge (e.g., AWS WAF rate-based rules, '
            f'Azure Front Door rate limiting, Akamai Bot Manager). '
            f'Rate limits may not be visible via passive header inspection but are likely active.</p>'
            f'<ul style="padding-left:18px;font-size:0.85em;line-height:1.9;margin-top:8px;">'
            f'<li><strong>AWS WAF</strong> — rate-based rules (100-20,000 req/5min per IP), auto-block on threshold</li>'
            f'<li><strong>Azure Front Door</strong> — rate limiting rules with custom thresholds per route</li>'
            f'<li><strong>Akamai</strong> — Bot Manager + Client Reputation, adaptive rate controls</li>'
            f'<li>Run <code>fray recon {_esc(host)} --deep</code> to actively probe rate limit thresholds</li>'
            f'</ul></div>')

    # Rate limit headers found
    rl_hdr_html = ''
    if rl_headers:
        hdr_rows = ''.join(f'<tr><td class="mono">{_esc(k)}</td><td>{_esc(str(v))}</td></tr>' for k, v in rl_headers.items())
        rl_hdr_html = f'<h3 style="margin-top:14px;font-size:0.95em;">Rate Limit Headers</h3><table><tr><th>Header</th><th>Value</th></tr>{hdr_rows}</table>'

    # Critical path rate limiting
    # Recommended critical paths to test when not enough were probed
    _CRITICAL_RL_PATHS = [
        "/login", "/signin", "/auth/login", "/api/auth/login",
        "/signup", "/register", "/api/auth/signup",
        "/api/v1", "/api/v2", "/api",
        "/password-reset", "/forgot-password",
        "/i/flow/login",       # Twitter/X
        "/oauth/token",        # OAuth
        "/graphql",
    ]
    rl_crit_html = ''
    tested_paths = {p.get("path", "") for p in rl_crit_paths if isinstance(p, dict)}
    untested_important = [p for p in _CRITICAL_RL_PATHS if p not in tested_paths][:6]

    if rl_crit_paths:
        cp_rows = ''
        for p in rl_crit_paths[:10]:
            path = p.get("path", "") if isinstance(p, dict) else str(p)
            status = p.get("status", "") if isinstance(p, dict) else ""
            ptype = p.get("type", "") if isinstance(p, dict) else ""
            limited = p.get("rate_limited", False) if isinstance(p, dict) else False
            row_col = 'color:var(--green);' if limited else 'color:var(--muted);'
            cp_rows += (f'<tr>'
                        f'<td class="mono">{_esc(path)}</td>'
                        f'<td>{_esc(str(status))}</td>'
                        f'<td class="muted">{_esc(str(ptype))}</td>'
                        f'<td style="{row_col}">{"✓ Rate limited" if limited else "✗ Not limited"}</td>'
                        f'</tr>')
        rl_crit_html = (
            f'<h3 style="margin-top:14px;font-size:0.95em;">Critical Path Rate Limiting</h3>'
            f'<table><tr><th>Path</th><th>Status</th><th>Type</th><th>Rate Limit</th></tr>'
            f'{cp_rows}</table>'
        )
        if untested_important:
            rl_crit_html += (
                f'<p style="margin-top:10px;font-size:0.85em;color:var(--text2);">'
                f'<strong>Recommended paths to also test:</strong> '
                + ', '.join(f'<code>{_esc(p)}</code>' for p in untested_important)
                + f' — run: <code>fray test https://{_esc(host)}/<i>path</i> -c rate_limit</code>'
                f'</p>'
            )
    elif rl_crit_summary:
        rl_crit_html = f'<p class="muted" style="margin-top:8px;font-size:0.85em;">{_esc(rl_crit_summary)}</p>'

    # Always recommend critical paths if nothing tested yet
    if not rl_crit_paths and not rl_crit_summary:
        suggested_paths = ', '.join(f'<code>{_esc(p)}</code>' for p in _CRITICAL_RL_PATHS[:8])
        rl_crit_html = (
            f'<div style="margin-top:12px;background:var(--surface2);border-radius:8px;'
            f'padding:12px 16px;border-left:3px solid var(--yellow);">'
            f'<p style="font-size:0.88em;font-weight:600;color:var(--yellow);margin-bottom:6px;">'
            f'Critical Path Rate Limiting — Not Tested</p>'
            f'<p style="font-size:0.85em;line-height:1.7;color:var(--text2);">'
            f'Rate limiting on sensitive endpoints (login, API, signup) was not verified. '
            f'Missing rate limits allow credential stuffing and brute-force attacks.<br>'
            f'<strong>Recommended paths to test:</strong> {suggested_paths}</p>'
            f'<p style="margin-top:8px;font-size:0.82em;">'
            f'<code>fray test https://{_esc(host)}/login -c rate_limit</code></p>'
            f'</div>'
        )

    rl_status_color = 'var(--green)' if rl_type != 'none' else 'var(--red)'
    parts.append(f'''
<div class="sec" id="rl">
  <h2>Rate Limits</h2>
  <table>
    <tr><td class="kv-key">Detection</td><td style="color:{rl_status_color};font-weight:600;">{_esc(str(rl_type))}</td></tr>
    <tr><td class="kv-key">Threshold</td><td>{rl_thresh or '<span class="muted">Not detected via headers</span>'}</td></tr>
  </table>
  {rl_hdr_html}{rl_crit_html}{rl_inferred}
</div>''')

    # ── VPN Endpoints ──
    if vpn_list:
        vpn_rows = ''
        for v in vpn_list:
            prod = _esc(v.get('label', ''))
            paths = ', '.join(v.get('paths', [])[:3])
            sigs = ', '.join(v.get('signals', [])[:2])
            sev_note = v.get('severity_note') or ''
            verified = v.get('verified_cves', [])
            potential = v.get('potential_cves', [])

            # Severity color
            if sev_note.startswith('Critical') or verified:
                sev_col = 'var(--red)'
                sev_label = 'CRITICAL'
            elif sev_note.startswith('High'):
                sev_col = 'var(--orange)'
                sev_label = 'HIGH'
            else:
                sev_col = 'var(--yellow)'
                sev_label = 'MEDIUM'

            cve_badges = ''
            for cv in verified:
                cve_badges += f'<span class="sev-badge" style="background:var(--red)20;color:var(--red);font-size:0.78em;">{_esc(cv)} &#x2713;</span> '
            for cv in potential:
                cve_badges += f'<span class="sev-badge" style="background:var(--yellow)20;color:var(--yellow);font-size:0.78em;">{_esc(cv)} ?</span> '

            vpn_rows += f'''<tr>
  <td><strong style="color:{sev_col};">{prod}</strong></td>
  <td><span class="sev-badge" style="background:{sev_col}20;color:{sev_col};">{sev_label}</span></td>
  <td class="mono" style="font-size:0.82em;">{_esc(paths)}</td>
  <td style="font-size:0.82em;">{cve_badges or '<span class="muted">—</span>'}</td>
  <td class="muted" style="font-size:0.82em;">{_esc(sigs[:80])}</td>
</tr>'''

        # CVE detail table
        cve_detail = ''
        if vpn_cve_findings:
            cve_rows = ''
            for c in sorted(vpn_cve_findings, key=lambda x: -(x.get('cvss', 0) or 0)):
                cvss = c.get('cvss', 0)
                cvss_col = 'var(--red)' if cvss >= 9 else 'var(--orange)' if cvss >= 7 else 'var(--yellow)'
                verified_icon = '&#x2713;' if c.get('verified') else '&#x26a0;'
                ver_col = 'var(--green)' if c.get('verified') else 'var(--yellow)'
                evidence = '; '.join(c.get('evidence', [])[:2])
                cve_rows += f'''<tr>
  <td><strong>{_esc(c.get("cve_id", ""))}</strong></td>
  <td style="color:{cvss_col};font-weight:700;">{cvss}</td>
  <td style="color:{ver_col};">{verified_icon}</td>
  <td style="font-size:0.84em;">{_esc(c.get("description", "")[:100])}</td>
  <td class="muted" style="font-size:0.82em;">{_esc(c.get("affected_versions", "")[:60])}</td>
  <td style="font-size:0.82em;">{_esc(c.get("remediation", "")[:80])}</td>
</tr>'''
            cve_detail = f'''<details style="margin-top:14px;"><summary style="cursor:pointer;font-weight:600;font-size:0.92em;color:var(--accent);">CVE Verification Details ({len(vpn_cve_findings)})</summary>
  <table style="margin-top:8px;"><tr><th>CVE</th><th>CVSS</th><th>Status</th><th>Description</th><th>Affected</th><th>Remediation</th></tr>{cve_rows}</table>
</details>'''

        # Sub-VPN findings
        sub_vpn_rows = ''
        sub_vpn_list = sub_sec.get('vpn_endpoints', []) if isinstance(sub_sec, dict) else []
        if sub_vpn_list:
            for sf, vd in sub_vpn_list[:10]:
                for sv in vd.get('vpn_endpoints', []):
                    sub_vpn_rows += f'<tr><td class="mono">{_esc(sf)}</td><td><strong>{_esc(sv.get("label", ""))}</strong></td><td class="mono" style="font-size:0.82em;">{_esc(", ".join(sv.get("paths", [])[:2]))}</td></tr>'
            if sub_vpn_rows:
                sub_vpn_rows = f'<details style="margin-top:14px;"><summary style="cursor:pointer;font-size:0.85em;color:var(--accent);">Subdomain VPN Findings ({len(sub_vpn_list)})</summary><table style="margin-top:8px;"><tr><th>Subdomain</th><th>Vendor</th><th>Paths</th></tr>{sub_vpn_rows}</table></details>'

        n_verified = len(vpn_data.get('verified_cves', []))
        n_potential = len(vpn_data.get('potential_cves', []))
        cve_summary = ''
        if n_verified:
            cve_summary += f' <span style="color:var(--red);font-weight:600;">{n_verified} verified CVE(s)</span>'
        if n_potential:
            cve_summary += f' <span style="color:var(--yellow);">{n_potential} potential</span>'

        parts.append(f'''
<div class="sec" id="vpn">
  <h2>VPN / Remote Access Endpoints <span class="count">({n_vpn} vendor(s){cve_summary})</span></h2>
  <div style="margin-bottom:14px;background:var(--surface2);border-radius:10px;padding:14px 18px;border-left:3px solid var(--red);">
    <p style="font-size:0.9em;line-height:1.6;margin:0;">Enterprise VPN concentrators are high-priority targets — consistently in <strong>CISA KEV</strong> and exploited by ransomware groups for initial network access. Each detected vendor is checked against known CVEs with safe, non-destructive probes.</p>
  </div>
  <table><tr><th>Vendor</th><th>Severity</th><th>Detected Paths</th><th>CVEs</th><th>Detection Signals</th></tr>{vpn_rows}</table>
  {cve_detail}{sub_vpn_rows}
</div>''')

    # ── API Security ──
    _api_has_data = (n_api_specs > 0 or
                     (isinstance(api_gw, dict) and api_gw.get('detected')) or
                     (isinstance(api_rate, dict) and api_rate.get('detected')) or
                     (isinstance(api_auth, dict) and api_auth.get('detected')) or
                     (isinstance(api_endpoints, list) and len(api_endpoints) > 0))
    if _api_has_data:
        # ── API Gateway — show which headers were found and what they mean ──
        gw_html = '<span class="muted">Not detected via response headers</span>'
        if isinstance(api_gw, dict) and api_gw.get('detected'):
            gw_vendor_rows = []
            for hdr, info in api_gw.items():
                if hdr == 'detected':
                    continue
                if isinstance(info, dict):
                    vendor = info.get('vendor', hdr)
                    hdr_val = info.get('value', '')
                    # Explain what this header means in plain language
                    _GW_EXPLANATIONS = {
                        'x-amzn-requestid':     'AWS API Gateway — request tracking ID',
                        'x-kong-proxy-latency': 'Kong API Gateway — proxy processing time',
                        'x-kong-upstream-latency': 'Kong API Gateway — upstream service latency',
                        'x-envoy-upstream-service-time': 'Envoy/Istio service mesh — upstream timing',
                        'x-request-id':         'Request correlation ID (generic gateway/CDN)',
                        'traceparent':           'OpenTelemetry W3C trace (distributed tracing)',
                        'x-goog-api-client':    'Google Cloud API Gateway / Endpoints',
                        'cf-apim':              'Cloudflare API Shield (API security layer)',
                    }
                    explanation = _GW_EXPLANATIONS.get(hdr.lower(), vendor)
                    gw_vendor_rows.append(
                        f'<div style="margin-bottom:4px;">'
                        f'<code style="font-size:0.82em;background:var(--surface);padding:1px 6px;border-radius:3px;">{_esc(hdr)}</code>'
                        f'<span class="muted" style="font-size:0.82em;"> → {_esc(explanation)}</span>'
                        f'</div>'
                    )
            if gw_vendor_rows:
                gw_html = ''.join(gw_vendor_rows)
            else:
                gw_html = '<span style="color:var(--green);">Detected — vendor unidentified from response headers</span>'

        # ── Rate limiting ─────────────────────────────────────────────────
        rl_api_html = '<span style="color:var(--red);font-weight:600;">&#x2717; Not Detected</span>'
        if isinstance(api_rate, dict) and api_rate.get('detected'):
            rl_api_html = '<span style="color:var(--green);font-weight:600;">&#x2713; Detected</span>'
            rl_hdrs = {k: v for k, v in api_rate.items() if k != 'detected'}
            if rl_hdrs:
                _RL_EXPLANATIONS = {
                    'x-ratelimit-limit':     'Max requests per window',
                    'x-ratelimit-remaining': 'Requests remaining in window',
                    'x-ratelimit-reset':     'Window reset time (Unix timestamp)',
                    'ratelimit-limit':       'Max requests per window (IETF draft)',
                    'retry-after':           'Seconds until retry allowed (429)',
                }
                rl_parts = []
                for k, v in list(rl_hdrs.items())[:3]:
                    meaning = _RL_EXPLANATIONS.get(k.lower(), '')
                    rl_parts.append(
                        f'<code style="font-size:0.82em;">{_esc(k)}: {_esc(str(v))}</code>'
                        + (f' <span class="muted" style="font-size:0.78em;">({meaning})</span>' if meaning else '')
                    )
                rl_api_html += ' — ' + ', '.join(rl_parts)

        # ── Authentication — specific method detected ───────────────────────
        _AUTH_SIGNALS_MAP = {
            'bearer':  ('JWT / Bearer Token', 'var(--green)',
                        'Token in Authorization header. Check alg:none bypass.'),
            'jwt':     ('JWT', 'var(--green)', 'JSON Web Token. Check weak secret, alg confusion.'),
            'api_key': ('API Key', 'var(--yellow)', 'Key in header. Verify rotation and scope.'),
            'x-api-key': ('API Key (X-Api-Key)', 'var(--yellow)', 'API key in X-Api-Key header.'),
            'oauth2':  ('OAuth2', 'var(--green)', 'Verify PKCE, state param, redirect_uri.'),
            'basic':   ('HTTP Basic Auth', 'var(--red)', 'Base64 creds. HTTPS required.'),
            'mtls':    ('mTLS (Mutual TLS)', 'var(--green)', 'Client cert required. Strong machine-to-machine auth.'),
            'session': ('Session Cookie', 'var(--yellow)', 'Verify SameSite, Secure, HttpOnly flags.'),
            'saml':    ('SAML 2.0', 'var(--green)', 'Check XML signature wrapping, XXE.'),
            'hmac':    ('HMAC Signature', 'var(--green)', 'Verify nonce/timestamp for replay protection.'),
        }
        auth_html = '<span style="color:var(--red);font-weight:600;">&#x2717; Not Detected</span>'
        auth_note = (
            f'<span class="muted" style="font-size:0.82em;display:block;margin-top:4px;">'
            f'Unauthenticated — endpoints accessible without credentials. '
            f'Check: <code>fray test https://{_esc(host)}/api -c auth_bypass</code>'
            f'</span>'
        )
        if isinstance(api_auth, dict) and api_auth.get('detected'):
            auth_methods = []
            auth_schemes = {k: v for k, v in api_auth.items() if k != 'detected'}
            for signal, val in auth_schemes.items():
                sig_lower = signal.lower()
                matched = False
                for key, (label, color, note) in _AUTH_SIGNALS_MAP.items():
                    if key in sig_lower:
                        auth_methods.append(
                            f'<strong style="color:{color};">{_esc(label)}</strong>'
                            f'<span class="muted" style="font-size:0.78em;display:block;margin-left:8px;">{_esc(note)}</span>'
                        )
                        matched = True
                        break
                if not matched and signal not in ('detected',):
                    auth_methods.append(
                        f'<strong style="color:var(--cyan);">{_esc(str(signal))}</strong>'
                        f': {_esc(str(val)[:60])}'
                    )
            if auth_methods:
                auth_html = '<br>'.join(auth_methods)
                auth_note = ''
            else:
                auth_html = '<span style="color:var(--green);font-weight:600;">&#x2713; Detected</span>'
                auth_note = ''
        auth_html = auth_html + auth_note

        # Exposed specs table
        spec_rows = ''
        if isinstance(api_specs, list) and api_specs:
            for s in api_specs[:10]:
                if isinstance(s, dict):
                    spath = _esc(s.get('path', ''))
                    scat = _esc(s.get('category', ''))
                    sst = s.get('status', 0)
                    ssev = s.get('severity', 'info')
                    sc = SEV_COLORS.get(ssev, 'var(--muted)')
                    spec_rows += f'<tr><td class="mono">{spath}</td><td>{scat}</td><td style="color:{sc};font-weight:600;">{sst}</td><td><span class="sev-badge" style="background:{sc}20;color:{sc};">{ssev.upper()}</span></td></tr>'
            spec_rows = f'<details style="margin-top:14px;"><summary style="cursor:pointer;font-size:0.85em;color:var(--accent);">Exposed API Specs / Docs ({len(api_specs)})</summary><table style="margin-top:8px;"><tr><th>Path</th><th>Category</th><th>Status</th><th>Severity</th></tr>{spec_rows}</table></details>'

        # Sub-API findings
        sub_api_list = sub_sec.get('api_security', []) if isinstance(sub_sec, dict) else []
        sub_api_html = ''
        if sub_api_list:
            sa_rows = ''
            for sf, ad in sub_api_list[:10]:
                n_sp = ad.get('total_specs', 0)
                gw_det = '&#x2713;' if ad.get('api_gateway', {}).get('detected') else '&#x2717;'
                rl_det = '&#x2713;' if ad.get('rate_limiting', {}).get('detected') else '&#x2717;'
                au_det = '&#x2713;' if ad.get('authentication', {}).get('detected') else '&#x2717;'
                sc_det = '&#x2713;' if ad.get('schema_validation', {}).get('detected') else '&#x2717;'
                sv_det = '&#x2713;' if ad.get('security_vendors', {}).get('detected') else '-'
                posture = ad.get('security_posture', 'unknown')
                posture_col = {'strong':'var(--green)','good':'var(--green)','partial':'var(--yellow)','none':'var(--red)'}.get(posture, 'var(--muted)')
                sa_rows += (f'<tr><td class="mono">{_esc(sf)}</td><td>{n_sp}</td>'
                            f'<td>{gw_det}</td><td>{rl_det}</td><td>{au_det}</td>'
                            f'<td>{sc_det}</td><td>{sv_det}</td>'
                            f'<td style="color:{posture_col};font-weight:600">{posture}</td></tr>')
            sub_api_html = (f'<details style="margin-top:14px;"><summary style="cursor:pointer;font-size:0.85em;color:var(--accent);">'
                            f'Subdomain API Findings ({len(sub_api_list)})</summary>'
                            f'<table style="margin-top:8px;"><tr><th>Subdomain</th><th>Specs</th>'
                            f'<th>Gateway</th><th>Rate Limit</th><th>Auth</th>'
                            f'<th>Schema</th><th>Vendor</th><th>Posture</th></tr>{sa_rows}</table></details>')

        # Schema validation and security vendor display
        schema_html = '<span class="muted">Not detected</span>'
        if isinstance(api_schema, dict) and api_schema.get('detected'):
            signals = api_schema.get('signals', [])
            schema_html = (f'<span style="color:var(--green);font-weight:600;">&#x2713; Detected</span>'
                           f'<span class="muted" style="font-size:0.82em;margin-left:6px;">'
                           f'{", ".join(signals[:3])}</span>')

        sec_vendor_html = '<span class="muted">Not detected</span>'
        if isinstance(api_security_vendors, dict) and api_security_vendors.get('detected'):
            vendor_products = [v.get('product', k) for k, v in list(api_security_vendors.get('products', {}).items())[:3]]
            sec_vendor_html = f'<span style="color:var(--cyan);font-weight:600;">{", ".join(vendor_products)}</span>'

        oidc_html = ''
        if isinstance(api_oidc, dict) and api_oidc.get('discovered'):
            issuer = api_oidc.get('issuer', 'OIDC/OAuth2')
            oidc_html = f'<tr><td class="kv-key">OIDC/OAuth2</td><td><span style="color:var(--green);font-weight:600;">&#x2713; {_esc(issuer[:60])}</span></td></tr>'

        # Security posture badge
        posture_colors = {
            'strong': ('var(--green)', '&#x1F6E1; Strong — multiple security controls active'),
            'good':   ('var(--green)', '&#x2713; Good — authentication + rate limiting'),
            'partial':('var(--yellow)', '&#x26A0; Partial — some controls, verify completeness'),
            'none':   ('var(--red)',    '&#x2717; None — no security controls detected'),
            'unknown':('var(--muted)', '&#x2753; Unknown'),
        }
        p_col, p_label = posture_colors.get(api_posture, posture_colors['unknown'])
        posture_html = f'<span style="color:{p_col};font-weight:600;">{p_label}</span>'
        if api_controls:
            posture_html += f'<div style="margin-top:4px;font-size:0.82em;color:var(--muted);">Controls: {", ".join(api_controls[:4])}</div>'

        api_summary = api_sec.get('summary', '') if isinstance(api_sec, dict) else ''
        parts.append(f'''
<div class="sec" id="apisec">
  <h2>API Security <span class="count">({n_api_specs} spec(s) exposed)</span></h2>
  <table>
    <tr><td class="kv-key" style="width:160px;">Security Posture</td><td>{posture_html}</td></tr>
    <tr><td class="kv-key">API Gateway</td><td>{gw_html}</td></tr>
    <tr><td class="kv-key">Rate Limiting</td><td>{rl_api_html}</td></tr>
    <tr><td class="kv-key">Authentication</td><td>{auth_html}</td></tr>
    <tr><td class="kv-key">Schema Validation</td><td>{schema_html}</td></tr>
    <tr><td class="kv-key">API Security Vendor</td><td>{sec_vendor_html}</td></tr>
    {oidc_html}
    <tr><td class="kv-key">Specs Exposed</td><td>{('<span style="color:var(--red);font-weight:600;">' + str(n_api_specs) + ' spec(s) — review for sensitive data</span>') if n_api_specs else '<span style="color:var(--green);">None exposed</span>'}</td></tr>
  </table>
  {f'<p class="muted" style="margin-top:8px;font-size:0.85em;">{_esc(api_summary)}</p>' if api_summary else ''}
  {spec_rows}{sub_api_html}
</div>''')

    # ── Cloud Buckets ──
    if n_buckets > 0 or n_public_buckets > 0:
        _BUCKET_VENDOR_COLORS = {
            # AWS S3 variants
            's3':          ('var(--orange)', 'AWS S3'),
            'aws_s3':      ('var(--orange)', 'AWS S3'),
            'aws':         ('var(--orange)', 'AWS S3'),
            'amazonaws':   ('var(--orange)', 'AWS S3'),
            # Azure
            'azure':       ('#3b82f6', 'Azure Blob'),
            'azure_blob':  ('#3b82f6', 'Azure Blob'),
            'azureblob':   ('#3b82f6', 'Azure Blob'),
            'windows.net': ('#3b82f6', 'Azure Blob'),
            # Google Cloud
            'gcs':         ('var(--green)', 'Google Cloud Storage'),
            'gcp':         ('var(--green)', 'Google Cloud Storage'),
            'google':      ('var(--green)', 'Google Cloud Storage'),
            'storage.googleapis.com': ('var(--green)', 'Google Cloud Storage'),
            # Alibaba
            'alibaba':     ('#ff6a00', 'Alibaba OSS'),
            'aliyun':      ('#ff6a00', 'Alibaba OSS'),
            'oss':         ('#ff6a00', 'Alibaba OSS'),
            # DigitalOcean
            'digitalocean': ('#0080ff', 'DigitalOcean Spaces'),
            'spaces':       ('#0080ff', 'DigitalOcean Spaces'),
            # Cloudflare R2
            'r2':           ('#f48120', 'Cloudflare R2'),
            'cloudflare':   ('#f48120', 'Cloudflare R2'),
             # Backblaze
            'backblaze':    ('#d00000', 'Backblaze B2'),
            'b2':           ('#d00000', 'Backblaze B2'),
            # Wasabi
            'wasabi':       ('#00b300', 'Wasabi Hot Cloud Storage'),
            's3.wasabi':    ('#00b300', 'Wasabi Hot Cloud Storage'),
            # Oracle Cloud Object Storage
            'oracle':       ('#c74634', 'Oracle Cloud Object Storage'),
            'oraclecloud':  ('#c74634', 'Oracle Cloud Object Storage'),
            'objectstorage.oraclecloud': ('#c74634', 'Oracle Cloud Object Storage'),
            'oci':          ('#c74634', 'Oracle Cloud Object Storage'),
            # Sakura Internet (Japan)
            'sakura':       ('#e60033', 'Sakura Object Storage'),
            'sakuracloud':  ('#e60033', 'Sakura Object Storage'),
            'is.sakura':    ('#e60033', 'Sakura Object Storage'),
            # Tencent Cloud
            'tencent':      ('#00a3e0', 'Tencent Cloud COS'),
            'myqcloud':     ('#00a3e0', 'Tencent Cloud COS'),
            'cos':          ('#00a3e0', 'Tencent Cloud COS'),
            # Huawei Cloud
            'huawei':       ('#cf0a2c', 'Huawei OBS'),
            'obs':          ('#cf0a2c', 'Huawei OBS'),
            # Linode / Akamai
            'linode':       ('#00b300', 'Linode Object Storage'),
            'linodeobjects':('#00b300', 'Linode Object Storage'),
            # Vultr
            'vultr':        ('#007bfc', 'Vultr Object Storage'),
            'vultrobjects': ('#007bfc', 'Vultr Object Storage'),
            # MinIO (self-hosted)
            'minio':        ('#c72c41', 'MinIO'),
        }

        def _bucket_vendor(key: str):
            """Normalise raw bucket vendor key → (color, label)."""
            if not key:
                return 'var(--muted)', 'Unknown'
            kl = key.lower().replace('-', '_').replace('.', '_')
            # Direct lookup first
            if kl in _BUCKET_VENDOR_COLORS:
                return _BUCKET_VENDOR_COLORS[kl]
            # Substring match
            for pat, val in _BUCKET_VENDOR_COLORS.items():
                if pat in kl or pat in key.lower():
                    return val
            # Human-readable fallback: replace underscores, title-case
            label = key.replace('_', ' ').replace('-', ' ').title()
            return 'var(--muted)', label

        bkt_rows = ''
        for b in bucket_list[:30]:
            if not isinstance(b, dict):
                continue
            bname = _esc(b.get('name', ''))
            burl = _esc(b.get('url', ''))
            bvendor_key = b.get('provider', b.get('vendor', ''))
            bvendor_col, bvendor_label = _bucket_vendor(
                str(bvendor_key) if bvendor_key else '')
            pub_read = b.get('public_read', False)
            pub_list = b.get('public_listing', False)
            found_on = b.get('found_on', '')
            status = b.get('status', '')

            access_badges = ''
            if pub_read:
                access_badges += '<span class="sev-badge" style="background:var(--red)20;color:var(--red);">PUBLIC READ</span> '
            if pub_list:
                access_badges += '<span class="sev-badge" style="background:var(--red)20;color:var(--red);">PUBLIC LIST</span> '
            if not pub_read and not pub_list:
                access_badges = '<span class="muted">Private</span>'

            # Build full URLs for bucket URL and found_on
            raw_burl = b.get('url', '')
            if raw_burl and not raw_burl.startswith('http'):
                raw_burl = f'https://{raw_burl}'
            burl_display = (f'<a href="{_esc(raw_burl)}" target="_blank" '
                            f'style="color:var(--accent2);text-decoration:none;font-size:0.82em;">'
                            f'{_esc(raw_burl)}</a>') if raw_burl else f'<span class="muted">{bname}</span>'

            raw_found_on = found_on or host
            if raw_found_on and not raw_found_on.startswith('http'):
                raw_found_on = f'https://{raw_found_on}'
            found_on_display = (f'<a href="{_esc(raw_found_on)}" target="_blank" '
                                f'style="color:var(--muted);font-size:0.82em;text-decoration:none;">'
                                f'{_esc(raw_found_on)}</a>')

            bkt_rows += f'''<tr>
  <td class="mono" style="font-size:0.85em;">{burl_display}</td>
  <td><span class="type-badge" style="background:{bvendor_col}20;color:{bvendor_col};">{bvendor_label}</span></td>
  <td>{access_badges}</td>
  <td>{found_on_display}</td>
  <td class="muted" style="font-size:0.82em;">{status}</td>
</tr>'''

        # Sub-bucket findings
        sub_bkt_list = sub_sec.get('cloud_buckets', []) if isinstance(sub_sec, dict) else []
        sub_bkt_html = ''
        if sub_bkt_list:
            sb_rows = ''
            for sf, bd in sub_bkt_list[:10]:
                n_pub = bd.get('total_public', 0)
                n_found = bd.get('total_found', 0)
                sb_rows += f'<tr><td class="mono">{_esc(sf)}</td><td>{n_found}</td><td style="color:{"var(--red)" if n_pub else "var(--green)"};">{n_pub}</td></tr>'
            sub_bkt_html = f'<details style="margin-top:14px;"><summary style="cursor:pointer;font-size:0.85em;color:var(--accent);">Subdomain Bucket Findings ({len(sub_bkt_list)})</summary><table style="margin-top:8px;"><tr><th>Subdomain</th><th>Total</th><th>Public</th></tr>{sb_rows}</table></details>'

        pub_color = 'var(--red)' if n_public_buckets else 'var(--green)'
        pub_warning = '<div style="margin-bottom:14px;background:var(--surface2);border-radius:10px;padding:14px 18px;border-left:3px solid var(--red);"><p style="font-size:0.9em;line-height:1.6;margin:0;"><strong style="color:var(--red);">Public buckets detected!</strong> These cloud storage containers are accessible without authentication. Data exfiltration, backup leakage, and sensitive file exposure are immediate risks.</p></div>' if n_public_buckets else ''
        parts.append(f'''
<div class="sec" id="buckets">
  <h2>Cloud Storage Buckets <span class="count">({n_buckets} found, <span style="color:{pub_color};">{n_public_buckets} public</span>)</span></h2>
  {pub_warning}
  <table><tr><th>Bucket</th><th>Vendor</th><th>Access</th><th>Found On</th><th>Status</th></tr>{bkt_rows}</table>
  {sub_bkt_html}
</div>''')

    # Subdomains
    if sub_list:
        src_line = f'<p class="muted" style="margin-bottom:10px;">Sources: {_esc(", ".join(f"{k}: {v}" for k, v in sub_sources.items()))}</p>' if sub_sources else ''
        waf_bypass_html = ''
        if waf_bypass_subs:
            wb_rows = ''
            for s in waf_bypass_subs[:20]:
                if isinstance(s, dict):
                    sd = _esc(s.get('subdomain', ''))
                    ips = _esc(', '.join(s.get('ips', []))) if s.get('ips') else '<span class="muted">—</span>'
                    reason = _esc(s.get('reason', ''))
                else:
                    sd = _esc(str(s))
                    ips = '<span class="muted">—</span>'
                    reason = ''
                wb_rows += f'<tr><td class="mono">{sd}</td><td class="mono">{ips}</td><td class="muted">{reason}</td></tr>'
            waf_bypass_html = (
                f'<p style="color:var(--red);font-weight:600;margin-bottom:12px;">&#x26a0; WAF Bypass — '
                f'{len(waf_bypass_subs)} subdomain(s) skip {_esc(str(waf_vendor))}</p>'
                f'<details><summary>Show WAF bypass subdomains ({len(waf_bypass_subs)})</summary>'
                f'<table><tr><th>Subdomain</th><th>IPs</th><th>Reason</th></tr>{wb_rows}</table></details>'
            )

        show_sub_limit = 200
        sub_rows = ''.join(f'<tr><td class="mono">{_esc(s)}</td></tr>' for s in sub_list[:show_sub_limit])
        sub_overflow = f' (first {show_sub_limit} of {n_subs})' if n_subs > show_sub_limit else ''

        parts.append(f'''
<div class="sec" id="subs">
  <h2>Subdomains <span class="count">({n_subs} unique)</span></h2>
  {src_line}{waf_bypass_html}
  <details><summary>Show subdomains{sub_overflow}</summary>
  <table><tr><th>Subdomain</th></tr>{sub_rows}</table></details>
</div>''')

    # Probes
    if probe_results:
        pr = ''
        for p in probe_results[:30]:
            st = p.get('status', 0)
            st_col = 'var(--green)' if 200 <= st < 300 else 'var(--orange)' if 300 <= st < 400 else 'var(--red)' if st >= 400 else 'var(--muted)'
            pr += f'<tr><td class="mono">{_esc(p.get("subdomain",""))}</td><td style="color:{st_col};font-weight:700;">{st}</td><td class="muted">{_esc(p.get("title","")[:50])}</td><td>{_esc(",".join(p.get("surfaces",[])))}</td></tr>'
        parts.append(f'''
<div class="sec" id="probes">
  <h2>Subdomain Probes <span class="count">({n_responsive}/{n_probes} responsive)</span></h2>
  <table><tr><th>Subdomain</th><th>Status</th><th>Title</th><th>Surfaces</th></tr>{pr}</table>
</div>''')

    # Origin IPs — with cloud provider detection per IP
    def _classify_ip_provider(ip_str: str) -> str:
        """Return cloud/ISP name for known IP ranges."""
        import re as _re
        ip = ip_str.strip()
        # IPv6 Google (2404:6800::/32, 2607:f8b0::/32, 2001:4860::/32, etc.)
        if ip.startswith(('2404:6800:', '2607:f8b0:', '2001:4860:', '2800:3f0:', '2a00:1450:')):
            return 'Google / GCP'
        # IPv6 Twitter/X infrastructure
        if ip.startswith(('2400::', '2606:4700:')):
            return 'Twitter / Cloudflare'
        # IPv4 Google
        if any(ip.startswith(p) for p in ('34.', '35.', '104.196.', '104.197.', '104.198.')):
            return 'Google Cloud / GCP'
        # IPv4 AWS
        if any(ip.startswith(p) for p in ('52.', '54.', '3.', '18.', '13.', '15.197.')):
            return 'Amazon Web Services'
        # IPv4 Azure
        if any(ip.startswith(p) for p in ('20.', '40.', '65.52.')):
            return 'Microsoft Azure'
        # Cloudflare
        if any(ip.startswith(p) for p in ('104.16.', '104.17.', '104.18.', '104.19.',
                                            '104.20.', '104.21.', '172.64.', '172.65.',
                                            '172.66.', '172.67.')):
            return 'Cloudflare'
        # Twitter/X specific ranges
        if any(ip.startswith(p) for p in ('199.16.156.', '199.59.148.', '199.59.149.',
                                            '199.59.150.', '199.59.151.')):
            return 'Twitter (X Corp)'
        # Fastly
        if any(ip.startswith(p) for p in ('151.101.', '199.27.')):
            return 'Fastly CDN'
        # Generic Google prefix detection for IPv6
        if ':4860:' in ip or ':f8b0:' in ip or ':6800:' in ip:
            return 'Google / GCP'
        return ''

    if origin_list:
        oi = ''
        provider_counts: dict = {}
        for o in origin_list[:30]:
            if isinstance(o, dict):
                ip_val = o.get("ip", "")
                src = o.get("source", "")
                provider = _classify_ip_provider(ip_val)
                if provider:
                    provider_counts[provider] = provider_counts.get(provider, 0) + 1
                provider_badge = (
                    f'<span style="background:var(--surface2);padding:1px 6px;border-radius:4px;'
                    f'font-size:0.78em;color:var(--text2);">{_esc(provider)}</span>'
                    if provider else ''
                )
                oi += (f'<tr><td class="mono">{_esc(ip_val)}</td>'
                       f'<td class="muted">{_esc(src)}</td>'
                       f'<td>{provider_badge}</td></tr>')
            else:
                ip_val = str(o)
                provider = _classify_ip_provider(ip_val)
                provider_badge = (
                    f'<span style="background:var(--surface2);padding:1px 6px;border-radius:4px;'
                    f'font-size:0.78em;">{_esc(provider)}</span>' if provider else ''
                )
                oi += f'<tr><td class="mono">{_esc(ip_val)}</td><td></td><td>{provider_badge}</td></tr>'

        # Build provider summary
        provider_summary = ''
        if provider_counts:
            provider_parts = ', '.join(
                f'<strong>{_esc(p)}</strong> ({c})'
                for p, c in sorted(provider_counts.items(), key=lambda x: -x[1])
            )
            provider_summary = (
                f'<p style="margin-bottom:12px;font-size:0.88em;color:var(--text2);">'
                f'Hosting providers: {provider_parts}</p>'
            )
        origin_rec = f'''<div style="margin-top:16px;background:var(--surface2);border-radius:10px;padding:14px 18px;border-left:3px solid var(--orange);">
  <p style="font-size:0.9em;font-weight:600;color:var(--orange);margin-bottom:8px;">Recommendations:</p>
  <ul style="padding-left:18px;font-size:0.85em;line-height:1.9;color:var(--text);">
    <li><strong>Restrict origin access</strong> — configure firewall rules (iptables, security groups, NSGs) to allow inbound traffic only from your CDN/WAF IP ranges</li>
    <li><strong>Enable origin cloaking</strong> — remove DNS records that directly expose origin IPs (e.g., mail, webmail, ftp subdomains)</li>
    <li><strong>Rotate origin IPs</strong> — if origin IPs are already leaked, migrate to new IPs and ensure they are never published in DNS</li>
    <li><strong>Use authenticated origin pulls</strong> — configure your CDN (Cloudflare, AWS CloudFront) to send a secret header that the origin validates before responding</li>
    <li><strong>Monitor for leaks</strong> — run <code>fray recon {_esc(host)} --deep</code> periodically to detect newly exposed origin IPs</li>
  </ul>
</div>'''
        parts.append(f'''
<div class="sec" id="origin">
  <h2>Origin IP Discovery <span class="count">({len(origin_list)} candidates)</span></h2>
  <table><tr><th>IP</th><th>Source</th><th>Provider</th></tr>{oi}</table>
  {origin_rec}
</div>''')

    # High Value Targets (includes Admin Panels)
    hvt_items = []
    if staging_envs:
        hvt_items.append(('Staging / Dev', staging_envs, 'var(--yellow)'))
    # Auth subdomains + path-level auth endpoints (e.g. x.com/i/flow/login)
    auth_subs = [s for s in sub_list if any(k in s.lower() for k in
                 ('auth', 'sso', 'login', 'id', 'account', 'oauth', 'identity', 'iam', 'saml'))]
    auth_ep_data = rd.get('auth_endpoints', {})
    auth_paths_found = []
    if isinstance(auth_ep_data, dict):
        for ep in auth_ep_data.get('endpoints', [])[:8]:
            path = ep.get('url', ep.get('path', '')) if isinstance(ep, dict) else str(ep)
            if path:
                full = path if path.startswith('http') else f'https://{host}{path}'
                if full not in auth_paths_found:
                    auth_paths_found.append(full)
    # Known platform-specific login paths
    _PLATFORM_AUTH_PATHS = {
        'x.com': '/i/flow/login', 'twitter.com': '/i/flow/login',
        'instagram.com': '/accounts/login/', 'facebook.com': '/login/',
        'github.com': '/login', 'gitlab.com': '/users/sign_in',
        'linkedin.com': '/login', 'netflix.com': '/login',
        'tiktok.com': '/login', 'reddit.com': '/login',
    }
    for domain_key, login_path in _PLATFORM_AUTH_PATHS.items():
        if domain_key in host.lower():
            full = f'https://{host}{login_path}'
            if full not in auth_paths_found:
                auth_paths_found.insert(0, full)
    auth_targets = [f'https://{s}' if not s.startswith('http') else s
                    for s in auth_subs[:6]] + auth_paths_found[:4]
    if auth_targets:
        hvt_items.append(('Auth / Identity', auth_targets[:10], 'var(--red)'))
    api_subs = [s for s in sub_list if any(k in s.lower() for k in ('api', 'graphql', 'grpc', 'gateway'))]
    if api_subs:
       hvt_items.append(('API', api_subs[:10], 'var(--orange)'))
    pay_subs = [s for s in sub_list if any(k in s.lower() for k in ('pay', 'shop', 'store', 'cart', 'order', 'checkout'))]
    if pay_subs:
       hvt_items.append(('Payment / E-Commerce', pay_subs[:10], 'var(--red)'))
    _HVT_AI_STRICT = {"llm", "gpt", "openai", "chatgpt", "copilot", "genai", "gen-ai", "langchain", "ollama", "agenticai", "agentic"}
    _HVT_AI_SEG = {"ai", "chat", "bot", "robot", "chatbot", "aibot", "assistant"}
    def _hvt_is_ai(s):
        sl = s.lower()
        segs = _re_mod.split(r'[.\-_]', sl)
        for seg in segs:
            if seg in _HVT_AI_SEG:
                return True
            if len(seg) > 3 and seg.endswith("ai"):
                return True
        return any(kw in sl for kw in _HVT_AI_STRICT)
    ai_subs = [s for s in sub_list if _hvt_is_ai(s)]
    if ai_subs:
        hvt_items.append(('AI / LLM', ai_subs[:10], '#a855f7'))
    # Add Admin Panels as HVT category
    # Helper: build full URL from path + host, or return dict's 'url' field
    def _full_url(path_or_url_or_dict, base_host: str = host) -> str:
        """Accept path string, full URL string, or endpoint dict."""
        if isinstance(path_or_url_or_dict, dict):
            # Prefer explicit 'url' field; fall back to building from 'path'
            if path_or_url_or_dict.get('url'):
                return path_or_url_or_dict['url']
            path_or_url_or_dict = path_or_url_or_dict.get('path', '')
        val = str(path_or_url_or_dict) if path_or_url_or_dict else ''
        if not val:
            return ''
        if val.startswith('http'):
            return val
        return f'https://{base_host}{val if val.startswith("/") else "/" + val}'

    if admin_panels:
        admin_paths = [_full_url(a.get('path', '')) for a in admin_panels if isinstance(a, dict)]
        hvt_items.append(('Admin Panels', admin_paths, 'var(--red)'))
    if hvt_items:
        total_hvt = sum(len(items) for _, items, _ in hvt_items)
        hvt_html = ''
        for label, items, color in hvt_items:
            if label == 'Admin Panels' and admin_panels:
                def _ap_row(a):
                    url = _full_url(a.get('path', ''))
                    cat = _esc(a.get('category', ''))
                    protected = a.get('protected')
                    prot_html = ('<span style="color:var(--red)">⚠ exposed</span>'
                                 if protected is False
                                 else '<span style="color:var(--green)">✓ protected</span>'
                                 if protected else '')
                    return (f'<tr>'
                            f'<td class="mono" style="font-size:0.85em;">'
                            f'<a href="{_esc(url)}" target="_blank" '
                            f'style="color:var(--accent2);text-decoration:none;">{_esc(url)}</a>'
                            f'</td><td class="muted">{cat}</td>'
                            f'<td class="muted" style="font-size:0.8em;">{prot_html}</td>'
                            f'</tr>')
                ap_rows = ''.join(_ap_row(a) for a in admin_panels[:30])
                ap_overflow = f'<span class="muted"> + {len(admin_panels) - 30} more</span>' if len(admin_panels) > 30 else ''
                hvt_html += f'''<div style="background:var(--surface2);border-radius:10px;padding:16px 20px;margin-bottom:12px;border-left:3px solid {color};"><div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;"><span class="type-badge" style="background:{color}20;color:{color};font-size:0.92em;">{_esc(label)}</span><span class="muted" style="font-size:0.85em;">{n_admin} panel(s) found</span></div><details><summary style="cursor:pointer;font-size:0.85em;color:var(--accent);">Show admin panel paths</summary><table style="margin-top:8px;"><tr><th>Path</th><th>Category</th></tr>{ap_rows}</table>{ap_overflow}</details></div>'''
            else:
                chips = ''.join(f'<code style="background:var(--surface);padding:5px 12px;border-radius:5px;font-size:0.9em;border:1px solid var(--border);">{_esc(s)}</code>' for s in items[:8])
                overflow = f'<span class="muted"> + {len(items) - 8} more</span>' if len(items) > 8 else ''
                hvt_html += f'''<div style="background:var(--surface2);border-radius:10px;padding:16px 20px;margin-bottom:12px;border-left:3px solid {color};"><div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;"><span class="type-badge" style="background:{color}20;color:{color};font-size:0.92em;">{_esc(label)}</span><span class="muted" style="font-size:0.85em;">{len(items)} environment(s)</span></div><div style="display:flex;flex-wrap:wrap;gap:6px;">{chips}{overflow}</div></div>'''

        # Per-category recommendations
        _HVT_RECOMMENDATIONS = {
            'Staging / Dev': ('Staging and development environments often have weaker security controls, debug modes enabled, and default credentials. They frequently expose internal APIs, database connections, and configuration details that mirror production.',
                ['Restrict access via IP allowlist or VPN — staging should never be publicly accessible',
                 'Disable debug mode, verbose error pages, and stack traces',
                 'Use separate credentials from production and rotate regularly',
                 'Remove or password-protect directory listings and development tools',
                 'Ensure staging data does not contain real customer PII']),
            'Auth / Identity': ('Authentication and identity endpoints are primary targets for credential stuffing, account takeover, and session hijacking. A single flaw here can compromise the entire user base.',
                ['Enforce rate limiting on login, registration, and password reset endpoints',
                 'Implement multi-factor authentication (MFA) for all user accounts',
                 'Use secure session management — HttpOnly, Secure, SameSite cookie flags',
                 'Deploy CAPTCHA or bot detection on authentication flows',
                 'Monitor for credential stuffing attacks and implement account lockout policies']),
            'API': ('API endpoints often lack the same security controls as web UIs. Missing authentication, excessive data exposure, and injection vulnerabilities are common attack vectors.',
                ['Enforce authentication and authorization on all API endpoints',
                 'Implement rate limiting and request throttling per API key/user',
                 'Validate and sanitize all input parameters — prevent injection attacks',
                 'Use API gateway with WAF rules to filter malicious requests',
                 'Disable unnecessary HTTP methods (PUT, DELETE, PATCH) where not required',
                 'Implement proper CORS policies — avoid wildcard (*) origins']),
            'Payment / E-Commerce': ('Payment and e-commerce endpoints process sensitive financial data. PCI DSS compliance is mandatory. A breach here has direct financial and regulatory consequences.',
                ['Ensure PCI DSS compliance for all payment processing flows',
                 'Use tokenization — never store raw credit card numbers',
                 'Enforce TLS 1.2+ on all payment endpoints',
                 'Implement Content Security Policy (CSP) to prevent Magecart-style skimming attacks',
                 'Monitor for unauthorized script injections on checkout pages',
                 'Use 3D Secure (3DS) for payment verification']),
            'AI / LLM': ('AI and LLM endpoints are vulnerable to prompt injection, data extraction, and model abuse. These are emerging attack surfaces that often lack mature security controls.',
                ['Implement input validation and prompt sanitization',
                 'Set strict output filtering to prevent data leakage',
                 'Rate limit API calls to prevent model abuse and cost escalation',
                 'Log and monitor all interactions for anomalous patterns',
                 'Ensure the model cannot access internal systems or sensitive data']),
            'Admin Panels': ('Administrative interfaces provide privileged access to application configuration, user management, and data. Exposure of admin panels is a critical finding.',
                ['Restrict admin panel access to internal networks or VPN only',
                 'Enforce strong authentication — MFA required for all admin accounts',
                 'Implement IP allowlisting for admin endpoints',
                 'Remove default admin paths (/admin, /wp-admin, /administrator) or rename them',
                 'Enable audit logging for all administrative actions',
                 'Use separate admin domains (e.g., admin.internal.company.com) not publicly resolvable']),
        }
        rec_html = ''
        active_cats = [label for label, _, _ in hvt_items]
        for cat in active_cats:
            if cat in _HVT_RECOMMENDATIONS:
                desc, recs = _HVT_RECOMMENDATIONS[cat]
                cat_color = next((c for l, _, c in hvt_items if l == cat), 'var(--muted)')
                rec_items = ''.join(f'<li>{_esc(r)}</li>' for r in recs)
                rec_html += f'''<div style="margin-bottom:14px;">
  <div style="font-weight:600;font-size:0.9em;color:{cat_color};margin-bottom:4px;">{_esc(cat)}</div>
  <p style="font-size:0.84em;color:var(--muted);margin-bottom:6px;">{_esc(desc)}</p>
  <ul style="padding-left:18px;font-size:0.84em;line-height:1.8;">{rec_items}</ul>
</div>'''

        parts.append(f'''
<div class="sec" id="hvt">
  <h2>High Value Targets <span class="count">({total_hvt})</span></h2>
  <div style="background:var(--surface2);border-radius:10px;padding:14px 18px;margin-bottom:16px;border-left:3px solid var(--accent);">
    <p style="font-size:0.88em;line-height:1.6;margin:0;">High Value Targets are subdomains, endpoints, and services that represent elevated risk due to their function (authentication, payment, admin), exposure level (staging, dev), or data sensitivity. Compromise of these targets can lead to data breaches, unauthorized access, financial loss, or regulatory violations. Each category below requires specific hardening measures.</p>
  </div>
  {hvt_html}
  <details style="margin-top:16px;"><summary style="cursor:pointer;font-weight:600;font-size:0.92em;color:var(--accent);">Security Recommendations by Category</summary>
  <div style="margin-top:12px;background:var(--surface2);border-radius:10px;padding:18px 22px;">
    {rec_html}
  </div>
  </details>
</div>''')

    # Suggested Tests — each with Fray-specific commands
    def _test_meta(typ, t0):
        """Return (sev_label, sev_color, description, fray_commands) for a test type."""
        t0e = _esc(t0)
        m = {
            'WAF Bypass': ('critical', 'var(--red)',
                'These subdomains resolve to origin IPs outside the WAF — payloads reach the server unfiltered. '
                'Use <strong>fray agent</strong> to run iterative bypass testing directly against origin, or '
                '<strong>fray test</strong> with XSS/SQLi categories.',
                [f'fray agent {t0e} -c xss --rounds 5',
                 f'fray test {t0e} -c sqli --smart',
                 f'fray bypass {t0e} -c modern_bypasses']),
            'Unprotected Subdomain': ('high', 'var(--orange)',
                'No WAF or CDN protection — all payloads reach these subdomains directly. '
                'Use <strong>fray test</strong> to probe for XSS, SSRF, and open redirect vulnerabilities.',
                [f'fray test {t0e} -c xss --smart',
                 f'fray recon {t0e} --deep',
                 f'fray test {t0e} -c ssrf --smart']),
            'Account Takeover': ('critical', 'var(--red)',
                'Login and authentication endpoints are exposed. Use <strong>fray test</strong> to check for '
                'injection in auth forms, and <strong>fray recon</strong> with auth credentials to map the '
                'authenticated attack surface.',
                [f'fray test {t0e} -c xss --smart',
                 f'fray recon {t0e} --deep --login-flow "{t0e}/login,user=test,pass=test"',
                 f'fray leak {t0e}']),
            'API Vulnerability': ('high', 'var(--orange)',
                'API endpoints discovered. Use <strong>fray recon --profile api</strong> for API-focused '
                'reconnaissance, then <strong>fray test</strong> with API-specific payloads for BOLA, SSRF, and injection.',
                [f'fray recon {t0e} --profile api',
                 f'fray test {t0e} -c api_security --smart',
                 f'fray test {t0e} -c ssrf --smart']),
            'LLM / AI Prompt Injection': ('high', 'var(--orange)',
                'AI/chatbot endpoints found. Use <strong>fray agent</strong> with prompt injection payloads '
                'to test for jailbreaking, system prompt leakage, and indirect injection.',
                [f'fray agent {t0e} -c xss --rounds 3 --ai',
                 f'fray test {t0e} -c modern_bypasses --smart']),
            'Payment / Financial Abuse': ('critical', 'var(--red)',
                'Payment and commerce endpoints detected. Use <strong>fray recon --deep</strong> to map the '
                'full payment flow, then <strong>fray test</strong> for injection in transaction parameters.',
                [f'fray recon {t0e} --deep',
                 f'fray test {t0e} -c xss --smart',
                 f'fray leak {t0e}']),
            'Staging / Dev Environment': ('high', 'var(--orange)',
                'Staging/dev environments are publicly accessible and often have weaker security. '
                'Use <strong>fray recon --profile bounty</strong> for maximum coverage, then '
                '<strong>fray agent</strong> to find bypasses on weaker WAF rules.',
                [f'fray recon {t0e} --profile bounty',
                 f'fray agent {t0e} -c xss --rounds 5',
                 f'fray test {t0e} -c ssti --smart']),
            'DDoS / L7 Denial of Service': ('medium', 'var(--yellow)',
                'No rate limiting detected. Use <strong>fray recon</strong> to verify rate limit thresholds '
                'and <strong>fray harden</strong> to generate WAF rules that enforce limits.',
                [f'fray recon {t0e} -v',
                 f'fray harden {t0e}']),
            'Web Cache Poisoning': ('medium', 'var(--yellow)',
                'CDN caching + authenticated pages = cache deception risk. Use <strong>fray smuggle</strong> '
                'to test HTTP request smuggling, and <strong>fray test</strong> with cache-specific payloads.',
                [f'fray smuggle {t0e}',
                 f'fray test {t0e} -c csp_bypass --smart']),
            'DDoS \u2014 Direct Origin': ('high', 'var(--orange)',
                'Origin servers reachable without CDN protection. Use <strong>fray recon</strong> to confirm '
                'origin IP exposure, and <strong>fray harden</strong> to generate firewall rules.',
                [f'fray recon {t0e} --deep',
                 f'fray harden {t0e}']),
        }
        return m.get(typ, ('medium', 'var(--muted)', '', []))

    tests_by_type = {}
    for t in attack_targets:
        typ = t.get('type', 'Other')
        tests_by_type.setdefault(typ, []).append(t.get('target', ''))
    if tests_by_type:
        st_html = ''
        for typ, targets in tests_by_type.items():
            first_target = targets[0] if targets else target
            meta = _test_meta(typ, first_target)
            sev_label, sev_color, test_desc = meta[0], meta[1], meta[2]
            fray_cmds = meta[3] if len(meta) > 3 else []
            chips = ''.join(f'<code style="background:var(--surface);padding:5px 12px;border-radius:5px;font-size:0.9em;border:1px solid var(--border);">{_esc(t)}</code>' for t in targets[:10])
            overflow = f'<span class="muted"> + {len(targets) - 10} more</span>' if len(targets) > 10 else ''
            desc_html = f'<p style="font-size:0.85em;margin:6px 0 10px;color:var(--text);">{test_desc}</p>' if test_desc else ''
            cmds_html = ''
            if fray_cmds:
                cmd_items = ''.join(f'<code style="background:var(--surface);padding:4px 10px;border-radius:5px;font-size:0.84em;display:inline-block;margin:2px 4px 2px 0;border:1px solid var(--border);">{c}</code>' for c in fray_cmds)
                cmds_html = f'<div style="margin-top:8px;"><span class="muted" style="font-size:0.8em;">Fray commands:</span><br><div style="margin-top:4px;">{cmd_items}</div></div>'
            st_html += f'''<div style="background:var(--surface2);border-radius:10px;padding:16px 20px;margin-bottom:12px;border-left:3px solid {sev_color};"><div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;"><span class="sev-badge" style="background:{sev_color}20;color:{sev_color};">{sev_label.upper()}</span><span style="font-weight:700;font-size:0.95em;">{_esc(typ)}</span><span class="muted" style="font-size:0.85em;">{len(targets)} target(s)</span></div>{desc_html}<div style="display:flex;flex-wrap:wrap;gap:6px;">{chips}{overflow}</div>{cmds_html}</div>'''
        parts.append(f'''
<div class="sec" id="tests">
  <h2>Suggested Tests <span class="count">({len(tests_by_type)} types, {n_attack_targets} targets)</span></h2>
  {st_html}
</div>''')

    # ── Build probe-based justification per category ─────────────────────
    def _cat_justification(cat: str) -> str:
        """Return short evidence string explaining WHY this category is recommended."""
        fp = rd.get('fingerprint', {}) or {}
        techs = fp.get('technologies', {}) or {}
        headers_raw = fp.get('headers', rd.get('headers', {})) or {}
        waf_v = atk.get('waf_vendor', '') if isinstance(atk, dict) else ''
        cdn_v = atk.get('cdn', '') if isinstance(atk, dict) else ''

        def _has_tech(*keywords):
            tech_str = ' '.join(str(k).lower() for k in techs.keys())
            return any(kw.lower() in tech_str for kw in keywords)

        def _hdr(name):
            if isinstance(headers_raw, dict):
                return str(headers_raw.get(name.lower(), headers_raw.get(name, '')))
            return ''

        # Unprotected subs count
        n_unprotected = sum(1 for s in per_sub
                            if isinstance(s, dict) and not s.get('waf') and not s.get('cdn'))

        if cat == 'csp_bypass':
            csp_hdr = _hdr('content-security-policy')
            if not csp_hdr:
                return 'No CSP header → XSS has no browser mitigation'
            if "'unsafe-inline'" in csp_hdr:
                return "CSP contains 'unsafe-inline' → inline scripts execute"
            if any(d in csp_hdr for d in ['ajax.googleapis.com', 'unpkg.com', 'cdn.jsdelivr.net', 'cdnjs']):
                return 'CSP allowlists JSONP-exploitable CDN origins'
            return 'CSP present but weak directives detected'

        if cat == 'xss':
            if not waf_v:
                return 'No WAF → reflected input reaches browser unfiltered'
            if n_unprotected:
                return f'{n_unprotected} subdomain(s) have no WAF — XSS payloads reach origin'
            if _has_tech('react', 'vue', 'angular', 'svelte', 'ember'):
                return 'Client-side SPA detected — DOM XSS vectors likely via routing'
            return f'{waf_v[:20]} WAF detected but response patterns suggest reflection points'

        if cat == 'sqli':
            if _has_tech('mysql', 'postgresql', 'mariadb', 'oracle', 'mssql', 'mongodb', 'sqlite'):
                return 'Database technology fingerprinted — SQL/NoSQL injection surface confirmed'
            api_data = rd.get('api_security', rd.get('api_endpoints', {})) or {}
            if isinstance(api_data, dict) and api_data.get('endpoints'):
                return f'{len(api_data["endpoints"])} API endpoint(s) found — query param injection surface'
            if not waf_v:
                return 'No WAF → SQL errors may leak in 500 responses'
            return 'Query parameters discovered via crawl/Wayback — injection surface mapped'

        if cat == 'ssrf':
            if _has_tech('aws', 'azure', 'gcp', 'lambda', 'ec2', 's3', 'cloudfunction'):
                return 'Cloud infra detected — SSRF may reach metadata endpoint 169.254.169.254'
            api_data = rd.get('api_security', {}) or {}
            if isinstance(api_data, dict) and api_data.get('endpoints'):
                return 'API endpoints discovered — URL/path parameters may trigger server-side requests'
            return 'External URL fetch patterns found in JS analysis'

        if cat == 'ssti':
            if _has_tech('jinja2', 'django', 'flask', 'mako', 'twig', 'smarty', 'freemarker', 'thymeleaf', 'pebble'):
                return 'Template engine fingerprinted — direct SSTI vector confirmed'
            if _has_tech('python', 'ruby', 'php', 'java', 'node'):
                return 'Server-side language detected — template injection possible in user-controlled input'
            return 'Server-side rendering patterns detected'

        if cat == 'prototype_pollution':
            if _has_tech('express', 'nodejs', 'next.js', 'nuxt', 'gatsby', 'sveltekit'):
                return 'Node.js detected — prototype pollution may reach server-side merge/deep-copy functions'
            if _has_tech('lodash', 'jquery', 'angular', 'vue'):
                return 'JS library with known prototype pollution CVEs detected'
            return 'JavaScript SPA — client-side __proto__ merge candidates likely present'

        if cat == 'api_security':
            api_data = rd.get('api_security', {}) or {}
            if isinstance(api_data, dict):
                specs = api_data.get('specs', []) or []
                if specs:
                    return f'API spec exposed ({_esc(str(specs[0])[:40])}) — BOLA/auth bypass surface mapped'
                eps = api_data.get('endpoints', []) or []
                if eps:
                    return f'{len(eps)} API endpoint(s) discovered — probe BOLA, mass assign, auth bypass'
            return 'REST/GraphQL patterns found — OWASP API Top-10 test recommended'

        if cat == 'xxe':
            if _has_tech('soap', 'wsdl', 'xml', 'jaxb', 'libxml', 'expat'):
                return 'XML processing library detected — XXE directly applicable'
            return 'Content-type analysis suggests XML-accepting endpoints'

        if cat == 'path_traversal':
            if _has_tech('apache', 'nginx', 'iis', 'lighttpd'):
                return 'Web server fingerprinted — check for misconfigured directory traversal aliases'
            return 'File-serving paths (/files/, /download/, /static/) found in crawl'

        if cat in ('cache_poison', 'web_cache_poisoning'):
            if cdn_v:
                return f'CDN ({str(cdn_v)[:20]}) detected — X-Forwarded-Host may poison shared cache'
            if _hdr('cache-control') or _hdr('x-cache') or _hdr('cf-cache-status'):
                return 'Caching headers present — unkeyed header injection may poison responses'
            return 'CDN/cache layer inferred from response timing'

        if cat in ('massassign', 'mass_assignment'):
            api_data = rd.get('api_security', {}) or {}
            if isinstance(api_data, dict) and api_data.get('endpoints'):
                return 'REST endpoints accept JSON body — unfiltered fields may allow privilege escalation'
            return 'User profile/settings endpoints found — mass assignment test recommended'

        if cat == 'modern_bypasses':
            if waf_v:
                return f'{waf_v[:20]} detected — Unicode/null-byte/chunked evasion may bypass signatures'
            return 'WAF or filtering layer present — encoding bypass opportunities likely'

        if cat == 'ai_prompt_injection':
            return 'AI/LLM endpoint discovered — prompt injection and jailbreak vectors active'

        return ''

    # Recommended Categories
    _CAT_DESC = {
        'csp_bypass': 'Bypass Content-Security-Policy restrictions via JSONP, base-tag, and trusted-type abuse',
        'modern_bypasses': 'Latest WAF evasion techniques — encoding tricks, DOM clobbering, prototype pollution payloads',
        'prototype_pollution': 'Pollute JavaScript Object.prototype to hijack application logic and achieve XSS',
        'ssrf': 'Server-Side Request Forgery — access internal services, cloud metadata, and private networks',
        'ssti': 'Server-Side Template Injection — execute arbitrary code via Jinja2, Twig, Freemarker templates',
        'api_security': 'OWASP API Top-10 payloads — BOLA, broken auth, mass assignment, injection',
        'xss': 'Cross-Site Scripting — reflected, stored, and DOM-based injection vectors',
        'sqli': 'SQL Injection — union, blind, time-based, and out-of-band techniques',
        'xxe': 'XML External Entity — file read, SSRF, and denial of service via DTD abuse',
        'lfi': 'Local File Inclusion — path traversal, null-byte injection, wrapper abuse',
    }
    if rec_cats:
        # Build a mapping: category → best target URL to use in the command.
        # Priority: unprotected subdomain matching the category > critical path > main target
        _cat_best_target = {}
        _unprotected_subs = [
            s.get('subdomain', s.get('host', ''))
            for s in per_sub if isinstance(s, dict) and not s.get('waf') and not s.get('cdn')
        ]
        _crit_paths_data = atk.get('critical_paths', []) if isinstance(atk, dict) else []
        _critical_urls = [cp.get('url', '') for cp in _crit_paths_data if isinstance(cp, dict)]
        # Category → keywords that indicate a subdomain is a good match
        _cat_keywords = {
            'xss':              ['www', 'portal', 'app', 'web', 'login', 'account'],
            'sqli':             ['api', 'search', 'query', 'data', 'db', 'admin', 'backend'],
            'ssrf':             ['api', 'internal', 'backend', 'service', 'proxy', 'fetch'],
            'ssti':             ['app', 'template', 'render', 'portal', 'web', 'cms'],
            'api_security':     ['api', 'v1', 'v2', 'graphql', 'rest', 'gw', 'gateway'],
            'xxe':              ['api', 'xml', 'soap', 'ws', 'upload'],
            'csp_bypass':       ['www', 'portal', 'app', 'web'],
            'path_traversal':   ['files', 'upload', 'static', 'cdn', 'media', 'api', 'docs'],
            'prototype_pollution': ['app', 'portal', 'api', 'web', 'front'],
            'modern_bypasses':  ['www', 'app', 'portal', 'web'],
            'cache_poison':     ['www', 'cdn', 'static', 'assets', 'cache'],
            'massassign':       ['api', 'account', 'profile', 'admin', 'user'],
            'ai_prompt_injection': ['chat', 'ai', 'gpt', 'llm', 'assistant', 'bot', 'copilot'],
            'lfi':              ['files', 'upload', 'download', 'static', 'docs', 'api'],
        }
        for c in rec_cats[:10]:
            kws = _cat_keywords.get(c, [])
            # Try unprotected subdomain first (no WAF = better for testing)
            best = ''
            for sub in _unprotected_subs:
                if any(kw in sub.lower() for kw in kws):
                    best = f'https://{sub}'
                    break
            # Fall back to critical path matching the category
            if not best:
                for cp_url in _critical_urls:
                    if any(kw in cp_url.lower() for kw in kws):
                        best = cp_url
                        break
            # Fall back to main target
            _cat_best_target[c] = best or target

        cl = ''
        for c in rec_cats[:10]:
            desc = _CAT_DESC.get(c, '')
            best_t = _cat_best_target.get(c, target)
            # Probe-based justification takes precedence over generic description
            justification = _cat_justification(c)
            display_reason = justification or desc
            why_html = ''
            if justification:
                # Show probe-based justification in green/accent (evidence-based)
                why_html = (f'<span style="font-size:0.8em;background:rgba(34,197,94,0.12);'
                            f'color:var(--green);padding:1px 7px;border-radius:4px;margin-left:6px;">'
                            f'Evidence: {_esc(justification)}</span>')
            elif desc:
                why_html = f'<span class="muted" style="font-size:0.85em;"> — {_esc(desc)}</span>'

            cmd = f'fray test {_esc(best_t)} -c {_esc(c)} --smart'
            # Highlight when the target differs from the main domain
            target_note = ''
            if best_t != target:
                target_note = (f'<span style="font-size:0.78em;background:rgba(99,102,241,0.15);'
                               f'color:var(--accent);padding:1px 6px;border-radius:4px;margin-left:6px;">'
                               f'Best target: {_esc(best_t.replace("https://",""))}</span>')
            cl += (f'<li style="margin:10px 0;"><strong>{_esc(c)}</strong>'
                   f'{target_note}{why_html}'
                   f'<br><code style="background:var(--surface2);padding:4px 10px;border-radius:5px;'
                   f'font-size:0.85em;margin-top:4px;display:inline-block;">{cmd}</code></li>')
        parts.append(f'''
<div class="sec" id="cats">
  <h2>Recommended Payload Categories</h2>
  <p class="muted" style="font-size:0.85em;margin-bottom:12px;">Commands target the highest-value URL for each category — unprotected subdomains where available (no WAF = payloads reach origin directly).</p>
  <ol style="padding-left:20px;line-height:1.8;">{cl}</ol>
</div>''')

    # Remediation Plan — auto-enrich from recon data
    _auto_remediation = list(remediation) if remediation else []
    _existing_actions = {r.get('action', '').lower() for r in _auto_remediation if isinstance(r, dict)}
    _sev_timeline = {
        'critical': 'Immediate',
        'high': 'Short-term',
        'medium': 'Medium-term',
        'low': 'Long-term',
    }

    # Promote finding-level remediation hints (from pipeline) into the plan
    atk_findings = atk.get('findings', []) if isinstance(atk, dict) else []
    if isinstance(atk_findings, list):
        for _f in atk_findings:
            if not isinstance(_f, dict):
                continue
            _rem = _f.get('remediation')
            if not _rem:
                continue
            _action = _f.get('finding') or _f.get('title') or 'Address finding'
            _action_key = (_action or '').lower()
            if _action_key in _existing_actions:
                continue
            _severity = (_f.get('severity') or 'medium').lower()
            _timeline = _sev_timeline.get(_severity, 'Medium-term')
            _auto_remediation.append({
                'action': _action,
                'severity': _severity,
                'why': _f.get('risk') or _f.get('finding', ''),
                'how': _rem,
                'timeline': _timeline,
            })
            _existing_actions.add(_action_key)

    # Auto-generate remediation items from recon findings
    # 1. Unprotected subdomains (no WAF/CDN)
    _sub_waf = rd.get('subdomain_security', {}) or {}
    _sub_total = _sub_waf.get('total_subdomains', 0)
    _sub_techs = _sub_waf.get('tech_fingerprints', [])
    _n_no_waf = 0
    if isinstance(_sub_techs, list):
        for _st in _sub_techs:
            if isinstance(_st, (list, tuple)) and len(_st) >= 2:
                _fp = _st[1] if isinstance(_st[1], dict) else {}
                _waf_name = _fp.get('waf', _fp.get('cdn', ''))
                if not _waf_name:
                    _n_no_waf += 1
    if _n_no_waf > 5 and 'waf coverage' not in ' '.join(_existing_actions):
        _auto_remediation.append({
            'action': f'Add WAF coverage for {_n_no_waf} unprotected subdomain(s)',
            'severity': 'high',
            'why': f'{_n_no_waf} of {_sub_total} subdomain(s) have no WAF/CDN protection — exposed to direct attacks',
            'how': 'Extend WAF rules to cover all subdomains, or route through CDN (Cloudflare, Akamai, AWS WAF)',
            'timeline': 'Short-term',
        })

    # 2. CORS misconfiguration
    _cors = rd.get('cors', {}) or {}
    _cors_issues = _cors.get('issues', [])
    if _cors_issues and 'cors' not in ' '.join(_existing_actions):
        _n_cors = len(_cors_issues)
        _worst = max(_cors_issues, key=lambda x: {'critical':4,'high':3,'medium':2,'low':1}.get(x.get('severity','low'), 0))
        _auto_remediation.append({
            'action': f'Fix {_n_cors} CORS misconfiguration(s)',
            'severity': _worst.get('severity', 'medium'),
            'why': _worst.get('risk', 'Cross-origin data theft possible'),
            'how': 'Validate Origin header server-side; never reflect arbitrary origins; avoid Access-Control-Allow-Credentials with wildcards',
            'timeline': 'Immediate' if _worst.get('severity') == 'critical' else 'Short-term',
        })

    # 3. Weak security header values
    _hdrs = rd.get('headers', {}) or {}
    _hdr_issues = _hdrs.get('value_issues', [])
    if _hdr_issues and 'header value' not in ' '.join(_existing_actions):
        _weak_names = [h.get('header', '') for h in _hdr_issues[:4]]
        _auto_remediation.append({
            'action': f'Fix {len(_hdr_issues)} weak security header value(s)',
            'severity': 'high',
            'why': f'Headers present but misconfigured: {", ".join(_weak_names)}',
            'how': 'Review and strengthen header values — e.g., remove unsafe-inline from CSP, increase HSTS max-age to 1 year',
            'timeline': 'Short-term',
        })

    # 4. Exposed files found
    _exposed = rd.get('exposed_files', {}) or {}
    _exposed_list = _exposed.get('exposed', [])
    _crit_exposed = [e for e in _exposed_list if isinstance(e, dict) and e.get('severity') == 'critical']
    if _crit_exposed and 'exposed file' not in ' '.join(_existing_actions):
        _paths = ', '.join(e.get('path', '') for e in _crit_exposed[:3])
        _auto_remediation.append({
            'action': f'Remove {len(_crit_exposed)} critically exposed file(s)',
            'severity': 'critical',
            'why': f'Sensitive files publicly accessible: {_paths}',
            'how': 'Block access via web server config (deny rules), remove from webroot, or add authentication',
            'timeline': 'Immediate',
        })

    # 5. Subdomain takeover vulnerabilities
    _takeover = rd.get('subdomain_takeover', {}) or {}
    _takeover_vulns = _takeover.get('vulnerable', [])
    if _takeover_vulns and 'takeover' not in ' '.join(_existing_actions):
        _auto_remediation.append({
            'action': f'Fix {len(_takeover_vulns)} subdomain takeover vulnerability(ies)',
            'severity': 'critical',
            'why': 'Dangling DNS records point to unclaimed services — attacker can claim and serve malicious content',
            'how': 'Remove stale CNAME records or reclaim the service (S3 bucket, Heroku app, Azure, etc.)',
            'timeline': 'Immediate',
        })

    # 6. WAF in monitor mode
    _diff = rd.get('differential', {}) or {}
    _waf_mode = _diff.get('waf_mode', '')
    if _waf_mode == 'monitoring' and 'monitor' not in ' '.join(_existing_actions):
        _auto_remediation.append({
            'action': 'Switch WAF from monitor mode to blocking mode',
            'severity': 'critical',
            'why': 'WAF is logging attacks but not blocking them — all payloads pass through',
            'how': 'Change WAF policy from monitor/detect to block/prevent mode in WAF management console',
            'timeline': 'Immediate',
        })

    # 7. Missing DNSSEC
    _dns = rd.get('dns', {}) or {}
    _dnssec = rd.get('dnssec', {}) or {}
    if isinstance(_dnssec, dict) and not _dnssec.get('signed', False) and 'dnssec' not in ' '.join(_existing_actions):
        _auto_remediation.append({
            'action': 'Enable DNSSEC',
            'severity': 'medium',
            'why': 'DNS responses are not signed — vulnerable to DNS spoofing/cache poisoning',
            'how': 'Enable DNSSEC signing at your DNS provider (Cloudflare, Route53, etc.)',
            'timeline': 'Medium-term',
        })

    # 8. Secrets/API keys in responses
    _secrets = rd.get('secrets', {}) or {}
    _secret_findings = _secrets.get('findings', []) if isinstance(_secrets, dict) else []
    if _secret_findings and 'secret' not in ' '.join(_existing_actions) and 'api key' not in ' '.join(_existing_actions):
        _auto_remediation.append({
            'action': f'Rotate and remove {len(_secret_findings)} exposed secret(s)/API key(s)',
            'severity': 'critical',
            'why': 'API keys or credentials found in HTTP responses — immediate compromise risk',
            'how': 'Rotate all exposed keys, move to environment variables or secrets manager, add to .gitignore',
            'timeline': 'Immediate',
        })

    # 9. VPN endpoint CVEs
    if vpn_cve_findings and 'vpn' not in ' '.join(_existing_actions):
        _auto_remediation.append({
            'action': f'Patch {len(vpn_cve_findings)} VPN endpoint CVE(s)',
            'severity': 'critical',
            'why': 'Known CVEs found on VPN endpoints — pre-auth RCE or credential theft possible',
            'how': 'Apply vendor security patches immediately; if EOL, migrate to a supported VPN solution',
            'timeline': 'Immediate',
        })

    # Sort: critical first, then high, medium, low
    _sev_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3, 'info': 4}
    _auto_remediation.sort(key=lambda r: _sev_order.get(r.get('severity', 'medium') if isinstance(r, dict) else 'medium', 3))

    if _auto_remediation:
        rr = ''
        for i, r in enumerate(_auto_remediation[:15], 1):
            if isinstance(r, dict):
                ra = _esc(r.get('action', ''))
                rs = r.get('severity', 'medium')
                rsc = SEV_COLORS.get(rs, 'var(--muted)')
                rw = _esc(r.get('why', ''))
                rh = _esc(r.get('how', ''))
                rt = _esc(r.get('timeline', ''))
                rr += f'<tr><td class="num">{i}</td><td><strong>{ra}</strong></td><td><span class="sev-badge" style="background:{rsc}20;color:{rsc};">{rs.upper()}</span></td><td class="muted" style="font-size:0.85em;">{rw}</td><td style="font-size:0.85em;">{rh}</td><td style="font-size:0.85em;white-space:nowrap;">{rt}</td></tr>'
            else:
                rr += f'<tr><td class="num">{i}</td><td colspan="5">{_esc(str(r))}</td></tr>'
        parts.append(f'''
<div class="sec" id="remediation">
  <h2>Remediation Plan <span class="count">({len(_auto_remediation)} action items)</span></h2>
  <p class="muted" style="margin-bottom:14px;">Prioritised remediation actions sorted by severity and business impact.</p>
  <table><tr><th>#</th><th>Action</th><th>Severity</th><th>Why</th><th>How</th><th>Timeline</th></tr>{rr}</table>
</div>''')

    # Dashboard link
    parts.append(f'''
<div style="background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);border:1px solid #4338ca;border-radius:10px;padding:16px 24px;margin:24px auto;max-width:700px;display:flex;align-items:center;justify-content:space-between;gap:16px">
  <div>
    <div style="font-size:14px;font-weight:600;color:rgba(99,102,241,0.15)">&#9876; Fray Live Dashboard</div>
    <div style="font-size:12px;color:var(--accent2);margin-top:4px">View live data, re-scan findings, track changes over time</div>
  </div>
  <div style="font-size:12px;color:var(--accent2);font-family:monospace;background:rgba(0,0,0,.2);padding:8px 14px;border-radius:6px;white-space:nowrap">fray dashboard</div>
</div>''')

    # ── #264 WAF-Centric Report View ─────────────────────────────────────────
    # Grouped by WAF vendor → per blocked pattern → bypass technique + mechanics
    # Only shown when bypass findings exist (from fray test/fray analyze output)
    # findings = atk.get('findings') — populated from attack_surface.findings
    # Also check rd['findings'] (raw recon findings) and rd.get('test_results')
    _all_findings_sources = (
        findings                                          # attack_surface.findings
        + (rd.get("findings") or [])                     # raw rd.findings
        + (rd.get("test_results", {}).get("findings", []) if isinstance(rd.get("test_results"), dict) else [])
    )
    bypass_findings = [f for f in _all_findings_sources
                       if f.get("type") in ("waf_bypass", "bypass")
                       or (not f.get("blocked", True) and f.get("payload"))]
    analyze_data = rd.get("analyze_results", {})  # from fray analyze --json output

    waf_section_html = ""
    if bypass_findings or analyze_data:
        waf_rows = ""
        for bf in bypass_findings[:20]:
            payload   = _esc(str(bf.get("payload", bf.get("finding", ""))[:60]))
            technique = _esc(str(bf.get("technique", bf.get("bypass_type", ""))[:40]))
            status    = _esc(str(bf.get("status", bf.get("waf_response", ""))))
            category  = _esc(str(bf.get("category", bf.get("type", ""))[:20]))
            reflected = bf.get("reflected", False)
            ref_badge = ('<span style="color:var(--red);font-size:0.75em;font-weight:600;">REFLECTED</span>'
                         if reflected else "")
            waf_rows += f'''<tr>
              <td style="font-family:monospace;font-size:0.82em;word-break:break-all;">{payload}</td>
              <td style="text-align:center;font-weight:700;color:var(--orange);">{status}</td>
              <td style="font-size:0.85em;">{technique} {ref_badge}</td>
              <td style="font-size:0.82em;color:var(--muted);">{category}</td>
            </tr>'''

        # From analyze results
        if isinstance(analyze_data, dict):
            for res in analyze_data.get("results", [])[:10]:
                bp = res.get("best_bypass") or {}
                if not bp:
                    continue
                payload   = _esc(str(res.get("pattern", ""))[:60])
                technique = _esc(str(bp.get("technique", ""))[:40])
                status    = _esc(str(res.get("waf_response", "")))
                category  = _esc(str(res.get("category", ""))[:20])
                waf_rows += f'''<tr>
                  <td style="font-family:monospace;font-size:0.82em;">{payload}</td>
                  <td style="text-align:center;font-weight:700;color:var(--orange);">{status}</td>
                  <td style="font-size:0.85em;">{technique}</td>
                  <td style="font-size:0.82em;color:var(--muted);">{category}</td>
                </tr>'''

        if waf_rows:
            waf_vendor_str = _esc(str(waf_vendor) if waf_vendor and waf_vendor != "—" else "Detected WAF")
            waf_section_html = f'''
<div class="sec" id="waf-bypass">
  <h2>WAF Bypass Intelligence <span class="count">({waf_vendor_str})</span></h2>
  <p style="font-size:0.9em;color:var(--text2);margin-bottom:16px;">
    Per-pattern bypass table: which payload patterns the WAF blocks and what technique
    bypasses each rule. Run <code>fray analyze &lt;url&gt; -c xss</code> to populate this section.
  </p>
  <div style="overflow-x:auto;">
  <table style="width:100%;border-collapse:collapse;">
    <thead><tr style="background:var(--surface2);">
      <th style="padding:10px 12px;text-align:left;font-size:0.85em;">Blocked Pattern</th>
      <th style="padding:10px 12px;text-align:center;font-size:0.85em;width:80px;">WAF</th>
      <th style="padding:10px 12px;text-align:left;font-size:0.85em;">Bypass Technique</th>
      <th style="padding:10px 12px;text-align:left;font-size:0.85em;width:100px;">Category</th>
    </tr></thead>
    <tbody style="font-size:0.88em;">{waf_rows}</tbody>
  </table>
  </div>
  <p style="margin-top:12px;font-size:0.82em;color:var(--muted);">
    Generate deeper analysis: <code>fray analyze {_esc(target)} --mechanics --waf {_esc(str(waf_vendor or "auto"))}</code>
  </p>
</div>'''
            parts.append(waf_section_html)

    # Footer
    parts.append(f'''
<div class="foot">
  <div style="border-top:1px solid var(--border);padding-top:20px;margin-top:8px;">
    <p><strong><a href="https://github.com/dalisecurity/Fray">Fray</a></strong> — DALI Security Reconnaissance Engine</p>
    <p style="margin-top:4px;">Report generated: {_esc(ts_short)}</p>
    <p style="margin-top:8px;font-size:0.75em;max-width:700px;margin-left:auto;margin-right:auto;">
      <strong>CONFIDENTIAL</strong> — This report contains sensitive security information.
      Share only with authorized personnel.
    </p>
  </div>
</div>
</div></body></html>''')

    return '\n'.join(parts)
