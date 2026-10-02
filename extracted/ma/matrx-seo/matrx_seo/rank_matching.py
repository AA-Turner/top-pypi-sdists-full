from __future__ import annotations

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import BaseModel, ConfigDict, field_validator


class RankMatchTarget(BaseModel):
    model_config = ConfigDict(extra="forbid")

    canonical_domain: str
    canonical_url: str | None = None
    url_aliases: tuple[str, ...] = ()
    include_subdomains: bool = True

    @field_validator("canonical_domain")
    @classmethod
    def normalize_target_domain(cls, value: str) -> str:
        domain = canonicalize_domain(value)
        if not domain:
            raise ValueError("rank target requires a canonical domain")
        return domain


class RankMatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    matched_domain: str
    matched_url: str
    match_rule: str


def canonicalize_domain(value: str) -> str:
    candidate = value.strip()
    if not candidate:
        return ""
    parsed = urlsplit(candidate if "://" in candidate else f"//{candidate}")
    hostname = parsed.hostname or ""
    normalized = hostname.rstrip(".").lower()
    if normalized.startswith("www."):
        normalized = normalized[4:]
    return normalized.encode("idna").decode("ascii") if normalized else ""


def canonicalize_rank_url(value: str) -> str:
    candidate = value.strip()
    if not candidate:
        return ""
    parsed = urlsplit(candidate if "://" in candidate else f"https://{candidate}")
    hostname = canonicalize_domain(parsed.hostname or "")
    if not hostname:
        return ""
    port = parsed.port
    netloc = hostname if port in (None, 80, 443) else f"{hostname}:{port}"
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/") or "/"
    query = urlencode(sorted(parse_qsl(parsed.query, keep_blank_values=True)), doseq=True)
    return urlunsplit(("https", netloc, path, query, ""))


def match_rank_url(result_url: str | None, target: RankMatchTarget) -> RankMatch | None:
    if not result_url:
        return None
    matched_url = canonicalize_rank_url(result_url)
    if not matched_url:
        return None
    matched_domain = canonicalize_domain(result_url)
    target_domain = target.canonical_domain
    if matched_domain != target_domain:
        if not target.include_subdomains or not matched_domain.endswith(f".{target_domain}"):
            return None

    canonical_target = canonicalize_rank_url(target.canonical_url) if target.canonical_url else None
    if canonical_target and matched_url == canonical_target:
        rule = "page_exact"
    elif matched_url in {
        canonicalize_rank_url(alias) for alias in target.url_aliases if alias.strip()
    }:
        rule = "page_alias"
    elif matched_domain != target_domain:
        rule = "subdomain"
    else:
        rule = "domain"
    return RankMatch(
        matched_domain=matched_domain,
        matched_url=matched_url,
        match_rule=rule,
    )
