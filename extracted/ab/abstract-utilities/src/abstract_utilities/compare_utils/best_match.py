from __future__ import annotations
from typing import Any, Iterable, Iterator, Tuple, Union, Dict, List, Optional
import re
from difflib import SequenceMatcher

JSONLike = Union[dict, list, tuple, set, str, int, float, bool, None]
PathType = Tuple[Union[str, int], ...]

def iter_values(obj: JSONLike, path: PathType = ()) -> Iterator[Tuple[PathType, Any]]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from iter_values(v, path + (k,))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            yield from iter_values(v, path + (i,))
    elif isinstance(obj, set):
        for v in obj:
            yield from iter_values(v, path + ('<setitem>',))
    else:
        yield path, obj

def _norm(s: str, case_insensitive: bool) -> str:
    return s.lower() if case_insensitive else s

def _word_boundary_regex(term: str, case_insensitive: bool) -> re.Pattern:
    flags = re.IGNORECASE if case_insensitive else 0
    # word boundary around the whole term; escape term for literal
    return re.compile(rf"\b{re.escape(term)}\b", flags)

def _score_string(
    value: str,
    terms: Iterable[str],
    *,
    case_insensitive: bool = True,
    min_ratio: float = 0.6,
) -> Tuple[float, Dict[str, float]]:
    """
    Score a *string* against the list of terms. Returns (score, per_term_scores).
    Weights:
      exact=+3, word-boundary=+2, substring=+1, fuzzy=+0.5*ratio (if ratio>=min_ratio).
      +0.2 bonus per extra unique term matched (beyond the first).
    """
    if not isinstance(value, str):
        return 0.0, {}
    v = _norm(value, case_insensitive)
    per_term: Dict[str, float] = {}
    matched_terms = 0

    for term in terms:
        t = _norm(term, case_insensitive)
        term_score = 0.0

        if v == t:
            term_score = max(term_score, 3.0)

        # word boundary
        if _word_boundary_regex(term, case_insensitive).search(value):
            term_score = max(term_score, 2.0)

        # substring
        if t in v:
            term_score = max(term_score, 1.0)

        # fuzzy similarity
        ratio = SequenceMatcher(None, v, t).ratio()  # 0..1
        if ratio >= min_ratio:
            term_score = max(term_score, 0.5 * ratio)

        if term_score > 0:
            matched_terms += 1
            per_term[term] = term_score

    # Bonus for covering more than one term
    bonus = 0.2 * max(0, matched_terms - 1)
    total = sum(per_term.values()) + bonus
    return total, per_term

def best_match(
    obj: JSONLike,
    *,
    terms: Iterable[str],
    case_insensitive: bool = True,
    min_ratio: float = 0.6,
    key_weight: Dict[str, float] | None = None,  # e.g. {'window_title': 1.5}
    coerce_non_strings: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    Return the single best leaf string:
    { 'value': str, 'path': PathType, 'score': float, 'per_term': {term:score} }
    """
    key_weight = key_weight or {}
    best: Optional[Dict[str, Any]] = None

    for path, val in iter_values(obj):
        s = val
        if not isinstance(s, str):
            if coerce_non_strings:
                s = str(val)
            else:
                continue

        score, per_term = _score_string(s, terms, case_insensitive=case_insensitive, min_ratio=min_ratio)
        if score <= 0:
            continue

        # Apply path-based weight if any path segment matches a key in key_weight
        weight = 1.0
        for seg in path:
            if isinstance(seg, str) and seg in key_weight:
                weight *= key_weight[seg]
        weighted = score * weight

        cand = {'value': s, 'path': path, 'score': weighted, 'per_term': per_term}
        if best is None or weighted > best['score']:
            best = cand
        # Optional tie-breakers (prefer more terms matched, then shorter value)
        elif best is not None and abs(weighted - best['score']) < 1e-9:
            if len(per_term) > len(best['per_term']):
                best = cand
            elif len(per_term) == len(best['per_term']) and len(s) < len(best['value']):
                best = cand

    return best

def top_k_matches(
    obj: JSONLike,
    *,
    terms: Iterable[str],
    k: int = 5,
    **kwargs
) -> List[Dict[str, Any]]:
    """Return top-k matches sorted by score desc."""
    items: List[Dict[str, Any]] = []
    for path, val in iter_values(obj):
        s = val if isinstance(val, str) else (str(val) if kwargs.get('coerce_non_strings') else None)
        if s is None:
            continue
        score, per_term = _score_string(s, terms,
                                        case_insensitive=kwargs.get('case_insensitive', True),
                                        min_ratio=kwargs.get('min_ratio', 0.6))
        if score <= 0:
            continue
        weight = 1.0
        for seg in path:
            if isinstance(seg, str) and kwargs.get('key_weight', {}).get(seg):
                weight *= kwargs['key_weight'][seg]
        items.append({'value': s, 'path': path, 'score': score * weight, 'per_term': per_term})

    items.sort(key=lambda d: d['score'], reverse=True)
    return items[:k]
