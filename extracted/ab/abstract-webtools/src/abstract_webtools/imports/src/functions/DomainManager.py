from ..imports import SingletonMeta,urlparse as _urlparse
from ..functions import *
from ..functions.domain_utils import  get_parsed_url as _get_parsed_url
from ..imports import SingletonMeta, urlparse as _urlparse
from ..functions import *
from ..functions.domain_utils import get_parsed_url as _get_parsed_url


class DomainManager(metaclass=SingletonMeta):
    def __init__(self, domain=None):
        if not hasattr(self, "initialized"):
            self.initialized = True
            self.domains = {}
        if domain:
            self.check_domains(domain)

    # ─────────────────────────────────────────────────────────────
    # Core domain checker
    # ─────────────────────────────────────────────────────────────
    def check_domains(self, url, valid_variants=None):
        valid_variants = True if valid_variants in [True, None] else False

        parsed_url = _get_parsed_url(url)

        domain      = parsed_url.get("domain")
        ext         = parsed_url.get("ext")
        domain_name = parsed_url.get("name")
        path        = parsed_url.get("path") or ""

        http = parsed_url.get("http") or "https"
        parsed_url["http"] = http

        # 🚨 HARD INVALID-DOMAIN GUARD
        if not domain or not ext:
            parsed_url.update({
                "domain_valid": False,
                "full_domain": url,
                "variants": [],
                "valid_variants": [],
                "paths": [path] if path else [],
            })
            return parsed_url

        # ─────────────────────────────────────────────────────────
        # Cache structure
        # ─────────────────────────────────────────────────────────
        if domain_name not in self.domains:
            self.domains[domain_name] = {}

        if ext not in self.domains[domain_name]:
            self.domains[domain_name][ext] = {}

        entry = self.domains[domain_name][ext]

        # ─────────────────────────────────────────────────────────
        # Path tracking
        # ─────────────────────────────────────────────────────────
        entry.setdefault("paths", [])
        if path and path not in entry["paths"]:
            entry["paths"].append(path)

        # ─────────────────────────────────────────────────────────
        # Variants (only if domain is valid)
        # ─────────────────────────────────────────────────────────
        entry.setdefault("variants", get_url_variants(domain))

        # ─────────────────────────────────────────────────────────
        # Valid variants
        # ─────────────────────────────────────────────────────────
        if "valid_variants" not in entry:
            valid_list = []
            if valid_variants:
                valid_list = get_valid_url_variants(domain=domain) or []
                if valid_list:
                    http = get_http(valid_list[0]) or http
            entry["valid_variants"] = valid_list
            entry["http"] = http

        # ─────────────────────────────────────────────────────────
        # Domain validity
        # ─────────────────────────────────────────────────────────
        entry["domain_valid"] = bool(entry["valid_variants"])

        # ─────────────────────────────────────────────────────────
        # Full domain (ONLY if valid)
        # ─────────────────────────────────────────────────────────
        entry["full_domain"] = (
            ensure_http(domain) if entry["domain_valid"] else None
        )

        # Merge parsed metadata (without overwriting with None)
        for k, v in parsed_url.items():
            if v is not None:
                entry[k] = v

        return entry

    # ─────────────────────────────────────────────────────────────
    # Public helpers
    # ─────────────────────────────────────────────────────────────
    def get_parsed_url(self, url, valid_variants=None):
        parsed = self.check_domains(url, valid_variants=valid_variants)
        parsed["path"] = get_domain_path(url)
        return parsed

    def urlparse(self, url, valid_variants=None):
        parsed = self.check_domains(url, valid_variants=valid_variants)
        parsed["path"] = get_domain_path(url)

        if not parsed.get("full_domain"):
            # Fallback to raw parsing if domain invalid
            return _urlparse(url)

        full_url = get_full_url(parsed_url=parsed)
        return _urlparse(full_url)


# Singleton instance
domain_mgr = DomainManager()


# Backward-compatible helpers
def get_parsed_url(url):
    return domain_mgr.get_parsed_url(url)


def urlparse(url):
    return domain_mgr.urlparse(url)


parse_url = get_parsed_url

