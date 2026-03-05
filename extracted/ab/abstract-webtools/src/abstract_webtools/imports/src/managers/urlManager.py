from __future__ import annotations
from ..imports import *
from ..functions import *
from dataclasses import asdict as _asdict





@dataclass
class ParsedURL:
    scheme:   str  = "https"
    host:     str  = ""
    port:     int | None = None
    www:      bool = False
    name:     str  = ""
    ext:      str  = ""
    path:     str  = ""
    query:    dict = field(default_factory=dict)
    fragment: str  = ""
    bare:     bool = False

    @property
    def netloc(self) -> str:
        return f"{self.host}:{self.port}" if self.port else self.host

    @property
    def full_domain(self) -> str:
        return f"{self.scheme}://{self.netloc}"

    @property
    def full_url(self) -> str:
        path = f"/{self.path.lstrip('/')}" if self.path else ""
        qs   = f"?{urlencode(self.query)}" if self.query else ""
        frag = f"#{self.fragment}" if self.fragment else ""
        return f"{self.full_domain}{path}{qs}{frag}"

    # ── dict protocol ────────────────────────────────────────────
    def _as_dict(self) -> dict:
        d = _asdict(self)
        d["netloc"]      = self.netloc
        d["full_domain"] = self.full_domain
        d["full_url"]    = self.full_url
        d["valid_variants"] = []   # bare hosts skip variant probing
        return d

    def get(self, key, default=None):
        return self._as_dict().get(key, default)

    def __getitem__(self, key):
        return self._as_dict()[key]

    def __contains__(self, key):
        return key in self._as_dict()



def _is_bare_host(host: str) -> bool:
    """True for localhost, IPs, and hostnames that have no public TLD."""
    if not host:
        return False
    bare = host.split(":")[0]
    if bare == "localhost":
        return True
    try:
        ipaddress.ip_address(bare)
        return True
    except ValueError:
        pass
    # no dot == no TLD
    return "." not in bare


def _parse_query(raw: str) -> dict:
    if not raw:
        return {}
    result = {}
    for pair in raw.split("&"):
        if not pair:
            continue
        k, _, v = pair.partition("=")
        result[k] = v
    return result


def parse_url_clean(url: str | None) -> ParsedURL:
    """
    Parse a URL into a fully explicit ParsedURL.
    Never produces None in string fields.
    Works for: https://example.com/path, http://localhost:8384/, 192.168.1.1:5000
    """
    if not url:
        return ParsedURL()

    url = url.strip()

    # inject scheme if missing so urlparse doesn't mangle netloc into path
    if "://" not in url:
        url = f"https://{url}"

    p: ParseResult = urlparse(url)

    scheme = p.scheme or "https"
    raw_host = p.hostname or ""        # always lowercase, no port
    port = p.port                      # int or None
    path = p.path.strip("/")
    query = _parse_query(p.query)
    fragment = p.fragment or ""

    www = raw_host.startswith("www.")
    host_no_www = raw_host.removeprefix("www.")
    bare = _is_bare_host(host_no_www)

    if bare:
        name = host_no_www.split(":")[0]
        ext  = ""
    else:
        name, ext = os.path.splitext(host_no_www)
        if not ext and "." in host_no_www:
            # splitext only fires on last component — fallback
            parts = host_no_www.rsplit(".", 1)
            name, ext = parts[0], f".{parts[1]}"

    return ParsedURL(
        scheme=scheme,
        host=raw_host,
        port=port,
        www=www,
        name=name,
        ext=ext,
        path=path,
        query=query,
        fragment=fragment,
        bare=bare,
    )
class urlManager:
    """
    urlManager for managing and cleaning URLs.

    Uses shared functions from domain_utils/url_utils/specUrl_utils.
    """

    def __init__(self, url=None, session=None, valid_variants=None):
        self.valid_variants = valid_variants or False
        self.session = session or requests.Session()
        self._url = url

        self.parsed = None
        if url is None:
            self.url = None
            self.clean_urls = []
            self.protocol = None
            self.domain = None
            self.path = ""
            self.query = {}
            self.all_urls = []
        else:
            self.update_url(url)

    def update_url(self, url):
        """Update the URL and refresh related attributes."""
        self._url = url
        if self._url == None:
            self.parsed = {}
        else:
            if self.valid_variants:
                self.parsed = parse_url(self._url,valid_variants=self.valid_variants)
            else:
                self.parsed = parse_url_clean(self._url)
        if url is None:
            self.clean_urls = self.parsed.get('valid_variants')
            self.url = self.parsed.get('full_url')
            self.protocol = None
            self.domain = None
            self.path = ""
            self.query = {}
            self.all_urls = []
            return

        self.valid_variants = self.parsed.get('valid_variants')
        self.path = self.parsed.get('path')
        self.clean_urls = [f"{variant}/{self.path}" for variant in self.valid_variants if variant]
        self.url = self.parsed.get('full_url')
        self.protocol = self.parsed.get("scheme")
        self.domain = self.parsed.get('full_domain')
        self.query = self.parsed.get("query")
        self.all_urls = self.clean_urls

    def _generate_variants(self, parsed) -> list:
        """Generate candidate URLs using ALL_URL_KEYS (scheme, www, extensions)."""
        netloc_data = parsed.get("netloc")
        base_domain = parsed.get("domain")
        ext = parsed.get("ext")
        variants = []

        for scheme in ALL_URL_KEYS["scheme"]:
            for www in ALL_URL_KEYS["netloc"]["www"]:
                for ext_cand in (ALL_URL_KEYS["netloc"]["extentions"][0] + ALL_URL_KEYS["netloc"]["extentions"][1]):
                    # skip if extension already fixed and doesn't match
                    if ext and ext != ext_cand:
                        continue
                    candidate_netloc = f"{'www.' if www else ''}{base_domain}{ext_cand or ext}"
                    candidate_url = f"{scheme}://{candidate_netloc}{parsed.get('path','')}"
                    variants.append(candidate_url)

        # Deduplicate
        seen = set()
        unique_variants = [v for v in variants if not (v in seen or seen.add(v))]
        return sorted(unique_variants, key=lambda v: (not v.startswith("https"), v))

    def get_correct_url(self, candidates=None) -> str:
        """
        Try candidates (HEAD request). 
        Return first that resolves with 200.
        """
        candidates = candidates or self.clean_urls
        for candidate in candidates:
            try:
                response = self.session.head(candidate, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    return candidate
            except requests.exceptions.RequestException as e:
                logging.info(f"Failed: {candidate} ({e})")
        return None

    # === convenience wrappers ===
    def get_domain(self) -> str:
        if not self.parsed:
            return None
        return reconstructNetLoc(self.parsed.get("netloc"))

    def is_valid_url(self, url=None):
        """Check if a URL parses into scheme+netloc."""
        url = url or self.url
        if not url:
            return False
        p = parse_url(url)
        domain=None
        scheme=None
        netloc=None
        if isinstance(p,dict):
            scheme = p.get("scheme")
            netloc = p.get("netloc", {})
            if isinstance(netloc,dict):
                domain = netloc.get("domain")
        return bool(scheme) and bool(domain or netloc)

    def make_valid(self, href, base_url=None):
        """
        Fix relative links by joining with a base URL.
        If base_url is not provided, uses self.url.
        """
        base_url = base_url or self.url
        if not base_url:
            return None
        return requests.compat.urljoin(base_url, href)


    def base_url(self):
        """Return base of current url (scheme+domain)."""
        if not self.parsed:
            return None
        scheme = self.parsed.get("scheme")
        netloc = reconstructNetLoc(self.parsed.get("netloc"))
        return f"{scheme}://{netloc}/"

    def url_basename(self):
        if not self.parsed:
            return ""
        return self.parsed.get("path", "").strip("/").split("/")[-1]
def get_url_mgr(url=None,url_mgr=None):
    return url_mgr or urlManager(url)
def get_url(url=None,url_mgr=None):
    url_mgr = get_url_mgr(url=url,url_mgr=url_mgr)
    return url_mgr.url

