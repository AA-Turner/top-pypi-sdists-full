"""robots.txt — the ONE parser for the whole package.

Two jobs the crawler and the SEO catalogue both need and had nowhere to get:

1. **Decide** whether a URL is crawlable for a user-agent, with the wildcard
   syntax every real robots.txt uses (``*`` and ``$``). ``urllib.robotparser``
   — what ``crawler.py`` uses for polite crawling — does not implement Google's
   longest-match precedence, so it cannot answer "is this sitemap URL blocked?"
   accurately enough to score a site on it.
2. **Describe** the file structurally: which agents are addressed, which
   declare a blanket ``Disallow: /``, which ``Sitemap:`` locations it points at,
   and which lines are malformed. That description is the evidence the
   ``robots_txt_health`` catalogue row is scored from.

Pure logic — no network, no DB. The fetch lives in
``web_crawl/site_probe.py``; the verdict lives in ``web_crawl/analysis.py``.

Matching follows Google's Robots Exclusion Protocol (RFC 9309 + Google's
documented extensions): the most specific (longest) matching rule wins, and
``Allow`` beats ``Disallow`` on an exact tie.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import unquote, urlsplit

# The agents whose blanket block is a site-wide catastrophe rather than a
# deliberate exclusion of one scraper. `*` counts: it addresses everyone.
MAJOR_SEARCH_ENGINE_AGENTS: frozenset[str] = frozenset(
    {"*", "googlebot", "bingbot", "duckduckbot", "slurp", "yandex"}
)

# Google stops reading a robots.txt after 500 KiB. Anything past that is not
# enforced by the crawler that matters, so it is not scored either.
ROBOTS_MAX_BYTES = 500_000

# Directives that are not in the standard but are widely emitted and harmless.
# Flagging these as syntax errors would fail half the web for no reason —
# `robots_txt_health` scores MALFORMED lines, not unfashionable ones.
_TOLERATED_FIELDS: frozenset[str] = frozenset(
    {
        "crawl-delay",
        "host",
        "clean-param",
        "request-rate",
        "visit-time",
        "noindex",
        "cache-delay",
    }
)
_GROUP_FIELDS: frozenset[str] = frozenset({"allow", "disallow"})
#: Group-scoped directives that state a PACING preference. Parsed, not skipped —
#: they are the only machine-readable rate a site publishes about itself.
_PACING_FIELDS: frozenset[str] = frozenset({"crawl-delay", "request-rate"})

#: A site asking for a longer gap than this is either misconfigured or means
#: "do not crawl me"; honouring it literally would turn a 500-page crawl into a
#: multi-day job. The value is still REPORTED so the clamp is never silent —
#: see ``host_pacing.HostPacingPlan.notes``.
MAX_HONOURED_CRAWL_DELAY_SECONDS = 60.0


@dataclass(frozen=True)
class RobotsRule:
    """One ``Allow:``/``Disallow:`` line, with its compiled path pattern."""

    field_name: str  # "allow" | "disallow"
    value: str
    pattern: re.Pattern[str]
    line_number: int

    @property
    def specificity(self) -> int:
        """Google's precedence measure: the length of the path pattern."""
        return len(self.value)

    @property
    def directive(self) -> str:
        """The source directive in the same vocabulary as robots.txt."""
        return f"{self.field_name.title()}: {self.value}"


@dataclass(frozen=True)
class RobotsDecision:
    """One crawl verdict with the exact source rule that produced it."""

    allowed: bool
    matched_rule: RobotsRule | None


@dataclass
class RobotsGroup:
    """One ``User-agent:`` block (several agents may share one rule set)."""

    user_agents: list[str] = field(default_factory=list)
    rules: list[RobotsRule] = field(default_factory=list)
    # ``Crawl-delay: N`` — seconds the site asks a crawler to wait between
    # requests. Non-standard but very widely emitted, and the ONE place a site
    # states a pacing preference in machine-readable form. Captured here rather
    # than skipped as decoration because the crawler honours it as an upper
    # bound (see ``host_pacing.py``).
    crawl_delay: float | None = None
    # ``Request-rate: <docs>/<seconds>[s|m|h]`` — the older, rarer twin of
    # Crawl-delay, stated as a rate instead of a gap. Normalised to seconds
    # per request so both directives answer the same question.
    request_rate_seconds: float | None = None

    @property
    def min_seconds_between_requests(self) -> float | None:
        """The slowest pacing this group asks for, across both directives."""
        stated = [v for v in (self.crawl_delay, self.request_rate_seconds) if v is not None]
        return max(stated) if stated else None

    def addresses(self, user_agent: str) -> bool:
        return user_agent.lower() in {a.lower() for a in self.user_agents}

    def blocks_everything(self) -> bool:
        """``Disallow: /`` with nothing carving an exception back out."""
        disallow_root = any(r.field_name == "disallow" and r.value == "/" for r in self.rules)
        return disallow_root and not any(r.field_name == "allow" for r in self.rules)


@dataclass
class RobotsDocument:
    """A parsed robots.txt. Every consumer in the package reads this shape."""

    groups: list[RobotsGroup] = field(default_factory=list)
    sitemaps: list[str] = field(default_factory=list)
    # One human-readable sentence per malformed line, already carrying its
    # line number — this text is shown to a non-technical user.
    syntax_errors: list[str] = field(default_factory=list)
    truncated: bool = False

    @property
    def user_agents(self) -> list[str]:
        seen: list[str] = []
        for group in self.groups:
            for agent in group.user_agents:
                if agent not in seen:
                    seen.append(agent)
        return seen

    def group_for(self, user_agent: str) -> RobotsGroup | None:
        """The group that governs ``user_agent`` — most specific name wins.

        Google matches on the longest addressed agent name that is a prefix of
        the crawler's own name, falling back to the ``*`` group.
        """

        target = user_agent.lower()
        best: RobotsGroup | None = None
        best_len = -1
        wildcard: RobotsGroup | None = None
        for group in self.groups:
            for agent in group.user_agents:
                name = agent.lower()
                if name == "*":
                    if wildcard is None:
                        wildcard = group
                    continue
                if target.startswith(name) and len(name) > best_len:
                    best, best_len = group, len(name)
        return best or wildcard

    def decision_for(self, url_or_path: str, user_agent: str = "*") -> RobotsDecision:
        """Explain whether ``user_agent`` may fetch this path.

        Fail-OPEN by construction: robots.txt is a deny list, so anything the
        file does not address is crawlable. A check must never invent a block.
        """

        group = self.group_for(user_agent)
        if group is None:
            return RobotsDecision(allowed=True, matched_rule=None)
        path = _path_of(url_or_path)
        matches: list[RobotsRule] = []
        for rule in group.rules:
            # `Disallow:` with an empty value is the documented way to say
            # "nothing is blocked" — it matches no path at all.
            if not rule.value or not rule.pattern.match(path):
                continue
            matches.append(rule)
        if not matches:
            return RobotsDecision(allowed=True, matched_rule=None)
        winner = max(
            matches,
            key=lambda rule: (rule.specificity, rule.field_name == "allow"),
        )
        return RobotsDecision(allowed=winner.field_name == "allow", matched_rule=winner)

    def is_allowed(self, url_or_path: str, user_agent: str = "*") -> bool:
        """Whether ``user_agent`` may fetch this path. Unknown → allowed."""
        return self.decision_for(url_or_path, user_agent).allowed

    def crawl_delay_for(self, user_agent: str = "*") -> float | None:
        """Seconds this file asks ``user_agent`` to wait between requests.

        Same group precedence as :meth:`decision_for` — the longest addressed
        agent name that prefixes ours wins, else the ``*`` group. ``None`` means
        the file states no pacing preference, which is NOT the same as "go as
        fast as you like": it hands the question to the ramp.
        """

        group = self.group_for(user_agent)
        return group.min_seconds_between_requests if group is not None else None

    def blanket_disallow_agents(self) -> list[str]:
        """Major-search-engine agents this file blocks from the whole site."""

        blocked: list[str] = []
        for group in self.groups:
            if not group.blocks_everything():
                continue
            for agent in group.user_agents:
                if agent.lower() in MAJOR_SEARCH_ENGINE_AGENTS and agent not in blocked:
                    blocked.append(agent)
        return blocked


def _path_of(url_or_path: str) -> str:
    """The path+query a robots rule matches against."""

    if "://" in url_or_path:
        parts = urlsplit(url_or_path)
        path = parts.path or "/"
        if parts.query:
            path = f"{path}?{parts.query}"
    else:
        path = url_or_path or "/"
    if not path.startswith("/"):
        path = "/" + path
    # Percent-encoding is not significant to matching; compare decoded forms so
    # `/private%20area` and `/private area` are the same path.
    return unquote(path)


def _compile_pattern(value: str) -> re.Pattern[str]:
    """A robots path value as an anchored regex (``*`` glob, ``$`` end)."""

    anchored = value.endswith("$")
    body = value[:-1] if anchored else value
    out = ["^"]
    for char in body:
        out.append(".*" if char == "*" else re.escape(char))
    if anchored:
        out.append("$")
    return re.compile("".join(out))


def _parse_crawl_delay(value: str) -> float | None:
    """``Crawl-delay: 10`` → ``10.0``. Rejects anything not a positive number."""

    try:
        seconds = float(value.strip().replace(",", "."))
    except (TypeError, ValueError):
        return None
    return seconds if seconds > 0 else None


_REQUEST_RATE = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*([smh])?\s*$", re.I)
_RATE_UNIT_SECONDS = {"s": 1.0, "m": 60.0, "h": 3600.0}


def _parse_request_rate(value: str) -> float | None:
    """``Request-rate: 1/10s`` → ``10.0`` seconds per request.

    The unit is optional and defaults to seconds, which is how the directive is
    written in practice. A rate of zero documents nothing and is rejected rather
    than silently becoming "unlimited".
    """

    match = _REQUEST_RATE.match(value or "")
    if match is None:
        return None
    documents = int(match.group(1))
    window = int(match.group(2)) * _RATE_UNIT_SECONDS[(match.group(3) or "s").lower()]
    if documents <= 0 or window <= 0:
        return None
    return window / documents


def parse_robots_txt(text: str) -> RobotsDocument:
    """Parse robots.txt content. Never raises — malformed lines are REPORTED.

    A parser that threw would turn "this site's robots.txt is broken" (the
    thing being measured) into "the check crashed".
    """

    doc = RobotsDocument()
    encoded = text.encode("utf-8", errors="replace")
    if len(encoded) > ROBOTS_MAX_BYTES:
        text = encoded[:ROBOTS_MAX_BYTES].decode("utf-8", errors="ignore")
        doc.truncated = True

    current: RobotsGroup | None = None
    # A `User-agent:` line after rules starts a NEW group; consecutive
    # user-agent lines join the same one.
    accepting_agents = False
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            doc.syntax_errors.append(f"line {number}: {line!r} is not a `field: value` directive")
            continue
        name, _, value = line.partition(":")
        name = name.strip().lower()
        value = value.strip()
        if not name:
            doc.syntax_errors.append(f"line {number}: directive name is empty")
            continue

        if name == "user-agent":
            if not value:
                doc.syntax_errors.append(f"line {number}: `User-agent:` has no value")
                continue
            if current is None or not accepting_agents:
                current = RobotsGroup()
                doc.groups.append(current)
                accepting_agents = True
            current.user_agents.append(value)
            continue

        if name == "sitemap":
            # `Sitemap:` is file-scoped, not group-scoped — it may legally
            # appear anywhere, including before any User-agent line.
            if value:
                doc.sitemaps.append(value)
            else:
                doc.syntax_errors.append(f"line {number}: `Sitemap:` has no value")
            continue

        if name in _GROUP_FIELDS:
            if current is None:
                doc.syntax_errors.append(
                    f"line {number}: `{name.title()}:` appears before any `User-agent:` line, "
                    "so no crawler is told to obey it"
                )
                continue
            accepting_agents = False
            current.rules.append(
                RobotsRule(
                    field_name=name,
                    value=value,
                    pattern=_compile_pattern(value),
                    line_number=number,
                )
            )
            continue

        if name in _PACING_FIELDS:
            # `str.title()` capitalises after the hyphen ("Crawl-Delay"), which
            # is not how the directive is spelled in any robots.txt. The error
            # text is read by a non-technical user comparing it to their file.
            display = "Crawl-delay" if name == "crawl-delay" else "Request-rate"
            # Pacing directives are group-scoped like Allow/Disallow, so one
            # before any User-agent line addresses nobody — same reporting as a
            # stray rule rather than a silent drop.
            accepting_agents = False
            if current is None:
                doc.syntax_errors.append(
                    f"line {number}: `{display}:` appears before any `User-agent:` line, "
                    "so no crawler is told to obey it"
                )
                continue
            seconds = (
                _parse_crawl_delay(value) if name == "crawl-delay" else _parse_request_rate(value)
            )
            if seconds is None:
                doc.syntax_errors.append(
                    f"line {number}: `{display}: {value}` is not a value a crawler can act on"
                )
                continue
            if name == "crawl-delay":
                current.crawl_delay = seconds
            else:
                current.request_rate_seconds = seconds
            continue

        if name in _TOLERATED_FIELDS:
            accepting_agents = False
            continue

        doc.syntax_errors.append(f"line {number}: `{name}` is not a robots.txt directive")

    return doc


__all__ = [
    "MAJOR_SEARCH_ENGINE_AGENTS",
    "MAX_HONOURED_CRAWL_DELAY_SECONDS",
    "ROBOTS_MAX_BYTES",
    "RobotsDocument",
    "RobotsDecision",
    "RobotsGroup",
    "RobotsRule",
    "parse_robots_txt",
]
