from ...imports import *
from ..domains import tokenize_domain

def _abbr(tokens):
    return "".join(t[0].upper() for t in tokens if t)

def title_variants_from_domain(domain: str):
    tokens = tokenize_domain(domain)
    caps = [capitalize(t) for t in tokens]
    abbr = _abbr(tokens)

    domain_lower = domain.lower().strip()
    domain_root = re.sub(r"\.[a-z0-9]{2,6}$", "", domain_lower)

    variants = [
        domain_lower,
        " ".join(caps),
        domain_root,
        "".join(caps),
        *caps,
        abbr
    ]
    variants.append(" ".join(caps))
    variants.append("".join(caps))
    if len(caps) > 1:
        variants.append(" ".join(caps[1:]))
        variants.append("".join(caps[1:]))

    if len(caps) > 2:
        variants.append(" ".join(caps[2:]))
        variants.append("".join(caps[2:]))

    cleaned = []
    used = set()
    for v in variants:
        if v and v not in used:
            cleaned.append(v)
            used.add(v)

    return sorted(cleaned, key=len, reverse=True)
