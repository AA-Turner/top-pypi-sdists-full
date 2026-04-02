"""
Fray Scope — Parse and validate scope files for bug bounty workflows

Supports:
  - Domains: example.com, *.example.com
  - URLs: https://example.com/app
  - IPs: 192.168.1.1
  - CIDRs: 10.0.0.0/24
  - Comments: # this is a comment
  - Blank lines: ignored
"""

import ipaddress
import re
from pathlib import Path
from urllib.parse import urlparse


def parse_scope_file(filepath):
    """Parse a scope file and return structured scope data.

    Returns:
        dict with keys: domains, wildcards, ips, cidrs, urls, out_of_scope
    """
    scope = {
        "domains": set(),
        "wildcards": set(),
        "ips": set(),
        "cidrs": [],
        "urls": set(),
        "out_of_scope": set(),
    }

    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Scope file not found: {filepath}")

    section = "in"  # track in-scope vs out-of-scope sections

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        # Skip empty lines and comments
        if not line or line.startswith("#"):
            # Check for section markers
            lower = line.lower() if line else ""
            if "out of scope" in lower or "out-of-scope" in lower or "exclude" in lower:
                section = "out"
            elif "in scope" in lower or "in-scope" in lower or "include" in lower:
                section = "in"
            continue

        # Handle negation prefix (- or !)
        if line.startswith(("-", "!")) and len(line) > 1:
            entry = line[1:].strip()
            scope["out_of_scope"].add(entry.lower())
            continue

        if section == "out":
            scope["out_of_scope"].add(line.lower())
            continue

        # Parse the entry
        _classify_entry(line, scope)

    # Convert sets for JSON serialization
    return {
        "domains": sorted(scope["domains"]),
        "wildcards": sorted(scope["wildcards"]),
        "ips": sorted(scope["ips"]),
        "cidrs": [str(c) for c in scope["cidrs"]],
        "urls": sorted(scope["urls"]),
        "out_of_scope": sorted(scope["out_of_scope"]),
    }


def _classify_entry(entry, scope):
    """Classify a single scope entry into the correct bucket."""
    entry = entry.strip()

    # Wildcard domain: *.example.com
    if entry.startswith("*."):
        scope["wildcards"].add(entry[2:].lower())
        return

    # URL: starts with http:// or https://
    if entry.startswith(("http://", "https://")):
        scope["urls"].add(entry.lower())
        parsed = urlparse(entry)
        host = parsed.hostname
        if host:
            try:
                ipaddress.ip_address(host)
                scope["ips"].add(host)
            except ValueError:
                scope["domains"].add(host.lower())
        return

    # CIDR: contains /
    if "/" in entry:
        try:
            net = ipaddress.ip_network(entry, strict=False)
            scope["cidrs"].append(net)
            return
        except ValueError:
            pass

    # IP address
    try:
        ipaddress.ip_address(entry)
        scope["ips"].add(entry)
        return
    except ValueError:
        pass

    # Plain domain
    if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*$', entry):
        scope["domains"].add(entry.lower())
        return

    # Fallback: treat as domain anyway
    scope["domains"].add(entry.lower())


def is_target_in_scope(target_url, scope):
    """Check if a target URL is within the parsed scope.

    Args:
        target_url: URL string (e.g. https://example.com)
        scope: dict from parse_scope_file()

    Returns:
        (bool, str) — (in_scope, reason)
    """
    parsed = urlparse(target_url)
    host = (parsed.hostname or "").lower()

    if not host:
        return False, "Could not parse hostname from URL"

    # Check out-of-scope first
    for entry in scope.get("out_of_scope", []):
        if host == entry or host.endswith("." + entry):
            return False, f"Excluded by out-of-scope rule: {entry}"

    # Check exact domain match
    if host in scope.get("domains", []):
        return True, f"Matches domain: {host}"

    # Check wildcard match: *.example.com covers sub.example.com
    for wildcard in scope.get("wildcards", []):
        if host == wildcard or host.endswith("." + wildcard):
            return True, f"Matches wildcard: *.{wildcard}"

    # Check URL prefix match
    target_lower = target_url.lower()
    for url in scope.get("urls", []):
        if target_lower.startswith(url) or target_lower == url:
            return True, f"Matches URL: {url}"

    # Check IP match
    try:
        target_ip = ipaddress.ip_address(host)
        if str(target_ip) in scope.get("ips", []):
            return True, f"Matches IP: {target_ip}"
        for cidr_str in scope.get("cidrs", []):
            net = ipaddress.ip_network(cidr_str, strict=False)
            if target_ip in net:
                return True, f"Matches CIDR: {cidr_str}"
    except ValueError:
        pass

    return False, f"Target {host} is not in scope"


def print_scope(scope, filepath=None):
    """Pretty-print a parsed scope."""
    bold = "\033[1m"
    dim = "\033[2m"
    green = "\033[92m"
    red = "\033[91m"
    reset = "\033[0m"

    print(f"\n{bold}Fray Scope{reset}")
    if filepath:
        print(f"  {dim}File: {filepath}{reset}")
    print("━" * 50)

    total = 0

    if scope["domains"]:
        print(f"\n  {bold}Domains ({len(scope['domains'])}):{reset}")
        for d in scope["domains"]:
            print(f"    {green}✓{reset} {d}")
        total += len(scope["domains"])

    if scope["wildcards"]:
        print(f"\n  {bold}Wildcards ({len(scope['wildcards'])}):{reset}")
        for w in scope["wildcards"]:
            print(f"    {green}✓{reset} *.{w}")
        total += len(scope["wildcards"])

    if scope["ips"]:
        print(f"\n  {bold}IPs ({len(scope['ips'])}):{reset}")
        for ip in scope["ips"]:
            print(f"    {green}✓{reset} {ip}")
        total += len(scope["ips"])

    if scope["cidrs"]:
        print(f"\n  {bold}CIDRs ({len(scope['cidrs'])}):{reset}")
        for c in scope["cidrs"]:
            print(f"    {green}✓{reset} {c}")
        total += len(scope["cidrs"])

    if scope["urls"]:
        print(f"\n  {bold}URLs ({len(scope['urls'])}):{reset}")
        for u in scope["urls"]:
            print(f"    {green}✓{reset} {u}")
        total += len(scope["urls"])

    if scope["out_of_scope"]:
        print(f"\n  {bold}Out of Scope ({len(scope['out_of_scope'])}):{reset}")
        for o in scope["out_of_scope"]:
            print(f"    {red}✗{reset} {o}")

    print(f"\n{'━' * 50}")
    print(f"  {bold}{total} target(s) in scope{reset}", end="")
    if scope["out_of_scope"]:
        print(f", {bold}{len(scope['out_of_scope'])} excluded{reset}")
    else:
        print()
