# src/canonmap/connectors/mysql_connector/matching/scoring.py

from difflib import SequenceMatcher

from metaphone import doublemetaphone

try:
    import jellyfish
    _have_jaro = True
except ImportError:
    _have_jaro = False

try:
    import Levenshtein
    _have_lev = True
except ImportError:
    _have_lev = False

try:
    import jellyfish
    _have_soundex = True
except ImportError:
    _have_soundex = False

from canonmap.mapping.models import MappingWeights
from canonmap.mapping.utils.normalize import normalize


def trigram_similarity(a: str, b: str) -> float:
    def grams(s):
        return {s[i:i+3] for i in range(len(s)-2)}
    A, B = grams(a), grams(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)

def levenshtein_ratio(a: str, b: str) -> float:
    if _have_lev:
        return Levenshtein.ratio(a, b)
    return SequenceMatcher(None, a, b).ratio()

def jaro_winkler_similarity(a: str, b: str) -> float:
    if _have_jaro:
        return jellyfish.jaro_winkler_similarity(a, b)
    # fallback to levenshtein-based ratio
    return levenshtein_ratio(a, b)

def token_overlap(query: str, candidate: str) -> float:
    # Example: overlap on first/last token
    q_tokens = query.split()
    c_tokens = candidate.split()
    if not q_tokens or not c_tokens:
        return 0.0
    first = float(q_tokens[0] in c_tokens)
    last = float(q_tokens[-1] in c_tokens)
    # Weight: 30% for first, 70% for last (tune as needed)
    return 0.3 * first + 0.7 * last

def phonetic_similarity(query: str, candidate: str) -> float:
    # Compare doublemetaphone of last word
    q_tokens = query.split()
    c_tokens = candidate.split()
    if not q_tokens or not c_tokens:
        return 0.0
    q_last = q_tokens[-1]
    c_metaphones = doublemetaphone(" ".join(c_tokens))
    q_last_metaphone = doublemetaphone(q_last)[0]
    return float(q_last_metaphone and q_last_metaphone in c_metaphones)

def initialism_similarity(query: str, candidate: str) -> float:
    def initialism(s):
        return "".join(w[0].upper() for w in s.split() if w)
    return float(initialism(query) == initialism(candidate)) if query and candidate else 0.0

def soundex_similarity(query: str, candidate: str) -> float:
    """Compare Soundex codes for similarity."""
    if _have_soundex:
        return float(jellyfish.soundex(query) == jellyfish.soundex(candidate))
    # Fallback: compute simple Soundex manually
    def soundex(s):
        if not s:
            return ""
        s = s.upper()
        # Soundex rules
        codes = {'B': '1', 'F': '1', 'P': '1', 'V': '1',
                'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
                'D': '3', 'T': '3',
                'L': '4',
                'M': '5', 'N': '5',
                'R': '6'}
        
        result = s[0]
        for char in s[1:]:
            if char in codes:
                code = codes[char]
                if code != result[-1]:
                    result += code
        return (result + "000")[:4]
    
    return float(soundex(query) == soundex(candidate))

def exact_match(query: str, candidate: str) -> float:
    return float(query == candidate)

def compute_feature_vector(query: str, candidate: str) -> dict:
    """Compute all string similarity features between query and candidate."""
    query_norm = normalize(query)
    cand_norm = normalize(candidate)
    return {
        "exact": exact_match(query_norm, cand_norm),
        "levenshtein": levenshtein_ratio(query_norm, cand_norm),
        "jaro": jaro_winkler_similarity(query_norm, cand_norm),
        "token": token_overlap(query_norm, cand_norm),
        "trigram": trigram_similarity(query_norm, cand_norm),
        "phonetic": phonetic_similarity(query_norm, cand_norm),
        "soundex": soundex_similarity(query_norm, cand_norm),
        "initialism": initialism_similarity(query_norm, cand_norm),
    }

def score_candidate(query: str, candidate: str, weights: MappingWeights) -> float:
    """
    Score a candidate entity by weighted sum of features.
    Uses MappingWeights model for consistent weight configuration.
    """
    features = compute_feature_vector(query, candidate)
    
    # Calculate base score using weights from MappingWeights model
    score = (
        features["exact"] * weights.exact +
        features["levenshtein"] * weights.levenshtein +
        features["jaro"] * weights.jaro +
        features["token"] * weights.token +
        features["trigram"] * weights.trigram +
        features["phonetic"] * weights.phonetic +
        features["soundex"] * weights.soundex +
        features["initialism"] * weights.initialism
    )
    
    # Multi bonus if multiple nonzero features
    multi = sum(1 for k in ("levenshtein", "token", "phonetic", "initialism") if features[k] > 0)
    score += max(0, multi - 1) * weights.multi_bonus
    
    return score

def scorer(query: str, candidate: str, weights: MappingWeights) -> tuple[str, float]:
    return candidate, score_candidate(query, candidate, weights)
